# 19 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with
the answer framed the way I'd actually say it. Review material — read
the chapters first.

------------------------------------------------------------------------

## Chapter 01 - What Is MCP and Why It Exists

**Q: What integration problem does MCP solve?**
Without it, connecting N tools to M models means N×M custom
integrations. MCP standardizes the wiring so a tool built once, as a
server, works with any compliant client regardless of which model sits
behind it.

## Chapter 02 - Architecture: Host, Client, and Server

**Q: Is the LLM call part of the MCP protocol?**
No — MCP governs host-to-server communication. The actual model call
is the host application's own responsibility, verified directly by
bridging an MCP server's tools to a local Ollama model with a small,
separate adapter function.

## Chapter 03 - MCP vs. Hand-Rolled Tool Calling

**Q: What's the deciding question for choosing MCP over a simpler
in-process function call?**
Whether more than one application or model plausibly needs the same
tool — reuse is what MCP's extra moving parts (a server process, a
transport) actually buy you.

## Chapter 04 - Transports: stdio and HTTP

**Q: Why does `stdio` transport need no network security thinking?**
The client spawns the server as a local subprocess and talks to it
over stdin/stdout — no port is ever opened, so there's no network
attack surface to secure in the first place.

## Chapter 05 - Tools

**Q: How does the `mcp` SDK derive a tool's schema?**
From the function's type hints and docstring, automatically — verified
by inspecting a running server's `list_tools()` output and confirming
it matched the function signature exactly.

## Chapter 06 - Resources

**Q: What's the practical difference between a tool and a resource?**
A tool is called with arguments and can have side effects; a resource
is read, meant to be data-oriented, and identified by a stable URI —
the same distinction as an RPC call versus a REST `GET`.

## Chapter 07 - Prompts

**Q: What does an MCP prompt actually return?**
A list of structured, role-tagged messages — not a raw string —
verified directly by rendering a prompt with a real argument and
inspecting the returned message content.

## Chapter 08 - Building a Minimal MCP Server

**Q: Why does a correctly-running `stdio` server appear to hang with
no output?**
It's blocked waiting on stdin for a client to connect — expected
behavior, not a bug. You verify it's working by connecting a client
(chapter 09), not by watching for console output.

## Chapter 09 - Building an MCP Client

**Q: Does the client connect to an already-running server?**
No — with `stdio_client`, the client spawns the server itself as a
subprocess via `StdioServerParameters`; there's no separately-running
server to connect to beforehand.

## Chapter 10 - Bridging MCP to a Model's Tool-Calling API

**Q: Why does the server file need zero changes to work with a
different model?**
It was written with no model-specific knowledge at all — verified
directly: the same unmodified server from chapter 08 was successfully
called by a local Ollama model through a small, separate bridging
function.

## Chapter 11 - Schema Design for MCP Tools

**Q: Why does a `dict` parameter produce a weaker tool schema than
named, typed parameters?**
A `dict` gives the model no structural guidance about expected keys —
named parameters (or a Pydantic model with field descriptions) produce
a schema that actually constrains the model toward a correct call.

## Chapter 12 - Error Handling in MCP Tools

**Q: Why is a structured error response more useful to a model than a
raw exception message?**
It gives the model something actionable — like a list of valid
values — rather than an opaque stack trace it has no way to act on.

## Chapter 13 - Authentication and Authorization

**Q: Why isn't a prompt instruction like "don't restart production" a
real security control?**
It's guidance a model can be talked out of — the actual boundary has
to live in code (a guard clause, an authorization check) that the
model cannot override through conversation.

## Chapter 14 - Security: MCP's Attack Surface

**Q: What's tool poisoning, and why is it a vector specific to MCP?**
An injection attempt hidden inside a tool's *description* field — the
model reads every connected tool's description on every request,
regardless of whether that tool is ever called, which is a risk
distinct from module 02's document/result-focused injection guidance.

## Chapter 15 - Sampling: Servers Requesting Completions

**Q: Who has final control over whether a sampling request is
fulfilled — the server or the client?**
The client, via its `sampling_callback` — verified directly: the
server can only *ask* for a completion; the client's callback decides
whether and how to actually provide one.

## Chapter 16 - Discovery: Listing Capabilities

**Q: Why does runtime discovery matter for MCP's model-agnostic goal?**
It's what lets a generic client (or bridging code) work with any
server's capabilities without being hardcoded to one specific server in
advance — verified as the exact mechanism chapter 10's bridge relies
on.

## Chapter 17 - Testing an MCP Server

**Q: What real, verified pitfall exists with async pytest fixtures and
MCP?**
A shared async-generator fixture wrapping `stdio_client` produces
intermittent cancel-scope teardown errors across pytest-asyncio's task
boundaries — connecting inside each test individually is more
repetitive but reliably passes clean.

## Chapter 18 - Best Practices

**Q: Which items on this checklist were verified directly rather than
just asserted?**
The model-agnostic server-to-model bridge (chapter 10), the sampling
round trip (chapter 15), and the async fixture testing pitfall
(chapter 17) — all confirmed by actually running the code, not just
described.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  MCP — a protocol standardizing how a model-hosting app connects to
    tools and data.
2.  Host/client/server — one client per server, always 1:1.
3.  Transport — `stdio` for local/no-network, HTTP for shared/remote.
4.  Tools — model-called, can have side effects, schema auto-derived.
5.  Resources — read-only, URI-addressed data.
6.  Prompts — server-shared, parameterized, structured message
    templates.
7.  Schema quality — entirely a function of type hints and docstrings.
8.  Error handling — structured, retryable-or-not, never a raw
    traceback.
9.  Security boundary — lives in code, never in a prompt instruction
    alone.
10. Tool poisoning — injection hidden in a tool's description field.
11. Sampling — server asks, client's callback decides.
12. Discovery — `list_tools()`/`list_resources()`/`list_prompts()`,
    what makes a client generic.
13. Testing — real connections, watch for async fixture scoping
    issues.

## Next Chapter

➡️ `20-Glossary.md`
