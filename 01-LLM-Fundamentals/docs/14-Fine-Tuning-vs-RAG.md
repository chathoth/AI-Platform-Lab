# 14 - Fine-Tuning vs RAG

## Introduction

This is the decision I expect to actually be asked to make at work:
"the model doesn't know about our internal tools/runbooks — how do we
fix that?" There are two very different answers — fine-tuning and RAG —
and picking the wrong one wastes real time and money. I map this
directly onto a decision I already know how to make: **bake it into the
image at build time, or mount it as an external volume at runtime?**

## Learning Objectives

After this chapter I should be able to:

-   Explain what fine-tuning does and its trade-offs.
-   Explain what RAG (Retrieval-Augmented Generation) does and its
    trade-offs.
-   Choose between them (or combine them) for a given real-world
    scenario.
-   Build a minimal RAG pipeline using embeddings from chapter 05.

------------------------------------------------------------------------

# Two Different Ways to Give a Model New Knowledge

``` text
Fine-tuning:  bake knowledge INTO the model's weights (chapter 08)
RAG:          fetch relevant knowledge and hand it to the model AT REQUEST TIME
```

## Fine-Tuning: Baked Into the Image

Fine-tuning takes a pretrained model and further trains it on your own
curated examples, updating the model's weights. The knowledge becomes
part of the model itself.

**Platform analogy:** this is baking a config or dataset **into the
Docker image at build time**. Pros: no runtime dependency, consistent
behavior baked in. Cons: every update means a full rebuild — retraining
is slow, needs GPU infra and ML expertise, and you can't easily audit
*why* the model said something, since the knowledge is now diffused
across billions of weights with no traceable source.

  Good fit for                        Bad fit for
  ------------------------------------ ------------------------------------
  Teaching a consistent *style/format* Injecting frequently-changing facts
  Domain-specific tone (legal, medical)Anything needing a citable source
  Narrow, stable task specialization   Data that updates daily/hourly

## RAG: Mounted as an External Volume

RAG doesn't touch the model's weights at all. Instead, at request time,
it retrieves relevant documents (using the embedding similarity search
from [05-Embeddings-Basics.md](05-Embeddings-Basics.md)) and stuffs them
into the prompt as context, so the model answers *using what's actually
in front of it* instead of relying on what it memorized during training.

``` mermaid
flowchart LR
A[User question] --> B[Embed the question]
B --> C[Vector search: find similar docs]
C --> D[Top-k relevant chunks]
D --> E[Inject into prompt as context]
E --> F[LLM generates answer grounded in that context]
```

**Platform analogy:** this is mounting a **config map / external
volume** at runtime instead of baking data into the image. Pros: update
the knowledge source (add a new runbook, update a doc) and it's
immediately reflected — no retraining. You also get traceability: you
know exactly which document the answer came from, which directly
mitigates the hallucination problem from chapter 11. Cons: adds runtime
dependencies (a vector DB, an embedding step) and retrieval quality
becomes a new thing you have to tune and monitor.

  Good fit for                          Bad fit for
  -------------------------------------- ------------------------------------
  Frequently-changing internal docs      Teaching a fundamentally new *skill*
  Answers that need a citable source     Ultra-low-latency, no extra hops
  Company-specific knowledge (runbooks)  Data too large/unstructured to chunk

## The Decision, As I'd Actually Make It

``` text
Does the knowledge change often (docs, tickets, runbooks)?
        → RAG

Do you need to know/cite WHERE an answer came from?
        → RAG

Are you teaching a stable behavior/format/style, not facts?
        → Fine-tuning

Both a stable style AND fresh facts?
        → Fine-tune for style + RAG for facts (they're not mutually exclusive)
```

In practice, most internal "chat with our docs" tools I'd build start
and stay as RAG — it's cheaper to build, cheaper to update, and far
easier to debug when something's wrong (you can literally inspect which
chunk was retrieved), the same reasons I'd default to mounting config
over baking it into an image unless there's a specific reason not to.

## Hands-on: A Minimal RAG Pipeline Over Your Own Runbooks

``` python
import numpy as np
from openai import OpenAI

client = OpenAI()

def embed(text):
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding

# 1. Index your own runbooks (do this once, or whenever docs change)
runbooks = {
    "pod-crashloop.md": "To debug CrashLoopBackOff, check kubectl describe pod and logs --previous...",
    "disk-full.md": "When disk usage hits 90%, first check /var/log for oversized log files...",
    "deploy-rollback.md": "To roll back a failed deployment, use kubectl rollout undo deployment/<name>...",
}
index = {name: embed(text) for name, text in runbooks.items()}

# 2. At request time: embed the question, find the closest doc
def retrieve(question, top_k=1):
    q_vec = np.array(embed(question))
    scored = [(name, np.dot(q_vec, np.array(vec))) for name, vec in index.items()]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [runbooks[name] for name, _ in scored[:top_k]]

# 3. Inject retrieved context into the prompt
question = "one of our pods keeps restarting, what do I check?"
context = "\n".join(retrieve(question))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"Answer using only this context:\n{context}"},
        {"role": "user", "content": question}
    ]
)
print(response.choices[0].message.content)
```

Run it, then swap in a question that has *no* matching runbook and watch
the model either say it doesn't know or start drifting toward
hallucination — that gap is exactly why retrieval quality (what counts
as "close enough" in the vector search) matters as much as the LLM call
itself.

## Common Misconceptions

❌ Fine-tuning is how you "teach the model your company's docs."
(Fine-tuning teaches *behavior/style*, not a reliable way to inject
fresh, citable facts — RAG is almost always the right tool for that.)

❌ RAG requires a big, complex vector database from day one.
(A small in-memory numpy array, like the example above, is a completely
legitimate RAG system for a few hundred documents — scale the
infrastructure only when the data volume actually demands it.)

✔ Fine-tuning and RAG solve different problems and are frequently
combined — fine-tune for consistent style/format, RAG for up-to-date,
citable facts.

## Interview Questions

1.  What's the core difference between what fine-tuning changes and
    what RAG changes?
2.  Why is RAG generally the better choice for frequently-updated
    internal documentation?
3.  Why does RAG make it easier to trace *why* a model gave a
    particular answer, compared to fine-tuning?
4.  Give a scenario where you'd want both fine-tuning and RAG together.

## Summary

Fine-tuning bakes knowledge into the model's weights at training time —
good for teaching stable style/behavior, expensive to update. RAG
retrieves relevant context at request time and hands it to the model
fresh — good for frequently-changing, citable facts, and it directly
addresses the hallucination problem from chapter 11 by grounding
answers in real source documents. Most "chat with our internal docs"
use cases should default to RAG.

## Next Chapter

➡️ `15-Open-vs-Closed-Models.md`
