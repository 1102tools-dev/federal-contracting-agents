#!/usr/bin/env python3
"""Start pinned MCP servers and list tools without calling an upstream API."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOOLS = {
    "acquisition-gov": {"list_rfo_parts", "get_rfo_part", "list_rfo_agency_deviations", "get_rfo_agency_deviation", "get_rfo_guidance"},
    "bls-oews": {"detect_latest_year", "get_wage_data", "list_common_soc_codes"},
    "ecfr": {"get_cfr_content", "get_version_history", "compare_versions"},
    "federal-register": {"search_documents", "get_document", "open_comment_periods"},
    "gsa-calc": {"keyword_search"},
    "gsa-perdiem": {"lookup_city_perdiem", "get_mie_breakdown"},
    "sam-gov": {"search_opportunities", "search_entities", "search_contract_awards"},
    "regulations-gov": {"search_documents", "search_comments", "search_dockets"},
    "usaspending": {"search_awards", "spending_over_time", "search_recipients"},
    "tavily-web": {"tavily_search", "tavily_extract"},
}
TAVILY_ENDPOINT = "https://mcp.tavily.com/mcp/"
TAVILY_HEADERS = {"X-Tavily-Access-Mode": "keyless"}


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
    return parser.parse_args()


async def discover(name: str, config: dict[str, object]) -> list[str]:
    env = os.environ.copy()
    env.update(config.get("env", {}))
    parameters = StdioServerParameters(
        command=str(config["command"]),
        args=[str(value) for value in config.get("args", [])],
        env=env,
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await asyncio.wait_for(session.initialize(), timeout=60)
            result = await asyncio.wait_for(session.list_tools(), timeout=30)
    tools = sorted(tool.name for tool in result.tools)
    missing = EXPECTED_TOOLS[name] - set(tools)
    if missing:
        raise RuntimeError(f"{name} is missing expected tools: {sorted(missing)}")
    return tools


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


async def main_async(plugin: str, include_remote: bool) -> None:
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
        tools = await discover(name, servers[name])
        print(f"{name}: discovered {len(tools)} tools without invoking any tool")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main_async(args.plugin, args.include_remote))
