# Module 10: End-to-End Projects

Two small projects that combine everything from modules 01-09 into
something closer to what I'd actually build for platform/DevOps work.
Both run entirely on local Ollama models - no hosted API keys, no
cost.

| Project | What it does | Builds on |
|---|---|---|
| [incident-similarity-finder](./incident-similarity-finder/) | Given a new incident description, finds the most similar past incidents by meaning, not keywords. Read-only, no agent. | Modules 03, 04, 05 |
| [runbook-ops-assistant](./runbook-ops-assistant/) | Retrieves the right runbook for a request, then runs a guarded agent loop that can actually act on it - checked by an allowlist and a human confirmation gate. | Modules 05, 07 |

## Why two, and in this order

`incident-similarity-finder` is pure retrieval: embed, store, query,
print results. It's the simplest possible useful thing to build with
this repo's concepts, and a good first project because there's nothing
in it that can go wrong destructively.

`runbook-ops-assistant` reuses that same retrieval pattern, then adds
the part that actually makes an "AI ops assistant" risky: real
actions. It exists specifically to demonstrate that a guardrail has to
live in code that runs regardless of what the model decides - not in
a prompt asking the model to be careful. Building it surfaced several
real, verified agent-reliability issues beyond what module 07 already
covered (see that project's README for the details) - the runbook's
multi-step nature exposed problems a single-step demo wouldn't have.

## Run either one

Each project is self-contained with its own README, `data/`, and
`src/`. Start with whichever matches what you want to see:

```bash
cd incident-similarity-finder && python src/index_incidents.py && python src/find_similar.py "..."
cd runbook-ops-assistant && python src/index_runbooks.py && python src/agent.py
```
