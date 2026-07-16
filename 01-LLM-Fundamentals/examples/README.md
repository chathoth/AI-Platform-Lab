# Examples

Ten small, self-contained scripts. Each one maps to a concept from
[../docs/](../docs/) and can be run on its own.

## Setup

All examples run against a **local Ollama model by default** - no API
key, no cost, safe to experiment freely.

```bash
# 1. install Ollama: https://ollama.com
ollama pull llama3.1:8b
ollama pull llama3.2:1b   # used by 05_compare_models.py

# 2. install Python deps
pip install openai tiktoken
```

To point any script at a hosted API (OpenAI, etc.) instead of Ollama,
see the commented-out block at the bottom of each file - it's usually
just swapping the `OpenAI(...)` client construction and model name.

## Scripts

| Script                     | Concept                          | Docs chapter |
| --------------------------- | --------------------------------- | ------------ |
| `01_token_count.py`         | Counting tokens                   | 04           |
| `02_first_api_call.py`      | The basic request/response loop   | 01, 03       |
| `03_compare_temperature.py` | Temperature and determinism       | 10           |
| `04_compare_top_p.py`       | Top-p (nucleus) sampling          | 10           |
| `05_compare_models.py`      | Model size vs. speed/quality      | 12, 15       |
| `06_json_output.py`         | Structured output + validation    | 16, 18       |
| `07_streaming.py`           | Streaming and time-to-first-token | 03           |
| `08_chat_completion.py`     | Multi-turn chat, stateless memory | 08, 16       |
| `09_summarization.py`       | Grounded summarization            | 09, 11       |
| `10_translation.py`         | Translation for on-call comms     | 01           |

Run any of them directly:

```bash
python 01_token_count.py
```
