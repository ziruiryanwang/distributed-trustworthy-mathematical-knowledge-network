# Independent source review: fixed-origin admission recovery

**SOURCE_REVIEW_NO_BLOCKER_FOR_ONE_ROOT_SELECTED_BOUNDED_CONTINUATION.**
Read all516 lines of `run_native_admission_recovery.py` and the complete
`ADMISSION-RECOVERY-PLAN.md`, against the adopted actual admission01 audit and
the unchanged original controller/catalog/checker interfaces. Reviewed source
SHA-256:
`e063c39127a5448784660cc946fb837ba68df2f173da9fa1745d6fb83e54e449`.
The canonical guard passed; no runtime, controller edit, original-state change
or Git operation was performed by this reviewer.

Root must still select and inspect the exact manifest/fresh outer selection.
This is not acceptance of arbitrary copied catalogs, and source review does not
establish actual recovery success or memory fit.

## Why the accepted prefix can be reused

The controller hard-codes the independently audited original path, selection,
profile, basis/prefix/failed roots, store identity and operation IDs. Its fresh
outer selection must pin a recovery manifest expressly adopting that exact
origin; the manifest has an exact bounded file inventory rather than accepting
extra caller-selected records. Original sources are authenticated before being
loaded; the original runtime pins are retained. Profile recomputation uses the
unchanged original driver/support, not a newly invented mathematical identity.

Original outer and nested events must be fully closed. Both committed worker
argv vectors, actual reports, emitted post-commit records, report hashes,
module/parent/name bindings and artifact hashes are matched to the two exact
catalog records. The failed third operation must remain uncommitted, its worker
report absent and its64 MiB reservation retained as `FAILED_RETAINED`. These
checks reinforce root's adopted actual-event authority; saved JSON success text
or hashes alone never establish mathematical checking.

The prior first-batch PANIC diagnostics remain selected/preserved. The adopted
argument supports only checked kernel records and protected snapshots, not a
coherent ordinary frontend environment. The recovery's claims explicitly retain
that boundary; it neither suppresses diagnostics nor replays the passed basis
or first1,024-unit batch.

## Copy, locking and failure preservation

`copy_catalog` checks the exact directory/file census, requires the existing
one-byte NUL owner lock and acquires the same exclusive Windows byte lock. It
never invokes `LocalCatalog.open` or SQLite recovery on the original database.
Files are streamed to exclusive fresh outputs, flushed, hashed and read back;
the original lock byte is read through the lock-owning handle, not another
handle that could violate Windows locking. Closing releases the lock without
writing its bytes. Empty failed staging is copied and preserved.

Only the copied catalog is reopened. Its profile/store/limits stay unchanged;
the expected operation/root census excludes any resumed live grant or hidden
extra root. `context(PREFIX)` authenticates the copied artifacts and reconstructs
the module chain. The controller compares the original failed call's parent
plan with the same chain using original paths, so relocation changes paths,
not module, root or symbol identities. Final origin revalidation checks every
selected original file again. Owner-controlled immutability remains a premise;
this is not protection against a hostile local administrator.

Failures stop the operation and preserve fresh output/staging. A worker failure
is settled before `abandon`; transaction uncertainty uses the existing closed-
owner behavior, without retry. If a post-reservation assertion fails before the
inner worker `try`, the reservation can remain `RESERVED` until a later open
marks it `INTERRUPTED`; its storage charge remains retained and it cannot be
committed by this failed process. No original data is deleted or overwritten.

## Exact dependencies and reduced live payload

The controller never parses the whole42,202,667-byte owner bundle. It streams
the selected evidence files one at a time through the original strict reader,
checks every imported symbol against the growing exact binding map, refuses
overwrites, and derives each newly introduced symbol from the original unit
identity. It recomputes exact per-batch counts, node bounds, byte totals and
request hashes. The first batch's exact introduced bindings/request must match
the accepted prefix. Original saved unit arrays for batches one/two must match
the recomputed bytes; only the never-written third array is generated.

Before each native call, only that batch's raw evidence is temporarily read for
the existing `reserve_extension`. That function independently reparses it and
validates dependencies against the actual accepted parent. The tuple and
transient context/plan objects are released and garbage collection runs before
launch; retained summaries contain names/identities, not full proof graphs.
This removes the specific original raw-bundle/parsed-bundle/all-batches live
retention. Python allocator behavior and the remaining Lean footprint still
require actual observation; fit is not proved merely by `del` or `gc.collect`.

Only the unfinished1,024- and804-unit batches execute, in dependency order.
The second batch must reproduce the old failed *root* with a new operation ID
and deadline; old failure accounting is not reused as a live grant. Each actual
promotion still requires the original supervised worker, exact current input
bytes, full cleanup, exact report module/parent/names/count/size and a live grant.
Final bindings must match all3,622 recomputed names and survive close/reopen.

## Finite budget and qualification limits

The fresh outer selection is capped at360 Job CPU seconds,420 wall seconds and
1,536 MiB. Internally at most350 known controller-plus-child CPU seconds and400
wall seconds are allowed, or tighter outer allowances minus headroom. Every
worker is capped by the remaining allowance and180 CPU/180 wall seconds; failed
worker CPU is added before testing success. Preparatory and final controller
work count from controller entry. There is no per-batch budget reset or retry.

The original116.921875 known CPU seconds remain reported separately. The new
350-second internal success limit leaves13.078125 seconds below480 for external
wrapper/headroom accounting. The outer360-second Job cap and sampled limits are
not a mathematical hard bound on cumulative known CPU including all wrappers;
actual totals must still be audited. Worker allowance is calculated before
reservation/prelaunch work, so final/internal and outer checks may refuse an
overrun rather than guaranteeing that all allocated worker time remains useful.
This does not authorize spending beyond the selected aggregate outer envelope.

A successful continuation would establish the real selected local checked
closure and durable snapshot reuse. It would not establish ordinary-source
frontend compatibility, unknown-result discovery, useful-growth advantage,
global deployment readiness or completion of v5.
