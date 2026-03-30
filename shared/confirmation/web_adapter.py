"""方案二：Web Dashboard 确认 — 支持在线编辑产出物"""
import json
import os
import time
from .base import (
    ConfirmationAdapter, ConfirmationRequest, ConfirmationResult, ArtifactEdit,
    snapshot_artifacts, detect_artifact_edits, save_edit_record,
)


class WebConfirmationAdapter(ConfirmationAdapter):
    """
    Web Dashboard 确认。PO 在浏览器中查看产出物、在线编辑、点击按钮操作。
    配套 FastAPI 应用见 shared/confirmation/web_dashboard.py
    """

    def __init__(self, project_root: str, port: int = 8080):
        self.project_root = project_root
        self.port = port

    def _pending_path(self, sprint_id: str, node_id: str) -> str:
        d = os.path.join(self.project_root, "sprints", sprint_id, "confirmations", "pending")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, f"{node_id}.json")

    def _resolved_path(self, sprint_id: str, node_id: str) -> str:
        return os.path.join(self.project_root, "sprints", sprint_id,
                            "confirmations", "resolved", f"{node_id}.json")

    def request_confirmation(self, req: ConfirmationRequest) -> ConfirmationResult:
        before_snapshot = snapshot_artifacts(req.artifact_paths)
        pending_file = self._pending_path(req.sprint_id, req.node_id)
        data = {
            "node_id": req.node_id, "phase": req.phase, "title": req.title,
            "level": req.level.value, "agent_name": req.agent_name,
            "sprint_id": req.sprint_id, "summary": req.format_summary(),
            "key_decisions": req.key_decisions, "confidence": req.confidence.value,
            "artifact_paths": req.artifact_paths,
            "artifact_snapshot": before_snapshot, "status": "pending",
        }
        with open(pending_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        url = f"http://localhost:{self.port}/confirm/{req.node_id}?sprint={req.sprint_id}"
        print(f"\n🌐 请在浏览器中确认: {url}")

        resolved_file = self._resolved_path(req.sprint_id, req.node_id)
        timeout = req.timeout_hours * 3600
        elapsed = 0
        while elapsed < timeout:
            if os.path.exists(resolved_file):
                with open(resolved_file, "r", encoding="utf-8") as f:
                    result = json.load(f)
                edits = detect_artifact_edits(before_snapshot, req.artifact_paths)
                if edits:
                    save_edit_record(req.sprint_id, req.node_id, edits, self.project_root)
                return ConfirmationResult(
                    decision=result["decision"], feedback=result.get("feedback", ""),
                    artifact_edits=edits)
            time.sleep(3)
            elapsed += 3
        return ConfirmationResult(decision="defer", feedback="确认超时")

    def send_async_notification(self, req: ConfirmationRequest) -> str:
        before_snapshot = snapshot_artifacts(req.artifact_paths)
        pending_file = self._pending_path(req.sprint_id, req.node_id)
        data = {"node_id": req.node_id, "title": req.title, "level": "async",
                "summary": req.format_summary(), "artifact_paths": req.artifact_paths,
                "artifact_snapshot": before_snapshot, "status": "pending_async",
                "sprint_id": req.sprint_id}
        with open(pending_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"{req.sprint_id}/{req.node_id}"

    def check_async_result(self, confirmation_id: str) -> ConfirmationResult | None:
        sprint_id, node_id = confirmation_id.split("/")
        resolved_file = self._resolved_path(sprint_id, node_id)
        if os.path.exists(resolved_file):
            with open(resolved_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            edits = [ArtifactEdit(file_path=e["file"], original_hash=e.get("original_hash", ""))
                     for e in data.get("artifact_edits", [])]
            return ConfirmationResult(decision=data["decision"],
                                      feedback=data.get("feedback", ""), artifact_edits=edits)
        return None
