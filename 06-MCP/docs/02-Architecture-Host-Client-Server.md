# 02 - Architecture: Host, Client, and Server

## Introduction

Chapter 01 named the three architectural pieces. This chapter is about
how they actually relate to each other at runtime — specifically the
one-client-per-server rule that trips people up the first time they
try to connect one application to multiple tool sources.

## Learning Objectives

After this chapter I should be able to:

-   Explain the relationship between a host, a client, and a server.
-   Explain why a host with multiple servers needs multiple clients.
-   Trace a single request through all three layers.

------------------------------------------------------------------------

# The Three Layers, Precisely

``` text
Host        - the user-facing application (a chat app, an IDE, a
               script). Owns the overall session and talks to the LLM.
  Client 1  - manages ONE connection to ONE server
  Client 2  - manages ONE connection to a DIFFERENT server
Server A     - exposes tools/resources/prompts for, say, Kubernetes
Server B      - exposes tools/resources/prompts for, say, incident tickets
```

**A client is always paired 1:1 with a server.** A host that needs to
talk to three different tool sources runs three clients, each with its
own connection — there's no single client that fans out to multiple
servers.

**Platform analogy:** this is a connection pool with one connection per
backend service, not one shared connection multiplexing everything —
each client-server pair is its own isolated channel, with its own
capabilities, its own security boundary (chapter 14), and its own
lifecycle.

## Tracing One Request Through All Three Layers

``` text
1. User asks the host application a question
2. Host decides (with the LLM's help) that a tool is needed
3. Host's client sends a "call this tool" message to the server
4. Server executes the tool, returns a result
5. Host's client receives the result
6. Host feeds the result back to the LLM to produce a final answer
```

This is exactly the loop module 02 chapter 14 built by hand — MCP adds
the standardized client-server messaging in steps 3-5, replacing
whatever bespoke code you'd have otherwise written for one specific
model's tool-calling format.

## Where the Actual LLM Call Happens

This is worth stating precisely, because it's a common point of
confusion: **the LLM call itself is not part of MCP.** MCP governs how
the host's client talks to servers — deciding *when* to call a tool and
actually calling the model are the host application's job, using
whatever model API it chooses. Chapter 10 verifies this directly by
bridging an MCP server's tools into a completely separate local Ollama
call.

## Hands-on: Identify the Layers in Code You'll Write

Chapters 08-10 build all three layers as real, runnable code:

``` text
Server  (chapter 08)  - a Python process exposing a get_disk_usage tool
Client  (chapter 09)  - a Python script that connects to that server
                          over stdio and calls its tools directly
Host     (chapter 10)  - the same client, now also calling a local
                           Ollama model and feeding it the server's
                           tool results
```

Notice the host and client aren't always separate files in a small
example — in a minimal script, the "host" logic (talking to the LLM)
and the "client" logic (talking to the MCP server) can live in the same
process, which is exactly what chapter 10's verified example does.

## Common Misconceptions

❌ One client can connect to multiple servers.
(Each client manages exactly one server connection — a host needing
multiple tool sources runs multiple clients, one per server.)

❌ MCP handles the actual call to the language model.
(MCP governs host-to-server communication only — the LLM call is the
host application's responsibility, using whatever model API it
chooses, verified directly in chapter 10 with a local Ollama model.)

✔ Host, client, and server are three distinct architectural roles, even
when — as in a small script — some of them end up implemented in the
same file.

## Interview Questions

1.  What's the relationship between a client and a server in MCP?
2.  Why does a host needing three different tool sources run three
    clients instead of one?
3.  Is the LLM call itself part of the MCP protocol? Why or why not?
4.  Walk through the six steps a single tool-calling request takes
    through the host-client-server architecture.

## Summary

A host owns the overall session and runs one client per server it
needs to talk to — each client-server pair is an isolated connection
with its own capabilities and security boundary. The actual LLM call
sits outside MCP entirely, in the host application's own code, which
is exactly why an MCP server built once can be bridged to any model,
local or hosted, without changes.

## Next Chapter

➡️ `03-MCP-vs-Hand-Rolled-Tool-Calling.md`
