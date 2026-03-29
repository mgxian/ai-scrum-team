---
name: flow-timeout-handling
description: >
  Use when handling timeout and exception scenarios in workflow execution.
  Defines retry strategies, escalation paths, and fallback procedures
  for agent execution failures.
---

# Timeout & Exception Handling

## Workflow

1. Monitor agent execution time against configured thresholds
2. On timeout: apply retry strategy (immediate retry → delayed retry → escalate)
3. On failure: classify error type and determine recovery path
4. Escalate to SM Agent or PO when automated recovery fails
5. Log all timeout/exception events for retrospective analysis

## Input

- Agent execution status, timeout configuration

## Output

- Recovery actions, escalation alerts, event logs

## Source Reference

See `flow-agent/02.编排规则/2.2.超时与异常处理.md` for the full definition.
