# 10 - Bridging MCP to a Model's Tool-Calling API

## Introduction

This is the payoff chapter — the moment MCP and a real model actually
meet. Chapter 02 stated the LLM call isn't part of MCP itself; this
chapter is the verified proof, bridging chapter 08's server's tools
into a local Ollama model's native tool-calling format (module 02
chapter 14) and watching the model correctly choose and call a real
tool.

## Learning Objectives

After this chapter I should be able to:

-   Convert an MCP tool's schema into a model's native tool-calling
    format.
-   Complete the full loop: model requests a call, MCP executes it,
    result feeds back.
-   Explain why this bridge code is what makes MCP genuinely
    model-agnostic.

------------------------------------------------------------------------

# The Complete, Verified Bridge

``` python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def mcp_tool_to_openai_schema(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema,
        },
    }

async def main():
    params = StdioServerParameters(command="python3", args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            openai_tools = [mcp_tool_to_openai_schema(t) for t in mcp_tools]

            messages = [{"role": "user", "content": "Is disk usage on db-primary-01 critical?"}]
            response = client.chat.completions.create(model="llama3.1:8b", messages=messages, tools=openai_tools)
            msg = response.choices[0].message

            if msg.tool_calls:
                for call in msg.tool_calls:
                    args = json.loads(call.function.arguments)
                    result = await session.call_tool(call.function.name, args)
                    print(f"{call.function.name}({args}) -> {result.content[0].text}")
            else:
                print("No tool call, direct answer:", msg.content)

asyncio.run(main())
```

Verified output, running this against chapter 08's server with
`llama3.1:8b` via Ollama:

``` text
get_disk_usage({'hostname': 'db-primary-01'}) -> {
  "hostname": "db-primary-01",
  "disk_percent": 92
}
```

The model, given only the MCP server's auto-derived schema (chapter
05), correctly decided a tool call was needed and correctly extracted
`hostname` from the question in plain English — with zero
model-specific tool code written by hand.

## The One Line That Does the Real Work

``` python
def mcp_tool_to_openai_schema(tool):
    return {
        "type": "function",
        "function": {"name": tool.name, "description": tool.description or "", "parameters": tool.inputSchema},
    }
```

This function is the entire "bridge" — it translates MCP's tool schema
format into the OpenAI-compatible format module 02 chapter 14 already
covered. This is genuinely all it takes, because MCP's schema format
(JSON Schema) and OpenAI-compatible tool-calling's parameter format are
close enough that no lossy conversion is needed for a typical tool.

## Why This Proves MCP Is Model-Agnostic

The server file from chapter 08 has **zero knowledge** of Ollama,
OpenAI's format, or any specific model — it was written once, in
chapters 05-08, entirely before this chapter existed. This chapter
only added a small conversion function and a completely separate model
call. Swapping `llama3.1:8b` for a different local model, or for a
hosted API, would only touch this bridging code — never the server.

**Platform analogy:** this is the adapter pattern — a small piece of
translation code at the boundary between two systems that otherwise
know nothing about each other, letting either side change independently
as long as the adapter keeps up.

## Hands-on: Run the Full Verified Loop Yourself

``` bash
ollama pull llama3.1:8b
pip install mcp openai
# with server.py from chapter 08 in the same directory:
python3 bridge.py
```

Then change the question to something the tool can't help with
("what's a Kubernetes readiness probe?") and confirm the model answers
directly, with no tool call — the same "don't force an irrelevant tool
call" check from module 02 chapter 14's own hands-on exercise.

## Common Misconceptions

❌ MCP servers need to be written differently depending on which model
will eventually use them.
(Chapter 08's server was written with no knowledge of any specific
model — this chapter's bridge function is the only model-specific code
in the entire chain, and it's small and swappable.)

❌ Bridging MCP to a model requires a large, complex integration.
(The verified bridge above is under 10 lines of actual translation
logic — MCP's schema format and typical tool-calling formats are
close enough that the conversion is nearly mechanical.)

✔ The clean separation between chapter 08's server (model-agnostic)
and this chapter's bridge (model-specific, small, swappable) is MCP's
core value made concrete — verified by literally reusing the same
server file unmodified.

## Interview Questions

1.  What does the `mcp_tool_to_openai_schema` function actually do,
    and why is it so small?
2.  Why does this chapter's server file need zero changes to work with
    a different model?
3.  Walk through the full verified loop from user question to tool
    result.
4.  How is this bridging code an example of the adapter pattern?

## Summary

Bridging an MCP server's tools to a model's native tool-calling API
takes a small, model-specific conversion function — verified directly
by running chapter 08's unmodified server against a local Ollama model
and watching it correctly select and call a real tool with zero
model-specific server code. This is the concrete proof behind chapter
01's central claim: build the tool once, use it with any model.

## Next Chapter

➡️ `11-Schema-Design-for-MCP-Tools.md`
