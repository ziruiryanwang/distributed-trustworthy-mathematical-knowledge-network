# Narrow maintained location adapter: concrete source map

Source/theory continuation of the root-selected `location/` boundary. No Node
adapter or runtime is launched by this document. Python pure controls have
independent source clearance; their actual outcome is separate. Frozen v4,
its state and its dependency tree remain read-only.

## Preserve one data path

The adapter locates an index service and obtains a descriptor. It does not run
the old Python fragment bridge, carry module/certificate payloads, or decide
mathematical acceptance. An owner controller passes private WorkflowBudget
route/descriptor tickets to the locally adopted Node adapter through bounded
IPC. Returned peer IDs and raw descriptor bodies go back to the same workflow.
The resulting one SearchClient uses the existing HTTP offer/candidate path.

The controller must treat Node as selected local transport code, not as a remote
provider response: only the actual Noise connection supplies authenticated_peer.
An arbitrary JSON file cannot recreate channel authentication. The descriptor
still remains advisory even when the channel is authentic.

## Explicit implementation map

| New location source | Reuse | New responsibility |
|---|---|---|
| `runtime.mjs` | Exact retained Node/libp2p packages and vendor-patched dependency identities | Owner-only local dependency selection; no npm/install, peer-supplied path or dynamic package name. Resolve a fixed import table beneath the selected dependency root; later packaging supplies its own pinned root. |
| `protocol.mjs` | Python location/protocol.py specification and fixed test vectors | Sorted-key canonical ASCII-field JSON, rendezvous digest/CID, exact descriptor fields, PeerID through retained parser with Ed25519 profile, identical owner egress. No new cryptography. |
| `intent.mjs` | Frozen QuotaDatastore class and atomic intent pattern | Fresh separate v5 state; v5 provider prefix and exact route keys; local publish/withdrawal guard, including reprovider writes after withdrawal. No old database migration. |
| `maintained.mjs` | Selected createLibp2p/tcp/noise/yamux/identify/kadDHT options and bounded provider search | Stable owned identity, owner-gated bootstrap/learned addresses, namespace-keyed hints, finite query/descriptor/service lifetime, expiry/reprovide, bounded descriptor streams, orderly stop. No old fragment protocol or bridge. |
| `transport.mjs` | Exactly retained TCP transport/upgrader and raw stream interface | One service-wide allowance for attempted outbound TCP connections, admitted inbound upgrades, raw receive forwarding and prebuffer send admissions, including background/failed work. No dependency-file edits; packet/kernel and pre-upgrade allocation are outside this byte counter. |
| `controller.py` (only if root selects its launch seam) | Existing finite child supervisor discipline, WorkflowBudget | One adopted Node adapter process; bounded IPC, exact ticket binding, single absolute deadline, conservative unknown-outcome charges. Root retains runtime launches. |

A route digest becomes a raw-codec CID whose SHA256 multihash bytes are the
already computed32-byte route digest. Do not apply the old
`DMKN-DHT-KEY-V1(namespace,key)` hash on top or use its fragment key regex.
Public key generation remains Ed25519; changing identity format requires an
explicit profile change rather than broadening Python label validation silently.

Prefer one new DHT protocol `/dmkn/v5/location-kad/1.0.0` for location metadata,
with namespace and role already cryptographically separated in each key. This
avoids requiring a fresh disjoint overlay bootstrap for every formal namespace.
A provider may initially serve only one owner-selected namespace/role. Its
descriptor stream protocol is separately versioned
`/dmkn/v5/index-descriptor/1.0.0`; request fields bind the exact namespace/key.
Neither protocol communicates with the frozen v4 namespace protocol.

The owner selects a finite explicit supported route vocabulary (at most its
configured advertised-key cap), consisting of singleton features and any chosen
conjunctions/stripes. It does not enumerate the power set of an object's features
or all256stripes. Exact predicates can later be demand-managed under a separately
funded policy, but no hidden automatic advertisement expansion is permitted.

## Retained runtime facts which must not be lost

Read package.json pins: libp2p3.3.11, kad-dht16.4.5, tcp11.0.28,
noise17.0.0, yamux8.0.1, crypto5.1.23, peer-id6.0.15,
identify4.1.14 and multiformats14.0.5. The full retained package-lock and
dependency manifest, not just these top-level version strings, bind the runtime.
The retained `VENDOR-PATCHES.patch` changes local-ID-path bucket splitting and
provider expiry behavior. Replacing this tree with upstream packages of the
same version would therefore be a different implementation and must not happen.

The existing QuotaDatastore already accepts a selected providerPrefix. Reuse
that property with a fresh `/dmknv5/provider` state. The old IntentQuotaDatastore
hardcodes `/dmkn/provider` and fragment logical keys; it cannot be reused
unchanged. New intent operations should keep the same synchronous SQLite
transaction around intent/provider/publication changes. `_put` of a self-owned
provider record checks the live durable intent in that transaction, preventing
a queued renewal from resurrecting withdrawn intent. Remote old hints can remain
until expiry; withdrawal is not instantaneous global deletion.

## Egress and endpoint trust are distinct gates

Outbound DHT/Noise learned addresses must pass connectionGater policy on every
dial, not merely result filtering or bootstrap validation. Public-mode addresses
are canonical direct `/ip4/<public>/tcp/<owner-listed-port>[/p2p/<id>]`, and an
embedded ID must equal the targeted peer. No DNS, relay, private or loopback
fallback. The same peerInfoMapper filters stored learned addresses, but mapping
alone is not the security boundary. Limit each peer's retained addresses.

Inbound remote source ports are normally ephemeral: do **not** apply the
outbound destination-port allowlist to them. The inbound gate checks allowed
remote address class, exact owner bind/listen policy and configured connection/
stream/resource caps. This distinction is needed for actual public operation,
not a reason to weaken outbound SSRF protection. Local tests still bind only
the explicit loopback test mode and finite endpoint list.

Python's current numeric IPv4 rule is from the pinned Python3.14 ipaddress
classification, plus explicit multicast/reserved/link-local/loopback/unspecified
rejection. The JavaScript gate must implement the same finite prefix rules:
deny0/8,10/8,100.64/10,127/8,169.254/16,172.16/12,192.0.0/24
(except192.0.0.9 and.10),192.0.2/24,192.168/16,198.18/15,
198.51.100/24,203.0.113/24 and224/3. Read the pinned stdlib constants;
do not reuse v4's slightly different blacklist without reconciliation.
Cross-language boundary vectors must cover every interval endpoint and exception.

An obtained descriptor's HTTPS address separately passes the Python owner gate
and is rechecked before every HTTP dial. It may be operated by a different
entity than the Noise peer. That is an advisory referral, not authenticated
same-operator ownership. Fixed system CA trust is owner-controlled; no descriptor
can provide a CA/path, secret, script, header, redirect or TLS downgrade. Remote
identity never substitutes for mathematical admission.

## Bound the right resources

Current Python `routing_peer_slots`/`peer_cap` reserves the **returned provider
ID slots**, not a measured count of all routing intermediates. Intermediate DHT
query dial/send/response attempts consume the selected full event allowance.
`network.js` emits `dialPeerEvent` before openStream and `sendQueryEvent` before
the RPC. The adapter progress guard must abort before exceeding its ticket,
with no new allowance for repeated peers, failures or duplicated hints. It
reports claimed/observed counts separately from the full prepaid allowance.
An operation-local AbortController is passed through the actual DHT options;
only adopted `kad-dht:query:*` progress events consume this allowance. Refused
predispatch dial/send callbacks throw to prevent the dispatch; terminal error/
path-ended notifications never throw into the retained Queue listeners. An
already-aborted `tcp:open-connection` hook also throws before net.connect;
ordinary TCP progress cannot itself spend the DHT event allowance. This avoids
the retained TCP abort-listener-registration race. Already-admitted in-flight
work remains charged and may finish its cancellation asynchronously.

Background identify/ping/routing maintenance/reproviding are separately funded
service activities; they are not silently charged to zero because a query
handler did not observe them. Service lifetime, connection/stream caps, metadata
quota, maintenance frequency and selected advertise-key count all need finite
owner inputs. Their amortized work is part of the growth operating model.

The retained `kad-dht/network.js` calls `pbStream(stream)` without maxDataLength.
`utils/stream-utils.js` sets no default length cap in that branch; incoming
`rpc/index.js` can process several messages while resetting its timeout. A
query-event ceiling is therefore **not** a hard whole-network byte or hostile
message-allocation bound. Initial adapter source must not invent that claim.
Root-owned process/memory/time containment bounds damage, but by itself cannot
promise fair useful service under a hostile flood. If public deployment needs
a protocol message/stream budget, select the narrow pinned-version boundary
explicitly rather than secretly monkey-patching the dependency or claiming
maxReadBufferLength bounds total protobuf accumulation.

The newly selected source-only `transport.mjs` now wraps the retained transport
instance and the supplied inbound/outbound upgraders. On outbound dial it charges
before `_connect`, including failed connects. On inbound it charges at entry to
the upgrader, after raw socket allocation but before Noise. The pinned TCP source
constructs its raw connection and enters that upgrader synchronously before
socket data events; its socket callback calls `this.onData` dynamically. The
wrapper refuses a prepopulated raw read/write buffer, then wraps `onData` before
forwarding received bytes and `send` before write-buffer admission. This is an
explicit pinned-version instance adapter, not a hidden vendor-file patch.

For configured receive/send limits R,S, synchronous check-and-charge gives
`sum(raw bytes forwarded) <= R` and `sum(raw send admissions) <= S`, across
all attached connections and foreground/background service work. Refused chunks
are counted separately; outgoing admissions are not refunded after lower-layer
failure. Overflow aborts all current raw connections, closes listeners and stops
the finite service; later attempts cannot receive a fresh budget. TCP/IP headers,
kernel buffered/refused packets and allocated refused chunks are not bounded by
these counters. The first refused incoming upgrade also allocates a raw socket
before the gate. External Job memory/CPU/wall containment remains mandatory;
these bounds do not establish hostile-flood availability or per-query bandwidth.
Per-protobuf length policy remains separate: aggregate admitted input is bounded,
but its decoder complexity must still fit the selected process budget.

Our new descriptor protocol can be strictly bounded now: exactly one request
and reply per stream, fixed4-byte body-length prefix, request<=2048B,
reply<=the private1024..4096Bcap, exact EOF/half-close, bounded read chunks,
abort at owner absolute deadline. Reuse the retained framing discipline but not
its64KiB JSON default, sender-selected object ordering, bulk file transfer or
fragment schemas. No unbounded eager `toArray`/concatenation is needed.

## Decisive controls, not another broad routing campaign

First prepare cross-language pure vectors: exact keys and request/reply bytes, all IPv4
prefix boundaries, PeerID/address identity, prefix/body/EOF limits, original
absolute deadlines and cancelled publish-intent renewal. These are changed
boundaries; do not rerun the old fragment/mathematics/proof campaigns.

Then, only after exact source/dependency review and root selection, one bounded
actual scenario may begin with namespace/features and replaceable bootstrap
peers but no injected index HTTP endpoint. Its location result must feed the
same WorkflowBudget, actual offer and candidate methods on retained index bytes.
Provider loss/withdrawal testing should target only the new maintenance boundary,
not repeat already adopted custody-loss or cryptographic proof operations.
Expected logarithmic routing and favorable selective coverage remain conditional
theory, never inferred from a small same-host scenario.

Current `test_location_node.mjs` has13 proposed groups. They use actual retained
SQLite, TCP/raw stream and DHT Network methods with fake sockets/RPC where
necessary, and never open a real listening socket or execute a real DHT query.
The IPv4/domain fixtures are independently written Node controls, not yet an
executed Python/Node vector interchange. The startup control creates state and
identity but stops before network start. The new root-selected
`run_node_controls.mjs` binds all5,894 overlay files plus the two bundled Node
files against the exact retained release manifest before/after imports. All
hashing/control work shares one supervised Job; its internal CPU breakdown is
not an extra charge. A resolve hook refuses imports outside builtins, exact
snapshotted source and manifested runtime. The selection remains pending
independent source review and root launch; none of these controls is yet a pass.
