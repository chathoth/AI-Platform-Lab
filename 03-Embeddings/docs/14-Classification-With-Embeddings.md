# 14 - Classification With Embeddings

## Introduction

Chapter 03 of module 02 used few-shot prompting to classify alert
severity — an LLM call per classification. This chapter covers a
lighter-weight alternative: classifying text by comparing its embedding
to a small set of labeled example embeddings, with no LLM call needed
at inference time at all. For high-volume, simple classification, this
is often faster and cheaper than reaching for a chat model every time.

## Learning Objectives

After this chapter I should be able to:

-   Explain nearest-neighbor classification using embeddings.
-   Build a classifier from a small set of labeled examples.
-   Know when this approach is a better fit than an LLM prompt.

------------------------------------------------------------------------

# Nearest-Neighbor Classification, in Plain Terms

Embed a small set of labeled examples once. To classify new text, embed
it and find which labeled example it's closest to — that example's
label becomes the prediction.

``` text
Labeled examples (embedded once):
  "CPU at 45%" -> LOW
  "Disk at 98%, 5 min to full" -> HIGH
  "Memory at 78%" -> MEDIUM

New input: "Disk at 95%, 10 minutes to full"
  -> closest labeled example: "Disk at 98%, 5 min to full" (HIGH)
  -> prediction: HIGH
```

``` python
import requests
import numpy as np

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return np.array(r.json()["embedding"])

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

labeled_examples = [
    ("CPU at 45% on web-node-01", "LOW"),
    ("Disk at 98% on db-primary-01, 5 minutes to full", "HIGH"),
    ("Memory at 78% on cache-node-03", "MEDIUM"),
    ("Disk at 90% on a replica node, 30 minutes to full", "MEDIUM"),
]
labeled_vectors = [(embed(text), label) for text, label in labeled_examples]

def classify(text: str) -> str:
    query_vector = embed(text)
    best_label, best_score = None, -1
    for vector, label in labeled_vectors:
        score = cosine(query_vector, vector)
        if score > best_score:
            best_label, best_score = label, score
    return best_label
```

**Platform analogy:** this is few-shot prompting (module 02 chapter 03)
with the LLM call removed from the hot path — the "examples teach the
pattern" idea is identical, but instead of sending examples to a model
on every request, you compare embeddings directly. Same underlying
concept, much cheaper per-classification cost once the examples are
embedded.

## When This Beats an LLM Prompt

  Factor                        Embedding classification        LLM few-shot prompting
  ------------------------------- --------------------------------- ---------------------------------
  Per-classification cost           One embedding call                 One full chat completion call
  Latency                             Faster (no generation loop)         Slower (module 01 ch. 03's loop)
  Handles nuanced/multi-factor cases  Weaker - purely similarity-based    Stronger - can reason about edge cases
  Explains its reasoning               No - just a nearest match           Can, if asked
  Best fit                             High-volume, simple categories       Lower-volume, nuanced judgment calls

For something like routing thousands of log lines per minute into a
handful of severity buckets, embedding classification is usually the
better fit — the volume makes the LLM-per-call cost add up fast, and
the categories are simple enough not to need real reasoning. For
something like "should this specific incident trigger a page," where
context and judgment matter, an LLM prompt (or a human) is still the
better tool.

## Averaging Multiple Examples Per Label

A single labeled example per category is noisy. Averaging several
examples' vectors per label (a **centroid**) is more robust:

``` python
def label_centroid(vectors_for_label: list[np.ndarray]) -> np.ndarray:
    return np.mean(vectors_for_label, axis=0)
```

This is the same idea chapter 12's k-means uses internally — comparing
against a category's "center of mass" instead of any single example
smooths out noise from any one example being slightly atypical.

## Hands-on: Build and Test a Small Classifier

Using the `classify()` function above, test it against 5-6 new alert
strings you write yourself, deliberately including one ambiguous case.
Compare its prediction against what you'd expect, and note where a
purely similarity-based approach starts to strain — that's the exact
boundary the table above is describing.

## Common Misconceptions

❌ Embedding-based classification is strictly worse than an LLM
prompt.
(For high-volume, simple categorization it's typically faster, cheaper,
and perfectly accurate enough — the LLM's extra reasoning capability
isn't always needed or worth the cost.)

❌ You need many labeled examples per category for this to work.
(A handful of representative examples per label, or even one good
centroid, is often enough — this scales down much further than
fine-tuning a real classifier would.)

✔ Nearest-neighbor classification is few-shot prompting's underlying
idea (pattern-matching against examples) with the LLM generation step
removed — cheaper and faster, at the cost of not being able to reason
about genuinely ambiguous cases.

## Interview Questions

1.  How does nearest-neighbor classification with embeddings work?
2.  When would embedding-based classification be a better fit than an
    LLM few-shot prompt?
3.  What is a centroid, and why average multiple examples per label
    instead of using just one?
4.  What's the main limitation of embedding-based classification
    compared to an LLM prompt?

## Summary

Classifying text by comparing its embedding to labeled example
embeddings is a fast, cheap alternative to an LLM prompt for
high-volume, simple categorization — the same underlying idea as
few-shot prompting, with the per-request LLM call removed. It trades
away the ability to reason about genuinely ambiguous cases, which is
exactly where an LLM prompt or human judgment still earns its keep.

## Next Chapter

➡️ `15-Hybrid-Search.md`
