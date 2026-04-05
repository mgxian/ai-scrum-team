# AI Scrum Team - CrewAI Flow Engine

基于 CrewAI Flows 实现的 AI Scrum Team 自动化流程引擎。

## 架构

```
CrewAI Flow（ScrumFlow）= Flow Agent
  │
  ├→ 第零段 Crew：生成问卷 → PO 填写 → 生成优化需求 → 确认
  ├→ 第一段 Crew：干系人 + 角色 + 术语 + 流程 → 确认
  ├→ 第二段 Crew：场景分析 + 细节分析 → 确认
  ├→ 第三段 Crew：依赖 + 功能列表 + Q&A → 确认
  ├→ Planning Crew：Arch Copilot 架构设计 → 确认
  └→ Execution：暂停，等待开发者在 IDE 中编码
```

概念映射：
- Flow = 阶段编排（Flow Agent）
- Crew = 一段内的 Agent 协作
- Task = 单个 Skill（.md prompt 模板）
- Agent = 角色（BA Copilot / Arch Copilot 等）

数据传递：
- 同一段内：CrewAI context 自动传递（内存级）
- 跨段：读取前面已保存的 .md 文件，填充到 prompt 模板变量

## 快速开始

```bash
# 1. 安装
pip install "crewai[tools]" litellm

# 2. 配置
export OPENAI_API_KEY="your-key"
export PROJECT_ROOT="/path/to/your/project"

# 3. 将 prompt 模板放到正确位置
#    {PROJECT_ROOT}/.ai-scrum/agents/ba-copilot/
#    {PROJECT_ROOT}/.ai-scrum/agents/arch-copilot/

# 4. 运行
cd flow-engine-crewai/src
python flow.py --req "开发一个企业用车管理系统" --req-id REQ-001 --sprint SP-001
```

## 执行流程

```
1. AI 生成业务背景澄清问卷
2. PO 填写问卷（流程暂停等待）
3. AI 根据原始需求 + 问卷答案生成优化后的需求
4. PO 确认优化需求 ← 后续所有分析都基于此
5. AI 执行：干系人 → 角色 → 术语 → 流程
6. PO 确认 ← 场景分析的基础
7. AI 执行：场景分析 → 场景引导法细节分析
8. PO 确认 ← 最核心的产出
9. AI 执行：依赖 → 功能列表 → Q&A
10. PO 确认 ← BA 结束
11. AI 执行：架构设计（技术选型→架构→领域模型→数据库→API→评审）
12. PO 确认 ← 进入 Execution
13. 开发者在 IDE 中编码
```

## 产出物

```
{PROJECT_ROOT}/docs/requirements/REQ-001/
├── original.md                    # 原始需求
└── ba/
    ├── 00_questionnaire.md        # 业务背景澄清问卷
    ├── 01_optimized_requirement.md # 优化后的需求
    ├── 02_stakeholders.md         # 干系人
    ├── 03_roles.md                # 角色
    ├── 04_glossary.md             # 术语
    ├── 05_flow.md                 # 流程
    ├── 06_scenarios.md            # 场景
    ├── 07_requirements_details.md # 场景细节
    ├── 08_dependencies.md         # 依赖
    ├── 09_function_list.md        # 功能列表
    └── 10_qa_list.md              # Q&A

{PROJECT_ROOT}/docs/architecture/
├── tech_selection.md              # 技术选型
├── system_architecture.md         # 系统架构
├── domain_model.md                # 领域模型
├── database_design.md             # 数据库设计
├── api_design.md                  # API 设计
└── arch_review.md                 # 架构评审
```
