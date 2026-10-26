# Exact-name native admission

Source-only successors under CONTRACT.md. The three files were read from the
actual `intake-progress-package01/distribution/package/installation/lean-src`
and their predecessor hashes checked before editing. All predecessors remain
unchanged. No compiler, Lean, test, owner, database or Git operation was run.

The source argument is in `ordinary_intake_progress/PRIVATE-NAME-COMPATIBILITY.md`
(`fe270247...`). The native receiver needs exact-name checked kernel state; it
does not need the frontend async trie that identifies different private origins
by the same user-facing suffix. Diagnostics from the failed run remain failures.

## One policy loop, two fixed checked adapters

`CheckedExtension.checkBatchCore` is private. It retains the original checks and
their order: finite bounds/parent premise, allowed declaration policy, exact-name
overwrite rejection, declared inventory completeness, closed grounded references,
actual checked addition, complete generated-record equality/safety, and final
stage-two name census. The only abstract operations are state projection to
`Kernel.Environment` and checked addition; both are supplied solely by these
two fixed source wrappers:

| Entry | Parent/result environment | Fixed addition |
|---|---|---|
| Existing `checkBatch` | `Environment` | `Environment.addDeclCore ... (doCheck := true)` |
| New `checkKernelBatch` | `Kernel.Environment` | `Kernel.Environment.addDeclCore ...` |

The latter API has no unchecked switch. There is no public callback, mode flag,
peer-controlled adapter or unchecked route. `private` prevents ordinary API
exposure; it is not a sandbox against a hostile in-process caller. The same
protected-parent and trusted-controller premises still apply, and `quotInit`
alone proves no warrant.

Existing `CheckedBatch` and `checkBatch` signatures and returned frontend
environment are preserved. That path keeps its actual public/private visibility,
extension, realization and async state. The distinct new `KernelCheckedBatch`
has `environment : Kernel.Environment`, `added : Array ConstantInfo`, and
`unitsChecked : Nat`. It contains only the actual successful result, not a
serialized acceptance grant. No kernel state is coerced into a frontend wrapper.

## Native persistence and routing

`LocalSnapshot.writeCheckedRecords` is the one private serializer. Its only two
callers pass the actual result of the corresponding fixed checked entrypoint.
All existing path/freshness, safety, output-size and duplicate checks are retained.
`ModuleData` still contains exactly the ordered checked records and their full
names, its one exact parent import, `isModule=false`, and empty extra names and
extension entries. It neither dumps unrelated stage-two records nor accepts
caller-supplied `ConstantInfo` as checked evidence.

The existing `checkAndWriteChunk`/`WrittenExtension` interface stays available.
New `checkAndWriteKernelChunk` takes `Kernel.Environment` followed by the same
parent-module, new-module, decoded-unit, output-path and optional limits arguments.
It returns `WrittenKernelExtension`, with the existing `SavedChunk` metadata and
the actual `Kernel.Environment`. Restoring protected snapshots still uses the
unchanged `restoreLocal` path and its metadata checks.

Only `OrdinaryWorkflowWorker.extend` changes routing: after the unchanged protected
restore/decode steps, it projects the parent with `toKernelEnv` and selects
`checkAndWriteKernelChunk`. It consumes only the returned chunk metadata for its
unchanged report. Basis initialization, source export, authoring/rebinding and
private/public reference-module APIs remain on their previous paths. There is
no module-layout change or new public CLI option.

## Evidence still required

The proof obligation is preservation of the existing acceptance loop under the
two fixed adapters, followed by exact snapshot serialization. A finite native
control should use different private full names with equal normalized suffixes,
a private/public pair, and genuine references to each exact constant; reject
duplicate full names, invalid proofs and wrong/generated inventories; restore
snapshots and check a further extension. Exercise the unchanged frontend path
with a noncolliding declaration. These are prepared by the separate controls
owner; this note is not execution authority or a test result.

All eight receiver module names and all existing caps stay unchanged. New native
support bytes nevertheless change implementation identity and require separate
build/package/adoption evidence and fresh-state policy. No old owner is silently
migrated, no large Std retry is selected, and no accepted artifact is recovered
from the rejected diagnostic run. Compatibility and useful mathematical growth
remain distinct from this source task's completion.
