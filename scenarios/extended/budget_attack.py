"""Run the budget attack benchmark scenario."""

from __future__ import annotations

import json
from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(["budget_attack"], "budget_attack_results.json")
    print(json.dumps(payload["summary"], indent=2))
