# 16 - Prompt Lifecycle

## Introduction

Every chapter so far explained one piece of the machinery. This chapter
zooms out to the full **request lifecycle** — from the moment a user
types something to the moment they see a response — which is the view I
actually need when I'm the one operating an LLM-backed system in
production. I treat this exactly like documenting a request's journey
through a service mesh: every hop is a place to add validation,
observability, or a failure mode.

## Learning Objectives

After this chapter I should be able to:

-   Trace a prompt through every stage from user input to final
    response.
-   Identify where system prompts, RAG context, and history get
    assembled.
-   Identify the observability points I'd instrument in a production
    system.
-   Explain where things commonly go wrong at each stage.

------------------------------------------------------------------------

# The Full Lifecycle

``` mermaid
flowchart TD
A[User input] --> B[Input validation / sanitization]
B --> C[Prompt assembly: system prompt + history + RAG context + user input]
C --> D[Token count check against context window]
D --> E[Send to model API]
E --> F[Model generates tokens - chapter 03 loop]
F --> G[Stream/return response]
G --> H[Output validation / guardrails]
H --> I[Store in conversation history for next turn]
I --> J[Deliver to user]
```

## Stage by Stage, With an Ops Lens

1.  **Input validation** — same as sanitizing any user input before it
    hits a backend. Strip/flag prompt-injection attempts (text trying
    to override your system prompt), oversized input, disallowed
    content.
2.  **Prompt assembly** — this is where the system prompt (your fixed
    instructions), retrieved RAG context (chapter 14), conversation
    history, and the new user message all get concatenated into one
    payload. This assembly step is the single highest-leverage place to
    add logging — if something goes wrong downstream, you want to know
    *exactly* what was sent to the model.
3.  **Token count check** — count tokens (chapter 04) against the
    context window (chapter 09) *before* sending, not after a failed
    call. This is the equivalent of a pre-flight payload-size check
    instead of letting the request fail downstream.
4.  **Model call** — the generation loop from
    [03-How-LLMs-Work.md](03-How-LLMs-Work.md). This is where
    temperature/top-p (chapter 10) get applied.
5.  **Output validation / guardrails** — check the response before it
    reaches the user: does it match an expected schema (for structured
    output), does it contain anything that shouldn't be exposed, does it
    look like a hallucination (chapter 11) on a topic you can
    cross-check?
6.  **History storage** — append the exchange to conversation state for
    the next turn. Since inference is stateless (chapter 08), this is
    entirely the application's responsibility — nothing about the model
    itself remembers this happened.

## Platform Analogy: Treat It Like a Request Pipeline With Hooks

I instrument this lifecycle the same way I'd instrument any multi-hop
request path — a log line (or trace span) at every stage boundary:

  Stage                Metric/log I'd want
  --------------------- --------------------------------------------
  Input validation      Rejected/flagged input count
  Prompt assembly       Full assembled prompt (for debugging), token count
  Token check            Requests blocked pre-flight for exceeding budget
  Model call              Latency (TTFT + total), tokens generated, model version used
  Output validation       Guardrail trigger rate, schema validation failures
  History storage          Conversation length growth over a session

That table is effectively an APM dashboard for an LLM feature — the
same instincts that make a normal service observable apply directly
here, just with different metric names.

## Hands-on: Instrument a Minimal Pipeline

``` python
import time
import tiktoken
from openai import OpenAI

client = OpenAI()
enc = tiktoken.encoding_for_model("gpt-4")

def call_llm(system_prompt, history, user_input, max_context=8000):
    # 1. assemble
    messages = [{"role": "system", "content": system_prompt}] + history + [
        {"role": "user", "content": user_input}
    ]

    # 2. pre-flight token check
    full_text = " ".join(m["content"] for m in messages)
    token_count = len(enc.encode(full_text))
    print(f"[metric] prompt_tokens={token_count}")
    if token_count > max_context:
        raise ValueError(f"Prompt too large: {token_count} tokens (limit {max_context})")

    # 3. call, timed
    start = time.time()
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    latency = time.time() - start
    print(f"[metric] latency_s={latency:.2f} completion_tokens={response.usage.completion_tokens}")

    # 4. minimal output guardrail
    output = response.choices[0].message.content
    if len(output.strip()) == 0:
        raise ValueError("Empty response from model - flag for review")

    return output
```

This is deliberately minimal, but it already has the four things I'd
insist on before calling any pipeline "production ready": pre-flight
validation, structured logging at the boundary, latency measurement, and
a basic output guardrail.

## Common Misconceptions

❌ The "prompt" is just what the user typed.
(It's the fully assembled payload — system prompt + history + RAG
context + user input — and most bugs live in that assembly step, not in
the model call itself.)

❌ Once the model responds, the job is done.
(Output validation and history storage are still your responsibility —
the model has no idea what "your application" needs to do next.)

✔ The most valuable single log line in an LLM system is the fully
assembled prompt right before it's sent — most "why did it say that"
debugging starts there, not in the model's response.

## Interview Questions

1.  Walk through the full prompt lifecycle from user input to stored
    history.
2.  Why should token count be checked *before* sending the request,
    not after a failure?
3.  What's the single most valuable thing to log in an LLM pipeline for
    debugging, and why?
4.  Why is output validation the application's responsibility rather
    than the model's?

## Summary

A "prompt" isn't a single string — it's the product of an assembly
pipeline (system prompt, history, RAG context, user input) that should
be validated, logged, and measured at every stage, the same way any
multi-hop request path would be instrumented in production. Most
real-world LLM bugs trace back to this assembly and validation layer,
not to the model itself.

## Next Chapter

➡️ `17-LLM-Limitations.md`
