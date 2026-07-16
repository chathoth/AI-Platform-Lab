# Examples

Ten self-contained scripts, each mapped to a concept from
[../docs/](../docs/). Every script was run for real against a local
Ollama instance while building this module, calling the native and
OpenAI-compatible APIs directly — no mocking, no simulated output.

## Setup

```bash
ollama pull llama3.1:8b
ollama pull llama3.2:3b
ollama pull nomic-embed-text
pip install requests openai
```

## Scripts

| Script                              | Concept                                       | Docs chapter |
| -------------------------------------- | ------------------------------------------------ | ------------ |
| `01_check_server_and_models.py`         | Health check + listing pulled models                 | 02, 03       |
| `02_native_api_calls.py`                | Calling generate/chat/embeddings directly              | 04           |
| `03_openai_vs_native.py`                | Confirming both endpoints hit the same server             | 05           |
| `04_build_custom_model.py`              | Building a custom model via `/api/create`, no CLI            | 06           |
| `05_model_specs.py`                     | Reading real specs for every pulled model                       | 03, 07       |
| `06_gpu_cpu_check.py`                   | Checking processor placement via the API                          | 09           |
| `07_context_window_memory.py`           | Measuring the real memory cost of `num_ctx`                          | 10           |
| `08_streaming_ttft.py`                  | Time-to-first-token vs. total generation time                           | 13           |
| `09_keep_alive_tuning.py`               | How long a model stays loaded, verified against real timing               | 16           |
| `10_performance_diagnostics.py`         | The "why is this slow" checklist, made runnable                             | 16           |

Run any of them directly:

```bash
python 01_check_server_and_models.py
```

## What testing found

Two real, non-obvious behaviors surfaced while verifying these
examples, both reflected in the code and the docs (not just noted as
caveats):

1. **`keep_alive=0` is not instant when combined with a real prompt.**
   A bare `keep_alive=0` "ping" with no prompt unloads a model
   immediately — but sending it alongside an actual generation request
   takes a couple of seconds to actually clear the model from memory.
   `09_keep_alive_tuning.py` polls briefly instead of assuming either
   timing, and `docs/16-Performance-Tuning.md` was corrected to say
   "shortly after" instead of "immediately."
2. **Capability differences are real and checkable.** Running
   `05_model_specs.py` against this module's own four pulled models
   showed `nomic-embed-text` reporting only `['embedding']` (no
   `completion`), and `phi3:3.8b` reporting `['completion']` with no
   `tools` support — confirming directly that not every local model
   supports tool calling, worth checking before assuming.
