# CP-001I proposal: metadata-only untrusted search brokers

Date: 2026-09-20. Status: **BROKER1 concept proposal, pending independent review**. Not a selected H amendment, release profile, executable design, native qualification result or efficiency measurement. No numeric record types, capability codes or operation codes are allocated here. Frozen native-provider records keep their meanings.

## Decision proposed and its scope

Allow a separately negotiated, optional service to index bounded **claims about** mathematical artifacts without importing, checking or retaining their native proof closures. Call its operator a *candidate broker*. A broker helps find candidate evidence; it is not thereby an evidence provider, custodian, checker, foundation authority or mathematical acceptance authority.

The existing native-provider path remains available. A qualified native search provider holds a checked, retained, locally authorized public closure and can offer both candidates and evidence. BROKER1 adds another role; it does not weaken that provider's contract or rename unchecked objects `PubliclyServed`.

The useful separation is between three independently supplied resources:

1. Search metadata and postings, which brokers can replicate.
2. Complete evidence and actual byte service, which native providers/custodians must still supply.
3. Receiver-owned checking and a checked local application, which the agent relying on the result must still perform.

A single machine may operate all three roles under distinct authority and accounting. Running only the first is permitted. There is no mandatory broker, global catalog, shared research goal, global ledger or agent assignment service. This proposal is token-only; native STRUCT2 pattern filtering remains a potentially stronger alternative.

## Bounded investigation modules

Investigate the uncertain seams independently; do not reopen H's settled native contracts. Each module's output is a conditional paper contract, not implementation qualification.

| Module | Input and bounded output | Local claim, countercase and exit criterion |
|---|---|---|
| Claimed-metadata ingestion | Existing bounded D, authenticated self lead or owner-admitted collected page; output a charged local metadata row/cut | Syntax admission creates no hidden native work or truth certificate. Test forged semantic bindings, duplicate submissions and a fifth lead. Exit when mutation/authority/resource outcomes are explicit and audited. |
| Snapshot candidate search | Fixed authorized metadata cut plus token query; output a bounded non-skipping page and exact continuation | Complete honest scan covers that local predicate only. Test a full page, interrupted row, stale holder, changed leads and revoked scope. Exit when each continuation retains one immutable meaning and every stopping case is distinguished. |
| Evidence-source leads | At most four exact-R public-native leads; output actual source-scoped byte observations and independent native acceptance or a scoped failure | Broker bytes grant no evidence read authority. Test wrong R, private/expired scope, missing bytes and constructor targets. Exit when the path reaches the unchanged receiver predicate without implicit fetch permissions or substitutions. |
| Broker discovery | Explicit contacts or separately negotiated broker ads and supplied placement work; output only observed route reachability | Known-panel success does not imply unfamiliar-broker discovery. Test native/broker record confusion, lease expiry and missing markers. Exit when the minimal direct-contact case is bounded and wider routing remains visibly gated on its own profile/supply contract. |
| Comparative cost | Fixed recovery/service target and stated positive/defeating workloads; output separately counted avoided, retained and added work | Role splitting can avoid unnecessary native replicas, not mandatory custody or client checking. Test scarce source bandwidth and ungrouped renewal. Exit when no resource is supplied free and improvement claims name their actual regime. |

The first three form the minimal direct-contact service argument. Broader routing and end-to-end efficiency are separate modules with separate acceptance gates; a good safety argument cannot substitute for either.

## Inherited contracts and explicit noninheritance

The relevant sources are the [G structural contract](CP-001G-structural-retrieval.md), [G profile/consumer bindings](CP-001G-profile-and-consumer-bindings.md), [F routing](CP-001F-dissemination-and-routing.md), [F exact scopes](CP-001F-exact-routing-coverage.md), [NET2/BUNDLE1/export contract](../../spec/OPERATIONAL-CORPUS-V2.md), and [H supplied-resource analysis](CP-001H-resource-supply-and-discovery.md). The companion [receiver trust boundary](CP-001I-candidate-service-trust-boundary.md) owns the unchanged acceptance obligations; the [economics analysis](CP-001I-broker-economics-and-availability.md) owns comparative workload arguments.

In particular:

- Existing STRUCT2 mode-6 pages include actual bounded `StructuralDescriptor 0x8124/1` payloads inline. A broker can collect those bytes through an authorized paid search. No generic descriptor-CAS read is needed or introduced.
- Existing `PublicIndexDescriptor 0x8111/3` is a candidate hint, not a general read capability. The minimal broker record below does not require fetching one.
- Existing `ProviderAd 0x8022/2`, native K4, `FULL_FEATURE`, and H's shared/consolidated native scopes require their stated native/public eligibility at the producer. Metadata-only brokers cannot use those assertions for themselves.
- Existing STRUCT2 pattern bodies are provider-local material. Copying their public digests does not copy a pattern, disclose it, or make it remotely readable.
- Existing public, holder-bound export and advisory read scopes remain unchanged. A replay hash in a broker record opens none of them by itself.

BROKER1 uses the bounded invocation, authentication, owner admission, one-shot accounting and disclosure principles of NET2. Its new service messages and record domains must be explicitly negotiated and separately allocated before implementation. Names in capitals below denote **symbolic proposal-level alternatives**, not existing integer tags or legal messages on a frozen connection.

## Objects, roles and predicates

Write `F` for an exact FoundationID, `E` for an exact ExtractorID, `R` for an exact PI1 InstanceReplayID, and `D` for the canonical bytes of one STRUCT2/1 descriptor. Its existing payload is:

`[1,F,E,targetRef,R,sortedTokens,flags,viewSummaries]`.

The existing limits are 4096 bytes, 32 unique sorted 32-byte tokens, 16 flags and eight view summaries. Exact target forms are `[2,JudgmentID]`, `[1,DefinitionID]`, `[4,OpaqueID]`, and `[3,GroupID,constructorSelector]`. These target tags are not the typed-root tags of InstanceReplay. A constructor view does not become an independent native root.

Let `d = ContentID(D)`. Since `D` already binds `F`, `E`, `targetRef` and `R`, use **d as the candidate identity**. Different descriptors for one target, different exact replays, and different foundations remain distinct. Deduplicating display entries by target must not discard distinct evidence identities needed for later acquisition. A change to leads changes a snapshot row, not d.

Keep the following predicates separate:

| Predicate | Exact meaning |
|---|---|
| `MetaListed(b,d,S)` | Broker b's immutable snapshot S contains descriptor d and its frozen bounded lead list |
| `MetaDisclosureAuthorized(b,S,a,now)` | b currently permits disclosure of that metadata scope to client a |
| `NativeScopeAuthorized(p,R,a,scope,now)` | Actual source p permits the specified native read under its own unchanged public/export rules |
| `EvidenceReadObserved(a,p,R,items,scope,interval)` | a obtained the specified exact CIDs/ranges during that local observation interval; partial reads do not establish complete closure availability or future service |
| `Reusable(a,R,context,policy,now)` | a satisfies the inherited complete native checking, actual realization, retention/protection and current-use conditions |

The first two imply neither of the last three. An authenticated broker connection establishes the source of its messages, not their mathematical truth or the current availability of another node. None of these predicates means globally complete discovery.

### Minimal candidate row and acquisition lead

The proposed abstract row is:

`BrokerCandidate = [descriptorPayloadBytes,orderedLeads]`.

An acquisition lead is:

`[PUBLIC_NATIVE,sourceNodeID,sortedPublicEndpoints,InstanceReplayID]`.

Each lead is at most 1024 canonical bytes and contains at most two existing-format public endpoints. A row has one to four leads, with distinct source NodeIDs, canonically ordered by NodeID. Every lead's replay ID must equal D's R. The entire row is at most 16 KiB. All IDs, endpoint shapes, integer ranges, descriptor flags and selector syntax must pass their bounded codecs; malformed rows are rejected before posting insertion or connection attempts. Schema validation compares visible fields and typed-ID grammar only. It does not establish a ProofInstance's actual target, R's actual typed root/representative map, constructor existence/type or the native target-to-replay relationship. Establishing those hidden bindings is not a broker-side fetch obligation; they remain claims until independent acquisition and checking.

There is deliberately no export lease, private source scope, executable program, arbitrary URL, remote tool instruction, free-form proof text, freshness certificate or native acceptance label in this row. The descriptor's view digests are merely copied claims. No source signature is required for the row, and forwarding it makes no portable assertion that its sources endorsed it. If a later profile forwards a source-signed observation, that signature must retain its own exact weaker meaning.

The role `PUBLIC_NATIVE` means the client is being pointed to the named node's candidate public-native service for exact R. It is **not** a claim by the broker to have that role. A fresh source may offer the ordinary public replay scope or issue a new holder-bound export through its existing service. Private/third-party export offers and broker-to-broker referrals are outside this minimal acquisition grammar.

If a source names a different valid replay for the same judgment, that is a different candidate, not a replacement of R inside this row. No arbitrary fallback replay is substituted during a supposedly exact fetch.

## Ingestion, publication and removal

### Two bounded ingestion paths

An owner can fund a broker-local collection job over explicit sources and **explicit bounded existing queries**. When collecting native STRUCT2 pages, the collector must implement and negotiate the actual source requirements, presently 3+7+8 for the code-4 service. Implementing the relevant reader does not require adopting the foundation or executing native checking during collection. The collector retains the inline D and a lead to the authenticated serving node; it does not fetch R's closure.

Existing token predicates are not a magic complete-corpus enumeration interface. A finite set of those queries may miss most of a provider's corpus. An owner-supplied finite metadata bundle can also be admitted as inert input, but must not be described as an independently observed complete or native-qualified collection. No remote request can force a broker to crawl an arbitrary library or follow an unbounded chain of hints.

For incremental contribution, propose a new bounded operation `BROKER_SUBMIT_SELF`. Its request contains one D and one self lead, at most 8 KiB total. The authenticated submitter must equal that lead's sourceNodeID. It submits only its own asserted PUBLIC_NATIVE lead, not a lead allegedly authorized by another source. An honest native source submits D only while the corresponding actual descriptor/evidence is locally public and qualified. The broker checks the message/identity/bounds but **does not certify that honest-producer premise**.

Submission consumes a separately admitted ingestion offer and actual record/posting/queue resources. It cannot trigger native fetch, native checking, routing publication, unlimited future rechecks or a protected storage pin. The broker's authorized local writer decides whether to list it. The reply distinguishes admitted at an identified local cut, already present, deferred without a publication promise, and declined. Both admitted and already present bind exact d **and the requested canonical self-lead payload** at that cut; d existing with other sources or older endpoints is not success for this requested lead. A fifth-lead refusal or declined endpoint replacement cannot masquerade as already present. Admission is not a custody or downstream-reuse receipt. Lost replies are resolved through the ordinary exact invocation identity; retry does not allocate another free copy.

### Merging and withdrawal

Rows are keyed by d. Repeated submissions of identical D do not allocate another descriptor identity or another posting per token. An authenticated source may propose an update of its own lead or request removal of its own previously admitted self lead. It cannot remove another source's lead or mutate D in place. Different D bytes require another d. The broker owner retains ultimate local publication authority. If an accepted removal leaves no selected lead, its same charged local transaction unlists/retires the current row and postings; it cannot leave a current zero-lead BrokerCandidate. A broker that declines the removal says so explicitly. Historical snapshots can retain their frozen rows under their independently live metadata disclosure/retention authority, unless that authority is also revoked.

At most four selected leads appear in any row. A fifth prospective source is explicitly declined or replaces an existing lead only by an owner-admitted selection decision. First arrival, multiple aliases or high submission frequency create no right to evict another source. Selection can use bounded authenticated collection observations or local success history, but those are heuristics, not independent-replica or availability proofs. Finite per-source limits are supplemented by global limits because keys are cheap.

All current rows and immutable snapshot versions remain charged. Removing a current row does not erase already disclosed bytes. Source withdrawal or source unavailability does not retroactively falsify D's target. Native authorization is rechecked at the actual source regardless of whether the broker has learned about that withdrawal.

### Distinct metadata disclosure authority

The broker owner must explicitly authorize `BROKER_METADATA_SERVE` over an exact local metadata collection. This authority covers only the selected candidate rows. It is neither PUBLIC_SERVE nor an advisory-CAS manifest and contains no native closure authority. A descriptor mentioning a private replay is still not permission to fetch or expose it.

Metadata authorization is checked when a reply is computed and atomically rechecked at delivery claim under its exact authorization generation. An owner withdrawal invalidates the affected unclaimed metadata deliveries and covering snapshots; a new permitted query needs a new snapshot. Bytes already transmitted cannot be recalled. A historical snapshot can survive ordinary current-index edits only while its own metadata disclosure remains authorized and its retention/expiry allocation remains live.

Routine source observations, lead replacements and local retention policy can create newer cuts. They do not rewrite an old cut. A native source's change does not automatically update every broker; that absence of synchronized global state is part of the service contract.

## Token query and pagination semantics

### Query and exact predicate

Propose a distinct `BROKER_FIND` service accepting:

`[F,E,sortedRequiredTokens,targetFilterOption,snapshotSelector,startPosition,pageCeilings]`.

There are one to four sorted unique 32-byte tokens. The optional target filter is absent or an exact targetRef of the descriptor grammar. It is an additional conjunction, not a standalone exact-judgment route service. When an investigator already knows the exact judgment/replay, the existing direct native path remains available.

For a row r, the selected predicate is exactly:

`Match(Q,r) iff r.D.F = Q.F and r.D.E = Q.E and Q.tokens subset-of r.D.tokens and (Q.target absent or Q.target = r.D.targetRef)`.

This tests **claimed token bytes**, not semantic entailment, native applicability, normalization, proof validity, target/replay consistency or native availability. A broker can operate on owner-admitted exact F/E namespaces without adopting those mathematical foundations. It cannot infer that a supplied extractor ID authorizes loading software. Any claimed semantic binding of E to F is independently established through the client's qualified extractor path when needed.

No patternOption is accepted. Supplying one is a request mismatch, not an ignored field or a false pattern success. A later public pattern-sharing extension would need an explicit bounded payload/disclosure grammar and separate semantics. The native baseline's pattern selectivity must not be credited to this token-only service.

The query may expose mathematical interests through tokens, target IDs, broker choice, timing and dictionary attacks. Local query disclosure requires owner authorization. No privacy from token hashing is promised.

### Immutable snapshot and ordered scan

A snapshot binds broker NodeID, broker service epoch, authenticated holder, exact broker record/profile version, F/E, metadata collection cut, row/posting roots, authorization generation, and finite issuer-local expiry. Its rows include frozen lead lists. Native checking state is not a snapshot component because the broker has no such obligation.

Choose the shortest required-token posting list in that exact snapshot, ties by token bytes. The posting is sorted by canonical d bytes and contains each d once. The planner identity fixes this choice. An exact-target filter does not silently switch the base ordering. Evaluate the other tokens and optional target on each base row.

BEGIN starts at the minimum key. A new lower-bound request may start at a canonical d boundary that does not itself exist. Continuation resumes at the **inclusive next unprocessed** key in the same snapshot. A row is processed only after its predicate test has completed and, if it matches, its entire BrokerCandidate has been included in the committed result. A matching row that does not fit, or whose processing is interrupted, stays next; it is not silently skipped.

Each page contains at most 64 rows and at most 1 MiB of complete encoded result bytes, with at most 8192 posting inspections, 0.25 CPU-seconds, two wall-seconds and 16 MiB working memory. Nonrow result metadata, tokens and cursors together fit 16 KiB. Requested result capacity is between 32 KiB and 1 MiB; hence one maximum-size 16 KiB row can fit with the maximum metadata allowance in an otherwise empty page. A 64-row page is not promised when its actual encoded bytes exceed the aggregate limit.

The reply states the exact snapshot/query, requested lower boundary, half-open processed interval, matched inline rows, and one of END, MORE or PARTIAL_BUDGET. END means that this base posting above the requested boundary was exhausted; no claim is made below it. MORE/PARTIAL includes the next unprocessed position and an authenticated continuation when its finite snapshot remains retained. A budget stop may produce zero rows and no progress. That is not an empty complete answer.

The broker authenticates snapshot/continuation tokens under its own epoch secret. They bind the broker, holder, epoch, snapshot, row schema, query, extractor interpretation, planner, original lower boundary, next unprocessed position, expiry and admitted ceilings. Each continuation is a new paid invocation, not a storage lease or unmetered cursor. A changed holder/query/schema/epoch, expired allocation, withdrawn authorization or mismatching snapshot yields stale/mismatch rather than resumption against a new cut. A restarted query can repeat results; client caches deduplicate exact d only within their finite admitted scope.

An honest complete scan supplies local predicate coverage of that exact retained snapshot. A malicious broker can omit or invent rows; token authentication or a signed root alone proves neither local completeness nor mathematical truth. Complete audit of a snapshot would require independently obtaining/verifying its actual committed index under a separate bounded path; BROKER1 supplies no such proof by assertion.

## Optional decentralized broker routing

Known broker contacts suffice for a first bounded use case. That alone does not solve unfamiliar-broker discovery in a large network. Propose a **separate** optional `BROKER_ROUTE` lane, rather than pretending the native K4 lane already advertises brokers.

Its abstract key is `BrokerTokenKey(F,E,token32)`. Its signed advertisement is:

`[BROKER_AD_V1,brokerNodeID,key,revision,brokerContact,anchorDescriptorID]`.

The key is at most 1024 bytes, the contact at most 1024 bytes, and the complete signed advertisement at most 4096 bytes. The contact has that same NodeID, at most two explicitly public endpoints and at most 16 supported broker-profile identifiers. It is a broker contact, not a native-profile promise. The broker's honest publication obligation is that it currently lists at least one authorized metadata row with that F/E/token and anchor d. It has **no new obligation to retain or check R** merely to place this ad.

Route holders validate schema, bounds, signature, authenticated submitting broker, key/record/profile consistency and local admission. They do not fetch the anchor or evidence. Only the named broker may place, replace, renew or withdraw its row. Copying its ad is allowed as a hint but cannot renew its lease. Revision handling, checked exhaustion, one owning live row per `(cell,key,broker)`, current lease gates, expiry/reclamation accounting and lost-reply fencing must be specified as explicitly as native ROUTE1 before selection.

The proposed route algorithm copies ROUTE1's bounded iterative lookup, four-copy observed placement target, adaptive finite-depth shard cells and ancestor-marker principle into a **domain-separated broker record/key namespace**. It requires distinct broker cell/target hashing and negotiated broker-capable contacts; native cells and existing capability-5-only contacts cannot be silently reinterpreted. Lookup remains a paid bounded one-hop operation, not a remote recursive crawl. Source/evidence discovery does not recursively traverse brokers: a final BrokerCandidate must name actual native-service leads.

The minimal proposal uses **ungrouped broker leases only**. It does not inherit FULL_FEATURE group renewals, shared native scope coverage, or H's renewal economies for free. Grouped broker publication would need a separately reviewed mode, membership grammar, ownership/handoff rules and supply calculation. An owner may therefore reasonably deploy a broker with a small token scope or known contacts while native grouped routing remains cheaper for a large publication scope.

For a selected finite broker publication scope, let U be the distinct claimed-token union of its explicitly chosen rows. Full metadata-token publication would require actual placement and marker observations for **every** token in U. A sampled/coarse subset must be reported as such. Merely keeping all rows locally does not establish full routing coverage. Missing placements, expired copies, stale anchors and incomplete renewal give partial/degraded status, not global discoverability.

No global mandatory roster or seed server is selected. Bootstrapping still requires at least one actual reachable willing contact, obtained out of band or through another known contact. Multiple names or signatures do not prove independent operators, resist key grinding, or rule out eclipse. A claimed broker extension cannot be marketed as operable network-wide until its record/operation allocation and actual funded routing profile are closed.

## Native acquisition and local use

For a returned row, the client follows this sequence within one finite investigation budget:

1. Validate the broker row's bounded syntax, exact D hash, F/E match, target grammar, token predicate and same-R leads. Cache it only as an untrusted candidate. Do not install a foundation, checker, plugin, local tool instruction or policy from it.
2. Choose at most the supplied four source leads under local endpoint and connection policy. No arbitrary URL, localhost/private-address access, hidden redirect chain or recursive broker request is authorized. Existing network transport restrictions continue to apply.
3. Authenticate the actual named source and negotiate its real native capabilities and exact F. A source's broker appearance is not that negotiation. Obtain its own current public-native authority or a freshly issued exact holder-bound export. A foreign/expired/copied export lease is not reusable authority.
4. Acquire explicit native objects/ranges through the unchanged read scopes and BUNDLE1/export rules. BUNDLE1 remains bounded to 256 explicit items, a 16 KiB request and 4 MiB payload plus 64 KiB metadata per call. No broker query authorizes generic CAS reads. Multiple item calls and sources share the investigation's cumulative budget.
5. Derive and check the complete actual closure, exact F/R/target binding, coherent realization, assumptions/support and current-use conditions under PI1 and the selected native reconstruction contracts. A source responding with another root is not an exact response. Missing bytes, incompatibility, invalidity and budget nondecision remain distinct outcomes.
6. Before treating a descriptor feature as a fact about the checked target, independently derive or validate it under the qualified extractor. Ranking can remain heuristic without that stronger assertion. A successful mathematical reuse additionally checks the actual local arguments, premises, equality transport or adapter; token matches do not discharge them.

Broker bytes never stand in for native evidence. A source can decline, disappear or return corrupt data after any earlier observation. A different source can serve exact R if independently authorized; a different proof of the same judgment requires its own candidate/evidence check. Cold receiver checking is not eliminated by the role split.

## Resource envelope and anti-amplification obligations

There is no free metadata plane. Each deployment must supply a finite owner-approved vector bounding current records, pinned versions, bytes, postings, sources, endpoints, snapshots, admitted namespaces, queues, concurrent calls, resident memory, recurring CPU/I/O/network work and routing stock/renewals. Admission compares **actual total live/reserved/uncertain resources** with that vector; increasing a record-count limit alone supplies no disk, memory or recurring work.

The following is a possible *illustrative local stock envelope*, not a throughput claim or selected release default:

| Stock | Illustrative maximum |
|---|---:|
| Current candidate identities | 65,536 |
| Current plus snapshot-pinned row versions | 131,072 |
| Actual posting entries across retained versions | 4,194,304 |
| All retained metadata/index/snapshot/control bytes | 4 GiB |
| Entire broker service resident memory | 256 MiB |
| Concurrent query/ingestion executions | 4 |
| Live snapshots, finite lifetime at most 600 issuer-local seconds | 8 |
| Pending admitted ingestion jobs | 128 |
| Admitted F/E namespaces | 16 |

These maxima need not all be simultaneously attainable: actual byte/memory/accounting limits dominate. Snapshot/copy-on-write data, result spools, queues, cursor state, per-source records, lead versions and unreclaimed retired rows count; neither deduplication nor expiry creates a free accounting category. In-flight work fits the same memory total, not another uncounted allowance. Snapshot expiry cannot be renewed indefinitely through continuation.

Recurring allocations and any broker-route stock must be separately specified before offering sustained service. They are reserved from the owner's real total allocation, not copied from H's native allowance. A per-request cap is not a per-investigation or per-day cap. Recurring source refresh, listing churn, advertisement signing/renewals, scans of nonmatches, ingestion rejection and cleanup all consume supplied work. Remote arrivals cannot replenish these budgets.

The client separately bounds total brokers, routed cells, pages, rows, source contacts, retries, type probes, staged bytes, native checking and elapsed time. Owner-admitted escalation to a larger native acquisition stage is explicit. Four leads per row does not grant four fresh unbounded acquisitions for every row in an unbounded stream.

Operational self-submission identities and local failure caches can bound repeated work, but are not political attribution or a proof against Sybil flooding. Global caps remain necessary. A false descriptor, stale lead or too-expensive proof cannot automatically trigger a network-wide blacklist, checker incident or full-corpus repair. Resource exhaustion is nondecision; an empty finite search is not mathematical nonexistence.

## Conditional paper properties and limits

### Mathematical safety preservation

Assume the inherited decoder/cryptographic/kernel/reconstruction/local-state integrity conditions, the client's admitted foundation/policy, and the separation that broker transitions can create only inert candidates or bounded acquisition plans. Assume every acceptance still uses the unchanged complete native predicate. Then **for any broker transcript**, each completed acceptance event has the same inherited conditional mathematical soundness implication as an ordinary direct acquisition.

The proof is a transition induction: ingestion/listing/routing events create no local native declaration or acceptance certificate; read events create only scoped unaccepted bytes; the sole acceptance transition checks the preexisting native prerequisites. This is not equality of accepted sets across executions. A broker can change which work is attempted, which valid result is selected, latency, false-lead costs and whether a useful result is ever found. Bugs crossing the stated boundary defeat the assumptions; this paper argument is not an implementation audit.

### Snapshot search property

Assume an honest broker, fixed live authorized snapshot, exact matching predicate, adequate per-step progress resources and enough admitted continuation work before expiry. Processing the finite base posting through END returns every matching row at or above the original lower boundary without skipping a matching row at a page boundary. The invariant is that the half-open processed prefix has completed tests and committed output for every match, while the next boundary is inclusive and unprocessed. This says nothing about objects absent from the snapshot or relevance outside the selected tokens.

### Conditional reciprocal use

Suppose a contribution has complete checked evidence at at least one reachable willing actual source; a compatible candidate is admitted by a reachable broker; the investigator chooses a matching token query; retained snapshots, routing/known contacts and sufficient declared budgets allow discovery and acquisition; and the actual local application is checkable under its adopted policy. Then the investigator can pass through the listed acquisition path without trusting the broker mathematically.

These premises are substantive. The service supplies no theorem that an arbitrary future useful result will share selected tokens, be indexed, retain evidence forever, fit every receiver, or be discovered across a partition. A local agent can produce a new checked result and repeat the process without a common root goal. Exponential *useful* accumulation remains an empirical workload/supply hypothesis, not a consequence of content hashes, metadata growth or signature count.

### Cost opportunity, not universal superiority

Holding a corpus, metadata coverage and explicit recovery/service target fixed, replacing some native-search replicas with metadata-only brokers can avoid native storage and repeated import/checking **only for copies not still needed for evidence custody, recovery, locality or serving throughput**. Metadata/posting bytes, lead maintenance, client checking, source traffic and route work remain. Token-only filtering may cause more expensive downstream probes than native pattern search.

Fewer evidence sources can become bottlenecks or correlated failure points. An extra broker added without retiring any native work is an added-resource experiment, not a proof of cost savings. Ungrouped broker route renewals can erase the intended saving relative to H's grouped native publication. The companion economics note must account for these cases before claiming material end-to-end benefit.

## Required audit cases and selection gates

An independent review should trace at least these paper cases through actual outcomes:

- D is schema-valid but lies about the target, tokens, extractor relation or R: untrusted candidate; actual native checking/feature validation decides the relevant binding.
- A true target has a stale source lead or copied foreign export head: no authority transferred; attempt fresh scoped service or return unavailable/nondecision.
- A group constructor descriptor is returned: the client acquires/checks the actual group-root replay, not a fictitious standalone constructor object.
- A client requests pattern filtering from the token broker: mismatch, not degraded silent success.
- A matching maximum-size row lies at the page boundary: retained next position; no skip.
- Metadata is withdrawn after page computation but before delivery claim: scope-generation recheck cancels that unclaimed disclosure.
- A source updates a lead while an authorized snapshot remains live: old snapshot remains an explicitly historical immutable observation, unless its scope is revoked.
- The same descriptor is submitted repeatedly, or five sources propose leads: bounded deduplication/admission; no unlimited versions, lead set or implicit eviction privilege.
- A broker copies another broker's candidate: the copied claim neither proves source endorsement nor authorizes a source fetch; client path is unchanged.
- A route holder receives a broker ad in a native ProviderAd2/K4 slot: reject that profile/record mismatch; do not relax native eligibility.
- A routing lease expires or a hot-key branch is unexplored: partial discovery, not absence or current full coverage.
- An invalid/corrupt response, policy mismatch and exhausted proof budget are cached: their exact scopes stay distinct; none implies every proof of the judgment is false.

Before selecting BROKER1, close its exact separately negotiated message/record allocation, complete finite invocation/result grammar, route namespace/hash and lifecycle bindings, sustained service/renewal envelopes and independently reviewed cost conditions. These are proposal obligations, not permission to deploy an ambiguous partial wire extension. Any grouped broker route mode needs its own review. No H/native contract is changed by this note.
