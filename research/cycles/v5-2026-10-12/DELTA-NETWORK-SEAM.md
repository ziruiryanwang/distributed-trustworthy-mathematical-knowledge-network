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
