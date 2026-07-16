# 07 - Chunking Before Embedding

## Introduction

Chapter 06 flagged that long input gets silently truncated. Chunking is
the fix — splitting a document into smaller pieces *before* embedding,
so each piece fully fits and each piece represents one coherent idea
instead of a truncated fragment. This is also the step where module 05
(RAG) actually begins, upstream of retrieval — get chunking wrong and
every later stage inherits the problem.

## Learning Objectives

After this chapter I should be able to:

-   Explain why whole documents are usually the wrong unit to embed.
-   Compare fixed-size, sentence-based, and semantic chunking
    strategies.
-   Choose a chunk size and overlap for a given document type.

------------------------------------------------------------------------

# Why Not Just Embed the Whole Document?

A single embedding vector represents the *overall* meaning of whatever
text went in. Feed it a 10-page runbook, and the resulting vector is a
blurry average of everything in it — a search for "how do I restart
Elasticsearch" might match the whole document's vector only weakly,
even if page 7 answers the question precisely, because the other nine
pages are diluting that signal.

**Platform analogy:** this is the same problem as logging one giant
combined line for an entire request instead of structured, queryable
events at each step — you can technically search it, but you lose the
ability to pinpoint exactly where the relevant detail lives. Chunking
is what gives you queryable granularity back.

## Chunking Strategies, Compared

  Strategy                       How it works                              Trade-off
  -------------------------------- ------------------------------------------ ---------------------------------
  Fixed-size (by characters/tokens)  Split every N characters/tokens             Simple, fast; can cut a sentence or idea in half
  Sentence/paragraph-based             Split on natural sentence/paragraph breaks  Respects meaning boundaries; chunk sizes vary
  Semantic chunking                     Split where meaning actually shifts (using embeddings themselves to detect the shift) | Best boundaries; more compute, more complexity

``` python
# fixed-size chunking with overlap - simple and effective for most cases
def chunk_fixed(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # overlap keeps context at chunk boundaries
    return chunks
```

## Why Overlap Matters

Without overlap, a sentence or idea that happens to fall right at a
chunk boundary gets split in half, and neither half fully represents
it. A small overlap (10-20% of chunk size) means the boundary content
appears fully in at least one chunk.

``` text
No overlap:
  Chunk 1: "...disk usage above 90% on a primary"
  Chunk 2: "database node pages on-call immediately..."
  -> neither chunk alone captures the full rule

With overlap:
  Chunk 1: "...disk usage above 90% on a primary database node pages on-call"
  Chunk 2: "on a primary database node pages on-call immediately..."
  -> the full rule appears intact in chunk 1
```

## Choosing Chunk Size

  Content type              Suggested chunk size          Why
  --------------------------- ------------------------------ -----------------------------------
  Short runbook steps           200-400 characters              Each step is usually self-contained
  Prose documentation             500-1000 characters              Balances context with granularity
  Code                              By function/logical block, not fixed size | Splitting mid-function breaks meaning entirely
  Structured data (YAML/JSON)      By logical record/section, not fixed size | Same reason as code — fixed-size cuts break structure

Fixed-size chunking is a reasonable default for prose, but code and
structured data need boundary-aware chunking — cutting a YAML block or
a function in half produces a chunk that's syntactically broken, not
just topically incomplete.

## Hands-on: Chunk a Real Document and Compare

``` python
runbook = """
To debug CrashLoopBackOff:
1. Run kubectl describe pod <name> to see recent events.
2. Check kubectl logs <name> --previous for the crash reason.
3. Common causes: OOMKilled (raise memory limits), failed liveness
   probe (check probe config), or a bad image (check the deploy diff).
4. If memory-related, correlate with the metrics dashboard before
   just raising limits blindly - it may be a real leak.
"""

chunks_no_overlap = chunk_fixed(runbook, chunk_size=150, overlap=0)
chunks_with_overlap = chunk_fixed(runbook, chunk_size=150, overlap=30)

for label, chunks in [("no overlap", chunks_no_overlap), ("with overlap", chunks_with_overlap)]:
    print(f"--- {label} ({len(chunks)} chunks) ---")
    for c in chunks:
        print(f"  {c!r}")
```

Look for a chunk boundary that cuts a numbered step or sentence in
half in the no-overlap version, then check whether the overlapping
version keeps that same content intact in at least one chunk.

## Common Misconceptions

❌ Embedding a whole document works fine as long as it fits the model's
input limit.
(Fitting isn't the only concern — even under the limit, a whole
document's embedding is a blurry average, which weakens search
precision for anything but very short documents.)

❌ Bigger chunks are always better because they preserve more context.
(Bigger chunks dilute the signal the same way whole documents do —
chunk size is a trade-off between granularity and context, not a "more
is better" dial.)

✔ Chunk boundaries should respect meaning where possible — sentence,
paragraph, function, or record boundaries — not just a fixed character
count, especially for code and structured data.

## Interview Questions

1.  Why does embedding an entire long document produce a weaker search
    signal than embedding it in chunks?
2.  What problem does overlap between chunks solve?
3.  Why is fixed-size chunking a poor fit for code or structured data?
4.  How would you choose chunk size differently for short runbook
    steps versus long-form prose documentation?

## Summary

Chunking splits a document into smaller pieces before embedding so
each vector represents one coherent idea instead of diluting many
ideas into a blurry average — the foundation every RAG pipeline (module
05) depends on. Choose chunk size and boundaries based on content type,
and use overlap to avoid splitting an idea exactly at a chunk boundary.

## Next Chapter

➡️ `08-Embedding-Different-Content-Types.md`
