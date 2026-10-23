# Actual ordinary admission01: accepted prefix, failed continuation

## Verdict

**PARTIAL_CHECKED_PREFIX_WITH_RETAINED_OOM_FAILURE; NOT FULL ADMISSION.**
Read actual outer RESULT, controller stdout/stderr, PLAN, three supervision
records, both successful worker reports, all failure logs and the first
extension's nonempty diagnostic log. Independently matched all13 selected
source snapshots. Inspected the terminal SQLite database in read-only immutable
mode, without opening the product catalog owner; its hash remained unchanged.
No native execution, retry, implementation edit or Git action was performed.

The fixed456-unit/581-name basis and the first1,024 exported units/1,175 names
were committed. The second extension batch failed with an explicit
`INTERNAL PANIC: out of memory`. It produced neither a worker report nor an
artifact, was not committed and remains `FAILED_RETAINED`. The third batch was
not launched. No `ADMISSION-RESULT.json` exists; the selected ReadFootprint target
is absent from the accepted1,756-name union.

## Actual durable state

| Item | Observed state |
|---|---|
| Basis root | `cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299`; COMMITTED;456 units/581 names |
| First extension root | `e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201`; COMMITTED;1,024 units/1,175 names; exact basis parent |
| Failed second root | `4be468bdaa615733e9509cc7fc76a33b2f4b4d0d175ae237b991bce0200ae95c`; absent from roots; operation FAILED_RETAINED;64 MiB reservation retained |
| Actual artifact census | Each committed operation contains only its `chunk.olean`; failed operation directory is empty |
| Prepared evidence |2,852 files totaling49,499,157 bytes; preparation does not imply acceptance |

Both committed artifact sizes and SHA-256 digests independently match their
database records. Their report name sets, module names and parent module names
match the committed bindings. The source event path requires a successful
actual supervised native invocation, exact report/input bindings and active
grant before `_commit_checked`; this was not adoption from arbitrary saved
PASS text.

| Evidence | SHA-256 |
|---|---|
| Outer RESULT | `2a3fe8f2b704521964bf4e5aff5480b3504a3c7645d450ad7bf29c43ca835103` |
| Unchanged catalog database | `8a16b43aabcd6973403f1843a55fa76a2e2551ed53ec281a81917a369f9f2f75` |
| Basis artifact,669,968 bytes | `d92288b5455002c95c81cd595ccfdedf357a2b9b249ff44e1f557e26fc4cb54b` |
| First extension artifact,2,149,984 bytes | `89ebbba3e3f0db1d4fdf5fbf56d8e7eaa2289ae7d2d69fbd62bf55b8518830ce` |
| Basis worker report | `fe7f067acf074c22701b8a9b29be0fefcc9ed6a781814cff8c34008975c2626d` |
| First extension worker report | `e7d17f0840b8b0090a4f5c7de40e503016c3a9a99c94b6857ba569a554ed25fd` |
| Failed second supervision | `c987336d86073048ac474408154eb4f5ff19565d7b487ee7004c4c43403dd0e9` |

## Nonfatal private-name PANIC diagnostics must remain visible

The first extension exits0, but its stderr is **not clean**:3,286 bytes contain
14 `Lean.AsyncConsts.add` PANIC messages involving distinct original private
names with equal normalized user-name suffixes. The affected suffixes include
`PSigma.casesOn._arg_pusher`, `List.filter.match_1.splitter` and two List membership
lemmas. This is a separate observed issue from the later allocation failure.

The exact pinned Lean source explains a narrow boundary:

1. `Lean/Environment.lean:701-731` calls the checked FFI operation
   `addDeclCheck` when `doCheck := true`, before adding elaborator async-map
   entries. The FFI binding is `lean_elab_add_decl` at687. The exported
   `updateBaseAfterKernelAdd` at2480 explicitly sets `checked := .pure kenv`.
2. `AsyncConsts.add` at459-469 tests a private-prefix-erased name in its
   normalized trie. On collision, its explicit `Inhabited` default is the
   previous async collection, not a replacement kernel environment.
   `Init/Prelude.lean:3710-3723` documents that `panic` prints and returns its
   default rather than terminating execution. Thus these logs are compatible
   with exit0, but mark an incomplete elaborator-side cache.
3. The selected `CheckedExtension` uses `toKernelEnv` for grounded references,
   exact generated-record comparison, new-name census and collected output.
   Its `addDeclCore` always uses `doCheck := true`. The selected `LocalSnapshot`
   writer serializes only actual `CheckedBatch.added` records, not async maps
   or a whole frontend environment. Its `ModuleData` contains no environment
   extension entries or IR.

Under the existing pinned-kernel/FFI correctness assumptions, these particular
async-map diagnostics do not invalidate the narrowly checked kernel records or
their stored snapshot. This is a source-boundary argument, not an independent
proof of Lean's native checker. It does **not** qualify the returned high-level
`Environment` for ordinary elaboration: private-name lookup and other frontend
behavior can be incomplete. Do not suppress the diagnostics, label the logs
clean, or infer ordinary owner-project usability. A future owner bridge must
respect or explicitly repair this separate environment boundary.

Reviewed frozen source hashes:

- `run_native_admission.py`:
  `a9bdbfc826221d21cd6454b1f8171b77e657996d89bac0461bee2f6e74ee897a`.
- `CheckedExtension.lean`:
  `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1`.
- `LocalSnapshot.lean`:
  `488a76f4b8599a95bdc748c5e89187bc55e23f63d34cf52952702d93ff68795c`.

## Resource evidence and causal limit

Outer execution failed with child exit1, direct child reaped, zero final active
processes, closed Job and no cleanup errors. All three nested Jobs also closed
with zero final active processes and no cleanup errors; the third nested
invocation is failed call002, not a third extension batch.

- Total inclusive outer Job CPU116.203125 + wrapper CPU0.71875 =116.921875
  known CPU seconds; outer wall122.18646450014785 seconds.
- Successful basis/extension nested Job CPU:8.234375 and25.125 seconds.
- Failed second-extension nested Job CPU:26.625 seconds. It remains part of
  the inclusive outer cost; do not add nested CPU to outer CPU again.
- Peak private commit: outer1,610,649,600 bytes; failed nested Job860,397,568
  bytes. The unchanged outer memory allowance is1,536 MiB.

The selected controller source demonstrably keeps `bundle_raw`, the complete
parsed bundle, all per-unit canonical evidence and all raw batch payloads live
while launching each worker. `Batch.evidence` and `Batch.raw_units` together
retain the prepared payloads; writing evidence files does not release these
references. The42,202,667-byte raw bundle and expanded Python object graph are
not needed for a worker once its selected data and final metadata are fixed.
Releasing unnecessary controller state before native work is therefore a
specific source-supported improvement, not a guess about system RAM.

The logs do not identify the exact failing allocation or checking phase.
Different recorded process-tree peaks need not occur simultaneously, so their
difference is **not** a measured controller allocation. We cannot prove that
payload retention alone caused the OOM, or promise that releasing it suffices.
The proposed repair has a reason to reduce peak live data without changing
mathematical acceptance or increasing a cap; its actual outcome remains open.

## Recovery boundary and next action

Root has assigned a fresh continuation controller to preserve and authenticate
the committed prefix, retain failed-operation accounting, release unneeded
parsed payloads and issue new finite grants only for unfinished work. Original
source, evidence and catalog tree stay immutable. No basis or first-batch replay
is justified merely because a later batch failed; old grants/deadlines do not
resume, and no uncommitted artifact or prior saved success becomes authority.

Clarification of the earlier export-size note:8 MiB is the **per-unit evidence
envelope** reader cap, not the aggregate native batch cap. The unchanged catalog
permits up to64 MiB total evidence/raw-unit payload per batch and1,024 units.
Actual PLAN uses1,024/1,024/804 units, with9,944,596/16,279,621/23,274,940 evidence
bytes; it does not raise an8 MiB batch limit. Complete envelopes remain checked
individually before reservation.

There is no accepted final method, reopened final context, ordinary source-use,
discovery, reciprocal growth or completed-v5 claim from this failed run.
