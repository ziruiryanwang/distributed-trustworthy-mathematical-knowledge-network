# Finite managed operator

`client/managed_owner.py` is an ordinary installed public `run` owner. It connects
the existing two-generation manager, surviving-supervisor session and actual
placement service; it is not another launcher, daemon, checker or trust domain.
This source candidate requires a separately reviewed 126-source installation
and public integration check. The existing consolidated 121-source installation
does not contain it. Source review is not an executed release qualification.

## What it does

A service request authenticates the explicitly adopted release and its exact
selected source map. It opens the private manager and reserves one prospective
session. The unchanged supervisor binds the real suspended worker before resume;
the unchanged boot loads that worker's pinned source snapshot. The worker joins
its exact session before allocating a generation or reserving a service run.
It serves for a finite interval, optionally seals, and closes actual roles.

The surviving supervisor observes the direct process handle and current Job
before recording quiescence. Orderly `CLOSED` stays `CLOSED`. A failed worker
remains a failed operation even if that supervisor establishes
`QUIESCED_UNCLEAN`. This owner cannot restart an unclean generation or repair
`UNKNOWN` after total supervisor loss. It never adopts a supplied closure JSON
or substitutes process IDs for still-owned handles.

Separate public requests can reopen status, adopt a fresh clock and retire,
then authorize one bounded reclamation step. No operation implicitly migrates
an old schema, creates on open failure, retries a session, or renews cleanup
allowances. This administrative machinery does not make any mathematical claim.

## Ordinary installed invocation

Use the exact new release's ordinary request schema:

```text
<release>/base/receiver/runtime/python/python.exe -I -S -B \
  <release>/distribution.py launch RELEASE_SHA run REQUEST_PATH REQUEST_SHA
```

This is a schematic command; quote full paths appropriately for the shell.
`RELEASE_SHA` is the SHA-256 of that adopted `V5-RELEASE.json`; `REQUEST_SHA`
authenticates the exact UTF-8 request bytes. No request hash is a safety proof:
the local operator must adopt the trusted code and private-root premise.

The outer `DMKN_V5_INSTALLED_REQUEST_V1` fields are unchanged:

| Field | Selection |
|---|---|
| `name` | Fresh lower-case operation name; never reuse its output directory |
| `workspace_root` | Existing ordinary absolute directory for operation output |
| `parameters` | Managed request described below |
| `limits` | All six ordinary Job limits, including parent and nested work |
| `output_limits` | Existing `{bytes, entries}` final-census limits |
| `owner.root` | `<release>/sdk/v5/client` |
| `owner.entry` | `managed_owner.py` |
| `owner.sources` | Exactly `{"managed_owner.py": <release file bytes/SHA row>}` |
| `runtime_mode` | `atomic`, the unchanged public dispatcher compatibility value |

The request also contains its `schema`. Do not use runtime placeholders or
construct a mathematical RuntimeProfile for this administrative owner. The
dispatcher prepares ordinary metadata, not mathematical trust.

## Managed request schema

Every request has exactly these common fields plus its operation's fields:

```json
{
  "schema": "DMKN_V5_MANAGED_OWNER_V1",
  "operation": "status",
  "release_sha256": "<adopted release SHA-256>",
  "manager_root": "<absolute private persistent manager path>",
  "manager_config": "<the complete supervised manager configuration object>",
  "owner_limits": {"calls": 128, "cpu_seconds": 30}
}
```

Angle-bracket values are explanatory placeholders, not accepted literal input.
The complete `manager_config` is the existing
`DMKN_V5_TWO_GENERATION_MANAGER_SUPERVISED_V1` object: epoch, clock-model identity,
registry and allocation bounds, protected roots, exactly two slot specifications
and `max_sessions`. Reopen it with identical configuration bytes. Do not add each
new request directory to that persistent configuration: dynamic disjointness
from this operation, sources and installation is checked separately every time.

`owner_limits.calls` is 1–8192 and `cpu_seconds` is 1–3600. These are sampled
manager-operation guards inside the unchanged encompassing Job, not independent
CPU allowance beyond that Job. Serving needs at least 11 owner CPU seconds so
the session's fixed binding/recovery actions can be prepaid.

### Initialize and status

`initialize` has no extra fields and explicitly creates a fresh root.
`status` has no extra fields and requires an existing manager.

Status is a locked normal reopen, not concurrent read-only inspection. The
manager conservatively converts saved `RESERVED`, `LIVE` or `CLOSING` to
`UNKNOWN` when no current exact launch owns the reopen. It never converts these
records to `CLOSED`. Do not poll status by opening a second owner during service.

### Serve and seal

Both operations add exactly:

```json
{
  "create_manager": false,
  "selection": {"generation": "<generation SHA-256 identity>"},
  "inner_limits": {
    "cpu_seconds": 30, "memory_mib": 256, "active_processes": 8,
    "wall_seconds": 60, "stdout_bytes": 1048576, "stderr_bytes": 1048576
  },
  "worker_owner_limits": {"calls": 128, "cpu_seconds": 20},
  "startup_seconds": 7,
  "service_seconds": 3,
  "close_seconds": 25,
  "boot_tail_seconds": 7,
  "parent_tail_seconds": 5,
  "supervisor_cleanup_seconds": 25,
  "seal_before_close": false,
  "restore_requests": [],
  "tls": {"read": null, "intake": null}
}
```

Alternatively, `selection` is exactly
`{"slot": 0, "generation_config": <existing generation configuration>}`.
That explicitly allocates an unoccupied slot after the worker joins its session.
The generation ID is derived, never caller-selected. `create_manager: true`
only permits a fresh manager with this allocation form; it is never a fallback.
`generation_config` has the existing workspace, placement, service-limits,
egress and location configuration, with no caller-specified placement generation.

`seal` requires `seal_before_close: true`. It starts/resumes an eligible service,
performs the finite interval, calls the actual manager seal operation, and closes.
It does not silently mutate a live service owned by another process. `serve`
can independently request the same seal-before-close behavior.

The numbers above illustrate schema, not a universally sufficient service
profile. The selected service's existing startup/HTTP drain/locator cleanup
reservations must fit too. All interval fields are positive integer seconds;
supervisor cleanup is 25–60 seconds. Startup, service, close and boot tail must
fit the inner wall allowance. Inner wall plus supervisor cleanup and parent tail
must fit the original remaining parent clock. Boot and source verification spend
that same clock. Child limits never raise the parent CPU/memory/process limits.
The requested service interval must fit the actual service's earlier deadline.
Close is bounded by both `close_seconds` and the original worker cutoff.

`restore_requests` is an explicit, unique list of at most 256 retained request
identities. Existing `advertise_retained` is called serially within the service
interval; it does not grant new custody or make unfunded repair promises.

Each non-null TLS role is
`{"certificate": {"path": ..., "bytes": ..., "sha256": ...}, "private_key": {...}}`.
The existing TLS helper validates exact files (at most 1 MiB each), creates a
server context with at least TLS 1.2, and the actual service checks endpoint
compatibility. Keep those files outside the install, source snapshots, operation
outputs and manager state. No certificate/key bytes are copied to reports.

This fixed owner does not issue or serialize intake bearer tokens. The existing
in-process API returns them only to a trusted caller; a new token handoff channel
is not silently added by this wrapper. Empty first serve and retained read/route
restoration are supported; general contribution automation is a separate seam.
An external reader uses the existing read endpoint and its own adopted contact,
egress/TLS policy and finite acquisition budget; these read routes do not require
an intake token. An external contributor needs the existing token-bearing intake
client, but this fixed owner has no way to deliver that token to it. Secure local
token handoff is explicitly an unimplemented composition seam, not something
proved by empty-service lifecycle success.

### Retire

Add `generation` and `clock`, where `clock` has exactly `lower_utc_ms`,
`valid_for_ms`, `rate_error_ppm`, and `model_id`. This is a fresh operator
assertion that the UTC lower bound and monotonic rate-error model hold at this
call. It is not a stored configuration timestamp or a network time oracle.
Retirement requires that lower bound to pass the original retention horizon and
the actual run state to be `NONE`, `CLOSED`, or supported `QUIESCED_UNCLEAN`.
It does not restore or refund the charged session, sequence or run.

### Reclaim

Add `generation`, `reclamation_profile`, `max_entries`, and `action_seconds`.
For a `RETIRED` generation, supply the exact existing profile fields:

```json
{
  "layout": "DMKN_V5_CLOSED_GENERATION_LAYOUT_V1",
  "ownership": "PRIVATE_ENROLLED_NO_OTHER_WRITERS_OR_RESTORES_V1",
  "max_calls": 1,
  "max_entries_per_call": 64,
  "max_apparent_bytes": "<integer no greater than the slot reservation>"
}
```

For an already `RECLAIMING` generation, `reclamation_profile` must be `null`:
reuse its original caps, never replace them. One request performs at most one
precharged fixed-layout window; it may report `RECLAIMING` rather than `FREE`.
This explicitly authorizes deletion within that exact retired generation. It is
not recursive deletion, a payload sweep, or deletion of request evidence. All
other writers/restores must remain excluded. Unknown layout, changed identities,
uncertain closure or spent caps refuse rather than trigger repair or cleanup.
The fixed reclaimer permits the `workspace/operations` directory only when empty;
operation artifacts below it are unknown layout and prevent deletion. Populated
reciprocal workloads are therefore not automatically covered by this reclamation
path. Nothing here selects a broader artifact deletion policy.

## Results and evidence

Every entered owner writes `<operation-run>/work/managed-result.json`, schema
`DMKN_V5_MANAGED_OWNER_RESULT_V1`, with `COMPLETE` or `FAILED` and a typed error.
Ordinary boot/public facade failures before owner entry retain their own reports.
The unchanged public command must also succeed; an owner report alone is not a
complete launch result. A write/census/boot failure can prevent a final report.

Service evidence under that work directory is:

```text
managed-result.json
managed-supervisor/                 exact nested command, stdout and stderr
managed-worker/
  plan.json                        original child plan and bounded clock
  BOOT-RESULT.json or BOOT-FAILED.json
  sources/                         unchanged boot's pinned worker snapshot
  work/managed-ready.json           endpoints only, no bearer secrets
  work/managed-result.json          join, allocation, service, close and status
```

The parent result includes the full actual `supervision`, worker report and
available boot result. The worker's manager status is captured before its exit,
so its session can still say `BOUND`; the surviving parent then records
`QUIESCED`, observable in a separate ordinary status request. `generation` is
present after a successful service. Administrative results contain `manager`;
retirement also contains `retired`, reclamation contains `reclamation`.

These are operational observations, never imported mathematical certificates
or closure authority. No claim follows about independent hosts, hostile-source
sandboxing, global completeness, guaranteed useful growth or full v5 release.
