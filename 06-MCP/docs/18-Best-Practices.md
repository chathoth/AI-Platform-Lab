# 18 - Best Practices

## Introduction

The consolidated checklist for this module, same spirit as every other
module's — each item traces back to a specific chapter, several to
something directly verified while building this module rather than
assumed.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist when building or connecting to an MCP
    server.
-   Explain the reasoning behind each item, tied to its source
    chapter.

------------------------------------------------------------------------

# The Checklist

## 1. Build Servers With No Knowledge of the Model That'll Use Them

Chapter 10. This is what makes MCP's reuse promise real — verified
directly by bridging one unmodified server to a completely separate
local model with a small adapter function.

## 2. Write Precise Type Hints and Docstrings — They Become the Schema

Chapter 05/11. There's no separate schema file to maintain, which
means the function signature and docstring *are* the entire schema
maintenance burden.

## 3. Choose the Right Primitive for the Job

Chapters 05-07. Tools for actions the model decides to trigger with
arguments; resources for read-only data; prompts for shareable,
reusable templates.

## 4. Return Structured Errors, Never Let Exceptions Propagate Raw

Chapter 12. A structured error with a `retryable` hint is something a
model can act on; a raw traceback usually isn't.

## 5. Put Safety Guards Inside the Tool, Never Only in the Prompt

Chapters 12, 13, 14. A prompt instruction is guidance a model can be
talked out of — the real boundary belongs in the tool's own code.

## 6. Choose `stdio` for Local, HTTP for Shared/Remote

Chapter 04. `stdio` needs no network security thinking at all; HTTP-
based transports need the same operational care as any other network
service.

## 7. Treat Every MCP Primitive as a Potential Injection Vector

Chapter 14. Tool results, resource content, *and* tool descriptions
themselves — the last one is genuinely MCP-specific and easy to miss.

## 8. Review a Third-Party Server's Tool Descriptions Before Connecting

Chapter 14. The model reads every connected tool's description on
every request, whether or not that tool is ever called.

## 9. Test Real Connections, Never Mock the Protocol Layer — But Watch
Fixture Scoping

Chapter 17. Spin up a real server subprocess and call it through a
real client — verified directly that a shared async-generator fixture
around `stdio_client` is unreliable; connect inside each test instead.

## 10. Use Sampling Only When a Server Genuinely Needs LLM Reasoning
Without Its Own Model Access

Chapter 15. It's the least commonly needed capability of the ones
covered here — most tools don't need it.

## Anti-Patterns to Avoid

-   **Vague, single-word tool names and one-line descriptions** —
    chapters 05, 11.
-   **A `dict` parameter where named, typed fields would work** —
    chapter 11.
-   **Connecting a client with destructive-tool access to an
    unverified third-party server** — chapter 14.
-   **Relying on a prompt instruction as the only defense against a
    destructive tool call** — chapters 12, 13, 14.
-   **A shared async pytest fixture wrapping `stdio_client`** — chapter
    17, a real, verified pitfall, not a hypothetical one.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as every other module: create an `mcp-checklist.md` with
these 10 items as literal checkboxes, and walk through it before
building or connecting to any MCP server for real.

## Common Misconceptions

❌ MCP handles security and correctness automatically, since it's a
standard protocol.
(The protocol standardizes the wiring — schema quality, error
handling, authorization, and injection defense are still entirely the
server and client authors' responsibility.)

❌ Following this checklist means an MCP integration is fully tested.
(It avoids the well-understood pitfalls covered in this module,
including the async testing gotcha found while building it — it
doesn't replace testing against your own specific tools and real
usage patterns.)

✔ Several items on this list — the model-agnostic bridge, the async
fixture pitfall, the sampling round trip — were verified directly while
building this module, not just asserted from documentation.

## Interview Questions

1.  Why does building a server with no model-specific knowledge matter
    for MCP's core value proposition?
2.  Why is a prompt instruction insufficient as the only defense
    around a destructive tool?
3.  What real, verified pitfall exists with shared async pytest
    fixtures and `stdio_client`?
4.  Why is tool description review part of the security checklist, not
    just a documentation nicety?

## Summary

Every practice in this checklist maps to a chapter's failure mode or a
directly verified result: model-agnostic server design, precise schema
authorship, structured error handling, code-level safety guards, and
careful async test construction. Together they're what separates an
MCP integration that works in a demo from one that's safe to depend on.

## Next Chapter

➡️ `19-Interview-Questions.md`
