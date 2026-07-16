"""
Example: 04_reflection.py

Add a reflection step that checks whether a just-taken action was
actually justified - applied directly to the verified chapter 08
failure. Ties back to docs/10-Reflection-and-Self-Correction.md.

Run:
    ollama pull llama3.1:8b
    python 04_reflection.py
"""

from agent_tools import MODEL, client


def reflect(goal: str, recent_action: str, recent_result: dict) -> str:
    prompt = f"""Goal: {goal}
Action just taken: {recent_action}
Result: {recent_result}

Was this action actually justified by the goal's conditions, based on
the result? Answer YES or NO, with a one-sentence reason."""
    response = client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # This is chapter 08's exact verified failure: the agent restarted
    # cleanup-service even though disk usage was 41%, well under the
    # 90% threshold. Applying reflection right after that action:
    goal = "Check disk usage on web-node-01, and if it is above 90%, restart the cleanup-service."
    recent_action = "restart_service('cleanup-service')"
    recent_result = {"disk_percent": 41}

    print(f"Goal: {goal}")
    print(f"Action taken: {recent_action}")
    print(f"Result observed: {recent_result}\n")

    verdict = reflect(goal, recent_action, recent_result)
    print(f"Reflection: {verdict}")
    print()
    print("A reflection step catching this DURING a run - instead of only")
    print("being visible afterward in a transcript - is what lets an agent")
    print("flag its own mistake before it's too late to matter.")
