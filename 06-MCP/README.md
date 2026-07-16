# 06 - Model Context Protocol (MCP)

> The standardized wiring between a model and the tools/data it's
> allowed to touch.

## Overview

Module 02 chapter 14 built tool calling by hand: define a JSON schema,
let the model request a call, execute it yourself, feed the result
back. That pattern works, but it's bespoke to whatever model API
you're using — a tool built for one model's function-calling format
doesn't automatically work with another's.

MCP standardizes that wiring. It's a protocol — client, server,
transport, and a small set of primitives (tools, resources, prompts)
— so a tool or data source gets built **once**, as an MCP server, and
any MCP-compatible client (Claude Desktop, an IDE, or a script you
write) can connect to it without custom integration code per tool.

Everything in this module runs **entirely locally**: a real MCP server
you build and run as a plain Python process, a real MCP client
connecting to it over stdio, and — where a model is actually needed —
a local Ollama model, bridged to the MCP server's tools using the exact
pattern verified in this module's examples. No hosted API, no signup.

## Learning Objectives

After completing this module you will be able to:

-   Explain what problem MCP solves that ad hoc tool calling doesn't.
-   Describe MCP's client-host-server architecture and its transports.
-   Build a real MCP server exposing tools, resources, and prompts.
-   Build a real MCP client that connects to a server and calls its
    capabilities.
-   Bridge an MCP server's tools to a model's native tool-calling API.
-   Apply the same security discipline from module 02 chapter 15 to
    MCP's specific attack surface.

## Prerequisites

-   [02-Prompt-Engineering](../02-Prompt-Engineering/) — specifically
    chapter 14 (Function and Tool-Calling Prompts) and chapter 15
    (Prompt Injection and Security). This module assumes you understand
    the underlying tool-calling loop; MCP is a standardized way to wire
    it up, not a new concept from scratch.

## Repository Structure

``` text
docs/
examples/
notebooks/
```

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What Is MCP and Why It Exists
  02        Architecture: Host, Client, and Server
  03        MCP vs. Hand-Rolled Tool Calling
  04        Transports: stdio and HTTP
  05        Tools
  06        Resources
  07        Prompts
  08        Building a Minimal MCP Server
  09        Building an MCP Client
  10        Bridging MCP to a Model's Tool-Calling API
  11        Schema Design for MCP Tools
  12        Error Handling in MCP Tools
  13        Authentication and Authorization
  14        Security: MCP's Attack Surface
  15        Sampling: Servers Requesting Completions
  16        Discovery: Listing Capabilities
  17        Testing an MCP Server
  18        Best Practices
  19        Interview Questions
  20        Glossary

## Learning Roadmap

``` text
Vector Databases
        ↓
RAG
        ↓
Model Context Protocol      ← you are here
        ↓
AI Agents
```

## Hands-on Labs

-   Build an MCP server exposing a tool, a resource, and a prompt.
-   Build an MCP client that lists and calls a server's capabilities.
-   Bridge an MCP server's tools into a local Ollama model's
    tool-calling loop and watch it choose and call a real tool.
-   Design a tool schema defensively, the way module 02 chapter 09
    recommends for any prompt-facing interface.
-   Attempt a prompt injection through a malicious MCP resource, then
    defend against it.
-   Use the MCP Inspector to explore a running server without writing
    a client.

## Technologies

-   Python
-   `mcp` (the official Model Context Protocol SDK)
-   Ollama (`llama3.1:8b`, for the model-bridging examples)
-   Jupyter

## Expected Outcome

You will be able to build, run, and connect to a real MCP server —
understanding exactly what's standardized versus what you still have to
design yourself (schemas, error handling, security) — before moving on
to AI Agents, where MCP servers become the standardized tool layer an
autonomous agent reasons over.

## Next Module

➡️ `07-AI-Agents`
