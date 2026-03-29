"""
Flow Agent - 基于 LangGraph 的端到端流程编排

与 CrewAI 版本的关键区别：
- 流程是显式的有向图，可用 graph.get_graph().draw_mermaid() 可视化
- 内置 interrupt_before 实现 human-in-the-loop，无需自定义装饰器
- MemorySaver 检查点支持流程中断后恢复（断电/重启不丢状态）
- 条件路由天然支持审批/驳回分支

用法:
  python flow.py --req "你的需求描述" --req-id REQ-001 --sprint SP-001
"""
import os
import argparse
from graph import compile_graph


def run_flow(requirement: str, req_id: str, sprint_id: str, llm: str):
    """交互式运行 Sprint 流程"""
    app = compile_graph()

    project_root = os.environ.get(
        "PROJECT_ROOT",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    initial_state = {
        "req_id": req_id,
        "sprint_id": sprint_id,
        "llm": llm,
        "project_root": project_root,
        "requirement": requirement,
        "questionnaire_answers": "",
        "ba_outputs": {},
        "arch_outputs": {},
        "current_phase": "start",
        "human_decision": "",
        "human_feedback": "",
        "error": "",
        "story_rollback_counts": {},
    }

    config = {"configurable": {"thread_id": f"{sprint_id}-{req_id}"}}

    # 启动图执行（会在第一个 interrupt_before 节点暂停）
    print(f"\n{'='*60}")
    print(f"AI Scrum Team - LangGraph Flow Engine")
    print(f"需求: {req_id} | Sprint: {sprint_id}")
    print(f"{'='*60}\n")

    for event in app.stream(initial_state, config):
        # 打印每个节点的执行结果
        for node_name, output in event.items():
            phase = output.get("current_phase", "")
            print(f"\n✓ 节点 [{node_name}] 完成 → {phase}")

    # 交互循环：每次中断后等待人工输入，然后 resume
    while True:
        snapshot = app.get_state(config)
        if not snapshot.next:
            print("\n✓ 流程结束")
            break

        next_node = snapshot.next[0]
        print(f"\n{'─'*40}")
        print(f"⏸ 流程暂停，等待人工输入")
        print(f"  下一步: {next_node}")
        print(f"{'─'*40}")

        if next_node == "optimize_requirement":
            # 等待 PO 填写问卷答案
            print("\n请填写问卷答案（输入 'q' 退出）：")
            answers = input("> ").strip()
            if answers.lower() == "q":
                break
            app.update_state(config, {"questionnaire_answers": answers, "human_decision": ""})

        else:
            # 等待 PO 审批
            print("\n请审阅产出物后输入决策：")
            print("  [y] 通过  [n] 驳回  [q] 退出")
            decision = input("> ").strip().lower()

            if decision == "q":
                break
            elif decision == "n":
                feedback = input("驳回原因: ").strip()
                app.update_state(config, {
                    "human_decision": "reject",
                    "human_feedback": feedback,
                })
            else:
                app.update_state(config, {
                    "human_decision": "approve",
                    "human_feedback": "",
                })

        # 继续执行
        for event in app.stream(None, config):
            for node_name, output in event.items():
                phase = output.get("current_phase", "")
                if output.get("error"):
                    print(f"\n✗ 节点 [{node_name}]: {output['error']}")
                else:
                    print(f"\n✓ 节点 [{node_name}] 完成 → {phase}")


def main():
    parser = argparse.ArgumentParser(description="AI Scrum Team - LangGraph Flow")
    parser.add_argument("--req", type=str, required=True, help="需求描述或文件路径")
    parser.add_argument("--req-id", type=str, default="REQ-001")
    parser.add_argument("--sprint", type=str, default="SP-001")
    parser.add_argument("--llm", type=str, default="gpt-4o")
    args = parser.parse_args()

    requirement = args.req
    if os.path.isfile(requirement):
        with open(requirement, "r", encoding="utf-8") as f:
            requirement = f.read()

    run_flow(requirement, args.req_id, args.sprint, args.llm)


if __name__ == "__main__":
    main()
