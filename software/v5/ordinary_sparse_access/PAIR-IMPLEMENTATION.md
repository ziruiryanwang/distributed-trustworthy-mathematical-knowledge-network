# Pair access source checkpoint

2026-10-25. Implements only the Store/helper assignment in CONTRACT.md.
Source written and compared read-only; **no import, syntax execution, test,
package, native process, existing database or Git mutation was performed**.
Independent source review and root's finite test selection remain separate.

## Files and interface

- `pair_access.py` SHA-256
  `7d3f2fc199736df54d76b421f3587ebc8a0167bd75363921385a1916b832116c`.
- `discovery_store.py` SHA-256
  `26ccca0fda86a255c38f7c3cc39b6b1fd88deba2ae10c6f79bc562b872c9502c`.

Store adds keyword-only `access_pairs=None`; enabled configuration is exactly
`{pairs, limits:{max_rows,max_logical_bytes}}` from the adopted contract. Plain
V2 configuration remains unchanged; opt-in physical V3 binds its exact local
config. No namespace, record, atomic posting or snapshot schema changes.

Helper entrypoints are `validate_config`, `create`, `open_config`, `append`,
`plan` and `next_row` with the contract signatures. Store imports it as `PA`.
`plan` returns a companion atom or None. Its three bounded SQL statements use
the candidate meter: base config/sequence, access counters, then LIMIT 0 to
resolve expected table/columns without scanning cache rows. `next_row` returns
the exact `(anchor_ordinal, companion_ordinal, object_id, admitted_seq)` tuple
through `io.one(probe=True)`; the caller alone precharges `scanned`.

## Transaction and failure behavior

Creation adds access tables/seq-zero counters within the fresh initialization
transaction, using execute rather than executescript to avoid implicit commit.
Admission checks readiness before its duplicate branch; new admissions collect
existing atomic ordinals, append both matching orientations, update base sequence,
seal the unchanged snapshot, check readiness and commit once. Any error uses the
existing whole metadata-transaction rollback. Duplicate rows add no pair work.

Enabled operation counters `access_checks`, `access_inserts` and
`access_logical_bytes` record attempted pair work; they remain in Store.work
after database rollback. Durable row/byte counters include only committed data.
The canonical config and row tuple bytes are constrained by both the independent
access allowance and global Store logical cap; existing max_db_pages bounds
combined physical allocation. Logical bytes are not physical SQLite size.

The public API author was informed that failed index.work is not exposed by the
old publish failure report, though it survives in memory and outer CPU remains
metered. Optional failed-attempt diagnostics belong to that author's successor.
Custody previews and earlier successful publication targets are not rolled back
by this metadata-store failure.

## Read-only checks and limits

Compared Store successor with the exact contact package: changes are confined
to the import/config/transaction hooks, enabled counters and physical-schema
status. Existing summary, authenticated-page, snapshot construction, atomic
Merkle operations and all base error/rollback paths retain their source.
The source is now LF in its fresh successor; predecessor bytes were untouched.

Independent source review found Python's bool/integer equality could accept a
malformed persisted access limit. Root authorized a specific pre-freeze repair:
`_state` now independently validates the stored access config before equality.
No execution was used to make or check that repair; reviewer reread is separate.

Inspected the separate candidate author's tuple consumption, old-cut ceilings,
original posting/object binding and extra-conjunct rejection; helper agreement
holds at source level. Actual behavior remains untested. Readiness checks detect
bounded metadata/expected-table inconsistencies, not arbitrary omission of an
unvisited row. Returned positives still require the unchanged atomic proof.
