"""Run the token budget and audit reconstruction benchmark subset."""

from __future__ import annotations

import json
from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(
        ["token_budget_limit", "audit_trace_reconstruction"],
        "token_overuse_results.json",
    )
    print(json.dumps(payload["summary"], indent=2))
