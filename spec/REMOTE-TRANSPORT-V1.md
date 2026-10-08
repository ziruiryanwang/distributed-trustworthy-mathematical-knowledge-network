# Remote transport v1: implementation contract addendum

2026-09-23. **Proposed implementation contract; not implemented, independently
reviewed, or qualified.** Read-only source-grounded design for the next central
module after the genuine producer/replica/receiver return. No key generation,
service, external connection, or product change was performed for this note.

This is an explicit narrow implementation addendum to
[Operational Corpus v1 network](OPERATIONAL-CORPUS-V1-NETWORK.md), not a claim that
the current product implements that older NET1 concept. In particular, this
profile does not adopt NET1's mutual Ed25519 identities, bidirectional sessions,
new message framing, service-ticket system, or hard handshake-byte claim. It
adds authenticated remote carriage to the implemented immutable catalog/page/
bundle protocol while preserving local mathematical admission. Historical
accepted sources, installations, evidence and specifications remain unchanged.

## Decision and precise claim

Select **owner-configured IPv4 + server-authenticated, exact-certificate-pinned
TLS 1.3**, carrying the existing bounded read-only HTTP application routes.
Use the pinned Python distribution's standard `ssl` implementation; no new
cryptographic primitive, public CA, global identity service, or mandatory
central server is introduced. Clients need no private key. A server serves only
explicit owner-exposed public inert views; this profile has no private-data
authorization and does not claim to identify clients.

For a configured endpoint E and certificate digest p, no application request
bytes may be sent until TLS 1.3 completes and SHA256(exact peer leaf DER) = p.
This establishes possession of the private key corresponding to the selected
certificate under the TLS/runtime assumptions. It establishes neither honest
catalog contents nor mathematical validity. The existing rule remains:

`candidate acquired != theorem admitted`; only the receiver's independent
native Lean checking can advance its accepted context.

Current selected code is deliberately loopback-only, not remote-capable but
untested. A fresh local operator test alone cannot satisfy the network goal.
Manual SSH remains an optional external route; it is not selected as the new
product's only remote capability because deployment currently depends on an
unqualified extra service, independently configured keys and port forwarding.

## Version and public configuration contract

- New immutable **configuration schema 5**, with fresh installation/state;
  reject schema 4 at this cut. No used-state mutation or in-place migration.
- SQLite physical schema stays **4**: endpoint records are existing strict JSON
  records and table layout/indexes need no change. Config digest continues to
  bind each fresh database. Do not equate config version with SQL schema version.
- Mathematical formats, foundation, stage-plan schema **2**, catalog/page/view
  schema **2**, object IDs and the `/v1/bundle/…` payload route remain unchanged.
- Each endpoint carries an explicit transport profile; no plaintext fallback,
  negotiation downgrade, remote redirect, DNS lookup or environment proxy.
- Retain at most two owner-configured outgoing aliases in this first cut; add
  zero or one TLS listener. No contact advertisements, transitive dialing or
  dynamic discovery is part of this change.

`configure --network ABS_FILE` is mutually exclusive with existing `--peer`.
Read strict UTF-8 JSON, at most 16 KiB, with exactly this shape (placeholders
below describe values, not accepted literal strings):

```json
{
  "schema": 1,
  "peers": {
    "beta": {
      "profile": "pinned-tls13-v1",
      "host": "192.0.2.20",
      "port": 48191,
      "certificate_sha256": "64 lowercase hex characters"
    }
  },
  "listeners": {
    "public": {
      "profile": "pinned-tls13-v1",
      "bind_host": "192.0.2.10",
      "port": 48191,
      "certificate_file": "ABS_PEM_CERTIFICATE_FILE",
      "private_key_file": "ABS_PEM_PRIVATE_KEY_FILE"
    }
  }
}
```

Documentation-only example addresses are not deployment targets. Alias/listener
entry key sets are strict: TLS peer
`{profile,host,port,certificate_sha256}`; loopback peer `{profile,host,port}`
with host exactly `127.0.0.1`; raw TLS listener
`{profile,bind_host,port,certificate_file,private_key_file}`. No extra keys.
Alias/listener
names use existing `SAFE_ID`; ports are actual integers in 1..65535. Hosts must
equal canonical dotted-decimal `str(IPv4Address(value))`, excluding unspecified,
multicast and limited-broadcast addresses. Private and loopback literals are
allowed; IPv6, hostnames, zones, URLs and wildcards are refused. The owner
explicitly approves the destination or local interface; peers cannot supply it.
The listener must bind precisely that local address/port or refuse. No
`0.0.0.0` convenience fallback, route provisioning or firewall change occurs.

Fresh schema-5 `--peer alias=port` keeps the existing local-only development
mode by materializing `{"profile":"loopback-http-v1","host":"127.0.0.1",
"port":N}`. Its previous HTTP/loopback behavior is unchanged and explicitly
unauthenticated. It cannot be combined with `--network`; the network file may
also contain explicitly shaped loopback peers if required. No automatic choice
between the two profiles is permitted.

**One default decision:** no `--network` and no `--peer` means offline
configuration (`peers:{}, listeners:{}`). Plaintext is available only through
explicit `--peer` or an explicitly tagged `loopback-http-v1` network-file entry,
always at exactly `127.0.0.1`; it is never the inferred default for a remote
endpoint. The network-file listener map accepts only `pinned-tls13-v1`. A legacy
`serve --port` remains an explicit local-only owner action, not a configuration
side effect. No listener is started by configure, init, peer_find or peer_acquire.

The immutable config adds `listeners` and stores normalized endpoints plus
certificate/key locators and exact byte/hash pins for the chosen TLS listener.
Each normalized TLS listener has exactly these keys:
`{profile, bind_host, port, certificate, private_key, certificate_sha256}`.
`certificate` and `private_key` are exact `{path, bytes, sha256}` file-byte pin
records. The input network file's `certificate_file` and `private_key_file`
fields are replaced by these pins before creating any node state. Generic
`load_config` checks shape, bounds and canonical path syntax without reading
either identity file. Only the explicit configure/service paths may read them.
Certificate pin is separately SHA256 of DER, not of PEM. Existing snapshots,
remote handles, acquisitions and replica authority continue binding the **whole
endpoint**, now including profile and certificate pin. Host or pin changes
therefore cannot silently reuse earlier remote handles.

Cross-profile snapshots are invalid even when address, port and catalog digest
coincide. `peer_snapshot`, `remote` and acquisition endpoint comparison includes
profile and certificate pin before any connection; changing a profile requires
new state/handles. New TLS aliases cannot reinterpret previously recorded local
plaintext observations. Replica custody may still expose the same inert bytes
through a different separately authorized listener: transport changes custody
reachability, not mathematical object identity or acceptance.

No mutable key rotation protocol is introduced: changing a pin, endpoint or
server identity requires an explicitly configured successor node in this first
profile. Retain old node/evidence. This is a stated operability limit, not a
claim of indefinite key lifecycle support.

**Usability boundary:** this constraint makes initial remote operation implementable
but does not solve long-term operation. Certificate reissuance (even for the same
key), address change or compromise requires coordinated explicit successor
configuration at affected owners. No in-place trust rotation, immediate remote
revocation, automatic historical-state migration or guaranteed preservation of
private/unexposed work follows. Existing sessions use their loaded identity until
their bounded stop; a newly refused grant is not retroactive revocation. The
complete product still needs a tested owner successor/custody handover or a
separately designed safe update path before claiming durable long-lived service.

## Key material and runtime boundary

The owner supplies one PEM leaf certificate and a matching unencrypted PEM
private key, each at most 16 KiB; leaf DER is at most 8 KiB. The cryptographic
key algorithm must be supported by the selected TLS-1.3 runtime. No custom
certificate parser or self-signature verification is required for exact-byte
pinning: TLS supplies key-possession authentication and the locally supplied
certificate digest supplies identity selection. A pinned self-signed certificate
is allowed; subject/SAN/CA/name and validity dates do not select the endpoint
or extend any resource grant. Certificates are not political identities.

The certificate must have exactly one CERTIFICATE PEM block and no chain or
extra blocks. The key must be a supported private-key PEM and match on
`load_cert_chain`. Supply a password callback that refuses instead of allowing
OpenSSL to prompt for an encrypted key. No passwords on command lines,
environment variables, JSON, logs or network messages. Encrypted-key unlocking
and a product key-generation command are deferred; the release needs a tested
owner provisioning procedure before it can claim usable TLS setup.

Keep both files in an owner-controlled **dedicated directory outside install,
state, scratch and Lean runtime**, on local fixed NTFS. Paths must be absolute,
canonical, non-reparse and not roots/alternate streams. This is an explicit
TLS-only read exception, not an enlargement of `Domains.require_read` or native
stage domains. The owner restricts key-file ACLs to the operating account and
trusted administrators; shared/untrusted local writers are unsupported. ACL
verification must be documented and checked during operator qualification;
pathname checks alone do not establish secrecy or hostile-account isolation.

Only `configure` and the owner service worker read private-key bytes. Generic
agent operations validate the locator schema, not the key contents. Recheck
certificate/key byte/hash pins immediately before creating each service TLS
context, then require the loaded certificate's DER digest to match config.
This is a start-of-session identity check. An already loaded TLS context
continues to represent its selected identity; this profile does not promise
instant detection or revocation when an on-disk key changes mid-session.
Every later session must recheck the pins and refuse changed identity files.
Do not copy secrets into installation archives, bundles, stage inputs, generic
supervisor input snapshots, request/reply bodies or evidence exports. Evidence
may include locators, lengths and hashes, never key/certificate raw bytes or
TLS secrets. Sanitize TLS errors to fixed codes, not raw library messages.
This reduction must happen inside TLS/configuration helper boundaries, before
errors reach `peer_node.prepare`'s `OSError` detail, `service_worker.main`'s
generic detail, or `manage.main`'s generic detail emitters. Their current broad
handlers are not a sanitizer. Re-raise only a fixed-code exception without
the original library string; never attach raw exceptions to public events.

Construct `SSLContext` directly, do not enable key logging or consume ambient
`SSLKEYLOGFILE`/CA settings. Record the selected Python and OpenSSL version in
qualification; the existing runtime-distribution trust assumption includes the
SSL extension/libraries and is not whole-runtime binary attestation. Pin/hash
checks assume stable owner files and do not defeat a malicious local account.

**Strict SSL availability:** before creating fresh state for a TLS configuration,
require importable standard `ssl`, `HAS_TLSv1_3`, `HAS_ALPN`, usable
`TLSVersion.TLSv1_3`, minimum/maximum version enforcement, ALPN configuration and
server ticket disabling. Construct the required client/server contexts locally
to check these operations; do not dial or bind. Missing features, unsupported
certificate/key algorithms, or rejected version/context settings produce a fixed
`TLS_PROFILE_UNAVAILABLE`/`TLS_IDENTITY_UNUSABLE` refusal before state creation,
never lower-version/plaintext fallback. Repeat feature/context checks in the
actual selected TLS worker; normal outgoing requests fail terminally with
`REFUSED/TLS_PROFILE_UNAVAILABLE` when the runtime cannot supply the profile.
Preserve generic outer unknown-outcome handling if a worker itself fails.
Offline/plaintext-only configuration need not import or pretend to qualify SSL.
Freeze actual Python/OpenSSL version evidence in the implementation test packet.

## Connection, HTTP authority and finite resource behavior

Client and server contexts set minimum = maximum TLS 1.3; compression off;
ALPN exactly `math-commons-http/2`, with successful selection required. Do not
use early data, renegotiation or client session reuse; server session tickets
are disabled. The client intentionally uses no CA/hostname validation, because
**exact leaf pinning is mandatory before HTTP**; missing/mismatching/oversize
leaf or wrong TLS version/ALPN closes the socket without a request. Server
does not request a client certificate. No auth failure downgrades to HTTP.

For TLS only, HTTP authority is fixed `Host: math-commons`, exactly once. It is
application-profile separation, not peer identity. This avoids conflating the
client's remote/public address with the server's local bind address and permits
explicit owner-managed NAT forwarding. ALPN and this Host are fixed profile
constants, not arbitrary owner or peer headers. The old loopback profile keeps
`Host: 127.0.0.1:PORT`. Existing method, route, header, content-type, length,
compression/chunking/redirect refusals and one-request-per-connection remain.

Client: TCP connect <=2 seconds, TLS handshake <=5 seconds, existing transfer
deadline <=30 seconds measured from **before connect**. Each bound is truncated
to the remaining overall deadline. Use `do_handshake_on_connect=False` and an
explicit deadline-bounded handshake; restore application I/O timeout to
`min(5 seconds, remaining transfer)` afterwards. Close on timeout without retry.

Server: count and charge every accepted TCP connection **before** TLS; one live
connection and backlog one remain. Handshake <=min(5 seconds, remaining
30-second connection envelope, remaining service session). TLS/context setup,
view authentication and listen preparation consume the original service clock;
no readiness after exhaustion. Existing 360-second owner service maximum,
120-CPU-second/256-MiB service Job and 128-connection maximum remain. Client
calls retain their outer 120-second/1024-MiB supervision. Measured overshoot may
occur under polling; exceeding the selected envelope never becomes a pass.

**Honest byte accounting:** current send/receive counters cover plaintext HTTP,
not TLS handshake/record or TCP overhead. Standard `SSLSocket` does not provide
a pre-parser hard handshake-byte quota. This profile therefore makes no such
claim: it bounds handshake time, accepted-connection count and process memory/
CPU, checks leaf size after handshake, and relies on the maintained TLS runtime
for protocol parsing. Do not label existing `max_bytes` a total-link-byte limit.
A future hard transport-byte requirement needs a separately reviewed bounded
BIO/network adapter; it is not silently implied here. Public-link flooding and
host-level denial of service remain availability assumptions.

## CLI, status and state semantics

- `manage serve`: retain mutually exclusive legacy `--port N` and new
  `--listener NAME`. New listener comes only from bound config; requests contain
  that name, never arbitrary key paths or remotely supplied hosts.
- The service worker's exact request schema permits **exactly one** of `port`
  and `listener`; it resolves the latter locally and authenticates the same
  committed view/publication/custody before opening a listener.
- `manage host`: preserve `finite-loopback-host-v1` grant semantics unchanged.
  Add `schema:2, profile:"finite-pinned-tls-host-v1"`, replacing `port` with
  `listener`; all other existing grant keys and finite limits remain. Grant and
  journal replay bind config/listener exactly. No timer/counter reset or implicit
  renewal. Host-manifest/slot envelope schemas may stay 1 because the nested
  grant has an explicit version/profile; parsers dispatch strictly by it.
- Finite hosting remains owner-funded sessions, not a daemon, autostart or
  indefinite uptime. Existing per-grant and lifetime journal ceilings persist;
  exhaustion stops safely without deleting counters. The TLS module does not
  solve lifetime rollover, unattended key renewal, peer replacement, backup or
  long-term custody. Qualifying bounded remote sessions must not relabel those
  continuing-operation obligations as complete.
- Ordinary `peer_find`/`peer_acquire`, builder schemas and success replies stay
  unchanged; peer aliases select bound profiles. Discovery/transfer still return
  candidate-only, no native acceptance and zero native stages.
- Client errors are terminal ordinary `REFUSED` with fixed codes
  `PEER_TLS_HANDSHAKE_TIMEOUT`, `PEER_TLS_PROTOCOL_REFUSED`,
  `PEER_TLS_PIN_MISMATCH`, `PEER_TLS_CERTIFICATE_BOUND`, or
  `PEER_TLS_HANDSHAKE_FAILED`. Existing connection/unavailability/content errors
  keep their meaning. No candidate/head advance on failure; charges/partial
  evidence remain. Outer-process failure remains `accepted:null`/unknown and
  uses existing explicit recovery rules, not a fictional terminal TLS refusal.
- Local listener/key/context errors produce `SERVICE_REFUSED` with fixed
  `TLS_IDENTITY_CHANGED`, `TLS_IDENTITY_UNUSABLE`, `TLS_PROFILE_UNAVAILABLE`,
  `LISTENER_CONFIG_REFUSED` or existing local-failure codes before readiness.
- Public observations/readiness add `transport_profile`, actual `bind_host`,
  actual `port` and server certificate DER SHA; client events record the exact
  public endpoint/pin and whether its pin check completed. Readiness remains a
  historical observation, not current liveness or mathematical acceptance.
- Service observations separately count accepted connections, TLS handshakes,
  completed TLS handshakes and refused peer connections. They carry constant
  byte-accounting scope `plaintext-http-only`. No client-authentication claim.

Each client `_get` appends one bounded event row with exactly
`{profile, endpoint, phase, pin_verified, http_request_started}`. The endpoint
is the complete public normalized endpoint, never a key locator. Initially
both booleans are false; `pin_verified` becomes true only after successful
version/ALPN/leaf-pin checks, and `http_request_started` becomes true immediately
before sending HTTP. A catalog-plus-page operation has two rows, not one
aggregate boolean. The loopback profile never reports a verified TLS pin.
No raw certificate or exception is recorded. Bound each ordinary operation to
at most two transport rows, with a finite phase vocabulary fixed in code.

For TLS hosting, derive the expected public identity exactly as
`{profile, bind_host, port, certificate_sha256}` from the immutable config's
listener selected by the grant. Reconcile observations and readiness against
that identity without reopening a key file. A schema-2 TLS grant cannot be
interpreted as a schema-1 loopback grant, or vice versa.

In the TLS hosting profile only, malformed/failed peer connections are bounded
expected refusals, not automatic permanent hosting failure: classify them
separately and allow later valid requests within the original session/grant.
By contrast changed local view/key bytes, unavailable authority, quota-envelope
violation, supervisor failure or uncertain cleanup is fatal and cannot authorize
another slot. Record a fixed `fatal_error` and halt. Natural request/time limit
with only peer refusals is normal bounded completion, **not evidence that an
honest consumer was served or a requested duration was delivered**. Legacy
hosting's old `last_error` rule remains unchanged for historical compatibility.
In particular, do not reuse `_serve_loaded`'s current blanket
`WireError/OSError -> last_error; continue` for TLS. Keep local selected-view
file reads and digest validation outside the peer-error classification; missing,
changed or unreadable local payloads are fatal local faults. Bounded handshake,
request syntax and connection failures may increment refusal counters and
continue. Hosting accepts such counters but rejects every `fatal_error`.

## Exact implementation seams and pre-change gate

All paths below are relative to selected editable
`product-local/integrated-frontend-source-03`; create a separately named reviewed
successor cut before implementation, do not edit a used installation.

| Seam | Required change |
| --- | --- |
| `manage.py::configure`, parser | Config 5; strict network-file parsing/normalization; mutually exclusive options; TLS-only identity pinning; add listeners. No network during configure. |
| `py/node.py::load_config`, `py/domains.py::from_config` | Accept exactly new config version; strict tagged endpoint/listener shapes; leave native domain record/plan schema unchanged. |
| `py/peer_node.py::find/acquire/replica_custody` | Pass complete endpoint, not just port, to transport. Preserve exact endpoint binding in every snapshot/remote/acquisition/custody record. |
| `py/peer_service.py::_get/fetch_catalog/fetch_page/acquire` | Tagged profile, deadline-bounded TLS/pin gate before HTTP, fixed TLS Host, precise refusal mapping. Preserve canonical/wire consumption. |
| `py/peer_service.py::_serve_loaded/serve` | Explicit locally resolved listener; TLS setup/handshake; readiness identity; split bounded peer refusals from fatal local faults. Plain entrypoint cannot select remote binds implicitly. |
| `manage.py::serve`, `py/service_worker.py::operation` | Listener-name grant, exact request shape, TLS identity reads only in worker, same authority check before serving. |
| `py/hosting.py::parse_grant/request_for/charge/reconcile` | Tagged TLS grant; exact listener/profile/cert observations; safe terminal classification; unchanged durable precharge/quiescence requirements. |
| `API.md`, `PEER.md`, `HOSTING.md`, `QUICKSTART.md`, package/build bindings | Actual supported profile, provisioning/pin exchange, no public deployment or direct-network qualification until tested; updated full-file-map audit. |

Keep TLS helpers in the already pinned `peer_service.py` for the first slice.
Current hosting has 15 input pins plus its grant, exactly the supervisor's
16-pin bound; naively adding a module or certificate/key pins breaks that path.
Config pins bind TLS identity descriptors; workers recheck identity bytes.
Never put the private key into generic pin/snapshot machinery. If extraction
into a new module becomes necessary, explicitly revise/review pin-count policy
and all lists; do not silently drop existing code/runtime pins.

**Before source changes**, an independent reviewer must check these exact schema
shapes, TLS pin-before-request order, secret-read path, hosting failure taxonomy,
and compatibility/accounting deltas against the caller seams. Resolve defects in
this addendum first. Freeze one successor source allocation and a finite test
plan. Contract review is not software qualification and does not require another
round of general architecture brainstorming.

## Acceptance gates, without external binding

1. **Native-free contract tests:** valid/invalid config versions and endpoint
   types, canonical addresses, conflicting flags, listener names and immutable
   pin bindings; no DNS/proxy/redirect/plaintext fallback. A socket double must
   observe the selected nonloopback destination and bind tuple (not an unnoticed
   `127.0.0.1` substitution). No actual nonloopback binding is required here.
2. **Real separate-process TLS on loopback:** explicit test identities, correct
   pin and ALPN success; wrong pin, TLS version/ALPN, plaintext peer, no/oversize
   certificate, changed/mismatched local key, stalled handshake, truncated TLS,
   wrong Host/route, malformed page/bundle and wrong content pin refuse with
   expected states. Assert no HTTP request reaches the server before a failed
   client pin check. Assertions must distinguish failures the chosen runtime
   can produce from unsupported synthetic cases; do not fabricate a pass.
3. **Service/hosting safety:** one bad handshake followed by valid acquisition
   in the same finite session; failed handshakes consume connection/time counts;
   no native checker/source execution in service; finite natural termination,
   positive process quiescence and exact grant replay/charges. A local key/view
   mutation fails closed at its declared check point: key changes present before
   TLS context setup/next session, and selected-view byte faults at the local
   read/recheck. Do not claim or test instantaneous revocation of an already
   loaded context on a mid-session disk-key change. Such failures do not advance
   hosting. No secret bytes appear
   anywhere in generated package or retained logs/requests/receipts.
4. **Real mathematical integration:** using the pinned successor package, carry
   genuine D1 catalog/page/bundle through TLS to a fresh node, then fresh Lean
   admission with exact identity/type/foundation matching. Repeat through a
   surviving replica after producer service stop. Acquisition/TLS success alone
   is not the pass condition. Reuse prior genuine bytes; no toy proof substitute.
5. **Independent operator usability and cost:** a packet-only operator performs
   documented identity provisioning, pin exchange, fresh configuration and the
   reciprocal continuation without private-state repair/root request relay.
   Record cold setup, all rejected/accepted work, handshake/service costs,
   retained bytes and interventions. Include a state-preserving next operation.

Freeze finite per-gate limits and expected poststates before executing; preserve
every failed run. Root owns outcome integration; one independent source/outcome
review should cover this module rather than repeated overlapping audit essays.
If gates pass, the claim is **implemented remote-capable transport with local
qualification**, not independently operated deployment, Internet resilience,
arbitrary NAT traversal, useful-growth speedup or the full project goal. A later
independent-host test remains needed for that deployment claim, but absent
hardware is not a reason to leave remote capability unimplemented.
