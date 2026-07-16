# 16 - Performance Tuning

## Introduction

A consolidated look at the specific knobs Ollama exposes for
performance — several already touched individually in earlier
chapters, brought together here as the tuning checklist they actually
form.

## Learning Objectives

After this chapter I should be able to:

-   Name the environment variables and parameters that affect
    performance.
-   Explain what each one actually trades off.
-   Diagnose a slow Ollama setup using the right lever for the actual
    bottleneck.

------------------------------------------------------------------------

# The Levers, Consolidated

  Setting                    Controls                              Chapter
  ------------------------------ -------------------------------------- ---------
  `num_ctx`                        Context window size (memory tradeoff)   10
  `keep_alive`                       How long a model stays loaded after use  below
  `OLLAMA_NUM_PARALLEL`                Concurrent request handling                 11
  `OLLAMA_MAX_LOADED_MODELS`             Cap on simultaneously loaded models           11
  GPU availability/VRAM                    Whether inference runs on GPU or CPU            09
  Quantization level                         Model size vs. speed vs. accuracy                07

## `keep_alive`: How Long a Model Stays Warm

``` bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "hi",
  "stream": false,
  "keep_alive": "10m"
}'
```

Verified: `keep_alive` accepts a duration string (`"5m"`, `"1h"`) or
`0` (unload shortly after this request — verified to take a couple of
seconds when combined with a real prompt, not instant) or `-1` (keep
loaded indefinitely). This directly controls the "cold load" cost from
chapter 04's `load_duration` field — a longer `keep_alive` means fewer
cold loads for bursty, intermittent usage; `0` means every single
request pays the full load cost, appropriate only when memory is
tight enough that holding a model loaded isn't affordable.

## Diagnosing "Why Is This Slow," Systematically

``` text
1. Check ollama ps - is the model on GPU or CPU? (chapter 09)
   -> CPU fallback is often the single biggest speed factor

2. Check load_duration in the response (chapter 04) - is this a
   cold-load cost, or genuinely slow generation?
   -> a large load_duration means keep_alive tuning (above) helps

3. Check num_ctx (chapter 10) - is it set far larger than the task
   actually needs, wasting memory that could speed up allocation?

4. Check the model's quantization (chapter 07) and parameter count
   (module 01 chapter 12) - is this simply a bigger/slower model than
   the task requires?

5. Check OLLAMA_NUM_PARALLEL if multiple requests are queuing instead
   of running concurrently (chapter 11)
```

This ordered checklist mirrors module 07 chapter 16's "predictable,
not random" framing for failure modes — slow Ollama performance
usually traces to one of these five specific, checkable causes, not a
vague or unexplainable slowdown.

## Hands-on: Run the Diagnostic Checklist on Your Own Setup

``` bash
ollama ps    # step 1: GPU or CPU?
curl -s http://localhost:11434/api/generate -d '{"model": "llama3.1:8b", "prompt": "hi", "stream": false}' | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f\"load: {d['load_duration']/1e9:.2f}s, generation: {d['eval_duration']/1e9:.2f}s\")
"
ollama show llama3.1:8b | grep -E "quantization|parameters"
```

Run this against whatever model you're actually using day to day, and
you'll have a real, specific answer for "why is this slow" instead of
a guess.

## Common Misconceptions

❌ Performance tuning means guessing at random settings until
something feels faster.
(Each lever addresses a specific, diagnosable bottleneck — the
checklist above is meant to identify *which* one applies before
touching any setting.)

❌ `keep_alive` set to `-1` (never unload) is always the right choice.
(It trades memory (holding a model loaded indefinitely, even when
unused) for avoiding reload cost — the right value depends on how
memory-constrained the machine is and how bursty usage actually is.)

✔ `ollama ps` and the timing fields in every API response (chapter 04)
are the two most useful diagnostic tools before touching any tuning
parameter — measure first, then tune the specific thing measurement
points to.

## Interview Questions

1.  What does `keep_alive` control, and what are its possible values?
2.  Walk through the diagnostic checklist for "why is my Ollama setup
    slow."
3.  Why might `OLLAMA_NUM_PARALLEL` matter for an application making
    several requests in quick succession?
4.  Why is measuring before tuning better than guessing at settings?

## Summary

Ollama's performance levers — `num_ctx`, `keep_alive`,
`OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, GPU availability,
and quantization — each address a specific, diagnosable bottleneck.
`ollama ps` and each API response's timing fields (chapter 04) are the
tools to measure with before reaching for any of them, turning
performance tuning into a systematic checklist instead of guesswork.

## Next Chapter

➡️ `17-Ollama-vs-Other-Local-Runtimes.md`
