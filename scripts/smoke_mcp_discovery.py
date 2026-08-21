#!/usr/bin/env python3
"""Start pinned MCP servers and list tools without calling an upstream API."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOOLS = {
    "bls-oews": {"detect_latest_year", "get_wage_data", "list_common_soc_codes"},
    "gsa-calc": {"keyword_search"},
    "gsa-perdiem": {"lookup_city_perdiem", "get_mie_breakdown"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin",
        choices=("pre-award-agent", "other-transaction-agent"),
        default="pre-award-agent",
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


async def main_async(plugin: str) -> None:
    path = REPO_ROOT / "plugins" / plugin / ".mcp.json"
    servers = json.loads(path.read_text(encoding="utf-8"))["mcpServers"]
    for name in sorted(servers):
        tools = await discover(name, servers[name])
        print(f"{name}: discovered {len(tools)} tools without invoking any tool")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main_async(args.plugin))
