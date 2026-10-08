# Evidence-plane reuse map and historical delivery plan

> **Historical plan:** [The cooperation testbed](COOPERATION-TESTBED.md) supersedes this as the primary first deliverable. Reuse decisions here remain relevant to the later evidence and transparency plane.

## 1. Architecture rule

Reuse mature mechanisms for bytes, signatures, receipts, builds, distribution, and proof checking. Build only the mathematical profiles and federation behavior that existing systems do not supply.

## 2. Build versus reuse

| Area | Reuse | DVMKN-specific work | Caution |
|---|---|---|---|
| Evidence envelope | SCITT RFC 9943; COSE receipts RFC 9942; COSE/CBOR/CDDL | Mathematical payload media types and relying-policy predicates | Registration authenticates an assertion; it does not make it accurate or complete |
| Canonical encoding | Deterministic CBOR/RFC 8949 profile | Frozen schema, type tags, Unicode rules, conformance vectors | Never hash an ordinary in-memory or noncanonical JSON representation |
| Formal checking | Lean 4, Mathlib, LCF-style kernel ideas, axiom reporting | Export boundary, environment root, verifier adapter, trust report | Kernel acceptance is relative to exact logic, axioms, and environment |
| Knowledge representation | OMDoc/MMT, Math-in-the-Middle, interface theories, theory morphisms, Dedukti ideas | Lean profile, typed relation/evidence model, later cross-system mappings | Do not impose a universal ontology or confuse translation with equality |
| Proof certificates | Lean terms; SAT/SMT proof formats such as LRAT/Alethe/LFSC where later useful | Adapter contract and certificate metadata | Proof-source compilation and final certificate checking have different TCBs |
| Supply chain | TUF, in-toto, SLSA, Sigstore/Rekor patterns, reproducible-build methods | Proof-specific predicates, axiom/dependency reports, trusted-base policy | Signed provenance can still be false; containers are not reproducibility proofs |
| Storage/transport | OCI/ORAS, content-addressed stores, ordinary object storage, optional IPFS transport | Typed artifact manifests, mirror policy, archival package | Content addressing is integrity, not persistence or discovery |
| Transparency | SCITT VDS receipts; CT v2; Trillian/Rekor/CONIKS lessons; checkpoint gossip/cross-logging | Witness policy, fork evidence, recovery, mathematical event views | A split view is detected only when views meet unless quorum prevention is added |
| Federation | Event sourcing, authenticated gossip, set-union/CRDT techniques for immutable facts | Registry discovery, subscriptions, policy-scoped materialized graph | CRDTs preserve conflicts; they do not resolve semantic disagreement |
| Consensus/blockchain | Mature BFT protocols or public chains only if a narrow state later requires them | Exact authority/escrow/anchoring profile | Never use consensus for theorem validity or routine object storage |
| Provenance | W3C PROV/PROV-O; database provenance | Agent/formalizer/verifier activity predicates and failure-domain genealogy | Signatures do not prove model identity, originality, or independence |
| Search/alignment | Vector retrieval, formal embeddings, e-graphs, equality saturation, premise retrieval, ontology matching | Typed candidates, bridge synthesis, counterexample search, certified edges | Similarity is retrieval evidence, never equivalence evidence |
| Agent coordination | Actor/blackboard/workflow models; proposer–critic–formalizer–replayer separation; capability delegation | Mathematical message types and persistent artifact/failure records | Do not store or require private chain-of-thought as scientific provenance |
| Protocol assurance | TLA+/Apalache, Tamarin or ProVerif, Alloy, property-based/differential fuzzing, Jepsen-style tests | Models for lifecycle, receipt/checkpoint policy, recovery, key epochs, federation | Model claims apply only to the modeled assumptions and abstraction |
| Confidentiality, later | Commitments, AEAD, SNARK/STARK/zkVM, MPC, PIR, FHE, ORAM, TEEs, threshold encryption/VSS | Restricted proof-possession or private-relation statement | ZK does not hide access patterns, ensure fair exchange, or certify semantics |

## 3. What Core v0 builds

### 3.1 Normative design artifacts

- deterministic object and event schemas;
- SCITT payload and relying-party policy profiles;
- CID, algorithm-agility, and versioning rules;
- Lean claim, environment, derivation, and attestation profiles;
- threat model, TCB inventory, and governance boundary;
- conformance and adversarial test specifications.

### 3.2 Executable components

- `dvmkn pack`: constructs and validates a bundle from a pinned Lean project;
- `dvmkn verify`: resolves dependencies, reconstructs the environment, replays the checker, and produces a report;
- `dvmkn inspect`: shows exact objects, axioms, dependencies, evidence types, and policy status;
- a content-addressed store with OCI import/export;
- one SCITT-compatible transparency service or adapter and a receipt verifier;
- a mirror and monitor/witness tool retaining checkpoints;
- lifecycle support for challenge, supersession, withdrawal, warning, and key status;
- reverse-dependency impact calculation;
- a minimal viewer that never displays one undifferentiated truth badge.

### 3.3 Formal and adversarial artifacts

- TLA+ model for publish/register/checkpoint/rollback/recovery flows;
- Tamarin or ProVerif model for issuer, verifier, and key-epoch authentication if the protocol warrants it;
- canonical-encoding golden vectors and two independent encoders;
- differential parser/property fuzzing harness;
- adversarial packages covering substitution, drift, hidden axioms, unsafe features, parser ambiguity, archive/build attacks, proof bombs, replay, forged attestations, freeze, and split view;
- reproducible evaluation report and raw measurements.

## 4. Definition of done

Core v0 is done only when:

1. two independent encoders produce identical CIDs for every golden vector;
2. material byte or typed-value changes alter the expected CID;
3. statement, proof, environment, dependency, signature, and predicate substitutions are rejected;
4. supported bundles replay on clean independent machines with the same checker result and axiom report;
5. missing, mutable, or nondeterministic environments fail closed;
6. prohibited axioms and unsafe mechanisms are surfaced and policy-rejected;
7. SCITT statements and receipts validate and bind the intended subject and predicate;
8. a simulated split view yields portable evidence after view intersection;
9. a pinned client rejects rollback/freeze under its declared freshness policy;
10. dependency mutation produces the complete manifest-defined transitive impact set;
11. withdrawal changes reliance without deleting history;
12. old objects remain interpretable and checkable after a schema/profile upgrade;
13. candidate relations never become certified without verified bridge evidence;
14. public objects and evidence export to an independent mirror without privileged database access;
15. failure injection measures recovery from log, mirror, verifier, and network faults;
16. overhead is reported against plain Git/Lean CI and a centralized registry without transparency.

Measurements include package size, environment reconstruction time, kernel replay time, resource-limit behavior, receipt/proof size, registry throughput, storage amplification, mirror recovery, and operator complexity.

## 5. Suggested one-semester sequence

### Weeks 1–2: boundary experiments

- package 20 small Lean claims;
- compare source, elaborated expression, proof term, `.olean`, dependency, and axiom extraction boundaries;
- decide what is logically material;
- build the first threat-driven golden vectors.

**Gate:** no schema freeze until the Lean export boundary is demonstrated.

### Weeks 3–4: object and evidence profile

- freeze deterministic CBOR subset, type tags, and CIDs;
- define SCITT predicates and key epochs;
- implement two small independent encoders and mutation tests;
- create initial OCI transport manifest.

**Gate:** cross-implementation CIDs and receipt binding agree.

### Weeks 5–7: local verification

- implement `pack`, `verify`, and axiom/dependency reports;
- reconstruct two pinned library snapshots in clean environments;
- apply time, memory, filesystem, and network limits;
- compare result reproducibility and binary reproducibility separately.

**Gate:** valid bundles replay; all failure modes fail closed.

### Weeks 8–9: transparency and lifecycle

- register publication and verification statements;
- validate receipts and retain checkpoints;
- append challenge, withdrawal, warning, and key events;
- simulate rollback, freeze, and split views.

**Gate:** an observed fork produces portable evidence and recovery is explicit.

### Weeks 10–11: storage, mirror, and impact

- mirror objects through OCI/CAS;
- test archive failure and credible export;
- compute declared reverse-dependency closure;
- test compromised dependency and alternative derivation cases.

**Gate:** the system distinguishes affected derivations from false propositions.

### Weeks 12–13: formal model and fault testing

- model checkpoint/recovery invariants in TLA+;
- fuzz codecs and archives;
- run network/service fault injection;
- test key rotation and compromise epochs.

**Gate:** every security claim has a passing mapped test or is downgraded.

### Weeks 14–16: evaluation and independent audit

- expand to 100–500 packages and two snapshots;
- run baselines and measure overhead;
- give an external operator only public specifications and test vectors;
- record interoperability failures and unresolved risks;
- produce the paper/report and `CP-001`/`CP-002` checkpoints.

**Gate:** a second operator can verify and mirror without private assistance.

## 6. Later phases

### Phase 2: real federation

Two independently implemented registries, cross-registry subscriptions, partition testing, registry-specific curation, mirror discovery, cross-logging or witness cosigning, and a demonstrated exit from one operator.

### Phase 3: typed Lean alignment

Approximately 200 theorem pairs with hard negatives, explicit concept mappings, typed labels, checked bridge proofs, and counterexamples. Evaluate Recall@\(k\), relation precision/recall, certification rate, human review time, and especially false-equivalence rate with confidence intervals.

### Phase 4: plural foundations

Use OMDoc/MMT-style theories and explicit morphisms to add one second proof assistant. Preserve foundation-specific assumptions and unresolved translation obligations.

### Phase 5: confidentiality

Start with a restricted decidable relation—SAT/SMT certificates, bit vectors, finite-field identities, or a small exported checker. Define leakage and fair-exchange assumptions before selecting ZK, MPC, PIR, FHE, ORAM, or TEE components.

### Phase 6: scale and governance

Only after external use: anti-spam economics, institutional identity, domain curation, archives, safety-sensitive disclosure, constitutional upgrades, and a standards consortium or public foundation. A private hosted service may be a complement; public mathematical objects and verification should remain portable.

## 7. Research deliverables

The first publishable package should contain:

- protocol and security specification;
- open reference implementation;
- evaluation corpus and attack suite;
- formal models and model-check outputs;
- reproducibility bundle;
- independent audit/disposition log;
- short systems/formal-methods paper centered on exact guarantees and measured cost;
- demonstration showing one malicious registry, one honest client, and one independent mirror/monitor.

The strongest paper claim is not “we built a global mathematics network.” It is:

> DVMKN Core separates local derivational verification from federated evidence coordination and demonstrates exact artifact binding, portable replay, accountable observable histories, append-only correction, and dependency incident analysis under an explicit threat model.

## 8. Market and institutional boundary

Core protocol, public schemas, public claim objects, and local verification should be open. Potential paid complements are managed private registries, continuous verification, dependency-risk analysis, integrations, high-availability operation, confidential workflows, audit reports, and contractual responsibility.

The private-vault thesis is speculative. It should be evaluated through customer discovery only after a public evidence pipeline works. Cryptographic feasibility alone is not evidence of demand.
