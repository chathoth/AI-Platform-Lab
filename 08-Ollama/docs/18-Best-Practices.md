# 18 - Best Practices

## Introduction

The consolidated checklist for this module, same spirit as every other
module's — each item traces back to a specific chapter, several
verified directly against a real local instance.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist when setting up or operating Ollama for
    real.
-   Explain the reasoning behind each item, tied to its source
    chapter.

------------------------------------------------------------------------

# The Checklist

## 1. Confirm the Server Is Actually Reachable Before Debugging
Anything Else

Chapter 02. `curl http://localhost:11434/api/tags` is the fastest way
to rule out "Ollama isn't running" before chasing a problem further
upstream.

## 2. Check `ollama show` Before Assuming a Model's Capabilities

Chapters 03, 07, 12. Confirm tool-calling support, quantization
level, and context length directly rather than assuming from the
model's name.

## 3. Reach for a Modelfile When Customization Needs to Be Reused

Chapter 06. A per-call system prompt is simpler for one application;
a Modelfile is worth it the moment the same customization needs to be
consistent across multiple applications or shared with a team.

## 4. Right-Size `num_ctx` to the Task

Chapter 10. Verified directly: a larger context window costs real,
measurable memory (5.3GB → 9.1GB in this module's own test) even for
a short prompt — don't set it larger than the task actually needs.

## 5. Check `ollama ps`'s `PROCESSOR` Column Before Assuming a
Slowdown Is a Prompt Problem

Chapter 09. A CPU fallback is often the single biggest speed factor,
and it's directly checkable in one command.

## 6. Tune `keep_alive` to Match Actual Usage Patterns

Chapter 16. Bursty, intermittent usage benefits from a longer
`keep_alive`; memory-constrained setups benefit from a shorter one —
verified directly that this setting changes real, observable behavior.

## 7. Never Set `OLLAMA_HOST=0.0.0.0` Without Real Authentication in
Front of It

Chapter 15. Ollama has no built-in authentication — network exposure
without a reverse proxy or firewall restriction is a genuine security
risk, not a theoretical one.

## 8. Verify a Service Setup Survives a Restart, Don't Assume It

Chapter 14. The same `curl` check from item 1, run again after a
restart, is the only real confirmation that a systemd/launchd setup
actually works.

## 9. Measure Before Tuning Performance

Chapter 16. `ollama ps` and each response's timing fields (chapter 04)
point to the specific bottleneck — diagnose before adjusting settings.

## 10. Periodically Audit the Local Model Library

Chapter 08. `du -sh ~/.ollama/models` against `ollama list` — the same
housekeeping discipline as pruning unused container images.

## Anti-Patterns to Avoid

-   **Assuming a model supports tool calling without checking `ollama
    show`'s Capabilities section** — chapter 03.
-   **Setting `num_ctx` far larger than needed "just in case"** —
    chapter 10.
-   **Exposing `OLLAMA_HOST=0.0.0.0` on a shared network with no auth
    layer** — chapter 15.
-   **Guessing at performance settings instead of checking `ollama
    ps` and timing fields first** — chapter 16.
-   **Letting a local model library grow indefinitely with no
    periodic cleanup** — chapter 08.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as every other module: create an `ollama-checklist.md`
with these 10 items as literal checkboxes, and walk through it before
deploying Ollama anywhere beyond a personal learning setup.

## Common Misconceptions

❌ Ollama is simple enough not to need this level of operational
discipline.
(It's a real service with real memory, security, and performance
characteristics — several verified directly in this module (context
window memory cost, `keep_alive` behavior) rather than assumed.)

❌ Following this checklist means Ollama is production-ready by
default.
(It covers the operational basics this module verified directly — a
genuine production deployment still needs the reverse proxy,
monitoring, and access control chapter 15 and 16 point toward, not
just Ollama's own defaults.)

✔ Several items here — context window memory cost, `keep_alive`
behavior, `/api/embed` batching — were confirmed by running real
commands against a real instance while building this module, not
assumed from documentation.

## Interview Questions

1.  What's the fastest way to confirm Ollama is running and reachable?
2.  Why should `num_ctx` be right-sized rather than set as large as
    possible by default?
3.  Why is `OLLAMA_HOST=0.0.0.0` a security decision, not just a
    convenience toggle?
4.  What two things should you check before touching any performance
    tuning setting?

## Summary

Every practice in this checklist maps to something verified directly
in this module — checking real capabilities, memory costs, security
defaults, and performance behavior against a running local instance,
not just described in the abstract. Together they're what makes
Ollama safe and predictable to operate beyond a single personal
learning setup.

## Next Chapter

➡️ `19-Interview-Questions.md`
