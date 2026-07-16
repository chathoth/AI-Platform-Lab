# 12 - Error Handling in MCP Tools

## Introduction

Every tool example so far assumed success. Real tools call real
systems that fail — a host doesn't exist, a service is unreachable, an
argument is invalid. This chapter covers what happens on the wire when
a tool raises, and how to make that failure actually useful to the
model instead of a confusing dead end.

## Learning Objectives

After this chapter I should be able to:

-   Explain what happens when a tool function raises an exception.
-   Return structured, actionable errors instead of letting exceptions
    propagate raw.
-   Distinguish errors the model should retry from errors it should
    report to the user.

------------------------------------------------------------------------

# What Happens on an Unhandled Exception

``` python
@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    known_hosts = {"db-primary-01": 92}
    return {"hostname": hostname, "disk_percent": known_hosts[hostname]}  # KeyError if unknown
```

Calling this with an unknown hostname raises a `KeyError`. The `mcp`
SDK catches it and returns an error result to the client rather than
crashing the whole server process — but the model receives a raw
Python exception message, which is rarely useful context for deciding
what to do next.

## Returning Structured, Actionable Errors Instead

``` python
@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host."""
    known_hosts = {"db-primary-01": 92, "web-node-01": 41}
    if hostname not in known_hosts:
        return {
            "error": True,
            "message": f"Unknown hostname: {hostname!r}. Known hosts: {list(known_hosts)}",
        }
    return {"hostname": hostname, "disk_percent": known_hosts[hostname]}
```

Returning a structured error **as a normal result**, rather than
raising, gives the model something it can actually reason about — in
this case, the list of valid hostnames, which it can use to retry with
a corrected argument or explain the problem to the user. This is module
02 chapter 06's structured-output discipline, applied to error paths
specifically.

**Platform analogy:** this is the difference between a bare 500 error
with a stack trace and a well-formed 4xx JSON error body with a
specific error code and message — both signal failure, but only one
gives the caller (here, the model) something actionable to do next.

## Which Errors Should Be Retryable?

  Error type                              Model's best response
  ------------------------------------------ ------------------------------------------
  Invalid argument (bad hostname, bad ID)      Retry with a corrected argument, if the error message gives it enough info
  Transient failure (timeout, service down)      Possibly retry once; don't loop indefinitely
  Permission denied / not authorized               Report to the user — not something the model can fix by retrying
  A genuinely destructive or ambiguous request       Ask for clarification, don't guess and retry

A tool's error response should hint at which category applies —
`{"error": True, "retryable": False, "message": "..."}` is a small
addition that helps the model (or the host application wrapping it)
make that decision instead of guessing.

## Validate Before You Execute, Not Just After Failure

``` python
@mcp.tool()
def restart_service(service_name: str, environment: str) -> dict:
    """Restart a named service. DESTRUCTIVE - requires explicit confirmation."""
    ALLOWED_ENVIRONMENTS = {"dev", "staging"}  # never "prod" without a separate, explicit path
    if environment not in ALLOWED_ENVIRONMENTS:
        return {"error": True, "retryable": False, "message": f"Environment {environment!r} not allowed via this tool."}
    # ... actually restart it
    return {"service": service_name, "environment": environment, "status": "restarted"}
```

This is module 01 chapter 18 and module 02 chapter 15's "never blindly
execute" rule, implemented as a guard clause inside the tool itself —
the safety check lives in code the model cannot talk its way around,
not in a prompt instruction alone.

## Hands-on: Trigger and Handle a Real Error

``` python
# in server.py, add the corrected get_disk_usage above, then:
result = await session.call_tool("get_disk_usage", {"hostname": "totally-made-up-host"})
print(result.content[0].text)
# should print the structured error with the list of known hosts,
# not a raw KeyError traceback
```

Compare this against the unhandled version — the difference in what
information actually reaches the model (and, through it, the user) is
the entire point of this chapter.

## Common Misconceptions

❌ Letting an exception propagate is fine — the SDK handles it.
(The SDK prevents a crash, but the resulting error message is rarely
useful context for the model — structured, deliberate error handling
produces a far more useful outcome.)

❌ Any error should be safe for the model to retry automatically.
(Permission errors and ambiguous/destructive requests should be
surfaced to a human, not retried — mark errors as retryable or not,
explicitly.)

✔ A tool's guard clauses (like the environment allowlist above) are a
real security boundary, not just error handling — they're what
prevents a talked-into-it model from executing something it shouldn't,
independent of whatever the prompt says.

## Interview Questions

1.  What happens when an MCP tool function raises an unhandled
    exception?
2.  Why is a structured error response more useful to a model than a
    raw exception message?
3.  Give an example of an error that should NOT be automatically
    retried.
4.  Why should destructive-action guard clauses live inside the tool
    itself, not just in the prompt?

## Summary

An unhandled exception in an MCP tool doesn't crash the server, but it
also doesn't give the model anything useful to act on — returning a
structured error result, marked retryable or not, is what turns a
failure into information the model (or the host application) can
actually use. Guard clauses inside a tool's own code, not just prompt
instructions, are the real defense against a destructive action being
executed inappropriately.

## Next Chapter

➡️ `13-Authentication-and-Authorization.md`
