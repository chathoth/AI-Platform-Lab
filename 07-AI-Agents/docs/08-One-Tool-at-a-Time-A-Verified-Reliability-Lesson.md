# 08 - One Tool at a Time: A Verified Reliability Lesson

## Introduction

This chapter exists because of something that actually happened while
testing chapter 07's agent, not because of a theoretical concern. Given
a goal with a clear condition — "restart the service **only if** disk
usage is above 90%" — the agent incorrectly restarted the service even
when disk usage was 41%. This chapter is that failure, the fix, and
why the fix worked.

## Learning Objectives

After this chapter I should be able to:

-   Describe the exact verified failure and why it happened.
-   Explain why letting a model request multiple tool calls in one
    turn removes a real safety check.
-   Apply the fix: force one tool call at a time, with real
    guardrails underneath.

------------------------------------------------------------------------

# The Verified Failure

Using chapter 07's exact agent code, this goal was given to
`llama3.1:8b`:

``` text
"Check disk usage on web-node-01, and if it is above 90%, restart the
cleanup-service."
```

`web-node-01`'s actual disk usage is 41% — well under the threshold.
The correct behavior is: check, see 41%, do **not** restart, say so.

Verified actual output:

``` text
turn 1: model calls get_disk_usage("web-node-01") -> {"disk_percent": 41}
        model ALSO calls restart_service("cleanup-service") -> {"status": "restarted"}
        (both in the SAME turn, before ever seeing the 41% result)
turn 2: "The disk usage on web-node-01 is below the threshold, so
         there's no need to take further actions. The cleanup-service
         has been restarted as a precautionary measure."
```

The model restarted a service it shouldn't have, then — worse —
described that action as unnecessary in the very same answer. It
never actually paused to observe the 41% result before deciding to
restart, because it requested **both tool calls in the same turn**,
before either result existed yet.

## Why This Happened

Chapter 02's whole point was that "observe" — reading a result before
deciding the next action — is what makes an agent different from a
single tool call. Requesting two tool calls in one turn skips that
step entirely for the second call: the model committed to calling
`restart_service` *before* it had seen whether the condition was
actually met.

``` text
What should have happened:
  reason (check usage) -> act (call it) -> OBSERVE (41%, below 90%)
  -> reason again (condition not met, don't restart) -> final answer

What actually happened:
  reason (check usage AND restart, decided together) -> act (both,
  at once) -> observe (both results, after the damage was done)
```

## The Fix, Verified

Forcing the loop to execute **only the first tool call per turn** —
even if the model requested more — combined with a more precise tool
description, fixed it:

``` python
# only execute ONE tool call per turn, even if the model requested more
if msg.tool_calls:
    messages.append(msg)
    call = msg.tool_calls[0]              # <- the actual fix
    args = json.loads(call.function.arguments)
    result = TOOLS[call.function.name](**args)
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
```

``` python
# also: a more precise tool description, stating the precondition explicitly
{"name": "restart_service", "description":
    "Restart a named service. Only call this if disk usage was "
    "confirmed ABOVE 90 percent by a previous get_disk_usage call "
    "in this conversation."}
```

Verified output with both changes:

``` text
turn 1: model calls get_disk_usage("web-node-01") -> {"disk_percent": 41}
turn 2: "The current disk usage on web-node-01 is 41%, which is below
         the threshold of 90%."
```

No incorrect restart. The model correctly stopped after observing the
result.

## Why This Matters Beyond This One Example

**Platform analogy:** batching the two tool calls together is like
running a database migration and its rollback check in the same
uninterruptible transaction, planned before either one runs — you've
removed your own ability to react to the first step's outcome before
committing to the second. One-tool-at-a-time is the equivalent of
running each step and actually checking its result before deciding on
the next one — slower, but the check is real instead of theoretical.

This is also why chapter 13's guardrails matter regardless of this
fix: even a well-designed loop can get a probabilistic model to make
the wrong call sometimes. The loop-level fix reduces the *frequency* of
this exact failure; it doesn't guarantee it can never happen again.

## Hands-on: Reproduce Both Versions Yourself

Run chapter 07's original agent against the `web-node-01` goal and
confirm you see the same incorrect restart. Then apply the one-line
fix above (`call = msg.tool_calls[0]` instead of looping over all of
`msg.tool_calls`) and the improved tool description, and confirm the
corrected behavior. Seeing the actual wrong output first is what makes
this lesson stick — it's a genuinely easy mistake to make by default.

## Common Misconceptions

❌ Letting a model batch multiple tool calls per turn is always more
efficient and therefore better.
(It's faster when it works, but verified directly: it removed the
observe step for the second call, causing an incorrect action based on
information the model hadn't actually seen yet.)

❌ A better prompt alone would have fixed this.
(The tool description improvement helped, but the structural fix —
forcing one tool call at a time — is what actually guarantees the
observe step happens before every action, not just makes it more
likely.)

✔ This specific, verified failure — restarting a service under a
condition that wasn't met — is exactly the class of mistake chapter 13's
code-level guardrails exist to catch even when the loop itself is
well-designed.

## Interview Questions

1.  Describe the verified failure in this chapter, in your own words.
2.  Why did requesting two tool calls in the same turn cause the
    model to skip a real safety check?
3.  What two changes fixed the behavior, and why did both matter?
4.  Why doesn't this fix guarantee the agent will never make an
    incorrect destructive call again?

## Summary

A real, verified test showed that letting a model request multiple
tool calls in a single turn can skip the agent loop's whole reason for
existing — observing a result before acting on it — leading to an
incorrect service restart under a condition that wasn't met. Forcing
one tool call per turn, combined with a precise tool description, fixed
it — but the deeper lesson is that even a correctly-built loop needs
real, code-level guardrails (chapter 13) for anything with real
consequences.

## Next Chapter

➡️ `09-Stopping-Conditions-and-Loop-Limits.md`
