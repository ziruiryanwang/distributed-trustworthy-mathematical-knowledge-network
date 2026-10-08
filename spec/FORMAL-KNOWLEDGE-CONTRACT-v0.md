# Formal knowledge contract: corpus-first version one

Date: 2026-09-19  
Status: Proposed concept contract, independently reviewed for concept consistency; see the audit disposition  
Scope: Mathematical knowledge collection and reliable reuse, without human-intention processing or an unsolved-mathematics task registry  
Implementation: None; this document contains definitions and paper obligations only

## Authoritative scope refinement

The user's latest scope is decisive:

> People and agents investigate independently and interact with the system. Version one gathers mathematical knowledge. It contains no human-intention layer and no list of unsolved mathematics tasks.

This document specializes and, where necessary, overrides the broader CP-001C concept for version one. Earlier descriptions of research-task lifecycles, semantic-intent parents, fidelity reviewers, and task-solving evaluations do not become mandatory features of this version.

The system is a mathematical corpus and exchange protocol, not a research manager. Its clients may be people, independent automated researchers, proof assistants, or other software. How a client chooses its investigations is outside the protocol.

The core cycle is:

\[
\text{available formal corpus}
\longrightarrow\text{independent investigation}
\longrightarrow\text{candidate formal artifact}
\longrightarrow\text{local verification}
\longrightarrow\text{publication and independent reuse}.
\]

The investigation occurs outside the knowledge-admission boundary. Neither its motivation nor a record of its desired outcome is required.

## What is deliberately absent

The version-one system excludes:

- human-language mathematical input or translation service;
- human-intention field, interpretation reviewer, or fidelity grade;
- question-answer relationship or claim that an artifact answers someone's question;
- global or local registry of unsolved mathematical tasks;
- producer work-item identifier, originating conjecture ticket, or research-program membership;
- common research agenda, root goal, or central chooser of worthwhile mathematics;
- natural-language explanation, novelty judgment, or importance score as a condition of mathematical validity.

The system need not know why an artifact was generated. No corresponding unsolved question must have been registered before publication.

Finite queues for downloads, verification, indexing, and storage repair are operational service queues. They are not unsolved-mathematics task lists. A prover may internally manipulate a goal stack while constructing a proof; that is an implementation detail of an independent client, not a registry required by the corpus.

## Core object: an established formal result

For the theorem case, represent the mathematical content conceptually by

\[
c=(L,E,\Gamma,\varphi,p,D,v).
\]

Here \(L\) is the exact formal logic profile; \(E\) the exact declaration environment; \(\Gamma\) the typed hypotheses; \(\varphi\) the formal statement; \(p\) the proof or admitted native certificate; \(D\) the required dependency closure; and \(v\) the versioned checking/encoding profile.

All semantically relevant parameters, universes, coercions, instances, and definitions must be bound by that representation. Its content identity must not depend on the investigation that produced it.

The fundamental judgment is

\[
E;\Gamma\vdash_L p:\varphi.
\]

It says what the evidence establishes. It says nothing about what a person wanted, how the result was found, whether it is surprising, or whether anyone has already used it.

Formal identifiers may happen to be spelled with English words. Their meaning here is their exact role in the formal environment, not an interpretation of their English spelling. A formal textual grammar is not a natural-language interface.

### Other admitted mathematical kinds

| Kind | Formal admission question |
|---|---|
| Definition | Does the declaration satisfy the chosen foundation's definition/extension rules? |
| Theorem | Does the supplied evidence establish the exact contextual judgment? |
| Construction | Does the supplied term inhabit the stated type and satisfy its stated verified properties? |
| Counterexample | Does the exact witness satisfy the conditions that refute the specified formal assertion? |
| Certified computation | Does the certificate establish the exact bounded relation under the admitted checking basis? |
| Formal relation | Does checked evidence establish the stated implication, equivalence, specialization, or representation map? |

An axiom declaration describes an assumption in a theory; it is not a proof of that assumption in a weaker theory. A definition with unproved properties supplies only the checked declaration, not those properties.

The v1 corpus is for checked content. A received unproved conjecture or unfinished draft remains outside it, in bounded ingress pending a disposition or in an external client's private workspace. V1 has no persistent conjecture catalogue or partial-task registry. A completed conditional theorem is different: its hypotheses are explicit mathematical content, not promises that the system will later solve them.

## Separate the mathematical judgment from operational decisions

Four distinct questions remain even without human intention:

| Layer | Question | What must not be inferred |
|---|---|---|
| Formal verification | What exact judgment does this evidence establish? | Usefulness, novelty, or unconditional truth in every foundation |
| Local admissibility/reliance | Is this basis currently allowed and is the required evidence available under this node's policy? | Universal acceptance by other nodes |
| Resource admission | Will this node spend resources to check, index, store, or serve the object? | Invalidity merely because service was declined |
| Reuse value | Does this material make subsequent independent investigation easier or more capable? | Invalidity merely because no benefit is known yet |

Mathematical eligibility must not require demonstrated usefulness. Otherwise a valuable unexpected result could be excluded simply because no application has yet been observed.

Conversely, mathematical eligibility cannot entitle its publisher to unlimited storage or attention from other participants. Exact deduplication, admission ceilings, and retention choices govern scarce resources without redefining truth.

### Verification outcome is not a truth vote

A native check can produce acceptance, rejection of the supplied evidence, an unsupported-profile outcome, or a resource-bounded nondecision. Failure to find or check a proof within budget does not refute the statement.

The verifier must check the declared relation, not merely parse the text, validate a signature, match a hash, or trust another node's verdict. Native checking remains relative to a specified trusted computing base.

### Knowledge is explicitly contextual

Under a sound implementation of the stated checking relation,

\[
\operatorname{Check}_{v}(c)=\texttt{ACCEPT}
\Longrightarrow E;\Gamma\vdash_L p:\varphi.
\]

A semantic truth conclusion additionally needs the ordinary mathematical assumption that the chosen interpretation satisfies the foundation and hypotheses. No human-language translation service is needed to state this conditional.

A correct classical checker may validate

\[
E;\{P,\neg P\}\vdash 0=1.
\]

That is not a proof of the unqualified arithmetic statement \(0=1\). Dropping its hypotheses would change the result. Similarly, adding \(\psi\) as a new axiom and deriving \(\psi\) does not establish \(\psi\) in the preceding foundation.

The system must therefore expose a verified transitive axiom and trust-feature footprint. It must not add a universal consistency test: consistency is not generally decidable for arbitrary expressive theories. An initial implementation can support a limited explicit foundation profile while preserving the design's ability to distinguish additional profiles later.

## Intent-independent and task-independent knowledge recognition

Fix the mathematical payload, exact environment, checker profile, local evidence policy, available closure, and relevant local state. Then changing or removing all external information about who wanted what, which question was being investigated, or whether a work item exists must not change formal verification.

Write \(m\) for those exact mathematical inputs, and \(h\) for external research-history information. The required factorization is

\[
\operatorname{FormalCheck}(m,h)=\operatorname{FormalCheck}(m).
\]

In version one, \(h\) is not an input to the core operation at all.

This is stronger and simpler than asking a fidelity reviewer to approve every result. No reviewer has to decide that a verified theorem matches an investigation's purpose. The theorem is recorded as the theorem actually checked.

### Conditional proposition: standalone contribution safety

Assume the parser, environment binding, footprint extraction, native checker, and local admission evaluator satisfy their stated specifications. Suppose an independently supplied artifact passes the ordinary native verification and local evidence policy.

Then it is eligible for recognition as that exact contextual mathematical result without any producer work item or previously registered unsolved task.

Proof sketch: the admission premises refer to the artifact's formal judgment, evidence, closure, and local policy. None refers to an originating research intention or task. Adding an origin requirement would therefore be a different, nonconforming v1 rule. Publication, durable retention, and service still require their separate finite resource decisions.

This proposition is conditional on correct implementation of its premises. It does not prove that every checker is sound, every foundation is consistent, or every valid result is valuable.

## Compatibility with inherited local reliance

The frozen Core already permits standalone mathematical artifacts and absent-by-tag semantic-intent/fidelity references. Its task-related machinery is not a prerequisite for every theorem. V1 does not expose intention or task fields; an internal adapter to the broader historical Core fixes any such legacy fields to their canonical absent tags. It must not expose them as optional v1 features.

To reuse its strict evidence semantics, derive a purely mathematical checking contract \(q_c\) from the submitted artifact and the receiver's native evidence policy. It binds the exact contextual judgment, allowed axioms, checker basis, closure, and current defect policy. It contains no human-intention reference.

The inherited invariant remains

\[
\operatorname{Rely}_i(c,e)
\Longrightarrow
\operatorname{Stable}_{P_i(e)}(q_c;A_i(e),O_i(e)).
\]

Here \(q_c\) is a machine checking contract for an existing candidate result. It is not an unsolved research question, an instruction to generate a theorem, or an entry in a mathematical task registry.

Successful checking records a formal-result assessment. Current reuse additionally checks that the selected evidence path remains active and its closure available. A later admitted checker defect can disable that path; an independently valid alternative proof can remain usable.

The v1 protocol excludes task-completion and informal-intent assessments. Those broader assessment types are not v1 operations, optional extensions within the v1 profile, or stored relations in its corpus.

## A corpus-first abstract lifecycle

The required semantic operations are:

1. **Read and discover:** retrieve existing exact objects or bounded structural candidates.
2. **Submit:** provide a candidate artifact and its exact required closure or retrieval references.
3. **Check:** verify its mathematical kind, exact evidence, environment, and footprint within admitted resources.
4. **Record:** store a local assessment of the exact result, separate from current availability and retention.
5. **Retain and index:** admit selected objects into receiver-funded storage and machine-readable indexes.
6. **Advertise and serve:** make retained objects available to willing peers, without imposing their acceptance.
7. **Import independently:** another node resolves the closure and applies its own native checking policy.
8. **Correct and preserve:** handle defects, alternative proofs, missing dependencies, and funded repair.

Independent investigation is not a protocol transition that the server must schedule. A client can use any method, pause indefinitely, never publish, or publish a result unrelated to its previous interactions.

The contents can be represented as a typed graph or hypergraph of definitions, environments, evidence, and formally justified relations. Different proofs of one statement may coexist. A global block order and a global catalogue of pending problems are unnecessary.

### Discovery without natural language

Candidate lookup can use exact identifiers, types, declarations, formal expression structure, applicable interfaces, verified specializations, and dependency relationships. A client can ask for existing material matching a structural predicate without asking the commons to solve an unsolved mathematical problem.

Unification, indexing, bounded normalization, and learned representations of formal syntax can propose candidates. In expressive logics, not all applicability or equivalence questions are decidable; bounded candidate search must report its limits. Candidate similarity never authorizes a substitution.

For actual reuse, the receiving prover checks the required formal instantiation or transport. This is a formal-to-formal interface, not a human-language interpretation step.

## Mathematical growth without an unsolved-task list

The corpus can grow through independently supplied:

- new checked statements and proof paths;
- useful definitions and abstractions;
- stronger generalizations or weaker sufficient hypotheses;
- constructive witnesses and certified counterexamples;
- checked relations between previously separate developments;
- smaller or cheaper evidence for an existing result;
- better formal interfaces and dependency packaging.

None needs a centrally assigned research question. A result's formal admission does not wait for a demonstrated application.

Mathematical correctness and meaningful growth are nevertheless different. Generating many instances of \(n=n\) can satisfy the first without demonstrating the second. No universal novelty or importance oracle is introduced.

Operational observations can measure distinct contextual judgments, exact duplicate rates, evidence size, native checking cost, dependency availability, cross-client imports, checked generalizations, and recurring reuse. These diagnose accumulation; none alone proves an increase in mathematical capability.

An independent evaluator may later compare research trajectories with and without access to prior corpus snapshots, with declared resources and controls. That is an external study, not a protocol task list or an admission criterion. The previous task-based testbed remains historical experimental work, not the definition of this corpus or a required v1 service.

The near-term claim to establish is narrower than exponential growth: formal results survive an independent producer-to-consumer boundary, and independently produced successors can take the same path. Whether this repeatedly produces accelerating useful mathematics remains empirical.

## What removing intention does and does not simplify

It removes a mandatory informal-to-formal translation boundary, semantic reviewers, intended-question tracking, and the risk that such assessments gate otherwise valid results. The core can be specified entirely with formal objects and machine-checkable relations.

It does not remove:

- the correctness assumptions of parsers, kernels, certificate checkers, and execution;
- exact foundation, context, version, and dependency binding;
- the need to distinguish new axioms from theorems;
- representation mismatch between independently built libraries;
- missing proof closure, partitions, finite storage, or valid-junk overload;
- the difficulty of autonomous investigation and useful abstraction;
- the difference between publicly reusable evidence and opaque attestations.

An LLM is neither required by the corpus nor granted evidential authority. Clients may use language models, purely symbolic systems, or people entering formal material. The public interface need not observe or regulate their private reasoning. A claim that no client internally uses natural language would be unnecessary and generally not enforceable.

## Paper obligations for version one

| ID | Required statement or counterexample |
|---|---|
| FK-RESULT | Every accepted mathematical kind has an exact independently checkable relation and declared foundation |
| FK-ORIGIN | Formal recognition is independent of producer intention, work item, question, and research agenda |
| FK-NOTASK | Every core operation is meaningful without a registry of unsolved mathematical tasks |
| FK-CONTEXT | No publication or import silently drops hypotheses, strengthens foundations, or changes declarations |
| FK-NOAXIOM-LAUNDERING | Adding an assumption cannot masquerade as a proof from the prior foundation |
| FK-STANDALONE | A fully checked standalone artifact can enter the candidate exchange path without task registration |
| FK-NATIVE | No translation model, human reviewer, or natural-language field is a mandatory native checking input |
| FK-RESOURCE | Declining resource service does not assert mathematical falsity; correctness does not mint resource rights |
| FK-REUSE | Actual formal substitution or transport is checked, even though no human intention is evaluated |
| FK-STATUS | Historical checking, current allowed reliance, availability, retention, and heuristic utility stay separate |
| FK-RECIPROCAL | Independent clients can both consume and supply the same portable mathematical object forms |

These remain obligations to refine, not completed mechanized proofs.

## Trace

- [CP-001C checkpoint](../notes/checkpoints/CP-001C-reciprocal-mathematical-commons.md).
- [Broader reciprocal-commons concept](RECIPROCAL-COMMONS-CONCEPT-v0.md).
- [Formal-native architecture analysis](../notes/analyses/CP-001C-formal-native-architecture.md).
- [Formal-native investigation analysis](../notes/analyses/CP-001C-formal-native-research.md).
- [Audit disposition](../notes/audits/CP-001C-AUDIT-DISPOSITION.md).

Earlier frozen documents remain unchanged. The scope refinement in this contract is explicit so that preserving their historical trace does not force their broader task/intention features into version one.
