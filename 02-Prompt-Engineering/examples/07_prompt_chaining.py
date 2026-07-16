"""
Example: 07_prompt_chaining.py

Break "analyze this incident" into three independently-checkable
steps instead of one prompt trying to do everything at once. Ties
back to docs/12-Prompt-Chaining.md.

Run:
    ollama pull llama3.1:8b
    python 07_prompt_chaining.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

incident_log = """
09:01 UTC - Alert fired: high 5xx rate on checkout-service (>15%)
09:04 UTC - Noted checkout-service pods restarting repeatedly (CrashLoopBackOff)
09:06 UTC - kubectl describe showed OOMKilled, exit code 137
09:08 UTC - Recent deploy 20 minutes prior bumped batch size in worker config
09:10 UTC - Rolled back to previous deployment revision
09:13 UTC - Pods stabilized, 5xx rate returned to baseline
"""


def extract_root_cause(log_text: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"In one sentence, what is the root cause in this log?\n{log_text}"}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()


def draft_status_update(root_cause: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": (
            f"Write a 2-sentence customer-facing status update for this "
            f"root cause, with no technical jargon: {root_cause}"
        )}],
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()


def suggest_action_items(root_cause: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": (
            f"Suggest 3 short follow-up action items for this root cause, "
            f"as a numbered list: {root_cause}"
        )}],
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()


if __name__ == "__main__":
    # Step 1 - fail loudly here before wasting two more calls on a bad input.
    root_cause = extract_root_cause(incident_log)
    if not root_cause:
        raise RuntimeError("root cause extraction failed - stopping the chain")
    print(f"1. Root cause:\n   {root_cause}\n")

    # Steps 2 and 3 both depend on step 1's output, not on each other,
    # so this is where you'd parallelize in a real pipeline.
    status_update = draft_status_update(root_cause)
    print(f"2. Status update:\n   {status_update}\n")

    action_items = suggest_action_items(root_cause)
    print(f"3. Action items:\n{action_items}\n")

    print("Each step above is independently checkable - if step 2's")
    print("wording is off, you fix step 2's prompt without touching")
    print("the other two.")
