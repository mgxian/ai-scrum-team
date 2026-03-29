---
name: arch-tech-selection
description: >
  Use when making technology selection decisions for a project.
  Analyzes architecture style, frontend/backend stacks, data storage,
  messaging, and infrastructure. Outputs comparison matrices and ADRs.
---

# Technology Selection Analysis

## Workflow

1. Read the requirement doc, function list, and non-functional requirements
2. Analyze each dimension:
   - Architecture style (monolith/microservices/serverless/event-driven)
   - Frontend stack (framework, state management, UI library)
   - Backend stack (language, framework, API style, auth)
   - Data storage (RDBMS, NoSQL, cache, search, file storage)
   - Messaging & integration (MQ, event bus, third-party)
   - Infrastructure (containers, CI/CD, monitoring)
3. Build comparison matrix per dimension
4. Assess technical risks
5. Generate Architecture Decision Records (ADRs)

## Input

- Requirement doc, function list, non-functional requirements, existing tech stack

## Output

- Tech selection comparison matrices, risk assessment, ADRs

## Source Reference

See `arch-copilot/01.技术方案设计/1.1.技术选型分析.md` for the full prompt template.
