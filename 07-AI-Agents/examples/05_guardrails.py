"""
Example: 05_guardrails.py

An allowlist and a confirmation gate, enforced in CODE rather than
relying on the model's own judgment. Applied to chapter 08's exact
scenario to show it catches what the model's reasoning missed. Ties
back to docs/13-Guardrails-and-Human-in-the-Loop.md.

Run:
    python 05_guardrails.py
"""

from agent_tools import TOOLS

ALLOWED_TOOLS = {"get_disk_usage", "list_large_files"}  # read-only, safe by default
DESTRUCTIVE_TOOLS = {"restart_service"}


def execute_tool(name: str, args: dict, caller_role: str = "readonly") -> dict:
    if name in DESTRUCTIVE_TOOLS and caller_role != "operator":
        return {"error": True, "message": f"{name} requires the 'operator' role. Caller was {caller_role!r}."}
    if name not in ALLOWED_TOOLS and name not in DESTRUCTIVE_TOOLS:
        return {"error": True, "message": f"{name} is not a recognized tool."}
    return TOOLS[name](**args)


def execute_tool_with_confirmation(name: str, args: dict, auto_confirm: bool | None = None) -> dict:
    """auto_confirm lets this run non-interactively for demo purposes -
    in a real system, this would be a real prompt to a human."""
    if name in DESTRUCTIVE_TOOLS:
        if auto_confirm is None:
            confirmed = input(f"Agent wants to call {name}({args}). Allow? [y/N] ").lower() == "y"
        else:
            confirmed = auto_confirm
        if not confirmed:
            return {"error": True, "message": "Action declined by human reviewer."}
    return TOOLS[name](**args)


if __name__ == "__main__":
    print("--- allowlist: readonly role tries a destructive tool ---")
    result = execute_tool("restart_service", {"service_name": "cleanup-service"}, caller_role="readonly")
    print(" ", result)

    print("\n--- allowlist: operator role, same tool ---")
    result = execute_tool("restart_service", {"service_name": "cleanup-service"}, caller_role="operator")
    print(" ", result)

    print("\n--- confirmation gate: applied to chapter 08's exact scenario ---")
    print("    (disk usage was 41%, well under 90% - a human should decline this)")
    result = execute_tool_with_confirmation(
        "restart_service", {"service_name": "cleanup-service"}, auto_confirm=False
    )
    print(" ", result)
    print()
    print("This is the guardrail that would have caught chapter 08's mistake")
    print("regardless of how the model reasoned about it upstream.")
