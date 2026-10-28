# Source correction after observation-modes-check01

Check01 remains **FAILED; no new endpoint was accepted**. Saved stdout
(`experiments/v5-local-checks/observation-modes-check01/command/stdout.txt`,
5,921 bytes, SHA-256
`89b8ea274ca5495a319b23408093be8d7003532eae20bf4805820c408700785b`)
reports successful axiom-free import of `FiniteMapRefinement.Context`, source
errors, and `sorryAx` in all five proposed endpoint listings. The separate
CHECK01-OUTCOME audit owns full execution/closure accounting.

I made a mistaken inference in SOURCE-REVIEW.md: I treated `rw`'s attempted cheap
reducible reflexivity step as guaranteed to close `(true && true) = true` here.
Actual diagnostics show that exact goal remained. Deleting the following `rfl`
was wrong and introduced an additional proof-script defect. The original source
was right at that line. This note supersedes that specific assertion, without
editing the frozen review, Proposed.lean, Proposed02.lean or failed run. The
other reported source errors were independent of that mistaken deletion.

Root selected this fresh, still-unchecked successor:

| File | Bytes | SHA-256 |
|---|---:|---|
| Proposed03.lean | 10,496 | `4743094ebb82157bff58c0131c52592911672909c522e58b0efae3c747d2754a` |

Its exact diff from Proposed02 (`ee736d99...`) contains only:

1. Restore standalone `rfl` after the two Boolean rewrites in Mode.meet_mono.
2. Add `include atomic_law` immediately after the section-variable declaration.
   The law occurs only in the proofs of execution_lower_bound, minimum_outcome
   and guarantee_iff, so Lean omitted it from their declaration context and
   emitted unknown-identifier errors. Including it retains the intended explicit
   premise and fixes the resulting call-arity mismatch in later proofs. The scope
   ends at the existing `end Semantics`; it adds no axiom or stronger assumption
   than the mathematical argument already states.
3. Spell the three concrete evidence arguments as `Exec.atom Mode.zero` or
   `Exec.atom Mode.one`. The original dotted constructors had no inferred action
   type at those applications. The theorem statements and selected actions are
   unchanged.

No definitions, execution rules, observation witnesses, theorem conclusions,
import requirements or proof strategy changed. Relative to the original source,
only the explicit section-premise retention and three constructor qualifications
remain. No sorry/admit, axiom, unsafe declaration or replacement assumption was
introduced. The source-only byte/diff check does not establish elaboration success.

Proposed03 and this correction are ready for independent exact-diff review.
No new native check, import, owner/state operation or Git action was performed
while preparing them. A subsequent check requires root's fresh finite selection;
the earlier failure and costs remain preserved. This is an assisted source repair,
not a discovery-tool or autonomous-efficacy result.
