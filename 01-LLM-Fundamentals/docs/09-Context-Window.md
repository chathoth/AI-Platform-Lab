# 09 - Context Window

## Introduction

The context window is the resource limit that has burned me the most in
practice — the LLM equivalent of a memory limit on a container. Hit it,
and you don't get a graceful degrade by default; you get a hard failure
or silent truncation. It deserves the same respect I give any hard
resource ceiling in production.

## Learning Objectives

After this chapter I should be able to:

-   Define the context window and what counts against it.
-   Explain why context windows have limits at all (tying back to
    attention's O(n²) cost from chapter 07).
-   Explain the "lost in the middle" problem.
-   Design around context limits the way I'd design around a memory or
    payload-size limit.

------------------------------------------------------------------------

# What Counts Against the Context Window

The context window is the **total token budget** for a single request —
and critically, it's `input tokens + output tokens combined`, not just
your prompt.

``` text
Context window: 128,000 tokens
─────────────────────────────────────────────
[ System prompt ][ Conversation history ][ RAG chunks ][ User message ][ Model's response ]
              all of this together must fit inside 128,000 tokens
```

For multi-turn chat, this means **the entire conversation history gets
re-sent and re-processed on every single turn** — nothing is "remembered"
between calls the way session state would persist in a normal
application (tying back to chapter 08: inference is stateless).

  Model class            Typical context window
  ----------------------- --------------------------
  Early GPT-3 (2020)      4K tokens
  GPT-4 (2023)            8K-32K tokens
  Claude 3+ / GPT-4-turbo 128K-200K tokens
  Long-context models     1M+ tokens

## Platform Analogy: This Is a Hard Memory Ceiling

I treat the context window exactly like a container memory limit:

-   Exceed it → the call **fails outright**, or the provider silently
    truncates the oldest content — neither is a good failure mode to
    discover in production.
-   Because of attention's quadratic cost (chapter 07), a bigger
    context window isn't "free" the way a bigger memory limit is
    relatively cheap — it directly drives up both latency and $ cost,
    every single call.
-   Just like I wouldn't naively raise a memory limit to "fix" an OOM
    without understanding *why* usage is growing, I shouldn't reach for
    "just use a 1M context model" as the default fix for "the model
    forgot something" — most of the time RAG (chapter 14) is the right
    fix, the same way fixing a memory leak beats bumping the limit.

## The "Lost in the Middle" Problem

Research has consistently shown models are more accurate at using
information near the **start** and **end** of a long context, and
measurably worse at using information buried in the **middle** — even
when it technically fits within the window.

**Platform analogy:** this is like a cache with degraded hit rates for
entries in the "middle" of its eviction order — technically present,
but less reliably retrieved. Practical implication: don't assume
"it fits in the context window" means "the model will actually use it
well." Put the most important instructions/facts at the start or end of
the prompt, not buried in a huge middle block.

## Hands-on: Watch Truncation Actually Happen

``` python
from openai import OpenAI
import tiktoken

client = OpenAI()
enc = tiktoken.encoding_for_model("gpt-4")

huge_log = open("app.log").read()  # a large log file
print(f"Log is {len(enc.encode(huge_log))} tokens")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this log:\n{huge_log}"}]
    )
except Exception as e:
    print(f"Failed - likely exceeded context window: {e}")
```

Run this against a genuinely large log file and watch it fail. Then
chunk the log (split into pieces that each fit comfortably, summarize
each piece, then summarize the summaries — "map-reduce" for text) and
compare. That chunking pattern is the same shape as processing a huge
file in batches instead of loading it all into memory at once.

## Common Misconceptions

❌ A bigger context window means the model "remembers you" across
sessions.
(It only remembers what's re-sent in the current request payload —
there's no persistent memory unless the application layer explicitly
stores and re-injects history.)

❌ If it fits in the context window, the model will use all of it
equally well.
("Lost in the middle" means position matters, not just whether it fits.)

✔ Every token of conversation history costs money and latency on every
subsequent turn — long chat sessions get progressively more expensive
to continue, not just to start.

## Interview Questions

1.  What counts toward the context window — just the prompt, or
    something else too?
2.  Why doesn't a model "remember" previous conversations by default?
3.  What is the "lost in the middle" problem, and how does it change
    how you'd structure a prompt?
4.  Why isn't "just use the biggest context window available" always
    the right fix for a model missing information?

## Summary

The context window is a hard, combined input+output token ceiling that
resets every request — closer to a strict memory limit than to human
memory. Its cost scales with attention's quadratic behavior (chapter
07), and models use the middle of a long context less reliably than the
edges, which should shape how prompts are structured, not just how long
they're allowed to be.

## Next Chapter

➡️ `10-Temperature-TopP-and-Sampling.md`
