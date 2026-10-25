# Grounded-cut protected catalog — source-only contract

This is a private storage boundary for the actual protected grounded-cut
controller. It is **not** a peer admission interface, mathematical checker,
controller implementation, or release qualification. No execution is selected.

The protected controller alone establishes bootstrap derivation and each clean
worker event. Neither imported summaries, stored success text, a caller-created
record, nor a matching hash establishes that authority. Calling these private
methods from untrusted code is outside the contract. The owner OS/storage and
controller code must be protected; whole-store rollback is excluded. Content
addressing detects accidental corruption, not a rewrite of that authority.

## Identity and lifecycle

`CutCatalog.open(directory, *, store_id, support_id, epoch, source_binding_raw,
check, create=False, limits=Limits())` binds a distinct grounded-cut schema and
three lowercase SHA-256-shaped identities. `support_id` identifies the actual
controller/kernel/adapter support selected by the controller; it is not a claim
this module can authenticate independently. `epoch` is a conservative support
epoch, not an arbitrary rename that can rehabilitate withdrawn results.

The canonical adoption marker contains these identities, the SHA-256 of the
entire exact source binding, the complete binding bytes, and the selected finite
limits. The database's sole `meta` row contains the exact marker, activation
state, bootstrap root and six cumulative quota counters. Every operation checks
that row by its primary key and checks the unchanged adoption file. No history
scan, operation recovery UPDATE, `count(*)`, map census or ancestor walk occurs.

`check` MUST run the original nonrenewing operation-budget check and the held
`SourceAnchor.check`. The controller must bind that anchor to the same exact
captured binding. Syntax-valid supplied binding bytes are not migration authority.
Calls occur on open, each operation and immediately before committing authority.
Callback or live-state failure denies further operations on that handle.

A fresh directory enters `BOOTSTRAPPING`. It grants no local origin and cannot
be reopened after an interrupted bootstrap. Only the actual one-time importer,
holding eligible native source authority, may commit its derived bootstrap root.
The same atomic transaction makes the store `ACTIVE`. An existing store opens
only if active with a nonzero committed-root counter. Requested roots still
require exact bounded committed-table membership; opening a catalog does not
accept every identifier supplied to it.

Owner locking is the existing Windows one-byte lock over an ordinary local file.
All selected paths exclude redirects/hard links. `WITHDRAWN` always refuses;
removing that protected marker is not a supported operation. SQLite uses DELETE
journaling, FULL synchronization, a fixed page size and a selected maximum page
count. Reopen refuses any journal/WAL/SHM sidecar instead of silently performing
recovery. This source slice intentionally has no recovery, source relocation,
epoch transfer, migration-resume, lock removal or quota-reset command.

## Event transaction API

1. Call `_begin(original_cut_map_allowance)` once. The caller retains its original
   finite `cut_map.Allowance`; the catalog does not replenish it.
2. `root(root_id)` reads one content-addressed root from the committed root table.
   `lookup(root_id, encoded_name_bytes)` resolves the exact map value, or absence
   under that root. Names are canonical encoded-name bytes, never dotted strings.
3. `put_summary(raw)` stores bounded opaque bytes; `read_summary(id)` reads them.
   All roles use `SHA256(b'DMKN-GROUNDED-CUT-SUMMARY-V1\0' + raw)`, matching
   `cut_summary`. The controller validates the distinct theorem/frontier/result/
   event schemas and their roles. A blob by itself grants no warrant.
4. `_insert(map_root, encoded_name_bytes, value_bytes)` path-copies the map. The
   controller supplies canonical `[exactSymbolId, summaryDigest]` value bytes.
   The starting map must have been obtained from a rooted lookup in this event,
   a prior insertion in this event, or the empty map during bootstrap.
5. After the actual clean worker event and all mathematical checks,
   `_commit_root(record)` atomically adds the root and commits the already-staged
   summaries/map nodes plus quota/state changes. It returns the exact root ID.
6. `_abort()` discards an uncommitted transaction. `close()` releases resources;
   unfinished database changes cannot become local origin by reopening.

The catalog checks storage lineage and presence, not the mathematical relation
between a parent, packet, map update and result. In particular, the controller
must prove that the selected output map extends the **named** parent, that new
names are absent in its whole root, and that every summary used by the worker is
grounded in that parent. Merely reading another committed map in the same event
does not authorize substituting it. A source review of the whole controller is
required before this API can be exercised as acceptance.

## Root record

Exact fields are `schema`, `store_id`, `support_id`, `epoch`,
`source_binding_sha256`, `kind`, `parent`, `map_root`, `request_id`, `unit_id`,
`frontier_summary`, `result_summary`, and `event_summary`. The schema is
`DMKN_GROUNDED_CUT_ROOT_V1`. Root ID is
`SHA256(b'DMKN-GROUNDED-CUT-ROOT-V1\0' + canonical_json(record))`; the record does
not contain its own ID. All nonempty identities have exact lowercase hex form.

`native-bootstrap` requires empty parent/unit ID and is allowed only once while
bootstrapping. `theorem-cut` requires an existing eligible parent in the same
store/support/epoch/source binding and the exact new unit ID. All three summary
references must exist in the current transaction. The controller binds the
event summary to actual clean worker input bytes, result and supervision
observation; a Boolean `PASS` is insufficient. Duplicate root insertion refuses.

## Costs, failures and authority

Roots and summaries use exact primary-key reads with SQL-side length/type checks
before payload materialization. Their logical reads/writes/bytes share the
original map allowance. Map insertion charges its actual new-node writes/bytes.
The fixed metadata/identity checks and SQLite physical page work are not those
logical payload counters: they remain inside the original enclosing supervised
CPU/wall/storage bounds. A quota UPDATE touches only the one metadata row.

The six counters bound committed roots, summaries, summary bytes, nodes, node
bytes and root bytes. Counters are advanced only with the atomic event commit.
The separate SQLite page ceiling bounds physical persistent storage; a journal
has its own fixed size bound. Quotas can refuse a transaction after bounded
staging; no prefix is accepted and rollback discards it. There is no free
garbage collection or indefinite-capacity claim.

Before-COMMIT operation failures roll back the event. A COMMIT exception closes
the handle and raises `CommitDisposition` with the **exact candidate root ID**
and `NOT_COMMITTED`, `COMMITTED`, or `UNKNOWN`. An active transaction is rolled
back before `NOT_COMMITTED`; after SQLite reports no transaction, one bounded
exact-root read may establish `COMMITTED`. Otherwise the result is `UNKNOWN`.
Neither uncertainty nor a committed disposition authorizes retry. The controller
retains diagnostics and must never roll back a confirmed root. Normal successful
COMMIT returns its identity without another fallible acceptance callback.

Abrupt process death can prevent both the return value and the exception. The
controller must durably bind a request to its exact candidate root before COMMIT,
or provide another bounded indexed resolution path. This catalog does not scan
root history to reconstruct an unknown candidate and does not by itself provide
that user-facing crash-resolution workflow.

Any persistent authority conclusion is conditional on the actual protected
controller and storage premises. This file alone does not demonstrate mathematical
soundness, performance improvement, continued export custody, usable recovery or
deployable-v5 readiness. It removes a particular required lifetime-history scan
from the candidate local reuse design, not from all costs of mathematics.
