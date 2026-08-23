#!/usr/bin/env python3
"""Run the same no-network orchestration scenarios across supported clients."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from fnmatch import fnmatch
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = REPO_ROOT / "tests" / "routing_scenarios.json"
DEFAULT_MODELS = {
    "codex": "gpt-5.6-sol",
    "claude": "sonnet",
    "copilot": "gpt-5.4",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=tuple(DEFAULT_MODELS), required=True)
    parser.add_argument("--case", action="append", default=[], help="Case ID glob")
    parser.add_argument("--model")
    parser.add_argument(
        "--claude-fast",
        action="store_true",
        help="Opt a Claude Opus noninteractive session into fast mode",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def prompt_for(client: str, scenario: dict[str, object]) -> str:
    prompt = str(scenario["prompt"])
    if scenario["invocation"] != "explicit":
        return prompt
    skill = str(scenario["orchestrator"])
    plugin = str(scenario["plugin"])
    if client == "codex":
        return f"${skill}\n\n{prompt}"
    if client == "claude":
        return prompt
    return f"Explicitly use the {skill} skill. {prompt}"


def run_case(
    client: str,
    model: str,
    scenario: dict[str, object],
    *,
    claude_fast: bool = False,
) -> tuple[int, str, str]:
    plugin = str(scenario["plugin"])
    prompt = prompt_for(client, scenario)
    with tempfile.TemporaryDirectory() as directory:
        workdir = Path(directory)
        if client == "codex":
            output = workdir / "last-message.txt"
            command = [
                "codex", "exec", "--ephemeral", "--skip-git-repo-check",
                "-s", "read-only", "-m", model,
                "-c", 'model_reasoning_effort="xhigh"',
                "-C", str(workdir), "-o", str(output), prompt,
            ]
            result = subprocess.run(command, text=True, capture_output=True, timeout=180)
            text = output.read_text(encoding="utf-8") if output.exists() else result.stdout
            return result.returncode, text, result.stderr
        if client == "claude":
            command = [
                "claude", "-p", "--no-session-persistence",
                "--plugin-dir", str(REPO_ROOT / "plugins" / plugin),
                "--tools", "Read", "Skill",
                "--permission-mode", "bypassPermissions",
                "--model", model, "--effort", "high", prompt,
            ]
            if scenario["invocation"] == "explicit":
                command[3:3] = ["--agent", f"{plugin}:{plugin}"]
            if claude_fast:
                command[3:3] = ["--settings", '{"fastMode":true}']
            result = subprocess.run(command, text=True, capture_output=True, timeout=180)
            return result.returncode, result.stdout, result.stderr
        command = [
            "copilot", "-C", str(workdir),
            "--plugin-dir", str(REPO_ROOT / "plugins" / plugin),
            "--model", model, "--reasoning-effort", "high",
            "--allow-all-tools", "--no-custom-instructions", "--no-remote",
            "--silent", "-p", prompt,
        ]
        if scenario["invocation"] == "explicit":
            command[3:3] = ["--agent", plugin]
        result = subprocess.run(command, text=True, capture_output=True, timeout=180)
        return result.returncode, result.stdout, result.stderr


def grade(scenario: dict[str, object], output: str) -> tuple[bool, list[str]]:
    lowered = output.lower()
    failures: list[str] = []
    for alternatives in scenario["required_any"]:
        if not any(str(term).lower() in lowered for term in alternatives):
            failures.append(f"missing one of {alternatives}")
    for forbidden in scenario["forbidden"]:
        if str(forbidden).lower() in lowered:
            failures.append(f"contains forbidden phrase {forbidden!r}")
    return not failures, failures


def main() -> None:
    args = parse_args()
    model = args.model or DEFAULT_MODELS[args.client]
    if args.claude_fast and args.client != "claude":
        raise SystemExit("--claude-fast is valid only with --client claude")
    if args.claude_fast and "opus" not in model.lower():
        raise SystemExit("--claude-fast requires an Opus model")
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    patterns = args.case or ["*"]
    selected = [
        scenario
        for scenario in scenarios
        if any(fnmatch(scenario["id"], pattern) for pattern in patterns)
    ]
    if not selected:
        raise SystemExit("No scenarios matched")
    results: list[dict[str, object]] = []
    for scenario in selected:
        code, output, stderr = run_case(
            args.client,
            model,
            scenario,
            claude_fast=args.claude_fast,
        )
        passed, failures = grade(scenario, output) if code == 0 else (False, [f"client exit {code}"])
        results.append(
            {
                "id": scenario["id"],
                "client": args.client,
                "model": model,
                "passed": passed,
                "release_blocking": scenario.get("release_blocking", True),
                "failures": failures,
                "output": output.strip(),
                "stderr": stderr.strip(),
            }
        )
        status = "PASS" if passed else (
            "FAIL" if scenario.get("release_blocking", True) else "ADVISORY_FAIL"
        )
        print(f"{status} {scenario['id']}")
        for failure in failures:
            print(f"  {failure}")
    payload = {
        "client": args.client,
        "model": model,
        "claude_fast": args.claude_fast,
        "results": results,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if not all(result["passed"] or not result["release_blocking"] for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
