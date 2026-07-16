# 04 - Transports: stdio and HTTP

## Introduction

Before building a real server, one decision needs to be made: how does
the client actually talk to it? MCP supports more than one transport,
and the choice has real operational consequences — this chapter is
verified against the `stdio` transport specifically, since that's what
every runnable example in this module uses.

## Learning Objectives

After this chapter I should be able to:

-   Explain what a transport is in MCP's architecture.
-   Compare `stdio` and HTTP-based transports.
-   Choose the right transport for a given deployment shape.

------------------------------------------------------------------------

# What a Transport Actually Is

The transport is how JSON-RPC messages physically move between client
and server — MCP defines the message format; the transport defines the
pipe those messages travel through.

## `stdio`: The Local, Process-Based Transport

``` python
# server side (chapter 08)
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

``` python
# client side (chapter 09) - the client SPAWNS the server as a
# subprocess and talks to it over its stdin/stdout
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command="python3", args=["server.py"])
async with stdio_client(params) as (read, write):
    ...
```

The client launches the server process directly and communicates over
standard input/output — no network, no port, no separate deployment.
This is what every example in this module uses, verified directly:
`stdio_client` spawning the server subprocess and exchanging real
messages over its stdin/stdout.

**Platform analogy:** this is exactly how a CLI tool pipes into
another (`cmd1 | cmd2`) — one process's stdout is the next process's
stdin. `stdio` transport is that same pattern, formalized for MCP's
JSON-RPC messages, and it only works when the client can spawn the
server as a local subprocess.

## HTTP-Based Transports: Remote, Network-Accessible

For a server that needs to run separately from its clients — a shared
team resource, or something running in a different environment
entirely — MCP supports HTTP-based transports (including
Server-Sent Events for streaming). The server runs as a standalone
process listening on a port; clients connect over the network instead
of spawning it directly.

``` python
# server side, HTTP instead of stdio
if __name__ == "__main__":
    mcp.run(transport="streamable-http")  # listens on a port instead
```

## Choosing Between Them

  Factor                          `stdio`                              HTTP-based
  ---------------------------------- -------------------------------------- --------------------------------------
  Deployment                            Client spawns server as a subprocess    Server runs independently, clients connect over network
  Best for                               Local tools, single-user setups          Shared tools, multiple simultaneous clients
  Network exposure                        None - no port opened at all              A real network service, needs the same care as any other (chapter 13, 14)
  Setup complexity                          Minimal - this module's entire setup      Requires running and exposing a service

For this module — and for most personal/learning setups — `stdio` is
the right choice: no port to secure, no separate deployment, and it's
what every verified example here uses. A shared, team-wide MCP server
would reasonably choose an HTTP-based transport instead.

## Hands-on: Confirm the Subprocess Relationship Directly

``` python
import subprocess

# this is conceptually what stdio_client does under the hood -
# spawn the server, get handles to its stdin/stdout
process = subprocess.Popen(
    ["python3", "-c", "print('a server would speak JSON-RPC here')"],
    stdout=subprocess.PIPE,
)
print(process.stdout.read())
```

Chapter 09 does this for real, through the actual `mcp` SDK rather than
raw `subprocess` — this is just to make the underlying mechanism
visible before treating `stdio_client` as a black box.

## Common Misconceptions

❌ `stdio` transport requires a network connection.
(It uses no network at all — the client spawns the server as a local
subprocess and communicates over standard input/output directly.)

❌ HTTP-based transport is strictly "better" than `stdio`.
(It solves a different problem — shared, remote access — at the cost
of needing to run and secure an actual network service. `stdio` is
simpler and sufficient for local, single-user tooling.)

✔ Transport choice is a deployment decision, not a capability
difference — the same tools, resources, and prompts work over either
transport; only how the client reaches the server changes.

## Interview Questions

1.  What does a transport handle in MCP's architecture?
2.  How does the `stdio` transport work, mechanically?
3.  When would you choose an HTTP-based transport over `stdio`?
4.  Why does `stdio` transport not require any network security
    considerations that HTTP-based transport would?

## Summary

The transport is the pipe MCP's JSON-RPC messages travel through —
`stdio` spawns the server as a local subprocess with no network
involved, verified as the mechanism behind every example in this
module; HTTP-based transports let a server run independently and serve
multiple remote clients, at the cost of needing to operate and secure
a real network service.

## Next Chapter

➡️ `05-Tools.md`
