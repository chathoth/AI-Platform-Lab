# 09 - Evaluation

## Introduction

Module 02 chapter 16 argued that "it looks right" isn't validation —
you need an eval set. This chapter is that discipline applied to the
whole RAG pipeline at once: retrieval correctness and answer quality,
measured separately, against a real dataset checked into this module.

## Learning Objectives

After this chapter I should be able to:

-   Explain why retrieval and answer quality are evaluated as separate
    checks, not one combined pass/fail.
-   Run this module's evaluator and interpret its output.
-   Explain why unanswerable questions are as important to test as
    answerable ones.

------------------------------------------------------------------------

# The Evaluation Dataset

``` text
evaluation/evaluation_dataset.csv
evaluation/evaluation_dataset.json
```

The dataset includes direct questions, paraphrased questions,
multi-condition questions, and — critically — **unanswerable**
questions, each with expected source pages and expected answer
keywords.

## Two Separate Checks, Not One

**Retrieval evaluation** — for each answerable question, does at least
one expected page appear in the retrieved top-k chunks?

``` text
Question: When must a carry-over request be submitted?
Expected page: 2
```

If page 2 isn't retrieved, generation quality is beside the point —
retrieval already failed, and chapter 10's debugging order says to fix
that before touching anything downstream.

**Answer evaluation** — does the generated answer contain the expected
keywords?

``` text
Expected keywords:
November 1
written request
```

Keyword matching isn't a complete semantic evaluation (it can't
detect a fluent, keyword-matching answer that's subtly wrong in some
other way) — but it's transparent, fast, and genuinely useful as a
regression check, the same "good enough starting point" module 02
chapter 16 recommends over no evaluation at all.

**Platform analogy:** this is exactly separating a health check into
"is the pod reachable" versus "is the pod returning correct data" — two
different failure modes, and conflating them into one pass/fail hides
which one actually broke.

## Negative Evaluation: Testing What the Model *Shouldn't* Answer

``` text
What dental benefits are provided?
```

This isn't in the vacation policy at all. A correctly grounded system
must produce exactly:

``` text
I could not find enough information in the provided documents.
```

This directly tests hallucination resistance (module 01 chapter 11) —
and it's arguably the more important half of the evaluation set,
because a model that answers *everything* confidently, including
things it has no evidence for, is far more dangerous than one that
occasionally under-answers.

## Hands-on: Run the Real Evaluator

``` bash
python src/08_evaluate_rag.py
```

Inspect the output:

``` text
artifacts/evaluation_results.json
```

The evaluator checks, per question: whether an expected page was
retrieved, whether expected keywords appear in the answer, and whether
unanswerable questions correctly triggered the no-answer response —
then reports an overall pass rate.

The evaluation dataset in this module covers: initial entitlement,
maximum entitlement, normal carry-over limit, carry-over deadline,
exceptional carry-over, maternity/parental leave, hospitalization
during vacation, unpaid leave, termination payout, definitions,
approval responsibilities — plus several deliberately unsupported
questions about benefits and compensation this policy doesn't cover.

``` python
def test_evaluation_dataset_exists():
    dataset = Path("evaluation/evaluation_dataset.csv")
    assert dataset.exists()
    rows = list(csv.DictReader(dataset.open()))
    assert len(rows) >= 10
```

This is `tests/test_08_evaluation.py` — a sanity check that the eval
set itself hasn't silently shrunk or gone missing, since an evaluator
is only as trustworthy as the dataset behind it.

## Common Misconceptions

❌ A high overall pass rate means the pipeline is fully correct.
(Keyword matching is a lightweight proxy, not a complete semantic
check — a passing result means "no known regression," not "provably
correct.")

❌ Unanswerable questions are a lower priority than answerable ones.
(They test the failure mode with the worst consequences — a
confidently wrong answer — and deserve at least equal weight in the
dataset.)

✔ Separating retrieval evaluation from answer evaluation tells you
*which stage* failed, the same value module 01 chapter 16's
per-stage logging brings to debugging a live pipeline.

## Interview Questions

1.  Why are retrieval and answer quality evaluated as two separate
    checks?
2.  What does a correctly grounded system do when asked something the
    source document doesn't cover?
3.  Why is keyword matching an acceptable, if imperfect, evaluation
    method here?
4.  Why does the evaluation dataset deliberately include unanswerable
    questions?

## Summary

This module's evaluator checks retrieval and answer quality as
separate signals against a real dataset covering direct, paraphrased,
multi-condition, and deliberately unanswerable questions — because a
model that never says "I don't know" is a bigger risk than one that
occasionally does. A passing evaluation run means no known regression,
not proof of correctness; it's a regression check, the same value an
eval set brings to prompt engineering in module 02.

## Next Chapter

➡️ `10-Debugging.md`
