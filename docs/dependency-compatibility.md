# Dependency Compatibility

`agent-governance-benchmark` consumes canonical package surfaces from the core repos after their boundary cleanup.

## Canonical module paths

- `token-governor`
  - runtime adapter used by the harness: `adapters.langchain_middleware`
  - canonical CLI surface expected to exist: `governor.cli`
- `aro-audit`
  - audit validation surface: `aro_audit.validation`
- `fdo-kernel-mvk`
  - optional verification surface when a scenario explicitly uses execution-integrity checks: `kernel.verify`

## Fallback order

1. Installed package import resolution
2. Environment variable override
3. Sibling repo discovery

Environment variables:

- `TOKEN_GOVERNOR_REPO`
- `ARO_AUDIT_REPO`

Sibling repo defaults:

- workspace-local `token-governor`
- workspace-local `aro-audit`

## Expected markers for sibling fallback

- `token-governor`
  - `adapters/langchain_middleware.py`
  - `governor/cli.py`
- `aro-audit`
  - `aro_audit/validation.py`

## Retired entrypoints

The benchmark no longer assumes legacy root-level entrypoints in the governance, audit, or MVK repos. Compatibility now follows the package surfaces and markers listed above.
