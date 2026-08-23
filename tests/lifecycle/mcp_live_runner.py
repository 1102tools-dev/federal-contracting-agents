#!/usr/bin/env python3
"""Run one minimal live canary through an installed, pinned MCP server.

The descriptor arrives as one JSON object on stdin. This runner starts the
published MCP distribution over stdio, initializes it, lists its tools, calls
one bounded read-only operation, and returns one JSON object for the sanitized
RC5 canary harness. It never prints environment variables or credential
values.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Mapping

CANARIES: dict[str, dict[str, Any]] = {
    "acquisition-gov": {
        "distribution": "acquisition-gov-mcp",
        "executable": "acquisition-gov-mcp",
        "tool": "list_rfo_parts",
        "arguments": {},
        "interval": "3",
    },
    "bls-oews": {
        "distribution": "bls-oews-mcp",
        "executable": "bls-oews-mcp",
        "tool": "get_wage_data",
        "arguments": {
            "occ_code": "151252",
            "scope": "national",
            "year": 2025,
            "datatypes": ["04"],
        },
        "interval": "3",
    },
    "ecfr": {
        "distribution": "ecfr-mcp",
        "executable": "ecfr-mcp",
        "tool": "get_cfr_content",
        "arguments": {"title_number": 48, "section": "10.001"},
        "interval": "3",
    },
    "federal-register": {
        "distribution": "federal-register-mcp",
        "executable": "federal-register-mcp",
        "tool": "search_documents",
        "arguments": {
            "term": "Federal Acquisition Regulation",
            "cfr_title": 48,
            "cfr_part": "10",
            "per_page": 1,
        },
        "interval": "3",
    },
    "gsa-calc": {
        "distribution": "gsa-calc-mcp",
        "executable": "gsa-calc-mcp",
        "tool": "keyword_search",
        "arguments": {"keyword": "Software Engineer", "page_size": 1},
        "interval": "3",
    },
    "gsa-perdiem": {
        "distribution": "gsa-perdiem-mcp",
        "executable": "gsa-perdiem-mcp",
        "tool": "lookup_city_perdiem",
        "arguments": {"city": "Washington", "state": "DC", "fiscal_year": 2026},
        "interval": "4",
    },
    "regulations-gov": {
        "distribution": "regulationsgov-mcp",
        "executable": "regulationsgov-mcp",
        "tool": "search_dockets",
        "arguments": {
            "search_term": "Federal Acquisition Regulation",
            "page_size": 5,
        },
        "interval": "4",
    },
    "sam-gov": {
        "distribution": "sam-gov-mcp",
        "executable": "sam-gov-mcp",
        "tool": "search_opportunities",
        "arguments": {
            "posted_from": "08/01/2026",
            "posted_to": "08/22/2026",
            "limit": 1,
        },
        "interval": "3",
    },
    "usaspending": {
        "distribution": "usaspending-gov-mcp",
        "executable": "usaspending-mcp",
        "tool": "search_awards",
        "arguments": {
            "award_type": "contracts",
            "time_period_start": "2026-08-01",
            "time_period_end": "2026-08-22",
            "limit": 1,
            "page": 1,
        },
        "interval": "3",
        "env": {"USASPENDING_TOOL_PROFILE": "acquisition-agent"},
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _parse_embedded_json(value: Any) -> Any:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith(("{", "[")):
            try:
                return _parse_embedded_json(json.loads(stripped))
            except json.JSONDecodeError:
                return value
        return value
    if isinstance(value, Mapping):
        return {str(key): _parse_embedded_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_parse_embedded_json(item) for item in value]
    return value


def _collect_metadata(value: Any) -> tuple[list[str], dict[str, str]]:
    warnings: list[str] = []
    hashes: dict[str, str] = {}

    def visit(item: Any, path: str = "response") -> None:
        if isinstance(item, Mapping):
            for key, child in item.items():
                child_path = f"{path}.{key}"
                lowered = str(key).lower()
                if lowered == "warnings" and isinstance(child, list):
                    warnings.extend(str(entry) for entry in child)
                if ("sha256" in lowered or "source_hash" in lowered) and isinstance(child, str):
                    hashes[child_path] = child
                visit(child, child_path)
        elif isinstance(item, list):
            for index, child in enumerate(item[:25]):
                visit(child, f"{path}[{index}]")

    visit(value)
    return sorted(set(warnings)), hashes


async def run(descriptor: Mapping[str, Any]) -> dict[str, Any]:
    # Keep the module importable by the repository's dependency-free unit
    # tests. The live runner itself is launched with ``mcp`` explicitly.
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    server = str(descriptor["server"])
    definition = CANARIES.get(server)
    if definition is None:
        raise ValueError("unknown canary server")
    pinned_version = str(descriptor["pinned_version"])
    if descriptor.get("distribution") != definition["distribution"]:
        raise ValueError("descriptor distribution does not match canary definition")
    env = os.environ.copy()
    env["FEDERAL_API_MIN_INTERVAL_SECONDS"] = str(definition["interval"])
    env.update({str(k): str(v) for k, v in definition.get("env", {}).items()})
    parameters = StdioServerParameters(
        command="uvx",
        args=[
            "--from",
            f"{definition['distribution']}=={pinned_version}",
            str(definition["executable"]),
        ],
        env=env,
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialized = await asyncio.wait_for(session.initialize(), timeout=90)
            listed = await asyncio.wait_for(session.list_tools(), timeout=60)
            tool_names = {tool.name for tool in listed.tools}
            if definition["tool"] not in tool_names:
                raise RuntimeError("required canary tool is missing")
            started_at = utc_now()
            called = await asyncio.wait_for(
                session.call_tool(str(definition["tool"]), dict(definition["arguments"])),
                timeout=120,
            )
            completed_at = utc_now()
    initialized_dump = _jsonable(initialized)
    server_info = initialized_dump.get("serverInfo", initialized_dump.get("server_info", {}))
    called_dump = _parse_embedded_json(_jsonable(called))
    response = called_dump.get("structuredContent") or called_dump.get("structured_content") or called_dump
    warnings, source_hashes = _collect_metadata(response)
    tools = [
        {"name": tool.name, "inputSchema": _jsonable(tool.inputSchema if hasattr(tool, "inputSchema") else tool.input_schema)}
        for tool in listed.tools
    ]
    return {
        "version": server_info.get("version", pinned_version),
        "tools": tools,
        "response": response,
        "warnings": warnings,
        "source_hashes": source_hashes,
        "source_call_started_at": started_at,
        "source_call_completed_at": completed_at,
        "called_tool": definition["tool"],
        "call_is_error": bool(called_dump.get("isError", called_dump.get("is_error", False))),
    }


def main() -> int:
    try:
        descriptor = json.loads(sys.stdin.read())
        if not isinstance(descriptor, Mapping) or descriptor.get("operation") != "mcp_canary":
            raise ValueError("invalid canary descriptor")
        payload = asyncio.run(run(descriptor))
        sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
        return 0
    except Exception as exc:
        sys.stderr.write(f"mcp canary failed: {type(exc).__name__}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
