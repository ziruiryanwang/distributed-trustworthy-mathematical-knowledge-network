# CP-001E: pinned Lean/mathlib source-scale evidence

Date: 2026-09-19  
Method: Read-only inspection of official public repository metadata and source text  
No source compilation, native extraction, software implementation, or benchmark was performed

## Security correction and current candidate

The original observations below concern a historical source release, not a recommendation to deploy its kernel. The [foundation-security audit](CP-001E-foundation-security-audit.md) withdraws Lean v4.22.0 from deployment candidacy and selects Lean v4.34.0 at `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` for fresh qualification.

The matching official mathlib v4.34.0 tag resolves to `5ed2965256430c3649e86755f9576b54eca72435`; its lean-toolchain is exactly `leanprover/lean4:v4.34.0`. A new exact recursive-tree response reported `truncated: false`. With the same Mathlib/*.lean blob filter, it contains **8529 source blobs totaling 98,449,500 bytes**. The largest is `Mathlib/MeasureTheory/Integral/IntegralEqImproper.lean`, 78,084 bytes. These are source-tree observations, still not theorem counts, extracted proof sizes, or replay measurements.

New qualification targets use this corrected pinned release. They must rederive the bootstrap and reserved-name interpretation, not copy v4.22 descriptors under a new label. Historical source observations remain useful evidence of scale and producer tooling, but are not mathematical acceptance certificates.

## Historical authoritative observations

The official mathlib4 tag v4.22.0 resolved to commit

`79e94a093aff4a60fb1b1f92d9681e407124c2ca`.

The lean-toolchain file at that release contains exactly:

`leanprover/lean4:v4.22.0`.

This establishes an actual matching library release for CP-001D's chosen historical Lean target. It does not establish that the proposed new native exporter has imported that library.

The GitHub recursive tree response at that exact commit reported `truncated: false`. Among blob entries whose path begins Mathlib/ and ends .lean:

| Source-tree quantity | Observed value |
|---|---:|
| Matching Lean source blobs | 6726 |
| Sum of their reported source-byte lengths | 77,230,502 |
| Largest matching source blob | Mathlib/Analysis/Analytic/Basic.lean, 77,493 bytes |

The filter is a source-file filter. It does not count theorem declarations, native expression nodes, mathematical CIDs, selected proof witnesses, generated helpers, or a theorem's transitive native closure. Files outside Mathlib/, bundled dependencies, tool binaries, and compiled module data are not included in that sum.

## Selected source observations

The pinned Mathlib/Algebra/Group/Defs.lean source imports ordinary mathematical modules and tactic-support modules, including Mathlib.Tactic.MkIffOfInductiveProp, Mathlib.Tactic.OfNat, and Mathlib.Tactic.Simps.Basic.

Mathlib/Algebra/Group/Hom/Defs.lean imports Mathlib.Algebra.Group.Defs, Mathlib.Algebra.Notation.Pi.Defs, Mathlib.Data.FunLike.Basic, and Mathlib.Logic.Function.Iterate. Its source contains homomorphism structures, classes, instance declarations, and theorem definitions.

Mathlib/Data/List/Basic.lean imports mathematical/list infrastructure and Mathlib.Tactic.Common. Its source contains list instances and lemmas.

This was line-oriented source inspection, not parsing the full declaration grammar. Documentation comments and examples can also contain declaration-looking lines; no declaration count was inferred from the search.

These observations matter because ordinary user-facing mathematical libraries rely on elaboration conveniences and source tooling. They do not imply that every imported source module, tactic, or executable belongs in the receiver's mathematical proof closure. The native exporter must derive the actual required declarations and evidence, not blindly trust a source import graph or execute the producer's toolchain on the receiver.

## Implications for qualification

The intended product cannot establish realistic usefulness solely by replaying a tiny seed plus reflexivity examples. The corrected matching source release above supplies the current concrete qualification target; the historical release established the same kinds of product obligations:

- common algebra structures, instances, and homomorphisms;
- ordinary list theorems and their actual generated/helper declarations;
- later slices exercising quotient/classical/dependent/nested constructions;
- independent native closure extraction, transfer, reconstruction, and checking with complete proof bodies.

A slice is not a substitute for the whole intended ecosystem: scope must expand, and every unsupported feature must be named. Conversely, forcing the entire source repository into every proof closure would be an avoidable and unsupported design choice.

The 77,230,502-byte source sum cannot establish either that NET1's closure cap is sufficient or that it is violated. Native body sizes and selected dependency closures can differ greatly from source sizes. Only actual qualified native extraction can resolve that empirical quantity.

The source evidence changes the next work item from “find whether a compatible library release exists” to “qualify the selected inert data path against exact representative declarations from this release.” Implementation remains unauthorized; concept work can specify that path and its failure conditions without claiming it has run.

## Reproducibility and sources

- [Corrected matching mathlib v4.34.0 tree](https://api.github.com/repos/leanprover-community/mathlib4/git/trees/5ed2965256430c3649e86755f9576b54eca72435?recursive=1).
- [Corrected matching lean-toolchain](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/lean-toolchain).
- [Official mathlib4 v4.22.0 tag reference](https://api.github.com/repos/leanprover-community/mathlib4/git/ref/tags/v4.22.0).
- [Exact recursive repository tree](https://api.github.com/repos/leanprover-community/mathlib4/git/trees/79e94a093aff4a60fb1b1f92d9681e407124c2ca?recursive=1).
- [Pinned lean-toolchain](https://github.com/leanprover-community/mathlib4/blob/79e94a093aff4a60fb1b1f92d9681e407124c2ca/lean-toolchain).
- [Pinned group definitions](https://github.com/leanprover-community/mathlib4/blob/79e94a093aff4a60fb1b1f92d9681e407124c2ca/Mathlib/Algebra/Group/Defs.lean).
- [Pinned homomorphism definitions](https://github.com/leanprover-community/mathlib4/blob/79e94a093aff4a60fb1b1f92d9681e407124c2ca/Mathlib/Algebra/Group/Hom/Defs.lean).
- [Pinned list basic source](https://github.com/leanprover-community/mathlib4/blob/79e94a093aff4a60fb1b1f92d9681e407124c2ca/Mathlib/Data/List/Basic.lean).

The tag is recorded alongside its resolved immutable commit so that later tag movement would not silently alter this observation. GitHub metadata correctness and access are premises of this source-tree observation, not premises of native mathematical validity.
