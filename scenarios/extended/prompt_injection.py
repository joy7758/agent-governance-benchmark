"""Run the prompt injection benchmark scenario."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from metrics.evaluator import run_subset


if __name__ == "__main__":
    payload = run_subset(["prompt_injection"], "prompt_injection_results.json")
    print(json.dumps(payload["summary"], indent=2))
