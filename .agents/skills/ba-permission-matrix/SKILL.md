---
name: ba-permission-matrix
description: >
  Use when designing role-based access control and data permission rules.
  Generates role-permission matrices and data-level access policies.
---

# Permission Matrix

## Workflow

1. Read the role list and function list
2. Map each role to allowed functions (CRUD level)
3. Define data-level permission rules (row/column filtering)
4. Output role-permission matrix and data permission rules

## Input

- Role list, function list

## Output

- Role-permission matrix, data permission rules

## Source Reference

See `ba-copilot/05.需求表达/5.15.角色权限矩阵.md` and `ba-copilot/05.需求表达/5.16.数据权限.md`.
