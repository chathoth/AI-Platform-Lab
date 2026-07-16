"""
Example: 03_bridge_to_ollama.py

Bridge 01_server.py's tools into a local Ollama model's native
tool-calling loop. The server has zero knowledge of Ollama - this
script is the only model-specific code in the chain. Ties back to
docs/10-Bridging-MCP-to-a-Models-Tool-Calling-API.md.

Run:
    ollama pull llama3.1:8b
    pip install mcp openai
    python 03_bridge_to_ollama.py
"""

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

SERVER = StdioServerParameters(command="python3", args=["01_server.py"])
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def mcp_tool_to_openai_schema(tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema,
        },
    }


async def ask(session, question: str, openai_tools: list[dict]):
    messages = [{"role": "user", "content": question}]
    response = client.chat.completions.create(model="llama3.1:8b", messages=messages, tools=openai_tools)
    msg = response.choices[0].message

    if msg.tool_calls:
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            print(f"  [tool call] {call.function.name}({args})")
            result = await session.call_tool(call.function.name, args)
            print(f"  [tool result] {result.content[0].text}")
    else:
        print(f"  [direct answer, no tool needed] {msg.content}")


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            openai_tools = [mcp_tool_to_openai_schema(t) for t in mcp_tools]

            print("Q: Is disk usage on db-primary-01 critical?")
            await ask(session, "Is disk usage on db-primary-01 critical?", openai_tools)

            print("\nQ: What is a Kubernetes readiness probe?")
            await ask(session, "What is a Kubernetes readiness probe?", openai_tools)
            print("  (should NOT trigger a tool call - the tool can't help with this)")


if __name__ == "__main__":
    asyncio.run(main())
