---
name: review-code-standards
description: >
  Use when reviewing code changes for coding standard compliance.
  Checks naming conventions, code structure, comments, error handling,
  and outputs a structured review report.
---

# Code Standards Review

## Workflow

1. Read the code diff and project tech stack
2. Check naming conventions (class, method, variable, constant, file, DB field)
3. Check code structure (method length, class length, params, nesting, complexity)
4. Check comments and documentation (public API docs, complex logic, TODOs)
5. Check error handling (empty catch, exception granularity, resource release)
6. Output review report with file, line, severity, and fix suggestions

## Input

- Code diff, project tech stack

## Output

- Code review report table

## Source Reference

See `review-agent/01.代码规范/1.1.代码规范检查规则.md` for the full prompt template.
