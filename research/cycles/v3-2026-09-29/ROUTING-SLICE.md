# Smallest consequential routed-publication slice

2026-09-29; `/root/contributor_plan`. **Source-only recommendation. No code,
runtime, new proof, product adoption or routing qualification is selected by
this note.** Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision and prerequisite

After root adopts the source02 shape gate and the genuine source01 certified
exchange prerequisites, select **bounded explicit publication to a typed
rendezvous index, followed by discovery of an initially unknown holder**.
Do not spend the next implementation on traversal alone. The additional
advertisement store is a consequential part of the minimum slice, not a full
DHT project. Preserve every used predecessor; root alone creates a fresh cut,
assigns disjoint source/test/review ownership and selects finite execution.

The existing `SCALE-ROUTING-CHALLENGE.md` correctly separates useful query
selectivity from reachability. Source02 now supplies one bounded shape feature,
but neither a local shape posting nor a referral makes an independently
published result appear at a discoverable remote index. Actual placement is
the missing connection:

```text
holder: existing local offer -> select derived keys -> bounded locate/announce
                                                        |
                                                inert rendezvous rows
                                                        |
receiver: key -> bounded locate/find -> unknown holder -> existing acquire
                                                        -> separate real verify
```

| Candidate | New behavior | What is still missing | Recommendation |
|---|---|---|---|
| Traversal only | Follow at least two referrals, then call existing `peer_find` at discovered nodes | No rule causes an independent publisher's result to be present there; a prearranged co-located holder supplies that fact | Useful component test, not the main next capability |
| Routed inert advertisements | Publisher and receiver independently locate the same typed rendezvous; publication actually inserts a bounded row naming the holder | General overlay maintenance, guaranteed replica intersection, adaptive splitting and adversarial availability | Implement this small cooperative slice |
| Full distributed index placement | Dynamic membership/replication, partition directories, repairs and admission policy | Substantial additional design and qualification | Defer until the small actual loop exposes the next obstacle |

The deadline is not a reason to present the first row as the second. If the
extra store/POST boundary cannot pass source review and finite tests in time,
keep the qualified known-contact release and label routing unfinished.

## Exact scope: typed, unsplit and explicitly partial

Use the source02 discovery namespace, already bound to its profile, image,
foundation and discovery version. Define

```text
target = SHA256("DMKN-ROUTE-UNSPLIT-V1\0" || compact({
  namespace, key, partition_policy: "unsplit-v1", partition: 0
}))
```

`key` is one source02 `validate_key` value: `bundle:`, `interface:`, `type:`,
`constant:` or `shape1:`. Keep the kind inside the hash; never substitute an
untyped hex digest. **Only partition 0 is implemented.** Reject any other
partition/policy rather than query an unpartitioned table and claim coverage
of a requested prefix. There is no concrete compatibility reason to exclude
shape keys: they are inert exact strings under the adopted namespace.

An announcement selects at most four keys that the honest holder rederives
from its one selected bundle with existing `discovery_keys`. Selection is
explicit, not automatic publication of all 129 possible keys. The actual
first integration needs only one exact interface key to isolate unknown-holder
reachability. It does not test unknown-theorem or semantic-query recall.
Focused inert controls exercise all five kinds and common-key saturation.

An unsplit popular feature may fill a node's per-key quota or the caller's
scan allowance. Return saturation/incomplete coverage. Do not silently split,
sample all prefixes, follow a split directory, or broadcast as a fallback.
This is a deliberately limited rendezvous profile, not the final huge-network
hot-key solution. The API reserves versioned partition fields for a later
actually indexed successor; it does not pretend that successor exists.

## Source footprint and public boundaries

Proposed fresh root-owned copy: `product-local/certified-routed-peer-source-03`,
based on the adopted nine-file source02 map. This directory is only proposed;
do not create it under this assignment. No mathematical image, capsule,
BundleV2, source02 feature extraction or certificate policy change is needed.

| File | Exact responsibility |
|---|---|
| New `cert_route.py` | Typed target/identity, endpoint policy, bounded local neighbor table, iterative locator, caller budget ledger, publish/discover/acquire orchestration and CLI |
| New `cert_route_store.py` | Separate SQLite inert-advertisement store; strict row validation, idempotent refresh, indexed bounded find and expiry cleanup |
| Fresh `cert_peer.py` | Optional routed dispatcher/service hooks for three routes below; existing certified find/bundle/acquisition behavior remains available; update its helper pin |
| Fresh `helpers/peer_service.py` | Small compatible transport extension for explicit absolute deadline and bounded POST body; preserve `_get` as the existing GET wrapper and all TLS/pin/framing rules |
| API/contract/docs | New routing schema, cooperative admission disclaimer, exact limits and result meanings; root owns final maps/pins |
| Unchanged payloads | `cert_index.py`, `cert_capsule.py`, `cert_bundle.py`, schema/registry and `helpers/peer_wire.py` |

Proposed Python boundaries, with a single mutable local `ctx` owned by the
originating caller rather than a peer-supplied allowance:

```text
target(namespace, key, partition=0) -> hex64
locate(ctx, key) -> authenticated_discovered_index_endpoints + trace
announce(ctx, local_store, bundle_id, selected_keys, own_holder_endpoint)
discover(ctx, key) -> routed_remotes + coverage + ledger
acquire(ctx, local_store, selected_routed_remote) -> ACQUIRED_UNVERIFIED
AdStore.put(key, offer, holder_endpoint, requested_lease_seconds) -> local row
AdStore.find(key, limit, max_scanned, max_bytes, timeout_ms) -> local snapshot
AdStore.expire(max_rows, max_sql_work, deadline) -> bounded maintenance result
```

Expose CLI `route-announce`, `route-discover` and one explicit
`route-discover-acquire` command for a shared-budget lookup/acquisition path.
The latter selects a returned candidate by a documented deterministic order
or caller selector, never promotes it to verified state. A later separate CLI
invocation is a separately declared operation, not an invisible retry of the
old allowance. The retained installed receiver remains the only verification
gate in integration; no route response can select its verifier/policy.

Wire routes:

- `GET /route-v1/neighbors/<query>`: namespace, exact key, policy and partition;
  at most eight inert endpoint descriptors, plus the responder's index-role
  flag. No forwarded RPC, advertisement scan or proof/blob read.
- `GET /route-v1/find/<query>`: the exact typed key and local row/byte/work
  bounds; only the separate indexed advertisement store is queried.
- `POST /route-v1/announce`: one bounded canonical JSON body with namespace,
  key, exact unverified offer, holder TLS descriptor and requested lease.
  No file, source code, proof or callback URL is accepted.

Use the existing pinned TLS 1.3 descriptors and strict HTTP framing. The POST
extension accepts only this exact route, one `Content-Length`, the designated
JSON media type, connection-close semantics and at most 8192 body bytes. No
chunking, compression, redirects, extra body, generic URL fetch or recursive
forwarding. Service request/body/send/time/CPU quotas apply before dispatch;
the body is read within the same connection deadline. Do not replace the
existing GET-only helper with an unrestricted HTTP client.

## Routing and endpoint admission

Let node identity be a tagged SHA-256 of the TLS certificate digest. The
descriptor includes literal IPv4 host, port, TLS profile and certificate pin;
its claimed identity must equal this derivation. Successful TLS must match
the pin before the endpoint is counted as authenticated. This authenticates
endpoint continuity, not mathematical truth, honesty or an independent
operator. Certificate rotation produces a new routing identity.

Referral following is **off by default**. An owner separately enables a
bounded address/port policy. Validate canonical literal IPv4 and the TLS
profile, then enforce at most 16 adopted CIDRs and eight port ranges; deny
special/private/loopback ranges unless explicitly enabled. No DNS, URL,
redirect, alternate address family or caller-supplied filesystem path.
Laboratory policy may allow one narrow loopback port interval, without
supplying a global table of node IDs, certificate pins or holder addresses.
Check policy before opening a socket, including advertisement holder endpoints.

Each serving router loads only its bounded local neighbor configuration:
256 XOR-distance buckets, at most eight entries per bucket, no replacement
queue in the first slice. A configuration is at most 1 MiB and 2048 records.
It contains generic endpoint neighbors, **not key-to-holder maps**. Namespace
support is local configuration, not remote policy adoption. Nearest-neighbor
selection may examine this fixed bounded table; record that work rather than
calling it zero-cost or proving logarithmic routing from the bound.

The caller starts with at most two independently owner-selected entries,
retains at most 64 candidate identities and performs serial RPCs initially.
No concurrency is needed to qualify the first boundary. Deduplicate both
identity and endpoint; one identity cannot fill the queue by advertising many
ports. A valid referral extends a branch only if strictly closer to the
target than its responding parent. Already queued alternate branches remain
eligible. Query closest eligible unvisited candidates until convergence in
the observed candidate set or budget exhaustion. Referrals are not persisted
as trusted contacts merely because they were returned.

Use up to three closest **successfully authenticated discovered index-role
endpoints** as the rendezvous replicas. Publisher and receiver run the same
algorithm. There is no claim that these are globally nearest, independent,
or identical under different observations. The first finite topology uses
owner-provisioned local tables; automatic bucket repair/churn convergence is
not part of this cut. It is a deployment limitation, not a global roster.

## One origin-controlled resource allowance

Prospective defaults below are test/profile choices, not measured performance.
Before runtime root can select smaller compatible bounds in the contract.

| Resource, shared across the entire operation | Bound |
|---|---:|
| All attempted RPCs, including failed TLS, announce/find/acquire and alternatives | 32 |
| Neighbor RPCs / advertisement find RPCs | 24 / 4 |
| Keys in one publication / queried keys in one discovery | 4 / 1 |
| Retained routing candidates / returned distinct bundles | 64 / 4 |
| Replicas for one key / acquisition attempts | 3 / 2 |
| Reserved remote postings over all find requests | 128 |
| Metadata HTTP plaintext, requests and responses including header reservations | 1 MiB |
| Selected bundle-frame bytes over all acquisition attempts | 128 MiB |
| Metadata phase / whole discovery-acquisition wall allowance | 8 s / 60 s |

Each dispatch reserves its maximum response/body/header bytes, one RPC and,
for a find, its requested scanned-row allowance **before connection**. Do not
refund work based on an untrusted peer's smaller `scanned` claim or failure.
Keep actual observed bytes separately where instrumentable. Headers reserve
the frozen 8192-byte receive bound, plus exact sent-header/body bounds. Bundle
transfer reserves the exact advertised frame size before fetch, in addition
to the existing local quarantine/custody storage reservations. A maximum-size
pair of bundles need not fit 128 MiB; refusal is the correct outcome.

Crucial existing-source mismatch: `peer_service._get` currently creates a new
30-second deadline internally, while `peer_find`/`peer_acquire` have no common
operation ledger. An outer check before calling them **does not implement**
the shared deadline. The fresh helper must accept an absolute monotonic
deadline and use `min(parent_deadline, now + existing_transfer_limit)` for
connect, handshake, head, stream and TLS shutdown. The injected `fetch`
closure supported by current peer APIs supplies this deadline and reservations.
Keep parser/work bounds and an outer finite process supervisor; a Python
deadline is not a hard real-time scheduling guarantee. Report HTTP plaintext
accounting, not measured TLS-record, OS socket or packet bytes.

Budget exhaustion terminates; no wrapper starts another pass, contacts all
peers, resets the deadline, or reuses an allowance after failed TLS. A remote
server may lie or waste its own CPU; the protocol bounds honest server work
and the originating client's requests/resources, not every Byzantine CPU.

## Inert advertisement store: minimal actual placement

An ad contains the exact source02 `validate_offer` descriptor, a validated
holder endpoint, exact key and namespace. The primary identity is
`(target, bundle_id, endpoint_id(holder))`. Same exact row refresh is idempotent;
it changes a lease/revision, not the theorem count. Reject conflicting offer
bytes for an existing bundle identity rather than silently overwriting them.
The honest `announce` command loads only its selected local bundle once,
rederives selected keys and binds its advertised endpoint to its configured
listener certificate; then it posts separately to the bounded located replicas.
Return actual per-key/per-replica acknowledgments and partial placement.

First-profile default caps: 65536 live-or-not-yet-reclaimed rows, 64 MiB
database, 4096 rows for one exact target and four holder alternatives for one
target/bundle. Enforce row/byte counters and SQLite page/work limits
transactionally; do not count the full table on insertion/startup. Excess
publication is refused, never converted into an unbounded overflow file.
There are no theorem/receipt blobs in this store and no custody claim.

Use a bounded lease (requested 60..3600 seconds, capped by the accepting
server), under that server's local time. No global freshness clock is inferred.
An indexed due-time cleanup deletes at most 64 expired rows per explicit
maintenance call. Query does not need to clean/rebuild the database. A clock
anomaly can invalidate leases conservatively; do not promise trusted remote
freshness from wall-clock timestamps. Refresh is an explicit separately
funded announce, not a hidden timer campaign. Automatic refresh, re-replication
and bucket repair remain outside this first slice.

Implement an index beginning `(target, expires, sequence)` and query live
rows in that same order, bounded by `max_scanned`; no unindexed `GROUP BY`,
global holder search or full sort. A read transaction binds the returned local
revision and observation time. The first ad API has **no continuation cursor**:
it returns one bounded local snapshot and an honest complete/incomplete flag
for that snapshot only. Do not borrow source02's immutable cursor semantics
for these mutable leases. Refresh can change ordering at the next observation.

Announcement admission deliberately differs from mathematical acceptance.
The first explicit cooperative profile permits unauthenticated **inert
metadata writes** under global/request/row quotas. Server-authenticated TLS
does not authenticate the publishing client or establish control of the
advertised holder. Do not claim per-holder quotas are Sybil-resistant, or a
stored announcement proves custody. Poisoned keys/holder addresses may waste
bounded work or suppress recall. Owner endpoint policy blocks disallowed
connections; acquired bytes must still pass exact offer/derived-key binding,
then the real installed verifier. Thus metadata poisoning cannot by itself
authorize a false theorem, but malicious flooding can defeat availability.

Signed announcements, client authentication, callback custody checks and a
permissionless spam policy are alternatives for a later admission successor.
Do not add them merely to make this cooperative experiment look stronger.
If open untrusted writers are required for the release's deployment claim,
the cooperative profile is insufficient and that claim must wait.

## Exact result and conditional claim

A discovery result includes the requested namespace/key/partition0, contacted
replicas, their local revision/time/coverage, rejected or unresolved referrals,
reserved/observed work, exact holder-bound offers and one termination reason.
Examples: `CANDIDATES_FOUND`, `ROUTING_INCOMPLETE`, `BUDGET_EXHAUSTED`,
`LOCAL_SNAPSHOT_EXHAUSTED`, `UNSUPPORTED`, `HOLDER_UNAVAILABLE`. None means
`COMPLETE_GLOBAL` or that no such mathematics exists. A missing/expired ad is
not theorem revocation. A successful POST is placement of metadata, not
cryptographic verification or guaranteed future service.

For the strongest justified liveness statement, let `R_p` be replicas that
actually accepted an announcement and `R_q` those actually queried. Discovery
can find it only under explicit premises: a reachable honest node in
`R_p ∩ R_q`; unexpired retained ad; matching supported key/profile; its row
reached within finite scan/byte limits; enough route/request time; and an
available exact-byte holder. Certificate acceptance adds its independent
existing cryptographic/checker premises. Stable connected well-maintained
overlay tables may support this intersection; the small slice neither proves
it for arbitrary membership nor establishes logarithmic hops empirically.

No obligatory operation reads all corpus entries, all peers, or ancestral
proof steps. It reads bounded route metadata, selected indexed rows and the
selected four-file bundle. This access boundary is useful even though global
recall, bandwidth balance, churn and adversarial availability remain open.

## Finite nonduplicate qualification

Do not repeat source02 feature extraction tests, old native proofs or completed
known-contact TLS campaigns. New tests must isolate the newly changed boundary:

1. **Actual publish then unknown-holder discovery.** Retain the already
   qualified genuine bundle A and its receiver policy. In one small loopback
   topology, holder H uses public `route-announce`; no test controller inserts
   an ad/key-to-holder row. Fresh consumer knows only two entries and the exact
   selected interface key. Neither its configuration nor either entry contains
   H or the destination index directly. At least two actual referrals reach
   an index, its new ad reveals H, and the consumer acquires exact A and calls
   the existing installed cold verifier. Index nodes need not hold A. Preserve
   the before-empty/after-announced rows and actual RPC trace. The evaluator's
   process inventory is not supplied to any product node/client.
2. **Budget/transport changes.** Cycles, duplicate identities, wrong pins,
   forbidden addresses, a hung peer, oversized response/body and late failure
   cannot reset totals or leave accepted/custody state. Deadline traces must
   show the same parent deadline reaches socket I/O; use the selected outer
   supervisor for final process closure. Refused addresses cause zero connects.
3. **Typed/locality boundary.** All five key kinds can be announced/found;
   wrong namespace or nonzero partition refuses. Add unrelated inert ad rows,
   protect unrelated blobs, inspect SQL plans/actual VM counters and prove no
   blob access in neighbors/find/startup. This is not another proof campaign.
4. **Publication/storage boundary.** Exact refresh does not multiply rows;
   conflicting descriptor refuses; per-key/global quotas, expiration and
   bounded cleanup hold. An intentionally wrong advertised key may be returned
   as untrusted metadata but acquisition rejects its derived-key mismatch.
   A returned `receipt_verified: true` or alternate policy is rejected.
5. **Failure and saturation.** One unavailable replica with an already routed
   alternative can still return the ad within the original allowance. If no
   replica intersection exists, terminate incomplete. An overfull common-key
   stream reports its finite local coverage; it does not fan out or reset.

Root should fix one finite source-only contract before implementation: fresh
owned paths, at most eight local processes/identities, one genuine selected
bundle and one real positive acquisition/verification, all other faults inert,
bounded native-free groups and explicit retained inputs. Generate laboratory
identities once; no certificate grinding to simulate favorable DHT security.
If a topology is arranged by XOR order to exercise two closer hops, disclose
that construction: it tests mechanics, not natural-network convergence.

Passing establishes actual bounded metadata placement and unknown-holder
exchange under this cooperative topology, not independently hosted operation,
arbitrary public DHT robustness, broad retrieval quality, or useful-growth
speedup. Reuse the same genuine bundle; producing another expensive proof as
a network fixture would be duplicative. The separate useful-growth comparison
and producer-cost bottleneck remain central and are not displaced by routing.

## Decision for root

Select the routed-advertisement slice only after shape and actual certified
prerequisites are adopted. Its minimum extra cost over traversal is one small
metadata store, one strict POST route and publication orchestration; that cost
buys **real publication placement**, which traversal alone cannot demonstrate.
Keep unpartitioned typed keys, cooperative writer admission, serial lookup,
explicit leases and fixed local tables. These are honest first-cut limits,
not reasons to build a full membership/replication system now. Independent
source review should prioritize shared deadlines, POST framing, transactional
quotas, indexed expiry/find and acquisition binding before cosmetic APIs.

### Source references read

- `research/cycles/v3-2026-09-27/SCALE-ROUTING-CHALLENGE.md` and
  `SCALE-NETWORK-NEXT-DECISION.md`.
- Source02 `cert_index.py`: namespace/key validation, feature derivation,
  offer binding and local find/cursor semantics.
- Source01 `cert_peer.py`: `peer_find`, `peer_acquire`, injectable `fetch`,
  quarantine-to-custody commit, service dispatch and known-contact configuration.
- Its `helpers/peer_service.py`: strict endpoint/TLS policy, `_get`'s current
  independent deadline, GET framing, bounded socket stream and TLS shutdown.
- Current `GOAL.md`, `AGENTS.md`, `research/NOW.md` and `DELIVERY-PLAN.md`.
