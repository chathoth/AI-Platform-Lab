# 15 - Reranking

## Introduction

A vector database's `n_results` is fast because it's approximate and
cheap per-candidate (chapter 02). Reranking is the next stage some
pipelines add: take that fast, approximate top-N, and re-score it with
something slower but more accurate, applied only to a small candidate
set instead of the whole collection.

## Learning Objectives

After this chapter I should be able to:

-   Explain why reranking exists as a distinct stage from initial
    retrieval.
-   Implement a simple LLM-based reranker.
-   Reason about the cost/quality trade-off of adding a reranking
    stage.

------------------------------------------------------------------------

# Two-Stage Retrieval

``` text
Stage 1 (retrieval):  vector search over the WHOLE collection,
                        fast, approximate, returns top-20 candidates
Stage 2 (reranking):   a slower, more accurate scorer re-ranks just
                        those 20 candidates, returns the final top-5
```

**Platform analogy:** this is a load balancer's two-phase health check
— a cheap, fast check (TCP connect) filters a large candidate pool
first, and a more expensive, thorough check (an actual HTTP request
with a body) only runs against the survivors. Running the expensive
check against every candidate would be correct but wasteful; running
only the cheap check misses nuance the expensive one would catch.

## Why Rerank at All?

Embedding similarity (chapter 07) is fast because it reduces meaning to
a single vector comparison — but that compression loses some nuance
that a more expensive comparison (like feeding both texts directly to
an LLM and asking "how relevant is this, really?") can recover. For
retrieval where getting the *very best* top few results actually
matters — like module 05's RAG pipeline, where the wrong chunk in the
prompt directly produces a wrong answer — that recovered nuance can be
worth the extra cost.

## A Simple LLM-Based Reranker

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def llm_rerank(query: str, candidates: list[str], model: str = "llama3.1:8b") -> list[tuple[str, float]]:
    scored = []
    for doc in candidates:
        prompt = (
            f"Question: {query}\nPassage: {doc}\n\n"
            "On a scale of 0-10, how directly does this passage answer "
            "the question? Respond with only the number."
        )
        r = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=0)
        try:
            score = float(r.choices[0].message.content.strip())
        except ValueError:
            score = 0.0
        scored.append((doc, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
```

``` python
initial_results = collection.query(query_texts=["carry-over deadline"], n_results=10)
reranked = llm_rerank("carry-over deadline", initial_results["documents"][0])
top_3 = reranked[:3]
```

Note this is deliberately run only against the **already-retrieved**
top-N (10 in this example), not the whole collection — that's the
entire point of the two-stage design.

## The Cost Trade-off, Honestly

Reranking with an LLM call per candidate is expensive relative to
vector search — module 01 chapter 03's generation loop, run once per
candidate. This only makes sense when:

-   the initial retrieval set is small (reranking 10-20 candidates,
    never the whole collection),
-   getting the very top results exactly right matters more than
    latency,
-   the vector search alone is measurably imprecise for your queries
    (verify with recall@k, module 03 chapter 16, before adding this
    complexity).

For many use cases, a good embedding model plus solid metadata
filtering (chapter 08) is accurate enough without reranking at all —
don't add this stage by default.

## Hands-on: Compare Ranking Before and After

``` python
collection.add(
    ids=["d1", "d2", "d3"],
    documents=[
        "Vacation policies vary by employment type across the organization.",
        "Requests to carry over vacation must be submitted no later than November 1.",
        "The HR department handles all leave-related paperwork and approvals.",
    ],
)

initial = collection.query(query_texts=["carry-over deadline"], n_results=3)
print("initial vector-search order:", initial["documents"][0])

reranked = llm_rerank("carry-over deadline", initial["documents"][0])
print("reranked order:", [doc for doc, score in reranked])
```

Check whether reranking pulls the genuinely most relevant passage
(`d2`, the one that actually states a deadline) to the very top, even
if vector search alone ranked it lower.

## Common Misconceptions

❌ Reranking should replace vector search entirely.
(It's a refinement stage applied to a small candidate set vector search
already narrowed down — running an LLM-based scorer against an entire
large collection would be far too slow and expensive.)

❌ Reranking always improves results enough to justify its cost.
(Verify with an eval set (module 03 chapter 16) whether initial
retrieval is actually the bottleneck before adding this complexity and
cost.)

✔ Reranking is a two-stage pattern: cheap and approximate first, over
everything; expensive and precise second, over a small survivor set —
never the other way around.

## Interview Questions

1.  Why is reranking applied only to a small candidate set, not the
    whole collection?
2.  What's the platform-engineering analogy for two-stage retrieval?
3.  What determines whether adding a reranking stage is actually worth
    its cost?
4.  How would you verify whether reranking meaningfully improves
    results before committing to the extra latency and cost?

## Summary

Reranking adds a second, more expensive and more accurate scoring pass
over the small candidate set an initial vector search already narrowed
down — the same two-phase pattern as a cheap health check followed by
a thorough one for survivors only. It's worth the added cost when
getting the very top results exactly right matters and initial
retrieval alone is measurably imprecise — verify that with an eval set
before adding it by default.

## Next Chapter

➡️ `16-Vector-Database-vs-Traditional-Database.md`
