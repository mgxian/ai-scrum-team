"""方案三：Git PR/Issue 确认 — 支持通过 PR 修改产出物"""
import os
import time
import subprocess
from .base import (
    ConfirmationAdapter, ConfirmationRequest, ConfirmationResult, ArtifactEdit,
)

try:
    import requests as http_requests
except ImportError:
    http_requests = None  # type: ignore


class GitConfirmationAdapter(ConfirmationAdapter):
    """GitHub PR/Issue 确认。PR 模式下 PO 可在 Files Changed 中直接编辑。"""

    def __init__(self, repo: str, token: str, assignee: str = "",
                 labels: list[str] = None, use_pr_mode: bool = True,
                 project_root: str = "."):
        self.repo = repo
        self.token = token
        self.assignee = assignee
        self.labels = labels or ["po-confirmation"]
        self.use_pr_mode = use_pr_mode
        self.project_root = project_root
        self.api_base = f"https://api.github.com/repos/{repo}"
        self.headers = {"Authorization": f"token {token}",
                        "Accept": "application/vnd.github.v3+json"}

    def _create_confirm_branch(self, req: ConfirmationRequest) -> str:
        branch = f"confirm/{req.node_id}-{req.sprint_id}"
        cwd = self.project_root
        subprocess.run(["git", "checkout", "-b", branch], cwd=cwd, capture_output=True)
        for p in req.artifact_paths:
            subprocess.run(["git", "add", p], cwd=cwd, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"[AI] {req.node_id}: {req.title}"],
                        cwd=cwd, capture_output=True)
        subprocess.run(["git", "push", "origin", branch], cwd=cwd, capture_output=True)
        subprocess.run(["git", "checkout", "main"], cwd=cwd, capture_output=True)
        return branch

    def _create_pr(self, req: ConfirmationRequest, branch: str) -> int:
        emoji = {"blocking": "🔴", "async": "🟡", "auto": "🟢"}
        body = f"## {emoji.get(req.level.value, '')} {req.title}\n\n"
        body += f"节点: `{req.node_id}` | 阶段: {req.phase} | 置信度: {req.confidence.value}\n\n"
        if req.key_decisions:
            body += "### 关键决策点\n" + "".join(f"- {d}\n" for d in req.key_decisions)
        if req.risk_notes:
            body += f"\n### ⚠️ 风险\n{req.risk_notes}\n"
        body += "\n---\n### 操作\n1. **Files Changed** 查看产出物\n"
        body += "2. 点 ✏️ 直接编辑，commit 到本分支\n"
        body += "3. **Approve** = 通过(自动merge)，**Request Changes** = 驳回\n"
        payload = {"title": f"[{req.node_id}] {req.title}", "body": body,
                   "head": branch, "base": "main"}
        resp = http_requests.post(f"{self.api_base}/pulls", headers=self.headers, json=payload)
        resp.raise_for_status()
        pr = resp.json()["number"]
        if self.assignee:
            http_requests.post(f"{self.api_base}/pulls/{pr}/requested_reviewers",
                               headers=self.headers, json={"reviewers": [self.assignee]})
        return pr

    def _detect_pr_edits(self, pr_number: int) -> list[ArtifactEdit]:
        resp = http_requests.get(f"{self.api_base}/pulls/{pr_number}/commits",
                                 headers=self.headers)
        resp.raise_for_status()
        edits = []
        for commit in resp.json():
            author = (commit.get("author") or {}).get("login", "")
            if author == self.assignee:
                detail = http_requests.get(f"{self.api_base}/commits/{commit['sha']}",
                                           headers=self.headers)
                detail.raise_for_status()
                for f in detail.json().get("files", []):
                    edits.append(ArtifactEdit(file_path=f["filename"],
                                              edit_summary=commit["commit"]["message"],
                                              edited_by=author))
        return edits

    def _poll_pr(self, pr: int, timeout: float) -> ConfirmationResult | None:
        elapsed = 0
        while elapsed < timeout:
            resp = http_requests.get(f"{self.api_base}/pulls/{pr}/reviews",
                                     headers=self.headers)
            resp.raise_for_status()
            for r in resp.json():
                if self.assignee and r["user"]["login"] != self.assignee:
                    continue
                if r["state"] == "APPROVED":
                    edits = self._detect_pr_edits(pr)
                    http_requests.put(f"{self.api_base}/pulls/{pr}/merge",
                                      headers=self.headers, json={"merge_method": "squash"})
                    return ConfirmationResult(
                        decision="approve_with_edits" if edits else "approve",
                        artifact_edits=edits)
                elif r["state"] == "CHANGES_REQUESTED":
                    http_requests.patch(f"{self.api_base}/pulls/{pr}",
                                        headers=self.headers, json={"state": "closed"})
                    return ConfirmationResult(decision="reject", feedback=r.get("body", ""))
            time.sleep(30)
            elapsed += 30
        return None

    def _create_issue(self, req: ConfirmationRequest) -> int:
        body = f"## {req.title}\n\n节点: `{req.node_id}` | 级别: {req.level.value}\n\n"
        if req.artifact_paths:
            body += "### 产出物\n"
            for p in req.artifact_paths:
                rel = p.replace("\\", "/")
                body += f"- [{os.path.basename(p)}](https://github.com/{self.repo}/blob/main/{rel})\n"
        body += "\n---\n回复 `approve` / `reject: 原因` / `defer`\n"
        payload = {"title": f"[{req.node_id}] {req.title}", "body": body, "labels": self.labels}
        if self.assignee:
            payload["assignees"] = [self.assignee]
        resp = http_requests.post(f"{self.api_base}/issues", headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()["number"]

    def _poll_issue(self, num: int, timeout: float) -> ConfirmationResult | None:
        elapsed = 0
        while elapsed < timeout:
            resp = http_requests.get(f"{self.api_base}/issues/{num}/comments",
                                     headers=self.headers)
            resp.raise_for_status()
            for c in resp.json():
                b = c["body"].strip().lower()
                if self.assignee and c["user"]["login"] != self.assignee:
                    continue
                if b.startswith("approve"):
                    return ConfirmationResult(decision="approve")
                if b.startswith("reject"):
                    return ConfirmationResult(decision="reject", feedback=b[7:].strip())
                if b.startswith("defer"):
                    return ConfirmationResult(decision="defer")
            time.sleep(30)
            elapsed += 30
        return None

    def request_confirmation(self, req: ConfirmationRequest) -> ConfirmationResult:
        if self.use_pr_mode:
            branch = self._create_confirm_branch(req)
            pr = self._create_pr(req, branch)
            print(f"\n📋 PR: https://github.com/{self.repo}/pull/{pr}")
            result = self._poll_pr(pr, req.timeout_hours * 3600)
        else:
            num = self._create_issue(req)
            print(f"\n📋 Issue: https://github.com/{self.repo}/issues/{num}")
            result = self._poll_issue(num, req.timeout_hours * 3600)
        return result or ConfirmationResult(decision="defer", feedback="确认超时")

    def send_async_notification(self, req: ConfirmationRequest) -> str:
        if self.use_pr_mode:
            branch = self._create_confirm_branch(req)
            pr = self._create_pr(req, branch)
            return f"{self.repo}#PR{pr}"
        num = self._create_issue(req)
        return f"{self.repo}#{num}"

    def check_async_result(self, cid: str) -> ConfirmationResult | None:
        ref = cid.split("#")[1]
        if ref.startswith("PR"):
            pr = int(ref[2:])
            resp = http_requests.get(f"{self.api_base}/pulls/{pr}/reviews",
                                     headers=self.headers)
            resp.raise_for_status()
            for r in resp.json():
                if self.assignee and r["user"]["login"] != self.assignee:
                    continue
                if r["state"] == "APPROVED":
                    edits = self._detect_pr_edits(pr)
                    return ConfirmationResult(
                        decision="approve_with_edits" if edits else "approve",
                        artifact_edits=edits)
                if r["state"] == "CHANGES_REQUESTED":
                    return ConfirmationResult(decision="reject", feedback=r.get("body", ""))
        else:
            return self._poll_issue(int(ref), timeout=0)
        return None