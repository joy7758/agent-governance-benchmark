# Compatibility Sweep Plan

## Goal

Align the benchmark harness with the latest canonical package surfaces exposed by the core repos after their boundary cleanup.

## Scan scope

- `README.md`
- `docs/`
- `scripts/`
- `harness/`
- `scenarios/`
- `tests/`
- `Makefile`

## Compatibility targets

1. Replace legacy root audit validation assumptions with `aro_audit.validation`.
2. Ensure bootstrap validates both the adapter import used by the harness and the new `governor.cli` package surface.
3. Remove any lingering references to retired root-level MVK prototype files.
4. Document canonical module paths and fallback rules in one place.
5. Add tests for installed packages, environment overrides, sibling fallback, and missing-dependency messaging.

## Planned changes

- Patch `scripts/bootstrap.py` to expose explicit expected import paths and clearer fallback errors.
- Update the governed harness to import audit validation from `aro_audit.validation`.
- Rename and expand bootstrap tests into dependency-resolution tests.
- Add `docs/dependency-compatibility.md`.
- Add a README compatibility section and a final sweep report.
