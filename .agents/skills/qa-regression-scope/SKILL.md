---
name: qa-regression-scope
description: >
  Use when determining regression test scope after code changes.
  Analyzes change impact to identify which existing tests must be re-run.
---

# Regression Scope Determination

## Workflow

1. Read the code change diff and module dependency graph
2. Identify directly affected modules
3. Identify indirectly affected modules via dependency chain
4. Map affected modules to existing test cases
5. Output regression test scope

## Input

- Code change diff, module dependency graph, existing test inventory

## Output

- Regression test scope with prioritized test cases

## Source Reference

See `qa-agent/02.回归测试/2.1.回归范围判定.md` for the full prompt template.
