# 13 - Deduplication With Embeddings

## Introduction

Exact-match deduplication (`if text1 == text2`) misses the far more
common case: two tickets, two alerts, or two runbook entries that say
the same thing in different words. This chapter is a narrow,
practical application of similarity search (chapter 10) — instead of
"find the top-k matches for a query," it's "find anything that's
suspiciously close to something I already have."

## Learning Objectives

After this chapter I should be able to:

-   Explain why exact-match deduplication misses most real duplicates.
-   Set and justify a similarity threshold for "close enough to be a
    duplicate."
-   Flag near-duplicates for review instead of auto-merging blindly.

------------------------------------------------------------------------

# Exact Match vs. Semantic Match

``` text
Exact match catches:
  "Disk usage critical on db-primary-02"
  "Disk usage critical on db-primary-02"     <- identical string, easy

Exact match misses:
  "Disk usage critical on db-primary-02"
  "db-primary-02 is almost out of disk space" <- same event, different words
```

The second pair is exactly the kind of duplicate that piles up in real
ticket queues — two people reporting the same incident in their own
words, two auto-generated alerts phrased slightly differently by
different monitoring tools. Cosine similarity (chapter 05) catches this
because it compares meaning, not exact characters.

## A Similarity Threshold Is a Judgment Call, Not a Constant

``` python
import requests
import numpy as np

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return np.array(r.json()["embedding"])

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_near_duplicates(texts: list[str], threshold: float = 0.92) -> list[tuple]:
    vectors = [embed(t) for t in texts]
    duplicates = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = cosine(vectors[i], vectors[j])
            if score >= threshold:
                duplicates.append((texts[i], texts[j], score))
    return duplicates
```

There's no universally correct threshold — it depends entirely on how
costly a false positive (merging two genuinely different things) is
versus a false negative (missing a real duplicate) for your specific
use case:

  Threshold      Effect
  ---------------- --------------------------------------------
  Very high (0.97+) Only near-identical text flagged; safe, misses more real dupes
  Moderate (0.90-0.95) Reasonable middle ground for most ticket/alert dedup
  Lower (0.80-0.90)   Catches more loosely related duplicates; more false positives

**Platform analogy:** this is a fuzzy-matching threshold, exactly like
tuning a fingerprinting algorithm for alert deduplication in a
monitoring system — set it too strict and real duplicates flood
through; too loose and unrelated alerts get incorrectly merged. There's
no free win here, only a trade-off to tune deliberately.

## Never Auto-Merge — Flag for Review

Because the threshold is a judgment call, treat matches as **candidates
for human review**, not automatic merges, especially the first time
you run this against real data:

``` python
candidates = find_near_duplicates(ticket_titles, threshold=0.90)
for a, b, score in candidates:
    print(f"[{score:.3f}] possible duplicate:\n  A: {a}\n  B: {b}\n")
    # a real system would surface this in a review queue,
    # not silently merge the two tickets
```

This mirrors module 01 chapter 18's rule about never blindly executing
LLM output — a similarity score is a strong signal, not a certainty,
and the cost of a wrong auto-merge (losing a real, distinct ticket) is
usually higher than the cost of a human spending five seconds
confirming a suggested match.

## Hands-on: Find Real Near-Duplicates

``` python
tickets = [
    "Disk usage critical on db-primary-02",
    "db-primary-02 is almost out of disk space",
    "Checkout service returning 500 errors",
    "Login page is loading slowly for some users",
    "payment service throwing intermittent 500s",
]

for a, b, score in find_near_duplicates(tickets, threshold=0.80):
    print(f"[{score:.3f}]\n  {a}\n  {b}\n")
```

Try lowering the threshold gradually and watch when the checkout/
payment pair (related but about different services) starts getting
flagged alongside the genuinely duplicate disk-usage pair — that's the
threshold trade-off from the table above, made concrete.

## Common Misconceptions

❌ A single "correct" similarity threshold exists for deduplication.
(It's a deliberate trade-off between missed duplicates and false
positives, tuned to your specific data and the cost of getting it
wrong — there's no universal right answer.)

❌ High-confidence duplicate matches are safe to auto-merge.
(Treat them as candidates for review, especially early on — the cost
of an incorrect auto-merge is usually worse than a few seconds of human
confirmation.)

✔ Semantic deduplication catches the far more common real-world case —
same event, different wording — that exact-match deduplication
structurally cannot.

## Interview Questions

1.  Why does exact-string-match deduplication miss most real-world
    duplicate tickets or alerts?
2.  What's the trade-off involved in setting a similarity threshold
    for deduplication?
3.  Why shouldn't high-similarity matches be auto-merged without
    review?
4.  How is threshold tuning for deduplication similar to tuning a
    fingerprinting algorithm for alert grouping?

## Summary

Semantic deduplication finds near-duplicate text based on meaning, not
exact characters, catching the common case of the same event reported
in different words. The similarity threshold is a deliberate trade-off
to tune for your data, not a fixed constant, and matches should be
surfaced for human review rather than auto-merged, given the asymmetric
cost of getting a merge wrong.

## Next Chapter

➡️ `14-Classification-With-Embeddings.md`
