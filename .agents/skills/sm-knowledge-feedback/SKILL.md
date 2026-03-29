---
name: sm-knowledge-feedback
description: >
  Use when distributing improvement items from Sprint retrospective
  to each role's knowledge base. Categorizes improvements and generates
  knowledge entries for continuous learning across Sprints.
---

# Knowledge Feedback Distribution

## Workflow

1. Read retrospective improvement items
2. Categorize by target role:
   - Requirement issues → BA Copilot rules
   - Architecture issues → Arch Copilot rules + ADR
   - Coding issues → Code Agent steering rules
   - Review issues → Review Agent rules
   - Testing issues → QA Agent test strategy
   - Estimation issues → SM Agent estimation model
   - Process issues → Flow Agent orchestration rules
3. Generate knowledge entry drafts
4. Submit for PO confirmation
5. Write confirmed entries to target role's knowledge base

## Input

- Retrospective improvement items

## Output

- Knowledge entries per role, changelog updates

## Source Reference

See `sm-agent/04.知识反馈/4.1.改进项提取与分发.md` and `sm-agent/04.知识反馈/4.2.知识库变更日志.md`.
