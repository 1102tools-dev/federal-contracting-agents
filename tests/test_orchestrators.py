from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class OrchestratorContractTests(unittest.TestCase):
    def text(self, plugin: str, skill: str) -> str:
        return (
            REPO_ROOT / "plugins" / plugin / "skills" / skill / "SKILL.md"
        ).read_text(encoding="utf-8")

    def test_pre_award_preserves_routing_and_transition_gates(self) -> None:
        text = self.text("pre-award-agent", "pre-award-workflow")
        for required in (
            "STAFFING HANDOFF TABLE: FOR IGCE BUILDER",
            "SECTION B HANDOFF TABLE",
            "igce-builder-ffp",
            "igce-builder-lh-tm",
            "igce-builder-cr",
            "Do you approve moving the approved handoff",
            "Never blend methodologies",
            "Do not ask the user to copy, upload, or restate them",
        ):
            self.assertIn(required, text)

    def test_ot_preserves_milestones_and_reserved_determinations(self) -> None:
        text = self.text("other-transaction-agent", "other-transaction-workflow")
        for required in (
            "MILESTONE HANDOFF TABLE: FOR OT COST ANALYSIS",
            "ot-project-description-builder",
            "ot-cost-analysis",
            "Do you approve moving the approved handoff",
            "Agreements Officer",
            "Do not ask the user to copy, upload, or restate it",
        ):
            self.assertIn(required, text)

    def test_keyed_calls_have_three_second_floor(self) -> None:
        for plugin, skill in (
            ("pre-award-agent", "pre-award-workflow"),
            ("other-transaction-agent", "other-transaction-workflow"),
        ):
            self.assertIn("at least three seconds", self.text(plugin, skill))

    def test_missing_capabilities_are_hard_stops(self) -> None:
        for plugin, skill in (
            ("pre-award-agent", "pre-award-workflow"),
            ("other-transaction-agent", "other-transaction-workflow"),
        ):
            text = self.text(plugin, skill)
            self.assertIn("HARD STOP", text)
            self.assertIn("do not call another pricing mcp", text.lower())

    def test_manual_release_matrix_is_complete(self) -> None:
        text = (REPO_ROOT / "tests" / "manual_release_matrix.md").read_text(encoding="utf-8")
        for scenario_id in (
            *(f"PRE-{index:02d}" for index in range(1, 17)),
            *(f"OT-{index:02d}" for index in range(1, 16)),
        ):
            self.assertIn(scenario_id, text)
        for client in ("Codex CLI", "Codex Desktop", "Claude Code CLI", "GitHub Copilot CLI", "VS Code/Copilot"):
            self.assertIn(client, text)

    def test_routing_matrix_covers_both_agents(self) -> None:
        import json

        scenarios = json.loads((REPO_ROOT / "tests" / "routing_scenarios.json").read_text())
        self.assertGreaterEqual(len(scenarios), 13)
        self.assertEqual(
            {scenario["plugin"] for scenario in scenarios},
            {"pre-award-agent", "other-transaction-agent"},
        )
        self.assertIn("explicit", {scenario["invocation"] for scenario in scenarios})
        self.assertIn("implicit", {scenario["invocation"] for scenario in scenarios})


if __name__ == "__main__":
    unittest.main()
