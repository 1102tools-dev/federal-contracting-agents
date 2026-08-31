import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class OrchestratorContractTests(unittest.TestCase):
    def text(self, plugin: str, skill: str) -> str:
        return (REPO_ROOT / "plugins" / plugin / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")

    def test_current_catalog_contains_exactly_three_agents(self) -> None:
        expected = {"govcon-growth-agent", "pre-award-agent", "other-transaction-agent"}
        self.assertEqual({path.name for path in (REPO_ROOT / "plugins").iterdir() if path.is_dir()}, expected)
        for manifest_path in (
            REPO_ROOT / ".claude-plugin" / "marketplace.json",
            REPO_ROOT / ".github" / "plugin" / "marketplace.json",
        ):
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["metadata"]["version"], "2.0.0")
            self.assertEqual({item["name"] for item in manifest["plugins"]}, expected)

    def test_current_17_routes_define_products_or_deterministic_help(self) -> None:
        route_contracts = {
            ("govcon-growth-agent", "govcon-growth-workflow"): (
                "references/launch-menu-and-question-blocks.md",
                (
                    "Federal Opportunity Shortlist in chat", "Opportunity Evidence Screen in chat",
                    "Competitor/Incumbent Intelligence Profile in chat", "Recompete Pipeline in chat",
                    "Partner Shortlist or Due-Diligence Profile in chat", "Agency/Market Intelligence Snapshot in chat",
                    "Labor-Rate/Pricing Context Table in chat", "Refreshed Prior Research with a change log",
                    "## Help me choose",
                ),
            ),
            ("pre-award-agent", "pre-award-workflow"): (
                "SKILL.md",
                (
                    "Validated SOW/PWS `.docx` plus two chat-only handoffs",
                    "Routed IGCE `.xlsx`, separated by confirmed pricing method or hybrid CLIN",
                    "SOW/PWS, approved chat-only handoffs, and routed IGCE workbook or workbooks",
                    "Affected artifact rebuild plus before/after change register",
                ),
            ),
            ("other-transaction-agent", "other-transaction-workflow"): (
                "SKILL.md",
                (
                    "Validated OT Project Description `.docx` plus chat-only milestone handoff",
                    "Milestone-based OT Cost Analysis `.xlsx`",
                    "Validated OT Project Description and OT Cost Analysis with the approved handoff carried forward",
                    "Affected artifact rebuild plus before/after milestone register",
                ),
            ),
        }
        self.assertEqual(sum(len(routes) for _, routes in route_contracts.values()), 17)
        for (plugin, skill), (relative_path, routes) in route_contracts.items():
            text = (REPO_ROOT / "plugins" / plugin / "skills" / skill / relative_path).read_text(encoding="utf-8")
            for route in routes:
                self.assertIn(route, text)

    def test_all_current_orchestrators_front_load_presence_only_readiness(self) -> None:
        checks = {
            ("govcon-growth-agent", "govcon-growth-workflow"): ("sam-gov", "get_access_status", "SAM_API_KEY is not configured"),
            ("pre-award-agent", "pre-award-workflow"): ("bls-oews.get_access_status", "gsa-perdiem.get_access_status", "BLS_API_KEY is not configured", "PERDIEM_API_KEY is not configured"),
            ("other-transaction-agent", "other-transaction-workflow"): ("bls-oews.get_access_status", "gsa-perdiem.get_access_status", "BLS_API_KEY is not configured", "PERDIEM_API_KEY is not configured"),
        }
        for (plugin, skill), required_strings in checks.items():
            text = self.text(plugin, skill)
            self.assertIn("presence-only", text)
            self.assertIn("https://1102tools.com/setup#credentials", text)
            for required in required_strings:
                self.assertIn(required, text)

    def test_current_agents_pin_expected_paced_mcp_surfaces(self) -> None:
        expected = {
            "govcon-growth-agent": {"sam-gov", "usaspending", "gsa-calc", "tavily-web"},
            "pre-award-agent": {"bls-oews", "gsa-calc", "gsa-perdiem"},
            "other-transaction-agent": {"bls-oews", "gsa-calc", "gsa-perdiem"},
        }
        for plugin, names in expected.items():
            manifest = json.loads((REPO_ROOT / "plugins" / plugin / "mcp.json").read_text(encoding="utf-8"))
            self.assertEqual(set(manifest["mcpServers"]), names)

    def test_routing_matrix_covers_only_current_agents(self) -> None:
        scenarios = json.loads((REPO_ROOT / "tests" / "routing_scenarios.json").read_text())
        self.assertEqual({scenario["plugin"] for scenario in scenarios}, {"govcon-growth-agent", "pre-award-agent", "other-transaction-agent"})
        self.assertIn("explicit", {scenario["invocation"] for scenario in scenarios})
        self.assertIn("implicit", {scenario["invocation"] for scenario in scenarios})


if __name__ == "__main__":
    unittest.main()
