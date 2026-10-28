# Refinement contribution01: executable-inductive support failure

2026-10-28. Saved-data and source audit only; no product import, database open,
native rerun, Git or old-file edits. The contribution is **FAILED in AUTHORING**,
with accepted=null and no candidate, admission report or successful result.

The actual request uses parent
`ad4aa90b014ff326ded6f4750dd4f6ac7e3b56d15027114b91788923d0238079`
and authoring frontier
`b75b2800b956aedbbb9c333806a7b369f3213442634482c1e3818137fefac6a6`.
Its V3 header carries 581 basis rows, six frontier labels, two acquired targets
and 11 groups. Acquired evidence totals 232,441 bytes. Construction read 971,618
raw bytes, reached 609 labels with 22 introduced names and checked nine units.
The log reports both intended imported signatures, nonempty_iff and
zero_effect_witness, and CONSTRUCTED_READY_FOR_AUTHORING_INSTALL. Thus the
selected frontier traversal and inherited mathematical construction completed.

The first subsequent diagnostic is:
`FiniteMapEffects.Plan was not compiled; compileDecls must run on inductive types first`.
It occurs while elaborating the new Context inductive, whose constructor fields
contain Plan. Later fill pattern-match failures, downstream type mismatches and
SORRY_REFERENCE are retained; they do not establish independently incorrect
theorems or successful elaboration of the refinement.

Pinned MutualInductive.lean calls Lean.compileDecls immediately after adding the
new inductive and before generating its auxiliary constructions. LCNF.Main then
eagerly invokes compileInductives before its deferred-function compilation branch.
That path needs runtime layout metadata for Plan, whereas the inherited kernel
declarations were reconstructed for mathematics. This is not an actual-parent
kernel rejection, failed ancestral replay or mathematical acceptance. The clean
authoring gate correctly stopped before binding/admission of the new refinement.

Outer wall is 6.2910984 seconds. Job CPU 5.09375 plus wrapper 0.546875 gives
5.640625 known CPU seconds; nested figures are not added again. Authoring and
outer child exit 1 with no termination request, zero final active processes,
closed/reaped Jobs and empty cleanup errors. No successful admission is claimed.

| Evidence | SHA-256 |
|---|---|
| selection | `ff76781b12f25c5a30e1f96b0df7440c745f5298c935242b0a4879a506a97deb` |
| used BodyMath.lean | `276e64eada849a8ed46a23b6ceee122124ef99c0b91a57fdd97b619de3708b89` |
| outer RESULT.json | `014dc7882e4c47957e6bff800093be0062f256e5c8a2a041e3f57c4c564d095c` |
| contribution FAILURE.json | `53ee2953ba6afb7f724c385efb852da77327842e018a5934379a8792ac66f1ef` |

A math-only modifier or deferred-function compilation option cannot bypass this
eager inductive path. The source-level proposal is to parameterize Context over
an arbitrary payload A, then specialize it to Plan K V in the existing
noncomputable fill and mathematical theorems. This moves no kernel checking
boundary and can avoid requiring Plan's executable layout for the new inductive.
Its exact source delta still needs independent review; no run is selected here.
