# Complete-delta discovery and independent custody seam

Owner: `v5_receipt_source_loop`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
This is a fresh theory/source decision, not runtime evidence or release completion.
Root approved the composite-provider-first implementation after the source
inspection below. Used receipt/index/location code remains unchanged.

## Central obstacle and smallest architectural intervention

Actual native-delta admission solves only local checking. The existing network
receipt ABI accepts real RISC Zero receipts and cannot transport a native-delta
packet as if it were one. The existing locator advertises only `formal-index-v1`,
not a generic custody service. Therefore a correct next end-to-end system needs
both (a) an explicit distinct proof-form transport, and (b) a discoverable surviving
holder, not an out-of-band private holder list used by an experiment harness.

Keep the existing mathematical export identity and formal index unchanged.
`ModuleExportAdapter.describe/extract` authenticate descriptor openings and derive
features without requiring a receipt. A module's exact semantics must not change
identity when its proof changes from a bounded native delta to a succinct receipt.
Index candidates remain candidates regardless of proof form.

The smallest integrated deployment role is a **composite index + semantic custody
+ delta-packet custodian**. Each independent replica indexes the export descriptors
it actually retains, serves their selected groups/bodies and complete packets, and
legitimately advertises the existing formal-index rendezvous keys. Existing
location and unknown-ID search can then find the surviving replica after the
producer disappears. An index-role advertisement still does not prove custody;
explicit proof-form offers and acquisition determine whether a contact can help.

This does not assert general custody-only routing. A pure custodian with no index
is reachable only through separately supplied owner-approved contacts for now.
Adding generic DHT roles/referral routing is unnecessary to demonstrate this
reciprocal path and should not be silently simulated by rebranding a custodian.

## Distinct wire contract

New local selection binds a delta wire profile containing the packet schema,
profile-2 relation/image, foundation, semantic policy and exact existing frontier
receipt wire profile. It is independent of machine-local source paths and of the
owner's finite envelope. The local receiver still independently adopts its
implementation; a downloaded profile never configures or authorizes a verifier.

Two new read-only routes are sufficient:

- `/v5/modules/delta-offer`: selected ModuleID/profile -> bounded list of exact
  packet SHA-256 digests and byte lengths. Assurance is explicitly unverified
  complete-packet byte locators, not a receipt or checked theorem.
- `/v5/modules/delta-packet`: exact digest/size -> exact complete packet bytes.
  The packet includes every needed uncertified ancestor and real receipt frontier.

The same provider continues to expose the existing formal discovery, group and
body routes. Existing receipt routes and receipt storage remain untouched. Packet
storage is a distinct bounded SQLite database with its own schema, quotas,
per-module offer cap, immutable digest binding, and atomic packet/offer commit.

Every response is finite; failures and stale offers consume the same original
workflow allowance. Endpoint discovery is advisory, and egress/TLS policy remains
the owner's. No redirects, remote source execution, remote write endpoint or
unbounded referral exploration is added.

## Three independent predicates

For a candidate export `e`, module `m`, packet `p`, and selected semantic set `S`:

1. `DescriptorBound(e,m)`: the existing canonical export/group opening and formal
   feature extraction match. This is not mathematical acceptance.
2. `Held(p,S)`: exact packet bytes and selected semantic components have been
   committed and read back under finite custody policy. This is not a future
   retention guarantee, and separate databases are not jointly atomic.
3. `DeltaAccepted(m,p)`: the actual same local DeltaVerifier checks every frontier
   receipt and every complete uncertified relation, binds its actual graph and
   creates a live distinct handle. This is not a succinct receipt.

An acquisition client may return an admitted local result only after all three
hold, original budget/deadline remain live, and post-admission custody readback
passes. If finalization fails after a handle was minted, it closes that verifier
so no resulting delta authority survives the failed operation.

Completeness for **checking** is not completeness for every future **use**.
The full packet is self-contained to its receipt frontiers, but ordinary source
reuse can demand additional group openings or transparent definition bodies.
Those remain explicit typed semantic demands. Publication must preserve the
selected semantic context needed for the chosen reciprocal workload; no
`all_future_bodies_covered` claim is justified.

## Resource argument

Let `P` be the chosen complete packet, `S` the selected semantic bytes, `Q` the
bounded discovery transcript and `R` the selected receipt frontiers. Acquisition
requires byte work proportional to `|Q| + |P| + |S|`, not the entire global corpus.
Receiving native work is bounded by the full selected uncertified closure, while
the certified frontier replaces proof ancestry below `R`. It is not independent
of unsealed chain length; exceeding the finite envelope returns incompletion or
requires selective sealing, never omission of proofs.

The new client reuses the existing aggregate acquisition budget for network and
verification reservation. It precharges the sum of all selected per-frontier and
per-delta CPU maxima before receiving. The existing 600-second per-verification
budget method is a conservative client envelope, not a new global lower cost
claim; larger selected closures may require a smaller native allocation or a
separate future budget successor. The receiver also enforces its own fixed owner
allowance. Nested reservations are constraints, not two actual CPU measurements
to add together. Verification wall time is clamped to the original outer deadline.

The replica's formal index can be sparse and specialized. Its per-query work and
coverage remain exactly the existing bounded authenticated index claims. Hash
membership and finite-index coverage do not prove global semantic completeness;
the composite-role choice changes neither conclusion.

## Fresh disjoint implementation selected by root

- `software/v5/delta/custody.py`: strict separate wire profile/offer and bounded
  opaque packet custody; no receipt subclass or accepting mathematical flag.
- `software/v5/delta/transport.py`: composite provider successor and aggregate
  acquisition, sharing existing low-level HTTP/TLS/resource primitives and
  unchanged discovery/group/body dispatch. No frozen source mutation.
- A compact API document and targeted test drafts may follow source review.

Required discriminator: discover the actual unfamiliar delta export by formal
features through the existing index; acquire its complete packet from an
independent retained composite provider after the original provider disappears;
actually admit it; author the substantive second delta; return complete material.
Same-host fixtures test protocol independence, not independent-host availability.

The new ordinary-source target selected by root is `DeltaFoldMapTwice`: two uses
of the previously authored fold-map law through transitivity, not rediscovery of
the original inductive theorem. Root owns all actual launch selections. No runtime,
network service, test, build, proof, license decision or deployment is performed
by this lane's source work.

## Draft implementation checkpoint

Fresh custody and transport source now exists with a compact `network_api.md`.
The source-only review selection is custody `4304e529`, transport `ab5757c2`, API
`f1d3567d`. Five fresh controls in `delta/test_network.py` are drafted, NOT RUN:
proof-form/route separation and untrusted offers; exact durable reopen/dedup/hash
corruption; target/profile/quota/transaction refusal; one bounded actual loopback
packet acquisition and supplier-offline selected readback; and refusal of
unoffered downloads/duck authority. Synthetic empty relation rows are explicitly
not valid mathematics. No actual native check, receipt verification or positive
authority is created by those controls. Earlier packet tests are imported only
for their inert fixture, not rerun as another campaign.

The initial `from_search` ledger-truthiness boundary has been strengthened before
runtime, with root/reviewer agreement. Fresh `DeltaLocatedHandoff` requires the
actual unstarted ServiceLocationProcess, original absolute deadline and exact
finite location/search grants. It creates the existing ServiceLocatedWorkflow
and prepays its full route/descriptor/search ceilings before dispatch. One actual
search and one acquisition handoff are permitted; identities, grants, original
deadline and prepayment are rechecked. Failed handoffs do not refund charges.
This is a trusted-owner composition check, not protection against malicious owner
Python. No source/loopback/SQLite test has been launched by this lane.

The handoff's fresh-reader gate covers process/start/spawn/close tasks, sequence,
sent/received/read-frame counts, stderr task/data, failed/closed state and reader
role. The precharged reply ceiling includes descriptor plus search bytes; routing
events do not bound DHT wire bytes. Location startup/service CPU, DHT traffic,
provider work, transport overhead and all controller CPU retain their existing
separate telemetry and enclosing Job responsibilities. AcquisitionBudget alone
is not a whole-system wire/CPU envelope.

Latest stable source-only review selection supersedes the earlier transport/test
draft hashes: custody `4304e529a15e9249d8ba43f5390e94082d0baad1c55db6fb5b74b4160a1fa27c`,
transport `18c1abda1dca45cd8f5e86c09c4e1b8d5b13d4472931173a1db4a080c0c71d40`,
test `39d8c9d28fab9ab1e0a2f0a7852a94f02565deabd64d1f15a7a484d6b019f23e`,
API `688fac0a8539b61aed288d1d6a784b4a20250cd96f9d4760a606580f3bde47d4`.
The independently source-cleared authoring `bf3f266c` remains unchanged. The fresh
actual authoring endpoint owned elsewhere is intended to retain a real complete
two-delta packet; the network integration should consume those exact result bytes
and never repeat a successful source prefix merely to obtain test material.

## Actual two-cold-recipient endpoint: fresh source selection

The five structural/loopback controls subsequently passed under root's selected
run. Their used source and evidence are frozen. They do not establish the real
DHT/Noise/semantic-import/native-admission endpoint below.

The first actual onward authoring run retained ordinary-source composition but
failed cold admission because of source-row correspondence, not because the
composition was disproved. Root preserved that failure and selected a distinct
canonical-row repair from the retained export, without reauthoring. Its corrected
662480-byte packet is independently audited at
`experiments/v5-local-checks/delta-reprepare-01/evidence/delta-packet.json`, SHA-256
`54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1`.
It has one actual receipt frontier and two complete native deltas. The network
harness consumes those exact bytes; previous reports do not confer authority.

Root selected a fresh source-only network endpoint and finite config proposal:

| Fresh file | SHA-256 |
|---|---|
| `software/v5/delta/network_actual.py` | `1d3a7802790186a7ceb929fecc2bcdd99bc72a46049ce23f0f0795b379b4ea2c` |
| `software/v5/delta/network_actual_api.md` | `c4675e6f61284292e672a51c6704ebb68b8b6ae9053759cc53602a4de982ac57` |
| `software/v5/location/node_entry_services_available.mjs` | `02bbdf1223602aff512ae9cfadcc58f2b5e6efc02e1c1b65b34e3f14ebc75fb2` |
| `software/v5/location/available_descriptor.py` | `d3b215f59c0b4745562fdc76339a53f22d0fa009932dfecbef4fecfff6743fba` |

The independent reviewer source-cleared these exact boundaries. Read-only packet
inspection found 11 available semantic body hashes across 16 selected declarations
and no missing demanded definition/recursor body. Runtime is root's separate
exact-selection decision; this lane has launched no test, service, native call,
proof or Git operation. The broad v5 goal is not completed by source clearance.

### Central reliability defect discovered before launch

The frozen Node entry and Python controller made every failed descriptor command
terminal. Thus catching an unavailable origin at the caller did not permit trying
the next returned provider: the actual reader process was already dead. This was
a real availability-path obstacle, not a test-only inconvenience. Private peer-ID
filtering, a preknown replica endpoint, or a newly created budget would conceal it.

The fresh entry therefore recognizes only a narrow class of actual local TCP
connect failures: `syscall == connect` and an explicit OS connect-unavailable
code, or a bounded aggregate consisting entirely of those failures. All original
owner/service signals must still be live. It returns `DESCRIPTOR_UNAVAILABLE`
without a remote-authentication claim. The helper abandons the same existing
WorkflowBudget ticket, charges its entire reserved descriptor allowance, and
keeps the same channel and absolute deadline. Malformed IPC/descriptors,
authentication errors, unclassified failures and expiry remain fail-closed.

Root will alias the exact fresh Node entry to `node_entry_services.mjs` in a fresh
14-file adopted Node snapshot; all other existing role/source names and retained
runtime bytes stay unchanged. The original controller and mathematical transport
classes remain exact, not monkeypatched or replaced by fake subclasses.

### Decisive sequence without private holder knowledge

There are five actual location nodes: neutral reader/router, origin index-provider,
replica index-provider, and two fresh readers. Only three location children are
live concurrently. The neutral node neither indexes/publishes mathematics nor
stores/serves packets. Both consumers query theorem/equality/known-base-fold
features, not the desired result ID, export ID, snapshot ID or private provider ID.

Reader1 locates origin, searches, acquires and cold-admits the complete packet.
It reconstructs durable selected group/body custody from packet bytes and closes
all its mathematical/location owners. Replica indexes the exact received export
and uses reader1's independent retained stores, not origin's state.

Reader2 starts fresh and obtains an actual route result before origin dies. It
has performed no mathematical acquisition or admission. Root-approved sequencing
then closes origin HTTP/Node/stores and starts the real replica. Reader2 attempts
its genuinely returned stale peer, observes a charged typed unavailable result,
and spends its preallocated second route on the same original channel/deadline.
Only IDs already observed to fail by that reader may be skipped; no private
replica identity influences routing or candidate choice. Alternative discovery,
all acquisition and mathematical admission happen after origin closure.

The second reader opens actual DeltaImportSession authority over its newly
accepted closure, supplies groups/bodies from its own durable readback, and
requires a complete ordinary authoring context using only its locally adopted
foundation plus received semantics. No native frontend/Lean author call is made;
theorem ancestry remains in the checking packet rather than being expanded into
the ordinary-source frontend context. This is not a promise that all possible
future semantic demands are covered.

### Resource and evidence boundary

The config proposal fixes original workflow wall 480 seconds within the existing
600-second enclosing owner limit, two cold receivers, at most two cryptographic
receipt verifications and four native relation checks. Each cold receiver has
one 90-CPU-second admission reservation. Reader2's two routes, stale failure and
alternative search/acquisition share their original finite grants; no retry
allocation, deadline renewal or new mathematical proof is selected. These are
reservations, not observed CPU savings or duplicated resource charges.

The actual source-snapshot import closure is pinned and foreign v5 project
imports are refused. Provider/controller/Node telemetry and outer Job work remain
separate from application bytes. Finalization checks the original deadline again
after writing RESULT; `FINALIZATION-FAILED.json` overrides any earlier PASS text.
Cleanup attempts each owner independently and retains the original operation error
even if another closer fails. Same-host success, if observed, will not be reported
as independent-host availability, global search completeness or final v5 readiness.

## Actual01 failure and event-readiness successor (source-only)

Actual01 ended with `NETWORK_NO_LOCATED_INDEX_CONTACT` before formal search,
acquisition, receipt verification or native admission. Reader1's actual route
was empty. Origin's publication reported `ADVERTISED_HINT` with `error:null`.
The independent outcome audit owns the complete retained 210-binding census;
this section diagnoses the source seam, not a repeated execution of that audit.
All used actual01 source/input/evidence remains frozen.

Two tempting inferences are incorrect:

- `READY.known_peers == 0` is the application descriptor cache size, populated
  only by locate. It is not a measurement of the DHT routing table.
- The retained DHT default removes private addresses, but our adopted role
  explicitly supplies `peerInfoMapper: mapPeer`, which applies the configured
  owner egress policy and permits the selected loopback endpoints. The default
  private-address mapper is therefore not the identified defect here.

### Causal source argument, and its evidentiary limit

The exact adopted library is beneath
`product-local/v4-library-commons-02/commons-v4/overlay/node_modules`.

1. `@libp2p/identify/dist/src/identify.js:21` starts identify asynchronously from
   `connection:open`; its callback does not await identify before dial returns.
2. Identify learns the remote protocol/address information. The DHT topology
   listener forwards that event asynchronously; `kad-dht.js:335` applies the
   configured mapper and queues routing-table insertion. A connected transport
   is not yet an admitted DHT peer.
3. Our previous `allowQueryWithZeroPeers:true` both disables the empty-table wait
   and immediately resolves the initial-self-query barrier. In the retained
   `query/manager.js:95-130`, a query with no routing peers simply returns.
4. `content-routing/index.js:50-123` first records self as provider locally and
   only dispatches provider records for returned `FINAL_PEER` events. Zero such
   events is a normal generator completion, not necessarily an exception.
5. Our old publisher discarded every yielded event, including `QUERY_ERROR`,
   and equated nonthrowing completion with `ADVERTISED_HINT`. Our old route
   wrapper also discarded Node's termination diagnostic.

Thus the previous interface permits this execution order:

`dial completes -> READY -> publish/query exhausts empty -> identify/routing admission`.

It lacks the required happens-before edge from routing admission to a query.
That is a concrete software defect and a sufficient explanation of the observed
empty result. The retained actual01 records do not identify whether its publisher
race, its reader race, or both occurred: the relevant event/table diagnostics
were not retained. We do not retrospectively convert the plausible interleaving
into a measured timeline, nor pretend that a completed local write proves remote
provider-record placement.

### Selected smallest semantic repair

Root selected source-only fresh `maintained_roles_ready.mjs`, to be aliased to
`maintained_roles.mjs` in a separate exact Node snapshot. It restores the library's
`allowQueryWithZeroPeers:false`; no bootstrap/provider list is injected and no
sleep, polling loop, retry, larger cap or renewed deadline is introduced.

Startup itself still means only listening and attempted bootstrap dials. The
neutral no-seed bootstrap is therefore allowed to start. Application queries,
not startup, wait on the library's `peer:add` event and initial-self-query promise.
`QueryManager.run` combines the supplied original operation signal with shutdown
and early-exit signals; its `pEvent(...,{signal})` and
`raceSignal(initialQuerySelfHasRun.promise,signal)` both observe that combined
signal. An unreachable/empty network returns bounded incomplete/aborted evidence
at the original operation cap, rather than silently exhausting an unready table.
The initial background self-query is separately bounded by the existing service
lifetime and shutdown; it is not represented as charged per-query work.

An event barrier establishes only local query readiness. It does not guarantee
publication delivery, global connectivity, search completeness or a stable peer
set after the barrier. Churn may still produce an incomplete or empty result.

### Publication and routing outcomes

Fresh fixed-size diagnostics retain event, send-query, peer-response, final-peer,
query-error, provider-event and completed-local-provider-write counts, bounded
last error and actual routing-table sizes before/after the operation. Counters
describe yielded library events; they are not packet counts or wire-byte bounds.
All earlier transport/owner/service limits remain in force.

The only positive publication label is `HINT_DISPATCHED_UNACKNOWLEDGED`, requiring
at least one actual local `ADD_PROVIDER` write completion and no yielded query
error. The library's `network.js:164-191` sends this message without expecting an
answer; it yields `PEER_RESPONSE` after `_writeMessage`, while `stream.close` is
not awaited. Therefore even that label sets `remote_placement_confirmed:false`.
Zero writes, yielded errors or aborts are `INCOMPLETE`, with separate termination
and error information. Subsequent actual discovery is the evidence of usefulness.

Fresh `observed_route.py` uses the exact existing `ServiceLocatedWorkflow`, its
original `WorkflowBudget`, one original ticket and actual child channel. It
validates and preserves advisory diagnostics while using unchanged peer acceptance
and full allowance settlement. It creates no subclass, additional command,
contact, search grant or mathematical authority. Malformed diagnostics, channel
failure or expired owner deadline close the channel and remain fail-closed.

Fresh `network_actual02.py` changes only these integration seams: requires the
explicit startup/readiness descriptions, persists publication before judging it,
requires actual advisory dispatch rather than a nonthrowing iterator, and calls
the observed route helper. The retained mathematical packet and two-receiver,
origin-loss, same-channel stale/alternative path are unchanged. Its schema is
`DMKN_V5_ACTUAL_DELTA_NETWORK_V2`. Config additionally pins the exact fixed
`location.ready_source` path and binds its hash to the aliased role entry before
and after the operation; it adds no arbitrary topology/configuration field.
No successor runtime is selected by this note.

| Fresh source awaiting independent review | SHA-256 |
|---|---|
| `software/v5/location/maintained_roles_ready.mjs` | `9824559f55eca9b1e56786c14cbe090b74904d1786a915f124dc4101b0aa9683` |
| `software/v5/location/observed_route.py` | `9800b5fd3a1f922dcc2e59818916b2333f79004b7f4b6ed42eb89d40891740f1` |
| `software/v5/delta/network_actual02.py` | `f772cce4aa6c33bb1970c931d3483f932b102f97258789673dcad8ab497c4718` |

### Smallest decisive follow-up, not launch authority

Independent source review must first check the retained library's abort reach,
the no-seed startup distinction, exact accounting/settlement and diagnostic
semantics. The focused network discriminator needs only one neutral router, one
publisher and one fresh reader: publish once immediately after dial readiness;
query once immediately after fresh reader dial; require actual returned advisory
provider and authenticated descriptor, with the new event census. This performs
no mathematical calls. A separate no-peer bounded query can check abort behavior
if the reviewer judges the exact source argument insufficient; it must not
silently renew any existing allocation.

For the full endpoint, root may instead select one fresh actual02 operation after
review, preserving the original finite caps. Its previously unreached mathematical
and origin-loss suffix is substantive integration evidence, not a repeat of a
passing network campaign. Failure is retained and diagnosed; no automatic retry
is authorized. This lane launched no runtime, test, proof, build or Git action.

## Actual02: useful prefix preserved, partial-publication gate corrected

Actual02's readiness repair reached genuine reader1 discovery, authenticated
descriptor, formal search, exact packet acquisition, one receipt verification,
two native checks and durable semantic custody. Reader2 then obtained an actual
first route; origin fully closed; replica started. The full operation nevertheless
failed at `NETWORK_ACTUAL_FEATURE_HINT_DISPATCH`: the replica had two completed
local provider-record writes and two query errors involving departed origin and
reader1 contacts. Independent assurance owns the actual prefix/outcome audit.
Root reports outer41.09375CPU + .65625wrapper,52.795668wall and clean closure.

The Node outcome `INCOMPLETE/QUERY_ERRORS/error:null` was correct. The V2 harness
wrongly required zero query errors before trying the actual consumer route. This
was an overly strong harness liveness precondition, not a mathematical rejection
or evidence that both writes were ineffective. A peer disappearance should not
require every other reachable advisory advertisement to be error-free.

All used V2, readiness-role, route-helper and actual02 evidence bytes are frozen.
The whole operation remains FAIL; the successful prefix is not discarded or
repeated. No result is silently upgraded by changing its old status/report.

### Fresh source-only continuation selected by root

Root selected one retained-recipient continuation, not another full two-reader
campaign. `network_continue.py` subclasses only V2's orchestration `Campaign`;
its new provider method accepts structurally bound advisory publication outcomes
while the original owner remains live. Root's subsequent source-only refinement
removes positive local write count as a precondition for trying real discovery;
the precise current outcome table is in the compact API below.
It reuses the exact old reader, real workflow/channel, mathematical admission,
semantic import and cleanup code. No verifier or controller subclass is added.

`retained_custody.py` reads these exact closed reader1 artifacts only:

| Artifact under actual02/evidence | Bytes | SHA-256 |
|---|---:|---|
| `reader1-result.json` |135076|`8b907e77d4f86a9c3d9fa2815663c89b2a6def76057aba23c988b91ec9aacf9a`|
| `reader1-packets/delta-packets.sqlite` |679936|`5054fecc3de547baf8204a273d74d40102aad2aa2d23802b68de86995e4bcb03`|
| `reader1-modules/modules.sqlite` |131072|`dba5e1dc2d3c2533c76f157b085c8944b4dded360f0ee1764b6304f6c73d8541`|

Preserved SQLite files are opened `mode=ro&immutable=1`, with query-only and
trusted-schema restrictions plus bounded progress. Sidecar existence refuses
the continuation. Before/after file pins, exact packet digest/module/profile,
complete group/body map equality and exact reproduced formal-export record bind
the selected input. Report accepting flags and journals confer no new authority.
The original producer packet is not an input to this continuation.

The fresh run creates separate transient-origin and replica stores from those
recipient-held bytes. Its only fresh reader first discovers the transient origin
through a neutral router. After that origin actually closes, the same reader
tries its genuinely stale contact, then performs alternative location/search and
one cold complete admission through the replica. Private target/provider IDs are
not passed to reader choice. Exact expected IDs/bytes are compared only afterward.
The inherited real ordinary-context reconstruction remains part of this suffix.

Four Node lifetimes, at most three concurrent; one actual receipt and two native
checks maximum; no reader1 re-admission, authoring, guest or proof calls. The
original 480workflow/600outer wall and other selected ceilings stay unchanged.
Accounting and evidence are explicitly stitched across distinct finite operations,
not claimed to be one uninterrupted successful test. Same-host limitations remain.

| Fresh source submitted for independent review | SHA-256 |
|---|---|
| `software/v5/delta/retained_custody.py` |`bb94845d77cac6016ac1be7a1ac04fc822412c557fa9300309cd1b54d120a901`|
| `software/v5/delta/network_continue.py` |`1d80a4dff3d578d8c5f58793381bf997a9dc314cb9363137309203576c0c5cd2`|

The exact configuration replaces top-level `packet` with fixed three-pin
`retained_custody` and uses `DMKN_V5_DELTA_RETAINED_CONTINUATION_V1`. Its API is
`software/v5/delta/network_continue_api.md`. Root owns snapshot/configuration and
any launch after independent review. This lane has run no test, service, proof,
build or Git operation for the continuation.

### Root-directed publication refinement before runtime

Fresh `network_continue.py` now has SHA-256
`39aae5225fb97cbc9fea6095dc280543e5e0ffe906192642dec5cb7fef5e9d5d`;
`retained_custody.py` remains `bb94845d...`. The earlier `1d80a4df...` review
was source-only; no runtime used those bytes. This revision removes local-write
count as a general eligibility precondition. Source-shaped zero-write completion,
partial query errors and exactly classified per-operation timeout/event-cap
outcomes may proceed to the original bounded discovery attempt. Unclassified
errors, failed channels, exited processes and expired owners still refuse.
The exact allowed combinations are recorded in `network_continue_api.md`.

This is not making publication itself pass: every original report/error/census
is retained, actual discovery is still decisive, and every mathematical gate is
unchanged. No retry, extra request/grant or deadline extension is introduced.
Root and independent assurance must read the fresh hash before runtime selection.

### Root-reported continuation01 terminal outcome; independent audit pending

Root reports one terminal raw PASS for continuation01: 93 inclusive Job CPU
seconds plus1 wrapper CPU second, 103.9922wall seconds and clean closure. The
fresh reader completed one actual receipt verification, two native checks and
ordinary received import-context reconstruction. Independent assurance is
auditing the exact saved outcome; this paragraph records root's report, not an
independent adoption by this source-author lane.

Used `network_continue.py` (`39aae522...`) and `retained_custody.py`
(`bb94845d...`) are now frozen. The evidence remains actual02's audited reader1
prefix plus this separate retained-custody continuation, not one uninterrupted
pass or final v5 release. Controller84.5CPU includes fresh provider/store/index
construction and all synchronous owner work; it is not an isolated marginal
network or receipt-verification timing and must not be added again to inclusive
Job CPU. No repeat operation is selected here.
