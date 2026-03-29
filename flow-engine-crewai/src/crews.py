"""各阶段的 Crew 定义"""
import os
from crewai import Crew, Process, Task
from agents import ba_copilot, arch_copilot, sm_agent
from skills import make_task


# ============================================================
# BA Copilot skill 分段定义
# ============================================================
# 第零段：生成业务背景澄清问卷（需要 PO 填写后才能继续）
BA_PHASE_0 = [
    ("01.原始需求优化", "业务背景信息补全.md", "00_questionnaire.md"),
]

# 第零段续：根据问卷答案生成优化后的需求
BA_PHASE_0B = [
    ("01.原始需求优化", "需求优化.md", "01_optimized_requirement.md"),
]

# 第一段：基础分析（基于优化后的需求）
BA_PHASE_1 = [
    ("02.需求分析", "2.1.干系人识别.md", "02_stakeholders.md"),
    ("02.需求分析", "2.2.角色识别.md", "03_roles.md"),
    ("02.需求分析", "2.3.术语梳理.md", "04_glossary.md"),
    ("02.需求分析", "2.4.流程分析.md", "05_flow.md"),
]

# 第二段：场景分析（核心，后续所有分析都依赖场景）
BA_PHASE_2 = [
    ("02.需求分析", "2.5.场景分析.md", "06_scenarios.md"),
    ("02.需求分析", "2.6场景引导法细节分析.md", "07_requirements_details.md"),
]

# 第三段：依赖、功能列表、Q&A（一口气跑完最后确认）
BA_PHASE_3 = [
    ("02.需求分析", "2.7依赖分析.md", "08_dependencies.md"),
    ("02.需求分析", "2.8功能列表梳理.md", "09_function_list.md"),
    ("02.需求分析", "2.9.Q&A识别.md", "10_qa_list.md"),
]


def _build_ba_crew(
    skill_list: list[tuple[str, str, str]],
    ba_agent,
    ba_dir: str,
    out_dir: str,
    variables: dict,
) -> Crew:
    """根据 skill 列表构建一个 BA Crew"""
    tasks: list[Task] = []
    for folder, template_file, output_file in skill_list:
        template_path = os.path.join(ba_dir, folder, template_file)
        if not os.path.exists(template_path):
            continue
        task = make_task(
            template_path=template_path,
            agent=ba_agent,
            variables=variables,
            output_file=os.path.join(out_dir, output_file),
            context=tasks[-1:],
        )
        tasks.append(task)

    return Crew(
        agents=[ba_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


def _read_ba_outputs(out_dir: str) -> dict:
    """读取已有的 BA 产出物，作为后续 skill 的输入变量"""
    variables = {}
    if not os.path.isdir(out_dir):
        return variables

    # 文件名 → 变量名的映射
    file_var_map = {
        "01_business_background": "optimized_requirements",
        "02_stakeholders": "stakeholders",
        "03_roles": "role_list",
        "04_glossary": "glossary",
        "05_flow": "flow",
        "06_scenarios": "scenario_list",
        "07_requirements_details": "requirements_details",
        "08_dependencies": "external_dependencies",
        "09_function_list": "function_list",
    }

    for f in sorted(os.listdir(out_dir)):
        if not f.endswith(".md"):
            continue
        key = f.replace(".md", "")
        with open(os.path.join(out_dir, f), "r", encoding="utf-8") as fh:
            content = fh.read()
        variables[key] = content
        # 映射到 prompt 模板里用的变量名
        if key in file_var_map:
            variables[file_var_map[key]] = content

    return variables


def refinement_phase0_questionnaire(
    requirement: str,
    req_id: str,
    agents_dir: str,
    output_dir: str,
    llm: str = "gpt-4o",
) -> Crew:
    """第零段：生成业务背景澄清问卷"""
    ba = ba_copilot(llm)
    ba_dir = os.path.join(agents_dir, "ba-copilot")
    out = os.path.join(output_dir, "requirements", req_id, "ba")

    variables = {"original_requirement": requirement}

    return _build_ba_crew(BA_PHASE_0, ba, ba_dir, out, variables)


def refinement_phase0_optimize(
    requirement: str,
    questionnaire_answers: str,
    req_id: str,
    agents_dir: str,
    output_dir: str,
    llm: str = "gpt-4o",
) -> Crew:
    """第零段续：根据问卷答案生成优化后的需求"""
    ba = ba_copilot(llm)
    ba_dir = os.path.join(agents_dir, "ba-copilot")
    out = os.path.join(output_dir, "requirements", req_id, "ba")

    variables = {
        "original_requirement": requirement,
        "questionnaire_answers": questionnaire_answers,
    }

    return _build_ba_crew(BA_PHASE_0B, ba, ba_dir, out, variables)


def refinement_phase1(
    req_id: str,
    agents_dir: str,
    output_dir: str,
    llm: str = "gpt-4o",
) -> Crew:
    """第一段：干系人 + 角色 + 术语 + 流程（基于优化后的需求）"""
    ba = ba_copilot(llm)
    ba_dir = os.path.join(agents_dir, "ba-copilot")
    out = os.path.join(output_dir, "requirements", req_id, "ba")

    variables = _read_ba_outputs(out)

    return _build_ba_crew(BA_PHASE_1, ba, ba_dir, out, variables)


def refinement_phase2(
    req_id: str,
    agents_dir: str,
    output_dir: str,
    llm: str = "gpt-4o",
) -> Crew:
    """第二段：场景分析 + 场景引导法细节分析"""
    ba = ba_copilot(llm)
    ba_dir = os.path.join(agents_dir, "ba-copilot")
    out = os.path.join(output_dir, "requirements", req_id, "ba")

    variables = _read_ba_outputs(out)

    return _build_ba_crew(BA_PHASE_2, ba, ba_dir, out, variables)


def refinement_phase3(
    req_id: str,
    agents_dir: str,
    output_dir: str,
    llm: str = "gpt-4o",
) -> Crew:
    """第三段：依赖分析 + 功能列表 + Q&A"""
    ba = ba_copilot(llm)
    ba_dir = os.path.join(agents_dir, "ba-copilot")
    out = os.path.join(output_dir, "requirements", req_id, "ba")

    variables = _read_ba_outputs(out)

    return _build_ba_crew(BA_PHASE_3, ba, ba_dir, out, variables)


def planning_crew(
    req_id: str,
    sprint_id: str,
    agents_dir: str,
    output_dir: str,
    llm: str = "gpt-4o",
) -> Crew:
    """Planning 阶段 Crew：Arch Copilot 执行架构设计 skill。"""
    arch = arch_copilot(llm)
    arch_dir = os.path.join(agents_dir, "arch-copilot")
    arch_out = os.path.join(output_dir, "architecture")

    # 读取 BA 全部产出物作为变量
    ba_out = os.path.join(output_dir, "requirements", req_id, "ba")
    variables = _read_ba_outputs(ba_out)

    arch_skills = [
        ("01.技术方案设计", "1.1.技术选型分析.md", "tech_selection.md"),
        ("01.技术方案设计", "1.2.系统架构设计.md", "system_architecture.md"),
        ("02.数据模型设计", "2.1.领域模型设计.md", "domain_model.md"),
        ("02.数据模型设计", "2.2.数据库表设计.md", "database_design.md"),
        ("03.接口设计", "3.1.API接口设计.md", "api_design.md"),
        ("04.架构评审", "4.1.架构评审检查清单.md", "arch_review.md"),
    ]

    tasks: list[Task] = []
    for folder, template_file, output_file in arch_skills:
        template_path = os.path.join(arch_dir, folder, template_file)
        if not os.path.exists(template_path):
            continue
        task = make_task(
            template_path=template_path,
            agent=arch,
            variables=variables,
            output_file=os.path.join(arch_out, output_file),
            context=tasks[-1:],
        )
        tasks.append(task)

    return Crew(
        agents=[arch],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
