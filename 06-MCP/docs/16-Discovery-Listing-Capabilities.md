# 16 - Discovery: Listing Capabilities

## Introduction

Every example so far already used discovery without naming it —
`list_tools()`, `list_resources()`, `list_prompts()` appeared in
chapter 09's very first client. This chapter is why that matters: MCP
capabilities are discovered at connection time, not hardcoded into the
client ahead of time, which is what lets one generic client work with
any server it connects to.

## Learning Objectives

After this chapter I should be able to:

-   Explain why runtime discovery matters for MCP's model-agnostic
    goal.
-   Use all three `list_*` methods to build a generic capability
    summary.
-   Explain the difference between fixed resources and resource
    templates in discovery.

------------------------------------------------------------------------

# Discovery Is What Makes a Client Generic

A client doesn't need to know in advance what a server offers — it
asks, at connection time:

``` python
tools = await session.list_tools()
resources = await session.list_resources()
resource_templates = await session.list_resource_templates()
prompts = await session.list_prompts()
```

**Platform analogy:** this is exactly what makes a generic API
explorer (like Swagger UI reading an OpenAPI spec) work against any
compliant API without being hand-written for that specific API — the
client reads the server's self-description at runtime instead of
having that description compiled in ahead of time.

## Why This Matters for Chapter 10's Bridge

The bridging code from chapter 10 works with *any* MCP server's tools
because it never hardcodes a tool name — it calls `list_tools()` and
converts whatever comes back:

``` python
mcp_tools = (await session.list_tools()).tools
openai_tools = [mcp_tool_to_openai_schema(t) for t in mcp_tools]
```

Point this exact code at a server with completely different tools, and
it works unmodified — verified by the fact that this is literally the
mechanism chapter 10 tested, with no changes needed between "list what
this server offers" and "translate it for the model."

## Fixed Resources vs. Resource Templates in Discovery

``` python
resources = await session.list_resources()
# fixed, enumerable resources - e.g. runbook://crashloop

resource_templates = await session.list_resource_templates()
# parameterized templates - e.g. runbook://{topic}, not enumerable
# ahead of time since {topic} could be anything
```

This distinction (chapter 06) matters for discovery specifically: a
generic client can enumerate every fixed resource up front, but a
templated resource requires knowing (from context, or from the
template's own description) what values are valid to substitute — the
server can't practically list every possible value in advance.

## Building a Generic Capability Summary

``` python
async def summarize_server(session) -> dict:
    tools = await session.list_tools()
    resources = await session.list_resources()
    prompts = await session.list_prompts()
    return {
        "tools": [{"name": t.name, "description": t.description} for t in tools.tools],
        "resources": [str(r.uri) for r in resources.resources],
        "prompts": [p.name for p in prompts.prompts],
    }
```

A function like this, run against any connected server, is a complete
"what can this server do" report — useful for debugging (does the
server expose what I expect?), for building a generic multi-server
client, or simply for exploring an unfamiliar server before trusting it
(chapter 14's security review starts exactly here).

## Hands-on: Summarize a Real Server

Run the `summarize_server` function above against chapter 08's server
and confirm it reports all three registered capabilities correctly —
this is the fastest way to sanity-check a server's public surface
before writing any tool-specific integration code against it.

## Common Misconceptions

❌ A client needs to know a server's tools in advance to use it.
(Discovery via `list_tools()` (and the resource/prompt equivalents) is
exactly what removes that requirement — a generic client can adapt to
whatever a server offers at connection time.)

❌ Resource templates show up the same way as fixed resources in
discovery.
(They're listed separately via `list_resource_templates()`, since
their exact addresses depend on a parameter that isn't enumerable
ahead of time.)

✔ Discovery is the mechanism underneath chapter 10's entire "build the
tool once, any model can use it" claim — without runtime discovery, the
bridging code would need to be rewritten for every new server.

## Interview Questions

1.  Why does runtime discovery matter for MCP's goal of being
    model/application-agnostic?
2.  What three `list_*` methods does a client typically call to
    discover a server's full capability set?
3.  Why are resource templates listed separately from fixed resources?
4.  How does chapter 10's bridging code rely on discovery to work with
    any server, not just one specific one?

## Summary

MCP capabilities are discovered at connection time via `list_tools()`,
`list_resources()`/`list_resource_templates()`, and `list_prompts()` —
this is the mechanism that lets a generic client (or bridging code,
chapter 10) work with any compliant server without being hardcoded to
that server's specific capabilities in advance.

## Next Chapter

➡️ `17-Testing-an-MCP-Server.md`
