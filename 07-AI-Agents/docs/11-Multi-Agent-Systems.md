# 11 - Multi-Agent Systems

## Introduction

Everything so far has been one agent, one loop. This chapter covers
why (and when) to split that into several agents working together —
and, matching this module's honest tone, why that's usually a later
step, not a starting point.

## Learning Objectives

After this chapter I should be able to:

-   Explain why multiple agents are sometimes used instead of one.
-   Describe the difference between splitting by role and splitting by
    step.
-   Recognize when a single, well-designed agent is actually the
    better choice.

------------------------------------------------------------------------

# Why Split One Agent Into Several

A single agent juggling too many different responsibilities and tools
tends to get worse at all of them — the same reason module 06 chapter
06's tool-description advice gets harder to follow as a tool list
grows. Splitting into multiple agents, each with a narrower job and a
smaller, more focused tool set, is one way to keep each individual
agent's reasoning simpler and more reliable.

``` text
One overloaded agent:
  tools: get_disk_usage, restart_service, query_incident_db,
         send_slack_message, create_jira_ticket, check_deploy_history
  -> the model has to correctly choose among 6 tools every turn,
     for very different kinds of tasks

Multiple focused agents:
  Diagnosis agent:  get_disk_usage, check_deploy_history, query_incident_db
  Remediation agent: restart_service
  Reporting agent:    send_slack_message, create_jira_ticket
  -> each agent chooses among 2-3 closely related tools
```

## Two Ways to Split

``` text
By ROLE:  each agent has a distinct area of expertise (diagnosis vs.
           remediation vs. reporting) - closer to a team of
           specialists

By STEP:   each agent handles one stage of a larger pipeline
            (investigate -> propose a fix -> get approval -> execute)
            - closer to module 02 chapter 12's chaining, but with each
              stage being a full agent instead of a single prompt
```

**Platform analogy:** this is the same reasoning behind splitting a
monolith into microservices — a service that does everything becomes
hard to reason about and hard to change safely. Splitting by
responsibility makes each piece simpler, at the cost of needing
communication between the pieces (chapter 12 covers exactly that
coordination problem).

## When Multiple Agents Are Worth It

  Situation                                    Multiple agents worth it?
  ----------------------------------------------- ------------------------------
  A handful of closely related tools                 No - one agent is simpler and sufficient
  Genuinely distinct areas of responsibility            Maybe - if each area is complex enough on its own
  Need different models for different sub-tasks           Yes - e.g. a fast/cheap model for triage, a stronger one for the final decision
  Tasks that naturally run in parallel                      Yes - independent agents can work simultaneously

## The Honest Trade-off

More agents means more coordination complexity (chapter 12), more
places for something to go wrong, and more cost (each agent runs its
own loop, chapter 17). A single, well-designed agent with a focused
tool set — chapter 06's lesson — solves most real problems without
needing this at all. This module builds one agent thoroughly first for
exactly that reason: it's the right default, and multi-agent is the
exception, not the starting point.

## Hands-on: Decide, Don't Just Build

Before writing any multi-agent code, take one of chapter 07's example
scenarios and answer honestly: does this genuinely need more than one
agent, or would a slightly larger tool set on the single agent already
built in chapter 07 handle it? For most realistic small tasks, the
honest answer is the second one — worth confirming for yourself before
chapter 12 shows how to actually coordinate multiple agents when they
are genuinely needed.

## Common Misconceptions

❌ Multi-agent systems are more capable than a single agent by default.
(They can handle more distinct responsibilities, but each added agent
adds coordination overhead and cost — capability isn't free, and a
single focused agent often outperforms a poorly-coordinated multi-agent
system on the same task.)

❌ Splitting by role and splitting by step are the same thing.
(Role-based splitting is about distinct areas of expertise running
potentially in parallel; step-based splitting is a pipeline, closer to
chaining with full agents instead of single prompts.)

✔ The default should be one well-designed agent (chapters 01-10) —
reach for multiple agents specifically when a single agent's tool set
or responsibilities have genuinely grown too broad to reason about
well, not preemptively.

## Interview Questions

1.  Why might splitting one agent into several improve reliability?
2.  What's the difference between splitting agents by role and by
    step?
3.  Name two situations where multiple agents are genuinely worth the
    added complexity.
4.  Why does this module build a single agent thoroughly before
    introducing multi-agent systems?

## Summary

Multiple agents can help when one agent's responsibilities or tool set
have grown too broad to reason about reliably — splitting by role
(distinct expertise) or by step (a pipeline of full agents) — but the
added coordination complexity and cost mean a single, well-designed
agent should be the default, not the starting assumption.

## Next Chapter

➡️ `12-Orchestration-Patterns.md`
