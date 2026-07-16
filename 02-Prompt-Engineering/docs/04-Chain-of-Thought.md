# 04 - Chain-of-Thought Prompting

## Introduction

Module 01 chapter 17 flagged that LLMs are weak at precise, multi-step
logic because they predict plausible tokens rather than compute
answers. Chain-of-thought (CoT) prompting is the standard mitigation:
asking the model to show its reasoning step by step instead of jumping
straight to a conclusion — the same reason I ask an engineer to write
out their debugging steps instead of just stating a root cause, so
errors in the logic are visible before they turn into a wrong action.

## Learning Objectives

After this chapter I should be able to:

-   Explain why "think step by step" measurably improves accuracy on
    multi-step problems.
-   Write a chain-of-thought prompt for a diagnostic/reasoning task.
-   Know when CoT is worth the extra tokens and latency, and when it
    isn't.

------------------------------------------------------------------------

# Direct Answer vs. Chain-of-Thought

``` text
Direct:
  "A service handles 200 req/s. After a deploy it drops to 150 req/s
   with the same traffic. What's the most likely cause?"
  → "Increased latency per request." (plausible-sounding, unverified)

Chain-of-thought:
  "...Think through this step by step before giving your answer."
  → "1. Same traffic, lower throughput means requests are taking
       longer or failing.
     2. This happened right after a deploy, so the deploy is the
        prime suspect.
     3. Check: did the deploy change replica count, resource limits,
        or add a new dependency call?
     4. Most likely cause: the deploy reduced replica count or added
        blocking I/O per request.
     Recommendation: check `kubectl get deploy` for replica count
     first, then check for new synchronous calls in the diff."
```

Forcing intermediate steps onto the page gives the model's own
next-token predictions something more concrete to build on — each step
narrows the space of plausible continuations for the next one, instead
of asking for a conclusion in one uninformed leap.

**Platform analogy:** this is a postmortem template, not a Slack
message. Asking "what broke?" invites a guess. Asking someone to walk
through timeline → symptom → hypothesis → verification → conclusion
produces something you can actually check at each step and catch a bad
inference before it becomes the accepted root cause.

## Two Ways to Trigger It

**1. Explicit instruction** — just ask for it:

``` text
"Think through this step by step, then give your final answer on the
last line prefixed with 'Answer:'."
```

**2. Few-shot with reasoning shown** — combine with chapter 03, showing
worked examples that include the reasoning, not just the final answer:

``` text
Q: A pod is OOMKilled with a 512Mi limit. Memory usage graph shows a
   steady climb over 6 hours before the kill. What's the likely issue?
A: Steady climb over hours, not a sudden spike, suggests a memory
   leak rather than a traffic burst. Sudden spikes point to load;
   gradual climbs point to something not releasing memory over time.
   Likely issue: memory leak in the application.

Q: A pod is OOMKilled with a 512Mi limit. Memory usage graph shows a
   spike within 30 seconds of pod start, correlated with a batch job
   trigger. What's the likely issue?
A:
```

## When CoT Is Worth It (and When It Isn't)

  Task type                                CoT helps?
  ----------------------------------------- ------------------------
  Multi-step diagnosis / root-cause analysis Yes, significantly
  Math, capacity planning calculations        Yes, significantly
  Multi-constraint decisions (trade-offs)      Yes
  Simple factual lookup                         No — adds latency/cost for no gain
  Classification with a well-defined rule       Usually no — few-shot alone is enough

The cost is real: more output tokens (module 01 chapter 04) and more
latency (chapter 03), since every reasoning token is another forward
pass in the generation loop. Reserve it for the tasks where wrong
reasoning is actually the failure mode you're worried about — not every
prompt needs a visible thought process.

## Hands-on: Prove the Improvement to Yourself

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

problem = ("A rolling deploy replaces 10 pods, 2 at a time, waiting "
           "60s between batches, with a 30s readiness probe delay. "
           "How long, at minimum, before all 10 pods are updated?")

direct = f"{problem} Answer with just the number of seconds."
cot = f"{problem} Think through this step by step, then give the final answer as 'Answer: N seconds'."

for label, prompt in [("direct", direct), ("chain-of-thought", cot)]:
    r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0)
    print(f"--- {label} ---\n{r.choices[0].message.content}\n")
```

Work the math out by hand (5 batches × 60s wait, plus one 30s readiness
delay = 270s) and compare both answers against it. This is a great
example to keep in your back pocket — small arithmetic-adjacent
reasoning problems are exactly where direct answers go wrong most
visibly.

## Common Misconceptions

❌ Chain-of-thought makes the model "actually reason" the way a human
does.
(It's still next-token prediction — CoT just gives the model
intermediate tokens to condition on, which empirically improves
accuracy on multi-step problems without implying real understanding.)

❌ You should always ask for step-by-step reasoning, just in case.
(It costs tokens and latency on every call — reserve it for genuinely
multi-step or trade-off-heavy tasks, per the table above.)

✔ For anything resembling root-cause analysis or a multi-step
calculation, CoT is close to a free accuracy win relative to its cost —
for simple lookups, it's pure overhead.

## Interview Questions

1.  Why does asking a model to "think step by step" improve accuracy on
    multi-step problems?
2.  What's the cost of chain-of-thought prompting, and when does it
    outweigh the benefit?
3.  Name two ways to trigger chain-of-thought behavior in a prompt.
4.  Why is chain-of-thought analogous to requiring a postmortem
    template instead of accepting a one-line root cause?

## Summary

Chain-of-thought prompting asks the model to show intermediate
reasoning before a final answer, which measurably improves accuracy on
multi-step diagnostic and calculation tasks — at the real cost of more
output tokens and latency. Use it where wrong reasoning is the actual
risk (root-cause analysis, capacity math, trade-off decisions), and skip
it for simple lookups and well-defined classification.

## Next Chapter

➡️ `05-Role-and-System-Prompts.md`
