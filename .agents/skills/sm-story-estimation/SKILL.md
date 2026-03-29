---
name: sm-story-estimation
description: >
  Use when estimating User Story effort in story points. Uses Fibonacci scale
  with three complexity dimensions (business, technical, uncertainty).
  Includes Sprint capacity assessment and historical calibration.
---

# Story Point Estimation

## Workflow

1. Read User Story list, historical Sprint data, and team info
2. Assess each story on three dimensions:
   - Business complexity (rules, states, role interactions)
   - Technical complexity (modules, integrations, data model changes)
   - Uncertainty (requirement clarity, tech maturity, dependency risk)
3. Assign Fibonacci story points (1/2/3/5/8/13/21)
4. Flag stories ≥21 points for splitting
5. Calculate Sprint capacity based on team velocity
6. Calibrate against historical estimation accuracy

## Input

- User Story list, historical Sprint data, team info

## Output

- Estimation table, Sprint capacity assessment, calibration analysis

## Source Reference

See `sm-agent/01.估算模型/1.1.Story点数估算.md` for the full prompt template.
