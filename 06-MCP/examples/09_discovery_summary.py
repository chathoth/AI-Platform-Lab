"""
Example: 09_discovery_summary.py

A generic function that summarizes ANY connected server's full
capability set via discovery - the same mechanism that lets
03_bridge_to_ollama.py's bridging code work with any server's tools
without being hardcoded to one. Ties back to
docs/16-Discovery-Listing-Capabilities.md.

Run:
    pip install mcp
    python 09_discovery_summary.py
"""

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])


async def summarize_server(session: ClientSession) -> dict:
    tools = await session.list_tools()
    resources = await session.list_resources()
    templates = await session.list_resource_templates()
    prompts = await session.list_prompts()
    return {
        "tools": [{"name": t.name, "description": t.description} for t in tools.tools],
        "resources": [str(r.uri) for r in resources.resources],
        "resource_templates": [t.uriTemplate for t in templates.resourceTemplates],
        "prompts": [p.name for p in prompts.prompts],
    }


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            summary = await summarize_server(session)
            print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
