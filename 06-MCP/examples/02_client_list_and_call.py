"""
Example: 02_client_list_and_call.py

A complete MCP client: spawn 01_server.py, connect, and exercise all
three primitives (tools, resources, prompts). Ties back to
docs/09-Building-an-MCP-Client.md.

Run:
    pip install mcp
    python 02_client_list_and_call.py
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])
            result = await session.call_tool("get_disk_usage", {"hostname": "db-primary-01"})
            print("Tool result:", result.content[0].text)

            resources = await session.list_resources()
            print("\nResources:", [str(r.uri) for r in resources.resources])
            content = await session.read_resource("runbook://crashloop")
            print("Resource content:", content.contents[0].text)

            prompts = await session.list_prompts()
            print("\nPrompts:", [p.name for p in prompts.prompts])
            rendered = await session.get_prompt("incident_summary", {"log_text": "pod crashed 3 times"})
            print("Rendered prompt:", rendered.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())
