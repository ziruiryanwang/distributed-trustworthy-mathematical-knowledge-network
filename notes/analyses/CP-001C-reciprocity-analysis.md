# CP-001C analysis: reciprocal mathematical reuse and contribution

Date: 2026-09-19. Status: concept analysis for synthesis and audit; not an implementation, measured productivity result, or replacement for the frozen specifications.

This note develops the main product requirement: an independent local agent can obtain useful mathematical material, build new work on it reliably, and return material that another independent agent can use in turn. It reads CP-001A, CP-001B, and the mathematical, evidence, acceptance, and repair portions of Cooperation Core v0 as its baseline. Existing resource authority, native-checker requirements, and receiver-local reliance semantics remain in force. The proposed additions below concern mathematical interfaces and the reciprocal production cycle.

## The requirement being specified

The commons should be a durable and searchable medium for mathematical work, with a narrow checkable boundary for what may support a formal conclusion. It must support both immediate reuse of results and the slower acquisition of useful methods, abstractions, and representations. These have different acceptance conditions.

The core reciprocal cycle is

\[
\text{discover}\longrightarrow\text{import and check}
\longrightarrow\text{independent work}
\longrightarrow\text{validate and package}
\longrightarrow\text{publish}\longrightarrow\text{another agent's reuse}.
\]

Every arrow needs a contract. A publication count measures only one intermediate event. A checker accepting a theorem measures only a different intermediate event. The product succeeds when these events repeatedly enable downstream work under explicit reliability and resource constraints.

No distinguished root research goal is necessary. The agents in one reuse chain need not know one another, be online simultaneously, share a priority function, or have coordinated their investigations. A local question can change between generations. A mathematical package can exist without a work item or research program.

### Reciprocal capability, rather than compulsory exchange

Reciprocity means that the framework supports both directions: local work can use the commons, and local outputs can improve it. It does not imply that each downloader must upload an equal amount, that each imported theorem incurs a debt, or that contributions entitle their sender to other people's resources. A read-only student, an intermittently connected researcher, an archival node, and a proof-producing agent are all legitimate participants.

Consequently, openness of the format and the ability to run a verifier are distinct from guaranteed storage, guaranteed discovery, and guaranteed execution of unsolicited work. Those latter services consume finite resources. CP-001A's receiver admission and CP-001B's funded retention constraints apply to every proposed contribution.

## A reusable object is more than a theorem string

A knowledge package has an immutable mathematical payload and separable operational observations. The former records what was asserted, defined, or demonstrated. The latter records what a particular receiver checked, retained, or currently relies on. Another receiver cannot inherit the latter as authority merely by downloading the former.

The following is a conceptual record contract, not a wire schema or implementation:

| Component | Required meaning |
|---|---|
| Content identity | Domain-separated identity of a canonical typed representation, including its schema version |
| Kind | Definition/interface, derivation, counterexample/model, certified computation, partial, method, relation/translation, or heuristic material |
| Exact semantic endpoint | Foundation and logic profile; exact theory/declaration environment; local parameters, assumptions, and conclusion or output type |
| Reuse interface | What an importer must provide; what the package then provides; side conditions; permitted modes of instantiation |
| Native payload | Proof term, independently checkable certificate, explicit model, typed transformation, or marked heuristic payload |
| Dependency manifests | Exact identities and typed roles of the dependencies needed at each claimed validation/reuse boundary |
| Assumption inventory | Conservative transitive logical assumptions and unsafe/axiomatic features of the selected evidence, obtained or verified independently of the producer's claims |
| Validation recipe | Pinned checker relation, supported input representation, required environment, and declared operational bounds |
| Remaining obligations | Explicit open assumptions, side conditions, missing translations, fidelity conditions, or unresolved subproblems |
| Discovery description | Bounded structural keys and optional natural-language explanations; useful for finding candidates but without proof authority |
| Reproduction/reuse material | Exact source and native artifacts appropriate to the claimed public reuse class, and optional examples or adapters |

Producer assessment, provider availability, popularity, local retention activation, and local reliance epoch are separate records referring to that content. They must not mutate its mathematical identity. Public-reuse claims require the available native closure specified by the receiver's contract; a succinct proof about unavailable native material alone does not meet the current strict P0 reuse contract.

### Several contribution types have legitimate mathematical value

| Contribution | How it can help later work | What it cannot establish by itself |
|---|---|---|
| Checked theorem | Discharges a matching obligation or supplies a premise through checked instantiation | Fidelity to an unspecified informal intention |
| Definition or interface | Supplies a shared vocabulary and reusable abstraction boundary | Existence, consistency, usefulness, or conservativity merely because a definition was published |
| Checked counterexample | Eliminates an exact claim or exposes a missing hypothesis | Falsity of differently quantified or differently scoped claims |
| Checked finite computation | Establishes a bounded statement or certificate-defined relation | An unrestricted generalization outside the certificate's scope |
| Typed partial proof | Reduces a target to explicit residual obligations through a checked transformer | Closure of the original target before those obligations are discharged |
| Method or tactic | Produces candidate proof terms, decompositions, or certificates | Correctness of each output unless checked or covered by an applicable verified transformation theorem |
| Informative failure | Records a bounded search, obstruction, or useful intermediate | Unprovability of the goal; only certified exhaustion can justify the corresponding bounded exclusion |
| Certified theory map | Allows transport across a stated portion of two exact theories | Automatic interoperability across arbitrary libraries or foundations |
| Example, explanation, analogy | Improves learning, discovery, or problem formulation | A formal support edge or semantic equivalence |
| Better packaging or index relation | Makes existing valid work substantially easier to find and import | New mathematics solely from a different name or listing |

This avoids two mistakes: excluding useful non-theorem contributions, and granting non-theorem contributions more evidential force than their contracts justify.

### Definition: two modes of reuse

**Support reuse** is use of a package as a premise, certificate, or checked transformation in an accepted derivation. It must satisfy the exact acceptance contract.

**Search or learning reuse** is use of a package to influence what is attempted: choose a conjecture, tactic, representation, premise candidate, or next experiment. It has no direct authority over formal acceptance. Its generated outputs pass through the ordinary acceptance boundary.

The same package can participate in both modes. A correct theorem about an unapproved foundation may inform a proof strategy without being an admissible premise in the receiver's current theory. A failed attempt may teach a tactic selector while proving nothing about the mathematical goal.

**Invariant: no promotion of epistemic strength by copying.** If an object is only a hint in its declared contract, republishing it, training on it, summarizing it, signing it, or collecting many endorsements does not turn it into a checked proof. A stronger grade requires new evidence satisfying a stronger contract.

## Exact theory identity and interfaces

Let an exact formal judgment be

\[
J=(L,E,\Gamma,\varphi),
\qquad E;\Gamma\vdash_L\varphi,
\]

where \(L\) identifies the logic and primitive inference rules, \(E\) the immutable declaration environment, and \(\Gamma\) the ordered local context. In dependent formalisms, the order and types in \(\Gamma\) matter. The schema also binds elaboration choices that remain semantically material in the native representation: type instances, coercions, universes, implicit arguments, and overloaded symbols.

Two occurrences of `group`, `continuous`, or `sum` with the same printed name need not have the same meaning. A theorem whose text looks identical may differ through an imported definition, quotient construction, convention, hidden instance, or axiom. A hash of the informal text does not identify \(J\).

### Definition: reusable semantic interface

An interface \(I\) consists of an exact signature \(\Sigma_I\), a telescope of assumptions \(\Delta_I\), exported types or judgments \(\mathcal E_I\), and explicit side conditions. A module implementing the interface supplies a typed assignment \(\theta\) for the signature and checked evidence for the substituted assumptions.

The interface is intentionally small enough to express what clients use. Its implementation may be larger. The package still retains exact dependency material needed to validate the particular implementation; a small interface is not permission to omit required proof closure.

For example, a list-fold theorem should expose monoid operations and laws, not silently require one particular matrix library or all the axioms imported by an unrelated development. Interface minimization improves portability, but determining a minimal logical dependency set in general is not required or claimed. A mechanically verified conservative overapproximation is safe; a producer's unverified minimality assertion is not.

### Three distinct kinds of identity or relation

| Relation | Evidence needed | Permitted action |
|---|---|---|
| Exact content identity | Verified canonical content identity | Byte/object deduplication |
| Judgment identity under a specified normalization | A fixed sound normalization with exact context binding | Matching in that precisely defined representation |
| Mathematical equivalence or transport | Applicable checked implication, equivalence, or theory-map evidence | Only the certified substitution, transport, or derived conclusion |

Universal semantic deduplication is not a prerequisite. It would demand decisions that are unavailable in general. Independent formulations may coexist; a later contribution can supply a certified relationship between them. This makes library diversity a manageable translation problem without pretending that equivalence can always be decided.

### Definition: an import contract

For receiver \(i\), an import contract \(q\) fixes:

- the target judgment or interface and its exact target context;
- the admissible logic/checker profiles and evidence bases;
- the permitted transitive assumption/features policy;
- any semantic-fidelity condition;
- the native-closure and availability requirements;
- the allowed interface-instantiation or theory-transport rules;
- local freshness/reliance requirements and operational ceilings.

These are a refinement of Core v0's `RelianceQuery` and evidence/fidelity contracts, not a new competing truth procedure. A package is reusable for \(q\) only if Core's current-epoch \(\operatorname{Stable}_i(q;A_i,O_i)\) holds for the selected evidence tree, including the target-side match or transport.

Changing \(q\) changes the acceptance question. An artifact accepted under classical logic cannot be inserted into a constructive-only query just because both queries display the same conclusion.

## Compositional checking and assumption hygiene

### Definition: logical footprint

For a selected finite native derivation \(\pi\), let

\[
\operatorname{Foot}(\pi)
=\bigl(L,\operatorname{Ax}(\pi),\operatorname{Features}(\pi),
\operatorname{Decls}(\pi)\bigr)
\]

be a receiver-verified conservative footprint: primitive logic profile, undischarged logical axioms used transitively, relevant trusted or unsafe features, and exact referenced declarations. Ordinary locally bound premises remain explicit in \(\Gamma\). This footprint is computed from or checked against the actual native derivation and recursively validated declarations. It cannot be taken from an unchecked manifest field.

An imported declaration is either checked with its required proof closure under the current contract, admitted as an explicit allowed axiom, or unusable for strict proof support. Calling it a theorem does not create a fourth case. A cached validation can replace repeated work only under its exact validation key and the current policy/incident constraints.

**Axiom transparency invariant.** For every accepted selected tree \(T\),

\[
\operatorname{Ax}(T)\subseteq\operatorname{AllowedAx}(q)
\]

when the policy is expressed as an allowed set. More general policies use an explicit mechanically evaluated predicate over the entire footprint. Every added proof rule, oracle, proof-producing runtime assumption, or admitted external statement appears in the appropriate declared basis. An outer proof cannot hide the use of a forbidden assumption inside a dependency.

**Counterexample: axiom laundering.** Package A declares \(a:\bot\) as an axiom and derives \(p\). Package B imports A and presents a small proof of \(q\) from \(p\) or from another theorem whose closure uses \(a\). Inspecting only B's source, or only whether B contains a literal `axiom`, misses the defect. A transitive verified footprint exposes \(a\). If a receiver explicitly admits an inconsistent axiom theory, derivability in that theory remains a conditional fact; it is not trustworthy unconditional mathematical truth.

### Proposition: conditional compositional soundness

Fix a target logic \(L\), exact declaration environment \(E\), and local context \(\Gamma\). Suppose:

- every primitive checker accepted by the selected contract is sound for its stated judgment relation;
- all exact parsing, hash, environment-binding, and dependency checks used by that relation succeed;
- each selected imported derivation has a finite verified closure and supplies its claimed judgment in \(E;\Gamma\), or is transported there by an accepted checked derivation;
- each composition edge is an applicable inference rule or a checked proof transformer in the same target logic;
- no residual assumption is omitted, and the entire selected footprint satisfies the receiver's policy.

Then every root accepted by the finite composition tree is derivable in the declared target theory with the declared remaining assumptions.

**Proof sketch.** Induct on tree height. Checked leaves establish their exact judgments relative to the stated axioms and context. At each internal node, target-side typing, substitution, and premise matching establish the hypotheses of the accepted rule or transformer. Rule soundness establishes its conclusion. Finiteness supplies a base case and excludes unsupported cycles. Footprint verification prevents the induction from silently strengthening its assumptions.

This proposition does not establish the truth or consistency of all chosen axioms, the correctness of an informal interpretation, or the absence of checker bugs. A separate semantic conclusion requires a model in which the accepted axioms and assumptions hold and soundness of \(L\) for that model. Those are explicit metatheoretic assumptions, not rewards for network consensus.

### Counterexample: circular apparent contribution

Agent A publishes \(p\) justified only by agent B's \(q\); B publishes \(q\) justified only by A's \(p\). Both packages are signed, indexed, and frequently downloaded. There is still no grounded derivation. Core's least fixed point contains neither unless another accepted leaf provides grounding. Mathematical induction, coinduction, and recursive definitions require their own checked rules; message cycles are not substitutes.

### Composition must respect dependent interfaces

In dependent type theory, a partial or interface may have obligations

\[
\Delta=(d_1:D_1,\ d_2:D_2(d_1),\ldots,d_m:D_m(d_1,\ldots,d_{m-1})).
\]

The importer must supply a well-typed dependent substitution, not an unordered bag of superficially matching results. Solving each printed goal independently is insufficient if later types depend on earlier chosen witnesses. Transporting equal witnesses may itself require checked equality evidence.

## Useful partials, failures, and methods

### Checked partial proofs

A useful partial proves a reduction of work:

\[
E;\Gamma,\Delta\vdash_L\varphi,
\]

where the residual telescope \(\Delta\) is completely explicit. Equivalently, it supplies an applicable typed proof function from the residual evidence to the target. Unbound metavariables and hidden admitted holes are not accepted residual contracts.

**Partial-completion rule.** If the receiver checks the partial and a well-typed dependent substitution \(\theta\) of checked evidence for all members of \(\Delta\), substitution yields a derivation of \(E;\Gamma\vdash_L\varphi[\theta]\). The unchanged conclusion \(\varphi\) is justified only when it is independent of the discharged residual variables. For example, supplying \(n=0\) to \(\Delta=(n:\mathbb N)\) and \(\varphi=(n=n)\) yields \(0=0\), not a judgment containing the now-unbound \(n\). Before substitution, the instantiated closed target is not supported by this partial.

The package should additionally expose which residual obligations are independent, which depend on witness choices, and the exact context of each. Such annotations are checked if used to authorize parallel composition. Mere scheduling hints need not be proof-grade.

A partial can be mathematically valid but unhelpful: the identity reduction from \(\varphi\) to \(\varphi\) closes nothing and reduces no cost. A positive utility claim therefore needs observed or assessed downstream improvement; validity alone does not establish progress.

### Failure and exclusion

Keep the following propositions distinct:

\[
\text{this run failed},\quad
\text{no solution in this certified finite region},\quad
\text{the mathematical statement is false}.
\]

The first is an execution observation. The second requires certified exhaustive coverage of a precisely defined region. The third requires an appropriate mathematical refutation. Neither implication between successive expressions holds in general.

A failure object binds the exact context, solver/executable, parameters, search-region definition, bounds, nondeterminism policy, and any independently checked obstruction. As in Core, it can suppress a proposed search only when certified exhaustion and a checked region-containment relation apply. Ordinary timeout data can guide ranking while leaving the search available.

### Methods and proof-generating tools

Three methods of packaging a strategy have different contracts:

- A heuristic generator returns candidate native evidence. Each output is checked.
- A verified transformation theorem establishes that a specifically represented transformation preserves a judgment under stated preconditions. Each use checks those preconditions and binds the exact transformation representation.
- An empirical method capsule records observed performance on a declared task distribution. It may guide local scheduling but is neither a proof of universal effectiveness nor a formal justification of future outputs.

Executing a contributed method is a separate operational action requiring the existing sandbox and resource authority. Reading a mathematical object or importing a proof must not implicitly execute publisher-selected build scripts with ambient authority.

## Multiple foundations and independently evolving libraries

The commons can contain Lean, Rocq, Isabelle/HOL, set-theoretic developments, or other formalisms without declaring that their assertions are automatically interchangeable. Their exact foundations and primitive rules belong to their identity. Initially supporting one native profile is a scope choice, not a claim that other mathematics is illegitimate.

### Definition: certified scoped transport

A transport package identifies exact source and target theories, the mapped source subtheory \(D\), the translation of symbols and judgments, all side conditions, and evidence sufficient for the target checker to accept transported results in its stated scope.

For a suitable same-logic interpretation, it must show that the translated declarations type-check and each used source axiom is derivable in the target. Across different logics, an axiom map alone is insufficient: the translation must also account for the used inference rules, binders, computation/equality principles, and relevant semantics. A generally sound translator may have a metatheorem, but the current strict profile still requires target-native evidence or a supported target certificate for each accepted use.

If \(S|_D\vdash\varphi\), all dependencies lie in \(D\), the transport obligations hold, and the target checker accepts the produced evidence, the receiver may use \(T\vdash m(\varphi)\). It cannot use an untransformed source expression as if it were already a target theorem.

**Counterexample: excluded middle.** A classical source theorem using excluded middle cannot become a constructive target theorem merely by renaming its symbols. A suitable translation may change the conclusion, or the target may explicitly admit a classical axiom. Both choices must be visible. Matching names and matching English explanations establish neither.

**Counterexample: representation change.** A finite-set theorem about extensional membership is not automatically a theorem about lists, where order and multiplicity matter. A map must discharge the conditions under which a list representation has the desired finite-set interpretation. Duplicate elimination and cardinality are mathematical obligations.

### Library evolution

A new library version is a new exact environment. A mutable label such as `latest` cannot occur in an accepted proof's identity. A migration package provides checked adapters, preservation statements, or transported proofs between named versions. The old and new developments can coexist.

If a refactor merely reorganizes an interface, the claimed preservation relation must still be explicit. If it changes a definition's mathematical meaning, no naming policy can make the old proof automatically apply. Discovery may suggest a likely replacement; acceptance requires the corresponding checked relation.

## Minimal local abstract machine

The following describes semantic transitions only. It is not code, a database schema, or a revision to the existing detailed resource ledger.

Let receiver state be

\[
\Sigma_i=(O_i,A_i,P_i,e_i,W_i,H_i,R_i),
\]

where \(O_i\) contains available immutable objects, \(A_i\) locally admitted facts, \(P_i\) policy, \(e_i\) reliance epoch, \(W_i\) bounded local work state, \(H_i\) bounded advisory hints, and \(R_i\) locally authorized resource/retention records. Indexes and current reliance answers are projections or caches over this state.

| Transition | Preconditions and observations | Semantic effect |
|---|---|---|
| Discover | A bounded local query or incoming hint under receiver policy | Add candidates to expendable hint state; no support is created |
| Select and fetch | Receiver grants the exact inherited bounded demand/reservation/claim path | Obtain verified bytes and declared closure, or report a bounded failure |
| Check import | Exact target contract, closure, checker relation, interface/transport evidence, and current policy are available | Produce a receiver-local immutable assessment; only accepted evidence can enter admitted support |
| Integrate | Accepted assessment plus required local admission/retention authority | Add exact evidence or typed non-supporting material; update affected state and epoch as required by Core |
| Work | A local question, captured exact inputs, approved tools, and finite resource authority | Produce fallible candidates, partials, methods, models, or failures; no automatic support |
| Validate export | Check the result, all declared dependencies, residuals, footprint, and requested export interface | Produce a self-contained or exactly resolvable package with the appropriate evidence grade |
| Publish | Local authority funds bounded advertisement and any promised retained closure | Expose a candidate to other receivers; no foreign acceptance is forced |
| Reuse elsewhere | Another receiver independently selects, fetches, checks, and integrates | Start a new local cycle under that receiver's own question and contract |
| Correct or lose availability | A relevant defect, override, policy change, or closure loss is locally admitted | Atomically change local reliance epoch and conservative dirty state; affected old acceptance cannot remain current |

Publishing an unchecked draft is permitted when its kind and evidence status remain explicit. It does not satisfy the validated public-reuse path. Likewise, exporting a locally accepted theorem does not make a different receiver's independent check unnecessary.

### Invariants of the cycle

- **Context preservation:** every formal support edge refers to exact source and target contexts and a checked matching/transport operation.
- **Footprint closure:** all transitive assumptions and declared trust features of the selected support path satisfy the receiver's exact contract.
- **Grounding:** accepted support has a finite grounded tree; work status, cyclic references, or remote acceptance markers cannot supply leaves.
- **Residual honesty:** a partial cannot advertise closure of obligations that remain open.
- **Grade preservation:** learning, summarization, signatures, and popularity cannot strengthen evidential status.
- **Receiver independence:** the sender cannot select the receiver's axiom policy, local budget, acceptance grade, or durable retention entitlement.
- **Version binding:** every reusable assessment names exact objects, checker/environment roots, policy, and relevant reliance epoch.
- **Correction safety:** an admitted local defect or unavailable required closure disables the affected current reliance immediately, even if impact recomputation proceeds incrementally.
- **Alternative preservation:** disabling one path does not disable a distinct checked alternative merely because both prove the same conclusion; a defect's scope is checked against exact dependencies.
- **Autonomy:** missing coordination scope, root research goal, historical credit, or producer work item cannot by itself make a mathematical package invalid.
- **Bounded induced work:** a publication cannot cause unbounded checking, indexing, repair, or retention without another receiver-authorized resource decision.

### Proposition: safe reciprocal composition

Assume each receiver obeys the conditional soundness premises above, imported packages enter formal support only through local checking, and each export binds the exact evidence actually used. For any finite sequence of agents \(i_0,\ldots,i_n\), an accepted result at the final agent remains derivable under that final agent's declared context and allowed assumptions, provided every required transport and selected native dependency closure passes its contract.

**Proof sketch.** The induction is over the final finite evidence tree, not publisher identities or publication chronology. Each generation contributes additional candidate evidence; the next receiver reconstructs an acceptable tree under its own contract. Repeating this operation adds no unexamined authority. A hostile intermediate agent can withhold, misdescribe, or corrupt a package, but those acts cannot establish the premises of the receiving check. They can still reduce availability, waste bounded work, or exploit a faulty trusted checker, which this proposition does not exclude.

This is a safety statement, not a theorem that researchers always discover useful new mathematics. There is no unconditional productivity or discovery guarantee in arbitrary mathematical domains.

## Three generations of actual mathematical reuse

This example specifies what an eventual demonstration should show; no software or measurement is claimed here.

### First generation: an independently useful algebraic lemma

Agent A studies folds over lists. In an exact monoid interface \((M,\cdot,e)\), it publishes a checked theorem

\[
\operatorname{fold}(x\mathbin{+\!+}y)
=\operatorname{fold}(x)\cdot\operatorname{fold}(y).
\]

The package exposes associativity and unit laws, list concatenation, the exact fold convention, and the native proof by list induction. It does not assume commutativity or cancellation. The agent need not anticipate any later use.

### Second generation: a range-aggregation theorem

Agent B independently studies range products. It discovers A's interface, instantiates it through a checked group-to-monoid map, and defines prefix products

\[
p_k=\operatorname{fold}(\operatorname{take}(k,x)).
\]

For \(0\leq i\leq j\leq |x|\), the list-splitting lemma and A's result give

\[
p_j=p_i\cdot\operatorname{fold}(x[i:j]).
\]

Group laws then establish

\[
\operatorname{fold}(x[i:j])=p_i^{-1}\cdot p_j.
\]

B publishes this new package with its own exact slice convention, index bounds, group obligations, and the checked dependency on A. Its reusable output contains mathematical material that A did not supply.

### Third generation: an integer sliding-window invariant

Agent C develops a local algorithm for moving sums of an integer sequence. It instantiates B's group theorem in \((\mathbb Z,+,0)\), thereby obtaining

\[
S_i=p_{i+w}-p_i
\]

for the sum of the half-open window \([i,i+w)\). Under \(w\geq1\) and \(i+w<|x|\), it uses the prefix-step equations and integer group laws to prove

\[
S_{i+1}=S_i-x_i+x_{i+w}.
\]

C can publish the recurrence together with an independently checked algorithm invariant and any separately established cost model. A proof of the recurrence alone does not establish the implementation's runtime complexity; that is another claim with another contract.

The chain has several testable properties: no shared root goal; no shared online session; exact formal instantiation; three distinct receiver checks; a later question that was not A's original question; and new reusable outputs at each stage. To establish an efficiency benefit, a future experiment must compare C's total cost including discovery, fetching, checking, and integration against a preregistered baseline. The existence of this dependency chain alone does not establish speedup or novelty.

### Failure variants of the same chain

| Variant | Why it fails | Required behavior |
|---|---|---|
| B imports A under natural-number addition and subtracts by an inverse without additional premises | A monoid does not supply group inverses; truncated subtraction has different laws | Reject the claimed instantiation or expose new obligations |
| B writes \(p_j\cdot p_i^{-1}\) for the range product in a noncommutative group | Factors cannot generally be reordered | Target checking rejects it; a concrete noncommutative counterexample can be published |
| C uses the recurrence at a boundary where \(x_{i+w}\) is out of range | The exact index-side condition is missing | Original contract remains open; changing to a padded sequence requires a new definition and proof |
| An agent proves only the case \(w=0\) but describes all moving windows | The formal claim is weaker than the intended application | Formal child may be valid; fidelity/application contract fails |
| B uses an undeclared axiom that makes every group trivial | The theorem's assumptions differ from C's intended interface | Transitive assumption policy blocks reuse unless the extra assumption is explicitly admitted |
| A's archive disappears and C lacks an alternative complete native closure | An address remains, but required evidence is unavailable | Availability becomes unknown/unavailable; strict reliance cannot claim a currently available tree |
| A's exact checker is found to accept a malformed proof | A locally admitted checker incident affects an active validation basis | Current affected reliance fails closed and is repaired or rechecked through another allowed basis |

For the noncommutative case, choose permutations \(a=(12)\), \(b=(23)\), with \(p_i=a\) and \(p_j=ab\). Then \(p_i^{-1}p_j=b\), whereas \(p_jp_i^{-1}=aba^{-1}\neq b\). A checker or certified finite-group computation can verify this exact counterexample under the selected multiplication convention.

## Logical validity, local reliance, and global circulation are different

An immutable native proof does not become a different proof because a provider disconnects or a receiver changes policy. The proposition “this derivation checks under exact checker K and environment E” refers to fixed objects and a specified checking relation. Whether K is currently allowed, its execution is trustworthy, its closure is available, and the result matches the current local query are additional questions.

CP-001B's status therefore remains multidimensional:

\[
\operatorname{Status}_i
=(\text{raw evidence},\text{strict reliance},\text{validation},
\text{availability},\text{observed coverage/freshness}).
\]

A checksum proves neither theorem validity nor current availability. A download count proves neither. A local retraction may change reliance without deleting exact objects from another node. Discovering a bug in a particular proof does not refute the theorem if a clean alternative proof exists. Conversely, keeping an old `ACCEPT` marker does not preserve present reliance after the receiver admits a relevant defect.

### Long-running work across corrections

An agent may work from a fixed captured snapshot. The work remains a candidate while running. If a relevant defect, policy change, or closure loss is admitted, final export under the current contract must re-evaluate the selected dependency tree at the current reliance epoch. Work may be recoverable by replacing the defective dependency or by independently reconstructing a valid proof. The system must not automatically discard all mathematical ideas learned from a defective source, nor certify a final output merely because an earlier snapshot once looked acceptable.

### No instantaneous global correction claim

If B is disconnected when A's checker defect is discovered, B may not yet know it. No protocol can make that missing message present. The attainable safety property is immediate local invalidation after local admission, plus conditional eventual propagation and re-evaluation under the network, retention, fairness, and bounded-work assumptions already specified in CP-001B. Status exposes the observation scope and uncertainty instead of claiming that every participant has the same belief.

## What counts as meaningful accumulation

The following predicates should not be conflated:

\[
\operatorname{Generated}(c),\quad
\operatorname{Checked}(c,q,i),\quad
\operatorname{Published}(c),\quad
\operatorname{Retained}(c,\Phi),\quad
\operatorname{Reused}(c,q',j),\quad
\operatorname{Helpful}(c,q',j).
\]

For example, the theorem \(n=n\) can be produced for arbitrarily many numeral encodings. This increases bytes, checks, and theorem counts without increasing the system's useful ability to solve later tasks. A renamed existing theorem may improve discoverability, but then the contribution claim should concern discoverability rather than new logical content.

### Definition: verified reuse event

A verified support-reuse event records a receiver, exact downstream question, selected imported package, checked instantiation/transport, current acceptance contract, and an accepted downstream evidence tree containing that imported result. This is evidence that the contribution participated in accepted work. It does not prove that the contribution was necessary or made the work faster.

For search or learning reuse, a trace can record exposure and later checked output, but causal benefit requires an intervention or another justified causal design. Model claims such as “I used this theorem” are not enough.

### Local utility without a universal utility function

Different communities may value finite-group classification, constructive analysis, educational explanations, or algorithmic proof certificates differently. The protocol need not rank these on one global scale. Each receiver chooses questions and budgets. A finite external evaluation can compare task yield, resources, reliability, latency, and downstream reuse under frozen contracts, as CP-001A already specifies.

A useful contribution may reduce proof search, reduce checking or translation overhead, enable a previously unsupported interface, expose a false conjecture early, or make a difficult proof discoverable. These benefits require different measurements. There is no general implication from an observed support-reuse edge to positive net benefit.

### Exponential growth is a hypothesis, not an acceptance rule

The architecture can make compounding possible: useful abstractions and methods lower the cost of later work; later work yields more useful abstractions. It cannot promise exponential useful growth from protocol correctness alone. Mathematical difficulty, limited resources, redundant results, library fragmentation, fixed checker cost, and exhausted easy tasks can all limit growth.

A meaningful growth claim needs a fixed horizon, a declared task distribution or externally assessed task sequence, controlled resources, and a nontrivial notion of new capability. The metric cannot be the number of emitted theorem strings. A future experiment should report several generations of verified downstream reuse and net useful-work gains after all retrieval, validation, storage, and learning costs are charged.

## Conditions for eventual reciprocal use

### Proposition: conditional completion of a reuse hop

Fix a candidate package \(c\), receiver \(i\), and import contract \(q\). Assume:

- \(c\) stays retained and advertised on an exact or mechanically enumerable structural/interest route matching i's declared subscription;
- at least one correct discovery route and the required integrity-valid closure providers are eventually responsive and non-omitting;
- the receiver actually selects c, authorizes its bounded work, and gives it positive service under the declared load/fairness envelope;
- all required closure transfers and checker/transport computations terminate within the authorized bounds;
- q accepts the resulting evidence and is not defeated by a relevant policy/incident change before integration.

Then i eventually integrates c as reusable under q. This follows by composing eventual discovery, finite authorized fetching, terminating validation, and the local integration transition. It makes no claim about an unselected artifact, a semantically relevant but unindexed formulation, unavailable closure, an undecidable missing bridge, or an incompatible receiver policy.

For a finite chain of reuse hops, apply this result to each hop and additionally assume that each intervening agent eventually produces and publishes the next admissible package. That last assumption is mathematical research success; networking cannot supply it. An infinite-chain or exponential-growth theorem does not follow from these finite conditional claims.

## Concrete specification questions still to resolve

- Which exact native representation provides stable declaration identities while allowing practical library upgrades? The answer must describe canonicalization and version changes without assuming universal theorem equivalence.
- Which smallest interface language captures reusable monoid/group, order/topology, measure, and algorithmic contracts without becoming a second unverified theorem prover?
- How are checked dependency and axiom footprints extracted for the first native checker? Which optimizations preserve a conservative footprint and which introduce a larger trusted boundary?
- Which partial-proof representation makes residual obligations and dependent witness choices explicit enough for independent continuation?
- Which certified adapters cover common representation mismatches and library versions? Which translations remain heuristic only?
- How is formal adequacy for an intended application assessed and retained separately from proof validity? Which parts admit mechanical examples or counterexamples, and which require explicitly scoped review?
- What packaging granularity minimizes downstream cost: individual declarations, interfaces, theorem bundles, or demand-selected closure packs? This requires measurement rather than a universal answer.
- Which failure capsules and method packages reliably improve later work rather than biasing agents away from fruitful searches?
- How are rare valuable packages retained when immediate demand is low? Receiver-controlled exploration and archival commitments need explicit finite budgets.
- Which prospective tasks can demonstrate three or more independent generations of useful reuse while separating mathematical benefit from solver strength and publication volume?

## Suggested concept-stage acceptance criteria

Before implementation, the consolidated specification should contain an explicit example and counterexample for every claimed import rule; a complete treatment of source versus target context; a transitive assumption/checker trust boundary; a typed residual-obligation rule; a receiver-local status rule; a correction trace; and a bounded-retention/discovery assumption profile.

It should also be possible to describe a complete three-generation run without any global research root, shared truth vote, trusted publisher identity, or global synchronous update step. The run should identify exactly where mathematical checking occurs and exactly which uncertainties remain. If this cannot be stated precisely on paper, a network implementation would obscure rather than resolve the ambiguity.

## References and conceptual sources

These are conceptual reference directions and the local specifications read for this analysis, not a claim of a fresh literature review.

- [CP-001A: Autonomous research, trustworthy reuse, and optional coordination](../checkpoints/CP-001A-autonomy-first-cooperation.md).
- [CP-001B: Distributed exact memory, indexed discovery, and frontier-relative status](../checkpoints/CP-001B-distributed-corpus-and-global-status.md).
- [DTMKN Cooperation Core v0](../../spec/COOPERATION-CORE-v0.md), especially mathematical types, support semantics, correctness rules, closure boundaries, and challenge/repair.
- The LCF approach: separate untrusted proof search from a small kernel that constructs/checks theorems.
- Dependent type theory and proof assistants: typed substitution, explicit contexts, proof terms, and kernel checking as reusable composition mechanisms.
- Logical frameworks, theory interpretations, and MMT-style module structures: explicit foundations, signatures, morphisms, and scoped transport rather than name-based interoperability.
- Proof-carrying code and certificate-producing solvers: contributed computation can carry independently checkable evidence, with execution safety specified separately.
- Content-addressed builds and immutable dependency graphs: exact environment identity, reproducibility boundaries, and shared dependency storage.
- Counterexample-guided refinement and proof-producing abstraction: failures and abstractions can become constructive inputs when their scope and preservation obligations are explicit.
