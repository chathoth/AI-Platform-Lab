"""
Example: 08_planning.py

Ask the model to sketch a plan BEFORE acting, then run the actual
agent and compare what it planned against what it actually did. Ties
back to docs/05-Planning-Breaking-a-Goal-Into-Steps.md.

Run:
    ollama pull llama3.1:8b
    python 08_planning.py
"""

from importlib import import_module

from agent_tools import MODEL, client

fix_module = import_module("02_one_tool_at_a_time_fix")


def get_plan(goal: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Before taking any action, list the likely steps to accomplish this goal. Just the plan, no action yet.\n\nGoal: {goal}"}],
        temperature=0.3,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    goal = "Check disk usage on db-primary-01, and if it is above 90%, restart the cleanup-service."

    print(f"Goal: {goal}\n")
    print("--- plan ---")
    print(get_plan(goal))

    print("\n--- what actually happened (the real agent run) ---")
    answer, tools_called = fix_module.run_agent_fixed(goal)
    print(f"Tools called: {tools_called}")
    print(f"Final answer: {answer}")

    print()
    print("Compare the plan's steps to what the agent actually did - a plan")
    print("is a starting guess (docs ch. 05), not something the loop is")
    print("bound to follow exactly.")
