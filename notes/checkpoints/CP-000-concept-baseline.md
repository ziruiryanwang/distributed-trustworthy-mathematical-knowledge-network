# CP-000: Evidence-first concept baseline

> **Historical checkpoint:** [CP-001](CP-001-cooperative-knowledge-generation.md) supersedes this document's priority order and first deliverable. The object-integrity and validation material remains supporting infrastructure, but identity, provenance, transparency, and attribution are no longer on the MVP critical path.

| Field | Value |
|---|---|
| Checkpoint | `CP-000` |
| Date | 2026-08-27 |
| Status | Superseded in priority by `CP-001`; retained for traceability |
| Project | Distributed Verifiable Mathematical Knowledge Network (`DVMKN`) |
| Source conversation | `D:\Downloads\ChatGPT-AI and Mathematics Research-20260827-1346.md` |
| Source SHA-256 | `82F92900EC07B78B80C99C19CDEA0179450DFE0CB4EC0FB0F22FB2A4B9328922` |
| Repository state | Workspace was empty and was not a Git repository when this checkpoint began |
| Review method | Independent security, technology, specification, and audit tracks; disagreements resolved in this synthesis |

## 1. Executive decision

The project is:

> **A federated evidence network in which exact formal mathematical claims are portable and locally checkable, publication and correction histories are accountable, semantic relations are typed and evidence-bearing, and no single operator controls verification, storage, visibility, or meaning.**

The bounded research question for the first artifact is:

> Can independently administered nodes exchange AI-generated Lean claims such that any conforming client can bind the exact statement, proof, dependencies, and logical environment; reproduce kernel acceptance; audit publication and correction history; and distinguish mechanically certified facts from semantic and institutional judgments?

The long-term network is the vision. `DVMKN Core v0` tests this question; it must not claim to be the global network.

## 2. Why this is a network problem

If AI systems make formal-claim production abundant, proof generation is only one step in a larger knowledge lifecycle:

1. state an intended informal claim;
2. choose definitions and assumptions;
3. produce an exact formal claim;
4. derive it in a declared logic and environment;
5. reproduce the derivation independently;
6. relate it to existing claims;
7. attribute, challenge, correct, supersede, or retract evidence;
8. preserve the object and its dependency closure;
9. allocate attention and reliance under plural institutional policies.

Proof assistants address step 4, conditional on their trusted base. They do not by themselves solve the other steps. DVMKN is the evidence and interoperability layer around proof systems, not a replacement for them.

## 3. Constitutional meanings

### 3.1 Global

Global means that separately administered systems can exchange stable objects and evidence. It does not mean:

- one physical database;
- one total order of discoveries;
- one theorem namespace;
- one proof assistant or foundation;
- one ontology of mathematics;
- one ranking service;
- one political jurisdiction.

### 3.2 Decentralized

Decentralization is a property of the allocation of critical powers. DVMKN aims for:

- recipient-local derivation checking;
- portable, content-addressed public objects;
- multiple registries, mirrors, transparency services, witnesses, and indexers;
- registry-local curation and reliance policies;
- protocol forkability and credible exit;
- polycentric, auditable upgrade authority if a community forms.

Centralized services remain acceptable for expensive search, proof computation, curation, user experience, and contractual responsibility, provided they do not become exclusive authorities over public objects or verification.

### 3.3 Knowledge

The network stores evidence-bearing assertions, not unqualified truth. It must preserve separate dimensions:

\[
(\text{formal derivability},\text{reproduction},\text{semantic fidelity},
\text{alignment},\text{novelty},\text{significance},
\text{provenance},\text{availability}).
\]

No API, database column, or user interface may collapse these dimensions into a single `THEOREM_IS_TRUE` or scalar trust score.

### 3.4 AI-assisted

An AI agent is an untrusted publisher, consumer, or service principal. The system verifies its artifacts, not its eloquence. Model name, prompt, tool use, and lineage are authenticated assertions unless independently measured by a trusted execution or provider-attestation mechanism. Multiple agents do not constitute independent evidence when they share models, data, orchestration, proof libraries, binaries, operators, or infrastructure.

## 4. Principal security property

The primary property is **evidence-preserving local verifiability under Byzantine federation**:

> Any relying party can obtain an immutable claim package, independently check the exact formal claim against an explicit trusted base and local policy, audit the recorded publication and correction history, and retain enough portable evidence to detect or prove observable substitution, rollback, or equivocation without trusting one registry, model provider, or ranking service.

This decomposes into four P0 guarantees:

1. **Local validity.** Consensus, popularity, or registry inclusion cannot replace recipient-side checking.
2. **Evidence integrity.** Statements, proofs, logical environments, dependency closures, attestations, and lifecycle events are cryptographically bound with type and version domain separation.
3. **History accountability.** Silent rewriting is impossible without changing identifiers; observable conflicting histories yield transferable cryptographic evidence. Prevention requires an explicit honest-quorum assumption.
4. **Failure containment.** A compromised dependency, checker, key, registry, or semantic assertion can be located, challenged, superseded, and propagated without asserting that every associated mathematical proposition is false.

For an exact formal claim \(C\), derivation \(D\), logical environment \(E\), and checker \(K\), the conditional mathematical statement is:

\[
\operatorname{KernelAccept}_K(E,C,D)=1
\Longrightarrow
\operatorname{Axioms}(E)\vdash_{\operatorname{Logic}(E)} C,
\]

assuming the checker implements its claimed calculus soundly. This establishes derivability relative to the declared foundation and axioms. It does not establish:

- consistency of arbitrary axioms;
- truth under an unstated intended interpretation;
- fidelity to the natural-language claim;
- novelty, importance, elegance, or correct attribution.

The full property and adversary assumptions are fixed in [the threat model](../../security/THREAT-MODEL-v0.md).

## 5. Project architecture

The first architecture has six planes.

### 5.1 Immutable object plane

Versioned deterministic CBOR objects form a typed content-addressed DAG. Exact artifacts, logical environments, formal claims, derivations, interpretations, provenance assertions, and theorem relations have distinct identities. Semantic equivalence is never inferred from equal hashes.

### 5.2 Derivational verification plane

A Lean-first adapter reconstructs a pinned environment, checks referential closure, invokes the declared checker, enumerates actual axioms and unsafe features, and emits a signed attestation. Relying clients may replay verification and apply their own policy.

### 5.3 Evidence and transparency plane

DVMKN profiles the IETF SCITT architecture in RFC 9943 and COSE receipts in RFC 9942. A signed statement binds a subject digest to a narrowly defined predicate. A transparency service registers it and returns a verifiable receipt. Registration authenticates a recorded assertion; it does not make the assertion accurate.

### 5.4 Storage and federation plane

Objects travel through ordinary content-addressed storage and OCI-style manifests. Registries publish signed append-only events and policy-scoped views. Public facts can merge by set union; conflicts remain first-class. There is no global total order. Content addressing supplies integrity, not persistence, so replication and archive policies are explicit.

### 5.5 Semantic relation plane

The network is a derived, multirelational graph. Relation types include `EQUIVALENT`, `IMPLIES`, `SPECIALIZES`, `TRANSPORTS`, `DUAL`, `USES`, and `ANALOGOUS`. Evidence status is one of:

- `candidate`: probabilistically retrieved or proposed;
- `attested`: asserted by identified reviewers;
- `certified`: supported by locally checkable bridge evidence binding endpoints, translation, context, and relation type.

### 5.6 Reliance and governance plane

Each relying party chooses trusted checkers, foundations, axioms, issuers, transparency services, freshness rules, and curation policies. Governance can determine protocol and registry policy, never mathematical derivability. Old objects must remain interpretable after upgrades.

The historical sketch is now maintained as [DTMKN Evidence Profile v0](../../spec/DTMKN-EVIDENCE-PROFILE-v0.md); its pre-freeze `DVMKN` wire/profile name was superseded by decision `D-023`.

## 6. Why a blockchain is not the base layer

A blockchain can order events under stated consensus assumptions. It cannot decide whether a Lean derivation checks, whether a formalization matches its intended statement, whether two theorems are semantically the same, or whether a discovery is important.

Routine objects therefore do not go on a public chain. Merkle transparency services, authenticated statements, local checking, and ordinary replicated storage provide the required base properties with lower cost and less privacy leakage. A chain may later be useful for:

- occasional external anchoring of checkpoints;
- escrow or payment;
- a narrowly scoped namespace or governance decision among mutually distrustful parties with no acceptable coordinator.

No token, DAO, theorem-count reward, or permissionless consensus is part of Core v0.

## 7. Principal issues

### 7.1 Semantic fidelity

A proof can be valid while formalizing the wrong claim. Quantifier order, domains, boundary cases, strengthened hypotheses, imported choice principles, and subtly different definitions are common failure modes. Formal validity and informal alignment must be separately reviewed and displayed.

### 7.2 Theorem identity and alignment

Exact bytes are easy to hash; mathematical sameness is not. Equivalence in expressive theories can be as hard as theorem proving and is undecidable in general. DVMKN therefore records typed, evidenced relations rather than a universal canonical theorem ID. The most dangerous alignment error is a false equivalence that merges materially different claims.

### 7.3 Trusted computing base and proof supply chain

The relevant base may include the kernel, logic, axioms, elaborated declarations, plugins, compiler, build tools, package resolver, native computation, container image, operating system, and hardware. A container digest is not proof of reproducibility. The system must distinguish logical dependency, build provenance, binary reproducibility, and independent replay.

### 7.4 Correlated verification failures

Ten signatures from machines using the same image, mirror, kernel binary, cloud, base model, and operator are not ten independent checks. Attestations need failure-domain lineage; any aggregation policy must be explicit and must not fabricate a probability of truth.

### 7.5 Transparency limits

A log receipt proves registration relative to a transparency service and its verifiable data structure. It does not prove discovery time, first priority, completeness of an issuer's submissions, truth of the payload, storage availability, or that every split view will be seen. Fork detection requires conflicting checkpoints to meet an honest monitor; stronger fork prevention requires quorum assumptions.

### 7.6 Spam, denial of service, and attention capture

Cheap generation enables trivial corollaries, proof bombs, archive bombs, malicious build recipes, near-duplicate objects, poisoned alignments, and ranking manipulation. Registries need bounded resource policies and staged verification. Open publication does not require every registry to relay every object.

### 7.7 Availability and long-term preservation

Hashes and logs can outlive their payloads. Public objects need mirrors, archive thresholds, format migration, cryptographic agility, and executable environment preservation. Legal removal, personal data, and dangerous payloads conflict with immutable publication; sensitive content must remain off public logs.

### 7.8 Identity, attribution, and key recovery

A signature proves control of a key, not moral authorship, originality, or causal contribution. Human, institution, service, model family, model build, agent run, and delegated task identities must be distinguished. Compromise, rotation, recovery, and historical interpretation need explicit key epochs.

### 7.9 Federation and governance

During partitions, strong global consistency and full availability cannot both be promised. Most knowledge objects should remain available and eventually merge; only narrow noncommutative authority changes may need consensus. Polycentric governance improves exit and pluralism but can fragment, stagnate, or be captured.

### 7.10 Confidentiality

Replication improves availability while increasing confidentiality exposure. Zero knowledge proves a precise relation over committed inputs; it does not provide query privacy, access-pattern privacy, fair exchange, semantic fidelity, or commercial value. Private theorem exchange is a later research program after a public Lean pipeline is measured.

## 8. Existing knowledge to reuse

The project should reuse rather than redesign:

- Lean 4, Mathlib, LCF-style small-kernel checking, axiom reports, and proof certificates;
- OMDoc/MMT, interface theories, theory morphisms, and Dedukti ideas for plural foundations;
- deterministic CBOR, COSE, SCITT statements and receipts;
- Certificate Transparency, witnesses, cross-logging, and key-transparency lessons;
- TUF, in-toto, SLSA, Sigstore/Rekor patterns, reproducible builds, and Nix/Guix;
- OCI/ORAS manifests, content-addressed storage, and archival replication;
- W3C PROV and database provenance;
- event sourcing, authenticated gossip, CRDTs for monotone metadata, and BFT only for narrow authority state;
- TLA+/Apalache, Tamarin or ProVerif, Alloy, differential fuzzing, property testing, and Jepsen-style fault injection;
- proposer/critic/formalizer/replayer agent separation and explicit tool/model lineage;
- commitments, SNARK/STARK/zkVM systems, MPC, PIR, FHE, ORAM, threshold encryption, and verifiable secret sharing only when a precise later privacy relation demands them.

The build-versus-reuse decisions and cautions are in [the reuse map](../../research/REUSE-AND-DELIVERABLES.md).

## 9. First deliverable

`DVMKN Core v0` is a security constitution plus executable adversarial prototype:

1. normative object, relation, event, and SCITT-predicate profiles;
2. threat model and trusted-computing-base inventory;
3. Lean 4 packaging and local-verification CLI against pinned library snapshots;
4. deterministic encoding and cross-implementation conformance vectors;
5. content-addressed object store and OCI transport profile;
6. one SCITT-compatible transparency service and receipt verifier;
7. at least one independently administered mirror and two witness identities;
8. signed verification, axiom, build, and failure-domain reports;
9. append-only challenge, supersession, withdrawal, policy-warning, and key-rotation flows;
10. dependency impact analysis;
11. a viewer that exposes the multidimensional evidence state;
12. TLA+ model of log, checkpoint, rollback, and recovery behavior;
13. adversarial corpus and reproducible evaluation against two baselines.

The corpus target is 100–500 claim packages across at least two pinned library snapshots, including legitimate proofs, AI-produced examples, deliberate corruptions, and a small manually certified relation set.

The successful claim is deliberately narrow:

> A registry operator is unnecessary for checking formal derivability, cannot silently alter identified content, and can be held accountable for observable history forks; challenges and dependency incidents remain auditable and portable.

The definition of done is in [the delivery plan](../../research/REUSE-AND-DELIVERABLES.md) and mapped to requirements in [the traceability matrix](../TRACEABILITY.md).

## 10. Explicit non-goals for Core v0

- a universal theorem database or canonical ontology;
- a general automatic theorem-equivalence oracle;
- a second proof assistant or cross-foundation proof transport;
- global novelty or priority;
- a single reputation or truth score;
- public-chain theorem storage or consensus;
- tokens, bounties, or a DAO;
- confidential theorem search or ZK proof checking;
- a commercial marketplace;
- complete agent chain-of-thought capture;
- production-scale global governance.

## 11. Falsifiers and stop conditions

The Core v0 thesis is weakened or falsified if any of the following persists after a bounded redesign:

1. A clean independent verifier cannot reconstruct and check supported bundles from their declared manifests.
2. Canonical encoders disagree or schema-valid distinct objects admit identifier ambiguity.
3. The system cannot expose its axiom and unsafe-feature footprint reliably.
4. The evidence protocol adds no meaningful assurance over signed Git commits plus ordinary Lean CI under the stated threat model.
5. Observable log equivocation cannot be converted into portable evidence.
6. Dependency-impact results are too incomplete to support incident response.
7. Users or agents consistently misread the evidence model as a truth or novelty certificate despite interface redesign.
8. Added verification, storage, and operational costs dominate measured benefits for the selected corpus.

The long-term global thesis is a hypothesis, not a premise. Lack of external adoption after an open, usable Core v0 and at least two integration attempts is evidence to revise the federation scope.

## 12. Audit of the source conversation

The source conversation contributed several strong ideas:

- endpoint proof checking should not be replaced by consensus;
- formal validity, semantic fidelity, novelty, and significance are distinct;
- federation is preferable to one globally synchronous state;
- theorem relations should be typed rather than compressed into similarity;
- false equivalence is a high-severity alignment failure;
- shared model and tool ancestry creates correlated failure.

The independent reviews corrected or quarantined several claims:

- numeric forecasts of a global network are speculation, not engineering evidence;
- absence claims such as “no project solves the integrated problem” require a systematic review;
- one hash must not conflate claim, proof, environment, and package identity;
- registration in a log is not global time or priority;
- transparency exposes only forks that reach a comparison point;
- a dependency incident affects derivations and reliance, not necessarily the theorem proposition;
- provenance signatures authenticate assertions, not causal truth;
- “truth layer” is replaced by “derivational verification plane”;
- content addressing provides integrity, not persistence;
- multiple attestations provide quantity, not independence;
- ZK private alignment and a private-vault market are research and market hypotheses, not near-term capabilities.

Very recent 2026 papers and company announcements named in the conversation are not premises of this checkpoint until independently verified. The source trace records the material used.

## 13. Next checkpoint

`CP-001` should freeze:

1. the deterministic CBOR schemas and domain separation tags;
2. the SCITT statement-payload and receipt profile;
3. the Lean logical-environment and derivation export boundary;
4. the TCB and relying-party policy language;
5. the exact log/witness property—detectable equivocation or quorum prevention;
6. the first adversarial test vectors.

It should include runnable conformance vectors and a model-checked lifecycle skeleton, not only prose.
