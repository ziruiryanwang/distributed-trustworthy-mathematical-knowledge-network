# DTMKN evidence-plane threat model v0

> **Priority note:** The project now optimizes first for large-scale cooperation among mostly honest but fallible agents. This Byzantine/evidence threat model remains a supporting security analysis. The P0 fault model and cooperation properties are specified in [Cooperation Core v0](../spec/COOPERATION-CORE-v0.md).

## 1. Security claim

DTMKN does not secure “mathematical truth.” It aims to provide **evidence-preserving local verifiability under Byzantine federation**:

> An honest relying client can bind exact typed objects, locally replay a declared derivation under an explicit trust policy, distinguish kinds of evidence, preserve correction history, and obtain portable evidence of any conflicting signed history that reaches a comparison point.

All claims below are conditional on stated cryptographic, checker, quorum, network, identity, and availability assumptions.

## 2. Assets

- exact formal statements, definitions, proof artifacts, counterexamples, and logical environments;
- declared and measured dependency and axiom closures;
- natural-language interpretations and informal–formal fidelity assessments;
- typed semantic relations and bridge evidence;
- provenance, contribution, registration, challenge, and retraction records;
- public-object availability and user exit;
- private claims, prompts, failed paths, model outputs, and institutional overlays in later phases;
- issuer, verifier, transparency-service, witness, mirror, and governance keys;
- checker sources and binaries, build systems, package repositories, and archive material;
- scarce user attention, search rankings, curation status, credit, and reputation;
- protocol continuity and interpretability over long time periods.

## 3. Actors

Actors include publishers, formalizers, proof agents, human reviewers, dependency maintainers, checker authors, verifier operators, registries, SCITT transparency services, witnesses, monitors, mirrors, archivists, alignment providers, indexers, curators, identity authorities, governance bodies, and relying clients.

No AI model, registry, transparency service, verifier, indexer, or ontology is universally trusted.

## 4. Trust boundaries

1. **Intent to formalization:** the checked proposition may not match the intended claim.
2. **Source to elaboration to kernel:** tactics may emit checked terms, while elaborators, plugins, native computation, unsafe features, or compromised binaries can enlarge the trusted base.
3. **Manifest to reconstructed environment:** declared versions do not guarantee content, hermetic acquisition, or reproducibility.
4. **Activity to provenance assertion:** signatures authenticate a key's statement, not its causal truth.
5. **Object to bytes:** parser differences, Unicode confusables, archive ambiguity, duplicate keys, and missing domain separation can alter interpretation.
6. **Registry to client:** registries can censor, delay, roll back, freeze, reorder, or split views.
7. **Witness set to client:** prevention properties depend on explicit quorum and key-compromise bounds.
8. **Indexer to attention:** valid objects can be hidden or promoted manipulatively.
9. **Private corpus to query service:** answers, timing, access patterns, and adaptive queries leak information.
10. **Governance to upgrade:** upgrade authority can redefine schemas, identities, accepted axioms, or historical interpretation.

## 5. Adversary model

The base adversary is probabilistic polynomial time with respect to cryptographic primitives and may:

- publish unlimited pseudonymous objects unless a registry imposes admission controls;
- control arbitrary publishers and some registries, transparency services, witnesses, mirrors, verifiers, maintainers, and indexers;
- compromise keys, insiders, build infrastructure, dependency servers, or verifier hosts;
- delay, drop, replay, reorder, or partition messages, with eventual synchrony only where liveness is claimed;
- publish formally valid but misleading, vacuous, expensive, duplicated, or semantically adversarial objects;
- poison dependencies, alignments, rankings, provenance, and agent memories;
- collude across nominally independent verification services;
- issue adaptive queries against later private services;
- exploit parsers, build scripts, archives, operating systems, hardware, or cryptographic implementations.

Each deployment must parameterize:

- maximum Byzantine witnesses/replicas and the acceptance quorum, if any;
- synchrony and freshness assumptions;
- storage or erasure-code recovery threshold;
- trusted checker source/binary, logic, axioms, and compilation chain;
- identity-to-key binding and recovery mechanism;
- privacy adversary and collusion threshold.

Correlated honest error is modeled separately. Nominal node count is not evidence of independent failure.

## 6. Security properties

### SEC-01: exact typed binding

Except with negligible probability, two distinct schema-valid typed canonical objects cannot have the same CID. All signatures and receipts bind type, schema version, subject CID, predicate type, and critical parameters.

### SEC-02: conditional local derivability

If an honest client accepts after local replay, the exact declared checker accepts the exact claim and derivation in the exact resolved environment. Assuming checker soundness:

\[
\operatorname{AcceptLocal}(E,C,D)=1
\Longrightarrow
\operatorname{Axioms}(E)\vdash_{\operatorname{Logic}(E)} C.
\]

### SEC-03: referential and dependency closure

Every material imported declaration, proof artifact, build input, and policy reference resolves to the bound content. Mutable names are forbidden in finalized derivations.

### SEC-04: attestation and provenance authenticity

Under EUF-CMA signature security and uncompromised authorized keys, an adversary cannot forge another issuer's signed assertion. The assertion remains a claim; authenticity does not imply factual accuracy, originality, independence, or authorization for an external action.

### SEC-05: append-only correction

Changing any material object produces a new CID. Challenges, supersessions, withdrawals, and warnings append evidence and preserve the earlier record.

### SEC-06: fork accountability

If incompatible signed transparency views reach an honest monitor, it can produce publicly verifiable evidence of the conflict. This is a conditional detectability property, not a claim that every isolated split view is eventually observed.

For stronger prevention, a future \(n=3f+1\), \(2f+1\)-signature checkpoint policy prevents two quorum-certified conflicting checkpoints if at most \(f\) witnesses are Byzantine and honest witnesses sign only valid extensions. Evidence Profile v0 need not make this stronger claim.

### SEC-07: rollback/freeze resistance

A client retaining checkpoint and freshness state rejects a nonextending view, stale receipt, or invalid recovery epoch according to policy. An offline client requires a separately trusted recovery path.

### SEC-08: typed epistemic integrity

Candidate, attested, and certified relations remain distinct. Formal validity, reproducibility, semantic fidelity, novelty, significance, provenance, and availability are not merged.

### SEC-09: failure containment

Dependency, checker, key, or policy incidents identify affected derivations, attestations, and reliance views. The system preserves unaffected alternative derivations and does not automatically label propositions false.

### SEC-10: availability and credible exit

Under a declared replication threshold and at least one honest reachable mirror, a public object remains recoverable. A user can export objects, evidence, identifiers, and manifests for independent verification. A hash or receipt alone is not availability evidence.

### SEC-11: resource and abuse safety

Parsing, archive expansion, environment construction, checking, graph traversal, and query evaluation have declared limits. A declared limit reached without a verdict produces `UNKNOWN(RESOURCE_LIMIT)`; a declared malformedness or certificate-invalidity verdict produces `REJECT`; an unexpected checker, sandbox, runtime, invariant, or TCB-integrity failure produces `ERROR`. Registry openness does not imply unbounded free storage or compute.

### SEC-12: governance safety

Protocol upgrades are versioned, delayed, auditable, and preserve old-object interpretation. No governance vote changes a checker result. No single operator should control identity, inclusion, verification status, ranking, and appeal simultaneously.

### SEC-13: privacy, deferred

Private objects require authenticated encryption, hiding commitments, access-control and query-leakage models, threshold recovery, and precise ZK relations. No confidentiality property is claimed by Evidence Profile v0.

## 7. Attack analysis

| Attack | Required mechanism | Residual limitation |
|---|---|---|
| Statement/proof substitution | Typed CIDs; signed subject/predicate binding | Canonicalization or hash failure is catastrophic |
| Dependency confusion/version drift | Full content roots; TUF-style metadata; hermetic acquisition | Recreating old toolchains remains difficult |
| Hidden axioms or unsafe features | Measured axiom/TCB report; relying policy | Policy semantics can be misunderstood |
| Malicious checker binary | Pinned digests; reproducible builds; independent replay/implementations | Shared compiler, OS, or hardware can correlate failure |
| Parser differential/Unicode confusion | One canonical binary profile; golden vectors; differential fuzzing | Sustained multi-language testing is required |
| Log split view | Stored checkpoints; gossip, cross-logging, or witness comparison | No comparison means no generic detection |
| Backdated priority | Multiple observation receipts and checkpoint context | No exact global discovery time follows |
| Censorship or deletion | Multiple registries/mirrors; portable objects | Broad coercion can defeat availability |
| Rollback/freeze | Client state; freshness policy; explicit recovery epochs | First-contact and long-offline recovery need trust |
| Stolen issuer key | Key epochs; transparency; hardware protection; recovery events | Historical signatures prove key control only |
| Fake independent verification | Failure-domain genealogy; diversity policy | Much lineage remains self-asserted |
| Semantic mismatch/vacuity | Separate interpretations; boundary tests; adversarial review | Fidelity is not generally decidable |
| Alignment poisoning | Typed status; checked bridge proof; disputes | Concept mappings can remain inappropriate |
| Theorem spam/proof bombs | Admission, quota, size/cost declarations, resource limits | Openness and exclusion remain in tension |
| Ranking manipulation | Competing identified indexers; audit features | Proprietary rankings may remain opaque |
| Dependency compromise | Reverse-dependency closure; re-verification | Foundational incidents can be expensive |
| Adaptive private-query extraction | Query budgets, coarse predicates, DP/MPC/PIR as required | Useful answers inherently leak information |
| Commitment dictionary attack | Randomized hiding commitments | Public metadata can still reveal identity |
| Lost private keys/refusal to disclose | Threshold custody, VSS, escrow | Trustless fair exchange is not supplied by ZK |
| Governance capture | Separation of powers, timelocks, forkability, constituency rules | Plural systems can fragment or ossify |
| Cryptographic aging | Algorithm agility, recommitment, archival timestamps | Migration policy is itself governance-sensitive |

## 8. Hard limits and impossibility boundaries

- **Consensus is not truth.** It orders selected events under a fault model.
- **Formal validity is relative.** Checker acceptance is derivability under a declared environment and trusted base.
- **Semantic fidelity and general equivalence are not completely decidable** for expressive theories; no universal theorem canonicalizer exists.
- **Novelty is corpus-relative.** A defensible statement names corpus, relation family, search procedure, and cutoff.
- **Signatures prove key control, not authorship or causal provenance.**
- **Transparency conflicts with erasure.** Personal, illegal, or hazardous payloads should not enter immutable public logs.
- **Privacy conflicts with replication.** More replicas create more confidentiality failure points.
- **Permissionless admission conflicts with Sybil resistance.** Identity, scarce resources, reputation, or curation introduce cost or power.
- **Strong consistency conflicts with availability during partitions.** Global synchronous state is not an Evidence Profile v0 requirement.
- **Asynchronous Byzantine consensus needs additional assumptions for liveness.** Any BFT claim must state bounds, synchrony, and randomness.
- **Append-only logs and content hashes do not guarantee data availability.**
- **Zero knowledge does not provide query privacy or fair exchange by itself.**
- **No design guarantees liveness against a globally controlling adversary.**
- **Attestation counts are not calibrated probabilities of correctness.**

## 9. Trusted computing base inventory

Evidence Profile v0 must record and test at least:

1. logic and admitted axioms;
2. canonical Lean expression/export boundary;
3. Lean kernel source and binary;
4. imported declarations and their exact roots;
5. elaboration boundary, compiler, plugins, native or unsafe mechanisms;
6. environment builder, package resolver, acquisition trust, and sandbox;
7. CBOR/COSE/SCITT codecs and cryptographic library;
8. transparency-service VDS and receipt verifier;
9. client policy interpreter;
10. operating-system/container/hardware assumptions when relevant.

The report must distinguish what is mathematically trusted, cryptographically assumed, operationally trusted, merely asserted, and independently reproduced.

## 10. Incident semantics

An incident record must identify:

- affected object, key, checker, dependency, registry, or policy;
- event and discovery time sources;
- direct and transitive affected derivations;
- which attestations are invalidated, stale, or under review;
- unaffected alternative proofs or environments;
- recovery epoch and new trust roots;
- residual uncertainty.

Retraction is a reliance event, not deletion. Legal takedown may remove payload availability from a registry while preserving a minimally identifying event only when lawful and privacy-safe; global erasure cannot be promised after public replication.

## 11. Security evaluation gates

Evidence Profile v0 cannot claim its security property until it passes the mapped tests in [the supporting evidence-profile traceability matrix](../notes/TRACEABILITY.md), including mutation/substitution tests, independent clean replay, axiom-footprint validation, canonicalization fuzzing, split-view simulation, rollback/freeze tests, key recovery, dependency impact, resource exhaustion, schema upgrade, and credible export.
