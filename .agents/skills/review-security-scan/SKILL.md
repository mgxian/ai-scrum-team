---
name: review-security-scan
description: >
  Use when performing security scanning on code changes.
  Checks for injection vulnerabilities, authentication issues,
  data exposure, and OWASP Top 10 compliance.
---

# Security Scan

## Workflow

1. Read the code diff
2. Scan for security vulnerabilities:
   - SQL/NoSQL injection
   - XSS and CSRF
   - Authentication and authorization flaws
   - Sensitive data exposure
   - Insecure dependencies
3. Classify findings by severity (high/medium/low)
4. Output security scan report

## Input

- Code diff

## Output

- Security scan report with findings and remediation suggestions

## Source Reference

See `review-agent/02.安全扫描/2.1.安全扫描规则.md` for the full prompt template.
