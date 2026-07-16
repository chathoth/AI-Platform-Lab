# 20 - Glossary

## Introduction

Every term from this module, alphabetical, defined the way I actually
think about it, with the analogy that made it stick attached.

------------------------------------------------------------------------

**Client** — The component inside a host that manages one connection
to one server; always paired 1:1 with a server. See
[02-Architecture-Host-Client-Server.md](02-Architecture-Host-Client-Server.md).

**Discovery** — The runtime process of a client asking a server what
it offers (`list_tools()`, `list_resources()`, `list_prompts()`)
instead of having that knowledge hardcoded in advance. See
[16-Discovery-Listing-Capabilities.md](16-Discovery-Listing-Capabilities.md).

**FastMCP** — The high-level Python class (`mcp.server.fastmcp.FastMCP`)
used to build an MCP server with decorator-based tool/resource/prompt
registration. See
[08-Building-a-Minimal-MCP-Server.md](08-Building-a-Minimal-MCP-Server.md).

**Host** — The user-facing application (a chat app, an IDE, a script)
that owns the overall session and talks to the LLM. See
[02-Architecture-Host-Client-Server.md](02-Architecture-Host-Client-Server.md).

**MCP (Model Context Protocol)** — A protocol standardizing how a
model-hosting application connects to tools and data sources, so a
tool built once works with any compliant client. See
[01-What-Is-MCP-and-Why-It-Exists.md](01-What-Is-MCP-and-Why-It-Exists.md).

**MCP Inspector** — A browser-based tool for interactively exploring a
running MCP server's tools, resources, and prompts without writing a
client. See
[17-Testing-an-MCP-Server.md](17-Testing-an-MCP-Server.md).

**Prompt (MCP)** — A server-defined, parameterized template that
returns structured, role-tagged messages, shareable across every
connected client. See [07-Prompts.md](07-Prompts.md).

**Resource** — Read-only, URI-addressed data a client can fetch from a
server — the standardized version of context injection. See
[06-Resources.md](06-Resources.md).

**Resource Template** — A parameterized resource URI (e.g.
`runbook://{topic}`) whose specific instances aren't enumerable ahead
of time, discovered via `list_resource_templates()`. See
[06-Resources.md](06-Resources.md) and
[16-Discovery-Listing-Capabilities.md](16-Discovery-Listing-Capabilities.md).

**Sampling** — A mechanism letting a server request that the client run
an LLM completion on its behalf, via `create_message()` and a client-
side `sampling_callback`. See
[15-Sampling-Servers-Requesting-Completions.md](15-Sampling-Servers-Requesting-Completions.md).

**Server** — The component exposing tools, resources, and prompts —
built once, independent of any specific model. See
[01-What-Is-MCP-and-Why-It-Exists.md](01-What-Is-MCP-and-Why-It-Exists.md).

**`stdio` Transport** — A transport where the client spawns the server
as a local subprocess and communicates over its stdin/stdout, with no
network involved. See
[04-Transports-stdio-and-HTTP.md](04-Transports-stdio-and-HTTP.md).

**Tool** — A function the model can request to have executed, with
arguments; MCP's standardized version of function/tool calling. See
[05-Tools.md](05-Tools.md).

**Tool Poisoning** — An injection attempt hidden inside a tool's
description field, read by the model on every request regardless of
whether that tool is ever called. See
[14-Security-MCPs-Attack-Surface.md](14-Security-MCPs-Attack-Surface.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **06-MCP**. Next up per the
[root README](../../README.md) roadmap:

➡️ `07-AI-Agents`
