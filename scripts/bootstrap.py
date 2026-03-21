"""Portable dependency bootstrap for the governance benchmark harness."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent

DEPENDENCIES = {
    "token_governor": {
        "env_var": "TOKEN_GOVERNOR_REPO",
        "sibling": "token-governor",
        "module": "adapters.langchain_middleware",
        "attrs": ("wrap_agent",),
        "marker": ("adapters", "langchain_middleware.py"),
    },
    "aro_audit": {
        "env_var": "ARO_AUDIT_REPO",
        "sibling": "aro-audit",
        "module": "validator",
        "attrs": (
            "build_evidence_object",
            "summarize_evidence",
            "validate_evidence_data",
        ),
        "marker": ("validator.py",),
    },
}


def _module_probe(module_name: str, required_attrs: tuple[str, ...]) -> bool:
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return False
    return all(hasattr(module, attr) for attr in required_attrs)


def _valid_repo_path(path: Path, marker: tuple[str, ...]) -> bool:
    return path.exists() and path.joinpath(*marker).exists()


def resolve_dependency(
    name: str,
    *,
    env: dict[str, str] | None = None,
    workspace_root: Path | None = None,
    module_probe: Any = _module_probe,
) -> dict[str, Any]:
    env = os.environ if env is None else env
    workspace_root = WORKSPACE_ROOT if workspace_root is None else workspace_root
    spec = DEPENDENCIES[name]
    module_name = str(spec["module"])
    required_attrs = tuple(spec["attrs"])
    marker = tuple(spec["marker"])

    if module_probe(module_name, required_attrs):
        return {"name": name, "source": "installed", "path": None, "module": module_name}

    env_path = env.get(str(spec["env_var"]))
    if env_path:
        candidate = Path(env_path).expanduser()
        if _valid_repo_path(candidate, marker):
            return {
                "name": name,
                "source": "env",
                "path": str(candidate.resolve()),
                "module": module_name,
            }
        raise RuntimeError(
            f"{spec['env_var']} points to {candidate}, but required marker "
            f"{Path(*marker)} was not found."
        )

    sibling_path = workspace_root / str(spec["sibling"])
    if _valid_repo_path(sibling_path, marker):
        return {
            "name": name,
            "source": "sibling",
            "path": str(sibling_path.resolve()),
            "module": module_name,
        }

    raise RuntimeError(
        f"Unable to resolve {name}. Install {module_name}, set {spec['env_var']}, "
        f"or place {spec['sibling']} beside this repo."
    )


def resolve_dependencies(
    *,
    env: dict[str, str] | None = None,
    workspace_root: Path | None = None,
    module_probe: Any = _module_probe,
) -> dict[str, dict[str, Any]]:
    return {
        name: resolve_dependency(
            name,
            env=env,
            workspace_root=workspace_root,
            module_probe=module_probe,
        )
        for name in DEPENDENCIES
    }


def ensure_dependencies() -> dict[str, dict[str, Any]]:
    resolved = resolve_dependencies()
    for dependency in resolved.values():
        path = dependency.get("path")
        if path and path not in sys.path:
            sys.path.insert(0, path)
    return resolved


def main() -> int:
    resolved = ensure_dependencies()
    print(json.dumps(resolved, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
