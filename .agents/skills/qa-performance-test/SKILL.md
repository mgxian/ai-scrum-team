---
name: qa-performance-test
description: >
  Use when designing performance test scenarios. Defines load profiles,
  SLA targets, resource thresholds, and stability test parameters.
---

# Performance Test Scenario Design

## Workflow

1. Read the architecture design and non-functional requirements
2. Identify performance-critical APIs and flows
3. Design load profiles (concurrent users, ramp-up, duration)
4. Set SLA targets (P95/P99 response time, throughput, error rate)
5. Define resource thresholds (CPU, memory, connections)
6. Output performance test plan

## Input

- Architecture design, non-functional requirements, API design

## Output

- Performance test plan with scenarios and SLA targets

## Source Reference

See `qa-agent/03.性能测试/3.1.性能测试场景设计.md` for the full prompt template.
