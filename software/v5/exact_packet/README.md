# Exact known-packet acquisition

This successor removes one acquisition obstruction: a caller who already knows
an evidence packet's SHA-256 **and exact byte count** can fetch it even when the
provider's bounded offer list omits it. The server already supports that request.
There is no new route, wire schema, global scan, verifier or discovery mechanism.

Source selection: [implementation decision](../../../research/cycles/v5-2026-10-20/EXACT-PACKET-IMPLEMENTATION-SELECTION.md).
The six predecessor/successor identities are in the
[source checkpoint](../../../research/cycles/v5-2026-10-20/EXACT-PACKET-SOURCE.md).
This is source implementation; executed qualification and installed adoption are
separate root decisions, not implied by this README.

## Two explicit choices

Existing offered-choice calls keep their offer prerequisite:

```python
offers = await client.packet_offers(candidate, max_offers=8)
warrant = await client.acquire(candidate, offers["packets"][0])
```

When the caller already has an exact entry from an earlier result or another
application-controlled selection, it may instead use:

```python
entry = {"packet_sha256": exact_sha256, "packet_bytes": exact_byte_count}
warrant = await client.acquire_exact(candidate, entry)
```

The candidate must still belong to this live client and identify the selected
module and supplier. The exact method neither creates a candidate nor accepts
an arbitrary provider URL. Both methods use the same ordinary mathematical
admission logic, body obligations, live cache warrants, journal checks and
operation/resource limits. Optional arguments are identical: `bodies`,
`expected_exact_journal`, `native_cpu_seconds`, `receipt_cpu_seconds`,
`wall_seconds` and `memory_mib`.

For interface-first semantic work, use the corresponding structural-only call:

```python
staged = await client.stage_packet_exact(candidate, entry)
# Or, with the existing finite SemanticReader:
selection = await reader.stage_exact(candidate, entry)
```

`stage_packet_exact` returns an untrusted staged-data token, not a warrant.
`stage_exact` obeys the reader's original selection/demand, source-count,
variant-conflict, inventory, ownership and step limits. It does not choose an
alternative variant automatically. Subsequent admission/import is unchanged.
The old `stage_packet` and `reader.stage` continue to require an actual offer
for a new transfer/selection. The reader's unchanged same-entry `NO_PROGRESS`
return performs no new transfer or admission and does not recheck that offer.

## Transport, placement and costs

`EvidenceAcquisition.packet_exact(provider, module, entry)` uses the existing
`/v5/modules/delta-packet` route. It validates/copies the strict digest/size
entry before awaiting, validates the current profile and object-size envelope,
and uses the original configured contact, request/reply budget and deadline.
The response must match both size and hash, pass the actual typed packet store,
survive its before-COMMIT activity guard and be read back exactly. Its result
explicitly says `mathematical_acceptance=False`.

Both transport choices share this implementation. Exact acquisition does not
insert a synthetic offer into the offered-choice set. Local packet-size
preflight is not a promise of remaining database capacity; the unchanged store
quotas and transaction checks still decide whether custody can commit.

Placement already has an exact validated manifest. Its missing-packet branch
now uses `packet_exact` directly, retaining opening/summary checks, custody,
receipts, same-request idempotence and recovery rules. Its existing conservative
request/byte reservation remains unchanged; removing an offer request creates
no refund or renewed allowance.

There is no digest-only mode, general offer pagination, automatic supplier
fallback or completeness claim. An absent packet, invalid reply, expired
contact, exhausted allowance or failed custody still fails under the existing
error/liveness rules. Transport errors are not newly classified as authoritative
global absence. Successful structural storage is never mathematical acceptance.

## Source and state compatibility

The managed-owner change updates only its explicit `workspace_evidence.py` pin.
Other selected source pins remain dynamically bound to the complete SDK map.
The full managed-storage writer identity changes with these six files. A root
selected successor release must therefore use its own compatible fresh managed
configuration/state; this change is not an old-state migration or permission to
overwrite a previous installation. All predecessor bytes remain preserved.
