# Contextual refinement source checkpoint

Source only, 2026-10-26. No Lean execution, compilation, admission, owner/state
access, publication or growth experiment was performed. The wrapper must supply
`Std.Data.HashMap.Lemmas`, `FiniteMapEffects.Contribution` and `public section`.
`Body.lean` has no module/import preamble.

This is the scaffolded new-to-network extension proposed in the adopted parent's
DOWNSTREAM-THEORY.md, not an independently discovered research question or a claim
of historical novelty. The accepted parent is the 19-unit contribution at root
`ad4aa90b014ff326ded6f4750dd4f6ac7e3b56d15027114b91788923d0238079`.
Only the supplied public interfaces and the first 27 declaration lines of its
Body were read; upstream theorem proof bodies and native proof terms were not
read or reused.

`FiniteMapRefinement.Context` has exactly one hole, with left/right sequence and
choice constructors. `fill` substitutes a plan. `NonemptyResults p m` says all
executions return a nonempty map. `Refines p q` preserves that guarantee for every
input; `ContextuallyRefines p q` additionally quantifies over all contexts.
`ContextuallyEquivalent` is mutual contextual refinement. These relations concern
nonemptiness guarantees, not equality of output maps or inclusion of traces.

Two private Boolean lemmas prove monotonicity of OR and AND by constructor cases.
Structural context induction proves `fill_summary_mono`. The acquired
`FiniteMapEffects.nonempty_iff` then gives `refines_of_summary` and
`contextual_refines_of_summary`, without any designated empty input. The reverse
direction in `contextual_refines_iff` uses the hole context and an explicit
`e : Std.HashMap K V`, `he : e.isEmpty = true`. The nonempty-input alternative
contradicts `he`, leaving the required summary implication.

`nonrefinement_witness` assumes the failing summary pair (true, false), constructs
`NonemptyResults p e`, obtains the concrete `Exec q e e` from the acquired
`FiniteMapEffects.zero_effect_witness`, retains `he`, and disproves contextual
refinement by applying it to that same execution. `contextual_equivalence_iff`
uses Boolean antisymmetry to characterize mutual refinement by summary equality.
No classical choice, execution search, extra map lemma, or added axiom is used.

Definitions of the semantic relations require only `[BEq K] [Hashable K]`.
Semantic theorems use the parent's exact additional `[EquivBEq K]
`[LawfulHashable K]` assumptions. Contexts, fill and summary monotonicity need no
map typeclasses. Completeness, the concrete failure and equivalence take the
empty witness explicitly; callers are responsible for supplying it.

Suggested eligible definition/theorem outputs (all under `FiniteMapRefinement`):

- `fill`, `NonemptyResults`, `Refines`, `ContextuallyRefines`,
  `ContextuallyEquivalent`;
- `fill_summary_mono`, `refines_of_summary`, `contextual_refines_of_summary`,
  `contextual_refines_iff`, `nonrefinement_witness`,
  `contextual_equivalence_iff`.

The `Context` concept must travel as its complete inductive group; it is not a
definition/theorem target of the automatic contribution-target interface. There
are 15 hand-written core declarations counting its group once: one inductive,
five definitions, three private Boolean lemmas and six public theorems. Generated
eliminator/equation helpers may add units. This is an estimate, not an exported
closure census or a claim that the 32-unit/4-MiB gate has passed. Proofs use only
small constructor cases, structural induction and explicit applications; no
general tactic automation is invoked. Root owns the later bounded ordinary
source-project execution, exact closure/admission check and adoption decision.
