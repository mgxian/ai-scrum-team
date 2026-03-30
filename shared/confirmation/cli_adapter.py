"""方案零：CLI 终端确认 — 支持 PO 手动编辑产出物后确认"""
from .base import (
    ConfirmationAdapter, ConfirmationRequest, ConfirmationResult,
    snapshot_artifacts, detect_artifact_edits, save_edit_record,
)


class CLIConfirmationAdapter(ConfirmationAdapter):
    """命令行终端交互确认。PO 可先编辑文件，再输入 'e' 确认。"""

    def __init__(self, project_root: str = "."):
        self.project_root = project_root

    def request_confirmation(self, req: ConfirmationRequest) -> ConfirmationResult:
        before_snapshot = snapshot_artifacts(req.artifact_paths)

        print(f"\n{'─' * 50}")
        print(req.format_summary())
        print(f"{'─' * 50}")

        artifacts = req.load_artifacts()
        if artifacts:
            print(f"\n📄 产出物（共 {len(artifacts)} 个文件）:")
            for name, content in artifacts.items():
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"\n  [{name}]\n  {preview}")

        print(f"\n请输入决策:")
        print(f"  [y] 原样通过  [e] 修改后通过  [n] 驳回  [p] 部分通过  [d] 暂缓")
        decision = input("> ").strip().lower()

        if decision == "e":
            edits = detect_artifact_edits(before_snapshot, req.artifact_paths)
            if edits:
                print(f"\n✏️ 检测到 {len(edits)} 个文件被修改:")
                for e in edits:
                    print(f"  - {e.file_path}")
                save_edit_record(req.sprint_id, req.node_id, edits, self.project_root)
                feedback = input("修改说明（可选）: ").strip()
                return ConfirmationResult(decision="approve_with_edits",
                                          feedback=feedback, artifact_edits=edits)
            else:
                print("⚠ 未检测到文件修改，按原样通过处理")
                return ConfirmationResult(decision="approve")
        elif decision == "n":
            return ConfirmationResult(decision="reject", feedback=input("驳回原因: ").strip())
        elif decision == "p":
            return ConfirmationResult(decision="partial", feedback=input("说明: ").strip())
        elif decision == "d":
            return ConfirmationResult(decision="defer")
        return ConfirmationResult(decision="approve")

    def send_async_notification(self, req: ConfirmationRequest) -> str:
        print(f"\n📬 异步确认: {req.title}（{req.timeout_hours}h 内审阅）")
        return f"ASYNC-{req.node_id}-{req.sprint_id}"

    def check_async_result(self, confirmation_id: str) -> ConfirmationResult | None:
        print(f"\n检查异步确认 {confirmation_id}? [y/n/skip]")
        resp = input("> ").strip().lower()
        if resp == "y":
            return ConfirmationResult(decision="approve")
        elif resp == "n":
            return ConfirmationResult(decision="reject", feedback=input("原因: ").strip())
        return None
