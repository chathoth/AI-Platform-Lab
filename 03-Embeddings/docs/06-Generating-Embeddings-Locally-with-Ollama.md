# 06 - Generating Embeddings Locally with Ollama

## Introduction

Every chapter so far has used a snippet of the local embedding call.
This chapter is the reference for that call itself — the practical
mechanics of generating embeddings with Ollama, including the mistake
that costs the most time when you first try to embed more than a
handful of documents: doing it one at a time, synchronously, with no
error handling.

## Learning Objectives

After this chapter I should be able to:

-   Call Ollama's embedding endpoint directly and through the OpenAI-
    compatible SDK.
-   Batch-embed a list of documents efficiently.
-   Handle the realistic failure modes (empty text, oversized input,
    the server not running).

------------------------------------------------------------------------

# Two Ways to Call It

**1. Ollama's native endpoint** (`requests`, used throughout this
module so far):

``` python
import requests

response = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "nomic-embed-text",
    "prompt": "The pod is stuck in CrashLoopBackOff",
})
vector = response.json()["embedding"]
```

**2. The OpenAI-compatible SDK** (matches module 01/02's pattern,
useful if your codebase already standardized on the `openai` client):

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.embeddings.create(model="nomic-embed-text", input="The pod is stuck in CrashLoopBackOff")
vector = response.data[0].embedding
```

Both hit the same local model — pick whichever fits the rest of your
codebase. This module uses the `requests` form for embeddings (it's
one line shorter and makes the raw HTTP call visible, useful for
learning) and the `openai` SDK for anything involving chat.

## Batching, and Why It Matters

Embedding documents one at a time in a loop works, but is slow — each
call has fixed overhead (connection, model load state) on top of the
actual computation:

``` python
# works, but slow for anything beyond a handful of documents
vectors = [embed(doc) for doc in documents]
```

``` python
# batched - most embedding APIs (including OpenAI-compatible ones)
# accept a list of inputs in one call
def embed_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model="nomic-embed-text", input=texts)
    return [item.embedding for item in response.data]

vectors = embed_batch(documents)
```

**Platform analogy:** this is the exact same lesson as batching database
writes instead of issuing one `INSERT` per row — the per-call overhead
dominates at small scale and batching is the fix, the same instinct
that applies to any bulk operation over a network call.

## Realistic Failure Modes

  Failure                             Symptom                       Fix
  ------------------------------------- ------------------------------- ---------------------------------
  Ollama server not running              Connection refused              Check `ollama serve` is up before calling
  Model not pulled                        404 / model not found            `ollama pull nomic-embed-text` first
  Empty string input                       Some models return an error, others a degenerate vector | Filter empty/whitespace-only text before embedding
  Extremely long input                      Silently truncated to the model's max input length | Chunk first (chapter 07) — don't assume it handles arbitrary length

``` python
def embed_safe(text: str) -> list[float] | None:
    text = text.strip()
    if not text:
        return None  # nothing meaningful to embed
    try:
        r = requests.post("http://localhost:11434/api/embeddings",
                           json={"model": "nomic-embed-text", "prompt": text}, timeout=10)
        r.raise_for_status()
        return r.json()["embedding"]
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Can't reach Ollama - is 'ollama serve' running?")
```

## Hands-on: Batch-Embed a Small Document Set

``` python
documents = [
    "To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.",
    "When disk usage hits 90%, first check for oversized log files.",
    "To roll back a deployment, use kubectl rollout undo.",
]

import time
start = time.time()
vectors = [embed_safe(d) for d in documents]  # one at a time
print(f"Sequential: {time.time() - start:.2f}s for {len(documents)} docs")
```

Try this with a larger list (20-50 short strings) and compare
sequential timing against `embed_batch()` if your Ollama version and
model support batched input — the overhead difference becomes very
visible past a few dozen documents.

## Common Misconceptions

❌ Ollama's embedding endpoint handles input of any length gracefully.
(Like any embedding model, it has a maximum input length — text beyond
that gets silently truncated, which is why chunking, chapter 07, is a
required step, not an optional optimization.)

❌ One-at-a-time embedding calls are fine for any dataset size.
(Fine for a handful of documents; the fixed per-call overhead makes it
noticeably slow once you're embedding hundreds or thousands of chunks —
batch where the API supports it.)

✔ Always check `ollama pull nomic-embed-text` has been run and
`ollama serve` is reachable before debugging "why is my embedding call
failing" further upstream in your code.

## Interview Questions

1.  What are the two ways to call Ollama's embedding functionality
    shown in this chapter?
2.  Why does batching embedding calls matter for performance?
3.  What happens if you embed text longer than the model's maximum
    input length?
4.  Name two realistic failure modes when generating embeddings
    locally, and how you'd handle each.

## Summary

Ollama exposes embeddings through both a native endpoint and an
OpenAI-compatible SDK — pick whichever fits your codebase. Batch calls
where possible instead of looping one document at a time, and handle
the realistic failure modes (server not running, model not pulled,
empty or oversized input) explicitly rather than letting them surface
as confusing downstream errors.

## Next Chapter

➡️ `07-Chunking-Before-Embedding.md`
