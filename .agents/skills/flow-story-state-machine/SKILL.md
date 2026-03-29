---
name: flow-story-state-machine
description: >
  Use when managing individual Story task flow during Sprint execution.
  Handles Code → Review → QA → Doc/Deploy pipeline with rollback,
  circuit-breaking, and escalation levels (L0-L4).
---

# Story Task State Machine

## Workflow

1. Trigger Code Agent for implementation
2. On completion, trigger Review Agent
3. If review rejected → rollback to Code Agent (increment counter)
4. If review passed → trigger QA Agent
5. If test failed → rollback to Code Agent (increment counter)
6. If test passed → parallel trigger Doc Agent + DevOps Agent
7. Monitor rollback counter for escalation:
   - L0: Normal rollback
   - L1: Require root cause analysis
   - L2: Alert PO (pattern detection)
   - L3: Pull in BA/Arch for diagnosis
   - L4: Circuit break (pause, PO decides)

## Input

- Story ID, Sprint ID, task assignments

## Output

- Story state transitions, rollback records, escalation alerts

## Source Reference

See `flow-agent/01.状态机定义/1.2.Story任务状态机.md` for the full definition.
