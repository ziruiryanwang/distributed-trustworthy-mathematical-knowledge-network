# Optional selective search for ordinary mathematics

This source successor is under review. Do not treat this document as a tested
release or use it to overwrite a retained index. The default search remains
`atomic-v1`; mathematical acceptance is unchanged in either mode.

## When it helps

Suppose many statements mention A, many mention B, but few mention both. An
investigator who knows A and B can search for connections without knowing a
theorem name or its complete type. A provider can prepare an optional local
access path for that pair. It contains only records already admitted to the
ordinary metadata index, not new mathematical assertions.

This is selective database indexing, not theorem generation, semantic equivalence
search or complete discovery. If almost everything mentions both symbols, or
the pair is rarely queried, its construction and storage may not pay for itself.
An equally capable local library can use the same optimization.

## Provider configuration

The existing public `publish` and `serve` configurations accept an optional
`access_pairs` field inside their `index` object. Its exact shape is:

```text
access_pairs = {
  "pairs": [[feature_a, feature_b], ...],
  "limits": {"max_rows": integer, "max_logical_bytes": integer}
}
```

Each feature is a lowercase 64-hex atomic feature ID in this ordinary namespace,
not a declaration name, export ID or theorem hash. Obtain the keys using the
existing ordinary query compiler for the two formal feature specifications;
the public find report also exposes its compiled namespace/features. Do not
guess keys or copy them from a different namespace. Each pair is sorted with
distinct members, and the 1–8 pair list is sorted without duplicates.

`max_rows` is 1–16,000,000; `max_logical_bytes` is 1,024–2^40. These are upper
limits, not recommended allocations. Count two oriented rows per matching pair.
The ordinary index's overall logical-byte and SQLite page caps still apply.

Select this configuration when creating a **fresh** index. Use exactly the same
configuration on reopening it, including when serving it. Omitting the field
keeps the original atomic profile. Neither adding this field to an old store nor
changing its pairs/quota settings performs a migration. Reindexing old material
is a separate, potentially expensive operator decision, not an automatic step.

Each new metadata admission updates ordinary postings and the optional access
rows in one transaction. Pair-capacity failure refuses that admission; it does
not silently produce an incomplete cache. The public multi-target publish call
may already have saved a custody preview or indexed earlier targets. Those
remain; a failed index transaction does not revoke checked mathematics.

## Reader configuration

Use the ordinary `find` configuration and optionally add:

```json
{"candidate_mode":"sparse-v2"}
```

This is an additional field in the complete existing configuration, not a complete
configuration by itself. For `directory-find`, put it inside the existing `search`
object. Directory suggestions cannot select this mode for the reader.

An enabled reader uses a distinct sparse-positive endpoint and V2 request/reply
schemas. It retains the same formal query, atomic summary and proof verification.
A new provider without a suitable access pair uses ordinary sequential traversal
inside that same V2 request and allowance. A legacy provider rejecting the new
route produces a charged incomplete outcome; there is no automatic V1 retry.
Choose `atomic-v1`, or omit the field, for the existing V1 route.

## What the counters and result mean

In V2, `scanned` counts attempted driver seeks, including an empty terminal seek.
It does not count every original atomic ordinal skipped by a selective access
path. SQL work, record probes, hashing, proof reads, bytes and deadlines remain
separately bounded. The client still spends its full selected per-page scan
allowance; unauthenticated provider counters never refund it.

For example, two A-only records, two B-only records and a final AB record require
three atomic visits to reach AB, but one pair-driver seek can reach it. That is
not one total SQL operation or a threefold end-to-end speedup. Initial index
population, maintenance, storage and service costs must also be considered.

Every returned hit still needs its original atomic membership proof and complete
query-feature match. Subsequent ordinary acquisition and checking are still
required for mathematical acceptance. `access_used` is an advisory provider
diagnostic, not a proof that no records were omitted. Old snapshots retain their
original ordinal ceilings; later cache rows do not make later results belong to
an earlier snapshot. Empty results, exhausted budgets and unavailable providers
remain incomplete knowledge, not mathematical negations or global absence.
