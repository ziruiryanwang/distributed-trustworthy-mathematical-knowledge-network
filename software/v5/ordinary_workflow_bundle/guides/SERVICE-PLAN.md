# Authorize a finite period of unattended serving

This separate Windows companion repeats **only** the current package's public
`peer serve` operation. An operator approves one exact configuration, a lease
count, a total horizon and aggregate resource allowances. The runner uses fresh
outputs and stops after the prepaid leases or any unsuccessful/uncertain service
operation. No perpetual background service or scheduled task is installed.

Status: independently reviewed and adopted finite controls, including two idle
loopback leases. This does not establish loaded-service performance or continuous
availability. See the [workflow guide](../../../START-HERE.md) for evidence scope.
This does not change the default package, its archive, mathematical checking or
owner lock. It is not a complete v5 release or an availability guarantee.

## Appropriate use

Use an existing, disclosure-approved owner/custody/index. Serving exposes the
whole addressable custody, including dependency/sibling declarations and retained
but unaccepted data; selecting an index entry does not create an access-control
boundary. Approve the entire store before selecting this plan. Keep private
investigation state separate. Other agents may investigate ordinary Lean projects
or perform state-free discovery while this owner serves.

The runner never publishes or admits mathematics. Do those operations explicitly
between plans. Supported commands selecting this same owner refuse while its
lease is active. The gaps between leases are not publication windows or fair
turns for competing writers. Do not share custody/index directories across other
catalogs or bypass their serialization. Keep all writers excluded for the entire
plan, including gaps: this companion does not hold a catalog lock between child
leases or snapshot database content. Immutable disclosure-approved store contents
are an operator premise, not a new cross-epoch lock guarantee.

## Inputs

Use independently approved Windows x86-64 Python 3.14.6, Lean 4.34.0 and the
current supported transport-release package. The companion recognizes the
unchanged contact launcher and selected peer/provider sources. Fresh builds may
have a different approved PROFILE hash; read that hash from the actual selected
build. Hash agreement selects bytes, not trustworthy software or mathematical
truth. Existing package/runtime/OS integrity and stable owner-controlled paths
remain assumptions.

Create one strict UTF-8 JSON plan. Unknown/duplicate fields, floating-point plan
numbers, booleans used as counts and redirected/noncanonical paths are refused.
All paths must be absolute local-drive paths. `config` and `custody_limits`
select existing exact files by SHA-256. The normal serve configuration must use
an existing index, a fixed nonzero port, `exclusive: true`,
`share_all_custody: true`, and explicit provider limits. Nonloopback serving
requires the existing pinned TLS configuration. Optional authoring-offer maps
and pair-index settings remain supported; nested input paths are validated.
Omit `authoring_offers` and `index.access_pairs` when unused; this companion
refuses explicit null for those two optional settings. `tls: null` is supported
for loopback service only.

Example shape (replace every path/hash with your approved selection):

```json
{
  "schema": "DMKN_ORDINARY_SERVICE_PLAN_V1",
  "package": "C:\\commons\\package",
  "profile_sha256": "APPROVED_PROFILE_SHA256",
  "python_runtime": "C:\\commons-runtime\\python",
  "lean_runtime": "C:\\commons-runtime\\lean",
  "catalog": "C:\\commons-public\\catalog",
  "custody": "C:\\commons-public\\custody",
  "store_id": "APPROVED_STORE_ID",
  "custody_limits": {"path": "C:\\commons-inputs\\custody-limits.json", "sha256": "APPROVED_LIMITS_SHA256"},
  "config": {"path": "C:\\commons-inputs\\serve.json", "sha256": "APPROVED_CONFIG_SHA256"},
  "leases": 12,
  "horizon_seconds": 22000,
  "runner_cpu_seconds": 600,
  "operation_limits": {"wall_seconds": 1800, "cpu_seconds": 20, "memory_mib": 512, "active_processes": 2, "stdout_bytes": 1048576, "stderr_bytes": 1048576},
  "epoch_limits": {"wall_seconds": 1815, "cpu_seconds": 80, "memory_mib": 640, "active_processes": 3, "stdout_bytes": 1048576, "stderr_bytes": 1048576},
  "aggregate": {"cpu_seconds": 1560, "accepted_attempts": 12288, "reply_bytes": 805306368, "log_bytes": 255852544}
}
```

Those example aggregate attempt/payload allowances assume each service config
permits 1024 accepted attempts and 67,108,864 response-payload bytes. Its lease
could be 1700 seconds with 10 seconds cleanup. These numbers demonstrate valid
reservations, not recommended production capacity or evidence that your load
will fit. No provider configuration is inferred or written by this runner.

Limits are reserved upfront, even when a lease uses less:

- `leases`: 1..96; original horizon: at most seven days.
- `operation_limits`: existing launcher ceilings, at least two process slots.
- `epoch_limits`: supervision around `run.py` and its entire descendant tree.
  Relative to operation limits, reserve at least 15 extra wall seconds, 60 CPU
  seconds, 128 MiB and one process slot. Outer ceilings remain 8192 MiB/eight
  processes; outer wall is at most 3660 seconds. These extra allowances cover
  the nested launcher, not a second mathematical operation.
- Service lease + cleanup + 15 seconds must be strictly below operation wall.
  Original horizon must be at least `leases * epoch_wall + 60`. Before each
  launch, at least its full epoch wall plus 25 seconds must remain for the
  existing supervisor's possible 10+10-second failure cleanup and reporting.
- Aggregate CPU reserves `leases * epoch_CPU + runner_CPU`. Accepted attempts
  and payload reserve `leases` times the respective provider cap. Log allowance
  reserves both nested stream caps plus 16 MiB metadata per epoch and 4 MiB for
  plan-level records. Runner CPU is explicitly selected between 60 and 6000
  seconds. Memory/process limits are simultaneous, not summed across epochs.

The output root must be absent, with an existing parent, disjoint from package,
runtimes, companion, all three state directories and selected inputs. The
atomic directory creation claims this output: two invocations cannot reuse it.
Different plans selecting the same owner still rely on the existing owner lock.

## Run once

After review/adoption, calculate the exact plan SHA-256 and invoke:

```powershell
& 'C:\commons-runtime\python\python.exe' -I -S -B `
  'C:\commons-tools\service_plan.py' `
  --plan 'C:\commons-inputs\evening-plan.json' `
  --plan-sha256 APPROVED_PLAN_SHA256 `
  --output 'C:\commons-runs\evening-01'
```

No hooks, arbitrary executable, shell or retry option exists. A normal OS
scheduler may launch this exact invocation if the operator separately configures
it; the companion does not install or change scheduled tasks. No manual approval
is needed for each already prepaid lease. Canceling preserves evidence and stops
continuation; never treat cancellation as rollback or automatically restart it.

## What the result means

`PLAN.json` records the exact plan, identities and reservations. Each
`epoch-NNNN` records `INTENT.json`, the outer `OUTER.json`, unchanged nested
launcher diagnostics under `inner/`, actual peer files under `service/`, and
`COMPLETE.json` only after validation. Final `RESULT.json` and stdout report the
finished count, attempted epochs, known CPU, counters, terminal reason and scope.

Continuation requires both Job reports clean, no termination request or active/
terminated descendants, matching RUN and peer stdout/files, exact selected
state/config/semantic/implementation identities, `LEASE_FINISHED`,
`quiescent: true`, and consistent provider counters. Readiness or exit zero alone
does not authorize another lease. Accept-loop or cleanup failures stop the plan.
Ordinary failed/malformed requests do not alone stop a cleanly completed epoch.
An exhausted lease may be followed by its **already prepaid** next epoch: it
never increases lease count, horizon or aggregate allowances. Byte-quota refusal
is not separately classified by the current provider; the companion does not
invent that diagnosis. Quota exhaustion can leave unavailable intervals.

No resume, output overwrite or automatic retry exists. Failed/missing reports,
changed inputs, unknown cleanup and exhausted original budgets stop. Keep all
partial state and diagnostics. The last attempt can cost resources even when
no epoch completes: `attempts` and `known_attempt_job_cpu_seconds` include known
failed-attempt Job CPU; unknown CPU is marked incomplete, not treated as zero.
Add `runner_cpu_seconds_before_final_report` once; this measurement excludes
the final result-file write and stdout printing. The corresponding wall field
also ends before final reporting. Do not add inner Job CPU or nested launcher CPU again;
they are already included in the outer Job.

Bounds retain the existing supervisor's sampling/cleanup overshoot limitations.
The runner itself uses cooperative CPU/wall checks, not a privilege sandbox.
Logs have conservative reservations, not a hard filesystem quota. Payload caps
exclude TLS/wire/request/header costs. Provider counters describe protocol work,
not useful mathematics. A finished plan does not establish continuous service,
per-user fairness, denial-of-service resilience, eventual publication, semantic
search completeness, perpetual custody, or operation on another host.
