"""
示例：如何在任意 Flow Engine 中使用确认适配器

通过环境变量 CONFIRM_ADAPTER 切换确认渠道：
  cli  → 命令行终端（默认）
  ide  → Kiro Chat
  web  → Web Dashboard
  git  → GitHub PR/Issue

用法（LangGraph 或 CrewAI 均可）：
  from confirmation import create_adapter, ConfirmationRequest, ConfirmLevel
"""
import os
from . import (
    ConfirmationRequest, ConfirmLevel, Confidence,
    CLIConfirmationAdapter, IDEConfirmationAdapter,
    WebConfirmationAdapter, GitConfirmationAdapter,
)


def create_adapter():
    """根据环境变量创建对应的确认适配器"""
    adapter_type = os.environ.get("CONFIRM_ADAPTER", "cli")
    project_root = os.environ.get("PROJECT_ROOT", ".")

    if adapter_type == "ide":
        return IDEConfirmationAdapter(project_root)
    elif adapter_type == "web":
        return WebConfirmationAdapter(project_root, port=8080)
    elif adapter_type == "git":
        return GitConfirmationAdapter(
            repo=os.environ["GITHUB_REPO"],
            token=os.environ["GITHUB_TOKEN"],
            assignee=os.environ.get("PO_GITHUB_USER", ""),
            project_root=project_root,
        )
    else:
        return CLIConfirmationAdapter(project_root)
