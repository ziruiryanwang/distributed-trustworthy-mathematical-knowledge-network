# Ordinary local snapshot implementation checkpoint

2026-10-22. `lean_persistence_boundary`; root-selected source only.

**Later source continuation:** root selected and the author implemented
`WrittenExtension { chunk, environment }`. `checkAndWriteChunk` now returns the
actual checked environment alongside its file description, so the next local
batch need not deserialize a snapshot. The private writer remains private and
receives only that call's real `checkBatch` result. Current source hash and focused
unexecuted controls are recorded in `SNAPSHOT-CONTROLS-PLAN.md`; the initial-source
hash and former return-type limitation below are preserved historical context.

Implemented `software/v5/ordinary_lean/LocalSnapshot.lean`, SHA-256
`bc0f305734ee36268c5e4e65e84c5db4e71fa9d1c9a3089e84bc447959dcdfc2`.
No compilation, runtime, test, basis replay, product edit or Git operation ran.

## Implemented seam

- `checkAndWriteChunk` invokes the actual existing `CheckedExtension.checkBatch`
  and passes that result directly to a **private** writer. The writer persists
  exactly `checked.added`, not all stage2 constants, with one recorded parent
  import, original constant names/metadata, no extension entries and no IR.
- `LocalImportPlan` contains a finite ordered one-parent chain, explicit basis
  and root names, exact protected local paths, byte lengths and constant counts.
  Missing/interchanged parents, extra unrelated branches, duplicate module/path
  entries and quota/size failures are refused before native deserialization.
- `restoreLocal` builds a complete explicit `ImportArtifacts` map, temporarily
  empties the global Lean search path, uses no plugins, `loadExts := false`,
  trust level0 and private-level single-part imports. It restores the old path
  on success/failure; concurrent path manipulation is excluded.
- Postrestore checks bind the exact module order/census, each embedded import,
  empty extension/IR-name metadata, counts and initialized quotient state.
- Output paths must be fresh; ordinary-file and single-link/size checks reject
  unexpected output kinds. Failure after writing leaves uncommitted bytes for
  the controller to account for, not an accepted root.

## Deliberately still controller obligations

This is **internal plumbing**, not a public peer API or standalone safe `.olean`
reader. Before import the root controller must authenticate every selected file
digest and the exact native profile/catalog lineage, enforce canonical protected
paths/ancestor no-redirection, hold storage stable, observe withdrawal and own
fresh process/output grants. Metadata checks do not authenticate bytes.

`parent : Environment` must actually be the independently warranted environment
named by `parentModule`; accepting arbitrary caller environments would be unsound.
The only supported basis comes from the separately selected exact initialized
seed path. No basis writer, generic basis callback or `import Init` promotion is
implemented here. Quotient-state=true alone is not proof of foundation identity.

Current `checkAndWriteChunk` returns `SavedChunk`, a description of the fresh
file, not the new in-memory environment. Cross-process use restores the accepted
chunk after catalog commit. For same-process chaining without a reload, root can
select an internal result pairing the actual checked environment and SavedChunk;
do not expose the private writer or add a caller-created CheckedBatch input.
This checkpoint does not claim that optimization already exists.

## Next verification

Root owns the next finite compile/round-trip selection. Target successful exact
delta writing and fresh-process restore, a second delta not duplicating previous
stage2 records, and malformed/incomplete local plans. The full protected catalog,
real basis initialization, evidence acquisition, owner bridge and reciprocal
workflow remain necessary before product adoption. Existing conditional admission
tests are not substitute evidence for those steps.
