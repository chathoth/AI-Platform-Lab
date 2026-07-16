# 04 - The Native REST API

## Introduction

Every OpenAI-compatible client call throughout this repository has
ultimately gone through an HTTP request. This chapter is that request,
made directly — Ollama's own native API, verified with real `curl`
calls, before chapter 05 covers the compatibility layer built on top
of it.

## Learning Objectives

After this chapter I should be able to:

-   Call `/api/generate`, `/api/chat`, and `/api/embeddings` directly
    with `curl`.
-   Read a raw response and identify the fields that matter.
-   Explain why seeing the raw API matters even if you always use a
    client library.

------------------------------------------------------------------------

# The Three Endpoints You'll Actually Use

``` text
POST /api/generate     - single-prompt completion (no message history)
POST /api/chat           - role-tagged messages (system/user/assistant)
POST /api/embeddings       - text in, a vector out
```

## `/api/generate`, Verified

``` bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Say OK",
  "stream": false
}'
```

Real response:

``` json
{
  "model": "llama3.1:8b",
  "created_at": "2026-07-15T20:46:52.254333Z",
  "response": "OK",
  "done": true,
  "done_reason": "stop",
  "context": [128006, 882, 128007, ...]
}
```

`context` is a raw token array representing the conversation state —
Ollama's own low-level way of continuing a conversation without
resending full text, distinct from the message-list approach module
02 chapter 11 covered for chat-style APIs.

## `/api/chat`, Verified

``` bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.1:8b",
  "messages": [{"role": "user", "content": "Say OK"}],
  "stream": false
}'
```

Real response:

``` json
{
  "model": "llama3.1:8b",
  "message": {"role": "assistant", "content": "OK!"},
  "done": true,
  "done_reason": "stop",
  "total_duration": 8501217709,
  "load_duration": 251617625,
  "prompt_eval_count": 12,
  "prompt_eval_duration": 8115762000,
  "eval_count": 3,
  "eval_duration": 122955000
}
```

This is the endpoint that matches module 02's role-tagged message
pattern directly — `messages` is the same list-of-dicts shape used
throughout this repository's examples. The timing fields
(`total_duration`, `eval_duration`, all in **nanoseconds**) are real,
detailed latency data — `load_duration` specifically tells you how much
of the total time was spent loading the model versus actually
generating (module 01 chapter 03's generation loop).

## `/api/embeddings`, Verified

``` bash
curl -s http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "test"
}'
```

Verified: returns a real vector, `768` numbers long for
`nomic-embed-text` — matching module 03 chapter 04's dimensionality
discussion exactly, now confirmed against the real endpoint every
module 03 example used under the hood.

## Why This Matters Even If You Always Use a Client Library

**Platform analogy:** this is the same value as reading raw HTTP
traffic with `curl` before trusting a client SDK's abstraction — it's
what lets you debug precisely when a client library behaves
unexpectedly, because you know exactly what's actually being sent and
received underneath it. Every timing field, every response shape
detail in this chapter is something an OpenAI-compatible client
(chapter 05) partially hides from you.

## Hands-on: Read the Full Timing Breakdown Yourself

``` bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.1:8b",
  "messages": [{"role": "user", "content": "Explain what a Kubernetes Deployment is in one sentence."}],
  "stream": false
}' | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('response:', d['message']['content'])
print(f\"load: {d['load_duration']/1e9:.2f}s\")
print(f\"prompt eval: {d['prompt_eval_duration']/1e9:.2f}s ({d['prompt_eval_count']} tokens)\")
print(f\"generation: {d['eval_duration']/1e9:.2f}s ({d['eval_count']} tokens)\")
"
```

This breaks total latency into load time, prompt processing time, and
generation time separately — a level of detail worth having when
diagnosing whether a slow response is a cold-load problem or a genuine
generation-speed problem.

## Common Misconceptions

❌ You need a client library to use Ollama at all.
(Every example in this chapter is a raw `curl` call — the API is
plain HTTP and JSON, no SDK required.)

❌ The OpenAI-compatible endpoint and the native API return identical
data.
(The native API exposes detailed timing and a raw `context` token
array that the OpenAI-compatible layer doesn't surface the same way —
chapter 05 covers exactly what gets translated and what doesn't.)

✔ Timing fields are in **nanoseconds** — divide by `1e9` for seconds,
a detail easy to misread the first time you look at raw output.

## Interview Questions

1.  Name the three core Ollama API endpoints and what each is for.
2.  What does the `context` field in `/api/generate`'s response
    represent?
3.  How would you determine whether a slow response was caused by
    model loading versus generation?
4.  Why is it useful to call the raw API directly even if you normally
    use a client library?

## Summary

Ollama's native REST API — `/api/generate`, `/api/chat`,
`/api/embeddings` — is plain HTTP and JSON, callable directly with
`curl`, and it's what every client library in this repository has been
wrapping the whole time. Its responses include detailed timing data
(in nanoseconds) that a client library often abstracts away, useful
for precisely diagnosing whether latency comes from loading, prompt
processing, or generation.

## Next Chapter

➡️ `05-The-OpenAI-Compatible-Endpoint.md`
