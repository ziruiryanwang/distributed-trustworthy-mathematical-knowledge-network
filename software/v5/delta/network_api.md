# Delta packets through replaceable indexes and independent custodians

Fresh source-only successor; no actual network or admission pass follows from
these modules' existence. Read `DELTA-NETWORK-SEAM.md` for the architectural argument.

## Provider

Use `delta.custody.public_profile(image, foundation, policy)` and its `profile_id`.
This distinct wire profile includes the exact receipt profile only for **frontier
receipts inside a packet**. It is not itself a receipt profile or local verifier
configuration. Native-delta packets and succinct receipts keep separate schemas,
routes, stores and authority types.

Construct `PacketStore(root, profile, limits, envelope=..., create=True)` with finite
quotas. `put(module_id, packet_bytes)` validates structural target/profile/aggregate
bounds and atomically retains the exact blob and its offer; it does not check the
mathematics. `get(sha256, bytes)` verifies exact stored bytes. Invalid mathematics
may be structurally custodied but cannot pass later mathematical admission.

`CompositeProvider(index=..., custody=ModuleStore(...), packets=..., **limits)`
serves the unchanged discovery/group/body routes and two new read-only routes:

- `/v5/modules/delta-offer` accepts `module_id`, `wire_profile_id`, `max_offers`,
  `max_bytes`; returns untrusted `packet_sha256`/`packet_bytes` locators.
- `/v5/modules/delta-packet` accepts one exact packet digest/length; returns the
  entire untrusted bounded delta packet as `application/octet-stream`.

The provider has finite connection/request/reply/deadline limits and inherits the
existing start/stop lifecycle. Remote endpoints require the existing verified TLS
policy; loopback plaintext remains an explicit local test mode. There is no remote
write, redirect, arbitrary URL, proof execution or receipt route. Owner writes
must populate packet custody, selected groups/bodies and formal index; their
separate databases are not one transaction.

An independent replica can index its retained exports and advertise the existing
formal-index rendezvous keys. It is a genuine composite service, not a pure
custodian falsely labelled as an index. A known index endpoint need not supply
packets: empty/refused/expired offers remain charged failures, not global absence.
The locator still does not implement generic custody-only routing.

## Acquisition and admission

Construct the original `AcquisitionBudget` before all selected workflow work.
Keep one absolute deadline and a caller-owned hard process envelope. For located
search, construct `DeltaLocatedHandoff(channel, adapter, features, policy, budget,
location_limits, search_limits)` while the exact ServiceLocationProcess is still
a fresh unstarted reader. The handoff constructs the existing ServiceLocatedWorkflow
and precharges its exact full configured request/reply ceilings before dispatch.
The caller then starts its channel, uses `handoff.location` for existing route and
descriptor calls, and calls `handoff.begin_search()` once. The returned original
search client performs the unchanged formal offer/candidate requests.

`DeltaAcquisition.from_search(handoff, profile, module_custody, packet_custody,
verifier=...)` consumes that SAME prospective handoff once, not a claimed prior
ledger or a reconstructed search. It checks origin objects, grants and original
deadline, revalidates contact expiry/egress before dials and permits export
acquisition only for an actual candidate returned by that same search session.
Failed handoff attempts do not refund precharges or permit a renewed handoff.
Alternatively, direct `DeltaAcquisition(...)` supports owner-approved endpoints
without claiming they originated in this search. The caller remains responsible
for eventually closing the separate original channel after active operations end.

The selected adapter, `ModuleStore`, `PacketStore`, wire profile and optional exact
actual `DeltaVerifier` must match foundation/policy/image. The client never accepts
a receipt-verifier substitute or remote verifier configuration.

1. `export(provider, record)` checks the canonical discovered export/opening and
   stores it with readback. It returns the correct delta-specific next-gate label.
2. `offers(provider, module)` obtains bounded candidate packet locators.
3. `packet(provider, module, entry)` requires that exact provider/module entry was
   offered, then acquires/hash-checks/stores/reads back the full packet.
4. `body(...)` acquires explicitly demanded committed semantic bodies if needed.
5. `custody_ready(...)` checks exact selected packet and semantic readback. It
   grants no mathematical authority or future retention guarantee.
6. `admit(...)` reserves all frontier-plus-delta CPU maxima in the original budget,
   clamps wall time to the original deadline, invokes the actual DeltaVerifier,
   opens the selected group, and repeats custody/deadline checks before returning
   its distinct live handle. Failed finalization closes that verifier.

The inherited workflow budget conservatively limits total reserved CPU for one
admission to 600 seconds. The complete packet must also fit its own parse/custody
envelope and the independently configured receiver envelope. Refusal does not
mean false mathematics and grants no retry or renewed allowance. Nested CPU
reservations are not distinct actual CPU measurements to sum.

These grants account application request/reply bytes and chosen verification
work, NOT all system resource costs. Location routing-event caps are not DHT wire
byte caps. Location child/bootstrap/service CPU, DHT traffic, provider resources,
TLS/framing overhead and controller work need their existing separate telemetry
and enclosing owner Job. The application AcquisitionBudget is not a whole-system
wire or CPU envelope. The source API assumes trusted serialized owner Python;
identity/grant checks do not create an adversarial owner-process sandbox.

Use `close()` only after active calls have been cancelled/awaited. It closes the
workflow budget and delta verifier, not separately owned durable stores or the
underlying frontier verifier. Immutable packet files/reports are never restored
as live authority after restart.

## Deliberate boundaries

Complete checking material includes all needed uncertified ancestors and genuine
receipt frontiers. It does not imply all bodies any future author might request
are available. Custody, checking, discovery relevance, finite-index coverage and
global completeness are separate predicates. This successor adds no global
ledger, ownership attribution, universal useful-growth guarantee, permanent
availability promise, autonomous retry or hostile-source sandbox.
