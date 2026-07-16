"""
Example: 04_resource_templates.py

Distinguish fixed resources from resource templates, and read a
parameterized resource with different topic values. Ties back to
docs/06-Resources.md and docs/16-Discovery-Listing-Capabilities.md.

Run:
    pip install mcp
    python 04_resource_templates.py
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            fixed = await session.list_resources()
            print("Fixed resources:", [str(r.uri) for r in fixed.resources])

            templates = await session.list_resource_templates()
            print("Resource templates:", [t.uriTemplate for t in templates.resourceTemplates])

            for topic in ["crashloop", "disk-full", "nonexistent-topic"]:
                content = await session.read_resource(f"runbook://{topic}")
                print(f"\nrunbook://{topic} -> {content.contents[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
