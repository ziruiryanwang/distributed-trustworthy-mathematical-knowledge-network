# Independent saved-outcome audit: candidate construction and reciprocal check

2026-10-23. Reviewer: `admission_event_audit`. Read-only saved-evidence audit;
no compiler, test, consumer, worker, catalog operation or Git command is run by
this review. The source contract is separately reviewed in
`OWNER-CONSTRUCTION-SOURCE-REVIEW.md` (`fb3bcd70...`).

## Current disposition

**Actual independent successor admission now passes for seven complete units:
two missing-library support units plus the five unchanged consumer05 units.**
The new checked root is `98e65adc...` in a fresh copy of the protected store;
the original store is unchanged. Source construction, inert export and actual
receiver acceptance are separately evidenced below. Consumer04's earlier export
refusal and all failed helper/control attempts remain preserved. This is local
reciprocal checked use, not yet unknown-ID discovery, growth or public release.

## Construction helpers02

Operation: `experiments/v5-local-checks/ordinary-construct-helpers-02`.

| Saved file | SHA-256 |
|---|---|
| `selection.json` | `faf57e3d64a1cd0098a0b1aa703a7972f74cc7c910487682b6f32d68596c959e` |
| `RESULT.json` | `f904c7e26f39dfd2f1c60c06f48465f1337b7aab4b280ef8fe7d19d69034791e` |
| `COMPILE-RESULT.json` | `2e59cbbdc7110cc3f163b8fe5af65f0601ae3f6d6f2182f9ffa253e7f3b72601` |

All seven selected snapshot sources and 67 runtime pins were independently
rehashed without mismatch. The selected helper is the reviewed explicit-field
syntax successor `04f60571...`; no old successful lower helper or mathematics
was rebuilt. The earlier helper01 failed attempt remains preserved, not relabeled.

The actual compile report lists exactly five zero-exit modules:
`OwnerConstruction`, `SuccessorExport`, `SuccessorExportCommand`,
`OwnerConstructCommand`, `ConstructExportCommand`. Their ten native stdout/stderr
files are all empty. All 25 expected nonempty `.olean` / private / server / IR /
IR-signature artifacts exist. Those are build artifacts, not accepted snapshots.

The supervising result is `COMMAND_EXITED_ZERO_AND_CLOSED`: child exit zero,
direct child reaped, Job closed, no cleanup errors or termination request,
zero active and zero terminated processes. Job CPU is 5.46875 seconds and
wrapper CPU is 0.53125 seconds, giving 6.0 known CPU seconds. Outer wall is
6.5126774 seconds and peak Job private commit is 878,620,672 bytes. These fit
the selected 150 CPU / 240 wall / 1,536 MiB envelope. This is not a speedup
measurement or whole-system cost bound.

## Actual consumer04: useful construction, safe export refusal

Operation: `experiments/v5-local-checks/ordinary-owner-consumer-04`.
Selection SHA-256:
`0d2df166f5eefa77a41065ddf437b6567c87b517fd19441bad37f2df924c0660`.
RESULT SHA-256:
`823e2292441ed39aab131de69892a9d6eecadbde949478fae4f4b22ebf4346d6`.

All three selected snapshot sources, 96 runtime pins and 388 copied request
files independently rehash without discrepancy. The copied preparation manifest
is the adopted `09477faa...` cut, not a new projection. The original consumer
source and retained body hashes match the source map; the body occurs verbatim
in generated source `9a9326060647f3c80c7f0fec991c475fe2dbe3e7a30e0acfbfb104c6304e531b`.
The source map records no producer import, explicit candidate construction and
no receiver policy change.

Actual native diagnostics report:

```text
groups=387 basisRows=316 targets=3
labels=833 introducedNames=3
introducedSignatures=#[DMKN.ReadFootprint.readsOnly_insertMany]
checkedUnits=2 scanNodes=546 encodedNodes=109672
payloadBytes=4549097 rawBytes=4549204
```

Thus the source path installed two checked construction units and one temporary
theorem signature, without matching the entire accepted body closure or replaying
that accepted theorem's proof. The body elaborated far enough for the export
command's actual current-module theorem-record requirement and new-unit scheduler
to run. The only earlier diagnostic is an unused-variable warning, not a proof
failure. This is scratch construction evidence, not final mathematical acceptance.

The first error is:

```text
ORDINARY_EXPORT MISSING_WARRANT_OR_FULL_DECLARATION ... name=Iff.rfl
```

`Iff.rfl` is an imported axiom-shaped public theorem record not included in the
833 prepared labels. The existing scheduler therefore tried to export its full
declaration instead of stopping at an accepted identity. No final owner `.olean`,
`consumer-export.json` or `CONSUMER-RESULT.json` exists. No receiver operation is
implied by this failed consumer.

Child exit 1 was cleanly reaped and Job-closed, without cleanup errors or
termination; final active/terminated processes are both zero. Job CPU is
28.15625 seconds and wrapper CPU 0.75 seconds: 28.90625 known CPU seconds.
Outer wall is 34.3150714 seconds; peak Job private commit is 977,334,272 bytes.
The failure is preserved and charged, not relabeled as a successful contribution.

## Exact presence check: the missing label is already accepted

Root requested this read-only decision prerequisite. An immutable read-only
SQLite query (`mode=ro&immutable=1`, no product `LocalCatalog.open`) followed only
the selected parent's accepted root chain and selected the exact encoded name
`Iff.rfl`. It returned one binding:

```text
parent context:
  4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026
introducing accepted root:
  e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201
symbol ID:
  5ca2de3b4b7bd17470027e72a1549cd53c482efb1743886968e3fd9d9c1c1850
```

The original database SHA-256 was checked before and after and remains
`bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9`.
No catalog bookkeeping, accepted state or experiment was changed. The query is
a bounded diagnostic over the retained local store, not evidence that its
current JSON-record storage provides an asymptotically efficient global index.

## Decision supported, not yet executed

The next seam is deferred candidate import binding, not acquiring `Iff.rfl`'s
old proof, adding every parent name to the authoring map, or retrying one missing
lemma at a time. An explicitly nonauthoritative candidate bundle can stop at
safe imported owner records, carry their reached unresolved names and let the
trusted controller resolve all of them in the actual accepted receiver context
before native checking. Known acquired IDs retain their stricter exact checks.

Gather and report the entire finite missing set before spending on native work.
An unresolved name absent from the receiver must not become a trusted axiom or
automatically trigger unbounded private-body acquisition. New current-module
declarations remain complete new units; name collisions must refuse rather than
silently becoming imports. Dynamic stopping must treat actual referenced names
and normalized generated-group owners consistently while retaining the actual
referenced member names in the candidate lookup map.

Root has selected source successors for this seam. Their independent source
review is separate; neither that selection nor this saved audit supplies a
successful export, independent successor acceptance, discovery result, growth
advantage or final-v5 release.

## Deferred-import helpers and controls: later saved evidence

The independent source review is now `DEFERRED-IMPORT-SOURCE-REVIEW.md`,
`aecde1751296b8be432a23025a58631d4a9b38920a1b10d21abc03cd38d704e4`.
The following later evidence supports compilation and pure resolution only;
the consumer04 outcome above is unchanged. Root may proceed with the same
consumer without repeating the successful helper or control operations.

| Operation under `experiments/v5-local-checks` | Selection SHA-256 | RESULT SHA-256 |
|---|---|---|
| `ordinary-deferred-import-helpers-01` | `9aaa09f0ab872816e41e796a5e5927e3cbd2a32445f29bb277e01c9a0d4e6793` | `9fb5850986d7d8dde4058cab438a90dfdc6510124eb4da35bde88ebe8179637d` |
| `ordinary-deferred-import-controls-01` | `56b7a3a4f32da6eb7b591110050a19336b4d69b4d0b5c108f9bb5c104e2d6820` | `d2332432b1876d47429d4e3ec4b1b41c0db3c25c8faafbe0c8e858ddd5988510` |
| `ordinary-deferred-import-controls-02` | `33c133bc1b8f6507e793d758732e11811eb5508f945c5fcbad5020fb5735bf53` | `4df5e5d471dae5334ee0e1b57e7e94d2901c32a0e35cab2b29abcf6ac638a258` |

Helpers01: all six snapshot source pins and 94 runtime pins rehash exactly.
The actual compile report lists zero exits for `OrdinaryExport`,
`SuccessorExport`, `SuccessorExportCommand`, `ConstructExportCommand`. All
eight native logs are empty and all 20 expected artifacts are nonempty. The
outer result is clean: zero exit, direct-child reap, Job closure, no cleanup
errors/termination and zero active/terminated processes. Job CPU 4.953125 plus
wrapper CPU 0.640625 gives **5.59375 known CPU seconds**; outer wall 7.0920609
seconds, peak private commit 875,696,128 bytes. No native receiver was rebuilt.

Both controls runs independently match four source pins and three runtime pins.
Controls01 preserves the original harness failure: six assertion failures and
two errors (`ARRAY` before intended branches), five passing controls. Its only
repair converts tuple fixture rows to JSON-list rows; reversing that exact
replacement reconstructs the failed snapshot byte-for-text content. No resolver
or parser was relaxed. Its clean failed run consumed 0.140625 known CPU seconds.

Controls02's saved stderr records all **13 tests passing**, with no failure,
error or skip, and stdout is empty. The result shows zero exit, clean reap/Job
closure, no cleanup errors/termination and zero active/terminated processes.
Job CPU 0.09375 plus wrapper CPU 0.09375 gives **0.1875 known CPU seconds**;
outer wall 0.3015305 seconds, peak private commit 18,317,312 bytes. This is the
repaired fixture `8f2ee59c...` against the reviewed controller `f976c9ea...`.
The reviewer authored the controls; this paragraph independently inspects saved
execution/pins but is not a claim of an independent test-design author.

## Consumer05: complete ordinary candidate, one missing receiver dependency

Operation: `experiments/v5-local-checks/ordinary-owner-consumer-05`.

| File | SHA-256 |
|---|---|
| `selection.json` | `5bf7e5ce4670eba2950498f38569d92d6897b2271e805591f7e9e4df5b4c2cf4` |
| `RESULT.json` | `1a0e881ae935a4a41aa7e726ad3e5f91165dd70b4e1db5c88ca939e9cd5474ea` |
| `CONSUMER-RESULT.json` | `e7eb05bb7fb719123c000f0115eede393a294c511ed4cd60d47f7ebef81518a4` |
| `consumer-export.json` | `a7f6f86bb28f10427d599bcfa2a3984ae66c418ad0a9bad18e37b90f10372975` |
| Generated consumer `.lean` | `96b60338a47ca5041558bcb934c81ec3f2597a58432212ae8ec10756b7c687f6` |

All three source pins, 118 runtime pins and 388 request-file length/hash pairs
match independently. The source-map original hash is
`8857b2aae97e574aa1305ad0bb3546a04f168c73d334ad0ab1f64386ba077e97`;
its body after the replaced import line occurs verbatim in generated source.
No producer import or theorem-statement simplification was substituted. The
same two checked construction units and one scratch theorem signature are
installed; construction counts agree with consumer04. The only warning is
again the unused `avoids` binder. Five owner build artifacts are nonempty.

Saved stdout, the candidate packet and the consumer result agree on five new
units: definitions `snapshot`, `applyBatches`, then complete theorems
`snapshot_readsOnly`, `snapshot_applyBatches`,
`snapshot_predicate_applyBatches` under `DMKN.ReadFootprint.Consumer`.
The candidate has 37 claimed imports, eight unresolved imports, seven selected
dependency edges, 2,754 scan nodes, 96,106 unit-JSON bytes and 103,060 total bytes.
No whole-owner source census occurred. This is an actual ordinary-source
reuse/export success, **not** a checked receiver extension.

The result records zero exit, clean direct-child reap and Job closure, no
cleanup errors/termination and zero active/terminated processes. Job CPU
22.921875 plus wrapper CPU 0.71875 gives **23.640625 known CPU seconds**;
outer wall 26.9183990 seconds, peak private commit 978,477,056 bytes. These
observations are not a controlled speedup comparison with consumer04.

Root requested inspection of **every** unresolved name before native spending.
An immutable read-only SQLite connection followed the exact accepted parent
chain, decoded its 3,622 unique bindings and compared the candidate names.
All 37 claimed IDs agree with that parent; seven of eight unresolved names
are present:

| Name | Parent lookup |
|---|---|
| `Iff` | Present in basis `cb8f9c2d...` |
| `instTransEq` | Present in accepted root `e0053044...` |
| `Iff.rfl` | Present in accepted root `e0053044...` |
| `List.foldl` | Present in accepted root `e0053044...` |
| `List.mem_cons_self` | Present in accepted root `e0053044...` |
| `List.map_congr_left` | **Absent** |
| `List.mem_cons_of_mem` | Present in accepted root `e0053044...` |
| `Trans.trans` | Present in accepted root `e0053044...` |

The full bundle hash was checked. The original database hash before and after
the diagnostic remains `bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9`.
No product catalog code, write, native checker or test was invoked. The finite
query is a decision prerequisite, not a new scalable-index implementation.

The HOLD was reported immediately so the known-incomplete candidate need not
consume a native attempt. The protocol now exposes the **complete missing set**
instead of serializing old proof histories or failing one unknown label per
owner run. The remaining need is actual complete evidence for the absent lemma
or another sound construction that no longer requires it. Its local public
axiom-shaped handle is not admissible as a new trusted axiom. Root owns selection
of that next step; this review does not rewrite the fixture or select acquisition.

## Actual combined successor admission01

The missing-library pass subsequently exported complete candidates for
`List.map_inj_left` and `List.map_congr_left`, without re-elaborating consumer05.
Its source/build/protocol and actual extraction are independently reviewed in
`MISSING-IMPORT-COMPLETION-REVIEW.md`. Root then selected one seven-unit receiver
operation over the original adopted parent; no earlier accepted proof closure
was replayed and no certificate was produced.

Operation: `experiments/v5-local-checks/ordinary-successor-admission-01`.

| Saved file | SHA-256 |
|---|---|
| `selection.json` | `9b24d042c429e90f260eaacdfd41c6ea14dd5fd98c6a619b09b8cca504204b41` |
| `RESULT.json` | `a0273ec06eb9be9e64e0695fe8a4fbc2ed2528d4f540fabc41d2cbf6b1718726` |
| `successor-admission/SUCCESSOR-RESULT.json` | `188110017e34f123f2a6b6fe9b6eb4df7dcd3d9ace888dd0beec9669a9de28a6` |
| `successor-admission/ADMISSION-PLAN.json` | `9172ac74b11f544b64e3517a5e348699078f281422515d17a2ea6e510b5d6cb3` |
| `successor-admission/call/SUPERVISION.json` | `77cacf7002d2954672eaed922d5a4b1bb9f7a0ebf60f11b39670f5ddbe42890c` |
| `successor-admission/call/worker-report.json` | `27326c11c5bdd3a89ddd4d4b24a4e06c79cec56c29973afa9477651237165b88` |

All two snapshot source hashes and 51 runtime pins independently match. The
controller is the reviewed combined cut `82a6e630...`. The actual worker argv
uses the retained old native admission controller, build, core, snapshot helper
and `extend` operation; it does not invoke the new authoring environment as a
receiver. All five original candidate raw units and both supplemental raw units
occur unchanged in the saved 127,594-byte native input, in the intended order.

Independently parsed all seven canonical evidence files, totaling 149,467 bytes.
Starting from the 3,622 accepted K bindings, every direct import ID agrees with
K or an earlier new unit. No new name overwrites a previous binding. Independent
domain-separated hash reconstruction yields exactly:

```text
batch request:
  10e2fed8961972014b5de35dfe9bdbe4c5d8c0203785473f62b05b5f400d84a0
new checked root:
  98e65adcb09061a78dd3088a4bbf966b9ac1cee9f98da6f8fbcdb410f3edf7b9
target symbol:
  b0170e3c14cc7dc005376c5f7a0449026fd9786966c734190f5ac7f665920317
native artifact:
  b0dded473db30ead07ba22ae9a3efed7cee778917826bbcce3ee7b9e79efd8d3
```

The actual worker reports **seven checked units and seven names**, exactly the
saved two support plus five consumer declarations, 4,038 encoded nodes and a
57,504-byte artifact. Both native stdout and stderr are empty. Inner supervision
records zero exit, direct-child reap and Job closure, no errors/termination and
zero active/terminated processes. The inspected controller only reaches the
private commit after this actual event and exact report/artifact/grant binding;
the saved PASS text alone is not used as an acceptance token.

Immutable read-only SQLite inspection of the new store confirms exactly one
additional root and one additional `COMMITTED` operation, with the actual
artifact size/hash and the seven independently reconstructed bindings. All four
original root records are byte-identical in the copied database; all previous
operation rows remain, including earlier failure state. The resulting context
has 3,629 names. The controller's postcommit close/reopen equality check succeeded.
Independent saved inspection obtains the same target ID. No product catalog
open or native check was rerun by this review.

The original store's seven files each still match the selected parent manifest,
and its database hash remains
`bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9`.
The copied original artifacts and adoption/lock files also match. The new store
is only under the new operation's `successor-admission/catalog`; original state
was not promoted in place or rewritten.

Actual native worker CPU is **2.234375 seconds**, peak private commit
627,838,976 bytes. Outer inclusive Job CPU 6.453125 plus wrapper CPU 0.53125 gives
**6.984375 known CPU seconds** for this entire admission operation; outer wall
8.9328583 seconds and peak private commit 669,491,200 bytes. Do not add the inner
worker CPU again to the outer inclusive Job count. Construction, completion,
builds and older failed work are separate previously reported costs; this is
not a full-cost growth benchmark.

## Combined pure controls, separate from actual mathematical acceptance

`ordinary-combined-admission-controls-01` selection
`5b3d7043faf328d759d384a2b2d16683cbe00d22cb0ebdb4e9ae0bf33aeddbde`,
RESULT `e42ed1d6fd6e0b87d23b048f897c21067230c264d8c6de22a5eb63214fcb603b`.
All four sources and three runtime pins match. Saved stderr records all 16
focused groups passing, without failure, error or skip; stdout is empty. The
result has clean zero-exit/reap/Job closure and zero active/terminated processes.
Job CPU 0.171875 plus wrapper CPU 0.09375 gives 0.265625 known CPU seconds,
wall 0.4108978 seconds, peak private commit 18,821,120 bytes. These controls test
planning and refusal boundaries; only the separate native event above checks
the actual new mathematical units.

## Scope now established

An ordinary local Lean author can use the acquired checked method, construct a
substantive unchanged extension, discover the complete missing installed-library
dependency set, obtain only the absent proof-bearing units, and have all new
units independently accepted against the receiver's existing mathematics.
Neither authoring correspondence, peer native artifacts nor proofless signatures
serve as receiver warrants. This establishes the selected local reciprocal loop.
Portable identity migration, unknown-ID federated discovery, justified net growth
and public deployment remain distinct unfinished work; the goal is not complete.
