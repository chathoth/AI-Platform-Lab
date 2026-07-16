"""
Example: 09_summarization.py

Summarize a raw incident log into a short, structured summary - a
realistic "shrink this wall of text" task. Ties back to
docs/09-Context-Window.md (chunking long input) and
docs/11-Hallucinations.md (grounding the model in the actual text).

Run:
    ollama pull llama3.1:8b
    python 09_summarization.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# A stand-in for a real incident log / postmortem thread.
incident_log = """
09:01 UTC - Alert fired: high 5xx rate on checkout-service (>15%)
09:02 UTC - On-call engineer acknowledged, began investigating
09:04 UTC - Noted checkout-service pods restarting repeatedly (CrashLoopBackOff)
09:06 UTC - kubectl describe showed OOMKilled, exit code 137
09:08 UTC - Recent deploy 20 minutes prior bumped batch size in worker config
09:10 UTC - Rolled back to previous deployment revision
09:13 UTC - Pods stabilized, 5xx rate returned to baseline
09:15 UTC - Root cause: new batch size config exceeded pod memory limit
09:20 UTC - Follow-up: add memory limit alerting before next batch-size change
"""

system_prompt = (
    "You summarize incident logs for an engineering status update. "
    "Only use information present in the log - do not invent details. "
    "Respond with: Impact, Root Cause, Resolution, Follow-up (one line each)."
)


def summarize(log_text: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": log_text},
        ],
        temperature=0.2,  # low - this is a factual task, not a creative one
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("Raw log:")
    print(incident_log)
    print("Summary:")
    print(summarize(incident_log))
    print()
    print("Notice the system prompt explicitly says 'only use information")
    print("present in the log' - that instruction is a cheap, useful")
    print("guardrail against hallucination (docs/11-Hallucinations.md),")
    print("though it doesn't replace actually verifying the output.")
