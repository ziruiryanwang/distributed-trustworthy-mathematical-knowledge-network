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
