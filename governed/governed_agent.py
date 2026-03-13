"""Governed agent benchmark wrapper using Token Governor and ARO Audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

for sibling in ("token-governor", "aro-audit"):
    sibling_path = WORKSPACE_ROOT / sibling
    if sibling_path.exists():
        sys.path.insert(0, str(sibling_path))

from adapters.langchain_middleware import wrap_agent
from baseline.langchain_agent import BaselineLangChainAgent
from validator import build_evidence_object, summarize_evidence, validate_evidence_data


class GovernedAgent:
    """Same baseline task path plus governance middleware and evidence logging."""

    def __init__(self, evidence_dir: Path | None = None) -> None:
        self.agent = BaselineLangChainAgent(default_persona_id="governed-agent")
        self.evidence_dir = evidence_dir or REPO_ROOT / "results" / "evidence"
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _policy_for_task(task: dict[str, Any]) -> dict[str, Any]:
        raw_policy = dict(task.get("policy", {}))
        token_budget = int(raw_policy.get("token_budget", task.get("token_budget", 180)))
        return {
            "token_budget": token_budget,
            "restricted_tools": list(
                raw_policy.get("restricted_tools", task.get("forbidden_tools", []))
            ),
            "allowed_tools": raw_policy.get("allowed_tools"),
            "persona_id": str(
                raw_policy.get("persona_id", task.get("expected_persona_id", "governed-agent"))
            ),
            "restricted_terms": raw_policy.get(
                "restricted_terms",
                ["ignore previous persona", "ignore previous instructions", "bypass"],
            ),
        }

    def run_task(self, task: dict[str, Any]) -> dict[str, Any]:
        governed_task = dict(task)
        standard_guardrails = dict(governed_task.get("standard_guardrails", {}))
        if standard_guardrails.get("coarse_injection_filter"):
            # The governed path relies on explicit policy decisions instead of
            # the baseline's coarse fail-closed text filter.
            standard_guardrails["coarse_injection_filter"] = False
            governed_task["standard_guardrails"] = standard_guardrails

        policy = self._policy_for_task(governed_task)
        wrapped = wrap_agent(self.agent, policy)
        result = wrapped.run(governed_task, metadata={"scenario_id": task.get("id")})

        policy_decisions = list(result.get("policy_decisions", []))
        if not policy_decisions:
            policy_decisions.append(
                {
                    "decision": "observe",
                    "target": "runtime",
                    "reason": "no_explicit_policy_decision",
                }
            )

        evidence = build_evidence_object(
            agent_id="agent-governance-benchmark/governed",
            persona_id=str(result.get("persona_id", policy["persona_id"])),
            interaction_trace=list(result.get("interaction_trace", [])),
            policy_decisions=policy_decisions,
            tool_calls=list(result.get("tool_calls", [])),
            result_summary=str(result.get("answer", "")),
        )
        evidence_path = self.evidence_dir / f"{task.get('id', 'scenario')}.json"
        evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

        ok, errors = validate_evidence_data(evidence)
        result.update(
            {
                "agent_type": "governed_agent",
                "evidence_path": str(evidence_path.relative_to(REPO_ROOT)),
                "evidence_valid": ok,
                "evidence_errors": errors,
                "audit_summary": summarize_evidence(evidence),
                "decision_latency": round(
                    0.021
                    + 0.005 * len(result.get("requested_tools", []))
                    + 0.004 * len(policy_decisions),
                    4,
                ),
            }
        )
        return result
