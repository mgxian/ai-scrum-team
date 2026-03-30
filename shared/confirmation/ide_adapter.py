"""方案一：IDE（Kiro）Chat 交互确认 — 支持 PO 直接编辑产出物"""
import json
import os
import time
from .base import (
    ConfirmationAdapter, ConfirmationRequest, ConfirmationResult, ArtifactEdit,
    snapshot_artifacts, detect_artifact_edits, save_edit_record,
)


class IDEConfirmationAdapter(ConfirmationAdapter):
    """
    通过 Kiro IDE Chat 确认。PO 点击 #File 链接编辑产出物，
    回复 approve 后系统自动检测 diff。
    """

    def __init__(self, project_root: str):
        self.project_root = project_root

    def _pending_path(self, sprint_id: str, node_id: str) -> str:
        d = os.path.join(self.project_root, "sprints", sprint_id, "confirmations", "pending")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, f"{node_id}.json")

    def _resolved_path(self, sprint_id: str, node_id: str) -> str:
        d = os.path.join(self.project_root, "sprints", sprint_id, "confirmations", "resolved")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, f"{node_id}.json")

    def request_confirmation(self, req: ConfirmationRequest) -> ConfirmationResult:
        before_snapshot = snapshot_artifacts(req.artifact_paths)

        pending_file = self._pending_path(req.sprint_id, req.node_id)
        request_data = {
            "node_id": req.node_id, "phase": req.phase, "title": req.title,
            "level": req.level.value, "agent_name": req.agent_name,
            "sprint_id": req.sprint_id, "story_id": req.story_id,
            "summary": req.format_summary(), "key_decisions": req.key_decisions,
            "risk_notes": req.risk_notes, "confidence": req.confidence.value,
            "artifact_paths": req.artifact_paths,
            "artifact_snapshot": before_snapshot,
            "status": "pending", "editable": True,
        }
        with open(pending_file, "w", encoding="utf-8") as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)

        resolved_file = self._resolved_path(req.sprint_id, req.node_id)
        timeout = req.timeout_hours * 3600
        elapsed = 0
        while elapsed < timeout:
            if os.path.exists(resolved_file):
                with open(resolved_file, "r", encoding="utf-8") as f:
                    result_data = json.load(f)
                edits = detect_artifact_edits(before_snapshot, req.artifact_paths)
                decision = result_data.get("decision", "approve")
                if edits and decision in ("approve", "approve_with_edits"):
                    decision = "approve_with_edits"
                    save_edit_record(req.sprint_id, req.node_id, edits, self.project_root)
                return ConfirmationResult(
                    decision=decision, feedback=result_data.get("feedback", ""),
                    rejected_items=result_data.get("rejected_items", []),
                    artifact_edits=edits)
            time.sleep(5)
            elapsed += 5
        return ConfirmationResult(decision="defer", feedback="确认超时")

    def send_async_notification(self, req: ConfirmationRequest) -> str:
        before_snapshot = snapshot_artifacts(req.artifact_paths)
        pending_file = self._pending_path(req.sprint_id, req.node_id)
        data = {"node_id": req.node_id, "title": req.title, "level": "async",
                "summary": req.format_summary(), "artifact_paths": req.artifact_paths,
                "artifact_snapshot": before_snapshot, "status": "pending_async", "editable": True}
        with open(pending_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"{req.sprint_id}/{req.node_id}"

    def check_async_result(self, confirmation_id: str) -> ConfirmationResult | None:
        sprint_id, node_id = confirmation_id.split("/")
        resolved_file = self._resolved_path(sprint_id, node_id)
        if os.path.exists(resolved_file):
            with open(resolved_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            edits = [ArtifactEdit(file_path=e["file"], edit_summary=e.get("summary", ""))
                     for e in data.get("artifact_edits", [])]
            return ConfirmationResult(decision=data["decision"],
                                      feedback=data.get("feedback", ""), artifact_edits=edits)
        return None
