# AI Scrum Team - LangGraph Flow Engine

基于 [LangGraph](https://github.com/langchain-ai/langgraph) 的 Sprint 流程编排引擎。

## 与 CrewAI 版本的区别

| 特性 | CrewAI Flow | LangGraph |
|------|------------|-----------|
| 流程定义 | 装饰器 + 事件监听 | 显式有向图（StateGraph） |
| 人工确认 | `@human_feedback` 装饰器 | `interrupt_before` + `update_state` |
| 状态持久化 | 无内置 | MemorySaver / SQLite / Postgres |
| 流程可视化 | 无 | `graph.get_graph().draw_mermaid()` |
| 条件路由 | 事件 emit | `add_conditional_edges` |
| 断点恢复 | 不支持 | 原生支持（checkpointer） |

## 架构

```
src/
├── state.py    # SprintState 定义（TypedDict）
├── agents.py   # 角色 system prompt
├── skills.py   # Prompt 模板加载 + 变量替换
├── nodes.py    # 图节点（每个节点 = 一个状态转换函数）
├── graph.py    # StateGraph 构建 + 编译
└── flow.py     # CLI 入口 + 交互循环
```

## 流程图

```
START → generate_questionnaire → [PO 填写问卷]
  → optimize_requirement → [PO 确认需求]
  → ba_phase1 → [PO 确认]
  → ba_phase2 → [PO 确认]
  → ba_phase3 → [PO 确认]
  → run_planning → [PO 确认架构]
  → start_execution → END
```

每个 `[PO 确认]` 节点支持 approve/reject 分支。

## 使用

```bash
pip install -e .
python src/flow.py --req "你的需求描述" --req-id REQ-001 --sprint SP-001
```
