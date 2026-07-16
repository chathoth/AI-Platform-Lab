"""
Example: 10_performance_diagnostics.py

A consolidated diagnostic script running through docs/16's checklist:
GPU/CPU placement, load vs. generation time, and model specs - the
"why is this slow" checklist made runnable. Ties back to
docs/16-Performance-Tuning.md.

Run:
    ollama pull llama3.1:8b
    python 10_performance_diagnostics.py
"""

import requests

BASE_URL = "http://localhost:11434"
MODEL = "llama3.1:8b"


def diagnose(model: str, prompt: str = "Explain what a load balancer does, briefly."):
    print(f"Diagnosing '{model}'...\n")

    # step 1: GPU or CPU?
    response = requests.post(f"{BASE_URL}/api/generate", json={"model": model, "prompt": prompt, "stream": False}).json()

    ps = requests.get(f"{BASE_URL}/api/ps").json()["models"]
    info = next((m for m in ps if m["name"] == model), None)
    if info:
        gpu_percent = round((info["size_vram"] / info["size"]) * 100) if info["size"] else 0
        print(f"1. Processor: {gpu_percent}% GPU" + (" - full GPU, good" if gpu_percent == 100 else " - CHECK: not fully on GPU, this could be your bottleneck"))

    # step 2: load vs. generation time
    load_s = response["load_duration"] / 1e9
    gen_s = response["eval_duration"] / 1e9
    print(f"2. Load time: {load_s:.2f}s" + (" - CHECK: significant cold-load cost, consider keep_alive tuning" if load_s > 1 else " - fine, likely already warm"))
    print(f"   Generation time: {gen_s:.2f}s for {response['eval_count']} tokens ({response['eval_count'] / max(gen_s, 0.001):.1f} tok/s)")

    # step 3: context window
    if info:
        print(f"3. Active context window: {info['context_length']} - right-sized to the task? (docs ch. 10)")

    # step 4: model size/quantization
    show = requests.post(f"{BASE_URL}/api/show", json={"model": model}).json()
    details = show.get("details", {})
    print(f"4. Model: {details.get('parameter_size', '?')} parameters, {details.get('quantization_level', '?')} quantization")


if __name__ == "__main__":
    diagnose(MODEL)
