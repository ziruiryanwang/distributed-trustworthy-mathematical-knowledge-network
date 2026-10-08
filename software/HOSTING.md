# Finite continued loopback hosting

`manage host` repeats the existing read-only service of **one committed immutable
view**, within a single explicit finite owner grant. It does not publish, admit,
check mathematics, alter accepted state, discover peers, run SSH, or provide a
permanent daemon. The mutable development implementation requires its own
qualification; synthetic contract tests are not real availability evidence.

Create a UTF-8 JSON grant outside the installation. Use the configuration file's
SHA-256 for `config`, and the view handle and catalog digest returned by a prior
successful `expose` or `replica_expose` operation:

```json
{
  "schema": 1,
  "profile": "finite-loopback-host-v1",
  "id": "my-first-host-grant",
  "config": "<64 lowercase hex characters>",
  "client": "local",
  "view": "view:<committed handle>",
  "catalog_sha256": "<64 lowercase hex characters>",
  "port": 48191,
  "max_sessions": 12,
  "seconds": 300,
  "max_requests": 128,
  "max_bytes": 268435456
}
```

From PowerShell, with absolute selected paths:

```powershell
& $Python -B -E -s -S "$Install\manage.py" host --config "$State\config.json" --grant "$OwnerWork\host-grant.json"
```

Use the identical command to resume after a controller restart. Grant values,
configuration and all selected source/runtime pins must remain identical;
whitespace-only edits to the external grant do not change its parsed values.
The immutable grant id is lowercase letters/digits/underscore/hyphen, 1–32
characters, excluding Windows reserved names. Each grant permits 1–128 sessions;
each session allows 1–360 seconds, 1–128 connections and 1–256 MiB charged sends.
An exhausted grant does nothing when invoked again. A separately authored new
id is an explicit new grant, not a reset or automatic renewal.

## Reservation and restart contract

The controller holds the existing nonblocking OS owner lock in
`scratch/hosting`, separate from the service worker's `scratch/services` lock.
Every slot is a new fsynced, immutable journal record **before** worker launch.
It reserves one full session, selected service seconds, `seconds + 30` supervised
wall seconds, 120 Job CPU seconds, all selected connections/send bytes and 1 MiB
retained-evidence allowance. Grant totals multiply these maxima by
`max_sessions`. Short sessions, refusals, failed launches and interrupted writes
never refund a slot. Concurrent controllers refuse `BUSY`.

The existing worker retains its 256 MiB private-commit and eight-process Job
profile; it normally starts one inert worker and no native checker. Runtime
limits are supervised per session, not by a new hard aggregate Job. Polling can
overshoot; controller CPU, final receipt writes and operator SSH are outside
those measurements. The evidence allowance is conservative accounting, not an
OS disk reservation or a transient filesystem quota. Keep the immutable view
and adequate free space available. There are at most 128 retained grants and
4,096 cumulative slots in one hosting journal; no automatic pruning exists.

Every unfinished reservation must have matching supervisor/request evidence,
positive child-reaped and Job-empty/closed evidence, and no cleanup uncertainty
before any later slot or new grant is permitted. The OS lock's disappearance is
not quiescence. Completed markers also require their retained supervisor receipt
to remain byte-identical. A missing, partial or inconsistent receipt blocks hosting;
there is no “assume stopped,” force, deletion or counter-reset option. Preserve
the evidence for operator investigation. A completed failure halts that grant
permanently. A normal completed session advances; a controller crash after its
receipt but before its terminal marker reconciles that slot without repeating it.

Only normal `SERVICE_STOPPED`/`SESSION_LIMIT` with matching catalog, nonacceptance
flags and no recorded transfer error advances automatically. `SESSION_LIMIT`
also covers CPU, connection and byte exhaustion; it is not proof of the promised
duration. Readiness follows view loading, which consumes the service window.

Session evidence and readiness are retained under
`scratch/services/host-<grant-id>-0001/` (then `0002`, etc.). The worker writes
`ready.json`; the supervisor writes `cases/serve/supervisor.json`. Readiness is
historical, not a current-liveness guarantee. Expect brief listener gaps while
one session closes and the next starts. There is no retry of interrupted client
transfers, backoff, expiry-date guarantee, service installation or boot autostart.

This remains trusted-owner local NTFS/Windows operation, not hostile-filesystem
or multi-user isolation. Plain HTTP binds only `127.0.0.1`. Independent-host
routes may use manually managed, independently authenticated SSH forwarding;
the local and remote application ports must match. SSH authorization never
transfers mathematical acceptance. No independent-host deployment is claimed.
