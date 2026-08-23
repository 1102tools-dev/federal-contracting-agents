import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_lifecycle_evidence import (
    PLUGIN_NAMES,
    semantic_errors,
    stale_claim_errors,
    validate,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER = REPO_ROOT / "tests" / "manual" / "rc5_lifecycle_ledger.json"
SCHEMA = REPO_ROOT / "tests" / "manual" / "rc5_lifecycle_ledger.schema.json"


class LifecycleEvidenceTests(unittest.TestCase):
    def test_rc5_ledger_is_schema_valid_and_preserves_p1_history(self) -> None:
        errors = validate(REPO_ROOT, LEDGER, SCHEMA)
        self.assertEqual(errors, [])
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(ledger["status"], "advisory")
        self.assertFalse(any(item["result"] == "pending" for item in ledger["artifacts"]))
        self.assertFalse(any(item["severity"] == "P0" for item in ledger["defects"]))
        self.assertEqual(
            [item["id"] for item in ledger["defects"] if item["severity"] == "P1"],
            ["P1-OT-CACHED-ERROR-AUDIT"],
        )

    def test_semantic_contract_requires_all_lifecycle_lanes(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        ledger["lanes"] = ledger["lanes"][:-1]
        self.assertTrue(any("lanes must be exactly" in error for error in semantic_errors(ledger)))

    def test_package_targets_match_current_manifests(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        ledger["packages"][0]["target_version"] = "1.0.0-rc.999"
        errors = semantic_errors(ledger, REPO_ROOT)
        self.assertTrue(any("must match manifest version" in error for error in errors))

    def test_stale_current_preview_claim_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in PLUGIN_NAMES:
                plugin = root / "plugins" / name
                plugin.mkdir(parents=True)
                (plugin / "plugin.json").write_text(
                    json.dumps({"version": "1.0.0-rc.5"}), encoding="utf-8"
                )
                (plugin / "test.md").write_text(
                    "# Test\n\nThe current public preview is `1.0.0-rc.4`.\n", encoding="utf-8"
                )
            errors = stale_claim_errors(root)
            self.assertTrue(any("does not match manifest" in error for error in errors))

    def test_historical_compatibility_claim_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in PLUGIN_NAMES:
                plugin = root / "plugins" / name
                plugin.mkdir(parents=True)
                (plugin / "plugin.json").write_text(
                    json.dumps({"version": "1.0.0-rc.5"}), encoding="utf-8"
                )
                content = "# Historical client checkpoint\n\nVS Code/Copilot installation remains pending.\n"
                (plugin / "test.md").write_text(content, encoding="utf-8")
            self.assertEqual(stale_claim_errors(root), [])


if __name__ == "__main__":
    unittest.main()
