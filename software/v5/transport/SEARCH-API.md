# Bounded discovery client API

This describes evolving v5 source, not a completed release. Discovery authenticates
provider-selected metadata. It does not accept a theorem, prove honest feature
extraction, promise object availability or describe the latest global corpus.
Acquisition, deterministic feature recomputation and mathematical checking remain
separate subsequent steps.

## One finite workflow

Create one `SearchSession(namespace, features, limits)` and one
`SearchClient(session, endpoints)` for a bounded investigation. The namespace
comes from the selected object/feature/foundation policy; features are a sorted,
duplicate-free list of one to eight formal feature IDs. Endpoints are an
owner-approved finite mapping of local labels to `Endpoint` values. Remote
connections require verified TLS; plaintext HTTP is permitted only on loopback.
The client never dials an arbitrary referral or retries automatically.

The session limits have exactly these keys:

```python
session_limits = dict(
    providers=4, snapshots=8, requests=64, pages=48,
    examined=16384, candidates=128, bytes=8*1024*1024,
    wall_ms=60000, inflight=2,
)
```

The owner must serialize a session's local methods on one event loop. Several
requests may be in flight within its cap; their resource reservations are shared.
Creating a fresh session on every provider, response or failed request is not
continuation of the same bounded workflow. Longer work requires an explicit new
owner allocation with earlier costs retained.

## Obtain a snapshot without knowing its ID

```python
offered = await client.offer(
    "peer-a", max_bytes=16384,
    max_expanded_bytes=1048576, max_age_ms=60000,
)
```

`OFFERED` includes `snapshot_id` and `partitions`; its compact summary has already
been authenticated and pinned in the same session. No second summary call is
necessary. `NO_OFFER` means this contact does not serve the index role/namespace.
`REFUSED` means the selected summary could not fit its finite resource limits.
Neither means the sought mathematics is absent.

The request contains namespace, features and byte caps, not a snapshot ID. The
provider selects one retained immutable snapshot. `max_bytes` covers the **whole
reply envelope**; `max_expanded_bytes` separately bounds reconstructed summary
encoding, not literal Python heap usage. `max_age_ms` uses only the owner's
request-relative monotonic clock. It limits offer adoption/hint reuse; it does
not prove that the snapshot is recent. An expired hint does not invalidate an
already pinned immutable snapshot.

Every offer attempt consumes one snapshot-admission slot before the ID is known,
including failure, refusal and duplicate offers. `report().session.snapshot_budget`
separates `charged_attempt_slots` from `known_snapshot_ids`. The legacy
`used.snapshots` field counts distinct caller-pinned or verified offered IDs,
not charged attempt slots. Subsequent pages for a known ID do not double-charge
its slot.

If the caller already knows the intended snapshot, the existing path remains:

```python
await client.summary("peer-a", snapshot_id, max_bytes=16384,
                     encoding="compact-v1", max_expanded_bytes=1048576)
```

`encoding="expanded-v1"` remains the default. There is no format downgrade,
guessing, retry or budget renewal if a response fails.

## Choose positive candidates or authenticated intervals

The local agent chooses a partition and starting position from the returned
plan. It need not query every partition. Two deliberately separate APIs exist.

### Positive candidates: inexpensive nonmatch transmission

```python
candidate_limits = dict(
    scanned=1024, matches=4, bytes=65536, timeout_ms=1000,
    record_probes=16384, node_reads=20000,
    hash_calls=200000, sql_vm_steps=1000000,
)
result = await client.candidates(
    "peer-a", snapshot_id, partition, start, candidate_limits,
)
```

The provider uses existing B-trees to test candidate IDs. Only surviving matches
load complete records and build ordinary anchor-vector membership proofs. Every
feature lookup respects the same selected snapshot's ordinal cutoff. The client
verifies each returned committed record against its pinned summary.

`VERIFIED_CANDIDATES` returns `matches`, `new_matches`, `duplicate_matches`,
`metadata_conflicts`, `advisory_next`, `provider_termination` and
`provider_work_claims`. The assurance is
`VERIFIED_POSITIVE_COMMITTED_RECORDS_ONLY`; `verified_scan_coverage` and
`mathematical_acceptance` remain false.

`advisory_next` is explicitly an advisory cursor, not a proof about omitted
records. Even `provider_termination="anchor_boundary"` or a null cursor does
not prove complete search. Budget/time refusal can return no hits and an
unchanged cursor. The honest implementation does not advance past an unfinished
positive record/proof. Do not automatically repeat a zero-progress response
without checking remaining workflow resources and the reason for refusal.

The provider's work counters and termination are untrusted claims. In particular,
a zero-hit or reported-zero-work reply does not establish absence or earn a
resource refund. Server search can still be linear in a common-feature
intersection. This path saves nonmatch transmission; it does not promise
universally sublinear search or a universal end-to-end speedup.

### Ordinary pages: authenticated scanned intervals

```python
page_limits = dict(examined=32, matches=8, bytes=65536,
                   timeout_ms=1000, node_reads=100000)
result = await client.page("peer-a", snapshot_id, partition, start, page_limits)
```

This original path transmits every examined anchor record and proves an exact
contiguous interval of the selected snapshot. Its verified coverage is kept in
`session.report()["coverage"]` and its cursor in `last_verified`. It may cost
more wire bytes when most examined records do not match.

Candidate replies never call `Coverage.accept`, never advance `last_verified`,
and never turn an advisory skipped interval into verified coverage. Their
positions are kept separately under `last_advisory`. Even ordinary complete
interval coverage concerns provider-selected committed metadata, not complete
indexing of the global/source corpus or mathematical truth.

## Accounting and deduplication

Both page APIs share the same request/page/provider/snapshot/byte/deadline and
in-flight caps. Before candidate I/O, the session reserves the whole requested
`scanned` allowance against its existing `examined` budget. Once the ticket is
consumed, **that whole scan allowance is charged**, including success, invalid
proofs, zero-work reports, deadline expiry and abandoned/unknown transport. It
is not refunded based on provider counters. Ordinary successful pages retain
their existing verified-examined-row accounting.

Every verified returned hit consumes the `candidates` allowance, including
duplicates. Failed/abandoned tickets conservatively consume their reserved hit
allowance. Actual received body bytes are charged before parsing; unknown
transport outcomes conservatively consume the full reserved byte ceiling.
HTTP header/request counts are also reported separately. A refusal cannot
reset any of these counters.

Deduplication is shared across providers, snapshots and both page APIs. Its key
is the exact pair `(object_id, RecordID)`, not object ID alone. `matches` retains
all verified hits for compatibility; `new_matches` contains only previously
unseen exact claims. A differing RecordID for the same object ID is a bounded
alternative, exposed through `metadata_conflicts` and charged normally. It is
not suppressed: otherwise a malicious first provider could poison an object-ID
key before content acquisition and hide an honest later result. A first-seen
metadata claim has no mathematical or acquisition authority. Within-snapshot
ordinary Coverage still enforces its original exact consistency checks.

`report().session.candidate_search` reports charged scan allowances, distinct
verified committed-record claims, duplicate verified hits and alternative
metadata claims. All of these are bounded by the session's allocations; none
is a measure of useful mathematical growth.

## Provider ownership and limits

The read-only route is `POST /v5/discovery/candidates`, using
`DMKN_FORMAL_CANDIDATE_REQUEST_V1`. The provider reserves the requested whole
reply byte cap before processing and clamps the operation's timeout to its own
remaining deadline. Malformed or over-budget requests close under the existing
strict HTTP profile; no fabricated absence result is returned.

Candidate execution exclusively borrows the Store's SQLite connection and its
otherwise unused progress handler. It temporarily disables lock waiting,
restores `busy_timeout`, and removes the handler in `finally`. Its data-path VM
allowance uses conservative100-instruction reservations; reported charged VM
steps are an upper allowance, not exact measured instructions. Three fixed
connection-control PRAGMAs are separate constant overhead. Snapshot, CAS and
proof-building SELECTs all use the same bounded executor. Hard process/memory
containment remains necessary; deadlines are cooperative, not real-time.

There is no indispensable central discovery server in this interface. Successful
discovery still requires an appropriate reachable contact within the selected
budget. Huge-network routing recall, maintenance, custody and useful growth are
separate obligations, not consequences of this small API.
