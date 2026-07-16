# 07 - Prompts

## Introduction

The third MCP primitive is the standardized version of module 02
chapter 07's prompt templates — instead of a template file living
inside one application's codebase, a server can expose it so any
connected client can use the same, versioned template. Verified
directly: a real prompt, defined on a server, correctly listed and
rendered by a real client.

## Learning Objectives

After this chapter I should be able to:

-   Define an MCP prompt with the `@mcp.prompt()` decorator.
-   Explain what an MCP prompt actually returns to the client.
-   Explain why sharing prompts via a server matters for consistency.

------------------------------------------------------------------------

# Defining a Prompt

``` python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.prompt()
def incident_summary(log_text: str) -> str:
    """Build a prompt that summarizes an incident log."""
    return f"Summarize this incident log in 2 sentences:\n{log_text}"
```

Verified directly: a client calling `get_prompt("incident_summary",
{"log_text": "pod crashed 3 times"})` receives back a fully rendered
message — `"Summarize this incident log in 2 sentences:\npod crashed 3
times"` — ready to send to whatever model the host is using.

## What Actually Comes Back

An MCP prompt doesn't return raw text — it returns a list of
role-tagged messages, matching module 02 chapter 02's message-role
anatomy (system/user/assistant):

``` python
prompt_result = await session.get_prompt("incident_summary", {"log_text": "..."})
for message in prompt_result.messages:
    print(message.role, message.content.text)
# verified output includes a "user" role message with the rendered text
```

This means an MCP prompt can define a whole multi-message exchange —
including a system message, or a few-shot example (module 02 chapter
03) — not just a single string, if the server author wants to encode
that structure.

## Why This Matters for Consistency

Module 02 chapter 17 covered prompt versioning — treating prompt files
like code, one source of truth, never edited in place. An MCP prompt
exposed from a server is that same discipline, now shared across every
client that connects: update the prompt on the server, and every
application using it picks up the change, instead of each application
maintaining its own copy that can silently drift out of sync.

**Platform analogy:** this is a shared library versus copy-pasted code
— the same problem module 02 chapter 07 solved by moving prompts into
files instead of inline strings, extended one level further: now the
"file" is centrally served instead of locally copied into every
consuming application.

## Hands-on: List and Render a Real Prompt

``` python
prompts = await session.list_prompts()
print([p.name for p in prompts.prompts])  # verified: ['incident_summary']

result = await session.get_prompt("incident_summary", {"log_text": "database connection pool exhausted"})
print(result.messages[0].content.text)
```

Try changing the `log_text` argument and confirm the rendered message
updates accordingly — the server is doing real template rendering
(Jinja2-style variable substitution, per module 02 chapter 07), not
just returning static text.

## Common Misconceptions

❌ MCP prompts are just a way to store a static string on a server.
(They're rendered templates that accept arguments and return structured,
role-tagged messages — verified directly, not just a text file lookup.)

❌ Prompts, tools, and resources all serve the same purpose.
(Each has a distinct role: tools trigger actions, resources expose
data, prompts standardize reusable interaction templates — the three
map directly onto module 02's tool calling, context injection, and
templating chapters respectively.)

✔ Exposing a prompt via an MCP server extends module 02 chapter 17's
versioning discipline across every application that connects — one
source of truth instead of copy-pasted templates per app.

## Interview Questions

1.  What does an MCP prompt actually return to the client — a string,
    or something more structured?
2.  How does an MCP prompt relate to module 02 chapter 07's templating
    concept?
3.  Why does exposing a prompt from a server help with the versioning
    problem covered in module 02 chapter 17?
4.  Can an MCP prompt define a multi-message exchange, or only a
    single message?

## Summary

MCP prompts are server-defined, parameterized templates that return
structured, role-tagged messages — the shared-library version of module
02's prompt templating, letting every connected client use the same,
centrally-updated prompt instead of maintaining separate copies.
Verified directly: a real prompt rendered correctly with real argument
substitution.

## Next Chapter

➡️ `08-Building-a-Minimal-MCP-Server.md`
