# 10 - Negative Prompting and Common Pitfalls

## Introduction

"Negative prompting" — telling the model what *not* to do — sounds like
it should work as cleanly as a positive instruction. In practice it's
one of the more counterintuitive corners of prompting, and this chapter
is a punch list of the specific ways it goes wrong, learned the way
most ops lessons are learned: by watching something misbehave first.

## Learning Objectives

After this chapter I should be able to:

-   Explain why "don't do X" is less reliable than "do Y instead."
-   Identify common prompting anti-patterns before they cause problems.
-   Rewrite a negative instruction as a positive one where possible.

------------------------------------------------------------------------

# Why "Don't" Is Weaker Than "Do"

``` text
Weaker:  "Don't use jargon."
Stronger: "Use plain language a non-technical stakeholder could follow."

Weaker:  "Don't make up information."
Stronger: "If the answer isn't in the provided context, say 'I don't
           have that information' instead of guessing."

Weaker:  "Don't be verbose."
Stronger: "Respond in 2-3 sentences."
```

A pure negative instruction ("don't do X") tells the model what to
avoid but not what to produce instead — it still has to fill that space
with *something*, and it can fill it with an equally undesired
alternative. A positive instruction ("do Y") gives it a concrete target
to aim at directly.

**Platform analogy:** this is the difference between a linter rule that
just flags `no-console` and one that also auto-fixes to a proper
logger call. Just saying "don't" leaves a gap the model — or the
developer — has to fill in on their own, often inconsistently. Telling
it what to do instead closes that gap.

## When Negative Instructions Do Help

Negative instructions aren't useless — they're most reliable for
**hard exclusions**, not vague quality judgments:

``` text
Works well:   "Never suggest running `rm -rf` or any destructive
               command without explicitly labeling it DESTRUCTIVE."
Works poorly: "Don't be unhelpful."
```

The first is a concrete, checkable rule. The second is just a vaguer
version of "be helpful" stated backwards — it doesn't add any new
information the model can act on.

## Common Pitfalls Checklist

  Pitfall                             Fix
  ------------------------------------ ---------------------------------------------
  Pure negative instructions            Pair with a positive alternative
  Burying the real instruction in a wall of text | Put the critical instruction first or last (recall "lost in the middle," module 01 ch. 09)
  Assuming the model remembers earlier context perfectly | Restate critical constraints near the actual question
  One prompt trying to do five unrelated things | Split into separate calls (chapter 12: prompt chaining)
  Testing only the happy path                          | Test with malformed, empty, and adversarial input too

## Hands-on: Rewrite Negative Instructions

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

negative = "Summarize this incident. Don't be too technical."
positive = "Summarize this incident in plain language a non-technical stakeholder could understand, avoiding acronyms."

incident = "Pod evicted due to node memory pressure after a sidecar container leaked file descriptors."

for label, instruction in [("negative", negative), ("positive", positive)]:
    prompt = f"{instruction}\n\nIncident: {incident}"
    r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.3)
    print(f"--- {label} ---\n{r.choices[0].message.content}\n")
```

Check whether the "negative" version still slips in jargon like
"eviction" or "file descriptors" unexplained — that's the gap a purely
negative instruction leaves open.

## Common Misconceptions

❌ Negative instructions never work.
(They work well for hard, checkable exclusions — "never do X." They
work poorly as a substitute for describing what you actually want.)

❌ A longer, more detailed prompt is automatically more reliable.
(A prompt trying to enforce five unrelated rules at once is more likely
to have the model drop one of them — split unrelated concerns into
separate calls, per chapter 12.)

✔ Wherever possible, replace "don't do X" with "do Y" — it gives the
model a concrete target instead of an empty space to fill in on its
own.

## Interview Questions

1.  Why is "do Y instead" generally more reliable than "don't do X"?
2.  When are negative instructions actually the right tool?
3.  Why does burying the critical instruction in the middle of a long
    prompt cause problems?
4.  What's the fix for a prompt trying to accomplish five unrelated
    things at once?

## Summary

Negative instructions leave a gap for the model to fill in on its own,
which it can fill inconsistently — positive instructions with a
concrete target are more reliable, except for hard, checkable
exclusions like "never suggest a destructive command." Combined with
the other common pitfalls (burying instructions, doing too much in one
prompt), this is the checklist to run through before blaming the model
for inconsistent output.

## Next Chapter

➡️ `11-Multi-Turn-Conversation-Design.md`
