"""
Example: 07_authorization.py

Call 01_server.py's restart_service tool with a readonly role (should
be refused) and an operator role (should succeed) - the authorization
check is a guard clause INSIDE the tool itself, not just a prompt
instruction the model could be talked out of. Also confirms 'prod' is
refused for every role. Ties back to
docs/13-Authentication-and-Authorization.md.

Run:
    pip install mcp
    python 07_authorization.py
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("--- readonly role calling restart_service (should be refused) ---")
            r1 = await session.call_tool(
                "restart_service",
                {"service_name": "checkout-api", "environment": "staging", "caller_role": "readonly"},
            )
            print(" ", r1.content[0].text)

            print("\n--- operator role, staging (should succeed) ---")
            r2 = await session.call_tool(
                "restart_service",
                {"service_name": "checkout-api", "environment": "staging", "caller_role": "operator"},
            )
            print(" ", r2.content[0].text)

            print("\n--- operator role, prod (should ALWAYS be refused, regardless of role) ---")
            r3 = await session.call_tool(
                "restart_service",
                {"service_name": "checkout-api", "environment": "prod", "caller_role": "operator"},
            )
            print(" ", r3.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
