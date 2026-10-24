# Ordinary reference bases: independent semantic audit

2026-10-24. `reference_soundness_audit`; canonical guard passed. Source/theory
review only: no native compilation/import, experiment, mathematical owner open,
protected registration, Git mutation or package change. This checkpoint owns
only the correspondence argument and its actual environment-view premises;
producer accounting and snapshot-file controls have separate reviewers.

## Decision and current status

The strict reference-base route is a useful, sufficient architecture: retain an
approved original library for ordinary Lean authoring, independently warrant its
selected mathematical closure, and match the actual imported representations to
that warrant. It need not regenerate the library or require a cryptographic
certificate for each consumer. One-time cold checking and selected-context
loading remain costs, not solved away by this route.

The first matcher draft had a genuine semantic gap: inspecting the exported
elaborator lookup does not inspect the environment the kernel will check against.
The native author is correcting this and the separate public-basis relation.
The final changed-source review below now passes for matcher `5120d6bb`; no
compile/runtime clearance, protected registration or mathematical acceptance
follows from that source/theory disposition. The conditional argument below
specifies the sufficient relation; it is not a full kernel-refinement proof.

## Two consequential findings, and one corrected concern

1. **Private basis correspondence does not imply public basis correspondence.**
   The selected imported private and exported artifacts can carry different
   records. The fixed basis must be matched in every representation used for
   later selected checking or public access. A correct private definition does
   not authenticate an incorrect public definition with the same name/type.

2. **`setExporting` does not select the kernel environment.** In the pinned
   `Lean/Environment.lean`, `Environment.toKernelEnv` returns `env.checked.get`
   (lines 648–650), independently of `isExporting`. `Environment.find?` consults
   the visibility-selected base (lines 839–842), while `setExporting` only changes
   the visibility flag (lines 652–657). `finalizeImport` separately constructs
   private and public maps. Therefore matching `(env.setExporting true).find?`
   is not enough to establish the premises of a later `addDeclCore` call. Match
   the actual `publicEnv.toKernelEnv` records as well. The same direct comparison
   should cover private frontend and private kernel records rather than relying
   on an unverified alignment invariant.

3. **Correction: the actual fixed-basis source comparison does bind theorem
   proofs.** `BootstrapProbe.inventoryRow` in the selected
   `ordinary_lean/BootstrapSupport.lean`, line 629, serializes the normalized
   theorem proof DAG and singleton `all` metadata. `Export.compareSourceBasis`
   calls that function. It is not the weaker theorem-interface branch of
   `OwnerRebind.matchBasisRow`, whose kind-2 branch expects an empty detail row
   and only matches the type/arity. Do not conflate these two contracts. The
   source-based concern that the fixed private seed comparison omitted every
   theorem proof was withdrawn after independently reading both definitions;
   it is not an unresolved requirement to add another seed proof checker.

These findings were sent directly to the native author and root before another
build. They require neither a large experiment nor a new foundation policy.

## Sufficient relation

Let `F` denote the already selected checked seed interpretation, `K` a currently
validated protected accepted context, and `U` a finite dependency-ordered set of
complete accepted ordinary units. Let `Dpk` and `Dpf` be the actual private
kernel and frontend maps, and `Dek` and `Def` the actual exported-import kernel
and public frontend maps. These are four lookup views, not four mathematical
foundations. A native report cannot assert their correctness in place of
performing the comparisons.

The registration argument requires:

- **Current mathematical warrants.** Each selected complete unit is really
  warranted by `K`; its authenticated evidence, original descriptor, complete
  generated inventory, ordered import SymbolIDs and exact output SymbolIDs are
  those of that warrant. Mere custody or matching an advertised name is not
  enough. Every nonbasis private dependency is included.
- **Fixed-basis interpretation.** `Dpk` satisfies the existing selected
  seed-normalization correspondence. Full original records in the other used
  maps match the corresponding private records, except the narrowly authorized
  theorem erasure. Permitted axiom/quotient records retain exact names, ordered
  universes, types and primitive payloads; no additional axiom is admitted.
- **Private realization.** Every original record of each unit in `U` matches in
  full in `Dpk` and `Dpf`, modulo only the established expression-metadata
  removal. All generated records are included. The genuine prior checking
  warrant supplies the complete generated census; a parser alone does not.
- **Public realization.** For every selected reusable whole unit, compare both
  `Dek` and `Def` against that same warranted inventory. Computational records
  must be full and exact. Only an actually singleton theorem with original
  `all = [own]` may become a safe axiom-shaped handle with its exact name,
  ordered universes and type. Its proof warrant remains the full private
  theorem, not the handle.
- **Semantic closure.** Follow actual full types, values, projections and
  generated recursor/group metadata. A full theorem contributes its proof
  references; an erased theorem contributes its type references. Include the
  selected foundation's implicit literal and primitive support. Do not invent
  semantic edges from definition/theorem/opaque `all`, whose documented
  nonkernel status is already a selected-runtime premise.
- **Lifetime.** Exact runtime/support, complete explicit artifact map and copied
  part bytes remain the selected ones during matching and later use. No ambient
  name-search fallback, saved-report registration, changed owner context or
  silently changed artifact can supply a warrant. Local immutability/OS control
  remains a stated trust premise; matching lengths is not content authentication.

The sufficient public domain can be the least whole-unit closure under the
**union** of dependencies of `Dek` and `Def`. Match both maps on that domain and
record both projection classes. Requiring the two classes to be identical is
unnecessary: independently warranted full and erased theorem representations
can both be sound. If either view is full, retain its proof dependencies.

This conservative common domain may refuse a library whose kernel retains a
proof-only helper unavailable publicly. That is a support-profile limitation,
not a reason to omit the kernel check. Separate per-view closure domains could
be a later justified extension if an actual useful library needs them; they
are not necessary to complete this small sufficient implementation.

## Why this relation suffices, conditionally

Induct over the genuinely checked complete units in `U`. The existing warrant
establishes each descriptor and generated inventory under `F` and the resolved
prior identities. Exact private correspondence, preserved computational records
and closed dependencies give those same selected meanings in the original
library. Unrelated ambient declarations are not automatically admitted to the
relation.

For each public view, a full computational record inherits that interpretation.
An erased theorem handle is interpreted by the already checked proof of its
exact type, not by a fresh axiom. This is a conservative presentation of a
proved result. Full theorem records retain their checked proof and support;
the argument does not assume all theorem bodies are universally irrelevant to
every native operation. Closure ensures that conversion cannot silently reach
unmatched computational support. Foundation literal/primitive semantics and
the selected Lean checker/importer are explicit premises of that claim.

Consequently, a delta decoded using only the validated public domain, `F`, and
previous new outputs can be checked against the matched actual kernel maps.
Both required checking views, exact new generated inventories and fresh
written-artifact rereads remain necessary. Later extraction and strict receiver
admission remain the mathematical acceptance boundary; ordinary source/compiler
success is not substituted for that boundary.

This is a conditional simulation/conservative-extension argument, not a
machine-checked proof of Lean's kernel, importer, codec or cryptography. In
particular, it assumes the preserved seed-normalization correspondence, complete
generated checking, correct bounded codecs, hash identity, current protected
local state, and unchanged selected implementation support. It does not establish
hostile-binary safety or a worldwide discovery/growth theorem.

## Controller request boundary inspected

`reference_request.py` (hash below) obtains the actual owner's validated context,
checks the fixed inventory hash and all 581 basis bindings, authenticates every
bounded portable evidence item, and requires each derived exact output SymbolID
to occur in the current context. `portable_evidence.read_evidence` binds the
canonical complete unit and exact external-reference/import census into its
UnitID. The planner then resolves every nonbasis import within its selected
private units, rejects conflicts/cycles, and binds exact requested target pairs.

Subject to current protected catalog semantics and collision resistance, those
conditions justify passing *already warranted* complete units to the matcher
without another proof replay. Snapshot/support strings in that request are only
labels: the later live controller must authenticate their actual artifacts and
support, retain owner serialization, validate the live report and commit the
reference last. The planner itself registers nothing and cannot extend a
context's lifetime. Its use of the full selected bundle is conservative, not a
claim to have minimized the selected proof closure for each target.

## Minimal decision-changing evidence after source review

Use one small original-library workflow, not the retained 2,852-unit campaign.
The decisive cases are exact computational reuse; private basis correct/public
basis wrong; frontend correct/checker map wrong; complete generated inventory;
erased theorem with private-only proof support; and full theorem in either used
view requiring that support. Controller controls should separately challenge
unwarranted exact-looking evidence, wrong context and changed bound snapshot.
Where constructing divergent native maps is deliberately synthetic, say so;
do not turn such a control into a claim about ordinary compiler output.

## Inspected identities

All paths are below the canonical project root. These identify reviewed source,
not a compiled support selection. The matcher is being revised and requires an
addendum against its actual final bytes before source clearance.

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_baseline/OrdinaryReferenceBase.lean` first draft | `68d1213c48608b16457a7e853a4e18426449425939f2bdf9c286d91a30109050` |
| `software/v5/ordinary_baseline/reference_request.py` | `a4cadb4beb75bdf86b7314a2c05e301cbbafd42da8500ccd524c82c7a7503923` |
| `software/v5/ordinary_lean/BootstrapSupport.lean` | `8a5771cc9f4e51cc0072959174bdc3a917bb0684b3dfdc8cdda2318bb8fd1bb0` |
| `software/runtime/lean-4.34.0-windows/src/lean/Lean/Environment.lean` | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |

No result here accepts a reference base, new theorem, release package or full v5.

## Final changed-source disposition

Independently read the complete revised `OrdinaryReferenceBase.lean`, SHA-256
`5120d6bb7939e32b2c2cd45981dde015d9e041fd9d7a05e11cc453ce5fd3b30a`.
Disposition: **PASS for the selected conditional semantic correspondence
source design; no remaining semantic blocker found in this scoped review.**
This does not select a native build/run or attest successful compilation.

The changed source resolves both findings:

- `matchPrivate` independently requires exact full warranted rows in the actual
  private frontend and actual private kernel maps. Their equal original encoded
  semantics make the existing private reference scan sufficient for both.
- `matchBasisViews` anchors on `privateEnv.toKernelEnv`, whose fixed normalized
  seed comparison has already succeeded. It separately matches private frontend,
  public frontend and exported-import kernel records. The helper no longer
  imports/calls `OwnerRebind.matchBasisRow`. Authorized foundational axioms match
  exact original signatures; quotient primitives additionally match the exact
  primitive-kind tag. The other records use exact original inventories with
  only the selected singleton-theorem public exception.
- `matchPublic` requires both actual views for every selected whole unit, scans
  their union of semantic references, and records `projection` and
  `kernel_projection` separately. It does not silently infer one from the other.
  Private generated-group completeness remains the actual prior warrant's
  premise, not a claim that this matcher re-proves it.
- Snapshot replay remains explicit-map, with cleared ambient search paths and
  actual private module-census checks. No declarations are added and the result
  explicitly reports zero newly checked units; all identity strings remain
  controller-authenticated labels rather than native hash verification.

The full fixed basis is deliberately compared, not merely the basis names
directly appearing in target types. This retains the selected literal/primitive
foundation and avoids allowing unmatched implicit computation through a public
basis row. Fixed-basis record comparison is additional bounded work and is not
included in the nonbasis `private_scan_nodes`/`public_scan_nodes` counters.
Those counters must not be advertised as total operation cost; the finite outer
execution envelope and full measured work remain separately charged.

Integration obligations are unchanged: authenticate exact snapshot/support
bytes, keep current owner warrants through the live operation, validate both
projection fields and complete report membership, commit the protected reference
last, and use the same explicit artifact resolution in later delta checks and
ordinary authoring. The actual original-library workflow and changed-view
controls remain decision-changing implementation evidence, not a reason to
repeat the large prior admission campaign.
