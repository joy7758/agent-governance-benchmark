# Benchmark Root Inventory

Pre-refactor root inventory snapshot for `agent-governance-benchmark`:

- `baseline/`
- `governed/`
- `metrics/`
- `results/`
- `scenarios/`
- `scripts/`
- `docs/`
- `README.md`

Primary boundary issues:

- baseline and governed harness code lived as peer roots instead of a single harness package
- reproducibility still assumed absolute local paths and sibling repos without a resolver
- committed sample results were mixed with the runtime output directory
