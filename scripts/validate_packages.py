#!/usr/bin/env python3
"""Validate the four self-contained 1102tools Agent Plugins packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import jsonschema
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAMES = (
    "pre-award-agent",
    "other-transaction-agent",
    "govcon-growth-agent",
    "market-research-agent",
)
EXPECTED_VERSIONS = {
    "pre-award-agent": "1.0.0-rc.3",
    "other-transaction-agent": "1.0.0-rc.3",
    "govcon-growth-agent": "1.0.0-rc.1",
    "market-research-agent": "1.0.0-rc.1",
}
MARKETPLACE_VERSION = "1.1.0-rc.1"
EXPECTED_SKILLS = {
    "pre-award-agent": {
        "pre-award-workflow",
        "sow-pws-builder",
        "igce-builder-ffp",
        "igce-builder-lh-tm",
        "igce-builder-cr",
    },
    "other-transaction-agent": {
        "other-transaction-workflow",
        "ot-project-description-builder",
        "ot-cost-analysis",
    },
    "govcon-growth-agent": {"govcon-growth-workflow"},
    "market-research-agent": {"market-research-builder"},
}
EXPECTED_MCPS = {
    "pre-award-agent": {"bls-oews", "gsa-calc", "gsa-perdiem"},
    "other-transaction-agent": {"bls-oews", "gsa-calc", "gsa-perdiem"},
    "govcon-growth-agent": {"sam-gov", "usaspending", "gsa-calc"},
    "market-research-agent": {"sam-gov", "usaspending"},
}
EXPECTED_MCP_REQUIREMENTS = {
    "bls-oews": "bls-oews-mcp==1.0.4",
    "gsa-calc": "gsa-calc-mcp==1.0.3",
    "gsa-perdiem": "gsa-perdiem-mcp==1.0.4",
    "sam-gov": "sam-gov-mcp==1.0.6",
    "usaspending": "usaspending-gov-mcp==1.0.3",
}
EXPECTED_PACING = {
    "bls-oews": "3",
    "gsa-calc": "3",
    "gsa-perdiem": "4",
    "sam-gov": "3",
    "usaspending": "3",
}
ALLOWED_SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "Cloudflare token": re.compile(r"\bcfat_[A-Za-z0-9_-]{20,}\b"),
    "SAM.gov key": re.compile(
        r"\bSAM-[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
    ),
}


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Skill does not start with frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"Skill frontmatter is not closed: {path}")
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        raise ValueError(f"Skill frontmatter is not an object: {path}")
    return value


def validate_links(skill_root: Path, errors: list[str]) -> None:
    root = skill_root.resolve()
    for markdown in skill_root.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            resolved = (markdown.parent / unquote(target)).resolve()
            if not is_within(resolved, root):
                errors.append(f"Escaping skill reference: {markdown}: {raw_target}")
            elif not resolved.exists():
                errors.append(f"Missing skill reference: {markdown}: {raw_target}")


def comparable_native(server: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in server.items() if key != "type"}


def validate_mcp_manifests(plugin_root: Path, errors: list[str]) -> None:
    portable = load_json(plugin_root / "mcp.json")
    native = load_json(plugin_root / ".mcp.json")
    portable_servers = portable.get("mcpServers")
    native_servers = native.get("mcpServers")
    expected_mcps = EXPECTED_MCPS[plugin_root.name]
    if not isinstance(portable_servers, dict) or set(portable_servers) != expected_mcps:
        errors.append(f"{plugin_root.name}: portable MCP surface must be exactly {sorted(expected_mcps)}")
        return
    if not isinstance(native_servers, dict) or set(native_servers) != expected_mcps:
        errors.append(f"{plugin_root.name}: native MCP surface must be exactly {sorted(expected_mcps)}")
        return
    for name in sorted(expected_mcps):
        portable_server = portable_servers[name]
        native_server = native_servers[name]
        if not isinstance(portable_server, dict) or not isinstance(native_server, dict):
            errors.append(f"{plugin_root.name}: MCP server {name} must be an object")
            continue
        if portable_server.get("type") != "stdio":
            errors.append(f"{plugin_root.name}: MCP server {name} must use explicit stdio")
        if comparable_native(portable_server) != native_server:
            errors.append(f"{plugin_root.name}: portable/native MCP drift for {name}")
        args = portable_server.get("args", [])
        if not isinstance(args, list) or "--from" not in args:
            errors.append(f"{plugin_root.name}: MCP server {name} must use uvx --from")
        else:
            requirement = args[args.index("--from") + 1]
            if not isinstance(requirement, str) or "==" not in requirement:
                errors.append(f"{plugin_root.name}: MCP server {name} is not exactly pinned")
            elif requirement != EXPECTED_MCP_REQUIREMENTS[name]:
                errors.append(
                    f"{plugin_root.name}: MCP server {name} must pin "
                    f"{EXPECTED_MCP_REQUIREMENTS[name]}"
                )
        env = portable_server.get("env", {})
        if isinstance(env, dict) and any(key.endswith("API_KEY") for key in env):
            errors.append(f"{plugin_root.name}: credentials must not be embedded in MCP env")
        if not isinstance(env, dict) or env.get("FEDERAL_API_MIN_INTERVAL_SECONDS") != EXPECTED_PACING[name]:
            errors.append(
                f"{plugin_root.name}: {name} must set the explicit "
                f"{EXPECTED_PACING[name]}-second pacing safeguard"
            )


def validate_skill(skill_root: Path, errors: list[str]) -> None:
    try:
        frontmatter = parse_frontmatter(skill_root / "SKILL.md")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(str(exc))
        return
    unknown = set(frontmatter) - ALLOWED_SKILL_FIELDS
    if unknown:
        errors.append(f"{skill_root}: nonportable frontmatter fields: {sorted(unknown)}")
    if frontmatter.get("name") != skill_root.name:
        errors.append(f"{skill_root}: frontmatter name must match directory")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append(f"{skill_root}: description must contain 1-1024 characters")
    compatibility = frontmatter.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > 500:
        errors.append(f"{skill_root}: compatibility exceeds 500 characters")
    for forbidden in ("test.md", "testing.md"):
        if (skill_root / forbidden).exists():
            errors.append(f"{skill_root}: development-only {forbidden} was vendored")
    agent_yaml = skill_root / "agents" / "openai.yaml"
    if agent_yaml.is_file():
        payload = yaml.safe_load(agent_yaml.read_text(encoding="utf-8"))
        prompt = payload.get("interface", {}).get("default_prompt", "") if isinstance(payload, dict) else ""
        if f"${skill_root.name}" not in prompt:
            errors.append(f"{skill_root}: OpenAI default prompt must invoke ${skill_root.name}")
    validate_links(skill_root, errors)


def validate_plugin(plugin_name: str, schemas: dict[str, dict[str, object]], errors: list[str]) -> None:
    plugin_root = REPO_ROOT / "plugins" / plugin_name
    portable = load_json(plugin_root / "plugin.json")
    mcp = load_json(plugin_root / "mcp.json")
    try:
        jsonschema.Draft202012Validator(schemas["plugin"]).validate(portable)
        jsonschema.Draft202012Validator(schemas["mcp"]).validate(mcp)
    except jsonschema.ValidationError as exc:
        errors.append(f"{plugin_name}: Agent Plugins schema error: {exc.message}")
    expected_version = EXPECTED_VERSIONS[plugin_name]
    if portable.get("name") != plugin_name or portable.get("version") != expected_version:
        errors.append(f"{plugin_name}: portable identity/version mismatch")
    codex_manifest = load_json(plugin_root / ".codex-plugin" / "plugin.json")
    claude_manifest = load_json(plugin_root / ".claude-plugin" / "plugin.json")
    if codex_manifest.get("name") != plugin_name or codex_manifest.get("version") != expected_version:
        errors.append(f"{plugin_name}: Codex identity/version mismatch")
    if claude_manifest.get("name") != plugin_name or claude_manifest.get("version") != expected_version:
        errors.append(f"{plugin_name}: Claude identity/version mismatch")
    default_prompt = codex_manifest.get("interface", {}).get("defaultPrompt", "")
    if not isinstance(default_prompt, str) or len(default_prompt) > 128:
        errors.append(f"{plugin_name}: Codex defaultPrompt must contain at most 128 characters")
    skills_root = plugin_root / "skills"
    actual_skills = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if actual_skills != EXPECTED_SKILLS[plugin_name]:
        errors.append(
            f"{plugin_name}: expected skills {sorted(EXPECTED_SKILLS[plugin_name])}, got {sorted(actual_skills)}"
        )
    for skill_name in sorted(actual_skills):
        validate_skill(skills_root / skill_name, errors)
    validate_mcp_manifests(plugin_root, errors)
    for required in (
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        "LICENSE",
    ):
        if not (plugin_root / required).is_file():
            errors.append(f"{plugin_name}: missing {required}")
    copilot_agent = plugin_root / "com.github.copilot" / "agents" / f"{plugin_name}.agent.md"
    claude_agent = plugin_root / "agents" / f"{plugin_name}.md"
    if not copilot_agent.is_file():
        errors.append(f"{plugin_name}: missing Copilot custom agent")
    if not claude_agent.is_file():
        errors.append(f"{plugin_name}: missing Claude Code native agent")


def validate_release_versions(errors: list[str]) -> None:
    lock = load_json(REPO_ROOT / "components.lock.json")
    locked_plugins = lock.get("plugins", {})
    if not isinstance(locked_plugins, dict):
        errors.append("components.lock.json: plugins must be an object")
    else:
        for plugin_name in PLUGIN_NAMES:
            record = locked_plugins.get(plugin_name, {})
            if not isinstance(record, dict) or record.get("version") != EXPECTED_VERSIONS[plugin_name]:
                errors.append(f"components.lock.json: stale version for {plugin_name}")

    for relative in (".claude-plugin/marketplace.json", ".github/plugin/marketplace.json"):
        marketplace = load_json(REPO_ROOT / relative)
        metadata = marketplace.get("metadata", {})
        if not isinstance(metadata, dict) or metadata.get("version") != MARKETPLACE_VERSION:
            errors.append(f"{relative}: marketplace metadata version mismatch")
        entries = marketplace.get("plugins", [])
        if not isinstance(entries, list):
            errors.append(f"{relative}: plugins must be a list")
            continue
        versions = {
            entry.get("name"): entry.get("version")
            for entry in entries
            if isinstance(entry, dict)
        }
        for plugin_name in PLUGIN_NAMES:
            if versions.get(plugin_name) != EXPECTED_VERSIONS[plugin_name]:
                errors.append(f"{relative}: stale version for {plugin_name}")

    codex_marketplace = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    entries = codex_marketplace.get("plugins", [])
    names = {entry.get("name") for entry in entries if isinstance(entry, dict)}
    if names != set(PLUGIN_NAMES):
        errors.append(".agents/plugins/marketplace.json: plugin catalog mismatch")

    pre_mcp = load_json(REPO_ROOT / "plugins" / "pre-award-agent" / "mcp.json")
    ot_mcp = load_json(REPO_ROOT / "plugins" / "other-transaction-agent" / "mcp.json")
    if pre_mcp.get("mcpServers") != ot_mcp.get("mcpServers"):
        errors.append("Shared MCP configurations drifted between the two packages")


def validate_repository_hygiene(errors: list[str]) -> None:
    for path in REPO_ROOT.rglob("*"):
        relative = path.relative_to(REPO_ROOT)
        if relative.parts and relative.parts[0] in {".git", "_skills", "_mcps"}:
            continue
        if path.is_symlink():
            errors.append(f"Symlinks are prohibited in package repository: {path}")
        if path.is_file() and path.stat().st_size <= 2_000_000:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"Potential {label} in {path}")
            if path.suffix in {".md", ".json", ".yaml", ".yml"}:
                for forbidden in ("mcp__", "AskUserQuestion", "/mnt/skills", "/mnt/user-data"):
                    if forbidden in text:
                        errors.append(f"Host-specific token {forbidden!r} remains in {path}")


def main() -> None:
    schemas = {
        "plugin": load_json(REPO_ROOT / "schemas" / "agent-plugins" / "1.0.0" / "plugin.schema.json"),
        "mcp": load_json(REPO_ROOT / "schemas" / "agent-plugins" / "1.0.0" / "mcp.schema.json"),
    }
    errors: list[str] = []
    for plugin_name in PLUGIN_NAMES:
        validate_plugin(plugin_name, schemas, errors)
    validate_release_versions(errors)
    validate_repository_hygiene(errors)
    if errors:
        print("Package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("All four Agent Plugins packages passed schema, portability, reference, pin, and hygiene checks.")


if __name__ == "__main__":
    main()
