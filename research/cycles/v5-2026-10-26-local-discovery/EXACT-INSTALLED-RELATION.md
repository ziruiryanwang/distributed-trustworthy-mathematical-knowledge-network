# Exact reuse of installed declarations for a received-vocabulary module

2026-10-26. Source-only principle and implementation boundary; no product edit,
product import, native execution, owner-state opening, network operation, or
acceptance of the retained example. Root owns subsequent selection. The canonical
workspace guard passed. Integration footprint belongs to the separate
received-vocabulary assignment.

## Decision

**Yes, a conservative exact installed-declaration relation can extend the current
module path to safe definitions and complete inductive groups. Opaque declarations
qualify only when their full exact records are available in both required views.**
Reuse is identity of an already warranted declaration's representation under the
same pinned semantics, not interpretation by a same-named local declaration.
An axiom-shaped public opaque/definition stub fails this relation even when a
matching private body is available. The existing special theorem-stub rule stays
theorem-specific.

The narrow change is an extra realization case for already installed *complete
selected units*. It skips adding those declarations, but does not remove their
received unit/export identities, authenticated closure, exact inventories, public
visibility checks, fresh-process rereads, or cost accounting. It neither enlarges
the 581-row foundation nor installs an axiom, imports peer binaries, renames
symbols, or converts an advisory construction into semantic correspondence.

This resolves the obstruction in principle, not for the actual ten retained
`AllClosure` units. `RECEIVED-VOCABULARY-QUERY.md` establishes their small inert
closure and the current rejection branch. Neither that graph census nor the
presence of source names in Init establishes the comparisons below. Exact runtime
rows, public visibility, complete-group correspondence, resource fit, and the
later public local-query route remain unexecuted.

## Inspected source and the gap being closed

Let `P` mean the unchanged selected package:

`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`.

The source argument uses these concrete seams:

- `P/module/OrdinaryModule.lean:177`: descriptors decode only against the fixed
  basis, authenticated anchor outputs, and preceding selected outputs. Ambient
  Init membership does not add a name to that allowed set.
- `:211`, `:228`, `:260`: full inventories are checked, but installed matches are
  restricted to singleton theorems; only those may have a public axiom-shaped
  signature after an exact full private proof match.
- `:297`, `:585`, `:639`: the report partition is reconstructed from the request;
  private/public checking and separate private/exported rereads bind the actual
  artifacts. These gates are part of the proposal, not optional follow-up checks.
- `P/installation/lean-src/OriginalDecl.lean:123`: the exact inventory projection;
  `:295`, `:357`: bounded canonical descriptor/unit decoding.
- `P/installation/lean-src/CheckedExtension.lean:99`: additions use checked kernel
  insertion, compare actual generated rows, and reject unexpected output census.
- `software/v5/ordinary_lean/OwnerRebind.lean:179`, `:270`, `:320`, `:345`:
  existing exact non-theorem row matching, semantic scans, atomic group checks,
  and complete prepared-request rebinding. `DefinitionView.existingAbstract` is
  deliberately outside this proposal.

`decodeUnit` is not a substitute for checked generation. For ordinary declarations
it checks a singleton name census; for inductives it checks inclusion of declared
types and constructors. It does not prove descriptor/inventory body equality,
complete generated recursor census, or acceptance. The unchanged add path supplies
these through the kernel. A new match path must obtain them from authenticated
previous acceptance plus the explicit checks below; simply deleting the current
collision refusal is insufficient.

## Relation and explicit premises

Fix one authenticated selected request, one pinned Lean/runtime profile, and one
immutable local Init/registered-anchor import chain. Write `J(c)` for
`DeclCodec.inventoryRow c`, with the selected limits and the existing
`erase-mdata-only-v1` expression encoding. Equality here is exact canonical JSON
equality, not Lean's coarser expression equality, alpha-equivalence, definitional
equality, matching pretty-printed text, or equality of a digest supplied by a peer.
Binder labels/annotations, universe parameter names/order, reduction metadata,
literal representation, and declaration names remain in the comparison.

Let `B` be the fixed basis, `A` the separately authenticated anchor bindings, and
`U_1, ..., U_k` the selected dependency-first units. Each `U_i` supplies a descriptor
`D_i`, complete ordered inventory `R_i`, output-name set `N_i`, and exact received
unit/export bindings. Set `S_i = B union A union N_1 ... union N_(i-1)`.

The following are existing trusted premises, not conclusions of string matching:

1. The controller authenticates the exact protected request, runtime, profile,
   fixed basis, custody/owner evidence, unit/export bindings, and imported local
   artifact chain. The selected accepted unit warrants that `D_i` was checked and
   `R_i` is its complete output inventory under this profile. Merely having a
   manifest, custody bytes, export preview, or claimed identifiers does not supply
   that warrant. A system allowing incomplete accepted generated inventories
   would invalidate this premise and must repair acceptance first.
2. The pinned Lean kernel and installed local runtime have their already-assumed
   soundness and record semantics; native literal and primitive interpretation
   agree with the selected profile. `quotInit`, an equal name, or a basis row
   comparison alone does not establish the whole profile. No additional native
   primitive, axiom, unsafe declaration, or partial declaration is authorized.
3. The codecs are canonical and faithful to the retained record fields modulo
   semantically irrelevant `Expr.mdata`. Group ownership and generated output
   conventions are those of the same pinned kernel. Environment import/export and
   immutable artifact bindings have their existing trusted meaning.

For each already-present unit, require all of the following.

**Atomic presence and supported shape.** Either none of `N_i` is present and the
unchanged add/check path handles the entire unit, or every name is present and the
whole unit is considered for matching. Any partial collision fails. Kernel and
frontend views must agree on the selected records; a hidden kernel collision
cannot become an overwrite attempt or an invitation to promote that record.
Require safe singleton definition/opaque descriptors, with `all = [name]`, or a
whole supported inductive descriptor and its complete generated output inventory.
Keep the present singleton-theorem branch separately. Reject mutual ordinary
definition/theorem/opaque metadata and all unsupported declaration kinds. This is
a deliberately small sufficient fragment, not a claim that other cases are
impossible.

**Descriptor-to-record correspondence.** For a definition or opaque, compute the
inventory row of the decoded descriptor's corresponding `ConstantInfo` and require
it to equal the sole expected row. For an inductive group, reconstruct the
descriptor from the selected actual inductive/constructor records using their
ordered `all` lists, universe parameters, parameter count, types, constructor
lists/types/indices, and safety fields; its canonical descriptor must equal `D_i`.
This can follow `BootstrapProbe.makeUnit`'s reconstruction logic over bounded
selected lookups; it does not require importing/re-executing peer source or an
unbounded environment census.

**Exact actual rows and atomic group consistency.** Every expected row must have
an actual safe non-axiom record with the same key and `J(actual) = row`. For a
generated unit, all rows must be inductive/constructor/recursor records belonging
to the same owner; the owner is in this unit and not already bound by `S_i`.
Every `all`, constructor-owner, constructor list and recursor-rule constructor
reference must agree with the complete selected group; no mixed owner or
basis/anchor/prior-unit straddle is permitted. The accepted complete inventory,
same pinned generation semantics, descriptor equality, and exact actual row
comparison supply whole-group correspondence. `OwnerRebind.groupScope` alone
explicitly inherits completeness and is not a census proof. If that premise is
unavailable, refuse; do not infer completeness merely from the names supplied.

**Closed semantic support.** Decode the descriptor against `S_i` with only its
legitimate inductive self-types additionally allowed. Scan matched actual types,
definition/opaque bodies, recursor rule right-hand sides, and group metadata
references. External references must lie in `S_i`; only internal references of
the complete inductive unit may use `N_i`. Preserve the profile's implicit literal
dependencies and all current forbidden-name checks. Ordinary singleton `all`
metadata is already fixed by the shape restriction. Do not grant all ambient
installed names, and do not assume descriptor decoding scans generated recursor
bodies. Existing `scanSemantics` is the reusable bounded operation for the latter.

**Two real views, then persisted views.** Require the exact non-theorem rows in
both the private import and the actual exported/public import that the module
will use. No missing record, axiom-shaped stub, different declaration kind,
hidden-body promotion, body erasure, changed reducibility hint, changed recursor
rule, or incompatible public row passes. Perform the same exact non-theorem
checks on the written module's separate private and exported fresh-process
rereads. Ordinary new additions continue through both current `checkBatch`
passes and their full inventory checks. Retain the old theorem exception only
after its complete exact private singleton proof match; public theorem signature
equality alone never supplies a warrant.

The practical relation is therefore `ExactInstalled(U_i, E_private, E_public)`
with all five clauses, not merely `J(E_private[name]) = row`. The immutable
request/partition/report/artifact checks transport that relation across phases.

### What exact rows preserve

Every row contains the same name, declaration kind, ordered original universe
parameters, and complete encoded type. Its remaining fields are:

| Kind | Additional fields that must remain exact |
|---|---|
| Definition (1) | Body, reducibility hint including regular height, ordered `all` |
| Opaque (3) | Body, safety flag, ordered `all` |
| Inductive (4) | Parameter/index counts, ordered `all`, constructors, nested count, recursion/safety/reflexivity flags |
| Constructor (5) | Owning inductive, constructor index, parameter/field counts, safety |
| Recursor (6) | Ordered `all`, parameter/index/motive/minor counts, ordered rules with constructor, field count and RHS, `k` and safety flags |

This is why same type is insufficient even for an apparently simple installed
definition, and why type/constructor signatures alone are insufficient for a
whole inductive group. The exactness intentionally rejects some semantically
equivalent representations; no equivalence solver or normalization migration is
being proposed. In particular, a nonbasis reducibility height is not silently
normalized using the foundation's distinct legacy normalization convention.

## Conditional sufficiency argument

Under the stated premises, the relation is sufficient for using selected received
non-theorem vocabulary with its selected meanings in a generated public module.

Proceed in the authenticated dependency order. Initially the basis has its
existing fixed interpretation, and every anchor binding has its separately
established exact local-artifact correspondence. Assume correspondence for `S_i`.

If the unit is absent, unchanged checked kernel addition yields exactly the
promised safe records and rejects extra generated outputs. Its references decode
only against the corresponded context and its legitimate group self-types.
Therefore extending by those records preserves the induction invariant.

If the unit is installed, it adds no declaration. Descriptor equality binds the
selected construction to the selected rows. Canonical row equality preserves all
type, body, constructor, projection-relevant metadata and recursor computation
fields in the supported records. Closed support replaces every external constant
lookup with an already corresponded lookup; the complete-group clause handles
the simultaneous internal references. The same pinned primitive/literal rules
apply. Consequently the installed records realize the selected records modulo
the codec's existing metadata erasure. Marking these *bindings* as realized
extends the invariant without extending kernel assumptions or changing received
identities. Unknown unrelated installed declarations receive no bindings and
cannot enter selected descriptors through the allowed-name set.

The public checks establish this non-theorem invariant in the environment actually
used for public checking. The second kernel pass is still necessary: existing
public theorem-body erasure can lose conversion, including the module source's
explicit `Acc.rec` example. Private success cannot imply public compatibility.
The writer's exact output census/import list and two protected fresh rereads
then establish that the persisted artifacts present the same selected records.
A successful proof-free local type query over those imports can consequently be
bound back to the selected unit/export symbols by the unchanged context checks.

This is a conditional source argument, not a machine-checked metatheorem or proof
of the trusted kernel/codec premises. It does not promise query elaboration will
succeed, recreate producer notation/instances/plugins, preserve execution of
compiled code, establish usefulness or novelty, or qualify the actual retained
units. The artifact supplies kernel vocabulary; ordinary explicit syntax may be
needed because the module path does not reconstruct arbitrary elaborator state.

## Falsifiers and refusal examples

These are prospective decision-changing controls, not executed outcomes.

1. **Same type, different body.** A received `f : Nat -> Nat := fun n => n` and an
   installed `f : Nat -> Nat := fun _ => 0` share a name/signature but change the
   meaning of a queried law. Full row mismatch must refuse. Equal body with a
   changed kind, reducibility hint/height, or universe parameter order must also
   refuse under this exact relation.
2. **Inconsistent descriptor and row.** A definition descriptor contains the
   received body while its expected row is copied from another installed body.
   The descriptor decodes and a naive installed-row comparison passes, but the
   selected unit no longer denotes its descriptor. Descriptor-to-row equality
   must refuse. The corresponding inductive descriptor/constructor-row mismatch
   must refuse too, independently of the authentication premise.
3. **Partial or mixed generated group.** Present `List.Mem` and a constructor but
   absent selected recursor; or a row from another group; or a group split over
   an anchor/basis and new unit. Refuse the whole unit. Removing a recursor from a
   raw request must fail its authenticated complete-unit binding; a parser that
   merely sees all descriptor constructors is not sufficient. There is no
   “match the existing prefix, generate the rest” operation.
4. **Same eliminator type, different reduction.** Mutating a recursor rule RHS,
   rule constructor/field count, `k` flag, or group/constructor ordering can alter
   computation without the obvious printed type changing. Exact generated rows
   must refuse. Exact type/constructor rows do not waive recursor equality.
5. **Private body, public abstract handle.** The private environment has exact
   `opaque secret : Nat`, while the public lookup is axiom-shaped or absent.
   Refuse even if public universes/type agree. The theorem-stub exception cannot
   be generalized to definition/opaque stubs. A private-only `def` also fails.
6. **Unbound ambient dependency.** A same-row installed declaration depends on an
   ambient `helper` absent from basis, anchors and earlier selected complete
   units. The semantic scan must refuse; Init membership is no authority. A
   generated recursor RHS is included in this control.
7. **Private pass, public conversion failure.** A fresh added declaration relies
   on conversion unavailable after public theorem erasure. The existing second
   `checkBatch` must still fail; adding a matched relation cannot bypass it.
8. **Fresh-import drift.** A matched public row changes/disappears, or any artifact,
   request partition, import map, target binding or protected request changes
   between build and reread. Existing phase binding plus fresh exact checks must
   refuse adoption. A successful build alone remains pending.
9. **Safe positive discriminator.** A warranted complete supported unit matches
   exact private/public installed records and a genuinely new selected dependent
   unit checks in both views and survives both rereads. Only that outcome supports
   the new realization case. It does not establish that every Init export, nested
   group, opaque declaration, or retained `AllClosure` closure is supported.

## Smallest implementation boundary

Reuse the existing inventory projection, allowed descriptor fragment, bounded
semantic scans, complete-group owner checks, exact protected closure, dual kernel
passes and fresh rereads. Add an explicit exact-installed non-theorem realization
alongside the existing singleton-theorem case. The private classifier, public
check dispatcher, request-derived partition validation and persisted anchor
realization handling must agree on this case. Their concrete Python/native
footprint is delegated to the integration note; no one-line relaxation qualifies.

Keep definitions and opaques singleton-only, and keep any unsupported/mismatching
or partially present group as a closed refusal. Keep the current requirement that
at least one genuinely new module declaration exists (`NO_NEW_MODULE_DECLARATIONS`)
for this first change; handling an all-installed request is a separate API choice
and is not needed to pretend a module was produced. Do not extend resource caps
to disguise mismatch; match encodings/scans remain charged under a finite selected
envelope and existing count/artifact limits.

For `AllClosure`, the smallest subsequent evidence is actual bounded comparison
of the selected received nonbasis Init rows/groups in both views, preserving every
failed comparison. If those rows differ or the public view hides required data,
this proposal correctly does not fix that example. Root should then choose
between an explicitly different checked representation/correspondence and ordinary
local theory work with an honest receiver-interpreted search claim. Increasing
the cap, declaring these names to be foundation, coercing V2 request headers into
V1, silently erasing bodies, or best-effort owner construction is not an exact
received-vocabulary solution.

A proof-free exact-rebinding query adapter is conceptually possible, but would
need its own protected portable context binding, exact public relation and finite
execution glue. It is not inherently smaller than repairing the already-public
module route and must not borrow the looser `existingAbstract` or best-effort
construction semantics. General renaming/import interpretation is a different
architecture decision. Stop here at the implementable exact fragment and its
falsifiers; no new mechanism, runtime, or actual correspondence is selected by
this document.
