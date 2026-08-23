from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "run_routing_scenarios.py"
SPEC = importlib.util.spec_from_file_location("run_routing_scenarios", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class RoutingRunnerTests(unittest.TestCase):
    def test_provider_matrix_has_complete_cross_agent_coverage(self) -> None:
        scenarios = json.loads(
            (REPO_ROOT / "tests" / "provider_scenarios.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(scenarios), 14)
        for prefix in ("market", "growth"):
            self.assertEqual(
                len([scenario for scenario in scenarios if scenario["id"].startswith(prefix)]),
                7,
            )
        ambiguous = [scenario for scenario in scenarios if scenario["id"].endswith("ambiguous-provider-reply")]
        self.assertEqual(len(ambiguous), 2)
        for scenario in ambiguous:
            self.assertEqual(
                scenario["required_order"],
                ["native web only", "native web with tavily fallback", "tavily only", "no public web"],
            )
        no_web = [scenario for scenario in scenarios if scenario["id"].endswith("no-public-web")]
        for scenario in no_web:
            self.assertIn("approved federal MCP", scenario["prompt"])

    def test_required_order_rejects_out_of_order_output(self) -> None:
        scenario = {
            "required_any": [],
            "forbidden": [],
            "required_order": ["first", "second", "third"],
        }
        passed, failures = RUNNER.grade(scenario, "first third second")
        self.assertFalse(passed)
        self.assertIn("ordered terms are out of sequence", failures[0])

    def test_required_order_accepts_ordered_output(self) -> None:
        scenario = {
            "required_any": [],
            "forbidden": [],
            "required_order": ["first", "second", "third"],
        }
        passed, failures = RUNNER.grade(scenario, "first then second then third")
        self.assertTrue(passed)
        self.assertEqual(failures, [])

    def test_grader_normalizes_markdown_emphasis_and_hyphens(self) -> None:
        scenario = {
            "required_any": [["does not make"], ["cost share"]],
            "forbidden": [],
        }
        passed, failures = RUNNER.grade(
            scenario,
            "Publication does **not** make it operative; the cost-share decision is reserved.",
        )
        self.assertTrue(passed)
        self.assertEqual(failures, [])

    def test_package_native_release_gates_are_front_loaded(self) -> None:
        pre = (REPO_ROOT / "plugins/pre-award-agent/skills/pre-award-workflow/SKILL.md").read_text()
        ot = (REPO_ROOT / "plugins/other-transaction-agent/skills/other-transaction-workflow/SKILL.md").read_text()
        self.assertIn("A shorter refusal", pre)
        self.assertIn("structured JSON plus Markdown or CSV", pre)
        self.assertIn("structured JSON plus Markdown or CSV", ot)
        self.assertIn("never call that fallback a completed workbook", pre)
        self.assertIn("never call that fallback a completed workbook", ot)

    def test_vendored_spreadsheet_skills_preserve_host_precedence(self) -> None:
        paths = [
            REPO_ROOT / "plugins/pre-award-agent/skills/igce-builder-cr/references/runtime-adaptation.md",
            REPO_ROOT / "plugins/pre-award-agent/skills/igce-builder-ffp/references/runtime-adaptation.md",
            REPO_ROOT / "plugins/pre-award-agent/skills/igce-builder-lh-tm/references/runtime-adaptation.md",
            REPO_ROOT / "plugins/other-transaction-agent/skills/ot-cost-analysis/references/runtime-adaptation.md",
        ]
        for path in paths:
            text = path.read_text()
            with self.subTest(path=path):
                self.assertIn("hard stop", text.lower())
                self.assertIn("structured JSON", text)
                self.assertIn("Do not label the fallback as a completed workbook", text)

    def test_claude_resolver_selects_current_manifest_version_among_old_caches(self) -> None:
        plugin = "market-research-agent"
        version = json.loads(
            (REPO_ROOT / "plugins" / plugin / "plugin.json").read_text()
        )["version"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = root / plugin / "1.0.0-rc.1"
            current = root / plugin / version
            old.mkdir(parents=True)
            current.mkdir(parents=True)
            (old / "plugin.json").write_text("{}")
            (current / "plugin.json").write_text("{}")
            self.assertEqual(
                RUNNER.resolve_claude_installed_plugin(root, plugin),
                current,
            )


if __name__ == "__main__":
    unittest.main()
