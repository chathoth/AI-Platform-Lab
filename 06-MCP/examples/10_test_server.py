"""
Example: 10_test_server.py

Automated tests for 01_server.py using the VERIFIED working pattern -
connecting inside each test, not a shared async fixture (which was
confirmed to produce intermittent teardown errors with MCP's
stdio_client). Ties back to docs/17-Testing-an-MCP-Server.md.

Run:
    pip install mcp pytest pytest-asyncio
    pytest 10_test_server.py -v
"""

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])


@pytest.mark.asyncio
async def test_get_disk_usage_known_host():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("get_disk_usage", {"hostname": "db-primary-01"})
            assert "92" in result.content[0].text


@pytest.mark.asyncio
async def test_get_disk_usage_unknown_host_returns_structured_error():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("get_disk_usage", {"hostname": "totally-made-up-host"})
            assert "error" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_server_exposes_expected_tools():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = {t.name for t in tools.tools}
            assert "get_disk_usage" in tool_names
            assert "restart_service" in tool_names


@pytest.mark.asyncio
async def test_tool_schema_has_required_hostname_param():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            disk_tool = next(t for t in tools.tools if t.name == "get_disk_usage")
            assert "hostname" in disk_tool.inputSchema["required"]


@pytest.mark.asyncio
async def test_restart_service_refuses_readonly_role():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "restart_service",
                {"service_name": "checkout-api", "environment": "staging", "caller_role": "readonly"},
            )
            assert "not authorized" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_restart_service_refuses_prod_even_for_operator():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "restart_service",
                {"service_name": "checkout-api", "environment": "prod", "caller_role": "operator"},
            )
            assert "never allowed against 'prod'" in result.content[0].text
