from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PLUGINS = {
    "govcon-growth-agent": "govcon-growth-workflow",
    "market-research-agent": "market-research-builder",
}


def load_validator():
    path = (
        ROOT
        / "plugins/market-research-agent/skills/market-research-builder/scripts/validate_research_record.py"
    )
    spec = importlib.util.spec_from_file_location("vendored_research_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def base_record(mode: str, providers: list[str]) -> dict[str, object]:
    return {
        "schema_version": "1.1",
        "skill": "market-research-builder",
        "workflow_mode": "quick-chat",
        "question": "Synthetic offline policy test",
        "scope": {"as_of_date": "2026-08-21"},
        "document_register": [],
        "user_context": [],
        "assumptions": [],
        "web_research": {
            "mode": mode,
            "approved": True,
            "approved_at": "2026-08-21T20:00:00Z",
            "disclosure_acknowledged": True,
            "planned_providers": providers,
            "providers_used": [],
            "fallback_events": [],
        },
        "queries": [],
        "evidence": [],
        "findings": [],
        "inferences": [],
        "user_decisions": [],
        "conflicts": [],
        "unresolved_questions": [],
        "outputs": [],
        "validation": {},
    }


class TavilyPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_shared_policy_is_identical_and_lists_failure_classes(self):
        policies = []
        for plugin, skill in RESEARCH_PLUGINS.items():
            policies.append(
                (
                    ROOT
                    / "plugins"
                    / plugin
                    / "skills"
                    / skill
                    / "references/web-provider-policy.md"
                ).read_bytes()
            )
        self.assertEqual(policies[0], policies[1])
        text = policies[0].decode()
        for required in (
            "connection failure or timeout",
            "401 or 403",
            "429 response",
            "5xx response",
            "malformed response",
            "missing required operation",
            "incompatible operation schema",
            "Never invoke Tavily Crawl, Map, or Research",
        ):
            self.assertIn(required, text)

    def test_each_failure_class_can_be_recorded_only_in_combined_mode(self):
        reasons = ("timeout", "401", "403", "429", "503", "malformed", "missing tool", "schema drift")
        for reason in reasons:
            with self.subTest(reason=reason):
                record = base_record("tavily_with_native_fallback", ["tavily", "native_web"])
                record["web_research"]["providers_used"] = ["tavily", "native_web"]
                record["web_research"]["fallback_events"] = [{
                    "timestamp": "2026-08-21T20:01:00Z",
                    "failed_provider": "tavily",
                    "replacement_provider": "native_web",
                    "reason": reason,
                }]
                result = self.validator.validate_record(record)
                self.assertEqual(result["status"], "pass", result["failures"])

        disallowed = base_record("tavily_only", ["tavily"])
        disallowed["web_research"]["fallback_events"] = [{
            "timestamp": "2026-08-21T20:01:00Z",
            "failed_provider": "tavily",
            "replacement_provider": "tavily",
            "reason": "429",
        }]
        result = self.validator.validate_record(disallowed)
        self.assertEqual(result["status"], "fail")

    def test_only_search_and_extract_are_valid_tavily_operations(self):
        for operation in ("tavily_search", "tavily_extract"):
            record = base_record("tavily_only", ["tavily"])
            record["web_research"]["providers_used"] = ["tavily"]
            record["queries"] = [{
                "provider": "tavily",
                "operation": operation,
                "parameters": {"query": "approved public term"},
                "retrieved_at": "2026-08-21T20:01:00Z",
                "count": 1,
                "limitations": "Synthetic offline fixture",
            }]
            result = self.validator.validate_record(record)
            self.assertEqual(result["status"], "pass", result["failures"])

        prohibited = base_record("tavily_only", ["tavily"])
        prohibited["web_research"]["providers_used"] = ["tavily"]
        prohibited["queries"] = [{
            "provider": "tavily",
            "operation": "tavily_research",
            "parameters": {"query": "approved public term"},
            "retrieved_at": "2026-08-21T20:01:00Z",
            "count": 0,
            "limitations": "Synthetic offline fixture",
        }]
        result = self.validator.validate_record(prohibited)
        self.assertEqual(result["status"], "fail")

    def test_remote_service_is_confined_to_research_agents(self):
        for plugin in RESEARCH_PLUGINS:
            portable = json.loads((ROOT / "plugins" / plugin / "mcp.json").read_text())
            server = portable["mcpServers"]["tavily-web"]
            self.assertEqual(server, {
                "type": "streamable-http",
                "url": "https://mcp.tavily.com/mcp/",
                "headers": {"X-Tavily-Access-Mode": "keyless"},
            })
        for plugin in ("pre-award-agent", "other-transaction-agent"):
            portable = json.loads((ROOT / "plugins" / plugin / "mcp.json").read_text())
            self.assertNotIn("tavily-web", portable["mcpServers"])


if __name__ == "__main__":
    unittest.main()
