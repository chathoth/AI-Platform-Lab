# 08 - Embedding Different Content Types

## Introduction

Every example so far has embedded clean, plain-English sentences. Real
infrastructure content is messier — YAML, log lines, code, ticket text
full of IDs and timestamps. This chapter covers what actually changes
per content type, building directly on module 01 chapter 04's finding
that technical text tokenizes differently than prose — the same gap
shows up here, for a different reason.

## Learning Objectives

After this chapter I should be able to:

-   Explain why raw logs and structured data often need pre-processing
    before embedding.
-   Strip noise (timestamps, IDs) that hurts semantic search without
    helping it.
-   Choose an embedding approach for code specifically.

------------------------------------------------------------------------

# The Core Problem: Noise Dilutes Signal

An embedding model encodes the whole input's meaning — including parts
that carry no real semantic content. A raw log line is full of exactly
that kind of noise:

``` text
Raw:      "2026-07-15T09:12:03.882Z [pod-7d9f4c8b6-x2k9p] ERROR CrashLoopBackOff exit=137"
Cleaned:  "ERROR CrashLoopBackOff exit=137"
```

The timestamp and pod hash are unique to this exact event and will
never match anything else — they add noise to the vector without
contributing meaning, and can measurably worsen search results by
diluting the parts that actually matter (`ERROR`, `CrashLoopBackOff`,
`exit=137`).

**Platform analogy:** this is the same instinct behind stripping
request IDs and timestamps before log-based anomaly clustering — you
want to group by *what happened*, not by the fact that no two log lines
share an identical timestamp. High-cardinality, unique-per-event fields
are noise for similarity purposes, signal for exact lookup purposes —
know which one you're optimizing for.

## Content-Type-Specific Guidance

**Logs** — strip timestamps, request IDs, pod hashes, and other
high-cardinality unique fields before embedding; keep the message,
severity, and any stable error codes.

**YAML/JSON/structured config** — embed a natural-language *description*
of the structure rather than the raw structure when possible; raw YAML
punctuation and indentation adds little semantic value and costs tokens
(module 01 chapter 04's finding, resurfacing here for embedding cost
too).

``` python
raw_yaml = "replicas: 3\nresources:\n  limits:\n    memory: 512Mi"
described = "A deployment with 3 replicas and a 512Mi memory limit."
# `described` embeds more meaningfully for search than the raw YAML does
```

**Code** — embedding models trained on general text handle code poorly
compared to code-specific embedding models (if precise code search
matters, look for one); for general-purpose search, embedding a
function's docstring/comment plus signature often works better than
embedding the raw implementation body.

**Tickets/incident text** — usually embeds well as-is (it's closest to
natural prose), but benefits from the jargon-expansion trick from
chapter 02 for team-specific shorthand.

## Hands-on: Compare Raw vs. Cleaned Log Embeddings

``` python
import requests
import numpy as np

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return np.array(r.json()["embedding"])

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

log1_raw = "2026-07-15T09:12:03.882Z [pod-7d9f4c8b6-x2k9p] ERROR CrashLoopBackOff exit=137"
log2_raw = "2026-07-15T14:47:19.201Z [pod-a3f8e1c2d-m7q4r] ERROR CrashLoopBackOff exit=137"
# same underlying event, different timestamp/pod - should be near-identical

log1_clean = "ERROR CrashLoopBackOff exit=137"
log2_clean = "ERROR CrashLoopBackOff exit=137"

print("raw logs similarity:    ", cosine(embed(log1_raw), embed(log2_raw)))
print("cleaned logs similarity:", cosine(embed(log1_clean), embed(log2_clean)))
```

The cleaned version should score noticeably closer to a perfect match
than the raw version — the timestamp and pod ID noise is measurably
dragging similarity down for what is, semantically, the exact same
event.

## Common Misconceptions

❌ Embedding raw log lines works just as well as cleaned ones.
(High-cardinality noise like timestamps and IDs measurably dilutes
semantic similarity — cleaning is a real, not cosmetic, improvement.)

❌ Code should always be embedded as raw source text.
(General embedding models weren't trained specifically on code
semantics — a docstring/signature-based approach, or a code-specific
embedding model, usually outperforms raw source for general search.)

✔ Before embedding any structured or semi-structured content, ask what
you actually want two pieces of content to be considered "similar"
for — and strip anything that would make near-identical events look
artificially different.

## Interview Questions

1.  Why does embedding a raw log line with its timestamp intact hurt
    semantic search quality?
2.  What fields would you typically strip from a log line before
    embedding it?
3.  Why might describing a YAML structure in plain language embed
    better than the raw YAML itself?
4.  Why do general-purpose embedding models often struggle with raw
    source code?

## Summary

Different content types need different pre-processing before
embedding: logs benefit from stripping high-cardinality noise like
timestamps and IDs, structured config often embeds better as a
plain-language description than as raw YAML/JSON, and code benefits
from a docstring/signature-based approach or a code-specific model.
The common thread: strip whatever doesn't contribute to the specific
notion of "similar" you're trying to build.

## Next Chapter

➡️ `09-Storing-Embeddings.md`
