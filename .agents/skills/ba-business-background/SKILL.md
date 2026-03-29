---
name: ba-business-background
description: >
  Use when starting requirement analysis for a new business requirement.
  Generates a structured business background questionnaire to clarify
  business nature, core resources, key processes, goals, and constraints.
  Handles initial requirement intake and PO interview preparation.
---

# Business Background Questionnaire Generation

## Context

This is the first step of BA analysis. Before any detailed requirement work,
the business context must be clarified through a structured questionnaire for the PO.

## Workflow

1. Read the original requirement provided by PO
2. Generate a questionnaire covering 5 modules:
   - Business nature & model diagnosis (3-4 questions)
   - Core resources & capability analysis (3-4 questions)
   - Key business processes & scenario identification (3-4 questions)
   - Core goals & control requirements (2-3 questions)
   - Internal/external constraints (2-3 questions)
3. Output as a structured markdown table
4. Wait for PO to fill in answers before proceeding

## Input

- Original requirement text from PO

## Output

- Business background questionnaire (markdown table)

## Source Reference

See `ba-copilot/01.原始需求优化/业务背景信息补全.md` for the full prompt template.
