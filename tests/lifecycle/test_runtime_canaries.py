import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from runtime_canaries import (  # noqa: E402
    REDACTED,
    SecretRedactor,
    assert_exact_values_redacted,
    credential_matrix,
    load_matrix,
    normalized_shape,
    run_live_mcp_canary,
    run_offline,
    run_pacing_canary,
    simulate_concurrent_calls,
    validate_pacing,
    MockResponse,
    SimulatedRequest,
)


class RuntimeCanaryTests(unittest.TestCase):
    def test_matrix_has_nine_federal_canaries(self):
        matrix = load_matrix()
        self.assertEqual(len(matrix["mcp_canaries"]), 9)
        self.assertEqual(len({item["server"] for item in matrix["mcp_canaries"]}), 9)

    def test_credential_matrix_records_presence_not_values(self):
        secret = "unit-test-sam-secret-123456"
        records = credential_matrix({"SAM_API_KEY": secret, "BLS_API_KEY": ""})
        rendered = json.dumps(records, sort_keys=True)
        self.assertNotIn(secret, rendered)
        sam_valid = next(record for record in records if record["credential_name"] == "SAM_API_KEY" and record["state"] == "valid")
        bls_valid = next(record for record in records if record["credential_name"] == "BLS_API_KEY" and record["state"] == "valid")
        self.assertTrue(sam_valid["credential_present"])
        self.assertFalse(bls_valid["observed_environment_present"])
        self.assertTrue(bls_valid["credential_present"])
        self.assertTrue(all(record["value_recorded"] is False for record in records))

    def test_redaction_catches_exact_values_and_secret_fields(self):
        secret = "unit-test-secret-value-987654"
        value = {"message": f"token={secret}", "SAM_API_KEY": secret, "nested": [secret]}
        sanitized = SecretRedactor((secret,)).redact(value)
        self.assertNotIn(secret, json.dumps(sanitized))
        self.assertEqual(sanitized["SAM_API_KEY"], REDACTED)
        assert_exact_values_redacted(sanitized, (secret,))
        with self.assertRaises(AssertionError):
            assert_exact_values_redacted(value, (secret,))

    def test_captured_429_retry_after_and_concurrency_are_deterministic(self):
        first = run_pacing_canary()
        second = run_pacing_canary()
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "pass")
        self.assertTrue(first["captured_429"])
        self.assertTrue(first["retry_after_honored"])
        self.assertEqual(first["pacing_violations"], [])

    def test_scheduler_serializes_calls_after_completion(self):
        events = simulate_concurrent_calls(
            (
                SimulatedRequest("one", 0, 2, (MockResponse(200),)),
                SimulatedRequest("two", 0, 2, (MockResponse(200),)),
            ),
            min_interval_seconds=3,
        )
        self.assertEqual([event.started_at for event in events], [0, 5])
        self.assertEqual(validate_pacing(events, 3), [])

    def test_normalized_shape_is_value_free(self):
        response = {"results": [{"secret": "must-not-be-recorded"}], "count": 1}
        shape = normalized_shape(response)
        self.assertEqual(shape, {"type": "object", "keys": ["count", "results"]})
        self.assertNotIn("must-not-be-recorded", json.dumps(shape))

    def test_offline_is_dry_run_and_never_calls_a_runner(self):
        ledger = run_offline(load_matrix())
        self.assertEqual(ledger["mode"], "offline")
        self.assertEqual(len(ledger["mcp_canaries"]), 9)
        self.assertTrue(all(item["status"] == "dry-run" for item in ledger["mcp_canaries"]))
        self.assertFalse(any(item.get("raw_output_recorded") for item in ledger["mcp_canaries"]))

    def test_live_runner_output_is_sanitized_and_schema_hashed(self):
        secret = "runner-secret-value-456789"
        script = (
            "import json,sys; descriptor=json.loads(sys.stdin.read()); "
            "print(json.dumps({'version':'1.0.8','tools':[{'name':'tool-a','inputSchema':{'type':'object'}}],"
            "'response':{'results':[{'secret':'runner-secret-value-456789'}]},"
            "'warnings':['token=runner-secret-value-456789'],"
            "'source_hashes':{'source':'abc'}}))"
        )
        definition = load_matrix()["mcp_canaries"][0]
        record = run_live_mcp_canary(definition, (sys.executable, "-c", script), secrets=(secret,))
        self.assertEqual(record["status"], "pass")
        self.assertEqual(record["tool_count"], 1)
        self.assertEqual(len(record["schema_hash"]), 64)
        self.assertNotIn(secret, json.dumps(record))
        self.assertFalse(record["raw_output_recorded"])

    def test_live_runner_protocol_error_does_not_echo_output(self):
        secret = "runner-secret-value-456789"
        script = "import sys; print('secret=runner-secret-value-456789'); raise SystemExit(3)"
        definition = load_matrix()["mcp_canaries"][0]
        record = run_live_mcp_canary(definition, (sys.executable, "-c", script), secrets=(secret,))
        self.assertEqual(record["status"], "fail")
        self.assertEqual(record["failure_class"], "runner_protocol_error")
        self.assertNotIn(secret, json.dumps(record))
        self.assertFalse(record["raw_output_recorded"])

    def test_live_runner_classifies_schema_loss_as_p1(self):
        script = (
            "import json; print(json.dumps({'version':'1.0.8','tools':[],'response':{},'source_hashes':{}}))"
        )
        definition = dict(load_matrix()["mcp_canaries"][0])
        definition["expected_tool_names"] = ["required-tool"]
        record = run_live_mcp_canary(definition, (sys.executable, "-c", script))
        self.assertEqual(record["status"], "fail")
        self.assertEqual(record["drift_classification"], "p1_tool_schema_loss")


if __name__ == "__main__":
    unittest.main()
