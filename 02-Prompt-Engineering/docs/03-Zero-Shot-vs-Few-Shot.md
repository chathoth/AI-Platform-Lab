# 03 - Zero-Shot vs Few-Shot Prompting

## Introduction

This is the first real technique choice in the module, and it's one I
make almost every time I write a prompt: do I just ask, or do I show
examples first? The trade-off is familiar — it's the same one behind
whether I write a detailed runbook or trust an experienced engineer to
figure it out from a one-line ticket description.

## Learning Objectives

After this chapter I should be able to:

-   Define zero-shot and few-shot prompting.
-   Explain why few-shot examples work (tying back to GPT-3's few-shot
    learning from module 01's history chapter).
-   Choose the right number of examples for a task.
-   Recognize when few-shot examples backfire.

------------------------------------------------------------------------

# Zero-Shot: Just Ask

``` text
Classify the severity of this alert as LOW, MEDIUM, or HIGH:
"Disk usage at 92% on db-primary-02"
```

No examples given — the model relies entirely on what it learned during
training to infer what "severity" means and how to map this alert to a
category. Works well for common, well-understood tasks the model has
seen a huge amount of during training (this is a direct callback to
GPT-3's few-shot *capability* emerging from pretraining scale, covered
in module 01 chapter 02).

## Few-Shot: Show, Then Ask

``` text
Classify the severity of the alert as LOW, MEDIUM, or HIGH.

Alert: "CPU usage at 45% on web-node-01"
Severity: LOW

Alert: "Disk usage at 98% on db-primary-01, 20 minutes to full"
Severity: HIGH

Alert: "Memory usage at 78% on cache-node-03"
Severity: MEDIUM

Alert: "Disk usage at 92% on db-primary-02"
Severity:
```

Given 2-4 labeled examples, the model infers the *pattern* — not just
"what severity means" in the abstract, but specifically how your team
draws the line between MEDIUM and HIGH. This is the single best lever
for making output match an internal convention that isn't publicly
documented anywhere the model could have learned it.

**Platform analogy:** zero-shot is trusting an experienced hire to
handle a ticket from a one-line description, relying on general
industry knowledge. Few-shot is handing them three resolved tickets
from your own queue first — same general skill, now calibrated to how
*your* team actually classifies severity. Neither is "wrong"; you pick
based on how standardized the task is.

## How Many Examples?

  Examples   When to use
  ---------- --------------------------------------------------------
  0 (zero-shot) Common, well-understood tasks; free-text answers
  1 (one-shot)   Mainly to pin the exact output *format*, not the logic
  2-5 (few-shot) Team-specific conventions, edge-case handling, classification
  6+             Diminishing returns; costs real tokens (chapter 04, module 01) with little accuracy gain past a handful of good examples

More examples cost more tokens on **every single call**, not just once
— the same "recurring cost vs. one-time cost" trade-off from choosing
between fine-tuning and RAG in module 01. If a handful of examples
reliably nails the pattern, adding a dozen more rarely earns its keep.

## When Few-Shot Backfires

Bad or inconsistent examples teach the model your inconsistency, not
your intent — the model has no way to know which of your examples was
the anomaly. Also watch for **order/recency bias**: models weight later
examples somewhat more heavily, so if your last example is
unrepresentative, it can skew everything after it.

## Hands-on: Measure the Difference

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

alert = "Disk usage at 92% on db-primary-02, 20 minutes to full"

zero_shot = f'Classify the severity of this alert as LOW, MEDIUM, or HIGH:\n"{alert}"\nSeverity:'

few_shot = f'''Classify the severity of the alert as LOW, MEDIUM, or HIGH.

Alert: "CPU usage at 45% on web-node-01"
Severity: LOW

Alert: "Disk usage at 98% on db-primary-01, 5 minutes to full"
Severity: HIGH

Alert: "Memory usage at 78% on cache-node-03"
Severity: MEDIUM

Alert: "{alert}"
Severity:'''

for label, prompt in [("zero-shot", zero_shot), ("few-shot", few_shot)]:
    r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0)
    print(f"{label}: {r.choices[0].message.content.strip()}")
```

Run this against a few more borderline alerts and see where zero-shot
and few-shot start to disagree — that gap is exactly where your team's
unwritten conventions live.

## Common Misconceptions

❌ Few-shot is strictly better than zero-shot.
(It's better for calibrating to a specific, non-obvious pattern. For
generic tasks it just adds token cost for no accuracy gain.)

❌ More examples always means more accuracy.
(Returns diminish fast after 3-5 good examples, and low-quality or
inconsistent examples actively hurt.)

✔ Few-shot examples teach *pattern*, not just topic — they're most
valuable exactly where your team's convention diverges from the
general-purpose default the model learned in training.

## Interview Questions

1.  What's the difference between zero-shot and one-shot prompting?
2.  Why does few-shot prompting help most with team-specific or
    non-obvious conventions specifically?
3.  What's the risk of including inconsistent examples in a few-shot
    prompt?
4.  Why isn't "more examples" a free win?

## Summary

Zero-shot relies on the model's general training; few-shot shows it a
handful of labeled examples to calibrate to a specific, often
team-internal pattern. A few good examples usually beat both zero
examples and a dozen — pick based on how standardized the task already
is, and watch the added token cost on every call.

## Next Chapter

➡️ `04-Chain-of-Thought.md`
