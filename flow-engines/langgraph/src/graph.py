"""
LangGraph 流程图定义 — Sprint 生命周期状态机

核心优势（相比 CrewAI Flow）：
- 显式的图结构，可视化流程
- 内置 human-in-the-loop（interrupt_before）
- 持久化检查点，可恢复中断的流程
- 条件路由，天然支持审批/驳回分支
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import SprintState
from nodes import (
    generate_questionnaire,
    optimize_requirement,
    ba_phase1,
    ba_phase2,
    ba_phase3,
    run_planning,
    handle_rejection,
    start_execution,
)


def route_human_decision(state: SprintState) -> str:
    """根据 PO 的决策路由到下一个节点"""
    if state.get("human_decision") == "reject":
        return "rejected"
    return "approved"


def build_graph() -> StateGraph:
    """构建 Sprint 流程图"""
    graph = StateGraph(SprintState)

    # --- 添加节点 ---
    graph.add_node("generate_questionnaire", generate_questionnaire)
    graph.add_node("optimize_requirement", optimize_requirement)
    graph.add_node("ba_phase1", ba_phase1)
    graph.add_node("ba_phase2", ba_phase2)
    graph.add_node("ba_phase3", ba_phase3)
    graph.add_node("run_planning", run_planning)
    graph.add_node("handle_rejection", handle_rejection)
    graph.add_node("start_execution", start_execution)

    # --- 边：起点 → 生成问卷 ---
    graph.add_edge(START, "generate_questionnaire")

    # 问卷生成后，中断等待 PO 填写答案
    # （外部通过 update_state 注入 questionnaire_answers 后 resume）
    graph.add_edge("generate_questionnaire", "optimize_requirement")

    # 优化需求后，中断等待 PO 确认
    graph.add_conditional_edges(
        "optimize_requirement",
        route_human_decision,
        {"approved": "ba_phase1", "rejected": "handle_rejection"},
    )

    # BA 第一段后，中断等待 PO 确认
    graph.add_conditional_edges(
        "ba_phase1",
        route_human_decision,
        {"approved": "ba_phase2", "rejected": "handle_rejection"},
    )

    # BA 第二段后，中断等待 PO 确认
    graph.add_conditional_edges(
        "ba_phase2",
        route_human_decision,
        {"approved": "ba_phase3", "rejected": "handle_rejection"},
    )

    # BA 第三段后，中断等待 PO 确认，通过则进入 Planning
    graph.add_conditional_edges(
        "ba_phase3",
        route_human_decision,
        {"approved": "run_planning", "rejected": "handle_rejection"},
    )

    # Planning 后，中断等待 PO 确认
    graph.add_conditional_edges(
        "run_planning",
        route_human_decision,
        {"approved": "start_execution", "rejected": "handle_rejection"},
    )

    # 终止节点
    graph.add_edge("handle_rejection", END)
    graph.add_edge("start_execution", END)

    return graph


def compile_graph(checkpointer=None):
    """编译图，启用人工确认中断点"""
    graph = build_graph()

    if checkpointer is None:
        checkpointer = MemorySaver()

    return graph.compile(
        checkpointer=checkpointer,
        # 在这些节点执行前中断，等待人工输入
        interrupt_before=[
            "optimize_requirement",   # 等 PO 填写问卷答案
            "ba_phase1",              # 等 PO 确认优化需求
            "ba_phase2",              # 等 PO 确认第一段
            "ba_phase3",              # 等 PO 确认第二段
            "run_planning",           # 等 PO 确认第三段
            "start_execution",        # 等 PO 确认架构设计
        ],
    )
