# 06 - Giving an Agent Tools

## Introduction

An agent that can only think isn't very useful — the "act" step
(chapter 02) needs real tools to act with. This chapter connects
straight back to module 02 chapter 14 and module 06: the tools
themselves are nothing new, but wiring several of them into one agent,
correctly, is worth doing carefully.

## Learning Objectives

After this chapter I should be able to:

-   Define a small set of tools for an agent to choose from.
-   Explain why tool descriptions matter even more for agents than for
    a single tool call.
-   Choose between plain functions and MCP servers (module 06) for an
    agent's tools.

------------------------------------------------------------------------

# Tools Are Exactly What Module 02 Chapter 14 Already Covered

``` python
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    ...

def restart_service(service_name: str) -> dict:
    """Restart a named service."""
    ...

tool_schemas = [
    {"type": "function", "function": {"name": "get_disk_usage", "description": "...", "parameters": {...}}},
    {"type": "function", "function": {"name": "restart_service", "description": "...", "parameters": {...}}},
]
```

Nothing about this is agent-specific — it's the same schema-plus-
Python-function pattern from module 02 chapter 14. What's different is
that an agent picks *which* tool to call, *repeatedly*, across many
turns — so a mistake in one tool's description doesn't just cause one
wrong call, it can steer several turns of reasoning in the wrong
direction.

## Why Descriptions Matter More Here

Module 02 chapter 09's instruction-clarity lesson and module 06
chapter 11's schema-design lesson both apply, with the stakes raised:
an agent choosing between three or four tools, turn after turn, needs
each one's description to clearly signal **when** to use it, not just
what it does.

``` python
# ambiguous - when should the model use THIS instead of get_disk_usage?
def check_storage(host: str) -> dict:
    """Checks storage."""
    ...

# clear - distinguishes itself from a similarly-named tool
def get_disk_usage(hostname: str) -> dict:
    """Get the CURRENT disk usage percentage for one host. Use this
    FIRST when investigating disk space issues, before any cleanup
    action."""
    ...
```

## Reusing MCP for an Agent's Tools

Module 06 built tools as MCP servers specifically so they're reusable
across applications. An agent is exactly the kind of application that
benefits: point an agent's tool-calling loop at an MCP server (module
06 chapter 10's bridging pattern) instead of hardcoding functions, and
the same tools become usable by any other agent or application later,
with no rewrite.

``` text
Plain functions (this module's examples):
  simplest to start with, tightly coupled to one script

MCP server (module 06):
  more setup, but the tools become reusable across every
  agent/application that speaks MCP - worth it once more than one
  agent needs the same tools
```

This module's own examples use plain functions to keep the core agent
loop visible without an extra layer — chapter 08's hands-on section
notes exactly where you'd swap in an MCP client instead.

## Hands-on: Write Two Tools With Deliberately Different Description
Quality

``` python
def vague_tool(host: str) -> dict:
    """Checks something."""
    return {}

def clear_tool(hostname: str) -> dict:
    """Get current disk usage percentage for a host. Use this to check
    if a server is running low on disk space."""
    return {}
```

Give both to a local model alongside a clearly disk-related question
and see which one it reaches for — this is the same exercise module 02
chapter 14 ran for a single tool call, worth repeating here because an
agent's repeated tool selection makes the effect more visible over
several turns.

## Common Misconceptions

❌ Agent tools need to be built differently from ordinary tool-calling
functions.
(They're the exact same pattern from module 02 chapter 14 — what
changes is that an agent selects among several of them, repeatedly,
which raises the bar on description clarity.)

❌ MCP is required to give an agent tools.
(Plain Python functions work fine, and this module's examples use
them for simplicity — MCP (module 06) becomes worth the extra setup
specifically when tools need to be shared across more than one
application.)

✔ A vague tool description doesn't just risk one wrong call — in an
agent's repeated loop, it risks steering several turns of reasoning
down the wrong path before the mistake becomes obvious.

## Interview Questions

1.  What's the difference between how tools are defined for a single
    tool call versus for an agent?
2.  Why does tool description quality matter more in an agent's loop
    than in a one-off tool call?
3.  When would you reach for an MCP server instead of plain functions
    for an agent's tools?
4.  What's the risk of an ambiguous tool description specifically in a
    multi-turn agent loop?

## Summary

An agent's tools are built exactly the way module 02 chapter 14 and
module 06 already covered — the difference is that an agent chooses
among several of them, repeatedly, so unclear descriptions can steer
multiple turns of reasoning astray instead of causing just one bad
call. Plain functions are the simplest starting point; MCP servers
(module 06) are worth the extra setup once tools need to be shared
across more than one agent or application.

## Next Chapter

➡️ `07-Building-a-Minimal-Agent-From-Scratch.md`
