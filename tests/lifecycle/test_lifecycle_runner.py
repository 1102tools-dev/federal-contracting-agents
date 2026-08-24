from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

try:  # Supports both ``unittest discover -s tests`` and direct invocation.
    from .lifecycle_runner import (
        AGENT_IDS,
        ClientProfile,
        CommandResult,
        LifecycleSafetyError,
        agent_specs,
        assert_no_residue,
        assert_same_version_reinstall,
        build_plan,
        capture_inventory,
        execute_plan,
        load_matrix,
        plan_install,
        plan_uninstall,
        prepare_upgrade_fixture,
        remove_scoped_targets,
        scoped_backup_metadata,
        HISTORICAL_TAGS,
        HISTORICAL_VERSIONS,
        _tree_sha256,
    )
except ImportError:  # pragma: no cover - direct discovery fallback
    from lifecycle_runner import (
        AGENT_IDS,
        ClientProfile,
        CommandResult,
        LifecycleSafetyError,
        agent_specs,
        assert_no_residue,
        assert_same_version_reinstall,
        build_plan,
        capture_inventory,
        execute_plan,
        load_matrix,
        plan_install,
        plan_uninstall,
        prepare_upgrade_fixture,
        remove_scoped_targets,
        scoped_backup_metadata,
        HISTORICAL_TAGS,
        HISTORICAL_VERSIONS,
        _tree_sha256,
    )


class FakeRunner:
    def __init__(self, returncode: int = 0) -> None:
        self.returncode = returncode
        self.calls: list[tuple[str, ...]] = []

    def run(self, argv: tuple[str, ...], *, cwd: Path | None = None) -> CommandResult:
        self.calls.append(tuple(argv))
        return CommandResult(tuple(argv), self.returncode, 21, 0)


class LifecycleRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = load_matrix()
        self.specs = agent_specs(self.matrix)
        self.temp = tempfile.TemporaryDirectory(prefix="rc5-lifecycle-test-")
        self.home = Path(self.temp.name) / "fake-home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def profile(self, client: str = "codex") -> ClientProfile:
        return ClientProfile(client, self.home)

    def write_plugin(self, client: str, plugin_id: str, version: str) -> None:
        root = self.profile(client).plugin_cache_root / plugin_id / version
        root.mkdir(parents=True)
        (root / "plugin.json").write_text(json.dumps({"name": plugin_id, "version": version}), encoding="utf-8")

    def test_matrix_has_five_agents_and_both_client_surfaces(self) -> None:
        self.assertEqual(set(AGENT_IDS), {spec.plugin_id for spec in self.specs})
        self.assertEqual({"codex", "claude"}, set(self.matrix["clients"]))
        self.assertEqual(self.matrix["safety"]["default_mode"], "dry-run")
        self.assertTrue(
            {"credentials", "resume", "concurrency", "drift", "long-session"}
            <= set(self.matrix["lifecycle_lanes"])
        )

    def test_evidence_lanes_are_nonmutating_and_declarative(self) -> None:
        for lane in ("credentials", "resume", "concurrency", "drift", "long-session"):
            plan = build_plan(self.profile("codex"), self.matrix, lane)
            self.assertEqual(plan.lane, lane)
            self.assertEqual(plan.commands, [])
            self.assertEqual(plan.targets, [])
            self.assertIn("evidence-only", " ".join(plan.notes))

    def test_install_plan_is_dry_and_uses_documented_commands(self) -> None:
        plan = plan_install(self.profile("codex"), self.matrix, self.specs)
        self.assertEqual(plan.lane, "install")
        self.assertEqual(plan.commands[0], ("codex", "plugin", "marketplace", "add", "1102tools-dev/federal-contracting-agents", "--ref", "main"))
        self.assertEqual(plan.commands[1][0:3], ("codex", "plugin", "add"))
        self.assertEqual(plan.commands[-1], ("codex", "plugin", "add", "acquisition-policy-agent@1102tools"))

        claude = plan_install(self.profile("claude"), self.matrix, self.specs)
        self.assertEqual(claude.commands[0], ("claude", "plugin", "marketplace", "add", "1102tools-dev/federal-contracting-agents"))
        self.assertTrue(all(command[2] == "install" for command in claude.commands[1:]))

    def test_upgrade_plan_matches_client_specific_update_paths(self) -> None:
        codex = build_plan(self.profile("codex"), self.matrix, "upgrade")
        self.assertEqual(
            codex.commands[0],
            ("codex", "plugin", "marketplace", "upgrade", "1102tools"),
        )
        self.assertIn("marketplace refresh/upgrade", " ".join(codex.notes))
        self.assertIn(("codex", "plugin", "remove", "market-research-agent@1102tools"), codex.commands)
        self.assertIn(("codex", "plugin", "add", "market-research-agent@1102tools"), codex.commands)

        claude = build_plan(self.profile("claude"), self.matrix, "upgrade")
        self.assertEqual(claude.commands[0], ("claude", "plugin", "marketplace", "update", "1102tools"))
        self.assertIn(("claude", "plugin", "update", "market-research-agent@1102tools"), claude.commands)

    def test_execute_requires_explicit_temporary_home(self) -> None:
        real_home = ClientProfile("codex", Path.home())
        with self.assertRaises(LifecycleSafetyError):
            real_home.assert_safe_execution_home()

    def test_fake_runner_receives_only_scoped_client_commands(self) -> None:
        try:
            from .lifecycle_runner import execute_plan
        except ImportError:  # pragma: no cover - direct discovery fallback
            from lifecycle_runner import execute_plan

        plan = build_plan(self.profile("claude"), self.matrix, "install")
        runner = FakeRunner()
        results = execute_plan(plan, runner)
        self.assertEqual(len(results), 6)
        self.assertEqual(runner.calls[0][0:4], ("claude", "plugin", "marketplace", "add"))
        self.assertTrue(all("1102tools" in " ".join(call) or "federal-contracting-agents" in " ".join(call) for call in runner.calls))

    def test_execute_creates_only_the_scoped_client_config_root(self) -> None:
        profile = self.profile("codex")
        self.assertFalse(profile.client_dir.exists())
        plan = build_plan(profile, self.matrix, "install")
        execute_plan(plan, FakeRunner())
        self.assertTrue(profile.client_dir.is_dir())
        self.assertEqual(profile.client_dir.stat().st_mode & 0o777, 0o700)

    def test_inventory_records_metadata_not_configuration_contents(self) -> None:
        profile = self.profile("claude")
        profile.client_dir.mkdir(parents=True)
        secret_text = '{"SAM_API_KEY":"do-not-record"}'
        (profile.client_dir / "settings.json").write_text(secret_text, encoding="utf-8")
        self.write_plugin("claude", "market-research-agent", "1.0.0-rc.5")
        metadata = scoped_backup_metadata(profile)
        inventory = capture_inventory(profile)
        serialized = json.dumps({"metadata": metadata, "inventory": inventory})
        self.assertNotIn("do-not-record", serialized)
        self.assertEqual(metadata["contents_saved"], False)
        self.assertEqual(inventory["plugins"][0]["id"], "market-research-agent")
        self.assertNotIn("plugin.json", metadata["files"][0].get("content", ""))

    def test_fixture_has_rc4_and_rc5_without_modifying_source(self) -> None:
        fixture = Path(self.temp.name) / "fixture"
        source_manifest = Path(__file__).parents[2] / "plugins" / "market-research-agent" / "plugin.json"
        before = source_manifest.read_bytes()
        metadata = prepare_upgrade_fixture(
            Path(__file__).parents[2], fixture, self.specs, historical=self.matrix["upgrade_fixture"]
        )
        self.assertFalse(metadata["source_modified"])
        self.assertEqual(json.loads((fixture / "rc4/plugins/market-research-agent/plugin.json").read_text())["version"], "1.0.0-rc.4")
        self.assertEqual(json.loads((fixture / "rc5/plugins/market-research-agent/plugin.json").read_text())["version"], "1.0.0-rc.5")
        for stage in ("rc4", "rc5"):
            claude_marketplace = json.loads(
                (fixture / stage / ".claude-plugin/marketplace.json").read_text()
            )
            codex_marketplace = json.loads(
                (fixture / stage / ".agents/plugins/marketplace.json").read_text()
            )
            self.assertEqual(claude_marketplace["name"], "1102tools-lifecycle")
            self.assertEqual(codex_marketplace["name"], "1102tools-lifecycle")
            self.assertEqual(
                codex_marketplace["interface"]["displayName"],
                "1102tools-lifecycle",
            )
        self.assertEqual(source_manifest.read_bytes(), before)

    def test_fixture_preserves_heterogeneous_historical_versions_and_exact_manifest_bytes(self) -> None:
        fixture = Path(self.temp.name) / "fixture-heterogeneous"
        source = Path(__file__).parents[2]
        metadata = prepare_upgrade_fixture(source, fixture, self.specs, historical=self.matrix["upgrade_fixture"])
        for stage, tag in HISTORICAL_TAGS.items():
            metadata_stage = metadata["from"] if stage == "rc4" else metadata["to"]
            self.assertEqual(metadata_stage["tag"], tag)
            expected = HISTORICAL_VERSIONS[stage]
            actual = {}
            for plugin_id in AGENT_IDS:
                manifest_path = fixture / stage / "plugins" / plugin_id / "plugin.json"
                actual[plugin_id] = json.loads(manifest_path.read_text(encoding="utf-8"))["version"]
                git_manifest = subprocess.run(
                    ["git", "-C", str(source), "show", f"{tag}:plugins/{plugin_id}/plugin.json"],
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout
                self.assertEqual(manifest_path.read_bytes(), git_manifest)
                package_meta = metadata_stage["packages"][plugin_id]
                self.assertEqual(package_meta["tree_sha256"], _tree_sha256(manifest_path.parent))
            self.assertEqual(actual, expected)

        self.assertNotEqual(
            metadata["from"]["packages"]["market-research-agent"]["tree_sha256"],
            metadata["to"]["packages"]["market-research-agent"]["tree_sha256"],
        )

    def test_fixture_rejects_nonempty_or_in_repo_target(self) -> None:
        nonempty = Path(self.temp.name) / "nonempty"
        nonempty.mkdir()
        (nonempty / "keep").write_text("x", encoding="utf-8")
        with self.assertRaises(LifecycleSafetyError):
            prepare_upgrade_fixture(Path(__file__).parents[2], nonempty, self.specs)

    def test_same_version_reinstall_ignores_capture_time(self) -> None:
        inventory = capture_inventory(self.profile())
        later = dict(inventory)
        later["captured_at"] = "2099-01-01T00:00:00+00:00"
        assert_same_version_reinstall(inventory, later)

    def test_uninstall_plan_and_residue_assertion_are_scoped(self) -> None:
        profile = self.profile("codex")
        plan = plan_uninstall(profile, self.matrix, self.specs)
        self.assertEqual(set(plan.targets), set(profile.allowed_scoped_paths))
        self.write_plugin("codex", "market-research-agent", "1.0.0-rc.5")
        before = capture_inventory(profile)
        with self.assertRaises(AssertionError):
            assert_no_residue(before)
        remove_scoped_targets(profile, plan.targets)
        after = capture_inventory(profile)
        assert_no_residue(after)

    def test_scoped_target_rejects_broad_client_directory(self) -> None:
        profile = self.profile("codex")
        with self.assertRaises(LifecycleSafetyError):
            profile.assert_scoped_target(profile.client_dir)
        with self.assertRaises(LifecycleSafetyError):
            profile.assert_scoped_target(profile.home)


if __name__ == "__main__":
    unittest.main()
