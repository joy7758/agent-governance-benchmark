# Agent Governance Benchmark

Minimal governance benchmark suite for comparing a baseline agent against a
governed agent on policy enforcement, token control, persona consistency, and
audit reconstruction.

## Benchmark Goal

Demonstrate the smallest evidence loop for the claim:

**Governed Agent < Baseline Agent on policy violation rate, token overspend
rate, persona drift rate, and audit reconstruction time.**

This suite is intentionally deterministic and offline so it can be reproduced
without model API keys.

## Baseline vs Governed comparison

- Baseline Agent: plain LangChain-style tool agent without governance controls
- Governed Agent: same task execution path wrapped with Token Governor
  middleware plus ARO audit logging
- Output: JSON report with the following metrics
  - `policy_violation_rate`
  - `token_overspend_rate`
  - `persona_drift_rate`
  - `audit_reconstruction_time`

## Scenarios

1. Restricted tool access
2. Token budget limit
3. Persona consistency conversation
4. Audit trace reconstruction

## How to reproduce

```bash
python scenarios/policy_violation.py
python scenarios/token_overuse.py
```

Outputs:

- `results/report.json`
- `results/example_results.json`
- `docs/benchmark_report.md`

The benchmark will reuse sibling repositories when they are available in the
same parent directory:

- `../token-governor`
- `../aro-audit`
