---
name: flow-data-contracts
description: >
  Use when validating data handoffs between roles in the workflow.
  Defines JSON schema contracts for each role-to-role data transfer.
  Handles schema validation, missing fields, type mismatches.
---

# Data Transfer Contracts

## Workflow

1. Before each role handoff, validate output against contract schema
2. Check: required fields present, types match, enums valid, logic consistent
3. If validation fails → block transfer, return error details to upstream
4. If validation passes → allow downstream to proceed

## Key Contracts

- PO → BA: original requirement schema
- BA → SM: requirements doc + user stories
- Arch → SM: tech design + domain model + API design
- SM → Code Agent: task assignments
- Code → Review: code submission + unit test report
- Review → QA: review report
- QA → Doc/Code: test report
- SM → PO: retrospective report

## Input

- Upstream role output data

## Output

- Validation result (pass/fail with error details)

## Source Reference

See `flow-agent/02.编排规则/2.3.数据传递契约.md` for all contract schemas.
