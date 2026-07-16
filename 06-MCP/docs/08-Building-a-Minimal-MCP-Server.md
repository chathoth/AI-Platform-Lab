# 08 - Building a Minimal MCP Server

## Introduction

Chapters 05-07 covered each primitive individually. This chapter puts
them together into one real, complete server file — the exact one
verified against a real client and a real local model in this module's
own testing, not a simplified version written just for the page.

## Learning Objectives

After this chapter I should be able to:

-   Write a complete MCP server file with a tool, a resource, and a
    prompt.
-   Run it and understand what `mcp.run(transport="stdio")` actually
    does.
-   Know where to look when a server doesn't behave as expected.

------------------------------------------------------------------------

# The Complete, Verified Server

``` python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    fake_data = {"db-primary-01": 92, "web-node-01": 41}
    return {"hostname": hostname, "disk_percent": fake_data.get(hostname, 50)}

@mcp.resource("runbook://crashloop")
def crashloop_runbook() -> str:
    """Runbook for debugging CrashLoopBackOff."""
    return "Check kubectl describe pod and kubectl logs --previous."

@mcp.prompt()
def incident_summary(log_text: str) -> str:
    """Build a prompt that summarizes an incident log."""
    return f"Summarize this incident log in 2 sentences:\n{log_text}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

This file, run as `python3 server.py`, is a complete, working MCP
server — no additional configuration needed. Every piece of this file
was independently verified against a real client connection while
building this module.

## What `mcp.run(transport="stdio")` Actually Does

Calling `.run()` starts the server's message loop: it reads incoming
JSON-RPC requests from stdin, dispatches them to the right registered
tool/resource/prompt handler, and writes responses to stdout (chapter
04). The `FastMCP("infra-tools")` name is how the server identifies
itself to a connecting client during the initialization handshake.

## Registration Happens at Import Time

Every `@mcp.tool()`, `@mcp.resource()`, and `@mcp.prompt()` decorator
registers that function with the `mcp` object the moment the module is
imported — before `mcp.run()` is ever called. This is why
`mcp.list_tools()`, checked immediately after import, already reflects
every decorated function in the file, with no separate "startup"
registration step to worry about.

## Hands-on: Run It Yourself

``` bash
pip install mcp
python3 server.py
```

Running it directly won't print anything and won't exit — it's
blocked, waiting for a client to connect over stdin/stdout. That's
correct behavior, not a hang. Press Ctrl+C to stop it, and continue to
chapter 09 to build the client that actually talks to it — this server
does nothing useful on its own, by design, until something connects.

``` bash
# a faster way to sanity-check a server without writing a client:
# the MCP Inspector (chapter 17) can connect to it interactively
npx @modelcontextprotocol/inspector python3 server.py
```

## Common Misconceptions

❌ Running a server file directly should produce visible output.
(A correctly running `stdio` server blocks silently, waiting on
stdin — this is expected, not a bug. Verify it's working by connecting
a client, chapter 09, rather than by watching for console output.)

❌ Tools, resources, and prompts need to be registered in some
separate configuration step.
(The decorators register everything at import time — by the time
`mcp.run()` executes, every capability is already known to the server
object.)

✔ This exact file is what chapters 09 and 10 connect to — if something
in those later chapters doesn't work, this file (and confirming it
runs without a Python error) is the first thing to check.

## Interview Questions

1.  What does `mcp.run(transport="stdio")` actually do when called?
2.  Why does a correctly-running stdio server appear to "hang" with no
    output?
3.  When are a server's tools, resources, and prompts actually
    registered — at `mcp.run()` time, or earlier?
4.  What's a fast way to sanity-check a server without writing a full
    client?

## Summary

A complete MCP server is a Python file that creates a `FastMCP`
instance, decorates functions as tools/resources/prompts, and calls
`.run()` to start its message loop — everything registers at import
time, and a correctly running `stdio` server blocks silently until a
client connects. This chapter's server file is the exact one used to
verify every other chapter in this module.

## Next Chapter

➡️ `09-Building-an-MCP-Client.md`
