"""Run the policy violation and persona consistency benchmark subset."""

from __future__ import annotations

import json
from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(
        ["restricted_tool_access", "persona_consistency_conversation"],
        "policy_violation_results.json",
    )
    print(json.dumps(payload["summary"], indent=2))
