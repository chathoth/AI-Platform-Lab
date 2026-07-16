# 16 - Evaluating Embedding Quality

## Introduction

Module 02 chapter 16 built an eval set to score prompts objectively
instead of trusting a gut feeling. This chapter is the same discipline
applied to search — "the results look reasonable" isn't good enough
once a search feature has real users depending on it. This is also
where a chunking or embedding-model decision from earlier chapters
actually gets tested against reality instead of intuition.

## Learning Objectives

After this chapter I should be able to:

-   Build a minimal relevance-labeled eval set for search.
-   Compute recall@k, the standard metric for "did the right answer
    show up in the results."
-   Use eval results to compare chunking strategies or embedding
    models objectively.

------------------------------------------------------------------------

# Recall@K: The Core Metric

Recall@k answers: **for a given query, was the correct document in the
top k results?**

``` text
Query: "how do I restart a stuck pod?"
Correct document: "runbook-crashloop.md"

Top-3 results: [runbook-crashloop.md, runbook-deploy.md, runbook-disk.md]
  -> correct document is in position 1 -> recall@3 = 1 (hit)

Top-3 results: [runbook-deploy.md, runbook-disk.md, runbook-network.md]
  -> correct document is NOT in the top 3 -> recall@3 = 0 (miss)
```

Averaged across many queries, this becomes a single, comparable number
— "our search finds the right document in the top 3 results 84% of the
time" is a measurable claim you can track over time and test changes
against.

## Building a Minimal Eval Set

``` python
eval_set = [
    {"query": "how do I restart a stuck pod?", "expected_source": "runbook-crashloop.md"},
    {"query": "what happens when disk is full on the primary db?", "expected_source": "runbook-disk.md"},
    {"query": "how do I undo a bad deployment?", "expected_source": "runbook-rollback.md"},
]
```

Just like module 02's prompt eval sets, this should include the queries
that are actually hard — phrased differently than the source document,
using synonyms, or slightly ambiguous — not just the easy cases that
would pass with any reasonable approach.

## Computing Recall@K

``` python
def recall_at_k(index: "SimpleSearchIndex", eval_set: list, k: int = 3) -> float:
    hits = 0
    for case in eval_set:
        results = index.search(case["query"], top_k=k)
        sources = [r["metadata"]["source"] for r in results]
        if case["expected_source"] in sources:
            hits += 1
    return hits / len(eval_set)

print(f"recall@3: {recall_at_k(index, eval_set, k=3):.0%}")
```

## Using This to Compare Real Decisions

This is where chapter 07's chunking choice and chapter 03's model
choice stop being theoretical:

``` python
# compare two chunk sizes on the same eval set
index_small_chunks = build_index(documents, chunk_size=200)
index_large_chunks = build_index(documents, chunk_size=800)

print(f"200-char chunks recall@3: {recall_at_k(index_small_chunks, eval_set):.0%}")
print(f"800-char chunks recall@3: {recall_at_k(index_large_chunks, eval_set):.0%}")
```

**Platform analogy:** this is A/B testing applied to a search pipeline
— instead of shipping a chunking or model change because it "seems
better," you measure it against a fixed benchmark before and after,
exactly the discipline module 02 chapter 16 applied to prompts.

## Hands-on: Score Your Own Search Index

Take the `SimpleSearchIndex` from chapter 10, build it from 4-5 short
runbook entries, write 3-4 eval queries phrased differently than the
source text, and compute recall@3. Then deliberately shrink `top_k` to
1 and watch recall drop — that's the direct trade-off between "how many
results do I show" and "how likely is the right one to be included."

## Common Misconceptions

❌ If search results "look reasonable" for the queries you tried, it's
working well enough.
(Spot-checking reproduces your existing blind spots — the same lesson
as module 02 chapter 16, now applied to search relevance instead of
prompt output.)

❌ Recall@k is the only metric that matters.
(Precision — how much of what's returned is actually relevant, not
just whether the right answer is *somewhere* in the results — and
latency both matter too; recall@k is the standard starting point, not
the whole picture.)

✔ An eval set turns a chunking strategy or model choice from "I think
this is better" into a measurable, comparable claim — the same value a
test suite brings to code.

## Interview Questions

1.  What does recall@k measure?
2.  Why should a search eval set include deliberately hard,
    differently-worded queries?
3.  How would you use an eval set to decide between two different
    chunk sizes?
4.  What's the trade-off of increasing `k` (the number of results
    shown) with respect to recall?

## Summary

Evaluating a search system means measuring recall@k against a labeled
eval set — did the correct document show up in the top results — rather
than trusting that results "look reasonable." This turns chunking and
model decisions from earlier chapters into testable, comparable claims,
the same discipline module 02 applied to prompt quality.

## Next Chapter

➡️ `17-Cost-and-Performance-at-Scale.md`
