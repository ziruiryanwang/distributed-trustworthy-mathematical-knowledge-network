# CP-001F: theorem identity, proof composition and source-neutral reconstruction

Date: 2026-09-20  
Status: New concept analysis and selected bounded improvements; CP-001E remains frozen  
Method: Explicit typed paper families and read-only inspection of pinned Lean source. No implementation, native execution, proof replay, benchmark or exploit execution.

## Question and outcome

Can a decentralized node efficiently reuse two developments that prove the same proposition differently, without giving proof choices control over proposition identity?

The V2 representation has a genuine useful property: a JudgmentID identifies an exact formal statement independently of its selected proof. Its global replay map, however, chooses exactly one ProofID per JudgmentID, including the root proof's own pair. This is stricter than requiring a finite acyclic graph of individually checked derivations. Independently checked developments can disagree on that global selection even when their mathematical interfaces are compatible.

Three conclusions follow from this analysis:

- The already documented same-statement alias cycle is real but does not, alone, establish an efficiency defect beyond the existing fallback. Literal source-proof expansion has a stronger exponential substitution family even with DAG sharing; the lower bound is for that exporter transformation, not for every equivalent proof.
- A bounded **proof-capsule exporter route** can preserve polymorphic source proof sharing and original statement identity using existing checked opaque-definition objects. It is selected only for an explicitly eligible source slice. It does not solve arbitrary proof-dependent nominal-group composition, and no global witness conflict is ignored.
- Fixing every transparent definition's native hint to `regular 0` has a separate source-backed avoidable unfolding family. Deterministic receiver-derived definitional heights are the selected concept improvement, subject to a newly qualified interpretation contract and checked native integer range.

Neither proposal makes proof irrelevance an excuse to copy an old acceptance cache or conceal actual dependencies. Fresh transformed artifacts still receive exact native checks and recomputed footprints.

## Existing exact contract

The frozen [V2 contract](../../spec/OPERATIONAL-CORPUS-V2.md) and [native-scaling note](CP-001E-native-scaling.md) distinguish:

- `JudgmentID`: exact universe arity, context/conclusion and recursively bound meanings;
- `ProofID`: that JudgmentID plus a native proof term whose theorem references name JudgmentIDs;
- `ReplayID`: exact root plus a canonical map W from reached JudgmentIDs to their selected ProofIDs.

For every reached theorem reference j, traversal follows W(j). A proof root p of j contributes the pair j ↦ p itself. Native environments and cached certificates must agree with the selected map. Conflicting map unions do not silently inherit old certificates. This is the actual contract being analyzed, not an imagined format with arbitrary proof-instance references.

The statement identity deliberately ignores source authors, names and chosen theorem witnesses. Definitions and opaque declarations still commit to exact bodies. Two opaque data values of the same type are not interchangeable merely because their types match.

## What proof irrelevance does and does not establish

Under the selected qualified Lean foundation, if Γ ⊢ p : P and Γ ⊢ q : P with Γ ⊢ P : Prop, native definitional proof irrelevance supplies p ≡ q at that same proposition. Congruence can therefore relate well-typed terms/types differing only in those proof arguments, under compatible declarations and universe instantiations.

This statement has important preconditions and limits:

1. The proofs must actually check at the same type. Equal printed names, a remote claim, or merely similar propositions does not establish that condition.
2. An independently checked proposition under different nominal inductive types or opaque data constants is not the same native interface by fiat.
3. The replacement may change the selected syntactic dependency/axiom footprint. Logical interchangeability does not imply equal actual evidence or unchanged policy admissibility.
4. Replacing source constants inside dependent declaration types must preserve scoping, universe substitutions and binding. The receiver checks the transformed result; the exporter is not a proof authority.
5. A theorem checker and its caches are concrete algorithms. A metatheoretic equality principle does not prove their cross-environment cache correspondence, completeness, or cost. In particular, the source's special treatment of proof computation such as accessibility recursion deserves qualification when theorem declarations become opaque proof-valued declarations.

For safe opaque declarations, the body is independently checked and retained in the selected closure even though ordinary native reduction does not unfold it. Opaque proof-valued capsules below are therefore not axioms. Arbitrary opaque data at a type in `Type` does not receive the proof-irrelevance argument.

## Baseline cycle and a stronger proof-dependent-context case

The frozen exporter already documents

\[
a : \mathrm{True} := \mathrm{True.intro},
\qquad b : \mathrm{True} := a.
\]

Both statements have the same JudgmentID j. Selecting b as W(j) while its body references j creates a self-edge. The original source is acyclic. Expanding the earlier a body, or selecting a instead, resolves this tiny example. Forking native environments alone does not change the encoded self-edge.

A related context example explains why replacing only obvious value-position aliases is insufficient:

\[
a : \mathrm{True},\qquad
c : a=a := \mathrm{Eq.refl}(a),\qquad
b : \mathrm{True} := (\lambda (\_ : a=a),a)\ c.
\]

This source graph is finite and acyclic. The canonical statement of c contains a theorem reference to j = JudgmentID(True). A new root b selected at j can therefore reach j again through **c's type**, even if another transformation hides b's direct reference to a. All type/telescope/body dependencies matter.

Proof irrelevance can support a checked transformation of this example. It does not justify omitting c's type from closure traversal or installing j as an axiom before b is proved. The selected restricted capsule route below intentionally detects such dependencies rather than claiming that a values-only rewrite universally solves them.

## Exponential literal-expansion family that survives raw DAG sharing

### Fixed checked background

Take a checked universe-polymorphic singleton `U.{u} : Sort u` with constructor `unit.{u} : U.{u}`; a standard PUnit-style safe inductive suffices. Take checked definitions

\[
I^{\{u\}} : U^{\{u\}}\to\mathrm{True},
\qquad I^{\{u\}}(x):=\mathrm{True.intro},
\]

and

\[
K : \mathrm{True}\to\mathrm{True}\to\mathrm{True},
\qquad K(a,b):=a.
\]

These are ordinary fully checked declarations with no new axioms. They are intentionally simple: the family isolates representation expansion, not difficult mathematics.

Fix N and the universe parameter list `(u,v₁,…,v_N)`. Every source theorem pᵢ has exactly that universe arity and proposition True, even though some declared parameters do not occur in its type. Unused declared universe parameters are not fresh existential metavariables. Native term/parameter range checks still apply.

Targeted source check supports this detail: pinned `environment.cpp:127–132` checks duplicate universe names and checks the declaration type against the supplied parameter list, but does not require every supplied parameter to occur in the type. `type_checker.cpp:85–90` rejects referenced undeclared parameters; lines 101–122 require a constant's actual universe-vector length to equal its declared arity. Thus this family supplies all N+1 actual universe arguments at every predecessor occurrence; it does not infer them from the printed proposition True or silently erase unused arity. The source's `Init/Prelude.lean:42` defines `PUnit : Sort u`, supporting the stated ordinary polymorphic singleton pattern. These are source observations, not an executed instance of the family.

Define

\[
p_0^{\{u,\vec v\}} := I^{\{u\}}(\mathrm{unit}^{\{u\}})
\]

and for 1 ≤ i ≤ N,

\[
p_i^{\{u,\vec v\}} :=
K\left(p_{i-1}^{\{u,\vec v\}},
       p_{i-1}^{\{\max(u,v_i),\vec v\}}\right).
\]

Each declaration is a proof of True under its previous checked declarations. Every theorem statement has the same exact JudgmentID, including the fixed universe arity. Each source body has two predecessor references and their explicit universe vectors. The full source term data use O(N²) universe-vector entries, not exponential information. The arity limit must of course accommodate N+1; an asymptotic family means an explicitly sufficient finite profile or growing qualified operational envelope.

### Exact expansion claim

Consider the literal fallback that eliminates these conflicting source theorem aliases by recursively substituting earlier proof bodies at each explicitly instantiated occurrence, while preserving ordinary definition references I and K and doing no proof-term evaluation or replacement by a different proof.

At depth N it contains an instance of I at a level

\[
L_S=\max(u,\{v_i\mid i\in S\})
\]

for every subset S of `{1,…,N}`, with the parenthesization induced by source substitution. There are 2ᴺ such distinct level substitutions. Even algebraic max normalization cannot identify different subsets in general: choose one vᵢ to be strictly above u and all other parameters to distinguish subsets that disagree on i. Raw Native2 identity does not perform that algebraic quotient in any event.

The constant applications `I.{L_S}` are therefore distinct expression nodes. A canonical syntax DAG can share equal subexpressions, but cannot identify these unequal universe-instantiated constants. The expanded root has at least 2ᴺ such nodes. Shared uninstantiated predecessor bodies in the **source declaration graph** are precisely what literal elimination removed.

This is stronger than a binary duplication example using the same closed proof twice: that simpler example can remain linear as a DAG and would not justify an exponential claim. It is also not evidence of an unavoidable exponential mathematical proof. Here, evaluating I/K or choosing p₀ as the exported witness yields a tiny proof. Those are different checked transformations and may change the exact artifact and conservative syntactic support. No proof-complexity lower bound, typical-library frequency, or executed runtime is claimed.

### Practical interpretation

The phrase "expand earlier proof bodies" is not a cost-qualified universal exporter algorithm. A competent exporter may perform bounded simplification or choose another existing witness, but it must report which transformed proof was actually checked. It cannot promise to preserve every source derivation efficiently merely because the original source graph was acyclic and each individual body was small.

## Selected bounded exporter improvement: checked proof capsules

### Eligibility is exact, not a heuristic truth decision

Select a finite source theorem slice T, a set T_out ⊆ T of selected wrapper exports, and a fixed retained non-theorem/background closure A. Capsules are generated for T; not every internal source theorem must receive a separately published wrapper. The initial capsule route applies only when:

- The source dependency graph being transformed is finite and acyclic, with complete bodies and exact universe-parameter lists available.
- Every theorem in T has a checked proposition type whose normalized canonical type/telescope contains no theorem reference back into T. References to fixed external theorems are allowed only with one already agreed exact selected replay under this route.
- Every preserved definition, opaque declaration, inductive descriptor/generated interface and background theorem closure in A has no dependency back into T. This is checked over types **and** values/constructor/generated-rule support, not only pretty-printed signatures.
- Let W_A be the complete compatible union of every retained background theorem witness map, including witnesses reached through all retained types/bodies/generated interfaces, and let J_out be the exact canonical JudgmentIDs of all wrappers selected for export. Require `dom(W_A) ∩ J_out = ∅` for this initial route. This is a canonical-identity check, not source-name nonmembership: an outside source theorem can have the same JudgmentID as a theorem inside T. Before accepting a wrapper, recompute its exact map and union its actual root pair under the unchanged V2 rule. A bounded re-plan may move eligible colliding earlier source proofs into T and repeat **all** eligibility checks; otherwise decline. Merely omitting the colliding witness from a manifest is forbidden.
- The original root statement is representable unchanged over that canonical background. No nominal inductive type is cloned and silently identified with its original.
- All generated capsules, root wrappers, retained backgrounds and actual transformed terms fit the independently funded envelope and pass ordinary Native2 reconstruction.

This is deliberately a sufficient restricted route. A producer reports ineligibility or nondecision when the guard fails; it may then use a separately checked bounded transformation, choose another already valid witness, or decline. It does not relax the V2 global-map rule.

The initial draft missed the canonical T/A boundary check. Both the root reviewer and native producer reviewer independently gave `T={b : True := a}` with fixed external `a : True := True.intro`: no source-name backedge exists, but a's selected JudgmentID conflicts with b's new wrapper root. The added disjointness guard rejects that plan or moves a into the newly checked capsule slice. This is a repaired exporter eligibility defect, not a permitted receiver acceptance bypass.

### Deterministic transformation

Process T in source dependency order. Ties can use the resulting canonical capsule payloads/IDs once their dependencies are resolved; source names do not enter a content identity. For each source theorem t:

1. Keep its exact universe-parameter order and canonical proposition type over A.
2. Rewrite each occurrence of an earlier theorem s in T, preserving its full universe vector and application spine, to the corresponding checked proof-valued opaque constant Cₛ.
3. Emit one safe `OpaqueDefinition` capsule Cₜ with that proposition type and the rewritten complete body. Its identity commits to its actual type/body and earlier capsule IDs. It is not an opaque axiom, remote binary, or hidden source plugin.
4. Reconstruct/check Cₜ against the actual already checked background and earlier capsules. A failed conversion, unsupported operation or exhausted native budget does not become success.
5. For each selected root in T_out, emit its `Proof` with its **unchanged original JudgmentID** and the exact context application described below. Check that wrapper independently.

For an original wire judgment `J = (uArity, Γ, φ)` with Γ containing n ordered variables, the capsule type is the closed `Π Γ, φ` and its rewritten value is the corresponding closed lambda abstraction of the original source proof. The wrapper proof payload, interpreted under Γ, is `C_t.{u₀,…,u_(uArity−1)} x₀ … x_(n−1)`: in de Bruijn form these arguments are indices `n−1,…,0` in that order. With n=0 it is just the universe-instantiated capsule constant. The existing Proof reader, not the exporter a second time, closes that payload with λΓ before native theorem insertion. This preserves the original context/conclusion split and universe ordering; replacing J by a differently placed closed-forall statement would be a different identity.

Opaque capsules are already a selected mathematical object kind in Native2. This proposal changes the untrusted export recipe, not the native acceptance rule or the frozen E schema. The extra evidence objects are explicit and fully charged.

Within the eligibility contract, the theorem references that caused identical-JudgmentID collisions are now exact capsule references inside the proof implementation. They no longer select one another through W(j). The root map still contains its own required singleton and every actually reached fixed external theorem witness; map exactness and cycle checks remain unchanged.

### Statement identity and size argument

The root's telescope/conclusion and semantic declaration identities are unchanged. Capsule IDs occur only in its proof implementation/selected support, not in the original statement descriptor. Hence the exact JudgmentID is preserved while ProofID/ReplayID intentionally change.

Every source theorem body is transformed once without universe instantiation of its predecessor's body. Universes remain arguments on ordinary constant references. If B is the complete source/native input syntax size of the eligible slice and A its already shared background, generated capsule payload is O(B), with linear wrapper/declaration overhead in the number of source theorem vertices and ordinary exact content-ID storage. This does not bound arbitrary kernel conversion cost, physical graph bookkeeping, or unknown background acquisition.

For the explicit family above, Cᵢ references Cᵢ₋₁ twice at different universe vectors and retains one polymorphic body. Capsule syntax stays O(N²), avoiding the literal export's 2ᴺ instantiated leaves. Each capsule's declared type is True, so this paper family does not rely on a hard convertibility test between complicated proposition types.

Independent eligible branches may use distinct capsules for two proofs of the same proposition; their bodies and supports can coexist as ordinary opaque declaration IDs. A later checked proof can reference both capsule values without a JudgmentID-to-two-values map conflict. The actual retained footprint includes both closures if both are syntactically referenced. Removing one unused proof is a new checked simplification, not silent footprint reuse.

### Honest limitations

The c : a=a example above is outside the simple eligibility guard if a belongs to T. More general source types can contain proof arguments, and definitions/inductives can incorporate those proofs in their own descriptors. Rewriting those occurrences can change DefinitionIDs or GroupIDs and hence the root statement. Fresh inductive groups are nominal interfaces: proof irrelevance alone does not make two separately generated groups equal.

The initial route therefore does **not** establish efficient round-tripping of every practical Lean environment, nor eliminate every branch-unification problem. A future evidence-instance graph or checked context-transport scheme may address a larger class, but selecting that would require its exact identity, decoder, nominal-interface, cache, footprint and grounding contracts. This note does not smuggle such a schema in as an optimization.

## Native environment selection is not source provenance

The producer-side investigator reports a relevant pinned source behavior: `Lean.Environment.subsumesInfo` treats same-name/same-type/parameter-list theorem records specially using proof irrelevance and largely opaque theorem behavior; module import can keep one complete body rather than preserve every branch-local body. The source comment also mentions the practical accessibility-recursion caveat. This reviewer has received that source finding from the independent producer investigator; it has not executed module import or independently reproduced all of that path.

Consequently, an exporter starting from a finalized merged environment can export the complete body it actually retrieved. It cannot claim that body necessarily preserves every module's original alternative derivation. If exact branch-specific evidence matters operationally, producer-controlled per-module/declaration-time capture must supply it; attribution is not the issue. The resulting capsules/proofs still receive ordinary native checks and explicit footprints.

No network identity or global ledger repairs information already discarded by a producer's source environment. Conversely, preserving all source alternatives is not necessary to establish the common proposition if one permitted complete proof is available.

## Independent finding: regular-zero hints can destroy cheap incremental conversion

### Source facts inspected directly

At Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`:

- `Declaration.lean` lines 26–36 describe regular definitional heights and unfolding the greater height first; the elaborator derives height as one plus the maximum regular height referenced by the definition body.
- `type_checker.cpp` lines 1026–1047 compare the two hints. Unequal heights unfold one side; equal hints unfold both sides, except the stated same-definition/application congruence shortcut.
- `type_checker.cpp` lines 1187–1206 first use weak-head reduction without delta, then proof irrelevance, then this lazy-delta path.
- `environment.cpp` lines 192–206 construct a fresh type_checker for each checked theorem insertion. Earlier theorem insertions do not automatically donate their private definitional-equality cache to the next checker.

These are read-only observations of the named source, not observed timings or a proof about every caller/build/runtime.

### Explicit family

Let checked transparent definitions be

\[
d_0 : \mathrm{Nat} := 0,
\qquad d_i : \mathrm{Nat} := d_{i-1}.
\]

For i ≥ 1, use the reflexivity proof with inferred type `dᵢ = dᵢ` at the declared proposition `dᵢ = dᵢ₋₁`. This is mathematically valid by one unfolding of dᵢ. Checking definition bodies needs their predecessor's type Nat, not normalization of the chain.

Under all-regular-zero reconstruction, the relevant fresh comparison is between two distinct transparent constants dᵢ and dᵢ₋₁. They are data terms, not proofs, so proof irrelevance does not solve it. They are not two applications of the same definition, so the same-head shortcut does not apply. Equal hints unfold both to dᵢ₋₁ and dᵢ₋₂; the inspected reduction path walks toward the base. With no preexisting cache entry for these comparisons, there are Θ(i) such chain steps.

With strictly derived dependency heights, h(dᵢ)>h(dᵢ₋₁). The same source branch unfolds dᵢ alone, leaving identical dᵢ₋₁ terms, so this particular comparison ends after one delta step. For N independently checked fresh theorem insertions along the family, these comparison steps can total Θ(N²) under regular-zero versus O(N) with derived heights, even when the unchanged declaration environment is already available. This counts the displayed conversion steps, not all parsing/closure/checking work or wall-clock time.

Cross-request native conversion caching could change that workload, but is not provided automatically by environment reuse; the inspected checked insertion makes a fresh checker. Such a cache would itself need qualified semantic/environment keys. It is unnecessary to invent one to recover the intended unfolding priority in this simple family.

### Selected deterministic height rule

For each contributed transparent definition d, after its exact earlier dependencies are established, select

\[
h(d)=1+\max\left(\{0\}\cup
\{h(c):c\text{ is a regular transparent constant syntactically referenced in }d\text{'s value}\}\right).
\]

Apply this same deterministic rule to **every reconstructed ordinary transparent seed definition**, in its qualified acyclic bootstrap order, as well as contributed transparent definitions. The inherited seed descriptor grammar does not serialize arbitrary source hints; therefore "use whichever source seed hint was observed" would leave reconstruction ambiguous. Theorem constants, inductive primitives and genuine opaque declarations do not become transparent regular definitions. The rule considers the complete value DAG's constant occurrences without beta/delta expansion. Existing source producer hints are not trusted or serialized as authority. Equivalent sources with the same canonical body/dependencies derive the same height independent of author, name and publication order.

The native field is UInt32. Compute with checked arithmetic; an out-of-range height gives explicit unsupported-range/nondecision under this initial rule, not truncation, wraparound, or a policy-dependent identity change. Heights are receiver-derived qualified metadata, but their exact reconstruction rule belongs to the interpretation contract. The selected CP-001F integration names this rule **HEIGHT1**, assigns `NativeRules.ruleSchemaCode = 3` to Native2 plus HEIGHT1, and consequently obtains a new NativeRulesID and FoundationID. It does not rewrite rule code 2 or inherit an old checker/adapter certificate as though nothing changed. Bootstrap materials and reconstruction/semantic-option keys must bind that new choice. This note does not reinterpret frozen E objects in place.

The source supports a concrete cost improvement for the displayed family. It does not prove that derived heights are optimal, that every source hint choice should be reproduced, or that the entire checker is complete/order-independent under every hint policy. Receiver-side checked reconstruction and practical qualification remain required.

## Exact renaming: conditional correctness, not "names never matter"

An injective consistent renaming of ordinary nonreserved declarations, applied to every constant/projection/group-member occurrence and preserving universe ordering/binding, should preserve the intended typed derivations under an equivariant kernel extension interface. The qualification premises are substantive:

- Fixed reserved bootstrap names stay fixed. Native arithmetic, strings, quotient initialization and other recognized names cannot be freely hashed away.
- Group-local binder references are not arbitrary external names. Reconstruct the same admitted inductive descriptor and check its regenerated constructor/recursor inventory, including all external rule dependencies.
- Numeric projection selectors, constructor ordering, recursor selectors and universe vectors remain exact. A human field label is not a renaming proof.
- Private/source names can be omitted only after all their actual referents are mapped. A missing proof body or name lookup does not become a new axiom.
- Merging identical content is stronger than injective renaming. Distinct theorems can merge semantically only under actual same-proposition evidence; distinct definitions/groups/opaque data still require their exact canonical identities and admitted interface behavior.
- Equal native mathematical meaning does not imply identical checker performance. Name-sensitive heuristics, reserved names, generated auxiliaries and changed hints must be audited against the actual qualified source path; source elaboration and plugins remain outside receiver acceptance.

The capsule route keeps original canonical semantic names in the eligible root interface and creates separate content-addressed evidence constants. It does not purport to prove a universal name-equivariance theorem for arbitrary Lean plugins or source-level elaboration.

## Required paper and future conformance cases

- Two independent valid proofs of one exact JudgmentID with different permitted footprints: neither copied acceptance nor global-map conflict suppression is allowed.
- Same-statement alias chain with identical universe instantiations: verify that ordinary DAG sharing is accounted rather than falsely charging a binary tree.
- The subset-universe family above: compare actual source DAG size, literal substituted DAG size and capsule payload size; separate optional simplification as another checked artifact.
- Proof-dependent statement `c : a=a`: eligibility detects the type dependency; it is not missed by a value-only traversal.
- A background definition or inductive descriptor uses a proof in T: capsule route refuses unchanged-interface claims until an explicit checked transformation is selected.
- An outside source theorem and an exported wrapper share the same canonical JudgmentID despite different source names: exact background witness-domain disjointness detects the collision; bounded slice expansion rechecks eligibility or the route declines.
- An opaque data constant at Type versus an opaque proof at Prop: proof irrelevance must never be applied to arbitrary data.
- Two eligible branches with different same-proposition capsules: both exact evidence closures remain visible, and a checked join reports their actual union footprint.
- A source import has already selected one same-name theorem body: exporter reports that selected body, not fictional recovery of all earlier module bodies.
- The dᵢ conversion family: compare regular-zero and deterministic derived-height paths under fresh checked declaration insertion; do not advertise source inspection as an executed benchmark.
- Native height overflow, missing dependency hints, or changed interpretation version: explicit nondecision/new qualification, never silent wrap or cache reuse.
- Reserved string/arithmetic/quotient names and nested generated members: exact checked reconstruction, not universal free renaming.

## Decision boundary

This note selects a restricted existing-schema capsule export improvement and a source-neutral derived-height interpretation improvement. The former is not universal proof-instance composition; the latter is not a claim that arbitrary native checking becomes linear. Both directly address identified avoidable mechanisms while preserving actual checking, statement/evidence separation, exact footprints and finite resource admission.

Broader compatibility remains an explicit project question: can arbitrary proof-dependent nominal contexts be imported and joined efficiently without unstable statement identities or unqualified proof-instance/environment equivalences? That question is not answered by the examples here. It should not be concealed behind "the kernel will check" or a claim that proof irrelevance makes all environment histories interchangeable.

## Sources and trace

- [Frozen V2 operational contract](../../spec/OPERATIONAL-CORPUS-V2.md).
- [Frozen native scaling and global witness-map rules](CP-001E-native-scaling.md).
- [Frozen original mathematical contract, source alias fallback and regular-zero reconstruction](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md).
- [Pinned declaration hints and their documented comparison](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Declaration.lean#L17).
- [Pinned lazy delta-reduction and hint comparison](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L999).
- [Pinned checked theorem and opaque insertion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp#L192).
- [Pinned universe declaration checks](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp#L127) and [constant universe-arity checks](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L85).
- [Pinned polymorphic singleton declaration](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Prelude.lean#L42).
- Producer-side source investigator's independent message on `Environment.lean` subsumption/import behavior; this note explicitly distinguishes that received finding from the directly inspected C++ checking/hint paths.
