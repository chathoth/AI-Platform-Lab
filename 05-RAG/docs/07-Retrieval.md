# 07 - Retrieval

## Introduction

This is the chapter where the "R" in RAG actually happens — finding the
policy chunks most relevant to a real question, and specifically
proving it works on a paraphrased question that shares almost no
vocabulary with the source text.

## Learning Objectives

After this chapter I should be able to:

-   Run similarity search against a real question and verify the
    correct source page comes back.
-   Explain what `TOP_K` controls and the trade-off in either
    direction.
-   Correctly interpret (and correctly avoid over-interpreting) a
    distance score.

------------------------------------------------------------------------

# Direct vs. Semantic Queries, Against the Real Document

**Direct query** — shares vocabulary with the source text:

``` text
When must a carry-over request be submitted?
```

Expected evidence is on page 2: the request must be submitted no later
than November 1.

**Semantic query** — same underlying question, almost no shared
vocabulary:

``` text
What is the deadline for moving unused vacation to next year?
```

Neither `"carry-over"` nor `"submitted"` appears here, but a working
embedding model (chapter 05) should still retrieve the same relevant
passage — this is the practical proof that retrieval in this pipeline
is semantic, not keyword-based.

## Top-K

``` env
TOP_K=4
```

This means the retriever returns the four closest chunks for every
question.

  Too small (`TOP_K=1-2`)             Too large (`TOP_K=10+`)
  ------------------------------------- ---------------------------------------
  Supporting evidence may be missed        Irrelevant or contradictory context gets added
  Faster, cheaper                             Slower, more tokens (module 01 ch. 04), and risks confusing the model with noise

This is the same precision-vs-recall trade-off module 03 chapter 16
covers via recall@k — `TOP_K` *is* the `k` in that metric, made
concrete in a running config value.

## Score Interpretation

Chroma returns a **distance** score in this pipeline — lower distance
generally means a closer match for this collection. Do not compare raw
scores across different embedding models, distance functions,
collections, or normalization strategies (module 03 chapter 05) — a
distance of `0.3` means nothing on its own; it's only meaningful
relative to other distances from the *same* collection and query.

## Hands-on: Prove Semantic Retrieval Works

``` bash
python src/05_similarity_search.py \
  --question "Can vacation continue to accumulate during parental leave?"
```

Expected evidence retrieved:

``` text
Employees will continue to accrue vacation during maternity and
parental leaves.
```

Now try a harder paraphrase:

``` bash
python src/05_similarity_search.py \
  --question "How are unused vacation days handled at termination?"
```

Expected evidence should come from page 3. If it doesn't, that's a real
retrieval failure worth debugging via chapter 10 — not something to
paper over by tweaking the prompt (chapter 08) instead.

``` python
def test_similarity_search(vector_store):
    results = vector_store.similarity_search(
        "When must a carry-over request be submitted?", k=2
    )
    assert results
    assert any(doc.metadata.get("page") == 2 for doc in results)
```

This is `tests/test_05_similarity_search.py`, verbatim — retrieval
correctness is something you can assert on, not just eyeball.

## Common Misconceptions

❌ A lower distance score always means a "good enough" match in
absolute terms.
(It only means "closer than the alternatives in this same search" —
there's no universal threshold for "good," and comparing distances
across different collections or models is meaningless.)

❌ If the paraphrased query fails to retrieve the right chunk, the
prompt or model must be the problem.
(Per chapter 10's debugging order, retrieval failures should be ruled
out *before* touching the prompt or model — a wrong answer downstream
of a retrieval miss isn't a generation problem.)

✔ The most convincing proof that retrieval is working semantically,
not just via keyword luck, is a paraphrased query that shares almost no
vocabulary with the source text still returning the right passage.

## Interview Questions

1.  Why does a paraphrased query with no shared vocabulary still
    retrieve the correct chunk?
2.  What's the trade-off of setting `TOP_K` too low versus too high?
3.  Why shouldn't you compare a Chroma distance score against a score
    from a different collection or embedding model?
4.  How would you verify retrieval correctness with an automated test,
    rather than by reading output?

## Summary

Retrieval finds the chunks most relevant to a question by comparing
embeddings, not keywords — proven concretely in this module by
paraphrased queries that still retrieve the correct policy page.
`TOP_K` trades missed evidence against added noise, and distance scores
are only meaningful relative to other results from the same search, not
as an absolute quality measure.

## Next Chapter

➡️ `08-Prompting.md`
