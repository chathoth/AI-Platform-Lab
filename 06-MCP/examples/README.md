# Examples

Ten self-contained scripts, each mapped to a concept from
[../docs/](../docs/). Every script was run for real while building
this module — against a real local MCP server (`01_server.py`), a real
local Ollama model where a model is involved, and no hosted API or
signup anywhere.

## Setup

```bash
ollama pull llama3.1:8b   # needed for 03 and 08
pip install mcp openai pydantic pytest pytest-asyncio
```

`01_server.py` is the shared server every other example connects to —
it's spawned automatically as a subprocess by each client script, so
you don't need to run it separately first. Run everything from inside
this `examples/` directory (the scripts reference `01_server.py` as a
relative path).

## Scripts

| Script                          | Concept                                   | Docs chapter |
| ---------------------------------- | -------------------------------------------- | ------------ |
| `01_server.py`                     | A complete server: tools, resources, prompt      | 05, 06, 07, 08 |
| `02_client_list_and_call.py`       | A complete client exercising all three primitives | 09           |
| `03_bridge_to_ollama.py`           | Bridging MCP tools into a local model's tool-calling | 10        |
| `04_resource_templates.py`         | Fixed resources vs. parameterized templates       | 06, 16       |
| `05_structured_errors.py`          | Structured error responses, not raw tracebacks     | 12           |
| `06_schema_design.py`              | Vague vs. precise auto-derived tool schemas          | 05, 11       |
| `07_authorization.py`              | A role-based guard clause inside a tool itself        | 13           |
| `08_sampling.py`                   | Server requests a completion, client fulfills it        | 15           |
| `09_discovery_summary.py`          | Generic capability discovery for any server               | 16           |
| `10_test_server.py`                | Automated tests, using the verified-working async pattern | 17     |

Run any client script directly:

```bash
python 02_client_list_and_call.py
```

Run the test file with pytest:

```bash
pytest 10_test_server.py -v
```

## A note on `10_test_server.py`

An earlier, tempting version of these tests used a shared
`@pytest.fixture` wrapping `stdio_client` — it produced intermittent
`RuntimeError: Attempted to exit cancel scope in a different task`
errors during teardown, even though every assertion passed. The
version in this file connects inside each test individually instead,
which is more repetitive but verified to run clean every time. See
`docs/17-Testing-an-MCP-Server.md` for the full story.
