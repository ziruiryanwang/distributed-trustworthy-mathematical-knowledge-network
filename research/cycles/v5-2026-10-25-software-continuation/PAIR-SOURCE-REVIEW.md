# Independent pair-cache and Store source review

2026-10-25. `ordinary_routing_gap`. **GO at the source boundary**, following one
small pre-use correction described below. No imports, test execution, build,
state access, package assembly or Git mutation was performed by this review.
Root still owns any finite runtime selection and subsequent adoption.

## Exact scope

Read the complete fresh `software/v5/ordinary_sparse_access/pair_access.py` and
`discovery_store.py`, comparing Store behavior with the previously read contact
baseline, PROFILE
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`.

Final reviewed SHA-256 identities:

| Source | SHA-256 |
|---|---|
| `pair_access.py` | `7d3f2fc199736df54d76b421f3587ebc8a0167bd75363921385a1916b832116c` |
| `discovery_store.py` | `26ccca0fda86a255c38f7c3cc39b6b1fd88deba2ae10c6f79bc562b872c9502c` |

The reviewer authored candidate/provider successors, not these two sources.
Their compatibility was checked against the separately selected contract and
actual helper calls; this is not independent approval of the reviewer's code.

## Findings

The optional configuration is validated and detached, bounded to eight distinct
ordered pairs, strict integer row/byte limits and bounded serialized size.
Absent configuration retains Store V2 fields/schema and no access tables;
enabled configuration selects local Store V3. Constructor equality plus helper
validation enforce exact reopening, with no migration or repair path.

Fresh auxiliary creation uses `execute`, not `executescript`, inside the same
transaction that installs initial base metadata and the empty snapshot.
Configuration bytes count once globally and against the independent access
allowance. Failed initialization closes the connection; it does not claim a
usable partially initialized store or silently delete failed output.

For admission, the source checks readiness before duplicate handling, captures
the original per-feature ordinal in the existing append closure, then calls
`append` before advancing the base sequence. The helper checks the current
base/access sequence equality and the new object's next sequence, inserts both
orientations, and advances only auxiliary state. Store advances base state,
seals the unchanged atomic snapshot, rechecks equality, then commits once.
Neither helper commits independently. Existing catch-all rollback encloses
objects, postings, CAS nodes, snapshots, counters and auxiliary state; the
operation node cache is cleared on failure. Duplicate admission cannot create
rows, charge new access bytes or repair inconsistent readiness.

Each oriented row is separately checked/charged before insertion. A failure on
the second orientation therefore cannot commit a half pair. Attempted insert
and byte counters live in operation memory and are not erased by SQL rollback;
durable row/byte counters are. Shared `max_db_pages` remains effective for base
and auxiliary storage. At most eight feature-membership checks and sixteen
row insertions are added per object, plus bounded metadata reads. This is not a
new unbounded powerset builder or hidden maintenance job.

Sparse planning uses the caller's `io.one` and deadline for all three readiness
SQL statements: base config/sequence, access counters, and a `LIMIT 0` table/
column check. Disabled access performs no auxiliary SQL. Enabled corruption
raises even if the query has no eligible pair. An eligible companion is chosen
only among requested fixed pairs containing the existing anchor. The range seek
fixes the leading primary-key columns and uses both ordinal bounds in SQL, with
ordered `LIMIT 1`, no OFFSET, materialization or temporary reorder. It charges
one record probe and SQL through the same I/O object, not `scanned`; candidate
code owns that driver charge before invoking the helper. The returned four-
column tuple matches the candidate's exact contract.

These changes do not enter atomic records, feature sets, Merkle commitments or
snapshot descriptors. Common admitted prefixes therefore retain their prior
identities; optional capacity refusals can still make actual prefixes differ.
Public custody and prior targets remain outside the failing index transaction.

## Corrected pre-use issue

The first helper revision compared parsed persisted `access_pairs` with the
validated owner configuration using Python mapping equality alone. JSON true
can equal integer one; the existing strict parser already rejects floating-point
JSON, so that analogous equality case is not a persisted-input exploit. This did not
weaken positive cryptographic proofs, but contradicted strict persisted-config
validation. The author, with root authorization, changed `_state` to call
`validate_config` on persisted access configuration before equality. I inspected
that delta and recalculated the final pin above. Store source did not change.

## Limits and next check

Readiness is a constant-size local invariant check, not a proof that no unvisited
row was deleted. This is explicitly disclosed. Positive records still require
their original atomic proof; complete intersection maintenance relies on the
trusted-owner/SQLite transactional model. Crash durability, arbitrary hardware
corruption, process isolation and full-cost usefulness are not established by
source review.

The next relevant falsifiers are the selected tiny real-Store range query,
old-cut, exact reopen, strict persisted config, duplicate/capacity and genuine
second-orientation SQL-abort rollback controls. No native proof, large-corpus
run or extra maintenance subsystem is needed to exercise this boundary.
