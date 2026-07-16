# 13 - Authentication and Authorization

## Introduction

Every example so far ran locally, over `stdio`, with no concept of
"who is calling." The moment a server moves to an HTTP transport
(chapter 04) or exposes anything sensitive, that stops being fine —
this chapter covers the two distinct questions any real deployment
needs answered: who is this, and what are they allowed to do.

## Learning Objectives

After this chapter I should be able to:

-   Distinguish authentication from authorization in an MCP context.
-   Explain why `stdio` servers get authentication "for free" and HTTP
    servers don't.
-   Design tool-level authorization instead of all-or-nothing server
    access.

------------------------------------------------------------------------

# Two Different Questions

``` text
Authentication:  WHO is calling this server?
Authorization:    WHAT is this caller allowed to do?
```

A `stdio` server (every example in this module) gets authentication
essentially for free — the client spawned the server as its own
subprocess, so "who is calling" is trivially "whoever is running this
process," inheriting the OS-level permissions of that process. An
HTTP-based server (chapter 04) has no such guarantee — any client that
can reach the port can attempt to connect, so authentication has to be
handled explicitly.

## Why This Matters More as Soon as You Leave `stdio`

**Platform analogy:** this is the exact same jump as moving from a
script that only you run locally to a service other people's clients
can call over the network — the trust boundary that used to be
implicit (only you can run your own local script) becomes something
that has to be explicitly enforced (anyone who can reach the port needs
to be checked).

`FastMCP` supports token-based authentication and OAuth-style provider
integration for HTTP-based transports — the specific mechanism matters
less here than the underlying principle: **the moment a server is
network-reachable, "which client is this" needs an actual answer, not
an assumption.**

## Authorization: Not Every Caller Should Get Every Tool

Authentication answers "who," but a server with multiple tools of
varying sensitivity still needs a second layer — not every
authenticated caller should be able to call every tool.

``` python
ALLOWED_TOOLS_BY_ROLE = {
    "readonly": {"get_disk_usage", "list_incidents"},
    "operator": {"get_disk_usage", "list_incidents", "restart_service"},
}

def check_authorized(caller_role: str, tool_name: str) -> bool:
    return tool_name in ALLOWED_TOOLS_BY_ROLE.get(caller_role, set())

@mcp.tool()
def restart_service(service_name: str, environment: str, caller_role: str = "readonly") -> dict:
    """Restart a named service. Requires operator role."""
    if not check_authorized(caller_role, "restart_service"):
        return {"error": True, "retryable": False, "message": "Not authorized for this operation."}
    ...
```

This is module 04 chapter 12's multi-tenancy access-control pattern,
applied to tool access instead of vector-search results — the same
principle: the check has to be centralized and structurally enforced,
never left as a convention every tool author independently remembers
to implement.

## The Model Is Never the Authorization Boundary

This is worth stating as plainly as module 02 chapter 15 and module 06
chapter 12 both already established: **a prompt instruction telling
the model "don't restart production services" is not a security
control.** The actual boundary has to live in the tool's own code (as
above) or in the server's request-handling layer — never solely in
what the model has been told to do or not do.

## Hands-on: Add a Role Check to a Tool

Take chapter 08's `get_disk_usage` tool and add a second, more
sensitive tool (`restart_service`, using the pattern above). Call both
with `caller_role="readonly"` and confirm the sensitive one correctly
refuses while the read-only one still works — this is the same "flag
for review, never blindly execute" discipline from module 01 chapter
18, now enforced at the authorization layer instead of just at the
execution layer.

## Common Misconceptions

❌ A `stdio` server needs the same authentication mechanism as an HTTP
server.
(It gets a form of authentication for free from process ownership —
explicit authentication mechanisms matter specifically once a server
becomes network-reachable.)

❌ Authentication (who's calling) is sufficient security for a
multi-tool server.
(Authorization — what a specific authenticated caller can actually do
— is a separate, equally necessary layer, especially when tools vary
in sensitivity.)

✔ Telling a model not to call a sensitive tool via a prompt instruction
is guidance, not enforcement — the actual boundary must live in code
the model cannot talk its way around.

## Interview Questions

1.  What's the difference between authentication and authorization in
    an MCP context?
2.  Why does a `stdio` server get authentication largely "for free,"
    while an HTTP server doesn't?
3.  Why isn't a prompt instruction like "don't restart production" a
    real security control?
4.  How would you design tool-level authorization for a server with
    tools of varying sensitivity?

## Summary

Authentication (who's calling) and authorization (what they can do)
are two distinct concerns — `stdio` servers inherit authentication from
process ownership, while HTTP-based servers need it handled explicitly,
and any server with tools of varying sensitivity needs a real
authorization layer on top, enforced in code rather than left to a
prompt instruction the model could be talked out of.

## Next Chapter

➡️ `14-Security-MCPs-Attack-Surface.md`
