# 16 - Evaluating Prompt Quality

## Introduction

Every technique so far has been about writing a better prompt. This
chapter is about proving it's actually better — the same discipline as
having a test suite instead of eyeballing whether a code change "looks
right." Without an eval set, "I improved the prompt" is just a feeling;
with one, it's a measurable, regression-testable claim.

## Learning Objectives

After this chapter I should be able to:

-   Build a small evaluation dataset for a prompting task.
-   Score prompt variants objectively instead of by impression.
-   Recognize when a "prompt improvement" is actually a regression on
    cases you didn't check.

------------------------------------------------------------------------

# Why "It Looks Better to Me" Isn't Enough

A prompt change that fixes the one example you were staring at can
easily break three other cases you weren't looking at — the prompt
equivalent of a code fix that passes the one manual test you ran and
breaks two others you didn't think to check. Without a fixed set of
test cases and a way to score them, there's no way to catch that.

## Building a Minimal Eval Set

An eval set is just labeled examples: input, and the expected (or
acceptable) output.

``` python
eval_set = [
    {"input": "CPU at 45% on web-node-01", "expected": "LOW"},
    {"input": "Disk at 98% on db-primary-01, 5 minutes to full", "expected": "HIGH"},
    {"input": "Memory at 78% on cache-node-03", "expected": "MEDIUM"},
    {"input": "Disk at 92% on a REPLICA db node", "expected": "MEDIUM"},  # the tricky one from chapter 08
    {"input": "5xx error rate at 0.01%", "expected": "LOW"},
]
```

Deliberately include the edge cases that made you write the prompt
carefully in the first place — those are exactly the cases most likely
to regress silently when the prompt changes later.

## Scoring Two Prompt Variants

``` python
def evaluate_prompt(client, model, prompt_template, eval_set):
    correct = 0
    failures = []
    for case in eval_set:
        prompt = prompt_template.format(alert=case["input"])
        r = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=0)
        answer = r.choices[0].message.content.strip().upper()
        if answer == case["expected"]:
            correct += 1
        else:
            failures.append((case["input"], case["expected"], answer))
    accuracy = correct / len(eval_set)
    return accuracy, failures

v1 = "Classify severity as LOW, MEDIUM, or HIGH: {alert}"
v2 = "You are an SRE. Classify severity as LOW, MEDIUM, or HIGH. Disk >90% on a PRIMARY is HIGH; on a REPLICA is MEDIUM.\nAlert: {alert}"

for label, template in [("v1", v1), ("v2", v2)]:
    accuracy, failures = evaluate_prompt(client, MODEL, template, eval_set)
    print(f"{label}: {accuracy:.0%} accuracy")
    for input_text, expected, got in failures:
        print(f"  MISS: '{input_text}' expected {expected}, got {got}")
```

Now "v2 is better" is a number, not a feeling — and the failure list
tells you exactly which case still needs work, the same way a failing
test's assertion message tells you exactly what broke.

**Platform analogy:** this is a regression test suite for a prompt.
Every prompt change is a diff; the eval set is what tells you whether
the diff is an improvement or a silent regression on a case you weren't
looking at.

## What to Measure Beyond Raw Accuracy

  Metric                       Why it matters
  ------------------------------ ------------------------------------------
  Accuracy against labels         The baseline signal
  Consistency across repeated runs Ties to module 01 ch. 10 - low temperature helps, but check it
  Format compliance                Did it actually return valid JSON/the right label, every time? (chapter 06)
  Latency / token cost              A more accurate prompt that's 3x slower/pricier may not be a net win

## Hands-on: Catch a Regression

Take the `v2` prompt above, "improve" it by adding an unrelated
instruction ("also explain your reasoning in detail"), and re-run the
eval. Check whether accuracy holds, output format breaks (now it's not
just the single word LOW/MEDIUM/HIGH), or latency changes meaningfully
— a very typical way a well-intentioned prompt edit introduces a
regression nobody would catch without a fixed eval set.

## Common Misconceptions

❌ A handful of manual spot-checks is a sufficient eval process.
(Spot checks reproduce your existing blind spots — a fixed eval set,
especially one seeded with known edge cases, catches what you weren't
already thinking to check.)

❌ Higher accuracy on the eval set is the only thing that matters.
(Format compliance, consistency, and cost all matter too — an
"improvement" that triples latency or breaks JSON output some of the
time isn't a clean win.)

✔ An eval set turns prompt changes from subjective judgment calls into
testable, comparable, regression-checkable diffs — exactly like a unit
test suite for code.

## Interview Questions

1.  Why is "it looks better to me" an insufficient way to validate a
    prompt change?
2.  What should a minimal eval set for a classification prompt contain?
3.  Beyond raw accuracy, name two other things worth measuring when
    comparing prompt variants.
4.  Why should an eval set deliberately include known edge cases?

## Summary

Evaluating a prompt means scoring it against a fixed, labeled set of
inputs — including the edge cases that made the prompt tricky in the
first place — rather than trusting a subjective impression. This turns
prompt iteration into something testable and regression-checkable,
exactly the discipline a unit test suite brings to code.

## Next Chapter

➡️ `17-Prompt-Versioning.md`
