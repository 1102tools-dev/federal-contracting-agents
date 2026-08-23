#!/usr/bin/env python3
"""Offline-first RC5 credential, pacing, and MCP drift canaries.

The default command performs no network, client, credential, or package
operations.  ``--live`` only invokes a caller-supplied MCP runner through a
JSON-over-stdin contract; this module never calls an upstream API directly.
The runner must return one JSON object per invocation.  Its output is parsed,
normalized, and redacted before it can enter the ledger.

The module deliberately records credential presence and failure classes, not
credential values.  Live runner stderr/stdout are never forwarded to the
terminal.  A runner that emits malformed JSON is represented by a bounded
failure record rather than its output.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import os
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


HERE = Path(__file__).resolve().parent
DEFAULT_MATRIX = HERE / "canary_matrix.json"
DEFAULT_CREDENTIALS = ("SAM_API_KEY", "BLS_API_KEY", "REGULATIONS_GOV_API_KEY")
REDACTED = "[REDACTED]"
_SECRET_KEY_RE = re.compile(r"(?i)(?:api[_-]?key|token|password|secret|authorization)")
_ASSIGNMENT_RE = re.compile(
    r"(?i)(?P<prefix>\b(?:[A-Z][A-Z0-9_-]*(?:API[_-]?KEY|TOKEN|PASSWORD|SECRET)|AUTHORIZATION)\s*[:=]\s*)(?P<value>[^\s,;}]+)"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class SecretRedactor:
    """Redact known secret values and credential-looking assignments."""

    def __init__(self, secrets: Iterable[str] = ()) -> None:
        # Values are retained only for the duration of this in-memory
        # sanitization operation.  They are never placed in a result record.
        self._secrets = tuple(sorted({s for s in secrets if isinstance(s, str) and len(s) >= 4}, key=len, reverse=True))

    def redact_text(self, text: str) -> str:
        result = text
        for secret in self._secrets:
            result = result.replace(secret, REDACTED)
        return _ASSIGNMENT_RE.sub(lambda match: match.group("prefix") + REDACTED, result)

    def redact(self, value: Any, *, key: str | None = None) -> Any:
        if key and _SECRET_KEY_RE.search(key):
            return REDACTED if value not in (None, "") else value
        if isinstance(value, str):
            return self.redact_text(value)
        if isinstance(value, Mapping):
            return {str(k): self.redact(v, key=str(k)) for k, v in value.items()}
        if isinstance(value, list):
            return [self.redact(v) for v in value]
        if isinstance(value, tuple):
            return [self.redact(v) for v in value]
        return value


def assert_exact_values_redacted(value: Any, secrets: Iterable[str]) -> None:
    """Raise if any supplied exact secret survives JSON-safe sanitization."""

    text = canonical_json(value)
    leaked = [secret for secret in secrets if secret and secret in text]
    if leaked:
        raise AssertionError("credential value survived redaction")


@dataclass(frozen=True)
class CredentialState:
    name: str
    state: str
    credential_present: bool
    expected_failure_class: str | None
    max_attempts: int


def credential_states(name: str) -> tuple[CredentialState, ...]:
    """Return metadata for the four required states without storing values."""

    return (
        CredentialState(name, "missing", False, "missing_credential", 0),
        CredentialState(name, "invalid", True, "authentication_failure", 1),
        CredentialState(name, "valid", True, None, 1),
        CredentialState(name, "rate_limited", True, "rate_limited_retry_after", 1),
    )


def credential_matrix(
    env: Mapping[str, str] | None = None,
    names: Sequence[str] = DEFAULT_CREDENTIALS,
) -> list[dict[str, Any]]:
    """Describe credential behavior using presence booleans only.

    ``env`` is accepted for testability, but values are read only to compute a
    boolean and are never copied into the returned records.
    """

    source = os.environ if env is None else env
    records: list[dict[str, Any]] = []
    for name in names:
        present = bool(source.get(name))
        for state in credential_states(name):
            records.append(
                {
                    "credential_name": state.name,
                    "state": state.state,
                    "credential_present": state.credential_present,
                    "observed_environment_present": present,
                    "expected_failure_class": state.expected_failure_class,
                    "max_attempts": state.max_attempts,
                    "value_recorded": False,
                }
            )
    return records


@dataclass(frozen=True)
class MockResponse:
    status: int
    retry_after_seconds: float | None = None
    body_shape: str = "object"


@dataclass(frozen=True)
class SimulatedRequest:
    request_id: str
    requested_at: float
    duration_seconds: float
    responses: tuple[MockResponse, ...]
    max_attempts: int = 2


@dataclass(frozen=True)
class PacingEvent:
    request_id: str
    attempt: int
    status: int
    requested_at: float
    started_at: float
    completed_at: float
    retry_after_seconds: float | None


def simulate_concurrent_calls(
    requests: Sequence[SimulatedRequest],
    min_interval_seconds: float = 3.0,
) -> list[PacingEvent]:
    """Run a deterministic virtual shared-key scheduler.

    Multiple callers may request work at the same instant.  The scheduler
    serializes attempts and measures the next eligible start from completion,
    honoring a longer captured ``Retry-After`` without sleeping or contacting
    a provider.
    """

    if min_interval_seconds < 0:
        raise ValueError("min_interval_seconds must be nonnegative")
    pending: list[tuple[float, int, int]] = [
        (request.requested_at, index, 0) for index, request in enumerate(requests)
    ]
    heapq.heapify(pending)
    next_allowed = float("-inf")
    events: list[PacingEvent] = []
    while pending:
        requested_at, index, attempt = heapq.heappop(pending)
        request = requests[index]
        started_at = max(requested_at, next_allowed)
        completed_at = started_at + request.duration_seconds
        response = request.responses[min(attempt, len(request.responses) - 1)]
        events.append(
            PacingEvent(
                request_id=request.request_id,
                attempt=attempt + 1,
                status=response.status,
                requested_at=requested_at,
                started_at=started_at,
                completed_at=completed_at,
                retry_after_seconds=response.retry_after_seconds,
            )
        )
        retry_after = response.retry_after_seconds or 0.0
        next_allowed = completed_at + max(min_interval_seconds, retry_after)
        if response.status == 429 and attempt + 1 < request.max_attempts:
            retry_at = completed_at + retry_after
            heapq.heappush(pending, (retry_at, index, attempt + 1))
    return events


def validate_pacing(events: Sequence[PacingEvent], min_interval_seconds: float) -> list[str]:
    """Return violations; an empty list means serialization/pacing passed."""

    violations: list[str] = []
    ordered = sorted(events, key=lambda event: (event.started_at, event.request_id, event.attempt))
    for previous, current in zip(ordered, ordered[1:]):
        gap = current.started_at - previous.completed_at
        if gap + 1e-9 < min_interval_seconds:
            violations.append(f"{previous.request_id}->{current.request_id}: interval below configured minimum")
    return violations


def run_pacing_canary(min_interval_seconds: float = 3.0) -> dict[str, Any]:
    """Exercise a local captured 429 and simultaneous callers."""

    events = simulate_concurrent_calls(
        (
            SimulatedRequest("caller-a", 0.0, 1.0, (MockResponse(429, 5.0), MockResponse(200))),
            SimulatedRequest("caller-b", 0.0, 1.0, (MockResponse(200),)),
            SimulatedRequest("caller-c", 0.0, 1.0, (MockResponse(200),)),
        ),
        min_interval_seconds=min_interval_seconds,
    )
    violations = validate_pacing(events, min_interval_seconds)
    retry_events = [event for event in events if event.status == 429]
    retry_honored = bool(retry_events) and all(
        next_event.started_at >= event.completed_at + (event.retry_after_seconds or 0.0) - 1e-9
        for event in retry_events
        for next_event in events
        if next_event.request_id == event.request_id and next_event.attempt > event.attempt
    )
    return {
        "status": "pass" if not violations and retry_honored else "fail",
        "mode": "offline",
        "provider_calls": len(events),
        "captured_429": bool(retry_events),
        "retry_after_honored": retry_honored,
        "pacing_violations": violations,
        "events": [event.__dict__ for event in events],
    }


def normalized_shape(value: Any) -> Any:
    """Return a stable, value-free description of a JSON response shape."""

    if isinstance(value, Mapping):
        return {"type": "object", "keys": sorted(str(key) for key in value)}
    if isinstance(value, list):
        return {"type": "array", "item": normalized_shape(value[0]) if value else None}
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, (int, float)):
        return {"type": "number"}
    return {"type": "string"}


def _safe_runner_error(returncode: int, timed_out: bool = False) -> dict[str, Any]:
    return {
        "status": "fail",
        "failure_class": "runner_timeout" if timed_out else "runner_protocol_error",
        "runner_exit_code": None if timed_out else returncode,
        "raw_output_recorded": False,
    }


def classify_drift(
    definition: Mapping[str, Any],
    tool_names: Sequence[str],
    schema_hash: str,
    source_hashes: Mapping[str, Any] | None,
) -> tuple[str, str | None]:
    """Classify deterministic contract drift without judging volatile data."""

    expected_tools = definition.get("expected_tool_names")
    if expected_tools is not None and sorted(str(item) for item in expected_tools) != sorted(tool_names):
        return "p1_tool_schema_loss", "required tool names changed"
    expected_schema = definition.get("expected_schema_hash")
    if expected_schema and expected_schema != schema_hash:
        return "p1_tool_schema_loss", "tool input schema hash changed"
    expected_sources = definition.get("expected_source_hashes")
    if isinstance(expected_sources, Mapping) and isinstance(source_hashes, Mapping):
        changed = [
            str(key)
            for key, expected in expected_sources.items()
            if key in source_hashes and source_hashes[key] != expected
        ]
        if changed:
            return "advisory_source_hash_change", ",".join(sorted(changed))
    return "baseline_not_configured", None


def run_live_mcp_canary(
    definition: Mapping[str, Any],
    runner_command: Sequence[str],
    *,
    timeout_seconds: float = 90.0,
    secrets: Iterable[str] = (),
) -> dict[str, Any]:
    """Invoke an external MCP-aware runner and record a sanitized canary.

    The runner receives a descriptor on stdin and must return JSON with
    ``version``, ``tools`` (list of name/schema objects), ``response``, and
    optional ``warnings``/``source_hashes``.  The runner is responsible for
    using the configured MCP/client path; this function has no HTTP/API bypass.
    """

    descriptor = {
        "operation": "mcp_canary",
        "server": definition["server"],
        "distribution": definition["distribution"],
        "pinned_version": definition["pinned_version"],
        "requested_operation": definition["operation"],
    }
    started = time.monotonic()
    try:
        completed = subprocess.run(
            list(runner_command),
            input=canonical_json(descriptor) + "\n",
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {
            "server": definition["server"],
            "distribution": definition["distribution"],
            "captured_at": utc_now(),
            "duration_seconds": round(time.monotonic() - started, 6),
            **_safe_runner_error(-1, timed_out=True),
        }
    if completed.returncode != 0:
        return {
            "server": definition["server"],
            "distribution": definition["distribution"],
            "captured_at": utc_now(),
            "duration_seconds": round(time.monotonic() - started, 6),
            **_safe_runner_error(completed.returncode),
        }
    try:
        result = json.loads(completed.stdout)
    except (json.JSONDecodeError, TypeError):
        return {
            "server": definition["server"],
            "distribution": definition["distribution"],
            "captured_at": utc_now(),
            "duration_seconds": round(time.monotonic() - started, 6),
            **_safe_runner_error(completed.returncode),
        }
    if not isinstance(result, Mapping):
        return {
            "server": definition["server"],
            "distribution": definition["distribution"],
            "captured_at": utc_now(),
            "duration_seconds": round(time.monotonic() - started, 6),
            **_safe_runner_error(completed.returncode),
        }
    redactor = SecretRedactor(secrets)
    tools = result.get("tools", [])
    if not isinstance(tools, list):
        tools = []
    tool_names = sorted(
        str(tool.get("name"))
        for tool in tools
        if isinstance(tool, Mapping) and tool.get("name") is not None
    )
    raw_tool_names = list(tool_names)
    tool_names = [redactor.redact_text(name) for name in tool_names]
    schemas = [tool.get("inputSchema", tool.get("schema", {})) for tool in tools if isinstance(tool, Mapping)]
    response = result.get("response")
    source_hashes = result.get("source_hashes", {})
    if not isinstance(source_hashes, Mapping):
        source_hashes = {}
    drift_classification, drift_note = classify_drift(
        definition, raw_tool_names, sha256_json(schemas), source_hashes
    )
    drift_failed = drift_classification.startswith("p1_")
    record = {
        "server": definition["server"],
        "distribution": definition["distribution"],
        "pinned_version": definition["pinned_version"],
        "discovered_version": redactor.redact(result.get("version")),
        "tool_count": len(tool_names),
        "tool_names": tool_names,
        "schema_hash": sha256_json(schemas),
        "normalized_response_shape": normalized_shape(response),
        "warnings": redactor.redact(result.get("warnings", [])),
        "source_hashes": redactor.redact(source_hashes),
        "drift_classification": drift_classification,
        "drift_note": drift_note,
        "captured_at": utc_now(),
        "duration_seconds": round(time.monotonic() - started, 6),
        "status": "fail" if drift_failed else "pass",
        "raw_output_recorded": False,
    }
    assert_exact_values_redacted(record, secrets)
    return record


def load_matrix(path: Path = DEFAULT_MATRIX) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        matrix = json.load(handle)
    if not isinstance(matrix, dict):
        raise ValueError("canary matrix must be an object")
    return matrix


def run_offline(matrix: Mapping[str, Any]) -> dict[str, Any]:
    pacing = matrix.get("pacing", {})
    interval = float(pacing.get("default_min_interval_seconds", 3.0))
    return {
        "schema_version": 1,
        "round": matrix.get("round", "rc5"),
        "generated_at": utc_now(),
        "mode": "offline",
        "credentials": credential_matrix(names=tuple(item["name"] for item in matrix.get("credential_variables", []))),
        "pacing": run_pacing_canary(interval),
        "mcp_canaries": [
            {
                "server": item["server"],
                "distribution": item["distribution"],
                "pinned_version": item["pinned_version"],
                "status": "dry-run",
                "live_gate_required": True,
                "raw_output_recorded": False,
            }
            for item in matrix.get("mcp_canaries", [])
        ],
    }


def run_live(matrix: Mapping[str, Any], runner_command: Sequence[str], timeout_seconds: float) -> dict[str, Any]:
    # Values are used only to redact an external runner response in memory;
    # credential-presence metadata remains boolean-only in the ledger.
    secrets = tuple(value for name in DEFAULT_CREDENTIALS if (value := os.environ.get(name)))
    result = run_offline(matrix)
    result["mode"] = "live"
    result["mcp_canaries"] = [
        run_live_mcp_canary(item, runner_command, timeout_seconds=timeout_seconds, secrets=secrets)
        for item in matrix.get("mcp_canaries", [])
    ]
    assert_exact_values_redacted(result, secrets)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path, help="write the sanitized ledger to this path")
    parser.add_argument("--live", action="store_true", help="invoke the explicitly supplied MCP runner")
    parser.add_argument(
        "--runner",
        help="MCP-aware runner command; receives one JSON descriptor on stdin per canary",
    )
    parser.add_argument("--timeout", type=float, default=90.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.live and not args.runner:
        parser.error("--live requires --runner; direct upstream API calls are not supported")
    try:
        matrix = load_matrix(args.matrix)
        ledger = run_live(matrix, shlex.split(args.runner), args.timeout) if args.live else run_offline(matrix)
        rendered = json.dumps(ledger, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        # Error text is intentionally bounded; never echo subprocess output or
        # environment values into the terminal.
        parser.exit(2, f"canary harness error: {type(exc).__name__}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
