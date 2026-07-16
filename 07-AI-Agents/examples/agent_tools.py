"""
agent_tools.py

Shared tools and schemas used across every example in this directory
- kept in one place so the same tools stay consistent everywhere they
appear, instead of drifting between copies. Not numbered like the
other examples because Python can't import a module whose filename
starts with a digit (the same reason module 05-RAG's numbered scripts
aren't imported directly either).
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# Fake infrastructure state, standing in for real systems.
DISK_USAGE = {"db-primary-01": 92, "web-node-01": 41}


def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a host."""
    return {"hostname": hostname, "disk_percent": DISK_USAGE.get(hostname, 50)}


def restart_service(service_name: str) -> dict:
    """Restart a named service."""
    return {"service": service_name, "status": "restarted"}


def list_large_files(hostname: str) -> dict:
    """List the largest files/directories on a host."""
    return {"hostname": hostname, "large_files": ["/var/log/app.log (12GB)", "/var/log/old (18GB)"]}


TOOLS = {
    "get_disk_usage": get_disk_usage,
    "restart_service": restart_service,
    "list_large_files": list_large_files,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_disk_usage",
            "description": "Get current disk usage percentage for a host.",
            "parameters": {
                "type": "object",
                "properties": {"hostname": {"type": "string"}},
                "required": ["hostname"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "restart_service",
            "description": (
                "Restart a named service. Only call this if disk usage was "
                "confirmed ABOVE 90 percent by a previous get_disk_usage "
                "call in this conversation."
            ),
            "parameters": {
                "type": "object",
                "properties": {"service_name": {"type": "string"}},
                "required": ["service_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_large_files",
            "description": "List the largest files or directories on a host, to investigate disk usage.",
            "parameters": {
                "type": "object",
                "properties": {"hostname": {"type": "string"}},
                "required": ["hostname"],
            },
        },
    },
]
