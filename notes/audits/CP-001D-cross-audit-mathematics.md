# CP-001D independent mathematical-profile cross-audit

Date: 2026-09-19. Reviewer: network/preservation specification agent, independently reviewing the mathematical author's draft. Scope: concept and interface consistency, practical Lean compatibility, complete native replay, typed roots, and negative-evidence transport. This is a paper/source audit, not implementation qualification, a mechanized metatheorem, or a successful Lean replay run.

Reviewed artifact: [Operational corpus mathematical profile](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md).

Reviewed SHA-256: `949E0428ABBFDB6637CF087F6FB518206309B3E0DA7D13B4C73CA99D07D6926E`.

Interoperating network draft at this review: [NET1](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), SHA-256 `46529C8040D8D58F9CB6C27FB4DBC148C525AFC0B0FCCA49788A71FD2136871B`.

## Conclusion and exact strength of the result

The revised draft specifies a coherent conditional native-admission route: inert exact data, locally fixed foundations, complete selected replay closure, receiver reconstruction, and checked declaration insertion. No additional unchecked mathematical-admission path was found in the reviewed paper contracts and selected source excerpts. The practical profile addresses structures, projections, opaque declarations, and native mutual/nested induction rather than presenting the six-seed demonstration profile as a sufficient real-library interchange format.

This finding is conditional and deliberately narrower than practical readiness. The profile's canonical bootstrap bytes, complete reserved-name inventory, exporter, verifier adapter, generated-member reconstruction, and representative library examples have not been implemented or qualified here. The audit does not establish universal Lean/mathlib compatibility, correctness of the Lean kernel, completeness of the new codec, mathematical invention, or any throughput/durability measurement.

## Reviewed argument boundaries

For a selected profile L, typed root r, and exact ReplayManifest R, the intended acceptance argument is conditional on at least:

- binding canonical content identities and complete, correctly reconstructed references;
- correct decoding, scope/universe handling, generated-name construction, and native declaration adaptation;
- the locally adopted foundation and soundness of the native checking/extension rules actually used;
- correct dependency/axiom-footprint extraction, local policy, resource isolation, and admission state;
- possession of the complete exact closure needed by that replay, rather than merely a proof ID or remote positive status.

Under those premises, a proof root establishes its exact contextual judgment relative to that checked basis. A definition, group, or opaque root establishes its own checked declaration relation; it is not converted into a theorem because the surrounding protocol expects a proof-shaped record. Alternate proof selection belongs to ReplayID and must not silently change a ProofID's identity or eliminate a receiver's footprint check.

The practical safe-extension argument is correctly distinguished from the core profile's proof-only auxiliary-substitution argument. An added inductive type cannot simply be described as an inlined definition. Conversely, bound recursion inside one native checked inductive group is not an unsupported cross-artifact theorem-support cycle.

## Findings and repaired dispositions

| Finding | Why it matters | Disposition in reviewed revision |
|---|---|---|
| Opaque reconstruction lacked one centralized exact generated-name rule | An independent adapter needs an unambiguous name mapping and declaration metadata, not an inferred extension of the definition/theorem mapping | Repaired: `DTMKN.o.<fullOpaqueID>`, safe `opaqueDecl`, and `all = [generatedName]`; central native-name paragraph now includes this kind |
| Parser result reconciliation named judgment/ProofID unconditionally | Group, construction, and opaque roots have no native proof/judgment projection merely by being accepted declarations | Repaired: stage 8 binds the typed root and kind-appropriate optional JudgmentID/ProofID |
| NativeRefutation envelope had no authorized NET1 retrieval path | The network permits exact Replay-root closure reads; an annotation outside that closure cannot become fetchable by inventing generic incident-CAS access | Independently reproduced during review and jointly repaired with the organization author: publish the ordinary negative proof's ReplayID; derive/check the scoped opposition relation locally; annotation storage remains bounded and has no independent public root/read authority |
| Same-context opposition must not be conflated with a faulty derivation | Both Gamma |- phi and Gamma |- not phi can be sound when Gamma is uninhabited; unconditional invalidation would corrupt conditional mathematics | Revised semantics reviewed as correct: exact contextual opposition is searchable information; a closed contradiction needs its own checked composition under a compatible joined basis before local basis-incident policy applies |

These are design/interface corrections, not measured implementation defect rates. The NativeRefutation relation reconstruction retains the exact telescope, universe parameters, and recomputed SemanticContext; it must not create an opposition edge merely from similar text or from a counterexample to a differently quantified proposition.

## Practical Lean checks against pinned source excerpts

The inspected source target is Lean v4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. This review inspected targeted relevant portions, not the entire upstream codebase.

- `Declaration.lean` has an opaque declaration carrying an actual value, unsafe flag, and declaration-group metadata. Its `mutualDefnDecl` variant explicitly says all definitions must be unsafe or partial. The proposal's separate checked safe opaque path and exclusion of this mutual-definition variant are consistent with those interfaces; source recursion lowered to safe acyclic declarations is a different case.
- `environment.cpp` has a checked opaque insertion path as well as separate checking control. An opaque type signature alone is therefore not the proposed evidence: the body must be present and checked. Naming the API does not prove that an eventual adapter always selects the checked path.
- `inductive.cpp` constructs recursor information and restores native nested-inductive declarations/auxiliary recursors from its checked transformation. This supports the proposal's regenerate-and-check boundary, not a path that trusts publisher-submitted recursor metadata. The actual descriptor/exporter round trip remains a qualification obligation.
- `type_checker.cpp` contains name-sensitive natural-number reduction and string-literal expansion behavior. `Prelude.lean` provides the logical models for native arithmetic and the `String`, `Char`, and `Char.ofNat` support used by literal reconstruction. This validates the need for exact locally frozen reserved-name bootstrap declarations: blindly renaming all constants or allowing arbitrary publisher definitions at those names would not preserve the intended native interpretation.
- The proposed exporter operates outside acceptance. If earlier source proofs collapse to one JudgmentID and induce an artificial selected-witness self-edge, expanding a prior complete proof or selecting its earlier witness is a checked-term transformation; bypassing the replay cycle check would not be an acceptable remedy. The revised document makes this resource-sensitive distinction explicit.

## Release gates that remain real, not cosmetic

Before a practical implementation can claim conformance, it must produce and independently inspect the complete selected seed descriptors, generated export inventory, actual source/profile/executable bindings, and reserved-name coverage. The historical source pin is not a substitute for those bytes.

Native compatibility also requires actual checked round trips for dependent telescope/universe mapping, structures and projections, group-local indexes, generated mutual/nested recursors, safe opaque bodies, strings, primitive quotient behavior, and the explicitly permitted axiom footprint. A representative pinned mathlib slice must retain all selected theorem/opaque bodies. Unavailable values, excluded compiler-trust axioms, or unsupported profile features must fail with precise bounded outcomes rather than fall back to foreign `.olean` import, source execution, or new axioms.

Finally, realistic dependency-closure size, bootstrap cost, checking cost, and proof-expansion cost must be measured. A logically eligible proof can still exceed a receiver's finite import/check envelope. This is an explicit compatibility/resource result, not a refutation or permission to weaken evidence checks.

## Sources inspected

- [Pinned Lean Declaration.lean](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Lean/Declaration.lean): opaque and mutual-definition interfaces, value availability, inductive/group metadata.
- [Pinned kernel environment.cpp](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/environment.cpp): checked opaque/declaration dispatch.
- [Pinned kernel inductive.cpp](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/inductive.cpp): native recursor generation and nested-declaration restoration.
- [Pinned kernel type_checker.cpp](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/type_checker.cpp): reserved arithmetic names and string-literal behavior.
- [Pinned Init/Prelude.lean](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Init/Prelude.lean): logical arithmetic models and String/Char support.

No source compilation, executable conformance test, native proof replay, or formal verification was performed by this audit.
