# Ordinary export location wire and owner boundary

2026-10-28. Source implementation contract under SELECTION.md. Backend and
Python owners agree the schemas below. No runtime is selected.

## Exact ordinary descriptor

Canonical bytes are UTF-8 JSON with lexicographically sorted object keys, no
whitespace, no ASCII escaping of Unicode, finite safe integers only, maximum
nesting 32, and exact parse/re-serialization equality. Closed objects reject
missing or extra fields. All IDs/nonces are 64 lowercase hexadecimal characters.
No formal-feature or certified-body role is accepted by this new operator.

`spec = {semantic_id, export_id, role: "ordinary-export-v1"}`.
`route_key = SHA256(ASCII("DMKN-V5-ORDINARY-EXPORT-RENDEZVOUS-V1") || NUL || canonical(spec))`.
The DHT uses the retained raw/SHA256 CID encoding of this key and retained
`/dmkn/v5/location-kad/1.0.0` protocol. The separate descriptor protocol is
`/dmkn/v5/ordinary-export-descriptor/1.0.0`.

Request fields are exactly `schema`, the three spec fields, `route_key`, `nonce`,
`max_bytes`. Schema is `DMKN_V5_ORDINARY_EXPORT_DESCRIPTOR_REQUEST_V1`;
`max_bytes` is exactly 4096 and request bytes are at most 2048.

Reply fields are exactly `schema`, the three spec fields, `route_key`, `nonce`,
`peer_id`, `endpoints`, `remaining_ms`, `assurance`, `global_complete`,
`mathematical_acceptance`. Schema is `DMKN_V5_ORDINARY_EXPORT_DESCRIPTOR_V1`;
assurance is `ADVISORY_SERVICE_HINT_ONLY`; both booleans are false. The exact
request key/nonce must match. `peer_id` must match the Noise-authenticated dial
target, not merely another JSON field. Retain the selected 52-character Ed25519
PeerID validator. `endpoints` contains exactly one approved own endpoint with
exact fields `host`, `port`, `tls`, `server_name`, checked by the retained owner
egress policy. No referral or write endpoint is accepted.

A valid request to a live custodian whose exact route is no longer published
gets a normal framed, closed negative descriptor. Its separate schema is
`DMKN_V5_ORDINARY_EXPORT_DESCRIPTOR_UNAVAILABLE_V1`; exact fields are `schema`,
the three spec fields, `route_key`, `nonce`, `peer_id`, `reason`, `assurance`,
`global_complete`, `mathematical_acceptance`. Reason is exactly `NOT_ADVERTISED`;
standard assurance and both false booleans remain. It has no endpoint or
lifetime fields. The gateway must validate the exact request key/nonce and
authenticated peer before counting and skipping this negative. This permits
normal stale remote hints after honest local revoke without treating absence
at one custodian as global absence. Malformed messages, wrong identity/domain,
and uncertain exchange cleanup remain terminal.

`remaining_ms` is an integer from 1 through 3,600,000, clipped to the provider's
original current routing-service horizon at reply construction. It is not a
custody-retention guarantee or DHT provider-TTL assertion. The gateway anchors
the received duration at its own descriptor-command start, clips its original
gateway/controller service cutoffs and owner maximum hint age, and emits only
the remaining duration. Lookup/descriptor execution and HTTP response must
finish within their original HTTP-call cutoff; that short call cutoff is not
the advisory hint's expiry. The reader anchors HTTP duration at its request
start, clips its original aggregate reader grant and owner hint-age policy,
and keeps that private horizon through locator and evidence setup/dial.
Expired candidates are omitted; no intermediate receipt or retry restarts a
duration. Duplicate endpoint expiry is conservatively combined only within
the same exact demand. A different demand may obtain a fresh advisory hint
under the same unchanged aggregate grant.

## Exact read-only HTTP lookup

`POST /v5/ordinary/export-location` accepts exact request fields `schema`,
`semantic_id`, `export_id`, `role`, `route_key`, `nonce`, `max_providers`,
`max_descriptors`, `max_bytes`, `timeout_ms`. Schema is
`DMKN_V5_ORDINARY_EXPORT_LOOKUP_REQUEST_V1`; role/key/nonce follow the same
ordinary specification. Provider and descriptor ceilings are each 1..64;
`max_bytes` is 1024..16384 and `timeout_ms` is 1..60000. The gateway clips all
of them to its own existing limits and original deadline.

Reply exact fields are `schema`, `semantic_id`, `export_id`, `role`, `route_key`,
`nonce`, `status`, `reason`, `candidates`, `descriptors_attempted`, `truncated`,
`assurance`, `global_complete`, `mathematical_acceptance`. Schema is
`DMKN_V5_ORDINARY_EXPORT_LOOKUP_REPLY_V1`. Status is `OK` with null reason, or
`UNAVAILABLE` with reason `BUSY`, `EXHAUSTED` or `EXPIRED` and empty candidates.
Assurance and both false booleans are as above; `truncated` is boolean and
`descriptors_attempted` is 0..the requested/owner-clipped descriptor cap.
An OK empty list means only that this bounded lookup returned no usable hint.

Candidate exact fields are `peer_id`, `endpoint`, `remaining_ms`; endpoint has
the same four closed fields above. Preserve authenticated peer binding and
request-start lifetime anchoring. Admit no more than the requested/owner-clipped
provider cap and no more candidate entries than descriptors attempted. Build a
bounded prefix whose full canonical reply fits `max_bytes`; set `truncated=true`
when a candidate/count/byte ceiling omits available candidates. Do not encode
all 64 expanded candidates and then rely on an oversized-frame failure.

## Owner state and count invariant

New ordinary config schema is `DMKN_V5_ORDINARY_EXPORT_OPERATOR_V1`, with exact
fields `schema`, `role`, `state`, `semantic_id`, `egress`, `listen`, `announce`,
`bootstrap`, `endpoints`, `limits`. Role is `gateway` (zero own endpoints) or
`custodian` (exactly one). Existing finite owner egress, transport and metadata
limits apply. Runtime/service grants do not follow from remote input.
Only gateway role exposes the HTTP lookup in this initial integration. Custodian
role publishes and serves peer descriptors; a different gateway locates those
publications. The retained DHT lookup skips its own PeerID. One operator can run
both roles as separate processes/configs; combined local-self discovery is not
implemented or claimed.

`create` versus `reopen` is a separate owner launch argument. A reopen requires
the same persisted config hash and retained identity; there is no implicit
migration or state deletion. Evidence is always fresh. A new finite service
grant authorizes maintenance of the same explicit retained scope.

Before libp2p construction/start or background renewal, scan the bounded
published prefix under the original startup/service signal, validate every key
and spec, and build charged Set S. Report census rows/time and count intents
without a matching self-provider row separately; those are pending, not claimed
maintained. For committed published keys P, preserve `P subset-of S`, `|S| <= K`.
Serialized publication reserves S before atomic intent/published commit and
retains its charge after ambiguous failure. Confirmed atomic revoke deletes
intent, self-provider and published rows before releasing S. The existing
self-provider write guard prevents background resurrection without intent.
Remote hints can remain stale after local revoke; no immediate revocation claim.
Reopen reconstructs S from committed rows without a durable counter schema.

## Private owner IPC

Only `locate`, `descriptor`, `publish`, `withdraw`, `status`, `stop` commands are
accepted. Ordinary payloads contain exact SemanticID/ExportID bindings; the
operator validates them before use. No remote arbitrary registration API exists.
Gateway role cannot publish, withdraw or serve descriptors. Custodian publication
requires the separately selected bundle/own-endpoint exact-read eligibility path.

The private channel uses four-byte unsigned big-endian body length, then the
same canonical JSON. Command envelope exact fields: `schema`, `sequence`,
`command`, `payload`, `remaining_wall_ms`; schema
`DMKN_V5_ORDINARY_LOCATION_IPC_COMMAND_V1`. Reply exact fields: `schema`,
`sequence`, `status`, `result`; schema
`DMKN_V5_ORDINARY_LOCATION_IPC_REPLY_V1`. Command sequence starts at one;
PREPARED and READY use zero.
No foreign absolute clock crosses the pipe. Each operation clips the received
remaining duration to its original local service and per-operation cutoff.

Before runtime creation, state opening or network startup, Node records a local
marker and emits PREPARED with exact result `{role, semantic_id, mode}`. Only
after receiving that marker does the parent emit one lifecycle BEGIN frame:
`{schema: "DMKN_V5_ORDINARY_LOCATION_IPC_BEGIN_V1", remaining_service_ms,
remaining_wall_ms}`. Both are positive integer durations, with service no larger
than channel duration. They are computed from the parent's original separate
service/channel deadlines at its current time, never renewed from receipt.
Node anchors both at its earlier marker and clips service to the configured
service maximum. Since that marker precedes the parent's duration calculation,
the resulting Node cutoffs cannot exceed the parent's original cutoffs under
the usual local monotonic-clock premise. Runtime setup and startup then consume
this remaining time. READY follows actual startup. No extra grant is persisted.

Node also caps private-channel life at the earlier marker plus configured
service time plus the fixed six-second finalization allowance (at most one
hour), and can only shorten that cap after BEGIN. The routing service stops at
its clipped service horizon; the private pipe remains available for bounded
status/stop work under its distinct channel cutoff. Ordinary commands use the
service cutoff; only status/stop may use the channel cutoff.

Exact command payloads:

- `publish` / `withdraw`: `{semantic_id, export_id}`.
- `status` / `stop`: `{}`.
- `locate`: `{ticket, operation: "ordinary-route", route_key, spec, event_cap,
  peer_cap, remaining_wall_ms}`. Ticket is a positive safe integer; event/peer
  caps narrow the configured maxima. Reply fields are exactly `ticket`,
  `route_key`, `peers`, `termination`, `error`, `census`, `routing_peers_before`,
  `routing_peers_after`, `assurance`, `global_complete`, `mathematical_acceptance`.
  Peers are at most 64 distinct validated IDs. Census exact fields are `events`,
  `send_query`, `peer_response`, `final_peer`, `query_error`, `provider`,
  `add_provider_write`, `last_query_error`; counts are nonnegative safe integers
  and the last error is null or at most 500 characters. Termination is
  `ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE`, `PROVIDER_BUDGET`,
  `INCOMPLETE_QUERY_ERRORS` or `INCOMPLETE_ABORTED_OR_FAILED`; error is null or
  at most 500 characters. None establishes global absence.
- `descriptor`: `{ticket, operation: "ordinary-descriptor", peer, request,
  max_reply_bytes: 4096, remaining_wall_ms}`. Success reply fields are exactly
  `ticket`, `authenticated_peer`, `raw_base64`, `request_body_bytes`,
  `reply_body_bytes`, `framed_reply_bytes`, `assurance`,
  `mathematical_acceptance`; body bounds are 2048/4096, framing adds four bytes.
  The retained narrow unavailable-TCP classification instead returns exact
  `{status: "DESCRIPTOR_UNAVAILABLE", ticket, peer,
  reason: "TCP_CONNECT_UNAVAILABLE", mathematical_acceptance: false}`.
  Malformed descriptors, authentication errors and uncertain cleanup remain
  terminal; a TCP-unavailable result conveys no authenticated descriptor.

The ordinary controller exposes async `command(command, payload, *, until)`
where `until` is a local absolute cutoff; only remaining milliseconds cross IPC.
It owns subprocess/pipe creation, pins and teardown. The gateway consumes this
concrete local controller, not a remotely supplied callback or proof of identity.
Both successful locate and descriptor results use assurance
`ADVISORY_SERVICE_HINT_ONLY`. A gateway holds its fail-fast busy lock across the
whole locate-to-descriptor sequence, because only the most recent lookup owns
the controller's bounded peer cache.

The separately pinned import is `transport.ordinary_location_controller`.
Construct `AdoptedLocationRuntime(source_directory, source_pins,
installation_root=..., workspace_root=...)`, then
`OrdinaryLocationProcess(adoption, configuration, evidence, mode="create"|"reopen",
deadline=..., service_deadline=...)`, with `service_deadline <= deadline`.
Public methods are async `start()`, `command(...)`, `close()` and
synchronous `report()`. `LocationUnavailable.reason` is exactly `BUSY`,
`EXHAUSTED` or `EXPIRED`, and is raised only before private command admission.
`LocationChannelFailure` is terminal for closed/poisoned channels or any issued
exchange uncertainty; teardown is awaited, and uncertain teardown remains
terminal with its diagnostic saved. There is no retry/reuse on that channel.

The ceiling is 8192 commands sharing publication, withdrawal, location,
descriptor, status and stop work; smaller owner command limits stop first.
Ordinary work reserves two commands for report/stop; status reserves one for
stop. An explicit `limits.ipc_bytes` input is at least `3 * (16384 + 4)` and at
most 129 MiB in each direction; smaller configured bytes stop first. Bodies are at most 16 KiB,
frames at most `commands + 2` (8194 maximum) each direction and aggregate framed bytes at most 129 MiB
each direction. These are counters, not preallocated buffers. The 64-provider
ceiling is not a promise that 64 expanded endpoint candidates fit one response;
the HTTP layer must truncate explicitly to its selected byte cap.
PREPARED plus READY consume the two reply lifecycle frames; BEGIN consumes one
input lifecycle frame. BEGIN bytes and both reply frames are charged to the same
existing byte/frame counters before ordinary commands. Report/stop command and
byte reserves remain intact; no command-count reset follows the handshake.

The Python controller permits one in-flight command with no unbounded waiter
queue. A busy gateway returns its explicit settled outcome. Uncertain IPC
cancellation/failure poisons the channel and drains its owned backend before
another operation can be admitted. Runtime byte verification, startup census,
network/renewal and gateway costs are separate reported scopes; 192 MiB bounds
retained runtime payload bytes, not process RAM.

## Source projection

New operator sources are `protocol.mjs`, `maintained_roles.mjs`,
`ipc_wire.mjs`, `node_entry.mjs`, and `controller.py`. Reuse the selected
`intent.mjs`, `runtime.mjs`, `framing.mjs`, `transport.mjs`, `role_composition.mjs` and
`services_composition.mjs` unchanged in the separately pinned operator role.
The latter wrappers preserve raw-connect service abort and required Ping.
The controller omits the unused certified/formal workflow imports. Root owns
the separate operator manifest/packaging/launcher; reader loaders, native and
module-anchor support remain outside this source assignment.
