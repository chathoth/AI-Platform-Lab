# 13 - Guardrails and Human-in-the-Loop

## Introduction

Chapter 08 wasn't a one-off anecdote — it's the whole reason this
chapter exists. A real, verified test showed a well-built agent loop
can still take an action a stated condition didn't justify. Guardrails
are what catch that even when the loop, the prompt, and the model all
did roughly what you'd expect.

## Learning Objectives

After this chapter I should be able to:

-   Explain why guardrails live in code, not in the prompt.
-   Add an allowlist and a confirmation gate to an agent's tool
    execution.
-   Decide when a human needs to be in the loop before an action runs.

------------------------------------------------------------------------

# Why the Guardrail Can't Just Be a Better Prompt

Chapter 08's fix (one tool call at a time, a clearer tool description)
reduced *how often* the model made the wrong call. It didn't make the
wrong call impossible — the model is still, fundamentally, predicting
plausible next tokens (module 01 chapter 03), not executing a
guaranteed-correct decision procedure. This is the same conclusion
module 02 chapter 15 and module 06 chapter 13 already reached from a
different angle: a prompt instruction is guidance the model can get
wrong, not an enforceable rule.

## An Allowlist: What the Agent Is Even Capable Of

``` python
ALLOWED_TOOLS = {"get_disk_usage"}  # read-only, safe by default

def execute_tool(name: str, args: dict) -> dict:
    if name not in ALLOWED_TOOLS:
        return {"error": True, "message": f"{name} is not in the allowed tool set for this agent."}
    return TOOLS[name](**args)
```

This is module 01 chapter 18's "never blindly execute" rule and module
06 chapter 13's authorization pattern, applied to an agent's tool
execution step specifically — the check happens in code the model
cannot talk its way around, exactly like chapter 08's structural fix
lived in the loop's code, not in a prompt.

## A Confirmation Gate: Pause Before Anything Destructive

``` python
DESTRUCTIVE_TOOLS = {"restart_service"}

def execute_tool_with_confirmation(name: str, args: dict) -> dict:
    if name in DESTRUCTIVE_TOOLS:
        confirmed = input(f"Agent wants to call {name}({args}). Allow? [y/N] ")
        if confirmed.lower() != "y":
            return {"error": True, "message": "Action declined by human reviewer."}
    return TOOLS[name](**args)
```

Applied to chapter 08's exact scenario, this gate would have stopped
the incorrect restart at the point of execution — a human seeing
`restart_service('cleanup-service')` proposed for a host reported at
41% disk usage would very likely say no, catching the mistake at the
last possible moment, independent of whether the loop or the model
reasoned correctly upstream.

## Deciding Where the Human Belongs

  Action type                              Human-in-the-loop?
  -------------------------------------------- ------------------------------
  Read-only (check status, look something up)     No - low risk, slows things down for no benefit
  Reversible action (restart a non-critical service) | Maybe - depends on blast radius
  Destructive or hard-to-reverse (delete data, restart production) | Yes - the cost of a wrong automatic action is too high

This is the same risk-based judgment call this whole repository's own
operating instructions apply to *any* action, not just agent tool
calls — match the level of caution to how reversible and how
consequential the action actually is.

## Layering All Three Defenses Together

``` text
1. Allowlist        - the agent literally cannot call a tool that's
                        not permitted, regardless of what it "decides"
2. Confirmation gate   - anything destructive pauses for a human,
                        regardless of how confident the model sounds
3. Chapter 08's fix     - one tool call at a time, reducing how often
                        a wrong call is even proposed in the first place
```

None of these alone is sufficient. Together, they're what makes an
agent safe to point at anything with real consequences.

## Hands-on: Add a Guardrail That Would Have Caught Chapter 08's
Mistake

Take chapter 07's original (unfixed) agent and add the confirmation
gate above. Run it against chapter 08's exact `web-node-01` scenario
and confirm the gate correctly intercepts the incorrect restart —
verifying, directly, that a code-level guardrail catches what the
model's own reasoning missed.

## Common Misconceptions

❌ A well-tested agent doesn't need runtime guardrails.
(Chapter 08's finding is the direct counter-example — a verified,
working agent still made an incorrect call under a real test. Testing
reduces risk; guardrails bound it.)

❌ Human-in-the-loop should be used for every action, to be safe.
(That defeats the purpose of automation for genuinely low-risk,
reversible actions — match the guardrail's strictness to the action's
actual blast radius, per the table above.)

✔ An allowlist, a confirmation gate for destructive actions, and
chapter 08's loop-level fix are three independent layers — each one
catches something the others might miss.

## Interview Questions

1.  Why can't a guardrail live only in the prompt?
2.  What's the difference between an allowlist and a confirmation
    gate, and what does each protect against?
3.  How would you decide whether a given tool needs human-in-the-loop
    confirmation?
4.  Applied to chapter 08's exact failure, which guardrail would have
    caught it, and how?

## Summary

Guardrails exist because chapter 08 proved, directly, that a correctly
built agent loop can still take an unjustified action — a prompt
instruction alone isn't enforcement. An allowlist bounds what an agent
can even attempt, a confirmation gate pauses destructive actions for
human review, and both work alongside (not instead of) chapter 08's
loop-level fix — three independent layers, because no single one is
sufficient on its own.

## Next Chapter

➡️ `14-Observability-Tracing-an-Agents-Steps.md`
