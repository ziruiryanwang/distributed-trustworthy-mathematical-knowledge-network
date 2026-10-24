# Strict library baselines: preserve the library, check the correspondence

2026-10-24. `project_intake_native`, source/theory-only contract for root's
selection. Canonical workspace guard passes. No implementation, native import,
owner/catalog access, experiment, package change or Git mutation is performed.
This is a proposed architecture boundary, not evidence of implemented support.

## Decision in ordinary language

**Prefer a protected correspondence to the owner's approved original Lean
library, followed by small generated deltas. Do not first reconstruct thousands
of already installed declarations into substitute modules.**

A normal Lean user already has a library, including notation, typeclass
instances, simp registrations, tactics and compiled support. The commons should
let the user keep that library. Separately, it must establish which exact
mathematical declarations are independently warranted under the commons policy.
An original library is usable locally because the owner approves it; selected
mathematics is acceptable to the commons because its complete evidence has
actually passed strict checking. These are different permissions.

The intended workflow is:

```text
approved original library              inert exact baseline bundle
          |                                      |
          |                              strict local admission
          |                                      |
          +---- exact private/public match ---- accepted context
                              |
                protected local reference base
                              |
          new small delta imports the original library
                              |
       normal Lean project uses it; new results undergo strict admission
```

This remains strict route A. It does not select the alternative route B in which
an operator trusts additional mathematical axioms or unchecked library results.
No semantic namespace, foundation, SymbolID, UnitID or ExportID is changed.
Different machines may have different local artifact/reference-record IDs while
sharing the same exact portable mathematical identities.

This supersedes the reification-first consequence of
[the previous bottleneck note](ORDINARY-NEXT-RELEASE-BOTTLENECK.md), not its
historical evidence. Its companion
[baseline intake contract](ORDINARY-BASELINE-BUNDLE-CONTRACT.md) owns inert input,
batching, partial outcomes and protected-root continuation. This note owns the
producer and the missing ordinary-Lean realization boundary.

## Why acceptance alone was not enough

Existing admission has already checked a retained 2,852-unit closure in
1,024 / 1,024 / 804-unit batches. Its 49,499,157 portable evidence bytes and
271.15625 known inclusive admission/recovery CPU seconds, including a failure,
are useful prior feasibility evidence. They are not evidence that all of Mathlib
is supported or that cold checking is free or impractical.

The current generated-module route nevertheless has a 32-unit / 4-MiB delta
envelope, a 1,024-unit registered frontier and a 32-module chain. Splitting this
closure into 32-unit modules requires at least 90 modules. Enlarging just the
unit cap fails: installed definitions and groups currently collide; native
reports, plans, registry records, artifact quotas and supervisors have additional
limits. Bare reconstructed kernel declarations also do not reconstruct the
ordinary library's frontend extensions or executable implementation.

The practical choice is therefore not merely 32 versus 8,192 declarations. It
is whether to preserve an existing library or attempt to replace its ecosystem.
Exact correspondence preserves it and avoids redundant reconstruction. It does
not remove the original independent admission expense.

## Authorities and objects

Let:

- `F` be the unchanged checked seed and supported kernel/literal policy.
- `K` be a currently validated protected accepted context under `F`.
- `U` be a complete canonical unit, with its exact import and output identities.
- `D_private` and `D_public` be the actual imported private and exported views
  of the selected approved local artifact closure.
- `R_private` relate the complete selected accepted proof closure to exact full
  private records; `R_public` relate its selected reusable interface closure to
  the actual public records. The second domain is a subset of the first.

There are three distinct local operations:

1. **Produce evidence.** Read owner-approved local artifacts and serialize
   selected complete units. Output is an inert candidate, not accepted mathematics.
2. **Admit evidence.** Independently check it under `F` and a protected context.
   Only the existing real admission commit establishes a new warrant.
3. **Register correspondence.** Authenticate complete accepted units and show
   that the approved ordinary library realizes their exact meanings. This adds
   a local reusable representation, not a mathematical theorem or new axiom.

A peer cannot perform step 3 by supplying a report, an artifact path, an
`accepted=true` flag or an apparent matching type. A local approval descriptor
also cannot replace any premise of step 2.

## Exact correspondence rule

The relation is deliberately sufficient rather than complete. Equivalent but
byte-distinct proofs or differently named universe parameters can refuse. Do
not expand this work into arbitrary mathematical equivalence or alpha-renaming
of the established identity scheme.

For each complete dependency-ordered accepted unit:

1. Resolve its real warrant from current `K`; authenticate its complete inert
   evidence and exact output IDs. Require every mathematical import to resolve
   through `F` or the already established exact correspondence. Possession in
   custody is not a warrant. A proof-bearing dependency is not optional merely
   because it is absent from the target's statement.
2. Use the original warranted descriptor and complete expected inventory. Retain
   the existing canonical round trip and exact `OriginalDecl.inventoryRow`
   relation, which removes only expression metadata. Match actual name keys,
   kinds, ordered universes, types, values, hints, flags and generated records.
3. Require **every** expected output in the private view to be present and equal.
   Partial groups, wrong bodies, wrong recursor rules, unsafe/partial records and
   unproved axiom records refuse. Do not reconstruct the original descriptor
   from an installed nested group when the warranted original is available.
4. Check the public view separately for the derived public interface closure
   specified below. Within that closure, definitions, opaque declarations,
   inductive types, constructors and recursors require the full selected record.
   A hidden computational body or public axiom-shaped definition refuses. Private
   proof helpers outside this closure need not be public. Do not infer public
   conversion from private success.
5. Preserve the existing narrow exception for a **singleton theorem**: an exact
   private full theorem may correspond publicly either to that full theorem or
   to a safe axiom-shaped handle with exactly its name, ordered universe
   parameters and encoded type. Its warrant is the independently checked full
   proof, never the handle. The current exception requires `all = [own]` and is
   not generalized by this note. Other theorem cases require full public equality
   or a separately justified successor rule.
6. Extend `R_private` only for that complete unit's exact outputs, and
   `R_public` only after its actual public relation and closure pass. Imported
   ambient names and private-only support never enter `R_public` automatically.
   Both new-delta decoder passes permit references only to `F`, selected
   `R_public` outputs and preceding newly checked outputs.

### Private proof closure is not the public interface closure

The local reference request selects finite exact `expose_targets` (SymbolIDs,
not merely names). `R_private` covers their complete accepted unit/proof closure.
Derive the public set as the least bounded whole-unit closure starting at these
targets, using the **actual matched public representation** of each selected
record:

- A permitted singleton theorem whose actual public record is the safe erased
  handle contributes its exact type's references, not its private proof's
  references. Its full private proof and all helpers remain independently
  warranted and exactly matched in `R_private`.
- If the actual public theorem record is full `thmInfo`, retain its full proof
  references too. Do not assume all theorem bodies are unavailable to conversion
  merely because ordinary theorem application usually treats them opaquely.
- Every other public record is full: follow types, values, projection references
  and complete generated computational metadata/rule expressions. Selecting any
  output of an inductive unit includes its entire previously checked generated
  inventory and the referenced support, not just its named constructor.
- Resolve these references by exact existing accepted identities. Account for
  the fixed basis's implicit literal/primitive semantics; historical `all`
  metadata on definitions/theorems/opaques is not an invented semantic edge.
  Repeated group-internal references are visited once. Missing, conflicting or
  hidden required public support refuses.

For example, an erased public `t : T` may have a checked private proof using a
hidden helper `h` absent from `T`. `h` must pass private correspondence but need
not pass public correspondence. If a transparent definition or a full-public
theorem proof refers to `h`, then `h` is required in the public closure and a
hidden public body still refuses. This is a smaller **domain** of public
obligations, not a weaker equality for computational records and not acceptance
of abstract axiom-shaped definitions.

The live native matcher derives this projection from its actual imported view;
the controller binds its selected targets, complete private evidence, projection
classes and derived public membership to the protected registration. A caller
cannot assert `proof-only` or omit dependencies in a manifest to choose the
result. Reference identity includes the exposed target set and validated public
projection, so two interfaces over one private baseline cannot be confused.
Only complete publicly covered units become the delta collector's cut boundary.
An accepted/private-only unit is not reusable through that boundary until an
explicit public correspondence operation establishes the additional closure.

### Completeness is inherited from actual checking, not guessed from syntax

`decodeUnit` alone verifies neither a complete generated census nor every
possible semantic dependency. In particular, an inductive descriptor enumerates
types/constructors but its native generated closure can contain more records.
The prior `CheckedExtension.checkBatch` checked each expected actual row and
performed the stage-two census excluding unadvertised generated names. That
real warrant supplies completeness. Correspondence must match **all** of its
generated rows, including nested types and recursors, not only user-facing names.

The imported environment may contain unrelated declarations. It is unnecessary
to rescan and certify the entire environment merely because it contains them.
This is safe only with the restricted reference relation and exact transitive
computational semantics. Existing fixed-basis literal/primitive semantics remain
premises; an expression constant/projection scan does not list implicit literal
roots. The source import census is not a theorem that all semantic support is
explicitly represented by its edges.

Definition/theorem/opaque `all` lists must be preserved exactly, but are not
automatically extra semantic dependencies. The inspected pinned
`Lean/Declaration.lean:118-161` documents `DefinitionVal.all` as not used by the kernel;
the theorem/opaque fields refer to that comment. Mutual definitions are compiled
to ordinary recursors or `WellFounded.fix`, rather than kernel recursive
definition groups. This is a documented selected-runtime premise, not a formal
proof about the native kernel. It avoids an unjustified restriction requiring
every historical mutual-block sibling to be separately warranted merely because
its name appears in `all`. Inductive/constructor/recursor metadata is different:
it participates in the complete generated semantics and must match in full.

### Conditional assurance argument

Start with the already selected exact interpretation of `F`. Induct over the
dependency-ordered warranted units. The warrant establishes validity under `F`;
exact private full records and already interpreted dependencies establish the
same selected meanings in `D_private`. Induction over the derived public closure
then retains the full computational records' selected meanings in `D_public`.
An erased theorem interface is interpreted by its independently proved theorem,
whose private support need not itself have public handles. It is not a new
foundation assumption. Actual full-public theorem bodies retain their full
support closure instead of borrowing this erasure argument.

New delta declarations are then checked in both required imported views with
the unchanged `doCheck := true` rule, restricted reference decoding and exact
output inventories. Fresh private/public rereads establish that the written
artifact actually represents the checked result. Any public conversion failure
remains a refusal, including cases where private proof bodies permit reductions
that ordinary theorem interfaces do not.

The argument depends on the selected kernel/importer/codecs, actual protected
warrants, exact artifact correspondence, complete generated census, finite
successful execution and hash identity assumptions. It is not a machine-checked
kernel refinement proof. Existing
[installed-declaration analysis](ORDINARY-MODULE-EXISTING-DECLARATIONS.md)
derives the theorem-erasure rule and explains why module-origin hints alone do
not prove equality of the selected native record.

## What a local reference base must bind

The current approved-project selection pins paths and module names, **not all
transitive artifact contents**. It is appropriate execution approval for
extraction but is not already a semantic reference-base certificate.

The new local record must bind at least:

- The selected supported runtime, foundation/semantic identity, checking and
  correspondence support identities.
- Exact original module names, import flags and transitive import graph, actual
  resolution under a fixed ordered local search path, and all semantic artifact
  parts read by the private/public importers. The reader validates actual import
  dependencies against that selected closure, not just filenames in a manifest.
- Exact hashes and lengths of those artifacts, selected evidence unit IDs and
  output SymbolIDs, accepted expected-inventory hashes and current warrant links;
  exact expose targets, private unit closure and derived public unit/binding
  membership with its actual full/erased-theorem projection classes.
- The finite native operation's inputs and successful exact correspondence
  results; explicit private/public outcomes and complete-unit census.
- Local storage/retention references, bounds, and a record-last protected commit.

The first implementation should copy the actual approved artifact closure to a
protected immutable snapshot before correspondence import, retaining original
module names and layout. Return its exact import configuration/directories with
the reference handle and delta. It must address shadowing,
duplicate modules, path aliases, mutation and missing private/public parts.
Binding a mutable project directory name, toolchain string or timestamp is
insufficient. A saved success report is not an alternative registration path.
The protected record is local authority created by a selected live operation,
not a peer-transferable mathematical certificate.

This lifetime rule is essential: a generated delta imports by **module name**,
not by cryptographic identity. Rebuilding the user's original project must not
silently change the delta's meaning. A later normal consumer must resolve the
original imports from the exact selected snapshot and runtime, with the returned
controlled precedence, not an arbitrary ambient `LEAN_PATH`. The controller
validates that selection at use; an uncontrolled manual import resolving other
bytes is outside the correspondence warrant. Protect and pin the frontend/IR
artifact parts needed by the intended ordinary authoring lane as well as the
semantic parts. Owner permission to execute those parts remains distinct from
mathematical acceptance. No new source build is required to copy them.

Use the existing selected import policy for correspondence inspection:
`plugins := #[]`, `loadExts := false`, explicit selected runtime-first paths,
no inherited `LEAN_PATH` or peer-chosen native module. Binary parsing remains a
local approved-input/TCB boundary, not a hostile-binary sandbox.

Ordinary authoring may load the original **owner-approved** frontend metadata
and executable support under the existing cooperative local execution model.
It must use the selected original module names, not silently substitute the
bare reconstructed environment. This preserves available notation/instances/simp
registrations rather than promising to regenerate them. Plugins or elaborators
can change the authoring environment; therefore correspondence at initial import
does not authenticate whatever they later output. Extraction and final strict
admission remain authoritative for each new contributed result.

On reuse, validate current protected warrants/support and the selected artifact
bytes or the already supported protected immutable-artifact guarantee. Missing,
changed or withdrawn material refuses. Do not infer artifact immutability from
its content-addressed filename. A new package/support selection needs explicit
compatibility handling; do not silently migrate old reference records.

Two compatible independently accepted branches can use one reference record
only if each currently warrants its exact selected units/import identities.
Matching names, an ancestor string or an old selected-root ID is not enough.
The local record can be context-independent in identity while its use remains
context-checked. This does not merge conflicting branches or remap symbols.

## All-matched baselines are a normal successful case

If all selected baseline units already exist in the approved library and match,
the output is a **reference-base registration** with zero new declarations.
There is no dummy theorem, no extra accepted root and no necessary wrapper
module. Report correspondence validations separately from proof-checking work:
zero new `checkBatch` calls, not a hard-coded two checking passes merely because
two imported views were inspected.

The current generated-module operation may retain `NO_NEW_MODULE_DECLARATIONS`;
the new operation has a deliberately different result type. Later export may
return the existing reference handle for a fully covered target, or generate a
real small module for new outputs. Do not force the reference base through
current anchor fields that require nonempty `added_names` and five newly
generated artifacts.

A generated delta imports the selected original library and, where needed,
registered previous deltas. The protected plan contains the exact base
correspondence plus that generated chain. The registry must distinguish original
references from generated-module events; neither may masquerade as the other.

## Evidence producer and bounded realization profile

### Producer

Reuse the existing ordinary export scheduler/codecs, initially the
`NativeOwnerExporter` fixed-seed route identified in the companion contract.
They already provide deterministic dependency ordering and complete unit
serialization. A baseline producer is a separate explicit command, not a forged
retained missing-candidate request. Owner-approved local artifacts and selected
targets are its inputs; the initial boundary is the unchanged checked seed.
It needs no fake protected owner or retained consumer. Existing exact boundary
machinery can support a later selected variant; that is not needed first.
The output is the inert manifest/units format in the companion intake contract.
Batch only at complete dependency-safe unit boundaries.

Initially, the already retained inert bundle avoids any new extraction. For a
new source library, extract the selected closure once and partition that output;
do not reload/re-extract it for every admission batch. The current exporter has
finite limits of 262,144 source records, 8,192 selected units, 262,144 edges,
20,000,000 scan nodes, 8-MiB individual units and 64-MiB total output. The shared
scheduler supports lazy group indexing, but the concrete `NativeOwnerExporter`
currently calls `Export.indexSource` eagerly before selection; budget that
whole-environment census. It accumulates a bounded output array and is not a
streaming constant-memory exporter. Unknown scope, unsafe declarations,
unsupported semantics and missing
complete private proofs refuse rather than becoming trusted interfaces.

### Keep interactive work small; bound baseline work separately

Retain the current **32-unit / 4-MiB new-delta envelope**. A separate finite
reference-base profile accounts for the larger accepted unit set and original
library artifacts; it is not a larger interactive request disguised as a flag.
It can validate complete units in the existing bounded admission-sized chunks,
or one independently bounded matching operation, without generating one module
per chunk. Its registration commits only after the whole selected reference
relation succeeds; partial matching events do not authorize a larger base.

The retained 2,852 units fit the exporter's unit/byte ceilings, and the later
2,859-unit portable result remains approximately 49.65 MB. This alone does not
select a working reference profile. Before implementation selection, a read-only
finite census must bound encoded nodes, imports, all generated names, selected
import graph/artifact bytes, per-unit limits, serialized plan/report bytes and
controller/native memory/work. Public visibility and exact installed matching
are eligibility conditions, not numerical capacity conditions. Their success
on every retained unit is not yet known.

Do not copy the whole proof inventory into every later delta plan or registry
report. Keep authenticated per-unit/output identity metadata and protected
evidence references; the one-time correspondence operation reads the full
evidence it actually compares. Binding only an inventory digest is not a
substitute for making that initial comparison. Warm operation may use the
protected validated relation under unchanged artifact/support identities.

An `8,192` unit knob by itself is not a resource profile. Producer, controller,
native request/parser, report, registry, artifact-store and supervisor ceilings
must agree. Reference metadata has its own larger finite envelope; it must not
inherit the current generated-anchor 1,024-unit total limit accidentally.

## Cost and large-network consequences

For a selected local baseline `B` and later deltas `d_i`, the intended cost form is:

```text
C_total = C_produce_or_acquire(B) + C_strict_admit(B)
        + C_correspondence(B, original_artifacts)
        + sum_i [C_warrant_and_artifact_validation(B)
                 + C_import_selected_native_context(B)
                 + C_check_and_write(d_i) + C_acquire_missing_i].
```

There is no mandatory replay of every ancestor's theorem proof in each delta.
There is still one-time cold checking, selected native environment loading,
current-warrant lookup and artifact validation. Rehashing an entire selected
library on every use can be substantial I/O; it must be counted rather than
renamed constant-time caching. Loading a full original module can also cost
more than loading only its selected mathematical subset. This is the practical
tradeoff for preserving the ordinary library ecosystem.

No participant must import the world's entire knowledge or all available
baselines. They select relevant finite contexts. A cold recipient without the
baseline still pays its strict missing-closure cost or chooses a separately
specified alternative policy. This route does not solve proof-independent cold
verification, global discovery completeness or an unbounded local context.

The comparison baseline is a normally pinned Lean/Lake library with equally
good local caches, tools and indexes. This work can remove artificial integration
cost from the commons; it does not by itself establish net growth benefit over
that ordinary baseline. Discovery of useful unfamiliar work, assurance needs,
selective reuse and reciprocal publication must earn the remaining costs.

## Smallest implementation consequence and discriminator

If root selects it, the next source successor needs only these coherent seams:

1. Native exact reference matcher using the existing codec/inventory and
   private/public relation, plus bounded exact selected-artifact closure input.
2. Protected local reference-record/plan variant with live-event registration,
   full-warrant checks and artifact/support validation; no external registration
   authority, journal or global scheduler.
3. Delta closure/export integration that treats only registered exact references
   as its boundary, imports the original modules, and keeps small new-delta
   checking and actual private/public rereads.
4. Standalone baseline producer/intake facade, profile selection and source
   recipe. Reuse existing controlled import, scheduler, admission and containment
   mechanisms. Freeze predecessors; do not patch installed packages in place.

Concrete smallest source seams (fresh successors; names are proposed, not edits
to selected frozen sources):

| File seam | Minimum change |
|---|---|
| New `OrdinaryReferenceBase.lean` | Load exact snapshot through `ImportArtifacts`; match all private warranted rows; derive/match public closure; emit exact projection report, no module or `checkBatch` call. Reuse `OriginalDecl` and the existing theorem-handle relation. |
| New `reference_base.py` beside the anchor integration | Authenticate current warrants/evidence, snapshot approved artifact closure, supervise live matching, validate report, commit protected local record last. Retain its ownership/locking discipline. |
| Successor of `OrdinaryModule04.lean` | Extend `AnchorPlan` with one optional exact reference base; initial imports use its original module names/artifacts; `names` exposes only public bindings. Preserve small delta checks, writer and both fresh rereads. |
| Successors of `module_closure.py`, `module_export.py`, `anchor_store.py`, `module_worker.py` | Recognize reference-backed public cut units; bind original snapshot plus generated chain; verify current warrants/pins and new result kind; retain live-event and cross-phase checks. No blind widening of old ceilings. |
| Existing facade/package selection | Expose explicit register/use commands and returned controlled import configuration; bind changed helpers/runtime support. Producer/intake facade remains the companion contract's responsibility. |

Minimum reference request/record fields, besides existing local operation
authorization, are `schema`, `support_id`, `semantic_id`, `foundation_id`,
`snapshot_id`, `modules` with exact imports/artifact part pins,
`private_units` with exact evidence/warrant/output identities, and
`expose_targets`. The successful live report/record additionally binds
`public_units`, `public_bindings` and per-row `full` or `erased_singleton_theorem`
class, plus exact input/report hashes and current validation events. The native
worker computes these sets; it does not trust a peer-supplied public inventory.
Later delta plans need only the protected reference ID/snapshot/approved public
bindings plus the generated anchor chain, not every ancestral proof body. Pin
the final canonical field encodings and coherent finite ceilings at source
selection; do not introduce a second generic registry or portable trust token.

One small decision-changing native workflow is enough to challenge the central
claim before handling the whole retained closure:

- Select an approved local library containing a compatible nonbasis transparent
  definition and a small supported generated inductive/constructor/recursor
  unit, with the definition genuinely computing through that group. Establish
  exact absence from the fixed seed; do not assume it from familiar names.
- Independently admit their complete inert evidence, then register an
  **all-matched** reference base to the original approved library without any
  synthetic theorem or new module.
- Generate one small new delta whose proof uses definitional/constructor
  reduction through those references. A normal project imports the original
  library plus the delta and uses at least one actual original notation or
  registered instance/simp rule, showing that the library's frontend metadata
  was preserved rather than recreated by the bridge.
- Extract and independently admit a genuine successor under the unchanged strict
  policy. This final check defeats any inference from compiler success alone.
- Target cheap controls at changed boundaries: wrong definition body, incomplete
  generated inventory, unsupported public erasure, changed artifact selection,
  unwarranted ambient reference and wrong-context reuse must refuse. Reuse
  existing unchanged admission/cleanup evidence; do not rerun a broad campaign.

Add the narrow public-projection discriminator within that same fixture: a
public erased theorem with a private proof-only hidden helper is usable; making
the same helper necessary to a public computational body (or retaining it in an
actual full-public theorem proof) must require its full public representation.
This tests the new distinction without a separate large-library experiment.

The existing large admission result already answers the batching-feasibility
question. Do not recheck the 2,852 units merely to decorate this architectural
decision with another large run. No producer or native workflow is authorized
by this contract. Root must first select the actual boundary, finite inputs,
resource profile and independent review.

## Sources and nonclaims

Read with the companion bundle contract, the prior exact-installed-declaration
argument, [independent challenge](ORDINARY-BASELINE-BUNDLE-CHALLENGE.md), and
[current distribution recipe](../../../software/v5/ordinary_distribution/CURRENT.md).
The existing `leanchecker --fresh` acceptance-boundary analysis remains the
reference for arbitrary axioms, unsafe/partial skips, binary input and absent
finite bounds; this proposal does not rediscover it or claim that tool alone
provides hostile validation.

Selected inspected source identities:

| Source below `software/v5/` | SHA-256 |
|---|---|
| `ordinary_lean/OriginalDecl.lean` | `bfb5fc910808d9dc178977cfa6edeacf0b5cbfe7bd99bc6277ee11a456d516c1` |
| `ordinary_lean/CheckedExtension.lean` | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |
| `ordinary_lean/OrdinaryExport.lean` | `1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f` |
| `ordinary_module_anchor/OrdinaryModule04.lean` | `901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8` |
| `ordinary_module_anchor/module_export.py` | `85f9a2b5695dd90dd888bd3868f51a41904cb0b2d0d14335abe0b65d5182b65c` |
| `ordinary_module_anchor/anchor_store.py` | `a244eaf2764b6a51f4006447eebe3b69529a46bf376f999804a99f23661a929e` |
| `ordinary_module_anchor/module_closure.py` | `f053e9726bdba24724e7e44baa03ffa0006f80b068440086a36023068512aa8c` |
| `ordinary_module_anchor/module_worker.py` | `7d577ce31e37a07a0ac4868d10da792e4476db4df6ab0492791f9d8434b6247b` |
| `ordinary_project_extraction/library_extraction.py` | `cd79d9050fbc80a94faef845ddf99fe7d1b8ba5e376048aa4a7698f06f396061` |

These pins identify inspected implementation evidence, not adoption of a future
support profile. No full-v5, useful-growth, foreign-runtime, independent-host,
arbitrary hostile-project or global-scale completion claim follows.

The inspected selected runtime source
`software/runtime/lean-4.34.0-windows/src/lean/Lean/Declaration.lean` has SHA-256
`fcb928c1686f0655279a790f92bd61f8c0d6df3be51a5eccaa2880de058e5e24`.
Its documented metadata role is not a compiled-kernel equivalence proof.
