"""
Flow Agent - 基于 CrewAI Flows 的端到端流程编排

BA Copilot 分段执行：
  第零段：生成问卷 → PO 填写问卷 → 生成优化后的需求
  第一段：干系人 + 角色 + 术语 + 流程 → 确认
  第二段：场景分析 + 场景引导法细节分析 → 确认
  第三段：依赖 + 功能列表 + Q&A → 确认（BA 结束）

用法:
  python flow.py --req "你的需求描述" --req-id REQ-001 --sprint SP-001
"""
import os
import argparse
from pydantic import BaseModel, Field
from crewai.flow.flow import Flow, start, listen
from crewai.flow.human_feedback import human_feedback, HumanFeedbackResult
from crews import (
    refinement_phase0_questionnaire,
    refinement_phase0_optimize,
    refinement_phase1,
    refinement_phase2,
    refinement_phase3,
    planning_crew,
)


class SprintState(BaseModel):
    requirement: str = ""
    req_id: str = "REQ-001"
    sprint_id: str = "SP-001"
    llm: str = "gpt-4o"
    project_root: str = Field(default_factory=lambda: os.environ.get(
        "PROJECT_ROOT",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ))
    questionnaire_answers: str = ""

    @property
    def agents_dir(self) -> str:
        return os.path.join(self.project_root, ".ai-scrum", "agents")

    @property
    def docs_dir(self) -> str:
        return os.path.join(self.project_root, "docs")


class ScrumFlow(Flow[SprintState]):

    # ==================== 第零段：问卷生成 ====================
    @start()
    def generate_questionnaire(self):
        """AI 根据原始需求生成业务背景澄清问卷"""
        print(f"\n{'='*60}")
        print(f"第零段：生成业务背景澄清问卷")
        print(f"{'='*60}")

        req_dir = os.path.join(self.state.docs_dir, "requirements", self.state.req_id)
        os.makedirs(req_dir, exist_ok=True)
        with open(os.path.join(req_dir, "original.md"), "w", encoding="utf-8") as f:
            f.write(self.state.requirement)

        crew = refinement_phase0_questionnaire(
            requirement=self.state.requirement,
            req_id=self.state.req_id,
            agents_dir=self.state.agents_dir,
            output_dir=self.state.docs_dir,
            llm=self.state.llm,
        )
        return str(crew.kickoff())

    # ==================== PO 填写问卷 ====================
    @listen(generate_questionnaire)
    @human_feedback(
        message=(
            "问卷已生成。请根据问卷逐项填写答案。\n"
            "填写完成后，请将答案粘贴到下方（或保存到文件后提供路径）。"
        ),
        emit=["answers_provided", "cancel"],
        default_outcome="answers_provided",
    )
    def wait_for_answers(self):
        ba_dir = f"docs/requirements/{self.state.req_id}/ba/"
        return f"问卷文件位于: {ba_dir}00_questionnaire.md"

    @listen("cancel")
    def questionnaire_cancelled(self, result: HumanFeedbackResult):
        print("\n⚠ 已取消。")

    # ==================== 生成优化后的需求 ====================
    @listen("answers_provided")
    def optimize_requirement(self, result: HumanFeedbackResult):
        """根据原始需求 + 问卷答案，生成优化后的需求"""
        print(f"\n{'='*60}")
        print(f"根据问卷答案生成优化后的需求")
        print(f"{'='*60}")

        # PO 的反馈就是问卷答案
        answers = result.feedback
        self.state.questionnaire_answers = answers

        crew = refinement_phase0_optimize(
            requirement=self.state.requirement,
            questionnaire_answers=answers,
            req_id=self.state.req_id,
            agents_dir=self.state.agents_dir,
            output_dir=self.state.docs_dir,
            llm=self.state.llm,
        )
        return str(crew.kickoff())

    @listen(optimize_requirement)
    @human_feedback(
        message="优化后的需求已生成。请确认需求是否准确完整，后续所有分析都基于此。",
        emit=["requirement_ok", "requirement_redo"],
        default_outcome="requirement_ok",
    )
    def review_optimized(self):
        ba_dir = f"docs/requirements/{self.state.req_id}/ba/"
        return f"优化后的需求: {ba_dir}01_optimized_requirement.md"

    @listen("requirement_redo")
    def optimized_rejected(self, result: HumanFeedbackResult):
        print(f"\n⚠ 优化需求被驳回: {result.feedback}")
        print("请补充信息后重新运行。")


    # ==================== BA 第一段 ====================
    @listen("requirement_ok")
    def ba_phase1(self, result: HumanFeedbackResult):
        """干系人 + 角色 + 术语 + 流程"""
        print(f"\n{'='*60}")
        print(f"BA 第一段：干系人 + 角色 + 术语 + 流程")
        print(f"{'='*60}")

        crew = refinement_phase1(
            req_id=self.state.req_id,
            agents_dir=self.state.agents_dir,
            output_dir=self.state.docs_dir,
            llm=self.state.llm,
        )
        return str(crew.kickoff())

    @listen(ba_phase1)
    @human_feedback(
        message="第一段完成（干系人、角色、术语、流程）。这些是场景分析的基础，请审阅。",
        emit=["phase1_ok", "phase1_redo"],
        default_outcome="phase1_ok",
    )
    def review_phase1(self):
        return f"产出物: docs/requirements/{self.state.req_id}/ba/ (02-05)"

    @listen("phase1_redo")
    def phase1_rejected(self, result: HumanFeedbackResult):
        print(f"\n⚠ 第一段被驳回: {result.feedback}")

    # ==================== BA 第二段 ====================
    @listen("phase1_ok")
    def ba_phase2(self, result: HumanFeedbackResult):
        """场景分析 + 场景引导法细节分析"""
        print(f"\n{'='*60}")
        print(f"BA 第二段：场景分析 + 场景引导法细节分析")
        print(f"{'='*60}")

        crew = refinement_phase2(
            req_id=self.state.req_id,
            agents_dir=self.state.agents_dir,
            output_dir=self.state.docs_dir,
            llm=self.state.llm,
        )
        return str(crew.kickoff())

    @listen(ba_phase2)
    @human_feedback(
        message="第二段完成（场景分析、细节分析）。场景是后续所有工作的基础，请重点审阅。",
        emit=["phase2_ok", "phase2_redo"],
        default_outcome="phase2_ok",
    )
    def review_phase2(self):
        return f"产出物: docs/requirements/{self.state.req_id}/ba/ (06-07)"

    @listen("phase2_redo")
    def phase2_rejected(self, result: HumanFeedbackResult):
        print(f"\n⚠ 第二段被驳回: {result.feedback}")

    # ==================== BA 第三段 ====================
    @listen("phase2_ok")
    def ba_phase3(self, result: HumanFeedbackResult):
        """依赖 + 功能列表 + Q&A（一口气跑完）"""
        print(f"\n{'='*60}")
        print(f"BA 第三段：依赖 + 功能列表 + Q&A")
        print(f"{'='*60}")

        crew = refinement_phase3(
            req_id=self.state.req_id,
            agents_dir=self.state.agents_dir,
            output_dir=self.state.docs_dir,
            llm=self.state.llm,
        )
        return str(crew.kickoff())

    @listen(ba_phase3)
    @human_feedback(
        message="BA 全部完成。确认后进入架构设计。",
        emit=["ba_done", "phase3_redo"],
        default_outcome="ba_done",
    )
    def review_phase3(self):
        return f"产出物: docs/requirements/{self.state.req_id}/ba/ (08-10)"

    @listen("phase3_redo")
    def phase3_rejected(self, result: HumanFeedbackResult):
        print(f"\n⚠ 第三段被驳回: {result.feedback}")

    # ==================== Planning ====================
    @listen("ba_done")
    def run_planning(self, result: HumanFeedbackResult):
        print(f"\n{'='*60}")
        print(f"阶段: Planning | Sprint: {self.state.sprint_id}")
        print(f"{'='*60}")

        crew = planning_crew(
            req_id=self.state.req_id,
            sprint_id=self.state.sprint_id,
            agents_dir=self.state.agents_dir,
            output_dir=self.state.docs_dir,
            llm=self.state.llm,
        )
        return str(crew.kickoff())

    @listen(run_planning)
    @human_feedback(
        message="架构设计已完成。确认后进入 Execution。",
        emit=["start_execution", "redo_planning"],
        default_outcome="start_execution",
    )
    def review_planning(self):
        return "产出物: docs/architecture/"

    @listen("redo_planning")
    def planning_rejected(self, result: HumanFeedbackResult):
        print(f"\n⚠ Planning 被驳回: {result.feedback}")

    @listen("start_execution")
    def start_execution(self, result: HumanFeedbackResult):
        print(f"\n{'='*60}")
        print(f"Execution - 请在 IDE 中开始编码")
        print(f"{'='*60}")
        print(f"  需求: docs/requirements/{self.state.req_id}/ba/")
        print(f"  架构: docs/architecture/")
        return "done"


def main():
    parser = argparse.ArgumentParser(description="AI Scrum Team - CrewAI Flow")
    parser.add_argument("--req", type=str, required=True, help="需求描述或文件路径")
    parser.add_argument("--req-id", type=str, default="REQ-001")
    parser.add_argument("--sprint", type=str, default="SP-001")
    parser.add_argument("--llm", type=str, default="gpt-4o")
    args = parser.parse_args()

    requirement = args.req
    if os.path.isfile(requirement):
        with open(requirement, "r", encoding="utf-8") as f:
            requirement = f.read()

    flow = ScrumFlow()
    flow.state.requirement = requirement
    flow.state.req_id = args.req_id
    flow.state.sprint_id = args.sprint
    flow.state.llm = args.llm
    flow.kickoff()


if __name__ == "__main__":
    main()
