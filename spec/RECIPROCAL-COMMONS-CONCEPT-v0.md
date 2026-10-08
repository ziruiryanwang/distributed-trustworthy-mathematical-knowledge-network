# Reciprocal Mathematical Commons: formal concept v0

Date: 2026-09-19  
Companion checkpoint: [CP-001C](../notes/checkpoints/CP-001C-reciprocal-mathematical-commons.md)  
Status: Reviewed proposed concept contract and paper proof obligations; see the [audit disposition](../notes/audits/CP-001C-AUDIT-DISPOSITION.md)  
Implementation status: No code, executable protocol, model-checking program, or experiment is introduced here

## Version-one scope and precedence

The [formal knowledge contract](FORMAL-KNOWLEDGE-CONTRACT-v0.md) specializes this broader concept for the user's final v1 scope: **no human intention and no list of unsolved mathematics tasks**. Independent investigators interact with a checked mathematical corpus; the protocol does not manage their research. Formal artifacts need no originating work item or registered question.

References below to semantic-intent review, task orchestration, unfinished-work records, and task-based experiments describe broader or historical possibilities, not v1 requirements. V1 enables neither informal-intent assessments nor a research-task registry. Operational checking/transfer/repair jobs remain resource-accounted without being mathematical research tasks.

## Specification intent

The system should let independently operated agents use earlier mathematical work as reliable input, create further useful work, and return portable artifacts that other agents can use in the same way. It should remain operational without a mandatory central server or universally privileged publisher.

This specification separates three kinds of statement:

- **Requirement:** a behavior an eventual implementation must provide under its declared profile.
- **Conditional proposition:** a mathematical implication with explicit assumptions and a paper proof sketch.
- **Hypothesis:** a claim about productivity, scaling, adoption, or economics that requires evidence.

“Must” specifies a proposed conformance requirement; it does not report an existing implementation. No paper proof below establishes that an unbuilt implementation satisfies its premises.

The preceding [Cooperation Core](COOPERATION-CORE-v0.md), [CP-001A](../notes/checkpoints/CP-001A-autonomy-first-cooperation.md), and [CP-001B](../notes/checkpoints/CP-001B-distributed-corpus-and-global-status.md) retain their exact acceptance and resource-accounting constraints. The present document adds a product contract, a reciprocal composition contract, and a long-term open-network profile.

## Product semantics: one commons, many physical and logical views

Let \(\mathcal O\) be the universe of canonically encoded typed artifacts. Let \(I(t)\) denote participants for mathematical analysis; this notation does not imply that a live node possesses a global roster.

Three collections must be distinguished:

\[
\mathcal P(t)=\bigcup_{i\in I(t)}\operatorname{Published}_i(t),
\qquad
\mathcal R_{\Phi}(t)\subseteq\mathcal P(t),
\qquad
\mathcal K_{i,P}(t).
\]

\(\mathcal P(t)\) is a notional union of published artifact identities. \(\mathcal R_\Phi(t)\) is the part recoverable under a declared retention/failure profile \(\Phi\). \(\mathcal K_{i,P}(t)\) is receiver \(i\)'s usable mathematical view under policy \(P\), available closures, admitted facts, and query contracts. No general equality among these collections is claimed.

Separately, \(\mathcal V_i(t)\) records exact locally verified formal results with their statements, hypotheses, environments, checking bases, and assessment snapshots. Recognition in this collection is not conditional on satisfying an originating research task or human intention. Historical verification, current allowed reliance, availability, retention, and usefulness are separate fields. V1's machine checking contract concerns the submitted formal artifact itself, not a requested research outcome.

“The software represents mathematics” means:

- the software understands documented artifact formats and their verification relations;
- a node can acquire a dependency-complete useful snapshot;
- participants can extend the object space through versioned formats and checker adapters;
- the distributed corpus can connect multiple areas and foundations through explicit interfaces;
- no domain is excluded merely because it lacks a central institutional sponsor.

It does not mean that a finite download contains all mathematical truth. An effectively axiomatized theory may have an enumerable theorem set, yet theoremhood or semantic truth need not be decidable. Enumeration alone does not provide efficient retrieval, short proofs, useful abstractions, or faithful formalization.

## Profiles and their precedence

| Profile | Membership | What it establishes | What it cannot establish by itself |
|---|---|---|---|
| Offline node | One local operator | Local package checking, research, and export | Current remote incidents or network discovery |
| Fixed experimental federation | Prior planned five authenticated cells | Controlled reuse, accounting, partition, and comparison studies | Open-network Sybil/eclipse resilience |
| Voluntary overlay | A named roster or locally chosen membership rule | Scoped discovery, archives, or service agreements | Authority over unrelated nodes |
| Open commons | Anyone can instantiate a node and self-host objects | No mandatory global enrollment or operator | Guaranteed attention, bandwidth, or retention from strangers |

The open commons is the end-state product requirement. The experimental federation remains useful evidence about particular mechanisms. Passing the federation profile does not imply conformance to the open profile.

The open profile must not import a global membership epoch from the experimental profile. Epochs, logs, rosters, and quorum rules are namespaced to the authority or overlay that actually owns them.

## Assumption ledger

Every advertised guarantee names its applicable assumptions.

| Tag | Assumption |
|---|---|
| A-ENC | Canonical encodings are injective for the declared typed representation, and parsers enforce size/depth limits |
| A-HASH | The selected hash profile resists collisions and substitution within the stated security horizon |
| A-AUTH | When a contract authenticates an operational principal or reviewer, its signature/capability mechanism is secure, its authorized keys are uncompromised, and scope, expiry, and revocation rules are enforced |
| A-CHECK | The local kernel or certificate checker and its execution environment implement the declared derivability relation |
| A-POLICY | Local contract, hypothesis-footprint, fidelity, and active-evidence evaluators implement their declared rules |
| A-STATE | Local authoritative state publication and resource accounting satisfy their crash/atomicity model |
| A-ISOLATE | Untrusted models, artifacts, tactics, plugins, and network peers cannot bypass the local service boundary |
| A-LOGIC | When a semantic truth claim is made, the specified interpretation satisfies the admitted axioms and inference rules |
| A-PATH | A relevant object has an eventually reachable, honest, willing dissemination path |
| A-SERVICE | Matching admitted jobs receive sufficient fair service and complete within declared bounds |
| A-RETAIN | Required bytes or fragments survive and can be reconstructed under the declared failure and repair model |
| A-FRESH | Claimed observation coverage is checked against specific committed records and an explicit freshness basis |

Safety against malicious remote publishers uses A-ENC through A-ISOLATE and the exact evidence rules; A-AUTH applies wherever authenticated authority is a premise, not as a substitute for proof checking. Liveness also requires A-PATH, A-SERVICE, and A-RETAIN. Semantic truth requires A-LOGIC in addition to successful formal checking. A-FRESH never certifies private or uncommitted remote information.

Independence of operators, implementations, hardware, models, or archives is a measured or expressly assumed failure-domain property. Several public keys do not establish it.

## Mathematical identities and interfaces

### Exact identity

For a canonical object \(o\), its content identifier has the conceptual form

\[
\operatorname{CID}(o)=
H(\operatorname{domain}\Vert\operatorname{schemaVersion}
\Vert\operatorname{canonical}(o)).
\]

Canonical encoding, domain separation, and hash algorithm identifiers must be explicit. An object identity binds the statement, proof representation or manifest, exact environment references, and semantically relevant options defined by its schema.

Exact-byte identity is distinct from:

- equality after elaboration;
- definitional equality;
- provable equivalence;
- specialization;
- analogy or textual similarity;
- conceptual usefulness for a particular task.

Each relation needs its own type and evidence. An embedding or model judgment may propose any of them but cannot establish a logical relation.

### Foundation and environment

A mathematical environment \(E\) specifies its logic, admitted axioms, declarations, universes, relevant elaboration options, library versions, and native checking basis.

The basic formal judgment is

\[
E;\Gamma\vdash p:\varphi.
\]

Here \(\Gamma\) contains explicit local hypotheses; \(p\) is native evidence for \(\varphi\). The hypothesis and axiom footprint includes transitive dependencies. A theorem imported as a newly trusted axiom does not satisfy the replay contract merely because its source file compiles.

Adding theorem derivations and conservative definitions is different from adding assumptions. A conservative definitional extension may preserve prior judgments when the foundation's extension rules justify it. An arbitrary library or axiom union is not automatically conservative.

For example, one independently consistent theory can assert a new proposition \(P\), and another can assert \(\neg P\); their union can be inconsistent. Therefore the network cannot merge axiom sets simply because each package has passed a checker in its own theory.

### Interface contract

A reusable mathematical interface specifies:

- parameters and their exact types;
- hypotheses and structure requirements;
- exported judgments;
- available construction or proof evidence;
- permissible instantiations and substitution rules;
- dependency and foundation requirements;
- exact formal endpoint and binding obligations; informal-intent obligations are outside v1;
- size and checking-cost bounds needed for admission.

The interface is the mathematical boundary between two independently developed projects. Portable byte storage supports the boundary but does not replace it.

### Evidence polarity and identity signatures

The existing Core uses a signed judgment \((\sigma,x)\), where \(\sigma\) is `SUPPORTS` or `REFUTES`. “Signed” here denotes logical polarity. It must not be confused with an author's cryptographic signature.

Proof acceptance need not depend on the author's identity. Cryptographic signatures authenticate operational offers, checkpoint histories, retention promises, or scoped reviewer actions where a principal is necessary. They do not prove the mathematical assertion.

## Contribution types and their permitted use

| Kind | Minimum contents | Permitted reliance |
|---|---|---|
| Checked theorem | Exact statement, hypotheses, native evidence, closure, environment | Mathematical premise after local contract validation |
| Checked counterexample | Exact universal claim, witness, and checked witness conditions | Refutation of that exact claim under its stated assumptions |
| Definition or abstraction | Formal declaration, extension rules, invariants or constructions | New vocabulary with the declared foundation and obligations |
| Specialization or bridge | Exact source/target interfaces, mapping, conditions, target-side evidence | Transfer only through the checked relation |
| Conditional partial | Checked partial result and explicit unsolved premises | Conditional information; cannot discharge unproved premises |
| Search failure | Exact search region, procedure, inputs, resource bounds, outcome | Heuristic avoidance only, unless certified exhaustion proves a specific negative |
| Method or tactic | Versioned strategy and bounded execution interface | Untrusted procedure that must produce checked evidence |
| Informal explanation | Text, associated formal artifacts, fidelity basis | Human/model guidance at its declared evidence grade |
| Retention or service record | Authority, exact object/service scope, budgets, expiry, evidence of service | Operational information, not theorem truth |

A tactic does not gain arbitrary host privileges because its outputs are sometimes valid. Dependency fetch does not imply permission to execute a package's build scripts. Implementations must separate inert mathematical data from untrusted executable tools.

The commons can help by avoiding repeated failed work, improving explanations, or repairing definitions without producing a new theorem. Those contributions have different contracts and success measures.

## Two export contracts

### Public reusable package

A public reusable package makes its declared native proof or certificate closure obtainable under its retention terms. It contains an exact manifest for statements, evidence, dependencies, environment, interfaces, and evidence metadata.

The declared native replay procedure must be closed over its supplied immutable closure and explicit local snapshot. It must make no mandatory live callback, even a bounded one, to a publisher, index, model service, or other remote authority. It must not require undocumented producer-local paths, secrets, credentials, mutable imports, or an unavailable private elaborator. If a proprietary tool is essential, the package must disclose that dependency and cannot claim the strongest open replay profile.

Acquiring missing closure is a separate fetch operation. Obtaining newer incident or freshness observations is also separate: offline native replay does not guarantee current strict reliance under a policy that requires unavailable external observations.

A finite theorem closure may be large. Shared chunks and cached foundations reduce cost. “Self-contained” means all required immutable references can be resolved from the supplied or declared archive closure, not that each package duplicates the complete library.

### Proposal or opaque package

The network may transport proposals, summaries, or succinct opaque evidence under explicit types. Such objects cannot silently inherit `PUBLIC_REUSABLE` status.

For strict P0, native local replay or the already admitted domain-certificate basis remains required. A future succinct-proof contract may establish a precisely bound verifier relation under cryptographic assumptions, but it does not make native evidence available or establish informal intent.

## The reciprocal state machine

This is an abstract transition contract, not executable pseudocode. Refining it must preserve the existing grant/ticket/reservation/unique-claim/meter/finalization rules for protected service work. Choose-local-work and derive transitions below describe independent clients, not mandatory v1 server research orchestration. V1's corpus lifecycle is specified in the formal knowledge contract.

For node \(i\), write

\[
S_i=(O_i,A_i,P_i,e_i,W_i,D_i,F_i,B_i,R_i).
\]

\(O_i\) is available admitted object closure; \(A_i\) is admitted evidence, defect, override, and availability facts; \(P_i\) is policy; \(e_i\) is the local reliance epoch; \(W_i\) is local work; \(D_i\) is advisory discovery state; \(F_i\) is scoped observation state; \(B_i\) is authoritative resource state; \(R_i\) is receiver-authorized retention state.

Raw ingress and quarantine are separately bounded and have no reliance authority. Finite control bookkeeping is charged even for unsuccessful publication, validation, or repair.

| Transition | Guard | Effect and authority boundary |
|---|---|---|
| Choose local work | Locally authorized task and resources | Creates \(W_i\); needs no global root goal or permission |
| Observe hint | Bounded schema/ingress checks and local hint quota | Changes advisory \(D_i\) only |
| Select import | Local relevance and service policy | Creates receiver-funded work authority; foreign priority is not imported |
| Fetch and inspect | Unique live metered execution and hard bounds | Stages inert CID-checked closure; staging is not acceptance |
| Validate formal content | Exact checker, environment, submitted judgment, and closure available | Records `ACCEPT`, `REJECT`, `UNKNOWN`, or `ERROR` for the exact validation key, independently of task history |
| Admit | Validation and full receiver contract permit promotion | Atomically commits local facts, authorized retained references, settlement, and necessary reliance-epoch changes |
| Use | Current finite active tree satisfies the exact query | Supplies a premise/interface plus its context to local work |
| Derive | Local attempt under explicit premises and budget | Produces a candidate; derivation attempts are fallible |
| Package | Exact export closure, interface, assumptions, and unresolved obligations identified | Produces a portable candidate package; it is not yet a remote acceptance |
| Advertise | Local publication policy and bounded service authority | Publishes a hint through willing paths; does not allocate a receiver's resources |
| Re-admit remotely | Independent receiver selects, fetches, and checks | Creates that receiver's local facts, never inherited publisher authority |
| Reuse downstream | Independent local query and current validated application | Produces a new checked outcome; later packaging repeats the cycle |
| Admit defect | Locally checked defect, opposing evidence, or authorized policy event | Atomically changes facts, conservative dirty seeds, and epoch; stale affected use fails closed |
| Renew or release storage | Receiver-local authority and capacity accounting | Changes retention/availability; no theorem becomes false solely because bytes expire |

Actual external index writes, replication, notifications, repair, and later audits require separate funded executions after nonauthorizing outbox intents. Neither local promotion nor a publication receipt asserts that an external effect has completed.

## Local reliance, formal truth, and correction

Current strict reliance is still defined by

\[
\operatorname{Rely}_i(q,e)
\Longrightarrow
\operatorname{Stable}_{P_i(e)}(q;A_i(e),O_i(e)).
\]

The right side requires an exact finite active signed evidence tree, full path-dependent contract checks, exact context, and available closure. In v1, semantic-intent/fidelity references are absent and create no reviewer obligation; the contract binds the submitted mathematical judgment. A model's confidence, popularity, token balance, foreign acceptance, or number of signatures cannot replace those premises.

A status response separates:

- raw support/refutation state;
- strict query-relative reliance;
- each selected native validation outcome;
- closure availability;
- local snapshot/epoch;
- scoped checkpoint coverage and freshness basis.

All fields and page cursors bind one snapshot. A current `ACCEPT` requires the unchanged-epoch check immediately before response emission. A challenge received after that response does not retroactively make the earlier response current under later knowledge.

A theorem proved correctly from fixed axioms does not become logically false because an author retracts it or its file disappears. Corrections may concern a buggy checker, corrupted evidence, wrong intended statement, hidden assumption, missing closure, or a local trust policy. These change justified reliance in different ways.

If sound checking establishes closed derivations of both \(\varphi\) and \(\neg\varphi\) in the same consistent classical theory, or derives both under the same jointly consistent exact context, at least one claimed premise about the checker, theory/context consistency, exact binding, or certificate must fail. Consistency of \(E\) alone is insufficient: the context \(\Gamma=\{P,\neg P\}\) allows both judgments to check without a checker defect. The system's `BOTH` state is a conflict-management mechanism, not a claim that classical contradiction has become harmless.

## Compositional reciprocity contract

Suppose a producer exports \(p\) with

\[
E;\Gamma\vdash p:\varphi,
\]

and a consumer wants to use it in \(E';\Delta\).

The consumer must provide either an exact compatible import or a checked transport whose conditions are satisfied. For a translation \(\tau\), the necessary relation is

\[
\operatorname{CheckTransport}(E,\Gamma,\varphi,E',\Delta,\tau,w)
=\texttt{ACCEPT},
\]

where \(w\) establishes the specific target judgment

\[
E';\Delta\vdash p':\tau(\varphi).
\]

This is not an assumption that arbitrary translations are computable or sound. For current strict reuse, target-native replay or an already admitted target-domain certificate is required for the actual translated statement and evidence. A general soundness theorem for a translator may later reduce repeated work only under an explicitly versioned contract.

Target derivability alone does not establish faithful transport of the source interface: a mapping sending every proposition to `True` would make target checking easy while discarding the intended content. A claimed transport must additionally check parameter typing, substitution and source-hypothesis discharge or explicit retention, the stated source-to-target interpretation contract, and exact agreement with the consumer's intended target interface. Nonmechanical assessments of informal intent retain their declared review grade; a native proof cannot upgrade them to formal equivalence.

Hypotheses cannot disappear under renaming. A theorem about all groups cannot be applied to a structure shown only to be a monoid when the proof uses inverses. A theorem over a field cannot be applied to every ring merely because the notation matches. A proof found in a stronger axiom system cannot meet a weaker consumer contract without new justification.

### Conditional proposition: finite composition safety

Assume A-ENC, A-HASH, A-CHECK, and A-POLICY. Let \(T\) be a finite formal derivation subtree of an admitted Core evidence tree, in which every leaf passes its native evidence contract, every internal node passes the declared inference or faithful transport contract, and the root query checks the accumulated environment and hypothesis footprint. A formal refutation node is interpreted through its declared refutation relation and is not automatically a proof of syntactic negation.

Then the root is derivable in the exact declared target theory. If A-LOGIC additionally holds, its corresponding interpretation is true under the declared hypotheses.

Proof sketch: structural induction on \(T\). Leaves satisfy the native relation. Each internal node consumes precisely its checked child judgments and applies a sound declared rule or witnessed transport. The root therefore satisfies the target relation. Exact references prevent substituting a different leaf; the footprint check prevents a forbidden premise from being hidden in a child.

Scope: this proves a mathematical implication about the formal subtree, not every operational or semantic-review judgment in a Core evidence tree. Nonmechanical fidelity assessments retain their reviewed grade. It does not establish that a particular checker binary is sound, that a theory is consistent, that the informal question was encoded correctly, or that the result is useful.

### Conditional proposition: no reputation laundering

Replace any producer identities, review counts, model confidences, network popularity, or publication venues while preserving exact artifacts, contracts, and authorized operational roles. If mathematical acceptance has no other dependency on those values, strict native acceptance is unchanged.

Exceptions must be explicit fidelity or service contracts that actually name reviewer or operational authorities. Political credit must not be smuggled into a native proof-validity predicate.

### Conditional proposition: no circular support

Under Core v0's least-fixed-point support semantics, an ungrounded cycle of claims has no finite derivation rank. It cannot enter stable reliance merely because many agents repeat or mutually endorse it.

Inductive or coinductive mathematics can contain recursion only through the foundation's independently checked rules, not through a graph of assertions certifying one another.

## Independent replay and portability

For an exact package \(c\), let \(\operatorname{Closure}(c)\) denote the finite transitive closure required by its declared replay procedure. The export obligation is

\[
\operatorname{ExportComplete}(c,X)
\Longrightarrow
\operatorname{Closure}(c)\subseteq X
\]

at the level of exact resolvable objects, including the environment and checking material required by the profile.

A complete manifest is not proved complete merely by a signature. Dependency extraction is part of the declared TCB or must itself be checked; hidden dynamic dependencies break the claim.

### Conditional proposition: producer independence

If a second receiver possesses the same exact immutable package closure and all inputs named by the public replay contract, and uses the same terminating checker relation with a fixed explicit local snapshot, native replay does not require a live producer or the original discovery provider. The replay contract excludes every mandatory live callback, regardless of its duration.

Proof sketch: the declared checker takes all required inputs from the exact closure and fixed local snapshot; no external interaction is an input. Successful local execution is therefore independent of the producer's current service.

This proposition concerns native replay. Equal strict-reliance decisions additionally require equal applicable policy and admitted evidence/fidelity/observation inputs. If the policy demands newer external observations, their unavailability can leave current strict reliance `UNKNOWN` even though offline native replay succeeds.

The result is conditional on compatible hardware/toolchains and bounded execution. Hashing a binary does not make it portable or prove it was compiled faithfully. Source availability, reproducible builds where feasible, independently implemented checkers, and explicit platform profiles support long-term replay.

## Contribution receipts and downstream use

One receipt cannot collapse all stages of a contribution. Distinguish:

| Receipt or event | Meaning | Does not establish |
|---|---|---|
| Transport receipt | A receiver obtained the bounded frame or object | Validation, retention, or use |
| Validation assessment | A stated receiver ran a stated procedure on exact inputs | Another receiver's acceptance |
| Retention acknowledgment | A provider undertook a scoped time/capacity obligation | Perpetual availability or independent redundancy |
| Index acknowledgment | A named index included a descriptor in a named snapshot | Complete worldwide discovery |
| Integration assessment | A local reliance contract was met at a snapshot | Semantic importance or lasting support after incidents |
| Checked application witness | Exact downstream evidence uses a theorem/interface | A counterfactual claim that the theorem saved work |
| Evaluation contrast | Matched experimental conditions show downstream benefit | Universal usefulness or individual credit entitlement |

A checked application witness can still encode a syntactically unused or avoidable dependency. Causal usefulness must be evaluated by task outcomes or meaningful resource savings under a suitable counterfactual, not merely by graph indegree.

Receiving remote receipts is optional for mathematical acceptance. Receipts are valuable for diagnosing missing stages and designing retention/discovery policies.

## Server independence and plural discovery

The protocol should permit:

- direct peer-to-peer object transfer;
- several independent bootstrap/contact distributions;
- alternative indexes over the same portable packages;
- local and overlay-scoped subscriptions;
- relays supplied by multiple operators or replaceable by direct connectivity;
- offline bundles and removable-media transfer;
- independently obtainable software, profiles, and archive snapshots.

No network-wide latest block, registrar, canonical index, privileged signing key, or hosted model API is a prerequisite for local research and self-publication.

### Reachability model

Let \(G_t=(V_t,E_t)\) be the time-varying graph of possible communication, not necessarily known to participants. Let \(a\leadsto_t b\) mean a time-respecting path that can carry the bounded relevant messages. Liveness needs a path whose forwarding and storage nodes are also willing and correctly operating.

A path in a graph of public keys is insufficient: the endpoints might all be controlled by one adversary, overloaded, withholding, or unable to serve the closure.

### Conditional property: no distinguished service dependency

For each named role such as software distribution, peer discovery, indexing, storage, relaying, or model proposal, a conforming open deployment must permit substitution of that role without changing mathematical object identities or weakening the receiver's checking contract.

Deleting a particular operator can preserve service only if sufficient alternative providers, routes, capacity, and object closure remain. The protocol cannot guarantee availability after deleting every copy or every path.

An operator-level removal study should examine all default services, including hidden dependencies on DNS, certificate authorities, time services, build registries, package managers, relays, and APIs. These need declared replacements or explicit boundaries; peer-to-peer transport alone is not sufficient evidence of independence.

### Bootstrap limit

A fresh node with no contact information, no local neighbors, no imported bundle, and no way to enumerate addresses cannot discover an arbitrary hidden network. Two worlds with different hidden peers are indistinguishable to it.

Therefore “no central server” requires multiple substitutable ways to acquire initial contact information, not the absence of all bootstrap assumptions. A new node should be able to start with a user-supplied peer or verified offline snapshot even if every default seed is unavailable.

### Optional overlays

An overlay defines its own discovery keys, membership rule, admitted metadata, retention terms, and checkpoint history. Multiple overlays may overlap and disagree.

Object publication must remain possible outside any particular overlay. An overlay's refusal to index a candidate does not invalidate it or prevent another index from serving it. A DHT can locate providers under its assumptions, but it is not a theorem authority or a universal guarantee of key ownership.

Home placement, anti-entropy, and re-sharding must be specified separately for each overlay profile. The old rendezvous scheme over five authenticated cells cannot simply be renamed “permissionless.”

## Openness, admission, and Sybil limits

Open entry means anyone may implement the format, choose local policies, form a node, self-host data, and seek willing peers without a mandatory global license.

It does not mean:

- each new key receives a fresh positive fraction of every receiver's capacity;
- every syntactically valid theorem must be indexed or archived;
- all participants have identical hardware or attention;
- a mathematical proof certifies a network identity;
- the system can prevent every censorship or eclipse attack.

An adversary can create many identities more cheaply than receivers can perform expensive checks. Correct proofs can also be costly or useless. Resource admission must therefore depend on receiver-owned aggregate ceilings and bounded service classes rather than unrestricted per-key entitlements.

Possible service profiles include local donations, institution-funded archives, reciprocal bandwidth arrangements, bounded anonymous gateways, capabilities, and optional paid services. None is promoted to universal protocol currency or mathematical truth.

Exploration must have an explicit budget so unfamiliar contributors and rare domains can be considered. This is a policy mechanism to study, not a theorem of equal opportunity under unbounded identities.

Open access also needs legal and practical portability: public reusable artifacts should declare redistribution permissions, required tools, and any proprietary dependency. A freely downloadable client does not automatically make a privately controlled corpus or required service open.

## Safety and liveness are separate obligations

### Safety: remote messages cannot alone create reliance

Under the local TCB assumptions, a received hint, foreign verdict, checkpoint, service receipt, or model output can create only bounded candidate state until the receiver's checked admission path succeeds.

Paper proof obligation: establish an invariant by induction over all permitted local transitions. The base state has no admitted reliance beyond its locally chosen checked seed. Candidate transitions do not modify active evidence. The admission transition requires the exact evidence predicate and performs the authorized atomic commit. Use and repair transitions preserve the current-epoch requirements.

This proof must later be refined against parser behavior, fault handling, and local storage transactions. Calling a transition “validate” is not a proof of its guards.

### Conditional liveness: eligible contribution reaches an interested receiver

Fix a particular candidate, receiver, mechanical discovery predicate, overlay scope, and finite work envelope. Assume:

1. at least one correct provider keeps the native closure available long enough;
2. a correct, willing path eventually carries its retained advertisement and later payload;
3. the relevant descriptor is actually registered and served by a non-omitting discovery route;
4. the receiver's policy admits the candidate and reserves enough checking/fetch resources;
5. the relevant jobs remain eligible and receive fair service under the declared load envelope;
6. required operations terminate and configurations remain stable or hand off without loss.

Then the receiver eventually completes its local validation decision. If the evidence meets the exact local contract, it can integrate the result. No theorem promises that the local research question will be solved or the result found useful.

Publishing alone does not satisfy premise 4. A contract for service may make that premise enforceable within a participating scope; the open commons cannot force unrelated nodes to consent.

### Convergence

Same-authority crash-fault replicas may reconcile immutable already admitted facts using the existing rules. Their materialized views agree only when facts, closures, availability state, schemas, evaluator/checker outcomes, policies, overrides, and logical freshness conditions agree.

Independent receivers need not converge on admission, retention, or utility. Given identical semantic inputs to the same deterministic evaluator they produce equal evaluations; this functional statement does not imply that the network delivers identical inputs or spends identical budgets.

### Partitions

Local research and local proof checking continue from retained closures. Publication may queue within finite bounds. Connectivity loss can make a required observation frontier unavailable, in which case strict freshness-dependent reliance must report nonacceptance or unknown.

An isolated node may accurately report “checked under these local inputs and observations.” It cannot accurately report “there is no remote incident anywhere.”

## Persistence and maintenance

The network retains a selected corpus, not an obligation to keep every attempt forever. Retention classes separate expendable proposals, local checked packages, replicated reusable material, and funded archives.

For each declared retained root, the service contract names:

- exact closure or fragment manifest;
- retention term and renewal procedure;
- capacity allocation and aggregate limits;
- provider failure-domain assumptions;
- integrity auditing and repair policy;
- exit/export/handoff behavior;
- consequences of expiry or failed repair.

Erasure coding lowers byte overhead relative to selected full replication profiles but can make retrieval more dependent on multiple simultaneously reachable fragments. Common foundational libraries often deserve broader caching and preservation than low-demand large proofs. These are workload-dependent decisions.

Garbage collection follows receiver-authorized live roots and active pins. Remote signatures cannot create pins. Deleting a shared dependency requires checking all local live roots, in-flight uses, and the grace-period/recovery rules. A retention contract must allocate later audits and repairs through the separate authorized-work mechanism.

The long-term corpus also needs maintainers: library adapters, checker-profile migrations, archive renewal, corrected metadata, and representation bridges. Autonomous theorem generation does not automatically provide these services.

## Sustainable correction and common-mode failure

The deeper the reuse graph, the more damaging a shared checker, elaborator, foundation, or translation error can be. A million agents using one flawed checker do not provide a million independent validations.

Protection should include:

- precise transitive dependency and checker/version footprints;
- small checking kernels and independently implemented validators where feasible;
- common-mode incident scopes that can conservatively block a relevant policy partition;
- alternative evidence paths using unaffected foundations or tools;
- protected bounded service for high-impact corrections;
- recovery that preserves incident knowledge and refuses stale cached acceptance;
- independent technical review of high-impact checking components; human-intention assessment is not a v1 operation.

Immediate local fail-closed behavior after admission of an incident does not imply immediate global correction. Incident propagation and rechecking can themselves overload the network; the design must reserve capacity and report backlog.

Consensus on a faulty checker result cannot repair the underlying flaw. Cryptographic succinctness can reduce computation only for the relation it faithfully represents; it does not remove the need to assess that relation and its implementation.

## Meaningful growth and its evaluation

This section records possible external experiments, not protocol requirements or a list of unsolved tasks maintained by v1. Formal recognition of an artifact does not require a benchmark success or a usefulness assessment. The corpus-first contract supplies the operative v1 boundary.

Let \(\mathcal Q\) be a finite preregistered task family, with hidden observer weights \(0\le w_q<\infty\), fixed task contracts, and explicit componentwise budgets \(b_q\). Let

\[
Y_{\mathcal Q}(K,\pi,B)=
\sum_{q\in\mathcal Q}w_q
\mathbf 1[
\operatorname{CheckedSuccessfulOutcome}(q;K,\pi,B)].
\]

\(K\) is the available external corpus, \(\pi\) the fixed agent/procedure profile, and \(B\) the total accounted resource envelope. This is an evaluation measure, not a global network utility or an instruction to participants.

At fixed \(\mathcal Q\), the score is bounded by \(\sum w_q\). An indefinite exponential score increase is impossible. Evaluating richer future task families is legitimate only with separately declared difficulty and comparability rules; one cannot silently change the score scale to manufacture growth.

More corpus bytes need not increase \(Y\). Retrieval noise, checking cost, weaker formalization, duplicates, and stale dependencies can make a larger corpus worse. The claim that a sufficiently capable ideal planner could ignore extra information does not prove that a deployed bounded agent will do so, or that background costs disappear.

### Multi-generation reciprocity experiment

Conceptually compare several successive cohorts of independent local tasks:

1. begin from the same checked seed corpus and solver profile;
2. let one cohort produce portable checked contributions;
3. expose eligible contributions to a later cohort under the assigned treatment;
4. require independent replay and exact application;
5. repeat for several generations;
6. assess later outcomes on sealed tasks not used to select the retained contributions.

The treatment must distinguish access to inherited public artifacts from online model adaptation, extra compute, deliberate coordination, and curator intervention. Models, seeds, temporal cuts, task releases, and total costs must be matched or explicitly treated as factors.

Preserve CP-001A's isolated, local typed, raw-store, passive federation, prior-artifact-blind, active coordination, optional-program, and central typed-service comparisons. Treat connected task histories as interference blocks; downstream tasks are not independent samples merely because they are different statements.

Report separate predefined claim families for yield superiority, resource-Pareto/noninferiority, and reliability/resilience. Causal marginal benefit is an experiment-dependent estimate, not a property inferred from a citation or dependency edge.

### Growth bottleneck model

A successful reuse chain needs discovery, compatibility, available evidence, checking, integration, and future task relevance. Each stage consumes capacity. If generation rate exceeds the sustained processing rate of any required stage, its backlog grows or admissions must be shed.

A phenomenological branching model may suggest a reproduction factor above one when a useful reusable contribution supports several later independently valuable contributions. It requires a fixed attribution/measurement rule, controls against duplicates and overlapping parents, sufficient resources, and a finite evaluation horizon. Neither a graph fanout nor a spectral radius proves real scientific acceleration without those premises.

Exact storage lower bounds concern distinguishable retained information and membership, not a claim that each new derivable theorem contributes independent entropy. Fixed axioms plus an enumerator can compactly describe infinitely many consequences. The practical obligation is affordable exact recovery, discovery, and checking within declared bounds.

## Adversarial and honest-failure examples

| Scenario | Required behavior | Relevant obligation |
|---|---|---|
| A stranger submits an invalid proof | Reject or report bounded nondecision; never rely on its claim | RC-VALID, RC-RESOURCE |
| A stranger submits a valid useful proof | Permit self-publication and matching willing-peer admission without global enrollment | RC-OPEN, RC-RECIPROCAL |
| A valid proof uses a hidden stronger axiom | Detect the transitive footprint and reject it for a weaker contract | RC-COMPOSE |
| A descriptor misstates the formal quantifier order | Recognize only the exact checked content; the descriptor cannot change its statement | RC-CONTENT |
| Millions of distinct easy tautologies arrive | Bound aggregate work and retention; preserve declared service reserves | RC-RESOURCE |
| A proof references a producer's private file | Fail public replay qualification until exact closure is exported | RC-PORTABLE |
| An index omits an unpopular branch of mathematics | Other indexes and self-hosted routes remain possible; no universal nonexistence claim | RC-OPEN, RC-DISCOVER |
| Every advertised provider is adversarial | Fail availability/discovery honestly; hashes cannot create a willing provider | RC-DISCOVER, RC-PRESERVE |
| Default bootstrap, relay, and website disappear | Existing nodes operate from retained data; new nodes can use alternative supplied contacts/bundles | RC-EXIT |
| Two theories contradict under combined assumptions | Keep contexts distinct and require compatible import or checked transport | RC-PLURAL, RC-COMPOSE |
| A popular checker version is found unsound | Block affected local reliance after admitted incident; preserve unaffected alternatives | RC-REPAIR |
| Corrected methods remain memorized incorrectly by a model | Model proposals remain untrusted; current exact checking and contracts govern reliance | RC-VALID |
| A contributor leaves | Replay and preservation depend on retained closure and willing archives, not that person's online status | RC-PORTABLE, RC-PRESERVE |
| A governance group forks | Both sides retain object interpretation; operational ledgers and authorities remain separate | RC-EXIT, RC-EVOLVE |

## Long-term evolution and voluntary coordination

Protocol upgrades need explicit schema and checker versions, migration objects, stable interpretation of old artifacts, and an export path. A new release must not silently reinterpret an old identifier or make an incompatible axiom system appear unchanged.

Key rotation and hash migration are operational needs. A new hash may re-address verified bytes with an explicit mapping; that mapping does not rescue an ambiguous or compromised old hash without recovering and checking the actual content.

Independent implementations and standards processes reduce lock-in. They do not eliminate the need for decisions. A community can coordinate a recommended profile without acquiring universal authority over every node.

Local agents may voluntarily coordinate research, share budgets, or fund archives. Joining such a group cannot weaken their mathematical acceptance predicate or impose a compulsory root goal on unrelated participants.

Sustainability remains partly a resource and participation problem: finite storage, administration, repair, verification, and software maintenance have to be supplied by someone. The concept should identify these obligations rather than assume that a token or recursive AI process solves them.

## Proof obligations before implementation

| ID | Paper obligation | Counterexample the definition must exclude |
|---|---|---|
| PO-01 | Native validity and semantic truth are separated with explicit assumptions | Inferring unconditional truth from a proof in an inconsistent theory |
| PO-02 | Composition preserves exact hypotheses, foundation, and target contract | Applying a field theorem to a ring because names match |
| PO-03 | Public export closure is sufficient for declared replay | A hidden producer-local build input |
| PO-04 | Abstract transitions preserve acceptance and accounting invariants | A remote receipt bypassing local checking or creating storage authority |
| PO-05 | Current reliance is tied to a coherent local epoch and observed scope | A cached proof survives admitted contrary evidence as current |
| PO-06 | Open entry is distinct from guaranteed service and unique identity | Infinitely many keys each create a queue share |
| PO-07 | Conditional discovery explicitly includes consent, retention, and fair service | A reachable but censoring or unfunded path is called live |
| PO-08 | Overlay changes preserve exact objects while scoping control authority | Two federations unknowingly spend the same replicated budget |
| PO-09 | Operator removal and bootstrap claims state residual paths and closure | Expecting a fresh node with zero contacts to find arbitrary peers |
| PO-10 | Retention protects active roots without unbounded remote pins | Millions of signed foreign contracts pin local storage |
| PO-11 | Multi-generation usefulness is defined independently of contribution count | Padding a corpus with copies or unused dependencies raises the primary score |
| PO-12 | Positive growth claims include maintenance and bottleneck capacity | Extrapolating indefinite exponential growth from three easy generations |
| PO-13 | Evolution preserves interpretation and explicit compatibility | A schema upgrade silently changes the theorem behind an old ID |

These obligations are not declared proved by listing them. For CP-001C the deliverable is precise statements, counterexamples, paper arguments, and remaining questions. Later executable refinement and empirical evidence remain necessary.

## Design alternatives retained for comparison

| Choice | Advantages | Costs or unresolved issues | Current position |
|---|---|---|---|
| Global blockchain of theorem transactions | One agreed publication history under consensus assumptions | Ordering and replicated metadata cost; open storage spam; no intrinsic semantic validity | Unnecessary base requirement |
| Central theorem server with mirrors | Simple operations and global index | Administrative dependence and privileged discovery | Useful comparison baseline, fails end-state independence |
| Several fixed federations | Measurable service and bounded membership | Fragmentation, gateways may become gates | Good optional overlays and experimental profiles |
| Flat public DHT | Open provider lookup | Key grinding, Sybil/eclipse, hot spots, limited semantic search | Candidate discovery component with separate assumptions |
| Portable packages plus plural overlays | Local replay, replaceable services, heterogeneous goals | Hard discovery, retention, compatibility, and usability problems remain | Preferred concept architecture |
| Continuously trained shared model | Compression and potentially better priors | Inexact memory, synchronization, poisoning, correction difficulties | Optional heuristic layer |

## References and inherited reasoning

These are conceptual sources and comparison targets, not claims that their implementations satisfy this specification. No new performance survey or release verification was performed for this checkpoint.

- [Cooperation Core v0](COOPERATION-CORE-v0.md): exact support semantics, receiver admission, resource accounting, atomic reliance.
- [CP-001A](../notes/checkpoints/CP-001A-autonomy-first-cooperation.md): autonomous work, optional goals, reliable useful-work efficiency and evaluation ladder.
- [CP-001B](../notes/checkpoints/CP-001B-distributed-corpus-and-global-status.md): distributed memory, retention, scoped frontiers, and model non-authority.
- [Technology reuse map](../research/COOPERATION-TECHNOLOGY-REUSE.md): Lean, native certificates, content-addressed storage, indexes, libp2p/DHT candidates, MMT-style theory interfaces, and formal-methods tools.
- [SNARK assessment](../research/SNARK-ASSESSMENT.md): succinct-proof relation and trusted-computing assumptions.
- [Decentralization analysis](../notes/analyses/CP-001C-decentralization-analysis.md).
- [Reciprocity analysis](../notes/analyses/CP-001C-reciprocity-analysis.md).
- [Growth analysis](../notes/analyses/CP-001C-growth-analysis.md).

Bibliography entries are deliberately unnumbered. Paper propositions in this file are original design arguments and remain conditional on their listed premises.
