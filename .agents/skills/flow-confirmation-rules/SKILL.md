---
name: flow-confirmation-rules
description: >
  Use when managing human confirmation nodes in the workflow.
  Defines three confirmation levels: blocking, async, and auto-approve.
  Handles timeout, delegation, and batch confirmation.
---

# Human Confirmation Node Rules

## Confirmation Levels

- Blocking: PO must explicitly approve (Sprint Goal, Story split, acceptance)
- Async: Flow continues, PO reviews in parallel, reject triggers rollback
- Auto-approve: Passes automatically if preset conditions met, PO can veto

## Workflow

1. Determine confirmation level for current node
2. For blocking: pause and wait for PO response
3. For async: continue flow, send confirmation request to PO
4. For auto-approve: check conditions, auto-pass or escalate to blocking
5. Handle timeout per level (8h/24h blocking, 24h async auto-pass)
6. Support batch confirmation and delegation

## Input

- Node ID, confirmation content, AI confidence score

## Output

- Confirmation result (pass/reject/partial/defer)

## Source Reference

See `flow-agent/02.编排规则/2.1.人工确认节点规则.md` for the full definition.
