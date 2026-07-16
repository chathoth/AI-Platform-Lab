# 17 - Monitoring and Observability

## Introduction

A vector database is a real, stateful piece of infrastructure — it
deserves the same observability discipline as any other datastore. This
chapter is the "what would I actually want on a dashboard for this"
question, tying together metrics implied by nearly every earlier
chapter into one coherent monitoring picture.

## Learning Objectives

After this chapter I should be able to:

-   Name the key metrics worth tracking for a vector database in
    production.
-   Explain why query latency alone is an incomplete health signal.
-   Instrument a basic query wrapper with the logging this module's
    earlier chapters implied.

------------------------------------------------------------------------

# What's Worth Tracking

  Metric                          Why it matters                              Source chapter
  --------------------------------- --------------------------------------------- ----------------
  Query latency (p50/p95/p99)          User-facing responsiveness                    07, 13
  Collection size (vector count)         Capacity planning, memory sizing               09, 13
  Recall@k against an eval set             Is retrieval actually still accurate?          module 03 ch. 16
  Insert/upsert throughput                   Ingestion pipeline health                      06, 09
  Disk/memory usage                            Approaching the wall from chapter 13             13
  Embedding model version per collection        Catching drift before it silently degrades results | module 03 ch. 11

**Platform analogy:** this is the same shape as monitoring any other
datastore — latency percentiles, size/growth, and a correctness signal
(recall@k is the vector-search equivalent of a synthetic health-check
query that verifies not just "is it up" but "is it returning the right
answer").

## Why Query Latency Alone Isn't Enough

A vector database can be fast *and* wrong at the same time — returning
quickly with irrelevant results due to a metric mismatch (module 03
chapter 05), a stale index after an embedding model change (module 03
chapter 11), or a filter bug (chapter 12). Latency tells you the system
is responsive; recall@k (module 03 chapter 16) tells you it's actually
useful. Both belong on the same dashboard.

## A Minimal Instrumented Query Wrapper

``` python
import time
import logging

logger = logging.getLogger("vector_db")

def monitored_query(collection, query_text: str, n_results: int = 5, where: dict | None = None):
    start = time.perf_counter()
    results = collection.query(query_texts=[query_text], n_results=n_results, where=where)
    latency_ms = (time.perf_counter() - start) * 1000

    logger.info(
        "vector_query",
        extra={
            "latency_ms": round(latency_ms, 2),
            "n_results_requested": n_results,
            "n_results_returned": len(results["documents"][0]),
            "collection_count": collection.count(),
            "had_filter": where is not None,
        },
    )
    return results
```

This is the module 01 chapter 16 "log the fully assembled request, not
just the final answer" lesson, applied to a vector database call
instead of an LLM call — structured, per-call metrics are what make a
production incident ("search suddenly got worse") debuggable instead
of a guessing game.

## Scheduled Recall@K as a Standing Health Check

``` python
def health_check_recall(collection, eval_set: list[dict], k: int = 3) -> float:
    hits = sum(
        1 for case in eval_set
        if case["expected_id"] in collection.query(query_texts=[case["query"]], n_results=k)["ids"][0]
    )
    return hits / len(eval_set)
```

Running this on a schedule (daily, or after every re-index) turns
module 03 chapter 16's one-off evaluation into a standing monitor —
the same instinct as a synthetic transaction check that periodically
verifies a critical user flow still works, not just that the service
responds to a ping.

## Hands-on: Wrap a Real Query and Read the Output

``` python
import logging
logging.basicConfig(level=logging.INFO)

collection.add(ids=["m1"], documents=["Restart the pod by deleting it."])
monitored_query(collection, "how do I restart a pod")
```

Confirm the logged output includes latency, result count, and
collection size — then imagine this same log line, aggregated across
thousands of real queries, as the actual dashboard you'd build from it.

## Common Misconceptions

❌ Uptime and latency are sufficient monitoring for a vector database.
(They confirm the system is responsive, not that it's returning
correct or complete results — recall@k or an equivalent correctness
signal belongs alongside them.)

❌ Monitoring a vector database is fundamentally different from
monitoring any other datastore.
(The shape is the same as any datastore: latency, size, throughput,
and a correctness check — vector-specific concerns like embedding model
version are additions to that shape, not a different discipline
entirely.)

✔ Recall@k, checked on a schedule against a fixed eval set, is the
vector-database equivalent of a synthetic health check that verifies
actual correctness, not just responsiveness.

## Interview Questions

1.  Name four metrics worth tracking for a production vector database.
2.  Why is query latency alone an incomplete health signal?
3.  What would make a vector database fast but also silently wrong?
4.  How is scheduled recall@k monitoring similar to a synthetic
    transaction check?

## Summary

A vector database needs the same monitoring discipline as any other
datastore — latency, size, throughput — plus a correctness signal
(recall@k, checked on a schedule) that latency and uptime alone can't
provide, since a fast, responsive vector database can still be quietly
returning bad results due to a metric mismatch, stale index, or filter
bug from any of this module's earlier chapters.

## Next Chapter

➡️ `18-Best-Practices.md`
