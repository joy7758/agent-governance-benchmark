# Compatibility Sweep Report

- old token-governor entrypoints removed? yes; benchmark docs and dependency resolution now target `governor.cli` plus the runtime adapter import actually used by the harness
- old aro-audit validator path removed? yes; governed harness and dependency resolution now target `aro_audit.validation`
- old mvk prototype paths removed? yes; no benchmark docs or scripts point at the retired root-level MVK prototype files
- bootstrap aligned to new package surfaces? yes; bootstrap now reports canonical import paths and validates the installed, env, and sibling fallback order
- docs updated? yes; README and `docs/dependency-compatibility.md` now describe the canonical module paths and fallback rules
- remaining cross-repo compatibility risks? the harness still depends on `adapters.langchain_middleware` remaining importable from `token-governor`; if that adapter surface moves again, the benchmark will need another compatibility sweep
