# 06 - Resources

## Introduction

Resources are MCP's standardized answer to module 02 chapter 08's
context injection — instead of hardcoding a runbook excerpt into a
prompt, a server exposes it as a resource that any connected client
can read on demand. This chapter's example was verified directly:
a real resource, read over a real client connection, returning real
content.

## Learning Objectives

After this chapter I should be able to:

-   Define an MCP resource with the `@mcp.resource()` decorator.
-   Explain the difference between a tool and a resource.
-   Choose correctly between the two for a given piece of
    functionality.

------------------------------------------------------------------------

# Defining a Resource

``` python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.resource("runbook://crashloop")
def crashloop_runbook() -> str:
    """Runbook for debugging CrashLoopBackOff."""
    return "Check kubectl describe pod and kubectl logs --previous."
```

Verified directly: a client connecting to a server with this resource
correctly lists it (`runbook://crashloop`) and correctly reads back the
exact string returned by the function.

## Tools vs. Resources: The Actual Distinction

  Tool                                     Resource
  ------------------------------------------ --------------------------------------
  The model *decides* to call it, with arguments | The client/host reads it, often to provide context upfront
  Can have side effects (restart a service)   Meant to be read-only, data-oriented
  Identified by a name                           Identified by a URI (`runbook://crashloop`)
  Analogous to module 02 ch. 14's tool calling    Analogous to module 02 ch. 08's context injection

**Platform analogy:** this is the same distinction as an RPC call
versus a `GET` request in a REST API — a tool *does something* (or
computes something specific to the arguments given), a resource
*is something* you fetch, identified by a stable address. Use a tool
when the model needs to decide, with specific arguments, that an action
should happen; use a resource for data that's simply there to be read.

## Resources Can Be Dynamic, Not Just Static Strings

``` python
@mcp.resource("incidents://recent")
def recent_incidents() -> str:
    """The 5 most recent incident summaries."""
    # a real implementation would query your actual incident database
    return "\n".join([
        "INC-2345: checkout service 500s, resolved via rollback",
        "INC-2346: disk full on db-primary-02, resolved via cleanup",
    ])
```

A resource function runs fresh on every read — it's not a static file,
it's a function, so it can reflect live state the same way a tool call
can, just without arguments shaping what comes back.

## Resource URIs Can Take Parameters

``` python
@mcp.resource("runbook://{topic}")
def get_runbook(topic: str) -> str:
    """Get the runbook for a specific topic."""
    runbooks = {
        "crashloop": "Check kubectl describe pod and logs --previous.",
        "disk-full": "Check for oversized log files before resizing.",
    }
    return runbooks.get(topic, f"No runbook found for topic: {topic}")
```

This is a **resource template** — the client can request
`runbook://crashloop` or `runbook://disk-full` against the same
function, with `{topic}` filled in from the URI. `list_resource_templates()`
is how a client discovers these parameterized resources exist,
distinct from `list_resources()` for fixed ones.

## Hands-on: Read a Resource for Real

Using the server from earlier in this chapter, chapter 09's client
pattern applies directly:

``` python
resources = await session.list_resources()
print([str(r.uri) for r in resources.resources])  # verified: ['runbook://crashloop']

content = await session.read_resource("runbook://crashloop")
print(content.contents[0].text)  # verified: the exact runbook text
```

## Common Misconceptions

❌ Resources and tools are interchangeable — just two names for the
same thing.
(A tool is called with arguments and can have side effects; a resource
is read, meant to be data-oriented, and identified by a stable URI —
different roles, verified by their distinct SDK decorators and client
methods.)

❌ A resource always returns the same static content.
(Like a tool, a resource function runs fresh on every read — it can
reflect live state, exactly as demonstrated by the dynamic
`recent_incidents` example above.)

✔ Choose a resource when the model/client just needs to *read*
something to gain context; choose a tool when the model needs to
*decide*, with specific arguments, that something should happen.

## Interview Questions

1.  What's the practical difference between a tool and a resource?
2.  How is choosing between a tool and a resource similar to choosing
    between an RPC call and a REST `GET` request?
3.  What is a resource template, and what problem does it solve?
4.  Can a resource reflect live, changing data, or only static
    content?

## Summary

Resources are MCP's standardized version of context injection (module
02 chapter 08) — read-only, URI-addressed data a client can fetch,
distinct from tools (which the model calls with arguments to trigger an
action or computation). Both can be dynamic; the real distinction is
who initiates the interaction and whether it's meant to have a side
effect.

## Next Chapter

➡️ `07-Prompts.md`
