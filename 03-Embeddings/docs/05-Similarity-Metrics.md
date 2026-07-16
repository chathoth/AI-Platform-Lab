# 05 - Similarity Metrics

## Introduction

Module 01 chapter 05 used cosine similarity without much explanation of
why that metric specifically. This chapter covers the actual options,
because the choice matters more than it looks — pick the wrong metric
for how your vectors were produced and search results get quietly,
confusingly worse without any error to point at.

## Learning Objectives

After this chapter I should be able to:

-   Explain cosine similarity, dot product, and Euclidean distance.
-   Know which metric to use for a given embedding model.
-   Implement any of the three from scratch in a few lines of Python.

------------------------------------------------------------------------

# Three Ways to Measure "Closeness"

``` text
Cosine similarity:  measures the ANGLE between two vectors
                     range: -1 (opposite) to 1 (identical direction)
                     ignores vector length/magnitude entirely

Dot product:         sum of element-wise multiplication
                     range: unbounded
                     sensitive to both angle AND magnitude

Euclidean distance:  straight-line distance between two points
                     range: 0 (identical) to infinity
                     the "as the crow flies" distance you'd expect
                     from geometry class
```

``` python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def dot_product(a, b):
    return np.dot(a, b)

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)
```

## Why Cosine Is the Default for Text Embeddings

Text embedding magnitude often correlates with things you don't
actually want to measure (like text length), while the *direction* of
the vector is where meaning tends to live. Cosine similarity strips out
magnitude entirely and compares direction only — which is why it's the
standard default for text search.

**Platform analogy:** this is like comparing two servers by their
*ratio* of CPU-to-memory usage rather than their raw resource numbers —
a small pod and a large pod doing the same kind of work should look
"similar" in shape even if their absolute numbers differ. Cosine
similarity does the equivalent for text: two short, related sentences
and two long, related paragraphs can still point in a similar
direction even though their raw vector magnitudes differ.

## When Dot Product Is Actually the Right Choice

Some embedding models (check the model's documentation) are trained
specifically so that dot product on **normalized** vectors gives the
best results, or use magnitude meaningfully as part of a relevance
signal (common in some retrieval-tuned models). Many vector databases
default to dot product for performance reasons when vectors are
pre-normalized, since it's cheaper to compute than cosine (no division
needed if magnitude is already 1).

## Practical Guidance

  Situation                                          Metric
  ---------------------------------------------------- -----------------------------------
  General text similarity (most common case)             Cosine similarity
  Model docs explicitly recommend it, vectors normalized  Dot product
  Comparing raw geometric distance/clustering              Euclidean distance
  Unsure                                                      Cosine — the safest general default

The important discipline: **check what your embedding model's
documentation recommends**, and use that metric consistently across
your whole pipeline. Mixing metrics (embedding with one assumption,
searching with another) is a silent-degradation bug, not a crash — search
results just get subtly worse with nothing pointing you at why.

## Hands-on: See All Three Side by Side

``` python
import requests
import numpy as np

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return np.array(r.json()["embedding"])

related_a = embed("The pod is stuck in CrashLoopBackOff")
related_b = embed("Container keeps restarting and failing health checks")
unrelated = embed("Best pizza toppings for a party")

for label, a, b in [("related pair", related_a, related_b), ("unrelated pair", related_a, unrelated)]:
    print(f"{label}:")
    print(f"  cosine:    {cosine_similarity(a, b):.4f}")
    print(f"  dot product: {dot_product(a, b):.4f}")
    print(f"  euclidean: {euclidean_distance(a, b):.4f}")
```

Notice cosine similarity is easiest to interpret at a glance (closer to
1 = more related) — that readability is a big part of why it's the
default choice for search-ranking use cases.

## Common Misconceptions

❌ All three metrics will always agree on which result is "most
similar."
(They usually agree for well-behaved embeddings, but magnitude-
sensitive metrics like dot product and Euclidean distance can rank
differently than cosine when vector lengths vary meaningfully.)

❌ The choice of similarity metric doesn't matter much.
(Using the wrong metric for how a model was trained/normalized degrades
search quality silently — no error, just worse results.)

✔ Cosine similarity is the safe general default for text because it
ignores magnitude and measures direction — the part of the vector where
meaning actually lives.

## Interview Questions

1.  What does cosine similarity measure, and what does it deliberately
    ignore?
2.  When would dot product be preferred over cosine similarity?
3.  Why is mixing similarity metrics across a pipeline a "silent"
    bug rather than a crash?
4.  Why is text embedding magnitude often not a reliable signal of
    similarity?

## Summary

Cosine similarity, dot product, and Euclidean distance are three
different ways to measure closeness between vectors — cosine ignores
magnitude and measures direction, making it the standard safe default
for text search. Whichever metric you choose, use it consistently
across the whole pipeline; mismatched metrics degrade results silently
with no error to flag it.

## Next Chapter

➡️ `06-Generating-Embeddings-Locally-with-Ollama.md`
