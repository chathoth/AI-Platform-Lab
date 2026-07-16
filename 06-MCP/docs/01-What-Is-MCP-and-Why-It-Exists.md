# 01 - What Is MCP and Why It Exists

## Introduction

Module 02 chapter 14 built a working tool-calling loop by hand: define
a schema, let the model request a call, execute it, feed the result
back. That pattern works — but it's specific to one model's function-
calling format, wired up inside one application. MCP (Model Context
Protocol) is what happens when that pattern gets standardized into a
real protocol, so the tool and the model don't have to be built
together.

## Learning Objectives

After this chapter I should be able to:

-   Explain the integration problem MCP solves.
-   Describe MCP in one sentence a colleague would understand.
-   Name the three core things an MCP server can expose.

------------------------------------------------------------------------

# The Problem: N Tools × M Models = N×M Integrations

Before a standard protocol, connecting *your* internal tools (a
runbook lookup, a deployment status check, an incident database query)
to *an* LLM meant writing custom integration code specific to that
model's tool-calling API. Want to swap models, or expose the same tool
to a second application? Rewrite the integration.

``` text
Without a standard:
  Tool A -- custom code --> Model 1
  Tool A -- custom code --> Model 2      (rewritten, again)
  Tool B -- custom code --> Model 1      (rewritten, again)
  Tool B -- custom code --> Model 2      (rewritten, again)

With MCP:
  Tool A --> MCP server --> any MCP client --> any model behind it
  Tool B --> MCP server --> any MCP client --> any model behind it
```

**Platform analogy:** this is exactly the problem a standard API
protocol (like REST, or gRPC) solves for services talking to each
other — before a shared convention, every client had to know every
server's bespoke interface. MCP is that shared convention, specifically
for "a model needs to call a tool or read some data."

## What MCP Actually Is

MCP is a protocol (JSON-RPC based) with three parts:

``` text
Host    - the application a user interacts with (an IDE, a chat app,
           a script you write)
Client   - lives inside the host, holds one connection to one server
Server    - exposes capabilities: tools, resources, and prompts
```

A server is built **once**, independent of any specific model. Any
host that speaks MCP can connect to it — this module verified that
directly: the same server built in chapter 08 gets called by a plain
Python client (chapter 09) and by a local Ollama model bridged through
that client (chapter 10), with zero changes to the server itself.

## The Three Things a Server Can Expose

  Primitive     What it is                          Chapter
  ------------- ------------------------------------- ---------
  Tools          Functions the model can call            05
  Resources       Data the model/client can read           06
  Prompts          Reusable prompt templates the server offers | 07

This maps directly onto concepts already covered: **Tools** are module
02 chapter 14's function calling, standardized. **Resources** are
module 02 chapter 08's context injection, standardized — a server-
exposed way to hand data to a model instead of hardcoding it into a
prompt. **Prompts** are module 02 chapter 07's templates, standardized
— shareable across any client that connects to the server.

## Hands-on: See It Work Before Building Anything

``` bash
pip install mcp openai
```

Every code example in this module was verified by actually running it
against a real local MCP server and a real local Ollama model — not
just written to look plausible. Chapter 08 walks through the exact
server used for that verification, so you'll build the same thing you
can already trust works.

## Common Misconceptions

❌ MCP is a new way to prompt a model.
(It's a protocol for connecting a model-hosting application to tools
and data — the model itself is unaware MCP exists; the host/client
translates between MCP and whatever the model's native API expects,
per chapter 10.)

❌ MCP requires using Claude specifically.
(It's model-agnostic by design — this module bridges MCP tools to a
local Ollama model with no Claude API involved at all, verified
directly.)

✔ The core value of MCP is decoupling: build a tool/data source once,
as a server, and any compliant client can use it — no per-model,
per-application rewrite required.

## Interview Questions

1.  What integration problem does MCP solve?
2.  Name the three parts of MCP's architecture.
3.  What are the three things an MCP server can expose?
4.  How does an MCP "tool" relate to the function calling covered in
    module 02?

## Summary

MCP standardizes the connection between a model-hosting application and
the tools/data it needs, solving the N-tools-times-M-models integration
problem — the same value any shared protocol brings over bespoke
per-pair integrations. A server exposes tools, resources, and prompts;
any MCP-compliant client can connect to it regardless of which model
sits behind that client.

## Next Chapter

➡️ `02-Architecture-Host-Client-Server.md`
