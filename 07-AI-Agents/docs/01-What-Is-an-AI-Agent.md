# 01 - What Is an AI Agent

## Introduction

"Agent" gets used loosely, so let's pin it down before anything else.
In plain terms: an agent is a model that can look at a goal, decide
what to do next, do it, look at the result, and decide again — on its
own, without you writing out every step in advance.

## Learning Objectives

After this chapter I should be able to:

-   Give a plain-language definition of an AI agent.
-   Tell the difference between a chatbot, a tool-calling call, and an
    agent.
-   Explain what makes something "agentic" versus just automated.

------------------------------------------------------------------------

# Three Things That Are Not Quite Agents

``` text
A chatbot:        question in, answer out. One turn, no tools, no plan.

A single tool call: "call this one function, then answer." Module 02
                     chapter 14's whole example. One decision, done.

A fixed script:      "do step 1, then step 2, then step 3." You wrote
                      the sequence. The model just fills in the blanks
                      at each step.
```

None of these decide **what to do next based on what just happened.**
That's the actual line between "using an LLM" and "running an agent."

## What an Agent Actually Does

``` text
1. Look at the goal
2. Decide the next action (could be a tool call, could be "I'm done")
3. Take that action
4. Look at the result
5. Go back to step 2 - decide again, using the new information
```

Repeat until the goal is met or something stops the loop (chapter 09).
This loop is called **reason → act → observe**, and chapter 02 goes
into it in full.

**Platform analogy:** a fixed script is a shell script — the same
commands run in the same order every time. An agent is closer to an
autoscaler's control loop — it checks the current state, decides what
action (if any) gets you closer to the target state, takes it, and
checks again. The number of steps isn't fixed in advance; it depends on
what actually happens.

## A Concrete Example

``` text
Goal: "Make sure db-primary-01 isn't about to run out of disk."

Chatbot:  "You should check disk usage and clean up old logs."
          (advice, no action taken)

Agent:    1. Calls get_disk_usage("db-primary-01") -> 92%
          2. Decides: that's high, check what's taking up space
          3. Calls list_large_files("db-primary-01") -> old logs
          4. Decides: safe to clean those up
          5. Calls cleanup_logs("db-primary-01")
          6. Calls get_disk_usage("db-primary-01") again -> 61%
          7. Decides: goal met, done. Reports what it did.
```

The agent didn't just describe what to do — it acted, checked its own
work, and kept going until the goal was actually met.

## Hands-on: Spot the Difference Yourself

``` bash
ollama pull llama3.1:8b
```

Ask a local model a question two ways and compare:

``` text
1. "What should I check if a server is running low on disk?"
   -> this is chatbot behavior: advice, no action

2. Give it a tool it can call (module 02 chapter 14's pattern) and the
   same question, phrased as a task: "Check disk usage on this server
   and tell me if it's a problem."
   -> if it calls the tool and reasons about the result, you're
      looking at the first piece of agent behavior
```

Chapter 07 builds the full loop; this is just enough to feel the
difference before diving in.

## Common Misconceptions

❌ Any use of tool calling makes something an agent.
(A single tool call, decided once, is module 02 chapter 14's pattern —
an agent specifically means the model keeps deciding, turn after turn,
based on what it just observed.)

❌ Agents need a special framework to exist.
(Chapter 07 builds a complete, working agent loop in well under 50
lines of plain Python — frameworks like the ones in module 09 add
convenience, not the core concept.)

✔ The one-sentence test: does the model decide what happens next based
on what just happened, more than once? If yes, it's agentic. If the
whole sequence was decided in advance, it isn't.

## Interview Questions

1.  What's the plain-language definition of an AI agent?
2.  What's the difference between a single tool call and an agent?
3.  Name the five steps of the basic agent loop.
4.  Why is a fixed script, even one that calls an LLM at each step,
    not really "agentic"?

## Summary

An agent is a model that repeatedly decides what to do next based on
what just happened — reason, act, observe, repeat — instead of
following a sequence you wrote out in advance. That loop, not any
specific framework or tool, is the actual definition worth holding onto
through the rest of this module.

## Next Chapter

➡️ `02-The-Agent-Loop-Reason-Act-Observe.md`
