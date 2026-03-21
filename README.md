# Agent Governance Benchmark

Deterministic offline benchmark harness for governed-vs-baseline comparisons.

## Role

`agent-governance-benchmark` is the benchmark-only evaluation repo for governance behavior. It packages scenarios, harness wrappers, metrics computation, and reproducibility helpers without re-implementing the canonical governance or audit libraries.

## Not this repo

- not the governance runtime implementation
- not the audit implementation
- not the architecture hub
- not the demo repo

## Benchmark scope

- restricted tool access
- tool misuse
- prompt injection
- token budget limit
- budget attack
- persona consistency
- audit reconstruction

## Reproducibility

- deterministic and offline
- no model API key required
- dependency resolution via installed package first, then environment variables, then sibling repo fallback

## Depends on

- [token-governor](https://github.com/joy7758/token-governor)
- [aro-audit](https://github.com/joy7758/aro-audit)
- optional future evidence substrate integration: [agent-evidence](https://github.com/joy7758/agent-evidence)

## Run

```bash
python -m scripts.bootstrap
make smoke
make scenarios
make report
```

## Output

- fresh run output goes to `results/`
- committed historical samples live under `docs/results-snapshots/`

## Status

- benchmark-only
- portable repro path enabled
- no absolute local paths
