"""
Example: 02_tool_calling.py

The @tool decorator and bind_tools() - LangChain's version of module
02 chapter 14's hand-rolled tool calling. Ties back to
docs/03-Tools-and-Agents-in-LangChain.md.

Run:
    ollama pull llama3.1:8b
    python 02_tool_calling.py
"""

from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a host."""
    known = {"db-primary-01": 92, "web-node-01": 41}
    return {"hostname": hostname, "disk_percent": known.get(hostname, 50)}


llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434", temperature=0)
llm_with_tools = llm.bind_tools([get_disk_usage])

if __name__ == "__main__":
    response = llm_with_tools.invoke("Is disk usage on db-primary-01 critical?")
    print("tool_calls:", response.tool_calls)

    for call in response.tool_calls:
        result = get_disk_usage.invoke(call["args"])
        print(f"{call['name']}({call['args']}) -> {result}")
