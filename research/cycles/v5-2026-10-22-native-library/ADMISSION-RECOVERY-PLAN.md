# Native admission recovery: retain accepted work, remove duplicate live data

2026-10-22. Source-only implementation assignment `ordinary_native_controller`.
New source: `software/v5/ordinary_lean/run_native_admission_recovery.py`.
No execution, compilation, test, original-state mutation or Git operation was
performed by this assignment. Root owns later review/selection and launches.

## Decision and actual evidence

The theoretical recovery is straightforward and does not need a new checker or
storage framework. The original protected catalog records relative operation
IDs, not absolute artifact paths. Its completed accepted prefix can therefore
be copied byte-for-byte into a fresh root, reopened with the **same** profile,
store identity and roots, and continued with fresh operation grants.

Actual original operation `ordinary-native-admission-01`:

- Original selection: `ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f`.
- Profile: `fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219`.
- Accepted basis: `cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299`.
- Accepted 1024-unit prefix: `e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201`.
- Failed next root, **not accepted**: `4be468bdaa615733e9509cc7fc76a33b2f4b4d0d175ae237b991bce0200ae95c`.
- Original total known CPU: 116.921875 seconds (`7483/64`), including outer wrapper.
- Exact plan: three batches of 1024, 1024 and 804 units; 49,499,157 evidence bytes.

Root has read/adopted `ACTUAL-ADMISSION-OUTCOME.md` (SHA
`ebe60db3` prefix): the first chunk's 14 auxiliary frontend-map diagnostics do
not invalidate its actual checked kernel/snapshot output. The recovery preserves
those diagnostics and claims no owner/frontend compatibility. The source does
not reinterpret exit0 as empty stderr, hide warnings, or run those successful
checks again.

The failed nested worker's measured private commitment was about 860 MB while
the outer Job reached about 1,610 MB. The original controller kept the raw owner
bundle, its fully parsed object graph, all canonical evidence and all raw unit
batches alive during native work. This is an actionable duplicate-live-data
problem, not evidence that a larger RAM allowance or another proof system is
necessary.

## What changes, and what does not

The new controller never parses the 42,202,667-byte owner bundle. It retains the
bundle's original hash pin but reads evidence one file at a time, validates it
through the exact original reader, and releases parsed declaration objects.
It recomputes bounded batch identities/counters, reuses the original saved first
and second batch units files, and reconstructs only the third units file that
was never written before the failure. During a native call it holds no whole
bundle graph or batch proof JSON, only compact name/identity summaries.

The original frozen `ordinary_evidence.py`, `local_catalog.py`,
`run_native_admission.py`, all native support sources, their existing compiled
artifacts, and exact worker remain unchanged. Profile recomputation explicitly
uses the **original** driver source and digest maps. The recovery controller is
separately root-selected; it does not rewrite old IDs to include its cleanup
implementation. A future semantic/local-implementation profile split is a
different migration task, not part of this recovery.

There is no basis reconstruction, replay of the accepted first batch, native
rebuild, certificate work, cap increase, automatic retry or mutation/deletion of
the original tree.

## Rooted local authority, not generic report trust

The executable is deliberately restricted to this exact origin path, original
selection hash, profile, store identity, accepted prefix and failed operation.
It is not an API accepting a stranger's catalog and PASS file.

Root must create/select a finite recovery manifest only after adopting the
actual kernel/snapshot review. Its fields are exactly:

```text
schema: DMKN_ORDINARY_ADMISSION_RECOVERY_V1
origin: E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\ordinary-native-admission-01
original_selection_sha256: ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f
profile_id: fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219
basis_id: cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299
accepted_root: e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201
store_id: 12185a972a6302a0a70899e968f4c249d1994afd252ecbb74c91e59961b81eb5
known_spent_cpu_ticks64: 7483
disposition: ADOPTED_FIXED_ORIGIN_AFTER_KERNEL_SNAPSHOT_REVIEW
files: {origin-relative POSIX path: {bytes: exact integer, sha256: exact digest}}
```

The outer fresh selection pins this manifest. The script's `required_files()`
specifies its exact file inventory, with no arbitrary extra or omitted entry:

- All 2852 `native-admission/evidence/00000.json` through `02851.json` files.
- Original `selection.json`, `RESULT.json`, `command/stdout.txt` and stderr.
- Original native `PLAN.json`, `PROFILE.json` and catalog `ADOPTION.json`,
  `catalog.sqlite`, `owner.lock`, and both committed `chunk.olean` files.
- All three calls' `SUPERVISION.json` and `supervision/stderr.txt`.
- The basis and first extension's actual `worker-report.json` files.
- The first and second extension's existing `plan.json` and `units.json` files.

This set is capped at 128 MiB total and 64 MiB per file; the manifest at 2 MiB.
Every member is authenticated before reuse and again before final success.
Metadata with floating-point time measurements is parsed only after its exact
root-selected bytes have been authenticated; the inert evidence itself still
uses the unchanged strict numeric/depth/canonical reader.

## Fresh-copy and accepted-prefix checks

1. Authenticate original selection/source/runtime, manifest and saved event
   files. Require the old outer process and failed nested process to be fully
   reaped/quiescent with no cleanup error. Require actual clean success for both
   accepted workers, exact invocation argv, exact output reports and printed
   post-commit records. The failed report must remain absent.
2. The only original file opened for coordination is its existing `owner.lock`;
   take the same exclusive OS byte lock without changing its bytes. Do **not**
   open the original database through `LocalCatalog.open`, since that can change
   operation state. Require the exact original store directory/file census, with
   no journal/sidecar/withdrawal marker or unexpected artifact.
3. Copy the catalog into fresh `native-recovery/catalog`, preserving all
   directories, including empty failed staging. Stream bytes, flush, and read
   each destination back against the exact selected digest. Close the lock.
   No original file is overwritten, removed or opened for SQLite recovery.
4. Reopen only the copied catalog under its original ADOPTION/profile/store ID
   and exact limits. Require exactly two committed roots and three operations:
   basis committed, first batch committed, second batch `FAILED_RETAINED` with
   its full 64 MiB reservation still charged. No old live grant is reconstructed.
5. Match actual report names/counts/parent/module/size to committed records and
   artifact hashes. Recompute basis symbol bindings and first-batch evidence
   identities and require exact equality with its committed request/bindings.
   Authentication and actual adopted admission events jointly justify reuse;
   JSON counts or matching hashes alone are not mathematical admission.
6. Call `context` on the copied accepted root before native use. It authenticates
   the copied local artifacts and derives the same module chain with new local
   paths. Verify that the original failed call used the corresponding exact old
   parent chain. The move changes paths only, never root/module/symbol identity.

## Remaining real worker events

Only the unaccepted second and third batches execute, sequentially because of
their actual dependency relation. Parallelizing them would add false independence
or a second mechanism, not reduce legitimate dependency work.

For each batch the controller temporarily reads only that batch's immutable raw
evidence bytes to call the original `reserve_extension`; it then releases the
tuple and explicitly collects garbage before native work. The original catalog
reparses evidence and matches actual protected parent bindings. Its new grant
has fresh operation identity/deadline. For batch two, the computed mathematical
root must equal the old failed candidate root, but its operation ID must differ
from the failed one. The earlier failure remains preserved and charged.

The controller invokes the original immutable driver in its existing `--worker`
mode, supervised by the same frozen `A.supervise` and `J.Job`. No checker source
or compiled artifact is regenerated. Each promotion still requires actual exit0,
reaped child, zero active/terminated processes, closed Job, no cleanup error,
unchanged selected source/runtime and exact current input bytes, and the actual
report's exact module/parent/names/unit count/artifact size. Only then does it
call the original private `_commit_checked` with that fresh still-live grant.

The final context must equal all 3622 recomputed exact bindings, retain the
target theorem, and survive a close/reopen with fresh artifact authentication.
The original entire selected evidence/catalog tree must remain byte-identical.
A failure stops immediately, preserving new staging; there is no retry loop.

## Finite envelope and prospective invocation

```text
python -I -S -B <fresh snapshot>/software/v5/ordinary_lean/run_native_admission_recovery.py
  <fresh output> <root-selected recovery manifest>
```

The fresh outer selection must retain every original runtime pin, including
original prerequisite source snapshots and the owner bundle's exact bytes,
and pin the recovery manifest. Fresh source selection needs this driver and
`tools/Run-V5-Check.py`; original modules are loaded from their authenticated
original snapshot, not copied from evolving development files.

At most 360 new outer Job CPU seconds, 420 wall seconds, 1536 MiB, and at least
3 process slots (normally 4). Internal recovery allowance is at most 350 known
CPU / 400 wall seconds, or the tighter outer allowance minus 10 CPU / 20 wall
seconds. Each of the two new workers is capped at 180 CPU / 180 wall seconds,
2 processes and 1 MiB per output stream. Initial authentication, streamed
preparation, copying, final revalidation and controller CPU count in the same
recovery envelope. The original 116.921875 known CPU is reported separately;
the new 360-second ceiling keeps known total below the original 480-second
allocation with some wrapper headroom. Actual final totals still require audit.

All declaration/parser/catalog defaults are unchanged. New output is bounded by
the same catalog quotas, two finite reports/plans/logs and one at-most-64-MiB
reconstructed units file. Sampled log limits are not a hard disk quota; the Job
and owner-controlled filesystem are not a hostile-source security sandbox.

Success would establish the actual selected local checked closure and durable
reuse. It would not establish normal owner/frontend compatibility, discovery,
useful-growth advantage, independently hosted deployment or final v5 release.
