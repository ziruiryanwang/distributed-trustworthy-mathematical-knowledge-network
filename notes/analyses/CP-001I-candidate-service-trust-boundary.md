# CP-001I proposal: candidate discovery without mathematical authority

Date: 2026-09-20. Status: next-stage concept proposal, not a selected wire extension or amendment to frozen public-native eligibility. No implementation, protocol execution, artifact extraction, native replay or benchmark. H's qualified index-provider contract remains the baseline.

## Question and division of work

Does an indexer really need to possess and check every proof whose metadata it can help an investigator find? For **candidate discovery**, no such requirement follows from mathematical safety alone. An arbitrary finite list of candidate identifiers can be safe to inspect if every eventual mathematical acceptance still requires independent complete native evidence. But that observation does not supply availability, useful search, affordable ingestion or an acquisition protocol.

The [broker-service proposal](CP-001I-untrusted-search-brokers.md) owns a concrete service mechanism. The [economics/availability analysis](CP-001I-broker-economics-and-availability.md) owns whether uncoupling roles actually saves resources. This note fixes the acceptance, failure and evaluation obligations that any selected version must preserve. Numeric capability/opcode/schema allocations are deliberately not assigned here; no existing record is silently reinterpreted.

## Three different assertions

For an exact target t, a claimed descriptor d, an acquisition source s and a receiving investigator a, distinguish:

| Assertion | Required basis |
|---|---|
| `CandidateListed(b,d,cut)` | Broker b actually retained and returned the bounded metadata at its stated local cut |
| `EvidenceReadObserved(s,R,coverage,scope,interval)` | Actual successful reads of the listed exact CIDs/ranges during the stated local observation interval under s's public/native or independently authorized export scope; not proof that the rest of R's closure was obtainable |
| `Reusable(a,R,context,policy,now)` | Receiver-owned complete checked evidence, coherent actual realization, protected local closure and current policy/incident guards |

The first implies neither the second nor the third. A root/header probe, one successful object read or a partial transfer establishes only that explicit observed coverage. Only complete selected-closure acquisition can establish that the receiver actually obtained that closure; parsing, grounding, checking and protection remain additional requirements for reusability. Even a valid signature on d authenticates a statement by a key, not mathematical truth, completeness, custody or long-term service. A past successful read is not future availability.

An untrusted broker can index **claimed** feature tokens without independently establishing their connection to the actual mathematical target. If it merely copies STRUCT2 descriptors, the tokens and view digests retain their exact claimed values, but the broker cannot describe that act as native qualification. A syntactic consistency check is allowed and useful; it must be labeled at its actual evidence grade. In particular, constructor types or normalized views that require checked native reconstruction cannot be certified by an indexer that has not performed that reconstruction.

The client need not trust metadata to investigate a candidate. Before using a claimed feature as an assertion about a checked target, it must derive or validate that feature through its qualified path. Candidate ranking may remain heuristic throughout. A useful application requires checking the actual local instantiation/transport, not just the external theorem's validity or a matching pattern.

## Conditional safety proposition

Consider the ordinary receiver acceptance predicate `Accept(a,R,E,Policy)` from the selected native contracts. It requires the exact adopted foundation, well-formed complete closure, coherent grounded realization, actual native checking, actual assumption/support accounting and applicable current-use guards.

Assume:

1. Broker messages can only supply bounded inert candidate data and acquisition hints. They cannot modify foundation adoption, proof checking, local policy or acceptance certificates.
2. Every data acquisition follows its own exact authenticated/read-scope/resource contract; a broker hint is not a read capability.
3. Only the receiver's ordinary complete checking path can cause an acceptance event; no broker score, identity, signature or search result bypasses it.
4. The inherited cryptographic, decoder, checked-reconstruction, kernel and local-state integrity assumptions hold.

Then, for **any** broker transcript, including faulty or malicious ones, every completed acceptance event still establishes precisely the inherited conditional mathematical judgment. Proof: the induction over receiving events has no new acceptance transition. Candidate events only add inert local records; acquisition events only add scoped unaccepted bytes; the unique acceptance transition checks the unchanged prerequisites. Thus arbitrary candidate substitution cannot introduce a new logical axiom or an unchecked proof through this service.

This is preservation of a **safety implication**, not equality of accepted knowledge sets between executions. A broker can hide useful targets, direct the client to unavailable evidence, waste its bounded budget, produce irrelevant valid mathematics or improve discovery. Those changes affect liveness, cost and utility. It would be false to conclude that a malicious broker cannot affect the investigator's work.

The proposition is conditional on the actual implementation respecting the boundary. Parsing, authentication, resource exhaustion, native implementation defects and compromised owner state are not eliminated by a paper transition argument.

## Acquisition must not become recursive authority laundering

A selected broker result needs a concrete bounded path to independent acquisition. At minimum it must identify an exact target/evidence replay candidate and a finite set of concrete candidate sources with their stated service roles. It must not merely refer to another broker which refers to a third broker without charging every hop and eventually naming an evidence-serving source.

Existing qualified sources may serve through their current public replay scope or an independently authorized export lease. The broker cannot mint that source's lease, use its own metadata manifest to authorize reads from someone else's CAS, or claim that copying a descriptor copied the underlying proof. All returned contacts remain untrusted network data subject to the existing transport/address/connection policy. No automatic request to arbitrary URLs or local/private resources follows from a metadata field.

One candidate can name several evidence sources, but the client validates every actual response against the exact requested content and scope. Combining chunks from different sources requires the same exact CID/range/hash and complete-closure checks as ordinary acquisition. It does not require agreement on political authorship. If sources offer different valid proof alternatives, their evidence identities and potentially different realizations/support remain distinct; the client can select one or explicitly compose them through PI1.

A broker may list stale or withdrawn evidence. Distinguish a failed source observation from a theorem's falsity. An alternative replay for the same judgment is useful only after its own check. A source-scope failure does not authorize a generic private CAS read.

Metadata also confers no authority over a local LLM agent or its tools. Returned strings, labels, source annotations or contacts are untrusted data, never instructions to change policies, execute commands, send secrets or broaden acquisition. The service must define allowed inert fields and their rendering/interpretation explicitly; a candidate result is not an agent-to-agent delegation message. Mathematical acceptance checks alone would not prevent unrelated tool misuse caused by treating remote text as authority.

## Resource and cache conditions

Broker discovery is still owner-admitted work. Each investigation receives finite aggregate metadata, contacts, pages, redirects, candidate-type probes, staged bytes, native work and elapsed-time budgets. Separate per-call caps do not grant unlimited retries or one new independent allowance per false candidate. Native acquisition can be a larger explicit local stage, but it must be admitted before it begins.

Candidate caching binds exact broker result/descriptor IDs, foundation/extractor interpretation, observation time and service role. Reuse of an old candidate record is not reuse of a positive native acceptance certificate or current evidence availability. Local negative observations must keep their actual scope:

- Invalid bytes at an exact CID are evidence against that response/source, not mathematical falsity of an unseen proposition.
- A native mismatch applies to its exact candidate/realization/checker conditions, not every alternative proof of the judgment.
- Resource exhaustion is nondecision, not invalidity.
- An exhausted broker page/query scope establishes no global absence theorem.

Bounded repeated-failure suppression may protect local resources. It should distinguish stable malformed exact data from transient unavailable sources, policy differences and expensive but potentially useful candidates. No mandatory global blacklist, identity election or universal popularity score is required.

Broker ingestion also needs finite local budgets and snapshot/retention rules. Removing native checking from ingestion does not make arbitrary forged metadata, token fanout, churn or index storage free. If the only published false-lead defense is the client spending its full proof-check budget repeatedly, practical operability has not been established.

## Decentralization and reciprocal contribution

A broker must be optional. An investigator should retain the existing direct qualified-provider/known-ID path and be able to select several independent brokers, run its own, or share bounded candidate collections directly. No broker assigns mathematical identities or elects accepted theorem bodies. Exact checked artifacts remain portable across broker boundaries.

Contribution has distinct milestones: locally checked, evidence actually served/retained, candidate metadata indexed, route discoverability observed, and downstream checked reuse. Reaching one does not imply the next. In particular, cheap metadata submission must not be counted as durable mathematical accumulation if every evidence copy disappears.

The reciprocal success case is concrete: a local investigator publishes complete checked evidence at an actually supplied source; one or more brokers make its exact metadata discoverable; another investigator acquires the evidence independently, checks a useful local application, and contributes a new checked artifact with its own evidence and discoverability path. Local research choices remain autonomous and require no public-goal registration. This is not a confidentiality guarantee: transmitted tokens, patterns, exact targets, contact identity/address, timing and follow-up reads may reveal an investigation to contacted peers. Query disclosure requires the owner's admitted policy; search privacy would require a separately specified mechanism. No system-level human-intention test or persistent unsolved-task list is introduced.

## Comparative evaluation required before claiming an improvement

Hold total supplied resources explicit and compare at least:

- Existing qualified native index/custody providers alone.
- The same evidence custody plus additional candidate-only brokers.
- A genuine redistribution of some index/checking resources to brokers while preserving a stated evidence-recovery target.

The second case can improve discovery but cannot claim savings merely because it adds free resources. The third can reduce checking/storage duplication only if the displaced copies were not still required for custody, availability, locality or serving throughput.

Use a declared diverse pool of private local formal investigations with useful candidate IDs hidden from the discovery client. This finite evaluation pool is not a public research-task registry and is not assumed to represent all mathematics. Independent native checking of actual applications defines successes. The query pool and all failed/expensive cases remain in the denominator; selecting only broker-friendly queries is not a valid general efficiency claim.

Count, separately, ingestion effort, maintained metadata/route state, evidence replicas, source onboarding, cold/warm client acquisition, native checking/reconstruction, false leads, unavailable candidates, candidate ranking work, actual checked applications and subsequent useful contributions. End-to-end comparisons must include evidence traffic shifted from brokers onto custodians/clients and correlated source failures. Token-query success is not checked mathematical reuse.

An acceptable concept outcome can be conditional: broker mode is worthwhile for a specified service/workload regime, while direct native indexes remain preferable elsewhere. No proof of universal superiority, globally complete search, correct popularity ranking or exponential knowledge growth is required or implied.

## Open design obligations

Before selecting a broker extension, the companion proposal must close its concrete metadata grammar, exact acquisition-role binding, scoped serving authority, bounded listing/cursor semantics, routing/profile separation, ingestion/publication/expiry rules and owner-resource accounting. Its audit must trace false descriptors, withdrawn sources, incompatible foundations, redirected hints, lost replies and cold acquisition through actual permitted outcomes.

This note fixes the invariants those mechanisms must satisfy. It is not itself an operable service specification or permission to bypass the selected baseline while the remaining contract is unfinished.
