"""LangGraph 节点定义 — 每个节点是一个状态转换函数"""
import os
from langchain_openai import ChatOpenAI
from state import SprintState
from agents import ROLES
from skills import build_messages, save_output, load_prompt, fill_variables


# --- Skill 定义：(模板子目录, 模板文件名, 输出文件名) ---
BA_PHASE_0 = [("01.原始需求优化", "业务背景信息补全.md", "00_questionnaire.md")]
BA_PHASE_0B = [("01.原始需求优化", "需求优化.md", "01_optimized_requirement.md")]
BA_PHASE_1 = [
    ("02.需求分析", "2.1.干系人识别.md", "02_stakeholders.md"),
    ("02.需求分析", "2.2.角色识别.md", "03_roles.md"),
    ("02.需求分析", "2.3.术语梳理.md", "04_glossary.md"),
    ("02.需求分析", "2.4.流程分析.md", "05_flow.md"),
]
BA_PHASE_2 = [
    ("02.需求分析", "2.5.场景分析.md", "06_scenarios.md"),
    ("02.需求分析", "2.6场景引导法细节分析.md", "07_requirements_details.md"),
]
BA_PHASE_3 = [
    ("02.需求分析", "2.7依赖分析.md", "08_dependencies.md"),
    ("02.需求分析", "2.8功能列表梳理.md", "09_function_list.md"),
    ("02.需求分析", "2.9.Q&A识别.md", "10_qa_list.md"),
]
ARCH_SKILLS = [
    ("01.技术方案设计", "1.1.技术选型分析.md", "tech_selection.md"),
    ("01.技术方案设计", "1.2.系统架构设计.md", "system_architecture.md"),
    ("02.数据模型设计", "2.1.领域模型设计.md", "domain_model.md"),
    ("02.数据模型设计", "2.2.数据库表设计.md", "database_design.md"),
    ("03.接口设计", "3.1.API接口设计.md", "api_design.md"),
    ("04.架构评审", "4.1.架构评审检查清单.md", "arch_review.md"),
]


def _get_paths(state: SprintState):
    """计算各目录路径"""
    root = state["project_root"]
    agents_dir = os.path.join(root, ".ai-scrum", "agents")
    docs_dir = os.path.join(root, "docs")
    ba_dir = os.path.join(agents_dir, "ba-copilot")
    arch_dir = os.path.join(agents_dir, "arch-copilot")
    ba_out = os.path.join(docs_dir, "requirements", state["req_id"], "ba")
    arch_out = os.path.join(docs_dir, "architecture")
    return ba_dir, arch_dir, ba_out, arch_out, docs_dir


def _run_skill_chain(
    state: SprintState,
    skill_list: list[tuple[str, str, str]],
    base_dir: str,
    out_dir: str,
    role: str,
    variables: dict,
) -> dict[str, str]:
    """执行一组 skill 模板，返回 {输出文件名: 内容}"""
    llm = ChatOpenAI(model=state["llm"])
    results = {}

    for folder, template_file, output_file in skill_list:
        template_path = os.path.join(base_dir, folder, template_file)
        if not os.path.exists(template_path):
            continue

        # 把之前的产出也加入变量，实现链式依赖
        all_vars = {**variables, **results}
        messages = build_messages(template_path, all_vars, ROLES[role])
        response = llm.invoke(messages)
        content = response.content

        output_path = os.path.join(out_dir, output_file)
        save_output(content, output_path)
        results[output_file.replace(".md", "")] = content

    return results


# --- 变量映射：BA 输出文件名 → prompt 模板变量名 ---
BA_VAR_MAP = {
    "01_optimized_requirement": "optimized_requirements",
    "02_stakeholders": "stakeholders",
    "03_roles": "role_list",
    "04_glossary": "glossary",
    "05_flow": "flow",
    "06_scenarios": "scenario_list",
    "07_requirements_details": "requirements_details",
    "08_dependencies": "external_dependencies",
    "09_function_list": "function_list",
}


def _ba_variables(state: SprintState) -> dict:
    """从 state 中提取 BA 产出物作为模板变量"""
    variables = {}
    for key, content in state.get("ba_outputs", {}).items():
        variables[key] = content
        if key in BA_VAR_MAP:
            variables[BA_VAR_MAP[key]] = content
    return variables


# ===================== 节点函数 =====================

def generate_questionnaire(state: SprintState) -> dict:
    """第零段：生成业务背景澄清问卷"""
    ba_dir, _, ba_out, _, docs_dir = _get_paths(state)

    # 保存原始需求
    req_dir = os.path.join(docs_dir, "requirements", state["req_id"])
    os.makedirs(req_dir, exist_ok=True)
    with open(os.path.join(req_dir, "original.md"), "w", encoding="utf-8") as f:
        f.write(state["requirement"])

    variables = {"original_requirement": state["requirement"]}
    results = _run_skill_chain(state, BA_PHASE_0, ba_dir, ba_out, "ba_copilot", variables)

    return {
        "ba_outputs": results,
        "current_phase": "wait_questionnaire_answers",
    }


def optimize_requirement(state: SprintState) -> dict:
    """根据问卷答案生成优化后的需求"""
    ba_dir, _, ba_out, _, _ = _get_paths(state)

    variables = {
        "original_requirement": state["requirement"],
        "questionnaire_answers": state["questionnaire_answers"],
    }
    results = _run_skill_chain(state, BA_PHASE_0B, ba_dir, ba_out, "ba_copilot", variables)

    return {
        "ba_outputs": results,
        "current_phase": "review_optimized",
    }


def ba_phase1(state: SprintState) -> dict:
    """BA 第一段：干系人 + 角色 + 术语 + 流程"""
    ba_dir, _, ba_out, _, _ = _get_paths(state)
    variables = _ba_variables(state)
    results = _run_skill_chain(state, BA_PHASE_1, ba_dir, ba_out, "ba_copilot", variables)
    return {"ba_outputs": results, "current_phase": "review_phase1"}


def ba_phase2(state: SprintState) -> dict:
    """BA 第二段：场景分析 + 场景引导法细节分析"""
    ba_dir, _, ba_out, _, _ = _get_paths(state)
    variables = _ba_variables(state)
    results = _run_skill_chain(state, BA_PHASE_2, ba_dir, ba_out, "ba_copilot", variables)
    return {"ba_outputs": results, "current_phase": "review_phase2"}


def ba_phase3(state: SprintState) -> dict:
    """BA 第三段：依赖 + 功能列表 + Q&A"""
    ba_dir, _, ba_out, _, _ = _get_paths(state)
    variables = _ba_variables(state)
    results = _run_skill_chain(state, BA_PHASE_3, ba_dir, ba_out, "ba_copilot", variables)
    return {"ba_outputs": results, "current_phase": "review_phase3"}


def run_planning(state: SprintState) -> dict:
    """Planning 阶段：Arch Copilot 执行架构设计"""
    _, arch_dir, _, arch_out, _ = _get_paths(state)
    variables = _ba_variables(state)
    results = _run_skill_chain(state, ARCH_SKILLS, arch_dir, arch_out, "arch_copilot", variables)
    return {"arch_outputs": results, "current_phase": "review_planning"}


def handle_rejection(state: SprintState) -> dict:
    """处理 PO 驳回"""
    phase = state["current_phase"]
    feedback = state.get("human_feedback", "")
    print(f"\n⚠ {phase} 被驳回: {feedback}")
    return {"error": f"{phase} rejected: {feedback}"}


def start_execution(state: SprintState) -> dict:
    """进入 Execution 阶段"""
    print(f"\n{'='*60}")
    print(f"Execution - 请在 IDE 中开始编码")
    print(f"  需求: docs/requirements/{state['req_id']}/ba/")
    print(f"  架构: docs/architecture/")
    print(f"{'='*60}")
    return {"current_phase": "execution"}
