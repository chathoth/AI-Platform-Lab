# Runbook: Rolling Back a Bad Deployment

## When to use this

A service starts failing (CrashLoopBackOff, elevated error rate, OOM
kills) shortly after a deploy. Timing correlation with the deploy is
the key signal - if there was no recent deploy, this is the wrong
runbook (see `service-restart.md` instead).

## Steps

1. Confirm the failure started shortly after a deploy, not before it.
2. Confirm current resource usage with `get_disk_usage` if the
   symptom involves memory or disk, to rule out an unrelated cause.
3. Call `rollback_deployment(service_name)` to revert to the last
   known-good revision.
4. Confirm the service is healthy on the rolled-back revision before
   closing out the incident.
5. File a follow-up to fix the underlying change before re-deploying.

## Safety notes

- `rollback_deployment` is destructive (it changes what code is
  running in production) and requires operator role approval before
  execution.
- Rolling back does not fix the underlying bug in the new revision -
  it only removes it from production. The follow-up fix still needs
  to happen separately.

## Related incidents

INC-1001 (checkout-service CrashLoopBackOff after a batch-size change
increased memory usage past the pod limit) was resolved by rollback,
not by a plain restart.
