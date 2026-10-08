# Layered problem decomposition for a mathematical knowledge commons

Date: 2026-09-19  
Status: Proposed decomposition for conceptual review; no implementation  
Scope: Corpus-first v1, with external independent investigators, no human-intention processing, and no unsolved-mathematics task registry

## Judgment on the proposed division

The user's distinction between reliable knowledge infrastructure and efficient, meaningful accumulation is the right primary separation. A system can store only valid results and still accumulate material that is expensive, redundant, hard to find, or unhelpful. Conversely, a productive-looking system can silently rely on false or mismatched results.

Two refinements make the division more precise:

- Separate formal correctness from distributed persistence and availability. They fail differently and require different assumptions.
- Separate organization/reuse mechanisms from the harder question of growth. Good indexing, checked relations, and representation sharing are concrete engineering problems; whether they produce compounding mathematical capability is a further hypothesis.

Identity, authentication, and human intention should not be bundled into one third layer. Authentication is needed wherever operational authority exists. Political identity and attribution can remain outside the core. Human intention is entirely outside v1; it can influence an external investigator's choices, not the system's knowledge-recognition rules.

## Four logical layers, grouped into two main research problems

| Main problem | Layer | Central question | Principal output |
|---|---|---|---|
| Reliable mathematical corpus | L1: Formal content and verification | Exactly what mathematical content has been established, under which assumptions? | Context-bound checked results and formally justified relations |
| Reliable mathematical corpus | L2: Decentralized preservation and service | Can independent nodes obtain, retain, exchange, and safely operate on those objects? | Recoverable packages and honestly scoped service/status claims |
| Efficient meaningful accumulation | L3: Organization, discovery, and reuse | Can earlier material be found, compared, combined, and represented economically? | Useful indexes, candidate retrieval, checked adapters, shared representations |
| Efficient meaningful accumulation | L4: Growth and resource-efficiency policy | Is the changing corpus becoming a better reusable mathematical resource at an acceptable cost? | Explicit diagnostics, bounded policies, experiments, and scoped growth claims |

These are logical responsibility and authority boundaries, not four servers and not a demand to implement them in sequence. All four can coexist in one node. They also have service dependencies in both directions.

For example, a verifier needs stored bytes, a search engine needs indexes, and retention policy needs resource measurements. None of those service dependencies makes a provider, index, or ranker an authority on mathematical correctness.

## L1: Formal content and verification

### Subject matter

L1 defines formal object kinds, exact foundation/environment identity, hypotheses, derivations, definition rules, constructions, counterexamples, and checked relations. It specifies what the checker must establish:

\[
E;\Gamma\vdash_L p:\varphi.
\]

Its inputs do not include a human intention, originating question, research-task identifier, popularity, or novelty score. The accepted content is the content actually checked.

### Core conditions

- Exact binding of statement, assumptions, definitions, versions, and evidence.
- Verified transitive axiom and trust-feature footprints.
- No hidden axioms, unchecked holes, or theorem imports treated as unquestioned facts.
- Checked formal substitution and transport.
- Finite grounded evidence; mutually citing unsupported claims cannot certify themselves.
- Explicit checker and foundation assumptions.
- Current reliance responsive to locally admitted defects, with clean alternative evidence preserved.

L1 must distinguish a valid conditional theorem from an unconditional statement. It must also distinguish rejecting a supplied proof from refuting its conclusion.

### Methods and proof obligations

Small proof kernels, typed native representations, certificate-producing solvers, checked module interfaces, and independently implemented validators are relevant. Formal methods can specify and test the admission invariant and its implementation refinements.

Succinct cryptographic proofs are an optional later optimization for a precisely encoded relation. They do not remove relation/checker assumptions or make unavailable native material reusable. The present strict native-evidence profile is not silently enlarged.

The principal paper obligation is sound composition relative to the declared foundation and trusted components. It is not an unconditional proof that every conceivable formal theory describes true mathematics.

## L2: Decentralized preservation and service

### Subject matter

L2 concerns content addressing, complete dependency closures, peer discovery, transfer, replication, archives, recovery, bounded ingress, and local operational state. No mandatory central server, universal membership registry, or global theorem ledger is required.

It distinguishes:

- an exact object identifier;
- a past observation of the bytes;
- current local possession;
- a scoped provider/retention commitment;
- reconstructibility under a stated failure model;
- a currently reachable willing provider.

None implies all the others.

### Core conditions

- Native replay from captured immutable closure without live producer callbacks.
- Replaceable bootstrap, indexes, relays, and storage providers.
- Receiver-owned resource admission; foreign messages do not allocate local resources.
- Recoverability claims bound to explicit failure domains, terms, and repair assumptions.
- Offline operation from retained material.
- Scoped observation and freshness; no instantaneous global completeness claim.
- No loss of mathematical identity when changing service providers.

An all-malicious peer set need not defeat a correct local checker, but it can defeat remote discovery and availability. Correctness safety and useful progress have different assumptions.

### Methods and proof obligations

Content-addressed storage, Merkle commitments, authenticated scoped feeds, peer transport, anti-entropy, replication, erasure coding, and optional DHT/index overlays are candidate tools. Their adopted profiles need exact threat and load models.

Consensus is potentially useful for a shared budget, exclusive lease, or mutable authority state within an optional group. Ordinary theorem publication has no inherent double-spend conflict requiring one network-wide block order.

Formal arguments can establish local invariants and conditional recovery/delivery properties. They cannot establish availability after every copy or willing route disappears.

## L3: Organization, discovery, and reuse

### Why this deserves its own layer

Having valid, available objects is insufficient if each investigator must rediscover their contents or pay excessive integration cost. Conversely, the growth problem should not be left as an undefined demand that the network somehow produce important mathematics.

L3 supplies specific mechanisms that can improve the usefulness of an existing corpus without claiming to decide all mathematical value.

### Three kinds of repeated material

| Repetition | What can be established | Appropriate treatment |
|---|---|---|
| Exact duplicate | Same canonical content, subject to the hash/binding assumptions | Deduplicate storage and idempotently handle repeated announcements |
| Equal or related under a declared formal relation | Checked normalization, equivalence, implication, specialization, or representation map | Add the certified relation and share representations when its contract permits |
| Apparently redundant or unhelpful | Heuristic similarity, low demand, repeated proof patterns, estimated low value | Advisory grouping/ranking and bounded retention decisions; no mathematical rejection |

A second proof of the same statement may use fewer axioms, check faster, avoid a defective kernel path, be constructive, or expose a reusable intermediate lemma. Treating every repeated conclusion as rubbish can destroy useful evidence.

Similarly, a general theorem and its specialized instance can both be worthwhile when the specialized proof is much cheaper to find, elaborate, or verify.

There is a stronger reason not to quotient knowledge by arbitrary propositional equivalence. Given closed proofs \(p:P\) and \(q:Q\), one can prove \(P\leftrightarrow Q\) by the constant functions \(\lambda\_:P.\,q\) and \(\lambda\_:Q.\,p\). Thus every pair of already proved closed propositions is equivalent in this sense, even when the theorems expose very different useful mathematical structure. Such equivalence does not mean they are interchangeable representations at the same cost or should share one content identity.

Useful redundancy contracts must therefore name what is preserved: parameters, interfaces, exact exported judgments, assumptions, constructions, proof paths, and bounded reconstruction costs. A certified relation is knowledge; it is not by itself permission to erase its endpoints.

### Methods allowed here

Formal expression indexes, type/signature indexes, bounded normalization, checked substitutions, certified equivalences, proof-DAG sharing, reusable modules, formal library maps, and receiver-local caches are candidates.

LLMs and other learned methods may propose clusters, equivalent statements, generalizations, abstractions, premise matches, and likely duplicate proofs. They may rank what to inspect next. They are useful precisely because general organization is difficult.

Their epistemic boundary is strict:

- A proposed equivalence becomes a mathematical relation only after the required proof is checked.
- A proposed proof substitution must satisfy its exact formal contract.
- A similarity score does not authorize theorem merging.
- A search returning no result does not prove mathematical nonexistence.
- A heuristic deletion proposal cannot claim lossless preservation without the required preservation evidence.

V1 does not ingest human intention even when an index or proposal engine uses an LLM. A system-side learned component can consume formal artifacts and operational signals. External clients may use any private reasoning method.

### Compression is a formal contract, not a synonym for forgetting

Fix a finite retained collection and its required exported judgments \(\mathcal J\). An exact-storage transformation must reconstruct the promised original bytes. A proof-preserving representation transformation may instead supply new checked evidence for every designated judgment under the same admitted foundations and exact contexts or explicitly checked transports.

These promises are different. A different proof cannot be served under the old proof's immutable content identifier. Nor does proof-preserving compression discharge a separate promise to retain original bytes.

For a resource envelope \(b_j\), a stronger preservation condition is

\[
\operatorname{Preserve}_{\mathcal J,\mathbf b}(K,K')
\iff
\forall j\in\mathcal J,\ 
\exists p_j\text{ recoverable from }K'
\text{ within }b_j:
\operatorname{Check}(j,p_j)=\texttt{ACCEPT}.
\]

The environment, dependency availability, recovery procedure, native checking basis, and budgets are part of the contract. The bound covers the declared lookup, fetching, reconstruction, and checking work, not merely producing a pointer. \(\mathcal J\) names already established exported content, not unsolved mathematical tasks.

Storage, recovery, transfer, and checking costs must include new definitions, bridges, decoder/expander machinery, and additional dependencies. A smaller displayed proof with a large hidden decoder is not automatically an improvement.

Some storage policies intentionally discard coverage. They may be legitimate under their retention terms, but must be described as lossy selection rather than certified preservation.

## L4: Growth and resource-efficiency policy

### What should not define growth

The number of theorem strings, proof bytes, registered agents, dependency edges, downloads, or newly coined definitions is insufficient. All can increase rapidly without making the corpus a better resource.

There is also a deeper distinction: when a foundation is fixed, a newly discovered theorem was already in its logical consequence set. A corpus can gain computational knowledge without adding logically independent information.

The gain is that a result becomes explicit, retrievable, checkable, composable, or substantially cheaper to reconstruct. That is not captured by counting independent axioms or asserting that every theorem contributes new entropy.

### A plural operational account

Growth should initially be reported as several scoped properties, not one universal scalar:

- **Coverage:** more exact checked content or formally certified relations are available in declared mathematical regions.
- **Accessibility:** existing content is easier or cheaper to find and obtain.
- **Reusability:** independently operated clients can use interfaces and constructions with lower integration cost.
- **Representation efficiency:** required content is preserved with better resource tradeoffs.
- **Robustness:** useful closures and alternative valid evidence survive provider failures or checker incidents.
- **Circulation:** newly supplied content appears in later independently checked developments.

The first can be inflated with trivial results; the last does not prove causal benefit. Each measure therefore needs a declared scope and limitations. None is a condition that every valid result must meet to count as formal mathematical content.

### Efficiency without arbitrary units

For a declared comparison and preservation scope, measure a vector such as

\[
\mathbf C=
(\text{storage},\text{network transfer},\text{checking compute},
\text{lookup compute},\text{integration cost},\text{maintenance}).
\]

One representation can improve storage while worsening checking latency. A componentwise improvement is a stronger claim than a gain under a chosen price vector. Both are legitimate if the comparison, costs, and preserved content are stated.

Policies may optimize local priorities with any useful technique: formal analysis, online algorithms, caching, learned ranking, LLM-generated abstractions, or hybrid search. Those policies cannot redefine L1 validity or escape L2 resource authority.

### What this layer does not do

L4 is not a central research scheduler. It does not allocate unsolved mathematics questions to participants or require them to explain their motivations. External investigators continue to decide what to investigate.

Its system-side functions are organization/retention policy, exposure and resource diagnostics, and transparent reporting of limited accumulation properties. Claims of productive or exponential growth require separate evidence; they are not protocol axioms.

The difficult research problem remains: how to preserve and expose promising new structure without paying indefinitely for all valid variants or suppressing rare work with delayed value.

No universal decidable semantic novelty test is assumed. In an expressive theory with undecidable theoremhood, deciding every provable equivalence would already solve an undecidable problem. Checking supplied equivalence proofs remains possible.

## Cross-cutting controls, not a postponed third layer

| Concern | Necessary role | Boundary |
|---|---|---|
| Operational authentication | Authenticate resource grants, authorized updates, service principals, and scoped commitments where used | A signature does not establish a theorem or unique human identity |
| Resource accounting and isolation | Bound all expensive checking, indexing, network, storage, repair, and untrusted tool execution | Correct results and many identities do not mint capacity |
| Exact version and dependency trace | Determine what was actually checked and what an incident affects | Technical dependency tracking is not political credit allocation |
| Recovery and observability | Report current local state, failure, and uncertainty accurately | No global latest/completeness guarantee under arbitrary partitions |
| Political identity, authorship, priority, and prestige | Not needed for native mathematical recognition | Outside the v1 core |
| Human intention | May influence external investigators' private choices only | Not a system input, stored relation, score, or assessment |

Authentication mechanisms depend on the operations offered. An entirely local anonymous verifier needs no author authentication; a service that honors signed storage grants must authenticate the grant authority. This is why authentication cannot simply be deferred together with attribution.

## Authority flow and forbidden shortcuts

The important relationships are:

1. L2 delivers bytes; L1 independently establishes what they prove.
2. L3 proposes useful matches or relations; L1 checks any relation used as mathematics.
3. L4 proposes priorities or representation policies; L2 enforces the authorized resource envelope.
4. Current usable knowledge combines L1's checked evidence with L2's available closure and local incident state.
5. L3/L4 observations may guide external clients, but no shared research assignment follows.

Forbidden shortcuts include treating replication as truth, ranking as proof, a model's equivalence claim as a merge certificate, a retention decision as refutation, or publication volume as demonstrated knowledge growth.

## Development of the concept, not implementation order

The next conceptual work should first freeze the L1 object/checking contract and the L2 fault/resource assumptions. In parallel, define several L3 mechanisms with exact preservation boundaries and several L4 diagnostics with counterexamples.

Then examine paper traces combining the layers: an independent contribution; duplicate arrival; a checked generalization; alternative proofs with different footprints; loss of a provider; a discovered checker defect; an overloaded receiver; and a compression that trades checking cost against bytes.

This produces a concrete research agenda without introducing a research-task list into the software. No coding is authorized by this note.

## Related checkpoint material

- [Formal knowledge contract](../../spec/FORMAL-KNOWLEDGE-CONTRACT-v0.md): authoritative corpus-first v1 boundary.
- [Concept checkpoint](../checkpoints/CP-001C-reciprocal-mathematical-commons.md).
- [Formal-native investigation analysis](CP-001C-formal-native-research.md): computational knowledge, abstraction, preservation, and proxy gaming.
- [Open decentralization analysis](CP-001C-decentralization-analysis.md): fault models and service boundaries.
- [Growth analysis](CP-001C-growth-analysis.md): conditional growth models and costs; its task-based studies are external possibilities, not protocol requirements.
- [Audit disposition](../audits/CP-001C-AUDIT-DISPOSITION.md).
