# Shared vocabulary: smallest existing arithmetic reuse seam

Decision: use existing exact-module imports; no foundation/policy/checker/global-ID/new-API change.
Source-only against current109 `experiments/v5-local-checks/distribution-coherent-01-input.json`.
No execution, proof production or public mathematical admission is claimed here.

## Identity and source spelling

Select one vocabulary module M; its identity is its exact content-derived ID.
Its imported type is `DMKN.Mod.«M».Nat`, not the frontend's builtin `Nat`.
Here M is a placeholder for that actual ID, not a literal Lean namespace.
`Nat.zero`, `Nat.succ`, `Nat.rec` and `Nat.add` use the same qualified prefix.
`codec.relocated_name` and `AuthorLean.absoluteName` already implement this.
Two children referring to M use precisely the same constants; a new capture
of builtin Nat in each child would instead create distinct relocated types.
There is no claim that independently defined natural-number types are equal.

Fully qualified names suffice. A local notation or spelling helper is optional
ergonomics and must expand to these exact names; it is not a semantic bridge.
Do not introduce an `OfNat` instance or builtin numeral automation for this step.
The new literal lowering handles captured builtin Nat, not arbitrary acquired
Nat; use imported zero/successor explicitly in shared-vocabulary source.

## Existing end-to-end path

1. Discover a vocabulary candidate through an authorized index, or select an
   explicitly supplied exact ID. Generic structural search is not selective at scale.
2. `SemanticReadPlan.stage/select_member/resolve/fetch_body/preview` stages
   exact evidence, complete inductive groups and required semantic bodies.
   `finish` admits selected evidence and constructs a live author context.
3. Existing `import_context/extend_context` also exposes this same selection
   directly. A retained packet is data; fresh owners still perform admission.
4. Author source referring to M's qualified constants with `client.author`.
   `AuthorLean` stops export at imported boundaries; `MixedSourceOperation`
   encodes these names as external `(M, relative_name)` references. M's Nat
   closure is not recaptured as the child's local declarations.
5. Admit the resulting packet and `publish` it with retained semantic material;
   subsequent agents can discover and reuse that new contribution.

Select needed group openings within M, not every declaration for authoring.
Complete inductive groups and any transitively demanded definitions/rules are
still necessary. A smaller newly produced seed would change identity and cost;
do not produce one merely to avoid selecting within the existing module.

## Substantive, numeral-free successor

Let N, add, zero and succ abbreviate M's exact constants in this paragraph only.
Target: forall a b c : N, add a (add b c) = add (add a b) c.
For the captured recursion-on-second-argument addition, induction on c gives
the zero case by reduction and the successor case by congruence of succ over
the induction hypothesis. Use explicit M.Nat.rec and fixed equality terms, not
unregistered imported tactics/typeclasses. This adds no numeral dependency.
Resolve the exact add body/rules before authoring; do not infer equations from
the human-readable name. Final unchanged native checking must confirm the term.
This is arithmetic reuse, not measured net growth or selective-scale discovery.

## Proof and semantic costs must not be conflated

Interface-only mode cannot compute with absent bodies. Use the existing demand
loop, or an available opaque theorem
interface whose proof body is not needed to apply it. Recursor rules still matter.
The current arithmetic smoke is a zero-parent native witness, NOT an I receipt.
Existing mixed packets allow empty claims/frontiers and a zero-parent delta;
the receiver already checks this, under configured I/A trust-owner supervision.
It yields a live mixed warrant only after the actual receiver call succeeds.
No new receiver mode is required, and a saved native report is not that warrant.
Frontend ancestral theorem-proof bytes can be zero while onward mixed packets
retain every selected uncertified delta ancestor. Fresh cold receivers recheck
that native closure. Existing true-I BASE/Tree supplies the separate certified
no-proof-replay route; it does not certify this new Nat module by analogy.

## Next action and stop rule

After root adopts the saved smoke outcome, select only the existing public
native-packet admission/import plus qualified-arithmetic successor seam above.
No new producer budget is justified merely by this note. Require the child's
captured refs to target M and no local Nat duplicate, correct fresh admission,
and explicit cold native-ancestry accounting. Keep true-I evidence separate.
If source refuses, fix the precise import/export obstruction; do not expand
into numeral convenience, equivalence search or another general API redesign.
