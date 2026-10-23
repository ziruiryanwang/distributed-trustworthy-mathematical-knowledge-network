# Owner-project rebinding: implementable interface-correspondence plan

2026-10-22. Source-only follow-up by `ordinary_native_controller`. No bridge
implementation, test, runtime, Git or product change is selected. This note
updates the earlier full-record recommendation in `OWNER-BRIDGE-REVIEW.md`
using an actual new obstacle: both standalone full-private owner export and the
combined getEnv/private-command-library route have exhausted the selected memory
envelope. There is still no usable actual method export bundle.

**Decision: retain the owner's existing environment, use warranted theorem
interfaces for already available mathematics, and check-add only missing
declarations. Do not require loading private proofs of every existing theorem
or the whole private Lean compiler library.**

## Smallest useful endpoint

A consumer imports its normal Std library and a narrow owner-installed command.
It acquires the peer method as inert data, uses its original names/binders, and
exports a substantive downstream result for independent receiver checking.
It does not import `examples.ReadFootprint`, a checker `DMKNLocal` snapshot,
or a second independent full owner environment.

Illustrative future source, not an implemented command:

```lean
import Std.Data.ExtHashMap.Lemmas
import OwnerRebind

#commons_use "<owner-prepared request directory>"

namespace DMKN.ReadFootprint.Consumer
-- Existing snapshot/applyBatches proof body, now using acquired
-- ReadsOnly, Avoids and readsOnly_insertMany.
end DMKN.ReadFootprint.Consumer
```

The selected first scope is kernel reasoning and ordinary elaboration, not
native execution of acquired definitions, arbitrary peer plugins, notation or
metadata packages. Existing owner notation/instances remain available because
the actual owner environment is retained.

## The decisive distinction: accepted meaning versus authoring view

Let `K` be the independently warranted receiver environment, and `O` the
ordinary owner authoring environment. The bridge is **not** a proof that `O`
is globally sound. It establishes a selected correspondence between the names
used for authoring and their already accepted meanings in `K`.

For an opaque theorem `c : P` already warranted in `K`, a consumer does not
need its original proof body to use `c`. Its proposition, universe parameters
and the meanings occurring in that proposition suffice. Lean theorem opacity
and proof irrelevance justify avoiding proof-value equality for this operation.
This is an **interface correspondence**, not equality of proof-bearing evidence
IDs or permission to issue a new acceptance warrant from a type alone.

An existing owner `.axiomInfo` may be a normal public theorem stub. It can also
be an arbitrary owner assumption. The bridge need not infer which history
produced it: it may use that existing name as an authoring handle **only when**
the requested exact accepted theorem already exists in `K`, its proposition
matches, and all proposition dependencies have their warranted meanings bound.
An arbitrary stub without that accepted theorem warrant is refused. No new
axiom is inserted, no owner stub is promoted, and no claim is made that the
owner's binary itself contains the accepted proof.

A final exported consumer proof is checked independently against `K` extended
by its new allowed declarations. Thus a false owner assumption, unsafe
elaboration shortcut, wrong correspondence or forgotten dependency cannot gain
network authority from this bridge. The exact original dependency names/symbol
IDs must resolve in that receiver check. Owner elaboration remains a construction
aid, not the acceptance event.

This permits useful ordinary public-module authoring without broadening
mathematical authority. A raw owner .olean containing stubs is not offered as a
portable checked proof artifact; exchange remains the inert exported successor.

## Concrete semantic matching rules

| Accepted dependency in K | Required owner view | What must be compared |
|---|---|---|
| Theorem, with an actual accepted theorem warrant | Safe theorem record, or an existing axiom-shaped authoring stub explicitly mapped to that warrant | Exact name, universe/interface parameters and original type; bind all type/projection dependencies. Do not compare or request the theorem proof body. |
| Transparent definition | Actual safe definition with required reduction semantics | Original type, value/body, universes and relevant definition metadata under bound dependencies. A matching type alone does not establish definition meaning. |
| Inductive group, constructor or recursor | Compatible actual kernel records for the required group | Types, parameters, constructor/recursor metadata and computation rules. No constructor insertion or group splitting from advertised data. |
| Opaque non-theorem value | Actual matching accepted semantics, or a future explicitly justified abstraction mode | First mode retains exact record comparison; do not silently generalize the theorem rule to arbitrary data. |
| Fixed permitted foundation axiom or quotient primitive | Exact fixed-profile counterpart | The selected basis's explicit policy/type/primitive identity. It is not a new theorem stub rule. |

The ordinary theorem type projection can use `ExprCodec.encode` on
`actual.levelParams`/`actual.type`, plus exact original names/parameter lists.
It must not call `DeclCodec.inventoryRow` merely to obtain a type, because that
would demand and encode the very proof body this rule avoids. For exact
definition/generated-record rows, the existing `DeclCodec.inventoryRow`
remains appropriate.

The frozen normalized basis is a special projection. Reuse
`BootstrapProbe.dagJson` for its type-only rows and the existing normalized
inventory projection for definitions/generated records, including its selected
definition-height convention. Its theorem entries also use the already
independently checked basis warrant and need no owner proof-body equality.
Do not blindly reuse `Export.compareSourceBasis` unchanged: that function was
written for full private source correspondence and compares proof-bearing rows.

A missing transparent body or computation rule yields
`NEEDS_DEPENDENCY_SEMANTICS`, not a fallback to whole-private import. The
controller can acquire just the needed semantics from already accepted inert
data. If a same-named existing owner record lacks or conflicts with those
semantics, first scope refuses; it does not overwrite the owner record.
New wider abstraction/refinement modes are not needed for the initial fixture.

## Exact prepared input and responsibility split

Keep identity/file authorization in the existing trusted controller and selected
semantic matching in the Lean helper. Do not build another registry or package
manager.

Controller preparation:

1. Open the existing protected accepted context and select exact target symbols.
   Obtain real accepted evidence/records, not a path, type preview or saved PASS
   offered as authority. Current integration can reuse admission's saved exact
   evidence; a public retrieval API is not assumed already implemented.
2. Validate ordinary evidence/profile/direct identities with the existing reader.
   Derive a selected **semantic interface closure**, not the transitive proof
   construction history of every existing theorem. For a theorem, follow its
   type dependencies only; for a transparent definition, follow required type
   and body dependencies; for inductives, retain required complete group
   semantics. Proof dependencies remain the accepted receiver's warrant lineage,
   not mandatory owner-side imports.
3. Produce a fresh pinned request containing:
   - exact profile and accepted context ID;
   - requested `(original name, accepted symbol ID)` targets;
   - ordinary theorem-interface rows tied to actual accepted theorem IDs;
   - required exact definition/inductive/opaque semantic rows;
   - missing candidate declaration units with full inert proofs/bodies;
   - fixed basis identity and finite aggregate counters.
4. Use fixed local filenames under the new request directory, not peer paths.
   The root-selected launcher pins the entire prepared request/helper support
   before ordinary source processing; bytes remain immutable during use and are
   rechecked at the supervised boundary. The same request cannot change which
   accepted theorem a name denotes midway through authoring.

The first implementation can represent these as a bounded manifest and numbered
JSON files. No new generic stream framework or duplicate SHA implementation in
Lean is required. Read one record at a time, retaining only the correspondence
map and bounded pending missing batch. Lexical numeric/depth/byte guards precede
JSON parsing as in the reviewed worker.

The helper's prepared inputs are trusted controller plumbing, not unforgeable
public warrants. A low-level call with a fabricated request does not create a
catalog acceptance event. Public client assembly must wire preparation and
launch together before calling this a deployed feature.

## Minimal helper API and algorithm

Proposed API, not implemented:

```text
rebindPrepared(
  owner : Lean.Environment,
  prepared : bounded selected correspondence request,
  limits : finite owner policy
) : IO {
  environment : Lean.Environment,
  interfaceMatched : Nat,
  exactMatched : Nat,
  checkedUnits : Nat,
  addedNames : Array Lean.Name,
  targetNames : Array Lean.Name
}
```

1. The top-level trusted command gets its actual `owner` through `getEnv`.
   Require `owner.asyncPrefix?.isNone`; never `unlockAsync`. Preserve module
   identity, imports, options, extensions and all old declarations. Start a local
   `candidate := owner`. No second `importModules` and no initial `setEnv`.
2. Match only selected required basis/semantic dependencies under the table
   above. Use direct kernel lookups, not a census of every imported constant.
   The type-interface graph may contain groups; use the request's bounded
   group structure rather than require an artificial acyclic ordering of every
   constructor name. No accepted interface is inferred from an owner type alone.
3. For each missing declaration group, classify actual kernel membership:
   all absent means decode and check-add; all present means match the appropriate
   accepted interface or exact semantic record; a partly present generated group
   refuses `PARTIAL_EXISTING_GROUP`. Do not split or overwrite a group.
4. Decode against previously bound required names and declared complete groups,
   not arbitrary unrelated owner constants. Earlier pending missing names help
   syntax decoding only. Flush pending units in dependency order through
   `CheckedExtension.checkBatch` with unchanged limits; retain only its actual
   returned candidate environment. A matched record needing pending definitions
   is resolved after that batch succeeds.
5. For new declarations, `addDeclCore(..., doCheck := true)` already updates
   normal frontend maps. For a newly generated hidden `.recInfo` only, reuse
   the frozen AgentClient pattern:
   `addConstAsync` -> `commitConst` with the actual checked record ->
   `commitCheckEnv` -> retain `mainEnv`. Resolve both promises before accessing
   it. Do not expose unrelated preexisting private records or insert advertised
   ConstantInfo. Other missing new frontend kinds refuse.
6. Register new normal namespace prefixes on the candidate following the short
   private upstream `registerNamePrefixes` rule (`privateToUserName`, string
   namespace prefixes, no solely internal underscore namespaces). No metadata
   package/notation loader is necessary.
7. Require targets in the kernel and usable frontend view with their selected
   interface correspondence. Return the candidate/counters. Only then perform
   one `modifyEnv (fun _ => result.environment)`.

Failures discard the candidate, including its newly created promises/namespaces.
Do not catch errors by installing axioms, call Lean.addDecl's recovery path,
change skip-check options, erase stage-two state, or relabel missing private data
as a mathematical result. Existing authoring stubs are not reinserted or promoted.

## Implementation and cost consequences

A future `OwnerRebind` must depend on narrow command APIs and the minimal
codec/checker support actually used, not `import all Lean` or the entire private
compiler helper library. Current failed getEnv integration proves that merely
moving a full-private import inside a command is not enough. Module visibility
and exact selected helper imports are an implementation constraint, not a reason
to increase RAM or retry the same failed construction.

The owner request omits full proof bodies of already warranted theorem
dependencies. Its remaining cost is selected type/semantic correspondence plus
checking missing new declarations. Transparent computation can still require
substantial data; the plan does not promise constant-cost semantic imports.
Any later immutable-owner correspondence cache should follow an observed
bottleneck, not precede this minimal usable path.

Reuse receiver defaults per checked missing batch:1024 units,65536 names,
2097152 scan nodes and existing finite kernel limits. Give the whole command
separate finite byte/record/CPU bounds and at most65536 newly introduced names.
Existing stage-two entries count toward the unchanged131072 checker bound.
Do not reset allowances per lemma or copy a huge exporter limit into admission.

The actual producer method may require only three new ordinary declarations,
but that count is not yet an executed result. Do not prepare a hardcoded success
census while the export is absent.

After a genuine export/admission is available, the next implementation decision
is one narrow helper/command plus a consumer-source successor replacing only
its known producer import with this data command. Reuse the already authored
consumer proof body. The decisive evidence is a source-level use with ordinary
named binders/namespace/Std functionality, followed by real inert consumer export
and independent checking over the accepted root.

Changed-boundary negatives: a theorem stub without its accepted warrant, a
same-type transparent definition with different body, incompatible proposition
dependencies, partial group, and failure after an earlier successful missing
group without environment leakage. A generated-recursor control is relevant
only if that bridge path is used. No such runtime is selected here. A successful
bridge would still not itself establish unknown-ID discovery, growth advantage,
or final deployable v5.

## Necessary matching successor-export seam

The downstream exporter must stop at the **selected already warranted binding
map**, not reconstruct every dependency back to the fixed seed again. Otherwise
the public-stub optimization would be lost as soon as the consumer contributed:
the exporter would ask the owner for private proof bodies it never needed.

Add only a narrow future `selectedAbove(owner, boundNamesAndSymbolIDs, targets)`
entry alongside the existing closure scheduler. Its boundary is supplied by
the actual prepared correspondence/accepted context, not by a peer's arbitrary
list of axioms. A referenced bound name emits that exact accepted dependency
identity and stops traversal. Unbound new declarations retain full ordinary
units/proof data and follow the existing allowed-declaration/group checks.
This does not permit an unbound owner axiom or sorry: such a reference is not a
warranted boundary and must fail export/admission. The receiver independently
rechecks every boundary identity and all new declarations over its real context.

This is the concrete reason the interface route can save work throughout the
reciprocal workflow, rather than only during owner import. It requires no new
proof system, identity scheme, global ledger or general environment framework.
