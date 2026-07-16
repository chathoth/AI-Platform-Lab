# Runbook: Restarting a Crash-Looping Service

## When to use this

A service is in CrashLoopBackOff, or is reported as unresponsive, and
a restart is being considered as a mitigation.

## Steps

1. Check whether the crash correlates with memory pressure using
   `get_disk_usage` and `list_large_files` where relevant, and check
   recent deploys first - a restart does not fix a bad deploy, a
   rollback does (see `deployment-rollback.md`).
2. Only if the crash is NOT caused by a bad recent deploy, and the
   service is confirmed unresponsive right now, call
   `restart_service(service_name)`.
3. After restarting, confirm the service is healthy again before
   closing out the incident.

## Safety notes

- `restart_service` is destructive (it interrupts in-flight requests)
  and requires operator role approval before execution.
- Do not restart a service as a first response to every alert - check
  the actual cause first. Module 07's verified finding: an agent that
  calls a check and a restart in the same turn can restart something
  that was never actually broken, because it never waited to observe
  the check's result.
- If the root cause is a bad deploy, use the rollback runbook instead
  of restarting - a restart of a bad deploy just crashes again.

## Related incidents

INC-1001 (checkout-service CrashLoopBackOff) was a bad deploy and was
fixed with a rollback, not a restart - restarting alone would not
have helped since the new pods would hit the same memory limit again.
