# Checked receiver snapshots as ordinary Lean libraries

2026-10-23, `ordinary_api_flow`; source/theory only. Canonical guard PASS.
No native artifact import, test, build, network, state opening or Git action.

## Answer and normal-user consequence

**Yes: genuinely committed CHECKED snapshots retain complete theorem proofs. No:
the current files are not drop-in modules for an ordinary Init/project import.**
The missing endpoint is a compatible checked-library view, not recovery of erased
receiver proofs. Do not conflate these artifacts with scratch authoring axioms.
A useful eventual command is “use these accepted results in my approved project”:
produce/cache a compatible proof-bearing module once, then use normal imports,
editor and tactics. It should not require reauthoring already accepted proofs.

## Proof completeness and exact parent

`CheckedExtension.lean:allowedDeclaration/checkBatch` accepts theorem declarations
with values, calls actual `addDeclCore ... (doCheck := true)`, rejects added
axioms/unsafe/partial records, and returns actual kernel-generated ConstantInfo.
`OriginalDecl.lean:inventoryRow` includes theorem/definition/opaque values in the
exact inventory comparison; the checker is not merely validating theorem types.
`LocalSnapshot.lean:writeCheckedBatch` stores `checked.added` directly as module
constants. It neither substitutes axioms nor calls a public-view proof eraser.
`BasisSnapshot.lean` similarly stores actual checked fixed-basis constants;
the foundation's explicitly permitted axioms remain the foundation, not new proofs.

`OrdinaryWorkflowWorker.extend` restores the selected full parent chain, decodes
new units against its names, checks the batch and writes one exact added delta.
The controller binds grant/parent/module/ordered units/report and a clean live
worker event before protected catalog promotion (`ordinary_admission.py:565–652`).
`portable_catalog.py:491–527` validates lineage, artifact pins and parent module
bindings, refusing shadowed names. These are owner warrant/provenance conditions;
a checksum or a copied CHECKED report alone does not establish them.
The five inspected native sources match the current installation manifest;
this source comparison did not deserialize any `.olean`.
Contrast: `OwnerConstruction.lean:207` deliberately constructs an `axiomDecl`
for an acquired theorem interface and checks only its type's well-formedness.
The authoring worker's `OrdinaryProducer.olean` may therefore depend on scratch
assumptions; it is not the receiver's checked snapshot or a proved-library export.

## Concrete interoperability blockers

1. Snapshots use `ModuleData.isModule := false`, one exported parent import,
   and one full `.olean`. Lean 4.34 `Environment.getData?` uses that same complete
   part at every visibility level: proofs are not hidden in missing private files.
   But `Environment.importModulesCore:2115–2119` explicitly rejects a legacy
   non-`module` import from a new `module`. Current `assemble_source:227` begins
   with `module`; simply placing these files on its search path cannot work.
2. Even a legacy source implicitly imports Init unless it says `prelude`
   (`Lean/Elab/Import.lean:29–38`). The snapshot basis redefines Init names.
   `Environment.finalizeImport:2334–2344` merges only compatible theorem/axiom
   views via `subsumesInfo`, not duplicate definitions/inductives, even identical
   ones. Thus normal Init plus the copied basis is not a harmless name union.
3. Storage is `operations/<id>/chunk.olean`; module names are
   `DMKNLocal.r<root>` with explicit parent imports. A search-path view needs the
   whole chain at matching module paths. Changing filenames/module labels does
   not rename the encoded declaration names or resolve project collisions.
4. `entries := #[]` and `extraConstNames := #[]` intentionally omit elaborator
   metadata, attributes/instances, notation, documentation and executable IR.
   Constants/proofs remain, but normal automation, pretty syntax or runtime
   evaluation is not thereby restored. Original private/generated names persist;
   there is no reconstructed source alias/visibility map or usability guarantee.

A closed legacy `prelude` view of an authenticated chain is plausible local
plumbing, but needs verification and lacks normal Init/project support. Do not
present that restricted workaround as the ordinary-project endpoint.

## Smallest principled bridge, if separately selected

Reuse the real checked declarations/retained inert evidence and existing bounded
closure/checking machinery. Select targets and one approved compatible project.
Bind the reached boundary to exact target records/IDs and the same literal/axiom
policy, not merely familiar names; refuse incompatible or partial groups.
Import that actual project's foundation instead of copying the receiver basis.
Add only the missing complete declarations, with real kernel checking against
that target environment and an exact output/statement mapping. Initially refuse
collisions; any later namespace rewrite must consistently rewrite all references
and be rechecked. Renaming a module or trusting import success is insufficient.

Emit a proper new-system module using Lean's normal writer/visibility machinery,
including matching public/server/private parts where required; do not flip the
old header bit. Keep proof-bearing private records available for independent
inspection/export. Define explicit public targets, private helpers and a small
optional ergonomic facade; do not pretend discarded notation/attributes exist.
Keep provenance, selected runtime/foundation, targets and artifact closure bound.
Local trusted output can use normal compiled-library trust; peers seeking the
commons' independent assurance still receive inert evidence and check it locally.
Neither a package hash nor a native import rechecks downloaded theorem proofs.
## Cost and decision gate

The current cold snapshot import loads the whole accepted chain, not just one
target. A project bridge should reuse exact existing project dependencies and
cache its selected missing closure/module; do not repeatedly replay the receiver
history or fetch/build a whole library by default. Proof/module load, boundary
comparison, new checking, output storage and normal-project imports all count.
The next evidence, only after source selection, is one existing accepted theorem
and dependency used through an ordinary default project import, with proof-value,
collision/foundation refusal and private-visibility checks. No new mathematics,
certificate campaign or general project audit is needed. This note selects no run.
