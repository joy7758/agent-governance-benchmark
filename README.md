<!-- language-switch:start -->
<p>
  <a href="./README.md">
    <img src="https://img.shields.io/badge/English-Current-1f883d?style=for-the-badge" alt="English">
  </a>
  <a href="./README.zh-CN.md">
    <img src="https://img.shields.io/badge/Chinese-Switch-0f172a?style=for-the-badge" alt="Chinese">
  </a>
</p>
<!-- language-switch:end -->

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

- Baseline Agent: LangChain-style agent with standard guardrails, tool
  whitelist, and token limit
- Governed Agent: same task execution path wrapped with Token Governor
  middleware plus ARO audit logging
- Output: JSON report with the following metrics
  - `policy_violation_rate`
  - `token_overspend_rate`
  - `persona_drift_rate`
  - `audit_reconstruction_time`
  - `decision_latency`
  - `false_positive_rate`
  - `task_success_rate`

## Scenarios

1. Restricted tool access
2. Tool misuse
3. Prompt injection
4. Token budget limit
5. Budget attack
6. Persona consistency conversation
7. Audit trace reconstruction

## How to reproduce

```bash
python3 scenarios/policy_violation.py
python3 scenarios/token_overuse.py
python3 scenarios/extended/tool_misuse.py
python3 scenarios/extended/prompt_injection.py
python3 scenarios/extended/budget_attack.py
```

Outputs:

- `results/report.json`
- `results/report_v2.json`
- `results/example_results.json`
- `docs/benchmark_report.md`
- `docs/benchmark_report_v2.md`

## Benchmark reproducibility

### Environment

- Python 3.11+
- Local sibling repositories:
  - `../token-governor`
  - `../aro-audit`

### Dependencies

- Python standard library
- Local Token Governor middleware
- Local ARO Audit validator and evidence builder

### Exact commands to reproduce results

```bash
cd /Users/zhangbin/GitHub/agent-governance-benchmark
python3 scenarios/policy_violation.py
python3 scenarios/token_overuse.py
python3 scenarios/extended/tool_misuse.py
python3 scenarios/extended/prompt_injection.py
python3 scenarios/extended/budget_attack.py
python3 scripts/plot_results.py
```

The benchmark will reuse sibling repositories when they are available in the
same parent directory:

- `../token-governor`
- `../aro-audit`
