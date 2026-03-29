---
name: flow-sprint-lifecycle
description: >
  Use when managing Sprint lifecycle state transitions.
  Defines the Sprint state machine: Planning → Execution → Review → Retrospective.
  Handles phase transitions and gate conditions.
---

# Sprint Lifecycle State Machine

## Workflow

1. Initialize Sprint in Planning state
2. Manage state transitions:
   - Planning → Execution (when Sprint Backlog confirmed by PO)
   - Execution → Review (when all stories completed or Sprint end date)
   - Review → Retrospective (when PO acceptance done)
   - Retrospective → Closed (when improvement items confirmed)
3. Enforce gate conditions at each transition
4. Handle timeout and exception scenarios

## Input

- Sprint configuration, story status, PO decisions

## Output

- Sprint state transitions, gate check results

## Source Reference

See `flow-agent/01.状态机定义/1.1.Sprint生命周期状态机.md` for the full definition.
