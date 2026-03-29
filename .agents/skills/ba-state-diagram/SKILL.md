---
name: ba-state-diagram
description: >
  Use when generating state lifecycle diagrams from business processes.
  Creates PlantUML state diagrams decomposed by lifecycle phases
  with transitions and trigger conditions.
---

# State Diagram Generation

## Workflow

1. Read business processes and status list
2. Extract all states using past-tense naming convention
3. Map transitions with trigger conditions
4. Decompose into phase-based independent diagrams
5. Generate PlantUML state diagram code per phase

## Input

- Business process flows
- Status list

## Output

- PlantUML state diagrams (one per lifecycle phase)

## Source Reference

See `ba-copilot/05.需求表达/5.0.状态梳理.md` and `ba-copilot/05.需求表达/5.1.状态图.md`.
