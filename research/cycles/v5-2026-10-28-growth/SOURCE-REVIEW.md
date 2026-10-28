# Destructive observation updates: source review

**PASS_PAPER_ARGUMENT_AND_CORRECTED_SOURCE_FOR_ONE_ORDINARY_CHECK.** No native
compile, module import, owner operation or state/Git mutation was performed by
this review. This is not Lean acceptance, portable admission or efficacy evidence.

Reviewed `INVESTIGATION.md` SHA-256
`556d75e6b8513fb52e61250275c94829b1a02f4746eceb8304cc299efb340ab9` and:

| Source | Bytes | SHA-256 |
|---|---:|---|
| Preserved Proposed.lean | 10,464 | `ae41afeb1305f6a6f890121ead2d6be6eaadae44315b1766a01826ca3fe9203e` |
| Selected Proposed02.lean | 10,458 | `ee736d991afd9bf95b8a56d8f0555b24c6e6563c58ac02395b9f17648f42b404` |

The original has a concrete tactic error: Mode.meet_mono ends with `rw` followed
by standalone `rfl`. After rewriting, `(true && true) = true` is reflexive;
Lean 4.34's `Init/Tactics.lean:610–616` defines `rw` with an automatic reducible
`rfl`, leaving no goal for the next tactic. Independent byte comparison confirms
root's successor deletes exactly that six-byte `  rfl` line and changes nothing
else. This reviewer assistance and root correction belong to the diagnostic's
provenance; the initial source remains unchecked and preserved.

The mathematical argument is sound on paper. A disjoint mathematical subreview
agrees. Total atoms and unrestricted finite choice give an actual outcome for
every supplied input state. The minimum-outcome induction first chooses an
actual prefix outcome, then a suffix outcome from that same intermediate state;
choice selects a branch attaining Boolean meet. Lower-bound monotonicity plus
this attainment proves guarantee_iff without empty-execution vacuity.

Composition and meet preserve the order zero <= keep <= one, yielding contextual
soundness. For completeness, the hole context at the explicit false/true
observation witnesses tests both transfer-function entries. Both witnesses are
needed for the uniform criterion: constant-true observations can collapse
keep/one, and constant-false observations can collapse zero/keep. They need not
be necessary for every restricted action vocabulary. The two-state example is
nonvacuous and distinguishes skip from reset; write-then-reset exhibits a real
false outcome.

The hypotheses are exact deterministic **total**, monotone Boolean-observation
contracts. Whole-map reset fits when an empty state is supplied; arbitrary
single-key erase, observation negation, partiality, divergence and correlated
choice do not. No HashMap instantiation is supplied here. The retained dependency
is only the polymorphic `FiniteMapRefinement.Context` datatype, not a prior theorem.
The proof argument is constructive. The source introduces no axiom, sorry/admit,
unsafe/partial declaration or foreign implementation hook.

One ordinary compile of a wrapper importing the explicitly approved compiled
context module is the cheapest faithful next check. The separate route review
owns exact artifact placement/helper dependencies; public contribute would add
owner reconstruction/admission and durable publication work that this diagnostic
does not need. Ordinary compilation must not be described as an independent
receiver check or product publication.

Include `#print axioms` for `ResetEffects.minimum_outcome`,
`ResetEffects.guarantee_iff`, `ResetEffects.contextual_iff`,
`ResetEffects.skip_not_refined_by_reset` and `ResetEffects.write_then_reset_false`.
Inspect their actual closure and compiler diagnostics: no placeholder/custom
axiom should replace a proof. Imported compiled support remains explicitly
approved local code; an axiom listing does not authenticate its provenance.
Lean elaboration/import/code-generation success is still unresolved until the
single selected compile. Preserve any failure instead of expanding into a
generic proof-repair, grounding or reciprocal campaign. The investigator used
ordinary source and root assistance; this proposal establishes no index benefit,
autonomy result, novelty or causal growth-speedup claim.
