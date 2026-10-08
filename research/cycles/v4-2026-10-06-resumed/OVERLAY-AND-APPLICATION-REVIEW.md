# Independent overlay and formal-application review

2026-10-06 UTC. `/root/v4_central_reaudit`. Source/theory review only. Canonical
workspace guard passed; latest user continuation to 15:00 UTC governs. No product
module was imported or executed by this reviewer. Earlier frozen package remains
evidence, not accepted v4 completion.

## Initial disposition

Using a maintained library is appropriate, but its name does not supply the
required scaling/security theorem. Exact acquired **libp2p 3.3.11 / kad-dht
16.4.5** source reveals consequential limits requiring explicit adapter policy
and, potentially, one narrowly justified routing-table patch before claims of
very-large-network behavior. Formal application is a promising consequential
improvement if its exact target and complete final proof check remain mandatory.

## A. Source findings in the acquired DHT

Paths below are relative to
`experiments/maintained-overlay-01/project/node_modules/@libp2p/kad-dht/src`.

### A1. The acquired routing table does not immediately inherit standard bounds

`routing-table/k-bucket.ts` splits a full bucket whenever
`bucket.depth < prefixLength`, regardless of whether it contains the local ID.
The exposed `index.ts` documents a maximum of `2^prefixLength * kBucketSize`;
the default prefix depth is six. Full maximum-depth buckets retain responsive
old peers instead of specifically ensuring closest-to-local-ID coverage.

Consequently, setting a small fixed prefix depth bounds memory but does not
establish the usual fine-grained Kademlia coverage near each node in a huge
network. Merely increasing depth with network size permits a potentially
network-wide table and is not the desired logarithmic-state argument. A blanket
claim of `O(log N)` lookup from the library brand would be unsupported here.

One minimal, theory-backed candidate is a pinned fork of the split predicate:
split only the leaf containing the local KAD ID, up to the full 256-bit depth.
The existing `localPeer` and `_determineBucket` supply the comparison. This is
the ordinary local-path bucket scheme, not an unbounded all-prefix trie. It
requires explicit selection, implementation review, source/distribution pins,
and compatibility review of routing refresh; it is **not yet selected or tested**.
Do not silently monkeypatch an undocumented private field after startup.

For that candidate, each split adds one sibling leaf and increases local-leaf
depth by one. Hence there are at most 257 leaves and at most `257k` contacts
(up to the exact implementation's handling of self/temporary queues). Under
uniform independent IDs and a responsive honest population, the depth needed
for at most k peers near the local ID is `O(log(N/k))` in expectation. This
establishes the storage shape, not automatic maintained coverage under churn.

The deterministic routing lemma is separate: whenever the routing table of a
queried peer contains a live contact in the XOR-distance bucket toward a target
and a query actually considers it, forwarding increases the common-prefix length
with that target by at least one. Full necessary bucket coverage and a sufficient
query budget therefore bound progress by the identifier width. Obtaining typical
logarithmic network-size behavior and finding the responsible nearest live peers
requires healthy/random placement, adequate maintained coverage, reachability,
and a nonadversarial scheduling/churn model. These premises are not implied by a
four-peer experiment. Arbitrary Sybil placement, partitions and missing buckets
can still defeat discovery without affecting mathematical soundness.

Further compatibility inspection: `routing-table/refresh.ts::_prefixLengths`
counts leading zero **bytes**, despite the rest of the implementation treating
CPL as bits. Its synthetic refresh-target generator is additionally capped at
15 matching bits, using a 16-bit precomputed hash-prefix table. Correct local-
path splitting therefore does not by itself establish refreshed deep coverage.
Periodic self-query discovers nearby peers but is not a proof of refreshing
every deep annulus. A bounded deep refresh may target known/remembered peer IDs
in each actual deep bucket; generating arbitrary long desired hash prefixes by
brute force would be an unacceptable substitute. Empty never-seen buckets still
require explicit coverage assumptions. Its stop method also only clears the
existing timer: an in-flight refresh can subsequently schedule another. A
selected clean-stop patch needs a running/shutdown guard and cancellation.

### A2. Provider storage and serving need application-owned quotas

`providers.ts` stores a timestamp per `(CID, PeerId)` and its `loadProviders`
collects **all** stored providers under the queried CID. The GET_PROVIDERS
handler resolves every provider through `Promise.all` and encodes them all.
There is no per-key quota in those paths. Bounding the caller's yielded result
count therefore does not bound the remote server's work or memory.

The ADD_PROVIDER handler does require the advertised provider identity to equal
the authenticated stream origin. That prevents arbitrary third-party provider
impersonation; it does not prove custody, useful content, honest metadata or
Sybil resistance. It then stores the provider and merges advertised addresses.
There is no project-specific per-key, total-provider or peerstore quota there.

An adapter needs persistent count/byte quotas, including per-key providers,
peerstore entries/address bytes and total datastore entries. Enforce reservations
before writes and bound existing-state reconstruction. A count in a wrapper that
is bypassed by datastore batches is not a quota. Reaching capacity returns an
explicit failed/partial maintenance result, not a successful durable advert.
Concurrent operations must not race past caps. Any retention/eviction policy
must distinguish expendable routing hints from actual mathematical custody.

The DHT also includes generic record handlers. Configuring only a custom
protocol does not remove them or automatically reject unrelated record domains.
Disable or explicitly bound unwanted record storage and ensure the common
datastore budget covers every namespace the selected library can write.

### A3. TTL and renewal semantics are weaker than immediate leases

`Providers.loadProviders` does not check expiry on reads. The reprovider scans
stored records and deletes expired **non-self** records during periodic cleanup;
expired self records remain as durable reprovide intent. Thus a returned provider
may be stale until cleanup, even under honest behavior. Successful `findProviders`
is not a freshness guarantee. Application acquisition must tolerate refusal and
distinguish stale hints from missing mathematical results.

The exposed `providers` options mention cache/cleanup/validity, but the current
Providers implementation consumes only prefixes and datastore. Actual renewal/
expiry behavior is implemented in **`reprovide`** (`validity`, `threshold`,
`interval`, concurrency/queue), so do not configure the older-looking provider
options and assume those controls are active. Defaults use hours, not seconds;
the exact source rather than stale documentation governs units.

`reprovider.ts` obtains an AdaptiveTimeout signal for a queued job, but calls
`reprovide(options.cid, options)` without passing the obtained signal. The
existing options carry shutdown cancellation; the newly created per-job timeout
is not passed onward at this seam. The scan also calls `queueReprovide(...).catch`
without awaiting it, so many pending capacity waiters can exist even with a
bounded active queue. A bounded datastore makes their number finite but does
not turn the configured queue size into a bound on all outstanding work.

Do not claim effective per-renewal timeout/queue bounds until a selected fix or
outer bounded maintenance design closes this gap. Whole-process containment and
fixed lifetime are valid hard backstops; they are not a theorem of sustainable
renewal throughput. Preserve cleanup/renewal failures and retry only under an
explicit finite later allocation or maintained-service rate policy.

### A4. Address and stream policy remains our responsibility

Default `peerInfoMapper` removes private addresses, which must be deliberately
overridden for loopback-only qualification. That mapper alone is not a dial
authorization boundary. Apply a connection-gater policy to **every** learned
address and initial contact before dialing. In local qualification allow only
selected loopback TCP endpoints. A public deployment profile must explicitly
address private/link-local/loopback destinations, IPv6, DNS, relays and rebinding;
do not implicitly permit protocols because multiaddr can parse them.

Noise/peer IDs authenticate a transport endpoint, not a mathematical authority.
Custom protocol IDs separate cooperative swarms, not malicious participants.
Persist keys privately; do not log them. No public bootstrap, default discovery,
telemetry or public-network joining is authorized by dependency acquisition.

DHT RPC streams can process several messages with reset idle timeouts. A per-
message timeout is not an aggregate rate or byte budget. Set finite connection,
inbound/outbound-stream and routing-update queues; account for background query,
refresh, identification and provider traffic as well as application RPCs.
Configured application limits do not automatically constrain library internals.

## B. Conditional maintained-discovery contract

### Distinguish the three key semantics

1. **Exact object ID**: provider hint locates candidates for one immutable object.
   Acquisition verifies framing, manifest and payload hashes; actual proof
   acceptance remains a separate genuine check.
2. **Exact type/structural key**: providers advertise a bounded local candidate
   view, potentially containing many distinct objects. Returned candidates must
   be rederived from exact acquired content. A finite provider/result limit is
   not complete enumeration or semantic theorem search.
3. **All matching results**: if M distinct results must be returned, output alone
   costs `Omega(M)`. No `O(log N)` routing argument removes this term. Hot-key
   refinement/shards need explicit selection semantics; otherwise declare a
   bounded partial view, never global absence or complete recall.

Hash `namespace || key-kind || exact-key` with unambiguous domain framing before
forming a DHT content identifier. Namespace binds the actual mathematical policy
and query version. A peer ID, source-friendly name, remote profile or claimed
type key cannot choose a checking policy.

### Reachability statement that is supportable

Let N be reachable participating routing peers, k bucket/redundancy parameter,
alpha query concurrency, and B the finite query work budget. Condition on: one
configured initial contact leading into the relevant connected component;
sufficient responsive honest routing coverage during the lookup; a holder that
has successfully advertised under the exact namespace/key; surviving reachable
provider records; admission capacity; and enough B/time for the actual path.
Then a maintained routing algorithm can discover a holder without a full roster
or corpus scan. With standard random-ID coverage assumptions and the appropriate
routing table, typical path/maintenance costs can be logarithmic in N.

Outside those conditions, return `INCOMPLETE`, `NO_REACHABLE_PROVIDER_WITHIN_BUDGET`,
`OVERLOADED`, `STALE_HINT` or the concrete failure. Do not return proof rejection
or global nonexistence. An initial contact is a bootstrap prerequisite, not a
central server if contacts are replaceable and established routing continues
without a unique indispensable bootstrap. The actual test should remove the
initial bootstrap after joining, not merely assert this property.

### Resource and availability conditions

Let A count distinct `(key,provider)` advertisements, tau the effective renewal
period, and q the metadata replication fanout. Under approximately balanced
placement, expected provider-record storage is on the order of `qA/N` records
per routing peer, plus peer/routing state. Publication and renewal traffic cost
on the order of `A * q * routing_cost / tau` network-wide. Actual costs depend
on lookup and retry policy; this is a model, not measured implementation data.

Uniform key hashing balances many independent keys but cannot distribute the
load of one extremely hot key beyond the nodes responsible for that key. Local
queries, provider advertisements, renewal and data serving all compete for
capacity. Every relevant node needs offered work below its service budget, with
specified burst/queue assumptions; aggregate unused capacity elsewhere is not
sufficient. Finite quotas must admit/refuse/evict explicitly. No fixed capacity
can retain an unbounded stream of positive-sized objects forever.

If validity is T, effective renewal period tau and worst covered queue/network
delay d, continuous metadata availability needs a strict margin such as
`tau + d < T`, while enough replicas/paths survive that interval. TTL cleanup
lag is additional staleness, not extra availability assurance. A wall-clock
timestamp needs a local-clock assumption and cannot be a cryptographic lease.

Metadata replication is **not proof-blob replication**. Holding q provider
records that all point to one departed source leaves zero useful holders. Actual
custody retention/replacement needs independently funded byte quotas, receipt of
the complete exact inert object and an explicit local retention policy. With r
live independent custodians and at most f<r departures before repair, at least
one survives; without those conditions there is no availability guarantee.
Independent-loss formulas such as `p^r` must not be used for correlated outages
without justifying independence. Do not claim the DHT implements custody repair
unless the adapter actually does.

## C. Formal application preimplementation challenge

The mechanism agent proposes a source-free bounded proof application DAG with
an independently given exact closed Prop interface, explicit telescope/universes,
formal term arguments and premise witnesses; the existing complete guest and
genuine certified frontier remain final authority. Its draft is requested for
full review. Initial necessary conditions were sent directly to its owner:

- Bind the expected output capsule independently and compare it byte-for-byte
  with the generated packet projection. Checking *some* generated theorem is
  insufficient if the transformer also changed its target.
- Exact universe arity/substitution, correct de Bruijn context and closure of
  every premise witness are required. Include binder/substitution state in memo
  keys where relevant. Reject holes, implicit inference and unresolved names.
- Frozen receipt/capsule bytes or final materialized bounded proofs supply
  warrant. An advertised theorem ID or local status string does not.
- Eliminating native source elaboration changes the evidence path: unchanged
  final Nanoda guest assurance is possible, but the removed additional native
  Lean authoring check must not be claimed to have occurred.
- DAG encoding reuse does not prove evaluator sharing. Charge plan construction,
  formal adaptation, search/acquisition and maintenance when they are additional;
  caller-provided exact terms are not free proof search.
- A nonempty conditional break-even region for repeat applications of a known
  formal template is meaningful. No mandatory planner, natural-language intent
  criterion or universal improvement claim is needed.

This section is a preimplementation obligation list, not approval of an unread
future implementation. The application source and complete draft need separate
review before runtime.

**Authorship boundary update:** root subsequently assigned this reviewer to
author the selected Kademlia vendor fixes. Those exact changes are recorded in
`experiments/maintained-overlay-01/VENDOR-PATCHES.md` and its reproducible patch,
with all original files preserved. The preceding upstream diagnosis remains
source evidence, but this note is **not an independent approval of its author's
vendor changes**. Root owns independent delta review. This agent remains
independent of the separate formal-application and action-scope authors.

## D. Focused qualification targets, not campaign authorization

The next execution should discriminate new boundaries only: a new node joins via
one contact and learns a previously unknown holder; bootstrap disappearance;
actual provider renewal and expiry; a second real custodian serves after first
holder disappearance; finite failure/overload; exact acquired fragment feeds the
unchanged mathematical check. Preserve scope: same-host tests exercise protocol
and lifecycle behavior, not global distribution or independently operated uptime.

Changed-boundary negative checks should cover per-key/global storage cap,
learned forbidden address, bounded malformed/truncated/extra-data frame, wrong
namespace/key, stale provider, unavailable holder and cancellation/cleanup. A
source-free application needs expected-target mismatch, wrong universe instance,
bad premise/context and same-checker positive endpoint checks. Do not repeat
unrelated archive integrity or old proof campaigns for confidence theatre.

Source identities and exact selected adapter changes must be recorded before
these tests. This review currently authorizes neither runtime nor a release claim.

## E. Subsequent design decisions and API clarification

Root has accepted A1-A3 as blockers to naive adoption and selected narrow vendor
fixes for independent review: local-ID-only splitting at depth256; read-time
provider expiry filtering; propagation of the reprovider's actual timeout
signal; and quota-enforcing persistent application datastore. These are selected
changes, not completed source review or runtime passes. Root was also sent the
deep-refresh/byte-count issue, refresh shutdown race and the need to await
`queueReprovide(cid, options)` during scanning to bound pending queue waiters.

The mechanism agent supplied this concrete application API for pre-code review:

```text
assemble(plan_raw, expected_capsule_raw, semantic_contexts,
         registry, foundation_witness)
plan = {
  schema: DMKN_EXPLICIT_APPLICATION_PLAN_V1,
  expected_capsule_sha256: exact independently supplied target-file digest,
  graph: existing-schema name/level/expression DAG rows only,
  proof: expression index
}
```

It returns an unverified packet, target index, exact capsule and assembly record.
The plan cannot add declarations; the independent target fixes its entire
name/universe/type interface. Context and foundation data generate declarations.
There is no helper proof-expression substitution in the builder itself; the
existing composer later materializes actual fragment proofs. Scope traversal
memoizes by `(node,depth)` and final checking establishes dependent typing.

No abstract API blocker was found, provided all C obligations hold and complete
demanded declaration closure includes **proof-only** semantic definitions. Bound
input/context/expanded graphs and total work/bytes, not plan bytes alone. The
foundation witness must match adopted registry declarations exactly. Contexts
remain inert candidates until the backend verifies receipts or materializes and
checks the full bounded proof. Name this a source-free explicit proof assembly/
application API: the caller still supplies the formal proof term; it is not an
automatic theorem matcher or a source-free proof-discovery oracle.
