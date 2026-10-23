# Concrete reverse seam: checked portable units to a normal Lean module

2026-10-23, `project_hook_design`. Source/theory only; guard PASS. No code,
build, import, experiment, owner opening, state change or Git operation. This
refines ORDINARY-PROVED-LIBRARY-EXPORT-DECISION without reopening its broad audit.

## Selected smallest candidate

**A local, cached, Init-only proof-bearing module builder**, not a snapshot
renamer or arbitrary project adapter. Given locally warranted target ExportIDs,
collect their complete selected portable-unit closure down to the fixed basis,
recheck that closure over the approved installed Init, and use Lean's module
writer. Keep original names; refuse collisions. Make the selected closure's
records publicly available initially; do not reconstruct lost notation or aliases.

Use inert full evidence rather than loading the receiver's complete snapshot
chain. This avoids native ancestor-module loading and re-export census. Current
`catalog.context` still checks/materializes bounded local lineage metadata and
artifact pins; selected proof closure can itself be large. Neither cost vanishes.

The existing authoring shortcut is unsuitable: `OwnerConstruction.demand`
inserts an `axiomDecl` for a theorem interface. This builder must instead decode
the original theorem value and use unchanged `CheckedExtension.checkBatch`.

## Exact reuse points and required new glue

All project source paths below are under `software/v5/ordinary_lean/`; Lean API
paths are under `software/runtime/lean-4.34.0-windows/src/lean/Lean/`.

| Step | Existing concrete mechanism | New glue / constraint |
|---|---|---|
| Select warranted inputs | `portable_catalog.py:PortableCatalog.context`; `ordinary_contribution.py:contribute_source`'s `evidence` callback pattern; `transport/ordinary_acquisition.py:OrdinaryStore.get_locator/get_evidence` | Capture the actual eligible owner context once. Fetch bounded exact units, not prepared theorem-interface groups. |
| Bind identities/closure | `portable_evidence.py:read_evidence`; `ordinary_semantics.py:export_id/basis_symbol_id`; admission `_plan`'s direct-import/collision/topological checks | Reuse these checks against an explicit foundation boundary. Calling normal preflight against the full receiver context would mark every accepted unit reused and supply no rebuilding order. |
| Construct an Init module environment | `Environment.lean:Lean.withImporting`, `importModulesCore`, `finalizeImport`, `Environment.setMainModule` | Fresh environment from installed Init, never copy or change the old snapshot header. See exact visibility choice below. |
| Check fixed boundary | `OrdinaryExport.lean:Export.compareSourceBasis`; `BootstrapSupport.lean:BootstrapProbe.inventoryRow/screen` | Direct lookup of all 581 pinned basis records. Use `Export.SourceRecords` with empty grouping, not `Export.indexSource`'s whole-environment census. |
| Rebuild exact declarations | `OriginalDecl.lean:DeclCodec.decodeUnit/expectedNames`; `CheckedExtension.lean:checkBatch` | Decoder allows only fixed-basis names and exact ordered selected-unit outputs, not every imported Init name. |
| Expose/write | `OwnerRebind.lean:exposeAdded`; `Environment.lean:mkModuleData/writeModule` | Expose actual generated recursors/prefixes; write a fresh normal module, with the writer's real file parts. |

The custody module's full path is `software/v5/transport/ordinary_acquisition.py`.
This is one small controller collector plus one native builder, reusing current
canonical codecs/checker and the existing one-operation supervision, not a new
checking language, certificate, service, scheduler or project package manager.

## Identity preservation is stronger than a successful Lean recheck

For every fetched unit U, reparse exact canonical bytes and bind S, all direct
imports and the complete unit to its UnitID. For every selected exported name n,
require the selected receiver context to warrant `ExportID(S,U,n)`; verify every
reached import against that same context. Custody possession/locator hashes alone
are not acceptance. Follow each nonbasis import to its exact unit, memoize units,
include every group member, reject cycles/conflicts and enforce aggregate caps.

In the target environment, require the pinned semantic/foundation descriptors,
same supported Lean/literal interpretation, and actual fixed-basis correspondence.
`Export.compareSourceBasis` compares the pinned foundation inventory (including
theorem values and allowed axioms/quotient primitives) against installed private
records; its existing regular-height normalization is part of that comparison,
not original-binder/implementation-byte identity. Do not replace it with names,
type equality, `quotInit`, or `OwnerRebind.matchBasisRow`'s authoring theorem view.

Permit **only** that verified fixed basis as an existing boundary in the first
endpoint. Every other reached external name must be rebuilt from its complete
exact selected unit, even if ordinary Init happens to contain that name; such a
collision refuses initially. Reject all selected output collisions, including
partial generated groups. Never broaden the boundary merely to make a proof pass.
In particular imported `sorryAx` or other unselected Init constants are not legal
decoder references; existing `CheckedExtension.requireName` also rejects sorry.

Then `checkBatch` kernel-checks each real declaration with `doCheck := true`,
compares every actual generated full inventory row, and refuses extra/missing
records. The original unit descriptor round trip, exact import IDs and actual
inventory comparison preserve the original ExportIDs; a proof valid under
differently interpreted same-named constants would not meet these premises.
No new axioms, theorem stubs, name rewriting or arbitrary equivalence claims.

## Precise module/visibility construction

Use a fresh import array containing the approved standard `Init`, exported and
non-meta. Within `Lean.withImporting`, run `importModulesCore` with
`globalLevel := .private, isExported := true`, then public `finalizeImport` with
`level := .private, isModule := true, loadExts := false, leakEnv := false` and
trust level 0. Set the fresh intended module name with `setMainModule`.
This uses the source API's separate loading-level/module parameters:
private Init records are available for boundary comparison and conversion, while
a genuine module header and public/private base maps are constructed together.
It is **not** changing `isModule` on an already-written legacy snapshot.

Because private-level import skips the new-system legacy-import prohibition,
the bridge must explicitly require every imported Init closure `ModuleData` in
the finalized header to be `isModule = true`. Import paths are fixed to the approved local runtime, with
no peer binary modules or plugins. Full imported-Std artifact authentication is
still the existing owner-trusted-installation premise, not a hermetic manifest.

`addDeclCore` adds declared records to both frontend visibility maps; generated
recursors may need the existing `exposeAdded` repair. Inspect both views for every
selected target. Initial policy retains full theorem/definition values in the
exported view as well as the private kernel data. No custom proof erasure needed.
`mkModuleData` writes stage-two additions, not imported Init's stage-one basis.
`writeModule` emits `.olean`, `.olean.server`, `.olean.private` together; its
default IR path also emits `.ir.sig`/`.ir`. Keep/pin all produced parts together.
Do not invent `ModuleData`, omit required parts, or merely rename `chunk.olean`.

The minimal builder does not compile executable IR for newly added definitions.
Proof use and kernel reduction are the target; `#eval`, `native_decide`, custom
attributes/instances, notation and source-level private aliases are not promised.
Full-closure public records are deliberate; an abstract/minimal interface is later
work only if actual users need it. A normal project with conflicting names refuses.

**Separate visibility obligation:** private-Init rechecking alone does not show
that a plain importing consumer can resolve every public record or perform the
needed conversions. The builder must check the selected public records' referenced
basis names against Init's public view, including dependencies reached through
required transparent definitions, and refuse an unavailable public boundary. The
normal consumer check below is decisive for the selected fixture; success is not
a theorem of arbitrary-library public compatibility. Do not silently switch the
consumer to `import all`, duplicate hidden Init constants, or promote hidden basis
records merely to pass. A separately documented `import all` export profile is a
possible later alternative, not the normal-import claim selected here.

## Cheapest alternative and cost boundary

If an approved ordinary Lean package already supplies the result, use its pinned
normal import. Rebuilding the same trusted package through the commons adds cost
and is not the default. The bridge matters when discovered results exist only as
commons evidence and the user wants editor/tactic/proof reuse in a normal project.

Pay once for owner-context validation + selected evidence acquisition + Init load
+ fixed-boundary comparison + selected proof checking + module writing. Cache by
selected portable identities/closure, supported runtime/writer and export policy;
unrelated context growth need not invalidate the mathematical cache. Record the
original warranted context in its local manifest, not as a global ledger.
Against repeated context reconstruction, a benefit requires
`R * (C_reconstruct - C_cached_import) > C_build`; against already available
trusted package import there is no asserted advantage. Counts/actual cost remain
needed before claiming a practical win. No whole-library proof recheck is required,
but all selected nonboundary proof dependencies are paid once by this first bridge.

## One narrow discriminator, only after separate selection

Reuse existing accepted `CommonsPeerExample.applyFour_eq` and its
`CommonsPackageExample.applyTwice` / `applyTwice_eq` dependency closure. The retained
B-contribution reports unit `d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51`
and accepted local root `84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13`;
these saved labels are fixtures, not fresh owner authority. Root must select actual
eligible retained custody/context, not trust the report or scratch producer olean.

Build one fresh module with public targets retaining a real definition and theorem
proof. In one ordinary new-system consumer, import it alongside standard Init,
apply the exact theorem and reduce the definition. A private reread must recover
the actual theorem value and compare all selected inventories. Recompute original
portable IDs using their bound imports. Include a changed-boundary/collision refusal
before writing; add no new mathematical benchmark or certificate campaign.
Start with existing public batch caps (32 units/4 MiB/131,072 nodes); if the selected
closure does not fit, report that discriminator limit instead of silently enlarging
it. Generated-group support remains the unchanged codec/checker obligation, not
evidence from this simple workload. No implementation or execution is selected here.

Citation correction to the earlier preparation02 note: the actual basis comparison
function in OwnerRebind is named `matchBasisRow`, not `checkBasisRow`.
