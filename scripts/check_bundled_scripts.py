#!/usr/bin/env python3
"""Compile each vendored validator and verify its command-line help."""

from __future__ import annotations

import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    scripts = sorted((REPO_ROOT / "plugins").glob("*/skills/*/scripts/*.py"))
    if len(scripts) != 13:
        raise SystemExit(f"Expected 13 bundled Python scripts, found {len(scripts)}")
    with tempfile.TemporaryDirectory() as compile_dir:
        for index, script in enumerate(scripts):
            cfile = Path(compile_dir) / f"{index}-{script.stem}.pyc"
            py_compile.compile(str(script), cfile=str(cfile), doraise=True)
            result = subprocess.run(
                [sys.executable, str(script), "--help"],
                text=True,
                capture_output=True,
                timeout=30,
            )
            if result.returncode:
                print(result.stdout, file=sys.stderr)
                print(result.stderr, file=sys.stderr)
                raise SystemExit(f"--help failed: {script}")
            print(f"PASS {script.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
