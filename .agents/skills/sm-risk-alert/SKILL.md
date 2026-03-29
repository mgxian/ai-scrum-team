---
name: sm-risk-alert
description: >
  Use when monitoring Sprint progress and identifying risks.
  Detects excessive rollbacks, task delays, blocked stories,
  and triggers escalation alerts.
---

# Risk Alert

## Workflow

1. Monitor Sprint execution metrics in real-time
2. Detect risk signals:
   - Excessive rollbacks on a single story
   - Task delays beyond scheduled dates
   - Blocked stories without resolution
   - Quality metric degradation
3. Classify risk level and determine escalation path
4. Generate risk alert with recommended actions

## Input

- Sprint execution data, task status, rollback history

## Output

- Risk alerts with severity and recommended actions

## Source Reference

See `sm-agent/03.风险预警/3.1.风险预警规则.md` for the full prompt template.
