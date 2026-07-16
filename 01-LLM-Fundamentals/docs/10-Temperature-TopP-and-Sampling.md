# 10 - Temperature, Top-P, and Sampling

## Introduction

These are the parameters I actually touch on every API call, so this
chapter is the most immediately practical one so far. I think of
temperature/top-p as **chaos engineering dials** — they control how much
controlled randomness gets injected into an otherwise deterministic-ish
process, similar to how I'd tune retry jitter or load-balancing
randomness.

## Learning Objectives

After this chapter I should be able to:

-   Explain how a token gets picked from the probability distribution
    described in chapter 03.
-   Explain temperature and its effect on output randomness.
-   Explain top-p (nucleus sampling) and how it differs from
    temperature.
-   Choose sane defaults for a given use case (deterministic ops
    tooling vs. creative writing).

------------------------------------------------------------------------

# From Probabilities to a Chosen Token

Recall from [03-How-LLMs-Work.md](03-How-LLMs-Work.md): at each step,
the model outputs a probability distribution over its entire vocabulary
for "what comes next."

``` text
Prompt: "The deployment failed because the"

Model's probability distribution for the next token:
  "pod"        → 34%
  "image"      → 21%
  "config"     → 18%
  "container"  → 12%
  "server"     → 8%
  ... (long tail of thousands of other tokens)
```

**Greedy decoding** always picks the single highest-probability token
(`"pod"`, every time — fully deterministic). **Sampling** instead picks
*probabilistically* from that distribution, which is where temperature
and top-p come in.

## Temperature: How "Flat" the Distribution Gets

Temperature reshapes the probability distribution before sampling.

  Temperature   Effect                              Distribution shape
  ------------- ------------------------------------ -------------------------
  0.0           Always pick the top token (greedy)   Fully deterministic
  0.3-0.5       Mostly favors likely tokens           Slightly flattened
  0.7-1.0       Balanced randomness                   Noticeably flattened
  1.5+          High randomness, more "creative"      Very flat, near-uniform

``` text
temperature=0.0  →  "pod" always wins → same output every time
temperature=1.5  →  "server" or even a low-probability token might get picked
```

**Platform analogy:** temperature is a jitter setting. `temperature=0`
is a fixed retry delay — fully predictable, but can get "stuck" in
repetitive patterns (a model at temp 0 sometimes loops on the same
phrase). `temperature=0.7+` is exponential-backoff-with-jitter — adds
useful variability, at the cost of losing strict reproducibility between
runs.

## Top-P (Nucleus Sampling): A Different Kind of Limit

Instead of reshaping the whole distribution, top-p restricts sampling to
the smallest set of tokens whose cumulative probability reaches `p`.

``` text
top_p = 0.9 means: keep adding tokens (highest probability first)
until their probabilities sum to 90%, then sample only from that set.

"pod" (34%) + "image" (21%) + "config" (18%) + "container" (12%) = 85%
+ "server" (8%) = 93% → cumulative crosses 90%, so these 5 tokens
form the sampling pool. Everything else (the long tail) is excluded.
```

**Platform analogy:** top-p is a percentile-based cutoff, like alerting
on p90/p99 latency instead of a fixed millisecond threshold. It adapts
to the shape of the distribution automatically — when the model is very
confident (one token dominates), the pool stays small even at
`top_p=0.9`; when it's uncertain (flat distribution), the pool naturally
grows.

Most APIs let you set both `temperature` and `top_p` — in practice I
pick one to actually tune and leave the other at its default, since
stacking both makes behavior harder to reason about.

## Hands-on: See the Same Prompt Diverge

``` bash
for t in 0.0 0.7 1.3; do
  echo "--- temperature=$t ---"
  curl -s http://localhost:11434/api/generate -d "{
    \"model\": \"llama3.1:8b\",
    \"prompt\": \"Write a one-line commit message for fixing a null pointer bug\",
    \"options\": {\"temperature\": $t},
    \"stream\": false
  }" | python3 -c "import json,sys; print(json.load(sys.stdin)['response'])"
done
```

Run it a few times at each temperature. At `0.0` you should get the
(near) exact same output every run. At `1.3`, real variation. This is
the practical test I'd run before picking a default for any automated
pipeline (e.g. auto-generating commit messages, summarizing PRs) — I
want `temperature=0` or very low for anything that needs to be
consistent/testable, and higher only where variety is actually the goal.

## Choosing Settings for Real Use Cases

  Use case                              Recommended setting
  -------------------------------------- ---------------------------
  Generating structured output/JSON      `temperature=0`
  Summarizing logs/incidents             `temperature=0.2-0.3`
  Code generation                        `temperature=0.2-0.5`
  Chat assistant                         `temperature=0.7`
  Brainstorming / creative writing       `temperature=0.9-1.2`

## Common Misconceptions

❌ `temperature=0` guarantees byte-for-byte identical output every time.
(It's close to deterministic, but floating-point/hardware batching
differences can still cause tiny variations across runs on some
providers — don't build tests that assume perfect reproducibility.)

❌ Higher temperature makes the model "smarter" or "more thoughtful."
(It only makes output *more random* — it doesn't add reasoning ability,
and past a point it actively degrades coherence.)

✔ For anything you'd call from a script or pipeline and need consistent,
parseable output from — keep temperature low. Save higher temperature
for human-facing, exploratory use.

## Interview Questions

1.  What does `temperature=0` do to the token selection process?
2.  How does top-p (nucleus sampling) differ from temperature?
3.  Why would you want low temperature for a script that auto-generates
    structured output, but higher temperature for a brainstorming
    assistant?
4.  Is `temperature=0` fully deterministic in practice? Why or why not?

## Summary

Temperature and top-p both control how the model samples a token from
its probability distribution — temperature reshapes the whole
distribution's "flatness," top-p cuts it off at a cumulative-probability
percentile. Treat them like jitter/backoff tuning: low for anything that
needs to be predictable and scriptable, higher only where variety is
the actual goal.

## Next Chapter

➡️ `11-Hallucinations.md`
