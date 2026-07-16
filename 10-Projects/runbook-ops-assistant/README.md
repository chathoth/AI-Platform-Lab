# Project: Runbook Ops Assistant

A small ops assistant that retrieves the right runbook for an incident
(RAG) and then actually acts on it through a guarded agent loop -
checking, deciding, and only performing a destructive action after
passing an allowlist and a human confirmation gate enforced in code.

This is the second, more advanced 10-Projects build. Where
`../incident-similarity-finder/` is pure read-only retrieval, this
project adds real (simulated) actions - which is exactly why it needs
module 07's guardrail lessons, not just module 05's RAG pattern.

## Why this is useful in a platform/DevOps context

"An AI that can search runbooks" is a nice-to-have. "An AI that can
search runbooks AND is structurally prevented from doing something
destructive without approval" is what you'd actually need before
letting anything touch production. This project builds the smallest
version of that second thing, from concepts already covered here:

- [Module 05 - RAG](../../05-RAG/) - retrieve the relevant runbook before deciding anything
- [Module 07 chapter 08](../../07-AI-Agents/docs/08-One-Tool-at-a-Time-A-Verified-Reliability-Lesson.md) - one tool call per turn, always observe before the next decision
- [Module 07 chapter 13](../../07-AI-Agents/docs/13-Guardrails-and-Human-in-the-Loop.md) - allowlist + confirmation gate enforced in code, not left to the model's judgment

## How it works

```text
data/runbooks/*.md  --embed-->  chroma_db/ ("runbooks" collection)
                                      ^
                                      |
"disk alert on db-replica-03" --embed--> retrieve top runbook
                                      |
                                      v
                     guarded agent loop (one tool call/turn)
                       get_disk_usage -> list_large_files -> cleanup_old_logs
                                      |
                        execute_tool(): allowlist + confirmation gate
```

1. `src/index_runbooks.py` embeds 4 runbooks (disk cleanup, service
   restart, deployment rollback, CoreDNS restart) into a persistent
   Chroma collection - same `OllamaEmbeddingFunction` pattern used in
   `../incident-similarity-finder/` and module 04.
2. `src/tools.py` defines 2 read-only tools (`get_disk_usage`,
   `list_large_files`) and 4 destructive tools (`cleanup_old_logs`,
   `restart_service`, `rollback_deployment`, `restart_coredns`) -
   simulated, no real infrastructure is touched.
3. `src/agent.py` retrieves the single most relevant runbook for the
   request, puts it in the system prompt, then runs a guarded loop:
   one tool call per turn (module 07 ch. 08's fix), and every
   destructive call passes through `execute_tool()`'s allowlist +
   confirmation gate (module 07 ch. 13) before it actually runs.

## Run it

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
pip install chromadb requests openai

cd src
python index_runbooks.py
python agent.py
```

### Verified output (3 scenarios, same request, different guardrail outcomes)

Request: *"Disk usage alert fired for db-replica-03. What should I do?"*
(db-replica-03 is simulated at 88% - above the runbook's 85% cleanup threshold)

**Scenario 1 - operator role, human approves:**

```text
[retrieved runbook: disk-cleanup.md]
  -> get_disk_usage({'hostname': 'db-replica-03'}) = {'disk_percent': 88}
  -> list_large_files({'hostname': 'db-replica-03'}) = {'large_files': [...]}
  -> cleanup_old_logs({'hostname': 'db-replica-03'}) = {'status': 'old logs removed'}
```

The destructive action actually ran, only after the read-only checks
that the runbook requires, and only after passing the confirmation
gate. (See "What went wrong first" below for what happened after this
point.)

**Scenario 2 - operator role, human declines:**

```text
  -> cleanup_old_logs(...) = {'error': True, 'message': 'Action declined by human reviewer.'}
  -> cleanup_old_logs(...) = {'error': True, 'message': 'Action declined by human reviewer.'}

Final response: STOPPED: cleanup_old_logs was denied twice - not retrying further. Escalate to a human operator.
```

**Scenario 3 - readonly role, blocked before confirmation is even asked:**

```text
  -> cleanup_old_logs(...) = {'error': True, 'message': "cleanup_old_logs requires the 'operator' role. Caller was 'readonly'."}
  -> cleanup_old_logs(...) = {'error': True, 'message': "cleanup_old_logs requires the 'operator' role. Caller was 'readonly'."}

Final response: STOPPED: cleanup_old_logs was denied twice - not retrying further. Escalate to a human operator.
```

All three scenarios call the exact same real tool - only
`execute_tool()`'s guardrail changes the outcome. That's the point:
the safety boundary lives in code that runs regardless of what the
model decided, not in a hope that the model reasons correctly.

## What went wrong first (real, verified findings)

Nothing above worked on the first try. Each of these was actually
observed while building this project, not anticipated in advance -
consistent with how every other module in this repo documents real
failures instead of hiding them.

1. **The model narrated actions instead of calling them.** After the
   first tool result, llama3.1:8b would often write "Let's call
   `cleanup_old_logs`..." as plain text instead of issuing a real tool
   call. Module 07 chapter 08's single one-shot nudge (works for a
   1-2 step goal) wasn't enough for this runbook's 3-4 step sequence -
   the model kept narrating after almost every step.

2. **A generic nudge made it worse, not better.** Nudging with "make a
   real tool call now" sometimes caused the model to treat its own
   narration as if the action had already happened, and it skipped
   straight to the *next* runbook step - meaning the destructive
   action was never actually called, but the agent behaved as if it
   was done. If any surrounding system had trusted that narration as
   confirmation, it would have silently skipped the guardrail
   entirely, since `execute_tool()` only ever runs on real tool calls.
   The fix that worked reliably: when the model stalls, detect which
   tool it *named* in its own text and nudge for that specific tool by
   name - see `build_nudge()` in `src/agent.py`.

3. **A guardrail decline doesn't stop the model from asking again.**
   Even after `cleanup_old_logs` was declined, the model just called
   it again on the next turn. `agent.py` now caps this: if the exact
   same call is denied twice in a row, the loop stops and reports
   "escalate to a human operator" instead of retrying indefinitely.

4. **The happy path doesn't cleanly stop either.** After the approved
   cleanup actually succeeded (scenario 1), the model sometimes kept
   re-verifying with more read-only checks instead of declaring the
   runbook complete, eventually hitting the step budget. This is
   harmless (only read-only calls repeat, never the destructive one
   again), but it's a real reminder that module 07 chapter 09's
   stopping conditions matter for successful runs too, not only for
   catching failures.

## What to try next

- Add a runbook for a scenario this repo's incidents cover but this
  project doesn't yet - the DNS/CoreDNS and rollback runbooks are
  already in `data/runbooks/` but not exercised in `agent.py`'s demo.
- Swap `auto_confirm` for a real `input()` prompt (already the
  default when `auto_confirm=None`) to approve/decline interactively.
- Compare this project's guardrail pattern to
  `../incident-similarity-finder/`, which deliberately has no
  destructive tools at all - a reminder that the safest agent is
  often one that can't act, only inform.
