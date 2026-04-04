# Skill 目录

Skill 按角色子目录组织，位于 `.kiro/skills/` 下。

## BA Copilot Skills（`skills/ba/`）

| Skill | 路径 | 关键词 | 源文件 |
|-------|------|--------|--------|
| `ba-requirement-clarification` | `ba/requirement-clarification/` | 需求澄清、问卷、业务背景、小功能 | `ba-copilot/01.原始需求优化/业务背景澄清.md`、`小功能需求澄清.md` |
| `ba-requirement-optimization` | `ba/requirement-optimization/` | 需求优化、结构化文档 | `ba-copilot/01.原始需求优化/需求优化.md` |
| `ba-stakeholder-analysis` | `ba/stakeholder-analysis/` | 干系人、关注点 | `ba-copilot/02.需求分析/2.1.干系人识别.md` |
| `ba-role-identification` | `ba/role-identification/` | 角色、权限、用户类型 | `ba-copilot/02.需求分析/2.2.角色识别.md` |
| `ba-glossary` | `ba/glossary/` | 术语、词汇表、领域术语 | `ba-copilot/02.需求分析/2.3.术语梳理.md` |
| `ba-process-analysis` | `ba/process-analysis/` | 业务流程、PlantUML、泳道图 | `ba-copilot/02.需求分析/2.4.流程分析.md` |
| `ba-scenario-analysis` | `ba/scenario-analysis/` | 场景、用例、CRUD、配置 | `ba-copilot/02.需求分析/2.5 & 2.6` |
| `ba-dependency-analysis` | `ba/dependency-analysis/` | 依赖、集成、外部系统 | `ba-copilot/02.需求分析/2.7依赖分析.md` |
| `ba-function-list` | `ba/function-list/` | 功能列表、功能分解 | `ba-copilot/02.需求分析/2.8功能列表梳理.md` |
| `ba-qa-identification` | `ba/qa-identification/` | Q&A、待澄清问题、歧义 | `ba-copilot/02.需求分析/2.9.Q&A识别.md` |
| `ba-ui-generation` | `ba/ui-generation/` | UI 原型、表单、大屏、HTML | `ba-copilot/03.UI生成/` |
| `ba-state-diagram` | `ba/state-diagram/` | 状态机、生命周期、PlantUML 状态图 | `ba-copilot/05.需求表达/5.0 & 5.1` |
| `ba-decision-matrix` | `ba/decision-matrix/` | 决策规则、判定标准 | `ba-copilot/05.需求表达/5.2 & 5.9` |
| `ba-validation-rules` | `ba/validation-rules/` | 校验、后台校验、编号 | `ba-copilot/05.需求表达/5.3 & 5.6 & 5.10 & 5.11` |
| `ba-permission-matrix` | `ba/permission-matrix/` | RBAC、权限、数据访问 | `ba-copilot/05.需求表达/5.15 & 5.16` |
| `ba-scheduled-tasks` | `ba/scheduled-tasks/` | 定时任务、文件导入、文件导出 | `ba-copilot/05.需求表达/5.12 & 5.13 & 5.14` |
| `ba-calendar-view` | `ba/calendar-view/` | 日历、资源排程 | `ba-copilot/06.资源时间模型/` |
| `ba-quality-scan` | `ba/quality-scan/` | 需求质量、完整性检查 | `ba-copilot/07.需求质量扫描/7.1` |
| `ba-story-splitting` | `ba/story-splitting/` | 用户故事、拆分、分解 | `ba-copilot/08.需求计划/8.1` |
| `ba-story-estimation` | `ba/story-estimation/` | 估算、故事地图、Sprint 排期 | `ba-copilot/08.需求计划/8.2 & 8.3` |
| `ba-impact-analysis` | `ba/impact-analysis/` | 变更影响、数据模型、UI、依赖 | `ba-copilot/09.需求开发/` |
| `ba-acceptance` | `ba/acceptance/` | 验收标准、验证 | `ba-copilot/10.需求验收/10.1` |

## Arch Copilot Skills（`skills/arch/`）

| Skill | 路径 | 关键词 | 源文件 |
|-------|------|--------|--------|
| `arch-tech-selection` | `arch/tech-selection/` | 技术选型、ADR、对比矩阵 | `arch-copilot/01.技术方案设计/1.1` |
| `arch-system-design` | `arch/system-design/` | 系统架构、模块、部署 | `arch-copilot/01.技术方案设计/1.2` |
| `arch-domain-model` | `arch/domain-model/` | DDD、限界上下文、聚合、ER 图、数据库 | `arch-copilot/02.数据模型设计/` |
| `arch-api-design` | `arch/api-design/` | REST API、端点、请求响应 | `arch-copilot/03.接口设计/3.1` |
| `arch-review-checklist` | `arch/review-checklist/` | 架构评审、可扩展性、安全性 | `arch-copilot/04.架构评审/4.1` |

## QA Agent Skills（`skills/qa/`）

| Skill | 路径 | 关键词 | 源文件 |
|-------|------|--------|--------|
| `qa-test-strategy` | `qa/test-strategy/` | 测试策略、测试级别、通过标准 | `qa-agent/01.测试策略/1.1` |
| `qa-regression-scope` | `qa/regression-scope/` | 回归测试、变更影响、测试范围 | `qa-agent/02.回归测试/2.1` |
| `qa-performance-test` | `qa/performance-test/` | 性能测试、负载测试、SLA | `qa-agent/03.性能测试/3.1` |
| `qa-test-environment` | `qa/test-environment/` | 测试环境、测试数据、环境供给 | `qa-agent/04.测试环境与数据/4.1` |

## Review Agent Skills（`skills/review/`）

| Skill | 路径 | 关键词 | 源文件 |
|-------|------|--------|--------|
| `review-code-standards` | `review/code-standards/` | 代码评审、命名、结构、错误处理 | `review-agent/01.代码规范/1.1` |
| `review-security-scan` | `review/security-scan/` | 安全扫描、注入、XSS、OWASP | `review-agent/02.安全扫描/2.1` |
| `review-compliance-audit` | `review/compliance-audit/` | 合规、隐私、许可证、审计 | `review-agent/03.合规审计/3.1` |

## SM Agent Skills（`skills/sm/`）

| Skill | 路径 | 关键词 | 源文件 |
|-------|------|--------|--------|
| `sm-story-estimation` | `sm/story-estimation/` | 故事点、斐波那契、Sprint 容量 | `sm-agent/01.估算模型/1.1` |
| `sm-sprint-retrospective` | `sm/sprint-retrospective/` | 回顾、指标、改进项 | `sm-agent/02.Sprint管理/2.1` |
| `sm-risk-alert` | `sm/risk-alert/` | 风险、告警、阻塞、延期、升级 | `sm-agent/03.风险预警/3.1` |
| `sm-knowledge-feedback` | `sm/knowledge-feedback/` | 知识库、反馈循环、持续学习 | `sm-agent/04.知识反馈/` |

## Flow Agent Skills（`skills/flow/`）

| Skill | 路径 | 关键词 | 源文件 |
|-------|------|--------|--------|
| `flow-sprint-lifecycle` | `flow/sprint-lifecycle/` | Sprint 状态机、阶段转换 | `flow-agent/01.状态机定义/1.1` |
| `flow-story-state-machine` | `flow/story-state-machine/` | Story 流转、回滚、熔断、升级 | `flow-agent/01.状态机定义/1.2` |
| `flow-confirmation-rules` | `flow/confirmation-rules/` | 人工确认、阻塞、异步、自动通过 | `flow-agent/02.编排规则/2.1` |
| `flow-timeout-handling` | `flow/timeout-handling/` | 超时、重试、异常、恢复 | `flow-agent/02.编排规则/2.2` |
| `flow-data-contracts` | `flow/data-contracts/` | 数据契约、Schema 校验、JSON Schema | `flow-agent/02.编排规则/2.3` |
