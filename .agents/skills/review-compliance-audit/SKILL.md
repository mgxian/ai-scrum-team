---
name: review-compliance-audit
description: >
  Use when auditing code for regulatory and organizational compliance.
  Checks data privacy, logging standards, license compliance,
  and organizational policies.
---

# Compliance Audit

## Workflow

1. Read the code diff and compliance requirements
2. Check against compliance checklist:
   - Data privacy (PII handling, encryption, retention)
   - Logging standards (no sensitive data in logs)
   - License compliance (dependency licenses)
   - Organizational policies
3. Flag violations by severity
4. Output compliance audit report

## Input

- Code diff, compliance requirements

## Output

- Compliance audit report

## Source Reference

See `review-agent/03.合规审计/3.1.合规检查清单.md` for the full prompt template.
