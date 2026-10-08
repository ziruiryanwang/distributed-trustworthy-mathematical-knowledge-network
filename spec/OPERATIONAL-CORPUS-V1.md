# Operational mathematical corpus v1: integrated design

Date: 2026-09-19  
Status: Cross-reviewed candidate concept; practical implementation qualification remains open  
Work type: Concept and paper specification, not implementation

## Purpose

This document turns the earlier four-layer concept into one candidate operable system. The target is not a perfect universal theory of knowledge growth. The target is a coherent service that independent investigators can actually use: obtain exact formal mathematics, construct new material privately, contribute it, and let another independent investigator repeat the process.

The corpus contains no human-intention assessment, question-answering workflow, or unsolved-mathematics task registry. Investigators are external clients. Fetching, checking, indexing, and repairing objects require operational work queues; these do not become research assignments.

The proposal combines:

- a precisely bounded formal checking boundary;
- a conventional, independently operated local service and peer protocol;
- deterministic baseline organization and retention rules;
- replaceable heuristics for identifying material worth exploring or preserving.

Usefulness need not be formally provable. A reuse counter, access history, learned score, or LLM-generated abstraction can be useful without being a truth oracle. The design must contain its failure modes and never confuse such a signal with proof validity.

## Companion specifications and ownership

| Contract | Responsibility |
|---|---|
| [Mathematical profile](OPERATIONAL-CORPUS-V1-MATHEMATICS.md) | Formal representations, source-pinned foundation, identities, replay, hypotheses, evidence, and formal relations |
| [Network and local service](OPERATIONAL-CORPUS-V1-NETWORK.md) | Peer messages, service authorization, bounded admission, transfer, snapshots, retention, restart, and transport faults |
| [Organization and growth](OPERATIONAL-CORPUS-V1-ORGANIZATION.md) | Index/query semantics, duplicate handling, proof-family choices, bounded policy, practical diagnostics, and capacity |
| This integration contract | Cross-component state, authority boundaries, common failure behavior, and end-to-end obligations |
| [Operational paper cases](../notes/analyses/CP-001D-operational-paper-cases.md) | Concrete ordinary and adversarial executions with expected outcomes |
| [Conditional safety arguments](../notes/analyses/CP-001D-conditional-safety-arguments.md) | Native composition, authority conservation, epochs, closure preservation, paging, and conditional progress |
| [Autonomy and sustainability](../notes/analyses/CP-001D-autonomy-and-sustainability.md) | Indefinite local operation, preservation, capacity renewal, profile evolution, and the limits of global knowledge |
| [Adversarial review](../notes/audits/CP-001D-OPERABILITY-AUDIT.md) | Findings, repairs, reviewed evidence, and remaining limitations |

Conflicting definitions are integration defects, not choices an implementer should resolve silently. In particular, object IDs, query bounds, expiry rules, snapshot semantics, and resource dimensions must agree across the companions before this draft can be called complete.

## Selected system shape

### One node, several optional service roles

A node owns one local admission authority, one resource ledger, one retained corpus, and one locally selected policy/checker configuration. V1 uses a single authoritative writer per local database. It does not introduce consensus among independently operated nodes for local admission.

The same node can:

- serve only its local investigator over a local client interface;
- expose selected corpus operations to authenticated peer connections;
- offer a bounded catalogue/index of its selected collection;
- retain and serve selected closures under explicit locally funded terms.

These are service configurations, not globally assigned offices. A participant can run all of them or none of the public roles. No special publisher or archive has theorem authority.

### Initial interoperability choice

Lean 4 is the chosen first foundation. The operational target is Lean-Native/v1: a data-only representation replayed through the pinned Lean v4.22.0 kernel, supporting safe definitions, proofs, checked opaque bodies, mutual/nested inductive groups, structures, projections, and a precisely selected standard foundation. Explicit axiom footprints distinguish propext, Classical.choice, and Quot.sound; no new peer axiom is accepted. The smaller Lean-Expr-6/v1 is a separate conformance profile, not the whole project's intended mathematical scope or an automatically identity-compatible subset.

This is not an arbitrary Lean project build service. The peer cannot submit source commands, compiled modules, tactics, plugins, executable migrations, or new checker binaries for execution on the acceptance path.

The mathematical companion defines the source-pinned bootstrap selection, term language, allowable extensions, and unsupported cases. Reserved native names require an exact checked compatibility bootstrap; changing every name to a hash would not preserve all native behavior. The actual canonical bootstrap inventory and representative library replay remain release qualification gates. This is a concrete selected interchange route, not a claim that every existing library has already been exported. New profiles require explicit local installation and a distinct identity.

External tools can translate their own work into the profile. Such an exporter can be fallible or malicious: the receiver checks the resulting formal objects independently.

### Initial network choice

V1 uses direct authenticated peer connections, full-object/full-closure replicas, and replaceable index endpoints over local collections. It does not depend on a public blockchain, a global roster, one universal DHT, erasure-coded storage, or cryptographic remote-execution proofs.

Those omissions are concrete scope decisions. They do not prevent future optional overlays, but the base protocol must run without them.

Initial contacts come from a user-supplied address/key, an exported contact bundle, or another already known willing peer. The bounded peer directory supports collection-aware selection, direct route hints, and later independently funded rounds; it is not restricted to repeatedly querying four arbitrary neighbors. An isolated node can operate on an offline corpus bundle. Discovery cannot conjure an unknown network from no information.

The downloadable software represents an open mathematical object space, not a finite installer containing every future theorem. No node needs all results. Every current reuse does need its selected complete local native closure; optional indexes describe only named observed collections.

## Exact objects versus local observations

The immutable mathematical plane consists of exact profile, definition, opaque declaration, inductive group, context, judgment, proof, replay, module, and relation objects specified by the mathematical companion.

ContentID binds exact typed bytes. JudgmentID binds the exact context and statement independently of a selected proof. ProofID binds the proof term and judgment. ReplayID binds the selected witnesses and complete native declaration closure. The practical replay root is tagged as proof, definition, inductive group, or opaque declaration. A definition/group result has no invented ProofID or JudgmentID; status uses the mathematical companion's exact typed root and kind-appropriate optional projections.

The local observation plane contains:

- verification assessments under exact checking profiles;
- locally admitted dependency/checker incidents;
- selected current evidence paths;
- actual local byte availability;
- authorized retention roots and in-flight pins;
- collection/index snapshot references;
- operational grants, reservations, meters, and settlements;
- bounded access and reuse observations used by policy.

An immutable statement does not change when its proof goes offline or a ranker changes its score. A past successful verification record is not a guarantee that the same evidence remains currently usable.

Remote assessments are claims to consider, never local assessments inherited by copying. Remote popularity and retention promises also remain advisory or operationally scoped.

## Local state and serial publication

Conceptually a node holds

\[
S=(O,V,D,P,e,R,B,X,H).
\]

- \(O\): exact admitted object references and actual availability facts.
- \(V\): native verification records and selected evidence/dependency relations.
- \(D\): locally admitted defects and overrides.
- \(P\): active mathematical and operational policy/profile references.
- \(e\): monotonically advancing local reliance epoch.
- \(R\): authorized retention roots and use pins.
- \(B\): authoritative resource and execution state.
- \(X\): immutable catalogue/index snapshots and publication pointers.
- \(H\): bounded hints, access counters, and heuristic state.

This is a semantic model, not a database schema.

Changes that can affect reliance publish their new facts, conservative dirty scope, and next epoch at one local transaction boundary. Changes only to heuristic ranking need not modify mathematical content or revalidate a theorem.

The filesystem/object store is not assumed transactionally identical to the database. Content is durably staged and hash-checked before a transaction can reference it as admitted. Unreferenced staging after a crash is an orphan, not accepted knowledge.

Actual copies to external storage, public announcements, replication, and nontransactional index maintenance occur later through separately funded executions. An outbox intent is a durable request to perform work, not permission, completed storage, or mathematical acceptance.

### Authority-changing transitions

| Transition | Required local precondition | Atomic authoritative effect |
|---|---|---|
| Select/import | Supported candidate, available finite allocation | Reserve exact bounded fetch/check/staging/metadata work |
| Claim execution | Live unclaimed reservation and fenced executor | Unique running claim and authoritative meter |
| Promote | Complete durable hash-checked bytes, native outcome, permitted policy, funded retention/metadata | Assessment, evidence references, root allocation, relevant epoch, settlement, nonauthorizing outbox |
| Publish collection | Full closure authorized for disclosure, funded index/service work | Public collection membership or a pending separately funded index intent |
| Admit incident | Locally checked or locally authorized incident with conservative affected scope | Facts, dirty scope, next epoch; no wait for descendant repair traversal |
| Commit status | Coherent evidence evaluation and unchanged epoch | Immutable observation of that local snapshot |
| Release retention | Actual term permits release and active protections accounted | Remove only that allocation, update availability/reliance if affected |
| Schedule deletion | Exact storage generation unprotected at writer boundary | DELETE_PENDING fence preventing new pins of that generation |

The table does not equate database commitment with successful network delivery. NET1 reserves separate computation and reply-delivery tickets; delivery remains metered after the computed outcome is immutable.

## Contribution path

An independent investigator submits the exact candidate representation and identifies the closure it offers. The service performs these separate decisions:

1. **Framing:** Is the input bounded and syntactically acceptable at the cheap ingress boundary?
2. **Service admission:** Does a receiver-controlled budget authorize this exact finite operation?
3. **Resolution:** Are the needed bytes present or obtainable through the admitted transfer plan?
4. **Native verification:** Does the artifact satisfy its declared mathematical checking relation?
5. **Local policy:** Is that evidence basis permitted, and what current status can the receiver justify?
6. **Retention/index admission:** Which exact new references fit the authorized local storage and metadata allocation?
7. **Publication:** Which later independently funded announcements or serving operations should run?

A failure at one stage does not mean failure at every stage. A well-formed artifact can be unavailable; a checked artifact can be unretained; a retained package can have no willing remote reader.

There is no question-completion stage. No proof must be connected to an investigator's intended problem.

Local submission has an explicit publication mode. Checking and retaining a private artifact does not authorize disclosure. Public activation requires permission for the complete exposed dependency closure; an incoming reference to a private object cannot publish it by implication.

## Independent reuse path

A client can retrieve an exact object it already knows or query a named local/peer collection using one of the declared bounded structural modes. It receives candidates, not a mathematical relevance verdict.

For a selected result:

1. resolve its exact typed root/profile, kind-appropriate statement or type, evidence, environment, and selected replay closure;
2. acquire missing bytes under local admission;
3. verify the native evidence locally, reusing only correctly keyed local validation caches;
4. evaluate current local reliance from one captured epoch;
5. export the exact admissible formal interface and closure to the independent investigator.

Applying the result to another formal expression is a checked mathematical operation in the investigator's prover or in a separately submitted result. Similarity, ranking, names, and model confidence cannot substitute for formal instantiation.

A subsequent contribution is checked on its own exact merits. It need not carry the first investigator's research history or remain connected to the service that originally provided the premise.

### External investigator interface

The local interface needs only existing-content search, exact read/export, candidate submission, scoped status, and owner-authorized retention/publication controls. Long operations use finite local tickets; changing retention or publication is not permission automatically granted to any connected client.

The reusable payload is inert native data, not a trusted peer .olean. A client adapter reconstructs exact declarations with generated names in its own compatible Lean environment through checked insertion. It can add local notation, aliases, instance-search registrations, tactic metadata, or model indexes afterward. These conveniences are outside mathematical identity and admission; actual instance values used by proofs remain checked declarations.

When the client exports a new result, all elaborated arguments and selected evidence are explicit again. Source names that collapse to the same JudgmentID can require inlining a prior witness rather than creating a self-support cycle. Missing bodies, unsupported declarations, or an over-budget expansion are reported as compatibility/nondecision outcomes.

## Historical verification and current reliance

The response must keep at least these dimensions separate:

| Dimension | Meaning |
|---|---|
| Native outcome | What the exact checking run established or failed to establish |
| Current reliance | Whether an allowed, active, available evidence path currently satisfies this local contract |
| Availability | Which required bytes are present or missing at the named snapshot |
| Retention | Which local storage terms are actually active |
| Observation scope | Which node, collection, snapshot, and local epoch the answer describes |

The checking contract binds the submitted formal content. It is not a research question.

Current native reuse specializes the inherited safety boundary as

\[
\begin{aligned}
\operatorname{NativeUsable}_i(r,e)\Rightarrow {}&
\operatorname{OwnNativeAssessment}_i(r,e)\\
&\land\operatorname{AllowedProfileFootprint}_i(r,e)\\
&\land\operatorname{CompleteAvailableClosure}_i(r,e)\\
&\land\operatorname{AuthorizedProtection}_i(r,e)\\
&\land\operatorname{IncidentClear}_i(r,e).
\end{aligned}
\]

Here r includes the exact root and ReplayID. A protected use holds its finite closure pin through the operation. IncidentClear means that no locally admitted applicable defect or conservative unresolved dirty scope blocks this evidence; it is not a claim that the node knows every possible defect in the world.

The v1 mathematical profile restricts the kinds of native evidence and composition admitted, rather than exposing the broader historical task/fidelity machinery. In particular, same-context opposite derivations do not by themselves invalidate a conditional theorem: contradictory hypotheses can soundly imply any proposition. This corrects an overbroad reading of historical opposition rules.

A status result is linearized at its captured local epoch. The service rechecks that epoch at the authoritative computed-observation commit. If a relevant commit raced with the query, it retries within the existing reservation or returns a stale/nondecision outcome. A separately delivered response can arrive later; its positive label remains “reusable at the named local snapshot,” never “guaranteed current when the recipient reads it.”

This guarantees a coherent local answer at issuance, not that no future incident exists or that every peer has heard the same information.

### Handling an incident

A peer's defect notice is a bounded hint. It does not itself disable a checker or force traversal of a large dependency graph.

A confirmed object-integrity failure or locally authorized checker/profile restriction can produce an admitted incident. Formal negative evidence has its exact scope: opposite proofs under an uninhabited context are valid conditional mathematics. A separately checked closed contradiction under a jointly admissible dependency/foundation basis can trigger a basis-inconsistency incident, without identifying which checker, axiom, or artifact is responsible. The precise authority and affected identifiers are recorded.

The incident transaction changes the local epoch and conservative dirty scope before returning. A cached old acceptance cannot remain current merely because a background descendant traversal has not yet reached it.

Unaffected alternatives remain candidates for current reliance. Disabling a proof path is not a theorem that its conclusion is false.

## Resource authority is local

Every expensive operation binds a receiver-issued grant, finite reservation, unique running claim, receiver-controlled meter, and immutable settlement. V1 does not require hierarchical research-work delegation.

For each cumulative resource dimension in a finite grant,

\[
\operatorname{settledUse}
+\sum_{\text{outstanding }r}\operatorname{reserved}(r)
\le \operatorname{grantCeiling}.
\]

Peak memory, live storage, cumulative traffic, CPU, wall deadlines, and control-record allowances are different quantities. Their respective bounds are enforced in the network/accounting companion rather than mixed into an untyped scalar budget.

Sender-reported usage cannot release resources. After an uncertain crash, a reservation is settled using sound receiver measurements or conservative reserved bounds. It is not reset and reused.

Idempotent requests can still consume bandwidth. Replaying a completed request creates no new semantic side effect but its reply still needs bounded egress/control service.

Correctness does not grant storage rights. Service refusal does not assert mathematical falsity.

## Retention, pinning, and deletion

Every retained root belongs to a receiver-authorized allocation. Exact closure bytes may be shared among roots, but incoming references do not automatically create durable pins.

Garbage collection protects:

- authorized unexpired retention roots;
- active locally authorized use/transfer pins;
- the fixed installed checking profile and seed;
- state needed for outstanding transactions and recovery.

It may release expired unreferenced material according to its stated policy. It must account for shared descendants and coordinate with in-flight uses. A compaction cannot overwrite one immutable object with different bytes under the same identifier.

A proof-preserving alternative representation is a new set of objects and a checked relationship. It is not fulfillment of an exact-byte retention promise unless the original bytes remain reconstructible under that promise's cost and term.

Physical deletion uses a generation fence. The writer first marks an exact unprotected storage generation DELETE_PENDING after rechecking roots, use/export pins, and transaction protections. New roots cannot bind that generation. A funded worker then removes it, and the writer records ABSENT. Crash recovery treats uncertain pending generations as unavailable, even if physical debris remains. Reimport can cancel deletion before its worker claim or install and verify another generation before publishing availability. The grace interval does not replace this exclusion rule.

Usage-based retention is permitted. The policy should distinguish locally observed access, checked downstream application, and remote self-report; their evidential strength differs. None establishes universal future value.

## Practical heuristics and their containment

The baseline organization profile uses simple, inspectable policies. It may later be replaced or augmented with learned retrieval, LLM-proposed abstractions, predicted reuse, or adaptive caching.

No optimization needs to prove that its ranking is globally optimal. It must instead:

- state what observations it uses and what operational decisions it influences;
- remain inside receiver-owned resource and retention authority;
- expose bounded failures such as missed candidates, starvation risk, or poor cache choices;
- preserve mathematical distinctions unless a checked transformation establishes the promised relation;
- allow a fallback path independent of the dominant ranking mechanism.

An access-frequency score can be manipulated and can underweight rare foundational work. That is a reason for decay, caps, exploration, and measurement—not a reason to forbid the score or call it formal evidence.

The system does not enforce one global importance metric, research agenda, or model.

## Autonomous long-term operation

Local investigators and corpus maintenance can operate indefinitely under locally chosen policies. The system need not have an end date, central coordinator, shared research goal, or permanently required remote service.

Recurring integrity checks, discovery, cache selection, replica repair, incident recovery, and accounting compaction are independently bounded service jobs. Their progress cursors and scopes prevent an infinite job record for every historical hint. A timer or LLM recommendation never supplies resource authority.

Finite CPU/network allocations can renew under preauthorized local interval/rate policies. Renewal preserves outstanding work, actual disk occupancy, pins, and obligations; a reboot or new public key cannot mint a fresh budget. Fixed-width counters never wrap into renewed authority. Exact old profiles and checker materials can be archived, while new foundation or encoding profiles require explicit local adoption and independently checked migration.

These mechanisms support continued accumulation provided people or agents keep supplying actual capacity and recoverable replicas. They do not guarantee eternal physical survival, unconditional global freshness, or storage of every valid generated artifact. The sustainability companion makes the distinction between derived knowledge, recoverable stock, and a node's observed view explicit.

## Conditions for a useful exchange

For a particular offered artifact and interested receiver, eventual independent verification requires:

- an exact supported representation;
- enough retained closure on reachable willing providers;
- an available discovery/contact path for that receiver;
- local authorization of the required bounded operations;
- adequate service despite competing admitted traffic;
- termination of the declared checking work within its allowance.

The system can expose and instrument these conditions. Successful acquisition also requires one actual attempt to fit finite service/export/checking deadlines. Eventual packet delivery alone is insufficient: all responses could arrive just after each attempt expires. Bounded termination with UNKNOWN is distinct from successful import. The system cannot guarantee success for every public artifact under arbitrary adversarial load or universal provider failure.

Growth is evaluated from actual retained coverage, access cost, alternative evidence, structural reuse, and independent circulation. A larger corpus may improve or worsen a bounded investigator's experience. That empirical distinction does not change mathematical validity.

## Limits of this first profile

No global theorem order, perfect semantic deduplication, universal relevance oracle, global freshness guarantee, or compulsory identity-based reputation is claimed.

The concrete initial proof language and foundation are narrower than all existing mathematics, but the intended operational profile includes realistic Lean structures, standard explicit axioms, quotient constructions, and checked inductive extensions. A small core-only demonstration cannot satisfy the practical-profile qualification gate. A later profile is a separately versioned trust and interoperability decision.

All performance estimates remain estimates until measured. Paper conformance cases are evidence that the procedures are specified and mutually consistent; they are not implementation tests.

## Completion evidence required for this design

The concept is not complete merely because the three companion drafts exist. The final review must show:

- unambiguous identity and environment binding across them;
- a contribution/reuse trace with no missing operational step;
- bounded behavior at every untrusted-input boundary;
- consistent failure outcomes for overload, unsupported objects, missing closure, and crashes;
- concrete duplicate/retention behavior that does not redefine mathematical correctness;
- at least one honest-capacity and one overload calculation;
- a practical account of how external investigators consume and supply the chosen formal representation;
- adversarial examination and resolution of blocking cross-component defects.

The linked paper cases, conditional arguments, and cross-audits now supply this concept-level review. They do not establish implementation conformance, measured capacity, universal library compatibility, or completion of the ultimate long-term project goal.
