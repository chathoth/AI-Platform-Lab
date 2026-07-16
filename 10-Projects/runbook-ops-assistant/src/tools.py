"""
tools.py

Shared simulated ops tools, kept in one un-numbered file so every
script in this project uses the same tool definitions and fake
infrastructure state (same reasoning as module 07's agent_tools.py -
Python can't import a module whose filename starts with a digit).

Two read-only tools and three destructive ones, matching the actions
described in data/runbooks/.
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# Fake infrastructure state, standing in for real systems.
DISK_USAGE = {"db-replica-03": 88, "web-node-02": 45}
LARGE_FILES = {
    "db-replica-03": ["/var/log/postgres/old-wal-archive (22GB)", "/var/log/app/rotated (9GB)"],
    "web-node-02": ["/var/log/nginx/access.log.old (3GB)"],
}


def get_disk_usage(hostname: str) -> dict:
    """Get current disk usage percentage for a host."""
    return {"hostname": hostname, "disk_percent": DISK_USAGE.get(hostname, 50)}


def list_large_files(hostname: str) -> dict:
    """List the largest files or directories on a host."""
    return {"hostname": hostname, "large_files": LARGE_FILES.get(hostname, [])}


def cleanup_old_logs(hostname: str) -> dict:
    """Delete old, rotated log files on a host to free disk space.
    Only call this if disk usage was confirmed at or above 85 percent
    by a previous get_disk_usage call in this conversation."""
    return {"hostname": hostname, "status": "old logs removed"}


def restart_service(service_name: str) -> dict:
    """Restart a named service. Only call this if the service is
    confirmed unresponsive right now, and the cause is NOT a recent
    bad deploy (use rollback_deployment for that instead)."""
    return {"service": service_name, "status": "restarted"}


def rollback_deployment(service_name: str) -> dict:
    """Roll back a service to its last known-good deployment revision.
    Only call this if the failure is confirmed to correlate with a
    recent deploy."""
    return {"service": service_name, "status": "rolled back to previous revision"}


def restart_coredns() -> dict:
    """Restart CoreDNS cluster-wide to force a configuration refresh.
    Only call this if DNS resolution failures were actually confirmed,
    not just suspected from a vague symptom."""
    return {"status": "coredns restarted"}


READ_ONLY_TOOLS = {"get_disk_usage", "list_large_files"}
DESTRUCTIVE_TOOLS = {"cleanup_old_logs", "restart_service", "rollback_deployment", "restart_coredns"}

TOOLS = {
    "get_disk_usage": get_disk_usage,
    "list_large_files": list_large_files,
    "cleanup_old_logs": cleanup_old_logs,
    "restart_service": restart_service,
    "rollback_deployment": rollback_deployment,
    "restart_coredns": restart_coredns,
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
            "name": "list_large_files",
            "description": "List the largest files or directories on a host, to investigate disk usage.",
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
            "name": "cleanup_old_logs",
            "description": (
                "Delete old, rotated log files on a host to free disk space. "
                "Only call this if disk usage was confirmed at or above 85 percent "
                "by a previous get_disk_usage call in this conversation."
            ),
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
                "Restart a named service. Only call this if the service is confirmed "
                "unresponsive right now, and the cause is NOT a recent bad deploy."
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
            "name": "rollback_deployment",
            "description": (
                "Roll back a service to its last known-good deployment revision. "
                "Only call this if the failure correlates with a recent deploy."
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
            "name": "restart_coredns",
            "description": (
                "Restart CoreDNS cluster-wide to force a configuration refresh. "
                "Only call this if DNS resolution failures were actually confirmed."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]
