"""Documented commands must actually work.

Through 1.0.0-rc.3 the README's MCP discovery command omitted `--with httpx`
while the script imported httpx and CI passed the flag. Anyone copying the
documented command got ModuleNotFoundError. Nothing caught it because no test
looked at what the README told people to run.

This is an explicit allowlist, not a sweep of every fenced block. README blocks
can install, mutate, authenticate, or publish, so only commands named here are
treated as documented-and-safe, and only their form is asserted. Execution of
the discovery command itself already happens in CI.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"

# Each entry: a documented command, and the tokens its form must contain.
# Add a command here only after confirming it is read-only and non-publishing.
SAFE_DOCUMENTED_COMMANDS = (
    (
        "smoke_mcp_discovery",
        ("uv run", "--with mcp", "--with httpx", "scripts/smoke_mcp_discovery.py"),
    ),
    ("sync_components", ("python3 scripts/sync_components.py", "--check")),
    ("validate_packages", ("python3 scripts/validate_packages.py",)),
    ("check_bundled_scripts", ("python3 scripts/check_bundled_scripts.py",)),
)


def documented_lines() -> list[str]:
    """Every line inside a fenced block in the README."""
    text = README.read_text(encoding="utf-8")
    lines: list[str] = []
    for block in re.findall(r"```[a-zA-Z]*\n(.*?)```", text, re.S):
        lines.extend(block.splitlines())
    return lines


class DocumentedCommandTests(unittest.TestCase):
    def test_allowlisted_commands_are_documented_in_working_form(self) -> None:
        lines = documented_lines()
        for name, required in SAFE_DOCUMENTED_COMMANDS:
            matches = [line for line in lines if name in line]
            self.assertTrue(matches, f"README documents no {name} command")
            for line in matches:
                for token in required:
                    self.assertIn(
                        token,
                        line,
                        f"README {name} command is missing {token!r}, so copying it fails: {line.strip()!r}",
                    )

    def test_discovery_script_imports_are_covered_by_documented_flags(self) -> None:
        """Every third-party import of the discovery script needs a --with flag.

        This is the general form of the httpx defect: if the script grows a new
        dependency, the documented command must grow the matching flag.
        """
        source = (REPO_ROOT / "scripts" / "smoke_mcp_discovery.py").read_text(encoding="utf-8")
        third_party = set()
        for match in re.findall(r"^(?:import|from)\s+([a-zA-Z_][\w]*)", source, re.M):
            if match in {"argparse", "asyncio", "hashlib", "json", "os", "pathlib", "sys", "__future__"}:
                continue
            third_party.add(match)
        documented = " ".join(line for line in documented_lines() if "smoke_mcp_discovery" in line)
        for module in sorted(third_party):
            self.assertIn(
                f"--with {module}",
                documented,
                f"scripts/smoke_mcp_discovery.py imports {module!r} but no documented command passes --with {module}",
            )


if __name__ == "__main__":
    unittest.main()
