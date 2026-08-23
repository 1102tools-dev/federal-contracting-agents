from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.9/3.10 lifecycle hosts
    tomllib = None

try:
    from .codex_host_profile import (
        KNOWN_CREDENTIALS,
        SERVER_CONFIG,
        main,
        render_profile,
        validate_profile,
    )
except ImportError:  # pragma: no cover
    from codex_host_profile import (
        KNOWN_CREDENTIALS,
        SERVER_CONFIG,
        main,
        render_profile,
        validate_profile,
    )


class CodexHostProfileTests(unittest.TestCase):
    def test_tracked_profile_matches_renderer(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        tracked = repo_root / "config" / "codex" / "1102tools-host.config.toml"
        self.assertTrue(tracked.is_file())
        self.assertEqual(tracked.read_text(encoding="utf-8"), render_profile())

    def test_profile_is_complete_parseable_and_contains_no_values(self) -> None:
        text = render_profile()
        self.assertEqual(validate_profile(text), [])
        if tomllib is not None:
            parsed = tomllib.loads(text)
            self.assertEqual(
                set(parsed["mcp_servers"]),
                {item[0] for item in SERVER_CONFIG},
            )
        for name in KNOWN_CREDENTIALS:
            self.assertNotIn(f'{name} = "', text)

    def test_write_then_check_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "1102tools-host.config.toml"
            self.assertEqual(main(("--output", str(path))), 0)
            self.assertEqual(main(("--output", str(path), "--check")), 0)

    def test_partial_host_override_is_rejected(self) -> None:
        text = render_profile().replace(
            'args = ["--from", "sam-gov-mcp==1.0.9", "sam-gov-mcp"]\n',
            "",
            1,
        )
        self.assertTrue(any("sam-gov" in item for item in validate_profile(text)))


if __name__ == "__main__":
    unittest.main()
