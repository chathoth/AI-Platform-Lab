# 03 - MCP vs. Hand-Rolled Tool Calling

## Introduction

Module 02 chapter 14's tool-calling example is genuinely correct and
still the right choice for plenty of cases. This chapter is an honest
comparison — what MCP adds, what it costs, and when reaching for a
protocol is worth it over the simpler hand-rolled version.

## Learning Objectives

After this chapter I should be able to:

-   Compare hand-rolled tool calling against an MCP server directly.
-   Identify the specific reuse and discovery benefits MCP adds.
-   Decide, for a given project, whether MCP is worth the extra
    moving parts.

------------------------------------------------------------------------

# Side by Side

``` python
# module 02 chapter 14's approach - a tool defined inline, in the same
# process that calls the model
tools = [{
    "type": "function",
    "function": {
        "name": "get_disk_usage",
        "description": "...",
        "parameters": {...},
    },
}]

def get_disk_usage(hostname: str) -> dict:
    ...

# the model, the tool schema, and the tool implementation all live
# in one file, tightly coupled together
```

``` python
# MCP approach - the tool lives in a SEPARATE process (the server),
# with no knowledge of which model or application will call it
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    ...
```

The tool implementation is nearly identical — MCP doesn't change *how*
you write a tool. What changes is **where it lives** and **who can use
it**.

## What MCP Actually Adds

  Capability                     Hand-rolled (module 02 ch. 14)   MCP
  --------------------------------- ---------------------------------- --------------------------------
  Reusable across applications         No - copy the code into each app    Yes - any client can connect
  Reusable across models                 No - schema format is model-specific | Yes - one server, any model behind the client
  Discoverable at runtime                   No - hardcoded into the app         Yes - `list_tools()` (chapter 16)
  Standardized resources/prompts too         No - ad hoc per project              Yes - three primitives, one protocol
  Process isolation                           No - runs in-process                 Yes - server can run as a separate process, even a separate machine

**Platform analogy:** this is the same trade-off as writing a function
inline in a script versus publishing it as a package with a stable
API. Inline is faster for a one-off; a published package pays off the
moment more than one consumer needs it, or the underlying implementation
needs to evolve independently of any one caller.

## What It Costs

  Cost                                      Detail
  -------------------------------------------- --------------------------------------
  Extra moving parts                              A server process, a client connection, a transport (chapter 04) to manage
  Slight latency overhead                           An extra hop (client -> server) vs. an in-process function call
  Learning curve                                     A protocol and SDK to learn, on top of the tool-calling concept itself

## When to Reach for Each

``` text
One tool, one application, never reused elsewhere?
        → hand-rolled (module 02 ch. 14) is simpler, faster to ship

A tool that should be usable from multiple apps (a chat UI, an
IDE assistant, a CLI script), or that should work with whichever
model a user has configured?
        → MCP server

Building toward an ecosystem of tools shared across a team or
org, where reuse matters more than any single integration's speed?
        → MCP server, from the start
```

## Hands-on: Feel the Coupling Difference

Take the `get_disk_usage` tool from module 02 chapter 14's example. In
that version, swapping to a different model means rewriting the tool
schema in that model's format. In chapter 08's MCP version (built next
in this module), the exact same server, unmodified, gets called by a
plain Python client (chapter 09) *and* bridged into a completely
different model's tool-calling format (chapter 10) — with zero changes
to the tool itself. That's the reuse benefit, made concrete rather than
asserted.

## Common Misconceptions

❌ MCP replaces the need to understand tool calling.
(It's built on the exact same underlying concept from module 02
chapter 14 — a model requests a call, something executes it, the
result comes back. MCP standardizes the wiring, not the concept.)

❌ Every tool should be built as an MCP server.
(For a single-use, single-application tool, the hand-rolled approach
is simpler and has less overhead — MCP earns its keep specifically
through reuse and discoverability.)

✔ The deciding question is reuse: will more than one application or
model need this tool, now or plausibly soon? If yes, MCP's extra
moving parts pay for themselves quickly.

## Interview Questions

1.  What does an MCP tool implementation have in common with a
    hand-rolled tool from module 02?
2.  Name three capabilities MCP adds that hand-rolled tool calling
    doesn't have.
3.  What's the cost of choosing MCP over a simpler in-process function
    call?
4.  What's the deciding question for choosing MCP over hand-rolled
    tool calling?

## Summary

MCP and hand-rolled tool calling share the same underlying concept —
the difference is reuse, discoverability, and process isolation, at
the cost of an extra process and protocol to manage. Choose hand-rolled
for a single-use, single-application tool; choose MCP the moment more
than one application or model plausibly needs the same tool.

## Next Chapter

➡️ `04-Transports-stdio-and-HTTP.md`
