# Benchmark Repro Audit

## Old portability risks

- README required changing into a machine-specific absolute local path
- governed harness mutated `sys.path` directly to find sibling repos
- scenario modules depended on local path injection instead of package execution

## Resolution order now required

1. installed dependency import
2. `TOKEN_GOVERNOR_REPO` / `ARO_AUDIT_REPO`
3. workspace-local sibling repos for `token-governor` and `aro-audit`
4. explicit error with remediation guidance
