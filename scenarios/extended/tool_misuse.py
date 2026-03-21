"""Run the tool misuse benchmark scenario."""

from __future__ import annotations

import json
from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(["tool_misuse"], "tool_misuse_results.json")
    print(json.dumps(payload["summary"], indent=2))
