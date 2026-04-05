"""Skill 加载器：从 prompt 模板生成 LLM 调用（复用 CrewAI 版的模板机制）"""
import os
import re
from langchain_core.messages import HumanMessage, SystemMessage


def load_prompt(template_path: str) -> str:
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def fill_variables(template: str, variables: dict) -> str:
    result = template
    for key, value in variables.items():
        pattern = rf"【\$\s*{re.escape(key)}\s*】"
        result = re.sub(pattern, str(value), result)
    return result


def build_messages(
    template_path: str,
    variables: dict,
    role_description: str = "",
) -> list:
    """从 prompt 模板构建 LangChain 消息列表"""
    template = load_prompt(template_path)
    prompt = fill_variables(template, variables)

    messages = []
    if role_description:
        messages.append(SystemMessage(content=role_description))
    messages.append(HumanMessage(content=prompt))
    return messages


def save_output(content: str, output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path
