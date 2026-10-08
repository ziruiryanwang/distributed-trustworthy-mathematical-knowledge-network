# DTMKN Reliable Mathematical Research and Reuse Testbed v0: technology reuse map

> Status: concept-generation input to `CP-002`, 2026-08-27. This document is a conservative design map, not a claim that the cited systems compose securely without additional work. It should be read with [COOPERATION-CORE-v0](../spec/COOPERATION-CORE-v0.md), [COOPERATION-TESTBED](COOPERATION-TESTBED.md), [TRUSTWORTHY-COOPERATION](../security/TRUSTWORTHY-COOPERATION.md), and [SNARK-ASSESSMENT](SNARK-ASSESSMENT.md).

## 1. Executive decision

The P0 system should not be a blockchain or coordination fabric with theorem objects attached. It should first be an effective local mathematical research and validation system, then a trustworthy reuse network whose stable mathematical state is reconstructed from receiver-local, context-bound checks. Active coordination is an experimental layer whose marginal benefit and overhead are measured against passive typed reuse.

The reuse boundary is:

1. **Reuse now:** Lean kernel replay, small domain-certificate checkers where available, immutable content addressing, deterministic encoding, local typed workspaces, fixed authenticated cells with object/goal/interest rendezvous, receiver-owned fair-share queues, receiver-issued capabilities, local truth maintenance, inter-cell candidate anti-entropy, same-authority crash-fault replica merge, hostile-input isolation, model checking, simulation, and adversarial testing.
2. **Build for DTMKN:** standalone mathematical work/evidence objects; bounded publication hints and subscriptions; grant/ticket/reservation/claim/meter/local-finalization/outbox demand admission; exact goal and attempt keys; formalization-fidelity contracts; conservative partial/failure semantics; signed support-tree fixed points and contract checks; atomic reliance-state/dirty-seed/epoch publication with linearized cache reads; receiver re-admission; exact root/child issuance and spend roll-up; nonreclaimable issue/action authority; crash-safe execution accounting; terminal tombstones; permission-only work capabilities with bounded control records; descendant-budget conservation; diversity-aware validation; optional coordination scopes; and the comparative testbed.
3. **Evaluate as separable mechanisms:** remote decomposition, bounded pull assignment, cross-cell soft leases, work stealing, remote portfolio orchestration, and shared programs. The same bounded local strategy portfolio remains in every comparison arm. Optional mechanisms remain only where active-minus-passive evaluation shows a classified yield, resource, or resilience benefit after full overhead.
4. **Reuse later, only after measurement:** public DHT/global ANN discovery, learned scheduling, general theory/cross-prover morphisms, general certified-exhaustion semantics, succinct verification, recursive proof aggregation, public transparency receipts, stronger replicated control-plane consensus, cross-foundation interchange, and privacy mechanisms.
5. **Reject as a P0 foundation:** voting, stake, work, popularity, authorship, remote signatures, remote validator counts, or a global chain as tests of mathematical truth.

Three boundary statements are architectural laws:

\[
\operatorname{Consensus}(m)\not\Rightarrow \operatorname{MathematicallyValid}(m),
\]

For security parameter \(\lambda\), separately bound frozen relation identifier \(\rho\), language

\[
L_{R_\rho}=\{x\mid\exists w\;R_\rho(x,w)=1\},
\]

and parameters produced under the scheme's stated setup assumptions, ordinary argument soundness promises only

\[
\Pr\!\left[
\begin{array}{l}
(pp,pk,vk,tr)\leftarrow
\operatorname{Setup}(1^\lambda,R_\rho,\textit{proofSystemID});\\
(x,\pi)\leftarrow\mathcal A(pp,pk,vk,tr):\\
\operatorname{KeyValid}(pp,vk,R_\rho,tr)=1
\land\operatorname{Verify}(pp,vk,R_\rho,x,\pi)=1\\
\land x\notin L_{R_\rho}
\end{array}
\right]
\leq\operatorname{negl}(\lambda),
\]

against the declared efficient adversary class. The receiver pins and validates the setup transcript, verifier key, exact relation/proof-system commitment, and security parameter; a well-formed key for another relation is irrelevant. This is a computational/probabilistic claim, not a deterministic implication; witness extraction additionally requires a separately stated knowledge-soundness/extractor assumption. Neither property establishes that \(R_\rho\) is the intended mathematical validation relation. Finally,

\[
\operatorname{LeanCheck}(E,\Gamma,\varphi,\pi)=\texttt{ACCEPT}
\Rightarrow \Gamma\vdash_{K,E}\varphi,
\]

not that \(\varphi\) faithfully formalizes an informal claim or is novel or useful. Every acceptance result is relative to an exact logic, axiom policy, environment closure, checker implementation, and hardware/runtime trust boundary.

## 2. Decision vocabulary and evidence discipline

### 2.1 Adoption status

| Status | Meaning in this document |
|---|---|
| **NOW** | Put the mechanism in the Reliable Mathematical Research and Reuse Testbed v0 implementation or its required verification/evaluation harness. It may first appear in a later v0 milestone, but it is part of P0. |
| **EVALUATE** | Implement as a separable testbed mechanism or ablation, but do not make the local research/reuse core or truth semantics depend on a positive result. |
| **LATER** | Preserve a clean interface and collect measurements, but do not place the mechanism on the P0 acceptance path. Adoption requires a stated trigger and a new threat/TCB analysis. |
| **REJECT-P0** | Explicitly exclude the mechanism from P0's safety or truth semantics. It may be used as a baseline, adversarial case, or a narrowly scoped later service. |

`NOW` does not mean “trust the cited implementation.” Exact versions, source hashes, configurations, conformance vectors, and resource limits must be frozen before an executable dependency enters an experiment.

### 2.2 Source classes

References are tagged as follows:

- **STD:** a published standards-track standard;
- **SPEC:** a normative or protocol specification that is not claimed to be a standards-track standard;
- **DOC:** maintainer documentation or an upstream protocol specification;
- **RP:** a primary research paper establishing a precedent under stated assumptions; non-peer-reviewed manuscripts are identified explicitly;
- **INT:** a DTMKN internal specification defining project-specific behavior.

A standard defines interoperability behavior; it does not prove a particular implementation correct. A research paper establishes feasibility or an analyzed model; it is not a production-security warranty. Maintainer documentation describes an implementation interface; it is not independent assurance.

## 3. P0 properties that the reused mechanisms must serve

Let \(A_i\) be cell \(i\)'s immutable, locally admitted fact set and let \(V_{P_i}(A_i,O_i)\) be its deterministic policy-scoped view over available objects. Let `Check` denote the exact acceptance procedure named by an obligation.

| ID | Required property | Precise boundary |
|---|---|---|
| **P-S1 Local evidence safety** | An automatically closed obligation has a finite locally checked *signed* support tree whose root polarity/judgment, exact context, axioms, validation bases, reviewer scopes, diversity requirements, and other path-dependent facts satisfy that obligation's contract. | Relative to the checker, logic, axioms, environment, and local policy; it is not metaphysical truth. Membership of a bare judgment in a cached set is insufficient. |
| **P-S2 Exact binding** | Statement, context, dependencies, environment, checker profile, policy epoch, and result are bound by typed content identifiers. | Hash collision resistance and canonical encoding are assumptions; availability is separate. |
| **P-S3 Grounded signed support** | Positive and negative conclusions are signed literals. Ordinary support/refutation is the least fixed point of locally valid finite-premise justifications over signed requirements, so mixed-polarity refutations compose and ungrounded cycles support nothing. | Inductive/coinductive mathematics must use an explicit checked rule, not ordinary cyclic graph edges. |
| **P-S4 Untrusted-input noninterference** | Raw, quarantined, malformed, over-budget, or merely remotely endorsed input cannot change stable support, protected caches, cancellation, priority, or durable anti-entropy state. | Availability under unlimited admitted load is impossible; the threat model must bound admitted resources. |
| **P-S5 Scoped correction** | A locally checked defect disables exactly the affected support paths; unaffected alternative support remains. | A challenge notice alone is advisory and cannot revoke valid support. |
| **P-S6 Demand-scoped promotion** | Checker acceptance does not itself allocate protected storage, indexing, replication, or attention. Before parsing beyond anonymous ingress, closure fetch, or checking, an authenticated audience-bound ticket reserves the candidate vector/slot and exactly one running execution claim creates a receiver meter. One immutable local-authority finalization records per-component authoritative/conservative work, soundly released resource, durable local retention/metadata, and nonauthorizing outbox intents. Every external effect uses a separate funded execution. | This controls valid-but-unwanted tautology/context floods; it does not decide mathematical usefulness globally. A public offer, claimant usage report, and outbox intent are not work authority, and promotion cannot be added after settlement. |
| **P-S7 Fidelity separation** | A valid proof closes the exact formal judgment only. If a parent goal carries semantic intent, closing it also requires its named fidelity contract and a visible mechanical or scoped reviewer basis. | Proof validity cannot show that a formalization is nonvacuous, faithful, or the problem the sponsor meant. |
| **P-C1 Idempotent cooperation** | At-least-once delivery and duplicate execution cannot duplicate durable facts or double-spend descendant budgets. | Duplicate compute during partitions is permitted and measured. |
| **P-C2 Conditional convergence** | If two cells eventually possess the same locally admitted facts, objects, policy, and policy epoch, their materialized views converge. | Cells with different policies or admission outcomes need not agree. No global instantaneous view is promised. |
| **P-C3 Bounded amplification and spend safety** | Every receive path, decomposition, fanout, lease renewal, challenge, and validation action is bounded by receiver-issued resources. Each fresh accepted mutation has an idempotent `actionID` and consumes finite receiver control-record allowance. Permission capabilities carry no mathematical-work vector; every protected action binds the unique running reservation/execution/principal/meter. Root objects require absent parent tags; child ticket/grant issuance binds exact parents, reserves full attenuated work allocation, and nonreclaimably consumes descendant issue authority. | Caveated tokens restrict scope but do not conserve work resources. Grant/ticket/reservation/claim/meter ledgers with irreversible terminal state supply issuer-local conservation; federation-wide conservation requires prepartitioned escrow or narrow consensus. |
| **P-C4 Useful progress** | Under declared honest-load, ticket, capability, and connectivity assumptions, mandatory validation and aged honest work retain service; in the five-cell primary v0, progressive routing reaches every configured cell by its declared horizon. | There is no unconditional asynchronous liveness guarantee, nor progress when the required capability is unavailable. The three-cell configuration is only a smoke test. |
| **P-C5 Conservative failure** | Failed or inconclusive attempts do not refute goals and suppress new search only through a checked exhaustion and containment relation. | This is DTMKN-specific; ordinary negative caches are insufficient. |
| **P-C6 Scalable locality** | No routine operation broadcasts to all agents or stores state proportional to global agent count. | DHT, gossip, and sketches supply probabilistic routing, not truth or guaranteed reachability under eclipse. |
| **P-C7 Deterministic fail-closed reliance** | Overrides form an acyclic explicit-supersession graph; incomparable quarantine/release resolves fail-closed. Every event that can change strict support, blocking, contract acceptance, or closure availability publishes the new state, dirty seeds, and next epoch at one linearization point or exposes a fail-closed in-progress epoch. An old cache needs an exact current-epoch tree check and a final unchanged-epoch read. | This does not make high-fanout recomputation instantaneous; affected queries return `STALE`/`UNKNOWN` until justified, raw opposite polarities coexist, and a release cannot cancel an unseen future quarantine. |
| **P-C8 Autonomous admissibility** | Standalone work, publication, validation, and reuse are valid with no coordination scope, sponsor, shared root, global budget, or common stopping rule. | Autonomous work still consumes receiver-local grants and has no guarantee of solution or external attention. |
| **P-C9 Publication-hint noninterference** | Before receiver selection and reservation, a hint changes only bounded expendable discovery state, telemetry, and advisory ranking. | Screening has bounded cost; a hint neither proves availability nor guarantees discovery. |
| **P-C10 Receiver-owned fairness** | Only a receiver can assign a finite `serviceClassID`; sender-created identities, goals, topics, namespaces, and scopes do not mint shares. | Local policy may still choose poor priorities; no global fairness notion is claimed. |
| **P-C11 Measurement noninterference** | Changing only harness-side weights, labels, groupings, or analysis leaves the protocol-state projection unchanged for equal visible inputs, faults, and random tapes. | Harness implementation and side channels remain part of the experimental TCB. |
| **P-R1 End-to-end efficacy** | The local no-network research/validation core exceeds a preregistered task-closure floor before federation claims; reuse and active coordination then have separate paired estimands. | This is an empirical gate, not a protocol theorem or universal mathematics-acceleration claim. |

For fixed local policy \(P\), let the signed-literal universe be

\[
\mathcal L=\{\textsf{SUPPORTS},\textsf{REFUTES}\}\times\mathcal J.
\]

Every locally admitted justification \(j\in J_P\) has a signed head \(\operatorname{head}(j)\in\mathcal L\) and a finite set of signed premises \(\operatorname{requiresAll}(j)\subseteq\mathcal L\). The exact evidence, closure, contexts, validation metadata, and composition procedure are locally available and accepted. Let \(\operatorname{Blocked}_{P,A}(j)\) be derived only from locally accepted defects, checker/dependency incidents, or deterministic durable reliance overrides. The raw grounded signed set is

\[
K_P=\mu X.
\{\operatorname{head}(j)\mid
j\in J_P
\land\neg\operatorname{Blocked}_{P,A}(j)
\land\operatorname{requiresAll}(j)\subseteq X\}.
\]

Project the four-state view:

\[
D_P=\{x\mid(\textsf{SUPPORTS},x)\in K_P\},
\qquad
R_P=\{x\mid(\textsf{REFUTES},x)\in K_P\}.
\]

Let \(\operatorname{opp}(\sigma,x)\) reverse polarity. The strict active-reuse set is

\[
U_P^{\mathrm{strict}}=\mu X.
\{\operatorname{head}(j)\mid
j\in J_P
\land\neg\operatorname{Blocked}_{P,A}(j)
\land\operatorname{opp}(\operatorname{head}(j))\notin K_P
\land\operatorname{requiresAll}(j)\subseteq X\}.
\]

This permits a refutation justification to depend on supported facts and refuted subclaims, while excluding an exactly disputed literal and every path through it from strict reuse.

Stable reliance is query-relative and path-sensitive rather than bare-set membership:

\[
\operatorname{Stable}_P(q;A,O)\iff
\exists T:
\operatorname{root}(T)=\operatorname{requiredSignedJudgment}(q)
\land\operatorname{FiniteActiveTree}_P(T)
\land\operatorname{CheckContract}_P(\operatorname{Contract}(q),T)=\texttt{ACCEPT}
\land\operatorname{ExactContextMatch}(q,T)
\land\operatorname{ClosureAvailable}(T,O).
\]

Thus a direct counterexample may satisfy a `REFUTES` query, and an artifact admitted under a permissive axiom/attestation/reviewer policy cannot leak into a stricter query merely because the judgment text matches. A work item compiles to a query when applicable, but standalone reuse requires no producer work item. No scheduler score, signature count, identity count, foreign admission, or consensus decision is an input to these operators.

## 4. Formal mathematics and certificate checking

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Lean 4 kernel replay | **NOW** | Primary evidence contract for the real workload. Replay a proof against an exact imported environment; report dependencies and axioms; return `ACCEPT`, `REJECT`, `ERROR`, or `UNKNOWN`. | Informal-to-formal fidelity, novelty, usefulness, absence of bugs in the kernel/runtime, or correctness under a different environment. Elaboration/build success is distinct from final kernel acceptance. | A pinned Lean 4 toolchain and Mathlib snapshot, invoked offline through a narrow adapter; retain the proof term/source closure needed for replay. | F1 **DOC**, F2 **RP** |
| Small-kernel/LCF design principle | **NOW** as an architectural constraint | Keep the stable acceptance boundary much smaller than the fallible search, elaboration, retrieval, and agent stack. Generated agents may propose arbitrary artifacts; only the named checker can admit mechanical support. | That the kernel is bug-free or that every imported axiom is acceptable. “Small” is not a proof. | Treat the Lean kernel plus explicit axiom/environment policy as the trusted logical core; prohibit unchecked “success” paths. | F2 **RP**; F1 **DOC** |
| Exact build and environment closure | **NOW** | Bind source, elaborator, macros/plugins, packages, compiler/runtime inputs, options, and imported declarations separately from the logical proof term. Replay without network or mutable lookup. | Byte-for-byte reproducibility merely from a container digest; absence of compromised compiler/toolchain components; mathematical soundness. | Content-addressed manifests, pinned Lean/Lake inputs, an offline object store, and clean-build replay. OCI images may package the closure but are not themselves evidence. | F1 **DOC**, S3 **SPEC**, S4 **SPEC** |
| Axiom and unsafe-feature reporting | **NOW** | Make conditionality explicit. Local policy rejects undeclared axioms, unresolved imports, `sorry`-like placeholders, unsafe escape hatches, or checker profiles outside the obligation contract. | Consistency of the accepted axiom set or fidelity of the statement to intended mathematics. | Extract the exact declaration dependency/axiom closure and attach it to the validation result; seed prohibited-axiom tests. | F1 **DOC**, INT1 **INT** |
| Domain certificates such as LRAT | **NOW where the workload uses the domain** | Let expensive SAT/computation producers emit a certificate checked by a small local verifier. Admit only the checker result and exact problem/certificate binding. | Correct encoding of the mathematical problem into SAT; completeness when no certificate is returned; arbitrary SMT theories. | Begin with LRAT for propositional unsatisfiability if a SAT subworkload is selected; pin a checker and cross-test mutation vectors. Add other formats only with a separate contract. | F3 **RP**, F4 **RP** |
| Counterexample/model validation | **NOW** | A generator proposes a witness; a separate, bounded local procedure checks \(M\models T\), \(M\models\Gamma\), and \(M\not\models\varphi\) for the exact scope. | Global refutation when the checked witness semantics is partial or the formalization/translation is wrong. A solver's textual `sat` response is not evidence. | For finite/decidable examples, export a compact witness and implement a direct evaluator or Lean-checked decision procedure. Treat solver discovery as heuristic. | F5 **RP**, INT1 **INT** |
| Formalization-fidelity contract | **NOW** | Split an informal/semantic-intent goal from its exact formal child. A formal proof may close only the child; the parent also needs an accepted `FidelityJustification` under the parent-owned rubric, scope, inputs, and authority. | Kernel checking cannot establish that definitions match the intent owner's concepts, that assumptions are nonvacuous, or that the formal theorem answers the informal question. Reviewer agreement is not mechanical proof. | Seed wrong, vacuous, and assumption-strengthened formalizations. Use mechanical equivalence/tests where possible; otherwise name an exact scoped operational reviewer authority and retain grade `REVIEWED`. | INT1 **INT**, INT4 **INT** |
| Independent checker or second foundation | **LATER** | Detect implementation/common-mode faults and test explicit theory transport after the Lean-first core is stable. | Absolute correctness or independence merely because executable names differ; both may share libraries, formalization errors, compilers, or hardware. | A second independently implemented certificate checker first; a second proof assistant only in the plural-foundations phase, with checked morphisms. | F6 **RP**, K1 **RP** |
| Native proof artifacts plus optional succinct wrapper | **NOW for native artifact; LATER for wrapper** | Preserve inspectable, reusable proof/certificate material even if a later succinct argument amortizes repeated checking. | A succinct wrapper does not improve the underlying theorem, checker, environment, or formalization. | `Derivation` stores native artifact/dependencies/checker profile; `SuccinctArgument` is a separate optional object. | C4 **RP**, C5 **RP**, INT2 **INT** |

### 4.1 Formal-math boundary

The P0 acceptance statement is deliberately conditional:

> The exact artifact was accepted by checker profile \(K\), in environment \(E\), under axiom policy \(P\), for judgment \(\Gamma\vdash\varphi\).

It is not shortened to “\(\varphi\) is true.” Semantic fidelity remains a typed review/formalization obligation. Multiple agents agreeing on the same mistranslation do not discharge it.

### 4.2 Validation-result taxonomy

Every adapter uses one fail-closed taxonomy:

- `UNCHECKED`: no validation attempt has begun; it is not a terminal validation result.
- `ACCEPT`: the declared procedure terminated and established its exact acceptance relation.
- `REJECT`: the declared procedure terminated with a definitive malformedness, contract-invalidity, or certificate/proof-invalidity verdict.
- `UNKNOWN(reason)`: the declared relation could not be decided under the declared procedure/bounds—for example missing closure, unavailable payload, documented incompleteness, timeout, fuel exhaustion, or a declared memory/resource limit.
- `ERROR(reason)`: there is no trustworthy execution result because of an unexpected checker crash, internal invariant failure, sandbox failure, corrupt runtime, or TCB-integrity alarm.

Neither `UNKNOWN` nor `ERROR` supplies support, refutation, or negative-cache suppression. Both settle receiver-authoritative parsing, closure-fetch, and validation work plus conservative bounds for measurement gaps and require a new immutable assessment for retry. `STALE` is health/cache status, not a validation verdict; an old reliance-epoch cache supplies no acceptance and may surface `UNKNOWN(STALE_RELIANCE_EPOCH)`.

## 5. Knowledge representation and integration

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Typed immutable object graph | **NOW** | Represent theories, contexts, judgments, obligations, attempts, evidence, relations, justifications, challenges, and failure capsules as separately typed immutable objects. Hash canonical bytes, not language runtime objects. | Semantic equality, persistence, availability, or validity merely because an object has a CID. | A versioned deterministic-CBOR profile with explicit tags, length limits, Unicode rules, and golden vectors; SHA-256 CIDs initially. | S1 **STD**, S2 **STD**, INT1 **INT** |
| Separate formal-query and semantic-obligation identity | **NOW, DTMKN-specific** | Deduplicate exact formal searches without confusing them with parent satisfaction. A semantic obligation identity binds kind, formal goal, `semanticIntentRef`, inputs/context, evidence contract, fidelity contract, acceptance procedure, and acceptable outputs. | That two obligations with identical formula text have the same intent, reviewer scope, axiom policy, or closure rule. | Use a narrow `FormalQueryKey` for search reuse and a distinct full `GoalTemplate/Obligation` CID for closure. Never key parent satisfaction by formula/context alone. | INT1 **INT**, INT4 **INT** |
| OMDoc/MMT-style theory modules and morphisms | **LATER for general interoperability; NOW only as a schema precedent** | Inform the separation of theories, contexts, imports, interfaces, symbol maps, and explicit transport obligations. | That two surface-similar concepts are equivalent, that a declared morphism is sound, or that one universal ontology can erase foundational differences. | Minimum slice stores only the Lean-first theory/context fields it actually checks. General MMT exchange and cross-prover morphisms wait for a concrete second consumer. | K1 **RP**, K2 **RP/SPEC** |
| Checked theory transport | **NOW only for manually supplied in-environment relations; LATER for general morphisms** | In v0, reuse a supplied relation only when the target-side Lean derivation or a small approved transporter output is locally replayed with exact endpoints, dependency subtheory, side conditions, checker profile, and axiom policy. | Equality of theories, conservativity beyond the checked subtheory, automatic discovery of correct maps, or cross-prover validity. | Hand-author a small interface relation set in the corpus and replay every target-side result. Defer general morphism synthesis/interchange. | K1 **RP**, INT1 **INT** |
| Datalog/seminaive signed fixed-point evaluation | **NOW** | Materialize the grounded signed set \(K_P\), project raw derivability \(D_P\) and refutability \(R_P\), and compute strict active literals \(U_P^{\mathrm{strict}}\). Retain predecessor justifications so closure can present a finite support tree to the obligation contract. | Correctness of facts/rules, safe unstratified negation, or permission to close from bare judgment membership. Computing positive reachability alone cannot express mixed-polarity refutation or path-dependent contracts. | A small audited evaluator over signed heads/premises: compute \(K_P\), derive \(D_P/R_P\), then \(U_P^{\mathrm{strict}}\) against opposites in \(K_P\). Cross-check sets and witness trees against a slow reference. | K3 **RP**, INT1 **INT** |
| Assumption-based truth maintenance (ATMS) | **NOW as a design precedent** | Retain alternative signed justifications, their exact assumption/context/validation bases, and reconstructible finite support trees. On a checked defect, block affected paths while preserving unaffected alternatives. | Logical soundness of a justification, globally consistent beliefs, or cheap worst-case recomputation on dense graphs. | Store signed justification hyperedges plus reverse indices and path metadata; derive four-valued projections and strict reusable witnesses per policy. Do not use a single mutable status field. | K4 **RP**, INT1 **INT** |
| Deterministic reliance overrides, epochs, and dirty roots | **NOW, DTMKN-specific** | An authorized override names its ID, subject/scope, action, policy epoch, authorization decision, and exact predecessors. Every support-relevant event publishes changed state, conservative dirty roots, and the next epoch at one linearization point; an unavailable atomic tuple uses a fail-closed in-progress epoch. This includes ordinary opposite-polarity justifications. Old caches fail closed and reverse impact proceeds in bounded batches. | Immediate complete recomputation, correctness of submitter impact lists, cancellation of unseen future quarantines, or removal of unaffected OR alternatives. Dirty-root disjointness alone is not a freshness proof. | Require an acyclic supersession graph and exact current-epoch tree recheck with final unchanged-epoch read before `ACCEPT`. Crash-test every state/dirty/epoch publication boundary; a missing predecessor stays quarantined and incomparable release/blocking resolves fail-closed. | INT1 **INT**, INT4 **INT** |
| Equality saturation/e-graphs | **LATER for optimization; NOW only as candidate generation if needed** | Discover rewrite chains, normal-form candidates, and repeated algebraic structure that may yield relation or abstraction obligations. | Semantic equivalence in DTMKN unless every rewrite and side condition belongs to a locally checked contract. Resource use can explode. | A bounded `egg`-style engine behind a discovery-only interface; export a proof/rewrite trace for checking rather than an “equivalent” flag. | K5 **RP** |
| Symbolic/structural indices | **NOW** | Retrieve exact keys, declarations, dependency shapes, type heads, and normal forms before expensive semantic search. | Logical relation or substitutability. Index omissions affect discovery, not validity. | Per-cell inverted indices over locally admitted objects; all hits resolve to typed immutable objects before use. | INT1 **INT** |
| Vector/embedding retrieval | **LATER for the minimum slice; optional discovery-only ablation** | Eventually route candidate premises, analogous goals, and possible cross-theory matches after exact/structural retrieval has a measured ceiling. | Implication, equivalence, theorem identity, independence, or safe merge. Similarity cannot close obligations. Global ANN also enlarges poisoning/eclipsing and evaluation scope. | No global ANN in the minimum vertical slice. Later evaluate a replaceable local FAISS/HNSW index with typed candidate edges and hard negatives. | K6 **RP**, K7 **RP** |
| Compact probabilistic summaries | **NOW for routing hints only** | Exchange bounded cell summaries to reduce global discovery traffic and locate likely objects/capabilities. | Sound absence, exact membership under stale epochs, admission, or permission to suppress work. | Bloom filters or sketches scoped by cell and epoch; false-positive/staleness behavior measured; exact CID lookup follows every useful hit. | K8 **RP** |
| W3C PROV-style activity interchange | **LATER** | Export operational lineage useful for debugging, failure-domain analysis, and reproducibility after the P0 mathematical/attempt schemas stabilize. | Truth, originality, human identity, priority, credit, or independence merely from signed provenance statements. | Map minimal execution/dependency fields to PROV-O without making social attribution part of support. | K9 **STD** |

The crucial separation is between a **candidate relation** and a **certified relation**. Retrieval systems may produce `SAME_SCHEMA`, `ANALOGOUS`, or a proposed `IMPLIES`; only an evidence contract may promote the corresponding logical edge. This prevents a high-recall search system from becoming an unsound theorem-merging system.

## 6. Distributed-systems mechanisms

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Fixed authenticated cell federation | **NOW** | Support the Core's 3–5 configured-cell range with stable rotating service principals, authenticated channels, explicit policy/cohort identifiers, and bounded gateways. The primary artifact instantiates exactly five independent cells; three cells are only a smoke test. Cells, not individual workers, are the P0 federation/failure-domain unit. | Permissionless membership, public discoverability, human identity, mathematical authority, Byzantine agreement, or a shared research purpose. A cell key cannot bypass receiver admission. | A frozen testbed cell roster; TLS proof of possession; per-cell quotas; explicit add/remove epoch; 8–16 workers initially behind the cells. | S5 **STD**, Q2 **RP**, INT1 **INT** |
| Grow-only/set-union CRDT semantics over admitted facts | **NOW, only inside one logical cell's replica cohort** | Make durable fact merge associative, commutative, and idempotent among non-Byzantine replicas governed by one admission authority, one nonsplit-brain issuer ledger (or disjoint writable-partition escrow), and an explicit crash-fault model. Every independently operated cell re-admits candidate CIDs/closures. | Semantic conflict resolution, Byzantine-replica safety, split-brain spend safety, global agreement, deletion, bounded storage, or validity of received facts. Authentication and matching policy identifiers do not make a peer safe. | Minimum v0 uses one authoritative writer/ledger per logical cell; optional replicas consume authority-admitted facts. Multiwriter crash-fault replication needs Raft or disjoint escrow; BFT replication is later. Inter-cell input always enters candidate queues. | D1 **RP**, B3 **RP**, INT1 **INT** |
| Epidemic anti-entropy | **NOW with two distinct profiles** | Within one logical cell's crash-fault replica cohort, reconcile admitted inventories. Between independently operated cells—five in the primary run and three in the smoke test—reconcile only candidate inventories and pull closures for receiver-local re-admission. | Timely delivery, foreign admission, Byzantine safety merely from signatures/equal policy roots, or bounded bandwidth without summaries/quotas. | Separate message types and stores for `ReplicaAdmittedDelta` and `InterCellCandidateDelta`; reject the former unless sender belongs to the local authority's exact replica cohort. | D2 **RP**, C2 **RP**, INT1 **INT** |
| Content-addressed storage and OCI/ORAS transport | **NOW locally; LATER for broad federation** | Deduplicate immutable objects, bind manifests, move archival bundles between cells, and separate object identity from location. | Persistence, discoverability, authenticity, safety of unpacking, or reproducibility. A digest says only which bytes were named. | Simple local CAS for P0; OCI Distribution/ORAS-compatible export after schemas stabilize. Never execute directly from an unvalidated archive. | S4 **SPEC**, S2 **STD** |
| Kademlia-style public DHT lookup | **LATER; optional scale simulation only** | Potentially find providers/cells for exact CIDs without \(O(N)\) routing state after a public membership and eclipse threat model exists. | Truth, provider honesty, data availability, privacy, admission, or eclipse resistance under arbitrary Sybils. | No public DHT in the minimum vertical slice. A later experiment may simulate Kademlia, then evaluate a pinned libp2p profile with multi-provider queries and bounded influence. | D3 **RP**, D4 **DOC** |
| Scoped gossip publish/subscribe | **NOW only among configured cells; LATER publicly** | Distribute expiring task/capability summaries and bounded publication hints among the configured authenticated cells: five primary, three only in the smoke test. | Reliable delivery, ordering, truth of advertisements, permission for a message to mutate stable state, or universal discovery. | Size-limited exact/structural/interest topics over authenticated peers; a hint relay requires a matching authenticated subscription/home shard, decreasing TTL, deduplication, and fixed routing quota. Exact objects are pulled only after receiver reservation plus its unique metered execution claim and are locally admitted. A Gossipsub implementation is optional, not a safety assumption. | D5 **DOC**, D2 **RP** |
| Bounded `PublicationHint` and interest subscriptions | **NOW, DTMKN-specific** | Let independent publishers advertise typed object availability and let receivers declare overlapping discovery interests without sharing a program. Before selection, a hint affects only expendable hint state, telemetry, advisory ranking, and quota-charged nonamplifying relay of the same bounded frame. | A validation request, unbounded forwarding mandate, payload relay, storage entitlement, durable index entry, task, evidence, or provider availability. | Strict frame/key/provider/TTL/rate limits; aggregate anonymous quota; separate hint cache; receiver/home-side canonical transformation from admitted `discoveryKeys[]` to domain-separated routing keys; lazy fetch after receiver demand; \(10^5\)-hint rotation test. | INT1 **INT**, INT4 **INT** |
| Rendezvous-hashed object/goal/interest homes | **NOW** | Map a domain-separated exact object, goal, environment, or receiver-approved interest key to a primary and bounded backups in the frozen roster, providing a routing/deduplication rendezvous without a global scheduler. After timeout, progressive exploration reaches every configured cell by the v0 horizon. | Exclusive ownership, mathematical authority, global consensus, admission authority, or availability after all cells fail. Adversarial hot keys and key grinding still require quotas/override. | Highest-random-weight hashing over `(membershipEpoch, keyKind, routingKey, cellID)`; bounded keys per hint; explicit replica count; per-home quota/hot-key override; bounded steps but all-roster final horizon. | D10 **RP**, D6 **RP**, INT2 **INT** |
| Soft leases | **EVALUATE** | Potentially suppress accidental duplicate attempts; cross-cell leases are enabled only in the active-coordination treatment. Expiration is judged by receiver-local elapsed time, and checkpoints—not heartbeats alone—extend suppression up to a fixed maximum. | Ownership, exclusion, completion, validity, positive net value, or safety from synchronized clocks. A report remains admissible after lease expiry. | Separable lease table keyed by exact `AttemptKey`; monotonic local timers; `L_max`; validated progress checkpoint for renewal; compare against the same local solver without cross-cell leases. | D7 **RP**, INT1 **INT** |
| At-least-once messaging plus idempotent handlers | **NOW** | Tolerate lost acknowledgments, retries, duplicate reports, and partitioned execution. Exact object/attempt keys make replay harmless to durable state. | Exactly-once physical delivery or absence of all duplicate producer cost. Receiver-paid execution is single-claimed and metered separately. | Message IDs, attempt keys, durable authorization and finite capability control-record debits, issuance, reservation/claim/meter/local-finalization/outbox records, and deterministic handlers. Avoid making broker-specific exactly-once claims. | INT1 **INT** |
| Dynamic membership via failure detectors | **LATER; churn is simulated without changing the P0 roster semantics** | Eventually route around a larger dynamic set of crashed/unresponsive cells. Treat suspicion as an availability hint. | Mathematical invalidity, maliciousness, perfect failure detection, or authority to change membership in an asynchronous network. | Minimum slice uses an explicit roster/epoch and simulates cell availability. Evaluate SWIM-like weak membership only with a separate membership-authority design. | D8 **RP**, D9 **RP** |
| Global strongly consistent metadata service | **REJECT-P0** | No P0 role: autonomous work, publication hints, optional program facts, and evidence do not require one global serialization point. | Global low-latency availability during partitions; Byzantine truth; decentralization. | Use it only as a centralized comparison baseline. Local cells may use a transactional store internally without exporting its semantics globally. | D9 **RP**, B2 **RP**, B3 **RP** |

The convergence claim is conditional. Replicas of one logical cell converge by set union only under their stated crash-fault admission-authority model. Independently operated cells always re-admit imported candidates; matching authentication or policy roots does not authorize direct union. If cells have different checker availability or admission outcomes, disagreement is expected and explicit. The system seeks portable evidence and eventual candidate reconciliation, not one mandatory global belief state.

## 7. Multi-agent cooperation and scheduling

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Blackboard architecture | **NOW** | Let heterogeneous proposers, formalizers, critics, solvers, checkers, and integrators communicate through typed partial artifacts and obligations rather than private bilateral state. | Global optimality, correctness of posted items, scalable federation by itself, or a single omniscient controller. | Sharded typed blackboards with a protected admitted layer, quarantine, ready frontier, conflict inbox, and failure atlas. | A1 **RP**, INT1 **INT** |
| Contract-Net-style offers and pull assignment | **EVALUATE** | Agents advertise hard capabilities; cells may expose eligible work items; bounded offers report predicted utility/cost; local policy grants a lease/capability. | Truthful bids, calibrated predictions, identity, fairness, mathematical correctness, or net benefit over passive reuse. | Receiver-filtered pull queues and `ResourceOffer` messages; probe new endpoints, treat self-reports as advisory, and compare active versus passive profiles. | A2 **RP**, INT1 **INT** |
| Locality-aware work stealing | **EVALUATE** | Potentially recover idle capacity without a global scheduler. Steal from adjacent subject/environment/resource cells after local ready work, respecting data-transfer and environment costs. | The classic work-stealing bounds for arbitrary heterogeneous, failure-prone, non-strict distributed workflows or positive net value. | Bounded randomized victim selection, work descriptors rather than mutable ownership, and exact input snapshots. Compare against passive/no-steal and centralized baselines. | A3 **RP** |
| Bounded top-\(k\) routing / sampled scheduling | **NOW with fixed rules** | Avoid broad initial fanout: apply declared hard predicates, rendezvous-route to a small cell set, and expand after timeout/diversity demand. In the primary five-cell v0, the declared final horizon is all five cells within five routing epochs. | Globally optimal assignment, honest queue reports, or discovery of an actually unavailable capability. | Deterministic hard filters and bounded progressive steps across the roster. Learned rankers are excluded from the minimum slice. | A4 **RP**, INT2 **INT** |
| Online exploration via bandit/learned scheduling | **LATER; fixed exploration lane NOW** | Eventually learn task-conditioned route/strategy choices after the vertical slice produces trustworthy outcome/cost traces. Minimum v0 only reserves a fixed bounded exploration share. | Stationary rewards, causal independence, truthful self-reports, mathematical validity, or a safe admission rule. Learned scores can amplify poisoned feedback. | Record raw receiver-observed features/outcomes now; evaluate UCB/contextual methods as a later ablation with frozen training/evaluation splits. | A5 **RP** |
| Receiver-owned service and validation reserve | **NOW, P0 contract** | Bound admitted service classes, protect mandatory validation capacity, and require declared service floors under the load envelope. | One uniquely correct scheduler, unconditional liveness, or equal scientific value across tasks. | Finite issuer-qualified classes, admission bounds, an aggregate onboarding lane, and a protected validation reserve. | A8 **RP**, INT2 **INT** |
| WFQ/DRR, priority aging, pull details | **EVALUATE under the P0 contract** | Compare concrete queue algorithms for rare capabilities, tail latency, and overload recovery without changing the finite-class and validation-reserve safety contract. | Net benefit, universal fairness, or safety merely from an algorithm name. | WFQ versus deficit round robin with frozen service floors and capped aging; scope-Sybil and adversarial traces. | A8 **RP**, INT2 **INT** |
| Grant-backed claimed and metered demand admission | **NOW, DTMKN-specific** | Allocate every local or imported paid path through a receiver grant; distinguish exact root/child forms; allocate full child work plus nonreclaimable subtree issue authority; advertise nonspendable offers; atomically reserve a candidate vector/slot; admit one bounded `RUNNING` execution with a receiver meter; locally finalize per-component authoritative/conservative spend, durable local retention, and optional outbox intents; fund external effects separately. | Mathematical truth, global usefulness, novelty, or permanent external replication entitlement. A public offer, claimant report, or outbox intent is not work authority, and a valid tautology outside demand remains cold/bounded. | `BudgetGrant`, `DemandOffer`, `DemandTicket`, `DemandReservation`, `DemandExecutionClaim`, and `DemandSettlement`; root/child tag and roll-up rules; nonreclaimable count/fanout allowances; crash-safe receiver time; `ACTIVE \| TERMINAL` tombstones; `RESERVED -> RUNNING -> FINALIZED`; local settlement plus transactional outbox; existing-action lookup before liveness/freshness/debit checks. | INT1 **INT**, INT4 **INT** |
| Tail hedging / bounded strategy portfolios | **EVALUATE** | Replicate selected high-value or heavy-tailed attempts across meaningfully different methods/failure domains after a delay; accept any locally valid result. | Independent replicas merely from different endpoint labels; free speedups; validity without checking; net benefit over passive reuse. Hedging can worsen overload. | Quantile-triggered hedges with a receiver-local replica grant, cancellation hints, and diversity descriptors checked against observed lineage. | A6 **RP**, INT2 **INT** |
| Token buckets, bounded queues, backpressure, circuit breakers | **NOW** | Protect validation and admitted-state capacity; shed or defer generation/candidate traffic before mandatory checks; cap fanout, bytes, graph degree, child objects, and work. | Fairness or availability by themselves; safety if privileged traffic bypasses accounting; a defense against unlimited resources with valid credentials. | Hierarchical per-cell/per-grant/per-ticket vectors, nonreclaimable grant/ticket/capability fanout, unique execution meters, token-bucket ingress, queue caps, overload hysteresis, and separate validation reserve. | A7 **SPEC**, INT1 **INT** |
| Exact action cache | **NOW** | Reuse only an output whose full `AttemptKey` binds method, executable, parameters, input snapshot, environment, resource ceiling, nondeterminism policy, tool/model version, and seed. | Semantic equivalence of different attempts, validity of a remote cache entry, or safe reuse after a material field changes. | CAS-indexed result records; local evidence contract revalidation on cache import; single-flight only within a controlled executor domain. | INT1 **INT** |
| Partial results and residual obligations | **NOW, DTMKN-specific** | Preserve useful lemmas, counterexamples, narrowed regions, checkpoints, and explicit residual goals so failed end-to-end attempts can unlock other work. | Completion of the parent, correctness of self-reported discharged obligations, or safe restoration of executable checkpoints. | Typed `WorkReport`, separate validation for each discharged obligation, safe checkpoint formats, and parent composition checks. | INT1 **INT** |
| Structured failure capsules | **NOW for hints/reproduced exact runs; LATER for general certified exhaustion** | Preserve exact negative-work context and useful intermediates. In the minimum slice, failures may affect bounded ranking but do not suppress a search unless a workload-specific finite-region containment checker is explicitly supplied. | Refutation of the mathematical goal, completeness outside the exact method/context/resource region, or safe negative caching after changed code/seed/policy. | `HINT` and `REPRODUCED_RUN` now; one narrow finite-domain `CERTIFIED_EXHAUSTION` case only if the corpus supplies a checker. Defer general `ATTEMPT_SUBSUMES`. | INT1 **INT**, INT2 **INT** |
| Private chain-of-thought collection | **REJECT-P0** | No protocol role. Persist public typed artifacts, inputs, outputs, uncertainty, and checkable evidence instead. | Scientific reproducibility, truth, or useful provenance merely from hidden reasoning transcripts; collection also creates privacy/security risk. | Agent adapters expose structured reports and optional concise public rationales, never a requirement for private hidden reasoning. | INT1 **INT** |

The scheduler optimizes expected useful checked yield; it never supplies evidence. In particular, a high estimated success probability changes *which work is tried*, not whether a submitted conclusion enters support.

## 8. Security, operational identity, and capabilities

Operational identity is P0 because the network must authenticate control actions, limit amplification, revoke access, and estimate correlated failure domains. Political attribution remains secondary. These are different questions and must not share one overloaded “identity” field.

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Authenticated encrypted sessions | **NOW** | Bind every configured cell service principal and each short-lived worker subject key to messages; prevent off-path forgery and passive disclosure; support proof of possession, replay windows, quotas, and revocation. | Human identity, authorship, mathematical correctness, independence, honest behavior, or resistance after endpoint compromise. | TLS 1.3 with pinned/configured cell keys; short-lived worker keys bound into capability requests; standard signature algorithms. Do not invent a transport cipher. | S5 **STD**, S6 **SPEC** |
| Receiver-issued attenuable capabilities | **NOW** | Authorize exact issuer, epoch, holder public key, actions, roles, execution caveats, expiry, nonreclaimable child-capability fanout, and a finite nonreclaimable control-record allowance. Every fresh accepted action proves possession and atomically consumes one record; rejected IDs create no durable per-ID state. Every protected action binds the exact unique running reservation, execution ID, principal, and receiver meter; child issuance preallocates the child's complete fanout/action-record subtree so the root bounds both capability objects and accepted replay records. | Truth, civil identity, correct self-reports, or any mathematical-work allocation merely from caveats. A capability cannot mint, reserve, claim, meter, or enlarge a ticket/reservation work balance; authorization idempotence still needs its finite action ledger. | Macaroon-like caveated tokens or a comparably small format plus holder proof of possession and an idempotent authorization/fanout/action-record ledger, bound to one issuing cell and authorization epoch. | Q1 **RP**, INT1 **INT** |
| Atomic issuer-local grant/ticket ledger | **NOW, DTMKN-specific** | For each mutation, first atomically look up its authority/action key: an existing identical digest returns the prior result even after expiry or terminalization; a mismatch is equivocation. Root issuance requires absent parent tags; child issuance binds exact parents. Finalization records local outcome, per-component spend, durable local retention, release, and optional outbox intents together. Terminal transitions roll exact child ticket/grant spend into the parent before releasing only unused allocation. | Federation-wide conservation, global fairness, cross-store atomicity, external-effect completion, or safety from a corrupted issuer. Copyable signed/MAC tokens alone cannot enforce aggregate ceilings or crash recovery. | One crash-recoverable transactional ledger per issuer; explicit `ACTIVE \| TERMINAL`, reserved, spent, finalized, released, stored-digest, outbox, and receiver-time-epoch states; sibling, nonzero child recycling, terminal resurrection, action-flood, clock-reset, split promotion, and crash-boundary tests. Cross-cell budgets use prepartitioned nonoverlapping escrow or deferred narrow consensus. | INT1 **INT**, INT4 **INT** |
| Operational validator and fidelity-reviewer roles | **NOW** | Limit who may consume reserved checker capacity, authorize quarantine, or satisfy a parent fidelity contract that explicitly names an intent-scoped reviewer authority. Preserve the principal, scope, rubric, inputs, and grade in the justification. | Mathematical correctness by role membership. A reviewer can establish only the named nonmechanical contract under local policy; it remains `REVIEWED`. A remotely signed `ACCEPT` is not local replay. | Stable rotating cell/reviewer service principals issue short-lived scoped role capabilities; maintain revocation epoch and visible validation basis. Keep author prestige out of proof-support rules. | INT1 **INT**, INT4 **INT** |
| Receiver-observed onboarding and probes | **NOW with fixed thresholds; learned calibration LATER** | Assign small onboarding caps and test claimed hard capabilities with unpredictable probes and receiver-observed results. Record raw outcome, cost, tool/environment, and error evidence for later analysis. | Unique personhood, true independence, immunity to adaptive gaming, or calibrated predictions. Probes may leak or be learned. | Fixed promotion/demotion thresholds and capped exploration in v0. Train/compare learned estimators only after frozen trace collection. | A5 **RP**, Q2 **RP**, INT2 **INT** |
| Failure-domain descriptors | **NOW, cautiously** | Avoid counting replicas that share the same model, retrieval corpus, formalization, checker build, cloud, or operator as independent validation against that failure mode. | Actual independence from self-asserted labels or statistical independence of errors. Identity diversity is not method diversity. | Combine authenticated session/cell keys, exact tool/environment hashes, receiver observations, and explicit “unknown/correlated” classifications. Require no diversity claim when lineage is unknown. | F6 **RP**, Q2 **RP** |
| Anonymous ingress | **NOW, bounded** | Permit open proposal/challenge gateways without persistent civil identity, while keeping raw traffic outside durable/protected state. Durable promotion normally requires a receiver demand ticket; unsolicited valid objects remain in a small cold/exploration lane. | Unlimited participation at zero cost, Sybil resistance, or a right to consume checking, storage, replication, or attention. | A shared anonymous quota, strict size/graph limits, session-key proof of possession, cheap schema checks, and separately reserved demand/exploration tickets. | Q2 **RP**, INT1 **INT** |
| Global reputation / one-agent-one-vote | **REJECT-P0** | No P0 truth or admission role. At most, local empirical outcome history is a routing prior. | Sybil resistance, correctness, independence, minority expertise, or robustness to collusion and popularity cascades. | Do not implement a global scalar reputation. Keep local, task-conditioned observations with uncertainty and bounded effect on scheduling. | Q2 **RP**, INT1 **INT** |
| Signatures and remote attestations | **NOW as binding/routing hints; REJECT-P0 as truth** | Authenticate which key asserted an object, allow replay suppression and optional trusted operational cache policy, and bind receipts later. | Accuracy of the assertion, identity of a human/model, originality, independence, or theorem validity. | Standard signatures over canonical typed object roots. Label validation basis `TRUSTED_ATTESTATION` when a local policy intentionally relies on a signer; otherwise replay/check locally. | S6 **SPEC**, INT2 **INT** |
| Challenges and defect evidence | **NOW, DTMKN-specific** | Accept cheap challenge notices as bounded repair hints. Change stable support only after local reproduction or checked defect/counterevidence identifies affected paths. | Revocation power by volume, identity, or signature count. A challenge flood must not cause unbounded recomputation. | Separate `ChallengeNotice` from `DefeatEvidence`; a notice may schedule only capped triage. Mark dependencies dirty only after locally admitting `DefeatEvidence`, a confirmed dependency/checker-policy incident, or an authorized reliance override; then recompute lazily and budgetedly. | INT1 **INT**, INT2 **INT** |
| Social authorship, priority, credit, ownership | **LATER** | Optional publication/governance layer after the cooperation and evidence semantics work. It may support credit, licensing, or dispute processes. | Mathematical correctness or operational authorization. | Keep optional attestations/provenance objects outside the P0 support operator. | K9 **STD**, INT2 **INT** |

### 8.1 Identity conclusion

P0 requires **key continuity long enough to enforce a capability and observe outcomes**, not a universal registry of people or models. An endpoint may be anonymous yet safe to receive from because its influence is bounded and its mathematical outputs are checked. Conversely, a famous authenticated institution may still submit a false artifact; its identity cannot bypass the evidence contract.

No purely identity-free open network can simultaneously promise unbounded free validation service and denial-of-service resistance. DTMKN therefore states progress only below declared admitted-load bounds and assigns budgets through receiver-controlled grants and capabilities, not through shared goals or the number of claimed agents.

### 8.2 Demand redemption state machine

Demand advertisement and spending authority must be separate. The minimum safe model has a receiver grant plus five demand objects. Every authority ID is issuer-qualified as `(issuerCell, issuerEpoch, localID)`:

```text
BudgetGrant {                 // receiver resource authority
  budgetGrantID, issuerCell, issuerEpoch, parentBudgetGrantID?,
  holderOrLocalPolicy,
  admittedServiceClassIDs[], admittedScopeIDs[],
  totalCeilingVector, totalRedemptionAllowance,
  ticketIssueLimit, childGrantLimit, expiry
}

DemandOffer {                 // public and non-spendable
  offerID, receiverCell,
  admissionScopeID, serviceClassID, routingKey,
  candidatePredicateRef, contractRef, artifactKinds,
  lanePolicy, coordinationScopeRef?, expiry
}

DemandTicket {                // issuer-authenticated authority
  ticketID, issuerCell, issuerEpoch, parentTicketID?,
  budgetGrantID, authorizationPrincipal,
  audience: HOLDER(subjectKey) | PUBLIC_GATEWAY(laneID),
  admissionScopeID, serviceClassID,
  candidatePredicateRef, contractRef, artifactKinds,
  totalCeilingVector, perRedemptionCeilingVector,
  maxRedemptions, childTicketFanoutLimit, expiry
}

DemandReservation {
  reservationID, ticketID, redemptionActionID, requestDigest,
  candidateCID, reservedVector, reservationExpiry
}

DemandExecutionClaim {
  reservationID, ticketID, redemptionActionID,
  executionActionID, claimDigest,
  executionPrincipal: HOLDER(subjectKey)
    | LOCAL_EXECUTOR(executorID)
    | GATEWAY_SESSION(laneID, subjectKey),
  meterRecordID, claimedAt, executionExpiry
}

DemandSettlement {
  reservationID, ticketID, redemptionActionID, requestDigest,
  candidateCID, executionActionID?, executionPrincipal?,
  finalizationDigest, terminalResultDigest?, meterRecordDigest?,
  measurementBasisByComponent:
    ResourceComponent -> NONE_UNCLAIMED
      | AUTHORITATIVE_METER | CONSERVATIVE_UPPER_BOUND,
  outcome, validationSpentVector,
  promotion: NONE | PROMOTED(admissionDecisionID),
  promotionSpentVector, totalSpentVector, releasedVector
}
```

The resource vector includes at least parsing beyond the anonymous ingress allowance, closure-fetch bytes/work, validation compute/memory/time, retained bytes, graph/index insertion, attention, and replication fanout. Vectors are finite canonical nonnegative quantities; redemption, issue, and fanout fields/counters are finite canonical nonnegative integers; overflow, underflow, and noncanonical encodings fail before mutation. Every grant and ticket has an issuer-ledger `ACTIVE | TERMINAL` state. Exact recorded actions replay before the state check; every fresh allocation/reservation action requires `ACTIVE`, and terminalization writes an irreversible tombstone. A grant ledger maintains

\[
\operatorname{finalizedSpend}[g]
+\operatorname{reservedTicketCeilings}[g]
+\operatorname{reservedChildGrantCeilings}[g]
\preceq\operatorname{totalCeiling}[g],
\]

and the analogous finalized/redemption-allocation inequality, plus

\[
\operatorname{consumedTicketIssueAllowance}[g]
\leq\operatorname{ticketIssueLimit}[g],
\quad
\operatorname{consumedGrantFanout}[g]
\leq\operatorname{childGrantLimit}[g].
\]

For a new idempotent root issuance action, the receiver requires `parentTicketID = NONE` and checks a live grant, equal issuer/epoch, grant authority, allowed issuer-qualified service class and admission scope, grant expiry/revocation, ticket expiry, vector/redemption balance, and sufficient nonreclaimable ticket-issue allowance in one transaction. A root grant similarly requires `parentBudgetGrantID = NONE`. It records the ticket's full work allocation, consumes \(1+\texttt{childTicketFanoutLimit}\) issue units, and creates the ticket `ACTIVE` before visibility. Child-grant and child-ticket transitions instead require exact parent IDs. Child-grant issuance consumes the child's full ticket-issue allowance and \(1+\) its grant-fanout allowance without later reclamation. Normative `IssueChildTicket` checks a live parent, same issuer/epoch/grant, authorized principal/audience attenuation, equal or receiver-approved scope/class attenuation, artifact-kind inclusion, mechanically checked predicate implication, equal or approved stricter contract, no later expiry, positive redemption allowance, work balance, and

\[
\operatorname{consumedTicketFanout}[p]
+1+\operatorname{childTicketFanoutLimit}(c)
\leq\operatorname{childTicketFanoutLimit}(p),
\]

then reserves the full child work allocation and consumes the fanout amount before visibility. These count/fanout consumptions never return on terminalization.

The issuer then first atomically looks up `(ticketID, redemptionActionID)`: an existing equal request digest returns the recorded reservation or settlement even after expiry/revocation, while a different digest is rejected as equivocation. Only when no record exists does issuer \(i\), before closure fetch or validation, atomically apply:

\[
\begin{aligned}
\operatorname{Reserve}_i(t,a,r,b)\Longrightarrow {}&
\operatorname{VerifyTicket}_i(t)
\land\operatorname{TicketAllocationLive}_i(t)
\land\operatorname{NotExpired}_i(t)
\land\operatorname{NotRevoked}_i(t)\\
&\land\operatorname{AudienceOK}_i(t,r)
\land\operatorname{GrantAllocationLive}_i(\operatorname{budgetGrantID}(t))
\land\operatorname{GrantNotExpired}_i(\operatorname{budgetGrantID}(t))
\land\operatorname{GrantNotRevoked}_i(\operatorname{budgetGrantID}(t))
\land\operatorname{ServiceClassAllowed}_i(t)\\
&\land\operatorname{AdmissionScopeMatch}_i(t,r)
\land\operatorname{CandidateHeaderMatch}(t,r)
\land b\preceq\operatorname{PerRedemptionCeiling}(t)\\
&\land\operatorname{usedRedemptionSlots}_i[t]<\operatorname{maxRedemptions}(t)\\
&\land\operatorname{spent}_i[t]
+\operatorname{outstandingReservations}_i[t]
+\operatorname{reservedChildren}_i[t]+b
\preceq\operatorname{totalCeiling}_i[t].
\end{aligned}
\]

Here `outstandingReservations` is the componentwise sum of `RESERVED` and `RUNNING` vectors, `reservedChildren` is the sum of unreclaimed child ceilings, and `usedRedemptionSlots` includes settled redemptions, outstanding redemptions, and redemption allowances reserved for children. Reservation atomically consumes a redemption slot, so concurrent in-flight requests count against `maxRedemptions`. Ticket/grant terminal state, expiry, and revocation block only new work; recorded-action lookup precedes those checks.

Each reservation follows

\[
\texttt{RESERVED}
\to\texttt{RUNNING}(\textit{executionActionID},\textit{principal},\textit{meterID})
\to\texttt{FINALIZED}.
\]

Before protected work, exactly one atomic claim creates a fenced receiver-controlled cumulative meter/hard envelope. Issuer time is `ReceiverTime(writerTimeEpoch, monotonicTick)`; each writer activation durably advances the epoch before work, expires earlier-epoch deadlines, and recovery-finalizes old running claims. The receiver derives `executionExpiry` no later than both reservation expiry and `claimedAt + MaxExecutionDuration` in one epoch; ticket/grant expiry or revocation blocks a fresh claim. Every paid subaction binds the exact running reservation, execution ID, and principal.

`ACCEPT`, `REJECT`, `UNKNOWN`, and `ERROR` charge receiver-authoritative parsing, closure-fetch, validation, inert staging, and promotion work through exactly one `FinalizeReservation`; each missing or integrity-alarmed component incurs its frozen conservative upper bound and records a per-component basis. The local-authority commit consumes the claim and records the terminal result, optional promotion, released vector, counters, durable local retention/in-transaction metadata, nonauthorizing outbox intents, meter digest/basis map, and immutable settlement. External storage/index/replication/notification effects MUST originate from a `PROMOTE` outbox and use a distinct funded claim. A running claim never returns to `RESERVED`; expiry/crash yields `UNKNOWN` with receiver-authoritative plus conservative-gap charges. Unclaimed cancellation releases the vector but consumes the redemption slot. No later transition can promote or add spend. A child ticket is unusable until its entire ceiling, redemption allowance, and count authority have been allocated from its parent.

A root ticket reaches irreversible `TERMINAL` state only with no `RESERVED`/`RUNNING` reservation or live descendant. Its transition removes the full grant work reservation, adds actual cumulative spend and consumed redemptions to the grant's finalized counters, and releases only unused resource/redemption allocation. Count/fanout authority remains consumed. For child ticket \(c\) of parent \(p\), the idempotent terminal transition instead enforces

\[
\begin{aligned}
\operatorname{spent}[p]'&=\operatorname{spent}[p]+\operatorname{actualSpend}[c],\\
\operatorname{reservedChildren}[p]'&=
\operatorname{reservedChildren}[p]-\operatorname{totalCeiling}[c],\\
\operatorname{settledRedemptions}[p]'&=
\operatorname{settledRedemptions}[p]+\operatorname{consumedRedemptions}[c],\\
\operatorname{reservedChildRedemptions}[p]'&=
\operatorname{reservedChildRedemptions}[p]-\operatorname{maxRedemptions}[c].
\end{aligned}
\]

A child grant \(c\) with exact parent \(g\) terminalizes only after all descendants are terminal and, in the same digest-first idempotent commit, enforces

\[
\begin{aligned}
\operatorname{finalizedSpend}[g]'&=
\operatorname{finalizedSpend}[g]+\operatorname{finalizedSpend}[c],\\
\operatorname{reservedChildGrantCeilings}[g]'&=
\operatorname{reservedChildGrantCeilings}[g]-\operatorname{totalCeiling}[c],\\
\operatorname{finalizedRedemptions}[g]'&=
\operatorname{finalizedRedemptions}[g]+\operatorname{finalizedRedemptions}[c],\\
\operatorname{reservedChildGrantRedemptions}[g]'&=
\operatorname{reservedChildGrantRedemptions}[g]
-\operatorname{totalRedemptionAllowance}[c].
\end{aligned}
\]

Its ticket-issue and grant-fanout allocations remain consumed. Subtracting the full child reservation without adding its finalized spend/redemptions is nonconforming.

Revocation alone does not reclaim allocation. New action IDs fail after terminalization even if signed expiry remains in the future; only identical stored actions replay. These transitions prevent sibling-ticket oversubscription, repeated zero-work child-object amplification, work-capacity recycling, and finalized-ticket resurrection.

A public `DemandOffer` is never a bearer ticket. An anonymous/public gateway creates a bounded audience-appropriate reservation per candidate, preventing an observer from stealing a visible single-use ticket. Permission capabilities have no mathematical-work vector; their finite nonreclaimable action-record allowance pays only bounded authorization bookkeeping from a separate receiver control reserve. Every fresh accepted action atomically consumes one unit, child issuance preallocates the child's entire action/fanout subtree, and rejected IDs create no per-ID durable state. Every protected action binds the exact unique `RUNNING` reservation, execution ID, principal, and receiver meter. Authorization records may share one transactional implementation with the demand ledger, but their schemas and work-resource invariants remain distinct.

## 9. Cryptographic mechanisms, including SNARKs

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Collision-resistant hashes over canonical encodings | **NOW** | Create typed CIDs and bind exact statements, contexts, inputs, dependencies, environments, policies, executables, and evidence. | Truth, authenticity without a key, persistence, availability, secrecy, or semantic equivalence. Ambiguous encoding defeats intended binding even with a strong hash. | Deterministic CBOR plus SHA-256, domain-separated by object type/schema version. Golden vectors and two independent encoders before federation. | S1 **STD**, S2 **STD** |
| Merkle trees / authenticated inventory roots | **NOW for reconciliation** | Commit to bounded object inventories, dependency closures, or anti-entropy buckets and request proofs/differences without transmitting an entire set. | Availability of leaves, correctness/admission of leaf content, freshness absent a trusted checkpoint, or one globally canonical tree. | Per-cell versioned Merkle bucket trees over admitted CIDs; roots are routing/reconciliation data until the receiver retrieves and checks leaves. | C2 **RP** |
| Digital signatures | **NOW for authentication; REJECT-P0 as validity evidence** | Bind a key to a canonical assertion, capability issuance, or transport message. | Truth, authority outside receiver policy, human/model identity, independence, or correct checking by the signer. | Standard signature suites exposed by TLS/COSE libraries; domain-separated signed structures; key/algorithm IDs and replay scopes. | S6 **SPEC**, S7 **STD** |
| General SNARK/succinct argument | **LATER, conditional on measured fanout** | Compress repeated verification of one *frozen deterministic relation* \(R_K\), such as “this exact exported checker accepted these committed public inputs.” Useful when many distinct validation domains would otherwise replay an expensive relation. | Correctness of \(R_K\), faithful arithmetization/VM semantics, correctness of formalization, witness availability, novelty, usefulness, or stronger logic. It does not turn social consensus into truth. | After P0.5, benchmark one pinned zkVM and one specialized construction against native replay on identical objects. Do not select either for the P0 acceptance path. | C3 **RP**, C4 **RP**, C8 **RP**, INT3 **INT** |
| zkVM | **LATER** | Reduce custom-circuit engineering when the fixed checker can run as a deterministic guest; bind guest image/ISA, inputs, outputs, and verifier key. | Correct compiler/ISA/syscall/memory semantics, low prover cost, small TCB, or coverage of arbitrary Lean tooling. | A pinned, audited-at-project-time zkVM candidate such as RISC Zero used only in a comparative benchmark; native replay remains the reference. No current version is endorsed here. | C9 **DOC**, INT3 **INT** |
| Specialized pairing-based SNARK | **LATER** | Benchmark a compact verifier for a small stable certificate relation if repeated fanout justifies circuit maintenance and any setup assumptions. | Setup integrity unless the scheme/setup provides it, circuit correctness, data availability, or easy upgrades. | A Groth16-style circuit implemented with a pinned library only for a small exported checker, never for the whole evolving agent stack. | C3 **RP** |
| Transparent STARK-like proof | **LATER** | Alternative benchmark when transparent setup or different cryptographic assumptions matter and larger proofs/hash work are acceptable. | Post-quantum security of every surrounding component, circuit correctness, confidentiality by default, or favorable economics. | One transparent implementation selected only after defining the relation and evaluation criteria; no P0 dependency. | C6 **RP** |
| Recursive proof-carrying data / folding | **LATER** | Aggregate already checked leaves and composition steps for stable, repeatedly consumed checkpoints; bind dependency and policy roots and enforce base cases/cycle rules. | Data availability, explainability, subset access, correct leaf policies, or groundedness unless the recursive relation explicitly checks them. | Prototype Nova/PCD-style aggregation only after native support graphs and demand distributions are measured. | C5 **RP**, C7 **RP** |
| Zero knowledge | **LATER only for a concrete confidentiality requirement** | Hide a witness to a narrowly defined validation relation while revealing named public inputs and the fact of acceptance. | Hidden access patterns, fair exchange, availability, statement confidentiality when public inputs reveal it, semantic fidelity, or truth beyond the relation. | Start, if needed, with a small SAT/finite-computation certificate relation. Public mathematical artifacts remain the default because reuse and repair need them. | C3 **RP**, C6 **RP** |
| Trusted execution environment attestation | **LATER; advisory unless explicitly trusted** | Potentially attest that a named measured image ran in hardware when native replay is unavailable or a confidential service is required. | Correctness of code, absence of hardware/firmware/side-channel flaws, mathematical validity, or durable witness availability. | Treat RATS-style evidence appraisal as `TRUSTED_ATTESTATION` with an explicit attester/verifier/endorser TCB and policy, never silently as `LOCAL_REPLAY`; select and pin a concrete hardware evidence format only if this mechanism is adopted. | S8 **SPEC**, INT3 **INT** |

### 9.1 Exact SNARK adoption gate

For a fixed native replay cost \(c_L\), native artifact transfer \(s_L\), succinct prover cost \(c_P\), verifier cost \(c_V\), succinct bytes \(s_V\), fixed engineering/audit/setup cost \(F\), transfer weight \(\mu\), and number \(h\) of distinct validation domains, succinct verification can be economically favorable only if

\[
h\bigl((c_L-c_V)+\mu(s_L-s_V)\bigr)>c_P+F.
\]

The relevant \(h\) is not the simulated logical-agent count. It is the measured number of independent receiver domains that would actually replay the same relation after cell-level caching. The denominator may be nonpositive. Even above the break-even point, adoption requires:

1. a frozen relation identifier/public-input encoding and a receiver-pinned setup/public-parameter transcript whose validated verifier key or universal-circuit commitment is bound to that exact relation, proof system, and security parameter;
2. cross-checks against native replay on valid and mutated inputs;
3. an explicit cryptographic/setup/verifier/VM TCB;
4. witness/native-artifact availability labels;
5. upgrade and key-epoch rules;
6. proof-generation resources isolated from mandatory checking.

Thus, SNARKs are plausible verification compression, not the mechanism that makes agents collaborate and not an oracle that decides mathematics.

## 10. Blockchain, consensus, and transparency

Consensus protocols can establish agreement on an ordered state-machine history under their fault, synchrony, membership, and cryptographic assumptions. They cannot establish that a mathematical payload is correct. Formally, even if a protocol proves

\[
\forall i,j\in H:\operatorname{decide}_i(k)=\operatorname{decide}_j(k),
\]

the decided value may be an invalid proof, a mistranslated statement, or an unavailable content hash. DTMKN must validate the payload independently.

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Public permissionless blockchain | **REJECT-P0** | No role in theorem admission, routine object storage, task assignment, or support. A later deployment may optionally anchor sparse checkpoint hashes if an explicit external-timestamp/censorship threat justifies the cost. | Mathematical truth, data availability of off-chain artifacts, identity, honest majority of mathematical experts, privacy, low latency, or correctness of clients/contracts. | None in v0. If evaluated later, anchor only a versioned checkpoint root and compare against ordinary cross-logging/witnesses. | B1 **SPEC**, B5 **STD**, B6 **STD** |
| Permissioned Byzantine consensus (PBFT/HotStuff family) | **REJECT-P0 globally; LATER for a narrow control object** | Potentially serialize a small governed state that genuinely needs one value, such as a policy epoch, capability-issuer set, or scarce cross-cell escrow. | Theorem validity, permissionless participation, data availability, or safety/liveness outside exact quorum/fault/network assumptions. It introduces membership governance. | Do not include in the mathematical data plane. If a later requirement appears, specify the state machine and fault threshold first, then benchmark a mature BFT implementation. | B2 **RP**, B4 **RP**, B8 **RP** |
| Crash-fault consensus (Raft) | **LATER, cell-local only** | Replicate a cell's mutable operational metadata when high availability is needed and operators share one trust domain. | Byzantine tolerance, global federation semantics, mathematical truth, or availability during loss of quorum. | A mature Raft-backed store behind one cell interface; never expose commit index as proof validity. | B3 **RP** |
| Smart-contract verification of a succinct proof | **LATER** | Let an on-chain or very constrained client check one frozen succinct relation if a real consumer requires it. | Correct relation/circuit, source artifact availability, theorem usefulness, or privacy unless separately provided. Consensus only agrees that the contract returned a result. | Only after the Section 9 gate; contract commits relation/verifier-key/public-input roots and native-witness status. | C3 **RP**, C4 **RP** |
| SCITT/COSE transparency receipts | **LATER supporting plane** | Provide portable registration/receipt proofs for signed statements and verifiable data structures; support auditing of publication/checkpoint events without putting truth in the log. | Accuracy of registered claims, completeness of observation, mathematical validity, or prevention of every split view. | Profile RFC 9943 statements and RFC 9942 receipts only after P0 evidence objects stabilize. These RFCs were published by the RFC Editor in June 2026; no maturity or deployment claim is made here. | B5 **STD**, B6 **STD** |
| Certificate-Transparency-style gossip/witnessing | **LATER** | Detect inconsistent checkpoint views when monitors exchange them and provide portable fork evidence. | Prevention of equivocation before views meet, mathematical validity of logged content, or artifact availability. | Independent monitors, checkpoint gossip, and optional cross-logging; keep this out of the first cooperation experiment. | B7 **SPEC** |
| Cryptocurrency/token rewards, proof-of-work/stake, truth markets | **REJECT-P0** | No P0 scheduling, identity, validation, or truth role. The testbed's utility function is an experimental measurement lens, not money or governance weight. | Alignment, Sybil resistance for arbitrary tasks, honest formalization, robustness to collusion, or a defensible value function. | No token. Use fixed experimental budgets, receiver-issued capabilities, and published component metrics/Pareto frontiers. | B1 **SPEC**, INT2 **INT** |
| Voting or quorum certification of theorem truth | **REJECT-P0** | None. Quorums may authorize an operational policy change but cannot replace the theorem's evidence contract. | Correctness under correlated honest mistakes, malicious majorities, ambiguous statements, or hidden shared dependencies. | Keep vote/quorum counts absent from `Stable_P(RelianceQuery)` and the support fixed point. | F6 **RP**, INT1 **INT** |

### 10.1 Why no blockchain is needed for v0

The durable P0 payload is an unordered, immutable set of locally admitted facts. Set union does not need total-order consensus. Mutable-looking status is a deterministic projection, leases are ephemeral, and conflicts are preserved rather than overwritten. Avoiding a global log removes a throughput bottleneck and a governance dependency while retaining local verifiability.

Consensus becomes relevant only if a later requirement introduces a scarce, globally exclusive, mutable object. That requirement must be named before choosing a consensus protocol. “Decentralized” alone is not such a requirement.

## 11. Hostile execution and sandboxing

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| Streaming bounded canonical parser | **NOW** | Return `REJECT` for declared malformed/noncanonical/over-limit syntax such as oversized frames, excessive nesting, duplicate keys, invalid tags, decompression amplification, or excessive graph degree before expensive work. An unexpected parser/sandbox/invariant failure is `ERROR`. | Semantic validity, safety of later build/execution, or canonical behavior if implementations disagree. | A small parser for the frozen CBOR profile; hard byte/object/depth/decompression limits; golden and mutation vectors; differential decoder tests. | S1 **STD**, V5 **RP**, INT1 **INT** |
| Separate parser, unpacker, builder, checker, agent, and checkpoint tiers | **NOW** | Prevent one hostile stage from inheriting the broad authority/resources of another. Checker capacity and credentials are isolated from generators. | Absence of sandbox escapes or side channels; correctness of the checker. | Distinct processes/principals, no ambient credentials/network, read-only CAS, fresh bounded temporary directories, explicit artifact handoff, and default-deny interfaces. | INT1 **INT** |
| Linux namespaces, cgroups v2, seccomp, and filesystem controls | **NOW on Linux workers** | Enforce CPU, wall-clock, memory, process, file, inode, output, syscall, device, and I/O bounds around native proof/build processes. | A complete security boundary against kernel vulnerabilities, deterministic execution, or mathematical correctness. | Rootless users, cgroups v2, seccomp, read-only mounts, and no host sockets/devices. A declared resource-limit kill maps to `UNKNOWN`; an unexpected sandbox/control failure maps to `ERROR`. | X1 **DOC**, X2 **DOC** |
| WebAssembly sandbox with fuel/memory limits | **NOW for suitable generated checkers/computations; not for arbitrary Lean builds** | Run small portable deterministic witness generators or certificate checkers with a narrow host API and metered execution. | Safety of the runtime implementation, constant-time behavior, full POSIX isolation, compatibility with all tools, or correctness of guest code. | A pinned Wasmtime runtime with fuel/epoch interruption, memory/table limits, no ambient WASI capabilities, and explicit input/output buffers. | X3 **SPEC**, X4 **DOC** |
| MicroVM isolation | **LATER for initial single-operator test; NOW before hostile multi-tenant native builds** | Strengthen isolation for untrusted native elaborators, compilers, solvers, or restored environments that require an OS-like surface. | Bug-free hypervisor/kernel/device model, reproducibility, absence of side channels, or theorem validity. | Firecracker-class microVMs with immutable root image, no network/credentials, minimal devices, resource caps, and destruction after each job. | X5 **RP** |
| OCI container images | **NOW as packaging; REJECT-P0 as the sole boundary** | Package pinned dependencies and simplify repeatable deployment. Verify manifests/digests before use. | Secure isolation, reproducibility, correct dependencies, safe contents, or absence of mutable external fetches. | Digest-pinned OCI images inside a stronger runtime policy; generate an explicit dependency/environment manifest. | S3 **SPEC**, S4 **SPEC** |
| Safe typed checkpoints | **NOW** | Resume useful work without deserializing arbitrary executable object graphs or granting restored authority. Bind checkpoint to attempt/input/environment and treat contents as untrusted. | Correct progress, completion, safe continuation across different code/environment versions, or authority to renew a lease. | Versioned data-only schemas; no pickle/native object deserialization; sandboxed validator; size/reference limits; separate validated progress summary. | INT1 **INT** |
| Resource-bounded proof checking | **NOW** | Contain proof bombs and preserve service. A declared timeout/fuel/memory/resource exhaustion yields `UNKNOWN`, never `REJECT`; an unexpected checker crash, sandbox failure, internal invariant failure, corrupt runtime, or TCB alarm yields `ERROR`. | Completeness or a proof that a resource-bounded/incomplete run's artifact is invalid. | Per-contract CPU/memory/output limits, warm/cold profiles, cancellation, and protected validation queues; record exact reason/limits and settle receiver-authoritative work plus frozen conservative bounds for gaps. | INT1 **INT**, INT2 **INT** |

The sandbox is part of availability and host integrity, not part of the mathematical proof. Validation must not access the network or mutable names. Every referenced object is resolved to a typed immutable CID before execution.

## 12. Protocol verification and systems testing

| Mechanism | P0 decision | Exact DTMKN role | What it does **not** establish | Implementation candidate | Primary source |
|---|---|---|---|---|---|
| TLA+ state-machine specification | **NOW** | Model exact root/child issuance and spend roll-up, live/terminal tombstones, reserve/claim/meter/cancel/local-finalization/outbox paths, capability fanout/action allowance, crash-safe time epochs, receive/quarantine/admit, reliance tuple publication, at-least-once delivery, lease retry, replica boundaries, and validation reserve. State safety and conditional liveness assumptions explicitly. | Correct implementation, cryptographic security, real-time performance, or mathematical validity of evidence. | A small normative TLA+/PlusCal model with TLC runs; keep unbounded mathematics abstract and inject crash points around every ledger, staged-object, epoch-publication, and outbox boundary. | V1 **RP/DOC**, INT2 **INT** |
| Apalache symbolic model checking | **NOW if it handles the frozen model; otherwise TLC remains sufficient** | Search bounded symbolic instances and parameter combinations for counterexamples to protocol invariants. | An unbounded proof, correctness outside the translation fragment, or coverage of implementation bugs. | Pin Apalache and its supported TLA+ subset; archive model/config/output and cross-check small instances with TLC. | V2 **RP/DOC** |
| Alloy relational analysis | **NOW for graph/schema audits** | Enumerate small signed support graphs to find ungrounded cycles, mixed-polarity composition errors, disputed literals leaking into \(U_P^{\mathrm{strict}}\), path-contract leakage, accidental fidelity closure, malformed remainders, and override-order ambiguity. | Correctness beyond the checked scope or temporal/network behavior unless modeled. Small-scope success is not proof. | Model \(K_P\), projected \(D_P/R_P\), \(U_P^{\mathrm{strict}}\), finite support trees, fidelity parents, and acyclic reliance supersession; convert counterexamples into fixtures. | V3 **RP** |
| Tamarin protocol analysis | **LATER, after the concrete auth/capability/demand wire protocol freezes** | Analyze authentication, holder/audience binding, action/digest replay, finite capability control-record debits, child attenuation, execution-claim binding, expiry/revocation epochs, and attacker-controlled traces symbolically. | Atomic database isolation/crash recovery, meter integrity, parser security, denial of service, mathematical validity, or properties absent from the model. | Model the exact handshake, permission-capability action, demand-ticket, reservation, claim/meter binding, local-finalization/outbox, cancellation, and terminal messages; pair it with transactional crash tests. | V4 **RP** |
| Property-based and differential testing | **NOW** | Test canonical encoding, root/child tags and issuance, nonzero child-grant roll-up, nonreclaimable fanout/action records, terminal nonresurrection, reservation/claim/meter/cancel/local-finalization/outbox, permission binding, valid-junk nonpromotion, action/digest idempotence, crash-safe time, atomic reliance publication, signed fixed points/witness trees, path-contract checks, result taxonomy, and independent encoders/checkers. | Exhaustive coverage or a proof of absence of bugs. Oracles can share the same mistake. | Generators/shrinkers; crash injection at issuance/reserve/claim/meter/check/staging/finalize/outbox/terminal and state/dirty/epoch publication boundaries; capability-ID floods; reboot/clock reset; a slow signed-support oracle; proof↔counterexample races; two encoders; native-vs-certificate cross-checks. | V5 **RP**, INT2 **INT** |
| Coverage-guided fuzzing | **NOW** | Attack parsers, archives, graph loaders, proof adapters, and checkpoint decoders with malformed and resource-amplifying inputs. | Semantic correctness or complete path coverage; a crash-free run is not a security proof. | libFuzzer/cargo-fuzz-like harnesses with sanitizers where supported, strict time/memory limits, and a retained minimized corpus. | V6 **DOC** |
| Deterministic event-driven simulation | **NOW** | Evaluate \(10^3\)–\(10^5\) logical agents under replayable loss, delay, churn, partitions, heavy-tailed runtimes, correlated errors, and bounded malicious load; reserve \(10^6\) for a stretch complexity run. Calibrate from held-out traces of the 8–16-worker minimum and later expansions. | Real-world fidelity merely from scale, cryptographic assurance, proof of liveness, or one model call per simulated agent. | Seeded virtual time, deterministic event order, trace recording/replay, invariant monitors, sensitivity ranges, and baseline/ablation runs across many seeds. | V7 **RP**, INT2 **INT** |
| Fault/history testing of a real deployment | **NOW** | Inject crash/restart/clock reset, delay, duplication, reordering, partitions, valid-junk and capability-action floods, nonzero child recycling, double-spend races, epoch-publication races, staged-object/outbox faults, hot keys, blackholes, stale ads, and overload; compare observed histories with invariants. | Proof for all executions or linearizability where the protocol intentionally offers only local views and re-admission. | A harness around exactly five primary cells plus a three-cell smoke configuration and 8–16 initial workers, with later 8–64-worker expansion, deterministic fault scripts, crash points, and post-run history checking. | V7 **RP**, INT2 **INT** |
| Machine-checked support semantics and refinement | **NOW for declarative lemmas; LATER for executable refinement** | In the first artifact, prove in Lean or an equivalent prover that the finite signed least-fixed-point construction is grounded, ungrounded cycles contribute nothing, mixed-polarity derivations compose, disputed literals and paths through them are excluded from \(U_P^{\mathrm{strict}}\), and accepted witnesses satisfy the finite-tree definitions. After the production evaluator freezes, prove it refines those declarative semantics and extracts valid witnesses. | Correct input facts, checker soundness, path-contract code, concurrency implementation, production-algorithm equivalence before the later refinement proof, or performance. | Formalize signed literals, finite ranks/approximants, strict opposites, and `FiniteActiveTree` in Lean now; retain a slow executable oracle and differential tests, then add the optimized-evaluator refinement theorem later. | F1 **DOC**, K3 **RP**, INT2 **INT** |

### 12.1 Minimum model obligations before implementation claims

The P0 artifact must not merely contain models; it must state and check at least these propositions under explicit bounds/fairness assumptions:

1. an unadmitted object cannot enter signed support, protected indices, cancellation, or durable merge;
2. a public `DemandOffer` cannot be redeemed, and a valid object cannot start protected closure fetch/checking without an authentic audience/scope-matching reservation and its unique running execution claim/meter;
3. lookup of an existing `(ticketID, redemptionActionID)` precedes live-state, freshness, revocation, and debit checks; the same request digest returns the recorded reservation/settlement even after terminalization, a different digest is rejected, and a fresh action cannot resurrect a terminal grant or ticket;
4. `ACCEPT`, `REJECT`, `UNKNOWN`, and `ERROR` locally finalize per-component receiver-authoritative/conservative parsing, closure-fetch, validation, staging, retention, and metadata work; external effects require separate funded executions, only soundly unused reserve is released, and crashes at every reserve/claim/meter/check/finalize/outbox boundary conserve issuer resources;
5. root constructors require absent parent tags; concurrent child issuance binds exact parents and checks issuer/epoch/grant, authority/audience attenuation, scope/class attenuation, artifact inclusion, predicate implication, contract strictness, expiry, parent work balance, and nonreclaimable descendant-issue balance; no child is usable before all allocations commit, and zero-work terminal loops remain finitely bounded;
6. an ungrounded signed-support strongly connected component contributes nothing to \(K_P\) or \(U_P^{\mathrm{strict}}\);
7. a refutation with mixed supported/refuted premises composes, and a direct checked counterexample can close `REFUTE`;
8. if both polarities of a judgment are in \(K_P\), neither is in \(U_P^{\mathrm{strict}}\), and no path through either closes downstream work;
9. closure presents a finite active support tree, so a proof admitted under a forbidden axiom, weaker validation basis, reviewer scope, or diversity policy cannot close a stricter same-judgment obligation; current strict P0 permits exactly local replay and receiver-checked domain certificates;
10. a formal proof cannot close a semantic-intent parent without the separate accepted fidelity contract;
11. `REJECT` is used only for a declared definitive malformed/contract/proof verdict; bounded incompleteness is `UNKNOWN`; unexpected checker/internal/sandbox/TCB failure is `ERROR`; neither latter outcome creates signed support or negative suppression;
12. a challenge notice without local defect evidence cannot remove support;
13. every superseding reliance action, including `QUARANTINE`, names exact earlier override CIDs; an unseen named predecessor leaves the action pending with `UNKNOWN(MISSING_OVERRIDE_PREDECESSOR)` until closure arrives; the graph is acyclic; and all delivery orders of incomparable quarantine/release facts derive the same fail-closed view;
14. every potentially support-changing event publishes its state, dirty seeds, and next reliance epoch at one linearization point or exposes a fail-closed in-progress epoch, and an old cached acceptance cannot return `ACCEPT` without rechecking its exact tree under one current snapshot and re-reading the epoch unchanged immediately before response;
15. a blackholed lease cannot suppress all retry after `L_max`;
16. direct set merge is associative, commutative, and idempotent only inside one logical cell's non-Byzantine replica cohort with one nonsplit-brain issuer ledger or disjoint writable escrow; every independently operated cell re-admits imported candidates even when policy identifiers match;
17. equal admitted facts/objects/policies/reliance epochs produce equal views;
18. a failed attempt cannot yield `REFUTED` without checked counterevidence;
19. overload admission prioritizes mandatory validation over new generation under the declared load bound;
20. rendezvous routing touches a bounded number of cells per step and, in the five-cell primary v0, progressive exploration reaches the full configured roster within five routing epochs.
21. capabilities have no mathematical-work vector; their finite control-record allowance is atomically debited for every fresh accepted action, child issuance preallocates the complete action/fanout subtree, rejected IDs create no per-ID state, and every protected resource action binds the exact unique running reservation, execution ID, principal, and receiver meter;
22. root-ticket, child-ticket, and grant terminal tombstones reject all fresh actions even when signed expiry remains in the future and released balance has been assigned to a sibling;
23. two competing finalization/promotion digests yield one immutable local settlement whose spend equals per-component authoritative/conservative accounting, whose promotion branch alone can retain staged local bytes and create nonauthorizing outbox intents, and whose external effects use separate funded executions;
24. `SUCCINCT_ARGUMENT` is not a current strict-P0 validation basis, and `OPAQUE_RELIANCE` cannot satisfy a public reusable-knowledge contract;
25. thirty-two concurrent claims for one reservation create exactly one running execution and one aggregate hard envelope;
26. an untrusted zero-use report cannot release nonzero actual use, and an integrity-alarmed/missing meter charges the conservative bound;
27. every running execution has an issuer-derived bounded expiry in crash-safe receiver time; writer restart advances the time epoch and recovery-finalizes old claims before new protected work, without returning any to `RESERVED`;
28. unclaimed cancellation consumes its redemption slot, and nested zero-work ticket/grant loops stop at nonreclaimable issue/fanout limits;
29. a cached proof followed by an exact counterexample—and symmetrically a cached refutation followed by proof—returns non-acceptance before bounded reverse traversal;
30. terminalizing a nonzero-spend child grant subtracts its full parent reservation while rolling its finalized spend/redemptions into the parent, so a sibling cannot reuse spent capacity;
31. \(10^5\) distinct authenticated control-action IDs cannot create more accepted replay records than the root capability subtree's finite action allowance, including at the last-unit concurrency boundary;
32. crash between fact preparation, dirty-seed recording, and epoch publication exposes only the old tuple, new tuple, or fail-closed in-progress epoch;
33. crash at inert staging, local retention/admission, outbox, and external-effect boundaries cannot create an admitted-but-unsettled object or spend a finalized reservation;
34. a platform monotonic-clock reset/reboot cannot extend an old grant, ticket, reservation, or running claim;
35. a forbidden-axiom derivation paired with an unrelated clean attestation fails exact local replay/attestation reconciliation.

## 13. Recommended P0 implementation profile

This is a candidate profile for measurement, not a normative mandate. A component may be replaced if it preserves the interfaces, conformance vectors, and fault semantics.

| Layer | P0 candidate | Why it fits | Mandatory qualification |
|---|---|---|---|
| Object wire format | Frozen deterministic-CBOR subset, typed domain separation, SHA-256 CID | Compact immutable objects and standard primitives | Two independent encoders must match golden vectors; reject noncanonical/duplicate-key inputs before hashing. |
| Local durable state and spend ledger | Inert staged CAS plus a pinned SQLite release, initially local-filesystem WAL with `synchronous=FULL`, or another crash-recoverable transactional local metadata store | Simple inspectable per-cell persistence; one transaction makes root/child allocation, reservation/claim/meter/cancel/local-finalization, local retention references, outbox intents, terminal tombstones, bounded permission replay, admission, and reliance tuple publication atomic | The database is issuer/logical-cell local, not a global truth service, and cannot atomically commit external stores or remote effects. Freeze SQLite/VFS/filesystem and sync semantics; do not place WAL on a network filesystem; retain one fenced writer and crash-safe time epoch. External effects require separately funded outbox executions. Crash/power-loss inject every ledger/staging/outbox/epoch boundary, then run integrity and history scans. See D11. |
| Support engine | Small fixed-rule evaluator for signed \(K_P\), projected \(D_P/R_P\), \(U_P^{\mathrm{strict}}\), finite support-tree witnesses, reliance epochs, and dirty-root cursors | Supports mixed-polarity composition and path-dependent closure without trusting a cached bare judgment | Cross-check sets/trees against a slow reference; old-epoch acceptance requires an exact current-tree check and final unchanged-epoch read, not dirty-root disjointness alone; no plugin/user rule execution in the core. |
| Lean validation | Pinned Lean 4 subprocess adapter, offline environment closure, exact axiom/dependency report | Matches the chosen real corpus and keeps generation outside the kernel boundary | Separate build/elaboration/check phases and limits; seed mutations, hidden assumptions, and environment drift. |
| Agent interface | Standalone typed work items, artifacts, and reports over local RPC/process pipes; adapters for proof, planner, critic, retrieval, checker, and repair roles | Heterogeneous agents can work alone or cooperate without sharing private internal state | Every report is untrusted; no direct access to admitted storage or validator credentials. |
| Scheduler | Grant/ticket/reservation/claim/meter/local-finalization/outbox admission, finite receiver service/capability classes with frozen service floors, fixed hard filters, object/goal/interest rendezvous, bounded exploration, and issuer-local grants; pull, WFQ/DRR/aging, leases, stealing, and portfolios are separable evaluation features | Protects scarce resources and tests optional execution-efficiency hypotheses without a learned/global scheduler | Claim/meter before protected work; per-component receiver-authoritative/conservative local settlement; inert pre-verdict staging; separately funded outbox effects; nonreclaimable issue/control-record bounds; protected validation reserve, valid-junk nonpromotion, idempotence, terminal nonresurrection, scope-Sybil resistance, and overload shedding are mandatory. |
| Federation | Exactly five independently governed authenticated logical cells for the primary run; three cells only for smoke testing; bounded publication hints/subscriptions, rendezvous home fanout \(r=2\), pull transfer, and candidate anti-entropy; one logical cell also has two crash-fault replicas | Gives a real thin autonomous reuse federation and reproducible scale experiments without a permissionless overlay | The two homes are independent candidate rendezvous sites, not one replica cohort or authority. Each autonomous cell has its own grant and fenced write-authoritative ledger replica per epoch; an optional program alone may prepartition a shared envelope into disjoint escrow. Public DHT/global ANN are later, and every independent cell re-admits. |
| Evaluation harness | Harness-only suite metadata, common visible inputs/faults/random tapes, sealed snapshots, prior-artifact-blind treatment, and estimand-specific bootstrap analysis | Separates base efficacy, reliability, local memory, cross-cell reuse, coordination, program overlay, and decentralization overhead | Resample complete seed replicates: use paired within-seed differences for contrasts and one-profile statistics for capability/queue gates. Population inference aggregates the relevant statistic within each instance and resamples whole independent instances. Tasks are never resampled across interference. Suite metadata never enters live scheduling/admission. |
| Isolation | Separate processes for all tiers; Linux cgroups/namespaces/seccomp for native jobs; Wasmtime for suitable narrow guests; microVM before hostile multitenancy | Layered containment matched to workload | Containers/digests alone are neither sandbox nor reproducibility proof. No ambient network or credentials during validation. |
| Verification harness | Lean or equivalent declarative grounded-support lemmas; TLA+/TLC; optional Apalache; Alloy graph model; property/differential tests; fuzzers; deterministic simulator | Different methods expose different failure classes | Each claim maps to a proof, model, or test and states its scope; machine-checked declarative lemmas do not yet prove refinement by the optimized implementation, and passing tests are not promoted to proofs. |
| Succinct field | Schema-only optional `SuccinctArgument` plus native-artifact availability flag | Avoids a future incompatible format without creating a P0 dependency | The field never participates in P0 acceptance; later verifier relation and policy must be explicit. |

### 13.1 Components deliberately not in the P0 critical path

- public blockchain or global BFT ledger;
- token economics, one-agent-one-vote, or global reputation;
- SNARK/STARK/zkVM verification;
- trusted remote validator quorum;
- global civil/model identity registry;
- social attribution, priority, and ownership workflow;
- universal ontology or automatic cross-theory equivalence;
- public DHT or permissionless membership;
- global ANN discovery or learned scheduling;
- general cross-prover/theory morphisms (beyond manually supplied in-environment relations);
- general certified-exhaustion/negative-cache semantics;
- arbitrary executable checkpoint restoration;
- mandatory transparency log.

This exclusion reduces the initial trusted computing base and lets the experiment answer the urgent question: whether typed, validated, resource-aware decentralized cooperation improves useful knowledge production.

## 14. Reuse/build boundary by deliverable

| Deliverable element | Reuse | DTMKN-specific work | Acceptance evidence |
|---|---|---|---|
| Protocol/specification | CBOR, TLS, capability and distributed-systems precedents | Offer/root-child-ticket/reservation/claim/meter/cancel/local-finalization/outbox lifecycle; exact root/child tags and roll-up; permission/work-resource separation plus bounded control records; nonreclaimable issue authority; crash-safe receiver time; terminal tombstones; fidelity contracts; signed \(K_P\), projected \(D_P/R_P\), \(U_P^{\mathrm{strict}}\), support-tree contracts; atomic reliance-state/epoch publication | Reviewable Markdown plus machine-readable schemas, conformance vectors, and machine-checked grounded-support lemmas |
| Reference blackboard | Local transactional/CAS primitives, CRDT set laws | Raw/quarantine/admit separation; inert staging and authoritative local retention; demand execution/settlement/outbox; signed trees; epoch-linearized overrides/dirty roots | Unit/property/model tests for every P-S and P-C property in Section 3 |
| Scheduler | Pull, leases, work stealing, fair-queue, aging, and backpressure precedents | Demand tickets and unique metered executions; fixed rendezvous routing; permission capabilities plus work/count envelopes; diversity/failure-domain policy | Equal-budget baselines/ablations; valid-tautology floods; claim/meter/replay/crash and overload histories |
| Knowledge integration | ATMS and Datalog precedents; narrow manual relation transport | Signed justifications; finite contract-checked trees; fidelity parents; local target replay; \(D_P/R_P/U_P^{\mathrm{strict}}\); bounded repair | Mixed-polarity refutations; contract leakage; vacuous formalizations; inconsistency; high-fanout incidents; alternate support |
| Lean adapter | Lean 4 kernel/toolchain | Exact environment profile, axiom policy, result object, sandbox interface | Mutation suite; independent clean replay; zero seeded invalid automatic admissions |
| Federation | Rendezvous hashing, scoped pub/sub, anti-entropy | Fixed authenticated cells; candidate-only inter-cell exchange; same-authority crash-fault replica merge; capability-gated pulls | Partition/heal histories, foreign-admission rejection, no \(O(N)\) broadcast, poisoned-route tests |
| Security boundary | TLS, signatures, caveated capabilities, local transactions, transactional-outbox patterns, OS/Wasm/microVM isolation | Holder proof of possession; permission/work-resource separation; bounded action records; atomic issuance/claim/meter/local-finalization/terminal state; explicit cross-store boundaries; demand admission; fidelity-reviewer scope; bounded gateways | Forgery/replay/double-authority/action-flood/multi-claim/meter-underreport/count-amplification/clock-reset/epoch-publication/outbox/cache-race/crash tests; valid-junk and sandbox-bomb corpora |
| Simulator/evaluation | Deterministic simulation and statistical experimental practice | Calibrated mathematical-agent/error/fault model; baselines and ablations | Raw traces, seeds, confidence intervals, calibration error, limitations |
| Succinct verification | Existing SNARK/STARK/zkVM research | Exact DTMKN relation/profile and native-artifact policy | Deferred benchmark and break-even analysis; no P0 success dependency |

### 14.1 Concrete first artifact

The first publishable artifact is the Lean-first **Reliable Mathematical Research and Reuse Testbed v0**:

- a one-cell local no-network research/validation capability gate before federation claims;
- exactly five independently governed authenticated logical cells for primary evaluation and a three-cell smoke test; object/goal/interest rendezvous fanout \(r=2\), issuer-local autonomous grants, one two-replica crash-fault cell for reconciliation/fenced-failover tests, 8–16 real/scripted workers initially, and 8–64 only after local gates pass;
- 2–3 overlapping Lean namespaces, 30–50 harness-side benchmark task contracts, staggered autonomous streams, zero coordination scopes in the primary profile, and roughly 100–200 internal work items initially; larger runs are expansion experiments;
- grant-backed ticket/reservation/claim/meter/local-finalization/outbox demand objects, exact root/child work allocation and spend roll-up, nonreclaimable issue/action authority, cancellation/terminal ledgers, permission-only work capabilities with bounded control records, and dynamic signed AND/OR work/justification graphs;
- bounded publication hints/subscriptions, receiver-owned fair scheduling, typed partial/failure hints, local proof/certificate/fidelity checking, support-tree contract checks, \(K_P/D_P/R_P/U_P^{\mathrm{strict}}\) truth maintenance, and deterministic dirty reliance epochs;
- benign-error, correlated-error, malicious-input, churn, partition, and overload injection;
- isolated, local-typed, raw-reuse, typed-reuse, prior-artifact-blind, full-coordination, optional-program, central-typed, central-FIFO, small-trace oracle, and naive-broadcast profiles;
- Lean or equivalent grounded signed-support/refutation lemmas, protocol/model artifacts, a source-pinned reproducibility bundle, raw traces, and an independent audit/disposition log.

The defensible experimental claims are decomposed and conditional: the local core either exceeds its capability floor or it does not; typed cross-cell reuse either improves the preregistered endpoints or it does not; active coordination and optional programs either add net value after complete overhead or they do not. Every negative result is a valid deliverable.

## 15. Conditional adoption triggers

| Deferred mechanism | Required trigger before adoption |
|---|---|
| SNARK/zkVM | A frozen deterministic relation and setup/key/relation binding; measured distinct-domain replay fanout above the break-even threshold; independent native cross-checks; acceptable prover/audit/upgrade cost; an adaptive multi-theorem soundness theorem and frozen \(q_{\max}\)/epoch error budget. |
| Recursive aggregation | Stable leaf policies and composition relation; repeated batch demand; cycle/base-case proof; acceptable subset-access and data-availability behavior; an explicit recursive composition/error budget. |
| Zero knowledge | A concrete confidentiality/leakage requirement that cannot be met more simply; a narrow public statement; an explicit witness-availability and fair-exchange policy. |
| BFT consensus | A named globally exclusive mutable state, explicit membership/fault threshold, and evidence that CRDT/local-policy semantics cannot meet it. |
| Raft/local replication | Measured cell-availability requirement that justifies operational complexity; crash-fault trust model is acceptable. |
| SCITT/transparency | Independent publication/audit actors and an explicit equivocation/rollback/freshness threat; stable DTMKN statement profile. |
| MicroVMs | Native hostile multitenancy or a build surface too broad for process/Wasm isolation; measured cost acceptable. |
| MMT/cross-foundation interchange | One working Lean-first theory-morphism corpus and a concrete second-system consumer; explicit translation obligations. |
| General morphism synthesis/transport | The manually supplied in-environment relations and target-side replay corpus work; a concrete reuse bottleneck and second theory/prover consumer justify generalization. |
| Public DHT/permissionless membership | The authenticated five-cell primary federation passes (with the three-cell smoke test reported separately); a concrete scale/discovery requirement exists; membership authority, Sybil/eclipse assumptions, multi-provider routing, and resource admission are specified. |
| Global ANN discovery | Exact/structural/manual-relation retrieval has a measured recall bottleneck; a frozen hard-negative set and poisoning/resource policy exist. |
| Learned scheduling | Fixed routing/fair queues produce enough frozen train/evaluation traces; improvement is evaluated out-of-sample without affecting validation or demand admission. |
| General certified exhaustion | At least one narrow finite-region capsule demonstrates safe containment reuse; search-region semantics and mutation invalidation are machine-checkable. |
| Persistent identity/attribution | A concrete abuse, contractual, credit, licensing, or governance requirement not met by ephemeral operational keys/capabilities. It still cannot enter theorem validity rules. |

## 16. Primary-source register

The register favors standards, official specifications/documentation, and original research papers. It deliberately avoids claims based only on product marketing or recent benchmark summaries. DOI and RFC links are stable locators; all executable dependencies still require an archived exact release/commit and local conformance testing.

### 16.1 Formal mathematics

- **F1 — DOC:** Lean developers, [*The Lean Language Reference*](https://lean-lang.org/doc/reference/latest/). This is upstream language/checker documentation; the implementation used by DTMKN must be pinned rather than following `latest` silently.
- **F2 — RP:** Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer, “The Lean Theorem Prover (System Description),” CADE-25, 2015, [DOI 10.1007/978-3-319-21401-6_26](https://doi.org/10.1007/978-3-319-21401-6_26).
- **F3 — RP:** Marijn Heule, Warren Hunt Jr., Matt Kaufmann, and Nathan Wetzler, “Efficient, Verified Checking of Propositional Proofs,” ITP 2017, [DOI 10.1007/978-3-319-66107-0_18](https://doi.org/10.1007/978-3-319-66107-0_18).
- **F4 — RP:** Luís Cruz-Filipe, Marijn Heule, Warren Hunt Jr., Matt Kaufmann, and Peter Schneider-Kamp, “Efficient Certified RAT Verification,” CADE-26, 2017, [DOI 10.1007/978-3-319-63046-5_14](https://doi.org/10.1007/978-3-319-63046-5_14).
- **F5 — RP:** Leonardo de Moura and Nikolaj Bjørner, “Z3: An Efficient SMT Solver,” TACAS 2008, [DOI 10.1007/978-3-540-78800-3_24](https://doi.org/10.1007/978-3-540-78800-3_24). This supports solver use as a generator; it is not a certificate for an arbitrary DTMKN claim.
- **F6 — RP:** Algirdas Avizienis, “The N-Version Approach to Fault-Tolerant Software,” *IEEE Transactions on Software Engineering* 11(12), 1985, [DOI 10.1109/TSE.1985.231893](https://doi.org/10.1109/TSE.1985.231893). DTMKN cites it as a diversity precedent and retains the correlated-failure caveat.

### 16.2 Knowledge representation and integration

- **K1 — RP:** Michael Kohlhase and Florian Rabe, “A Scalable Module System,” *Information and Computation* 230, 2013, [DOI 10.1016/j.ic.2012.06.001](https://doi.org/10.1016/j.ic.2012.06.001).
- **K2 — RP/SPEC:** Michael Kohlhase, *OMDoc — An Open Markup Format for Mathematical Documents, Version 1.2*, 2006, [DOI 10.1007/11826095](https://doi.org/10.1007/11826095). This is a representation precedent, not a DTMKN correctness proof.
- **K3 — RP:** Stefano Ceri, Georg Gottlob, and Letizia Tanca, “What You Always Wanted to Know About Datalog (And Never Dared to Ask),” *IEEE TKDE* 1(1), 1989, [DOI 10.1109/69.43410](https://doi.org/10.1109/69.43410).
- **K4 — RP:** Johan de Kleer, “An Assumption-Based TMS,” *Artificial Intelligence* 28(2), 1986, [DOI 10.1016/0004-3702(86)90080-9](https://doi.org/10.1016/0004-3702%2886%2990080-9).
- **K5 — RP:** Max Willsey et al., “egg: Fast and Extensible Equality Saturation,” POPL 2021, [DOI 10.1145/3434304](https://doi.org/10.1145/3434304).
- **K6 — RP:** Jeff Johnson, Matthijs Douze, and Hervé Jégou, “Billion-Scale Similarity Search with GPUs,” *IEEE Transactions on Big Data*, 2019, [DOI 10.1109/TBDATA.2019.2921572](https://doi.org/10.1109/TBDATA.2019.2921572).
- **K7 — RP:** Yu. A. Malkov and D. A. Yashunin, “Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs,” *IEEE TPAMI*, 2020, [DOI 10.1109/TPAMI.2018.2889473](https://doi.org/10.1109/TPAMI.2018.2889473).
- **K8 — RP:** Burton H. Bloom, “Space/Time Trade-offs in Hash Coding with Allowable Errors,” *Communications of the ACM* 13(7), 1970, [DOI 10.1145/362686.362692](https://doi.org/10.1145/362686.362692).
- **K9 — STD:** W3C, [*PROV-O: The PROV Ontology*](https://www.w3.org/TR/prov-o/), W3C Recommendation, 2013.

### 16.3 Distributed systems

- **D1 — RP:** Marc Shapiro, Nuno Preguiça, Carlos Baquero, and Marek Zawirski, “Conflict-Free Replicated Data Types,” SSS 2011, [DOI 10.1007/978-3-642-24550-3_29](https://doi.org/10.1007/978-3-642-24550-3_29).
- **D2 — RP:** Alan Demers et al., “Epidemic Algorithms for Replicated Database Maintenance,” PODC 1987, [DOI 10.1145/41840.41841](https://doi.org/10.1145/41840.41841).
- **D3 — RP:** Petar Maymounkov and David Mazières, “Kademlia: A Peer-to-Peer Information System Based on the XOR Metric,” IPTPS 2002, [DOI 10.1007/3-540-45748-8_5](https://doi.org/10.1007/3-540-45748-8_5).
- **D4 — DOC/protocol specification:** libp2p, [Kademlia DHT specification](https://github.com/libp2p/specs/tree/master/kad-dht). Pin a commit before implementation; the paper's routing analysis does not automatically transfer to this code/protocol profile.
- **D5 — DOC/protocol specification:** libp2p, [Gossipsub specification](https://github.com/libp2p/specs/tree/master/pubsub/gossipsub). Peer scoring and gossip are routing mechanisms, not evidence semantics.
- **D6 — RP:** David Karger et al., “Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web,” STOC 1997, [DOI 10.1145/258533.258660](https://doi.org/10.1145/258533.258660).
- **D7 — RP:** Cary Gray and David Cheriton, “Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency,” SOSP 1989, [DOI 10.1145/74850.74870](https://doi.org/10.1145/74850.74870).
- **D8 — RP:** Abhinandan Das, Indranil Gupta, and Ashish Motivala, “SWIM: Scalable Weakly-Consistent Infection-Style Process Group Membership Protocol,” DSN 2002, [DOI 10.1109/DSN.2002.1028914](https://doi.org/10.1109/DSN.2002.1028914).
- **D9 — RP:** Seth Gilbert and Nancy Lynch, “Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services,” *SIGACT News* 33(2), 2002, [DOI 10.1145/564585.564601](https://doi.org/10.1145/564585.564601).
- **D10 — RP:** David Thaler and Chinya Ravishankar, “Using Name-Based Mappings to Increase Hit Rates,” *IEEE/ACM Transactions on Networking* 6(1), 1998, [DOI 10.1109/90.663936](https://doi.org/10.1109/90.663936). This is the highest-random-weight/rendezvous mapping precedent; it supplies placement, not authority.
- **D11 — DOC:** SQLite maintainers, [*Write-Ahead Logging*](https://www.sqlite.org/wal.html), [*PRAGMA synchronous*](https://www.sqlite.org/pragma.html#pragma_synchronous), and [*Atomic Commit in SQLite*](https://www.sqlite.org/atomiccommit.html). These documents state important VFS, filesystem, sync, and journal assumptions; DTMKN must pin a release/configuration and verify ledger invariants under crash/power-loss injection rather than infer durability from the word “transaction.”

### 16.4 Multi-agent scheduling

- **A1 — RP:** Barbara Hayes-Roth, “A Blackboard Architecture for Control,” *Artificial Intelligence* 26(3), 1985, [DOI 10.1016/0004-3702(85)90063-3](https://doi.org/10.1016/0004-3702%2885%2990063-3).
- **A2 — RP:** Reid G. Smith, “The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver,” *IEEE Transactions on Computers* C-29(12), 1980, [DOI 10.1109/TC.1980.1675516](https://doi.org/10.1109/TC.1980.1675516).
- **A3 — RP:** Robert D. Blumofe and Charles E. Leiserson, “Scheduling Multithreaded Computations by Work Stealing,” *JACM* 46(5), 1999, [DOI 10.1145/324133.324234](https://doi.org/10.1145/324133.324234). Its formal bounds have stronger assumptions than DTMKN's workload.
- **A4 — RP:** Kay Ousterhout et al., “Sparrow: Distributed, Low Latency Scheduling,” SOSP 2013, [DOI 10.1145/2517349.2522716](https://doi.org/10.1145/2517349.2522716).
- **A5 — RP:** Peter Auer, Nicolò Cesa-Bianchi, and Paul Fischer, “Finite-Time Analysis of the Multiarmed Bandit Problem,” *Machine Learning* 47, 2002, [DOI 10.1023/A:1013689704352](https://doi.org/10.1023/A:1013689704352).
- **A6 — RP:** Jeffrey Dean and Luiz André Barroso, “The Tail at Scale,” *Communications of the ACM* 56(2), 2013, [DOI 10.1145/2408776.2408794](https://doi.org/10.1145/2408776.2408794).
- **A7 — SPEC:** Juha Heinanen and Roch Guerin, [RFC 2697: *A Single Rate Three Color Marker*](https://www.rfc-editor.org/rfc/rfc2697), Informational RFC, 1999. DTMKN reuses token-bucket accounting, not the network-marking semantics wholesale.
- **A8 — RP:** M. Shreedhar and George Varghese, “Efficient Fair Queueing Using Deficit Round Robin,” SIGCOMM 1995, [DOI 10.1145/217382.217453](https://doi.org/10.1145/217382.217453). DTMKN applies the fair-share idea to finite receiver-owned service/capability classes; scientific priorities remain local policy.

### 16.5 Encoding, transport security, and capabilities

- **S1 — STD:** Carsten Bormann and Paul Hoffman, [RFC 8949: *Concise Binary Object Representation (CBOR)*](https://www.rfc-editor.org/rfc/rfc8949), 2020, especially deterministic encoding considerations. DTMKN still needs a narrower frozen profile.
- **S2 — STD:** NIST, [FIPS PUB 180-4: *Secure Hash Standard*](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), 2015. Algorithm agility remains necessary; this source does not define DTMKN object semantics.
- **S3 — SPEC:** Open Container Initiative, [OCI Image Format Specification](https://github.com/opencontainers/image-spec). Pin the exact release/commit used.
- **S4 — SPEC:** Open Container Initiative, [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec). This is transport interoperability, not archival availability or safety.
- **S5 — STD:** Eric Rescorla, [RFC 8446: *The Transport Layer Security (TLS) Protocol Version 1.3*](https://www.rfc-editor.org/rfc/rfc8446), 2018.
- **S6 — SPEC:** Simon Josefsson and Ilari Liusvaara, [RFC 8032: *Edwards-Curve Digital Signature Algorithm (EdDSA)*](https://www.rfc-editor.org/rfc/rfc8032), Informational RFC, 2017.
- **S7 — STD:** Jim Schaad, [RFC 9052: *CBOR Object Signing and Encryption (COSE): Structures and Process*](https://www.rfc-editor.org/rfc/rfc9052), 2022.
- **S8 — SPEC:** Henk Birkholz et al., [RFC 9334: *Remote ATtestation procedureS (RATS) Architecture*](https://www.rfc-editor.org/rfc/rfc9334), Informational RFC, 2023. It supplies an attester/verifier/endorser architecture, not assurance that any evidence, hardware, appraisal policy, or mathematical payload is correct.
- **Q1 — RP:** Arnar Birgisson et al., “Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud,” NDSS 2014, [DOI 10.14722/ndss.2014.23212](https://doi.org/10.14722/ndss.2014.23212).
- **Q2 — RP:** John R. Douceur, “The Sybil Attack,” IPTPS 2002, [DOI 10.1007/3-540-45748-8_24](https://doi.org/10.1007/3-540-45748-8_24).

### 16.6 Succinct and authenticated computation

- **C2 — RP:** Ralph C. Merkle, “A Digital Signature Based on a Conventional Encryption Function,” CRYPTO 1987, [DOI 10.1007/3-540-48184-2_32](https://doi.org/10.1007/3-540-48184-2_32).
- **C3 — RP:** Jens Groth, “On the Size of Pairing-Based Non-interactive Arguments,” EUROCRYPT 2016, [DOI 10.1007/978-3-662-49896-5_11](https://doi.org/10.1007/978-3-662-49896-5_11).
- **C4 — RP:** Evan Laufer, Alex Ozdemir, and Dan Boneh, “zkPi: Proving Lean Theorems in Zero-Knowledge,” CCS 2024, [DOI 10.1145/3658644.3670322](https://doi.org/10.1145/3658644.3670322). This is feasibility evidence for a selected construction, not a DTMKN performance or full-coverage result.
- **C5 — RP:** Nir Bitansky, Ran Canetti, Alessandro Chiesa, and Eran Tromer, “Recursive Composition and Bootstrapping for SNARKs and Proof-Carrying Data,” STOC 2013, [DOI 10.1145/2488608.2488623](https://doi.org/10.1145/2488608.2488623).
- **C6 — RP manuscript:** Eli Ben-Sasson et al., “Scalable, Transparent, and Post-Quantum Secure Computational Integrity,” IACR ePrint 2018/046, [primary manuscript](https://eprint.iacr.org/2018/046). Treat exact assumptions and version as part of any later evaluation.
- **C7 — RP:** Abhiram Kothapalli, Srinath Setty, and Ioanna Tzialla, “Nova: Recursive Zero-Knowledge Arguments from Folding Schemes,” CRYPTO 2022, [DOI 10.1007/978-3-031-15985-5_13](https://doi.org/10.1007/978-3-031-15985-5_13).
- **C8 — RP manuscript:** Ning Luo, Timos Antonopoulos, William Harris, Ruzica Piskac, Eran Tromer, and Xiao Wang, “Proving UNSAT in Zero Knowledge,” IACR ePrint 2022/206, [primary manuscript](https://eprint.iacr.org/2022/206). It is a domain feasibility precedent, not an implementation selection.
- **C9 — DOC:** RISC Zero maintainers, [zkVM documentation](https://dev.risczero.com/api/zkvm/). This mutable documentation is listed only to identify a possible benchmark family; a future experiment must pin and audit an exact version.

### 16.7 Consensus and transparency

- **B1 — SPEC:** Satoshi Nakamoto, [*Bitcoin: A Peer-to-Peer Electronic Cash System*](https://bitcoin.org/bitcoin.pdf), 2008. It is treated here as a protocol proposal, not a peer-reviewed theorem-validation source.
- **B2 — RP:** Miguel Castro and Barbara Liskov, [“Practical Byzantine Fault Tolerance”](https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance), OSDI 1999.
- **B3 — RP:** Diego Ongaro and John Ousterhout, [“In Search of an Understandable Consensus Algorithm”](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro), USENIX ATC 2014.
- **B4 — RP:** Maofan Yin et al., “HotStuff: BFT Consensus with Linearity and Responsiveness,” PODC 2019, [DOI 10.1145/3293611.3331591](https://doi.org/10.1145/3293611.3331591).
- **B5 — STD:** Henk Birkholz et al., [RFC 9943: *An Architecture for Trustworthy and Transparent Digital Supply Chains*](https://www.rfc-editor.org/rfc/rfc9943), June 2026. The cited claim is limited to the architecture defined in the official RFC Editor publication.
- **B6 — STD:** Orie Steele et al., [RFC 9942: *CBOR Object Signing and Encryption (COSE) Receipts*](https://www.rfc-editor.org/rfc/rfc9942), June 2026. The cited claim is limited to receipt/VDS syntax and semantics in the official publication.
- **B7 — SPEC:** Ben Laurie, Emilia Messeri, and Rob Stradling, [RFC 9162: *Certificate Transparency Version 2.0*](https://www.rfc-editor.org/rfc/rfc9162), Experimental RFC, 2021.
- **B8 — RP:** Michael Fischer, Nancy Lynch, and Michael Paterson, “Impossibility of Distributed Consensus with One Faulty Process,” *JACM* 32(2), 1985, [DOI 10.1145/3149.214121](https://doi.org/10.1145/3149.214121). It motivates explicit timing/fairness assumptions; it does not prohibit DTMKN's local monotone progress model.

### 16.8 Sandboxing

- **X1 — DOC:** Linux kernel maintainers, [*Control Group v2*](https://docs.kernel.org/admin-guide/cgroup-v2.html). Pin the worker kernel/runtime and test enforcement; documentation is not a proof of isolation.
- **X2 — DOC:** Linux kernel maintainers, [*Seccomp BPF*](https://docs.kernel.org/userspace-api/seccomp_filter.html). The documentation explicitly describes attack-surface reduction; DTMKN must not treat seccomp alone as a complete sandbox.
- **X3 — SPEC:** W3C WebAssembly Community Group, [*WebAssembly Core Specification 2.0*](https://www.w3.org/TR/wasm-core-2/), Candidate Recommendation Draft at the cited URL. Host capabilities and the runtime remain separate trust boundaries.
- **X4 — DOC:** Wasmtime maintainers, [*Wasmtime Security*](https://docs.wasmtime.dev/security.html). Exact runtime version and configuration must be pinned and independently tested.
- **X5 — RP:** Alexandru Agache et al., [“Firecracker: Lightweight Virtualization for Serverless Applications”](https://www.usenix.org/conference/nsdi20/presentation/agache), NSDI 2020. Its measurements and design do not prove absence of vulnerabilities.

### 16.9 Formal/model-based protocol analysis and testing

- **V1 — RP/DOC:** Leslie Lamport, “The Temporal Logic of Actions,” *ACM TOPLAS* 16(3), 1994, [DOI 10.1145/177492.177726](https://doi.org/10.1145/177492.177726), and the [TLA+ project](https://lamport.azurewebsites.net/tla/tla.html).
- **V2 — RP/DOC:** Igor Konnov, Markus Kuppe, and Stephan Merz, “Specification and Verification with the TLA+ Trifecta: TLC, Apalache, and TLAPS,” 2022, [DOI 10.1007/978-3-031-19849-6_6](https://doi.org/10.1007/978-3-031-19849-6_6), plus [Apalache documentation](https://apalache-mc.org/docs/). This source supports tool selection, not completeness for every TLA+ model.
- **V3 — RP:** Daniel Jackson, “Alloy: A Lightweight Object Modelling Notation,” *ACM TOSEM* 11(2), 2002, [DOI 10.1145/505145.505149](https://doi.org/10.1145/505145.505149).
- **V4 — RP:** Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin, “The TAMARIN Prover for the Symbolic Analysis of Security Protocols,” CAV 2013, [DOI 10.1007/978-3-642-39799-8_48](https://doi.org/10.1007/978-3-642-39799-8_48).
- **V5 — RP:** Koen Claessen and John Hughes, “QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs,” ICFP 2000, [DOI 10.1145/351240.351266](https://doi.org/10.1145/351240.351266).
- **V6 — DOC:** LLVM project, [*libFuzzer — a Library for Coverage-Guided Fuzz Testing*](https://llvm.org/docs/LibFuzzer.html). Pin toolchain/sanitizer versions and retain minimized artifacts.
- **V7 — RP:** Jingyu Zhou et al., “FoundationDB: A Distributed Unbundled Transactional Key Value Store,” SIGMOD 2021, [DOI 10.1145/3448016.3457559](https://doi.org/10.1145/3448016.3457559). DTMKN cites its simulation-testing precedent, not its database semantics as the network architecture.

### 16.10 Internal normative references

- **INT1 — INT:** [DTMKN Cooperation Core v0](../spec/COOPERATION-CORE-v0.md).
- **INT2 — INT:** [DTMKN Cooperative Research Testbed v0](COOPERATION-TESTBED.md).
- **INT3 — INT:** [SNARK and succinct-verification assessment](SNARK-ASSESSMENT.md).
- **INT4 — INT:** [Trustworthy cooperation model](../security/TRUSTWORTHY-COOPERATION.md).

## 17. Open uncertainties and required audits

These are not editorial footnotes; each limits the claims the first artifact may make.

1. **Lean export boundary.** It is not yet demonstrated which source, elaborated expression, proof-term, `.olean`, compiler, plugin, and option fields are necessary and sufficient for portable replay. Run boundary-mutation experiments before freezing `GoalKey`, environment roots, or proof bundles.
2. **Canonical encoding.** RFC 8949 permits choices; DTMKN still needs a narrow profile. Two independent encoders, duplicate-key rejection, Unicode policy, floating-point exclusion or normalization, and cross-language golden vectors are unresolved engineering work.
3. **Signed support trees and dirty repair.** The signed \(K_P\), projected \(D_P/R_P\), and \(U_P^{\mathrm{strict}}\) semantics prevent polarity and bare-judgment leakage, but witness extraction and incremental behavior under high-fanout dirty roots, multiple policies, missing objects, epoch changes, and resumable invalidation need complexity analysis and differential testing. Old-epoch queries fail closed.
4. **Replica convergence versus inter-cell admission.** Direct set union is safe only inside one non-Byzantine logical admission authority with a nonsplit-brain ledger or disjoint writable escrow. Independently operated cells re-admit candidates even with equal authenticated policy roots. Multiwriter crash replication needs Raft/escrow; Byzantine replication needs a separate BFT model.
5. **Formalization fidelity and reviewer authority.** A fidelity contract exposes rather than eliminates semantic judgment. The corpus must measure detection of wrong, vacuous, or assumption-strengthened formalizations, and every nonmechanical result must name a scoped operational reviewer/authority without turning prestige into proof.
6. **Cross-theory transport.** MMT/OMDoc provide representation precedents, but the exact Lean symbol-map, coercion, universe, typeclass, quotient, and axiom boundaries remain work. Minimum v0 therefore uses only manually supplied in-environment relations with target-side replay; general morphisms are deferred.
7. **Failure certificates.** `CERTIFIED_EXHAUSTION` is meaningful only for an explicitly finite or otherwise certifiable search region. Most failed attempts remain hints; general exhaustion/containment is deferred from the minimum slice.
8. **Scheduling nonstationarity.** Agent capabilities, versions, queues, and task distributions drift. The minimum contract uses fixed hard predicates, rendezvous homes, finite receiver classes, service floors, protected validation capacity, and bounded exploration; pull/WFQ/DRR/aging are frozen test treatments rather than conformance requirements. Learned scheduling waits for frozen traces and out-of-sample evaluation.
9. **Diversity evidence.** Endpoint, operator, model name, or signature does not prove independent errors. The achievable failure-domain taxonomy and common-mode-error detection rate need seeded experiments.
10. **Demand redemption policy and implementation.** Claimed/metered demand objects contain valid-tautology floods but can overcentralize curation or starve rare work. Multi-redemption, audience binding, same-reservation claims, metering integrity/gaps, unclaimed cancellation, bounded crash-safe execution expiry, zero-work descendant issuance, terminal resurrection, and every issue/reserve/claim/meter/check/inert-staging/local-finalization/outbox/external-effect/terminal crash point need tests. Atomic reliance-state/dirty-seed/epoch publication needs its own crash matrix. Measure rare-domain service, exploration abuse, grant-authority concentration, and ticket overhead.
11. **Public discovery boundary.** The primary real federation is exactly five configured authenticated independent cells with rendezvous home fanout \(r=2\); three cells are only a smoke test. It is not Kademlia. A later public DHT must separately address membership, Sybil/eclipse attacks, poisoned providers, and resource admission.
12. **Permission capability and demand-ledger boundary.** Caveats restrict scope but cannot conserve work resources. Capabilities therefore carry permission, exact execution caveats, nonreclaimable fanout, and a finite nonreclaimable control-record allowance; they carry no mathematical-work vector. The separate issuer-local grant/ticket/reservation/claim/meter ledger needs atomic root/child work/count allocation, unique execution, per-component receiver-authoritative/conservative local finalization with inert staging and nonauthorizing outbox intents, separately funded external effects, irreversible terminal state, stored digest equality, crash-safe bounded expiry/revocation rules, and recovery. The autonomous primary profile uses independent issuer-local grants. Only an optional coordinated program may freeze nonoverlapping escrow slices whose componentwise sum equals its explicit shared envelope; dynamic cross-cell transfer remains deferred unless a separate narrow consensus protocol is specified.
13. **Sandbox TCB.** Process, Wasm, and microVM layers have different gaps. The exact host OS, runtime, syscall policy, filesystem mediation, side-channel scope, and supply-chain assumptions must be recorded. A container digest is not sufficient.
14. **Data availability and retention.** CIDs, signatures, Merkle roots, receipts, and SNARKs bind or attest data but do not retain native artifacts. Replication/archival guarantees and garbage-collection rules are not yet specified for a global deployment.
15. **Succinct economics and relation fidelity.** No current measurement shows that Lean replay fanout crosses the SNARK break-even threshold. Circuit/VM equivalence to native checking, setup, upgrades, prover bottlenecks, and opaque-witness effects remain open.
16. **Recent transparency standards.** RFC 9942 and RFC 9943 are official June 2026 RFC Editor publications, but this document makes no claim about implementation maturity, interoperability experience, deployment, or fitness for DTMKN. They remain deferred.
17. **Simulation validity.** A \(10^6\)-logical-agent stretch run generated from an inaccurate distribution proves little. Calibrate \(10^3\)–\(10^5\) runs against held-out real traces, publish sensitivity ranges, and state where simulation and deployment diverge.
18. **External validity.** A 30–50-task, roughly 100–200-internal-work-item Lean corpus cannot establish universal mathematics acceleration. The initial claims are restricted to the harness-side tasks, held-out reuse, budgets, and injected faults.
19. **Validation taxonomy conformance.** Adapters may naturally conflate an invalid artifact, declared incompleteness, and infrastructure failure. Mutation, timeout/fuel/memory, missing-closure, checker-crash, sandbox-failure, and corrupt-runtime fixtures must show consistent `REJECT`/`UNKNOWN`/`ERROR` behavior and debit settlement.
20. **Override and reliance-version resolution.** Acyclic explicit supersession plus the pending state for missing named predecessors makes delivery-order independence well-defined, but authorization conflicts, policy-epoch rollover, garbage collection of superseded facts, scalable exact current-tree freshness checks, and linearizable final epoch reads remain implementation work.
21. **Source/version drift.** DOC-class references such as Lean, libp2p, OCI, Wasmtime, Linux, and RISC Zero are mutable. Before implementation, record release/commit, source hash, license, configuration, known limitations, and local test result. No 2025–2026 software-performance claim is made here.
22. **Publication and interest abuse.** Bounded hints enable autonomous discovery but add key-grinding, hot-key, provider-withholding, scope/topic spam, and evaluation-leakage surfaces. Freeze hint/key/provider/TTL quotas, receiver-only service-class creation, lazy-fetch rules, and protocol-projection noninterference tests.
23. **Coordination value.** Decomposition, remote assignment, leases, work stealing, hedging, and shared programs may cost more than they save. Implement them as separable active-minus-passive treatments and publish the full overhead vector; activity counts do not establish value.

## 18. Final reuse rule

A mechanism enters the stable P0 path only if the following review can be answered precisely:

1. What typed input and output relation does it implement?
2. Which P0 property does it support?
3. What assumptions and trusted components are added?
4. Can a failure create invalid mathematical support, or only lost/delayed work?
5. What local check prevents remote error from becoming stable state?
6. What resource bound prevents amplification?
7. What model, conformance vector, mutation test, or fault test covers the claim?
8. What simpler mechanism is the baseline?

If these answers are unavailable, the mechanism remains advisory or deferred. In particular, decentralization, cryptographic sophistication, agent count, and publication prestige are not substitutes for a narrow checkable relation and a receiver-local admission rule.
