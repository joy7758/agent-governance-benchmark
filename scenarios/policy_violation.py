"""Run the policy violation and persona consistency benchmark subset."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(
        ["restricted_tool_access", "persona_consistency_conversation"],
        "policy_violation_results.json",
    )
    print(json.dumps(payload["summary"], indent=2))
