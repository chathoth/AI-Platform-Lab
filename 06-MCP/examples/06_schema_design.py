"""
Example: 06_schema_design.py

Compare the auto-derived schema for a vague tool against a precise
one using named types, Pydantic, and Literal constraints. Runs
entirely in-process - no client/server connection needed, since a
FastMCP object can be introspected directly. Ties back to
docs/11-Schema-Design-for-MCP-Tools.md.

Run:
    pip install mcp pydantic
    python 06_schema_design.py
"""

import asyncio
import json
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("schema-demo")


@mcp.tool()
def vague_tool(x: str, y: str, z: dict) -> dict:
    """Does a thing."""
    return {}


class IncidentUpdate(BaseModel):
    incident_id: str = Field(description="The incident ID, e.g. INC-2345")
    status: Literal["open", "investigating", "resolved", "closed"] = Field(
        description="New status for the incident"
    )
    notes: str = Field(default="", description="Optional notes about this update")


@mcp.tool()
def precise_tool(update: IncidentUpdate) -> dict:
    """Update an incident's status and notes."""
    return {"incident_id": update.incident_id, "status": update.status}


async def main():
    tools = await mcp.list_tools()
    for tool in tools:
        print(f"--- {tool.name} ---")
        print(json.dumps(tool.inputSchema, indent=2))
        print()

    print("Notice: vague_tool's schema gives the model no guidance about")
    print("what 'z' should contain. precise_tool's schema includes an enum")
    print("constraint on 'status' and a per-field description - a model")
    print("has far less room to send something wrong.")


if __name__ == "__main__":
    asyncio.run(main())
