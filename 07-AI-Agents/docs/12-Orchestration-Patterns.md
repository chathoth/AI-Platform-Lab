# 12 - Orchestration Patterns

## Introduction

Chapter 11 said multiple agents need coordination. This chapter covers
the two most common shapes that coordination takes — worth knowing by
name, since they show up constantly in agent frameworks (module 09)
under exactly these terms.

## Learning Objectives

After this chapter I should be able to:

-   Describe the supervisor pattern and the pipeline pattern.
-   Explain who decides what happens next in each pattern.
-   Choose between them for a given multi-agent task.

------------------------------------------------------------------------

# Supervisor Pattern: One Agent Directs Others

``` text
Supervisor agent
   |-- decides which worker agent handles this request
   |
   v
Worker agent A (diagnosis)   Worker agent B (remediation)   Worker agent C (reporting)
```

A supervisor agent's job is routing and coordination — it looks at the
task, decides which worker agent(s) should handle it, and combines
their results. This is chapter 11's "split by role" pattern with an
explicit coordinator added on top.

``` python
def supervisor(goal: str) -> str:
    routing_decision = ask_model(f"Given this goal, should it go to the diagnosis, remediation, or reporting agent? Goal: {goal}")
    if "diagnosis" in routing_decision:
        return diagnosis_agent(goal)
    elif "remediation" in routing_decision:
        return remediation_agent(goal)
    else:
        return reporting_agent(goal)
```

**Platform analogy:** this is a load balancer with routing logic — one
component's whole job is deciding which backend handles a given
request, without doing the actual work itself.

## Pipeline Pattern: Agents in a Fixed Sequence

``` text
Investigate agent -> Propose-fix agent -> Approval gate -> Execute agent
```

Each agent's output becomes the next agent's input, in a fixed order —
chapter 11's "split by step" pattern. Unlike the supervisor pattern,
there's no dynamic routing decision; the sequence itself is fixed,
even though each individual stage is a full agent (not just a single
prompt, which is what made module 02 chapter 12's chaining pattern
simpler).

``` python
def pipeline(goal: str) -> str:
    findings = investigate_agent(goal)
    proposed_fix = propose_fix_agent(findings)
    if not human_approves(proposed_fix):   # chapter 13's guardrail, made concrete
        return "fix proposed but not approved - no action taken"
    return execute_agent(proposed_fix)
```

## Choosing Between Them

  Factor                              Supervisor                          Pipeline
  --------------------------------------- ------------------------------------- --------------------------------------
  Which task goes where                     Decided dynamically, per request        Fixed in advance
  Good fit for                                Varied requests needing different handling | A consistent multi-stage process every request goes through
  Predictability                                Lower - routing itself is a judgment call  Higher - the sequence never changes

## Both Patterns Still Rest on Chapter 02's Loop

Worth remembering: whether it's a supervisor routing between workers or
a pipeline handing off between stages, **each individual agent** in
that system is still just chapter 02's reason-act-observe loop,
chapter 07's code, chapter 08's reliability lesson, and chapter 09's
stopping conditions, all still applying at the level of any one agent
in the system. Orchestration adds a layer on top; it doesn't replace
what's underneath.

## Hands-on: Sketch, Don't Necessarily Build

Take a realistic multi-step ops task — "investigate an incident, draft
a remediation plan, get it approved, then execute it" — and sketch
which pattern fits: is the sequence always the same (pipeline), or does
routing depend on what kind of incident it is (supervisor, or a
combination of both)? This is worth doing on paper before writing any
multi-agent code, since the pattern choice shapes the whole design.

## Common Misconceptions

❌ Supervisor and pipeline patterns are mutually exclusive.
(A supervisor can route to a pipeline, and a pipeline stage can itself
be a supervisor over several workers — they combine naturally for
more complex systems.)

❌ Orchestration replaces the need for each agent's own loop design.
(Every agent inside a supervisor or pipeline is still built from
chapters 02-10's foundations — orchestration is an additional layer,
not a substitute.)

✔ Choose supervisor when routing itself is a judgment call that varies
by request; choose pipeline when every request goes through the same
fixed sequence of stages.

## Interview Questions

1.  What's the core difference between the supervisor and pipeline
    patterns?
2.  Who decides "what happens next" in each pattern?
3.  Can the two patterns be combined? Give an example.
4.  Why does chapter 02's loop still matter inside a multi-agent
    system?

## Summary

The supervisor pattern has one agent dynamically route requests to
specialized workers; the pipeline pattern runs agents through a fixed
sequence of stages. Both are coordination layers on top of the same
foundation — each individual agent inside either pattern is still
built from the reason-act-observe loop and everything else covered in
chapters 02 through 10.

## Next Chapter

➡️ `13-Guardrails-and-Human-in-the-Loop.md`
