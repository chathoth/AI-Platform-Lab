# Runbook: Disk Cleanup on a High-Disk-Usage Host

## When to use this

Disk usage alert fired for a host (warning at 80%, critical at 90%).
Applies to app nodes and database nodes alike.

## Steps

1. Confirm current disk usage with `get_disk_usage(hostname)`. Do not
   proceed on assumption alone - the alert may be stale.
2. If usage is below 85%, this is not yet actionable. Monitor only.
3. If usage is at or above 85%, run `list_large_files(hostname)` to
   see what's actually consuming space before removing anything.
4. If the large files are old, rotated log files (not active
   database data), run `cleanup_old_logs(hostname)` to remove them.
5. Re-check disk usage after cleanup to confirm it actually helped.

## Safety notes

- `cleanup_old_logs` is destructive (deletes files) and must only be
  called after disk usage has been confirmed at or above 85% by an
  actual `get_disk_usage` call in this session - not from memory of a
  past incident, and not from the alert text alone.
- Never call `cleanup_old_logs` on a database's active WAL or data
  directory. This runbook is for old, rotated log files only.
- Requires operator role approval before execution, even if the
  condition is met.

## Related incidents

INC-1002 (db-primary-02 disk critical, WAL segments) and INC-1008
(db-replica-01 disk trending up) both followed this pattern.
