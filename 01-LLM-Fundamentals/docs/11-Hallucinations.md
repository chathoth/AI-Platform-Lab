# 11 - Hallucinations

## Introduction

Hallucination is the failure mode I have to design *around* the most,
because unlike a service crash, it doesn't look like a failure — it
looks like a confident, well-formatted, completely plausible answer
that happens to be wrong. In ops terms, this is the scariest kind of
bug: no error code, no non-zero exit status, no stack trace. Just a
wrong answer delivered with full confidence.

## Learning Objectives

After this chapter I should be able to:

-   Define hallucination and explain why it's an inherent property of
    how LLMs generate text, not a rare bug.
-   Identify common hallucination patterns (fake APIs, fake citations,
    fabricated facts).
-   Explain concrete mitigations: RAG, grounding, verification steps,
    lower temperature.
-   Design a system that treats LLM output like untrusted input.

------------------------------------------------------------------------

# Why Hallucinations Happen

Recall from chapter 03: the model isn't looking anything up — it's
predicting the statistically most plausible next token, based on
patterns learned during training. It has no built-in mechanism to say
"I don't actually know this." If the most plausible-sounding continuation
of `"the AWS API method for listing S3 buckets is"` is a token sequence
that *looks* like a real method name but isn't, the model will produce
it just as confidently as it would produce a real one.

``` text
Prompt: "What's the kubectl flag to force-delete a stuck pod?"

Correct:    kubectl delete pod <name> --grace-period=0 --force
Hallucinated: kubectl delete pod <name> --force-terminate
                                          ^^^^^^^^^^^^^^^^ sounds plausible, doesn't exist
```

**Platform analogy:** this is the LLM equivalent of a service that
returns HTTP 200 with a wrong body instead of a 4xx/5xx error. There's
no signal in the response shape telling you something went wrong — you
have to validate the *content*, not just check that the call succeeded.
That single fact should drive every design decision downstream of an
LLM call in a system I'm responsible for.

## Common Hallucination Patterns

-   **Fabricated APIs/flags** — plausible-sounding CLI flags, function
    names, or config keys that don't exist (the example above).
-   **Fake citations/sources** — confidently generated URLs, paper
    titles, or docs links that look real but 404.
-   **Confident wrong facts** — dates, version numbers, statistics
    stated with no hedging.
-   **Outdated knowledge presented as current** — the model's training
    data has a cutoff; it can't know about a tool version or CVE
    released after that date, but won't necessarily say so.

## Mitigations, Ranked by What I'd Actually Reach For

1.  **Grounding / RAG** — give the model the actual source document
    (real API docs, your real runbook) in the prompt instead of relying
    on its trained-in memory. Covered in
    [14-Fine-Tuning-vs-RAG.md](14-Fine-Tuning-vs-RAG.md). This is the
    single highest-leverage fix — same principle as "don't trust cached
    state, read from the source of truth."
2.  **Lower temperature** (chapter 10) — reduces (but does not
    eliminate) creative/fabricated output for factual tasks.
3.  **Ask for citations, then verify them** — force the model to point
    at *where* in the provided context it got an answer, and treat
    ungrounded claims with suspicion.
4.  **Verification step in the pipeline** — for anything that will
    actually run (a generated `kubectl` command, a generated SQL
    query), validate/dry-run it before executing, the same way you
    wouldn't apply an unreviewed Terraform plan straight to prod.
5.  **Structured output + schema validation** — constrain the model to
    a JSON schema and validate the response before using it downstream,
    treating it like any other untrusted API response.

## Hands-on: Trigger and Catch a Hallucination

``` bash
# ask about something very likely to be outdated or obscure
ollama run llama3.1:8b "What is the exact flag to enable the 'ExperimentalGangScheduling' feature gate added in Kubernetes 1.34?"
```

Cross-check the answer against the real Kubernetes changelog/docs.
Small/older local models hallucinate on obscure or very recent details
far more readily than large hosted models — this is a good way to build
a gut sense for how much to trust a given model's output on niche
technical facts before you ever put it in a pipeline that executes
commands unattended.

``` python
# a minimal "verify before execute" pattern
suggested_cmd = "kubectl delete pod my-pod --force-terminate"

ALLOWED_FLAGS = {"--grace-period", "--force", "--namespace", "-n"}
flags_used = [f.split("=")[0] for f in suggested_cmd.split() if f.startswith("-")]

if not all(f in ALLOWED_FLAGS for f in flags_used):
    raise ValueError(f"Refusing to run - unrecognized flag(s) in: {suggested_cmd}")
```

## Common Misconceptions

❌ Hallucination is a bug that will get fixed in the next model version.
(It's a fundamental consequence of next-token prediction without a
built-in fact-checking mechanism — newer/bigger models hallucinate
*less often*, but the failure mode doesn't go away entirely.)

❌ If the model sounds confident, it's probably right.
(Confidence of *tone* and correctness of *content* are completely
uncorrelated in LLM output — this is the opposite of how most
engineers are trained to read error signals.)

✔ The reliable fix isn't "trust it more" or "trust it less" uniformly —
it's grounding the model in real source data (RAG) and verifying
anything that will actually be executed, exactly like you'd treat any
other untrusted input.

## Interview Questions

1.  Why do LLMs hallucinate — what's the root cause in how they
    generate text?
2.  Why is hallucination a more dangerous failure mode than a typical
    5xx error?
3.  What's the highest-leverage mitigation for reducing hallucination
    on factual questions, and why?
4.  How would you design a pipeline that lets an LLM suggest a shell
    command, without letting a hallucinated flag actually run in
    production?

## Summary

Hallucination isn't a rare glitch — it's the direct, expected
consequence of a model predicting plausible next tokens with no
built-in ground truth to check against. The fix isn't blind trust or
blind distrust; it's grounding answers in real source data (RAG) and
treating any LLM output that will be executed or acted on as untrusted
input requiring validation, exactly like any other external API
response.

## Next Chapter

➡️ `12-Model-Parameters.md`
