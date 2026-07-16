# 05 - The OpenAI-Compatible Endpoint

## Introduction

Every single example script in modules 01 through 07 used
`OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")`. This
chapter finally explains that line — what it actually gets you, and
where the compatibility layer stops being perfectly transparent.

## Learning Objectives

After this chapter I should be able to:

-   Explain what `/v1` compatibility actually provides.
-   Know which OpenAI SDK features are supported and which aren't.
-   Decide when to use the compatible endpoint versus the native API.

------------------------------------------------------------------------

# What `/v1` Actually Is

``` text
http://localhost:11434/v1/chat/completions   <- OpenAI-shaped
http://localhost:11434/api/chat                <- Ollama's native shape (chapter 04)
```

Ollama runs a second, parallel set of endpoints under `/v1` that accept
and return data in the same shape OpenAI's API uses — that's the entire
mechanism behind every `client.chat.completions.create(...)` call in
this repository working against a local model with zero code changes
from what would be needed against a real OpenAI endpoint.

**Platform analogy:** this is an API shim — the same pattern as an
S3-compatible API in front of a different storage backend, letting
existing S3 client tooling work unmodified against something that
isn't actually S3. The compatibility layer's whole value is letting
you swap the backend without rewriting the calling code.

## Why `api_key="ollama"` Is Required But Meaningless

``` python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

The OpenAI SDK requires a non-empty `api_key` argument to construct a
client at all — Ollama's server doesn't actually check or use this
value for anything, since there's no authentication on a default local
setup (chapter 15 covers why that's fine locally and not fine once
exposed beyond localhost). Any non-empty string works; `"ollama"` is
just a readable convention.

## What's Supported, and What to Watch For

  Feature                          Supported via `/v1`?
  ------------------------------------ --------------------------------
  Chat completions                        Yes - this repository's core pattern
  Tool/function calling                     Yes, for models with `tools` capability (chapter 03's `ollama show` check)
  Streaming                                  Yes (module 01 chapter 03's generation loop, streamed)
  Embeddings                                  Yes, via `/v1/embeddings`
  Some advanced OpenAI-specific parameters      Not always — check before assuming full parity

Not every OpenAI SDK feature has a matching Ollama implementation —
this is the practical reason to occasionally drop down to the native
API (chapter 04) for something the compatibility layer doesn't expose
cleanly, or to check Ollama's own documentation for `/v1` coverage
before assuming full parity with a real OpenAI account.

## Hands-on: Compare Both Endpoints for the Same Request

``` python
from openai import OpenAI
import requests

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# via the OpenAI-compatible endpoint
response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Say OK"}],
)
print("compatible endpoint:", response.choices[0].message.content)

# via the native endpoint, same underlying request
native = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.1:8b",
    "messages": [{"role": "user", "content": "Say OK"}],
    "stream": False,
}).json()
print("native endpoint:    ", native["message"]["content"])
```

Both should produce equivalent answers — confirming, directly, that
these are two shapes over the same underlying model call, not two
different systems.

## Common Misconceptions

❌ The OpenAI-compatible endpoint means Ollama is secretly calling
OpenAI's actual API.
(Nothing leaves your machine — `/v1` is Ollama's own server, speaking
a compatible request/response shape, verified throughout this
repository by every example running with no internet connection
required beyond the initial model pull.)

❌ Every OpenAI SDK feature works identically against Ollama.
(Core chat, tools, and streaming work well — some advanced or
provider-specific parameters may not have a direct equivalent; check
before assuming full parity.)

✔ `api_key="ollama"` is a required-but-unchecked placeholder — the
SDK needs *a* string, Ollama's local server doesn't validate it at
all, which is a very different situation from a real hosted API key.

## Interview Questions

1.  What does Ollama's `/v1` endpoint actually provide?
2.  Why is `api_key="ollama"` required by the SDK but meaningless to
    Ollama itself?
3.  Name two things confirmed to work well via the compatible
    endpoint, per this chapter.
4.  When would you drop down to the native API instead of the
    OpenAI-compatible one?

## Summary

Ollama's `/v1` endpoints are a compatibility shim that accepts and
returns OpenAI-shaped requests and responses, which is the entire
mechanism behind every example in this repository working unmodified
against a local model. It covers the core patterns (chat, tools,
streaming, embeddings) well, but isn't a perfect 1:1 replica of a real
OpenAI account — worth verifying against Ollama's own documentation
before assuming full feature parity.

## Next Chapter

➡️ `06-Modelfiles-Customizing-a-Model.md`
