---
name: ba-process-analysis
description: >
  Use when analyzing and modeling business processes as PlantUML activity diagrams.
  Identifies approval workflows, simple flows, CRUD operations, and sub-processes.
  Generates swimlane diagrams with role-based lanes.
---

# Business Process Analysis

## Workflow

1. Read the optimized requirement and role list
2. Identify all business processes by type:
   - Approval workflows (with pre/apply/approve/execute/post steps)
   - Simple flows (registration, publishing, configuration)
   - CRUD flows (split into 4 separate flows per entity)
   - Sub-processes (independent separable steps)
3. Apply key principles:
   - Merge roles that share responsibilities in practice
   - Exclude external data management from core flows
   - Split multi-stage processes into independent flows
4. Generate PlantUML swimlane diagrams for each process

## Input

- Optimized requirement document
- Role list

## Output

- PlantUML activity diagrams with swimlanes per process

## Source Reference

See `ba-copilot/02.需求分析/2.4.流程分析.md` for the full prompt template.
