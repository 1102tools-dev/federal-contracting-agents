# RC5 lifecycle test infrastructure

Everything in this directory is test-only and lives outside the shipped
plugin directories.

## Installation and upgrade harness

`lifecycle_runner.py` drives the declarative Codex and Claude install,
upgrade, reinstall, uninstall, coexistence, and restoration matrix. Its
default mode is a sanitized dry-run:

```sh
python3 tests/lifecycle/lifecycle_runner.py \
  --client codex --lane upgrade --home /tmp/1102tools-fake-home
```

The runner emits command plans, scoped inventory metadata, and
credential-presence booleans; it never records command output or
configuration contents. `--execute` is intentionally restricted to an
explicit temporary home. It redirects client configuration into that home,
rejects the real user home, and only permits removal of resolved 1102tools
cache and marketplace roots. Real-profile lifecycle tests must be performed
as separately reviewed, serialized release-captain commands.

The historical transition fixture exports authentic package bytes from the
`v1.2.0-rc.4` and `v1.2.0-rc.5` Git tags. The fixture root must be empty,
outside the repository, and disposable:

```sh
python3 tests/lifecycle/lifecycle_runner.py \
  --client claude --lane upgrade --home /tmp/1102tools-fake-home \
  --fixture-root /tmp/1102tools-rc5-fixture
```

The fixture contains only disposable `rc4/`, `rc5/`, and metadata files.
`fixture.json` records each tag, resolved commit, per-file hashes, and package
tree hashes so the transition can be audited without rewriting manifests.

## Credential, pacing, and upstream canaries

`runtime_canaries.py` is an offline-first harness for the credential,
pacing/concurrency, and upstream-drift lanes:

```sh
python3 tests/lifecycle/runtime_canaries.py --output /tmp/rc5-runtime-ledger.json
python3 -m unittest discover -s tests/lifecycle -p 'test_*.py'
```

The default makes no network calls, starts no MCP, reads credentials only as
presence booleans, and marks all nine MCP entries as requiring a live gate.

Live operation requires `--live --runner`. The release-captain-selected
runner must use MCP protocol calls and return a JSON object containing
`version`, `tools`, `response`, and optional `warnings` and `source_hashes`.
Runner stdout and stderr are captured, never echoed, and only sanitized
fields enter the ledger. Exact-value redaction assertions prevent credential
values from surviving in evidence.

The nine federal MCP canaries are SAM.gov, USAspending, GSA CALC+, BLS OEWS,
GSA Per Diem, eCFR, Federal Register, Regulations.gov, and Acquisition.gov.
Tavily is a separate keyless web connector and is not counted in this lane.

The pacing canary uses a captured local 429 with `Retry-After: 5` and a
virtual shared-key scheduler. It sleeps zero seconds, makes no provider call,
and checks serialization from request completion using the larger of the
configured interval and `Retry-After`.
