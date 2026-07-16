# 09 - Instruction Clarity and Constraints

## Introduction

Most of the earlier chapters showed *techniques*. This one is about
*wording discipline* — the small, boring changes to how an instruction
is phrased that measurably change output quality. This is the prompt
equivalent of writing clear acceptance criteria on a ticket instead of
"make it better" — vague input produces vague, unpredictable output,
regardless of how good the model is.

## Learning Objectives

After this chapter I should be able to:

-   Identify vague instructions and rewrite them as explicit
    constraints.
-   Use concrete constraints (length, format, scope) to reduce output
    variance.
-   Avoid instructions that quietly contradict each other.

------------------------------------------------------------------------

# Vague vs. Explicit, Side by Side

``` text
Vague:     "Keep it short."
Explicit:  "Respond in 2 sentences or fewer."

Vague:     "Explain this error."
Explicit:  "Explain this error in one paragraph, aimed at someone who
            knows Kubernetes but has never seen this specific error."

Vague:     "Format it nicely."
Explicit:  "Format as a markdown table with columns: Resource, Issue,
            Fix."
```

"Short," "nicely," "clearly" are all judgment calls the model has to
make on your behalf, without knowing your actual bar for any of them.
Every one of those judgment calls is a place output can drift between
calls — the direct cause of the "inconsistency across runs" limitation
from module 01 chapter 17, made worse by vague instructions on top of
inherent sampling variance.

**Platform analogy:** this is the exact same discipline as writing
acceptance criteria instead of a vague user story. "The page should
load fast" tells a developer nothing actionable; "The page should load
in under 2 seconds at p95" does. A model is in the same position as
that developer — it needs a concrete target, not an adjective.

## Constraints Are Cheap Insurance

Explicit constraints cost almost nothing to add and meaningfully reduce
output variance:

  Constraint type   Example
  ------------------ --------------------------------------------
  Length              "in 3 bullet points", "under 50 words"
  Format               "as a markdown table", "as valid JSON"
  Scope                "only syntax errors, not style suggestions"
  Tone                 "formal, no jokes", "for a junior engineer"
  Negative space        "do not include the word 'simply'"

## Watch for Self-Contradicting Instructions

Long prompts, especially ones edited over time by multiple people,
accumulate instructions that quietly conflict — the prompt equivalent of
config drift where two settings override each other unpredictably.

``` text
Contradictory:
  "Be extremely detailed and thorough. ... Keep your answer under
  two sentences."

Resolved:
  "In exactly 2 sentences, give the single most likely root cause
  and the one command to verify it."
```

When a prompt starts behaving unpredictably, re-reading it end to end
for contradictions is often more productive than trying more
temperature/sampling tweaks — the inconsistency is frequently coming
from the instructions themselves, not from the model.

## Hands-on: Rewrite for Variance Reduction

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

vague = "Explain what a Kubernetes readiness probe is."
explicit = ("Explain what a Kubernetes readiness probe is, in exactly "
            "2 sentences, for an engineer who knows Docker but is new "
            "to Kubernetes. Do not mention liveness probes.")

for label, prompt in [("vague", vague), ("explicit", explicit)]:
    outputs = []
    for _ in range(3):
        r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.7)
        outputs.append(r.choices[0].message.content.strip())
    print(f"--- {label} ({[len(o) for o in outputs]} chars across 3 runs) ---")
    for o in outputs:
        print(f"  {o[:80]}...")
```

Compare the spread of response lengths and content across the 3 runs
for each prompt. The explicit version should cluster much more tightly
— that clustering is the measurable value of clear constraints.

## Common Misconceptions

❌ Adding more instructions always improves the result.
(Past a point, more instructions just increase the odds of two of them
quietly contradicting each other — precision beats volume.)

❌ The model should be able to infer "reasonable" length/format/tone
on its own.
(It will infer *something* reasonable — just not necessarily the same
something you had in mind. State it.)

✔ Concrete, measurable constraints (word counts, explicit formats,
explicit exclusions) reduce output variance more reliably than lowering
temperature alone.

## Interview Questions

1.  Why does a vague instruction like "keep it short" lead to
    inconsistent output across calls?
2.  Give three types of constraints that reduce output variance.
3.  What should you check first when a long-lived prompt starts
    behaving unpredictably?
4.  Why is this discipline comparable to writing acceptance criteria on
    a ticket?

## Summary

Vague instructions leave judgment calls to the model, and every one of
those judgment calls is a place output can drift between calls.
Concrete, explicit constraints — length, format, scope, tone, negative
space — are cheap to add and directly reduce that variance, the same
way clear acceptance criteria reduce ambiguity in a ticket.

## Next Chapter

➡️ `10-Negative-Prompting-and-Pitfalls.md`
