# Admit the real consumer successor without replaying the library

2026-10-23. Source-only integration plan, requested by root. **No new controller
code, copy operation, runtime allowance or admission is selected by this note.**
Author: `successor_export`.

## Decision and endpoint

The useful next gate is the actual consumer theorem produced after
`#ordinary_use`, exported through `#ordinary_export_above`, and independently
checked over the retained accepted root. This resolves whether the ordinary
authoring route can contribute back without asking for accepted theorem proof
history. It also exercises loading the final accepted recovery chunk.

Use the existing native worker, artifact format, evidence parser, catalog and
Windows Job supervisor. Do not write a new recovery framework, verifier, storage
format, retry manager or proof system. Proposed fresh root-selected driver:
`software/v5/ordinary_lean/run_successor_admission.py`.

The first actual consumer bundle does not yet exist. Its successful production,
exact source/request/output mapping and independent source review must precede
runtime admission selection. A failed export is not a partial valid bundle.

## Inputs that retain authority

The parent receiver context is the already adopted **local** context, not a peer
catalog:

```text
profile fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219
basis   cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299
parent  4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026
store   12185a972a6302a0a70899e968f4c249d1994afd252ecbb74c91e59961b81eb5
database bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9
```

Retained store:
`experiments/v5-local-checks/ordinary-native-recovery-01/native-recovery/catalog`.
Its actual four-root checking/recovery event chain was independently adopted;
the next controller need not re-prove that adoption by replaying all original
declarations or repeating the old event audit. A fresh exact input manifest
anchors the already adopted catalog bytes, adoption marker and four chunks.
All original failed operations and reservations remain present and charged.

Native worker and support remain the exact original admission selection's
`run_native_admission.py --worker` / `OrdinaryWorkflowWorker.lean`, compiled
core05/snapshot01/workflow01 artifacts and Lean runtime. Load these from their
retained selected snapshots, not the now-module-enabled mutable authoring files.
The new controller may reuse `clean_worker`, `REPORT_FIELDS`, `AuthoredFiles`,
fixed runtime-pinning helpers and the existing supervisor import seam. It must
not silently derive a different receiver profile from the new authoring helpers.

## Minimal preservation copy, not another recovery

The recovery evidence is frozen, so opening its original SQLite through
`LocalCatalog.open` is inappropriate: that method owns writable bookkeeping and
can transition reservations. Make one fresh local working copy of the existing
catalog and its operation subdirectories, preserving the relative artifact paths
and identical store/profile identity. This is continuation of the same protected
local lineage, not permission to import a foreign catalog or relabel identities.

Use the existing recovery copy discipline, reduced to this selected store:

1. The root manifest lists exact relative ordinary files/directories, sizes and
   hashes. Validate ordinary paths, bounds, no unexpected aliases/sidecars, and
   absent `WITHDRAWN` before copying.
2. Acquire the original `owner.lock` with the existing Windows lock mechanism.
   Do not open original SQLite through mutable product code.
3. Create fresh destination paths and stream each manifest file once with
   exact digest/size checks and fsync/readback. Copy the lock byte through its
   held handle. Retain all existing operation state, including failed rows.
4. Verify source bytes remain unchanged, then release the original lock.
   Only the new copy is opened using unchanged `LocalCatalog.open`.

This is a small manifest-driven copy helper, not a duplicated admission history
validator. It must not hardcode the earlier recovery's three-operation census or
delete failed evidence. No original 2,852 evidence files or producer export need
be recopied/read merely to admit the successor.

## Bundle preparation and exact dependency binding

Inputs are the successful consumer run's exact bundle, immutable prepared request
and selected expected theorem name. The outer root selection pins their hashes,
source snapshot, controller and native artifacts. Before parsing, enforce bounded
bytes/depth/number tokens using the existing parsers. Lean JSON object order is
not Python evidence canonical order; parse the pinned bundle with the bounded
owner-output reader, then canonicalize **new evidence envelopes** with
`ordinary_evidence.canonical_json`. Do not rewrite the bundle or its evidence.

Preparation steps:

1. Require the exact successor bundle schema/fields and profile/context/basis
   equal the selected parent. Require exact selected nonempty target names;
   all targets must be absent from the parent and present among new units.
   Numeric statistics are bounded claims; unit/target/import counts are checked
   against actual data, not used as authority.
2. Obtain actual parent bindings through `catalog.context(parent)` on the new
   protected copy. This authenticates four selected chunks and 3,622 names;
   it does not read every theorem proof evidence document or recheck the library.
3. Reconstruct the supplied correspondence map from the pinned prepared header
   and group rows (or a separately pinned controller-authored map derived at
   preparation). Validate every advertised bundle boundary name/ID against both
   that actual prepared map and the accepted parent binding. Reject duplicates,
   malformed names/IDs and conflicting identities. A saved bundle's labels alone
   cannot supply mathematical or controller authority.
4. Iterate raw new units in bundle order. `inspect_unit` derives the exact
   external serialized references and expected export names. For each external
   name, use its exact selected accepted boundary identity or an earlier new
   unit's derived export identity. **Do not silently fall back to any same-named
   parent declaration absent from the authenticated correspondence.**
5. For each unit, form the existing V1 evidence envelope with exactly those
   sorted direct imports, canonicalize it, then `read_evidence` the exact bytes.
   Compute `export_id(profile, unit_id, name)` only for genuinely new names.
   Refuse any name already in the parent or an earlier unit, even if it looks
   equivalent. A duplicate existing result needing correspondence should be
   returned as such, not relabeled as newly generated mathematics.
6. Write fresh numbered evidence and `units.json`, retaining exact byte hashes,
   units/names/node counts and the batch request identity. No theorem proof body
   is omitted from a new unit. Per-unit evidence imports exclude any incidental
   literal-stage support present in the bundle lookup map.

The first driver should admit **one bounded batch**: at most 1,024 new units,
65,536 generated names, 2,097,152 total encoded nodes, 8 MiB per evidence document
and 64 MiB aggregate evidence/native-unit input. The real fixture is expected to
be much smaller, but that must be observed. If it exceeds the batch envelope,
refuse before native spending; do not implement multi-batch scheduling speculatively.
Only compact identity/name summaries and the current batch need remain resident.
Release the parsed owner bundle and preparation temporaries before native launch.

## Existing worker and catalog event

After exact source review and fresh finite root selection:

1. Call unchanged `reserve_extension(parent, exactEvidenceBytes, ...)` once on
   the copied catalog. It independently reparses evidence, resolves exact import
   identities and rejects overwrites. Reservation is not acceptance.
2. Obtain the real parent `context` and write the existing three-field native
   import plan (`basis_module`, `root_module`, `modules`). Pass the new exact
   `units.json`, reserved root and exclusive grant artifact/report destinations
   to the unchanged worker's `extend` mode under the existing supervisor.
3. The worker restores the retained four-root local snapshot chain, decodes new
   units, calls the existing checked extension boundary, writes only its actual
   delta artifact and actual generated inventory report. It does not rerun the
   old basis or the accepted 2,852 units. This is initial local snapshot loading,
   not a claim of constant-cost arbitrary cold onboarding.
4. Require clean terminal supervision, exact process closure, bounded artifact,
   unchanged selected input hashes and exact report binding: module/root, parent,
   extension kind, new unit count, actual names in expected order and artifact
   size. Only then call the existing private `_commit_checked(grant)` seam.
5. On failure, preserve logs/input/output/reservation and call `abandon` only
   after worker cleanup. No automatic retry, grant renewal or cap increase.
   If commit outcome is uncertain, use existing reopen resolution, not replay.
6. Close/reopen the new catalog once and confirm exact successor target identity
   and unchanged parent bindings. Reverify original catalog manifest unchanged.

The controller should save a compact outcome recording selected input hashes,
parent and new root, new target symbols, request/evidence identities, actual
report/artifact hashes and full known controller/worker cost. This does not need
a second general-purpose ledger or another original-history audit.

## Expected evidence and limitations

Decision-changing success requires actual ordinary source use **and** independent
checking of the substantive successor over the real parent. Neither compilation,
a theorem-shaped stub, prepared evidence nor a copied catalog is a substitute.
The native operation also validates loading the final recovery snapshot without
adding a redundant standalone snapshot-load experiment.

Useful source/control review focuses on the new seam: wrong boundary identity,
same name absent from the prepared correspondence, duplicate/overwriting output,
per-unit exact-import census, out-of-order new dependencies, and no promotion
after a failed/unclean worker. Existing passing catalog/codec suites are not
automatically rerun.

All creation, failed preparation, lookup-map setup, copied storage, snapshot load,
authoring and native checking costs remain visible. Success would establish a
real reciprocal compatibility path, not novelty or independent discovery, a
growth advantage over an equally optimized local library, portability, a public
hostile-input sandbox or final v5 deployment readiness.
