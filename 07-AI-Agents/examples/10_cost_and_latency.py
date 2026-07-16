"""
Example: 10_cost_and_latency.py

Measure a real agent run's round-trip count and wall-clock time
against a single call. Reuses 02_one_tool_at_a_time_fix.py's verified
run_agent_fixed rather than a separate implementation, since that one
is already confirmed reliable. Ties back to
docs/17-Cost-and-Latency-of-Agentic-Systems.md.

Round-trip count is the reliable, deterministic part of this lesson -
it scales directly with agent turns, regardless of machine load.
Wall-clock time is included too, but it's sensitive to whatever else
is running on your machine at the time (this was very visible while
writing this example - a loaded local Ollama instance briefly made a
"single call" take 40-60s, which would have been a misleading number
to hardcode as an expectation). Compare your own timing numbers, don't
assume the ones printed here.

Run:
    ollama pull llama3.1:8b
    python 10_cost_and_latency.py
"""

import time
from importlib import import_module

from agent_tools import MODEL, client

fix_module = import_module("02_one_tool_at_a_time_fix")


def timed_call(messages: list[dict]) -> tuple[str, float]:
    start = time.time()
    response = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    elapsed = time.time() - start
    return response.choices[0].message.content, elapsed


if __name__ == "__main__":
    goal = "Check disk usage on db-primary-01, and if it is above 90%, restart the cleanup-service."

    print("--- single call (no tools, no loop) - always exactly 1 round trip ---")
    answer, elapsed = timed_call([{"role": "user", "content": "What is a Kubernetes readiness probe?"}])
    print(f"Round trips: 1")
    print(f"Time: {elapsed:.2f}s")

    print("\n--- full agent run (multi-turn loop, the verified fixed version) ---")
    agent_start = time.time()
    answer, tools_called = fix_module.run_agent_fixed(goal)
    agent_elapsed = time.time() - agent_start
    # run_agent_fixed makes one round trip per tool call, plus at least
    # one more for the final answer - a direct, deterministic count.
    round_trips = len(tools_called) + 1

    print(f"Round trips: {round_trips} ({len(tools_called)} tool calls + 1 final answer)")
    print(f"Time: {agent_elapsed:.2f}s")
    print(f"Tools called: {tools_called}")
    print(f"Final answer: {answer}")

    print()
    print(f"The agent made {round_trips} round trips versus the single call's 1 -")
    print("that ratio is the deterministic part of the cost story (docs ch. 17).")
    print("Wall-clock time tracks that ratio roughly, but is sensitive to")
    print("whatever else your machine is doing - compare your own numbers")
    print("across a few runs rather than trusting any single measurement.")
