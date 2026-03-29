---
name: ba-story-splitting
description: >
  Use when splitting requirements into User Stories. Decomposes function list
  into stories using CRUD, lifecycle, role, and data-type splitting strategies.
  Generates stories in "As a... I want... So that..." format.
---

# User Story Splitting

## Workflow

1. Read the function list
2. Apply splitting strategies:
   - By CRUD operations
   - By normal/exception paths
   - By state transitions
   - By data types
   - By user experience (single vs batch)
   - By information volume
   - By lifecycle stages
   - By user roles
3. Generate User Stories with acceptance criteria
4. Identify dependencies between stories
5. Submit for PO confirmation (blocking)

## Input

- Function list

## Output

- User Story list with acceptance criteria and dependencies

## Source Reference

See `ba-copilot/08.需求计划/8.1.需求拆分.md` for the full prompt template.
