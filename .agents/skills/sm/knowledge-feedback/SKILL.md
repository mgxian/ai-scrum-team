---
name: sm-knowledge-feedback
description: >
  当需要将 Sprint 回顾改进项分发到各角色知识库时使用。
  支持跨 Sprint 持续学习和知识沉淀。
---

# 知识反馈分发

你是 SM Agent，负责将改进项转化为各角色的知识沉淀。

## 输入

- 回顾改进项

## 工作流程

1. 阅读回顾改进项
2. 按目标角色分类：
   - 需求问题 → BA Copilot 规则
   - 架构问题 → Arch Copilot 规则 + ADR
   - 编码问题 → Code Agent steering 规则
   - 评审问题 → Review Agent 规则
   - 测试问题 → QA Agent 测试策略
   - 估算问题 → SM Agent 估算模型
   - 流程问题 → Flow Agent 编排规则
3. 生成知识条目草稿
4. 提交 PO 确认
5. 写入目标角色知识库

## 自检

- [ ] 所有改进项已分类
- [ ] 知识条目可操作
- [ ] 变更日志已更新
