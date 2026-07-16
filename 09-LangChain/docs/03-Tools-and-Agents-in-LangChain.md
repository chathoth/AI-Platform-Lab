# 03 - Tools and Agents in LangChain

Module 02 chapter 14 defined tools as a schema dict plus a Python
function. LangChain's `@tool` decorator does the same thing, deriving
the schema from type hints and the docstring — the same auto-derivation
module 06's MCP `@mcp.tool()` uses.

``` python
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a host."""
    known = {"db-primary-01": 92, "web-node-01": 41}
    return {"hostname": hostname, "disk_percent": known.get(hostname, 50)}

llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434", temperature=0)
llm_with_tools = llm.bind_tools([get_disk_usage])

response = llm_with_tools.invoke("Is disk usage on db-primary-01 critical?")
print(response.tool_calls)
```

Verified output:
`[{'name': 'get_disk_usage', 'args': {'hostname': 'db-primary-01'}, ...}]`
— the model correctly requested the tool call, exactly like module 02
chapter 14's hand-rolled version, just with `bind_tools()` instead of
passing a raw schema list.

## Agents: The Loop From Module 07, Framework-Assisted

Module 07 built the reason-act-observe loop by hand — including
finding, in that exact process, that batching multiple tool calls into
one turn causes real, verified incorrect actions (module 07 chapter
08). LangChain's agent executors run the same loop, but **that finding
still applies** — the framework doesn't automatically protect against
it. The guardrails module 07 chapter 13 built (allowlists, confirmation
gates, forcing deliberate steps) are still your responsibility whether
the loop is hand-written or framework-provided.

**The practical takeaway:** LangChain's agent tooling is worth using
for the boilerplate it removes — not as a reason to skip the
reliability lessons module 07 verified directly. A framework doesn't
make an unreliable pattern reliable; it just makes the reliable
pattern faster to wire up.

## Next Chapter

➡️ `04-Best-Practices-and-Interview-Questions.md`
