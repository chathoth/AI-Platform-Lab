# Examples

Ten self-contained scripts, each mapped to a concept from
[../docs/](../docs/), plus a shared `agent_tools.py` every other
script imports from. Every script was run for real against local
Ollama (`llama3.1:8b`) while building this module — including finding
and fixing three real bugs along the way (see "What testing found"
below).

## Setup

```bash
ollama pull llama3.1:8b
pip install openai tiktoken
```

`agent_tools.py` isn't numbered like the others because Python can't
import a module whose filename starts with a digit — the same reason
module 05-RAG's numbered scripts aren't imported directly either.
Scripts that need to reuse `02_one_tool_at_a_time_fix.py`'s functions
use `importlib.import_module("02_one_tool_at_a_time_fix")`, which
works around that restriction.

## Scripts

| Script                              | Concept                                       | Docs chapter |
| -------------------------------------- | ------------------------------------------------ | ------------ |
| `agent_tools.py`                        | Shared tools/schemas used across every example      | 06           |
| `01_basic_agent_loop.py`                | A complete reason-act-observe loop                    | 07           |
| `02_one_tool_at_a_time_fix.py`          | The verified failure and its fix, side by side         | 08           |
| `03_stopping_conditions.py`             | Step limit, token budget, repetition detection            | 09           |
| `04_reflection.py`                      | A self-review step catching a bad action after the fact     | 10           |
| `05_guardrails.py`                      | Code-level allowlist and confirmation gate                     | 13           |
| `06_tracing.py`                         | A full step-by-step trace that makes the bug visible               | 14           |
| `07_evaluation.py`                      | Scoring broken vs. fixed agents against an eval set                  | 15           |
| `08_planning.py`                        | Getting a plan, then comparing it to what actually happened            | 05           |
| `09_multi_agent_supervisor.py`          | A supervisor routing to two narrower worker agents                       | 11, 12       |
| `10_cost_and_latency.py`                | Round-trip count and timing, single call vs. agent loop                    | 17           |

Run any of them directly:

```bash
python 01_basic_agent_loop.py
```

## What testing found

Three real bugs surfaced while verifying these examples, all fixed in
the code (not just noted as caveats):

1. **The core lesson itself** (`02_one_tool_at_a_time_fix.py`) — the
   basic agent, allowed to batch tool calls, reliably restarted a
   service under a condition that wasn't met. This is this module's
   central, repeatedly-reproduced finding, not a one-off.
2. **A "narrates instead of calls" quirk** — even the one-tool-at-a-
   time fix sometimes described a needed action in text instead of
   actually issuing the tool call, when the system prompt phrasing
   was too tentative. Fixed with a bounded, one-time "confirm the goal
   is actually complete" nudge — see `02_one_tool_at_a_time_fix.py`'s
   `run_agent_fixed`.
3. **A misrouted supervisor** (`09_multi_agent_supervisor.py`) — a
   zero-shot routing prompt classified "restart the cleanup-service"
   as DIAGNOSIS instead of REMEDIATION. A few-shot prompt (module 02
   chapter 03) fixed it.

None of these were hypothetical — all three were caught by actually
running the code against a real local model, which is exactly the
point of this module's "verify, don't assume" approach.
