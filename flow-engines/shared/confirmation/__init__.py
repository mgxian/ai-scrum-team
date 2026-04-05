"""PO 确认交互适配器 — 框架无关的共享模块，可被 LangGraph / CrewAI / 任意引擎使用"""
from .base import (
    ConfirmationRequest,
    ConfirmationResult,
    ConfirmationAdapter,
    ArtifactEdit,
    ConfirmLevel,
    Confidence,
    snapshot_artifacts,
    detect_artifact_edits,
    generate_diff,
    save_edit_record,
)
from .cli_adapter import CLIConfirmationAdapter
from .ide_adapter import IDEConfirmationAdapter
from .web_adapter import WebConfirmationAdapter
from .git_adapter import GitConfirmationAdapter

__all__ = [
    "ConfirmationRequest",
    "ConfirmationResult",
    "ConfirmationAdapter",
    "ArtifactEdit",
    "ConfirmLevel",
    "Confidence",
    "snapshot_artifacts",
    "detect_artifact_edits",
    "generate_diff",
    "save_edit_record",
    "CLIConfirmationAdapter",
    "IDEConfirmationAdapter",
    "WebConfirmationAdapter",
    "GitConfirmationAdapter",
]
