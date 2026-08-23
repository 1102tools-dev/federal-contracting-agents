# RC5 runtime canaries

`runtime_canaries.py` is a dependency-free, offline-first harness for the RC5
credential, pacing/concurrency, and upstream-drift lanes. It is test
infrastructure only and is outside every shipped plugin directory.

Run the safe default and its unit tests from the repository root:

```sh
python3 tests/lifecycle/runtime_canaries.py --output /tmp/rc5-runtime-ledger.json
python3 -m unittest discover -s tests/lifecycle -p 'test_*.py'
```

The default mode makes no network calls, starts no MCP, reads credential
values only as presence booleans, and marks all nine MCP entries as
`dry-run`/`live_gate_required`.

## Live runner contract

Live operation is deliberately gated behind `--live --runner`. The runner is
an external MCP-aware client/connector chosen by the release captain; this
harness does not call a provider API or bypass the configured MCP. It invokes
the runner once per matrix entry with a JSON descriptor on stdin:

```json
{
  "operation": "mcp_canary",
  "server": "sam-gov",
  "distribution": "sam-gov-mcp",
  "pinned_version": "1.0.8",
  "requested_operation": "list_opportunities_minimal"
}
```

The runner must return one JSON object on stdout containing `version`, a
`tools` list (each tool has `name` and `inputSchema` or `schema`), `response`,
and optional `warnings` and `source_hashes`. Runner stdout/stderr is captured,
never echoed, and only sanitized fields are recorded. Raw output is always
marked `raw_output_recorded: false`. Credential values are never written to
the ledger; exact-value redaction assertions cover runner output and the
result ledger.

The nine matrix entries are the federal MCP distributions in the current
plugin manifests: SAM.gov, USASpending, GSA CALC+, BLS OEWS, GSA Per Diem,
eCFR, Federal Register, Regulations.gov, and Acquisition.gov. Tavily is a
separate keyless web connector and is not counted in this federal MCP lane.

The pacing canary uses a captured local 429 with `Retry-After: 5` and a virtual
shared-key scheduler. It sleeps zero seconds, makes no provider call, and
checks that calls are serialized from request completion with the larger of
the configured interval and `Retry-After`.
