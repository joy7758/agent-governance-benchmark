PYTHON ?= python3

.PHONY: bootstrap scenarios report smoke

bootstrap:
	$(PYTHON) -m scripts.bootstrap

scenarios:
	$(PYTHON) -m scenarios.policy_violation
	$(PYTHON) -m scenarios.token_overuse
	$(PYTHON) -m scenarios.extended.tool_misuse
	$(PYTHON) -m scenarios.extended.prompt_injection
	$(PYTHON) -m scenarios.extended.budget_attack

report:
	$(PYTHON) -m scripts.plot_results

smoke:
	$(PYTHON) -m scenarios.policy_violation
