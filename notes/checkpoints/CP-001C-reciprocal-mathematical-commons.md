# CP-001C: A reciprocal, decentralized mathematical commons

Date: 2026-09-19  
Status: Concept checkpoint with corpus-first v1 refinement; see the audit disposition for reviewed scope  
Public vision: Democratization of mathematics  
Technical project: Distributed Trustworthy Mathematical Knowledge Network (DTMKN)

## Version-one scope: a corpus, not a research manager

The user's final clarification takes precedence: **no human intention, no list of unsolved mathematics tasks.** People and agents investigate independently and interact with the system by obtaining and supplying formal mathematical artifacts.

The [formal knowledge contract](../../spec/FORMAL-KNOWLEDGE-CONTRACT-v0.md) is the authoritative v1 specialization of this checkpoint. Formal recognition depends on what an artifact proves or defines under its exact assumptions, not why it was produced, whether it answers a question, or whether its usefulness has already been demonstrated. No task registration or fidelity reviewer is required.

Research orchestration, informal explanations as evidence, intended-question relations, and persistent unfinished-task registries discussed in broader earlier analyses are outside v1. Operational queues for checking, transfer, indexing, and repair are not mathematical task lists. An explicit conditional theorem is a completed formal result under its stated hypotheses, not a request that peers solve those hypotheses.

## Purpose and priority

The intended deliverable is freely obtainable software and an interoperable mathematical knowledge format. A person or autonomous agent can run a node, acquire a useful portion of mathematical knowledge, check it independently, pursue local research, publish reusable contributions, and help other nodes preserve and extend those contributions. The network continues without a mandatory central service, publisher, curator, model provider, or network-wide goal.

The primary success criterion is **reliable reciprocal mathematical productivity**: the shared body of work helps local agents accomplish useful mathematics, and their results in turn expand what other agents can accomplish. Storage growth, number of peers, publication counts, consensus throughput, and agent activity are supporting measurements. None alone establishes the primary outcome.

“Reciprocal” describes an enabled feedback loop. It does not impose a transaction in which every download must be paid for with a theorem. A reader, educator, archive operator, independent checker, or occasional contributor can legitimately participate without producing novel results.

This amendment preserves receiver-local mathematical reliance, resource safety, and CP-001B's distributed exact memory and scoped observation. It extends the long-term design to open participation. Earlier research-task managers and fixed-roster testbeds remain optional historical experimental designs, not mandatory v1 components. CP-002 remains reserved for a future executable specification; the present task stays conceptual.

## What the software represents

The software interprets a family of typed mathematical objects and their relations. It does not hard-code the entire corpus into an executable or require all participants to download every proof.

The broader extensible object space previously considered by the project includes the following. The v1 checked corpus uses the exact formal kinds specified in the formal knowledge contract; unfinished-work registries and informal-intent material are outside v1:

- theories, definitions, structures, assumptions, and formal statements;
- native proofs and independently checkable computational certificates;
- counterexamples under exactly specified hypotheses;
- compositional interfaces, checked specializations, and theory translations;
- partial developments with explicit unfulfilled obligations;
- proof methods, search strategies, and failures with accurately limited scope;
- informal explanations linked to formal objects by an explicit fidelity contract;
- local validation, availability, correction, and policy facts.

The “whole body of mathematics” is an extensibility objective: sufficiently general formats and adapters to represent diverse mathematical work, and a distributed corpus that can grow without one institutional boundary. It is not a claim that all mathematical truth is enumerated, all public work is known to every node, or every informal claim is already formalized.

For any declared observation scope, the public corpus is a virtual union of retained objects. There need not be a unique network-wide list of accepted theorems. A receiver's usable knowledge is a checked projection of this corpus under its selected foundations, tools, contracts, available dependencies, and observation frontier.

## Downloadable participation contract

The end product should have a complete local mode and a peer-to-peer mode.

| Capability | Required experience | Exact limit |
|---|---|---|
| Install and inspect | Obtain source, build instructions, checker profiles, and documented formats | Availability of a distribution channel remains a physical prerequisite |
| Work offline | Import a dependency-complete snapshot, check it, and perform local research | Offline status cannot assert awareness of later remote incidents |
| Discover peers | Use interchangeable seeds, user-supplied addresses, local discovery, or portable contact bundles | Discovering an unknown network from zero information is impossible |
| Learn from the commons | Retrieve candidates, inspect assumptions, check exact evidence, and import under local policy | Retrieval can be incomplete and resource-bounded |
| Contribute | Self-host packages, send bounded advertisements, and obtain scoped receipts when a peer accepts work | No protocol can oblige arbitrary peers to store every valid result |
| Serve others | Offer selected indexes, objects, checking, or archives within local budgets | Service consent and aggregate limits remain local |
| Leave and preserve | Export exact retained packages and continue checking with alternative software | Live global updates require reachable participating peers |
| Fork and reconnect | Run an alternative implementation or policy, exchange candidates later, and preserve old object identities | Cross-policy reliance requires explicit compatibility and rechecking |

The local bundle should work after the disappearance of the original project website, default relay, index provider, model vendor, or publisher, provided the user already has the necessary software and object closure. Cold-start access must have multiple independently usable distribution paths.

## The reciprocal cycle

1. An independent investigator obtains existing mathematical material of interest.
2. It searches its local corpus and reachable peer indexes.
3. It selects a candidate under a local time, bandwidth, checking, and storage budget.
4. It retrieves an exact immutable package and its required closure.
5. It checks the package and any formal adaptation it actually uses.
6. It investigates independently, outside the corpus protocol.
7. It supplies a portable formal result, definition, construction, counterexample, or checked relation with its exact assumptions and evidence.
8. It validates and retains the contribution locally.
9. It advertises through any willing reachable peers.
10. Another independently operating agent repeats the cycle.

Useful development can continue through many generations without a common organizer. The critical handoff is from a producer-specific artifact to an independently reusable mathematical interface. The network must preserve this handoff, not merely replicate text.

Three achievements must be distinguished:

- **publication:** another node can potentially obtain the advertised bytes;
- **reliable integration:** an independent receiver has checked a suitable exact evidence tree and local contract;
- **productive reuse:** a later task benefits from the result after retrieval, adaptation, verification, and maintenance costs are counted.

Only the third closes the productivity loop. An independently accepted but never useful theorem is a reliable contribution of uncertain value, not evidence of compounding capability.

### A concrete three-generation example

Agent A studies lists in a monoid and publishes the checked interface

\[
\operatorname{fold}(x\mathbin{+\!+}y)
=\operatorname{fold}(x)\cdot\operatorname{fold}(y).
\]

Agent B independently studies range products in a group. It imports A through a checked group-to-monoid instantiation, defines \(p_k=\operatorname{fold}(\operatorname{take}(k,x))\), and proves

\[
\operatorname{fold}(x[i:j])=p_i^{-1}\cdot p_j,
\qquad 0\le i\le j\le |x|.
\]

Agent C independently studies moving sums in integer sequences. It checks the integer additive-group instance and obtains \(S_i=p_{i+w}-p_i\) for the half-open window \([i,i+w)\). Using checked prefix-step equations, it then proves

\[
S_{i+1}=S_i-x_i+x_{i+w},
\qquad w\ge1,\quad 0\le i,\quad i+w<|x|.
\]

Each generation exports its exact definitions, assumptions, proof closure, and reusable interface. The agents need no common research root or simultaneous session. The same export protocol can carry the next independently useful result.

The interfaces matter: a monoid does not generally provide inverses; the factor order in the group formula cannot generally be reversed; the window recurrence needs its index bounds. A perfectly checked theorem about a different convention does not establish the intended result. The [full worked example](../analyses/CP-001C-reciprocity-analysis.md#three-generations-of-actual-mathematical-reuse) records these counterexamples. This chain demonstrates possible composition, not novelty or measured speedup; the latter requires charging discovery, adaptation, checking, publication, and maintenance against a matched baseline.

## Architectural decision

The [layered decomposition](../analyses/CP-001C-layered-problem-decomposition.md) divides the conceptual problem into formal content/verification, decentralized preservation/service, organization/discovery/reuse, and growth/resource-efficiency policy. These are authority boundaries, not separate required servers. Authentication and resource safety cut across them; human intention is outside the system.

The base design is a proof-carrying mathematical package network with autonomous nodes and plural discovery overlays.

Each node has a local verifier and policy evaluator, typed workspace, content-addressed storage, dependency and structural indexes, bounded peer interfaces, resource ledger, retention state, and agent interface. Models and remote peers produce suggestions; the local acceptance boundary checks evidence.

Overlays are optional services for discovery, archival retention, subscriptions, or collaborative work. An overlay can have a fixed roster, a cooperative membership rule, a DHT, or a curated index. Its membership and state are scoped to that overlay. No overlay has an exclusive right to name, publish, or validate all mathematical objects.

Objects are portable across overlays. Content identity does not depend on a chosen index, publisher domain, project account, or global naming registry. Human-friendly names are namespaced aliases that resolve to immutable identities.

The architecture inherits useful blockchain ideas: independently runnable nodes, cryptographic object identities, peer transfer, independently checkable rules, and auditable histories where needed. It does not require a single block order for every theorem. Appending a checked theorem normally creates no double-spend conflict. Two valid independent results can coexist without selecting a winning branch.

Consensus may still be appropriate inside a group that elects to share a budget, membership decision, exclusive lease, or mutable namespace. That consensus governs the group's operational state, not mathematical validity for the rest of the network.

## Formal requirements

The companion [formal concept specification](../../spec/RECIPROCAL-COMMONS-CONCEPT-v0.md) defines assumptions, state, transition obligations, and proof sketches. The principal requirements are:

| ID | Requirement | Why it is necessary |
|---|---|---|
| RC-VALID | Every current strict reliance decision has a receiver-checked finite evidence tree satisfying the exact query | Faulty or malicious publishers cannot manufacture trusted premises |
| RC-CONTENT | Recognition records exactly the checked mathematical content, independently of intention or task history | Unanticipated results remain admissible; no question-answering gate excludes valid knowledge |
| RC-COMPOSE | Reuse preserves foundations, hypotheses, side conditions, and exact dependency identities | Many individually correct packages can still be combined incorrectly |
| RC-PORTABLE | A declared public package can be exported and independently replayed with its closure | Contributions cannot depend on a vanished author's private workspace |
| RC-RECIPROCAL | A consumer can also publish through the same open object protocol | The commons can grow through local work rather than one privileged producer |
| RC-OPEN | No mandatory universal registrar, account, token, or approval is needed to create a node and publish on one's own resources | Universal entry must survive changes in institutional control |
| RC-EXIT | A participant can continue local verification and work after severing external service dependencies | Downloading should confer operational independence |
| RC-RESOURCE | Aggregate receiver work and durable state remain within explicit admitted budgets | Cheap identities and correct but useless objects cannot demand unlimited service |
| RC-DISCOVER | Retained relevant candidates are eventually discoverable under explicit willing-path, fairness, and connectivity assumptions | Local agents need a credible path from earlier work to usable inputs |
| RC-REPAIR | Locally admitted defects stop affected stale reliance while preserving unaffected alternatives | Recursive reuse otherwise magnifies earlier errors |
| RC-PRESERVE | Selected classes have explicit recoverability objectives, repair duties, and expiry semantics | A growing hash inventory is useless when its proofs disappear |
| RC-PLURAL | Alternative foundations, encodings, and policies coexist; crossing them requires explicit evidence | A single enforced ontology would concentrate both power and common-mode risk |
| RC-GROWTH | Repeated independent reuse and its costs are studied without making usefulness a prerequisite for formal recognition | Theorem-count inflation must not stand in for scientific progress |
| RC-EVOLVE | Schema, checker, key, and hash migrations preserve historical interpretation or declare their loss | The commons must survive technical change over decades |

These are conditional requirements. In particular, no-center safety can survive malicious peers if the local trusted components remain correct, while no-center liveness still needs some reachable, honest, willing service. Those are different claims.

## Openness, reliability, and finite resources

Open entry and reliable proof checking can coexist: a proof can be checked regardless of who submitted it. Open entry and unconditional service for everyone cannot coexist under finite resources and arbitrarily many requests.

The proposed compromise is an open publication interface with receiver-controlled admission. Anyone can run a node or self-host a package. Peers independently choose what to download, check, retain, index, or relay. Local exploration and onboarding reserves make unfamiliar contributors reachable without conferring unlimited queue shares on newly created identities.

This creates a real design obligation: contribution opportunities must not depend solely on existing popularity. The concept therefore requires independent indexes, bounded exploration, alternative contact paths, rare-domain preservation policies, and measurements of useful work missed through admission or ranking. None establishes equal attention for infinitely many applicants.

Operational keys identify service principals and authenticate bounded commitments. They do not establish unique human identity, mathematical truth, independence of operators, or deserved credit.

## Why useful growth is difficult

There is an unlimited supply of low-value valid mathematics: renamed duplicates, elementary specializations, proofs under impossible assumptions, and syntactic variations. A public corpus can grow rapidly while making retrieval and reuse worse.

A useful contribution may instead reduce a proof from hours to seconds, generalize many special cases, remove an unnecessary assumption, connect two libraries through a checked bridge, explain an important abstraction, or rule out a precisely scoped failed approach. Such gains require tasks and resource measurements to establish; they cannot be recognized by theorem count alone.

For a chosen finite evaluation horizon, study useful accumulation through independent research trajectories and componentwise resource use. External task-based benchmarks are possible observer tools, not a live protocol task list, a definition of knowledge, or a v1 admission gate. Growing capability across generations requires enough:

- discoverability of relevant prior work;
- compatibility between representations and local tasks;
- affordable independent verification;
- abstraction and package quality;
- independent research effort;
- preservation of earlier useful closures;
- error detection and repair;
- capacity for checking, indexing, storage, and communication.

If any of these stages saturates, more generated statements can reduce productivity. The system therefore needs a stable service envelope and explicit backpressure.

## What exponential growth could mean

Let \(K(t)\) denote an operational useful-capability measure under a declared workload family and resource accounting, not the total number of true propositions. A phenomenological relation

\[
\frac{dK}{dt}=g(t)K(t)-\ell(t)
\]

can exhibit exponential growth only while a positive proportional gain persists and capacity, discoverability, preservation, and task supply support it. It is a model to be challenged, not a consequence of using a blockchain or many agents.

With fixed total compute, storage, and attention, an indefinite exponential increase in retained unique information is impossible. Finite task suites also have a maximum score. A credible research claim is therefore initially **measurable compounding reuse over several independently evaluated generations**, followed by investigation of its scaling regime and eventual bottlenecks.

The [growth analysis](../analyses/CP-001C-growth-analysis.md) separates intrinsic task benefit, transfer cost, capacity, and learning effects. Its models are hypotheses with declared assumptions.

## Proof and specification work before coding

The next phase should produce paper-level definitions and reviewable proof obligations for:

- compositional evidence acceptance and explicit assumption accounting;
- faithful specialization and theory translation;
- closure-complete export and import;
- the local contribution lifecycle and its receiver-side dual;
- local defect propagation and epoch-consistent reliance;
- preservation under alternative proofs and policy disagreement;
- bounded aggregate admission, indexing, retention, and correction work;
- no-center bootstrap, discovery, export, fork, and recovery scenarios;
- conditional delivery and fairness claims for each overlay profile;
- growth definitions and causally meaningful experiments.

Examples and counterexamples should be written down before selecting libraries or implementing network protocols. Executable schemas, model-checking programs, a reference implementation, and experiments belong to the later CP-002 phase.

## Decisions and open choices

Decisions proposed by this checkpoint:

1. Adopt a mathematical commons with reciprocal local use and contribution as the product description.
2. Make server-independent operation and unrestricted self-hosting end-state requirements.
3. Treat the fixed federation as an experimental profile with a distinct threat model.
4. Use portable typed packages and local proof checking as the core trust mechanism.
5. Use optional plural discovery overlays, with no universal membership or theorem registry.
6. Recognize checked mathematical results without human-intention or task-completion criteria.
7. Require actual downstream benefit evidence before claiming productive accumulation, but not before recognizing formal content.
8. Treat exponential growth as an empirical hypothesis under resource assumptions.
9. Exclude human-intention processing and unsolved-mathematics task registries from v1.
10. Continue concept and formal specification work; do not begin implementation.

Important choices remain unresolved: package interface granularity; the minimum useful bootstrap library; exact semantic-bridge formats; discovery topology under churn; protection for rare-domain contributions; archive funding and renewal; verifier diversity; long-lived software distribution; and the right operational measure of compounding mathematical capability.

## Reading and review trace

- [Authoritative corpus-first v1 contract](../../spec/FORMAL-KNOWLEDGE-CONTRACT-v0.md)
- [Detailed formal concept](../../spec/RECIPROCAL-COMMONS-CONCEPT-v0.md)
- [Decentralization analysis](../analyses/CP-001C-decentralization-analysis.md)
- [Reciprocity and composition analysis](../analyses/CP-001C-reciprocity-analysis.md)
- [Growth and bottleneck analysis](../analyses/CP-001C-growth-analysis.md)
- [Audit disposition](../audits/CP-001C-AUDIT-DISPOSITION.md)
- [Previous autonomy-first checkpoint](CP-001A-autonomy-first-cooperation.md)
- [Previous distributed-memory checkpoint](CP-001B-distributed-corpus-and-global-status.md)

The prior frozen artifacts are historical inputs. New decisions and unresolved issues are recorded here and in the companion specification.
