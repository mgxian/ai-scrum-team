# AI Scrum Team

An AI-powered Scrum team framework that orchestrates multiple AI agents to drive the full software development lifecycle — from requirement analysis to deployment and retrospective.

## Roles

| Role | Name | Type | Responsibility |
|------|------|------|----------------|
| Orchestration | Flow Agent | Agent | Drives end-to-end flow: Refinement → Planning → Execution → Review → Retrospective |
| Requirements | BA Copilot | Workflow + RAG | Requirement refinement, business rule analysis, User Story splitting |
| Architecture | Arch Copilot | Workflow + RAG | Technical design, data modeling, API design |
| Development | Code Agent | Agent | Coding + unit testing + debugging |
| Testing | QA Agent | Agent | E2E, integration, regression, performance testing |
| Code Review | Review Agent | Lightweight Agent | Code standards, security scanning, compliance audit |
| Documentation | Doc Agent | Agent | Auto-tracks code changes, maintains API docs and changelogs |
| Scrum Master | SM Agent | Agent | Sprint planning, estimation, progress tracking, risk alerts, retrospective |
| DevOps | DevOps Agent | Agent | CI/CD, automated deployment, monitoring, environment management |
| Product Owner | Human | — | Decision-making, confirmation, acceptance |

> 7 Agents + 2 Copilots + 1 Human PO = 10 roles.
> Naming convention: autonomous decision-making → Agent; fixed steps with human confirmation → Copilot.

## Workflow Overview

```
Backlog Refinement → Sprint Planning → Sprint Execution → Sprint Review → Sprint Retrospective
```

1. **Refinement** — PO submits requirements → BA Copilot analyzes in stages (with PO confirmation gates) → Story splitting → SM estimation → Product Backlog
2. **Planning** — SM Agent prioritizes → PO selects Sprint Goal → Arch Copilot designs → SM assigns tasks → Sprint Backlog
3. **Execution** — Code Agent → Review Agent → QA Agent → (parallel) Doc Agent + DevOps Agent. Failed reviews/tests trigger rollback to Code Agent with escalation levels (L0–L4).
4. **Review** — DevOps deploys to demo env → PO acceptance
5. **Retrospective** — SM Agent analyzes Sprint metrics → generates improvement items → PO confirms → knowledge feedback distributed to each role's rules/knowledge base

## Key Mechanisms

- **Flow Agent** orchestrates via state machines (Sprint lifecycle + Story task flow) with rollback, circuit-breaking, and tiered human confirmation (blocking / async / auto-approve)
- **Knowledge Feedback Loop** — retrospective improvements are written back into each role's rules and knowledge base, enabling cross-Sprint continuous learning
- **Data Passing** — all artifacts stored in repo; Flow Agent passes lightweight trigger signals (not data), each role reads context by sprint/story ID
- **Parallel Execution** — multiple stories can flow through different stages concurrently

## Project Structure

```
.
├── AI-Scrum-Team.md          # Full design doc (Chinese)
├── ba-copilot/               # BA workflow: 10 phases of requirement analysis
├── arch-copilot/             # Architecture design workflow
├── flow-agent/               # State machines + orchestration rules
├── flow-engine-crewai/       # CrewAI-based flow engine implementation
├── sm-agent/                 # Estimation, Sprint mgmt, risk alerts, knowledge feedback
├── qa-agent/                 # Test strategy, regression, performance
├── review-agent/             # Code standards, security scanning, compliance
└── convert_rtf_to_md.py      # Utility script
```

## Getting Started

This repo contains the prompt templates, workflow definitions, and orchestration rules for the AI Scrum Team. To integrate into a real project:

1. Add this repo as a git submodule under `.ai-scrum/`
2. Create runtime directories (`docs/`, `sprints/`, `knowledge/`) in your project
3. Configure the CrewAI flow engine (`flow-engine-crewai/`)

See [AI-Scrum-Team.md](AI-Scrum-Team.md) for the complete design documentation.

## License

MIT
