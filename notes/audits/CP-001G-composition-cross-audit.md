# CP-001G independent audit: proof-instance composition

Date: 2026-09-20. Auditor: `commons_reciprocity`, independently of the PI1 author. Scope: concept/specification, mathematical arguments, exact representation boundaries and read-only pinned-source evidence. No code, Lean execution, extraction, native replay, test, exploit or benchmark was performed. CP-001F and earlier checkpoints remain unchanged.

## Audited revision and bounded verdict

Read [CP-001G proof-instance composition](../analyses/CP-001G-proof-instance-composition.md) in full, including its F4 migration and proof-root consumer amendments. Audited SHA-256:

`B76AF1B40ABEE6ADA192E4C8A2B6DA22AC4436C0EC8B66FE94CCD3F3B3F21102`.

No blocking contradiction was found in this revision's finite source-rank argument, S/I/A dependency distinction, semantic-versus-witness grammar, or contextual validation/footprint contract. The proposed representation addresses cases excluded by the prior unchanged-background capsule rule without declaring different nominal groups equal.

This is a conditional paper result, not a claim that broad Lean/mathlib interchange already works. The most important retained obligations are complete source evidence, qualified native reconstruction and group generation, actual final checks under the chosen representatives, and explicit failure on incomplete support or exhausted resources. The proposed foundation remains a preimplementation candidate, not a qualified installed system.

## Identity and foundation boundary

PI1 selects a new NativeRules code 4 and consequently a new FoundationID F4. It does not reinterpret rule code 3 or relabel F3 semantic bytes as F4 content. Within one F4, changing selected proof representatives does not change an otherwise exact semantic descriptor's bytes or identity. Across F3-to-F4 migration, all foundation-dependent identities and references are re-expressed and checked.

That distinction resolves a possible ambiguity in the phrase "unchanged interface": unchanged within a fixed F4 proof-selection problem is not unchanged across foundations. The migration paragraph now names the source/target foundation, explicit seed correspondence, changed referenced IDs and new independent replay. Old certificates do not cross that boundary.

The audited exact new types are WitnessTermDAG `0x0022/1`, ProofInstance `0x0023/1`, RepresentativeMapNode `0x0024/1`, InstanceReplay `0x0015/3`, InstanceModule `0x0016/3`, and InstanceOpposingEvidence `0x0017/3`. A replay proof root is `[4,ProofInstanceID]`, not the old `[0,ProofID]`. Semantic theorem references remain `[2,JudgmentID]`. These tags belong to their explicitly different surrounding grammars; the witness constant-reference tag 7 is not the native expression tag 7 for a literal.

The added proof-root consumer table names the corresponding typed-record changes and negotiation boundary. This audit checked its consistency with PI1's own mathematical grammar. It is not an independent exhaustive audit of every integrated network opcode or every v4 registry row; those bindings remain the integration author's responsibility.

## The two term grammars are genuinely separate

Every theorem occurrence inside a witness expression uses an exact proof-instance reference. This includes lambda domains, forall domains, let annotations and other expression children, not just the final proof-producing subterm. A reference denotes the closed theorem type at the explicit universe vector, and ordinary native applications supply telescope arguments.

Semantic judgment/telescope/type, definition type/value, opaque declaration and group descriptors instead retain semantic JudgmentID references. Those references require checked canonical aliases realized through B. Following an ordinary declaration from a witness expression does not turn that declaration's internals into witness grammar.

This separation is essential. Replacing JudgmentIDs with ProofInstanceIDs inside every semantic descriptor would reintroduce proof-dependent definition and group identities. Conversely, retaining JudgmentIDs inside witness annotations would lose the exact source proof-instance edges that PI1 is intended to preserve.

The note also correctly distinguishes closure operations. A witness body under a nonempty telescope is closed once with the corresponding lambdas. A canonical alias body is the already closed constant `w(B(j))` at its universe vector, not that constant incorrectly wrapped/applied a second time. The ordered telescope and universe list remain part of the judgment identity.

## Statement lookup is not an inhabitation obligation

The dependency node sorts have different meanings:

- `S(j)` checks the descriptor and referenced meanings of the statement.
- `I(p)` checks one actual proof instance, requiring `S(target(p))` and all actual witness/ordinary references.
- `A(j)` materializes a semantic theorem constant using `I(B(j))`, and therefore requires both that proof and the exact statement.

There is no general edge from `S(j)` to `A(j)`. Such an edge would ask for a proof of a proposition merely to inspect the proposition and would restore the old artificial root cycle. A theorem constant actually occurring in j's telescope/conclusion does require the alias for that referenced theorem; that is a different edge.

The repeated-True example is consequently coherent: a later proof b can refer directly to the earlier instance a while the root target remains the same j and B is empty. When a proof occurs inside another statement, its semantic alias obligation is retained. The displayed `a`, `c : a = a`, `b` example uses both mechanisms rather than suppressing annotation/type dependencies.

## Expanded verification of the earliest-rank construction

Assume precisely the note's premise: a finite complete supported source graph, with all external dependencies earlier in a topological order after admitted native groups are treated atomically. Hashes identify exact canonical bytes under their binding assumption; no arbitrary semantic-equivalence quotient is used.

For each semantic descriptor, take its earliest source occurrence rank. For each distinct proof-instance object, take its earliest emitting source-theorem rank. Refine the order at one source-theorem rank so that its statement descriptor precedes its instance, which precedes the canonical alias realized by that instance. A declaration/group uses its earliest matching supported source occurrence and its actual external prerequisites.

Each required edge then decreases this refined order:

1. A semantic descriptor's external reference came from an earlier actual source declaration. Choosing the earliest exact-equal semantic occurrence can only move that reference earlier.
2. A witness's direct instance reference came from an earlier source theorem. Exact deduplication can again only decrease the referenced rank.
3. `I(p)` requires `S(target(p))`. The statement's earliest occurrence is no later than p's source occurrence; if equal, the local refinement puts S first.
4. `A(j)` requires the earliest proof instance of j and its statement. Both precede A in the refined order.
5. The earliest proof of j cannot have an earlier source dependency on another source theorem of the same j while also being the earliest such source theorem. Thus it cannot acquire a self-supporting alias choice through that alleged predecessor. More generally, all its real descriptor/witness dependencies decrease the same order.

Every external prerequisite therefore precedes its user. A finite graph with that ranking is acyclic. Restricting to an exact root-reachable closure preserves acyclicity. This verifies the note's claimed existence of a structural materialization plan for the stated source premise.

Three limits are essential. Source textual order is not enough if the actual generated dependency graph differs. Complete source names/types without bodies are not the assumed graph. Acyclicity proves neither native well-typedness of the transformed terms nor affordable kernel execution. PI1 retains independent checks for those obligations rather than accepting the ranking as theorem evidence.

## Independent branches and grounded choice

The finite AND/OR argument is appropriate for structural planning. Fixed descriptor/instance nodes require all prerequisites. An alias requires its statement plus one available exact-target proof instance. The monotone sequence of grounded sets stabilizes after at most V strict-growth rounds because every such round adds at least one of the finite V candidate vertices.

For any supplied acyclic branch whose required alternatives occur in that graph, induction over the branch's topological order places all its vertices in the fixed point. Adding candidates does not remove already groundable vertices. The claim concerns this fixed finite structural graph; it does not assert unrestricted discovery across the network.

Selecting a witness only after it is grounded gives a direct topological certificate for the selected edges. Freezing the chosen alias avoids a later replacement introducing a cycle into that plan. The paper P_A/Q_B example correctly distinguishes a cyclic arbitrary union from a grounding order that retains the independent base proofs.

Already checked base units must retain their actual compatible support/context obligations; "base" cannot hide an old incompatible representative assignment. PI1's environment-compatibility and final cold-replay rules provide that condition. Untrusted proposed alternatives may participate in planning but receive no acceptance from grounding. A first-ready invalid, resource-expensive or policy-inadmissible choice can still require rejection or a separately funded re-plan. The note explicitly acknowledges those outcomes.

## Proof irrelevance: source evidence and limits

Independently read the pinned Lean kernel source at commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.

`src/kernel/type_checker.cpp:932–938` implements the cited proof-irrelevance check by inferring the first term's type, requiring it to be a proposition, inferring the second term's type and checking their definitional equality. The main conversion path calls it at 1202–1203. This supports the rule used by the note: proofs of the same convertible proposition can be compared by definitional proof irrelevance in the qualified native setting.

`src/kernel/environment.cpp:192–208` implements checked theorem insertion. When checks are enabled, it checks the constant declaration, proposition type, absence of metavariables/free variables in the closed value, value typing and conversion against the declared type. PI1's independently checked native theorem instances and aliases agree with this source-level route. Merely calling an insertion path with checking disabled would not meet the contract.

Under the stated coherent-environment premise, congruence/conversion supports replacement of proof-valued subterms in dependent expression contexts. The proposition types must actually be checked convertible; proof irrelevance does not identify arbitrary types, data values or independently cloned nominal groups.

This source inspection is not a proof of all kernel metatheory or a universal source-to-content preservation theorem. In particular:

- It does not permit erasing the replaced proof's actual selected support or assumptions from footprint accounting.
- It does not show equal conversion cost, equal reduction traces or transferable cross-environment caches.
- It does not make native theorem declarations and opaque declarations operationally interchangeable. PI1 selects native theorems for both instances and aliases and preserves actual opaque declarations separately; proof-computation/accessibility-recursion cases remain a practical qualification obligation.
- It does not qualify frontend plugins, source elaboration, name-sensitive syntax or generated inductive interfaces.

The draft already makes native checking the decision boundary. These are retained qualification boundaries, not newly identified unsound acceptance paths.

## Why nominal interfaces can remain unchanged within F4

For a selected F4 descriptor set, B affects the checked bodies/support of canonical theorem aliases. Ordinary semantic definition/group syntax still refers to the same semantic IDs. The receiver reconstructs each group once at its exact canonical names and checks its qualified generated interface. It does not construct two nominal copies and appeal to proof irrelevance to equate them.

Consequently the proposed remedy for proof-bearing data is materially different from recursively replacing theorem references by new opaque capsules. The latter changes definition descriptors and can propagate changes into a group descriptor; PI1 keeps those semantic references and records their realization separately. If two developments already have different exact GroupIDs, PI1 does not merge them. Any useful cross-interface transport remains BRIDGE1's job.

The argument is conditional on the exact supported native reconstruction and descriptor qualification. It is not a promise that changing representatives leaves all existing native environment certificates valid.

## Footprints, certificates and pooled costs

The actual footprint includes witness bodies, checked alias bodies, statement/telescope references, semantic type/value dependencies, regenerated group support and admitted seed/rule uses. PI1 does not equate proof irrelevance with support irrelevance. The same ProofInstanceID can have distinct accepted replays and footprints under B_1 and B_2 because its semantic dependencies realize their aliases differently.

Its certificate and environment rules correctly require actual reached representative compatibility. An installed `A(j)` with body p is not relabeled as one with body q because both prove j. Conflicting changes require a coherent rebuilt/forked environment and affected checks. A source importer that happens to coalesce native theorem records is not an alternative compatibility authority.

The pooled representation avoids requiring a complete transitive B map inside every proof instance or per-unit certificate. A root context map, shared exact syntax, receiver-owned batch context and direct-dependency handles can express the contract without prescribed quadratic copying. The baseline may still recheck conservatively when cross-context compatibility has not been established.

The stated persistent-map path-copy bound is explicitly a representation bound. Changing a small number of aliases can force a large amount of native rebuilding or checking. Across arbitrary independent contexts, the retained choices and environments can require much more space than one syntax DAG. PI1 does not claim otherwise. Its structural planning bound also excludes native checking cost K, which remains separately charged.

## Practical library applicability and remaining source obligations

The independently researched [CLIENT1 library note](../analyses/CP-001G-library-interoperability.md) supplies actual source cases for the required separation:

- `Finset.range` contains a proof field. Its F4 definition can retain the semantic nodup judgment while different actual mem_range proof instances coexist.
- `Fin.castLE_castLE` contains `Nat.le_trans` inside its statement. The statement retains the F4 semantic reference; its alias obligation is not discarded because it appears in a type.
- The List-setoid/Multiset/Finset chain carries proof dependencies toward a nominal interface. PI1's separate realization avoids requiring a new group merely to select different proof evidence.
- Safe classical quotient choice remains distinct from an unsafe implementation; neither a new witness identity nor proof irrelevance licenses unsafe evidence.

These are meaningful broad-library targets, not a retreat to proof bodies with no proof-dependent background. Their cited source declarations have been inspected, but complete native closures have not been extracted or replayed. Extra elaborated arguments/helpers, supported generated groups and ordinary frontend reconstruction remain to be qualified.

The frozen producer review also documents that a combined Lean import may coalesce same-name/type theorem records with different bodies. PI1 can preserve alternatives that the collector actually captured; it cannot reconstruct an alternative body that the collector never retained. Complete per-module/declaration-time capture is necessary when those particular alternatives matter. This is a technical evidence-availability condition, not a demand for political attribution.

## Conclusion

The audited PI1 note provides a coherent concept-level route for multiple proofs, proof-bearing definitions and statement-level proof dependencies to coexist under one exact semantic interface. Its finite construction and grounding arguments establish representation/planning properties; the final native checks establish the selected typing judgments; current support/policy guards establish present usability. None of those claims alone implies the others.

No blocking correction is requested for the audited revision. Broad source coverage, independent implementation qualification and integrated protocol conformance remain unperformed release obligations, and no guaranteed exponential knowledge growth follows from this paper result.

## Focused post-amendment check

On 2026-09-20, inspected the subsequent PI1 amendments in revision:

`22ACBD948A92084226A02918AE5D85E50CF71F3425E02A4972A9FB5ABEF9F5C7`.

The semantic-realization section now explicitly retains the native theorem/opaque distinction and accessibility-recursion qualification boundary described above. The consumer table also selects versioned F4 provider advertisements `0x8022/2` anchored by actual schema-3 public descriptors, and new F4 advisory manifest/page schemas `0x8120/2`, `0x8121/2`, `0x8122/2`, rather than changing frozen advisory schema-1 meanings. The table retains semantic JudgmentID target references and nonauthorizing replay hints.

Those inspected amendments introduce no new conflict with this audit's mathematical/identity conclusions. This focused check does not expand the audit into an exhaustive review of the integrated wire specification.

## Sources

- [Audited PI1 note](../analyses/CP-001G-proof-instance-composition.md), revision bound above.
- [Pinned Lean proof-irrelevance check](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L932) and [conversion use](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L1202).
- [Pinned Lean checked theorem insertion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp#L192).
- [CLIENT1 actual library and frontend analysis](../analyses/CP-001G-library-interoperability.md).
- [Frozen complete producer path](../analyses/CP-001F-lean-producer-client-path.md).
- [Frozen capsule/composition boundary](../analyses/CP-001F-proof-identity-composition.md).
