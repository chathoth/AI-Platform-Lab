# 10 - Debugging a RAG Pipeline

## Introduction

This is the chapter I'd actually pin to the wall. Every earlier chapter
built one stage of the pipeline; this one is the incident-response
runbook for when the final answer is wrong and you don't yet know why.
The single most important habit here: **debug in pipeline order, not
in "most interesting" order** — jumping straight to the model is almost
always the wrong first move.

## Learning Objectives

After this chapter I should be able to:

-   Walk the pipeline stage by stage to isolate where a wrong answer
    actually originates.
-   Use each stage's real artifact file as the checkpoint for that
    stage.
-   Diagnose a real example failure using this exact sequence.

------------------------------------------------------------------------

# The Debugging Sequence

``` text
1. Was the PDF loaded?
2. Is the expected text present in the page document?
3. Is it preserved in a chunk?
4. Was the chunk embedded and stored?
5. Was the correct chunk retrieved?
6. Was the chunk included in the prompt?
7. Did the LLM follow the prompt?
```

**Platform analogy:** this is exactly a request-tracing runbook —
check the load balancer, then the app server, then the database, in
order, instead of guessing which layer is broken. Jumping to "maybe
it's the database" before confirming the request even reached the app
server wastes time; jumping to "maybe the model is bad" before
confirming retrieval worked is the same mistake.

## Stage by Stage, With the Real Command and Artifact

**1. Document loading**

``` bash
python src/01_load_documents.py
```

Check whether the expected text exists in `loaded_documents.json`
(chapter 03).

**2. Chunking**

``` bash
python src/02_chunk_documents.py
```

Search `chunks.json` for the expected evidence, and confirm it survived
intact (chapter 04).

**3. Embedding and storage**

``` bash
python src/04_store_vectors.py --reset
```

A full rebuild rules out stale or duplicate vectors (chapter 06).

**4. Retrieval**

``` bash
python src/05_similarity_search.py --question "..."
```

Confirm the expected source, page, relevant text, and a reasonable
rank all show up (chapter 07).

**5. Prompt**

``` bash
python src/06_build_prompt.py --question "..."
```

Confirm the correct chunk actually made it into the assembled prompt
(chapter 08) — retrieval succeeding doesn't guarantee the prompt
formatting preserved it usefully.

**6. Generation**

Only *after* stages 1-5 are confirmed correct should you investigate
the chat model itself: temperature, prompt wording, or context
ordering. If you change the model before ruling out the earlier
stages, you're debugging blind.

## A Real Example, Walked Through

``` text
Question: "When is the carry-over request due?"
Wrong answer: "December 31."
```

Debug it in order:

1.  Search the chunks for `November 1` — is it even present?
2.  Check whether the chunk containing it was actually retrieved for
    this question.
3.  Check whether a *different* chunk — one about the accrual period,
    which does mention `December 31` in a different context — got
    retrieved instead or alongside it.
4.  If both chunks were retrieved together, the model may have
    conflated them — reduce irrelevant context (lower `TOP_K`, chapter
    07) or strengthen the instruction to cite the specific rule that
    answers the specific question (chapter 08).
5.  Re-test the exact same question after each change, not a different
    one — you need to confirm the *specific* failure is fixed.

## Hands-on: Reproduce and Fix a Real Failure

Deliberately misconfigure the pipeline — set `TOP_K=1` in `.env` — and
re-run `05_similarity_search.py --question "How are unused vacation
days handled at termination?"`. If the single retrieved chunk isn't the
right one, you've just reproduced a real retrieval failure. Restore
`TOP_K=4` and confirm it's fixed — this is the debugging sequence
applied to a failure you caused on purpose, which is a safe way to
build the instinct before you need it on a failure you didn't cause.

## Common Misconceptions

❌ A wrong answer usually means the model needs to be changed or
re-prompted.
(Per the sequence above, retrieval and chunking failures are far more
common causes in practice — model/prompt changes should be the *last*
thing tried, not the first.)

❌ Debugging can start wherever seems most likely.
(Starting out of order risks "fixing" a symptom at the wrong stage —
e.g. rewriting a prompt to compensate for a retrieval bug, which
papers over the real problem instead of solving it.)

✔ Every stage in this pipeline has a real, inspectable artifact file —
use the artifact for the stage you're checking, not the final answer,
to isolate exactly where a failure originates.

## Interview Questions

1.  Why should debugging follow pipeline order instead of jumping to
    the model first?
2.  For each of the 7 debugging stages, name the command or artifact
    used to check it.
3.  In the "December 31" example, what step revealed the actual root
    cause?
4.  Why is changing the prompt to compensate for a retrieval bug a
    risky fix?

## Summary

Debugging a RAG pipeline means walking the same seven stages it's built
from, in order, using each stage's real artifact as the checkpoint —
document loaded, text preserved through chunking, chunk embedded and
stored, correct chunk retrieved, chunk present in the prompt, and only
then, the model's generation. Skipping ahead to "fix the model" before
ruling out the earlier stages is the single most common way to waste
time on a RAG bug.

## Next Chapter

➡️ `11-Best-Practices.md`
