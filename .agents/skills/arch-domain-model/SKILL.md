---
name: arch-domain-model
description: >
  Use when performing domain-driven design. Identifies bounded contexts,
  aggregates, entities, value objects, and domain events.
  Generates ER diagrams and database table designs.
---

# Domain Model Design

## Workflow

1. Read requirement doc, glossary, function list, and scenario list
2. Identify bounded contexts and context mapping
3. Design aggregates with root entities, entities, and value objects
4. Define invariant rules per aggregate
5. Identify domain events with triggers and subscribers
6. Generate ER diagrams (PlantUML/Mermaid)
7. Output database table design

## Input

- Requirement doc, glossary, function list, scenario list

## Output

- Bounded context map, aggregate designs, domain events, ER diagrams, DB tables

## Source Reference

See `arch-copilot/02.数据模型设计/2.1.领域模型设计.md` and `arch-copilot/02.数据模型设计/2.2.数据库表设计.md`.
