# DTMKN Evidence Profile v0: protocol and object-model sketch

> **Priority note:** [Cooperation Core v0](COOPERATION-CORE-v0.md) is now the primary protocol. This document supplies optional/supporting exact-object, attestation, and transparency mechanisms. SCITT, detailed provenance, identity, and publication history are not required on the first research/reuse-testbed critical path. A `PUBLISH` event, registry admission, or SCITT receipt belongs only to the optional history plane: it is never a Cooperation Core demand decision, candidate admission, validation result, durable-promotion entitlement, or stable-support premise.

## 1. Status and scope

This document is a **non-normative pre-specification**. It fixes the semantics to test before choosing implementation libraries. Keywords such as MUST and SHOULD indicate intended future requirements but are not yet an interoperability standard.

Evidence Profile v0 supports Lean 4 claims, public artifacts, signed lifecycle assertions, local replay, transparency receipts, mirrors, and policy-scoped views. It does not support private objects, cross-proof-assistant transport, global consensus, or automatic semantic certification.

## 2. Design axioms

1. Formal derivability is decided by an identified local checker, never by registry or network consensus.
2. Immutable objects and signed events are primary; registry graphs and “current status” are derived views.
3. Claim identity, derivation identity, bundle identity, and semantic relation are distinct.
4. A signature authenticates an assertion by a key; a receipt authenticates registration; neither makes the assertion true.
5. Every guarantee is conditional on an explicit trust base and relying-party policy.
6. Missing or unavailable evidence yields `UNKNOWN`; an unexpected untrustworthy execution failure yields `ERROR`; neither yields `VERIFIED`.
7. Public objects are portable across registries and independently implementable.

## 3. Encoding and cryptographic profile

### 3.1 Canonical objects

Normative object bytes SHOULD use deterministic CBOR as specified by a frozen DTMKN profile of RFC 8949. JSON MAY be exposed as a human-readable derived view but MUST NOT determine identifiers unless a later profile explicitly selects RFC 8785 JCS.

For each schema-valid object \(o\):

\[
\operatorname{cid}(o)=H(
\texttt{"DTMKN"}\parallel
\operatorname{uvarint}(v)\parallel
\operatorname{typeTag}(o)\parallel
\operatorname{Canon}_v(o)).
\]

Requirements:

- `typeTag` and version are domain separators;
- the canonical profile is injective over valid data-model values;
- text is Unicode-normalized only where the schema says so; raw source artifacts remain byte-exact;
- maps, integers, tags, floats, and duplicate keys follow one deterministic rule;
- implementations reject unknown critical fields;
- golden vectors and differential parser fuzzing are mandatory;
- algorithm identifiers permit cryptographic migration without ambiguous reinterpretation.

The initial hash candidate is SHA-256 for ecosystem compatibility; final selection and multi-hash migration rules remain open for `CP-001`.

### 3.2 Evidence envelope

DTMKN SHOULD profile:

- SCITT signed statements and transparency architecture: RFC 9943;
- COSE receipts: RFC 9942;
- COSE signing: STD 96 / RFC 9052 family.

DTMKN must define payload media types and predicate schemas for publication, verification, challenge, relation, withdrawal, key status, and policy warning. A SCITT transparency service registers statements and issues receipts. Object storage, discovery, notification, verification computation, and semantic judgment remain adjacent services.

in-toto, SLSA, DSSE, and Sigstore assertions may be imported through adapters; Evidence Profile v0 should avoid two competing native signature envelopes.

## 4. Object model

### 4.1 Logical environment

Let:

\[
E_L=(\ell,d,a,n),
\]

where:

- \(\ell\) identifies the logic/foundation profile;
- \(d\) is the Merkle root of all declarations that determine meaning;
- \(a\) declares foundational axioms or trusted features made available by the environment;
- \(n\) records namespace and elaboration-context facts necessary to interpret the canonical statement.

`logicalEnvironmentID = cid(E_L)`.

The logical environment is separated from an execution environment. Changing an OS image or checker binary does not by itself change the formal proposition if the canonical logical environment is unchanged.

### 4.2 Formal claim

Let:

\[
C=(\operatorname{profile},\operatorname{logicalEnvironmentID},s),
\]

where \(s\) is the canonical fully elaborated proposition or an export with precisely specified interpretation.

\[
\operatorname{formalClaimID}=\operatorname{cid}(C).
\]

This identifies an exact proposition in an exact logical context. It is not an identifier for every semantically equivalent theorem.

### 4.3 Derivation

Let:

\[
D=(\operatorname{formalClaimID},p,\delta),
\]

where \(p\) is a proof artifact CID and \(\delta\) is the content root of the proof's declared dependency closure.

\[
\operatorname{proofID}=\operatorname{cid}(D).
\]

Alternative proofs of the same claim have distinct proof IDs. Their actual axiom and dependency footprint belongs in verification output, because it may differ from the declaration or across proof implementations.

### 4.4 Execution environment and checker

Let:

\[
E_X=(\operatorname{checkerID},\operatorname{toolchain},\operatorname{buildRecipe},
\operatorname{inputRoots},\operatorname{options},\operatorname{platform}).
\]

`checkerID` binds source, build provenance when available, binary digest, checker protocol version, and critical options. Evidence Profile v0 must record enough material to distinguish:

- source reproducibility;
- binary reproducibility;
- verification-result reproducibility;
- independent implementation or failure-domain diversity.

### 4.5 Interpretation

Let:

\[
I=(\operatorname{formalClaimID},i,\sigma,l),
\]

where \(i\) is an informal statement or explanation, \(\sigma\) is its source/citation set, and \(l\) identifies language and notation conventions.

An interpretation never inherits formal certification from its target claim. Fidelity is separately attested and may be disputed.

### 4.6 Provenance assertion

A provenance object is a W3C PROV-inspired typed DAG of entities, activities, agents, delegations, inputs, outputs, and software/tool identities. It MUST distinguish:

- human or organizational principal;
- signing/service principal;
- model family or claimed provider build;
- agent run and delegated task;
- verifier run;
- tool, retrieval corpus, proof library, binary, operator, and infrastructure lineage.

Fields without independent measurement are labeled `asserted`, not `observed`. Private chain-of-thought is not required; externally checkable inputs, outputs, tool calls, transformations, and attestations are preferred.

### 4.7 Bundle

A bundle is a manifest referencing a formal claim, zero or more derivations, interpretations, provenance assertions, licenses, disclosures, and auxiliary artifacts:

\[
B=(C,\{D_i\},\{I_j\},G,L,M).
\]

`bundleID = cid(B)`. Adding a proof, explanation, or provenance assertion produces a new bundle without changing the formal claim ID.

### 4.8 Typed theorem relation

Let:

\[
R=(C_1,C_2,\rho,\tau,\Gamma,\mathcal E),
\]

where:

- \(\rho\in\{\texttt{EQUIVALENT},\texttt{IMPLIES},\texttt{SPECIALIZES},\texttt{GENERALIZES},\texttt{TRANSPORTS},\texttt{DUAL},\texttt{USES},\texttt{SAME_SCHEMA},\texttt{ANALOGOUS}\}\);
- \(\tau\) is an explicit concept or theory translation;
- \(\Gamma\) is the context and side conditions;
- \(\mathcal E\) is evidence.

Relation status:

- `candidate`: retrieved or inferred probabilistically;
- `attested`: asserted by identified reviewers under a stated process;
- `certified`: checkable evidence establishes the exact typed relation.

For certified equivalence, evidence must establish:

\[
\Gamma\vdash \tau(C_1)\leftrightarrow C_2.
\]

For certified implication:

\[
\Gamma\vdash \tau(C_1)\rightarrow C_2.
\]

Similarity scores can generate candidates but cannot upgrade relation status.

### 4.9 Verification attestation

Let:

\[
A=(\operatorname{proofID},\operatorname{checkerID},\operatorname{executionEnvironmentID},
\operatorname{policyID},r,\alpha,\delta',m,q,f),
\]

where:

- \(r\in\{\texttt{ACCEPT},\texttt{REJECT},\texttt{ERROR},\texttt{UNKNOWN}\}\);
- \(\alpha\) is the measured axiom and unsafe-feature footprint;
- \(\delta'\) is the measured dependency footprint;
- \(m\) is the digest of the canonical deterministic checker-result and footprint record;
- \(q\) contains deterministic diagnostics and resource measurements;
- \(f\) records verifier failure domains and claimed independence metadata.

The signed attestation envelope binds all fields, its signer, key epoch, and signature algorithm. Signature and authorization validation are distinct: a valid signature proves which key asserted the bytes, while relying-party policy decides whether that key was authorized for the named checker, environment, and policy at that epoch. An attestation does not substitute for local replay. Policy is not included in the claim ID because different relying parties may apply different policies to the same formal object.

## 5. Lifecycle events

Events are immutable signed assertions:

\[
X=(\operatorname{kind},\operatorname{subjectRefs},\operatorname{payloadRefs},
\operatorname{actor},\operatorname{keyEpoch},\operatorname{actorSequence},
\operatorname{previousActorEvent}).
\]

Initial event types:

- `PUBLISH`: issuer makes a bundle or object discoverable;
- `ATTEST`: verifier or reviewer asserts a result;
- `CHALLENGE`: identified objection with evidence and scope;
- `SUPERSEDE`: new object or statement replaces a prior recommendation;
- `WITHDRAW`: issuer advises against reliance without erasing history;
- `POLICY_WARNING`: authority or curator reports a dependency, checker, legal, or safety issue;
- `KEY_STATUS`: rotation, compromise, recovery, or deauthorization;
- `MIRROR`: storage operator asserts possession or availability under a declared policy.

The current status of an object is a function of an event set and a relying policy. It is not a mutable field controlled by a global server.

## 6. Core protocol

### 6.1 Package

The publisher constructs canonical objects, verifies referential closure, creates a bundle, and signs a SCITT statement whose subject is the bundle or event CID and whose payload uses the appropriate DTMKN predicate.

### 6.2 Register

A registry or transparency service validates syntax and its admission policy, registers the statement, and returns a SCITT receipt. Registration means only that identified bytes and an issuer assertion appear in that service's history.

### 6.3 Store and mirror

Adjacent content-addressed storage retains objects. OCI/ORAS is the preferred transport candidate because it supplies typed manifests, registries, digests, and mature distribution. Mirrors fetch and verify objects before issuing storage assertions. An availability policy must name replica or erasure-code thresholds and freshness requirements.

### 6.4 Verify

A verifier:

1. validates object canonicalization and all CIDs;
2. resolves the full declared logical and proof dependency closure;
3. reconstructs the execution environment from pinned inputs;
4. validates checker identity and policy;
5. invokes the checker with resource limits;
6. enumerates actual axioms, unsafe mechanisms, and dependencies;
7. compares measured and declared reports;
8. emits a signed attestation and optionally registers it.

The outcome taxonomy is deterministic for the declared profile: a completed declared invalidity or malformedness check yields `REJECT`; missing or unavailable closure, declared incompleteness, nondeterminism without a permitted resolution, timeout, or declared resource exhaustion yields `UNKNOWN(reason)`; an unexpected checker crash, internal invariant failure, sandbox failure, corrupt runtime, or TCB-integrity alarm yields `ERROR(reason)`. `UNKNOWN` and `ERROR` never imply proof invalidity and require a new immutable attestation for retry.

### 6.5 Witness and monitor

Clients or witnesses retain checkpoints and validate receipts and append-only extensions under the selected VDS profile. Monitors exchange checkpoints or cross-log them. If incompatible signed views meet, they emit portable fork evidence.

Evidence Profile v0 initially claims **fork accountability after view intersection**, not universal fork detection. A stronger \(3f+1\) witness configuration with \(2f+1\) cosigned checkpoints may later prevent two quorum-certified conflicting checkpoints if at most \(f\) witnesses are Byzantine and honest witnesses sign only valid extensions.

### 6.6 Relate

Agents or humans publish relation candidates. Bridge provers and reviewers add evidence. Registry views display each relation type, context, translation, evidence, and status. Disagreement creates additional assertions; it does not overwrite the prior edge.

### 6.7 Challenge and recompute

Challenges, withdrawals, key compromise, or dependency warnings trigger policy-scoped impact recomputation. The service identifies affected **derivations and attestations**. It must not infer that all associated propositions are false; an alternative derivation or environment may survive.

## 7. Client acceptance

For relying policy \(P\), let receiver-controlled replay of \(D\) under an explicitly selected checker \(k\) and execution environment \(e\) return either no trustworthy record or the authoritative record

\[
\mathcal R=
(r^*,p^*,k^*,e^*,P^*,\alpha^*,\delta^*,m^*).
\]

Here \(p^*\) is the proof ID computed from the exact replay input; \(k^*\) and \(e^*\) are measured from the receiver-selected replay contract rather than copied from a claimant; \(\alpha^*\) and \(\delta^*\) are the replay-observed axiom/unsafe-feature and dependency footprints; and \(m^*\) is the digest of the canonical deterministic checker-result and footprint record. Missing closure, an unmeasured critical field, or an integrity failure produces no acceptance record.

Define exact attestation reconciliation by

\[
\begin{aligned}
\operatorname{AttestationMatches}_P(A,\mathcal R):={}&
\operatorname{SignatureValid}(A)
\land\operatorname{AttesterAuthorized}_P(A)\\
&\land A.r=r^*=\texttt{ACCEPT}
\land A.\operatorname{proofID}=p^*\\
&\land A.\operatorname{checkerID}=k^*
\land A.\operatorname{executionEnvironmentID}=e^*\\
&\land A.\operatorname{policyID}=P^*
\land A.\alpha=\alpha^*
\land A.\delta'=\delta^*
\land A.m=m^* .
\end{aligned}
\]

For the local-replay-with-corroborating-attestation path, a client accepts a formal derivation only if:

\[
\begin{aligned}
\operatorname{Accept}^{\mathrm{local+att}}_P(D,A,X;k,e)= {}&
\operatorname{CIDsValid}(D)\land
\operatorname{ClosureResolved}(D)\land
\operatorname{Replay}_P(D;k,e)=\mathcal R\\
&\land p^*=\operatorname{cid}(D)
\land r^*=\texttt{ACCEPT}\\
&\land\operatorname{CheckerAllowed}_P(k^*)
\land\operatorname{EnvironmentAllowed}_P(e^*)\\
&\land P^*=\operatorname{policyID}(P)
\land\operatorname{AxiomPolicy}_P(\alpha^*)
\land\operatorname{DependencyPolicy}_P(\delta^*)\\
&\land\operatorname{AttestationMatches}_P(A,\mathcal R)\\
&\land\operatorname{EventsBoundTo}_P(X,p^*,\operatorname{cid}(A))
\land\operatorname{EventPolicy}_P(X)
\land\operatorname{Freshness}_P(X).
\end{aligned}
\]

The attestation is optional corroboration for a receiver that has replayed locally: omitting \(A\) removes only the `AttestationMatches` and attestation-event-binding conjuncts, never any replay-derived conjunct. In particular, axiom and dependency policy is always applied to \(\alpha^*\) and \(\delta^*\), not to unbound claimant fields.

A client may choose attestation-only operation for performance, but it then applies the same exact proof/checker/environment/policy/result/footprint binding to a signature- and authority-validated attestation and explicitly trusts that verifier's measurement. That mode must be labeled `TRUSTED_ATTESTATION` and must not be represented as local replay or as strict-P0 mechanical closure.

## 8. Federation semantics

- No globally synchronous state or total event order is required.
- Immutable objects and signed facts merge by set union when available.
- Challenges, incompatible interpretations, and competing semantic relations coexist.
- A registry computes a local materialized view from its admitted event set and policy.
- CRDT techniques are suitable only for monotone or explicitly multi-value metadata; they do not resolve semantic disputes.
- Consensus is reserved for narrow noncommutative decisions such as a fixed-membership registry's authority set, namespace assignment, governance action, or payment.
- Cross-registry “priority” means observed by identified services/checkpoints under stated time assumptions, never first discovery worldwide.

## 9. Core invariants

1. **Type-separated content binding:** equal CIDs imply equal typed canonical values except with negligible collision probability.
2. **Referential closure:** every material reference resolves to the stated CID.
3. **No mutable dependencies:** finalized derivations never resolve `latest`, branch heads, or unpinned URLs.
4. **Conditional derivational soundness:** checker acceptance implies derivability relative to the declared logic and axioms, assuming checker soundness.
5. **Attestation binding:** no attestation transfers to another proof, checker, policy, or environment.
6. **Epistemic separation:** formal, semantic, historical, institutional, and availability evidence remain distinct.
7. **Certified-edge discipline:** a certified relation has locally checkable, endpoint-bound evidence.
8. **Append-only lifecycle:** correction changes reliance through new events and never overwrites history.
9. **Pinned checkpoint monotonicity:** later log views extend a stored checkpoint or invoke an explicit recovery procedure.
10. **Fork accountability:** compared incompatible signed views yield transferable evidence.
11. **Fail closed:** uncertainty never becomes acceptance.
12. **No global authority by implication:** inclusion, votes, or attestation counts do not alter kernel results.

## 10. Versioning and recovery

- Schema versions and type tags are immutable.
- New clients may support multiple old profiles; migrations create new objects linked by `SUPERSEDE` or explicit conversion evidence.
- Hash or signature migration uses dual commitments during a published transition window.
- Key epochs distinguish historical signatures from prospective authorization.
- A compromised transparency-service key invokes an explicit rollback/recovery epoch consistent with the selected SCITT/VDS profile.
- Emergency registry policy cannot make old bytes disappear from honest mirrors.

## 11. Open design questions for CP-001

1. Which Lean export is canonical enough for a formal claim: kernel expression, environment slice, source declaration, or a two-level representation?
2. How is the logical declaration root computed without binding irrelevant library content?
3. Can actual dependency extraction be complete for every accepted Lean feature?
4. Which deterministic CBOR profile and multihash rules are frozen?
5. Which SCITT VDS and transparency implementation are practical for the prototype?
6. What does a witness sign, and is Evidence Profile v0 detect-only or quorum-preventive?
7. Which failure-domain fields are measurable rather than self-declared?
8. What exact reliance-policy language is expressive but auditable?
9. How are resource limits specified so proof bombs fail consistently?
10. What minimum archival package permits verification after toolchain disappearance?
