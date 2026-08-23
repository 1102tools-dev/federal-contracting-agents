from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import tempfile
import time
import unittest
from pathlib import Path

try:
    from .client_session_runner import (
        apply_credential_state,
        apply_client_home,
        claude_command,
        codex_command,
        load_credentials,
        parse_claude,
        parse_codex,
        redact_text,
        run_claude_streaming,
    )
except ImportError:  # pragma: no cover
    from client_session_runner import (
        apply_credential_state,
        apply_client_home,
        claude_command,
        codex_command,
        load_credentials,
        parse_claude,
        parse_codex,
        redact_text,
        run_claude_streaming,
    )


class ClientSessionRunnerTests(unittest.TestCase):
    def args(self, client: str, session_id: str | None = None) -> argparse.Namespace:
        return argparse.Namespace(
            client=client,
            claude_binary=Path("/bin/claude"),
            codex_binary=Path("/bin/codex"),
            model=None,
            effort="high",
            claude_fast_mode=False,
            session_id=session_id,
            mcp_config=Path("/tmp/package/.mcp.json") if client == "claude" else None,
            claude_agent=None,
            codex_profile=None,
            codex_config=[],
        )

    def test_claude_command_defaults_non_fast_opus_and_explicit_resume(self) -> None:
        command = claude_command(self.args("claude", "session-1"), "continue")
        self.assertIn("opus", command)
        self.assertIn("high", command)
        self.assertNotIn('{"fastMode":true}', command)
        self.assertNotIn("--permission-mode", command)
        self.assertIn("stream-json", command)
        self.assertIn("--verbose", command)
        self.assertIn("--strict-mcp-config", command)
        resume_index = command.index("--resume")
        self.assertEqual(command[resume_index : resume_index + 2], ["--resume", "session-1"])

    def test_claude_command_fast_mode_is_opt_in(self) -> None:
        args = self.args("claude", "session-1")
        args.claude_fast_mode = True
        command = claude_command(args, "continue")
        self.assertIn('{"fastMode":true}', command)

    def test_claude_command_passes_allowed_tools_restriction(self) -> None:
        args = self.args("claude")
        args.claude_allowed_tools = "Skill,Read,Glob,Grep,LS,TodoWrite"
        command = claude_command(args, "verify")
        index = command.index("--allowed-tools")
        self.assertEqual(command[index + 1], "Skill,Read,Glob,Grep,LS,TodoWrite")

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
        self.assertEqual(
            command[:5],
            ["/bin/codex", "-c", 'model_reasoning_effort="high"', "exec", "resume"],
        )
        self.assertIn("thread-1", command)
        self.assertIn("gpt-5.6-sol", command)
        self.assertIn("--sandbox", command)
        self.assertIn("read-only", command)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)

    def test_codex_command_accepts_explicit_config_override(self) -> None:
        args = self.args("codex")
        args.codex_config = ["shell_environment_policy.inherit=all"]
        command = codex_command(args, "verify")
        self.assertEqual(
            command[:6],
            [
                "/bin/codex",
                "-c",
                'model_reasoning_effort="high"',
                "-c",
                "shell_environment_policy.inherit=all",
                "exec",
            ],
        )

    def test_codex_command_selects_host_profile_before_exec(self) -> None:
        args = self.args("codex")
        args.codex_profile = "1102tools-host"
        command = codex_command(args, "verify")
        self.assertEqual(
            command[:6],
            [
                "/bin/codex",
                "--profile",
                "1102tools-host",
                "-c",
                'model_reasoning_effort="high"',
                "exec",
            ],
        )

    def test_isolated_client_home_sets_codex_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".codex").mkdir()
            environment: dict[str, str] = {}
            self.assertTrue(apply_client_home(environment, "codex", root))
            self.assertEqual(environment["HOME"], str(root.resolve()))
            self.assertEqual(environment["CODEX_HOME"], str((root / ".codex").resolve()))
            resolved = root.resolve()
            self.assertEqual(environment["XDG_CONFIG_HOME"], str(resolved / ".config"))
            self.assertEqual(environment["XDG_CACHE_HOME"], str(resolved / ".cache"))
            self.assertEqual(environment["XDG_DATA_HOME"], str(resolved / ".local" / "share"))
            self.assertEqual(environment["XDG_STATE_HOME"], str(resolved / ".local" / "state"))

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

    def test_short_credentials_are_rejected_without_echoing_value(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "credentials.json"
            path.write_text(json.dumps({"SAM_API_KEY": "abc"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SAM_API_KEY credential value is too short"):
                load_credentials(path)

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

    def test_claude_stream_parser_extracts_final_result(self) -> None:
        payload = "\n".join(
            (
                json.dumps({"type": "system", "session_id": "session-1"}),
                json.dumps({"type": "assistant", "session_id": "session-1"}),
                json.dumps(
                    {
                        "type": "result",
                        "session_id": "session-1",
                        "result": "done",
                        "is_error": False,
                        "duration_api_ms": 123,
                        "num_turns": 2,
                        "modelUsage": {"claude-opus-5": {}},
                        "fast_mode_state": "on",
                    }
                ),
            )
        )
        session, response, meta = parse_claude(payload)
        self.assertEqual(session, "session-1")
        self.assertEqual(response, "done")
        self.assertEqual(meta["event_count"], 3)
        self.assertEqual(meta["fast_mode_state"], "on")

    def test_claude_stream_parser_rejects_missing_or_error_result(self) -> None:
        with self.assertRaisesRegex(ValueError, "without a final result"):
            parse_claude(json.dumps({"type": "assistant", "session_id": "session-1"}))
        with self.assertRaisesRegex(ValueError, "reported an error"):
            parse_claude(
                json.dumps(
                    {
                        "type": "result",
                        "session_id": "session-1",
                        "result": "failed",
                        "is_error": True,
                    }
                )
            )

    def test_streaming_timeout_is_nonzero_and_redacts_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            command = [
                sys.executable,
                "-c",
                "import sys,time; print('secret-value', flush=True); "
                "print('secret-value', file=sys.stderr, flush=True); time.sleep(10)",
            ]
            completed, timed_out = run_claude_streaming(
                command,
                cwd=root,
                environment=os.environ,
                timeout=0.1,
                warning_after=0.05,
                heartbeat_interval=0.02,
                drain_timeout=0.1,
                termination_grace=0.1,
                secrets=("secret-value",),
                stdout_path=root / "stdout",
                stderr_path=root / "stderr",
                progress_path=root / "progress",
            )
            self.assertTrue(timed_out)
            self.assertEqual(completed.returncode, 124)
            self.assertNotIn("secret-value", completed.stdout + completed.stderr)
            self.assertIn("[REDACTED]", (root / "stdout").read_text(encoding="utf-8"))
            self.assertTrue((root / "progress").read_text(encoding="utf-8").strip())

    def test_streaming_kills_descendant_that_holds_pipes_after_leader_exit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pid_path = root / "child.pid"
            child = (
                "import os,signal,time; "
                "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                f"open({str(pid_path)!r}, 'w').write(str(os.getpid())); "
                "time.sleep(10)"
            )
            leader = (
                "import pathlib,subprocess,sys,time; "
                f"subprocess.Popen([sys.executable, '-c', {child!r}]); "
                f"p=pathlib.Path({str(pid_path)!r}); "
                "[(time.sleep(0.01)) for _ in range(100) if not p.exists()]"
            )
            completed, timed_out = run_claude_streaming(
                [sys.executable, "-c", leader],
                cwd=root,
                environment=os.environ,
                timeout=5,
                warning_after=0.05,
                heartbeat_interval=0.02,
                drain_timeout=0.1,
                termination_grace=0.1,
                secrets=(),
                stdout_path=root / "stdout",
                stderr_path=root / "stderr",
                progress_path=root / "progress",
            )
            self.assertTrue(timed_out)
            self.assertEqual(completed.returncode, 124)
            child_pid = int(pid_path.read_text(encoding="utf-8"))
            child_alive = True
            for _ in range(100):
                try:
                    os.kill(child_pid, 0)
                except ProcessLookupError:
                    child_alive = False
                    break
                time.sleep(0.01)
            if child_alive:
                os.kill(child_pid, signal.SIGKILL)
            self.assertFalse(child_alive, "SIGTERM-ignoring descendant survived cleanup")


if __name__ == "__main__":
    unittest.main()
