# R1: source-derived proof-context reconciliation

Date: 2026-09-20. Draft bounded local experiment contract; NOT RUN. This follows the completed [source-composition checkpoint](2026-09-20-source-composition-qualified.md). It is a small continuation of the user's authorized useful local experimental work, not networking or deployment. It does not change the selected PI1 protocol or any held Gate A artifacts.

## Decision and meaningful success

Can a local receiver use independently produced exact proofs of the same semantic dependency in one coherent, freshly checked environment, without overwriting an old alias or discarding the second contribution?

The completed B source really generated a proof helper. Its semantic map definition `d` references the helper judgment `j`; its replay chooses one exact instance `p` to realize that semantic alias. A second source branch is intended to preserve `d` and `j` while supplying a different exact instance `q`. Original contexts selecting different representatives are not one unchanged native environment.

Choosing `p` again and rediscovering the old map package is legitimate deduplication but is **not by itself this experiment's positive result**. Require one final exact consumer root with both paths:

```
consumer type -> shared map d -> semantic alias A(j) -> selected instance I(s)
consumer proof -------------------------------------> unselected instance I(r)
```

Here `{s,r} = {p,q}` and `s != r`. Both actual instances must survive least-closure pruning, actual export and fresh replay. Merely carrying an unused alternative in a manifest or an unrelated preparation root does not satisfy the test.

## Held inputs and the one new source candidate

Reuse the exact Gate A foundation, Lean pin, common source interface, original B map/helper/law packages, source codec, receiving logic and reviewed process containment. Reference their real immutable files and hashes in new plans. All `experiments/lean-source-composition/` held code, executed runs and final report-01 remain preservation-only.

Create one separately compiled `ProducerB2` module with no source/module dependency on A or original B. The following is the selected new source blueprint, not compiled evidence:

```lean
import Init.Data.Function
universe u v
namespace SharedSubtypeB2

theorem preserves_at {α : Type u} {β : Type v}
    {p : α → Prop} {q : β → Prop}
    (f : α → β) (h : ∀ a, p a → q (f a))
    (a : α) (ha : p a) : q (f a) := h a ha

theorem map_property {α : Type u} {β : Type v}
    {p : α → Prop} {q : β → Prop}
    (f : α → β) (h : ∀ a, p a → q (f a))
    (x : Subtype p) : q (f x.val) :=
  preserves_at f h x.val x.property

def map {α : Type u} {β : Type v} {p : α → Prop} {q : β → Prop}
    (f : α → β) (h : ∀ a, p a → q (f a)) : Subtype p → Subtype q :=
  fun x => ⟨f x.val, map_property f h x⟩

theorem map_val {α : Type u} {β : Type v} {p : α → Prop} {q : β → Prop}
    (f : α → β) (h : ∀ a, p a → q (f a)) (x : Subtype p) :
    (map f h x).val = f x.val := rfl

end SharedSubtypeB2
```

The extra theorem application is a genuine alternative evidence route, not a byte-edited canonical witness. The frontend may still elaborate this differently than expected; actual capture decides. Keep complete generated/private dependencies. Source spelling is not an identity authority.

Before reconciliation, require actual captured equality of original helper JudgmentID and B2 `map_property` JudgmentID; original and B2 map DefinitionID; original and B2 map-law JudgmentID; and all shared interface descriptors. Require distinct actual helper ProofInstanceIDs `p != q`, with B2's witness referencing its actual `preserves_at` proof instance. The two map-law proof instances may coalesce; do not force an unnecessary difference.

Independently replay B2 under its own exact context before treating it as checked input. If semantic IDs differ or helper instances coalesce, report `CASE_NOT_INSTANTIATED` with the actual differences. Do not hand-edit descriptors or relax equality conditions to manufacture the case. A malformed/unsupported source, native rejection or resource nondecision is reported at its actual boundary instead.

## Conflict control and finite candidate pool

First submit the original B1 and B2 map/law packages to the unchanged ordinary merge procedure. Their maps must actually bind the same `j` to `p` and `q`, respectively. Expected outcome is `incompatible representative contexts; rebuild required`. A missing file, malformed object or unrelated merge error is not this control's success.

For replanning only, load and validate each package separately. Merge their inert immutable canonical objects and agreeing generated inventories; do **not** claim their original replay contexts have already merged. The only variable alternatives are the two actual helper instances for `j`; every other encountered alias must have a single coherent retained alternative or be classified as out of this case. Include complete fixed prerequisites and exact direct instance references. There is no candidate discovery, fabricated proof, extra axiom, remote lookup or unlimited alternative enumeration.

Derive the actual PI1 nodes `S(j)`, `I(p)`, `A(j)`, `D(d)`, `O(o)` and `G(g)`, with the prerequisite edges from the existing specification. A practical implementation may instrument the existing checked planner's enter/leave traversal separately under each original valid context, retaining every direct edge even when its child was already visited. Union the fixed edges; replace only an alias's selected-instance edge by its candidate alternatives. If a supposedly fixed node has different prerequisites under the two traversals, fail the graph construction rather than silently union inconsistent interpretations. Seed references are already qualified base inputs, not alias candidates.

Use synchronous finite grounding rounds. Ordinary nodes become ready when all fixed predecessors were grounded in an earlier round. An alias becomes ready when its statement/fixed predecessors and at least one candidate instance were grounded earlier. At the earliest such alias round, choose the lexicographically smallest exact typed candidate ID among those ready in that round, then freeze the choice. Process same-round nodes in fixed kind/ID order, without treating a just-added same-round node as an earlier-round prerequisite. Save actual nodes, prerequisites, alternatives, rounds and choices. This is the concrete local deterministic PI1 choice, not a global preferred-proof election or a claim of optimal cost.

Grounding proves only structural availability and acyclicity for the selected finite pool. It does not establish native conversion, well-typedness of a new realization, acceptable footprint or useful mathematics. Stop at a fixed point or the declared limits. No automatic alternate-plan search or proof repair is part of this first R1 case.

## Rebind, reconstruct, and actually use both instances

For each needed original typed root, retain its exact semantic/proof-instance ID, derive its least reachable obligations under the selected `B*`, and construct a replay with exactly the restricted map. A map-root replay may equal an existing package; deduplicate it honestly. Original replays and all prior evidence remain unchanged. No old certificate is transferred into the new context; cold-reconstruct the required new coherent environment.

Let `s = B*(j)` and `r` be the other actual instance. Supply only the checked canonical names needed for the following ordinary-source consumer, with original explicit carrier/predicate/universe arguments:

\[
\forall\{\alpha:\mathrm{Type}\,u\}\{\beta:\mathrm{Type}\,v\}
\{P:\alpha\to\mathrm{Prop}\}\{Q:\beta\to\mathrm{Prop}\}
(f:\alpha\to\beta)(h:\forall a, P(a)\to Q(f(a)))
(x:\operatorname{Subtype}(P)),\quad
Q\bigl(\operatorname{val}(d(f,h,x))\bigr).
\]

The proposed proof is the direct application `r f h x`, with all implicit arguments made explicit in the source template. Native/frontend conversion must verify that the data projection of the shared map reduces to `f (val x)`. The proof route is a predeclared two-case choice of the unselected instance, not proof search or a required mathematical objective in the future network.

Capture the actual completed theorem. Require two universe parameters, exact original semantic interface/map bindings, an actual map reference in its stored type, and substantive direct use of `r` in its stored proof. After canonical export and least-closure derivation, require actual reachable `I(r)`, `A(j)` and `I(s)` with the intended edges and unchanged `p`, `q`, `j`, `d` bytes. The source names may differ; their roles must follow exact IDs. Reject a purported success if either proof becomes unused or the stored target no longer requires the shared map.

Then perform cold native reconstruction, actual inverse-native export and fresh replay, comparing the full exact canonical closure and actual type/body records. Track all dependencies and actual axiom/seed uses; no referenced proof support is erased by proof irrelevance. No in-place `.j` replacement, imported producer environment, nominal clone, theorem-to-definition reclassification or unchecked transport is allowed.

This is the existing map-preservation fact, not a novelty or efficiency claim. [REDUCE1](../../notes/analyses/CP-001H-proof-computation-and-reconstruction.md) explicitly distinguishes this favorable projection case from proof-dependent accessibility computation. A native conversion failure is an experiment result, not evidence that either original theorem is false.

## Finite execution and failure accounting

Use a new `experiments/lean-proof-context-reconciliation/` directory. Root alone launches; separate authors own native/source and finite planning code; an independent reviewer checks launch bindings and actual results. All code is snapshotted immutably before review and launch. Reuse the reviewed runner with only the declared directory/attempt-count change, separately reviewed.

The first R1 cut admits **two numbered attempts total**, each with at most six serial stages (`A0`–`A5` runner labels): bindings/tests; isolated B2 capture/replay; actual-ID preconditions and conflict control; finite planning plus checked consumer; actual export/fresh replay; final controls/audit if needed. One reviewed retry may address an implementation or source-instantiation issue; it must preserve failed evidence and explicitly record any source change. No moving target or silent budget refill.

Each stage shares at most 300 seconds wall/aggregate child CPU, 4 GiB private commit and one active child. Whole-attempt staging remains at most 256 MiB; each canonical closure at most 64 MiB. Native extension limits remain 256 rows/1024 exports, with inherited universe/DAG limits. Add finite planning ceilings of 2048 graph nodes and 8192 prerequisite/alternative incidences. The candidate pool is the specified two helper alternatives plus their finite inherited support; these caps do not authorize searching for more proofs. Every unsuccessful parse, planning, compilation, check and retry consumes the stage/attempt allowance.

Report original separate checks, conflict classification, planning/rebuild and final consumer costs separately; report retained/exploratory bytes separately from final closure bytes. A local availability or budget failure is noncompletion. All successful and failed runs remain preserved. Prepared runtime/setup and existing Gate A evidence are disclosed inputs, not free measured work.

## Decision and stopping rule

Positive means one actual source-derived, nonvacuous coexistence/reconciliation case has passed—not all proof-sensitive conversions, arbitrary foundations, broad library interoperability, discovery or useful growth. Failure is classified precisely and informs the existing PI1/REDUCE1 boundary. Either result ends this small discriminator before moving back to unknown-result discovery and useful reuse. Do not grow R1 into a general solver or an indefinite catalogue of compatibility variants.

## References

- [Completed Gate A result](../../experiments/lean-source-composition/RESULTS.md) and [audit](../../experiments/lean-source-composition/AUDIT.md).
- [PI1 prerequisite graph and finite joining](../../notes/analyses/CP-001G-proof-instance-composition.md).
- [REDUCE1 operational conversion boundary](../../notes/analyses/CP-001H-proof-computation-and-reconstruction.md).
- [Central-priority decision](2026-09-20-source-composition-qualified.md).
