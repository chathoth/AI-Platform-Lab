"""
Example: 01_server.py

A complete, minimal MCP server exposing a tool, a resource, and a
prompt. This is the shared server every other example in this
directory connects to - it has zero knowledge of which client or
model will eventually call it. Ties back to
docs/08-Building-a-Minimal-MCP-Server.md.

Run standalone (it will block waiting for a client - that's correct):
    pip install mcp
    python 01_server.py

More useful: run it through one of the client examples (02+), or
explore it interactively with the MCP Inspector:
    npx @modelcontextprotocol/inspector python3 01_server.py
"""

import mcp.types as types
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("infra-tools")


@mcp.tool()
def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a given host. Use this
    when asked about disk space, storage capacity, or whether a host
    is running low on disk."""
    known_hosts = {"db-primary-01": 92, "web-node-01": 41}
    if hostname not in known_hosts:
        return {
            "error": True,
            "message": f"Unknown hostname: {hostname!r}. Known hosts: {list(known_hosts)}",
        }
    return {"hostname": hostname, "disk_percent": known_hosts[hostname]}


ALLOWED_TOOLS_BY_ROLE = {
    "readonly": {"get_disk_usage"},
    "operator": {"get_disk_usage", "restart_service"},
}


@mcp.tool()
def restart_service(service_name: str, environment: str, caller_role: str = "readonly") -> dict:
    """Restart a named service in a given environment. DESTRUCTIVE -
    requires the 'operator' role. Never allowed against 'prod' via
    this tool, regardless of role."""
    if "restart_service" not in ALLOWED_TOOLS_BY_ROLE.get(caller_role, set()):
        return {"error": True, "retryable": False, "message": f"Role {caller_role!r} is not authorized for restart_service."}
    if environment == "prod":
        return {"error": True, "retryable": False, "message": "restart_service is never allowed against 'prod' via this tool."}
    return {"service": service_name, "environment": environment, "status": "restarted"}


@mcp.resource("runbook://crashloop")
def crashloop_runbook() -> str:
    """Runbook for debugging CrashLoopBackOff."""
    return "Check kubectl describe pod and kubectl logs --previous."


@mcp.resource("runbook://{topic}")
def get_runbook(topic: str) -> str:
    """Get the runbook for a specific topic."""
    runbooks = {
        "crashloop": "Check kubectl describe pod and logs --previous.",
        "disk-full": "Check for oversized log files before resizing.",
    }
    return runbooks.get(topic, f"No runbook found for topic: {topic!r}")


@mcp.prompt()
def incident_summary(log_text: str) -> str:
    """Build a prompt that summarizes an incident log."""
    return f"Summarize this incident log in 2 sentences:\n{log_text}"


@mcp.tool()
async def summarize_via_client(text: str, ctx: Context) -> str:
    """Ask the CLIENT's model to summarize text, instead of calling an
    LLM directly - see docs/15-Sampling-Servers-Requesting-Completions.md."""
    result = await ctx.session.create_message(
        messages=[types.SamplingMessage(
            role="user",
            content=types.TextContent(type="text", text=f"Summarize in 5 words: {text}"),
        )],
        max_tokens=50,
    )
    return result.content.text


if __name__ == "__main__":
    mcp.run(transport="stdio")
