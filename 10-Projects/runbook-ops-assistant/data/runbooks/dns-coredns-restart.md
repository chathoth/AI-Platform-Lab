# Runbook: Internal DNS Resolution Failures (CoreDNS)

## When to use this

Services intermittently fail to resolve internal service DNS names,
especially shortly after a node pool change or cluster upgrade.

## Steps

1. Confirm the failure is DNS-specific, not a general network issue -
   check whether the same host is reachable by IP but not by name.
2. Check whether the failures correlate with a recent node pool
   upgrade or CoreDNS configuration change.
3. If CoreDNS configuration is suspected to be stale, call
   `restart_coredns()` to force a config refresh.
4. Confirm DNS resolution has recovered before closing out the
   incident.

## Safety notes

- `restart_coredns()` is destructive (it briefly disrupts cluster-wide
  DNS while pods restart) and requires operator role approval before
  execution.
- Do not restart CoreDNS reflexively for every DNS-flavored symptom -
  confirm it's actually a resolution failure first, since a
  cluster-wide DNS restart affects every service, not just the one
  reporting the issue.

## Related incidents

INC-1004 (auth-service DNS failures after a node pool upgrade) was
resolved this way, caused by a CoreDNS config that hadn't propagated
to the new node pool.
