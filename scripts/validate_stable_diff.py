#!/usr/bin/env python3
"""Prove that stable promotion changes no unexplained packaged runtime bytes."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "stable_1_0_allowed_diff.json"
PLUGIN_NAMES = (
    "market-research-agent",
    "pre-award-agent",
    "govcon-growth-agent",
    "other-transaction-agent",
    "acquisition-policy-agent",
)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def validate() -> list[str]:
    errors: list[str] = []
    record = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base_tag = record["base_tag"]
    expected_commit = record["base_commit"]
    resolved = git("rev-list", "-n", "1", base_tag)
    if resolved.returncode != 0:
        return [f"cannot resolve {base_tag}: {resolved.stderr.strip()}"]
    if resolved.stdout.strip() != expected_commit:
        errors.append(
            f"{base_tag} resolves to {resolved.stdout.strip()}, expected {expected_commit}"
        )

    allowed: set[str] = set()
    for plugin in PLUGIN_NAMES:
        allowed.update(
            {
                f"plugins/{plugin}/plugin.json",
                f"plugins/{plugin}/.codex-plugin/plugin.json",
                f"plugins/{plugin}/.claude-plugin/plugin.json",
                f"plugins/{plugin}/README.md",
                f"plugins/{plugin}/test.md",
            }
        )
    runtime_path = record["runtime_change"]["path"]
    allowed.add(runtime_path)

    target = record["target"]
    changed = git("diff", "--name-only", base_tag, target, "--", "plugins")
    if changed.returncode != 0:
        errors.append(changed.stderr.strip())
        return errors
    unexpected = sorted(set(changed.stdout.splitlines()) - allowed)
    if unexpected:
        errors.append("unexpected packaged paths changed: " + ", ".join(unexpected))

    before = git("show", f"{base_tag}:{runtime_path}")
    if before.returncode != 0:
        errors.append(f"cannot read base runtime file {runtime_path}")
        return errors
    old_text = record["runtime_change"]["old_text"]
    new_text = record["runtime_change"]["new_text"]
    if before.stdout.count(old_text) != 1:
        errors.append(f"base runtime file must contain exactly one approved old URL, found {before.stdout.count(old_text)}")
    expected = before.stdout.replace(old_text, new_text)
    target_file = git("show", f"{target}:{runtime_path}")
    if target_file.returncode != 0:
        errors.append(f"cannot read target runtime file {runtime_path}")
        return errors
    actual = target_file.stdout
    if actual != expected:
        errors.append("approved runtime file differs by more than the one source URL")

    for plugin in PLUGIN_NAMES:
        for relative in ("mcp.json", ".mcp.json"):
            path = f"plugins/{plugin}/{relative}"
            comparison = git("diff", "--quiet", base_tag, target, "--", path)
            if comparison.returncode != 0:
                errors.append(f"MCP manifest changed unexpectedly: {path}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Stable allowed-diff validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Stable allowed-diff proof passed: one approved source URL and no other runtime drift.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
