# Examples

Ten self-contained scripts, each mapped to a technique from
[../docs/](../docs/). Same setup as module 01 — runs against a local
Ollama model by default, no API key needed.

## Setup

```bash
ollama pull llama3.1:8b   # supports tool calling, used throughout
pip install openai jsonschema jinja2
```

## Scripts

| Script                          | Concept                          | Docs chapter |
| -------------------------------- | ---------------------------------- | ------------ |
| `01_zero_shot_vs_few_shot.py`    | Calibrating to a team convention   | 03           |
| `02_chain_of_thought.py`         | Step-by-step reasoning accuracy    | 04           |
| `03_system_prompt_design.py`     | Identity, scope, tone, refusals    | 05           |
| `04_structured_json_output.py`   | Reliable JSON + schema validation  | 06           |
| `05_prompt_templates.py`         | Reusable templates with Jinja2     | 07           |
| `06_context_injection.py`        | Grounding answers in real data     | 08           |
| `07_prompt_chaining.py`          | Decomposing a multi-goal task      | 12           |
| `08_tool_calling.py`             | Model-requested function calls     | 14           |
| `09_prompt_injection_demo.py`    | Attack shape + delimiting defense  | 15           |
| `10_eval_prompt_variants.py`     | Scoring prompts against an eval set| 16           |

Run any of them directly:

```bash
python 01_zero_shot_vs_few_shot.py
```
