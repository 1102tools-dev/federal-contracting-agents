#!/usr/bin/env python3
"""Safe, declarative lifecycle planning for the 1102tools agent packages.

This module deliberately defaults to a *plan*.  The live client commands are
only run when the caller supplies ``--execute`` and an explicit temporary
client home.  The package repository and the user's real ``~/.claude`` and
``~/.codex`` trees are never mutation targets of this harness.

The runner records package names, versions, paths, command status, and file
metadata.  It does not record command output or configuration contents.  A
small set of credential names is represented as presence booleans only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MATRIX = Path(__file__).with_name("lifecycle_matrix.json")
KNOWN_CREDENTIALS = (
    "SAM_API_KEY",
    "BLS_API_KEY",
    "REGULATIONS_GOV_API_KEY",
    "PERDIEM_API_KEY",
)
AGENT_IDS = (
    "market-research-agent",
    "pre-award-agent",
    "govcon-growth-agent",
    "other-transaction-agent",
    "acquisition-policy-agent",
)
MARKETPLACE_MANIFESTS = (
    ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
    ".github/plugin/marketplace.json",
)
EVIDENCE_LANES = (
    "credentials",
    "resume",
    "concurrency",
    "drift",
    "long-session",
)

HISTORICAL_TAGS = {
    "rc4": "v1.2.0-rc.4",
    "rc5": "v1.2.0-rc.5",
}
HISTORICAL_VERSIONS = {
    "rc4": {
        "market-research-agent": "1.0.0-rc.4",
        "pre-award-agent": "1.0.0-rc.4",
        "govcon-growth-agent": "1.0.0-rc.3",
        "other-transaction-agent": "1.0.0-rc.4",
        "acquisition-policy-agent": "1.0.0-rc.2",
    },
    "rc5": {
        "market-research-agent": "1.0.0-rc.5",
        "pre-award-agent": "1.0.0-rc.5",
        "govcon-growth-agent": "1.0.0-rc.4",
        "other-transaction-agent": "1.0.0-rc.5",
        "acquisition-policy-agent": "1.0.0-rc.3",
    },
}


class LifecycleSafetyError(ValueError):
    """Raised when a requested path or operation is outside the harness scope."""


class CommandRunner(Protocol):
    def run(self, argv: Sequence[str], *, cwd: Path | None = None) -> "CommandResult":
        ...


@dataclass(frozen=True)
class CommandResult:
    argv: tuple[str, ...]
    returncode: int
    stdout_length: int = 0
    stderr_length: int = 0

    def as_dict(self) -> dict[str, Any]:
        # Lengths are useful evidence without ever persisting potentially
        # sensitive command output (including environment dumps).
        return {
            "argv": list(self.argv),
            "returncode": self.returncode,
            "stdout_length": self.stdout_length,
            "stderr_length": self.stderr_length,
        }


class SubprocessRunner:
    """Subprocess adapter that intentionally discards command output.

    Client-home variables are redirected to the explicit fake home so an
    execution run cannot silently mutate the operator's normal profile.
    """

    def __init__(self, profile: "ClientProfile") -> None:
        self.profile = profile

    def run(self, argv: Sequence[str], *, cwd: Path | None = None) -> CommandResult:
        environment = os.environ.copy()
        environment["HOME"] = str(self.profile.home)
        environment["XDG_CONFIG_HOME"] = str(self.profile.home / ".config")
        if self.profile.client == "codex":
            environment["CODEX_HOME"] = str(self.profile.client_dir)
        else:
            # Claude Code supports CLAUDE_CONFIG_DIR for isolated test state.
            environment["CLAUDE_CONFIG_DIR"] = str(self.profile.client_dir)
        completed = subprocess.run(
            list(argv),
            cwd=str(cwd) if cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
            text=True,
            check=False,
        )
        return CommandResult(
            tuple(str(part) for part in argv),
            completed.returncode,
            len(completed.stdout),
            len(completed.stderr),
        )


@dataclass(frozen=True)
class AgentSpec:
    plugin_id: str
    version: str


@dataclass(frozen=True)
class ClientProfile:
    """Resolved paths for one client under an explicit user home."""

    client: str
    home: Path
    marketplace: str = "1102tools"

    def __post_init__(self) -> None:
        if self.client not in {"codex", "claude"}:
            raise LifecycleSafetyError(f"unsupported client: {self.client}")
        object.__setattr__(self, "home", self.home.expanduser().resolve())

    @property
    def client_dir(self) -> Path:
        return self.home / (".codex" if self.client == "codex" else ".claude")

    @property
    def plugin_cache_root(self) -> Path:
        return self.client_dir / "plugins" / "cache" / self.marketplace

    @property
    def marketplace_root(self) -> Path:
        return self.client_dir / "plugins" / "marketplaces" / self.marketplace

    @property
    def config_files(self) -> tuple[Path, ...]:
        if self.client == "codex":
            return (
                self.client_dir / "config.toml",
                self.client_dir / "config.json",
                self.client_dir / "plugins.json",
            )
        return (
            self.client_dir / "settings.json",
            self.client_dir / "settings.local.json",
            self.client_dir / "plugins.json",
        )

    @property
    def allowed_scoped_paths(self) -> tuple[Path, ...]:
        return (self.plugin_cache_root, self.marketplace_root)

    def assert_safe_execution_home(self) -> None:
        """Reject real user homes and client directories as mutation targets."""

        actual_home = Path.home().resolve()
        if self.home == actual_home:
            raise LifecycleSafetyError(
                "--execute requires an explicit temporary home, not the current user home"
            )
        if self.home.name in {".claude", ".codex"}:
            raise LifecycleSafetyError("client directory cannot be used as the fake home")

    def assert_scoped_target(self, target: Path) -> Path:
        """Return a target only if it is exactly a known 1102tools root/child."""

        resolved = target.expanduser().resolve()
        for allowed in self.allowed_scoped_paths:
            allowed = allowed.resolve()
            if resolved == allowed or allowed in resolved.parents:
                return resolved
        raise LifecycleSafetyError(f"path is outside the scoped 1102tools roots: {target}")


@dataclass
class Plan:
    client: ClientProfile
    agents: tuple[AgentSpec, ...]
    commands: list[tuple[str, ...]] = field(default_factory=list)
    targets: list[Path] = field(default_factory=list)
    lane: str = "install"
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "client": self.client.client,
            "home": str(self.client.home),
            "lane": self.lane,
            "commands": [list(command) for command in self.commands],
            "scoped_targets": [str(path) for path in self.targets],
            "notes": list(self.notes),
        }


def load_matrix(path: Path = DEFAULT_MATRIX) -> dict[str, Any]:
    matrix = json.loads(path.read_text(encoding="utf-8"))
    if matrix.get("schema_version") != "1.0":
        raise LifecycleSafetyError(f"unsupported lifecycle matrix schema: {matrix.get('schema_version')!r}")
    for required in ("clients", "agents", "lifecycle_lanes"):
        if required not in matrix:
            raise LifecycleSafetyError(f"lifecycle matrix missing {required!r}")
    return matrix


def agent_specs(matrix: Mapping[str, Any]) -> tuple[AgentSpec, ...]:
    specs = tuple(AgentSpec(str(item["id"]), str(item["version"])) for item in matrix["agents"])
    ids = [spec.plugin_id for spec in specs]
    if len(set(ids)) != len(ids) or set(ids) != set(AGENT_IDS):
        raise LifecycleSafetyError("matrix must contain exactly the five 1102tools agents")
    return specs


def credential_presence(env: Mapping[str, str] | None = None) -> dict[str, bool]:
    """Return key presence only; values are never read into the ledger."""

    source = os.environ if env is None else env
    return {name: bool(source.get(name)) for name in KNOWN_CREDENTIALS}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scoped_backup_metadata(profile: ClientProfile) -> dict[str, Any]:
    """Capture metadata for relevant config files without copying their contents."""

    files: list[dict[str, Any]] = []
    for path in profile.config_files:
        record: dict[str, Any] = {"path": str(path), "exists": path.exists()}
        if path.is_file():
            stat = path.stat()
            record.update({"mode": oct(stat.st_mode & 0o777), "size": stat.st_size, "sha256": _sha256(path)})
        files.append(record)
    return {
        "client": profile.client,
        "home": str(profile.home),
        "files": files,
        "credential_presence": credential_presence(),
        "contents_saved": False,
    }


def _safe_relative_entries(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        item: dict[str, Any] = {"path": str(relative), "kind": "symlink" if path.is_symlink() else "file" if path.is_file() else "directory"}
        if path.is_file() and not path.is_symlink():
            item["size"] = path.stat().st_size
        entries.append(item)
    return entries


def _plugin_records(cache_root: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    if not cache_root.exists():
        return records
    for manifest in cache_root.rglob("plugin.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        plugin_id = data.get("name") or data.get("id")
        version = data.get("version")
        if isinstance(plugin_id, str) and isinstance(version, str):
            records.append({"id": plugin_id, "version": version, "relative_manifest": str(manifest.relative_to(cache_root))})
    return sorted(records, key=lambda item: (item["id"], item["version"], item["relative_manifest"]))


def capture_inventory(profile: ClientProfile) -> dict[str, Any]:
    """Capture a sanitized inventory scoped to the client and marketplace."""

    cache_root = profile.plugin_cache_root
    marketplace_root = profile.marketplace_root
    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "client": profile.client,
        "home": str(profile.home),
        "config": scoped_backup_metadata(profile),
        "plugins": _plugin_records(cache_root),
        "cache_entries": _safe_relative_entries(cache_root),
        "marketplace_entries": _safe_relative_entries(marketplace_root),
        "scoped_roots_present": {
            "cache": cache_root.exists(),
            "marketplace": marketplace_root.exists(),
        },
        "credential_presence": credential_presence(),
    }


def _base_commands(profile: ClientProfile, matrix: Mapping[str, Any]) -> tuple[str, ...]:
    config = matrix["clients"][profile.client]
    return tuple(str(part) for part in config["marketplace_add"])


def plan_install(profile: ClientProfile, matrix: Mapping[str, Any], specs: Iterable[AgentSpec]) -> Plan:
    specs = tuple(specs)
    config = matrix["clients"][profile.client]
    plan = Plan(profile, specs, lane="install", notes=["new-session refresh required after installation"])
    plan.commands.append(_base_commands(profile, matrix))
    command = str(config["install_subcommand"])
    for spec in specs:
        plan.commands.append((profile.client, "plugin", command, f"{spec.plugin_id}@{profile.marketplace}"))
    return plan


def plan_upgrade(profile: ClientProfile, matrix: Mapping[str, Any], specs: Iterable[AgentSpec]) -> Plan:
    specs = tuple(specs)
    config = matrix["clients"][profile.client]
    plan = Plan(profile, specs, lane="upgrade", notes=["assert no mixed old/new runtime files"])
    if profile.client == "claude":
        plan.commands.append(("claude", "plugin", "marketplace", "update", profile.marketplace))
        for spec in specs:
            plan.commands.append(("claude", "plugin", "update", f"{spec.plugin_id}@{profile.marketplace}"))
    else:
        # Codex has no separate plugin-update operation: refresh the
        # marketplace and replace each installed package explicitly.
        plan.notes.append("Codex marketplace refresh/upgrade precedes remove/add replacement")
        plan.commands.append(("codex", "plugin", "marketplace", "upgrade", profile.marketplace))
        for spec in specs:
            qualified = f"{spec.plugin_id}@{profile.marketplace}"
            plan.commands.append(("codex", "plugin", "remove", qualified))
            plan.commands.append(("codex", "plugin", "add", qualified))
    return plan


def plan_reinstall(profile: ClientProfile, matrix: Mapping[str, Any], specs: Iterable[AgentSpec]) -> Plan:
    plan = plan_install(profile, matrix, specs)
    plan.lane = "reinstall"
    plan.notes.append("compare normalized inventories before and after; require idempotence")
    return plan


def plan_uninstall(profile: ClientProfile, matrix: Mapping[str, Any], specs: Iterable[AgentSpec]) -> Plan:
    specs = tuple(specs)
    command = str(matrix["clients"][profile.client]["remove_subcommand"])
    plan = Plan(profile, specs, lane="uninstall", notes=["remove only explicit plugin IDs and resolved 1102tools roots"])
    for spec in specs:
        plan.commands.append((profile.client, "plugin", command, f"{spec.plugin_id}@{profile.marketplace}"))
    for target in profile.allowed_scoped_paths:
        plan.targets.append(profile.assert_scoped_target(target))
    return plan


def plan_restore(profile: ClientProfile, matrix: Mapping[str, Any], specs: Iterable[AgentSpec]) -> Plan:
    plan = plan_install(profile, matrix, specs)
    plan.lane = "restore"
    plan.notes = [
        "restore only the captured scoped configuration metadata if an operator performs restoration",
        "finish with a new-session refresh",
    ]
    return plan


def plan_evidence_lane(
    profile: ClientProfile,
    _matrix: Mapping[str, Any],
    specs: Iterable[AgentSpec],
    lane: str,
) -> Plan:
    """Describe a non-mutating evidence lane driven by its dedicated runner.

    These lanes intentionally contain no client-management commands. They use
    the installed packages and write only to the operator-supplied validation
    directory through ``runtime_canaries.py`` or ``client_session_runner.py``.
    """

    if lane not in EVIDENCE_LANES:
        raise LifecycleSafetyError(f"unsupported evidence lane: {lane}")
    runner = "runtime_canaries.py" if lane in {"credentials", "concurrency", "drift"} else "client_session_runner.py"
    return Plan(
        profile,
        tuple(specs),
        lane=lane,
        notes=[
            f"evidence-only lane; execute through tests/lifecycle/{runner}",
            "no marketplace, plugin, or client-configuration mutation",
            "raw evidence belongs outside the repository; commit only sanitized summaries and replay inputs",
        ],
    )


def build_plan(profile: ClientProfile, matrix: Mapping[str, Any], lane: str) -> Plan:
    specs = agent_specs(matrix)
    if lane in EVIDENCE_LANES:
        return plan_evidence_lane(profile, matrix, specs, lane)
    planners = {
        "install": plan_install,
        "upgrade": plan_upgrade,
        "reinstall": plan_reinstall,
        "uninstall": plan_uninstall,
        "restore": plan_restore,
    }
    try:
        return planners[lane](profile, matrix, specs)
    except KeyError as exc:
        raise LifecycleSafetyError(f"unsupported lifecycle lane: {lane}") from exc


def execute_plan(plan: Plan, runner: CommandRunner | None = None, *, cwd: Path | None = None) -> list[CommandResult]:
    """Execute client commands after the caller has opted into mutation."""

    plan.client.assert_safe_execution_home()
    command_runner = runner or SubprocessRunner(plan.client)
    return [command_runner.run(command, cwd=cwd) for command in plan.commands]


def remove_scoped_targets(profile: ClientProfile, targets: Iterable[Path]) -> list[str]:
    """Remove only resolved marketplace/cache roots named by an uninstall plan."""

    removed: list[str] = []
    for target in targets:
        resolved = profile.assert_scoped_target(target)
        if resolved not in profile.allowed_scoped_paths:
            raise LifecycleSafetyError(f"uninstall target must be an explicit marketplace/cache root: {resolved}")
        # An explicit root is safe; a symlink is unlinked rather than followed.
        if resolved.is_symlink():
            resolved.unlink()
            removed.append(str(resolved))
        elif resolved.is_dir():
            shutil.rmtree(resolved)
            removed.append(str(resolved))
    return removed


def normalized_inventory(inventory: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(inventory)
    result.pop("captured_at", None)
    if isinstance(result.get("config"), Mapping):
        config = dict(result["config"])
        result["config"] = config
    return result


def assert_same_version_reinstall(before: Mapping[str, Any], after: Mapping[str, Any]) -> None:
    left = normalized_inventory(before)
    right = normalized_inventory(after)
    if left != right:
        raise AssertionError("same-version reinstall changed the normalized client inventory")


def assert_no_residue(inventory: Mapping[str, Any], plugin_ids: Iterable[str] = AGENT_IDS) -> None:
    expected = set(plugin_ids)
    found = {str(item.get("id")) for item in inventory.get("plugins", []) if isinstance(item, Mapping)}
    residual = sorted(found & expected)
    if residual:
        raise AssertionError(f"1102tools plugin residue remains: {', '.join(residual)}")
    roots = inventory.get("scoped_roots_present", {})
    if roots.get("cache") or roots.get("marketplace"):
        raise AssertionError("1102tools cache or marketplace root remains after scoped uninstall")


def prepare_upgrade_fixture(
    source_root: Path,
    fixture_root: Path,
    specs: Iterable[AgentSpec],
    *,
    from_tag: str = HISTORICAL_TAGS["rc4"],
    to_tag: str = HISTORICAL_TAGS["rc5"],
    historical: Mapping[str, Any] | None = None,
    marketplace_alias: str = "1102tools-lifecycle",
) -> dict[str, Any]:
    """Export authentic historical rc4/rc5 package bytes into a fixture.

    The release tags intentionally contain heterogeneous agent versions.  We
    export each tag with ``git archive`` instead of copying current packages
    and rewriting manifests; this makes an upgrade test exercise the actual
    historical bytes and metadata.
    """

    source_root = source_root.resolve()
    fixture_root = fixture_root.expanduser().resolve()
    if fixture_root == source_root or source_root in fixture_root.parents:
        raise LifecycleSafetyError("upgrade fixture must not be inside the source repository")
    if fixture_root.exists():
        if any(fixture_root.iterdir()):
            raise LifecycleSafetyError(f"fixture root must be empty: {fixture_root}")
    else:
        fixture_root.mkdir(parents=True, mode=0o700)
    spec_list = tuple(specs)
    fixture_definition = historical or {
        "from": {"marketplace_tag": from_tag, "versions": HISTORICAL_VERSIONS["rc4"]},
        "to": {"marketplace_tag": to_tag, "versions": HISTORICAL_VERSIONS["rc5"]},
    }
    stages = (
        ("rc4", str(fixture_definition["from"]["marketplace_tag"])),
        ("rc5", str(fixture_definition["to"]["marketplace_tag"])),
    )
    historical_hashes: dict[str, Any] = {}
    for stage, tag in stages:
        commit = _git_text(source_root, "rev-parse", f"{tag}^{{commit}}")
        definition_key = "from" if stage == "rc4" else "to"
        definition = fixture_definition.get(definition_key)
        expected_versions = definition.get("versions") if isinstance(definition, Mapping) else None
        if not isinstance(expected_versions, Mapping):
            raise LifecycleSafetyError(f"no expected heterogeneous versions for fixture stage {stage!r}")
        archive = _git_archive(source_root, tag, spec_list)
        stage_root = fixture_root / stage
        stage_root.mkdir(parents=True, mode=0o700)
        _extract_archive_safely(archive, stage_root)
        marketplace_manifests = _alias_marketplace_manifests(
            stage_root, marketplace_alias
        )
        packages: dict[str, Any] = {}
        for spec in spec_list:
            package_root = stage_root / "plugins" / spec.plugin_id
            if not package_root.is_dir():
                raise LifecycleSafetyError(f"historical tag {tag} lacks package {spec.plugin_id}")
            manifest = package_root / "plugin.json"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            actual_version = data.get("version")
            expected_version = expected_versions.get(spec.plugin_id)
            if actual_version != expected_version:
                raise LifecycleSafetyError(
                    f"historical tag {tag} has {spec.plugin_id} version {actual_version!r}; expected {expected_version!r}"
                )
            packages[spec.plugin_id] = {
                "version": actual_version,
                "tree_sha256": _tree_sha256(package_root),
                "files": _tree_file_hashes(package_root),
            }
        historical_hashes[stage] = {
            "tag": tag,
            "commit": commit,
            "packages": packages,
            "marketplace_alias": marketplace_alias,
            "marketplace_manifests": marketplace_manifests,
        }
    metadata = {
        "fixture_root": str(fixture_root),
        "source_root": str(source_root),
        "from": historical_hashes["rc4"],
        "to": historical_hashes["rc5"],
        "agents": [spec.plugin_id for spec in spec_list],
        "source_modified": False,
    }
    (fixture_root / "fixture.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata


def _git_text(source_root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(source_root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise LifecycleSafetyError(f"git lookup failed for historical fixture: {' '.join(args)}") from exc
    return completed.stdout.strip()


def _git_archive(source_root: Path, tag: str, specs: Sequence[AgentSpec]) -> bytes:
    paths = [f"plugins/{spec.plugin_id}" for spec in specs]
    paths.extend(MARKETPLACE_MANIFESTS)
    try:
        completed = subprocess.run(
            ["git", "-C", str(source_root), "archive", "--format=tar", tag, "--", *paths],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise LifecycleSafetyError(f"git archive failed for historical tag {tag!r}") from exc
    return completed.stdout


def _alias_marketplace_manifests(stage_root: Path, alias: str) -> list[dict[str, Any]]:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", alias):
        raise LifecycleSafetyError(f"invalid disposable marketplace alias: {alias!r}")
    records: list[dict[str, Any]] = []
    for relative in MARKETPLACE_MANIFESTS:
        path = stage_root / relative
        if not path.is_file():
            raise LifecycleSafetyError(f"historical fixture lacks marketplace manifest {relative}")
        original_sha256 = _sha256(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("name") != "1102tools":
            raise LifecycleSafetyError(f"unexpected marketplace name in {relative}")
        data["name"] = alias
        if relative == ".agents/plugins/marketplace.json":
            interface = data.setdefault("interface", {})
            interface["displayName"] = alias
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        records.append(
            {
                "path": relative,
                "source_sha256": original_sha256,
                "fixture_sha256": _sha256(path),
                "name": alias,
            }
        )
    return records


def _extract_archive_safely(archive: bytes, destination: Path) -> None:
    import io

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
        resolved_destination = destination.resolve()
        for member in stream.getmembers():
            target = (destination / member.name).resolve()
            if target != resolved_destination and resolved_destination not in target.parents:
                raise LifecycleSafetyError(f"historical archive escapes fixture root: {member.name!r}")
            if member.issym() or member.islnk():
                raise LifecycleSafetyError(f"historical archive contains unsupported link: {member.name!r}")
        stream.extractall(destination)


def _tree_file_hashes(root: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(path for path in root.rglob("*") if path.is_file() and not path.is_symlink()):
        files.append({
            "path": str(path.relative_to(root)),
            "size": path.stat().st_size,
            "sha256": _sha256(path),
        })
    return files


def _tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for item in _tree_file_hashes(root):
        digest.update(item["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(item["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def ledger_for_plan(
    profile: ClientProfile,
    matrix: Mapping[str, Any],
    lane: str,
    *,
    execute: bool = False,
    runner: CommandRunner | None = None,
) -> dict[str, Any]:
    plan = build_plan(profile, matrix, lane)
    before = capture_inventory(profile)
    command_results: list[CommandResult] = []
    if execute:
        command_results = execute_plan(plan, runner)
    after = capture_inventory(profile)
    return {
        "schema_version": "1.0",
        "mode": "execute" if execute else "dry-run",
        "lane": lane,
        "client": profile.client,
        "backup_metadata": before["config"],
        "before_inventory": before,
        "plan": plan.as_dict(),
        "command_results": [result.as_dict() for result in command_results],
        "after_inventory": after,
        "credential_presence": credential_presence(),
        "verdict": "pass" if not execute or all(result.returncode == 0 for result in command_results) else "fail",
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("codex", "claude"), required=True)
    parser.add_argument(
        "--lane",
        choices=("install", "upgrade", "reinstall", "uninstall", "restore", *EVIDENCE_LANES),
        default="install",
    )
    parser.add_argument("--home", type=Path, default=Path.home(), help="explicit user-home root; execute requires a temporary root")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fixture-root", type=Path)
    parser.add_argument("--execute", action="store_true", help="opt into running client commands")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        matrix = load_matrix(args.matrix)
        profile = ClientProfile(args.client, args.home)
        ledger = ledger_for_plan(profile, matrix, args.lane, execute=args.execute)
        if args.fixture_root:
            metadata = prepare_upgrade_fixture(
                REPO_ROOT,
                args.fixture_root,
                agent_specs(matrix),
                historical=matrix.get("upgrade_fixture"),
            )
            ledger["upgrade_fixture"] = metadata
        rendered = json.dumps(ledger, indent=2) + "\n"
        if args.output:
            args.output.expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
            args.output.expanduser().resolve().write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0 if ledger["verdict"] == "pass" else 1
    except (LifecycleSafetyError, AssertionError, OSError, json.JSONDecodeError) as exc:
        print(f"lifecycle runner: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
