# 13 - Streaming Responses

## Introduction

Module 01 chapter 03 established that generation is a loop, one token
at a time. This chapter is how that loop actually reaches your code —
Ollama's raw streaming response, verified directly, underneath every
`stream=True` call this repository has made.

## Learning Objectives

After this chapter I should be able to:

-   Read Ollama's raw streaming response format.
-   Explain why `stream: false` waits for the whole generation before
    responding.
-   Compute time-to-first-token from raw streamed output.

------------------------------------------------------------------------

# `stream: false` vs. `stream: true`

Every earlier chapter in this module used `"stream": false` — one
request, one complete response, once generation finishes entirely.
Setting `"stream": true` (the default if omitted) changes the response
shape entirely.

``` bash
curl -N http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Count to 5",
  "stream": true
}'
```

Instead of one JSON object, this returns a sequence of JSON objects,
one per line, each containing one small piece of the response:

``` json
{"model":"llama3.1:8b","response":"1","done":false}
{"model":"llama3.1:8b","response":",","done":false}
{"model":"llama3.1:8b","response":" ","done":false}
{"model":"llama3.1:8b","response":"2","done":false}
...
{"model":"llama3.1:8b","response":"","done":true,"total_duration":...}
```

This is module 01 chapter 03's generation loop, made directly visible
— each streamed line is one iteration of "predict the next token,
append it, repeat."

## Consuming a Stream in Python

``` python
import requests
import json

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1:8b", "prompt": "Count to 5", "stream": True},
    stream=True,
)

for line in response.iter_lines():
    if line:
        chunk = json.loads(line)
        print(chunk["response"], end="", flush=True)
        if chunk["done"]:
            break
```

The `-N` flag in the earlier `curl` example disables output buffering,
so you actually see output arrive incrementally instead of all at
once at the end — worth remembering when debugging streaming behavior
with `curl` directly.

## Measuring Time-to-First-Token From Raw Output

``` python
import time
import requests
import json

start = time.time()
first_token_time = None

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1:8b", "prompt": "Explain Kubernetes in detail", "stream": True},
    stream=True,
)

for line in response.iter_lines():
    if line:
        chunk = json.loads(line)
        if first_token_time is None and chunk.get("response"):
            first_token_time = time.time()
        if chunk["done"]:
            break

print(f"Time to first token: {first_token_time - start:.2f}s")
print(f"Total time: {time.time() - start:.2f}s")
```

This is module 01 chapter 03's TTFT-versus-total-time distinction,
now computed directly from Ollama's own raw stream instead of a
higher-level client abstraction.

## Why This Matters for Anything User-Facing

**Platform analogy:** this is the same reason a web server streams a
large file response instead of buffering the whole thing before
sending the first byte — the user sees progress immediately instead of
staring at nothing until the entire operation completes. For a chat UI
or a CLI tool, streaming is the difference between feeling responsive
and feeling frozen, even if total completion time is identical either
way.

## Hands-on: Compare Streamed vs. Non-Streamed, Directly

``` bash
time curl -s http://localhost:11434/api/generate -d '{"model": "llama3.1:8b", "prompt": "Write a short paragraph about Kubernetes", "stream": false}' > /dev/null

time curl -s -N http://localhost:11434/api/generate -d '{"model": "llama3.1:8b", "prompt": "Write a short paragraph about Kubernetes", "stream": true}' > /dev/null
```

Total time should be similar between the two — streaming doesn't make
generation *faster*, it makes the first useful output arrive sooner.
Confirm that distinction directly rather than assuming it.

## Common Misconceptions

❌ Streaming makes total generation time faster.
(It doesn't change total generation time — it changes when the first
piece of output becomes visible, which is a latency-*perception*
improvement, not a throughput one.)

❌ `stream: false` is somehow a different generation process.
(It's the same underlying loop — `stream: false` just waits for every
token before returning one complete response, instead of returning
each token as it's produced.)

✔ Time-to-first-token and total generation time are genuinely
different numbers, worth measuring separately — module 01 chapter 03's
distinction, now directly computable from Ollama's raw streamed
output.

## Interview Questions

1.  What does Ollama's streaming response format actually look like,
    line by line?
2.  Does streaming make generation faster overall? Why or why not?
3.  How would you compute time-to-first-token from a raw streamed
    response?
4.  Why does streaming matter more for a user-facing chat UI than for
    a batch script?

## Summary

Ollama's streaming response is a sequence of small JSON chunks, one
per generated token (or a few), making module 01 chapter 03's
generation loop directly visible in raw output. Streaming doesn't
change total generation time — it changes how soon the first useful
output appears, which matters specifically for anything user-facing
where perceived responsiveness is the actual goal.

## Next Chapter

➡️ `14-Running-Ollama-as-a-Service.md`
