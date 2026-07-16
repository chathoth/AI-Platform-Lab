# 05 - Tools

## Introduction

Tools are the MCP primitive most directly inherited from module 02
chapter 14 — a function the model can request to have executed. This
chapter covers defining them with the `mcp` SDK, verified against a
real server that a real local model successfully called in this
module's own testing.

## Learning Objectives

After this chapter I should be able to:

-   Define an MCP tool using the `@mcp.tool()` decorator.
-   Explain how the SDK derives a tool's schema automatically.
-   Write tool descriptions with the same care module 02 chapter 14
    recommends for tool schemas generally.

------------------------------------------------------------------------

# Defining a Tool

``` python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    fake_data = {"db-primary-01": 92, "web-node-01": 41}
    return {"hostname": hostname, "disk_percent": fake_data.get(hostname, 50)}
```

This is verified, runnable code — the exact tool used to confirm this
module's server-client-model bridge works end to end (chapter 10).

## Where the Schema Actually Comes From

Unlike module 02 chapter 14, where the JSON schema was written by
hand, the `mcp` SDK **derives it automatically** from the function's
type hints and docstring:

``` text
Function signature:  get_disk_usage(hostname: str) -> dict
Docstring:            "Get current disk usage percentage for a given host."

Derived schema (verified output from list_tools()):
{
    "name": "get_disk_usage",
    "description": "Get current disk usage percentage for a given host.",
    "parameters": {
        "properties": {"hostname": {"title": "Hostname", "type": "string"}},
        "required": ["hostname"],
        "type": "object"
    }
}
```

**Platform analogy:** this is the same idea as generating an OpenAPI
spec from type-annotated route handlers (FastAPI does exactly this) —
the schema isn't hand-maintained separately from the code; it's derived
from the code itself, so it can't silently drift out of sync with the
actual function signature.

## Descriptions Still Matter as Much as Ever

The SDK generates the schema's *shape* automatically, but the
*description* quality is still entirely up to you — and module 02
chapter 14's warning still applies directly: a vague docstring produces
wrong tool selection, exactly like a vague tool description would in
hand-rolled function calling.

``` python
# vague - a model may not reliably know when to reach for this
@mcp.tool()
def check(h: str) -> dict:
    """Checks a thing."""
    ...

# specific - clear about what it does and when it's useful
@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host. Use this
    when asked about disk space, storage capacity, or whether a host
    is running low on disk."""
    ...
```

## Tools Can Do More Than Return Static Data

``` python
@mcp.tool()
def restart_service(service_name: str, environment: str) -> dict:
    """Restart a named service in a given environment. DESTRUCTIVE -
    only call this after explicit user confirmation."""
    # a real implementation would call your actual deployment API
    return {"service": service_name, "environment": environment, "status": "restarted"}
```

The same rule from module 02 chapter 14 and module 01 chapter 18
applies without exception: a tool with real side effects needs
validation and confirmation built into its own logic (or the calling
application's logic) — the model requesting a call is still just a
suggestion, never an unchecked command (chapter 14 of this module goes
deeper on this specific risk).

## Hands-on: Verify the Derived Schema Yourself

``` python
# save as server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    return {"hostname": hostname, "disk_percent": 50}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Chapter 09's client, run against this server, prints the real derived
schema via `list_tools()` — confirm it matches your function's type
hints and docstring exactly, rather than assuming the SDK did the right
thing.

## Common Misconceptions

❌ You need to write a JSON schema by hand for an MCP tool.
(The SDK derives it from your function's type hints and docstring —
verified directly against a running server's `list_tools()` output.)

❌ A well-typed function signature means the description doesn't
matter.
(Type hints define the schema's *shape*; the docstring is still what
determines whether a model correctly understands *when* to use the
tool — same discipline as module 02 chapter 14.)

✔ Because the schema is derived from the function itself, keeping the
function signature and docstring accurate is now the *entire*
maintenance burden for schema correctness — there's no separate schema
file that can silently drift.

## Interview Questions

1.  How does the `mcp` SDK derive a tool's schema, and what verified
    this in this module?
2.  Why does tool description quality still matter even though the
    schema is auto-generated?
3.  What additional care does a tool with real side effects need,
    beyond just being correctly defined?
4.  How is auto-derived schema generation similar to FastAPI's OpenAPI
    generation?

## Summary

MCP tools are Python functions decorated with `@mcp.tool()`, with their
schema automatically derived from type hints and docstrings — verified
directly by inspecting a running server's `list_tools()` output.
Description quality remains entirely the developer's responsibility,
and any tool with real side effects still needs the same validation
discipline module 02 chapter 14 requires for hand-rolled tool calling.

## Next Chapter

➡️ `06-Resources.md`
