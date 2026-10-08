# CP-001I candidate contract: direct-contact broker service

Date: 2026-09-20. Status: root-owned proposed exact interface binding, under independent audit. These numeric allocations are candidate specifications, not a deployed or frozen profile. No implementation, native replay, extraction, executable model or benchmark. H remains the selected integration until an I checkpoint explicitly selects its amendments.

## Small module selected for investigation

Close the direct-contact portion of [BROKER1](CP-001I-untrusted-search-brokers.md): bounded metadata submission/withdrawal, immutable token search and exact native-source leads. Do **not** select its optional broker-routing sketch. There are no new broker DHT keys, ads, group modes or routing opcodes in this candidate contract. Existing native routing remains unchanged and available; it does not advertise a metadata-only broker as a qualified native provider.

A client obtains a broker NodeID and at most two permitted public endpoints through owner configuration, an explicitly imported inert contact, or an already known authenticated peer. This is an optional contact choice, not a mandatory central directory. No automatic contact crawl follows. The actual connection authenticates the named broker before negotiation. Cold unfamiliar-broker discovery is outside this module's guarantee, not allegedly solved by these contacts.

The [candidate trust boundary](CP-001I-candidate-service-trust-boundary.md) and [economics](CP-001I-broker-economics-and-availability.md) remain binding concept companions. Brokers index claims; they neither acquire native authority nor supply evidence custody by listing them. Heuristic selection is permitted; mathematical acceptance remains unchanged.

## Candidate registry delta

Keep NET2 envelope version 2 and ServiceCall `0x8004/2`. Propose capability **9=BROKER_DIRECT1**. Both sides must observe it through reciprocal authenticated HELLO exchanges before these operations. Supporting 9 includes these bounded metadata codecs, not capability 7's extractor algorithm, native capability 8, foundation adoption, native service or any routing role. Ordinary native collection/acquisition separately negotiates its actual existing capabilities.

No HELLO field is added. Existing capability/service-kind list and byte bounds apply; a broker advertises only its actually supported service kinds. `nativeProfileIDs` does not become a list of unverified broker namespaces. The client names its F/E in the query; unsupported local metadata namespaces receive UNSUPPORTED_PROFILE without triggering foundation installation or collection. A metadata-only peer may advertise no native profiles.

| Proposed type/schema | Payload meaning |
|---|---|
| `0x8125/1` BrokerCandidate | `[descriptorBytes,orderedLeads]` |
| `0x8126/1` BrokerPredicate | `[F,E,sortedRequiredTokens,targetOption]` |
| `0x8127/1` BrokerPage | Exact page tuple below |
| `0x8128/1` BrokerMutationAck | Exact acknowledgment tuple below |

These types are inert organizational data. They enter no mathematical closure, native/advisory read-scope whitelist, ProviderAd2 anchor slot or existing FIND_WINDOW result domain. A content ID identifies bytes only; none of these types creates generic CAS read permission.

| Proposed operation | Arguments |
|---|---|
| 21 BROKER_SUBMIT_SELF | `[descriptorBytes,selfLead,expectedPriorOption]` |
| 22 BROKER_WITHDRAW_SELF | `[descriptorID,expectedPriorOption]` |
| 23 BROKER_FIND | `[predicate,snapshotSelector,startPosition,pageCeilings]` |

Each operation uses ordinary NET2 OFFER_REQUEST/OFFER/CALL/RESULT, exact-call binding, independent operation/reply tickets, single execution, authoritative metering, disclosure-version checks, lost-reply handling and paid retries. No new notification, deferred execution right, native push or remote research assignment is added.

## Exact row, key and lead meanings

`descriptorBytes` is the canonical payload byte string of STRUCT2 `0x8124/1`, at most 4096 bytes, with its inherited exact shape and bounded flags/selectors. Compute `d` as its ordinary typed ContentID. The broker's current row key is d, not the BrokerCandidate CID. D changes imply a new d; changes to a row's lead list change its BrokerCandidate bytes but not d.

`lead = [0,sourceNodeID,sortedPublicEndpoints,R]`, where 0 means PUBLIC_NATIVE, endpoints use the existing public endpoint codec, there are at most two endpoints, and the entire lead is at most 1024 canonical bytes. R is `0x0015/3` and equals the replay ID visibly claimed by D. A candidate has one to four leads with distinct source NodeIDs, sorted by canonical NodeID bytes, and at most 16 KiB canonical payload bytes in total.

Descriptor target tags keep their original semantic-reference grammar, not InstanceReplay typed-root tags. A constructor target points to its claimed group replay. Broker validation checks syntax and equality of visible claimed fields only. It does not determine the hidden ProofInstance target, actual replay root/map, native group shape, extractor correctness, axiom support or availability. No source signature or portable freshness assertion is created by the copied row.

Define `LeadDigest(l)` as SHA-256 of ASCII `DTMKN-BROKER-LEAD-1`, one zero byte, u64be length of the canonical lead payload, then that payload. It is an exact local mutation comparison value, not a signature or acquisition capability. `expectedPriorOption` is `[0]` for no selected current self lead or `[1,digest32]` for that exact prior selected self lead. It never refers to another source's lead.

All input strings/bytes and contacts remain inert. There are no free-form instruction, script, arbitrary URL, source export-token or broker-referral fields. Rendering metadata to a local LLM does not grant it tool/policy authority. Query tokens/contacts/timing can disclose an investigation; owner authorization of those disclosures remains required.

## Synchronous mutation and acknowledgments

The authenticated caller is the source principal for operations 21 and 22. For 21 it must equal `selfLead.sourceNodeID`. Ordinary authorization/admission is checked before consulting any nonpublic metadata. This service mutates only the explicitly owner-authorized broker-public metadata collection; it neither exposes private metadata nor places a native pin.

An owner-selected automatic admission policy may accept a valid request within its reserved resources; it is not a promise to list every valid submission. Expensive bounded syntax validation/preparation may precede the decision. One authority-writer transaction then reads the actual current selected self lead, checks every prepared precondition, decides no-op/conflict/policy/capacity, applies any row/lead/posting changes, and selects the acknowledgment cut and self-lead observation. These actions share one linearization point, including no-op acknowledgments. An earlier executor comparison is not sufficient. Source self-mutations cannot replace another source's lead. Owner-local selection changes use the same serialized authority and finite accounting. Repreparation/retry consumes the same admitted grant; exhaustion yields charged nondecision, never an unchecked stale commit.

For submit/update (steps 2 through 5 are the single authority-writer decision just specified, not independent compare/commit phases):

1. Validate D, the self lead and the visible same-R relationship within the request bounds. No evidence or endpoint fetch is triggered.
2. If the exact proposed self lead is already selected in a currently listed row for d, return ALREADY_LISTED without mutation. This idempotent no-op may succeed despite an obsolete expected-prior value; it cannot overwrite anything.
3. Otherwise compare the selected current self lead with `expectedPriorOption`. A mismatch gives CONFLICT without modification. Expected absent is satisfied only by actual selected-self absence, not an unexamined old record.
4. If inserting would exceed four selected source leads or another actual policy/resource bound, decline or defer without a queued promise. The request cannot evict another source. An owner can separately choose and commit a different bounded lead set.
5. On acceptance, install/update this self lead, create the row/postings only if necessary, allocate its actual current/snapshot-version costs, commit a new public metadata cut and return LISTED.

For withdrawal, the caller identifies d and only its own source key is eligible for removal. If no currently selected self lead exists, return ALREADY_ABSENT without mutation. Otherwise its expected prior must be `[1,LeadDigest(currentSelfLead)]`; a mismatch gives CONFLICT. Remove that lead atomically. If it was the last selected lead, unlist the current row and its current token postings in the same transaction. Old authorized snapshots keep their immutable prior row only under their own live disclosure/retention scope. Source withdrawal supplies no global erasure promise and does not retroactively falsify the mathematical target.

Use the acknowledgment payload:

`[d,outcome,publicCutID32,selfLeadOption]`.

Outcome codes are 0 LISTED, 1 ALREADY_LISTED, 2 WITHDRAWN, 3 ALREADY_ABSENT, 4 CONFLICT, 5 DECLINED, 6 DEFERRED_NO_PROMISE. For 0/1, `selfLeadOption=[1,actualSelectedSelfLead]` at that cut. For 2/3 it is `[0]`. For 4/5/6 it is `[0]`, intentionally withholding unrelated state and making no selected-lead claim. A malformed/unauthorized request is a top-level failure, not an accepted acknowledgment. The full ack payload is at most 2048 bytes.

`publicCutID32` is an issuer-generated opaque identifier for the exact broker-public metadata cut at commitment; it is not a clock, native assessment or private-corpus count. Its binding to the actual immutable/current index state is owner-controlled, collision-checked for retained outcomes/snapshots under the issuer's existing local identity discipline. It is never used alone as an authorization token. Private changes do not advance or become visible through this public cut.

DECLINED and DEFERRED_NO_PROMISE commit no requested metadata change and create no background job, future publication obligation or retained per-rejection tombstone. DEFERRED means only that a new independently funded attempt may be appropriate. An admitted local queue, if the owner separately uses one, has its own allocation and is not promised by this result.

Ack outcomes are immutable computation observations, not proof of delivery or ongoing listing. An exact invocation replay returns its prior metadata through NET2; a fresh invocation sees the then-current state.

This interface deliberately selects **plain value-CAS**, not revision fencing. A delayed update expecting an absent former nonempty lead conflicts, but an independently admitted expected-absent submission can succeed after `absent -> listed -> absent`. Likewise `l0 -> l1 -> l0` satisfies a delayed comparison with l0. These are distinct unexecuted actions, not exact-action replay; hashing more strongly does not remove ABA. A no-op ALREADY_LISTED still selects its observed cut inside the transaction.

Withdrawal therefore removes the currently selected self value; it does not cancel every earlier distinct intent or guarantee lasting absence. A source requiring quiescent local withdrawal must first settle/cancel its outstanding mutations according to NET2 (cancellation before claim differs from uncertain/already running work), cease creating new ones, then obtain the withdrawal observation. It cannot claim stronger absence while any restoring intent is unresolved, nor control separate owner-local selection or already disclosed snapshots. No permanent tombstone/revision service or instantaneous global cancellation is introduced.

## Query, snapshots and progress

BrokerPredicate contains exact F/E typed IDs, one to four sorted unique 32-byte required tokens, and `targetOption=[0]` or `[1,targetRef]`. Its canonical payload is at most 2048 bytes. The predicate ID is its `0x8126/1` ContentID. There is no pattern field and no implicit native-pattern test. Unknown fields or modes are mismatches, not ignored extensions.

Match exactly the visibly claimed F/E, containment of every required token, and optional exact target reference. Choose the shortest required-token posting at the immutable snapshot, ties by token bytes; order by canonical d bytes. No target-filter shortcut changes the declared base ordering. This is the BROKER1 claimed-metadata predicate, not applicability.

Request unions are:

- `snapshotSelector=[0]` for a new snapshot or `[1,snapshotTokenBytes]` for exact resumption.
- `startPosition=[0]` for BEGIN, `[1,d]` for a new inclusive lower bound, or `[2,continuationBytes]` for resumption.
- New snapshots permit only start 0/1. Existing snapshots permit only start 2, whose original boundary/query must match. This small profile deliberately offers no independently redirected seek on a live snapshot.
- `pageCeilings=[maxRows,maxEncodedReplyBytes,maxPostingInspections]`, with `1..64`, `32768..1048576`, and `1..8192` respectively. Native work is not a query option. Actual offer/local allocations may be smaller and may decline the call; they do not silently change the predicate or resume position.

A snapshot binds its actual frozen row/lead/posting roots, public metadata cut, authenticated holder, exact predicate, original lower boundary, planner/schema/profile, metadata disclosure generation and finite issuer-local expiry. It has a distinct issuer-local snapshot identity. The issuer selects a positive lifetime of at most 600 issuer-local seconds at creation, reports the exact expiresTick in the token and never extends it by continuation. This is a ceiling, not a guaranteed 600-second lease. The small economic fixture selects at most 60 seconds. At most eight snapshot-slot allocations may be occupied; this includes reserved-but-not-created snapshots and retired snapshots whose active scans/root release have not completed. Retained bytes and independent in-flight results are additionally charged.

Tokens use the exact opaque wrapper `encode([tupleBytes,mac32])`, with both fields CBOR byte strings and tupleBytes the inherited canonical encoding of the ordered tuple below. Compute `mac32=HMAC-SHA-256(epochSecret,ASCII(domain)||0x00||u64be(length(tupleBytes))||tupleBytes)` under a broker-private random 256-bit admission-epoch secret. Domains are `DTMKN-BROKER-SNAPSHOT-1` and `DTMKN-BROKER-CONTINUATION-1` respectively. Each complete token is at most 2048 bytes. Snapshot tuple order is `[brokerNodeID,admissionEpoch,holderNodeID,snapshotID32,publicCutID32,predicateID,originalBoundary,plannerCode,metadataAuthorizationGeneration,expiresTick]`; plannerCode is 0 for this exact shortest-posting plan. The retained snapshot additionally binds its actual root objects; a token is not sufficient without that state. Continuation tuple order is `[SHA256(snapshotTokenBytes),inclusiveNextBoundary,initialPageCeilings]`, hashing the complete exact snapshot wrapper. Unknown/oversized fields, bad authentication or disagreement with retained state are mismatches.

Continuation calls may lower the initial ceilings but not raise them, even if another local resource grant is larger. A new larger query requires a new snapshot. All calls remain independently paid. Tokens confer neither storage authority nor a free scan.

Unlike some explicitly retained NET2 data scopes, this proposed broker profile chooses **not** to preserve query snapshots across an admission seal or uncertain restart. Expire/revoke them and their unclaimed derived disclosures; new-epoch work requires a new query. Already claimed executions/replies follow the exact existing NET2 bounded continuation/cancellation rules and do not recreate a snapshot or remote authority. Restart/seal cannot renew expiry, replenish an investigation budget or relabel a historical page current.

Boundary values in pages/continuations are `[0]` BEGIN, `[1,d]` inclusive d, or `[2]` END. Continuations cannot name END. A zero-progress partial page can repeat BEGIN or the same d. An END scan has no next continuation. The page payload is:

`[snapshotTokenBytes,predicateID,0,scanOutcome,originalBoundary,pageStart,pageEnd,candidatePayloads,nextOption]`.

Coverage code 0 means SERVER_DECLARED_BROKER_SNAPSHOT. Scan outcomes are 0 END, 1 MORE_OUTPUT_LIMIT, 2 PARTIAL_BUDGET. `nextOption` is `[0]` for END or `[1,continuationBytes]` for 1/2. `pageEnd=[2]` exactly for END; otherwise it is the next inclusive unprocessed boundary. `pageStart` is the requested/resumed boundary, and the page represents completed processing of its half-open interval. Candidate payloads are ordered, duplicate-free by d and obey the 16-KiB row bound.

Only complete tests and committed matching output advance the boundary. A match that does not fit is not processed. An interrupted test is not a negative test. At most 8192 posting entries, 0.25 CPU-seconds, two wall-seconds and 16 MiB query working memory may be spent per page under the admitted allocation. Graceful budget cutoff returns partial progress if it can safely commit within the reserved resources; a hard interruption instead follows ordinary charged abort/nondecision, not fabricated progress.

The entire encoded RESULT including NET2 envelope is at most the requested reply-byte ceiling and at most 1 MiB. All non-candidate material, including the page framing, outer envelope, result metadata and tokens, is at most 16 KiB; this is included, not extra. Thus an otherwise empty 32-KiB response can carry one maximum 16-KiB candidate. At most 64 rows fit; 64 is not promised when bytes bind first. No BUNDLE1 BODY stream or new frame kind is used. The ordinary 2-MiB frame ceiling is unchanged.

Rows observed in an old snapshot remain explicitly historical. Current metadata edits do not rewrite them. Owner withdrawal of their disclosure scope invalidates unclaimed deliveries and relevant snapshots; delivery claim atomically checks the exact scope/generation, and already disclosed bytes cannot be recalled. Source-native availability changes do not automatically change broker state, but actual later native reads always check the source's own authority.

## Snapshot retirement and supplied turnover

Reserve a counted slot before admitting a new-snapshot execution whose offer commits that resource; outstanding unclaimed reservations consume slots until actual cancellation/expiry/release. Creation converts its reservation into a retained snapshot without increasing the allocation count. Failed creation releases it only after actual outcome/recovery obligations permit release. Existing-snapshot calls borrow the retained slot but require their own execution, memory and result allocations.

On committing an END page, the authority writer also retires that snapshot for new scan claims. Later continuations get STALE_CURSOR. Already claimed scans may finish only within their original bounded grants; any returned continuation remains subject to actual retired/expired state and is not a promise of future admission. MORE_OUTPUT_LIMIT and PARTIAL_BUDGET do not automatically retire their snapshot. Abandonment, a lost first response or a hard-aborted first scan can leave an unreachable orphan snapshot until its original expiry. No keepalive, automatic renewal or close opcode is selected.

Expiry, END retirement, admission seal or applicable disclosure revocation prevents new scan claims. Actual slot release waits until the snapshot's retained roots and all already-claimed scan references can be released; retirement lag consumes stock and cleanup resources. Required immutable committed result bytes, exact-action outcomes and delivery authority are retained in their separately charged NET2 spool/record allocations, without retaining an unnecessary snapshot root. Query expiry/END alone does not erase a still-authorized immutable result delivery. Disclosure revocation and admission-seal rules above still revoke their specified unclaimed disclosures. A replay returns only the inherited exact outcome metadata, not permission to execute an expired query again.

For new-snapshot reservation j let r_j be its reservation tick and u_j its actual slot-release tick. A sufficient snapshot-stock condition is `sum_j 1[r_j <= t < u_j] <= 8` at every local time t, including unused offers, orphan snapshots and retired-but-pinned roots. Daily CPU/traffic totals alone do not imply this inequality. If every occupied slot lasts 600 seconds, ideal sustained turnover is only `8*86400/600 = 1152` starts/day, before overhead. Thus the small 10000/day fixture requires its separate short-lifetime/timing premises; it is not a universal throughput promise of this profile.

## Typed results and errors

For a successful mutation use top-level OK with the typed BrokerMutationAck body. For search END/MORE_OUTPUT_LIMIT use top-level OK; for a gracefully committed PARTIAL_BUDGET page use top-level PARTIAL. Query/body kind is determined by the exact operation, never guessed from a CID in an old FIND slot. BodyOption is `[1,payload]` for these typed bodies. Failures without such a committed body use `[0]` and the inherited exact error code.

Bad shape, role, expected schema or token binding gives REQUEST_MISMATCH; a well-formed unsupported broker namespace/profile gives UNSUPPORTED_PROFILE; invalidated/expired snapshot state gives STALE_CURSOR; denied metadata disclosure gives NOT_SERVABLE without private-existence detail; pre-execution capacity refusal gives BUSY_NO_ADMISSION; actual hard resource interruption gives the inherited LIMIT_EXCEEDED/ABORTED_RUNNING or unknown classification appropriate to its committed state. CONFLICT is a mutation-ack outcome, not an invented NET2 top-level result code.

All broker results set `publicAssessmentDigestOption=[0]`. For a committed typed body, `encodedBodyBytes` is exactly the length of its canonical payload. Bind `outcomeDigest` to SHA-256 of ASCII `DTMKN-BROKER-OUTCOME-1`, a zero byte, canonical ServiceCall CID bytes, u16be top-level result code, canonical typed body ContentID bytes, and u64be encodedBodyBytes. The type/schema is determined by the operation table; the body CID can be independently derived. This outcome digest supplies integrity, not native truth or proof of complete broker coverage. Ordinary no-body failures/replay metadata retain their inherited NET2 semantics.

## Supplied initial direct-service profile

The following is an example **selected-for-audit local policy**, not universal hardware, a measured service rate or a remotely granted quota. The owner must actually fund it; lower policies can refuse work. It does not raise any native, frame or kernel limit.

| Local aggregate | Maximum or supplied allowance |
|---|---:|
| Current rows / current plus retained row versions | 65,536 / 131,072 |
| Retained posting entries | 4,194,304 |
| All retained metadata/index/control/snapshot bytes | 4 GiB |
| Entire broker resident memory | 256 MiB |
| Concurrent admitted executions | 4 |
| Occupied snapshot slots / maximum created-snapshot lifetime | 8 including reservations/retiring roots / 600 local seconds; issuer may select shorter |
| Admitted F/E namespaces | 16 |
| Locally admitted pending work items | 128, with no remote deferred-job entitlement |
| Broker service CPU per supplied 86,400-second accounting interval | 3,600 CPU-seconds |
| Combined service traffic per such interval | 16 GiB, all directions/setup/failed work included |
| New paid broker executions per such interval | 20,000, shared by mutations and query pages |

Native evidence service has separate actual owners and allocations. The broker profile funds none of it. Pre-authentication, offer issuance, live control records, result spools, finite grants, disclosure state, garbage collection and inherited NET2 admission limits still apply inside the real aggregate resources; repeated fresh keys do not obtain another copy of these allowances. Carrying a reservation across an interval boundary does not mint new resources or evade charging. Counts are not promises that every dimension can be simultaneously maximal.

Query grants include their parsing, scan, commit and result preparation. A mutation grant admits at most one CPU-second, two wall-seconds and 16 MiB working memory; native fetch/checking is forbidden in it. Recurring ingestion, listing/snapshot retirement, durable accounting, source-independent cleanup and all paid failures share the total CPU/traffic/control budget. Rate/burst admission may decline excess work while unused aggregate stock remains; a daily total is not a latency guarantee.

The economics note's small 4000-to-4096-target known-contact fixture lies inside the count/stock envelope only under its stated actual-size/memory **and temporal occupancy** premises, including short selected snapshot lifetimes, outstanding reservations, orphan responses and retirement lag. Its recurring inequalities are a conditional service case, not a measurement. Every paid new execution, including failures, continuations, source updates and withdrawals, shares the 20000 count; offer/control work is separately charged whether or not executed. Eight search copies and two evidence sources provide different availability from eight evidence sources; selecting brokers does not authorize deleting a promised native copy. Useful yield, practical native costs and eventual retry behavior retain their separate module obligations.

## Concept conformance and limits

The direct module must pass paper traces for: exact self-lead idempotence; two prepared writes sharing a prior value; nonempty-prior delayed submit conflicting after withdrawal; expected-absent ABA insert succeeding after insert/withdraw; last-lead row retirement; fifth-lead refusal without eviction; current edits versus frozen snapshots; zero-progress pages; maximum-permitted-row bound at a boundary; changed query/holder/epoch; scope withdrawal before delivery; END retirement with an independently retained result; lost-first-response slot expiry; sustained all-MORE/PARTIAL snapshot stock; wrong-replay lead; group-constructor target; local bytes needing rechecking without downloading; and broker text/contact attempts to gain local tool authority. The 16-KiB row allowance is a bound, not a claim that every byte length up to it is constructible under the smaller descriptor/lead field limits.

An honest finite scan can cover its exact live metadata scope under sufficient admitted progress. Arbitrary broker messages cannot bypass the unchanged native predicate. Neither claim supplies unfamiliar-broker routing, query confidentiality, useful candidate recall, continuous evidence availability or universal economic superiority.

Selection requires independent review of these exact bindings and their composition with the broker/client/economic contracts. Broader broker routing remains a separately investigated module; its unclosed namespace/lifetime/cost sketch is not part of this direct service. No frozen H file or existing wire slot is changed by this candidate document alone.
