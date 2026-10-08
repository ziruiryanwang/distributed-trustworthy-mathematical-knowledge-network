# CP-001G: proof instances, semantic representatives, and grounded composition

Date: 2026-09-20. Status: selected PI1 concept, integrated in [v4](../../spec/OPERATIONAL-CORPUS-V4.md) and independently reviewed in the [composition audit](../audits/CP-001G-composition-cross-audit.md). This is not code, an executed Lean experiment, a measured benchmark, or a completed implementation qualification. Frozen CP-001D/E/F and [v3](../../spec/OPERATIONAL-CORPUS-V3.md) are not edited.

## Purpose and the defect being repaired

Independent investigators must be able to retain and use different proofs of one exact statement. Ordinary mathematics also puts proofs inside types, definitions, structures and quotient constructions. The evidence representation must support both facts together without forcing recursive expansion of shared proof bodies or changing nominal interfaces merely to avoid a witness-selection conflict.

The frozen v3 representation has one map `W : JudgmentID -> ProofID`, requires its proof root's own pair, and interprets every theorem reference through W. This can introduce cycles into an originally acyclic source development. CP-001F's checked proof capsules solve a substantial restricted case, but its unchanged-background/type guard intentionally excludes proof-dependent backgrounds. Removing that guard without another mechanism would be unsound specification work.

Select **PI1** as a broader evidence representation. Its central decision is:

- A semantic statement or declaration continues to refer to the same exact mathematical judgments, definitions and nominal groups.
- A proof implementation refers directly to particular proof instances, preserving an ordinary acyclic source proof graph.
- A separate exact representative map supplies checked theorem constants where semantic descriptors genuinely require those constants.

The root proof does not automatically become the representative for its own judgment. This distinction removes the artificial root-selection constraint. It does not remove actual support cycles, alter the meaning of a native inductive type, waive bodies, or confer trust on an exporter.

Different nominal interfaces remain a different problem, addressed by [BRIDGE1](CP-001G-interface-bridges-and-applications.md). No part of PI1 identifies two GroupIDs because their fields look similar.

## Two kinds of identity, neither a popularity vote

Fix one exact adopted foundation F, including its native kernel source, qualified seed, allowed axioms, reserved-name interpretation and HEIGHT1 rule. Content identities retain the existing typed canonical encoding and hash-binding assumption.

For a semantic judgment j, write

\[
j=(F,u,\Gamma,\varphi),\qquad T_j=\Pi\Gamma,\varphi.
\]

This notation suppresses the already specified SemanticContext record and exact term identifiers; it does not change their payloads. The universe parameter order, telescope/conclusion split, direct semantic-reference set and all recursively referenced meanings remain committed.

A **proof instance** p has exact target j and an implementation term e. Its evidence identity commits to the particular earlier proof instances referenced by e. Two instances can have the same target without having the same body, assumptions, cost, availability, or current policy status.

The semantic descriptors retain their existing identities when their exact bytes and F remain unchanged. The new evidence objects have new identities. An old ProofID is not reinterpreted as a ProofInstanceID. Preserving a statement's identity is not preserving its historical witness choices or its previous checking certificate.

## Selected exact registry and grammar

These allocations are new to CP-001G and selected by the v4 integration. They do not change any old schema in place.

| Type/schema | Object | Exact payload |
|---|---|---|
| `0x0022/1` | WitnessTermDAG | `[FoundationID,universeArity,levelNodes,exprNodes,rootExprIndex]` |
| `0x0023/1` | ProofInstance | `[JudgmentID,WitnessTermID]` |
| `0x0024/1` | RepresentativeMapNode | Patricia grammar below, mapping exact JudgmentIDs to ProofInstanceIDs |
| `0x0015/3` | InstanceReplay | `[FoundationID,typedRoot,representativeMapRoot]` |
| `0x0016/3` | InstanceModule | `[FoundationID,sortedDefinitionReplayPairs,sortedRootInstanceReplayPairs,sortedGroupReplayPairs,sortedOpaqueReplayPairs]` |
| `0x0017/3` | InstanceOpposingEvidence | `[targetJudgmentID,negativeProofInstanceID,negativeInstanceReplayID]` |

`typedRoot` is exactly `[4,ProofInstanceID]`, `[1,DefinitionID]`, `[2,GroupID]`, or `[3,OpaqueID]`. Tag 0 is not admitted in this schema. Existing `0x0015/2` still interprets tag 0 as an old ProofID with the frozen W contract. Type/schema, not a friendly label or peer version string, selects the reader.

### Witness expressions

WitnessTermDAG uses the same explicit native expression/level grammar, canonical postorder sharing, binder normalization, literal encodings, scope rules and value-preserving integer conversions as the selected semantic NativeTermDAG. Its constant-reference alternatives are precisely:

- `[0,seedExportIndex]`;
- `[1,DefinitionID]`;
- `[3,GroupID,selector]` with the existing exact external member selectors;
- `[4,OpaqueID]`;
- `[7,ProofInstanceID]`, the new proof-instance reference.

Tag 7 here belongs to the **constant-reference subgrammar**, not expression tag 7 for a natural literal. The containing expression remains `[2,constantRef,levelIndexes]`.

`[2,JudgmentID]` is not a constant-reference alternative in a witness term. All source theorem occurrences in that expression, including occurrences in lambda domains, forall domains and let type annotations, become exact proof-instance references. Semantic declarations reached from the expression still have their ordinary semantic grammar, including JudgmentID references. Group-local tag 5 and bootstrap-only tag 6 remain prohibited in external witness terms. A projection still names an actual exact seed/group structure and field selector, never an arbitrary proof-instance ID.

Each proof-instance reference denotes the native constant of its target's **closed** type `Pi Gamma, phi`, at the supplied exact universe vector. The ordinary application nodes supply telescope arguments. There is no implicit argument inference and no recursive instantiation of the referenced proof body during encoding.

For `p=[j,e]`, e has j's exact universe arity and is checked under j's telescope. The receiver closes e with `lambda Gamma` exactly once. If Gamma has n variables, a wrapper referencing another instance q of the same j is `w(q).{u_0,...,u_(u-1)} x_0 ... x_(n-1)`; its de Bruijn argument indexes are `n-1,...,0`. This is not the distinct judgment with an empty telescope and a separately placed forall conclusion.

### Semantic descriptors do not acquire evidence references

NativeTermDAG `0x0010/2`, Definition, Judgment, SemanticContext, InductiveGroup and OpaqueDefinition retain their current schema-2 grammar. Proof-instance tag 7 is forbidden there. In particular, a definition's value can continue to mention a theorem by JudgmentID even if that value constructs proof-bearing data. The definition's identity does not change merely because a different independently checked proof of that exact judgment supplies the theorem constant.

The producer must not mechanically use witness grammar everywhere. Doing so would introduce particular proof-instance identities into semantic definitions/types, potentially changing their DefinitionIDs and downstream GroupIDs. That is a different transformation, not PI1's unchanged-semantic-interface route.

### Canonical representative map

Let B be the finite partial map from exact JudgmentID to ProofInstanceID used by one selected replay. Its new Patricia node grammar is:

| Node | Payload |
|---|---|
| Empty root | `[2]` |
| Leaf | `[0,keyBytes,ProofInstanceID]` |
| Branch | `[1,splitBit,prefixBytes,leftNodeID,rightNodeID]` |

Keys use the existing injective 37-byte ContentID lookup encoding, with L=296 bits. Every decoded key must be a selected schema-2 JudgmentID. Every value must be a new `0x0023/1` ProofInstanceID. A later exact check requires `target(B(j))=j`; matching a pretty-printed proposition is insufficient. Branches obey the existing first-differing-bit, canonical-prefix, two-nonempty-child and increasing-split rules. Nodes retain the 256-byte maximum; all child IDs have the new map-node type/schema. This does not reinterpret the old `0x0021/1` map's ProofID-valued leaves.

The operational ROUTE1 types `0x8022/1` and `0x8023/1` are different allocations. Neither routing membership nor a routing provider record can stand in for mathematical proof-instance evidence.

### Module and opposing-evidence consumers

In InstanceModule, each pair is `[artifactID,InstanceReplayID]`; its artifact type must match its list and the replay's exact typed root. The instance list contains ProofInstanceIDs, never legacy ProofIDs. Lists retain the existing canonical pair ordering, duplicate prohibition and bounded packaging rules. `Import(moduleID,exportKind,index)` selects tag 4 for this instance list and tags 1/2/3 for definition/group/opaque lists. Tag 0 is unsupported for a schema-3 module. Import still adds no mathematical authority, and a module is not a global corpus manifest.

InstanceOpposingEvidence targets an F4 judgment j and requires its named negative instance to target the exact inherited same-context `Neg(j)` construction, with the named schema-3 replay rooted at that instance. Independently check that complete replay. The meaning remains a proof of `Gamma |- phi -> False`, not a claim that `Gamma |- phi` is underivable or that a conditional positive theorem is invalid. The old `0x0017/2` record is not expanded to accept a different evidence type in its negativeProofID field.

## Foundation and reader qualification

PI1 changes the evidence-reference/naming and replay contract. Select **NativeRules ruleSchemaCode=4**, using the existing `0x0003/1` payload shape, same native family, feature codes `[0,1,2,3,4,5]`, exact allowed axiom paths/types, and HEIGHT1. The changed NativeRulesID yields a new FoundationID F4. Rule code 4 means the complete PI1 reconstruction contract under the pinned qualified kernel/seed, not an optional alternative interpretation of code 3. Frozen F3 retains its root-in-W contract.

This makes the foundation boundary unambiguous even though PI1 adds no axiom or primitive reduction rule. Existing semantic schema-2 grammars are retained **with F4 identities and F4 references throughout**. Ordinary semantic names retain the `.j`, `.d`, `.i` and `.o` naming algorithm, but their full IDs differ from F3 when F changes. New `DTMKN.w.<fullProofInstanceID>` names occur only as independently checked proof constants under PI1. The namespace is fixed, disjoint from all reserved/internal/semantic names, and not chosen by a peer.

Identity preservation claims in this note mean unchanged exact semantic descriptors under **one F4**, across different proof instances or representative maps. They do not mean F3 bytes acquire F4 meaning. F3-to-F4 migration re-expresses and independently rechecks affected terms/statements/declarations under new identities. Old acceptance certificates and native environments are never relabeled.

PI1 does not admit old Proof `0x0014/2` or Replay `0x0015/2` as mixed selected evidence. Retained schema-2 semantic terms/declarations/contexts/judgments are admitted only by their explicit F4 binding and grammar. A peer cannot select a reader by supplying an old familiar type/schema and an incompatible foundation. The exact adapter, checked-name construction, actual generated interface and new reader still require local implementation qualification; no digest or execution success is invented here.

F4 is a selected **preimplementation profile candidate**, not a protocol demanding a global upgrade event. Actual installed foundations can coexist under separate owner-adopted qualified policies. A future correction or migration retains its independently justified authority and current-use boundaries.

## Exact native realization

The receiving node constructs one coherent environment for its selected replay. It never accepts a publisher's native environment, raw ConstantInfo, inferred theorem truth, or prechecked status.

For every reached proof instance p with target j, reconstruct a safe native theorem named `DTMKN.w.<fullProofInstanceID>`, with type T_j and body obtained by closing its decoded witness expression under Gamma. Check its type is Prop, its actual body, universe parameters, scope and body/type conversion through the qualified native checker.

For every actually required semantic theorem constant j, first independently check `B(j)`. Then reconstruct the canonical semantic theorem named `DTMKN.j.<fullJudgmentID>`, with the same exact T_j and body

\[
w(B(j)).\{u_0,\ldots,u_{u-1}\}.
\]

Both sides of this alias declaration have the closed type T_j; no extra telescope application or lambda wrapping is required for the alias body. This is a checked theorem declaration, not an axiom. Its actual body contains the proof-instance constant, and its support includes that instance's complete evidence.

A definition is reconstructed once at its exact `.d` name from its original semantic descriptor; an opaque declaration once at its exact `.o` name with its full checked body; and an inductive group once at its exact `.i` names from its exact group descriptor. The qualified native operation regenerates the complete group interface and rules. There is no second nominal copy of the same group followed by an assertion that the copies are definitionally equal.

Different representatives may change the bodies/support of canonical theorem aliases. They do not authorize replacing an already inserted alias in place, relabeling an existing environment, or retaining a certificate whose selected evidence has changed. An incompatible existing environment is rebuilt or forked and rechecked as explicitly accounted below.

## Dependency graph: statements are not theorem constants

The crucial distinction is between needing the descriptor of a statement and needing an inhabitant as a theorem constant. Use the following derived node sorts; these are planning/checking vertices, not additional publisher-trusted wire records:

- `S(j)`: the exact statement descriptor and its telescope/conclusion references;
- `I(p)`: an exact proof instance and its witness body;
- `A(j)`: the canonical semantic theorem alias for j, supplied by B(j);
- `D(d)`, `O(o)`, `G(g)`: exact ordinary semantic declarations/groups;
- the fixed already qualified seed and its exact support.

The edges are **prerequisite edges**, from a node to what must precede it:

| Node | Required predecessors |
|---|---|
| `S(j)` | All actual semantic references in its telescope/conclusion; a theorem constant reference means `A(k)`, not just `S(k)` |
| `I(p)` | `S(target(p))`; every direct proof-instance reference `I(q)` in its witness term; all actual ordinary semantic references in that term |
| `A(j)` | `S(j)` and `I(B(j))`, with exact target equality |
| `D(d)` / `O(o)` | All actual semantic references in complete type and body |
| `G(g)` | All external references in its admitted descriptors and actual qualified generated interface/rules |

Traversing `I(p)` to `S(target(p))` does **not** insert an edge to `A(target(p))`. Merely proving P requires P's well-formed type, not another proof of P. A theorem occurrence genuinely present inside that type does require its own checked alias.

Every ordinary semantic JudgmentID occurrence is interpreted consistently through the one B selected for this replay. Each proof implementation can simultaneously reference many distinct proof instances of the same judgment. No edge is suppressed because its value has a proof type or because a dependency seems operationally unimportant.

The native group operation's permitted internal induction is contained inside one G vertex. It is not an excuse for a cross-artifact support cycle. Derived external dependencies and generated names must be reconciled against the qualified actual operation, not trusted from a publisher's summary. A dependency newly discovered during reconstruction is incorporated and checked before success; an unexplained external reference is not provisionally admitted.

## Exact root closure and checking procedure

For a submitted InstanceReplay `(F,r,B)`, perform the following receiver-owned finite procedure under explicit limits:

1. Validate typed content IDs, canonical objects, the new map grammar, all ranges and same-foundation constraints. Old Proof/Replay records remain inert migration inputs, not mixed-instance proof authority.
2. Start at the exact typed root. Traverse actual terms and every reached declaration's complete type/body/interface. Distinguish S, I and A as above. At `A(j)`, read B(j), require its exact target j, and traverse its proof instance. Direct witness references traverse the named instance without asking B to replace it.
3. Derive the set R of actually encountered alias obligations. Build the expected canonical map of exactly `(j,B(j))` for j in R. Require this map root to equal the submitted representativeMapRoot. A proof-instance root does not contribute its own pair unless its closure actually encounters that alias obligation.
4. Reject an actual selected-support cycle; do not insert a theorem to break it. Topologically reconstruct all reached units, preserving the exact supported native group operation. Every theorem instance and alias gets the required independent native check.
5. Reconcile any qualified generated interface/rule support, exact map membership, actual generated-name inventory and final footprint. A discrepancy cannot be hidden by an optimistic earlier plan. Commit a complete successful certificate only after all required checks finish.
6. Apply the ordinary protection, current policy and incident guards before current local reuse. Publication/custody are separate effects.

The least reachable closure is finite only for a supported successful case; missing objects or exceeded budgets give nondecision. Missing/extra map entries or a selected cycle demonstrated from complete available data reject the **submitted representation**, not the proposition. An invalid proof instance fails checking; this is not proof that no proof of its target exists.

Exploratory candidates, rejected choices and unrelated package objects do not enter the final selected closure, footprint, public read scope, or custody obligation merely because they were inspected. Conversely, every binding map/term/descriptor object in the final closure belongs to its actual incident and availability support.

## Why the native substitution is justified, conditionally

There are two separate arguments: typed proof replacement and reconstruction of semantic declarations. Neither argument transfers acceptance without checking.

### Proof replacement lemma

Assume a qualified native environment establishes

\[
\Gamma\vdash p:P,\quad\Gamma\vdash q:P,\quad\Gamma\vdash P:\mathrm{Prop}.
\]

Its definitional proof-irrelevance rule yields `p` definitionally equal to `q`. Under ordinary congruence and conversion, replacing a proof-valued subterm p by q in a well-typed expression preserves typing up to the induced definitional equality, provided the surrounding declarations, universes and binder context are the same and substitutions avoid capture.

Apply this by structural induction on the finite expression and by declaration order. It covers proof occurrences in data constructors, lambda-domain types, dependent applications and types themselves, not only final proof bodies. The proposition types being compared must first be checked convertible under the coherent environment. The lemma does not say all inhabitants of a data type are equal or that merely similarly named propositions coincide.

Pinned source supports the relevant native mechanism: `type_checker.cpp:932-938` infers the first term's type, requires it to be a proposition, and checks definitional equality with the second term's inferred type. The main conversion path invokes this at lines 1202-1203. This is evidence of the selected mechanism, not a machine-checked proof of the entire exporter.

### Semantic realization lemma and its boundary

For one exact semantic descriptor set, all PI1 realizations use the same canonical semantic names, universe order, group member selectors, types and bodies expressed in those names. B changes the checked implementation of a proof alias, not its exact statement or the descriptor syntax of an ordinary definition/group. Consequently a compatible declaration-order induction can reuse the semantic interpretation of that interface while checking the new proof support.

For a source export, replacing each source theorem occurrence by its canonical checked alias is justified at its actual proposition by the proof replacement lemma. Ordinary definitions are reconstructed once in that environment. A native inductive group is regenerated from that one exact descriptor; its generated interface, positivity/recursor rules and external support still need the qualified operation and native checking. The design does not prove a blanket plugin/elaborator/name-equivariance theorem.

For an independent branch join, the intended preservation statement is conditional on these exact semantic-descriptor and generated-interface qualifications. Native checking remains the decision boundary for every selected result. There is no claim that arbitrary Lean elaborator metadata, source coercions, unsafe native facilities, or two independently cloned nominal inductives satisfy this lemma.

Native theorem and opaque declaration kinds are not interchangeable by this argument. In particular, accessibility-recursion reduction and other proof-dependent computation require the actual qualified declaration kinds and native conversion path, not a heuristic assertion that all proof-valued constants behave identically. PI1 deliberately uses checked native theorem declarations for its instances/aliases and preserves genuine semantic opaque declarations as opaque. Typed proof replacement does not assert identical normalization traces/costs or complete source replay compatibility for every supported-looking library fragment.

## A constructive acyclic export from a supported source

Assume a finite, complete, supported source declaration graph under one qualified foundation; its external dependency graph is acyclic after admitted native groups are treated atomically. All declaration kinds, actual theorem/opaque bodies, universe parameters and generated interfaces must be available. No future declarations can appear in its actual source dependency graph.

Choose a topological source order with rank `r(s)`. Export in that order:

1. Normalize every semantic descriptor by replacing source theorem references with already determined JudgmentIDs and ordinary references with their already determined exact semantic IDs. The current theorem's target identity is derived from its type before its body; it does not contain its own chosen proof.
2. Emit each theorem's witness expression by replacing source theorem occurrences with the already emitted exact proof instances, including theorem references inside expression annotations. Do not unfold predecessor proof bodies. Deduplicate exact identical instance objects if they arise.
3. For every semantic ID choose its earliest source occurrence as the representative descriptor occurrence. For each JudgmentID j needed as a semantic theorem constant, choose the instance of the earliest source theorem with that exact j as B(j).
4. Restrict B to the exact alias obligations reached from each selected final root. Check the complete resulting replay independently.

This earliest-occurrence choice is a construction proving existence of an acyclic plan; it is not a required global time order, publisher authority, historical provenance, or permanent preferred proof. A node importing different branches can choose another grounded map.

### Rank argument

Assign semantic statement/declaration vertices their earliest source occurrence rank. An instance emitted for a source theorem s has its own source rank, or the earlier representative's rank if the instance bytes deduplicate. Within one source rank, order its statement descriptor before its proof instance, and its canonical alias after that instance. Ordinary definition/group vertices use their original supported source order.

Every proof-instance reference in s's witness body points to an actual earlier source theorem. Every external semantic reference of a source declaration/type points to an earlier source declaration. Replacing its target by the earliest equal semantic occurrence cannot increase that rank. The earliest theorem proving j cannot require `A(j)` through an earlier source theorem of exactly j: such an earlier theorem would contradict earliestness. The type descriptor is not itself a demand for `A(j)`.

Therefore all external prerequisites strictly precede their users in this refined finite order. The map and instance graph produce an acyclic materialization plan. This remains true when a later proof of j uses a definition whose type/body depends on an earlier proof of the same j: the definition uses the earlier representative, while the later proof remains its own instance.

This argument relies on the **actual** source dependency graph and exact semantic equality of descriptors, not on source textual line numbers or names. It does not cover omitted private bodies, unsupported axioms, unexplained generated references, a changed foundation, or a failed native reconstruction. Those premises are part of the exporter qualification, not assumptions that a hostile sender may assert into truth.

## Joining independent finite branches

An arbitrary union of representative maps is not a valid join rule. Even if every input branch is acyclic, selecting an unfortunate representative from each can create a combined cycle.

Select a finite receiver-local **AND/OR grounding** procedure. It chooses candidate support, not theorem truth. Its candidate pool can include complete independently checked local branches and untrusted proposed alternatives, with distinct checking states; only the actual final independent checks justify acceptance.

### Candidate hypergraph

Semantic declaration/statement vertices and exact proof-instance vertices have the fixed AND-prerequisites above. An alias vertex `A(j)` has alternatives `I(p)` for exact candidate instances with `target(p)=j`, together with its fixed statement prerequisite. Different proof instances are not conflated into one instance node.

Begin with the exact qualified seed and other deliberately retained compatible checked base units. Repeatedly ground an ordinary/instance/statement node once all its fixed predecessors are grounded. Ground an alias only after its statement and at least one candidate instance are grounded. At that moment choose one ready candidate and fix it for this plan. Never justify a node by an ungrounded alias or by the mere existence of an OR alternative.

A concrete deterministic choice is earliest grounding round, then lexicographically smallest exact typed candidate ID among that round's ready alternatives. Node processing within a round uses exact node-kind/ID order. These are local finite planning choices; another node may select another valid B without disagreement about truth.

When the target is grounded, derive its exact selected root closure, discard unrelated exploratory vertices from that closure, encode the exact restricted B, and run the complete native replay procedure. An exploratory successful check under another map is not silently transferred into this final replay.

### Structural grounding theorem

For a **fixed finite fully available dependency/candidate graph**, let G_0 be the grounded base and G_(k+1) add every node whose AND-predecessors, or one alias alternative together with its fixed predecessors, are in G_k. This increasing sequence stabilizes after at most V strict-growth rounds, where V is the number of candidate vertices.

Induction on a supplied acyclic branch's topological order shows every node of that branch eventually lies in the least fixed point if its requisite alias alternatives occur in the candidate pool. Adding candidates cannot remove nodes from this structural fixed point. Thus the union of two individually grounded branch graphs retains their structural groundability; an arbitrary cyclic representative choice is avoidable when the grounding witnesses are retained.

Choosing only already grounded alias witnesses also yields a DAG: number each chosen node by its grounding event, with all actual predecessors numbered earlier. No later choice changes an already chosen alias. Prune to the root's selected closure and the order remains acyclic.

This is a theorem about finite dependency grounding. It does **not** prove all candidate terms are well typed, all foundations are trustworthy, footprints meet a policy, resource limits suffice, or an unexplored missing candidate exists. Final native checking supplies typing; current-use guards supply the operational claims.

### Determinism, cost and incomplete outcomes

Implementationally, readiness can be represented conceptually by unresolved-predecessor counts and reverse incidence lists, avoiding V full rescans. For a supplied graph with V vertices, E prerequisite incidences and C alias-candidate incidences, graph bookkeeping can take `O(V+E+C)` events plus deterministic ordering/dictionary cost, exact content parsing, map construction and native checks. A comparison-based ordered frontier may add `O((V+E+C) log V)` work. These are paper representation/planning bounds, not a claim about kernel running time.

Candidate discovery and acquisition are separately bounded. No reachable remote endpoint can force unlimited candidate enumeration. A node can declare `UNKNOWN(NO_GROUNDED_PLAN_IN_SCOPE)` for its exact finite pool; this does not mean the theorem is false or that no compatible plan exists in the network.

Greedy first-ready choices need not minimize bytes, assumptions or conversion cost. A ready representative acceptable for one target can later make a narrower policy target unusable. Under footprint/budget constraints, a structurally groundable pool may still need another choice, another environment, or a separately admitted bounded re-plan. Failed checking/policy does not justify keeping an invalid alias, and it does not prove logical inconsistency. No polynomial-time optimal witness-selection theorem is claimed.

Planning must not falsely count exploratory candidates as final evidence. Conversely, using a preexisting native environment that contains exploratory or differently realized declarations requires exact environment compatibility and a complete selected-footprint argument; the baseline cold route checks the pruned plan in a clean coherent environment.

## Typed paper examples

The following are source-shaped mathematical examples for the design argument, not executed declarations or export fixtures.

### Repeated proofs of one statement

Let `a : True := True.intro` and later `b : True := a`. Their semantic target is the same j. The new objects have `I(b) -> I(a)` and both have statement predecessor S(j). There is no A(j) obligation if their statements and other reachable semantic descriptors contain no theorem constant reference. Therefore B is empty for either instance replay. In particular, selecting b as the root does not force a self-edge.

### A proof appears in another theorem's type

Consider:

```text
a : True := True.intro
c : a = a := Eq.refl a
b : True := (fun (_ : a = a) => a) c
```

Write j for the exact judgment True and k for the semantic judgment `J(j)=J(j)`. Export a's body as I(a). The semantic type of c uses A(j), supplied by `B(j)=a`. Its witness body uses the exact instance a. Native proof irrelevance checks the required conversion between its witness-instance occurrences and the canonical semantic alias at the same proposition.

I(b) uses the actual earlier instance a in its lambda-domain annotation and body and the actual earlier instance c. The argument's type and lambda-domain type are checked convertible in that coherent environment. The root target remains j, but there is no rule `B(j)=b`. The resulting order is I(a), A(j), S(k), I(c), I(b), with each ordinary prerequisite inserted as needed. All actual support, including a, is retained.

This example exhibits why changing only direct final proof-body references is insufficient: annotations and referenced declaration types must obey the separated grammars too.

### A representative choice that would introduce a cycle

Branch A contains a grounded base proof Q_A of Q, a semantic definition D whose body/type mentions the semantic theorem Q, and a proof P_A of P using D. Branch B contains a grounded base proof P_B of P, a semantic definition E mentioning semantic theorem P, and a proof Q_B of Q using E. Assume exact shared targets P and Q and otherwise supported matching semantic interfaces.

Choosing `B(P)=P_A` and `B(Q)=Q_B` arbitrarily produces

```text
I(P_A) -> D -> A(Q) -> I(Q_B) -> E -> A(P) -> I(P_A).
```

Grounding instead first admits the actual bases Q_A and P_B, then can choose those ready representatives, admit D/E, and check both later instances. This is a branch-join procedure, not an exception to cycle rejection. The resulting support can differ from each source branch's original preferred choices; it is recorded and checked as a new replay.

### Polymorphic sharing

For CP-001F's subset-universe family, each source proof p_i has two predecessor occurrences at distinct explicit universe vectors. PI1 stores its witness body once, with two exact references to p_(i-1) and the corresponding vectors. No predecessor body is instantiated into the serialized parent. The family retains its source `O(N^2)` vector/syntax size instead of the `2^N` distinct instantiated leaves of the literal-substitution fallback. Within F4 the target True remains the same exact judgment with its fixed N+1 universe arity; it does not share its F3 identity.

This removes that representation-induced blowup. It neither proves that all native checking is polynomial nor that all equivalent proof representations have the same size.

## Ordinary library cases beyond F's capsule guard

At the pinned mathlib source, `Mathlib/Data/Finset/Range.lean:53-54` defines `Finset.range n` by a Finset constructor containing the proof `nodup_range n`; lines 64-65 state `mem_range` using that definition. A proof-bearing semantic definition is ordinary library mathematics, not an exceptional logical trick.

PI1 retains Finset.range's exact canonical semantic definition body within F4, where nodup_range is a JudgmentID theorem reference. B supplies a checked representative for that judgment. Different proof implementations of mem_range can coexist as distinct instances without cloning Finset or changing range's identity merely to insert capsules. Exporting the library slice still requires the complete actual bodies, exact nominal group descriptor and successful native reconstruction; the source snippet alone does not establish that qualification.

Pinned Lean `src/Init/Data/Fin/Lemmas.lean:488-490` gives `castLE_castLE` with `Nat.le_trans km mn` directly inside its theorem statement; lines 492-494 give the related function-composition theorem. PI1 leaves that F4 statement's semantic reference to the exact F4 Nat.le_trans judgment intact, supplies its checked alias, and exports each implementation with exact instance references. F's unchanged-type restriction is no longer required merely because this semantic type contains a proof.

The producer's separate interoperability review traces related proof-bearing definitions through List.Perm, List.isSetoid, Multiset, Finset and classical choice. Those examples reinforce the same boundary: genuine data/nominal interface descriptors remain exact; changing proof evidence alone is not a reason to regenerate a distinct nominal hierarchy. They do not authorize treating `Quot.unquot` or any unsafe implementation as accepted logical evidence.

## Footprints and assumptions belong to the actual realization

For a chosen replay, define its actual footprint by the least closure of every selected proof body, checked alias body, statement descriptor, semantic type/body, regenerated group rule and fixed seed/rule dependency. Compute the permitted axiom/rule uses over that closure. Proof irrelevance does not erase any referenced proof's assumptions from this accounting.

Changing B can change the footprint of a proof-bearing definition without changing that definition's semantic ID. This is intentional: the identity commits to the declaration's mathematics with theorem **statements**, while the replay commits to their selected evidence. A source's original witness footprint is not asserted to survive normalization. If source history matters later, it is separate metadata, never mathematical acceptance authority.

If the same instance p is checked under B_1 and B_2, the InstanceReplayIDs and relevant native checking contexts differ whenever their reached choices differ. The proof-instance body commits to its direct evidence references, but not to a recursively embedded transitive representative map. Its acceptance and footprint are therefore contextual, not an unconditional property of its ID alone.

A root's policy must allow the actual final footprint. An alternative classical proof cannot silently replace a constructive representative in a replay claiming a constructive footprint. A local policy can require a supplied representative, a permitted axiom set, or another explicit criterion, but this may force replanning and does not make a rejected target false.

## Certificates, environment compatibility and pooling

The cold check establishes one exact complete root closure. Its certificate binds at least the InstanceReplayID, F, exact new reader/representation interpretation, checker image, adapter, native ABI, semantic options, actual regenerated group inventory, and receiver-derived complete support/footprint. The root already commits to exact B and all direct proof-instance identities through content references.

The actual native environment additionally records which B(j) supplies each installed canonical alias, the exact checked instance constants present, semantic declaration identities and qualified generated interfaces. An environment with `A(j)` realized by p cannot be relabeled as one realized by q because both prove the same j. Compatible extensions can reuse retained receiver-owned certificates; conflicting realizations require an explicitly coherent rebuilt/forked environment and renewed checks for the affected closure.

This must not mandate a complete transitive B map in every proof-instance record or every local unit certificate. The baseline pooled representation consists of:

- one exact selected B trie/root for each retained replay context;
- the unique CAS object DAG, with proof bodies stored once per exact object;
- one receiver-owned topological checking batch/context certificate;
- bounded per-unit handles identifying that exact context and direct checked dependency edges;
- optional persistent support summaries only where their construction/storage is actually funded.

An interior unit can be reused within that certified compatible environment via its exact handle. To reuse it in another environment, either establish exact relevant-context compatibility from receiver-owned records and required checks, or recheck it. A foreign handle, a matching body ID alone, or a hand-waved transitive-map equality cannot establish compatibility. This conservative contract may recheck more than a future qualified optimization; it does not copy all transitive maps by definition.

The root's B is exact even when a retained native environment contains a compatible larger base. The receiver must derive the smaller root's actual reached support and current guards; unrelated installed declarations are neither hidden premises nor automatically part of its public disclosure. Ordinary native dependency checking and actual reference extraction, not the environmental presence of a famous theorem, determine that support.

### Storage and work claims

Let S be the total distinct admitted source/wire syntax, including explicit universe vectors; V and E the distinct reached units and prerequisite incidences; b the number of reached semantic alias obligations. A cold selected graph stores `O(S+V+E)` mathematical syntax/direct graph information and `O(b)` canonical Patricia nodes for one complete B, up to fixed object overhead. Canonical map lookup/update bookkeeping can be bounded by `O((V+E)L)` together with actual parsing/trie validation. Native checking cost K remains an additional term, not a function silently bounded by S.

For N ordinary compatible incremental extensions with bounded new syntax/direct references and at most k new/changed alias choices per extension, persistent B roots add at most `O(N k L)` map nodes. This is a **map-representation** bound even when a choice changes. Reusing prior unit certificates additionally requires their exact reached alias context to remain compatible; otherwise affected declarations and environments must be reconstructed/rechecked, and those events can be much larger than the new syntax. Proof instances with no new semantic alias obligation need not add a B entry. Shared physical evidence and compatible dependency handles can remain pooled, with new local certificate records proportional to the actual admitted checking events/direct incidences. Optional secondary inventories/support-map indexes add their actual charged path-copy work, potentially an additional L factor.

This is a compatible-extension bound. Across R arbitrary substantially different representative contexts, native environments, certificates and root maps can require much more state. In particular, many independent witness vectors may encode incompressible choice information. No claim bounds all retained branch contexts by one graph's size, promises constant-cost arbitrary joins, or deduplicates contexts merely because their statement IDs agree.

If context rebuilding changes a large shared alias region, affected checking can be large. If a budget cannot fund it, return exact nondecision while retaining previously valid independent branches under their own guards. The system must not present a refusal as successful interoperable reuse.

## Migration and protocol integration

An old complete acyclic F3 Replay2 can be converted locally under the explicit cross-foundation migration contract: select the locally qualified F4 target and its explicit seed correspondence; process the old selected proof graph topologically; re-express every semantic descriptor/term under F4 with all changed referenced IDs; translate each old proof expression's JudgmentID occurrences to the corresponding selected converted F4 proof instances; choose those converted instances for the new semantic alias obligations; derive the new exact root-reachable B; and independently check the new InstanceReplay. No F3 semantic object is relabeled as an unchanged F4 object. The old root's mandatory pair can disappear if no actual semantic alias needs it. Different complete old replays may emit different new instance graphs from the same old ProofID because their W choices differ; the migration key includes the old exact replay context, source/target foundation, transformation interpretation and actual target choices.

No producer acceptance bit or old certificate crosses this conversion. Old Proof/Replay schemas remain readable under their frozen rules or as inert archival inputs; they do not become instance evidence merely by substituting a type label. Re-expression plus target checking is not a blanket proof of equivalence between arbitrarily different foundations.

The new evidence reader must be advertised as an exact supported mathematical schema capability in the integrated G protocol. A peer supporting only Replay2 cannot be sent InstanceReplay as if it understood the same profile. Network public-root/export authorization, closure inventories, current-use checks, proof indexes, custody and incident support must recognize the new exact root and map/term/object kinds. This is a finite registry/read-scope extension, not generic CAS-read authority or permission to execute a peer exporter.

The producer/client surface must expose whether an available root is an old proof or a proof instance, with its actual evidence context. A user's explicit application can reference a checked instance directly in a witness term. Ordinary semantic definition construction continues to use canonical theorem aliases and therefore needs the appropriate compatible B realization. Publishing a new result, acquiring it and making it locally reusable remain separate state transitions.

### Proof-root consumer audit

The integrated [v4 registry](../../spec/OPERATIONAL-CORPUS-V4.md) owns the exact operational schema/capability allocation; this table states the required typing changes and guards. Allocate negotiated capability 8 to PI1. A capability advert is not evidence that a remote result has been checked or that a local foundation is qualified.

| Consumer | Required PI1 interpretation; forbidden shortcut |
|---|---|
| InstanceModule / module import | New `0x0016/3`, proof list contains `[ProofInstanceID,InstanceReplayID]`, exportKind 4. Never place an instance in an old ProofID list. |
| Same-context opposing evidence | New `0x0017/3`, exact negative target and root `[4,negativePI]`. Context/negation checks are unchanged, not bypassed by a new record kind. |
| Native validation/reconciliation and public result projections | Bind exact schema-3 replay/typed root; judgment/instance fields occur only for tag 4. New unit/context certificates bind actual B and F4. |
| Status observation `0x800A` | New schema 3 for PI1: the former proof-valued position means `proofInstanceIDOption`; it and judgmentIDOption are present exactly for tag 4, absent for tags 1/2/3. Retain exact root/replay agreement and all signed-local-observation guards. Old schema 2 does not accept tag 4. |
| Local IndexDescriptor `0x8101`, PublicIndexDescriptor `0x8111`, ProofFamilySelection `0x8104` | New schema-3 PI1 records distinguish `(ProofInstanceID,InstanceReplayID)` alternatives. Public projection still excludes private assessments; judgment equality groups alternatives but never merges their evidence/footprints. |
| HINT and proof-root selectors | Object kind 4 means a PI1 root only after the new capability/profile binding. Unknown kinds are not silently coerced to legacy proof kind 0. The hint remains nonauthorizing. |
| FIND/PAGE/FIND_WINDOW and exact judgment indexes | Returned PI1 public descriptor types and their replay/instance target bindings are checked. Deduplication uses exact descriptor and instance/replay pair, not legacy ProofID or JudgmentID alone. Pagination still names the actual descriptor-ID ordering. |
| Provider advertisements | All F4 ads use `0x8022/2` with a `0x8111/3` root-descriptor anchor and schema-3 replay. K4 additionally requires that descriptor's actual `0x8124/1` structural hint to contain the token with exact matching extractor/foundation/replay. Schema-1 advertisements retain frozen F3 semantics. |
| BUNDLE1 / public-root and export read scopes | A schema-3 replay scope contains exactly its PI1 native closure, including WitnessTerm/ProofInstance/B-map nodes and binding semantic objects. Generic CID transport is not permission to read unrelated or exploratory instances. |
| EXPORT_HEAD2, inventory nodes and portable archives | Commit the exact schema-3 replay and required F4/schema capability. Reconcile all new mathematical object kinds in the derived closure, not just an old ProofID inventory. Pure generic-CID inventory layouts need not change if their exact eligible-type/read-scope contract is explicitly extended. |
| AdvisoryManifest / LibraryViewPage / CollectionGuidePage | F4 uses `0x8120/2`, `0x8121/2`, `0x8122/2` with their existing fixed array shapes and schema-3 replay hints only. Manifest kind/type bindings name the new page schemas. Semantic theorem targetRef remains `[2,JudgmentID]`, not a proof-instance constant. A replay hint still grants no read authority; frozen advisory schema 1 is not reinterpreted. |
| Retention acknowledgments, custody roots, current-use pins and incidents | A root is the exact schema-3 replay; actual protected support includes B-map and instance objects. Their opaque root-CID fields do not confer compatibility with legacy evidence; retained local guard/certificate fields bind F4/PI1. |
| Counters, cost/selection/repair caches, frontend maps and migration | Count exact instances and instance/replay contexts separately; include new schemas and exact realization in keys. A source alias or old ProofID is never an implicit PI identifier. |

All unchanged generic-CID layouts retain their existing signatures, local authority, finite limits and schema-specific decoder. Only the explicitly negotiated eligible-type extension permits the new exact CID kinds. A legacy peer cannot be offered those meanings without PI1 negotiation. Strictly proof-typed record fields receive new schemas instead of an untyped substitution. Unknown or unsupported combinations fail explicitly; they do not downgrade to a foreign acceptance claim.

## Required audit and qualification cases

- Root and earlier theorem have identical JudgmentIDs: the root must not automatically overwrite the semantic representative.
- A theorem occurrence appears only in a lambda-domain or let annotation: its exact instance dependency is still traversed.
- A theorem occurrence appears only inside a definition type/body or group-generated interface: it requires a checked semantic alias and appears in B/support.
- A submitted map includes the root's pair without an alias obligation: exact-map validation rejects the extra entry.
- A selected alias points to the root through a proof-dependent definition: the actual selected cycle is rejected; no provisional axiom is inserted.
- Two acyclic source branches admit the P_A/Q_B cycle above: grounding must find the retained base alternatives in a sufficiently complete funded pool.
- The selected B changes but the instance body does not: neither environment acceptance nor its actual footprint is copied blindly.
- A cheaper-looking representative adds a forbidden axiom: the target's current policy blocks it or requires a new checked plan.
- One source declares unused universe parameters and uses different explicit vectors: the exact arity/vectors survive instance sharing.
- A judgment has a nonempty dependent telescope: its body is closed once and constant applications supply arguments in the right order.
- Finset.range's proof-bearing data definition is retained exactly while two mem_range proof instances coexist: no unnecessary Finset GroupID cloning.
- The statement of castLE_castLE contains Nat.le_trans: statement identity remains bound to the exact semantic theorem reference, not one proof instance.
- Two distinct nominal GroupIDs have superficially identical structure: PI1 must leave the distinction intact; an actual BRIDGE1 map/transport is needed.
- A hostile candidate pool contains an unbounded supply of same-target proofs: finite selection/acquisition/state budgets apply before checking or storage allocation.
- A complete graph grounds structurally but native checking exceeds limits or fails: report the actual nondecision/failure; no structural-validity certificate becomes theorem acceptance.
- An old Replay2 read scope receives a new-schema map: reject schema mismatch; do not broaden disclosure or reinterpret values.
- A candidate or selected support object is lost, corrupted, or affected by an incident: current reuse blocks under the ordinary exact guards, independently of unchanged statement identity.

## What has and has not been established

The selected paper construction preserves source proof-instance sharing, separates statement lookup from theorem inhabitation, supplies a constructive acyclic plan for complete supported acyclic source graphs, and gives a finite grounding mechanism for independent branches under one exact F4 semantic interface. It covers proof-dependent definitions/types excluded by F's simple capsule guard without requiring those semantic descriptors to contain particular proof implementations.

It does not establish broad real-library export success, an executed kernel adapter, native resource bounds, complete discovery, optimal witnesses, a proof of all kernel metatheory, or exponentially increasing mathematical usefulness. Successful native checking and current evidence guards remain mandatory. Producer/source qualification, complete protocol bindings and independent audit remain prerequisites to release; selecting F4 does not claim their execution.

## Sources

- [Frozen v3 integrated contract](../../spec/OPERATIONAL-CORPUS-V3.md).
- [Frozen Native2 scaling and exact witness-map/certificate analysis](CP-001E-native-scaling.md).
- [Frozen F proof identity and restricted capsule analysis](CP-001F-proof-identity-composition.md).
- [Pinned Lean proof-irrelevance conversion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L932).
- [Pinned Lean checked theorem insertion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp#L192).
- [Pinned mathlib Finset.range](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Finset/Range.lean#L53).
- [Pinned Lean Fin.castLE_castLE](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Data/Fin/Lemmas.lean#L488).

The four linked upstream source portions were inspected directly, read-only, on 2026-09-20. No declaration, theorem, source module, tactic, exporter, kernel image or benchmark was executed for this note.
