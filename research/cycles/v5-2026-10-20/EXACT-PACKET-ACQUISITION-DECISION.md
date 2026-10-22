# Exact known-packet acquisition: reuse the existing wire route

2026-10-22, storage_integration_adapter. Source-only; no code/runtime/Git change.

## Decision

**The exact public read already exists; the integrated client unnecessarily
requires a truncated discovery offer first. No new transport protocol, cursor,
global scan or packet-store schema is needed.** Add an explicit owner-selected
known-packet acquisition path over the existing charged transport, then use it
for placement's already exact manifest. Preserve ordinary offered-choice APIs.
This is a proposed source change, not an existing integrated capability/pass.

## Current129 source trace

Authoritative map: `distribution-managed-storage-01-input.json`, SHA256
`a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.
Relevant actual sources were read and rehashed:

| Logical source / SHA prefix | Concrete behavior |
|---|---|
| placement/codec6f32569d | Manifest binds exact module, packet SHA/size, export and wire profile; funded quote includes opening+offer+packet requests. |
| placement/controller ef1c9b59 | `_run` first uses exact local packet if present; otherwise asks first4 offers, requires wanted membership, then calls `packet`. |
| evidence_network/transport7ac7204b | `EvidenceAcquisition.offers` records provider/module/SHA/size in `_offers`; `packet` inherits the requirement below. |
| delta/transport18c1abda | `DeltaAcquisition.packet` requires `_offers` membership before downloading. `_get` enforces current owner/budget, configured contact, original timeout and cumulative request/byte accounting. |
| evidence_network/custody4264841e | `offer` SQL orders digests and LIMITs max_offers. No cursor or exact filter. |
| delta/custody4304e529 | Inherited `get(digest,size)` performs exact size/length lookup, then blob lookup, both `WHERE digest=?`; checks exact length/SHA. `packets` is digest-primary-key WITHOUT ROWID. |
| client/workspace_evidence d94e3825 | Public `acquire(candidate,entry)` independently requires that same `_offers` membership before structural acquisition and mathematical admission. |

The provider's existing public route is:

```text
POST /v5/modules/delta-packet
{"packet_sha256": <exact SHA>, "packet_bytes": <exact size>}
  -> CompositeProvider.dispatch
  -> PacketStore.get(SHA,size)
```

It does not require a prior offer, module enumeration or cached offer token.
The evidence provider inherits this dispatch unchanged. Its HTTP path reserves
the exact response size and checks framing; the shared exchange requires exact
Content-Length. The route name is historical: the selected evidence provider
already serves its profile-selected typed packets there.

This works for **known digest and exact size**, as placement manifests supply.
A digest alone is insufficient: the existing blob request requires size. Do
not guess size, download under an unbounded ceiling or claim this solves digest-
only discovery. A future exact metadata query, if actually needed, is separate.

Offer discovery is genuinely insufficient: request max_offers is at most8,
while storage allows64 offers per module. Raising4 to8 or retrying the same
request cannot select a later known digest. A malicious earlier offer could
consume choices without weakening mathematical verification, but still deny
useful acquisition. Complete inventory remains storage_launch_review's separate
export-contract question.

## Minimum remedy and safety conditions

Introduce explicit `EvidenceAcquisition.packet_exact(provider,module,entry)`:
validate exact entry shape/SHA/size, current module/profile and local packet
capacity before I/O; use the existing `_get`/PACKET_ROUTE and original shared
budget; verify length/SHA; perform the existing typed `put(module,raw)` with
current before-COMMIT guard; reread exact custody. `put` structurally checks
target module and selected wire/foundation/policy envelope. The route itself
does not carry those semantics; receiver validation must remain mandatory.
Retain configured endpoint/egress/TLS and expiring-contact checks, current owner
and original deadline, finite HTTP framing/request/byte caps, failed-request
settlement, typed parsing limits, store object/count/page quotas and final
liveness. Public use must retain exact candidate ownership and body/group binding.

Do not use unaccounted raw exchange or fabricate `_offers` membership. Report
local exact demand, not a provider-advertised offer.
Keep old `packet`/`acquire` offer semantics unchanged. A small explicit public
`acquire_exact(candidate,entry,...)` can share the existing admission machinery,
using the same candidate/contact, body/custody/journal checks, cache warrants
and genuine verifier. A trusted caller's chosen
digest is a retrieval target, never mathematical or availability authority.

Placement already supplies this exact demand through a validated charged
manifest: replace its offer-then-packet branch with `packet_exact`, leaving
local reuse, opening/summary comparison and receipts intact. Preserve the
existing sufficient conservative quote and nonrefund semantics initially.

Duplicate behavior stays distinct: an identical placement request ID returns
its retained result without a new reservation/pull. A new request/grant is
charged even when exact local custody makes acquisition unnecessary. Existing
`put` verifies exact duplicate bytes and adds zero logical packet/offer storage
for a genuine duplicate; it does not refund network/CPU charges. Live admission
cache reuse remains subject to the original warrant, not a stale saved report.

Prospective fresh successors: `evidence_network/transport.py` (explicit exact
method), `placement/controller.py` (exact manifest path),
`client/workspace_evidence.py` (explicit public exact admission sharing), plus
`client/managed_owner.py` only for its changed workspace source pin. A fresh
complete SDK map/writer identity is required; preserve used predecessors.
Existing provider/delta transport, custody schema/get and quote codec need not
change. No new public wire route, global registry or offer-cache token.

## Cost and focused evidence

Server work is two indexed identity lookups plus selected-byte read/hash;
recipient parsing/storage is bounded by that packet's existing envelope and
local quotas (including at most64 same-module offers), not the global corpus.
Under ordinary B-tree assumptions lookup is O(log local packets + packet bytes),
not a latency guarantee. No new succinct proof or ancestry campaign.
One missing packet costs one HTTP request and its exact `L` response bytes,
plus fixed bounded framing; no4096B offer reply is required. Hashing/parsing is
O(L) plus envelope-bounded structural work; custody lookup/write/index overhead
and logical/page limits remain real costs. CPU uses existing owner/Job guards,
not an inferred constant-time promise. Verification cost is unchanged and is
separately charged only when mathematical admission is requested.

One focused future test should place the chosen valid packet after the offer
prefix, show existing offer omission, then exact acquisition/placement success
through the genuine public route. Wrong size/SHA/module/profile and exhausted
budget must refuse without false admission/refunds. Reuse verifier evidence;
structural custody is nonmathematical. No execution is selected here.
