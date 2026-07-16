# Project: Incident Similarity Finder

A small, read-only tool that takes a description of an incident that's
happening *right now* and finds the most similar past incidents from a
local knowledge base - by meaning, not by keyword.

This is the simplest of the two 10-Projects builds: pure retrieval. No
agent loop, no tool calls that change anything. If you've been paged
at 2am and typed a symptom into Slack search hoping someone hit this
before, this is that search, but semantic.

## Why this is useful in a platform/DevOps context

Postmortems pile up over time, but keyword search over them is weak:
"disk full" won't surface an incident someone titled "writes failing
on primary." Embeddings fix that by matching on meaning. This project
is deliberately the smallest possible version of that idea, built
entirely from concepts already covered in this repo:

- [Module 03 - Embeddings](../../03-Embeddings/) - why "similar meaning" beats keyword match
- [Module 04 - Vector Databases](../../04-Vector-Databases/) - the `OllamaEmbeddingFunction` + Chroma pattern reused directly here
- [Module 05 - RAG](../../05-RAG/) - retrieval as the core building block (no generation step needed here - just showing the retrieved incidents is the whole product)

## How it works

```text
data/incidents.json  --embed-->  chroma_db/ (local, on disk)
                                       ^
                                       |
new incident description  --embed-->  query  -->  top-N similar past incidents
```

1. `src/index_incidents.py` reads `data/incidents.json` (8 fictional
   but realistic incident postmortems - CrashLoopBackOff/OOM, disk-full,
   connection pool exhaustion, DNS, TLS expiry, memory leak, network
   partition), embeds each one with a local `nomic-embed-text` model
   via Ollama, and stores them in a persistent local Chroma collection.
2. `src/find_similar.py` embeds your new incident description the same
   way and returns the closest matches, each with its original
   resolution and follow-up.

Nothing here is destructive or agentic - it only ever reads the
vector store and prints results. That's what makes it a good first
project before the guarded-agent project (`../runbook-ops-assistant/`).

## Run it

```bash
ollama pull nomic-embed-text
pip install chromadb requests

cd src
python index_incidents.py
python find_similar.py "checkout pods keep restarting after we deployed, seeing OOMKilled in the logs"
```

### Verified output

```text
Query: checkout pods keep restarting after we deployed, seeing OOMKilled in the logs

Top 3 similar past incidents:

[INC-1001] checkout-service CrashLoopBackOff after deploy  (service: checkout-service, distance=0.2146)
  Resolution: Rolled back to the previous deployment revision. Follow-up: raise the memory limit and add a memory usage alert before the next batch-size change.

[INC-1007] checkout-service returning 500s, unrelated to the OOM incident  (service: checkout-service, distance=0.2727)
  Resolution: Added a request timeout and circuit breaker on the inventory-service client. Follow-up: audit other services for missing timeouts on downstream calls.

[INC-1006] worker-queue memory usage climbing steadily over 6 hours before OOM  (service: worker-queue, distance=0.3369)
  Resolution: Rolled back the caching change and added a TTL-based eviction policy before re-deploying. Follow-up: add a memory-growth-rate alert, not just an absolute threshold.
```

The nearest match (INC-1001) is the actual same-root-cause incident,
even though the query never used the words "CrashLoopBackOff" or
"batch size." A second, unrelated query about a database replica
running low on disk correctly surfaced the two disk/WAL incidents
(INC-1008, INC-1002) ahead of an unrelated connection-pool incident -
confirming the ranking isn't just matching on the word "disk."

## What to try next

- Add your own team's real (anonymized) postmortems to
  `data/incidents.json` and re-run `index_incidents.py` - re-running it
  is safe to repeat; per module 04 chapter 06's verified finding,
  Chroma's `add()` silently no-ops on IDs that already exist rather
  than erroring or duplicating, so edit the JSON and re-run instead of
  deleting `chroma_db/` first.
- Increase `n_results` in `find_similar.py` to see more candidates.
- Compare this to `../runbook-ops-assistant/`, which takes the same
  retrieval pattern and adds a guarded agent loop on top for actually
  acting on a runbook instead of just reading about one.
