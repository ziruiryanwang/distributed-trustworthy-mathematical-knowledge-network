# Operational Corpus v1: direct exchange, independent admission, and preservation

Date: 2026-09-19. Status: CP-001D concept specification; no implementation, executable model, or test result is introduced here. CP-002 remains the future implementation checkpoint.

This document chooses one baseline protocol, called NET1. It implements the operational part of the [formal knowledge contract](FORMAL-KNOWLEDGE-CONTRACT-v0.md). It preserves the exact local accounting and current-reliance rules inherited from Cooperation Core v0, while replacing its fixed global federation with independently operated direct peers. Existing frozen documents are not edited.

Words such as MUST specify requirements on a future conforming implementation. Numerical defaults below are concrete starting policy choices, not measurements showing that a particular workload succeeds.

NET1 is one selected operable concept profile, not a claim that these particular constants are the only possible decentralized standard. Its semantic boundaries are firmer than its engineering defaults: a later reviewed profile can revise transfer sizes or capacities while preserving exact evidence identity, bounded authority, and independent admission.

## Scope and chosen deployment

NET1 consists of independently operated nodes with local object storage, local native verification, local operational ledgers, and optional remotely queryable local indexes. A node connects directly to explicitly known peers. It may consult at most four selected peers for one lookup round. A contacted peer MUST NOT recursively forward that lookup. Peers can advertise bounded object hints to established peers; they do not broadcast a theorem to the whole network.

There is no global peer roster, global membership epoch, public DHT, blockchain, universal publication log, shared budget, compulsory index, or central bootstrap service. Each peer connection, service offer, index snapshot, accounting epoch, and retention root belongs to one identified local authority. All byte replication in NET1 is full replication; erasure coding is not part of this profile.

An imported result becomes currently reusable only after the receiver has the complete required native closure in its own admitted storage and has checked it under its own policy. This deliberately makes current native replay independent of the source remaining online. A node need not store every result: it stores selected roots and their exact closures, with local deduplication of shared dependencies.

The system has no human-intention field, research assignment, unsolved-conjecture registry, or question-completion operation. Independent clients investigate outside the protocol. The operational jobs specified here are downloads, checks, index reads, serving, export, retention, and repair.

## Dependencies and authority boundaries

NET1 uses the [mathematical object profile](OPERATIONAL-CORPUS-V1-MATHEMATICS.md) for exact native judgments and certificates. It does not interpret an author's description as a theorem. It exposes the [organization profile](OPERATIONAL-CORPUS-V1-ORGANIZATION.md)'s bounded exact/structural FIND requests without making an index verdict authoritative.

`ReplayID` identifies the separate exact witness selection and complete replay manifest for a typed native root. For a proof root, `ProofID` identifies the judgment and native evidence, and descriptors also carry the corresponding `JudgmentID`; a proof ID alone is not a portable closure. Definition, opaque-construction, and declaration-group roots use the mathematical profile's own typed root and checking relation, not a fabricated theorem identity. NET1 publication, import, status, retention, and export roots select a ReplayID in every case. Validation binds the typed native root and ReplayID, plus ProofID/JudgmentID where that root kind supplies them. Generic GET_MANIFEST/GET_CHUNKS calls retrieve referenced typed objects but cannot infer a missing replay selection.

| Boundary | What crosses it | What does not cross it |
|---|---|---|
| External client to node | Candidate formal object identifiers and retrievable bytes | Human intentions, remote authority over local resources |
| Provider to receiver | Exact object bytes, bounded descriptors, operational observations | Publisher theorem acceptance, budgets, retention pins |
| Native checker to local authority | Exact outcome, checked footprint, environment and validation key | Authority to perform unfunded external effects |
| Local ledger to executor | One holder-bound, metered execution and hard envelope | An indefinitely reusable spend capability |
| Local index to client | Candidate IDs and a precisely scoped snapshot page | Global completeness, mathematical validity, global absence |

Matching profile roots, identical node software, or identical policy hashes do not make two nodes one authority. Every independent node re-admits imported mathematical evidence. NET1 does not merge independent spend ledgers or import foreign promotion flags into its own accepted evidence graph.

## Common encoding, identifiers, and cryptography

The wire and content encodings use the same restricted deterministic CBOR profile as the native mathematical layer:

- definite-length arrays, unsigned integers in the range \(0\ldots2^{64}-1\), and byte strings only;
- shortest integer and length encodings;
- no maps, tags, floats, text strings, indefinite lengths, duplicate logical fields, or trailing bytes;
- every record has the exact positional array shape shown by its schema;
- an optional value is `[0]` for absent or `[1,value]` for present; absence is never an omitted array position;
- finite enums are unsigned integer codes; prose names in this document are explanatory labels;
- unknown record versions, unexpected field counts, out-of-range enums, and unsupported mandatory profiles are rejected with a typed outcome.

A `ContentID` is exactly

\[
[1,\operatorname{type}_{16},\operatorname{schema}_{16},\operatorname{digest}_{32}],
\]

where the first value selects SHA-256, the next two values are unsigned 16-bit integers, and the last value is a 32-byte string. For canonical payload bytes \(b\),

\[
\operatorname{digest}
=\operatorname{SHA256}(\texttt{DTMKN-CAS}\Vert 0x00
\Vert\operatorname{u16be}(type)
\Vert\operatorname{u16be}(schema)
\Vert\operatorname{u64be}(|b|)\Vert b).
\]

`DTMKN-CAS` means those ASCII bytes exactly. Type and schema integers in this preimage use fixed-width big-endian encodings. They remain CBOR integers in the `ContentID` array. The current network schema version is 1. Network objects use types `0x8000` through `0x80FF`; organization objects use `0x8100` through `0x81FF`; mathematical object types use their separate allocated range.

NET1 assigns these network types:

| Code | Type |
|---:|---|
| `0x8000` | Node key record |
| `0x8001` | Contact bundle |
| `0x8002` | Raw byte chunk |
| `0x8003` | Byte manifest |
| `0x8004` | Service-call description |
| `0x8005` | Service offer |
| `0x8006` | Service result metadata |
| `0x8007` | Provider observation |
| `0x8008` | Export manifest |
| `0x8009` | Local retention acknowledgment |
| `0x800A` | Status observation |
| `0x800B` | Export manifest page |

Operational signatures use Ed25519. A signed record is `[payload,signature]`, where `signature` is a 64-byte signature over `ASCII("DTMKN-SIGNED") || 0x00 || encode(ContentID(payload))`. The payload's record type and schema are known from its envelope; a signature for one record type cannot authorize another. Public keys are 32-byte Ed25519 keys. Signatures authenticate scoped operational statements; they do not authenticate mathematical truth or real-world identity.

The mathematical `ContentID`, `JudgmentID`, or `ProofID` is never replaced by a byte-manifest ID, an index entry ID, or a service receipt ID. They identify different objects.

## Node identity, transport, and cold start

`NodeKey = [1,publicKey]`. `NodeID` is the content ID of that exact node-key record. Nodes use TLS 1.3 over TCP with mutual Ed25519 certificate authentication. A certificate is self-signed for the node key. A dialer pins the expected `NodeID` from its chosen contact; the receiver binds the connection to the client's demonstrated key. No public certificate authority or global enrollment service is required.

Peer validation checks the Ed25519 SubjectPublicKeyInfo, self-signature, expected node-key hash when dialing a selected contact, and TLS proof of possession. DNS names and a CA path confer no additional authority. Certificate validity dates are not used to create service time or extend an epoch; this pinned-key profile does not rely on certificate wall-clock dates for authorization. Local key revocation/denial remains authoritative even if a TLS certificate is otherwise well formed. One certificate is allowed, its encoded size is at most 4 KiB, and unsupported critical certificate features fail the handshake.

TLS authenticates the chosen key, not the trustworthiness of its operator. An untrusted bootstrap bundle can introduce hostile peers. Native checking remains independent of their honesty; discovery and availability do not.

An endpoint is `[addressFamily,addressBytes,port]`, where family 4 requires 4 address bytes, family 6 requires 16 address bytes, and port is in `1..65535`. NET1 does not require DNS. Both peers can issue requests over an established authenticated connection, permitting a node that can make outgoing connections to serve that connected peer. NET1 promises no universal connectivity between nodes behind arbitrary firewalls or NATs.

A contact bundle is `[1,[[nodeKey,endpoints]...]]`, with at most 32 contacts and at most four endpoints per contact. The total encoded bundle is at most 16 KiB. Bundles are untrusted discovery inputs, not membership certificates. An operator can import one from removable media, a previous export, another person, a software distribution, or any reachable site. A node can also begin with one manually supplied contact or with no network contacts and a local archive.

Cold start has two concrete paths:

1. **Offline start:** obtain the verifier/profile software and a portable archive; verify object identities, native closure, and local policy; operate without network access.
2. **Connected start:** obtain the software and at least one chosen contact; authenticate that contact's key; request its available profiles and optional index service; retrieve selected objects; check them locally.

If every supplied contact is unreachable, there is no protocol guarantee of discovering unknown peers. If every supplied contact censors the same objects, there is no discovery guarantee for those objects. Alternative contact bundles and direct addresses are required escape paths, not a proof that an honest path always exists.

## Framing and connection state

Each application frame is a four-byte unsigned big-endian length followed by one canonical CBOR array. The length excludes the four-byte prefix. A frame exceeding the hard limit is rejected before body allocation. A partially received frame has a 10-second idle timeout and a 30-second total envelope-read timeout.

Every message is

`[version,kind,senderNodeID,receiverNodeID,serviceEpoch,requestID,body]`.

`version=1`; `requestID` is 16 bytes generated independently for each logical request; sender and receiver must match the authenticated connection. Within a request/reply exchange, `serviceEpoch` always identifies the service-providing authority's epoch, including in its responses; it is not the receiving client's epoch. HELLO and unadmitted HINT use zero, while HELLO_REPLY advertises the responding provider's epoch. A response repeats its request ID. An unsolicited HINT uses a fresh message ID with no response entitlement.

Message kinds are fixed for this profile: `1=HELLO`, `2=HELLO_REPLY`, `3=OFFER_REQUEST`, `4=OFFER`, `5=CALL`, `6=RESULT`, `7=CANCEL`, `8=HINT`, `9=REFUSAL`. A REFUSAL has `[resultCode]` only and creates no service authority. An initial refusal need not allocate durable request state. OFFER issuance and paid CALL results use the idempotence rules below.

The initial exchange is `HELLO` and `HELLO_REPLY`:

`HELLO = [challenge32,supportedNetworkVersions,nativeProfileIDs,clientLimits]`.

`HELLO_REPLY = [challenge32,serverServiceEpoch,serverLimits,nativeProfileIDs,serviceKinds]`.

The reply echoes the challenge inside the authenticated connection. Each list contains at most 16 entries. Limits are numeric records in the fixed order of the limits table below. Neither side may negotiate a wire size above NET1's hard maximum. The peer advertises its actual lower local limits. A client must not infer that advertised native support means a remote theorem assessment can replace its own check.

The connection is stateful only for authentication, bounded flow control, and live requests. Mathematical objects, retention roots, and final admission assessments do not depend on keeping that TLS connection open.

Live TLS handshakes count against a separate pre-authentication reserve before application quotas apply. Defaults are eight incomplete handshakes, a 10-second deadline each, aggregate admission of four new handshakes/second with burst eight, and at most 64 KiB received per handshake. The implementation must bound socket buffers and certificate parsing work. These limits are aggregate, not fresh per-key entitlements. Host-level link and pre-application denial of service remain explicit availability assumptions.

## Concrete limits

Hard limits belong to NET1 compatibility. Local defaults belong to the named policy profile `NET1-DEFAULT`; an operator can lower or raise a local default up to the hard ceiling, subject to its aggregate resource reservation. Changing a default affects later admissions, not already committed grants or pins. Raising a hard limit requires a new network profile/version.

| Quantity | NET1 hard maximum | NET1-DEFAULT |
|---|---:|---:|
| Application frame | 2 MiB | 2 MiB |
| Control request body | 64 KiB | 16 KiB |
| HELLO or anonymous HINT | 4 KiB | 4 KiB |
| Wire CBOR nesting depth | 16 | 16 |
| One descriptor | 4 KiB | 4 KiB |
| FIND predicates | 8 | 8 |
| FIND result descriptors/page | 256 | 64 |
| FIND encoded reply including envelope | 1 MiB | 1 MiB |
| Byte-chunk raw data | 256 KiB | 256 KiB |
| Chunks in one GET_CHUNKS call | 4 | 4 |
| Byte-manifest encoded payload | 1 MiB | 1 MiB |
| Reassembled individual object | 256 MiB | 128 MiB |
| Distinct objects in one imported closure | 65,536 | 16,384 |
| Unique closure payload bytes | 8 GiB | 512 MiB |
| Declared dependency traversal depth | 1,024 | 512 |
| Active peer connections | 128 | 32 |
| Concurrent outgoing lookup peers | 4 | 4 |
| Live offered service tickets | 1,024 | 128 |
| Queued admitted service jobs | 4,096 | 256 |
| Concurrent paid network executors | 32 | 4 |
| Concurrent native checkers | 16 | 2 |
| Live hints | 16,384 | 4,096 |
| Hint bytes | 64 MiB | 16 MiB |
| Live local index query snapshots | 64 | 8 |
| Extra snapshot/copy-on-write bytes | 512 MiB | 64 MiB aggregate |
| Cursor lifetime in one service epoch | 600 seconds | 120 seconds |
| Unused service-offer lifetime | 300 seconds | 30 seconds |
| Retained control-record bytes | 1 GiB | 128 MiB |
| Live control records | 262,144 | 32,768 |
| Simultaneous export snapshots/pins | 64 | 4 |
| Explicit retained roots | 262,144 | 16,384 |

All count and byte limits apply together; a request cannot trade one for another. Reaching either limit causes explicit refusal, partial progress where the operation permits it, or a local allocation decision. It never permits silently truncated mathematical evidence to be accepted.

Further local defaults are:

- aggregate pre-admission control ingress: 64 frames/second, burst 128, at most 512 KiB/second, burst 1 MiB;
- aggregate HINT ingress: 16/second, burst 64, shared by all identities;
- aggregate newly offered service tickets: 32/second, burst 64, subject to live-record and resource reservations;
- control/replay response egress: 512 KiB/second, burst 1 MiB; responses may be dropped once this reserve is exhausted;
- admitted application transfer: 8 MiB/second each direction, burst 16 MiB;
- one native import: 60 CPU-seconds for parsing/checking, at most 1,200 seconds total wall time including at most 900 seconds transfer and 300 seconds native checking, 2 GiB peak checker RAM, and explicitly reserved transfer/staging bytes;
- one closure transfer attempt: at most 900 seconds, within its byte/object bounds, with no more than four live provider requests per receiver;
- one ordinary network service execution: at most 30 seconds wall time and 1 CPU-second unless its operation has a smaller stated bound;
- object storage allocation: 32 GiB live unique retained bytes; inert staging: 1 GiB; derived index: 256 MiB; all are separate aggregate ceilings;
- HINT TTL: 600 seconds in the receiver's current boot; failed-provider backoff: 1, 4, 16, then 60 seconds with local jitter and bounded state;
- provider observation lifetime: at most 600 seconds in the issuing service epoch; it is an observation/promise scope, not proof of remote current availability.

Live unclaimed offers and queued jobs together must fit the queued-job allocation; issuing offers does not overbook future queue slots. Transient computed response bodies have a separate 32 MiB default aggregate reserve and a 30-second delivery lifetime. A service unable to reserve its reply body and delivery envelope is declined before making an offer.

These are enforceable envelopes only under the declared host isolation and metering assumptions. They do not prevent an adversary from saturating a physical link before application admission. Byte meters count bytes submitted to or received from the application transport; TCP/TLS retransmission and framing overhead are separately charged to the host's bounded networking reserve, not falsely reported as theorem payload bytes.

Lower-power nodes advertise lower service limits and may serve selected existing bytes while declining native verification of a large closure. An unsupported or over-budget object remains potentially valid mathematics; that node has made no mathematical refutation.

## The minimal remote service protocol

NET1 deliberately uses one paid service primitive instead of a separate ad hoc resource scheme for every message. A remote operation is `OFFER_REQUEST -> OFFER -> CALL -> RESULT`. A node creates equivalent local tickets for its own fetch, check, index, retention, and repair work. An offered service reserves both its operation and a distinct one-shot reply-delivery allocation before becoming visible; completing computation does not make subsequent network writes free.

### Service-call descriptions

`ServiceCall = [operation,arguments]` is content-addressed with network type `0x8004`. The operation enum is:

| Code | Operation | Arguments |
|---:|---|---|
| 1 | FIND | The exact bounded organization-profile query and optional cursor |
| 2 | GET_MANIFEST | `[readScope,objectContentID]` |
| 3 | GET_CHUNKS | `[readScope,objectContentID,[[chunkIndex,chunkContentID]...]]`, one to four entries |
| 4 | GET_STATUS | `[rootReplayID,requestedPolicyView]` |
| 5 | EXPORT_HEAD | `[retainedReplayID]` |
| 6 | GET_PROVIDER | `[rootReplayID]` |
| 7 | GET_ROUTES | `[nativeProfileID,queryKeys,excludedNodeIDs]` |

`requestedPolicyView` is `[0]` for the server's current local profile, or `[1,policyRoot]` for a specifically retained supported view. Requesting a view does not cause the server to load arbitrary remote policy code. An unknown view returns `UNSUPPORTED_PROFILE`.

For mathematical-result status, the requested root is a `ReplayID`; the returned observation names its exact typed native root, with proof/judgment fields present only for a proof root. It must not invent mathematical status for an unselected ProofID or coerce a nonproof root into a theorem.

`readScope` is `[0,publicReplayID]` or `[1,exportID16]`. A public-root scope requires that the root belongs to the node's explicitly authorized `PUBLIC_SERVE` collection and that the requested object belongs to its locally checked exact closure. An export scope additionally binds the authenticated audience and a live finite export snapshot; it permits only the native objects and explicit export root/pages named by that snapshot. For GET_CHUNKS, each index/ID pair must match the permitted object's locally derived byte manifest. The server checks scope membership before reading arbitrary CAS entries.

Locally private, quarantined, control-ledger, grant, ticket, meter, authentication, and unrelated operational objects are never exposed through generic content-addressed reads. Their IDs confer no read permission. FIND exposes only a public projection of the `PUBLIC_SERVE` collection. GET_STATUS and remote EXPORT_HEAD require a public root; GET_PROVIDER reveals only explicitly public provider observations. An unauthorized scope returns `NOT_SERVABLE` without distinguishing private existence from absence. Shared chunks are served only when they occur in an authorized object's verified byte layout.

There is no remote operation `ACCEPT_THEOREM`, `PIN_FOREVER`, `SPEND_FOREIGN_GRANT`, `ASSIGN_RESEARCH`, or `SOLVE_QUESTION`.

### Offer request and offer

`OFFER_REQUEST = [callCID,operation,callByteLength,requestedReplyByteLimit]`.

It is a bounded request for service, not spend authority. It can be refused without a durable per-request record. Repeated requests and new identities share aggregate onboarding limits. Before offering service, the provider's local policy selects a finite service class and creates a receiver-local root grant/ticket allocation under the inherited ledger invariants.

Successful offer issuance stores the request digest under `(issuerEpoch,clientNodeID,envelopeRequestID)` before returning the offer. Repeating that exact issuance request returns the same offer or its terminal outcome; changing its digest is a mismatch. Accepted issuance keys remain remembered until epoch retirement. A provider cannot discard one and then treat the same active-epoch request as authority to issue another offer. Rejected requests need no persistent negative record.

`ServiceOfferPayload = [issuerNodeID,serviceEpoch,offerID16,audienceNodeID,callCID,operation,callByteLimit,replyByteLimit,resourceCeiling,issuedTick,expiresTick]`.

The response is its signed record. `resourceCeiling` has the fixed numeric order `[cpuMilliseconds,wallMilliseconds,applicationReadBytes,applicationWriteBytes,peakMemoryBytes,scratchBytes,storageIOBytes,controlRecordUnits]`. The wire ceiling is an offer's remote-readable limit; the issuer additionally maintains its complete inherited local resource vector, including byte-time or conservative envelopes where relevant. The signature does not replace the issuer's authoritative ledger.

An offer is audience-bound, exact-call-bound, issuer-bound, epoch-bound, nondelegable, and single-redemption. NET1 uses two preallocated issuer-local root tickets under the offer's local grant: one holder-bound operation ticket and one issuer-executor-only reply ticket. Each has `maxRedemptions=1`, `childTicketFanoutLimit=0`, and no child grants. The offer's resource ceiling covers their summed allocation. The caller can redeem only the operation ticket; it acquires no ability to choose a different reply or issue descendants.

The wire offer expiry is the deadline for admitting the call. The issuer's enclosing grant and preallocated reply ticket have later, finite deadlines sufficient for the admitted operation and one bounded reply attempt; the default maximum is 90 seconds from offer issuance. There is no caller-extensible renewal. An expired or revoked offer cannot start an operation, and an expired reply allocation produces no unfunded send.

An unused offer reserves its issuer-side ticket allocation until expiry or explicit terminalization. This is intentional: accepting offers already consumes scarce capacity. Unfamiliar clients share one bounded onboarding lane, so an unbounded number of new keys cannot reserve an unbounded fraction of service. This does not guarantee that an honest newcomer wins admission during an unlimited Sybil flood.

### Call, execution, and result

`CALL = [signedOffer,redemptionActionID16,serviceCall]`.

The provider checks the authenticated audience, exact call CID, operation, body bound, current epoch, expiry, revocation, and unspent ticket. One atomic local transition creates the reservation identified by `(offerID,redemptionActionID)`. Another atomic claim creates exactly one provider-controlled execution and authoritative meter. No storage/index query or payload transfer begins before that claim.

The remote key is the authorization principal; only the issuer's fenced local executor performs the service. NET1 does not let a remote client supply its own metering result. All protected effects remain bound to the one reservation/claim pair.

`RESULT = [offerID,redemptionActionID,resultCode,resultMetadata,bodyOption]`.

Result codes are:

| Code | Meaning |
|---:|---|
| 0 | OK |
| 1 | PARTIAL, a typed resumable page operation only |
| 2 | NOT_FOUND_IN_LOCAL_VIEW |
| 3 | UNSUPPORTED_PROFILE |
| 4 | LIMIT_EXCEEDED |
| 5 | BUSY_NO_ADMISSION |
| 6 | EPOCH_RETIRED |
| 7 | OFFER_EXPIRED_OR_REVOKED |
| 8 | REQUEST_MISMATCH |
| 9 | REPLAY_RESULT, prior immutable outcome metadata only |
| 10 | REPLAY_EXPIRED, no reexecution occurred |
| 11 | STALE_CURSOR |
| 12 | CANCELLED_BEFORE_CLAIM |
| 13 | ABORTED_RUNNING, charged terminal nondecision |
| 14 | UNKNOWN_RESOURCE_OR_AVAILABILITY |
| 15 | ERROR_LOCAL_FAILURE |
| 16 | NOT_SERVABLE |

`resultMetadata = [issuerNodeID,serviceEpoch,localOutcomeID16,callCID,outcomeDigest,publicAssessmentDigestOption,encodedBodyBytes]`. `encodedBodyBytes` is the known byte length of the canonical response body, not bytes received by the requester. `outcomeDigest` binds the computed typed result and exact body identity, excluding delivery meters and mutable transmission state. Any public assessment digest refers only to the deliberately exposed public result projection; it is not a capability to fetch private validation or policy records. Metadata cannot make the issuer's mathematical assessment authoritative at another node.

The operation first prepares the bounded typed reply in its inert response buffer. Its final authority transaction records computation/staging charges, immutable result metadata, any authorized operational snapshot/pin allocation, and a nonauthorizing reply-delivery intent. This is an operational result commitment, not mathematical promotion or support. It occurs before reply bytes are sent.

The provider's reply executor then claims the separately preallocated issuer-local delivery ticket. It sends the committed reply to the exact authenticated audience, meters application bytes handed to TLS while its own reservation is RUNNING, and finalizes that delivery reservation separately. A send failure or crash can occur after the computation committed; the result remains the computed result, while delivery can be failed or unknown. Neither a write completion nor a settlement proves that the peer received or retained the bytes. Finalizing the computation never releases the reserved reply allocation to unrelated work before its delivery ticket is terminalized.

For replies exposing corpus bytes or metadata, computation commit also records the exact local disclosure scope and its authorization version in the private reply intent. Delivery claim atomically rechecks that this same scope/version is still authorized for this audience. A withdrawn or revised scope cancels an unclaimed delivery without rewriting its immutable computed result; a later permitted read needs a fresh computation. Withdrawal revokes pending derived export/read scopes as specified by that local disclosure authorization, independently of whether their storage pins still exist. If delivery has already claimed, withdrawal requests bounded executor cancellation and settles the actually metered handoff to TLS. Bytes already handed to TLS or disclosed cannot be recalled; no current-confidentiality guarantee is made for an already running transmission. Unrelated authorization changes do not invalidate an unchanged scope/version.

If no connection or reply capacity remains before its bounded expiry, the delivery ticket finalizes without successful delivery. The original operation is never rerun to repair delivery. Control-budgeted replay metadata or a fresh paid read is the recovery path. Large reply bodies can expire from their bounded buffer independently of immutable outcome metadata.

A service `OK` is not mathematical acceptance: for example, GET_STATUS can successfully return a historical rejection or current unknown state. Native admission, advertisements, and replication use their own funded executions. In particular, a theorem-promotion transaction may create a replication intent, but the operation/reply pair above does not authorize that replication.

## Idempotence, replay, expiration, and cancellation

The issuing node durably stores one request digest for each admitted `(serviceEpoch,offerID,redemptionActionID)`. An exact duplicate returns the prior outcome metadata or in-progress status under the aggregate control-response allowance. A different digest for the same action key returns `REQUEST_MISMATCH` and never changes the original execution.

Idempotence concerns execution and state effects, not free delivery. Every repeated reply consumes egress/control resources. A client that lost a large result body may request the same immutable bytes or snapshot page using a fresh paid call. The original action must not rerun merely because a response was lost.

Result-body caching is optional and bounded separately. The required replay record is a bounded outcome digest/summary, not an indefinitely retained copy of every response. After safe epoch retirement and replay-cache compaction, an old completed request can return `REPLAY_EXPIRED`. It must never be treated as a fresh request.

`CANCEL = [serviceEpoch,offerID,redemptionActionID]` is accepted only from the offer's authenticated audience or local operator. It has these exact meanings:

- Before reservation: terminalize the unused offer; release only unallocated service resources; issue/control allowances stay consumed.
- `RESERVED`: race atomically against claim; if cancellation wins, finalize unclaimed with zero protected execution and one consumed redemption.
- `RUNNING`: request executor termination; do not release its reservation or make it claimable again. Finalize once as a charged `UNKNOWN/CANCELLED_RUNNING` outcome using authoritative meters and conservative gap bounds. Late successful output cannot upgrade it to promotion.
- Operation `FINALIZED`, reply not yet claimed: the original computation is unchanged, but cancellation may finalize the separate unclaimed reply ticket and release its unused delivery envelope.
- Operation `FINALIZED`, reply `RUNNING`: request termination of that reply execution, then charge and finalize it; never roll back the computed result.
- Both tickets `FINALIZED`: return prior terminal metadata under the control allowance; no state change.

Releasing unused work allocation never restores fresh-object, fanout, redemption, or replay-record creation allowances. This preserves the inherited protection against infinitely many zero-work reserve/cancel records.

## Crash-safe service epochs

Each authority has one fenced writer for its operational ledger. Before accepting service after any startup or writer change, it durably advances a monotonically increasing `serviceEpoch`. Remote service/capability deadlines are `[serviceEpoch,monotonicTick]`. Separately, receiver-local warm-retention deadlines are `[retentionClockGeneration,monotonicTick]`, where that durable generation advances on actual startup/writer takeover or any inability to establish continuity of the local monotonic time origin. Ticks are local and nondecreasing only within the established boot/writer time origin. Clean service-epoch rollover keeps `retentionClockGeneration` and its existing deadlines unchanged; it does not churn or extend warm roots merely to compact service records.

Startup performs these steps before new protected work:

1. acquire the exclusive writer fence and advance the durable service epoch and retention-clock generation;
2. make all prior-epoch offers and cursors unusable for new work;
3. recovery-finalize old RUNNING claims as nonpromoting unknown outcomes, charging authoritative observations plus conservative bounds for every missing component;
4. finalize or cancel old unclaimed reservations and terminalize associated offers;
5. restore persistent pinned roots, committed assessments, outstanding byte allocations, dirty reliance state, and nonauthorizing outbox intents; expire old-generation warm retention conservatively before any positive reuse observation;
6. open the new epoch only after the authority invariants hold.

A wall-clock rollback cannot revive a ticket. Rotating the service epoch does not erase cumulative charges or automatically replenish the node's aggregate service budgets. Admission token buckets and storage allocations persist conservatively across recovery; missing timing information does not grant a full new burst.

An old action key is rejected by the durable retired-epoch rule even when its individual replay record has been removed. Epoch retirement requires that no live claim or descendant allocation remains; NET1 has no remote descendants. Compaction retains enough cumulative accounting and epoch-floor state to prevent reactivation. It does not reclaim already spent resources.

### Clean rollover without a reboot

The authority also rolls epochs during continuous operation, because remembered issuance/replay keys cannot accumulate forever in a finite control store. The default trigger is 75% of the control-record count or byte allocation, or 24 hours of one service epoch, whichever occurs first. A stricter early trigger is required if the remaining capacity cannot cover the already reserved worst-case finalization records. Before issuing any offer or local job, admission reserves its complete bounded terminal-record footprint, so a burst cannot consume the records needed to settle existing work.

Rollover follows `OPEN -> DRAINING -> RETIRED -> OPEN(newEpoch)`:

1. Enter DRAINING atomically; stop issuing new offers and admitting new local jobs. Already issued live offers retain only their original finite admission deadlines; their reserved work is accounted for in the drain.
2. Finish or cancel existing operation and reply tickets, local imports, snapshot/cursor leases, and export leases using their original finite bounds. Drain finalization and recovery retain reserved local capacity. A clean shutdown may abort an admitted execution under the existing charged-nondecision rule; it never silently grants it a fresh deadline.
3. Release or terminate every service-epoch-scoped lease. Locally authorized warm roots retain their exact unchanged retention-clock generation/deadline; persistent pins, cumulative charges, retained assessments, and nonauthorizing outbox intents survive. None acquires new remote service authority. Actual warm expiry still takes effect immediately even while the node is draining.
4. Once every old-epoch execution claim and epoch-scoped authority allocation is terminal, atomically advance the durable epoch/floor, retire its cursor secret, and compact its issuance/replay records. Persistent funded storage allocations are carried unchanged into the new ledger view, not released and reminted. Install a fresh cursor secret and reopen only after the ledger invariants hold.

This can pause new admissions until the longest still-admitted finite job settles: at most its residual 1,200-second default import envelope, plus bounded recovery/finalization under a stable functioning host. Repeated crashes or failed storage can prevent progress; rollover is not a failure-free availability promise. Rotation neither replenishes cumulative budgets nor resets rate tokens. Only an independently authorized standing-policy renewal can fund later work.

Service epochs, retention-clock generations, monotonic deadline arithmetic, sequence counters, and cumulative uint64 fields use checked arithmetic. Approaching exhaustion stops affected admissions before overflow; the node fails closed or explicitly migrates to a new reviewed profile/authority with fresh local authorization. No counter wraps, and no migration revives old capabilities. A fresh identity is not a mathematical trust endorsement or an exemption from another node's aggregate limits.

Recovering from an arbitrarily rolled-back whole-disk image is outside ordinary crash recovery. If a node cannot establish that its persisted epoch/accounting history is current, it must restore under a new node key/identity and independently re-admit any retained artifacts; it must not resume old service authority from the stale image.

This baseline has one local ledger writer, not a Byzantine replicated authority. Full object mirrors are independent nodes with their own ledgers. Adding multi-writer authority would require a different explicitly specified fencing/consensus protocol.

## Bytes, manifests, and direct fetch

`RawChunk` payload is a CBOR byte string containing at most 256 KiB of raw bytes. Its chunk ID uses network type `0x8002`. The canonical mathematical object payload is sliced into consecutive 256 KiB raw segments, with only the final segment shorter. Empty payloads, if permitted by an object's profile, have an empty chunk list; the ordinary native object schema determines whether such a payload can be valid.

`ByteManifest = [objectContentID,totalPayloadBytes,262144,[[chunkCID,rawLength]...]]`.

All nonfinal chunks have raw length 262,144; the final chunk length is in `1..262144`. The sum equals `totalPayloadBytes`. The number of entries is consistent with the object-size ceiling. The manifest has its own `0x8003` ID.

After checking its read scope, GET_MANIFEST returns `[manifestCID,manifestPayload]`. GET_CHUNKS returns an ordered array of `[chunkCID,chunkPayload]` records for all exact requested IDs. If any requested chunk is unavailable or corrupt, it returns `UNKNOWN_RESOURCE_OR_AVAILABILITY` with bounded unavailable-index reason data and no successful chunk-body array. The caller can issue a fresh paid request for a smaller subset or another provider. `PARTIAL` is reserved for resumable FIND pages, not incomplete chunk success. No operation silently substitutes different chunks.

A completed object is accepted as bytes only after reassembly and recomputation of its original content ID from the canonical full payload. Correct chunk hashes alone are insufficient. Internal native expression DAG depth and native canonical-payload size follow the mathematical profile; the effective bound is the minimum of its limit, NET1's limit, and the locally admitted envelope. NET1 wire depth 16 applies to outer CBOR records, not to native objects carried as opaque bytes before protected native parsing.

A byte manifest establishes a proposed byte layout, not a mathematical dependency closure. The dependency closure comes from the exact mathematical package/profile. The receiver's profile parser extracts or checks all required references. A source-supplied list that omits a native dependency does not permit acceptance.

Fetch proceeds as follows:

1. Local policy selects a candidate descriptor or explicit object ID.
2. Allocate a receiver-local fetch/check envelope before requesting manifests or payloads.
3. Fetch and check bounded manifests. Reject type mismatches, inconsistent chunk lengths, out-of-range counts, and unsupported encodings before large allocation.
4. Fetch missing chunks directly from selected willing providers. Each provider independently authorizes and meters serving; the requesting node independently meters receiving and staging.
5. Reconstruct and verify each exact object ID in inert staging. Existing local chunks can be reused only after local integrity verification or an applicable current integrity cache entry.
6. Traverse exact mathematical dependencies under the unique-object, byte, edge/depth, and time ceilings. Maintain a visited set charged to the same reservation. Detect forbidden dependency cycles according to the native profile; a repeated reference is not new authority or new work.
7. Invoke only the locally admitted native parser/checker for this profile. Peer source files, elaborator plugins, compiled caches, shell commands, or proof tactics are not executed on the acceptance path.
8. Either finish local admission within the original envelope, or finalize a bounded `UNKNOWN`, `REJECT`, or `ERROR`. Resource exhaustion does not refute the theorem.

A closure that crosses a local bound can be retried only through a fresh locally authorized larger envelope, within NET1 hard limits. It cannot repeatedly extend its original reservation by discovering new dependencies. A remote hint cannot induce automatic unlimited fanout or recursive fetching.

## Exact discovery and snapshot pagination

NET1's FIND operation carries the organization profile's exact query. The baseline supported modes are `EXACT_JUDGMENT`, `MENTIONS_ALL` with at most eight exact declaration IDs, `HEAD_SHAPE` with exact extractor version and bounded optional keys, `DEPENDENTS_DIRECT`, and `RELATIONS` for one exact endpoint and typed relation kind. These are lookups of existing records, not requests to solve a mathematical problem.

Each remote FIND operates over one immutable provider-local admitted descriptor snapshot filtered to its explicit `PUBLIC_SERVE` collection. A node's separate local index can also contain private/local-only material. The public snapshot binds `issuerNodeID`, `serviceEpoch`, `snapshotID`, public collection/filter root, local index schema/extractor roots, its admitted-corpus/index cut, and a conservative local reliance epoch. Descriptors are self-contained public hint projections; they do not expose arbitrary private validation, footprint, or control-record CIDs as fetchable references. Exact native assumptions are recovered and checked from the permitted replay closure. Descriptors may be historical observations from that cut; they are candidates at the receiver, not current receiver reliance assertions.

For each page, the organization profile enforces at most 8,192 scanned posting entries, 250 CPU-milliseconds, 2 wall-seconds, 16 MiB working memory, the descriptor limit, and the total 1 MiB encoded response limit. It stops before exceeding the first relevant bound.

`FindPage = [snapshotToken,queryCID,coverageCode,scanOutcome,descriptors,nextCursorOption]`.

`coverageCode=0` means `SERVER_DECLARED_LOCAL_SNAPSHOT`. A signature or opaque cursor does not prove global or even Byzantine-server-local completeness. `scanOutcome` distinguishes `END_OF_LOCAL_MATCH_SCAN`, `MORE_RESULTS`, and `PARTIAL_SCAN_BUDGET`. The last can return zero descriptors and a continuation cursor; it is never converted to an empty complete answer.

A cursor is an opaque server-authenticated byte string encoding the exact tuple

`[issuerNodeID,serviceEpoch,holderNodeID,snapshotID,queryCID,extractorRoot,plannerVersion,scanPosition,expiresTick]`.

`scanPosition` is the organization's precisely resumable scan position, not merely the last returned result; this is essential when a budget is exhausted while scanning nonmatches. The issuer authenticates the encoded tuple with HMAC-SHA-256 under a random 256-bit current-epoch secret confined to its local authority; the cursor is `[encodedTuple,mac32]` inside the opaque cursor byte string. Cursor contents convey no right to storage or free query execution: each continuation needs a fresh paid service call.

The chosen organization scan fixes one canonical ordered base posting list. Its exact `scanPosition` union is `[0]` for initial, `[1,nextDescriptorID]` for the least item not completely processed, and `[2]` for complete. Resumption seeks the inclusive lower bound of `nextDescriptorID` in that same immutable base list; the fixed query/planner determine the list. An item is complete only after its membership test finishes and, if it matches, its descriptor has been included in the committed page. If a matching descriptor cannot fit the page's remaining byte/count budget, or its test is interrupted, it remains the next item and is retried on the next paid page. This avoids silently skipping nonmatches, half-examined candidates, or matches stranded at a response boundary.

A changed query, holder, schema, planner, epoch, expired snapshot, or missing snapshot state gives `STALE_CURSOR` or `REQUEST_MISMATCH`. A cursor is never silently resumed against a newer snapshot. Snapshot limits count both snapshot records and extra pinned/copy-on-write bytes. Admission can fail rather than retaining unlimited old versions.

When an old snapshot expires, a caller starts a new query explicitly. Results may repeat or differ. The client deduplicates exact candidate IDs within its own bounded cache; it does not treat repeated results as independent evidence.

No negative result means that no such theorem exists in mathematics, in the open network, or under another representation. An honest complete local scan establishes only absence from that exact local snapshot and query interpretation. A remote receiver treats that assertion as the index server's scoped observation unless it independently verifies the full coverage.

## Hints, optional indexes, and correction observations

`HINT = [rootReplayID,objectKind,descriptorIDOption,providerObservations]`, with at most four provider observations and a total 4 KiB envelope bound. A hint can be received on an authenticated connection or imported in an offline bundle. It cannot request payload execution, create a pin, issue a priority class, or assert local acceptance.

`ProviderObservation = [providerNodeID,serviceEpoch,rootReplayID,endpoints,retentionAckOption,issuedTick,expiresTick]`, signed by the named provider, with at most four endpoints. GET_PROVIDER takes one exact ReplayID and returns at most four explicitly public observations for exactly that root already known by the responding node; it is not an arbitrary private-object-to-root lookup. These are routing hints. A receiver cannot convert another machine's ticks into its own wall clock or infer freshness merely from recent receipt of an old signed record. A live authenticated response to its own current request establishes only the responding peer's current scoped assertion; an actual fetch is still needed to obtain bytes.

Before local selection it changes only the bounded expendable hint cache and telemetry. Hint replacement/expiry is local; there is no durable per-rejected-hint tombstone. A node may advertise the same bounded frame to at most four locally selected established peers, charged to its own dissemination reserve. NET1 recipients do not automatically forward received hints; a later independently selected publication is a new local decision.

Optional index providers may index objects they have locally checked and retained, or expose separately labeled advisory provider descriptors. The two descriptor kinds must not be conflated. A descriptor that says another provider has bytes remains an availability hint.

There is no required global feed or standing remote subscription record. A node can perform locally scheduled FIND and GET_STATUS calls over its selected peers and active retained roots. The schedule is bounded by local resources. No peer can install an unbounded callback or force another node to poll.

### Bounded routing beyond the initial contacts

The node maintains a local `PeerDirectory` with at most 256 contacts and 256 KiB aggregate directory allocation, including encoded contact data and bounded local response statistics. Each lookup's tried set and pinned directory view consume its separately reserved query memory. A contact can advertise at most 16 exact native-profile or structural-category keys for its optional index. Contact entries come from manually imported bundles, direct public provider observations, or GET_ROUTES. They are untrusted hints and create no new service class or storage entitlement.

GET_ROUTES is a paid one-hop read of the server's explicitly shareable contact hints, not recursive query execution. It accepts at most eight query keys and 16 excluded node IDs, returns at most eight contact records, and fits a 16 KiB reply. A record is `[nodeID,endpoints,nativeProfileIDs,indexKeys]`, bounded by the same per-contact endpoint/profile/key limits. A server discloses only contacts marked locally shareable; private connection state is not a public routing directory.

For one lookup round the receiver selects at most four distinct compatible directory peers. Up to three are ranked by matching-key count, then the locally observed count of successful relevant responses in the last 32 completed calls to that peer, then canonical NodeID as tie-break. One remaining slot follows a persistent round-robin cursor over compatible peers ordered by NodeID. Self-advertised coverage affects candidate selection only; local service outcomes do not certify mathematical correctness.

Later rounds, if independently funded by the receiver, select previously untried compatible contacts within the initially pinned snapshot of that bounded directory. Its at most 256-contact tried set prevents loops. Refreshes and new route hints can seed a new separately funded lookup session; they cannot expand or reset the active session's snapshot, tried set, or authority. The declared lookup horizon is at most that admitted initial directory snapshot; it is never the entire open network. No peer automatically forwards a FIND or follows every GET_ROUTES answer.

Network HINT supports exact native negative/counterexample evidence through an ordinary proof-root ReplayID; it does not introduce generic incident-CAS objects or bypass public read scopes. A local NativeRefutation annotation is derived from that checked negative proof under the mathematical profile's exact target/context rule, not fetched as a new root kind. Same-context opposition alone is not a validity veto: opposite conditional derivations can both be sound when their common context is uninhabited. A closed contradiction must instead be independently composed/replayed under a compatible joined basis before the locally adopted basis-incident policy can suspend affected reliance.

A remotely alleged checker defect, binary compromise, or corruption report requiring nonnative evidence is out-of-band advisory input to local policy in NET1, not an unspecified additional wire authority. No remote hint can itself advance the receiver's reliance epoch, dirty every dependency, revoke a checker, or override policy. Only a precisely applicable locally admitted incident, locally detected corruption, or locally authorized profile-disable/policy event can do so under the integrated contract. After that local event commits, affected current reliance fails closed immediately; cross-node learning remains conditional on communication and admission.

## Local checking, retention, and publication lifecycle

The local candidate lifecycle is

`SEEN_HINT -> SELECTED -> STAGING -> CHECKING -> FINALIZED`.

These are operational states. Only finalization can add a checked mathematical assessment or promote retained roots; they do not represent stages of a research question.

`FINALIZED` records one of:

- `CHECKED_AND_RETAINED`: exact native check and local evidence policy passed, and full required closure was atomically admitted under a retention allocation;
- `CHECKED_NOT_RETAINED`: historical native success, but no current retention-backed reliance is advertised;
- `EVIDENCE_REJECTED`: the submitted evidence failed the exact relation or policy; distinguish these reasons;
- `UNSUPPORTED_PROFILE`, `UNKNOWN_BUDGET_OR_AVAILABILITY`, or `ERROR_LOCAL_FAILURE`.

Native checking outcome, policy admissibility, current reliance, availability, and retention remain separate fields. A result can be a correctly checked derivation in its stated theory yet inadmissible as a premise under the receiver's axiom policy.

An authenticated local client can submit `[rootReplayID,sourceReferences,publicationMode]` through the node's owner-authorized local interface or import a portable archive. `publicationMode` is `LOCAL_ONLY` or `PUBLIC_REQUESTED`; it is a request to local policy, not remote storage authority. It has no research-task or intention field. The same bounded parse/fetch/check/retention path applies to local candidates. File archives are inert data: member names cannot cause arbitrary filesystem paths, symlinks, scripts, or local secret reads to be followed.

`PUBLIC_SERVE` activation is a separate explicit local authorization covering the full exposed native closure. The node does not automatically publish a private dependency merely because a candidate refers to its CID. Publishing a root can proceed only when every exposed dependency is already public or its disclosure is locally authorized. On successful activation and indexing, the node may fund an outgoing HINT. A result can remain checked and locally reusable while not remotely served.

All inert bytes are durably staged and identity-checked before the admission commit. The authority transaction commits the assessment, exact selected evidence references, retention allocation, reliance epoch/dirty state when needed, local transactional metadata, resource settlement, and deterministic nonauthorizing outbox intents. A crash orphan not referenced by that commit is not admitted knowledge.

An index implemented inside that same authority transaction can receive its descriptor atomically. An external or asynchronous index receives only a pending outbox intent. Its descriptor is not reported as present until the separately funded indexing execution commits. The same rule applies to remote replicas, advertisements, export publication, and notifications.

The profile permits a historical `CHECKED_NOT_RETAINED` assessment to survive within a bounded local assessment store. It does not keep the underlying proof available by implication. Such an assessment cannot be served as `CURRENT_REUSABLE` without reestablishing its currently admitted closure and evidence tree.

## Retention roots, full replicas, and garbage collection

NET1 has three storage classes:

| Class | Activation and lifetime | Reliance role |
|---|---|---|
| Inert staging | A running local job; bounded bytes and deadline; uncommitted state is disposable after recovery | Never admitted support |
| Warm checked cache | Local promotion under a finite receiver-local retention-clock deadline, default 24 hours; survives clean service rollover unchanged but expires on boot/writer generation loss or earlier eviction allowed by its declared policy | Reusable only while complete and protected during each use |
| Pinned checked closure | Explicit receiver-local allocation, persistent across ordinary reboot, until locally authorized release | Supports current local reuse while all closure and policy checks hold |

A pin is never created by a remote signature, remote retention proposal, index entry, or incoming proof alone. Only the receiver's funded local promotion or separately funded local retention transition creates it. Its complete mathematical closure is part of the charged reachability graph.

Pinning does not promise immortality. A local owner can later release a root under its policy, after accounting for active uses and other roots. The node must update availability/reliance before advertising the released closure as currently reusable. No future-preservation claim is made beyond the actual retention policy and its explicit failure assumptions.

For peer replication, the baseline target for a node-selected high-value root is three full copies at distinct node keys, including the selecting node. A remote node contributes a copy only after its own selection, native check, and retention allocation. Its acknowledgment is a signed observation of a local pin, not a transfer of another node's pin authority. Three keys alone do not establish three independent failure domains.

`RetentionAck = [providerNodeID,serviceEpoch,rootReplayID,closureInventoryCID,retentionClass,localActivationID16,observationTick,observationExpiresTick]`.

The default observation window is at most 600 seconds and ends at service-epoch retirement. The underlying local pin can persist longer and across reboot, but a fresh remote observation is then needed. The receipt is not a guarantee that a future request will be served, that bytes survive catastrophic loss, or that the holder will never release the pin.

The selecting node periodically performs separately funded integrity/fetch checks under its local repair policy. It targets full replacement when an observed replica is lost, but never reports replication target achieved before a remote independent acknowledgment and appropriate availability observation. Repair consumes new authority; a failed remote promise cannot mint replacement bandwidth or storage.

Strict reuse in this baseline always has a complete local admitted closure, so ordinary source disappearance does not disable an unaffected local proof. Losing a local chunk, detecting local corruption, or releasing the final local retention path does require availability invalidation unless another complete local path remains.

Warm-root expiration is a local authority event. A current-reuse query checks the root's exact retention-clock generation and applicable monotonic deadline and fails closed if generation continuity is lost or expiry has occurred but its state/epoch update has not completed. A delayed cleanup timer cannot make expired storage authority appear current. Clean service rollover neither expires nor refreshes this deadline; remote timestamps never define local pin or warm-root lifetime.

Garbage collection uses these rules:

1. Persistently enumerate only receiver-authorized live roots and bounded active-use/export pins.
2. Mark their exact object and chunk closure under a metered local maintenance job.
3. Use a new mark epoch for concurrent root changes; a newly created root cannot refer to bytes eligible for deletion without atomically protecting them.
4. Keep in-flight fetch/use/export pins until their execution is terminal. A foreign request cannot create an unfunded pin.
5. After the 60-second grace interval in the same boot, the authority writer atomically checks that an exact physical storage generation has no live root, use, export pin, or newer committed reference and marks it `DELETE_PENDING`. A grace interval or old refcount alone is not concurrency exclusion.
6. New root/use transactions cannot bind a `DELETE_PENDING` generation. A funded deletion worker claims that exact generation, physically deletes it, and then commits `ABSENT`. A restart before that claim recomputes unclaimed sweep candidates; an already claimed pending generation remains unavailable while deletion/recovery finishes.
7. A crash after the pending mark but before deletion can leave unreachable physical debris; it does not expose admitted availability. A crash after physical deletion but before `ABSENT` also remains conservatively unavailable. Reimport may cancel an unclaimed pending deletion atomically before any worker claim, or create a different durably staged, hash-checked storage generation and bind new roots to that generation. It cannot race a claimed delete of the same generation.
8. Commit resulting availability/reliance changes before any positive current local reuse observation. Every physical generation and its temporary copy count against the applicable retained/staging allocation; a reimport is not a free way to duplicate physical bytes.

Root count, unique retained bytes, metadata bytes, in-flight pins, and maintenance queues all have independent finite limits. Shared chunks are charged once to resident byte capacity, while each root's accounting still records the dependency reachability needed to prevent premature collection. Removing one root cannot delete a dependency still protected by another root.

## Long-horizon autonomous maintenance

Autonomy means a locally authorized standing policy can schedule and fund repeated finite jobs without a human approving each one. It does not mean that a remote object can create unbounded future obligations. Each node declares finite per-period CPU, read/write, network, retained-byte, control-record, and concurrency ceilings for maintenance; renewal is a local policy event and preserves cumulative accounting. A new service epoch, foreign receipt, clock rollback, or failed replica never itself replenishes these budgets. The local scheduler must distinguish a recurring policy's authorization from the fresh finite grant and execution claim for each occurrence.

The baseline chooses the following bounded recurring routines. Their intervals are engineering defaults, not empirical durability guarantees:

| Routine | Baseline finite work | Consequence when incomplete or unfunded |
|---|---|---|
| Local byte-integrity scrub | Every 15 minutes, admit at most 64 MiB of sequential verified object/chunk reading, at most 1 CPU-second and 30 wall-seconds; persist a bounded resumable scan cursor | Keep the measured last-verified cut; mark detected damage unavailable immediately; do not claim a complete fresh scrub |
| Replica observation | Every 10 minutes, select at most 16 locally pinned high-value roots by a persistent fair cursor and at most two previously selected peer observations per root; each remote call needs its own finite paid service | Expire stale remote observations; report target unknown/degraded rather than increasing a replica count from old receipts |
| Repair | Queue at most one bounded repair intent per affected locally selected root within the maintenance-queue allocation; each replacement transfer, native admission, and new pin is independently admitted | Retain useful surviving local evidence, report the unmet target, and defer or drop an unfunded intent according to local policy |
| Contact refresh | At most once an hour, choose at most four known contacts for control-budgeted HELLO exchanges and independently paid one-hop GET_ROUTES work, still within the 256-contact/256 KiB directory bound | Retain or expire bounded hints; do not infer that an unreachable contact has permanently ceased to exist |
| Ledger/GC maintenance | Check rollover triggers and reclaim only through the fenced generation protocol under bounded local jobs | Pause new admissions when safety reserves would otherwise be exhausted |

At the nominal 64 MiB per 15 minutes, a static 32 GiB byte allocation takes 512 funded successful scrub occurrences, about 5.3 days, for one full pass. This arithmetic excludes duplicated work, newly arriving bytes, outages, CPU/I/O limits, and interrupted jobs; therefore the node records achieved coverage, not an assumed five-day freshness promise. Byte-hash scrubbing is distinct from rerunning native proof checking after a relevant local checker/profile incident.

Replica observations are also distinct from audits. A receipt proves only that a key made the signed assertion. A successful sampled fetch demonstrates possession/serving of the sampled exact bytes during that attempt, not the complete closure or future retention. If local policy requires a complete remote availability check, it must fund a complete closure transfer and verification, reuse its immutable already-verified byte checks only as policy permits, and name that finite observation's cut. Even that cannot prove future service or physical failure-domain independence. Any assurance claim must state which observation was actually performed.

Maintenance is prioritized within the existing receiver-owned admitted-corpus and incident/repair pools, not an additional hidden resource pool. Fair cursors prevent persistent selection of the same small subset under feasible admitted load, but cannot promise bounded refresh latency for unbounded pinned roots or sustained overload. When an already admitted repair detects a new deficit, it may commit a nonauthorizing intent; it cannot recursively mint another paid job.

There is no mandatory central upgrade signer, online software registry, or universal migration vote. Operators can retain an exact locally admitted profile, deliberately install a reviewed replacement, or operate different supported profiles simultaneously within their limits. Automatic executable-code installation from a peer or mathematical package is outside NET1. Old exact closures and native profile/distribution identifiers remain portable; replay still requires a compatible locally admitted verifier and available dependencies. A profile defect can make old local reliance inadmissible without deleting the historical bytes or rewriting their IDs.

### The finite-capacity preservation boundary

For node i at time t, let U_i(t) be its unique physically retained bytes, including protected transient copies under their separate allocations, and C_i(t) its authorized total physical storage capacity. Safety requires U_i(t) <= C_i(t), together with the independent root/metadata/count limits. A local pin is a commitment constrained by those bounds, not authority to violate them. For any collection promised permanent preservation, the union's irreducible exact information must be represented in the storage that actually survives; names, indexes, receipts, and model weights cannot replace missing replay bytes in this native profile.

Consequently, fixed finite surviving capacity cannot retain an indefinitely growing, incompressible, never-released corpus. Sustainable growth requires some combination of added funded storage/providers, reduced redundancy where policy allows, deduplication/compression with exact recovery, selective nonadmission, or deliberate release. NET1 chooses full-copy replicas and does not claim arbitrary proof data compresses enough to remove this constraint. Long-term preservation is conditional on continued surviving copies, compatible verification material, capacity, authorized maintenance, connectivity when repair is needed, and timely work; it is not an unconditional theorem about eternity.

## Portable export and source disappearance

`EXPORT_HEAD(root)` is a paid request for a pinned snapshot manifest, not a promise of infinite transfer. The server reserves one bounded export slot and enough pin/control capacity for the selected exact closure. The default export lease is 300 seconds in its current service epoch. An export can be declined if the closure is too large for its admitted envelope.

Remote EXPORT_HEAD accepts only a root currently in `PUBLIC_SERVE`. Its successful body is `[exportManifestCID,exportManifestPayload]`, and its export scope is bound to that requester. Creating an archive from local-only material is an owner-authorized local operation, not a public remote service.

`ExportManifest = [issuerNodeID,serviceEpoch,exportID16,rootReplayID,objectCount,pageCIDs,requiredNativeProfileIDs,createdTick,expiresTick]`.

`ExportPage = [exportID16,pageOrdinal,objectIDs]` uses type `0x800B`. Every export, even a small one, uses this single fixed-depth page form. Object IDs are globally sorted by their canonical encoded bytes, duplicate-free, and partitioned into consecutive pages of at most 4,096 entries. There are at most 16 pages and 65,536 objects. The root lists page IDs in order and binds the exact count; every nonfinal page is full. The selected root's complete native closure must occur in that list. The export's mathematical replay root, operational 16-byte export ID, and content ID of its export manifest are three different identities.

The export manifest and its pages are ordinary content-addressed operational objects retrievable by the same byte-transfer operations. Their storage and finite pin are charged separately from mathematical proof identity. The 1 MiB byte-manifest bound remains enforced for them.

Transfer uses ordinary GET_MANIFEST/GET_CHUNKS calls. Each is separately charged at both ends. The export snapshot pins its selected bytes only until expiry or explicit termination. The receiver must resume from already verified immutable object IDs after interruption; it cannot extend the provider's export lease by replaying old requests.

A portable offline archive contains: the export root and all manifest pages; every named exact payload or its complete byte manifests/chunks; and the explicitly required native profile/distribution identifiers. Archive import does not execute bundled software. The receiver installs or selects its own admitted verifier/profile separately, verifies closure completeness, and independently checks mathematical objects before promotion.

An exported archive that contains only URLs or a live database handle is nonconforming. Source disappearance is harmless to replay only when the receiver actually possesses the complete exact closure and compatible locally admitted checking material. A manifest containing unavailable references is not a complete archive.

## Status semantics

`GET_STATUS` returns a signed observation about one node's local state, never a global truth verdict. Its conceptual payload is

`Status = [nodeID,serviceEpoch,rootReplayID,typedRoot,proofIDOption,judgmentIDOption,policyRoot,nativeProfileID,localSnapshotID,relianceEpoch,validationCode,publicAssessmentDigestOption,admissibilityCode,availabilityCode,retentionCode,reuseAtSnapshotCode,observationScope,observedTick]`.

`typedRoot=[rootKind,artifactID]` uses the mathematical profile's exact discriminated union: `[0,ProofID]`, `[1,DefinitionID]`, `[2,GroupID]`, or `[3,OpaqueID]`. Proof/judgment options are both present exactly for tag 0, and absent for tags 1 through 3; a definition or declaration group is never coerced into a proof kind to fit a status field. The named ReplayID must bind this same typed root.

The assessment field, when exposed, is the digest of the explicit public assessment projection, not an arbitrary private ledger record or generic read capability. The policy root names the publicly disclosed checking policy relevant to this observation; it need not reveal confidential operational configuration.

The finite codes distinguish:

- validation: unchecked, accepted exact derivation, rejected evidence, bounded unknown, local error, unsupported;
- admissibility: allowed, disallowed footprint/profile, unknown;
- availability: complete local closure, incomplete/corrupt local closure, unavailable, unknown;
- retention: none, warm, pinned, export-pinned;
- reuse at snapshot: reusable at the named committed local snapshot, not reusable, stale/unknown.

All fields are read from one local authority snapshot. A positive reuse observation requires the exact active evidence-tree check at that epoch and a final unchanged-epoch reread immediately before committing the immutable status outcome. Its linearization point is that local computation commit, not a later network send or receipt. The separately funded reply can be delayed while the node's state changes; it still reports only the named old snapshot. It cannot be labeled current at delivery.

A node may detect an intervening epoch change before reply delivery and decline to transmit an obsolete result, but cannot mutate an already committed outcome. Obtaining a newer observation requires a new funded computation. A remote consumer treats even a fresh signed positive as an observation, not its own current reliance. Local use of native evidence still checks the receiver's current epoch at its own use/admission boundary. Historical native success is not erased merely because a later current-use field becomes unknown.

`observationScope` names only the local state and, if present, bounded explicit remote observations already admitted by the node. It cannot claim observation of the entire open network. Remote status records are candidates to the querying receiver; the receiver does not merge the sender's status into its own trusted state.

## Resource allocation and service scheduling

Every authority uses its own grants, tickets, reservations, claims, meters, and terminal settlements. A remote ticket issued by A can spend only at A. A receiving node B allocates its own resources to receiving and checking, even when A advertises that its budget or software is identical.

The default node has four fixed service classes: `CONTROL`, `INCIDENT_OR_REPAIR`, `ADMITTED_CORPUS`, and `EXPLORATION`. Remote keys, object kinds, topics, and newly chosen descriptors cannot mint more classes.

`CONTROL` has the separate ingress/egress/record caps already specified. The paid service pools reserve 20% of capacity for locally admitted incident/repair work, 60% for already admitted corpus serving/checking/preservation, and 20% for bounded exploration/new imports. Idle service capacity can be borrowed, but a borrower obtains no persistent entitlement and must respect the pool's execution bounds. Memory and retained storage are reserved componentwise; they are not inferred from CPU shares.

The scheduler services admitted jobs fairly within each receiver-owned class and bounds the number of nonpreemptive native checks. Since each such execution has a wall limit, the reserved incident share is a bounded-latency service opportunity under the declared admitted load, not an assumption of instantaneous preemption. An incoming message labeled "urgent" does not itself enter the protected class.

Actual default utilization is not claimed. A node admits jobs only when the full conservative envelope fits its residual resource allocation, queued-job limit, and record limits. If the admitted load cannot be sustained, it rejects or defers before promising service. A published object has no claim to admission just because it is formally valid.

Fairness applies to jobs that have actually been admitted under these conditions. It does not guarantee fair treatment of every possible identity or every object in an unbounded arrival stream.

## Failure traces that the design must preserve

### Invalid bytes through a correct index

A valid-looking descriptor leads to a provider. The provider returns a byte manifest but corrupts a chunk. The receiver rejects the chunk hash, records bounded provider failure telemetry, and may try another locally chosen provider within the same fetch envelope. It does not run the native checker on those corrupted bytes, admit the candidate, or mark the mathematical statement false.

### A complete transfer with a missing logical dependency

All transferred chunk IDs match. The native dependency extractor finds a required declaration absent from the supplied closure. The receiver either obtains it through remaining authorized capacity or ends `UNKNOWN_MISSING_CLOSURE`. The publisher's manifest or signature cannot authorize an assumed theorem in place of the missing derivation.

### Crash after checking but before promotion

Inert proof bytes exist and the checker produced success, but the authority transaction did not commit. After restart, the old running execution is conservatively finalized without promotion. Its orphan bytes remain inert and may be garbage-collected. A retry uses fresh local authority; the old uncommitted success does not create admitted support.

### Crash after promotion but before advertisement

The admission/retention transaction and outbox intent committed. After restart, retained roots and the assessment remain. The advertisement is still pending. A new separately funded outbox execution sends a bounded hint when admitted. Until then, no status says the external index already contains the object.

### Duplicate paid call and lost reply

Two equal CALL messages race. One reservation and one claim win; both refer to the same eventual terminal outcome. A lost body does not cause a second execution of that action. Returning its summary is control-budgeted. Re-fetching the immutable bytes uses a new paid call. Changed bytes under the same action key are rejected.

### Stale cursor during index replacement

A FIND page refers to snapshot S. S expires while a newer snapshot S' is built. The next old cursor returns `STALE_CURSOR`; it cannot resume at the same numeric offset in S'. The caller explicitly starts another query and tolerates duplicate candidate IDs. No gap-free or complete scan of S' is claimed from the mixed pages.

### Provider leaves after another node has imported

B has fully checked and pinned A's closure locally. A leaves. B's native replay remains possible. B updates its optional replica observations and may fund replacement. If B had only A's hint or manifest, it must report missing availability; the two cases must never share a current-reuse status.

### Remote incident attempts mass invalidation

A malicious peer sends many native-evidence hints advertised as showing a checker defect, or sends out-of-band alleged compromise notices. NET1's native hints remain bounded candidate records, and its public native read scope never expands into arbitrary incident-object access. Such inputs cannot directly disable B's checker, dirty its full corpus, or obtain protected repair priority. If B's local authority later admits a precisely scoped checker-disable event, all affected current answers fail closed under B's new epoch while unaffected evidence paths remain available.

### Root release races with active export

A local owner releases a theorem pin while an admitted export is sending its closure. The export's separately authorized finite in-flight pin keeps those bytes alive until export completion or timeout. Once every protection is gone, GC may reclaim them after its recheck/grace procedure. A foreign unsigned reference cannot create another pin.

### Many identities request empty service

Attackers create fresh keys and unused offers. Their requests share onboarding, offer-count, live-byte, issue, and control-record limits. Unused offers expire without restoring issue/redemption authority. Node resource safety survives under its ingress assumptions; an honest newcomer is not guaranteed admission until load and willing-path assumptions permit it.

### Entire authority restored from stale backup

The operator cannot prove that the backup's service epoch is current. The node does not sign new offers under the old identity/epoch history. It creates a new authority identity, treats stored mathematics as candidate bytes, independently checks its retained corpus, and establishes new local allocations. Old clients cannot spend old authority at the new node.

## Conditional safety and progress claims

### Exact-byte safety

Assume the canonical encoders/parsers and hash profile satisfy their declared properties. Accepted reassembled bytes for object ID c match the exact typed canonical payload bound by c, except with the selected cryptographic failure probability. Chunk identity alone is insufficient; the final full-object check is necessary.

### Local resource conservation

Assume the single-writer ledger, execution fencing, metering, and conservative recovery bounds implement the inherited transitions. Since every fresh paid service requires a live issuer-local ticket, unique reservation/claim, and terminal accounting, independent replay, cancellation, restart, or endpoint changes cannot amplify that issuer's granted work allocation. Count/byte/issue allowances additionally bound zero-work records. The claim excludes physical-link denial of service before the declared admission boundary.

### Independent mathematical admission

Assume the native checker, dependency/footprint extraction, policy, exact identity, local state, and isolation premises. An object arriving through any peer or optional index can enter current local reliance only through its exact checked evidence and locally available admitted closure. Index endorsements, key counts, service receipts, and foreign ledger state add no mathematical authority.

### Bounded attempt termination

For an admitted import attempt, assume its local authority eventually has a stable recovery interval, its executor fencing and deadline enforcement work, and finalization receives reserved local service. Then the attempt terminates with a success, rejection, error, or bounded nondecision; repeated crashes without a stable recovery interval can prevent externally observable completion. Timeouts preserve resource and evidence safety but need not produce successful imports.

### Conditional successful completion of one import

Fix one receiver-selected object and finite native closure. Assume: an honest willing route identifies the needed providers within the receiver's admitted finite lookup horizon; both serving and receiving authorities admit sufficient finite envelopes; all requests, response-delivery jobs, byte transfers, and local native checking for at least one attempt actually finish within their respective offer, execution, snapshot/export, and import deadlines; the object fits every applicable profile limit; and no relevant policy/incident change defeats admission before its local commit.

Then that attempt commits a checked retained result when its exact evidence and retention contract pass. Proof outline: the finite closure and timely independently funded serving/receiving steps establish exact staged bytes; bounded terminating native checking yields its accepted relation; timely atomic finalization commits the retained evidence and one settlement. For an export-based transfer, the actual export-dependent transfer must fit the 300-second default export lease, even though the receiver's overall import envelope can last 1,200 seconds. Otherwise it must obtain a fresh admitted export or use other still-public direct reads, with additional authorized work.

An alternative eventual-success premise is an eventually sufficiently long timely interval plus a receiver policy that funds and starts a suitable fresh attempt during that interval. It is not enough that every message is eventually delivered: an adversary can deliver every response just after its finite deadline, causing every finite attempt to fail. Retries are neither free nor automatically guaranteed.

No protocol theorem implies successful mathematical invention by an external agent, universal retention, global index completeness, unconditional resistance to eclipse, or exponential useful growth.

## Refinement obligations remaining before implementation

The choices above remove the architectural menus, but implementation still needs mechanically checked encoders and conformance vectors, exact mathematical-profile dependency parsing, the organization profile's cursor/scan-position representation, concrete transaction and file durability ordering, executor/meter integration, cryptographic library selection, host isolation, and measured capacity calibration. These are refinements of stated contracts, not permission to alter their authority boundaries.

CP-001D should include paper traces for the races above and an integrated schema inventory across the mathematical, organization, and network documents. CP-002 may later turn them into executable schemas, state-machine models, conformance tests, and software. Nothing in this document authorizes beginning that implementation now.

## References

- [Formal knowledge contract v0](FORMAL-KNOWLEDGE-CONTRACT-v0.md).
- [Operational mathematical profile](OPERATIONAL-CORPUS-V1-MATHEMATICS.md), native exact roots, replay closure, and local checking.
- [Operational organization profile](OPERATIONAL-CORPUS-V1-ORGANIZATION.md), descriptors, exact discovery, and deterministic bounded pagination.
- [Cooperation Core v0](COOPERATION-CORE-v0.md), inherited receiver-local accounting, admission, current-reliance, and repair rules.
- [CP-001B](../notes/checkpoints/CP-001B-distributed-corpus-and-global-status.md), exact external memory, retention, and scoped status.
- [Decentralization analysis](../notes/analyses/CP-001C-decentralization-analysis.md).
- RFC 8949, CBOR deterministic encoding concepts; NET1 deliberately uses a stricter array/unsigned-integer/byte-string subset.
- RFC 8446, TLS 1.3; RFC 8032, Ed25519 signatures. These standards specify mechanisms, not correctness of an eventual implementation or honesty of a peer.
