#!/usr/bin/env python3
"""Synchronize canonical 1102tools skills into self-contained agent packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = REPO_ROOT / "components.lock.json"
PLUGIN_SKILLS = {
    "pre-award-agent": [
        "sow-pws-builder",
        "igce-builder-ffp",
        "igce-builder-lh-tm",
        "igce-builder-cr",
    ],
    "other-transaction-agent": [
        "ot-project-description-builder",
        "ot-cost-analysis",
    ],
    "govcon-growth-agent": ["govcon-growth-workflow"],
    "market-research-agent": ["market-research-builder"],
    "acquisition-policy-agent": ["acquisition-policy-workflow"],
}
RUNTIME_DIRS = ("agents", "references", "scripts", "assets")
MCP_PACKAGES = {
    "acquisition-gov": {"distribution": "acquisition-gov-mcp", "version": "1.0.0"},
    "bls-oews": {"distribution": "bls-oews-mcp", "version": "1.0.4"},
    "ecfr": {"distribution": "ecfr-mcp", "version": "1.0.4"},
    "federal-register": {"distribution": "federal-register-mcp", "version": "1.0.3"},
    "gsa-calc": {"distribution": "gsa-calc-mcp", "version": "1.0.3"},
    "gsa-perdiem": {"distribution": "gsa-perdiem-mcp", "version": "1.0.4"},
    "sam-gov": {"distribution": "sam-gov-mcp", "version": "1.0.6"},
    "regulations-gov": {"distribution": "regulationsgov-mcp", "version": "1.0.3"},
    "usaspending": {"distribution": "usaspending-gov-mcp", "version": "1.0.3"},
}
EXTERNAL_MCPS = {
    "tavily-web": {
        "provider": "Tavily",
        "repository": "https://github.com/tavily-ai/tavily-mcp",
        "endpoint": "https://mcp.tavily.com/mcp/",
        "access_mode": "keyless",
        "expected_tools": ["tavily_extract", "tavily_search"],
        "observed_tools": [
            "tavily_crawl",
            "tavily_extract",
            "tavily_map",
            "tavily_research",
            "tavily_search",
        ],
        "prohibited_tools": ["tavily_crawl", "tavily_map", "tavily_research"],
        "observed_tool_schema_sha256": "f28255db8e816ce522e9bd20a89b6fcf2312af41e60c3846799e9c3195e60992",
        "verified_at": "2026-08-21",
    }
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy or verify canonical skill runtime files and their lock."
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=REPO_ROOT.parent / "federal-contracting-skills",
        help="Canonical federal-contracting-skills checkout.",
    )
    parser.add_argument(
        "--mcp-root",
        type=Path,
        default=REPO_ROOT.parent / "federal-contracting-mcps",
        help="Canonical federal-contracting-mcps checkout.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify vendored copies and the lock without writing.",
    )
    return parser.parse_args()


def git_commit(path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Unable to resolve source commit for {path}: {exc}") from exc


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def runtime_files(skill_root: Path) -> list[Path]:
    files: list[Path] = []
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Missing canonical skill manifest: {skill_md}")
    files.append(skill_md)
    for dirname in RUNTIME_DIRS:
        directory = skill_root / dirname
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_symlink():
                raise SystemExit(f"Runtime symlinks are prohibited: {path}")
            if (
                path.is_file()
                and path.name != ".DS_Store"
                and path.suffix != ".pyc"
                and "__pycache__" not in path.parts
            ):
                files.append(path)
    return sorted(files, key=lambda path: path.relative_to(skill_root).as_posix())


def relative_hashes(skill_root: Path) -> dict[str, str]:
    return {
        path.relative_to(skill_root).as_posix(): sha256(path)
        for path in runtime_files(skill_root)
    }


def copy_skill(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for path in runtime_files(source):
        relative = path.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def build_lock(skills_root: Path, mcp_root: Path) -> dict[str, object]:
    plugins: dict[str, object] = {}
    for plugin_name, skill_names in PLUGIN_SKILLS.items():
        manifest = json.loads(
            (REPO_ROOT / "plugins" / plugin_name / "plugin.json").read_text()
        )
        skills: dict[str, object] = {}
        for skill_name in skill_names:
            canonical = skills_root / "skills" / skill_name
            vendored = REPO_ROOT / "plugins" / plugin_name / "skills" / skill_name
            canonical_hashes = relative_hashes(canonical)
            vendored_hashes = relative_hashes(vendored)
            if vendored_hashes != canonical_hashes:
                raise SystemExit(
                    f"Vendored runtime differs from canonical source: {plugin_name}/{skill_name}"
                )
            skills[skill_name] = {"files": canonical_hashes}
        plugins[plugin_name] = {
            "version": manifest["version"],
            "skills": skills,
        }

    return {
        "format_version": 2,
        "agent_plugins_spec": "1.0.0",
        "sources": {
            "skills": {
                "repository": "https://github.com/1102tools-dev/federal-contracting-skills",
                "commit": git_commit(skills_root),
            },
            "mcps": {
                "repository": "https://github.com/1102tools-dev/federal-contracting-mcps",
                "commit": git_commit(mcp_root),
                "packages": MCP_PACKAGES,
            },
        },
        "external_mcps": EXTERNAL_MCPS,
        "plugins": plugins,
    }


def sync(skills_root: Path, mcp_root: Path) -> None:
    for plugin_name, skill_names in PLUGIN_SKILLS.items():
        for skill_name in skill_names:
            copy_skill(
                skills_root / "skills" / skill_name,
                REPO_ROOT / "plugins" / plugin_name / "skills" / skill_name,
            )
        shutil.copy2(REPO_ROOT / "LICENSE", REPO_ROOT / "plugins" / plugin_name / "LICENSE")
    lock = build_lock(skills_root, mcp_root)
    LOCK_PATH.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(f"Synchronized canonical skills and wrote {LOCK_PATH}")


def check(skills_root: Path, mcp_root: Path) -> None:
    if not LOCK_PATH.is_file():
        raise SystemExit(f"Missing component lock: {LOCK_PATH}")
    expected = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    actual = build_lock(skills_root, mcp_root)
    if actual != expected:
        print("Component lock drift detected.", file=sys.stderr)
        print(json.dumps(actual, indent=2), file=sys.stderr)
        raise SystemExit(1)
    print("Component lock and all vendored runtime files are current.")


def main() -> None:
    args = parse_args()
    skills_root = args.skills_root.expanduser().resolve()
    mcp_root = args.mcp_root.expanduser().resolve()
    if args.check:
        check(skills_root, mcp_root)
    else:
        sync(skills_root, mcp_root)


if __name__ == "__main__":
    main()
