#!/usr/bin/env python3
"""Start pinned MCP servers and list tools without calling an upstream API."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 release hosts
    import tomli as tomllib

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOOLS = {
    "acquisition-gov": {"list_rfo_parts", "get_rfo_part", "list_rfo_agency_deviations", "get_rfo_agency_deviation", "get_rfo_guidance"},
    "bls-oews": {"get_access_status", "detect_latest_year", "get_wage_data", "list_common_soc_codes"},
    "ecfr": {"get_cfr_content", "get_version_history", "compare_versions"},
    "federal-register": {"search_documents", "get_document", "open_comment_periods"},
    "gsa-calc": {"keyword_search"},
    "gsa-perdiem": {"get_access_status", "lookup_city_perdiem", "get_mie_breakdown"},
    "sam-gov": {"get_access_status", "search_opportunities", "search_entities", "search_contract_awards"},
    "regulations-gov": {"get_access_status", "search_documents", "search_comments", "search_dockets"},
    "usaspending": {
        "search_awards",
        "spending_over_time",
        "spending_by_category",
        "get_agency_overview",
        "get_agency_awards",
        "search_recipients",
        "get_recipient_profile",
        "autocomplete_naics",
        "autocomplete_psc",
        "search_subawards",
    },
    "tavily-web": {"tavily_search", "tavily_extract"},
}
TAVILY_ENDPOINT = "https://mcp.tavily.com/mcp/"
TAVILY_HEADERS = {"X-Tavily-Access-Mode": "keyless"}
KEYED_ENV_VARS = {
    "sam-gov": "SAM_API_KEY",
    "bls-oews": "BLS_API_KEY",
    "gsa-perdiem": "PERDIEM_API_KEY",
    "regulations-gov": "REGULATIONS_GOV_API_KEY",
}
EXPECTED_KEYLESS_STATUS = {
    "sam-gov": "missing_required",
    "bls-oews": "limited_fallback",
    "gsa-perdiem": "limited_fallback",
    "regulations-gov": "limited_fallback",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin",
        choices=(
            "pre-award-agent",
            "other-transaction-agent",
            "govcon-growth-agent",
            "market-research-agent",
            "acquisition-policy-agent",
        ),
        default="pre-award-agent",
    )
    parser.add_argument(
        "--include-remote",
        action="store_true",
        help="Initialize and list tools on approved remote MCPs. This makes no tool call.",
    )
    parser.add_argument(
        "--host-profile",
        type=Path,
        help="Discover every stdio server in a complete Codex host profile instead of one plugin.",
    )
    parser.add_argument(
        "--keyless-status",
        action="store_true",
        help="Remove credential variables and call each local get_access_status operation.",
    )
    return parser.parse_args()


async def discover(
    name: str, config: dict[str, object], keyless_status: bool = False
) -> tuple[list[str], str | None]:
    env = os.environ.copy()
    env.update(config.get("env", {}))
    if keyless_status:
        for credential in KEYED_ENV_VARS.values():
            env.pop(credential, None)
    parameters = StdioServerParameters(
        command=str(config["command"]),
        args=[str(value) for value in config.get("args", [])],
        env=env,
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await asyncio.wait_for(session.initialize(), timeout=60)
            result = await asyncio.wait_for(session.list_tools(), timeout=30)
            access_status = None
            if keyless_status and name in EXPECTED_KEYLESS_STATUS:
                status_result = await asyncio.wait_for(
                    session.call_tool("get_access_status", {}), timeout=30
                )
                dumped = status_result.model_dump(mode="json", by_alias=True)
                payload = dumped.get("structuredContent") or dumped.get("structured_content")
                if not isinstance(payload, dict):
                    for item in status_result.content:
                        value = getattr(item, "text", None)
                        if isinstance(value, str):
                            try:
                                candidate = json.loads(value)
                            except json.JSONDecodeError:
                                continue
                            if isinstance(candidate, dict):
                                payload = candidate
                                break
                if not isinstance(payload, dict):
                    raise RuntimeError(f"{name} get_access_status returned no object")
                access_status = payload.get("status")
                if access_status != EXPECTED_KEYLESS_STATUS[name]:
                    raise RuntimeError(
                        f"{name} keyless status must be {EXPECTED_KEYLESS_STATUS[name]}, got {access_status!r}"
                    )
    tools = sorted(tool.name for tool in result.tools)
    missing = EXPECTED_TOOLS[name] - set(tools)
    if missing:
        raise RuntimeError(f"{name} is missing expected tools: {sorted(missing)}")
    if name == "usaspending":
        profile = config.get("env", {}).get("USASPENDING_TOOL_PROFILE")
        if profile != "acquisition-agent":
            raise RuntimeError("Packaged USASpending must select acquisition-agent")
        if len(tools) != 20:
            raise RuntimeError(
                f"Packaged USASpending profile must expose 20 tools, got {len(tools)}"
            )
    return tools, access_status


async def discover_remote(name: str, config: dict[str, object]) -> tuple[list[str], str]:
    if config != {"type": "http", "url": TAVILY_ENDPOINT, "headers": TAVILY_HEADERS}:
        raise RuntimeError(f"{name} does not match the approved keyless Tavily configuration")
    async with httpx.AsyncClient(headers=TAVILY_HEADERS, timeout=30.0) as client:
        async with streamable_http_client(TAVILY_ENDPOINT, http_client=client) as streams:
            read_stream, write_stream = streams[:2]
            async with ClientSession(read_stream, write_stream) as session:
                await asyncio.wait_for(session.initialize(), timeout=30)
                result = await asyncio.wait_for(session.list_tools(), timeout=30)
    observed = [
        {"name": tool.name, "inputSchema": tool.input_schema}
        for tool in sorted(result.tools, key=lambda item: item.name)
    ]
    tools = [item["name"] for item in observed]
    missing = EXPECTED_TOOLS[name] - set(tools)
    if missing:
        raise RuntimeError(f"{name} is missing expected tools: {sorted(missing)}")
    encoded = json.dumps(observed, sort_keys=True, separators=(",", ":")).encode()
    return tools, hashlib.sha256(encoded).hexdigest()


async def main_async(
    plugin: str,
    include_remote: bool,
    host_profile: Path | None = None,
    keyless_status: bool = False,
) -> None:
    if host_profile is not None:
        parsed = tomllib.loads(host_profile.read_text(encoding="utf-8"))
        servers = parsed["mcp_servers"]
        expected = set(EXPECTED_TOOLS) - {"tavily-web"}
        if set(servers) != expected:
            raise RuntimeError(
                f"host profile server inventory differs: expected {sorted(expected)}, got {sorted(servers)}"
            )
    else:
        path = REPO_ROOT / "plugins" / plugin / ".mcp.json"
        servers = json.loads(path.read_text(encoding="utf-8"))["mcpServers"]
    for name in sorted(servers):
        if name == "tavily-web":
            if not include_remote:
                print("tavily-web: remote discovery skipped; use --include-remote for the manual release check")
                continue
            tools, schema_hash = await discover_remote(name, servers[name])
            print(
                f"{name}: discovered {len(tools)} advertised tools without invoking any tool; "
                f"required subset present; schema sha256={schema_hash}"
            )
            continue
        tools, status = await discover(name, servers[name], keyless_status)
        suffix = ""
        if status is not None:
            suffix = f"; keyless get_access_status={status}"
        print(f"{name}: discovered {len(tools)} tools without an upstream call{suffix}")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(
        main_async(
            args.plugin,
            args.include_remote,
            args.host_profile,
            args.keyless_status,
        )
    )
