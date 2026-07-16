# Examples

Three short, verified scripts against local Ollama.

```bash
ollama pull llama3.1:8b
pip install langchain langchain-ollama
```

| Script                                     | Concept                                   |
| --------------------------------------------- | ---------------------------------------------- |
| `01_basic_chain.py`                            | Prompt → model → output parser (LCEL)             |
| `02_tool_calling.py`                           | `@tool` + `bind_tools()`                              |
| `03_module_07_lesson_still_applies.py`         | Confirms module 07's tool-batching finding reproduces here too |

Run any of them directly: `python 01_basic_chain.py`
