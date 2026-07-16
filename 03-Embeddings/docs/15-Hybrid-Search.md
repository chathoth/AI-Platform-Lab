# 15 - Hybrid Search (Keyword + Semantic)

## Introduction

Semantic search (chapter 10) has a real weakness I glossed over until
it bit me: it's bad at exact, literal matches — an error code, a
hostname, a specific version number. Ask semantic search for
`"error E4021"` and it might return something *conceptually* related
about errors in general, missing the one document that contains the
literal string `E4021`. Hybrid search fixes this by combining semantic
search with old-fashioned keyword search — the two are complementary,
not competing.

## Learning Objectives

After this chapter I should be able to:

-   Explain what semantic search structurally can't do well.
-   Combine keyword and semantic search results into one ranked list.
-   Choose a blending strategy for a given use case.

------------------------------------------------------------------------

# What Semantic Search Is Bad At

Embeddings encode general meaning — they're not built to preserve exact
identifiers, and there's no guarantee two texts sharing a specific code,
version number, or hostname land close together in vector space just
because they share that one token.

``` text
Query: "error E4021"

Semantic search might return:
  "Common causes of database connection errors" (conceptually related,
   but doesn't actually mention E4021 at all)

Keyword search reliably returns:
  The one document that literally contains the string "E4021"
```

**Platform analogy:** this is exactly why full-text search engines keep
both a semantic vector index *and* a traditional inverted index side by
side — cosine similarity is fuzzy by design, and fuzzy is the wrong
tool for "find the document containing this exact error code." You want
grep's precision and embeddings' flexibility, together, not one or the
other.

## Combining the Two: A Simple Blend

``` python
def keyword_score(query: str, text: str) -> float:
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    if not query_words:
        return 0.0
    return len(query_words & text_words) / len(query_words)  # fraction of query words present

def hybrid_search(query: str, index: list, top_k: int = 3, semantic_weight: float = 0.6) -> list:
    query_vector = embed(query)
    scored = []
    for entry in index:
        semantic = cosine(query_vector, entry["vector"])
        keyword = keyword_score(query, entry["text"])
        combined = semantic_weight * semantic + (1 - semantic_weight) * keyword
        scored.append({**entry, "score": combined, "semantic": semantic, "keyword": keyword})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
```

This is deliberately simple — a real implementation would use a proper
keyword-ranking algorithm (like BM25) instead of naive word overlap, but
the *shape* of the idea is the same: compute both scores, blend them,
rank by the combination.

## Choosing the Blend Weight

  `semantic_weight`   Behavior
  --------------------- ---------------------------------------------
  1.0                    Pure semantic search (chapter 10's behavior)
  0.0                    Pure keyword search
  0.5-0.7                A reasonable default — favors meaning, but exact terms still count

The right weight depends on your content: documentation full of exact
error codes, hostnames, and version numbers benefits from more keyword
weight; conversational content (tickets, chat logs) benefits from more
semantic weight.

## Hands-on: See Hybrid Search Rescue a Literal Query

``` python
runbook_index = [
    {"text": "Common causes of database connection issues include pool exhaustion and network partitions.", "vector": embed("...")},
    {"text": "Error E4021 occurs when the connection pool hits its configured max size.", "vector": embed("...")},
    {"text": "To roll back a failed deployment, use kubectl rollout undo.", "vector": embed("...")},
]
# (in real code, embed each "text" value directly - shortened here for clarity)

results = hybrid_search("what causes error E4021", runbook_index, semantic_weight=0.5)
for r in results:
    print(f"combined={r['score']:.3f} semantic={r['semantic']:.3f} keyword={r['keyword']:.3f}: {r['text'][:60]}")
```

Compare the ranking here against running pure semantic search
(`semantic_weight=1.0`) on the same query — the document containing the
literal `"E4021"` string should rank more reliably at the top once
keyword score is factored in.

## Common Misconceptions

❌ Semantic search alone is always sufficient for a good search
experience.
(It structurally underperforms on exact identifiers, codes, and
uncommon proper nouns — hybrid search exists specifically to cover that
gap.)

❌ Hybrid search means running two completely separate search systems.
(It means computing two scores per candidate and blending them into one
ranked list — the two techniques share the same candidate set, they're
not run as isolated pipelines.)

✔ Semantic and keyword search are complementary, not competing — the
right system uses both and blends the results based on what kind of
content and queries it's actually serving.

## Interview Questions

1.  Why does semantic search structurally struggle with exact error
    codes or hostnames?
2.  How does hybrid search combine keyword and semantic scores?
3.  What factors would push you toward a higher keyword weight versus
    a higher semantic weight?
4.  Why are semantic and keyword search described as complementary
    rather than as alternatives?

## Summary

Semantic search is fuzzy by design and structurally weak at exact
identifiers — hybrid search fixes this by blending semantic similarity
with keyword matching into one combined ranking, tuned by how much
weight to give each side based on the content being searched. This is
the standard production pattern, not an either/or choice between the
two techniques.

## Next Chapter

➡️ `16-Evaluating-Embedding-Quality.md`
