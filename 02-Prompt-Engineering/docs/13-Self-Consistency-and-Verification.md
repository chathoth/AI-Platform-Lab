# 13 - Self-Consistency and Verification Prompts

## Introduction

Module 01 chapter 11 established that a model's confident tone tells
you nothing about correctness. This chapter covers two prompting
techniques that push back on that specific problem: asking the same
question multiple ways and checking for agreement, and asking the model
to check its own work. Neither is a substitute for real verification,
but both are cheap, practical ways to catch a wrong answer before it
ships — similar in spirit to running the same test suite against two
environments and comparing results.

## Learning Objectives

After this chapter I should be able to:

-   Explain self-consistency prompting and when it's worth the extra
    calls.
-   Write a verification pass that checks a model's own prior answer.
-   Recognize the limits of both techniques.

------------------------------------------------------------------------

# Self-Consistency: Ask Multiple Times, Check Agreement

Instead of trusting one response, sample the same prompt several times
(at nonzero temperature, per module 01 chapter 10) and take the
majority answer, or flag disagreement for human review.

``` python
from collections import Counter

def self_consistent_answer(client, model, prompt, n=5):
    answers = []
    for _ in range(n):
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        answers.append(r.choices[0].message.content.strip())

    counts = Counter(answers)
    top_answer, top_count = counts.most_common(1)[0]
    confidence = top_count / n
    return top_answer, confidence

answer, confidence = self_consistent_answer(
    client, MODEL, "Classify severity as LOW, MEDIUM, or HIGH: disk at 92% on a replica node."
)
print(f"Answer: {answer} (agreement: {confidence:.0%})")
```

Low agreement across samples (e.g. 2/5 say MEDIUM, 3/5 say HIGH) is a
genuinely useful signal — it means the question is ambiguous *to the
model*, which often means it's ambiguous, period, and worth a human
second opinion.

**Platform analogy:** this is a quorum/consensus check, the same
pattern behind leader election or distributed config agreement — no
single node is trusted blindly; agreement across multiple independent
attempts is what earns confidence.

## Verification Prompting: Ask It to Check Itself

A second, independent call asks the model to critique the *first*
model's answer, sometimes catching errors the original generation
missed — because generating an answer and evaluating one are different
tasks, and evaluating tends to be the easier of the two.

``` python
def generate_and_verify(client, model, question):
    draft = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": question}], temperature=0.3
    ).choices[0].message.content

    verify_prompt = f"""Question: {question}
Proposed answer: {draft}

Check this answer for factual errors or unsupported claims. Respond
with "VALID" if it's correct and well-supported, or explain the
specific problem if not."""

    verdict = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": verify_prompt}], temperature=0
    ).choices[0].message.content

    return draft, verdict
```

This is a specific application of prompt chaining (chapter 12) — one
call generates, a second call critiques — and it inherits the same
cost/latency trade-off: an extra round trip, in exchange for a chance
to catch an error before a human (or a downstream system) sees it.

## The Real Limits of Both Techniques

Neither technique catches every error, and it's important to be honest
about why: if the model has a **systematic** misunderstanding (a wrong
belief baked into its training, not a one-off sampling fluke), both
self-consistency and self-verification will agree with themselves
confidently and consistently. These techniques catch **noise**
(inconsistent, low-confidence errors) — they do not catch **bias**
(a consistently wrong belief). For that, you still need grounding
(RAG, module 01 chapter 14) or human review.

## Hands-on: Find a Question With Low Agreement

``` python
questions = [
    "What is 2 + 2?",  # expect near-100% agreement
    "Is 85% disk usage on a staging node LOW, MEDIUM, or HIGH severity?",  # genuinely ambiguous
]

for q in questions:
    answer, confidence = self_consistent_answer(client, MODEL, q, n=5)
    print(f"{q}\n  -> {answer} (agreement: {confidence:.0%})\n")
```

The second question should show noticeably lower agreement than the
first — that gap is the self-consistency signal doing its job.

## Common Misconceptions

❌ Self-consistency guarantees a correct answer.
(It surfaces disagreement/uncertainty in the model's own output — it
doesn't guarantee the majority answer is actually right, especially for
systematically wrong beliefs.)

❌ Asking a model to verify its own answer is redundant with generating
it.
(Generation and evaluation are different tasks — a second, differently
-framed call genuinely does catch some errors the first pass missed,
even though it's not foolproof.)

✔ Both techniques catch *inconsistent* errors well and *systematic*
errors poorly — know which failure mode you're actually worried about
before relying on either.

## Interview Questions

1.  How does self-consistency prompting work, and what does low
    agreement across samples actually tell you?
2.  Why can asking a model to verify its own prior answer catch errors
    the original generation missed?
3.  What kind of error do self-consistency and verification prompting
    fail to catch, and why?
4.  What's the cost of both techniques, and when is that cost worth
    paying?

## Summary

Self-consistency (sampling multiple times and checking agreement) and
verification prompting (a second call critiquing the first) are cheap,
practical ways to catch inconsistent, low-confidence errors before they
ship — quorum-style techniques, not guarantees. Neither catches a
systematic, confidently-wrong belief; that still requires grounding via
RAG or human review.

## Next Chapter

➡️ `14-Function-and-Tool-Calling-Prompts.md`
