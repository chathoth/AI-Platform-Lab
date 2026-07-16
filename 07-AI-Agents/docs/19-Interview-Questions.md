# 19 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with
the answer framed the way I'd actually say it. Review material — read
the chapters first.

------------------------------------------------------------------------

## Chapter 01 - What Is an AI Agent

**Q: What's the one-sentence test for whether something is an agent?**
Does the model decide what happens next based on what just happened,
more than once? If the whole sequence was fixed in advance, it isn't
an agent — it's a workflow or a single tool call.

## Chapter 02 - The Agent Loop

**Q: Why does the "observe" step matter more than it might seem?**
It's what the next reasoning step is actually built on — skip it, and
you're back to deciding everything up front, with no ability to react
to what actually happened.

## Chapter 03 - Agents vs. Chains vs. Fixed Workflows

**Q: What's the deciding question for choosing an agent over a fixed
workflow?**
Does the right next step genuinely depend on something you can't fully
predict ahead of time? If you already know the exact sequence, a fixed
workflow is simpler and cheaper.

## Chapter 04 - Agent Memory

**Q: What is short-term agent memory, concretely?**
The growing list of messages within one run — no more mysterious than
that, and the same statelessness-plus-resent-history mechanism
covered in modules 01 and 02.

## Chapter 05 - Planning

**Q: Why should a plan be treated as a draft, not a contract?**
The loop's observe step is what lets the agent correct course when
reality diverges from the plan — a good agent skips ahead or adjusts
rather than mechanically following a plan that's clearly wrong.

## Chapter 06 - Giving an Agent Tools

**Q: Why does tool description quality matter more for agents than
for a single tool call?**
An agent chooses among tools every turn — an ambiguous description
doesn't just risk one wrong call, it can steer several turns of
reasoning in the wrong direction.

## Chapter 07 - Building a Minimal Agent

**Q: What's the only genuinely new code in a basic agent loop,
compared to a single tool call?**
The `for` loop and the check for whether the model wants another tool
call or is ready to give a final answer — everything else reuses
module 02 chapter 14's pattern directly.

## Chapter 08 - One Tool at a Time (Verified)

**Q: What exactly went wrong, and why?**
A real test showed the agent restarted a service even though disk
usage was 41%, well under the 90% threshold — because it requested
both the check and the restart in the same turn, before it had
observed the check's result. Forcing one tool call per turn fixed it.

## Chapter 09 - Stopping Conditions

**Q: Why isn't a step limit alone sufficient?**
It bounds turn count but not cost, since the message history grows
every turn — a token/cost budget and repetition detection catch
failure modes a step count alone would miss.

## Chapter 10 - Reflection and Self-Correction

**Q: What kind of mistake does reflection catch well, and what does
it miss?**
It catches inconsistent, one-off slips reasonably well — it doesn't
reliably catch a systematic misunderstanding, since the same flawed
reasoning that caused the mistake can also produce a flawed reflection
that says everything was fine.

## Chapter 11 - Multi-Agent Systems

**Q: Why should a single agent be the default, not multiple agents?**
More agents add coordination complexity and cost — worth it only once
a single agent's tool set or responsibilities have genuinely grown too
broad to reason about reliably.

## Chapter 12 - Orchestration Patterns

**Q: What's the core difference between supervisor and pipeline
patterns?**
A supervisor dynamically routes each request to the right worker; a
pipeline runs every request through the same fixed sequence of agent
stages.

## Chapter 13 - Guardrails and Human-in-the-Loop

**Q: Why can't a guardrail live only in the prompt?**
The model is predicting plausible tokens, not executing a guaranteed-
correct decision procedure — chapter 08 proved a well-built loop can
still make a wrong call. Enforcement has to live in code the model
can't talk its way around.

## Chapter 14 - Observability

**Q: Why couldn't chapter 08's bug be found from the final answer
alone?**
The final answer sounded reasonable on its own — only a full,
turn-by-turn trace revealed that the restart happened before the
disk-usage result had actually been checked against the threshold.

## Chapter 15 - Evaluating Agent Performance

**Q: What should an agent eval set score against?**
The actual actions taken (tools called, in what sequence), not just
whether the final answer sounds reasonable — chapter 08's exact
failure proved those two things can disagree.

## Chapter 16 - Common Failure Modes

**Q: Why are agent failures predictable rather than random?**
Each one traces to an identifiable mechanism — skipped observation,
missing stopping conditions, ambiguous tools, unchecked context
growth, untrusted tool results, or unreviewed cumulative risk — not a
mysterious model quirk.

## Chapter 17 - Cost and Latency

**Q: Why does an agent's cost grow faster than linearly with turn
count?**
Every turn resends the accumulated message history (module 02 chapter
11's mechanism), so later turns cost more than earlier ones, not just
the same amount repeated.

## Chapter 18 - Best Practices

**Q: Which practice in this checklist is backed by a directly
verified finding?**
Forcing one tool call at a time — chapter 08 reproduced a real
incorrect action caused by batching, and confirmed the fix resolves
it.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  Agent — decides what's next based on what just happened, more
    than once.
2.  Loop — reason, act, observe, repeat.
3.  Chain vs. agent — fixed sequence vs. model-decided sequence.
4.  Memory — short-term is a message list; long-term is a retrieval
    problem.
5.  Planning — a draft, not a contract.
6.  Tools — same pattern as module 02, chosen repeatedly instead of
    once.
7.  One tool call per turn — the single most important verified
    lesson in this module.
8.  Stopping conditions — step limit, token budget, repetition
    detection.
9.  Reflection — catches noise, not systematic bias.
10. Multi-agent — the exception, not the default.
11. Guardrails — allowlist + confirmation gate, in code, not just
    prompt.
12. Tracing — every step, not just the final answer.
13. Evaluation — score actions, not tone.

## Next Chapter

➡️ `20-Glossary.md`
