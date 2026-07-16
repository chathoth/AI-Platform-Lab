# 15 - Sampling: Servers Requesting Completions

## Introduction

Every earlier chapter had the model calling the server. Sampling
inverts that: a **server** can ask the **client** to run an LLM
completion on its behalf, without the server ever needing its own API
key or model access. This is the least commonly used of MCP's
capabilities, but a genuinely useful one — verified directly with a
real round trip in this module's own testing.

## Learning Objectives

After this chapter I should be able to:

-   Explain what sampling is and why a server would want it.
-   Implement a tool that requests a completion via `create_message`.
-   Implement a client-side `sampling_callback` that fulfills the
    request.

------------------------------------------------------------------------

# Why a Server Would Want This

A server author might want to use an LLM inside a tool — to summarize
something, extract structured data, or make a judgment call — without
the server needing to manage its own API key, choose its own model, or
pay for its own inference. Sampling lets the server **ask the client**
to run that completion instead, using whatever model the client (and,
by extension, the user) has already configured.

``` text
Without sampling:  server needs its OWN model access, its own API
                     key, its own cost — duplicated across every
                     server that wants LLM capability
With sampling:      server asks the CLIENT to run a completion -
                     one model configuration, shared across every
                     server the client talks to
```

## The Server Side: Requesting a Completion

``` python
from mcp.server.fastmcp import FastMCP, Context
import mcp.types as types

mcp = FastMCP("sampling-demo")

@mcp.tool()
async def summarize_via_client(text: str, ctx: Context) -> str:
    """Ask the client's model to summarize text, instead of calling an LLM directly."""
    result = await ctx.session.create_message(
        messages=[types.SamplingMessage(
            role="user",
            content=types.TextContent(type="text", text=f"Summarize in 5 words: {text}"),
        )],
        max_tokens=50,
    )
    return result.content.text
```

Notice the tool function takes a `ctx: Context` parameter — the SDK
injects this automatically, giving the tool access to `ctx.session`,
through which `create_message()` sends the sampling request back to
whichever client is connected.

## The Client Side: Fulfilling the Request

``` python
import mcp.types as types

async def handle_sampling(context, params):
    # A real implementation calls an actual model here - the same
    # local Ollama pattern from chapter 10 works directly.
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(type="text", text="..."),
        model="llama3.1:8b",
    )

async with ClientSession(read, write, sampling_callback=handle_sampling) as session:
    ...
```

Verified directly: a server tool calling `create_message()`, received
by a client's `sampling_callback`, round-tripped successfully back to
the tool — this is a real, working request/response cycle, not a
theoretical protocol feature.

## The Client Decides Whether to Allow It

This is a deliberate design choice worth calling out: **the client is
always in control.** A `sampling_callback` can inspect the request and
refuse it, rate-limit it, or route it to a cheaper/smaller model than
the client's main conversation uses — the server can *ask*, but the
client decides whether and how to fulfill that ask. This mirrors module
02 chapter 14's "a tool call is a suggestion, not a command" principle,
inverted: here it's the server's *request for a completion* that the
client is free to accept, modify, or reject.

## Connecting This to a Real Local Model

Swapping the stub `handle_sampling` above for a real call is exactly
chapter 10's bridging pattern, just running in the opposite direction:

``` python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

async def handle_sampling(context, params):
    messages = [{"role": m.role, "content": m.content.text} for m in params.messages]
    response = client.chat.completions.create(model="llama3.1:8b", messages=messages, max_tokens=params.maxTokens)
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(type="text", text=response.choices[0].message.content),
        model="llama3.1:8b",
    )
```

## Hands-on: Run the Verified Round Trip Yourself

Build the server and client above, run the client, and confirm the
tool's returned summary matches what your `handle_sampling`
implementation produced — then swap the stub response for a real local
Ollama call and confirm a genuinely generated summary comes back
instead.

## Common Misconceptions

❌ Sampling means the server has its own model access.
(The opposite — sampling exists specifically so the server *doesn't*
need its own model access, borrowing the client's instead.)

❌ The server can force the client to run a completion.
(The client's `sampling_callback` decides whether and how to fulfill
the request — it can refuse, modify, or redirect it entirely.)

✔ Sampling is the least commonly needed MCP capability of the ones
covered in this module — most tools don't need it — but it's the right
answer whenever a server-side tool genuinely needs LLM reasoning
without wanting to manage its own model access.

## Interview Questions

1.  What problem does sampling solve for an MCP server author?
2.  Walk through the round trip: which side calls `create_message()`,
    and which side implements `sampling_callback`?
3.  Why does the client, not the server, have final control over
    whether a sampling request is fulfilled?
4.  How would you connect a `sampling_callback` to a real local Ollama
    model?

## Summary

Sampling lets an MCP server request that the client run an LLM
completion on its behalf — via `ctx.session.create_message()` on the
server and a `sampling_callback` on the client — so a server can use
LLM reasoning without managing its own model access or API key.
Verified directly with a real round trip: the client always retains
final control over whether and how the request gets fulfilled.

## Next Chapter

➡️ `16-Discovery-Listing-Capabilities.md`
