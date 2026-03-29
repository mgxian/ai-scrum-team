"""Skill 加载器：从 .ai-scrum/agents/ 读取 prompt 模板，生成 CrewAI Task"""
import os
import re
from crewai import Task, Agent


def load_prompt(template_path: str) -> str:
    """从 .md 文件加载 prompt 模板"""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def fill_variables(template: str, variables: dict) -> str:
    """替换模板中的 【$variable_name】 占位符"""
    result = template
    for key, value in variables.items():
        pattern = rf"【\$\s*{re.escape(key)}\s*】"
        result = re.sub(pattern, str(value), result)
    return result


def make_task(
    template_path: str,
    agent: Agent,
    variables: dict,
    output_file: str,
    context: list[Task] | None = None,
    human_input: bool = False,
) -> Task:
    """
    从 prompt 模板创建 CrewAI Task。

    Args:
        template_path: .md 模板文件路径
        agent: 执行该 task 的 agent
        variables: 模板变量
        output_file: 产出物保存路径
        context: 依赖的上游 task 列表
        human_input: 是否需要人工确认
    """
    template = load_prompt(template_path)
    description = fill_variables(template, variables)
    task_name = os.path.splitext(os.path.basename(template_path))[0]

    return Task(
        name=task_name,
        description=description,
        expected_output=f"按照模板要求的格式输出完整的 {task_name} 分析结果",
        agent=agent,
        output_file=output_file,
        context=context or [],
        human_input=human_input,
        create_directory=True,
    )
