# 12 - Embeddings via Ollama

## Introduction

Module 03's entire foundation ran through Ollama's embedding endpoint
without stopping to look at it directly. This short chapter closes
that loop — the exact API every embedding example in this repository
called, verified once more, on its own terms.

## Learning Objectives

After this chapter I should be able to:

-   Call the embeddings endpoint directly and read its response.
-   Explain why an embedding model shows up differently in `ollama
    show` than a chat model.
-   Know which local models are suited for embeddings versus chat.

------------------------------------------------------------------------

# Verified: The Embeddings Call

``` bash
curl -s http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "test"
}'
```

Verified: returns a real vector, `768` numbers long — this is the
literal request every module 03 example made under
`requests.post("http://localhost:11434/api/embeddings", ...)`, now
seen directly instead of through that wrapper.

## Why `nomic-embed-text` Looks Different in `ollama show`

``` bash
ollama show nomic-embed-text
```

An embedding model's `ollama show` output has no `completion`
capability listed (chapter 03's capabilities section) — it's built to
produce vectors, not generate text, matching module 03 chapter 01's
distinction between embedding models and chat models exactly.
Attempting to use `nomic-embed-text` as if it were a chat model (via
`/api/chat` or `/api/generate`) won't work the way you'd expect,
because it was never trained for next-token generation.

## The OpenAI-Compatible Embeddings Endpoint

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.embeddings.create(model="nomic-embed-text", input="test")
vector = response.data[0].embedding
print(len(vector))  # 768
```

Same underlying call as the raw `curl` example, through chapter 05's
compatibility layer — this is the exact form some of module 03's
examples used as an alternative to the `requests`-based direct call.

## Batch Embedding, Verified Against the Native API

``` bash
curl -s http://localhost:11434/api/embed -d '{
  "model": "nomic-embed-text",
  "input": ["first text", "second text", "third text"]
}'
```

Note: `/api/embed` (newer, supports batching multiple inputs in one
call) is distinct from `/api/embeddings` (older, single input) — check
which one a given Ollama version supports, since this is an area
that's evolved across releases. Batching multiple inputs in one call
is module 03 chapter 06's batching advice, applied directly at the API
level instead of just in application code.

## Hands-on: Compare Single and Batch Embedding Calls

``` python
import time
import requests

texts = [f"Sample document number {i}" for i in range(10)]

start = time.time()
for text in texts:
    requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
print(f"10 sequential calls: {time.time() - start:.2f}s")

start = time.time()
requests.post("http://localhost:11434/api/embed", json={"model": "nomic-embed-text", "input": texts})
print(f"1 batched call: {time.time() - start:.2f}s")
```

Compare the two timings on your own machine — this is module 03
chapter 06's batching lesson made directly observable against the real
API.

## Common Misconceptions

❌ Any Ollama model can be used for embeddings.
(Only models specifically trained for it — `nomic-embed-text` and
similar — produce meaningful embedding vectors. Check `ollama show`
for capabilities before assuming.)

❌ `/api/embeddings` and `/api/embed` are the same endpoint under
different names.
(They differ in whether they accept a single input or a batch — worth
checking which your installed Ollama version supports and prefers.)

✔ An embedding model's `ollama show` output (no `completion`
capability listed) is the definitive way to confirm it's actually
suited for embeddings, not a chat model being misused for the wrong
purpose.

## Interview Questions

1.  What does `ollama show` reveal about whether a model supports
    embeddings versus chat?
2.  What's the difference between `/api/embeddings` and `/api/embed`?
3.  Why would batching embedding calls at the API level matter, per
    module 03 chapter 06?
4.  Why can't a chat model like `llama3.1:8b` be used the same way as
    `nomic-embed-text` for embeddings?

## Summary

Ollama's embedding endpoints (`/api/embeddings`, and the newer batch-
capable `/api/embed`) are the literal API every module 03 example
called under the hood — verified directly here, alongside the
`ollama show` check that confirms whether a given model is actually
suited for embeddings versus chat generation.

## Next Chapter

➡️ `13-Streaming-Responses.md`
