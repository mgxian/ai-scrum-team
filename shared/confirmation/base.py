"""确认交互的基类和数据模型 — 框架无关，纯 Python"""
from __future__ import annotations

import os
import glob
import hashlib
import difflib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Literal


class ConfirmLevel(str, Enum):
    BLOCKING = "blocking"
    ASYNC = "async"
    AUTO = "auto"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ConfirmationRequest:
    """确认请求 — Flow Agent 发给 PO 的结构化摘要"""
    node_id: str
    phase: str
    title: str
    level: ConfirmLevel
    agent_name: str
    sprint_id: str
    story_id: str = ""
    key_decisions: list[str] = field(default_factory=list)
    change_scope: str = ""
    risk_notes: str = ""
    confidence: Confidence = Confidence.MEDIUM
    artifact_paths: list[str] = field(default_factory=list)
    timeout_hours: float = 8.0

    def load_artifacts(self) -> dict[str, str]:
        contents = {}
        for path in self.artifact_paths:
            if os.path.isdir(path):
                for f in glob.glob(os.path.join(path, "*.md")):
                    with open(f, "r", encoding="utf-8") as fh:
                        contents[os.path.basename(f)] = fh.read()
            elif os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as fh:
                    contents[os.path.basename(path)] = fh.read()
        return contents

    def format_summary(self) -> str:
        lines = [
            f"【确认请求】{self.title}",
            f"节点: {self.node_id} | 阶段: {self.phase} | 级别: {self.level.value}",
            f"产出角色: {self.agent_name}",
            f"Sprint: {self.sprint_id}" + (f" | Story: {self.story_id}" if self.story_id else ""),
            "",
            "摘要:",
        ]
        if self.key_decisions:
            lines.append(f"  关键决策点: {'; '.join(self.key_decisions)}")
        if self.change_scope:
            lines.append(f"  变更范围: {self.change_scope}")
        if self.risk_notes:
            lines.append(f"  ⚠ 风险提示: {self.risk_notes}")
        lines.append(f"  AI 置信度: {self.confidence.value}")
        if self.artifact_paths:
            lines.append(f"\n产出物路径:")
            for p in self.artifact_paths:
                lines.append(f"  - {p}")
        return "\n".join(lines)


@dataclass
class ArtifactEdit:
    """PO 对单个产出物的修改记录"""
    file_path: str
    original_hash: str = ""
    edit_summary: str = ""
    edited_by: str = "PO"


@dataclass
class ConfirmationResult:
    """PO 的确认结果"""
    decision: Literal["approve", "reject", "partial", "defer", "approve_with_edits"]
    feedback: str = ""
    rejected_items: list[str] = field(default_factory=list)
    artifact_edits: list[ArtifactEdit] = field(default_factory=list)


class ConfirmationAdapter(ABC):
    """确认交互适配器基类 — 不同渠道实现这个接口"""

    @abstractmethod
    def request_confirmation(self, req: ConfirmationRequest) -> ConfirmationResult:
        ...

    @abstractmethod
    def send_async_notification(self, req: ConfirmationRequest) -> str:
        ...

    @abstractmethod
    def check_async_result(self, confirmation_id: str) -> ConfirmationResult | None:
        ...


# ─── 产出物快照与 diff 检测工具 ───


def snapshot_artifacts(artifact_paths: list[str]) -> dict[str, str]:
    """对产出物做快照（内容 hash），确认前调用。"""
    hashes = {}
    for path in artifact_paths:
        if os.path.isdir(path):
            for f in glob.glob(os.path.join(path, "**", "*.md"), recursive=True):
                with open(f, "r", encoding="utf-8") as fh:
                    hashes[f] = hashlib.sha256(fh.read().encode()).hexdigest()
        elif os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as fh:
                hashes[path] = hashlib.sha256(fh.read().encode()).hexdigest()
    return hashes


def detect_artifact_edits(
    before_snapshot: dict[str, str],
    artifact_paths: list[str],
) -> list[ArtifactEdit]:
    """对比快照，检测哪些产出物被 PO 修改了。"""
    current = snapshot_artifacts(artifact_paths)
    edits = []
    for path, old_hash in before_snapshot.items():
        new_hash = current.get(path, "")
        if new_hash and new_hash != old_hash:
            edits.append(ArtifactEdit(file_path=path, original_hash=old_hash,
                                      edit_summary="PO 手动修改"))
    return edits


def generate_diff(file_path: str, original_content: str) -> str:
    """生成文件修改前后的 unified diff"""
    if not os.path.isfile(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        current_content = f.read()
    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        current_content.splitlines(keepends=True),
        fromfile=f"{file_path} (AI 原始版本)",
        tofile=f"{file_path} (PO 修改后)",
    )
    return "".join(diff)


def save_edit_record(
    sprint_id: str, node_id: str, edits: list[ArtifactEdit], project_root: str,
):
    """将 PO 的修改记录保存到 Sprint 目录"""
    record_dir = os.path.join(project_root, "sprints", sprint_id, "confirmations", "edit_records")
    os.makedirs(record_dir, exist_ok=True)
    record = {
        "node_id": node_id,
        "edited_at": datetime.now().isoformat(),
        "edits": [
            {"file": e.file_path, "original_hash": e.original_hash,
             "summary": e.edit_summary, "edited_by": e.edited_by}
            for e in edits
        ],
    }
    record_path = os.path.join(record_dir, f"{node_id}.json")
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return record_path
