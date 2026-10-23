# Actual prefix-preserving ordinary admission recovery

## Verdict

**PASS_ACTUAL_SELECTED_CHECKED_CLOSURE_AND_CATALOG_REOPEN; NOT FRONTEND,
DISCOVERY, GROWTH OR RELEASE.**

The actual recovery completed both remaining batches, without rerunning the
accepted basis or first extension. The final protected local chain contains
the selected `DMKN.ReadFootprint.readsOnly_insertMany` theorem. This is a real
Lean checked-closure result under the pinned checker/foundation/owner-store
assumptions, not acceptance from a JSON success field or arbitrary peer binary.

The reviewer read the complete selected recovery controller, prior source and
actual-prefix reviews, terminal outer result, both actual worker event records,
both reports, all emitted controller records and all new diagnostic logs.
Independent read-only checks matched the complete original manifest, source
snapshots, exact batch payloads, dependency/symbol bindings, reports, plans,
catalog records and artifacts. SQLite inspection used `mode=ro&immutable=1`;
neither product catalog was opened through its owner API. The old database's
hash remained unchanged. No Lean run, replay, retry, product/state change or
Git action was performed by this reviewer.

## Exact operation and preserved original state

- Recovery: `experiments/v5-local-checks/ordinary-native-recovery-01`.
- Selection: `c00f1ab60ff9134402cea0edd869c0f0903727988b58fef67036ef8d1fa55cf1`.
- Selected controller:
  `e063c39127a5448784660cc946fb837ba68df2f173da9fa1745d6fb83e54e449`.
- Recovery manifest:
  `4af119ba2ae759634529f01093555ba45bdf420307ab057f61b2085f16f23bef`.
- All **2,875 original files / 75,549,957 bytes** still match that manifest.
  All thirteen original and two recovery source snapshots match their selections.
- Original database remains
  `8a16b43aabcd6973403f1843a55fa76a2e2551ed53ec281a81917a369f9f2f75`.
- The copied basis and first-extension catalog records are identical to their
  original records; both artifacts retain their original bytes and hashes.
- Original failed operation
  `7160c6db37d6548f76f6fa319131ca50c8428147f85f278697a9613eddf1abcb`
  remains `FAILED_RETAINED`, with its empty staging directory and 67,108,864-byte
  charged reservation, in both the original and the continued store.

Only two new call directories exist: `002-extension` and `003-extension`.
Their actual argv select `extend`, the original frozen controller/worker,
the corresponding authenticated parent plan, and the correct unit array.
The previously failed second-batch root is reused as the deterministic result
identity, **not** as a resumed grant: the new operation ID is different.

| Newly checked batch | Units | Added names | Artifact bytes | Actual nested Job CPU |
|---|---:|---:|---:|---:|
| 2 | 1,024 | 1,032 | 4,456,784 | 42.953125 s |
| 3 | 804 | 834 | 5,883,880 | 57.84375 s |

The independently reconstructed complete dependency map has 3,622 unique names:
581 basis + 1,175 first-batch + 1,032 second-batch + 834 third-batch names.
All 2,852 exact inert evidence documents' imported symbol IDs match previously
available bindings, and every exported symbol ID matches its original
profile/unit/name derivation. Exact streamed batch arrays and batch request
hashes match the actual worker inputs and catalog records. This independent
identity/dependency check is not a second mathematical check.

## Accepted target and durable roots

The ordered chain is:

1. Basis `cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299`.
2. Reused first extension
   `e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201`.
3. New second extension
   `4be468bdaa615733e9509cc7fc76a33b2f4b4d0d175ae237b991bce0200ae95c`.
4. Final third extension
   `4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026`.

The final theorem comes from evidence `02851.json`, unit
`1dcc39a00ec466fb4a5a23531ddf6105181a630340f6d2c2ebd5ef26c7a2a554`, with symbol ID
`69149e1f8a896e4c754256527cac79b2d90e2777ea89772cde3efb88c88edd13`.
It appears in the actual third worker's exact name census and committed record,
not merely in the original export bundle. The same original V1 profile remains
`fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219`.

Both reports match the exact module/parent modules, units, new names, output
size, request and emitted post-commit records. All four artifact hashes match
their catalog records; each committed operation contains exactly `chunk.olean`.
The final store has four roots and five operation records, including the retained
failure, and 13,160,616 bytes of actual committed snapshot payload.

The executed controller closes/reopens the final catalog and compares its entire
context, authenticates the selected artifacts and checks target membership
before writing the final result. This establishes **catalog/context reopening**.
The two extension workers also actually restore their earlier native parent
snapshots. It does not separately establish a fresh Lean consumer deserializing
the final third snapshot: that later consumer boundary remains to be exercised
as part of useful source reuse, not an otherwise redundant standalone rerun.

| New evidence | SHA-256 |
|---|---|
| Outer RESULT | `2c765a3fa63ec4e2df88ef67ea735eb0af7fa448155a0dae7238d7225eb1121e` |
| RECOVERY-RESULT | `0929879c732acf0439f021801c763351ebb3ff59bebd2a0b06c8c543211c7e08` |
| Continued database | `bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9` |
| Second artifact | `21078a36e4dad055f20b02e58e4978682a9bd3669d8ca7d8b3589a27d339b375` |
| Third artifact | `bef81407fcde9f2068a232ae7b0bb9605fc12e6a7edeebd2ab6614b1542f2569` |
| Second worker report | `82fcced0f1a36ba998be7b0506ab1cb7eea2b1f9913a336d5cd77938355e95cd` |
| Third worker report | `95b8449c19225b7cf942a9addd2c6a119364ce760bb8e7bf9b72d563f74aa079` |
| Second supervision | `90a4215949c10c013bde7755a3a6256ea75d566896f85dcaecc66c530f270f0d` |
| Third supervision | `dc09f51968b0d9bd873844ea837ec72009f248b1624d2c2a2ed3ffff0164ad7e` |

## Diagnostics and assurance boundary

Outer stderr is empty. **The two new native stderr files are not clean:**
batch 2 has eight `Lean.AsyncConsts.add` duplicate-normalized-private-name
PANIC lines / 2,180 bytes; batch 3 has six such lines / 1,664 bytes. Every line
is the same auxiliary frontend-map collision class explained in
`ACTUAL-ADMISSION-OUTCOME.md`, now involving hash-map model/well-formedness,
Nat bitwise/power-of-two and associative-list internal names. There is no new
out-of-memory diagnostic or other diagnostic class in these logs.

The unchanged worker restores its authenticated local parent, decodes inert
units, calls the unchanged `checkAndWriteChunk`, and reports only its actual
checked delta. CheckedExtension still performs `addDeclCore(doCheck := true)`
and obtains dependencies/census/records from `toKernelEnv`. The prior narrow
kernel/snapshot argument therefore applies to these same specific diagnostics.
No generic permission to ignore PANIC messages is inferred. A fully coherent
ordinary frontend environment and private-name handling remain an owner-bridge
obligation; the local acceleration snapshots are not portable peer authority.

## Full selected costs and closure

Outer and both nested Jobs exited zero, reaped the direct children, reached zero
active/terminated processes, closed their Jobs and recorded no cleanup errors.
No worker or retry remains live in this operation. The unchanged limits were
360 CPU seconds / 420 wall seconds / 1,536 MiB for this selected continuation.

- Recovery inclusive outer Job CPU: 153.21875 s.
- Separate outer runner CPU: 1.015625 s.
- **Recovery known CPU: 154.234375 s; outer elapsed: 155.74402860039845 s.**
- Recovery peak Job private commit: **1,074,900,992 bytes**; nested peaks:
  910,716,928 and 1,021,550,592 bytes. Do not subtract different-time peaks
  and call the difference measured controller RAM.
- Original failed admission remains charged: 116.921875 known CPU seconds.
- **Admission plus recovery: 271.15625 known CPU seconds**, below the original
  480-second planning total; summed outer elapsed is 277.9304931005463 s.
  Nested worker CPU is already inside outer Job CPU and is not added again.

For broader context, the three preserved failed export routes, successful native
exporter build, successful export, original admission and recovery together cost
**349.328125 known CPU seconds / 362.1086601004936 summed outer wall seconds**.
This includes their failures, not just the successful path. It excludes earlier
component development/tests, audit effort, index/service costs and future
consumer work; it is not a measured total research cost or full-cost advantage.

The revised streaming controller completed the exact remaining workload under
the unchanged memory cap without replaying accepted checking. This supports
the concrete workflow repair; it does not isolate the exact allocation that
failed previously or establish a general memory scaling bound.

## Next central boundary

Use the accepted method from ordinary source through the separately designed
warranted owner bridge, export/check a substantive consumer extension above the
accepted boundary, then integrate unknown-ID discovery. That work should reuse
this checked store and exact evidence rather than rebuilding its ancestry.
The common-author fixture is compatibility evidence, not mathematical novelty
or a growth advantage against an equally optimized ordinary library baseline.
Portable semantic identity, public isolation, distributed availability and
whole-system economic benefit remain unresolved; v5 is not completed here.
