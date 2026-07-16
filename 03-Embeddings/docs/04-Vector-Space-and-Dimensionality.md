# 04 - Vector Space and Dimensionality

## Introduction

Every embedding chapter so far has waved at "a vector of numbers"
without asking how many numbers, or what that count actually costs. This
chapter is the sizing conversation — the embeddings equivalent of
module 01 chapter 12's "how much memory does this model need" — because
dimensionality directly drives storage size and search speed once
you're storing more than a handful of vectors.

## Learning Objectives

After this chapter I should be able to:

-   Explain what a dimension is in an embedding vector.
-   Estimate storage size for a given number of embeddings.
-   Explain the trade-off between higher and lower dimensionality.

------------------------------------------------------------------------

# What "768 Dimensions" Actually Means

`nomic-embed-text` produces a vector of 768 floating-point numbers per
piece of text. Each of those 768 numbers is one **dimension** — think of
it as 768 independent axes the model learned to position meaning along,
compared to the 2 or 3 axes you can actually visualize on a graph.

``` text
2D (visualizable):  [x, y]                      -> a point on a page
3D (visualizable):  [x, y, z]                    -> a point in a room
768D (not visualizable, but mathematically identical concept):
                     [d1, d2, d3, ..., d768]      -> a point in a space
                                                      with 768 independent
                                                      directions
```

The math (distance, angle, similarity) works exactly the same regardless
of dimension count — you just can't draw it. More dimensions generally
mean more capacity to encode subtle distinctions between meanings, at a
direct storage and compute cost.

## Storage Cost Scales Directly With Dimension Count

Each dimension is typically a 4-byte float. Storage per vector is just
`dimensions × 4 bytes`:

  Model                      Dimensions   Size per vector   10,000 documents
  --------------------------- ------------ ------------------ -------------------
  `nomic-embed-text`            768          ~3 KB              ~30 MB
  OpenAI `text-embedding-3-small` 1536         ~6 KB              ~60 MB
  OpenAI `text-embedding-3-large` 3072         ~12 KB             ~120 MB

**Platform analogy:** this is the exact same sizing exercise as
estimating disk usage for a database table — row count × row size. Here
the "row" is one embedding, and the "row size" is dimension count × 4
bytes. Before indexing a large document set, run this math the same way
you'd estimate disk footprint before provisioning a database.

## Higher Dimensions Isn't Automatically Better

More dimensions can capture more nuance, but also cost more to store
and search, and — past a point — can add noise rather than signal for a
given task (a phenomenon related to the "curse of dimensionality" in
search literature: as dimensions grow very large, distances between
points can become less discriminating). In practice, for most internal
document search, a 768-1536 dimension general-purpose model is a solid
middle ground — you don't need the largest available model to get
useful results.

## Hands-on: Measure It Yourself

``` python
import requests

response = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "nomic-embed-text",
    "prompt": "The pod is stuck in CrashLoopBackOff",
})

vector = response.json()["embedding"]
dimensions = len(vector)
bytes_per_vector = dimensions * 4

print(f"Dimensions: {dimensions}")
print(f"Bytes per vector: {bytes_per_vector}")
print(f"Estimated size for 10,000 documents: {bytes_per_vector * 10_000 / 1_000_000:.1f} MB")
print(f"Estimated size for 1,000,000 documents: {bytes_per_vector * 1_000_000 / 1_000_000_000:.2f} GB")
```

Run this, then imagine embedding every ticket your team has ever filed,
or every log line from a busy week — that back-of-envelope math is
exactly what you'd do before choosing a vector database's storage tier
in module 04.

## Common Misconceptions

❌ More dimensions always means a strictly better embedding model.
(Past a reasonable point, returns diminish and storage/compute cost
keeps climbing — bigger isn't free, the same lesson as module 01
chapter 12's parameter-count discussion.)

❌ Dimensionality is a fixed, universal number.
(It's specific to each embedding model — different models produce
different-length vectors, and vectors from different models can never
be compared or mixed, per chapter 01.)

✔ Storage cost for embeddings is `count × dimensions × 4 bytes` — a
simple, useful formula to run before committing to a model for a
large document set.

## Interview Questions

1.  What does a "dimension" represent in an embedding vector?
2.  How do you estimate the storage cost for embedding 100,000
    documents with a given model?
3.  Why isn't a higher-dimension embedding model automatically the
    right choice?
4.  Why can't vectors from two different-dimension models ever be
    compared directly?

## Summary

Each number in an embedding vector is a dimension — an axis the model
learned to position meaning along — and dimension count directly drives
storage and compute cost, calculated the same simple way you'd estimate
database disk usage. More dimensions isn't automatically better; a
mid-sized general-purpose model like `nomic-embed-text` (768
dimensions) is a solid default for most internal document search.

## Next Chapter

➡️ `05-Similarity-Metrics.md`
