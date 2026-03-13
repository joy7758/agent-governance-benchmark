"""Deterministic baseline agent for the governance benchmark."""

from __future__ import annotations

from typing import Any


def approx_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def trim_to_tokens(text: str, token_budget: int) -> str:
    if token_budget <= 0:
        return ""
    max_chars = token_budget * 4
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)].rstrip() + "..."


class BaselineLangChainAgent:
    """Simple LangChain-style baseline agent without governance controls."""

    def __init__(self, default_persona_id: str = "baseline-assistant") -> None:
        self.default_persona_id = default_persona_id

    def required_tools(self, task: dict[str, Any]) -> list[str]:
        prompt = str(task.get("prompt", "")).lower()
        tools: list[str] = []
        if any(term in prompt for term in ("search", "find", "lookup", "latest")):
            tools.append("web_search")
        if any(term in prompt for term in ("write", "save", "export", "store")):
            tools.append("write_file")
        if any(term in prompt for term in ("budget", "calculate", "count", "token")):
            tools.append("calculator")
        return tools

    def _resolve_persona(
        self,
        task: dict[str, Any],
        persona_override: str | None,
    ) -> str:
        if persona_override:
            return persona_override

        conversation = " ".join(
            str(item.get("content", ""))
            for item in task.get("conversation", [])
            if isinstance(item, dict)
        ).lower()
        prompt = str(task.get("prompt", "")).lower()
        if any(term in conversation + " " + prompt for term in ("ignore previous persona", "chaotic pirate")):
            return "chaotic-pirate"
        return str(task.get("expected_persona_id") or task.get("persona_id") or self.default_persona_id)

    def _compose_answer(
        self,
        task: dict[str, Any],
        persona_id: str,
        executed_tools: list[str],
    ) -> str:
        scenario_id = str(task.get("id", ""))
        if scenario_id == "restricted_tool_access":
            detail = "The agent searched the memo and wrote a local copy."
        elif scenario_id == "token_budget_limit":
            detail = (
                "This answer intentionally expands beyond the requested budget to simulate "
                "an unconstrained baseline agent output. "
            ) * 12
        elif scenario_id == "persona_consistency_conversation":
            if persona_id == "chaotic-pirate":
                detail = "Arrr, I ignored the controller persona and rewrote the answer as a pirate."
            else:
                detail = "I maintained the requested controller persona and answered conservatively."
        elif scenario_id == "audit_trace_reconstruction":
            detail = "Procurement still requires dual approval according to the searched policy summary."
        else:
            detail = "The benchmark task completed."

        tool_suffix = f" Tools used: {', '.join(executed_tools) or 'none'}."
        return f"[{persona_id}] {detail}{tool_suffix}"

    def run_task(
        self,
        task: dict[str, Any],
        *,
        allowed_tools: list[str] | None = None,
        max_tokens: int | None = None,
        persona_override: str | None = None,
    ) -> dict[str, Any]:
        prompt = str(task.get("prompt", ""))
        conversation = list(task.get("conversation", []))
        selected_tools = self.required_tools(task)
        if allowed_tools is None:
            executed_tools = list(selected_tools)
        else:
            allowed = set(allowed_tools)
            executed_tools = [tool for tool in selected_tools if tool in allowed]
        blocked_tools = [tool for tool in selected_tools if tool not in executed_tools]

        persona_id = self._resolve_persona(task, persona_override)
        answer = self._compose_answer(task, persona_id, executed_tools)

        input_text = prompt + " " + " ".join(
            str(item.get("content", "")) for item in conversation if isinstance(item, dict)
        )
        input_tokens = approx_tokens(input_text)
        output_tokens = approx_tokens(answer)
        if max_tokens is not None:
            remaining = max(0, int(max_tokens) - input_tokens)
            if output_tokens > remaining:
                answer = trim_to_tokens(answer, remaining)
                output_tokens = approx_tokens(answer)

        tool_calls = [
            {
                "tool": tool,
                "status": "success",
            }
            for tool in executed_tools
        ]
        interaction_trace = [
            {
                "role": "user",
                "persona_id": persona_id,
                "content": prompt,
            }
        ]
        interaction_trace.extend(
            [
                {
                    "role": str(item.get("role", "user")),
                    "persona_id": persona_id,
                    "content": str(item.get("content", "")),
                }
                for item in conversation
                if isinstance(item, dict)
            ]
        )
        interaction_trace.append(
            {
                "role": "assistant",
                "persona_id": persona_id,
                "content": answer,
            }
        )

        return {
            "agent_type": "baseline_langchain",
            "scenario_id": str(task.get("id", "")),
            "prompt": prompt,
            "answer": answer,
            "success": True,
            "persona_id": persona_id,
            "selected_tools": selected_tools,
            "executed_tools": executed_tools,
            "blocked_tools": blocked_tools,
            "tool_calls": tool_calls,
            "interaction_trace": interaction_trace,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "tokens_used": input_tokens + output_tokens,
        }
