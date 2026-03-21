from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.bootstrap import resolve_dependencies


class BootstrapResolutionTests(unittest.TestCase):
    def test_installed_dependency_wins(self) -> None:
        def probe(module_name: str, required_attrs: tuple[str, ...]) -> bool:
            return module_name in {"adapters.langchain_middleware", "validator"}

        resolved = resolve_dependencies(
            env={},
            workspace_root=Path("/tmp/workspace"),
            module_probe=probe,
        )
        self.assertEqual(resolved["token_governor"]["source"], "installed")

    def test_env_var_beats_sibling(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            env_repo = workspace / "custom-token-governor"
            sibling_repo = workspace / "token-governor"
            env_repo.joinpath("adapters").mkdir(parents=True)
            env_repo.joinpath("adapters", "langchain_middleware.py").write_text("", encoding="utf-8")
            sibling_repo.joinpath("adapters").mkdir(parents=True)
            sibling_repo.joinpath("adapters", "langchain_middleware.py").write_text("", encoding="utf-8")
            aro_repo = workspace / "aro-audit"
            aro_repo.mkdir(parents=True)
            aro_repo.joinpath("validator.py").write_text("", encoding="utf-8")

            resolved = resolve_dependencies(
                env={"TOKEN_GOVERNOR_REPO": str(env_repo)},
                workspace_root=workspace,
                module_probe=lambda module_name, attrs: False,
            )
            self.assertEqual(resolved["token_governor"]["source"], "env")
            self.assertEqual(resolved["token_governor"]["path"], str(env_repo.resolve()))

    def test_sibling_fallback_is_used(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            tg_repo = workspace / "token-governor"
            tg_repo.joinpath("adapters").mkdir(parents=True)
            tg_repo.joinpath("adapters", "langchain_middleware.py").write_text("", encoding="utf-8")
            aro_repo = workspace / "aro-audit"
            aro_repo.mkdir(parents=True)
            aro_repo.joinpath("validator.py").write_text("", encoding="utf-8")

            resolved = resolve_dependencies(
                env={},
                workspace_root=workspace,
                module_probe=lambda module_name, attrs: False,
            )
            self.assertEqual(resolved["token_governor"]["source"], "sibling")
            self.assertEqual(resolved["aro_audit"]["source"], "sibling")

    def test_missing_dependency_raises_clear_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            with self.assertRaises(RuntimeError) as ctx:
                resolve_dependencies(
                    env={},
                    workspace_root=workspace,
                    module_probe=lambda module_name, attrs: False,
                )
        self.assertIn("Unable to resolve token_governor", str(ctx.exception))
