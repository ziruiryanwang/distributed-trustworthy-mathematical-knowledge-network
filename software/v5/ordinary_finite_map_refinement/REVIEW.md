# Contextual refinement: independent source review

2026-10-26. `kernel_package_audit`.

**PASS_SOURCE_ARGUMENT; ELABORATION_AND_ADMISSION_NOT_RUN.** Reviewed actual
Body.lean, 6,812 bytes, SHA-256
`3c965c818395db4d2f20b1abcfbdf6dbe972a492b63f325b00789ccf33572f7c`,
and PROOF.md, 3,703 bytes, SHA-256
`9e88168733d3fa13c1f6c55421c9144fe4c33427d02b93f6b07707e393e05f45`.
Compared statements and applications with accepted upstream public interfaces;
upstream proof bodies were not reread or reaudited.

Context's five constructors represent exactly one hole. `fill` preserves the
plan's key/value types and substitutes recursively in the correct left/right
positions. Universes remain polymorphic. Context, fill and summary monotonicity
need no map instances; semantic definitions require BEq/Hashable, and semantic
theorems use the upstream EquivBEq/LawfulHashable assumptions. No Inhabited
assumption or implicit empty-map lemma is introduced.

The refinement orientation is correct: guarantees of `p` imply guarantees of
replacement `q`. It concerns universal nonemptiness, not equal maps or trace
inclusion. Each Boolean monotonicity branch proves the required implication;
mutual implication proves Boolean equality. Context induction uses OR for both
sequence positions and AND for both choice positions, with the fixed argument
related reflexively. The goals reduce definitionally through fill/mustWrite.

`refines_of_summary` correctly transports the two alternatives of nonempty_iff.
Its contextual version applies the context-summary induction. Completeness
chooses the hole and explicit empty witness: `he.symm.trans hem` has type
`true = false`, so Bool.noConfusion eliminates precisely the impossible branch.
The equivalence proof applies completeness in both orientations; its reverse
direction transports summary equalities in the correct directions.

The negative theorem supplies an actual `Exec q e e` through the acquired
zero_effect_witness, retains `e.isEmpty = true`, proves the source guarantee,
and contradicts contextual refinement using that same execution. It is a
constructive witness rather than mere failure of a decision test. No new
HashMap theorem, classical choice or execution-search dependency is needed;
remaining helpers use ordinary Boolean/equality eliminators.

No deterministic source error or likely elaboration mismatch was identified.
The 15 handwritten core declarations are not an actual closure census; generated
helpers, native checking and resource fit remain runtime obligations. This source
implements refinement/equivalence criteria and a witness theorem, not the proposed
quotient algebra or a packaged decision API.

The header/PROOF's named imports describe one wrapper route. The actual Body has
no preamble and is mathematically usable with either those module imports or
reconstructed exact upstream declarations in scope. This clarification selects
neither route and does not certify their operational integration.

Only source/document reads and hashes occurred; no source edit, Lean/product
execution, owner/database operation or Git mutation was performed.
