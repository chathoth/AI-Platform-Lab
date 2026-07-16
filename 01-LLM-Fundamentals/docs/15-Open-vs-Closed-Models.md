# 15 - Open vs Closed Models

## Introduction

Chapter 02 called 2023-2024 the "multi-vendor era" and compared it to
the multi-cloud moment. This chapter is where I actually make that
decision concrete: self-host an open-weight model, or call a closed
API. It's the same evaluation I'd run for build-vs-buy on any piece of
infrastructure — and the answer is genuinely "it depends," not a
default.

## Learning Objectives

After this chapter I should be able to:

-   Distinguish closed (API-only) models from open-weight models.
-   Compare them across cost, latency, data control, and ops burden.
-   Identify major players in each category as of today.
-   Make a build-vs-buy style recommendation for a given scenario.

------------------------------------------------------------------------

# Two Models of Access

  Closed (API-only)                    Open-weight
  ------------------------------------- --------------------------------------
  Claude, GPT-4/5, Gemini               Llama, Mistral/Mixtral, Qwen, DeepSeek
  You call an API, provider hosts it    You download weights, host it yourself
  Pay per token                         Pay for your own compute
  No access to the weights              Full access to the weights
  Provider controls updates/versions    You control versions and rollout

**Platform analogy:** this maps almost exactly onto **managed service
vs. self-hosted** — RDS vs. running your own Postgres, or a managed
Kafka vs. self-hosted Kafka. Same underlying trade-offs apply:

  Factor              Closed API (managed)               Open-weight (self-hosted)
  -------------------- ----------------------------------- ---------------------------------------
  Ops burden            None — provider handles scaling     You own capacity planning, scaling, patching
  Cost model             Pay-per-token, scales with usage    Fixed infra cost, better at high, steady volume
  Data control            Data leaves your network            Can run fully in your own VPC/on-prem
  Latency control          Provider's infra, provider's region Your infra, your region — you control it
  Model quality (frontier) Usually ahead at the top end         Closing the gap, strong at small/mid sizes
  Customization             Limited (prompting, some fine-tuning) Full — fine-tune, quantize, modify freely

## When I'd Reach for Each

**Closed API** — same logic as reaching for a managed database:

-   Getting something working fast, low initial ops investment.
-   Variable/spiky load where you don't want to own capacity planning.
-   Need the current frontier-level reasoning quality.
-   Data isn't sensitive enough to require staying in your own network.

**Open-weight, self-hosted** — same logic as running your own cluster:

-   Data residency/compliance requires it never leaving your network
    (healthcare, finance, government workloads).
-   High, steady request volume where the token-cost math clearly beats
    infra cost at scale.
-   Need to fine-tune deeply or run heavily customized inference logic.
-   Want zero dependency on a third party's uptime/rate limits/pricing
    changes.

## The Real Calculation: When Does Self-Hosting Pay Off?

``` text
Closed API cost  ≈  tokens_per_month × price_per_token
Self-hosted cost ≈  GPU_instance_cost_per_month (mostly fixed, regardless of usage)

Self-hosting wins when:
  tokens_per_month × price_per_token  >  GPU_instance_cost_per_month
```

This is exactly the reserved-instance-vs-on-demand calculation I already
run for regular cloud infra — low, spiky usage favors pay-per-use
(closed API); high, steady usage favors owning fixed capacity
(self-hosted open model). The crossover point depends entirely on your
actual traffic pattern, not on which option is "better" in the
abstract.

## Hands-on: Price Out Both Options for a Real Workload

``` python
# rough monthly cost comparison for a hypothetical workload
tokens_per_day = 2_000_000          # 2M tokens/day
days = 30

# closed API (example pricing, check current rates)
price_per_million_tokens = 3.00     # USD, blended input/output estimate
api_cost = (tokens_per_day * days / 1_000_000) * price_per_million_tokens

# self-hosted (example: single A100 GPU instance, cloud rental)
gpu_hourly_cost = 2.50              # USD/hour, example cloud GPU price
self_hosted_cost = gpu_hourly_cost * 24 * days

print(f"Closed API cost:  ${api_cost:,.2f}/month")
print(f"Self-hosted cost: ${self_hosted_cost:,.2f}/month")
```

Run this with your own real (or estimated) token volume — the crossover
point is usually clearer than expected once actual numbers go in. Then
sanity-check the *engineering time* to actually stand up and maintain a
self-hosted deployment — that's the operational cost the raw dollar
comparison always leaves out.

## Common Misconceptions

❌ Open-weight models are always worse than closed ones.
(At small-to-mid scale, top open models are now competitive with closed
models a generation behind them — the gap narrows every few months, and
for many non-frontier tasks it's already closed.)

❌ Self-hosting is always cheaper because "you own the hardware."
(Only true at sufficient, steady volume — at low/spiky usage, a managed
API is almost always cheaper once you account for idle GPU time and the
engineering effort to operate it.)

✔ This decision should be revisited periodically, not made once and
forgotten — pricing, model quality, and your own traffic volume all
shift over time, same as any build-vs-buy infra decision.

## Interview Questions

1.  What's the core difference between a closed and an open-weight
    model, from a deployment perspective?
2.  Name three factors, beyond raw model quality, that should drive a
    closed-vs-self-hosted decision.
3.  At what usage pattern does self-hosting typically start to make
    financial sense?
4.  Why might a company choose a slightly weaker open-weight model over
    a stronger closed API, despite the quality gap?

## Summary

Closed vs. open-weight models is the LLM-era version of managed vs.
self-hosted infrastructure — same trade-offs around ops burden, cost
model, data control, and customization. The right choice depends on
traffic volume, data sensitivity, and how much control/customization you
actually need, not on which option is universally "better."

## Next Chapter

➡️ `16-Prompt-Lifecycle.md`
