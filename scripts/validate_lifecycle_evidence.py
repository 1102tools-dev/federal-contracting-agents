#!/usr/bin/env python3
"""Validate the sanitized RC5 lifecycle ledger and current evidence wording.

This is intentionally a test-only check. It reads the ledger and test records;
it never touches client configuration, credentials, plugin caches, or upstream
services. Dated historical checkpoints remain valid, while an unqualified
present-tense preview/support claim must match the repository's current package
manifest and maintained Codex/Claude support contract.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = DEFAULT_ROOT / "tests" / "manual" / "rc5_lifecycle_ledger.json"
DEFAULT_SCHEMA = DEFAULT_ROOT / "tests" / "manual" / "rc5_lifecycle_ledger.schema.json"
PLUGIN_NAMES = (
    "market-research-agent",
    "pre-award-agent",
    "govcon-growth-agent",
    "other-transaction-agent",
    "acquisition-policy-agent",
)
LANE_IDS = {"install", "upgrade", "credentials", "resume", "concurrency", "drift", "long-session"}
HISTORICAL_MARKERS = ("historical", "before rc5", "pre-rc5", "superseded", "dated checkpoint")
CURRENT_PREVIEW_RE = re.compile(
    r"(?:current (?:public|installable) preview|public preview)\s+is\s+[`']?(1\.0\.0-rc\.\d+)",
    re.IGNORECASE,
)
VERSION_RE = re.compile(r"\bVersion:\s*[`']?(1\.0\.0-rc\.\d+)", re.IGNORECASE)
SUPPORT_TERMS = re.compile(r"\b(copilot|vs\s*code)\b", re.IGNORECASE)
SUPPORT_CLAIM_TERMS = re.compile(
    r"\b(?:maintained|support(?:ed)?|support\s+gate|release\s+gate|block(?:s|ed)?|open|pending|remain(?:s|ed)?|required)\b",
    re.IGNORECASE,
)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc


def schema_errors(ledger: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(ledger), key=lambda item: list(item.path))]


def _is_historical_heading(line: str) -> bool:
    lowered = line.lower()
    return lowered.startswith("#") and any(marker in lowered for marker in HISTORICAL_MARKERS)


def stale_claim_errors(root: Path) -> list[str]:
    """Find stale present-tense preview claims and current Copilot/VS Code gates."""
    errors: list[str] = []
    current_versions: dict[str, str] = {}
    for plugin in PLUGIN_NAMES:
        manifest_path = root / "plugins" / plugin / "plugin.json"
        try:
            manifest = load_json(manifest_path)
            current_versions[plugin] = manifest["version"]
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"{manifest_path.relative_to(root)}: cannot resolve current package version: {exc}")

    records = sorted((root / "plugins").glob("*/test.md"))
    for path in records:
        plugin = path.parent.name
        expected = current_versions.get(plugin)
        historical = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                historical = _is_historical_heading(stripped)
            if historical:
                continue

            preview_match = CURRENT_PREVIEW_RE.search(line)
            if preview_match and expected and preview_match.group(1) != expected:
                errors.append(
                    f"{path.relative_to(root)}:{number}: current preview {preview_match.group(1)!r} "
                    f"does not match manifest {expected!r}"
                )
            version_match = VERSION_RE.search(line)
            if version_match and expected and version_match.group(1) != expected:
                errors.append(
                    f"{path.relative_to(root)}:{number}: current Version {version_match.group(1)!r} "
                    f"does not match manifest {expected!r}"
                )

            lowered = line.lower()
            if SUPPORT_TERMS.search(line) and SUPPORT_CLAIM_TERMS.search(line):
                if "historical" not in lowered and "not current" not in lowered and "compatibility observation" not in lowered:
                    errors.append(
                        f"{path.relative_to(root)}:{number}: unqualified Copilot/VS Code current-support or gate claim"
                    )
    return errors


def semantic_errors(ledger: dict[str, Any], root: Path = DEFAULT_ROOT) -> list[str]:
    errors: list[str] = []
    package_names = {item.get("name") for item in ledger.get("packages", [])}
    if package_names != set(PLUGIN_NAMES):
        errors.append(f"ledger packages must be exactly {sorted(PLUGIN_NAMES)}")
    for item in ledger.get("packages", []):
        name = item.get("name")
        if name not in PLUGIN_NAMES:
            continue
        manifest = load_json(root / "plugins" / name / "plugin.json")
        if item.get("target_version") != manifest.get("version"):
            errors.append(
                f"ledger target for {name} must match manifest version {manifest.get('version')!r}"
            )
    lane_ids = {item.get("id") for item in ledger.get("lanes", [])}
    if lane_ids != LANE_IDS:
        errors.append(f"ledger lanes must be exactly {sorted(LANE_IDS)}")
    credential_names = {item.get("name") for item in ledger.get("credentials", [])}
    expected_credentials = {
        "SAM_API_KEY",
        "BLS_API_KEY",
        "REGULATIONS_GOV_API_KEY",
        "PERDIEM_API_KEY",
    }
    if credential_names != expected_credentials:
        errors.append(f"ledger credentials must be exactly {sorted(expected_credentials)}")
    canary_servers = {item.get("server") for item in ledger.get("mcp_canaries", [])}
    expected_canaries = {"acquisition-gov", "bls-oews", "ecfr", "federal-register", "gsa-calc", "gsa-perdiem", "regulations-gov", "sam-gov", "usaspending"}
    if canary_servers != expected_canaries:
        errors.append(f"ledger MCP canaries must be exactly {sorted(expected_canaries)}")
    if ledger.get("status") == "pending":
        pending_artifacts = [item for item in ledger.get("artifacts", []) if item.get("result") != "pending"]
        if pending_artifacts:
            errors.append("pending ledger cannot contain completed artifact results")
    return errors


def validate(root: Path, ledger_path: Path, schema_path: Path) -> list[str]:
    try:
        ledger = load_json(ledger_path)
        schema = load_json(schema_path)
    except ValueError as exc:
        return [str(exc)]
    errors = [f"{ledger_path}: {message}" for message in schema_errors(ledger, schema)]
    errors.extend(semantic_errors(ledger, root))
    errors.extend(stale_claim_errors(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()
    errors = validate(args.repo_root.resolve(), args.ledger.resolve(), args.schema.resolve())
    if errors:
        print("Lifecycle evidence validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("RC5 lifecycle ledger schema and present-tense evidence claims passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
