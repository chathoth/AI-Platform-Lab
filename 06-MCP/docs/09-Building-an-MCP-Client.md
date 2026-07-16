# 09 - Building an MCP Client

## Introduction

Chapter 08 built a server that does nothing until something connects
to it. This chapter is that something — a real, complete MCP client
that spawns the server, connects, and calls every one of its
capabilities. Every line of output shown here is from an actual
verified run, not a hypothetical transcript.

## Learning Objectives

After this chapter I should be able to:

-   Write a complete MCP client that connects to a server over stdio.
-   Call a tool, read a resource, and render a prompt from client
    code.
-   Explain the `initialize()` handshake's role.

------------------------------------------------------------------------

# The Complete, Verified Client

``` python
# client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python3", args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])
            result = await session.call_tool("get_disk_usage", {"hostname": "db-primary-01"})
            print("Tool result:", result.content[0].text)

            # resources
            resources = await session.list_resources()
            print("Resources:", [str(r.uri) for r in resources.resources])
            content = await session.read_resource("runbook://crashloop")
            print("Resource content:", content.contents[0].text)

            # prompts
            prompts = await session.list_prompts()
            print("Prompts:", [p.name for p in prompts.prompts])
            rendered = await session.get_prompt("incident_summary", {"log_text": "pod crashed 3 times"})
            print("Rendered prompt:", rendered.messages[0].content.text)

asyncio.run(main())
```

Verified output, running this against chapter 08's server:

``` text
Tools: ['get_disk_usage']
Tool result: {
  "hostname": "db-primary-01",
  "disk_percent": 92
}
Resources: ['runbook://crashloop']
Resource content: Check kubectl describe pod and kubectl logs --previous.
Prompts: ['incident_summary']
Rendered prompt: Summarize this incident log in 2 sentences:
pod crashed 3 times
```

## What `StdioServerParameters` Actually Does

``` python
params = StdioServerParameters(command="python3", args=["server.py"])
```

This tells `stdio_client` exactly how to **spawn the server as a
subprocess** — chapter 04's transport explanation, made concrete. The
client doesn't connect to an already-running server over `stdio`; it
starts one itself, and the connection lives exactly as long as that
subprocess does.

## The `initialize()` Handshake

``` python
await session.initialize()
```

Before any tool, resource, or prompt call succeeds, the client and
server exchange an initialization handshake — protocol version
negotiation and capability discovery. Skipping this call is a real,
common error; every method call afterward assumes it already happened.

## Hands-on: Run This Exact Client Yourself

``` bash
pip install mcp
# with server.py from chapter 08 in the same directory:
python3 client.py
```

Confirm your own output matches the verified transcript above, line
for line, for the tool and resource sections at minimum (the
`db-primary-01` disk value is hardcoded in chapter 08's server, so it
should match exactly).

## Common Misconceptions

❌ The client connects to a server that's already running somewhere.
(With `stdio_client`, the client spawns the server process itself —
there's no separately-running server to connect to beforehand.)

❌ You can call `list_tools()` or `call_tool()` before `initialize()`.
(The handshake must complete first — every subsequent call assumes the
session is already initialized.)

✔ This client, run against chapter 08's server, is a complete,
working, verified round trip through all three MCP primitives — a
solid base to extend rather than a simplified toy.

## Interview Questions

1.  What does `StdioServerParameters` actually configure?
2.  Does the client connect to an already-running server, or does it
    start one? How, specifically?
3.  What is `session.initialize()` for, and what happens if you skip
    it?
4.  Walk through what this chapter's client does, from spawning the
    server to printing the prompt result.

## Summary

A complete MCP client spawns the server as a subprocess via
`StdioServerParameters`, performs an `initialize()` handshake, and then
calls `list_tools()`/`call_tool()`, `list_resources()`/`read_resource()`,
and `list_prompts()`/`get_prompt()` — all verified directly against
chapter 08's server with real output. This client is the piece that
turns a server sitting idle into something actually useful.

## Next Chapter

➡️ `10-Bridging-MCP-to-a-Models-Tool-Calling-API.md`
