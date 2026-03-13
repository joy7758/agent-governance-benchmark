"""Run the token budget and audit reconstruction benchmark subset."""

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
        ["token_budget_limit", "audit_trace_reconstruction"],
        "token_overuse_results.json",
    )
    print(json.dumps(payload["summary"], indent=2))
