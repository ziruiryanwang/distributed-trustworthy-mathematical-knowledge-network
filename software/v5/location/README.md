# V5 advisory location boundary (source-only, not a routing release)

`protocol.py` defines exact domain-separated rendezvous keys, a strict bounded
descriptor request/reply, canonical Ed25519 libp2p identity labels and
owner-selected IPv4 egress. `workflow.py` supplies one finite locate-to-search
envelope. These files do not yet implement a DHT adapter or authenticate a
socket. A caller-supplied JSON peer field cannot establish an authenticated peer.
The future adopted Noise transport must supply the channel peer identity.

The intended sequence is:

1. Construct `OwnerEgressPolicy` from owner configuration and `WorkflowBudget`
   from one namespace, sorted query features, location limits and search limits.
2. `begin_route(features, stripe, event_cap=..., peer_cap=...)` reserves and
   immediately charges the full selected route allowance. Features must be a
   nonempty subset of the query;1..8features and stripe0..255 are finite values,
   not a mandate to enumerate all subsets or stripes.
3. A future adopted adapter enforces those caps and calls `accept_route` with
   bounded authenticated-identity labels, or `abandon_route`. Returned peer IDs
   and addresses remain hints. Every learned-address DHT/Noise dial must apply
   the same owner egress policy; validating only this result is insufficient.
4. `begin_descriptor(peer, route_key, ...)` privately binds the located peer,
   route key, random nonce, body cap and owner-clock expiry. The adopted Noise
   transport obtains a reply; `accept_descriptor` verifies the channel peer
   supplied by that local transport plus exact response bindings and egress.
5. `begin_search()` issues exactly one existing `SearchSession`/`SearchClient`.
   All offered providers share that session and its existing failure/accounting
   rules. No route/referral creates another session. Search capacity was reserved
   when the workflow was constructed, and its absolute deadline cannot extend
   past the original workflow deadline. Expired contacts are not used.

Every HTTPS dial rechecks the originally adopted endpoint, owner egress and
owner-clock contact expiry. A post-reservation predial refusal conservatively
settles its search ticket; it neither leaks a reservation nor refunds a new
attempt. This is deliberate conservative accounting, not measured wire usage.

Public mode accepts only numeric public IPv4, owner-listed ports and HTTPS.
The TLS name is a strict optional lowercase DNS A-label name. The fixed policy
is **owner/system CA trust only**: descriptors cannot select CA files, local
paths, client credentials, redirects or executable handlers. OS trust-store
updates remain part of the trusted owner environment; this is not an exact
pinned root-set or Noise-peer-to-HTTPS-operator identity proof. Mathematical
acceptance never relies on either identity. Loopback tests need an explicit
owner list of exact127.0.0.1ports and do not enable arbitrary local dialing.

Descriptor body bytes and the whole search reply allowance share one finite
capacity. Invalid bodies charge before parsing; unknown descriptor transport
outcomes charge their whole reserved body cap. Duplicate descriptors still
consume attempts and bytes. Duplicate endpoint storage is bounded; different
endpoints cannot silently exceed the contact cap. Reports distinguish reserved
capacity from actual used search bytes. Headers/request bodies are additional
separately reported costs, not misnamed response bytes.

**DHT query events are not DHT wire bytes.** The retained Kademlia library uses
protobuf streams with its own framing; onProgress counts do not bound all
inbound traffic, identify/noise handshakes or background maintenance. These
files explicitly report DHT bytes as unmeasured. A later adapter must preserve
process/time/connection/event/storage containment and state any additional
wire-metering policy honestly. The hard external resource supervisor remains
required. No total-network-bandwidth guarantee is established by these classes.

Remote correctness, usefulness, index truth, availability and global coverage
are not descriptor assertions. V5's existing authenticated offer/candidate path
still applies; acquisition and root-owned mathematical admission are separate.
The selective-coverage/maintenance model and retained-source map are in
`research/cycles/v5-2026-10-07/DISCOVERY-INTEGRATION.md` under the canonical root.

`test_location.py` prepares12 focused native-free control groups using mocked
HTTP only. Root owns exact selection and launches; source existence is not a
test result, real DHT qualification, or a finished deployable release.
