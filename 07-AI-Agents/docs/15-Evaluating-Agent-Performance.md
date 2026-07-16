# 15 - Evaluating Agent Performance

## Introduction

Module 02 chapter 16 and module 03 chapter 16 both built eval sets
instead of trusting "it looked right." This chapter is the same
discipline for agents — and chapter 08's failure is the perfect
motivating example: without a real eval set, that exact mistake could
easily have shipped, because it happened on only one of two very
similar-looking test cases.

## Learning Objectives

After this chapter I should be able to:

-   Build a small eval set for an agent, with known correct outcomes.
-   Score an agent run against expected actions, not just a "looks
    reasonable" final answer.
-   Explain why edge cases (like chapter 08's) belong in the eval set
    deliberately.

------------------------------------------------------------------------

# Why "The Final Answer Sounds Right" Isn't Enough

Chapter 08's incorrect run produced a final answer that, read on its
own, sounds perfectly reasonable: *"there's no need to take further
actions... restarted as a precautionary measure."* Read carelessly,
that could pass a casual review. Only checking the **actual actions
taken** against the **actual condition** catches the real bug — the
same "verify structure, not just tone" lesson as module 01 chapter 11's
warning that confident tone and correctness are uncorrelated.

## A Minimal Agent Eval Set

``` python
eval_cases = [
    {
        "goal": "Check disk usage on db-primary-01, and if it is above 90%, restart the cleanup-service.",
        "expected_tools_called": ["get_disk_usage", "restart_service"],  # condition IS met - should restart
    },
    {
        "goal": "Check disk usage on web-node-01, and if it is above 90%, restart the cleanup-service.",
        "expected_tools_called": ["get_disk_usage"],  # condition NOT met - should NOT restart
    },
]
```

Notice the second case is exactly chapter 08's scenario — deliberately
included because it's the case a naive agent gets wrong, the same
reason module 02 chapter 16 recommends seeding an eval set with the
tricky cases that motivated writing careful logic in the first place.

## Scoring Against Actual Actions Taken

``` python
def score_agent(run_agent_fn, eval_cases: list[dict]) -> tuple[float, list[dict]]:
    correct = 0
    failures = []
    for case in eval_cases:
        _, trace = run_agent_fn(case["goal"])
        tools_called = [t["tool"] for t in trace if t["type"] == "tool_call"]
        if tools_called == case["expected_tools_called"]:
            correct += 1
        else:
            failures.append({"goal": case["goal"], "expected": case["expected_tools_called"], "actual": tools_called})
    return correct / len(eval_cases), failures
```

Run this against chapter 07's original agent and chapter 08's fixed
version — the score should measurably improve, turning "the fix
helped" from a felt impression into a number, the same value module 02
chapter 16 already established for prompt evaluation.

## What to Measure Beyond "Did It Call the Right Tools"

  Metric                              Why it matters
  --------------------------------------- --------------------------------------
  Correct actions taken (above)              The core correctness signal
  Number of steps to completion                 Efficiency — did it take a reasonable path?
  Whether it stopped cleanly or hit `max_steps` | Chapter 09's stopping conditions actually working
  Cost/latency per run (chapter 17)               Whether it's affordable to run at scale

## Hands-on: Measure the Chapter 08 Fix, Don't Just Trust It

Using the eval set above, run `score_agent()` against both the
original agent (chapter 07) and the fixed one (chapter 08). Confirm the
score goes from 1/2 (the unfixed version gets the `db-primary-01` case
right by luck, but fails `web-node-01`) to 2/2 — a measured
confirmation of the fix, not just a single anecdotal test.

## Common Misconceptions

❌ If an agent's final answer sounds reasonable, it probably did the
right thing.
(Chapter 08's exact failure produced a reasonable-sounding final
answer despite taking a genuinely wrong action — score the actions,
not just the summary.)

❌ A single passing test case means the agent is reliable.
(Chapter 08's bug only showed up on one of two very similar cases — an
eval set needs multiple cases, deliberately including the tricky ones,
to actually catch this class of problem.)

✔ Seed the eval set with the exact case that exposed a real bug
(chapter 08's `web-node-01` scenario) — that's the single highest-value
test case an eval set can contain, because it's proven to catch a real
regression.

## Interview Questions

1.  Why wasn't chapter 08's incorrect run obviously wrong just from
    reading its final answer?
2.  What should an agent eval set score against, beyond the final
    answer text?
3.  Why does the eval set specifically need chapter 08's `web-node-01`
    case, not just the straightforward `db-primary-01` case?
4.  Name two metrics worth tracking beyond raw correctness.

## Summary

Evaluating an agent means scoring its actual actions against known
correct outcomes, not judging whether its final answer sounds
reasonable — chapter 08's exact failure proved a wrong action can still
produce a plausible-sounding summary. An eval set should deliberately
include edge cases like that one, since they're what actually catch a
regression before it reaches production.

## Next Chapter

➡️ `16-Common-Failure-Modes.md`
