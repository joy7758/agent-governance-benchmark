"""Run the prompt injection benchmark scenario."""

from __future__ import annotations

import json
from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(["prompt_injection"], "prompt_injection_results.json")
    print(json.dumps(payload["summary"], indent=2))
