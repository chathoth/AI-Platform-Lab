"""
Example: 05_structured_errors.py

Compare a tool call for a known host against an unknown one, showing
01_server.py's structured error response instead of a raw exception.
Ties back to docs/12-Error-Handling-in-MCP-Tools.md.

Run:
    pip install mcp
    python 05_structured_errors.py
"""

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            good = await session.call_tool("get_disk_usage", {"hostname": "db-primary-01"})
            print("Known host:")
            print(" ", good.content[0].text)

            bad = await session.call_tool("get_disk_usage", {"hostname": "totally-made-up-host"})
            print("\nUnknown host:")
            print(" ", bad.content[0].text)

            parsed = json.loads(bad.content[0].text)
            assert parsed.get("error") is True
            print("\nThis is a structured error the caller can act on -")
            print("not a raw Python traceback.")


if __name__ == "__main__":
    asyncio.run(main())
