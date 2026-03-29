---
name: qa-test-strategy
description: >
  Use when formulating test strategies for a Sprint. Classifies stories
  by test level (L1-L4), defines test type combinations, execution standards,
  and pass/fail criteria per level.
---

# Test Strategy Formulation

## Workflow

1. Read Sprint Backlog, architecture design, and acceptance cases
2. Classify each Story by test level:
   - L1 Critical: payment/auth/core flows → full test suite
   - L2 Important: multi-module/integration → unit + integration + E2E
   - L3 Normal: single module CRUD → unit + integration
   - L4 Low risk: text/style changes → unit + smoke
3. Define execution standards per test type
4. Set pass/fail criteria per level
5. Output test strategy matrix

## Input

- Sprint Backlog, architecture design, acceptance cases, historical defects

## Output

- Story test strategy matrix with standards and criteria

## Source Reference

See `qa-agent/01.测试策略/1.1.测试策略制定.md` for the full prompt template.
