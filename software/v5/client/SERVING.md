# Serve an existing v5 workspace

`serve_workspace.py` is an ordinary trusted-owner entry for the existing
`client.launch` / `client.boot` launcher. It makes a persistent workspace's
formal index, semantic groups/bodies and typed packets available over the
existing read-only HTTP protocol. It creates no mathematical owner, proof,
admission warrant, new workspace, remote-write endpoint or location service.

Use its `main(context)` as the selected owner entry, with its exact import
closure selected by the normal launcher source map. The launcher, not this
entry, supplies the hard CPU/memory/process/wall limits. Direct callers may
await `serve(context)` only inside equivalent trusted-owner containment.
This is not an untrusted-source sandbox.

## Parameters

The launcher plan's `parameters` must contain exactly these fields:

```json
{
  "schema": "DMKN_V5_WORKSPACE_SERVICE_V1",
  "mode": "atomic",
  "workspace_path": "E:\\absolute\\existing-workspace",
  "workspace_config": {"...": "the exact configuration used to create this workspace"},
  "bind": {"host": "127.0.0.1", "port": 0},
  "tls": null,
  "service_limits": {
    "max_connections": 2,
    "max_requests": 1024,
    "max_reply_bytes": 33554432,
    "operation_ms": 1000,
    "lifetime_seconds": 60
  }
}
```

`workspace_config` above is a placeholder: supply the complete existing
workspace configuration, without changing its stored profile or limits.
An absent/mismatched workspace is refused; it is never silently initialized.

| Mode | Workspace | Existing packet/provider profile |
|---|---|---|
| `atomic` | `workspace_atomic.Workspace` | I-frontier |
| `mixed` | `workspace_mixed.Workspace` | Mixed |
| `evidence` | `workspace_evidence.Workspace` | Evidence |
| `staged` | `workspace_staged.Workspace` | Evidence |
| `validated` | `workspace_validated.Workspace` | Evidence |

All selection is explicit; there is no migration or fallback. Data paths must
be absolute, canonical, existing ordinary directories with no symlink/junction
ancestor, disjoint from the installation, current run/output and selected
source snapshots in both directions. Keep retained frozen evidence separate:
the service owns a mutable working copy or independently imported workspace.

Binding uses an explicit nonmulticast/nonunspecified IP address. Port zero
asks the operating system for a free port. Nonloopback binding requires TLS:
replace `null` with `{"certificate": PIN, "private_key": PIN}`, where each
`PIN` has exactly `path`, `bytes`, `sha256`. Paths must be canonical ordinary
files; contents are bounded to 1 MiB and checked before constructing the
existing TLS context. The local operator must prevent concurrent replacement
of these files. Private-key contents are never written to the result.
Clients still select their own verified CA and expected server identity.

Provider limits retain their existing meaning. In particular, reply allowance
reserves the route's maximum response before dispatch, not just the eventual
response length. The group/body route requires a 16 MiB available reservation
even for a small object. A 32 MiB aggregate allowance is a small usable example,
not a claim that all workloads fit it.

## Lifetime, outputs and ownership

The service stops at the earlier of its requested lifetime and the original
outer deadline minus `operation_ms / 1000 + 5` seconds. This leaves a nominal
in-flight dispatch and cleanup margin; it never extends the launcher deadline.
Insufficient remaining time is refused. Hard containment remains necessary
because synchronous code and OS cleanup cannot be guaranteed to finish merely
by an asynchronous timer.

Once listening, the service writes `context.location_workspace/service-ready.json`.
It contains endpoint `{host,port,tls,server_name}`, formal namespace, wire-profile
identity and monotonic deadline. The endpoint can be used while the service is
live. The file remains historical after shutdown: reading it does not establish
current reachability. Both output filenames must be fresh for each invocation.

On termination, `service-result.json` contains status, original and effective
deadlines, selected service limits, counters, primary error and cleanup errors.
`serve` returns that report; `main` returns zero only for `PASS`. Parameter
prevalidation errors occur before opening and may raise without a result.
Runtime failures yield `FAILED`; cancellation attempts cleanup then propagates.
Failed output writes raise and must be reported by the enclosing launcher.
No endpoint, counter or successful result is mathematical authority.

The service stops/drains HTTP before closing the workspace. It attempts
remaining resource closes after a cleanup exception and does not label
uncertain cleanup as success. If `Workspace.open` raises before returning an
object, its existing constructor cleanup and the enclosing process boundary
are responsible for inaccessible partial state; the service cannot certify
that state closed. Do not use a failed service as authority for automatic retry.

**Remote read-only is not filesystem immutability.** Workspace opening holds its
exclusive owner lock, applies SQLite settings and can mark interrupted operation
records; index queries can retain snapshots. A separate publishing process
cannot concurrently own this workspace. Stop and close, then reopen under a
fresh explicit allocation. The entry does not remove locks to allow writers.

Location advertisements, automatic replication, indefinite daemon supervision,
public deployment and mathematical acceptance are not added here. Existing
bounded location composition remains available separately; consumers verify
retrieved mathematics through the unchanged admission APIs.
