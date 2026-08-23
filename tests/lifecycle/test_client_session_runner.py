from __future__ import annotations

import argparse
import json
import os
import tempfile
import unittest
from pathlib import Path

try:
    from .client_session_runner import (
        apply_credential_state,
        apply_client_home,
        claude_command,
        codex_command,
        load_credentials,
        parse_codex,
        redact_text,
    )
except ImportError:  # pragma: no cover
    from client_session_runner import (
        apply_credential_state,
        apply_client_home,
        claude_command,
        codex_command,
        load_credentials,
        parse_codex,
        redact_text,
    )


class ClientSessionRunnerTests(unittest.TestCase):
    def args(self, client: str, session_id: str | None = None) -> argparse.Namespace:
        return argparse.Namespace(
            client=client,
            claude_binary=Path("/bin/claude"),
            codex_binary=Path("/bin/codex"),
            model=None,
            effort="high",
            session_id=session_id,
            mcp_config=Path("/tmp/package/.mcp.json") if client == "claude" else None,
            claude_agent=None,
            codex_profile=None,
            codex_config=[],
        )

    def test_claude_command_requests_fast_opus_and_explicit_resume(self) -> None:
        command = claude_command(self.args("claude", "session-1"), "continue")
        self.assertIn("opus", command)
        self.assertIn("high", command)
        self.assertIn('{"fastMode":true}', command)
        self.assertIn("--strict-mcp-config", command)
        resume_index = command.index("--resume")
        self.assertEqual(command[resume_index : resume_index + 2], ["--resume", "session-1"])

    def test_claude_command_accepts_explicit_installed_agent(self) -> None:
        args = self.args("claude")
        args.claude_agent = "market-research-agent:market-research-agent"
        command = claude_command(args, "verify")
        self.assertEqual(
            command[:4],
            [
                "/bin/claude",
                "--agent",
                "market-research-agent:market-research-agent",
                "-p",
            ],
        )

    def test_codex_command_uses_explicit_thread_resume(self) -> None:
        command = codex_command(self.args("codex", "thread-1"), "continue")
        self.assertEqual(command[:3], ["/bin/codex", "exec", "resume"])
        self.assertIn("thread-1", command)
        self.assertIn("gpt-5.6-sol", command)

    def test_codex_command_accepts_explicit_config_override(self) -> None:
        args = self.args("codex")
        args.codex_config = ["shell_environment_policy.inherit=all"]
        command = codex_command(args, "verify")
        self.assertEqual(
            command[:4],
            ["/bin/codex", "-c", "shell_environment_policy.inherit=all", "exec"],
        )

    def test_codex_command_selects_host_profile_before_exec(self) -> None:
        args = self.args("codex")
        args.codex_profile = "1102tools-host"
        command = codex_command(args, "verify")
        self.assertEqual(
            command[:4],
            ["/bin/codex", "--profile", "1102tools-host", "exec"],
        )

    def test_isolated_client_home_sets_codex_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".codex").mkdir()
            environment: dict[str, str] = {}
            self.assertTrue(apply_client_home(environment, "codex", root))
            self.assertEqual(environment["HOME"], str(root.resolve()))
            self.assertEqual(environment["CODEX_HOME"], str((root / ".codex").resolve()))

    def test_credentials_are_loaded_and_never_rendered(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "credentials.json"
            path.write_text(
                json.dumps({"mcpServers": {"sam": {"env": {"SAM_API_KEY": "secret-value"}}}}),
                encoding="utf-8",
            )
            credentials = load_credentials(path)
        environment = {"UNRELATED": "preserve"}
        presence = apply_credential_state(environment, credentials, "valid")
        self.assertTrue(presence["SAM_API_KEY"])
        self.assertEqual(environment["UNRELATED"], "preserve")
        self.assertNotIn("secret-value", redact_text("key=secret-value", tuple(credentials.values())))

    def test_missing_sam_preserves_other_valid_credentials(self) -> None:
        environment = os.environ.copy()
        credentials = {"SAM_API_KEY": "sam", "BLS_API_KEY": "bls"}
        presence = apply_credential_state(environment, credentials, "missing-sam")
        self.assertFalse(presence["SAM_API_KEY"])
        self.assertTrue(presence["BLS_API_KEY"])

    def test_invalid_bls_preserves_other_valid_credentials(self) -> None:
        environment: dict[str, str] = {}
        credentials = {"SAM_API_KEY": "sam", "BLS_API_KEY": "bls"}
        presence = apply_credential_state(environment, credentials, "invalid-bls")
        self.assertEqual(environment["BLS_API_KEY"], "rc5-invalid-placeholder")
        self.assertEqual(environment["SAM_API_KEY"], "sam")
        self.assertTrue(presence["BLS_API_KEY"])

    def test_invalid_regulations_preserves_other_valid_credentials(self) -> None:
        environment: dict[str, str] = {}
        credentials = {
            "SAM_API_KEY": "sam",
            "REGULATIONS_GOV_API_KEY": "regulations",
        }
        presence = apply_credential_state(environment, credentials, "invalid-regulations")
        self.assertEqual(
            environment["REGULATIONS_GOV_API_KEY"], "rc5-invalid-placeholder"
        )
        self.assertEqual(environment["SAM_API_KEY"], "sam")
        self.assertTrue(presence["REGULATIONS_GOV_API_KEY"])

    def test_invalid_perdiem_preserves_other_valid_credentials(self) -> None:
        environment: dict[str, str] = {}
        credentials = {"SAM_API_KEY": "sam", "PERDIEM_API_KEY": "perdiem"}
        presence = apply_credential_state(environment, credentials, "invalid-perdiem")
        self.assertEqual(environment["PERDIEM_API_KEY"], "rc5-invalid-placeholder")
        self.assertEqual(environment["SAM_API_KEY"], "sam")
        self.assertTrue(presence["PERDIEM_API_KEY"])

    def test_codex_jsonl_parser_extracts_thread_and_last_agent_message(self) -> None:
        payload = "\n".join(
            (
                json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "first"}}),
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "last"}}),
            )
        )
        thread, response, meta = parse_codex(payload)
        self.assertEqual(thread, "thread-1")
        self.assertEqual(response, "last")
        self.assertEqual(meta["event_count"], 3)


if __name__ == "__main__":
    unittest.main()
