#!/usr/bin/env python3
"""Run one resumable RC5 client turn and store credential-safe evidence.

The caller supplies one prompt file, one working directory, and optionally a
captured session ID.  This runner deliberately executes exactly one client
turn so the release captain can inspect each approval checkpoint before the
next turn.  Credential values are loaded only into the child environment and
are redacted in memory before stdout or stderr is written to disk.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


KNOWN_CREDENTIALS = (
    "SAM_API_KEY",
    "BLS_API_KEY",
    "REGULATIONS_GOV_API_KEY",
    "PERDIEM_API_KEY",
)
DEFAULT_CODEX = Path("/Applications/ChatGPT.app/Contents/Resources/codex")
DEFAULT_CLAUDE = Path.home() / ".local" / "bin" / "claude"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_credentials(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    data = json.loads(path.expanduser().read_text(encoding="utf-8"))
    found: dict[str, str] = {}

    def visit(item: Any) -> None:
        if isinstance(item, Mapping):
            for key, value in item.items():
                if key in KNOWN_CREDENTIALS and isinstance(value, str) and value:
                    if len(value) < 4:
                        raise ValueError(f"{key} credential value is too short for safe redaction")
                    found[key] = value
                visit(value)
        elif isinstance(item, list):
            for value in item:
                visit(value)

    visit(data)
    return found


def apply_credential_state(
    environment: dict[str, str], credentials: Mapping[str, str], state: str
) -> dict[str, bool]:
    for name in KNOWN_CREDENTIALS:
        environment.pop(name, None)
    if state == "valid":
        environment.update(credentials)
    elif state == "invalid-sam":
        environment.update(credentials)
        environment["SAM_API_KEY"] = "rc5-invalid-placeholder"
    elif state == "invalid-bls":
        environment.update(credentials)
        environment["BLS_API_KEY"] = "rc5-invalid-placeholder"
    elif state == "invalid-regulations":
        environment.update(credentials)
        environment["REGULATIONS_GOV_API_KEY"] = "rc5-invalid-placeholder"
    elif state == "invalid-perdiem":
        environment.update(credentials)
        environment["PERDIEM_API_KEY"] = "rc5-invalid-placeholder"
    elif state == "invalid-all":
        environment.update(credentials)
        for name in KNOWN_CREDENTIALS:
            environment[name] = "rc5-invalid-placeholder"
    elif state == "missing-sam":
        environment.update(credentials)
        environment.pop("SAM_API_KEY", None)
    elif state == "missing-all":
        pass
    else:
        raise ValueError(f"unsupported credential state: {state}")
    return {name: bool(environment.get(name)) for name in KNOWN_CREDENTIALS}


def redact_text(value: str, secrets: Sequence[str]) -> str:
    result = value
    for secret in sorted({item for item in secrets if len(item) >= 4}, key=len, reverse=True):
        result = result.replace(secret, "[REDACTED]")
    return result


def claude_command(args: argparse.Namespace, prompt: str) -> list[str]:
    command = [str(args.claude_binary)]
    if getattr(args, "claude_agent", None):
        command.extend(("--agent", str(args.claude_agent)))
    command.extend([
        "-p",
        prompt,
        "--model",
        args.model or "opus",
        "--effort",
        args.effort,
    ])
    if getattr(args, "claude_fast_mode", False):
        command.extend(("--settings", '{"fastMode":true}'))
    command.extend([
        "--output-format",
        "stream-json",
        "--verbose",
    ])
    if args.session_id:
        command.extend(("--resume", args.session_id))
    if args.mcp_config:
        command.extend(("--mcp-config", str(args.mcp_config), "--strict-mcp-config"))
    return command


def codex_command(args: argparse.Namespace, prompt: str) -> list[str]:
    prefix = [str(args.codex_binary)]
    if getattr(args, "codex_profile", None):
        prefix.extend(("--profile", str(args.codex_profile)))
    prefix.extend(("-c", f'model_reasoning_effort="{args.effort}"'))
    for override in getattr(args, "codex_config", ()):
        prefix.extend(("-c", str(override)))
    common = [
        "--json",
        "--model",
        args.model or "gpt-5.6-sol",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
    ]
    if args.session_id:
        return [*prefix, "exec", "resume", *common, args.session_id, prompt]
    return [*prefix, "exec", *common, prompt]


def apply_client_home(
    environment: dict[str, str], client: str, client_home: Path | None
) -> bool:
    """Point one test turn at an explicit isolated client home.

    This is intentionally opt-in and rejects the operator's real home. The
    caller creates the disposable profile before invoking the runner.
    """

    if client_home is None:
        return False
    resolved = client_home.expanduser().resolve()
    if resolved == Path.home().resolve():
        raise ValueError("--client-home must not be the operator's real home")
    client_dir = resolved / (".codex" if client == "codex" else ".claude")
    if not client_dir.is_dir():
        raise ValueError("isolated client directory does not exist")
    environment["HOME"] = str(resolved)
    environment["XDG_CONFIG_HOME"] = str(resolved / ".config")
    environment["XDG_CACHE_HOME"] = str(resolved / ".cache")
    environment["XDG_DATA_HOME"] = str(resolved / ".local" / "share")
    environment["XDG_STATE_HOME"] = str(resolved / ".local" / "state")
    if client == "codex":
        environment.pop("CLAUDE_CONFIG_DIR", None)
        environment["CODEX_HOME"] = str(client_dir)
    else:
        environment.pop("CODEX_HOME", None)
        environment["CLAUDE_CONFIG_DIR"] = str(client_dir)
    return True


def parse_claude(stdout: str) -> tuple[str | None, str, dict[str, Any]]:
    payloads: list[Mapping[str, Any]] = []
    try:
        parsed = json.loads(stdout)
        if isinstance(parsed, Mapping):
            payloads.append(parsed)
    except json.JSONDecodeError:
        for line in stdout.splitlines():
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, Mapping):
                payloads.append(parsed)
    if not payloads:
        raise ValueError("Claude emitted no parseable JSON events")
    result_payload = next(
        (item for item in reversed(payloads) if item.get("type") == "result"),
        None,
    )
    if result_payload is None and len(payloads) == 1 and "result" in payloads[0]:
        result_payload = payloads[0]
    if result_payload is None:
        raise ValueError("Claude stream ended without a final result event")
    if result_payload.get("is_error") is True:
        raise ValueError("Claude final result reported an error")
    session_id = next(
        (
            str(item["session_id"])
            for item in reversed(payloads)
            if isinstance(item.get("session_id"), str) and item.get("session_id")
        ),
        None,
    )
    usage = result_payload.get("modelUsage") or {}
    event_types = [str(item.get("type")) for item in payloads if item.get("type")]
    summary = {
        "model_usage": sorted(usage),
        "num_turns": result_payload.get("num_turns"),
        "duration_api_ms": result_payload.get("duration_api_ms"),
        "is_error": result_payload.get("is_error"),
        "fast_mode_state": result_payload.get("fast_mode_state"),
        "fast_mode_disabled_reason": result_payload.get("fast_mode_disabled_reason"),
        "event_count": len(event_types),
        "event_types": sorted(set(event_types)),
    }
    return session_id, str(result_payload.get("result") or ""), summary


def run_claude_streaming(
    command: Sequence[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    timeout: float,
    warning_after: float,
    heartbeat_interval: float,
    drain_timeout: float,
    termination_grace: float,
    secrets: Sequence[str],
    stdout_path: Path,
    stderr_path: Path,
    progress_path: Path,
) -> tuple[subprocess.CompletedProcess[str], bool]:
    """Stream credential-safe Claude evidence and emit content-free heartbeats."""

    process = subprocess.Popen(
        list(command),
        cwd=cwd,
        env=dict(environment),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        start_new_session=True,
    )
    events: queue.Queue[tuple[str, str | None]] = queue.Queue()

    def pump(name: str, stream: Any) -> None:
        try:
            for line in iter(stream.readline, ""):
                events.put((name, line))
        finally:
            stream.close()
            events.put((name, None))

    assert process.stdout is not None and process.stderr is not None
    threads = (
        threading.Thread(target=pump, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=pump, args=("stderr", process.stderr), daemon=True),
    )
    for thread in threads:
        thread.start()

    started = time.monotonic()
    next_heartbeat = started + heartbeat_interval
    closed: set[str] = set()
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    last_event_type: str | None = None
    timed_out = False
    leader_exited_at: float | None = None

    def terminate_process_group() -> None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        if termination_grace > 0:
            time.sleep(termination_grace)
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)

    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr_file, progress_path.open("w", encoding="utf-8") as progress_file:
        while len(closed) < 2 or process.poll() is None:
            try:
                source, raw = events.get(timeout=0.25)
            except queue.Empty:
                source = ""
                raw = None
            if source:
                if raw is None:
                    closed.add(source)
                else:
                    safe = redact_text(raw, secrets)
                    target = stdout_file if source == "stdout" else stderr_file
                    parts = stdout_parts if source == "stdout" else stderr_parts
                    target.write(safe)
                    target.flush()
                    parts.append(safe)
                    if source == "stdout":
                        try:
                            parsed = json.loads(safe)
                        except json.JSONDecodeError:
                            parsed = None
                        if isinstance(parsed, Mapping) and parsed.get("type"):
                            last_event_type = str(parsed["type"])
            now = time.monotonic()
            elapsed = now - started
            if process.poll() is not None and leader_exited_at is None:
                leader_exited_at = now
            if now >= next_heartbeat:
                progress_file.write(
                    json.dumps(
                        {
                            "at": utc_now(),
                            "elapsed_seconds": round(elapsed, 3),
                            "last_event_type": last_event_type,
                            "process_running": process.poll() is None,
                            "warning_threshold_reached": elapsed >= warning_after,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
                progress_file.flush()
                next_heartbeat = now + heartbeat_interval
            if process.poll() is None and elapsed >= timeout:
                timed_out = True
                terminate_process_group()
                break
            if (
                leader_exited_at is not None
                and len(closed) < 2
                and now - leader_exited_at >= drain_timeout
            ):
                timed_out = True
                terminate_process_group()
                break
        for thread in threads:
            thread.join(timeout=2)
        if any(thread.is_alive() for thread in threads):
            timed_out = True
            terminate_process_group()
    if process.returncode is None:
        try:
            process.wait(timeout=0)
        except subprocess.TimeoutExpired:
            timed_out = True
            terminate_process_group()
    return subprocess.CompletedProcess(
        list(command),
        124 if timed_out else int(process.returncode if process.returncode is not None else 125),
        "".join(stdout_parts),
        "".join(stderr_parts),
    ), timed_out


def parse_codex(stdout: str) -> tuple[str | None, str, dict[str, Any]]:
    thread_id: str | None = None
    responses: list[str] = []
    event_types: list[str] = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        event_type = str(event.get("type") or "")
        if event_type:
            event_types.append(event_type)
        if event_type == "thread.started":
            thread_id = event.get("thread_id")
        item = event.get("item")
        if event_type == "item.completed" and isinstance(item, Mapping):
            if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                responses.append(item["text"])
    return thread_id, (responses[-1] if responses else ""), {
        "event_count": len(event_types),
        "event_types": sorted(set(event_types)),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--client", choices=("codex", "claude"), required=True)
    result.add_argument("--workdir", type=Path, required=True)
    result.add_argument("--prompt-file", type=Path, required=True)
    result.add_argument("--turn", type=int, required=True)
    result.add_argument("--session-id")
    result.add_argument("--credential-source", type=Path)
    result.add_argument(
        "--credential-state",
        choices=(
            "valid",
            "invalid-sam",
            "invalid-bls",
            "invalid-regulations",
            "invalid-perdiem",
            "invalid-all",
            "missing-sam",
            "missing-all",
        ),
        default="valid",
    )
    result.add_argument("--mcp-config", type=Path)
    result.add_argument("--model")
    result.add_argument("--effort", default="high")
    result.add_argument(
        "--claude-fast-mode",
        action="store_true",
        help="opt a Claude turn into fast mode; default is off",
    )
    result.add_argument("--codex-binary", type=Path, default=DEFAULT_CODEX)
    result.add_argument("--claude-binary", type=Path, default=DEFAULT_CLAUDE)
    result.add_argument("--claude-agent")
    result.add_argument("--client-home", type=Path)
    result.add_argument("--codex-profile")
    result.add_argument("--codex-config", action="append", default=[])
    result.add_argument("--timeout", type=float, default=1800)
    result.add_argument("--warning-after", type=float, default=600)
    result.add_argument("--heartbeat-interval", type=float, default=30)
    result.add_argument("--stream-drain-timeout", type=float, default=5)
    result.add_argument("--termination-grace", type=float, default=2)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    args.workdir.mkdir(parents=True, exist_ok=True)
    prompt = args.prompt_file.read_text(encoding="utf-8").strip()
    credentials = load_credentials(args.credential_source)
    environment = os.environ.copy()
    presence = apply_credential_state(environment, credentials, args.credential_state)
    isolated_client_home = apply_client_home(environment, args.client, args.client_home)
    command = claude_command(args, prompt) if args.client == "claude" else codex_command(args, prompt)
    stem = f"turn{args.turn}"
    secrets = tuple(credentials.values())
    started_at = utc_now()
    started = time.monotonic()
    if args.client == "claude":
        completed, timed_out = run_claude_streaming(
            command,
            cwd=args.workdir,
            environment=environment,
            timeout=args.timeout,
            warning_after=args.warning_after,
            heartbeat_interval=args.heartbeat_interval,
            drain_timeout=args.stream_drain_timeout,
            termination_grace=args.termination_grace,
            secrets=secrets,
            stdout_path=args.workdir / f"{stem}.stdout",
            stderr_path=args.workdir / f"{stem}.stderr",
            progress_path=args.workdir / f"{stem}.progress.jsonl",
        )
    else:
        try:
            completed = subprocess.run(
                command,
                cwd=args.workdir,
                env=environment,
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
            timed_out = False
        except subprocess.TimeoutExpired as exc:
            completed = subprocess.CompletedProcess(command, 124, exc.stdout or "", exc.stderr or "")
            timed_out = True
    elapsed = round(time.monotonic() - started, 6)
    safe_stdout = redact_text(str(completed.stdout or ""), secrets)
    safe_stderr = redact_text(str(completed.stderr or ""), secrets)
    if args.client != "claude":
        (args.workdir / f"{stem}.stdout").write_text(safe_stdout, encoding="utf-8")
        (args.workdir / f"{stem}.stderr").write_text(safe_stderr, encoding="utf-8")
    session_id: str | None = None
    response = ""
    client_meta: dict[str, Any] = {}
    parse_error: str | None = None
    if completed.returncode == 0:
        try:
            if args.client == "claude":
                session_id, response, client_meta = parse_claude(safe_stdout)
            else:
                session_id, response, client_meta = parse_codex(safe_stdout)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            parse_error = type(exc).__name__
    (args.workdir / f"{stem}.response.md").write_text(response, encoding="utf-8")
    meta = {
        "schema_version": 1,
        "client": args.client,
        "turn": args.turn,
        "started_at": started_at,
        "completed_at": utc_now(),
        "elapsed_seconds": elapsed,
        "returncode": completed.returncode,
        "timed_out": timed_out,
        "session_id": session_id,
        "resumed_session_id": args.session_id,
        "model_requested": args.model or ("opus" if args.client == "claude" else "gpt-5.6-sol"),
        "effort_requested": args.effort,
        "fast_mode_requested": bool(
            args.client == "claude" and getattr(args, "claude_fast_mode", False)
        ),
        "fast_mode_effective": (
            client_meta.get("fast_mode_state") if args.client == "claude" else None
        ),
        "credential_state": args.credential_state,
        "credential_presence": presence,
        "credential_values_recorded": False,
        "isolated_client_home": isolated_client_home,
        "codex_profile": args.codex_profile if args.client == "codex" else None,
        "claude_agent": args.claude_agent if args.client == "claude" else None,
        "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
        "stdout_sha256": sha256_bytes(safe_stdout.encode("utf-8")),
        "stderr_sha256": sha256_bytes(safe_stderr.encode("utf-8")),
        "response_sha256": sha256_bytes(response.encode("utf-8")),
        "parse_error": parse_error,
        "timeout_seconds": args.timeout,
        "warning_after_seconds": args.warning_after,
        "heartbeat_interval_seconds": args.heartbeat_interval,
        "stream_drain_timeout_seconds": args.stream_drain_timeout if args.client == "claude" else None,
        "termination_grace_seconds": args.termination_grace if args.client == "claude" else None,
        "progress_path": f"{stem}.progress.jsonl" if args.client == "claude" else None,
        "progress_sha256": (
            sha256_bytes((args.workdir / f"{stem}.progress.jsonl").read_bytes())
            if args.client == "claude" and (args.workdir / f"{stem}.progress.jsonl").exists()
            else None
        ),
        **client_meta,
    }
    rendered = json.dumps(meta, indent=2, sort_keys=True) + "\n"
    (args.workdir / f"{stem}.meta.json").write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if completed.returncode == 0 and not timed_out and parse_error is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
