# Bounded intake progress diagnostics

This is one source-only auxiliary successor of
`software/v5/ordinary_parse_reuse/baseline_intake.py`, whose SHA-256 is
`9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142`.
It makes an interrupted invocation's last recorded phase and partial costs
inspectable. It does not establish why the prior intake disappeared, improve
its performance, change mathematical acceptance, or authorize another intake.
No product import, native operation or test execution was performed by the author.

## What is recorded

Inside the already locked owner directory, `_Progress` creates a fresh ordinary
directory at `intake-diagnostics/<32-hex-random-token>`. The parent, invocation
directory and every record use the existing ordinary-path validation. Each
record is written using the existing `PortableCatalog._write_fresh`: exclusive
creation, flush and file fsync. An existing invocation or record is never
overwritten. This provides the existing file-writer's durability semantics; it
does not add a power-loss-proof directory transaction or a global retention policy.

Records are canonical JSON, named `<four-digit-sequence>-<event>.json`. The schema
is `DMKN_BASELINE_INTAKE_PROGRESS_V1`. Allowed events are:

- `ENTRY`, before manifest reading or selected-context validation.
- `METADATA_BATCH_BEGIN` / `METADATA_BATCH_END`, around each planning batch.
- `METADATA_COMPLETE`, after all planning and capacity checks.
- `BATCH_READ_BEGIN` / `BATCH_READ_END`, around each actual batch reread.
- `BATCH_PREFLIGHT_BEGIN` / `BATCH_PREFLIGHT_END`, around actual preflight.
- `ADMIT_INTENT`, written before entering `owner.admit`.
- `BATCH_CONFIRMED`, after a genuine valid returned result.
- `COMPLETE`, before the existing success response.
- `FAILED`, best-effort inside the existing ordinary-exception handler.

The fixed scalar fields are `schema`, `authority`, `sequence`, `event`, `batch`,
`selected_root`, `manifest_sha256`, `selected_root_validated`,
`last_confirmed_root`, `confirmed_batches`, `possible_unreported_commit`,
`wall_seconds`, `controller_cpu_seconds`, `native_cpu_reservation_seconds`,
`observed_worker_cpu_seconds`, and `worker_cpu_accounting`. Unknown values are
null. The manifest hash is absent until parsing succeeds; the selected root is
marked validated only after the existing protected-context validator returns.
No proof bytes, proof trees, arbitrary text, per-theorem events or native logs
are placed in a record. The metadata callback receives only an event and batch
index; the existing batch proof-tree aliases are discarded before its end event.

Every record states
`DIAGNOSTIC_OBSERVATION_NOT_WARRANT_OR_RESUME_CURSOR`. No acceptance, planning,
context selection or recovery code reads these records back. A selected root
spelling is not evidence that the root is valid. A recorded confirmed prefix is
an observation of this invocation, not a portable warrant. Recovery must still
use the existing protected status/context path: a process can die after a
commit and before a diagnostic write, including between an intent and entry
into admission.

## Bounds and cost

The existing bundle permits at most 64 batches. For `n` successful batches the
event count is `8n + 3`: two metadata and six actual events per batch, plus
entry, metadata-complete and complete. At the maximum this is 515. Capacity is
516 attempted records, permitting one further failed-terminal attempt. Each
encoded record is at most 2,048 bytes; the entire invocation reserves at most
1,056,768 attempted bytes. Failed partial files consume their reservation.
The sequence and bytes are charged before fallible I/O, so later failure
logging cannot reuse a partially written filename. Empty invocation directories
can remain if construction is interrupted; no retention deletion is automatic.

The writer checks the same existing invocation budget before and after every
write. Its CPU and wall time are ordinary controller work, with no renewal or
parallel observer. Construction requires the diagnostic reservation to fit the
existing spool limit. Planning adds it to the unchanged admission-call spool
reservation before any admission. These remain conservative reservations, not
an operating-system disk quota. `planning.call_spool_reservation_bytes` retains
its previous admission-call-only meaning; it is not a total diagnostics field.
Repeated invocations are not globally storage-bounded by this per-call limit.

Native reservations remain nonrefundable authorization accounting. The retained
`observed_worker_cpu_seconds` is a partial observation. In particular,
`BATCH_CONFIRMED` is written before the existing enclosing `finally` adds the
just-returned batch's worker counter. Subsequent records, including a terminal
record when reachable, include that addition. Every diagnostic uses
`PARTIAL_OBSERVATION_NOT_COMPLETE_MEASURED_CPU`; the existing result resource
fields and accounting order remain unchanged. Missing records cannot establish
zero work, elapsed time to death, peak memory, clean closure or a failure cause.

## Failure and compatibility rules

`ADMIT_INTENT` must complete before the existing `entered` uncertainty flag is
set and admission is called. Failure before that boundary refuses without a
new admission. Once `owner.admit` returns a valid result, the confirmed root,
uncertainty flag and observations are updated before `BATCH_CONFIRMED` can fail.
Thus a failed post-return diagnostic cannot erase a known confirmed prefix.
If admission itself fails, the prior prefix and possible-unreported-commit
indicator retain their existing semantics. A second error while attempting
`FAILED` is swallowed; it cannot replace the original exception, prefix or
uncertainty. Budget exhaustion may prevent any terminal record. Process death
and exceptions outside ordinary `Exception` handling need not write one.

The success dictionary and `IntakeError.report` each add one field,
`progress_directory`. It is the invocation path as a string after `_Progress`
construction completes, or null in a caught failure before construction
completes. A null value does not prove that no partial directory exists.
Existing fields retain their meanings. Configuration/budget failures preceding
the original `try` still raise as before. No new CLI flag or stdout/stderr
progress stream is introduced; callers still receive the final JSON protocol.
The path is an access convenience, never an acceptance or resumption token.

Private `_plan_all` callers may omit `progress` and retain the old behavior and
return shape. The product intake supplies its own private scalar callback.
All checking, custody, catalog, native and controller payloads are unchanged by
this source task. The auxiliary package PROFILE must change on integration.
The protected implementation identity can remain unchanged only if root's later
exact support-map comparison verifies every identity-bearing payload unchanged.
This design does not itself select installation, packaging or a runtime.

## Evidence boundary

Focused controls should exercise the real intake loops and pinned ordinary-path,
JSON and exclusive/fsync writer helpers with explicitly labeled semantic/native/
store doubles. Check the bounds and partial-file behavior, failures before and
after synthetic admission, original-error preservation, the additive path field,
and unchanged checking order/count relative to the pinned predecessor. A
64-batch maximum-count fixture must use reused tiny batches: 64 new batches
would violate the unchanged admission spool cap and cannot justify raising it.

This source cannot diagnose owner startup before `intake` or distinguish the
internal subphases of `owner.admit`. Extending it to those boundaries requires a
separate demonstrated need. It is observability for a finite existing workflow,
not a diagnostics platform, mathematical acceptance result, or final-v5 claim.
