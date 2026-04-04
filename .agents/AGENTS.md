# AI Scrum Team

An AI-powered Scrum team framework with 7 Agents + 2 Copilots + 1 Human PO.

## Roles

| Role | Name | Type | Responsibility |
|------|------|------|----------------|
| Orchestration | Flow Agent | Agent | End-to-end flow: Refinement → Planning → Execution → Review → Retrospective |
| Requirements | BA Copilot | Workflow + RAG | Requirement analysis, business rules, User Story splitting |
| Architecture | Arch Copilot | Workflow + RAG | Tech design, data modeling, API design |
| Development | Code Agent | Agent | Coding + unit testing + debugging |
| Testing | QA Agent | Agent | E2E, integration, regression, performance testing |
| Code Review | Review Agent | Lightweight Agent | Code standards, security scanning, compliance |
| Scrum Master | SM Agent | Agent | Estimation, Sprint planning, risk alerts, retrospective |
| Product Owner | Human | — | Decision-making, confirmation, acceptance |

## Workflow

```
Backlog Refinement → Sprint Planning → Sprint Execution → Sprint Review → Sprint Retrospective
```

## Data Passing

All artifacts stored in repo. Flow Agent passes lightweight trigger signals, each role reads context by sprint/story ID.

## Skill Organization

Skills in `.agents/skills/` are organized by role subdirectory (`ba/`, `arch/`, `qa/`, `review/`, `sm/`, `flow/`), mirroring the role-based structure. Source prompt templates live in `ba-copilot/`, `arch-copilot/`, etc. Each SKILL.md references the original source files.

## Full Documentation

See [AI-Scrum-Team.md](../AI-Scrum-Team.md) for complete design documentation (Chinese).
