# AI Scrum Team

## 角色定义

| 角色 | 命名 | 实现方式 | 职责 |
|------|------|---------|------|
| 流程编排 | Flow Agent | Agent | 驱动端到端全流程：Refinement→Planning→Execution→Review→Retrospective，管理各角色间的衔接、数据传递、分支回退，在人工确认节点暂停等待 |
| 需求分析 | BA Copilot | 工作流 + RAG | 需求细化、业务规则梳理、知识库检索、User Story 拆分，每步人工确认 |
| 架构设计 | Arch Copilot | 工作流 + RAG | 技术方案、数据模型、接口设计 |
| 开发 | Code Agent | Agent | 写代码 + 单元测试 + 调试 |
| 测试 | QA Agent | Agent | E2E、集成、回归、性能测试 |
| 代码审查 + 安全 | Review Agent | 轻量 Agent | 代码规范审查、安全扫描、合规审计 |
| 文档管理 | Doc Agent | Agent | 自动跟踪代码变更、维护 API 文档、变更日志 |
| Scrum Master | SM Agent | Agent | Sprint 规划、Story 估算、进度跟踪、风险预警、Sprint 回顾分析 |
| DevOps | DevOps Agent | Agent | CI/CD 执行、自动化部署、监控告警、环境管理 |
| Product Owner | 人类 | — | 决策、确认、验收 |

> 7 个 Agent + 2 个 Copilot + 1 个人类 PO，共 10 个角色。
>
> 命名原则：需要自主决策和环境交互的叫 Agent，步骤固定、人工确认的叫 Copilot。

## 协作流程

### 一、Backlog Refinement（Sprint 之前，持续进行）

```
  PO（提出原始需求）
       ↓
  BA Copilot 第零段：生成业务背景澄清问卷
       ↓
  PO（填写问卷）← 阻塞确认，等待 PO 提供答案
       ↓
  BA Copilot：根据原始需求 + 问卷答案，生成优化后的需求
       ↓
  PO（确认优化后的需求）← 阻塞确认，后续所有分析都基于此
       ↓
  BA Copilot 第一段：干系人识别 → 角色识别 → 术语梳理 → 流程分析
       ↓
  PO（确认）← 阻塞确认，这些是场景分析的基础
       ↓
  BA Copilot 第二段：场景分析 → 场景引导法细节分析
       ↓
  PO（确认）← 阻塞确认，场景是后续所有工作的核心依赖
       ↓
  BA Copilot 第三段：依赖分析 → 功能列表梳理 → Q&A 识别
       ↓
  PO（确认）← BA 全部完成
       ↓
  BA Copilot（拆分 User Story，人工确认）
       ↓
  SM Agent（Story 工作量估算）
       ↓
  产出：Product Backlog（已估算的 Story 池）
```

> BA Copilot 分段执行的原因：后面的步骤依赖前面步骤的输出，如果前面有错误会传播到后续所有分析。关键节点（优化需求、基础分析、场景分析）必须确认后才继续。

### 二、Sprint Planning（Sprint 开始时）

```
  SM Agent（优先级排序建议、Sprint 容量评估）
       ↓
  PO（确定 Sprint Goal，挑选 Story 进入 Sprint）
       ↓
  Arch Copilot（根据选中的 Story，自行读取 BA 产出物，进行架构设计，人工确认）
       ↓
  SM Agent（任务拆分、排期、分配）
       ↓
  产出：Sprint Backlog（任务列表）
```

### 三、Sprint Execution（Sprint 进行中）

> 由 Flow Agent 驱动整个 Sprint 流程，管理各角色间的衔接和回退。

```
  Code Agent（编码 + 单元测试）
       ↓
  Review Agent（代码审查 + 安全扫描）
       ↓  ← 不通过则回退到 Code Agent（附回退工单）
  QA Agent（E2E、集成、回归测试）
       ↓  ← 不通过则回退到 Code Agent（附回退工单）
  测试通过后并行触发：
       ├→ Doc Agent（更新文档）
       └→ DevOps Agent（部署到测试/预发环境）
```

> 回退采用渐进式干预：L0 正常回退 → L1 关注（要求根因分析）→ L2 预警 PO（模式识别）→ L3 诊断（拉入 BA/Arch 介入）→ L4 熔断（暂停流转，PO 决策）。详见 Flow-Agent/01.状态机定义/1.2。
>
> Sprint 进行中，SM Agent 持续监控各 Agent 执行状态，生成进度报告，发现阻塞及时预警。

### 四、Sprint Review（Sprint 结束时）

```
  DevOps Agent（部署到演示环境）
       ↓
  PO（验收 + Demo 展示）
       ↓
  PO（反馈 → 新需求/调整回到 Product Backlog）
```

### 五、Sprint Retrospective（Sprint 结束后）

```
  SM Agent（分析本 Sprint 数据：审查通过率、回退次数、测试失败率、任务完成率、各 Agent 执行效率）
       ↓
  SM Agent（输出流程优化建议）
       ↓
  PO + SM Agent（确认改进项）
       ↓
  SM Agent（知识反馈分发：将确认的改进项按类别写入各角色的知识库/规则配置）
       ↓
  产出：更新后的各角色规则 + 知识库条目（下个 Sprint 自动生效）
```

## 协作机制

### Sprint 规划与优先级

- SM Agent：Story 工作量估算，根据依赖关系、复杂度给出优先级排序建议和 Sprint 容量评估
- PO（人类）：确定 Sprint Goal，最终拍板优先级，决定哪些 Story 进入当前 Sprint
- 流程：SM Agent 建议 → PO 确认/调整 → Sprint 开始 → Flow Agent 驱动执行

> 优先级决策必须由人参与，AI 只提供数据支撑和建议。

### 进度监控（替代 Daily Scrum）

- SM Agent 持续监控各 Agent 的执行状态
- 每个任务完成或阻塞时，自动生成进度报告
- 发现风险（回退过多、任务延期）时主动预警 PO
- PO 可随时查看当前 Sprint 进度总览

### Flow Agent（总调度）

- 驱动端到端全流程：Refinement → Planning → Execution → Review → Retrospective
- 按 Sprint 状态机推进阶段流转（详见 Flow-Agent/01.状态机定义/1.1）
- 按 Story 状态机管理每个 Story 的执行流转，支持多 Story 并行（详见 Flow-Agent/01.状态机定义/1.2）
- 处理回退逻辑：审查/测试不通过时回退到 Code Agent，维护回退计数器
- 熔断升级：单个 Story 回退超限时暂停流转，SM Agent 诊断根因后升级到 BA/Arch/PO
- 人工确认节点分三级管理（详见 Flow-Agent/02.编排规则/2.1）：
  - 阻塞确认：Sprint Goal、Story 拆分、验收——必须 PO 明确通过
  - 异步确认：BA 分析步骤、改进项——流程先继续，PO 并行审阅，驳回再回退
  - 自动通过：满足预设条件的架构设计和知识条目——自动推进，PO 可事后否决
- 每次数据传递前校验产出物是否已写入 repo 且符合契约 schema（详见 Flow-Agent/02.编排规则/2.3）
- Agent 执行超时/失败时按策略自动重试或升级（详见 Flow-Agent/02.编排规则/2.2）

### SM Agent 与 Flow Agent 的分工

- Flow Agent：管流程编排，负责发送触发信号、校验产出物就绪、处理回退
- SM Agent：管项目管理，负责估算、排优先级、监控进度、风险预警、回顾分析

### 知识反馈闭环

Sprint Retrospective 产出的改进项不能只停留在报告里，必须落地到各角色的规则和知识库中，形成跨 Sprint 的持续学习。

反馈分发规则：

| 改进类别 | 目标角色 | 写入位置 | 示例 |
|---------|---------|---------|------|
| 需求类问题 | BA Copilot | BA-Copilot/ 对应步骤的补充规则 + RAG 知识库 | "本 Sprint 3 个 Story 因未识别逆向流程导致回退" → 补充到场景分析的检查项 |
| 架构/技术类问题 | Arch Copilot | Arch-Copilot/ 对应模块的补充规则 + ADR 库 | "接口超时未设降级方案" → 补充到架构评审检查清单 |
| 编码类问题 | Code Agent | 编码规范 / Steering 规则 | "批量操作未做分页处理导致 OOM" → 补充到编码规范 |
| 审查类问题 | Review Agent | Review-Agent/ 对应规则文件 | "连续 2 个 Sprint 漏检 SQL 注入" → 提升 SQL 注入检查权重 |
| 测试类问题 | QA Agent | 测试策略 / 回归用例库 | "支付回调场景测试覆盖不足" → 补充到回归测试必测清单 |
| 估算类问题 | SM Agent | SM-Agent/01.估算模型/ | "涉及外部集成的 Story 估算普遍偏低 40%" → 调整估算系数 |
| 流程类问题 | Flow Agent | 流程编排规则 | "Doc Agent 等待 QA 通过后才启动导致交付延迟" → 调整为并行触发 |

知识库更新流程：

```
  SM Agent（从回顾报告中提取改进项）
       ↓
  SM Agent（按上表分类，生成知识条目草稿）
       ↓
  PO（确认知识条目，防止错误经验污染知识库）
       ↓
  SM Agent（写入对应角色的规则文件 / RAG 知识库）
       ↓
  各角色（下个 Sprint 自动加载更新后的规则）
```

> 关键原则：所有知识条目必须经 PO 确认后才能写入，避免单次偶发问题被错误地固化为规则。

### 并行场景

- Doc Agent 不一定要等测试通过才开始，可以在 Code Agent 完成后就同步更新文档
- 多个需求可以同时在不同阶段流转，SM Agent 协调资源

### 数据传递

所有产出物统一存储在 repo 中，各角色按需读取，不做显式数据搬运。Flow Agent 传递的只是触发信号（"轮到你了"+ Story/Sprint ID），各角色根据 ID 自行从 repo 读取所需上下文。

#### 产出物存储目录

| 角色 | 产出物 | 存储位置 | 阶段 |
|------|-------|---------|------|
| PO | 原始需求 | `docs/requirements/REQ-{id}/original.md` | Refinement |
| BA Copilot | 需求分析全套产出 | `docs/requirements/REQ-{id}/ba/` | Refinement |
| BA Copilot | User Story | `docs/stories/US-{id}.md` | Refinement |
| SM Agent | 估算结果、Sprint 计划 | `sprints/SP-{id}/plan.md` | Planning |
| Arch Copilot | 技术方案、领域模型、接口设计 | `docs/architecture/` | Planning |
| Arch Copilot | 架构决策记录 | `docs/architecture/adrs/ADR-{id}.md` | Planning |
| SM Agent | 任务列表、排期 | `sprints/SP-{id}/tasks/` | Planning |
| Code Agent | 代码 + 单元测试 | 代码分支 `feature/US-{id}` | Execution |
| Review Agent | 审查报告 | `sprints/SP-{id}/reviews/` | Execution |
| QA Agent | 测试报告 | `sprints/SP-{id}/tests/` | Execution |
| Doc Agent | API 文档、变更日志 | `docs/api-docs/` | Execution |
| DevOps Agent | 部署结果 | `sprints/SP-{id}/deployments/` | Review |
| SM Agent | 回顾报告、改进项 | `sprints/SP-{id}/retrospective/` | Retrospective |
| SM Agent | 知识条目 | `knowledge/` | Retrospective |

#### 触发信号

Flow Agent 在角色间传递的不是数据，而是轻量触发信号：

```json
{
  "signal": "your_turn",
  "target_role": "string",
  "sprint_id": "string",
  "story_id": "string, 可选",
  "task_id": "string, 可选",
  "context_hint": "string, 可选, 提示该角色重点关注的内容"
}
```

各角色收到信号后，根据 sprint_id / story_id 自行从 repo 读取所需的上下文。

## 项目目录结构

将 AI Scrum Team 集成到实际项目时，按以下结构组织。流程定义（跨项目复用）和运行时产出（项目特有）分开存放。

```
project-repo/
│
├── .ai-scrum/                           # 流程定义（跨项目复用，可做 git submodule）
│   ├── AI-Scrum-Team.md                 # 总览：角色、流程、协作机制
│   ├── agents/                          # 各角色的 prompt 模板和规则配置
│   │   ├── ba-copilot/                  # 需求分析工作流（10 个步骤）
│   │   ├── arch-copilot/               # 架构设计工作流
│   │   ├── flow-agent/                 # 状态机 + 编排规则
│   │   ├── sm-agent/                   # 估算模型 + 预警规则 + 知识反馈
│   │   ├── review-agent/              # 代码规范 + 安全扫描 + 合规审计
│   │   └── qa-agent/                  # 测试策略 + 回归 + 性能
│   └── overrides/                       # 项目级覆盖（定制本项目特有的规则）
│
├── docs/                                # 运行时产出：需求与设计（按需求编号组织，生命周期长于 Sprint）
│   ├── requirements/                    # 需求
│   │   └── REQ-001/
│   │       ├── original.md             # PO 原始需求
│   │       └── ba/                     # BA 全套分析产出
│   ├── stories/                         # User Story
│   │   └── US-001.md
│   ├── architecture/                    # 架构设计（持续演进，不按 Sprint 切分）
│   │   ├── domain-model.md
│   │   ├── database-design.md
│   │   ├── api-design.md
│   │   └── adrs/                       # 架构决策记录（追加，保留历史）
│   └── api-docs/                        # API 文档（Doc Agent 维护）
│
├── sprints/                             # 运行时产出：Sprint 记录（按 Sprint 编号，结束后只读归档）
│   └── SP-001/
│       ├── plan.md                     # Sprint Goal + Story 列表 + 任务分配
│       ├── tasks/                      # 任务详情
│       ├── reviews/                    # 代码审查报告
│       ├── tests/                      # 测试报告
│       ├── deployments/                # 部署记录
│       └── retrospective/             # 回顾报告 + 改进项
│
├── knowledge/                           # 知识积累（知识反馈闭环产出，跨 Sprint 持续更新）
│   ├── changelog.md                    # 知识库变更日志
│   ├── lessons/                        # 经验教训
│   └── regression-checklist.md         # 回归测试必测清单
│
└── src/                                 # 项目源代码
```

关键设计点：

- `.ai-scrum/` 是流程引擎，可以做成 git submodule 多项目共享，升级时统一拉取。`overrides/` 用于项目级定制（如金融项目覆盖合规清单）
- `docs/` 按需求编号组织，不按 Sprint。一个需求可能跨多个 Sprint，需求文档生命周期比 Sprint 长
- `docs/architecture/` 不按 Sprint 切分，架构是演进的。ADR 用编号追加，保留决策历史
- `sprints/` 按 Sprint 编号组织运行时数据，Sprint 结束后只读归档
- `knowledge/` 是知识反馈闭环的落地点，各角色从这里读取历史经验
