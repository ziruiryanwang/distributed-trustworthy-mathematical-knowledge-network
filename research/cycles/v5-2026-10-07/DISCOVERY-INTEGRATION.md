# V5 discovery integration: exported declarations and bounded sessions

Scale owner, canonical root only. Root selected source implementation after the
primitive01 (4/4), contract01 (9/9), budget01 (1/1) clean local passes. These
results apply to retained source snapshots, not the new changes below. No
unchanged campaign or network runtime is selected.

## Per-export object and acquisition contract

One indexed object is one selected declaration from one authenticated group
opening, not a union of unrelated exports. Canonical wrapper fields are schema,
module_id, relative_name, opening. The opening binds its summary, group index,
all declarations of the atomic group and Merkle siblings; codec's exact
verify_group_opening checks that structural binding. The adapter selects exactly
one relative_name and computes codec.export_id(ModuleID,relative_name).

New DMKN_FORMAL_FEATURE_RECORD_V2 keeps V1's common fields and adds a typed
locator: schema DMKN_MODULE_EXPORT_LOCATOR_V1, module_id, group_index,
relative_name, descriptor_id. The descriptor uses codec.hash_value domain
declaration-descriptor over the exact selected descriptor. object_sha256/bytes
bind the canonical wrapper, not a full module/proof blob. RecordID has a separate
V2 hash domain; V1 field/digest semantics remain unchanged.

The discovery namespace binds module schema, foundation, semantic policy and
DMKN_MODULE_EXPORT_FEATURES_V1, not the whole ModuleID. Features are selected
declaration kind, exact relocated declared type, declared-type symbols, syntactic
result/binder heads, constructor/slot/constructor edges and external modules
actually referenced by the selected type. No value bodies, other declarations'
features, semantic normalization or proof ancestry are fetched.

Resolve rechecks wrapper bytes/hash, exact export identity, descriptor/group
binding and deterministic feature record before returning the typed locator.
ExportID must never be passed as an old custody ModuleID. Actual acquisition
uses locator.module_id plus group_index/relative_name; mathematical acceptance
still requires the applicable resolved module certificate/checker. Structural
membership and discovery are never mathematical authority.

## Public SearchSession contract

A local agent chooses what to search and which provider/snapshot to contact.
SearchSession provides accounting and verification, not a research planner or
automatic all-partitions/provider loop. Fixed namespace and conjunction; explicit
max providers, snapshots, requests, pages, examined rows, candidate matches,
raw reply bytes, wall duration and in-flight requests.
Canonical outgoing request bytes are separately counted and each request is
bounded by16KiB, so their aggregate is at most16384*max_requests. Transport
framing/connection overhead is outside these payload counters and must be
included separately by the selected network adapter and full-cost accounting.

Before returning a request ticket, reserve its maximum reply bytes and, for
pages, examined/match allowances. A failed reservation emits an explicit budget
error and no ticket. All attempted provider/snapshot/request counts remain
charged, even if that provider fails. Every received raw byte is charged before
JSON decoding or proof checking, including invalid/error replies. Transport
must enforce the ticket's byte ceiling while receiving; an oversized reply
poisons the session rather than silently restoring an exceeded allowance.
Abandoned tickets conservatively consume reserved reply/scan/match ceilings
unless a bounded actual response was supplied. No caller-supplied server charge
is trusted as actual network/CPU cost.

Only successfully verified summaries enter the session's private state. Pages
use those summaries and private Coverage; invalid pages do not advance verified
intervals/cursors. Repeated/overlapping pages still consume request/byte/scan
allowances. Coverage tracks committed metadata only; neither global absence nor
source corpus completeness is inferred. Deadline expiry denies new requests and
late adoption; received bytes remain charged. Outer hard wall/CPU/memory/network
containment remains required around cooperative local checks.

## Source ownership and changed-boundary controls

- New module_export_adapter.py and test_module_export_adapter.py.
- Narrow V2 record validation/hash support in formal_features.py; recognized
  export feature schema in authenticated_index.py; adapter schema binding in
  discovery_store.py. Existing Merkle and page algorithms unchanged.
- New search_session.py and test_search_session.py with finite synthetic
  metadata only; no real network, prover or old mathematical campaign.
- Root owns launch selection/source snapshots; assurance owns independent
  changed-boundary review. All implementation stays in the single software/v5
  development tree; predecessor evidence remains immutable.

Required controls include two unrelated exports not satisfying a false union
conjunction, exact ExportID/locator resolution, wrong module/name/group/type
rejection, V1 digest/snapshot compatibility, independent per-export records in
the actual SQLite store, invalid bytes charged, failed proof leaves cursor,
budget reservation exhaustion, deadline refusal and cross-provider continuation.

## Authored source checkpoint, awaiting independent review and root selection

module_export_adapter.py and search_session.py are implemented. V2 record and
feature-schema branches preserve V1 exact fields/hash domains/config bytes.
Coverage.accept gains only an optional before_commit callback so the session
can recheck its deadline after verification but before recording progress.
The session retains private last_verified cursors; invalid replies cannot
overwrite them. No caller-returned summary/report mutation changes private state.

test_module_export_adapter.py has six changed-boundary controls including actual
SQLite indexing of three distinct synthetic export records and V1 hash-domain
regression. test_search_session.py has seven finite synthetic controls including
deadline expiry after verification and raw transport-cap violation. These source
tests are authored, not yet run; no result is inferred. Root owns source
snapshotting, finite execution and outcome adoption. Reviewer has been asked to
review the complete changed source boundary. No network service is implemented
or launched by this slice.

## Next concrete integration recommendation (source-read only)

Implement one small **read-only HTTP provider adapter** over the existing v5
Store and ModuleSpec codec, plus a matching bounded client that drives
SearchSession. Do not modify frozen v4, disguise the new protocol as its find
operation, or create another complete product copy. This is the smallest useful
replaceable-provider boundary: two independent provider directories/processes
can serve one pinned SnapshotID, and a separate custodian can supply the exact
opened declaration/body material. No central server is required; each provider
is optional and replaceable. No launch is selected by this recommendation.

### What the frozen v4 actually supplies

Source inspection of `product-local/v4-library-commons-02/commons-v4` finds no
HTTP service to reuse. `overlay/library_overlay.mjs` is libp2p TCP/Noise/Yamux
with DHT hints and bounded bridge spawning; `overlay/wire.mjs` is length-prefixed
half-close framing, not HTTP. Its JSON_MAX is65536, metadata parser depth24 and
bridge output ceiling131073. These cannot carry arbitrary new1MiB summaries or
deep ModuleSpec group objects unchanged. Its old `acquire` accepts fragment_id
plus old frame/offer bindings and routes into library_bridge's named-definition
policy. A v5 ExportID or ModuleSpecID cannot safely be substituted there.

Reuse the established invariants, not incompatible identities: selected exact
addresses; finite connection/request concurrency; overall abort deadlines;
bounded read chunks; pre-reserved transfer storage; exact bytes/hash binding;
exclusive local file creation and atomic persistent admission; separate transport
versus mathematical assurance. Keep v4's current libp2p service unchanged.
Retain its optional DHT provider-hint integration as a later endpoint discovery
adapter, not a prerequisite for the first HTTP-to-existing-v5-store path.

### Concrete transport/source seam

One new v5 Python transport module using stdlib asyncio streams can enforce a
narrow HTTP/1.1 subset without hidden high-level buffering: fixed read-only POST
routes, canonical JSON request<=16KiB, header block<=8KiB, no transfer encoding,
no content encoding/compression, one exact Content-Length, one request/connection,
no redirect following, no arbitrary URL fetch and `Connection: close`.
Read bounded chunks under one absolute connection deadline; incremental byte
counting happens before JSON parse or retaining more data. Client uses configured
literal IP/port endpoints under an explicit address policy, avoiding arbitrary
DNS/redirect routing. Internet operation needs the selected TLS/authentication
policy and deployment isolation; content commitments alone do not provide
confidentiality or make an unaudited HTTP server production-qualified.

Bound active connections before reading, refuse excess immediately, and choose
small listen backlog/read buffers. One provider process serializes Store access;
no unbounded thread-per-request server. Store computation is bounded but is not
hard-isolated by asyncio: external process/job supervision must kill overrun.
The client serializes SearchSession method calls; in-flight tickets permit
pending I/O, not unsynchronized concurrent mutation of its dictionaries.

Routes return the existing canonical payload directly, not an unauthenticated
status wrapper mistaken for a verified summary/page:

| Route | Exact requested scope | Validation/adoption |
|---|---|---|
| `/v5/discovery/summary` | pinned SnapshotID,1..8FeatureIDs,max reply bytes | SearchSession reserves first; verify_summary authenticates every returned descriptor |
| `/v5/discovery/page` | existing request schema against that same snapshot | SearchSession supplies privately verified summary, then checks every examined row/interval |
| `/v5/modules/group` | ModuleSpecID,structured relative name, optional known group index | codec verifies opening against ModuleSpecID; requested name must occur exactly once |
| `/v5/modules/body` | owner ModuleSpecID,relative name,universe arity,exact demanded body hash | verify descriptor/permission first, then codec.body_id; store under owner-qualified context |

Module certificate acquisition is a separate typed route only after the real
v5 certificate wire format/relation is selected. Do not serve an ImportClaim
JSON or old v4 receipt as if it discharged the new module relation. The current
model reports NOT_PERFORMED; HTTP transport must not change that fact.

Response body cap is the request ticket's selected cap, not only a trusted
Content-Length. Read errors/truncation abandon the ticket conservatively unless
the complete bounded actual body is available for accept. HTTP error bodies are
still charged and cannot advance a cursor. Headers are independently counted;
with8KiB caps in each direction their total is<=16KiB*request_count, additional
to recorded canonical request bytes and session reply bytes. Transport connection
costs/failures belong in full workflow accounting. No retry has a free ticket.

### Exact acquisition chain and two missing seams

1. Authenticated discovery returns a V2 record. Its locator is a **routing
   candidate**, not proof of descriptor truth or mathematics.
2. Ask any configured module custodian for that module/group/name. Receive an
   opening; locally construct the canonical per-export wrapper using the exact
   advertised ModuleSpecID and relative name. ModuleExportAdapter.resolve must
   reproduce wrapper SHA/bytes, ExportID, descriptor_id, locator and feature
   record. A mismatching opening, name or declaration refuses.
3. Obtain and actually verify the new module certificate against its exact
   foundation/policy/summary. Only that acceptance boundary permits imported
   mathematical authority. The group opening itself cannot discharge it.
4. Supply the opened group to the conditional environment. A later NeedBody
   requests only its exact committed body; absence remains an unresolved demand.
   A NeedDeclaration with only (ModuleID,name) needs a custodian name-to-group
   locator table. An untrusted provider may propose any group index, but the
   consumer checks opening membership and exact name. A negative reply is only
   provider-local not-found, never global nonexistence.
5. New local declarations still undergo their own checker/certificate path;
   publication contributes new module and feature records only after that path.

`modules/model.py` already provides Address, NeedDeclaration/NeedBody,
add_import_opening and supply_body. It does not provide durable custody or real
certificate verification. Add a distinct module custody database/CAS whose
typed keys are (ModuleID,groupIndex), (ModuleID,relativeName)->groupIndex and
(owner,universes,bodyHash); body hash includes universe arity, while owner keeps
relative references contextualized. An owner-local import must validate exact
group/body bytes and atomically charge rows/blobs before serving them. No remote
write endpoint, arbitrary file path, source execution or proof generation is
needed in this provider adapter.

The two missing seams are therefore concrete: **bounded transport around the
already implemented index/session**, and **typed durable ModuleSpec group/body
custody**. Actual certificate discharge remains mechanism's separate central
gate; neither seam should wait by inventing a fake certificate acceptance token.

### Persistence and minimal decisive actual test

Providers reopen the existing v5 index Store with exact namespace/schema/limits;
retained SnapshotIDs survive process restart. For the first finite replica test,
use a bounded SQLite backup into a separate provider directory, preserving all
chosen store roots/records. Charge copied bytes; do not claim this is an
Internet-scale snapshot replication protocol or a global corpus copy. Later
snapshot-specific CAS transfer can avoid unrelated retained snapshots.

The first client session is process-local. Its report JSON is not a trusted
resume token. A crash ends that workflow; a new workflow receives an explicit
new allowance. Qualifying crash-resumable aggregate budgets later requires
write-ahead ticket reservations and verified-evidence recovery, not resetting
counters after each restart. Provider persistent state and client session
resumability must not be conflated.

Select one actual test when source review is complete: two metadata providers
with identical pinned snapshot, a distinct module custodian, and one client.
Fetch a summary and first page from provider A, stop A, continue from B with the
same snapshot/cursor, select a formerly unknown export, fetch its group from the
custodian and resolve the exact locator. Restart the custodian and retrieve a
demanded committed body. Distinct tests target an oversized/truncated response
and bad group/body binding. This demonstrates new transport/retention boundaries,
not yet mathematical acceptance, global hosting, growth or another rerun of
unchanged pure tests. The later same workflow must connect actual certificate
verification and substantive reuse before it can satisfy the full core loop.

## Transport/custody implementation checkpoint

Root adopted the source map. New evolving files are
`software/v5/custody/module_store.py`, `software/v5/transport/http_provider.py`
and `software/v5/transport/clients.py`. No mechanism files or frozen sources
changed. Module custody atomically retains group openings, owner/name lookup,
and only descriptor-committed definition/opaque/recursor-rule bodies. Get paths
recheck canonical commitments. Hash-valid material remains structural custody,
not a certificate or mathematical acceptance.

Provider supports the four fixed read-only routes, exact request fields,
8KiB headers,16KiB requests, bounded response lengths/chunks, one absolute
operation deadline, closed connections, configured IP endpoints, application
concurrency and finite lifetime request/reply budgets. Internet plaintext is
refused; verified TLS client and server contexts are available. **TLS handshake
work begins before asyncio's application connection callback and is not bounded
by its application concurrency counter.** Public deployment therefore still
requires an independently selected handshake/connection-limiting front end or
equivalent OS/process boundary. Loopback controls do not qualify public TLS
DoS resistance. Unmodified Store calls are synchronous; outer hard CPU/wall
containment remains necessary despite cooperative deadlines.

Independent source review found a consequential deadline gap at receiver custody
commit. It is repaired with optional before_commit callbacks inside group/body
transactions, including duplicate branches, and client deadline guards passed
through them. Expiry rolls back any new counters/rows instead of returning a
late committed acquisition. New focused tests include this boundary.

`test_provider_contract.py` contains five focused loopback/SQLite controls:
provider loss and portable page retrieval/custody restart; atomic deadline/quota
and bad-body refusal; read-only route/request overflow; oversized/truncated
response and corrupted stored body refusal; remote plaintext endpoint refusal.
These source tests are quiescent pending review/root-selected execution. Earlier
export6/6 and session7/7 results apply only to their retained source snapshots;
none is claimed to qualify the new networking boundary automatically.

### Actual FoldFusion harness, awaiting selection

`transport/public_integration.py` accepts1..8 repeated --bundle and
--bundle-sha256 pairs plus --selection/--selection-sha256 and fresh --evidence.
It uses root's existing DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1 outputs directly;
it does not regenerate source, proofs, roots or fixtures. The current retained
inputs are `experiments/v5-local-checks/fold-prepare-01/prepared/` bundles:

| Bundle | Raw SHA256 |
|---|---|
| base | 030d35200bf5b81a219a18b322d8568e4c76b94664a7ac111cba3d527fb9daa0 |
| fusion | 756a75e3e8e49bf1135d4bedd0b94318023c03f27a382b212869ee0b8e823ce0 |
| fold_map | c6f82d3cb7c6ced8adf3af99d48cf4e59f50bdf42395c55b2a64c81d843b8454 |
| fusion_map | 2e7092030f04b2b1ef194bf4285f4bb495e8136496c2f87195576233a65892fa |
| project_summary | 4969d2f65b5b99aabd684baa87ebf616532c43992161a82acbe06f47a6649962 |

The human-readable FoldFusionSearchSelection chooses theorem kind/equality
result head and relative names CommonsV5.fusion/CommonsV5.fold, not content IDs.
Its convenience result-head-foundation-name compiles deterministically using
the public foundation-name hash domain. The actual candidate foundation/policy
are explicitly not an adopted mathematical foundation or verified certificate.

Provider setup knows its own supplied modules; the consumer API receives only
query features, pinned snapshot and selected relative names. All roles currently
share one local harness process/event loop; this is logical API separation,
**not an enforced blind-agent or independent-host test**. Two separate persistent
indexes hold the same selected snapshot. A supplies summary/first page; A is
stopped, B completes the bounded remaining search. If the first vector remains
unexhausted this uses its cursor; otherwise the report explicitly says
SAME_SNAPSHOT_REMAINING_PARTITIONS, not same-vector continuation.

The discovered fusion record is acquired from separate custody and fully
resolved. Its authenticated type supplies the exact external owner for fold;
the consumer is not supplied that owner ID in advance. A name-only declaration
request resolves its group, and the descriptor supplies the demanded value
hash. Custody is closed/reopened before the body is fetched and bound. The
receiver retains the target group, fold group and exact body. RESULT records
operation events, returned identifiers, aggregate client/provider costs and
closed provider state; acquired-target/body are retained canonical artifacts.
No native checker, certificate or mathematical-reuse claim is made by this
harness. All calls/loops/objects have fixed finite caps; root owns actual launch.

Completed exchanges report exact payload/header bytes; failed exchanges charge
their reserved body maxima conservatively but do not invent measured header
counts. Header exposure remains separately bounded per attempted request.
Connection/TLS/TCP overhead and failed-work uncertainty must remain in final
workflow accounting rather than being hidden in a successful-response subtotal.

## Durable public operator/client seam (read-only recommendation)

Root requests a concrete next source map, not broad CLI authoring. Existing
transport/custody sources remain held unchanged. A usable operator must retain
resource admission and recover known state across commands; wrapping the current
classes in argparse while resetting SearchSession on every invocation would not
meet that requirement.

### Minimal command/data boundary

One owner-local profile binds its state directories, source/adoption manifest,
allowed foundation/policy/image/verifier parameters, budgets and configured
peer endpoints. This profile is local policy, not a central server or global
identity registry. A node can initialize with zero peers and contribute/store
locally; querying remote data needs at least one actually reachable provider,
but no *particular* provider is indispensable. Peers/configurations/snapshot pins
can arrive out of band or through later bounded provider hints. A provider hint
is never mathematical authority or an exhaustive network membership list.

The minimum command set should expose existing state transitions, not introduce
a mandatory research agenda:

| Local command | Existing seam | Success means |
|---|---|---|
| `init PROFILE` | Store/ModuleStore configuration | Exact bounded local role/state selected; no global registration |
| `contribute MODULE-PACKET --operation ID` | ModuleStore put_group/put_body; future opaque receipt store | Requested exact groups/bodies/receipt bytes durably held under quota; mathematical status is explicit and separate |
| `index EXPORT-WRAPPER --operation ID` | ModuleExportAdapter + Store.admit | Truthful local syntactic feature record appended to selected snapshot; not proof acceptance |
| `query start/summary/page --operation ID` | SearchSession + SearchClient | Finite reserved requests, authenticated metadata intervals and persistent last verified progress |
| `acquire EXPORT-RECORD --operation ID` | AcquisitionClient + ModuleStore | Exact locator/group/body bytes retained; unresolved certificate status cannot silently become truth |
| `verify-module RECEIPT --expected SUMMARY --operation ID` | Forthcoming actual receipt verifier | The exact adopted module relation is cryptographically verified for that summary in this invocation |
| `status/recover --operation ID` | Proposed local admission journal | Known terminal/pending/resource state; no hidden retry, allowance reset or proof inference |
| `serve PROFILE` | Provider over selected roles | Read-only service of already held immutable material under renewed finite service allowance |

Contribution can include structurally valid but unverified material without
making it mathematically trusted. Providers/indexers may choose stricter local
admission policies, but the semantic invariant is that consumers never acquire
an imported-validity role merely because bytes were custodied or popular. Source
elaboration, local investigation and proof production remain separate explicitly
funded operations. The CLI does not execute arbitrary source during remote get,
query, receipt storage or feature extraction.

### Concrete handshake with the new receipt module

Read source `modules/receipt/src/journal.rs`, newly authored by mechanism:
fixed216bytes, magic DMKNM001, profile1, image[8u32], foundation32,
semantic-policy32, ModuleSpecID32, groupRoot32, groupCountu32, ranku64,
witnessHash32. Integer words are little-endian. Journal validation recomputes
ModuleSpecID from the existing summary schema, foundation/policy/group root and
count. Image identity is an acceptance profile, not part of immutable module
mathematical identity. This source is prospective pending root/reviewer adoption;
there is not yet an actual v5 receipt to transport or accept.

Minimal receipt-library interface (naming proposal, not a replacement encoding):

```text
verify_module(actual_receipt_bytes, expected_module_summary,
              locally_adopted_verifier_profile, finite_limits)
    -> process-local VerifiedModule evidence or explicit refusal
```

It must authenticate the actual guest image/trust parameters, verify a fully
resolved receipt with all recursive assumptions discharged, decode the exact new
journal, recompute its summary/ModuleSpecID and compare every expected foundation,
policy/group binding. Mere journal decode, an ImportClaim, a successful native
exit or a cached caller-supplied `verified:true` field is not this operation.
An expected module summary must be pinned independently of the sender's success
claim; an opening-derived summary is subsequently bound by the actual verifier.

An in-process Rust API can mint a non-publicly constructible VerifiedModule
value. If Python calls a verifier executable, the public controller must itself
launch the exact adopted binary under supervision, hash-bind its actual receipt
input and same-call output, and build its private evidence from that verified
invocation. Do not import authority from an arbitrary saved JSON success report.
Only exact groups whose openings bind that evidence may receive imported roles.
Cold processes reverify the retained succinct receipt; this does not replay its
proof ancestry. A process-local cache may avoid duplicate verification of the
same receipt bytes/profile while host integrity holds.

Receipt custody remains separate: immutable opaque receipt bytes are keyed by
their raw digest; (ModuleSpecID,receiptDigest) is a bounded **unverified offer**
index. Several proof witnesses/receipts/ranks may certify the same immutable
ModuleSpecID, so receiptDigest must not replace ModuleSpecID or force one
globally canonical proof. Persistent records may retain actual verification
evidence for audit, but no networked serialized cache row grants authority.

A future read-only receipt route needs an explicitly bounded opaque binary
response profile alongside current canonical-JSON routes. Its expected media
type/size is determined by the route and adopted receipt scheme, not arbitrary
sender headers; no base64 wrapper or old-v4 receipt compatibility is presumed.
The current HTTP code and ModuleStore do not implement this receipt route/store.
Receipt envelopes and byte caps await mechanism's actual chosen verifier format.

### Local write-ahead resource admission, not a global ledger

Add one bounded local operation journal; it records this owner's work, not all
network mathematics. Index every lookup by OperationID/request sequence so
starting/recovering one operation never scans complete unrelated history.
Suggested minimum tables are:

```text
allowances(id, immutable_policy_hash, granted_resource_vector,
           charged_resource_vector, reserved_resource_vector)
operations(id, request_hash, profile_hash, allowance_id, state, result_hash)
attempts(operation_id, sequence, action, immutable_input_hash,
         full_reservation, state, actual_or_conservative_charge, output_hash)
outputs(hash, kind, byte_count, durable_location)
```

All arrays/rows/blobs have explicit count/byte/page quotas. Resource dimensions
include requests/providers/received body and header bytes, examined rows/matches,
storage, verifier/native/prover invocation counts and CPU/wall/process/log bounds
where those workers are selected. At every durable transition, componentwise:

`charged + reserved <= granted`.

Before opening a connection, starting verification or creating a transfer file,
an immediate SQLite transaction reserves the *full next step* and records exact
input/policy identity. Commit that reservation durably before external I/O.
Completion records bounded actual cost where measured; otherwise consume the
reserved maximum conservatively. A lost reply or killed process cannot refund
unknown work. Explicit owner grants may add future allowance; reopening a CLI,
retrying an ID or restarting a service cannot reset the old allowance. Local
service maintenance needs its own finite renewable allowance, not an unlimited
background exception.

Recovery is not automatic replay. First ensure the old owned process tree is
quiescent using its actual supervised job/process identity; a reused PID is not
authority to terminate a process. Mark interrupted attempts as uncertain and
conservatively settle their reservation. Read-only inspect the exact target
stores/output pins to resolve whether a structural write committed. Since CAS
and identical Store admissions are idempotent, a later newly reserved retry can
coalesce exact existing material without duplicate mathematical publication.
An ID reused with a different immutable request must refuse.

The operation journal and existing stores are separate SQLite databases. Do not
pretend their commits form one atomic transaction. The narrow initial solution
is write-ahead intent plus idempotent exact-object reconciliation: if ModuleStore
committed but the journal result did not, recovery checks the exact stored
opening/body and records that structural fact. If proof verification finished
without a trustworthy completed same-call record, reverify under a new reserved
attempt. No uncertainty resolution can promote structural custody to truth.

Search recovery additionally needs retained canonical raw summary/page responses
or an equally justified private durable representation. The current report JSON
alone is insufficient: reconstruct verified summaries/intervals by replaying only
that operation's retained responses through the actual verifiers, rebind the
snapshot/query and preserve all failed-request charges. This is bounded local
metadata proof checking, not ancestral mathematical proof replay. Pending
tickets remain conservatively charged; no silent network retries occur.

### Source map and execution boundary

Smallest next source proposal:

- `operator/admission.py`: exact operation identity, bounded SQLite allowances,
  write-ahead step reservations, conservative settlement and local recovery.
- `operator/commands.py`: narrow durable command dispatcher over existing
  index/custody/client APIs; keeps operational/mathematical facets separate.
- `operator/receipt_gate.py`: exact adopted verifier invocation and private
  evidence binding, implemented only against mechanism's actual verifier API.
- `custody/receipt_store.py`: bounded opaque receipt bytes/unverified offers;
  no authority constructor or proof execution in its get/put path.

Reuse tested *invariants* from frozen v4 rather than import its format-specific
controllers wholesale. `receiver/cert_stages.py:reserve/invoke` already require
full-stage CPU/deadline reservation and actual process-tree closure; the old
operator/library_session pins code/config and bounds request/response logs.
Those are relevant supervision patterns. Their old identity/receipt formats,
large accumulated state census and OS-specific public facade are not a v5
generic admission journal. Adapt the smallest reviewed process-supervision seam
only when an actual verifier/worker is selected.

This closes one central operability gap: an agent can stop/restart its owner
process and retain funded, trustworthy progress instead of an ephemeral toy
session. It does not require a UI, package redesign, global task list, universal
bootstrap, political identity/attribution mechanism or a second proof campaign.
No broad CLI source or runtime is authorized by this read-only recommendation.

## Central cost diagnosis: compress physical sparse-map paths

The actual `discovery-network-01` result is a correctness success but exposes a
central efficiency defect: two indexes of only18 exported declarations plus the
selected network/custody operations consume44.1875 inclusive Job CPU seconds;
each retained SQLite index is28,975,104 bytes. Search transfers105,068 reply
payload bytes and2,947 request payload bytes. These are whole-run measurements,
not separately measured index-build CPU. No duplicate network run is proposed.
The root is collecting the retained database's read-only node census; the
analytic diagnosis below follows directly from current source and does not
pretend to be a per-stage timing profile.

### Dominant source mechanism and rejected insufficient fixes

`Store.admit` loops over each selected export's formal features. For **every
posting**, `authenticated_index.map_set` writes one map leaf plus all256
map-node ancestors. This is a sparse256-bit authenticated map represented as a
physically uncompressed binary trie. Empty subtrees themselves are implicit,
but every unary path bordering them is materialized. Thus a feature occurring
once still needs257 physical map records before its partition/vector records.
Every changed feature root replaces its entire256-level path. Copy-on-write
correctly preserves old snapshots, but also retains intermediate map roots
created between features of one admission, although these are never snapshots.

Each new CAS record currently performs a SELECT, meta SELECT, meta UPDATE and
INSERT, as well as canonical JSON encoding/hash verification. The long chains
therefore amplify more than just SHA calls: they multiply SQLite B-tree writes,
rollback-journal work, hash text keys, encoded JSON and per-row quota updates.
`admit` first calls `map_get` to obtain the old feature root; `map_set` then
calls `map_get` a second time for the same current root/key. Both regenerate
the257-entry namespace default-hash chain and both traverse selected stored
nodes. `get_node` and the pure `_get` each recompute the node's hash. These are
independent avoidable computation factors, not the storage root cause.

Batching transactions is not the first answer: there is already one SQLite
transaction per admitted export. A multi-export batch would change publication
granularity and leave the256-per-update representation problem. Hash/node
memoization helps CPU but not persistent amplification. Batch updating all
features within one existing admission can remove unreachable intermediate
roots, but does not remove its mostly-unary paths. A new sorted B-tree or
different commitment could be efficient, but would unnecessarily change
SnapshotIDs, authenticated proofs and client compatibility for this defect.

### Exact recommended source selection: storage-only compressed map runs

Retain the **existing logical sparse Merkle map**, hash domains, leaves,
256-level expanded proof, partition/vector commitments, records and snapshots.
Replace maximal physically unary map paths by a bounded authenticated run.
This is Patricia-style physical compression, not a weaker/new truth predicate.
For namespace `N`, let `E_N[d]` be the current `map_empty(N)[d]`. A run contains:

```text
kind = map-run
namespace = N
depth = d                  0 <= d < e <= 256
end_depth = e
path = 256-bit hex value    zero outside bit positions [d,e)
child = c                  c != E_N[e]
```

Bit positions are numbered from the most-significant key bit. Start with
`v_e = c`. For `j = e-1,...,d`, use the **unchanged** logical hash:

```text
v_j = H(MAP-NODE, j, v_(j+1), E_N[j+1])  if path[j] == 0
v_j = H(MAP-NODE, j, E_N[j+1], v_(j+1))  if path[j] == 1
```

The run is stored by `v_d`, not by a new domain hash of its JSON encoding.
Lengths, namespace, path masking, child and expected starting depth are checked
before traversal; all hashing is at most256 iterations. Endpoints are either
the existing map leaf at depth256 or a genuine two-nonempty-child branch at
depth`e`. New writers merge adjacent runs and emit ordinary map-node records
only at branches. The empty map remains entirely implicit.

`map_get` traverses the compressed structure and reconstructs the exact old
256 siblings. If a query diverges inside a run, the run's authenticated suffix
hash is the nonempty sibling at the divergence; lower queried subtrees are
default. Reporting all-default siblings at that divergence would be unsound.
For a matching path, the run supplies default siblings and traversal continues
at its child. Hence `verify_map` can remain unchanged.

`map_set` performs one bounded compressed traversal:

1. An empty subtree becomes a leaf plus its unary run.
2. At a branch, recurse into the chosen child and recreate that branch.
3. At a matching run, recurse at its endpoint, then merge adjacent runs.
4. At the first divergent bit inside a run, retain its old suffix, construct
   the new leaf/suffix, introduce one genuine branch and retain any common run.
5. At the existing exact key's leaf, replace only its selected feature root.

Use an internal traversal result/callback to supply the old feature root to
the posting update, or a private checked path token bound to exact namespace,
root and key. Do not accept a caller-supplied arbitrary sibling array as an
unchecked authority to update the map. The current duplicate `map_get` should
not survive merely because physical compression made it cheaper.

For `F>=1` keys, a single fully compressed snapshot contains `F` leaves,
`F-1` genuine branches and at most`2F-1` runs: at most`4F-2` physical map
records, versus approximately`256F` before sharing in the current tree. For
an update whose old lookup path contains`b` genuine branches, replacement
requires at most`2b+2` records for an existing key or`2b+5` for an insertion
split. Here `b<=min(F-1,256)`; expected logarithmic depth additionally assumes
well-distributed feature hashes and is **not** an adversarial guarantee.
Across retained histories cost remains proportional to changed paths; this
does not solve infinite retention and does not authorize deleting old cuts.

Importantly, unchanged commitments still require up to256 hash steps to form
a changed root. The main saving is physical I/O/storage, not a claim that
SHA computation disappears. Return/record actual storage and hash work separately
in local build evidence. Keep the public page's existing
`charged:{node_reads,examined}` format. The selected implementation counts
node_reads as capped accessor calls, including cache hits; node_selects separately
counts actual CAS SELECT statements (including put deduplication). Enforce a
separate finite internal hash-work limit/deadline.
Do not substitute fewer SQL reads for a claim of negligible total work.

### Compatibility, quotas and bounded memoization

This is **wire/commitment compatible, not automatically disk-format
compatible**. New physical records need an explicit local store encoding
version/profile. Initial implementation should create fresh V2 physical stores
and leave all V1 evidence/databases unchanged; no in-place migration is needed
to decide the central issue. A later dual reader may reconstruct old expanded
records, but old software cannot decode map-run records. Avoid silently calling
the changed local format V1 merely because public snapshots remain V1.

Do not accidentally weaken `CAS_CONFLICT`: distinct compressed/expanded
encodings can yield the same logical map hash without a cryptographic collision.
The narrow fresh-store solution is one canonical compressed representation,
with deterministic maximal-run normalization and exact-byte equality on
re-insertion. Do not mix expanded unary and compressed records in one CAS and
then suppress all byte conflicts. Legacy import/mixed-representation support
needs a separately specified logical-equivalence check if later selected.

Cache immutable namespace default-hash tuples with a finite capacity (selected
implementation:64 namespace chains, plus one fixed partition-default chain).
Cache verified decoded nodes only within one operation, with a strict entry/
encoded-content bound and no unbounded global cache. Enforce caps before work/charge just as current reads
and writes do. Persistent `logical` must charge actual stored compressed bytes
and all new metadata, independently of SQLite page caps. Quota exhaustion or
deadline expiry must roll back the whole admission, including meta counters,
new nodes and snapshot. Explicitly report transient memory/hash work; compression
does not entitle the node to ignore its prior per-operation resource envelope.

### One changed-boundary qualification, not another network campaign

Proposed implementation ownership is this scale lane, limited to
`discovery/authenticated_index.py`, `discovery/discovery_store.py` and new focused
compression tests; root-owned discovery contract tests and all retained source
snapshots are untouched. Source changes await root selection. New tests should:

- Compare compressed roots and **expanded proofs** to a simple independent
  old-format sparse-map reference across insertion/update orders, empty maps,
  long shared prefixes, divergence at first/last bit and exact old snapshots.
- Reject malformed depth/path/namespace/child bindings, corrupted stored runs
  and noncanonical encodings; test quota/deadline rollback and restart.
- Re-establish pre-increment read-cap behavior at the new smaller prelude.
  The old266/269-read test is retained evidence for its old implementation,
  not a constant that compressed storage must deliberately preserve.
- Build exactly **one** new index from the18 retained network01 export inputs
  in the identical order. Compare every one of its19 snapshot IDs/descriptors,
  record IDs, summary contents and page proofs/results with the retained V1
  database. Only actual work telemetry is expected to differ. Report actual
  byte/node/CPU totals and every failure; do not rerun peer loss/custody/native
  work merely to measure this changed storage boundary. Open the old retained
  database by an immutable/read-only SQLite adapter, not `Store.__init__`, which
  issues mutable PRAGMAs. Reuse the frozen pure commitment/query code or an
  independently specified reader; never migrate or VACUUM retained evidence.

Before runtime, root should adopt a finite resource allocation and a concrete
cost threshold against the retained28,975,104-byte single-index baseline. A
reasonable decision-changing gate is at least90% physical size reduction for
that exact workload, identical public mathematical/discovery bindings and no
new failure of old-snapshot/query/refusal behavior. This is a prospective
engineering threshold, not a measured result or a universal growth theorem.

### Separate remaining search-wire amplification

Physical map compression does **not** shrink the current two-feature summary:
it still sends256 descriptors and256 hex siblings per feature, most describing
defaults. A subsequent sparse summary encoding can omit known default
partitions/siblings and let clients reconstruct the unchanged complete summary
before verification. It requires explicit duplicate/order/bitmap checks and a
new wire encoding discriminator; it should follow the central physical fix,
not be smuggled into its equality test. Search acquisition, cryptographic
mathematical admission, retention and full-cost useful growth remain distinct
unclosed release obligations.

### Source-ready selection and finite comparator

Root adopts the design as D08 and authorizes source implementation only. The
root's immutable/read-only legacy census is now available:18 objects,
362 postings,67 features,19 snapshots,17,427,183 logical bytes;7,074 SQLite
pages at4,096 bytes/page, totaling28,975,104 physical bytes. CAS census:

| Kind | Records | Encoded bytes |
|---|---:|---:|
| map-node | 92,672 | 16,641,140 |
| partition-node | 2,896 | 503,904 |
| map-leaf | 362 | 65,522 |
| vector-leaf | 362 | 68,056 |
| partition-leaf | 362 | 104,475 |

Exactly`92,672 = 362 * 256`: this actual small workload obtained no map-node
deduplication across its posting updates. The analytic amplification is not a
hypothetical large-scale concern; it dominates retained actual encoded bytes.

Source is now ready in `software/v5/discovery/`:

- `authenticated_index.py`: compressed map-run hashing/validation, matching and
  divergent expanded proofs, canonical split/merge and single-traversal local
  `map_update` callback; unchanged public root/proof verification equations.
- `discovery_store.py`: explicit DMKN_DISCOVERY_STORE_V2 physical profile,
  MAXIMAL_SPARSE_MAP_RUNS_V1, exact-byte CAS conflicts, canonical map admission,
  deadline-before-commit including duplicates, rollback cache clearing.
- `test_compressed_map.py`:6 focused contracts, including an independent
  expanded-map reference with first/last-bit and long-prefix splits, old cuts,
  noncanonical/malformed runs, read12/15 boundary, hash/deadline/quota rollback,
  restart, mutable-return protection, CAS conflict and actual corruption.
- `compare_compressed_index.py`: one fresh actual18-export index, identical
  bundle order/records and all19 old snapshots; exact expanded proofs at every
  cut plus all67 final features and absence; exact final two-feature summary;
  five populated pages and one empty page with exact results/proofs excluding
  changed work telemetry; restart, legacy SHA preservation and90% size gate.

Per-operation authenticated-index SHA calls have a2,000,000 invocation cap,
checked before each counted hash; the wall guard also applies. This telemetry
does not purport to count every feature-adapter/record/Python-library SHA call.
The operation decoded-node cache is at most512 entries and2MiB **encoded
contents**; decoded Python objects/copies/container overhead are additional,
so it is not a literal2MiB process-heap bound. Default tuples have bounded
cross-operation memoization; actual warm-cache hash savings are reflected in
counted invocations, not manufactured cold-cache costs. `node_reads` charges
every get accessor, including cache hits, preserving pre-increment ceilings;
`node_selects` records database CAS SELECTs and `node_cache_hits` explains the
difference. Whole-operation/process CPU remains the actual cost measure.

Independent assurance has fully read the first three sources and reports no
blocking algorithm/resource/CAS issue. The comparator is newly ready for its
separate review. No run is launched by this lane. Suggested root selection:

1. Focused6-contract source snapshot, fresh evidence,60 CPU/90 wall seconds,
   one Python child and512MiB outer memory.
2. Only after a reviewed passing boundary, one comparator snapshot using the
   retained network01 index-a database (immutable mode and exact raw hash) and
   the five previously pinned bundles in order: fusion_map, base,
   project_summary, fusion, fold_map. Fresh evidence;120 CPU/180 wall seconds,
   one Python child and512MiB memory. No network, native checker or proof calls.

The comparator records new index-build process CPU separately from compatibility
checking and whole-process time. It **cannot** claim a matched CPU speedup over
network01 because that baseline did not separately time one index build. The
space gate is prospectively fixed and directly comparable; the44.1875 CPU
whole-run baseline remains intact rather than being retroactively attributed.

### Actual compression outcome reported by root

The six focused compression contracts now actually pass with clean process
closure and0.84375 inclusive Job CPU seconds. Root's one-index comparator also
actually passes:28,975,104 ->2,396,160 SQLite bytes, a91.73028% reduction, meeting
the prospectively fixed90% gate. All19 snapshots,421 expanded map proofs,
the exact89,988-byte two-feature summary and six pages agree. Retained database
bytes remain unchanged. New map census:2,054 branches,697 runs,362 leaves.
New single-index build consumed1.296875 measured process CPU seconds and1.36827
wall seconds; total comparator Job CPU14.28125 includes old/new compatibility
checking. This is not a matched CPU speedup against the unsplit network01 run.
Independent actual-outcome adoption remains root/reviewer-owned. No index
rebuild or duplicate network campaign is selected here. Indefinite retained
history/GC is not solved by compression.

## Compact summary wire boundary: selected new source only

The unchanged summary still sends89,988 bytes for two selected features. Root
selects `discovery/summary_wire.py` plus independent-focused
`discovery/test_summary_wire.py`; existing commitment/store/query/session and
transport sources remain untouched. The interface contract was sent to and
adopted by root before implementation.

New discriminator is `DMKN_FORMAL_QUERY_SUMMARY_COMPACT_V1`. Preserve the complete
existing header: namespace, snapshot ID/descriptor, sorted query features,
coverage marker and mathematical_acceptance:false. Each row is:

```text
feature_id: exact selected query feature
presence: "present" | "absent"
partitions: strictly increasing nonempty {partition,count,tree_root} descriptors
siblings: strictly increasing [depth,hash] entries differing from E_N[depth+1]
```

Partition/depth indices are0..255, counts1..MAX_VECTOR, all hashes canonical64
hex characters. Explicit default siblings and zero-count partition descriptors
refuse, as do duplicate/out-of-order indices and unknown fields. `absent` requires
partitions:[] and reconstructs null; `present` with partitions:[] reconstructs
the256 default descriptors. Those cases must remain distinct: an authenticated
empty feature leaf and absence of the feature are different commitments.
Omission of a truly nondefault value can remain structurally valid but then
fails the unchanged authenticated summary verifier. Codec success is not proof
success and cannot update trusted coverage.

Public helpers:

```text
encode_summary(expanded, expected_snapshot_id, namespace, features,
               max_wire_bytes=1MiB, max_expanded_bytes=1MiB, check_budget=None)
    -> canonical compact bytes
decode_summary(raw, expected_snapshot_id, namespace, features,
               max_wire_bytes=1MiB, max_expanded_bytes=1MiB, check_budget=None)
    -> ordinary reconstructed SUMMARY_V1 dictionary (NOT authenticated)
```

The caller must pass the dictionary to the existing `Q.verify_summary` using
its independently selected snapshot/query before retaining verified state.
The codec checks exact header/query/snapshot bindings but does not verify the
map proof or claim truthful source indexing. Encoder and decoder are lossless
structural transformations, not new authority constructors.

Before allocating expanded arrays, decoding validates all sparse shapes/counts
and computes the **exact canonical expanded JSON size** from fixed scalar
widths,256 indices, actual count digit widths and null-vs-present flags. It
refuses if that would exceed the independently selected expanded-byte ceiling.
Only then does it reconstruct known defaults. Final serialization length must
equal the predicted size. Maximum arrays are eight rows,2,048 partition
descriptors and2,048 sibling hashes. The wire and expanded byte ceilings are
not literal Python heap bounds; object/copy/container overhead is additional.
An optional owner guard runs before parse, during each validation/expansion row
and before return. Outer process/memory limits and actual deadline enforcement
remain required when integrated.

Seven focused source tests use an independently constructed full-path map,
not new map-run construction, and check exact reference compact bytes, exact
expanded round trips and the original verifier. They cover malformed indices/
ordering/duplicates/default encodings, namespace/snapshot/query mismatch,
absence-vs-empty-presence, false omitted data rejected by authentication,
noncanonical/deep/duplicate-key JSON, malformed expanded input and exact byte
limits. A mocked default constructor proves the expanded-size refusal occurs
before reconstruction. These newly authored tests are source-only pending root
selection and review; they do not inherit passing status from compression tests.

### Required narrow integration after source qualification

SearchSession must charge `len(actual_raw_wire_bytes)` before parsing, preserving
the current failed-reply accounting and full unknown-outcome reservations. Do
not feed reconstructed legacy bytes into `accept` as if they were transmitted:
that would defeat and misreport the wire saving. Keep finite expanded/decode
work caps separately, plus the existing deadline check before any summary/
coverage commit. Bind the expected wire encoding to the pending request/ticket,
not an unauthenticated sender success flag. Compact and expanded formats need
explicit request/route negotiation; old callers retain their old encoding.

The provider must also keep the two ceilings distinct: construct a bounded
legacy summary under its fixed expanded ceiling, then encode under the caller's
wire ceiling. Calling `Store.summary(max_bytes=small_compact_wire_cap)` would
incorrectly refuse a valid small compact reply merely because its temporary
expanded form is larger. A new read-only compact-summary route is a minimal
possible discriminator; no pagination change, global negotiation service or
CLI redesign is needed. These are integration requirements, not implemented
session/transport behavior yet. No runtime is launched by this lane.

### Compact public integration source ready

Root reports all seven pure wire tests actually PASS, clean closure,
0.765625 Job CPU seconds. It then selects only the changed public integration:
`discovery/search_session.py`, `transport/http_provider.py`,
`transport/clients.py`, and new `transport/test_compact_summary.py`. The used
codec/compression snapshots and actual evidence remain unchanged. No tests are
rerun by this lane, and no index is rebuilt.

Agreed public client/session API:

```text
await client.summary(provider, snapshot_id, max_bytes=1048576,
                     encoding="expanded-v1", max_expanded_bytes=1048576)
session.begin_summary(provider, snapshot_id, max_bytes=1048576,
                      encoding="expanded-v1", max_expanded_bytes=1048576)
```

`encoding` and `max_expanded_bytes` are keyword-only. Default expanded operation
retains `/v5/discovery/summary` and its exact three request fields. Explicit
`compact-v1` selects `/v5/discovery/summary-compact` with four fields:
snapshot_id, features, max_bytes, max_expanded_bytes. Both caps are1024..1MiB.
The expanded cap on an expanded request remains a separate local decoding cap;
it does not silently change the old route/request profile. Invalid local
encoding/cap selection refuses before request reservation.

The private pending ticket retains its own encoding/expanded ceiling. Mutating
a returned public ticket cannot change those bindings. On reception, actual raw
wire bytes are charged first; compact decode uses the selected ceiling and
session deadline guard. Only subsequent unchanged `Q.verify_summary` success
and the final live-deadline check allow private summary/coverage insertion.
An expanded response to a compact request or compact response to an expanded
request refuses; there is no format sniffing, automatic fallback, hidden retry
or renewed allowance. Invalid/incomplete proof replies keep their actual byte
charges. Interrupted/unknown exchanges retain existing conservative reservations.

Provider dispatch on the new compact route returns already canonical wire
bytes; existing routes still return ordinary dictionaries. `_serve` chooses
serialization by the explicit selected route. Compact requests reserve their
validated `max_bytes` allowance, **not** the larger reconstruction ceiling or
the route's1MiB absolute maximum. The selected Store summary is built under
`max_expanded_bytes`, then compressed under `max_bytes`, with an owner deadline
guard before/during encoding and before response transmission. An over-budget
request cannot create a free error body or claim global absence.

Seven source-focused integration tests isolate these new boundaries: explicit
route selection and actual-wire charging, old expanded compatibility/no silent
downgrade, private ticket mutation and false-proof refusal accounting, separate
wire/expanded caps, deadline expiry during reconstruction and after verification,
memory-stream service reservation/exhaustion, and provider request/cap refusal.
They reuse the prior wire fixture without rerunning its test suite, create no
index, and do not repeat pages/custody/provider-loss scenarios. Mocked exchange
and memory-stream checks are **not** real network evidence. Source is quiescent
for independent review/root-selected execution; root separately authors one
actual public loopback comparison over the retained summary.

### Exact local-check selection and subsequent reported outcome

At root's request this lane prepared
`experiments/v5-local-checks/compact-summary-controls-01-selection.json`, SHA256
`9470f0d5ace47bdfa7d936d14a1115aec0cf0ee6b9603941a4bc6cd1a2b4a335`.
It pins all12 transitive project source files (including the imported wire
fixture and custody helper's Store import) and18 selected Python/native runtime
files;45 CPU seconds,90 wall seconds,512MiB, two processes and1MiB per log.
Read-only pin checks found no mismatch and the named output was fresh before
root launch. Python stdlib/Windows are not falsely described as a hermetic
toolchain proof. This lane launched nothing.

Root subsequently reports the seven changed integration controls passing and
the actual retained-summary public comparison passing:3,017 compact payload
bytes versus89,988 expanded bytes (about96.65% fewer), with no index rebuild.
Root/reviewer own the exact terminal evidence and adoption. These outcomes do
not solve provider discovery, intersection selectivity or indefinite retention.

## Next central discovery priority: obtain offers before optimizing candidates

**Recommendation: first implement bounded namespace/query -> provider/snapshot
offers over owner-approved contacts. Then add a distinct candidate-only path;
retain the existing authenticated interval-scan API unchanged.** No source or
runtime for these future mechanisms is selected by this recommendation.

### Concrete gap and minimum reuse

Current `SearchClient.summary` requires both a configured endpoint and an exact
SnapshotID. The actual consumer does not know the target ExportID, but the
harness still supplies the snapshot out of band. Thus current code can verify
a chosen provider's selected index; it cannot itself obtain that selection from
its namespace/query. Optimizing intersections first leaves this ordinary public
entry point incomplete.

The smallest next seam is a read-only **offer** operation: a client sends its
namespace,1..8 formal features and finite limits, with no SnapshotID. An index
provider freezes its own current `Store.status()/snapshot()` selection using
existing indexed point reads, then returns that descriptor/ID with the already
implemented compact summary. The client validates the namespace/query/profile,
recomputes the offered SnapshotID, explicitly pins that provider-selected cut,
and invokes existing summary verification. Selecting a self-consistent offered
root is **not** proof of issuer honesty, truthful features, global completeness,
freshness or mathematics. Those limits already apply to provider-built indexes;
the offer must make its source/selection explicit instead of pretending the
root was independently authenticated beforehand.

Reuse `Endpoint/configured`, bounded `exchange`, provider quotas, compact codec,
`Q.verify_summary/plan_partitions` and SearchSession's pre-I/O reservation/
failed-byte/deadline discipline. Add the offer operation to the **same finite
workflow accounting**, not a new uncharged session that resets budgets before
each queried provider. An offer arrives before its SnapshotID is known, so
attempt/request/provider/byte and pending-snapshot reservations need a genuine
pre-snapshot transition. A serialized offer never constructs trusted coverage.

Initially choose at most`B` owner-approved contacts from a bounded local contact
catalog. Use namespace/formal-symbol scope hints and locally observed success/
cost to order them; those hints are advisory, not mathematical ranking authority.
Offer summaries provide authenticated per-cut counts for a cheap subsequent
work estimate. Identical SnapshotIDs share one coverage domain; provider
replacement must not restart completed intervals. Different snapshots keep
separate coverage; candidate ExportIDs can be deduplicated without inventing a
global root. Zero peers means local-only operation, not magical network search.

Contact maintenance needs finite entries/bytes/expiry, namespace scoping,
bounded referrals/hops and per-contact attempts, failure backoff without hidden
retries, and an owner-selected egress policy before dialing any new address.
Untrusted peer hints must not authorize requests to loopback/private services.
Offer expiry is bounded by local observation/policy, not trusted sender clocks;
it is not an availability lease. Old snapshots can remain valid but unavailable.
Maintenance/republishing has a separately funded finite allowance. No particular
bootstrap server is indispensable, but success requires some reachable honest
provider/contact path within the selected budget. This first seam removes
injected snapshot IDs; it does **not** establish huge-network routing recall.

The frozen v4 `overlay/library_overlay.mjs` already has bounded Kademlia
`findProviders`, provider limits, TTL/reprovide limits, address policy and a
quota datastore. Reuse those *invariants* and possibly its small rendezvous
adapter later. Do not import its whole old fragment bridge: its key regex,
namespace derivation, identity formats and transport are incompatible with v5.
A separately domain-separated v5 hint adapter may later expose the same bounded
contact-offer interface; a large DHT rewrite is neither necessary nor selected.

### Why compact metadata does not solve hot conjunctions

For a truthful selected snapshot`s`, the existing exhaustive algorithm examines

`E(Q,s) = sum_p min_{f in Q} count_s(f,p)`

anchor records to cover the whole selected domain, apart from authenticated
zero cases. With`N` divisible by512, place`N/512` records of feature`a` and
`N/512` disjoint records of feature`b` in each partition. Query`{a,b}` has zero
matches but`E=N/2`. The protocol must transmit those examined nonmatches to
justify its current interval-coverage claim. Fixed256 partitions reduce neither
this total nor worst-case search work; deeper random-ID hash partitions do not
generally produce a sublinear intersection theorem. No new feature may relabel
a provider's unsupported filtering as authenticated completeness.

### Alternatives and the selected next-after-offers boundary

| Approach | Concrete reuse/benefit | Cost/limit |
|---|---|---|
| Existing B-tree seek/intersection | `postings` has `(feature,partition,ordinal)` primary order and `(feature,partition,object_id)` unique lookup. Drive a bounded rarest-anchor interval, probe other conjuncts by exact object ID and fetch full records/proofs only for matches. | Ordinal vectors are **not** object-ID-sorted Merkle sets. SQL filtering does not prove skipped intervals. Worst-case server work remains linear; cap scans/VM work/deadline. |
| Object-ID merge/seek | The unique B-tree order supports local sorted-ID intersection; monotone seeks may skip favorable gaps. | Current authenticated vectors commit admission ordinals. The database's sortedness is not a new authenticated range-proof relation; dense/disjoint sets still have linear worst cases. |
| Dense/compressed bitmaps | Fast local wordwise AND can help repeatedly queried dense features; local object ordinals can name bits. | Extra storage/update/cut-version costs; dense space scales with the local ID universe, compressed bitmaps have distribution-dependent benefit. They do not certify filtering and do not route to providers. |
| Selective joint/composite keys | Materialize frequently reused conjunctive intersections and amortize them over future queries. | All pairs of128 features already mean8,128 pairs/object; all subsets are infeasible. Choose a bounded funded subset by observed demand. A joint feature is not silently an existing anchor; external proofs require explicit semantics or remain only a local acceleration. |
| New authenticated set/intersection proof | May certify stronger skipped-set claims, if the construction/cross-index relation is justified. | Substantial commitment/build-assurance change and still no universal cheap intersection proof. Premature before a demonstrated need for certified exhaustiveness. |

After offers, prefer **bounded positive-candidate retrieval using current
B-trees**, not a new tree/bitmap protocol. A separate response returns selected
matching records, their existing snapshot/vector membership proofs and explicit
`POSITIVE_MATCHES_ONLY` status. It does not enter `Coverage.accept`, advertise
verified scanned intervals, or turn a zero-result response into absence. A
provider may propose a continuation position, but that is an advisory cursor,
not verified coverage. The current exhaustive API remains available when its
stronger evidence is actually wanted.

With at most`C` scanned anchor IDs,`d<=8` conjuncts and`k` returned matches,
straightforward indexed probes cost`O(C*d*log M)` local DB work; wire payload
scales with`k*(record_size+log vector_length)` instead of all`C` nonmatch records.
An honest source implementation checks the snapshot's per-feature ordinal
ceilings on each probe; matches get their exact old-snapshot membership proofs.
Strict scan/SQL-step, result, byte, wall and memory caps remain mandatory. This
is a useful finite network-cost improvement, **not** a claim that finding a rare
match takes sublinear server time or that returned metadata is mathematical
knowledge before acquisition/feature recomputation/certificate verification.

An exact next discriminator should begin with only namespace/features and a
small contact set, obtain and pin an offered snapshot, then use the already
qualified summary/page path to discover a result. Replace or stop one contact
without a mandated central endpoint; verify all failed attempts stay charged.
Only then select a fixed sparse-intersection workload for candidate filtering.
Provider-hint quality and growth benefit remain conditional/measured hypotheses,
not consequences of root hashes or small loopback payloads.

## Implemented provider offers: source-ready, not yet actual-qualified

Root approved the minimal one-roundtrip entry point. New source is confined to
`software/v5/discovery/search_session.py`, `transport/http_provider.py`,
`transport/clients.py` and the new `transport/test_provider_offer.py`. Existing
Store roots, summary/proof schemas, compact codec and immutable used evidence
are unchanged. This lane has launched no runtime.

Public call:

```python
await client.offer(contact, max_bytes=8192,
                   max_expanded_bytes=1048576, max_age_ms=60000)
```

The contact must already be in the finite owner-configured endpoint map. The
client sends `POST /v5/discovery/offer` with exactly `namespace`, `features`,
`max_bytes`, `max_expanded_bytes`; no caller-known snapshot ID is needed. One
selected provider freezes `Store.snapshot()` and computes its existing exact
SID, obtains that cut's ordinary summary and applies existing compact encoding.
There is no extra redundant summary request. It sends a canonical
`DMKN_DISCOVERY_OFFER_V1` envelope with exactly:

```text
schema, namespace, features, status, reason, summary,
global_complete=false, mathematical_acceptance=false
```

The finite status/reason relation is:

| Status | Reason | Summary |
|---|---|---|
| `OFFERED` | `SNAPSHOT_SELECTED` | Existing compact summary, including exact SID |
| `NO_OFFER` | `ROLE_NOT_SERVED` or `NAMESPACE_NOT_SERVED` | null |
| `REFUSED` | `SUMMARY_RESOURCE_BOUND` | null |

Malformed requests, corrupt state and unexpected provider errors close under
the existing transport profile; they are not fabricated no-offer results.
Recognized finite summary resource refusals may produce `REFUSED` while the
provider's operation deadline remains live. The reply reservation and final
wire check cover the **whole envelope**, not only its inner summary. The
expanded cap separately bounds reconstructed summary encoding; it is not a
literal Python heap cap. Existing external process containment remains needed.

### Binding and exact assurance

Before I/O the session privately records provider, namespace, feature tuple,
reply/expansion caps and local offer deadline. Caller mutation of the returned
ticket cannot replace those bindings. The original session query is also fixed;
later mutation of public query fields refuses instead of changing the pending
request's meaning. On reception, raw bytes are charged first, the entire typed
envelope is checked, compact metadata is expanded under its cap and the existing
`Q.verify_summary` authenticates the snapshot/map commitments. A final owner
deadline check precedes insertion. Failed offers never initialize coverage.

`OFFERED` initializes the same selected-snapshot Coverage used by explicit-SID
search. Nonempty partitions start with no scanned interval; committed-empty
metadata partitions have only their existing selected-snapshot empty status.
It proves neither mathematical correctness of records, completeness of a
provider's source library, actual custody, availability, latest global state,
nor global absence. Pages still need their existing proofs. Acquisition and
mathematical acceptance remain separate subsequent boundaries.

### One aggregate workflow, including unknown IDs and failures

The original `limits.snapshots` now bounds **charged snapshot admission/attempt
slots**. Each offer attempt consumes one slot before its SID is known. Typed
refusal, invalid bytes, expiry and unknown/abandoned transport all retain that
slot. Duplicate offers can conservatively consume multiple slots for one SID.
An offered SID is registered only after summary verification, with no second
charge; its later pages or explicit-summary calls do not charge another slot.
An explicit caller-pinned SID's first encounter still consumes one slot, and
repeated encounters of that ID do not. Concurrent reservations are checked
before either result is known. No allowance is created by changing providers.

For compatibility, `used.snapshots` remains the number of distinct known IDs
(caller-pinned attempts plus verified offered IDs), **not** consumed slots.
`snapshot_budget` explicitly reports `charged_attempt_slots`,
`known_snapshot_ids`, and `limit`; the first field governs the ceiling. This
avoids describing failed unknown-ID offers as unique authenticated snapshots.
Requests, raw bytes, providers, pages, examined rows, candidates, wall duration
and in-flight operations remain the original single session's allowances.

### Freshness is owner-local elapsed time, not remote data recency

`max_age_ms` is request-relative monotonic elapsed time, clamped by the session
deadline. It bounds eligibility to adopt that reply and marks a contact/SID hint
expired after the local bound. No sender timestamp, nonce freshness assertion,
global latest claim or availability lease is trusted. A malicious provider may
offer an old valid cut even in a fast response. Hint `fresh` means only that this
local elapsed-time bound has not expired; it is **not** snapshot recency.

After adoption the caller has an immutable pinned SID. Expiring the contact hint
does not erase that summary, make its commitments false, or prohibit an explicit
page request for the same SID. The ordinary session deadline still applies.
There is no automatic hint reuse, arbitrary referral dialing, retry or refresh.

### Prepared exact focused selection

`experiments/v5-local-checks/provider-offer-controls-01-selection.json`, SHA-256
`15f7c0b9a40d191da5ce0a5d0b96ac5b7efb8312db8090b3232b6df10ae24946`,
selects 14 transitive project source pins, 18 runtime pins, 45 CPU seconds,
90 wall seconds, 512 MiB, two processes and 1 MiB each log. Root owns launch
after independent review. Nine proposed controls cover offer-to-page through
the client, typed refusals, private bindings/proof corruption, concurrent and
duplicate slot accounting, failure budgets, local expiry, total-wire/expansion
caps, memory-stream provider reservation and strict malformed-request refusal.
These are new-boundary in-memory controls, not remote deployment or actual
mathematical-use evidence. Root's later retained-index/receipt integration must
test the public unknown-SID entry point without rebuilding passed indexes.

## Isolated positive-candidate query: source implementation and argument

Root selected `software/v5/discovery/candidate_query.py` and its focused tests
after the offer seam. The candidate module does not change Store schema,
commitments, existing Coverage, SearchSession or HTTP transport. No runtime was
launched by this lane. Source review and root's exact finite run remain required.

### Why this algorithm, and what it costs

For a pinned snapshot `s`, partition `p`, and conjunction `F` (`d=|F|<=8`), derive
each feature's partition descriptor from `s.feature_map_root`. Choose the same
rarest anchor as the exhaustive API, with the same lexicographic tie break. If
its count is `n`, the driver probes only ordinal positions `start <= i < n`.
Each anchor probe uses the existing `(feature_id,partition,ordinal)` primary
B-tree. Each other feature is checked by the existing unique
`(feature_id,partition,object_id)` B-tree, and its returned ordinal must be below
**that feature's count in the same pinned snapshot**, not its latest count.

Rejected IDs never load or parse full objects and never build vector proofs.
Only a surviving ID loads its record, with `admitted_seq <= s.local_cut`, and
opens its exact anchor-vector membership. The returned record must have the
requested namespace, partition/object ID, stored RecordID and all conjunctive
features, and the anchor leaf must commit that RecordID. The client independently
rechecks the record and vector proof under its already authenticated summary.

The anchor membership authenticates the **whole record**, including its feature
list; consequently one anchor proof suffices for positive committed-record
membership. It does not authenticate the provider's non-anchor SQL filtering,
prove correct extraction of those features from an object, or certify omitted
records. Acquiring/recomputing features and verifying mathematical certificates
remain separate necessary boundaries. An inconsistent/malicious index can omit
answers but cannot forge a changed positive record under the selected root
without violating the hash-binding assumptions.

Let `C` be the scan allowance and `k` the number of returned positive records,
with record byte length bounded by `R`. Excluding fixed descriptor-resolution
work, honest provider work is bounded in algorithmic terms by

```text
O(C*d*log M + (k+1)*(R + log(n)*log M))
```

for B-tree table size `M`, ignoring bounded-key hashing constants. The `+1`
covers the final survivor whose record/proof is built but cannot fit the reply
or completes after a resource boundary. Explicit VM, probe, hash, node-read and
time allowances override this asymptotic description. Response wire volume is

```text
O(k*(R + hash_bytes*log(n)) + bounded_envelope)
```

There is **no `C*d` negative-record transmission term**. There is still up to
`C*d` local indexed probing. Dense disjoint features can still require linear
server work; no sublinear semantic-search theorem is claimed. At high match
density, extra secondary probes may cost more than the exhaustive algorithm;
the separate original API remains available. This is a selective network/object-
materialization improvement, not a universal end-to-end speedup.

Object-ID sorted seeks could skip favorable gaps using the same unique B-tree.
They do not dominate ordinal scanning in all distributions, and would require
different advisory cursor/cut semantics because current authenticated vectors
are admission-ordinal ordered. The minimal selected implementation therefore
uses the existing exact ordinal driver. This choice is revisable after a real
central workload identifies a sorting/intersection bottleneck.

### Separate wire relation and continuation semantics

`validate_request`, `page(store,request)` and
`verify_page(locally_verified_summary,request,response)` are isolated public
functions in the new module. Request schema is
`DMKN_FORMAL_CANDIDATE_REQUEST_V1`; fields are namespace, exact snapshot ID,
features, partition, anchor, start and limits. Response schema is
`DMKN_FORMAL_CANDIDATE_PAGE_V1`. Every result explicitly says
`POSITIVE_MATCHES_ONLY_NO_VERIFIED_SCAN_COVERAGE`, `global_complete=false`, and
`mathematical_acceptance=false`.

Hits carry strictly increasing anchor ordinals, complete bounded records and
ordinary vector siblings. There is no negative-record list. The verified result
reports `VERIFIED_POSITIVE_COMMITTED_RECORDS_ONLY`, with
`verified_scan_coverage=false`. It exposes remote work/termination only as
`provider_work_claims` / `provider_termination`; those are not cryptographic
evidence. Existing `Coverage.accept` refuses this schema.

The continuation is explicitly
`ADVISORY_POSITION_NOT_VERIFIED_COVERAGE`. In the honest implementation `next`
advances after a nonmatch's probes finish, or after a positive record and proof
fit the reply and the deadline remains live. Interruption during an item leaves
`next` at that item, so retrying does not silently skip an unfinished positive.
The response can terminate at an `anchor_boundary` or at a scan, match, byte,
probe, node, hash, SQLite VM or time limit. Even `anchor_boundary` is an advisory
endpoint, **not** a proof that the selected corpus was exhaustively searched.
No-hit responses are not absence proofs. If setup cannot derive descriptors
within its allowance, `anchor_count=null`, zero hits and unchanged `next`
explicitly describe a resource refusal rather than a completed search.

### Resource envelope, including proof-building queries

Per-call bounds are: scan1..4096, matches1..8, full reply2048..1MiB,
timeout1..1000ms, record/index probes1..65536, node reads1..100000,
hash calls1..2,000,000, and data-path SQL VM allowance100..10,000,000.
All candidate, snapshot, CAS and proof-building SELECTs share one guarded SQL
executor. Node reads include cache hits. Its operation cache is at most512
decoded nodes and2MiB encoded bytes; Python container overhead is additional.
Snapshot/node/record encodings retain the existing4096/4096/16384-byte limits.

The SQL progress callback uses100-instruction blocks. Before a statement starts
and before each next callback block, it reserves100 instructions or refuses.
Incomplete blocks are not refunded. Thus `charged.sql_vm_steps` is a conservative
**upper charged allowance**, not an exact executed-instruction measurement.
Probe counts are separate and do not replace the VM cap. This prevents a
pathological query plan from pretending one expensive SQL statement is one unit
of bounded work. Callback aborts become explicit resource terminations; parsing
or corrupt-state failures instead raise and require full conservative caller
accounting when integrated.

The owner must lend the Store connection exclusively and have no pre-existing
SQLite progress handler. Candidate processing installs its handler, temporarily
sets `busy_timeout=0`, and restores the previous timeout/removes the handler in
`finally`, including on corrupt input. Three fixed connection-control PRAGMAs
are explicit constant overhead outside the data-query VM counter. No on-disk
metadata changes, schema migration or persistent authority/cache are introduced.
The deadline is cooperative and hard process/memory containment is still needed;
the API does not promise real-time scheduling or interruption of arbitrary
operating-system stalls. Hash charges cover authenticated-index calls plus the
query identity and each loaded record identity; generic JSON/SQLite work has
separate bounded byte, count and VM allowances.

Whole-envelope sizing reserves worst allowed counter/cursor scalar widths
before accepting another hit, so a later limit name or larger charge count does
not invalidate a previously accepted byte allowance. The final exact encoding
is checked again. Refusal may spend one full positive-record/proof attempt
without returning it; this work is retained and `next` stays unchanged.

### Future aggregate client allocation (not integrated yet)

This source is not independently deployable transport. Before integration, the
same existing SearchSession must own candidate request/provider/snapshot/page,
scan, match, byte, deadline and in-flight allowances. Reserve before I/O. Since
the scan/probe claims are not authenticated, conservatively consume the full
requested scan allowance on success as well as failed/unknown outcomes; do not
refund it based on a remote low work count. Bound receiver proof checking by
its local hit/record/proof-size limits and owner deadline, independently of any
remote meter. Candidate replies must never mutate Coverage or reset an existing
workflow. Owner-controlled per-provider resource service limits remain distinct
from client-wide contact budgets. These are integration requirements, not a
claim that the isolated module already implements aggregate network accounting.

### Prepared focused controls

`candidate-query-controls-01-selection.json` SHA-256
`55cf42282c6322087800823cbe4f4957a8d7349a22f9d3eee56fa59157665856`
selects seven transitive source files, the already pinned Python runtime,45CPU/
90wall seconds,512MiB/two processes/1MiB logs. It runs nine new groups on real
in-memory SQLite tables with the same primary/unique indexes and synthetic
authenticated records. Both actual query implementations run against the same
fixture: ten anchor candidates, one old-cut positive, nine negatives, and a
later positive excluded by the old cut. Proposed assertions compare wire bytes
and exact positive identities, count object loads/proof attempts, challenge all
cutoff/resource/corruption boundaries and confirm Coverage remains separate.
This is a narrow metadata-algorithm discriminator, not a benchmark of huge
networks, mathematical verification or whole-agent speed. No actual result is
claimed before root's reviewed launch and independent outcome adoption.

### Candidate controls01 failure and integration pause

Root reports the actual first candidate run failed cleanly: three groups pass,
five errors and one failure; Job CPU0.8125s, wrapper0.28125s, wall1.91826s.
The repeated error is `CANDIDATE_CAS_NODE_MISSING` while traversing partition
nodes. Used01 source, selection, inputs and results remain unchanged. The scale
lane now diagnoses the new reader against existing Store implicit-node behavior;
this is not presumed to be a fixture-only issue.

Root had separately selected public candidate integration. Draft edits exist in
`search_session.py`, `http_provider.py` and `clients.py`: same-session candidate
route/method, conservative full scan charging, shared positive-record dedup and
separate advisory cursors. Those drafts are NOT reviewed or runtime-qualified;
no integration tests/API note/selection has been completed. At root's direction,
integration edits are paused until the isolated reader failure is fixed and
independently reviewed under a fresh exact selection. No previous allocation
is renewed. This lane has still launched no runtime.

### Controls02 source repair: materialize the fixture's committed partition tree

Reading the actual five traces, the old fixture, `A.partition_get`, and
`Store.admit/get_node` resolves the cause. `Fixture.seal` called the pure
`A.feature_root` hash calculation, followed by `A.map_set`, but never persisted
partition-leaf/partition-node records. The referenced nonempty partition roots
therefore did not exist in fixture CAS. Production Store admission uses
`A.partition_set`; both reader implementations fetch nonempty nodes while the
shared `A.partition_get` already handles implicit empty paths. The independent
reviewer reached the same diagnosis. There is no observed reason to change the
candidate reader or weaken missing-node refusal.

Only the mutable test fixture's `seal` now builds each feature's nonempty
partition paths with `A.partition_set`, asserts the resulting root equals the
independently computed `A.feature_root`, and then commits that root in the map.
No candidate algorithm, checking policy, expected test outcome or resource cap
changes. Candidate source remains SHA-256
`b5d87baa539ce734b95891ea7358db96f137b39520151fd05c8e8272efe2d639`.
The repaired test is
`7a829f98bc7f25361b1e27c1fd510fed83df811bb39f44e421502702ea7b9615`.

Fresh `candidate-query-controls-02-selection.json` SHA-256
`f2866c2b4c1e26f87636fa26f625aa1eb698a4ba3cc55bf1bef906be0aa66d61`
changes only run name and the repaired fixture pin relative to the retained01
selection; all other source/runtime pins and finite limits remain identical.
Root owns a new launch after independent review. This does not repair, reclassify
or erase the failed01 execution. Public integration remains paused/unqualified.

### Controls02 actual pass and public integration source readiness

Root reports controls02 PASS with all nine groups, Job CPU0.796875s,
wrapper0.265625s, wall1.2334623s and clean closure. Scale read the retained raw
`candidate-query-controls-02/command/stderr.txt`, which records all nine `ok`
and terminal `OK`. The candidate algorithm remains unchanged at
`b5d87baa539ce734b95891ea7358db96f137b39520151fd05c8e8272efe2d639`.
The earlier01 failure remains preserved and charged. Root separately requests
independent actual audit and explicitly resumes public integration source work.

The new public branch is now source-ready in `SearchSession.begin_candidates`,
`SearchClient.candidates` and `/v5/discovery/candidates`. It requires an existing
verified summary, derives the selected partition's same anchor, and reserves its
whole scan/match/byte allowances before I/O. Candidate requests consume the same
session request/page/provider/snapshot/deadline/in-flight ceilings as ordinary
pages. The provider reserves exactly `limits.bytes`, not1MiB, and clamps its
local request-copy timeout to the client's cap and remaining owner operation
window without changing the caller's request object. No candidate-query, Store,
commitment, ordinary wire schema, offer wire schema or custody changes occur.

Candidate completion charges the **full reserved scan allowance** against the
existing session `examined` budget in `_take`, before parsing/verification.
Invalid replies, timeout, expiry and abandonment cannot refund it; failure
handling skips a second scan charge. Successful verified hits consume the
ordinary candidate allowance including duplicates; failed/unknown replies
consume their reserved hit allowance. Actual raw bytes are charged before
decoding, unknown transport consumes the whole byte reservation, and provider
work counters never authorize refunds. `candidate_search.charged_scan_allowances`
makes the changed interpretation of aggregate `examined` explicit.

Positive verification calls the isolated candidate verifier with the owner's
deadline guard. It does not call `Coverage.accept`. Its cursor/termination is
stored only in `last_advisory`; original interval pages retain `last_verified`
and their existing exact Coverage semantics. Existing offers and explicit
summaries still pin snapshots as before. The ordinary page branch adds only
bounded post-verification dedup preparation before its existing coverage commit;
returned `matches` and successful interval costs retain their original meaning.

#### Avoiding first-provider metadata poisoning

The initial unpublished integration draft considered rejecting differing
RecordIDs for the same object ID. Review of the authority boundary exposed a
problem: authenticating an index record is not content acquisition/recomputation.
A malicious first provider could claim an honest object's ID with false metadata
and thereby suppress the honest later candidate in the same bounded session.
Root adopts exact `(object_id, RecordID)` dedup instead. Different committed
metadata claims remain separately charged alternatives. First-seen metadata is
not authority. The client exposes advisory `metadata_conflicts`, never suppresses
a new exact alternative, and keeps the ordinary within-snapshot Coverage
consistency checks unchanged.

Both page APIs return unchanged complete `matches`, plus bounded `new_matches`,
`duplicate_matches` and `metadata_conflicts`. The session stores only bounded
identity pairs/first-claim hints, not a new unbounded record corpus. Distinct
stored claims cannot exceed the charged candidate allowance; every duplicate
still consumes hit/byte/scan/request resources. `candidate_search` reports unique
verified committed-record claims, duplicates and alternative metadata counts;
none is mathematical acceptance or useful-growth evidence.

#### Documentation and exact proposed controls

`software/v5/transport/SEARCH-API.md` now documents namespace/query/contact entry,
offers, both page modes, aggregate limits, exact-claim dedup, typed refusals,
advisory continuation, provider connection ownership and remaining global-scale
limits. It explicitly labels the evolving source as not a completed release.

`candidate-session-controls-01-selection.json` SHA-256
`365f6640d384f49c6890c2678ab69860ba47cbe3eaf1a9010dc3ae508f3103e0`
selects16 source/document pins and18 runtime pins,45CPU/90wall seconds,512MiB,
two processes and1MiB logs. Its nine new groups cover mocked client offer to
candidate to ordinary page, no refund from a zero-work claim, malformed/proof/
assurance failure costs, private tickets and post-verification deadline, unknown
transport/HTTP failure, concurrent/cross-API budgets, independently constructed
poison-first/honest-second metadata, memory-stream wire reservation/time clamp,
and pre-dispatch refusal of unverified snapshots/unconfigured contacts/bad input.

These are changed public-boundary controls, not a repeat of the nine isolated
candidate groups, actual socket deployment or mathematical certification. The
source uses the repaired retained synthetic fixture; no claims are made about
huge-network routing or runtime performance. Source/selection review and root's
finite actual launch are still pending. No runtime was launched by this lane.

### Actual offer-to-candidates integration prepared, not launched

Root selected a source-only actual two-call successor to the retained ordinary
offer/page integration. New `transport/candidate_integration.py` SHA-256
`22a1caa12676d40fd6da6ce0cb0543a219c82b1af4ca9b93603bbf55be4d18a7`
uses a fresh copy of the same exact compact database (SHA-256
`0871e1957c05589f998879bbe553dec84aecd96e0726daae1c30b0c34d4d0fea`)
and retained base bundle. There is no index rebuild, native/proof/custody call,
repeated offer/page campaign or provider-loss campaign. Runtime remains root-owned.

The initially empty consumer knows only namespace/features and its approved
loopback contact. It calls public `offer`, chooses the first nonempty returned
partition, and calls public `candidates` using only the authenticated returned
SID/partition/anchor. The expected `CommonsV5.fusion` object and locator are
postconditions on the positive result, not query inputs or a hidden snapshot
plan. Production candidate verification must pass before that postcondition.

The harness stores sender wire-body requests separately from provider dispatch
requests: the provider may shorten its local timeout. It checks all other
request fields remain equal, actual request/reply/header accounting agrees,
full scanned32 is charged, one actual hit and its exact `(object_id, RecordID)`
claim are stored, no duplicate/conflicting metadata is invented, and every
reservation/task/socket is closed. Coverage is compared to its immediate
post-offer state; no candidate ordinal, termination or cursor can promote
verified coverage or `last_verified`. Only `last_advisory` changes.

Fresh selection `candidate-public-integration-01-selection.json` SHA-256
`b36def28096695bba3e637e94d79cb19fb1bc8cd275829edb14d88870e056654`
pins16 source files and20 runtime/input files,45CPU/90wall seconds,512MiB,
two processes and1MiB logs. Independent source/selection review was requested.
No actual outcome is claimed. Root separately owns `software/v5/admission/`;
this lane must not infer acceptance from a receipt JSON or structural custody.

## Next central seam: maintained provider location, not another query encoding

Source/theory recommendation to root; **not an implementation or runtime
selection**. Public offers remove the injected SnapshotID and positive-only
candidates remove nonmatch wire transmission. They still require injected
index contacts. A huge-network claim therefore needs a location mechanism and
an explicit condition that bounded work can reach a useful provider.

### Concrete retained implementation seams

Read-only inspection of frozen
`product-local/v4-library-commons-02/commons-v4/overlay/` establishes:

| Source and SHA-256 | Reusable behavior | Required v5 change |
|---|---|---|
| `library_overlay.mjs`, `9665273e0f5309197cc4e72fd3f125b5061284e99403f47b5ee4f436a3614b48` | Kademlia provider discovery; alpha3/disjoint paths3/k20; peer/address limits; query event caps; abort; owned maintenance; TTL/reprovide; replaceable bootstrap contacts. | New domain/protocol and service descriptor. Its fragment regex, bridge, namespace, find/get wire and per-call Python process are not v5 discovery. Do not transplant the whole bridge. |
| `intent_store.mjs`, `81bc08b7a2ea01fc0934cf3e3cbf38b00c3d4b8eb12673d6dcc795179e75e3b9` | Durable publish intent and atomic withdrawal. Queued renewal cannot reinsert the owner's provider record without still-live intent. | New versioned logical-key validation; its current regex permits only fragment/interface/type/constant keys and its provider prefix is hardcoded. |
| `quota_store.mjs`, `7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4` | Entry/value/logical-byte/provider-per-key/SQLite-page caps; restart census; transactional quota updates. | Separate v5 state/config/schema. Metadata caps are finite storage safety, not a guarantee a relevant provider survives saturation. |
| `address_policy.mjs`, `16eac626aea421380b089c34a16dd482141b534c36c832ca624767b12a6e3bc5` | Exact IPv4/TCP multiaddr policy, bounded peer suffix, no DNS/relay/address rewriting. | Retain the invariant, review reserved ranges against the chosen deployment profile, and separately validate the advertised HTTP endpoint. Do not infer that a Noise peer address is an HTTP address. |

### Recommended minimal new adapter

Keep the current Python offer/candidate/custody protocols. Add a small separate
Node/libp2p **location adapter**, using the retained pinned dependencies and
quota/intent invariants through an explicitly new source selection. It only
publishes/locates service hints and obtains bounded service descriptors; it does
not execute Python per search request, accept mathematics, or proxy module bytes.

Proposed logical route identity:

```text
RoutingKey = H("DMKN-V5-INDEX-RENDEZVOUS-V1\0",
               canonical({namespace, role:"formal-index-v1",
                          predicate:{all:[sorted unique FeatureIDs]}, stripe}))
```

The `all` field initially has one feature, or a separately selected bounded
conjunction actually materialized/served by the provider. It is not an arbitrary
subset catalogue:128 features have8,128 pairs and exponentially many subsets.
The routing identity and namespace are independent of a transient SnapshotID.
Exact snapshot-availability hints may later use a distinct role/domain; they
must not be confused with unknown-ID provider location or module custody.

An index owner selects which local supported predicates to advertise under
finite key/byte/renewal allowances. The hint says only "try this provider".
It does not prove that an index contains any matching record or that the owner
retains a promised snapshot. The receiver still calls the public offer and
verifies the selected summary before querying. A local advertisement check can
inspect indexed metadata without replaying mathematical dependencies, but that
local check does not make remote promises cryptographic truth.

The retained DHT returns peer IDs/multiaddresses, not v5 HTTP endpoints. Over
one short Noise-authenticated stream to a returned peer, request a separately
versioned descriptor containing namespace, supported role, and at most a small
fixed number of numeric-IP HTTPS endpoints with optional TLS server name.
The descriptor is advisory, bounded by wire/field counts and owner-local elapsed
time. Do not accept remote `ca_file`, filesystem paths, credentials, headers,
redirect rules, executable adapters or arbitrary URL schemes. TLS uses the
owner's trust configuration; a self-selected remote server name has no
mathematical authority or privileged administrative identity.

Before **each** dial, the owner applies its egress policy: declared public IPv4
mode with permitted ports/ranges, or an explicit local test allowlist. A remote
hint cannot enable loopback/private/link-local/multicast destinations, DNS
rebinding, redirects, or a remote CA file. Numeric address policy applies
independently to both DHT/Noise and HTTPS connections. A reachable public network
deployment is still a separately authorized operation; this proposal launches
nothing externally. Multiple bootstrap contacts are permitted; zero reachable
ones can mean local-only failure, not magical global discovery.

Why this adapter: it retains the actual bounded Python service and its exact
verified offer/candidate path, and avoids a new bulk transport/bridge or two
competing mathematical acceptance implementations. An alternative direct
libp2p byte-RPC is viable but would require a bounded persistent dispatch bridge
and another whole wire/accounting boundary. No evidence yet justifies replacing
the working HTTP path with that larger integration.

### Finite-workflow accounting is a required integration, not optional polish

One query owner must preallocate provider-location calls, DHT events, Noise
descriptor requests, endpoint attempts, reply bytes, retained hints and elapsed
time. The subsequent offer/candidate budget is a sub-allocation of that owner
workflow, not a new budget created each time routing finds another contact.
The location adapter must return charged actual/unknown-outcome costs and never
auto-retry. A cancelled/failed query keeps its spent allowances. Separate finite
service maintenance allowance funds publication/renewal/expiry/recovery; query
cost reports include the amortization model rather than declaring those free.

An explicit `WorkflowBudget` boundary is preferable to silently extending
`SearchSession.used.providers`: routing intermediates, discovered service peers
and contacted HTTP providers are different charged quantities. The existing
SearchSession remains the exact owner of offer/page/candidate reservations.
An adapter that merely hands unlimited contacts into repeated fresh sessions
would not close V5-S and must fail review. Saved hints are finite and expiring;
recent contact is not a verified latest/global state. Independent owner-issued
budget renewal is visible, never implicit in pagination or provider failover.

### What scalability claim is actually supportable

Let a predicate route cover P advertised providers, of which r can currently
serve at least one desired verified candidate. If B providers are selected
uniformly without replacement, the exact success probability is

`1 - choose(P-r,B)/choose(P,B)`, with the natural zero-binomial convention.

By the union bound this is at most `min(1,B*r/P)`. Consequently fixedB and a
single relevant provider do **not** give network-size-independent recall.
With independent uniform draws **with** replacement the exact probability is
`1-(1-r/P)^B`, again at most `min(1,B*r/P)`; repeated draws consume the budget
even if the contact is deduplicated afterward. Without replacement the earlier
binomial formula requires0<=B<=P. No randomness assumption means no such exact
success expression. In particular, an arbitrary/adversarial fixed selection
rule can repeatedly choose only irrelevant providers.
DHT membership proofs, compact summaries and fixed256 index partitions do not
alter this fact. With arbitrary adversarial hint selection the lower bound is
zero even when many honest providers exist. Neither uniform sampling nor
independence is promised by the retained Kademlia implementation.

A useful operating theorem needs named assumptions instead: some selected
selective routing predicate reaches a relevant serving set, the selected
routing path remains reachable, hint admission is not eclipsed/saturated beyond
the specified fault model, and the query budget can cover its required contacts.
If each of B independent trials reaches a usable provider with probability at
least p, success is at least `1-(1-p)^B`. This formula is conditional; correlated
replicas, churn, Sybils and route bias invalidate the independence premise.
Do not substitute provider count or several hosts for independent failure domains.
Independence can instead be replaced by the stronger directly stated adaptive
condition that, conditioned on **every reachable prior all-failure history**,
the next selected trial succeeds with probability at leastp. Multiplying the
conditional failure bounds then proves the same result. Merely observing an
unconditional average success ratep does not establish this adaptive condition.

More selective syntactic features, locally chosen conjunction keys and
replicated index scopes can increase p. Their advertisement, indexing, storage
and renewal costs belong in the growth model. Missing an unadvertised theorem
does not falsify mathematical correctness but does limit discovery coverage.
The software must report exhausted/incomplete scope instead of claiming absence.

Under ordinary well-connected balanced Kademlia assumptions, provider location
has expected logarithmic routing depth in network peers; source-enforced event,
time, fanout and result caps provide a hard finite refusal envelope even when
those assumptions fail. With a advertised keys/provider, replication k and
renewal period T, a rough routing-maintenance term is proportional to
`a*k*log(N)/T` per provider plus storage/connection churn. This is a model, not
a measured internet result; k, payloads, RPC counts and replicas must be charged.
Query wire has routing/descriptor work **plus**, not instead of, compact offer
metadata and selected positive proofs. No complete global body is downloaded.

Hot route keys remain a real load issue. Several explicitly domain-separated
stripes and finite provider samples can spread ordinary demand; a finite stripe
count does not create asymptotically unlimited capacity or stop an attacker
grinding peer identities. Selectivity, replication, admission quotas and visible
incompleteness are necessary. A dynamic authenticated global sharding directory
would be substantially different work and is not justified as the next slice.

### Small decisive next selection, if root adopts this recommendation

Source first: exact v5 logical keys/descriptor/egress schema and finite aggregate
workflow budget; then one narrow location adapter using retained dependency
pins and separate state. Do not edit frozen v4 or expand into a DHT rewrite.
Independent review challenges egress, timeout/failure charges, key separation,
intent-withdrawal races and stale/duplicate/saturated provider hints.

Only afterward, a fresh bounded actual scenario should start with namespace,
formal features and replaceable bootstrap peers, but **no index HTTP endpoint**.
It must locate a service, obtain an unknown-SID offer, verify a selected positive
candidate, and carry the exact result into root's separately owned admission
gate. Reuse the retained index and qualified unchanged mathematics rather than
rebuild or rerun proof campaigns. A separate small maintenance/withdrawal
scenario is justified only for the new changed hint lifetime boundary.

This closes a concrete missing public entry seam. It still must be integrated
with the stipulated selective-coverage and funded-service region before any
large-network useful-discovery or growth claim is accepted.

### Sustainable selective coverage is a capacity condition

For an explicit finite family of supported route predicatesj, let A_j be the
providers advertisingj, R_j the currently reachable providers holding a useful
candidate for the local demand, and E_j the provider-selection law after routing.
The consequential service quantity is `p_j = Pr_{E_j}[provider in R_j]`, not
the total world corpus size, a global theorem counter, or `|A_j|` alone. Query
and outcome distributions are evaluation/local-agent demand models; they do not
enter mathematical acceptance or become mandatory network research goals.

A source-compatible honest advertisement policy can retain a bounded local
positive witness for each advertised conjunction, obtained from existing B-tree
intersection, and withdraw/refrain from renewal when that serving scope is lost.
The actual witness and its module mathematical warrant remain separately checked
at retrieval/admission. Such a policy makes ordinary exact-feature matching
plausible; it neither proves the witness is useful for a particular agent nor
protects against dishonest advertisements or incomplete hint retention.

Let provideri select at most a_i route predicates, with maintenance workm_ij per
renewal and periodT_ij. If its sustainable maintenance capacity is M_i, require
`sum_j m_ij/T_ij < M_i` with an explicit reserve for churn/repair; query service
requires a separately funded arrival/work inequality. If a shard's offered
work exceeds its serving capacity, queues/latency or refusal grow. More replicas
can reduce per-replica query pressure but increase write/renewal/storage costs;
neither finite quotas nor branching processes evade that tradeoff.

Choose selective conjunctions by bounded observed demand and served-witness
availability, with explicit admission/eviction policy; do not advertise every
possible conjunction. Coverage is then scoped to those maintained predicates.
For a supported demand distributionw_j and B_j tries, a justified retrieval
term is `sum_j w_j * success_j(B_j)` only under the stated selection/reachability
model. Uncovered predicates contribute zero lower-bound success, not an assumed
future index. This term can feed the root-owned full-cost growth comparison.

Thus a favorable huge-network region is possible without a global corpus scan:
selective advertised scopes keep usable-provider probability bounded away from
zero for covered demands, bounded routing locates those scopes under its
reachability model, and independently funded maintenance/query/custody/admission
capacity stays ahead of the relevant load. Each premise is observable or a
declared model assumption. None is established by a tiny loopback test alone.

### Actual candidate integration outcome received

Root's selected `candidate-public-integration-01` completed PASS with clean
closure: Job0.78125CPU seconds plus wrapper0.28125, wall1.7538827seconds.
Scale read retained `evidence/RESULT.json`: exactly two calls,877 request-body
bytes,6,305 reply-body bytes,453 combined HTTP header bytes; one exact
`CommonsV5.fusion` committed record; full scanned32 charged; candidate state
contains one pair, no duplicates/conflicts; coverage unchanged and last_verified
empty. Dispatch timeout remained1000ms. No index rebuild, guest, proof or
mathematical acceptance. Candidate-session-controls01 stderr separately records
nine tests/OK, and assurance records its independent actual PASS.

Candidate-public independent actual review is pending at this checkpoint; raw
PASS is not substituted for that audit. Used harness/selection/source snapshot
and both runs stay frozen. Root now selects this maintained-location design
investigation source-only, with no adapter code or routing campaign yet.

## Selected location boundary: first source slice ready, not runtime-qualified

Root read/adopts the maintained-location seam and selects disjoint
`software/v5/location/` implementation: exact route keys, strict service
descriptor/owner egress and aggregate workflow accounting first. No runtime or
large routing campaign is selected. Reviewer finds no architectural blocker in
the probability/capacity model, and independently adopts actual candidate HTTP01
PASS. That run and its evidence remain unchanged.

New `protocol.py` provides the route digest above and exact bounded descriptor
schema. The first PeerID profile is canonical Base58 identity-multihash Ed25519
(the retained overlay's generated key kind), not arbitrary labels. Peer syntax
does not verify a signature: the future adopted Noise adapter must supply the
actual authenticated channel peer, separately from a reply's self-claimed field.
The private descriptor ticket binds peer, namespace, role, route key, random
nonce, maximum body bytes and an owner-local absolute expiry. Exact fields,
canonical JSON, endpoint count, query/channel bindings and assurance are checked.

OwnerEgressPolicy copies an owner configuration with one explicit public or
loopback-test mode. Public mode needs numeric globally routable nonreserved
IPv4, an owner-listed port and TLS; optional SNI names are strict lowercase DNS
A-label syntax. Loopback tests allow only listed exact127.0.0.1ports. Peer
multiaddresses are direct IPv4/TCP only, with exact optional Ed25519 PeerID
suffix binding; learned DHT/Noise addresses must later use this same policy at
the actual connection gate. No remote CA path, URL, redirect, header, credential
or executable field exists. The selected policy is fixed system-CA-only;
reviewer agrees no new pinned-root-set seam is needed for this advisory slice.
OS trust-store updates remain owner-environment assumptions, not reproducibility
or proof of a Noise-peer/HTTPS-operator identity relationship.

`WorkflowBudget` immediately charges full route event/peer-slot allowances on
ticket issuance. Failure, malformed/duplicate peers and abandonment cannot
refund them. Descriptor requests charge attempts and request-body bytes at
issuance; raw reply bytes charge before validation; unknown outcomes consume
the whole private reservation. Retained peer/key pairs and contacts are bounded
by those charged allowances. Duplicate descriptors still consume requests/bytes.
Different endpoints cannot silently exceed the selected contact cap.

The whole SearchSession reply allocation is prepaid at workflow construction:
`descriptor_used + descriptor_pending + search_allocated <= workflow_reply_cap`
for compliant bounded transport. A detected oversized response marks
TRANSPORT_BYTE_VIOLATION and records actual bytes, rather than pretending that
inequality survived a broken transport. Routing events are NOT counted as reply
bytes. Exactly one SearchSession/SearchClient can be issued, with its deadline
clamped to the original workflow deadline; referrals/failed contacts cannot
create another. Each HTTP `_send` rechecks adopted endpoint equality, egress and
contact expiry. Predial refusal occurs after ordinary method reservation and
conservatively settles that ticket. Actual HTTP activity is still separately
reported, so this reservation charge is not mistaken for measured wire traffic.

Read-only retained dependency inspection found a crucial limit: Kademlia
`network.js` uses `pbStream(stream)` defaults, while inbound RPC can read
multiple messages. Query `onProgress` events do **not** bound all DHT/network
bytes or background identify/Noise/maintenance. Reports explicitly set
`dht_wire_bytes=null` and `NOT_MEASURED_OR_BOUNDED_BY_QUERY_EVENTS`. The future
adapter must retain finite process/time/connection/event/storage containment;
additional wire accounting cannot be inferred from event caps. Root was informed.

`test_location.py` prepares12 focused groups, with mocked HTTP only, targeting
the exact new seams and shared SearchSession behavior. No DHT, socket, native
or cryptographic proof operation is repeated. Source/selection were sent for
independent review; root alone may launch a reviewed finite run.

| New source | SHA-256 |
|---|---|
| protocol.py | `cb336e51339b31db9510e93576b9a4fea368396a95dee11cdf4b839be00c22a1` |
| workflow.py | `0e0eafd11ff601ac069aa95e5b9de3608f3d77c7f9864cf5709d900d4c25c57e` |
| test_location.py | `0b6ffede549bf244296be8fd8b9373f6c6bc10d025881ad92e2a2b7ff4bf04b4` |

`location-contracts-01-selection.json` SHA-256
`73d40d59e3555fd8d23a694d098d86b5303df7e180ebf6f5f1f71cd51124d116`
pins16 source/doc and18 runtime files,45CPU/90wall seconds,512MiB,two processes
and1MiB logs. No actual test pass is claimed yet. Existing discovery/transport
production and root-owned admission sources stay unchanged by this selection.

### Python location actual result and Node maintained-source preparation

Root reports `location-contracts-01` actual12/12PASS with clean closure,
0.640625Job +0.3125wrapper CPU seconds,1.3072217wall seconds; independent actual
review was requested. This is the native-free/mocked boundary, not a DHT run.
Used Python source and exact selection remain unchanged. Root explicitly
continues Node source preparation, not runtime.

`software/v5/location/ADAPTER-PLAN.md` now records a concrete retained runtime,
protocol, quota/intent, maintained service and later controller source map.
It distinguishes returned provider slots from intermediate routing events,
outbound destination-port policy from inbound ephemeral source ports, v5
namespace-in-key/global-location DHT from the old namespace-specific fragment
overlay, and the still-unbounded retained protobuf-message seam. All14fixed
runtime import paths were checked to exist beneath the frozen overlay. No
dependency was installed, changed or loaded for execution by this lane.

New source-only Node files now implement the planned location branch:

| Node source | SHA-256 at source-review handoff |
|---|---|
| protocol.mjs | `6c9b0742d0ab72f7490c4c128b4d3636a098ddc99150407a78090dbd2502934c` |
| framing.mjs | `689d1336d8d5aadd3f7068208605dc0abb6d1e01ea72e8d3b9b2b1592ed929a5` |
| intent.mjs | `c366ec0854d20f4a1e5f1dd0f0e1e9464967f5d7f7d87be49d1d54271c91e58c` |
| runtime.mjs | `d7ba51000d2860856a0fa52b7757bf9a65080aed77a10c1e9bdab21d898c7380` |
| maintained.mjs | `98829a3d40b40e581fa1a374864b41b0f3aacee13785b29ffee8cf2b16f99e0c` |

The maintained service uses new DHT/descriptor protocols, exact route-key CIDs,
fresh adopted state/config and Ed25519 identity, same owner egress at learned-
address mapping and actual outbound gates, finite descriptor service caps,
bounded returned-peer cache, maintained hint TTL/reprovide and durable intent
withdrawal. Its loader fixes local module names/paths but intentionally does
not pretend path validation authenticates the full runtime: root's launch must
pin every transitive dependency and retained vendor patch. No old fragment
bridge or module/certificate payload path is imported into this service.

Descriptor streams use one bounded prefix/body/EOF request and reply, scoped
to2048/4096bytes; measured/queued application framing is not mislabeled TCP or
DHT bytes. Shared start/stop promises make every stop caller await the same
cleanup and avoid closing before asynchronous startup creates its node/store.
Hard external process/memory/wall containment remains necessary. Source review
was requested; focused Node controls and exact launch selection remain pending.

The remaining controller integration is central: Python monotonic absolute
`until` cannot be compared with Node performance.now. An adopted controller must
refresh private remaining allowance immediately before IPC, account transit
elapsed, enforce the original outer deadline and settle unknown outcomes. A
relative duration captured long before dispatch must not renew the workflow.
This is not yet an actual authenticated descriptor-to-WorkflowBudget path.

Root also confirms the retained compact discovery DB uses the old conditional
policy, whereas current receipts use the new policy. All existing discovery
tests correctly remain metadata-only. Genuine certified integration requires
fresh new-policy module export records/index once, not relabeling that DB or
conflating its namespace with current certificates. Generic transport/location
code remains reusable; root owns fresh input selection and admission integration.

### Aggregate transport and cancellation boundary, source only

Independent review confirmed two concrete problems in the initial Node slice:
failed descriptor frames were missing from observed request bytes, and throwing
from every DHT progress hook could recur inside query terminal listeners. The
handler now settles `reader.received` in finally, including truncated frames,
and explicitly labels pre-reader traffic outside that application counter.
The operation now owns an AbortController; only DHT query progress consumes its
event allowance. Predispatch dial/send refusal throws, while path-ended/error
notifications never throw into Queue listeners. The already-aborted TCP-open
hook refuses before net.connect, avoiding its abort-listener-registration seam.

Root selected service-wide transport/ingress limits as central, not optional.
New `transport.mjs` uses retained TCP instance/upgrader seams without editing
any frozen dependency: cumulative outbound attempts (including failed connects),
inbound upgrade admissions, raw receive forwarding and prebuffer raw send
admissions. The source argument depends on the pinned constructor invoking the
upgrader synchronously before raw data callbacks and its dynamic `this.onData`
lookup. The wrapper checks empty raw buffers before installation. Counters are
shared across foreground and background service work; unknown/failed outgoing
work does not refund admissions. Overflow aborts raw connections, closes
listeners and schedules orderly service stop. No new budget is issued.

The honest scope is `received-forwarded <= R`, `send-admitted <= S`, and bounded
admitted connection attempts/upgrades, not packet/kernel bandwidth or all raw
socket allocation. Observed/refused incoming chunks may exceed R and are kept
separate. Pre-upgrade incoming allocation, TCP/IP overhead, kernel buffering,
decoder resource amplification and hostile-flood availability still require
external finite process/memory/wall containment or further selected controls.
The DHT protobuf framing still has no separate per-message length policy.

Thirteen focused Node groups now include actual retained raw-TCP callbacks,
TCP dial/upgrader methods with fake sockets, and actual Network dispatch hooks
with mocked RPC; SQLite, descriptor failures, route syntax, egress and startup
cancellation remain covered. No real socket/DHT/proof operation is performed.
These are source preparations, not execution passes. The earlier Node hashes
above are superseded only for changed unused source; Python controls and all
used predecessor inputs/evidence remain unchanged.

Root separately selected source-only manifest-verifying launch harness
`location/run_node_controls.mjs`. Read-only census found5,894 overlay files,
37,682,183bytes; these plus bundled Node executable/license can be fully pinned
without checking unrelated Lean/prover assets. The harness verifies the exact
manifest SHA and vendor-patch SHA, complete selected subtree census and contents
before/after imports, restricts resolution to manifested runtime/snapshotted
source/builtins, and verifies snapshots. Verification/control CPU stays inside
one selected Job; its reported breakdown is not summed again. Exact selection
and independent review follow; root retains every launch and adoption decision.

### Node controls01 actual failure and finite continuation02

Root launched independently cleared selection01
`141b3a17d37762b7f487e7743a4418424d6dfd670a6d87d81d8e1c413cfb3dc7`.
It failed after seven passing groups: the eighth mock-routing test called actual
status on a fake node missing `getMultiaddrs`. Production status behavior is not
weakened. Full dependency postverification passed, clean closure; root reports
13.34375Job +1.09375wrapper CPU seconds,112.66557wall seconds, with104seconds
cold prehash and5.55seconds posthash. This result/source is used and frozen.

Root selects only the unfinished six groups in new `test_location_node02.mjs`:
add the missing empty-address fixture method and skip the seven already-passed
group bodies, preserving required fresh setup. New `run_node_controls02.mjs`
changes only its self/test entry names. All production source and runtime remain
unchanged. Source-only selection02 SHA
`f7c5107c885b70d92bc2056afc1656e6010f0e53ba8c194784c855066974d1b2`
retains60CPU/180wall/512MiB/two-process/1MiBlog caps; independent review was
requested. No run02 result is yet claimed and no launch was made by this lane.

Root now also selects new source-only Python controller/private Node IPC,
cross-language vectors and one later bootstrap-to-Noise-to-same-workflow HTTP
integration. No endpoint is to be injected into the SearchClient: only the
verified advisory descriptor populates it. Original outer deadlines/tickets
must be conserved; failures settle fully and cannot refresh capacity. The old
retained index can still support only metadata discovery, not current-policy
mathematical receipt acceptance. Before a real socket scenario, a new narrow
runtime-composition wrapper will combine service cancellation with each caller
signal before retained TCP `_connect`, so pending raw connections do not depend
solely on asynchronous node.stop/connection-manager shutdown. Used production
files remain frozen; this is a separate successor seam, not an in-place repair.

### Controller/source successor and actual changed-seam controls

Location Node continuation02 passed and its independent actual audit is adopted:
six remaining groups, seven explicit skips, exact5,896runtime-file pre/post
verification,6.21875Job +0.46875wrapper CPU seconds,6.738182wall seconds, clean
closure. Actual result SHA
`1779c5c03b93a2db98a66d8d944084520c86b0c31d8692c836e9d4b4aeb6fd74`.
The first seven passing01groups plus remaining six02groups support thirteen
scoped controls;01remains FAILED and is not relabeled. No real network follows.

Root selected new `controller.py`, `node_entry.mjs`, `ipc_wire.mjs` and
`composition.mjs`, documented by `CONTROLLER-PLAN.md`. The composition merges
service cancellation with each caller signal before retained TCP dial. The
controller creates and owns private pipes, exact source/runtime adoption,
finite frame/count/byte scope and original absolute work deadline. Its wrapper
owns WorkflowBudget ticket creation; only an actual adopted child reply can
supply authenticated_peer. Python descriptor expiry stays private; Node gets
only a tightened relative duration and unused zero `until` sentinel. No endpoint
is injected into the eventual SearchClient.

Independent source review found a startup/close race: the first code could close
before asynchronous process creation returned its handle. Before execution this
was repaired using shared spawn/start/close tasks, shielded ownership of the
pending creation, late-child kill and joining/reaping before successful close.
Lock acquisition now uses the original deadline. A separate fixed six-second
aggregate teardown budget performs no new commands; posthash stays inside the
parent Job. `closed` means new work refused, not independently proved reaping;
successful closure plus actual process returncode is required. Reply counters
explicitly cover consumed bytes/EOF partials, not unread timeout-buffered OS-pipe
arrivals. Independent source review accepted these distinctions.

The new `test_controller.py`/`controller_controls.mjs` prepare seven mock Python
lifecycle/ticket controls and one actual source/builtin-only Node child. That
child checks three exact Python/Node route/request vectors, twelve critical IPv4
boundary/exception vectors, a Node descriptor reverified by Python, IPC bounds/
sequence/cancellation and service-signal composition on a mocked pending dial.
It loads no libp2p runtime dependencies and opens no socket. A scheduling-sensitive
close-before-core fixture was repaired before launch with an explicit barrier;
production behavior was not weakened. Final selection01SHA
`ef683441fdbb22fd6c2aa86dcb2db57c6310d60eb454299aa7d8629ca39fff4d`
pins28source and19runtime files,30CPU/60wall/512MiB/three-process caps.

Root reports actual PASS with clean closure:0.765625Job +0.40625wrapper CPU,
2.3283583wall seconds, three total processes; independent actual review is
pending at this checkpoint. All selected source is now used/frozen. Full actual
controller startup/import/runtime verification and Noise routing remain to be
tested. Mock verification in race controls is not an actual manifest-adoption
pass.

Root's next real integration selection permits an unused/nonadvertised consumer
endpoint placeholder only if runtime enforces no consumer publication. The
current frozen config requires1..4endpoints even on a consumer and still exposes
publish through its private owner pipe. It has durable intent guards against
unintended/queued self publication, but no explicit reader-only role. Scale has
reported this distinction and proposed an explicit narrow reader/provider role
successor if the stronger no-publication requirement is intended. Do not insert
the real index endpoint into consumer config or claim a role restriction which
the runtime does not implement. Root retains the direction/launch decision.

### Adopted controller result and selected explicit role successor

The independent actual controller review is now adopted. The seven lifecycle/
ticket controls use mocked spawning/runtime hashing; the one actual Node child
checks three cross-language route/request vectors, twelve selected IPv4 cases,
descriptor verification, IPC and cancellation composition using source/builtins
only. Actual PASS,0.765625Job +0.40625wrapper CPU,2.3283583wall seconds, clean
closure. Outer result SHA256
`d8b2c76044f0da9d7e8981422a012175522d9cf9781f53d0d21cfece77bc67aa`;
inner SHA256 `741614db38006e81b2bc7e995699ae48f7509de365403d5823d0134329c3b6e8`.
Preserved stderr1866B includes Python3.14's shield callback warning for the
deliberately refused startup future after mock caller cancellation. Independent
review found no unreaped child. Do not rerun or suppress it for cosmetic cleanup.
All used controller source and evidence are frozen.

Root rejects a fabricated reader endpoint and selects a narrow explicit role
successor. New `maintained_roles.mjs` changes only the configuration schema/role,
reader zero/provider1..4endpoint rule, pre-command reader publish/withdraw
refusal, no reader descriptor handler/serving and reported role. Its DHT,
transport, budgets, metadata and lifetime mechanics remain unchanged.
`role_composition.mjs` changes the maintained import only;
`node_entry_roles.mjs` adds the three role source pins and role import only.
`controller_roles.py` preserves the frozen lifecycle through inheritance, adding
three exact source pins, role-aware entry/map and exact READY-role verification.
The independently reviewed role source has no identified lifecycle/budget
weakening. **Reader means non-index-provider, not a zero-service/lightweight
client:** it still has a listener and DHT `clientMode:false`, so participates in
routing and incurs background service work.

New `role_controls.mjs` covers zero/nonzero role endpoint constraints, early
publish/withdraw/serve refusal without spending counters, and actual startup
handler registration with explicit runtime/store mocks: reader registers none,
provider registers the descriptor protocol. It loads no retained dependencies
and opens no socket. Mock identities/state are explicitly mock evidence, not
cryptographic key-generation or SQLite qualification.

### Actual location-to-index integration prepared, not launched by this lane

Fresh `location_integration.py` copies retained compact-index bytes, starts one
finite HTTP provider and two separate role-aware Node processes, bootstraps the
reader to the actual provider PeerID, publishes one exact feature route, then
uses actual DHT location and a Noise descriptor to populate one WorkflowBudget.
Its only SearchClient comes from that workflow; it has no preseeded HTTP contact.
The same client makes unknown-SnapshotID offer then positive-candidate calls.
The exact fusion candidate is an output assertion, never a planning input.

This is an owner-authorized **loopback** test: its egress allowlist necessarily
contains the selected HTTP and DHT ports before location. No claim that the port
was wholly unknown is made. The meaningful integration invariant is that the
client starts with zero contacts and obtains its selected endpoint exclusively
through an actually authenticated descriptor accepted by the same workflow.
The reader has zero configured advertised endpoints and no publish authority;
fresh reader SQLite must have no `/application/published/` or
`/application/provider-intent/` entries. Reader DHT rows for remote peers are
not local publication intent.

The source requires real publication status ADVERTISED_HINT, actual connected
bootstrap, provider discovery, descriptor contact, unchanged exact returned
candidate and two HTTP calls. It closes every child even if another close
fails, preserves cleanup failures, verifies all selected runtime/source before
and after, requires zero-exit/no-forced-termination, and rechecks retained input
pins. External parent Job remains the hard containment boundary. One earlier
sequential pure role child plus the Python/two-Node integration fits the
proposed three-active-process cap. No broad old control group is repeated.

Prepared selection:
`experiments/v5-local-checks/location-public-integration-01-selection.json`,
SHA256 `6719492c48ff4ed71fadb4fb105b8043905ebf96f0afde7b5586bf35bb096606`.
It pins35source/21direct runtime-input files, proposes60CPU/240wall seconds,
1024MiB and three active processes, with explicit39171/39172loopback DHT ports.
Full retained5896-file Node subtree verification stays inside the parent Job;
direct pins are not mistaken for the complete import closure. Root owns final
selection/launch; independent harness/selection review is pending at this note.

All records remain **old-policy metadata-only**. The retained policy
`b49e45c0bde61982e9faa6cbeca7ea0619a33b85fee5579412b45301d95bea2c`
is not the current receipt policy
`5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377`.
No current certificate acceptance, independently hosted deployment, huge-network
recall or V5-S completion follows from this scenario even if it passes.

### Big-picture scale obligations: reuse the existing argument

The substantive scale model is already above, under **What scalability claim
is actually supportable** and **Sustainable selective coverage is a capacity
condition**. It states finite sampling limits; the needed adaptive conditional
success lower bound; no promised uniform DHT sampling; supported exact route
vocabularies; selectivity; funded routing/maintenance/query/custody capacity; and
zero lower-bound coverage for unsupported demand. This is a nonempty conditional
success region, not a blanket success assertion for arbitrary huge corpora.
`DISCOVERY-CONTRACT.md`, **Immutable index structure and hot-key partitions**,
its resource discussion and **Network and custody separation** give the
candidate/index-side costs and hot-prefix limitations. The frozen predecessor
`research/cycles/v4-2026-10-06-resumed/SCALING-CONTRACT.md`, **Routing locality and
its nonempty favorable regime** and **Renewals and admission cannot outrun
service**, supplies retained bucket coverage and renewal-margin premises.
No duplicate theory or new global completeness claim is needed here.

An actual endpoint-discovery pass would close one required implementation seam.
It would not establish that maintained advertised scopes actually cover a useful
demand distribution, that offered load stays below serving capacity, or that
discovered current-policy mathematics can be admitted/reused/returned. Root
keeps these as central release obligations alongside the full-cost growth path.

Independent reviewer subsequently cleared exact selection6719492c: all35source
and21runtime-input pins match, output absent, changed role controls and actual
integration harness reviewed. The correct intent prefix, independent cleanup
attempts, owner egress-only port preauthorization and metadata/certificate
distinction were accepted. Root has been informed; this is launch clearance,
not an actual runtime result.

### Actual location01 failed before provider READY; source diagnosis

Root launched exact selection6719492c once, session13592, and reaped it.
Actual outcome is FAILED, not an endpoint-discovery pass:19.15625Job +1.015625
wrapper CPU seconds,118.6758416wall seconds, clean process closure. Four pure
role groups passed, including mocked registration. Provider state reached fresh
identity/config/SQLite creation, but the provider exited1 before any IPC frame;
reader never started and no HTTP request occurred. All full5896runtime-file
pre/post checks passed. Cold preverification consumed105.9572299wall seconds;
postverification8.5554732seconds. No cap renewal is inferred from slow hashing.

The driver retained only the2793-byte childstderr count, not its bytes. The
actual4092-byte outerstderr therefore establishes EOF before READY but cannot
establish the lost Node error text. This is an evidence-capture defect to fix
in a fresh harness, never by filling in fabricated historical diagnostics.
All used source/evidence stays frozen; passed role groups need not run again.

Source inspection identifies a deterministic startup blocker: retained
`@libp2p/kad-dht/dist/src/kad-dht.js` declares both `@libp2p/identify` and
`@libp2p/ping` as service dependencies. `libp2p/dist/src/libp2p.js` checks these
after construction. V5's `maintained_roles.mjs` supplies identify and dht only,
and `runtime.mjs` does not import ping. No configured component supplies the
missing capability. The frozen working v4 `overlay02.mjs` explicitly supplies
`ping:ping()`. This configuration must refuse at the adopted library's dependency
check; that fact is distinct from claiming an observed lost error message.
Independent reviewer agrees with the source diagnosis.

Recommended smallest fresh successor: add the already retained, manifest-pinned
ping service through a narrow composition/entry seam without editing the used
maintained or vendor source; save bounded captured childstderr on all closure
paths; omit the four already-passed role groups in continuation. Retain all
egress, transport/service/deadline limits and original mathematical boundaries.
Ping traffic remains inside the same aggregate transport/service budget, not an
unaccounted background exemption. Root owns exact successor selection/launch.
Receipt transport inventory is paused until this actual core path works.

### Source-prepared Ping continuation02, pending independent clearance

Root selected the narrow missing-service repair, no cap increase or dependency
installation. `services_composition.mjs` calls the original fixed runtime loader,
loads only retained `@libp2p/ping/dist/src/index.js` under the same complete
manifest and import confinement, then wraps createLibp2p to require the existing
exact identify/dht service map and add Ping before DHT. Ping uses at most5000ms
(or the smaller configured operation time),4inbound/8outbound streams; original
muxer, owner egress, aggregate raw-transport, service lifetime and parent Job
remain in force. It supplies the capability instead of suppressing the adopted
library's mandatory dependency check.

`node_entry_services.mjs` changes only the exact source-name map and imports
the new composition's runtime/locator functions. `controller_services.py` copies
the reviewed role-aware launch core with five extra pins instead of three and
the selected entry name; frozen base lifecycle/commands/ticket methods remain
inherited. No used maintained/role/vendor source is edited.

`location_integration02.py` runs the previously uncompleted actual path, without
the four passed role controls. It cites the preserved actual inner result
`3793693abf785a1a596ae57b3424cae769d63accb6189b68670df077b4b55dcd`.
After each owned child close attempt it persists bounded captured stderr,
including failed-start/failed-close cases, before final cleanup/report checks.
The bound69632B is the inherited65536Bthreshold plus one at-most4096Bchunk;
this is captured owned output, not a fabricated historical failure log.

Prepared selection02:
`experiments/v5-local-checks/location-public-integration-02-selection.json`,
SHA256 `86337227efea517ec85e0a0476edc391fbd97c15569b80817af76c6f19722fc7`.
36source/21runtime-input pins, same60CPU/240wall/1024MiB/three-active-process
caps and39171/39172ports. Readback matches every source pin and output is absent.
Reviewer/root have the exact selection. No new runtime was launched by this lane.

Paused receipt inventory has one consequential finding: current HTTP globals
and JSON-only headers/acquisition parsing cannot safely acquire opaque receipts
by merely registering a route or subclassing Provider. A small explicit binary-
response successor is needed, preserving the existing JSON group/body/index
paths; never monkeypatch frozen route globals. Public receipt scheme/profile
identity must bind journal profile2, adopted image/foundation/policy, not the
machine-local ReceiptVerifier profile identifier (which includes local runtime
paths). Receipt custody is digest-keyed bytes plus bounded unverified offers;
local same-call verification alone grants a live mathematical handle. This
inventory is not implementation selection and remains lower priority than the
unfinished actual location path.

Independent reviewer clears source/exact selection02(86337227): all36source/
21runtime-input pins match, output absent, required DHT Ping declaration and
retained Ping limits checked. The new composition does not weaken lifecycle,
budget or import confinement. Stderr preservation and reuse of the four adopted
role controls are accepted. Root alone selects/launches the cleared continuation.

### Actual location02 PASS, independently adopted

Root launched exact86337227continuation once under session18825 and reaped it.
Independent reviewer read/rehashed the actual source/input/runtime/result set
and adopts the scoped PASS. Outer result SHA256
`a07f9ff5ff561d8d9e794d70169649a36d88f12be1ae3589435930d071d59ca3`;
inner result SHA256
`42460634513a3aa39170948764f97862bb18a6c4aadb95bd1e6e88a82b03525c`.
Costs:28.890625Job +0.5625wrapper CPU seconds,33.2744171wall, zero outerstderr,
zero-exit and clean closure. The four complete5896-file runtime checks consume
25.890625CPU **inside** the Job total, not an additional charge. No role-control
group or frozen proof/index campaign was repeated.

Actual path: zero preseeded search contacts -> connected bootstrap -> DHT provider
location -> Noise descriptor -> same WorkflowBudget/SearchSession -> unknown-SID
offer -> one exact retained fusion candidate. Reader publication/intent rows0;
no index rebuild and no mathematical acceptance. Owner egress preauthorized the
loopback ports; the descriptor, not a preseeded SearchClient map, supplied the
actual contact. Retained metadata policy remains the old policy.

The provider admitted8query events; reader admitted6, returned1provider, served
zero descriptors and made only its locate/descriptor commands before status/
stop. Workflow conservatively charged its full256routing-event/4provider-slot
reservation,1descriptor request and542reply-body bytes (493request body bytes;
provider observed497framed request bytes). There is no reserved/pending request
left. Search made2HTTP calls:877request-body,6305reply-body and453combined header
bytes,1candidate,32charged scan slots, empty verified-cursor map. No scan coverage
was promoted. Final subsearch status expires during post-close runtime hashing;
no operation occurred after expiry, and the original workflow still had about
27seconds left. This is not a reason to renew or rerun the search.

Node raw transport counts agree across the two ends: provider receive3168/send3522
and reader receive3522/send3168 bytes, no refusals/exhaustion. These are admitted
raw stream bytes including service work, not packet/kernel bandwidth. Reader
made1outbound attempt; provider admitted1inbound upgrade. Preserved852/853-byte
owned stderr files contain IPC_CLOSED summaries with0active connections. Both
Node exit codes are0, no forced termination or failed channels. All runtime
pre/post bindings pass. This closes actual endpoint-discovery integration only;
not huge-network recall, independent-host evidence or current-policy admission.

Root next requested a source-only minimal receipt seam. Its complete proposed
contract is `software/v5/transport/RECEIPT-ACQUISITION-PLAN.md`: exact raw-digest
receipt custody and bounded unverified offers; owner-created public wire profile
distinct from machine-local admission ID; two static read-only JSON-offer/binary-
blob routes; one explicit aggregate/deadline composition; actual same-call
verification and cold re-verification of retained bytes. Existing JSON groups/
bodies/search and verified mathematical relation stay unchanged. No source
implementation is selected by the proposal. Positive integration needs genuine
current-image receipt and fresh current-policy export/index records, not another
old-policy metadata run. Root retains the next implementation decision.

## D18 selected receipt source and focused control preparation

Root subsequently selected source implementation, with no runtime renewal.
New unused sources are `custody/receipt_store.py`,
`transport/http_provider_receipts.py` and `transport/receipt_client.py` under
`software/v5`. All used predecessor providers, clients, custody, admission,
location and evidence remain unchanged. The first reviewer source read finds
no immediate false-acceptance path; exact controls/selection review is pending.

The store implements raw SHA-256 keyed opaque receipt bytes and bounded
unverified `(ModuleID,WireProfileID,ReceiptSHA256)` offers, with exact owner
profile, per-blob/local/global quotas, SQLite FULL synchronization, atomic local
put, precommit deadline and content-authenticating readback. It never parses a
receipt or persists mathematical authority. Duplicate bytes coalesce and
different certificates/ModuleID associations are permitted without consensus.

The narrow provider successor adds two static routes only: bounded canonical
JSON receipt offers and exact-length raw `application/octet-stream` blobs. It
retains old JSON paths, TLS/egress assumptions and the same provider-wide
requests/concurrency/reply reservation accounting. No old module global is
monkeypatched. Receipt requests additionally require canonical JSON encoding.

The client composes structural group/body acquisition with offers/blobs under
one serial attempt/reply ledger and original monotonic deadline. Unknown HTTP
outcomes retain their complete selected byte allowance. Unknown request/header
exposure is separately upper-bounded, never mislabeled measured payload.
Earlier search/location work may be prepaid before local dispatch; this is an
owner-enforced suballocation contract, not a proof that arbitrary external code
obeyed it. Integration must pass the same original deadline and retain actual
phase accounting. Outer Job CPU/memory bounds remain necessary.

Only an exact owner-created `DeadlineReceiptVerifier` can admit. Its original
deadline is initialized before the inherited constructor, so adoption hashing
checks it too. All inherited real verifier, install, evidence and private-handle
checks remain. Separate ModuleStore/ReceiptStore commits are explicitly not
atomic together; partial state is incomplete. Whole selected custody requires
each demanded component durably committed and reauthenticated before and after
actual verification. A late/failing final check revokes the verifier's handles.
Cold store reopening grants no authority and needs genuine receipt verification.

At root's challenge, profile fields were corrected from misleading ABI names
to exact `retained_*_rlib_sha256` and `retained_dependency_manifest_sha256` names.
These pin the adopted implementation selection and provenance, not portability
of independent builds. Normative fixint/little-endian/no-trailing/64MiB rules,
exact Receipt type and verification context are explicit. Current source hashes
identify only this retained compatibility profile; a new implementation requires
separate schema/parameter conformance and owner adoption. No local admission ID
or machine path is sent on the wire. LINK-INPUTS provenance hash was read back as
`ced49032a348d1784cee327d5a3368e8f942335210854e403053d289b06b5e0a`.

Focused harness `transport/test_receipt_contract.py` has eight fresh groups:
store/coalescing/reopen/corruption/profile; atomic quota/deadline refusal; actual
binary + old JSON group/body transfer and supplier-offline selected custody;
partial separate-store failure; six binary framing/digest failures; shared
provider quota; offer/owner-profile refusal; original deadline/reservations and
no refund. All fixture bytes explicitly say NOT A RISC ZERO RECEIPT. No genuine
positive, wrong-module-valid-receipt or actual verifier adoption is claimed.
The latter remain current-image receipt integration obligations.

Prepared exact selection:
`experiments/v5-local-checks/receipt-controls-01-selection.json`, SHA256
`450598d2c05b02510f9183dc41b0a974bb263addef32b8556f81a8d5ff211f1c`.
Twenty source and eighteen explicit runtime pins, 30 CPU seconds / 90 wall
seconds / 512MiB / two active processes. Source readback matches; output absent.
The unused draft selection8dd907 was repinned after strengthening actual mixed-
route depletion: two prepaid + four actual requests exhaust six allowed attempts;
the next offer must refuse before provider dispatch. No operation used the draft.
No runtime, guest/proof, old campaign or unknown-custodian routing was launched
by this lane. Root owns launch after independent source and selection review.

### Actual receipt-controls01 adopted; used source frozen

Root executed final450598 selection once. All eight groups passed with zero
failures/errors/skips and clean child/Job closure. Independent assurance
rehashed all20saved/current source and18runtime pins and adopted the narrow
synthetic structural outcome. Outer result SHA256
`398a0695b268eae0a72c66ff97bc2670cdef03a2ac68e14a0fa0799708eb0f41`;
inner result SHA256
`ef6fdae38b88598493d00a11b36e8deaf2f26760e735a88d64f9fd5ade8c42e1`.
The author read the inner actual result and independently rehashed both files.
Root reports0.78125Job +0.28125wrapper CPU seconds,1.6384wall, clean closure.

The actual composed synthetic path made four network requests,638request-body,
1354reply-body and900combined-header bytes. Two earlier logical attempts and
4096reply bytes were prospectively prepaid; six aggregate attempts were exhausted
and the next offer refused before any provider dispatch. Receipt HTTP was
301request/461reply/459header; old JSON group/body was893reply/441header. No
pending/reserved request remained. Cold local readbacks succeeded after supplier
shutdown; all saved authority flags remain false. Six binary faults each consumed
27reply bytes and one attempt; five unknown outcomes conservatively recorded
81920header and81920request-body exposure bounds. No receipt decoding, verifier
worker, mathematical admission or old campaign ran. All used source/test/selection
and actual evidence now stay frozen; no repeat is needed.

### D19 source-only common workflow composition

Root next selected preparation of a minimal original-deadline public wrapper,
not another transport campaign. New unrun source:
`software/v5/transport/located_receipts.py` (`LocatedReceiptWorkflow`). It
composes exactly the adopted `ServiceLocationProcess`/`ServiceLocatedWorkflow`,
one SearchSession and the frozen D18 acquisition/admission classes. The owner
creates D before setup and supplies a fresh private reader and optional actual
verifier with identical D. Initial namespace/policy/wire-profile/store checks
precede network work. Existing phase deadlines may be earlier, never later.

Before reader start, the wrapper prepays maximum route-operation + descriptor +
search-request allowances and full location/search reply capacity into the
acquisition ledger. Route attempts are logical operations, not DHT packet counts;
Node raw-traffic/event/connection caps and actual reports remain distinct. No
unused prepaid capacity is refunded. One caller-driven route/descriptor/search
phase transitions once into acquisition, retaining the same ledger and D.
The selected candidate must actually occur in that SearchSession's exact
`(object_id,RecordID)` candidate set; no first-seen metadata gains authority.

The newly consequential seam is endpoint lifetime: each acquired descriptor's
owner-adopted endpoint and original expiry are wrapped in an endpoint-compatible
guard. Both frozen HTTP implementations already call `validate()` immediately
before dial, after attempt reservation. The guard rechecks D, descriptor TTL,
unchanged endpoint and owner egress; an expired/changed contact refuses with the
attempt charged. No frozen global/class is patched. The index endpoint may be
tried for cohosted custody, with missing role consuming/refusing the attempt.
This does not implement generic unknown-custodian routing or promise custody
from an index role. Durable stores remain owner-managed; workflow close revokes
handles and closes its reader with the retained bounded cleanup allowance.

No runtime selection exists for this new wrapper, and no fake-positive integrated
campaign is proposed. Next consequential actual run needs a genuine current-image
receipt and freshly derived same-policy module export/index. It should connect
the already scoped location/search and D18 phases once, perform actual local
admission, and establish fresh cold re-verification from retained custody after
the supplier closes. Used passing component evidence should be reused rather
than rerunning the old suites. All broader release/growth obligations remain open.

### D19 post-Git focused control preparation

Root completed local baseline7e2c038 and safeguards2f9be5f, then explicitly
resumed this lane. Canonical guard passed; new Git discipline and VERSION-CONTROL
were read. Root alone stages/commits/configures Git. This lane has performed no
Git mutation, cleanup, branch switch or runtime launch. D18 used bytes stay frozen.

Independent read-only D19 source review found no blocker: location reply capacity
already includes search exactly once, original D binds reader/verifier, the one
transition retains exact `(objectID,RecordID)` candidate membership, and both HTTP
implementations reach the expiry/egress guard after reserving an attempt. Contact
expiry restricts future dialing, not mathematical validity of already held bytes.
The consequential new control is expiry AFTER `begin_acquisition`, not a repeat
of existing location or transport tests.

New unused harness `software/v5/transport/test_located_receipts.py` contains six
focused groups. It uses actual wrapper, store constructors and both HTTP preflight
paths, but mocks reader start/close and explicitly seeds **unauthenticated owner
fixtures** for contacts/candidates. Placeholder runtime reference pins are never
adopted, read as executable dependencies or launched. Runtime-adoption, process
and socket tripwires forbid such work. The frozen D18 fixture is imported; its
test suite is not loaded or rerun. No real verifier object or success is fabricated.

Controls cover upfront shared prepayment and original D, insufficient grants and
initial namespace mismatch; pending-search/exact candidate pair/one transition;
post-transition TTL expiry for structural and raw receipt calls; post-transition
owner egress invalidation for both calls; later original-deadline exhaustion; and
close's work-revocation/store-ownership scope. The expiry clock is explicitly
past contact TTL but before D and the location deadline. Each refused predial
attempt keeps its full selected byte allowance, pending remains zero and no store
write occurs. Owner policy mutation is test-fixture invalidation, not a newly
implemented policy-rotation API. All report authority flags remain false.

Reviewer has the source and was asked to challenge it before the exact finite
selection is finalized. No new selection or runtime is yet prepared by this note;
root alone may launch after review. Genuine current-image mathematical integration
remains separate and must not be inferred from these source/guard controls.

Root and independent reviewer subsequently read the full wrapper/harness and
found no source blocker. The reviewer confirms the real constructor accepts the
snapshot location-directory shape; mocked lifecycle/reference markers do not
claim actual adoption; named-suite loading cannot execute the old D18 tests.
The expiry and policy controls reach both actual HTTP preflight boundaries.

Prepared fresh finite selection:
`experiments/v5-local-checks/located-receipt-controls-01-selection.json`, SHA256
`8a302e1ed3211365c16c7ee0929dce0c878940aca3750e288b8af80e1885dfb8`.
Twenty-seven source and eighteen explicit runtime pins;15CPU seconds /60wall
seconds /512MiB /two active processes. All twenty used D18 source hashes were
rechecked against the adopted450598 selection and match. The seven additions
are the D19 wrapper/test, four location Python dependencies and SearchSession.
Output is absent. Independent exact-selection clearance is pending; root alone
launches. No Node, DHT, socket or genuine receipt verification is selected.

### Located-controls01 partial result and minimal continuation

Root executed8a302e once. The full six-group run is **FAIL**, not reclassified:
five groups passed, one failed at its undersized-request-grant assertion; no
error/skip and clean process/Job closure. The product correctly raised
`INTEGER_BOUND` from the component bound in `AcquisitionBudget.charge_external`
before its later aggregate-sum check. The harness wrongly expected
`RECEIPT_AGGREGATE_BUDGET`. Earlier assertions in that group had reached the
original-D/shared-prepayment/different-deadline checks; its subsequent undersized
byte and wrong-profile checks did not run. No product repair is indicated.

Actual outer SHA256
`96a7c365702c1a2d63c76a3f581764bb3f0cf6f771eb081c52f7fc93e1ba5b5c`;
inner SHA256 `0103c4a4912fbbcbaead9b5e137685f8bdbd61cf9d1c509c10bb3ca7c81cba20`;
stderr SHA256 `e84c5ffd63cff359fcd3687c6607fe508067f482997edbab4fc86fe7837c626d`.
The author read and rehashed these actual files. Root reports0.671875Job +
0.28125wrapper CPU seconds,1.5174142wall and clean closure. All used product,
harness, selection and evidence bytes remain frozen. Independent outcome audit
was requested. No blanket retry or repeat of the five passed groups is selected.

Passed post-transition expiry and policy controls each charged7prepaid logical
attempts/24576reply bytes plus one789-byte structural allowance and one27-byte
opaque receipt allowance:9attempts/25392charged reply bytes, no pending/reserved
request and no store writes. Guard refusals happened before either provider dial
tripwire was called. These are charged allowances, not actual network bytes.
More precisely, the tripwire excludes provider `asyncio.open_connection` and
process-spawn calls; it is not an audit of OS/event-loop internal handles.
No DHT, authenticated contact or mathematical verification was established.

Root selected a fresh source-only continuation for just the three unfinished
constructor refusals. `transport/test_located_receipts_remaining.py` imports the
used fixture setup but explicitly constructs **one named TestSuite case**;
default discovery, which would inherit/repeat old methods, is forbidden.
Undersized request and reply grants both correctly expect `INTEGER_BOUND` from
the retained per-component bounds. The policy mismatch expects the retained
initial namespace/profile refusal. The runner pins/requires the old actual
FAIL6/1/0/0 and five passed stderr groups without rewriting them.

Prepared selection02:
`experiments/v5-local-checks/located-receipt-controls-02-selection.json`, SHA256
`699f931132b2a7bda37f63f669c077a4dff1e24b008c8e8299646a69ddf4f9ed`.
Twenty-eight source/twenty runtime-input pins,10CPU seconds /45wall seconds /
512MiB /two active processes. All27used source pins from01 still match; only
the new continuation and two retained evidence inputs are added. Output absent.
Source/exact selection review is pending; no runtime was launched by this lane.

Independent reviewer subsequently adopted the original partial result: all27
saved/current sources and18runtime pins match, five groups plus the executed
constructor prefix are valid narrow evidence, and both incomplete component
overruns properly raise `INTEGER_BOUND`. The same reviewer clears continuation
699f9311:28source files329,513bytes and20runtime/evidence pins match; output absent;
the explicit one-case suite cannot repeat inherited old groups. Root alone has
the cleared finite launch. No product change, fake admission or broad rerun.

### Actual continuation02 PASS; composition controls closed within scope

Root executed exact699f9311 once. One explicit test / three remaining constructor
refusals passed, zero failures/errors/skips, clean child/Job closure. Independent
reviewer rehashed28saved/current sources and20runtime/evidence pins and adopted
the actual result. Outer SHA256
`d979411e1ad79944bf0a21ca591ef416162498632d73b6a4f86f17b2835df032`;
inner SHA256 `8bac4b723a5a51bddddfe36c7a8122c9cfdb9de54b55409b2c27e0f99a90b5f5`.
The author read the inner result and rehashed both. Cost0.734375Job +
0.359375wrapper CPU seconds,1.5822417wall. Five earlier groups and their valid
constructor prefix were reused, not rerun or relabeled. The prior full-suite
FAIL remains preserved. All28used source files, both selections and results
are frozen. The D19 changed-boundary gate is now satisfied in its explicitly
mocked/no-provider-dial/no-Node/no-admission scope. Genuine integration is open.

### Genuine current-policy integration: prerequisites and discovered reuse seam

The smallest next actual path is **one** newly certified current-policy module
through the D19 public composition, not another old-policy location campaign.
Before any selection, root needs a completed genuine profile2 receipt, adopted
actual image/host/runtime pins, exact ModuleSummary and matching committed group
opening/body data. The image comes from actual assembly; neither a guest ELF SHA
nor diagnostic journal is an adopted image/certificate. Profile2 binds184-byte
DMKNM002, exact foundation/policy/module and empty assumptions. Current receipt
format/implementation compatibility remains the D18 wire-profile selection.

Use the exact current-policy spec already bound by that certification to derive
the selected export object and fresh `ModuleExportAdapter` namespace/index.
No old-policy ModuleID, SnapshotID, locator or export is relabeled. Producer-side
opening/index construction is not receiving-side download of proof ancestry;
its actual cost must nevertheless be counted. At the receiving boundary obtain
only the selected group, exact receipt and explicitly demanded committed bodies.
Old proven components/control results are reused; one current namespace's actual
location -> candidate -> group/receipt -> local verification is the new boundary.

For this first path, the owner-approved provider can explicitly cohost index,
module and receipt roles. The descriptor authenticates an advisory contact,
not a custody promise; missing roles spend/refuse. The experiment cannot establish
unknown-custodian routing, independent-host deployment, global recall or growth.
Budget and original D must be assigned before setup, including location runtime
adoption, metadata construction, all HTTP work, receipt verification, readbacks
and teardown. DHT events/raw transport and HTTP body/header costs remain separate.

The source inventory found a central **authoring compatibility gap**:
`software/v5/authoring/imports.py:ImportSession.__init__` currently demands
`type(verifier) is ReceiptVerifier`, so it rejects the exact
`DeadlineReceiptVerifier` used by D18/D19. This is a safe refusal, not false
acceptance, but located admission alone therefore does not yet compose into the
authoring session. Root and independent reviewer were notified; this lane did
not edit authoring ownership. A separately selected bridge should support only
explicitly adopted owner verifier types, retain originating live-handle checks,
and clamp the import-session deadline to the original verifier/workflow D.
Generic duck-verifier acceptance or loading saved success JSON is not a repair.

There is also an explicit lifetime dependency: `LocatedReceiptWorkflow.close()`
closes its verifier and revokes handles. Verified authoring selection (`use_handle`,
`open_group`, demanded bodies, `make_request`) must occur with the same live
verifier before workflow closure, unless root separately selects an ownership
split. A generated prover request is untrusted data and may be retained for a
later bounded proof operation because the actual prover rechecks the selected
parent receipts; the prior local acceptance is not serialized as authority.

Supplier-independent and cold claims require distinct evidence: stop the
supplier after exact receipt/group/demanded bodies commit and read back; a fresh
consumer process must reopen those stores and invoke the genuine adopted verifier
again, obtaining no handle from stored flags. Reserve any cold-worker verification
attempt/input/CPU allowance before its launch and keep its deadline within the
same selected outer operation; do not silently create a fresh global grant. A
valid receipt associated with a different ModuleID must still refuse against the
wrong expected summary. These actual receipt/cold-binding checks cannot be
replaced by the synthetic D18/D19 passes. No such runtime is selected by this note.

### D19 explicitly selected unused authoring bridge

After reading `imports.py` and finding no used-selection references, root assigns
this lane temporary, narrow ownership of **unused** `software/v5/authoring/imports.py`
and the lifetime section of `VERIFIED-IMPORT-AUTHORING-CONTRACT.md`. This does
not authorize changing used product source or the separate Lean frontend lane.

The source now allows exactly `ReceiptVerifier` and `DeadlineReceiptVerifier`;
it checks actual verifier liveness before construction, clamps session D to the
minimum of requested lifetime/actual verifier deadline/original outer deadline,
and checks the originating verifier again on every `_active`, including empty
sessions. Original handle registry, exact receipt/summary/journal bindings,
body checks and untrusted-request construction are unchanged. The updated
contract requires acquired-handle authoring before LocatedReceiptWorkflow.close
and preserves subsequent independent host/guest verification of retained requests.

New source-only `authoring/test_import_lifetime.py` has six focused groups for
exact classes/all deadline minima; duck/subclass refusal; closed/expired
constructor refusal; verifier-close revocation of empty-session operations;
independent session/verifier expiry and session-close ownership; and refusal of
unregistered/serialized tokens. Lifetime fixtures bypass actual installation
adoption and retain **empty handle tables** throughout. Public `VerifiedModule()`
construction appears only as a negative unregistered token. No positive handle,
receipt, journal, verification output or cryptographic success is fabricated;
`receive` is never selected. The root and reviewer have the source; independent
challenge precedes a fresh finite selection. No runtime or Git mutation by lane.

Prepared exact finite selection:
`experiments/v5-local-checks/import-lifetime-controls-01-selection.json`, SHA256
`b032573207b7c8c8b370ee95fcd85ef209b6b32786eec2dc79b6ce722077f94b`.
Twenty-three source and eighteen explicit Python runtime pins;10CPU seconds /
30wall seconds /256MiB /two active processes. The source snapshot entry is only
the new six-group lifetime harness; no positive admission, network, Lean or
proof runtime is selected. Root and reviewer have the exact selection and
contract. Reviewer previously found no scoped source blocker and is checking
the exact finite selection. Output was absent at preparation; root alone launches.

Independent exact-selection review now clears b0325732:23source pins/230,273bytes
and18runtime pins match; output remains absent. The full bridge and lifetime
contract were read. This clearance remains limited to exact verifier types and
empty-registry lifecycle controls, not broad authoring or mathematical admission.

### Actual import-lifetime01 result

Root ran the cleared selection once; all six groups passed with zero failures,
errors or skips. Independent reviewer adopted the actual result and all23saved/
current source plus18runtime pins. Job CPU0.734375seconds, wrapper0.296875seconds,
wall2.2575266seconds; clean closure. The author read/rehashed actual evidence:
outer `524dbab053ca1c2d4e4ed7e2d36fe00f1441d82147e20835ce099a9845b59d96`,
inner `642b351077c973fb1f7fa7b9e64ea7b3c8651ae9334218b48c10687c0ec60915`.
No positive handle was registered and receive was never selected. Bridge,
harness and selected dependencies are now used/frozen. This closes the narrow
lifetime/type seam, not ordinary authoring or genuine receipt reuse.

### D20 current-profile path: existing data versus missing software

Root requested a concrete integration map while proof work proceeds, not another
campaign or new plan. Source inspection establishes the following composition:

| Step | Existing callable path | Additional input or gap |
|---|---|---|
| Current module bytes | Snapshot03's `profile2-request.json` contains actual local spec and committed bodies used by guest execution | A proving capsule is not a receipt. Preserve the original spec/image identities. |
| Publish discoverable data | ModuleExportAdapter + existing authenticated index, ModuleStore and ReceiptStore + receipt-capable provider | Prepare a fresh exact current-namespace index/openings and owner-configured provider; do not relabel the old fixture's index. |
| Find unknown export | LocatedReceiptWorkflow.start/route/descriptor/begin_search/offer/candidates | One current-namespace descriptor/index binding and one selected query, within the original finite D. No mathematical authority from any search answer. |
| Acquire and verify | begin_acquisition/export/receipt_offers/receipt/admit | Genuine final current-profile receipt and locally adopted host/image/runtime pins. No substitute from expected journal or capsule. |
| Select verified import | ImportSession(same verifier), use_handle(actual handle, exact stored receipt), open_group | Must finish while the workflow's originating verifier remains live. Receipt copied from local custody must hash-bind the actual handle. |
| Expand semantic context | Existing structural declaration/body routes; session.open_group/supply_body | Public exact-address dependency-group forwarding was missing; D20 companion below is selected. No ancestor theorem proof bodies are requested. |
| Ordinary local authoring | Pinned Lean source exporter and source_rows.decode_source are usable ingredients | No current AuthorLean/source adapter installs the selected module interfaces and derives a new local closure from caller roots. This remains the major source gap. |
| Produce child request | ImportSession.make_request(local-only environment, exact foundation rows, adopted image words) | Local source adapter must return the actual new local-only environment. make_request is not a child certificate; host/guest must reverify real parent receipts. |

Read-only inspection of actual snapshot03 identifies the prospective base module
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`,
foundation `d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481`,
policy `5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377`.
It has11groups/14declarations and11body entries: one Tree inductive group,
Tree helpers, fold/map definitions and binary_congr theorem. These data already
exist; they need not be invented or re-exported just to construct provider
openings. This is source/data inventory, not admission. Assembly04 actually
records image ID `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`
and image-file SHA256
`d76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f`.
The image ID is not the file SHA. Future root selection must bind exact retained
files, current receipt and actual adoption manifest; this note is not that selection.

Still missing/adoption-dependent: final genuine base receipt and actual verification;
exact receipt wire profile/local host-runtime adoption; current-namespace provider
index and location descriptor; independent ordinary child source and selected roots;
general authoring adapter; source-derived child request and final child receipt.
Foundation rows already exist in retained preparation and must be bound exactly,
not regenerated from whatever Init happens to be locally installed. No synthetic
PrepareWorkload ImportClaim or old profile1 PrepareReceiptWorkload output can fill
the receipt/verified-parent gap. Child proving is a later separate finite operation;
its parent bytes are rechecked even when its untrusted request outlives this session.

### D20 selected dependency-group acquisition seam

Source inspection found that `AcquisitionClient.declaration` already resolves
an exact `(ModuleID, structured Name)` without an index hint, but D18 receipt
acquisition and D19 located composition forward only search-returned exports
and committed bodies. Semantic closure may need another group that does not
match the original search query. Requiring every dependency to be an original
search candidate is therefore an operability defect, not a trust safeguard.

Root selects fresh **source-only** `software/v5/authoring/acquisition.py` and
the narrow dependency section of the existing authoring contract. The new
DependencyAcquisition requires exact workflow/session types, the same actual
DeadlineReceiptVerifier and an already selected module. It captures/rechecks
the existing acquisition/client/store/budget/verifier identities and uses only
the SAME underlying structural client; there is no renewed deadline or grant.
The copied validated structured address goes through the existing route, exact
summary/address checks, ModuleStore commit/readback, actual live session.open_group,
and final liveness after output copying. It cannot promote search candidates,
mint handles, verify a new module or crawl proofs. A late failure may leave
structural custody or a live opening; this is explicitly not one atomic commit.

Independent source review caught an important correction before execution:
the retained public declaration helper performs optional discovery-feature
extraction twice and may reject a valid complex type at its feature-profile cap.
Root therefore selects direct use of the SAME structural `_get` and existing
group route, followed by canonical group-opening/live-summary/unique-name checks
and direct typed locator construction. No feature extraction, RecordID or
synthetic candidate is needed. The fresh companion/contract now implement this
correction; retained transport sources remain unchanged. This removes a real
discovery-to-semantics coupling rather than merely documenting a restricted route.

The source and contract are with the independent reviewer. Focused new controls
are selected only after that review; no runtime or Git mutation by this lane.
Used receipt/located/import sources remain untouched.

### Most consequential next source proposal: ordinary certified-context authoring

After the bounded dependency companion, prioritize the existing contract's
`AuthorLean.lean` plus `source.py` adapter, not another network experiment.
Mechanism confirms its present assignment is proof-cost work, not frontend work.
The key input is **ImportSession.selected_data() from the same live verifier**,
owner source and structured roots; a proof-authenticating JSON flag is not input.
Root must explicitly assign implementation ownership before work begins.

The minimum coherent slice is a bounded semantic-context assembler and Lean
frontend together. Starting at caller-selected import addresses, traverse types;
for transparent definitions traverse the committed actual bodies; for inductives
include the whole group and reproduce/compare native-generated recursor metadata.
For imported theorem and opaque interfaces traverse their types but not proof/
opaque value ancestry. Missing groups/bodies produce bounded typed demands to
the existing acquisition/session APIs. Exhaustion refuses without treating missing
definitions as opaque. Context cost can depend on selected semantic-body closure;
it must not depend on transitive theorem proof histories or unrelated corpus size.

Use `DMKN.Mod.<ModuleID>` structured relocation and explicit foundation/external
name inventories; never derive semantic names by splitting display strings.
Install theorem/opaque assumptions only inside this owner-controlled authoring
environment, transparent definitions with real bodies/hints, and inductives via
Lean's group constructor. Preserve all old bindings across source elaboration.
Export reachable NEW local groups/auxiliaries from the caller's actual structured
roots. `source_rows.decode_source` can omit precisely registered external rows
while rejecting unclassified declarations, partial groups and fresh local axioms.
Unknown used Init/library constants must become captured local dependencies or
refuse; importing Init for syntax does not expand the mathematical foundation.

The frozen AgentClient source gives the environment-assembly/old-binding-check/
reachable-export pattern. It cannot be used unchanged because it replays complete
old proofs in an obsolete content format. ExportWorkload likewise cannot be used
unchanged: it starts from Init with fixed theorem roots and has no certified import
environment. A thin wrapper around either would not close the missing capability.
Retain independent final relation checking as the soundness boundary, but require
one actual source-derived Tree/map child to establish useful frontend compatibility;
a handcrafted canonical child or an assumption-only identity example cannot replace it.

### D20 actual dependency companion controls adopted

Root executed the independently cleared exact selection
`experiments/v5-local-checks/dependency-acquisition-controls-01-selection.json`,
SHA256 `34f32284af2979e996f795d2407df2cee50fdc3adf759a556137481df1141a59`.
Thirty-four source/eighteen runtime pins,15CPU/45wall seconds/256MiB/two processes.
All six groups passed with no failure/error/skip; independent actual audit adopted
all saved/current pins and clean closure. Job CPU0.921875seconds, wrapper0.34375,
wall2.0356054seconds. Author read/rehashed outer
`9c39b930643bb208beea39be35fc7a9981364d6853d4725fba955a15247be51e`
and inner `a1231bf57da74b1c82d4e2b3d07f70f94e234290372b43c341c03a63e570c9c6`.

The synthetic140-symbol structural type actually exceeds discovery's feature cap,
yet passes the feature-free conditional group path (one request/9486reply bytes).
Exact-name/corrupt-opening/wrong-selected-summary refusals precede any commit;
TTL then earlier-session-expiry preserve two charged attempts/4618reply bytes
and no commit. Late readback/open refusals leave structural custody only. Exact
classes, live owner identity, copies and absent candidate promotion are checked.
The conditional selected-summary/open callbacks are explicitly mocked; there is
no positive registered handle, receipt verification, provider dial, authenticated
location or genuine imported mathematics. All used companion/harness bytes are
frozen. No rerun; the actual genuine endpoint remains required.

### D20 next source selection: context/frontend/owner adapter

Root now assigns new source-only `authoring/context.py`, `AuthorLean.lean` and
`source.py`; no build, runtime, proof or positive admission is selected. The
complete-group design below is added to the existing authoring contract and
sent for independent challenge before coding that native seam. Used helpers,
imports/acquisition and exporters remain unchanged. No transport variant is added.

### D22 ordinary Lean frontend draft and compile-only proposal

Native source now includes canonical descriptor decoding, exact adopted
foundation/runtime comparison, checked imported definitions and full inductive
groups, recursor metadata/RHS matching, actual imported frontend visibility,
old-binding preservation and source-derived bounded export. Imported theorem/
opaque values are authoring-only assumptions at exact registered boundaries;
their proofs are neither traversed nor exported. Unknown used Init constants
must be captured as local data or refused. Fresh axioms/quotient constants refuse.

Independent source review found Lean's ordinary Expr BEq ignores binderInfo;
the fresh frontend now uses Expr.equal after narrow normalization and structural
expression-key caches. Direct full-group insertions also have the4096 cap.
Root's hidden-Init visibility concern is resolved without weakening mandatory
new imported-group visibility. Reviewer read all932 lines and reports no immediate
semantic source blocker; actual compilation/native compatibility remain unrun.

Source draft identities at compile proposal:

- `context.py`: `a6d0b794204fb92dd43b7b63d38cd4f4dd15dff5d7f33d0254c4f1cbc1650541`.
- `source.py`: `834718f8e52ca8360d97d921f16bcf1c22ef0a111528bc8edf53d4572c116df0`.
- `AuthorLean.lean`: `00f90c7f449d1228227d89fc251283061ccfa59791e5bd563e058b3d41f1f78e`.

Root requested the exact small compile-only selection at
`experiments/v5-local-checks/author-lean-build-01-selection.json`. It uses unchanged
Run-V5-Check and retained Lean4.34, three source/seven runtime pins (all inspected
and matched),60CPU/90wall seconds,2048MiB,two processes,1MiB per output stream.
It emits checked .olean and C source only, not a linked executable and not an
authoring run. Root owns review/adoption/launch; this lane has launched nothing.

The existing contract records native64 versus codec256 universe scope, existing
8-parent/session and selected semantic-closure caps, exact-address external-owner
bootstrap requirement, and preservation of any foundation mismatch. Suggested
next meaningful native input is an actual imported Tree/fold/map/binary_congr
source-derived fold_map law, not an assumption-only identity. Structural packet
success cannot replace actual positive receipt/session-to-child qualification.

### D22 compile repair, retained native link and conditional control selection

Build01 failed on Lean's reserved local identifiers `meta` and `scoped`; all35
parser diagnostics and clean failure remain. Outer RESULT390df8553cd197a19bf1c2e02b6da052986d176e1f264d571fd1284e2747191e:
5.265625JobCPU+0.703125wrapperCPU seconds,50.7992943whole-wall seconds. No authoring
input ran. Original source00f90c7f is frozen. Root selected fresh
`native02/AuthorLean.lean`: exact byte copy hash-checked before the minimal local
identifier and relative-license-path edits. Source9597caa077301506fbbbde257a3a466b042f2eb1a6b442c0a1a550b619cddd1c
and build02selectionc763b5c9833aa6efbe0bdee1afcabd1658134e8366c38e587b25bebb7245d83c
passed independent source review and actual root compilation.3.875JobCPU+
0.5625wrapperCPU seconds,4.6882247whole-wall seconds, empty logs and clean closure.
Native02 is now used/frozen. Actual .olean22e17b5663a8c9779666e3b3e218155ca111eccaf81e0eff369a7ea0b0492a2b
(4,457,008B) and generated C5cd6401e02f59989350e04a2900df88d47a2a548f67be6d1e458515123473e73
(1,488,069B) are retained. Compilation is not authoring success.

Root selected the assigned harness's stdlib-only exact link mode. Selection
`author-lean-link-01-selection.json`57ebc233489601091bf3a4a55e7c14da90a4cc581483e2803c492d06bb1b6277
uses three sources/69runtime pins,90CPU/150wall seconds,2048MiB/six processes.
The harness3f13702cea308fff9e0552c9465f1b00361fa3d8fda2824de9193c4cca90f547 and
runtime manifest373862d53214e39d92209d2afbca563eefa037b4eaab223400abe3a821f2fb8c
are used/frozen. It links held C with retained `leanc -O0 -leanshared`, without
Lean re-elaboration. Root reports/adopts independent actual PASS:
2.421875JobCPU+1.765625wrapperCPU seconds,6.7398912whole-wall seconds. The resulting
593,408B executable is `author-lean-link-01/link/AuthorLean.exe`, SHA256
1f73b8b0ea20395a43202a3c155e6fd929a5ae0cef2a74a4c70d2625b9e3f69d.
This lane read the inner result and did not launch anything.

The runtime manifest pins66 explicit retained tools/libraries/Lean headers;
owner-local LEAN_SYSROOT/binPATH is installed inside the supervised worker.
This is not a hermetic toolchain claim. Timeout handling preserves bounded
partial logs/disposition; capture-output quotas are explicitly posthoc under
outer memory. `API.md` documents the actual source preparation/return methods,
demands/lifecycle and the production source-worker environment integration gap.

Proposed exact conditional controls selection is
`author-lean-controls-01-selection.json`8433dbc4b677135c328ad6bd4ba43b6966bc50d4804fdf4bc63d7d54802e3f24:
31sources/87runtime pins,90CPU/270wall seconds,2048MiB/four processes. It calls
the retained executable directly, with no repeated successful compile/link.
Inputs are actual `receipt-prepare-01/prepared/base/bundle.json`
09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926 and foundation
736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c. The base bundle
has the current module2b54d3be...,11groups/11semantic bodies and no theorem proof
bodies. No verifier/session/positive handle is fabricated. One positive source
uses exact-qualified Tree/fold/map/binary_congr and explicit Tree.rec induction,
plus two binder-info-distinct roots. Four negatives cover foundation binderInfo,
generated recursor RHS, missing transparent body and fresh-axiom escape. Root
owns separate review/launch; actual controls are not claimed here. Mechanism
separately owns genuine receipt/session-to-source child integration; no duplicate
fixture work is assigned.

### D22 actual five-case native result read

Root's controls01 returned zero and closed/reaped cleanly. Author read full outer
and inner results and rehashed them: outer
033a67348d6f389c629090607ead798aabd71a63b6099f55ae77d35fd4741053;
innerc8e03b22146fef679fcf88a67dc14d3c2fb54204e3878ccd4201da99d03231ae.
All five cases pass. Actual positive output has three local groups/declarations,
module890b30cc92673437addbe6d33409e89ced54b03ce29abb97043db9016eb700f9,
substantive inductive/definition/theorem use and preserved binderInfo distinction.
Four exact native refusals occurred, with no final EXPORT for negatives. No
receipt verification or positive handles; imported theorem proof bytes zero.
Total7.59375JobCPU+1.921875wrapperCPU seconds,11.7218668whole-wall seconds;
peak499,224,576B,active0,total7processes,no cleanup errors. Independent actual
audit is root/reviewer-owned; no new run is selected by this checkpoint.

API documents the passed conditional scope and still-open genuine source endpoint.
The old fold-prepare01 bundle is NOT appropriate for that endpoint: it binds
module28b3e7c4.../policyb49e45c0.... Author identified and sent this stale-reference
correction to mechanism/root before implementation. Use the current receipt-
prepare01 bundle09e4f3bb... (module2b54d3be.../policy5edfd0ee...), which was used in
the actual five controls. Do not reinterpret old-policy identifiers. A meaningful
genuine child should select only the substantive theorem root, so its resulting
ModuleID is to be derived, not copied from this three-root control.
