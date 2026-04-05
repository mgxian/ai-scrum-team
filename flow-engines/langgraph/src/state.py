"""Sprint 状态定义 — LangGraph 的核心状态对象"""
import operator
from typing import Annotated, Literal
from typing_extensions import TypedDict


class SprintState(TypedDict):
    """LangGraph 全局状态，贯穿整个 Sprint 生命周期"""

    # --- 配置 ---
    req_id: str
    sprint_id: str
    llm: str
    project_root: str

    # --- 原始输入 ---
    requirement: str
    questionnaire_answers: str

    # --- BA 产出物（每阶段追加） ---
    ba_outputs: Annotated[dict[str, str], operator.or_]

    # --- Arch 产出物 ---
    arch_outputs: Annotated[dict[str, str], operator.or_]

    # --- 流程控制 ---
    current_phase: str
    human_decision: Literal["approve", "reject", ""] 
    human_feedback: str
    error: str

    # --- Story 执行跟踪 ---
    story_rollback_counts: Annotated[dict[str, int], operator.or_]
