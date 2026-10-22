# Bounded packet-offer enumeration

This source successor permits an explicitly requested count of up to64 packet
locators on the existing offer API. It is not a standalone package or an adopted
installation. Root selects its exact source map and qualification separately.

## Use with a known upgraded provider

After ordinary formal discovery and candidate resolution, a caller can request:

```python
offers = await client.packet_offers(
    candidate, max_offers=64, max_bytes=16384
)
```

The candidate retains its original authorized provider and module. The response
contains unverified `packet_sha256` and `packet_bytes` entries. The caller chooses
an entry and uses the existing offered acquisition or staged-reader API; this
method does not pick, download or verify a proof automatically. Already-known
exact identities remain usable through the separate exact-packet APIs.

The existing store permits at most64 variants per module/profile, possibly fewer
under its configured quota. A compatible honest provider's single SQL read can
therefore expose its whole current local set without paging. Its fixed-size
locators fit within the explicit16KiB reply allowance. The old default4096-byte
allowance is not silently raised and may be too small for a full64-entry reply.
Every request still uses the original grant, deadline, contact and byte budget.

## Compatibility and limits

- Default `max_offers=4, max_bytes=4096` and explicit1..8 requests are unchanged.
  Counts9..64 are optional;65, booleans and other invalid inputs still refuse.
- The unchanged wire profile does not advertise this larger count. An older
  eight-entry provider may reject a64-entry request, causing the current public
  client operation to fail closed. Use the larger count only with an explicitly
  known upgraded provider. No automatic capability probe, retry or renewed grant
  is provided.
- A response is a local read view, not an authenticated complete inventory or a
  retention promise. Concurrent later insertions need not appear. Unavailable
  or dishonest providers can still omit useful knowledge. `global_complete` and
  `mathematical_acceptance` remain false.
- Packet SHA and size identify bytes; they do not establish mathematical truth
  or proof cost. Actual selected-profile custody and mathematical checking stay
  mandatory. Staging still selects one variant per module; certificate failure
  still follows existing owner/client revocation. Enumeration is not recovery.
- Cached offers consume memory: at most64 new tuples per funded offer call,
  before deduplication. Aggregate calls, request/reply bytes and process limits
  still apply. No packet blobs or proof ancestry are fetched by this call.

## Integration scope

Only `delta/custody.py` changes: its shared packet-offer count bound is widened
from8 to64. This same grammar is used by delta, mixed, frontier and evidence
packet transports/stores. Their response shape, exact profile checks, storage
quotas and HTTP route remain unchanged. The separate receipt-store offer grammar
is not changed.

Use a fresh selected SDK map and its resulting writer identity; never patch an
existing installation or silently reopen managed storage under a different
writer profile. See `research/cycles/v5-2026-10-20/OFFER-ENUMERATION-SOURCE.md`
for exact source identity, pin analysis and qualification status.
