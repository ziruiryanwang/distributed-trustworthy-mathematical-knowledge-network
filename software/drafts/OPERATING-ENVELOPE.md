# First renewable local operating envelope

Proposed implementation decision, 2026-09-21. This selects a small concrete
next cut from [CAPACITY-RENEWAL](CAPACITY-RENEWAL.md), its
[review](CAPACITY-RENEWAL-REVIEW.md), and the continuing-operation milestone
in [V1-CRITICAL-PATH](V1-CRITICAL-PATH.md). It was checked against current
`py/storage.py`, `py/node.py`, `manage.py` and the existing checking/domain
constraints. Only this document was authored; no product, test, database or
native code was executed or changed.

## Decision

Implement a fresh schema/configuration version 3 with cumulative authorization
separate from consumed work, a finite owner grant command, a genuinely
read-only status command, and SQLite page tiers for ordinary writes, terminal
refusals and administration. Keep the current single writer, exact request
replay, per-operation limits, mathematical checking path and retained files.
No migration, garbage collection, global identity system or automatic renewal
belongs to this cut.

These are engineering ceilings and guard policies, not claims that every
possible workload reaches every ceiling. A node can exhaust metadata or
physical space before its logical credits. A grant is authorization to spend
supplied capacity; it is not evidence that capacity exists.

| Dimension | Fresh default | Absolute ceiling for this cut |
| --- | ---: | ---: |
| Authorized ordinary requests | 128 | 4,096 |
| Authorized mathematical stages | 16 | 256 |
| Authorized cumulative reserved bytes | 4 GiB | 64 GiB |
| Successful owner grant records | 0 | 64 |
| Control database cap | 32 MiB / 8,192 pages | 256 MiB / 65,536 pages |
| Clients, provider entries, context package count | Existing 16 / 8,192 / 16 | Unchanged |

The last permitted stage allocation has ID 255 and directory `stage-0255`.
This is comfortably inside existing exact-four-digit recognition. Increasing
the lifetime ceiling to 10,000 is not selected; any future change must retain
IDs 0..9999 or separately revise every affected consumer. Request, stage,
entry, record and metadata ceilings are independent, not interchangeable.

Expose fresh-only `configure --initial-requests N --initial-stages N
--initial-reserved-mib N --initial-metadata-mib N`. The first two range from 1
to their table ceilings. Reserved MiB ranges from 136 to 65,536 for the normal
8-MiB request plus 128-MiB stage profile, and must cover one bootstrap request
and stage if those per-operation grants ever become configurable. Metadata
MiB must be one of 32, 64, 128, 256. Defaults remain those above. Validate exact
integers before pinning/build inspection/directory creation; CLI conversion
does not replace validation in `configure` and `load_config`. Do not edit an
initialized configuration to change any value.

## Fresh storage format and ownership

Use config `schema: 3` and SQLite `PRAGMA user_version=3`. A fresh database
creates the existing eight tables plus exactly two new tables in its initial
schema transaction:

- `authorization`: singleton ID 1, config digest, authorized request/stage/
  reserved-byte integers, selected metadata-page cap, and successful-grant
  count. Initial values are copied from immutable configuration exactly once.
- `owner_grants`: unique grant ID, unique sequence 1..64, exact envelope BLOB
  up to 4,096 bytes, and exact successful response BLOB up to 4,096 bytes.

Keep `meta.requests`, `meta.stages`, and `meta.charged` as consumed vector
`U`. In the new API, `reserved_bytes` names `meta.charged`; it includes BOTH
ordinary request grants and native-stage grants, never actual file size.
The authorization row is vector `A` plus metadata cap `B`. Do not cache A by
recomputing it from config on open, and do not reconstruct it through an
unbounded history scan. Keep normal exact indexed request/grant lookup.

Use SQL type/range checks on persisted counters, and validate loaded integers
with exact integer tests before use. Require `0 <= U <= A <= ceilings` and
valid metadata/grant counters. Validate additions in Python before SQL; assign
the checked integer results rather than trusting an overflowing SQLite `+`.
The chosen limits are far below signed-64-bit boundaries. Malformed internal
state refuses; a grant does not repair it.

New code rejects config/schema 2 and unsupported existing `user_version`
without adding tables, resetting counters or changing their configured pins.
Read the existing version before applying writable setup pragmas. Update the
new cut's config/domain reader explicitly for version 3; preserve unrelated
stage-plan and mathematical object schemas unless their formats change.
Frozen old installations retain their own runtime/source and history. There
is no implicit in-place migration or reuse of old accepted receipts under a
new config identity.

Authorization is created when the fresh control store is created; it survives
a later bootstrap failure unchanged. Fresh grants require successful node
initialization. Failed initialization/pending work still needs its separate
reconciliation contract; renewal is not a shortcut around it.

## Ordinary work accounting

Preserve `prior(client,id,raw)` before all new-work capacity/headroom checks.
An exact terminal retry returns its original bytes even after subsequent
logical or metadata exhaustion; different bytes conflict and a pending retry
remains blocked. These guarantees still require readable intact state and the
ordinary output/evidence supply.

In `reserve`, require `U_requests + 1 <= A_requests` and
`U_reserved + request_grant <= A_reserved`, then commit the ordinary pending
row, attempt marker, active key and consumed counters together. In `stage`,
require `U_stages + 1 <= A_stages` and
`U_reserved + stage_grant <= A_reserved` before committing the stage row and
charge. Read A under the existing owner lock/transaction at both sites.

Per-operation grants remain ordinary 8 MiB, acquisition 64 MiB, exposure
80 MiB, and the configured 128-MiB stage default; existing per-call CPU/time/
memory, source, proof, package and response limits remain unchanged. A refused
reservation consumes nothing. A stage refusal after a request reservation
retains that request's charge. Failed native work and all retained evidence
remain consumed. Renewal supplies no refund and no automatic retry.

## Owner grants: one exact envelope and transaction

Add `manage.py renew --config ABS --request ABS` using a separate bounded
administrative worker, not an ordinary dispatcher operation. The strict
envelope is:

```json
{"schema":1,"op":"renew","grant_id":"owner-grant-001",
 "config":"EXPECTED_CONFIG_SHA256",
 "add":{"requests":1,"stages":1,"reserved_bytes":142606336},
 "metadata_cap_mib":32}
```

`metadata_cap_mib` is optional: omission keeps B. `grant_id` is a 1..64 ASCII
safe identifier used as a database key, not an authority or mathematical ID.
Reject unknown/duplicate fields, floats, booleans, negative increments and
oversized input. Require a positive increment or a strictly larger selected
metadata cap; all-zero/no-expansion grants refuse. A requested cap may equal
the present cap but may never lower it, and must be one of the four supported
sizes. The owner interface supplies authority locally; no remote grant API,
signature scheme, peer acceptance or service-session renewal is added.

Under the existing writer lock, validate schema/config and use this order:

1. Look up the grant ID. If present and raw bytes match exactly, return its
   stored response immediately. Do not recheck active work, current remaining
   credits, new-grant count, physical expansion needs or current authorization
   as if this were a fresh grant. Different bytes return `GRANT_ID_CONFLICT`.
   This includes whitespace differences. Basic integrity/config authentication
   still applies; corrupted state is not covered by replay promises.
2. For an absent ID, require initialized state, `meta.active IS NULL`, valid
   U/A, fewer than 64 successful grants, valid proposed sums/cap, and the
   headroom/physical premises below. Return `PENDING_EXECUTION` for a live or
   stranded active key. Never clear it or remove a charged stage.
3. Within one visibility transaction, recheck these guards, insert one exact
   grant record, assign A+d and B', increment the grant count, and store the
   exact success response. U, ordinary requests/stages, mathematical records,
   heads, providers, snapshots, entries and files remain logically unchanged.

The bounded success response names the grant ID/sequence, config,
`authorized_before`, `authorized_after`, `metadata_cap_before/after`, and
`used_at_commit`, and explicitly says `mathematicalAcceptance:false` and
`refund:false`. Those are historical values, not current remaining capacity.
Exact replay cannot add a new `historical` field to those bytes; the separate
administrative event records whether this invocation replayed. Use status
for current observations.

Only committed successful grants occupy `owner_grants`. Every pre-commit
refusal says `grant_recorded:false` and `state_outcome:UNCHANGED_BY_RENEWAL`;
the same previously refused ID may succeed after conditions change. Such
unrecorded refusals have no exact historical replay promise. They must not
claim that an ambiguous commit failed. Commit/persistence uncertainty returns
`RENEWAL_OUTCOME_UNKNOWN`, with no false unchanged assertion; retry the SAME
exact envelope to discover whether it committed. Missing caller output is
not permission to use a new grant ID. Retain actual costs and evidence on
every path.

Metadata-cap expansion is part of this same exact grant, not a third subsystem.
It monotonically raises the durable selected cap before enabling more normal
writes. A cap-only grant is valid. It cannot exceed 256 MiB, replenish the
64-grant limit, raise unrelated record/package/entry limits, or supply disk.

## Metadata headroom: actual page tiers, measured margins

Keep SQLite 3.50.4, 4,096-byte pages, delete-journal mode, FULL synchronous,
memory temp storage and the existing single-writer/nonempty-sidecar refusal
profile. The selected cap B replaces hardcoded `max_page_count=8192` in this
new cut. Persist B in authorization, not only in a connection pragma.

For every selected B, choose these fixed tiers:

| Tier | Maximum database pages | Allowed new writes |
| --- | ---: | --- |
| Ordinary | B minus 2,048 pages (8 MiB) | Reservations, stages, ordinary visibility transactions including successful terminal replies |
| Terminal-only | B minus 1,024 pages (4 MiB) | One pending request's failure response/terminal phase and active-slot clear only |
| Administrative | B | Successful owner grant/authorization transaction only |

Require an additional 2,048-page (8-MiB) admission margin below the ordinary
tier before reserving NEW work. At default B=8,192 this means new admission
requires `page_count <= 4096` (16 MiB); ordinary writes can reach 24 MiB,
terminal-only writes 28 MiB, and administration 32 MiB. At larger B the same
margins apply. Use actual allocated `page_count` conservatively, without
treating freelist bytes as supplied physical storage or reclaiming them.

Crucial ordering: open the database at its durable TOTAL cap B, authenticate
it and perform exact historical replay first. Do not lower the cap to the
ordinary tier at connection open. SQLite cannot set `max_page_count` below
the current page count; terminal/admin use above the ordinary tier must not
strand old replies. Before a new ordinary reservation, inspect actual pages
and refuse `METADATA_HEADROOM` with no new row/charge if the admission margin
does not fit. Only then set/check the ordinary connection ceiling for its
writes. Keep the writer lock throughout; every new connection repeats this
policy. Do not depend on undocumented persistence of a previous connection's
pragma setting.

If ordinary `SQLITE_FULL` is encountered during a transaction, require its
rollback to finish and recheck the selected request remains pending with the
same active key before attempting a terminal-only refusal. The permitted
terminal write cannot create a context, entry, publication, candidate or
mathematical acceptance. It preserves all consumed charges. The existing
maximum allowed failure response remains 1 MiB; a metadata-space refusal is
small and bounded, not a truncated successful acceptance. Failed native or
prepared files remain retained. If rollback/pending binding cannot be
established, or the terminal write itself fails, retain an uncertain/pending
outcome. Do not promote partially persisted visibility, claim rollback, or
use grant authority to clear it. This is not general crash recovery.

Fresh admin work uses B (or the explicit proposed larger B') after its replay
check. Validate actual pages before any attempt to lower a connection cap;
expansion is only upward. Apply a proposed larger connection ceiling only to
the owner transaction, and persist the authoritative B' atomically with the
grant. If that transaction does not commit, the old durable B remains the
policy; next open reestablishes it. Do not treat a transient pragma change as
a committed grant. If actual pages cannot be reconciled with durable B after
a storage failure, status reports the inconsistency and new writes stop.

The tier partition is an enforceable allocation policy under SQLite's stated
behavior; the 8/4/4-MiB margins are deliberately conservative engineering
choices. They are NOT a proved upper bound on B-tree splits, overflow pages,
indexes, rollback journals or all possible operation encodings. A normal
operation can exceed its available metadata tier and refuse despite valid
logical credits. Native work consumed before that refusal stays charged.
Owner cap expansion can restore admission headroom; at 256 MiB, exhaustion
is a declared stop, not an invitation to reset history.

Before wiring these tiers into live product paths, use a separate synthetic
SQLite test to check the exact pragma/rollback behavior on this runtime:
filled ordinary tier, denied reservation, failed visibility transaction and
terminal-only completion, admin growth above the ordinary tier, exact old
request/grant replay at that point, and a cap-only grant reopening ordinary
headroom. Include near-limit 1-MiB responses, 2-MiB records, index splits and
the 64 bounded grant rows. Measure peak pages and journal bytes. If margins
fail this qualification, revise the numeric policy before native execution;
do not call the present numbers formally certified.

## Physical supply and status when credits run out

The first envelope is one trusted local Windows/NTFS volume for state and
scratch, with no competing writer that consumes the supplied reserve.
Installation/runtime may be elsewhere. Check actual OS volume identity, not
only drive-letter spelling. Owner-supplied physical capacity, stable storage,
working permissions and intact evidence remain premises. The OS/filesystem
can still fail; this is not a disk reservation or power-loss guarantee.

At fresh configuration, new ordinary admission, and a NEW owner grant, sample
free bytes and require at least:

```text
(proposed authorized_reserved_bytes - current used_reserved_bytes)
    + 2 * proposed_metadata_cap_bytes + 1 GiB
```

The first term conservatively covers the remaining authorized retained work;
the rest is a chosen database/journal/transient/diagnostic supply margin.
Existing retained work is already on disk. Do not compare consumed reserved
bytes to free space as if they were actual retained file bytes, and do not
refund the difference. Preserve existing endpoint audits of selected work
and stage directories. Checkpoint limits do not prevent every transient disk
burst, and the `2*B + 1 GiB` margin is an empirical profile assumption, not a
formal maximum. Unrelated writes or unexpectedly large temporary behavior
can invalidate it. Exclude support-build/runtime installation supply from
claims about this node's retained-work authorization and account it separately.

Exact replay precedes the above NEW-work free-space test. It still needs
enough physical diagnostic/output supply; no interface is promised available
on a completely full, unreadable or corrupted disk. Status reports physical
free bytes as a sample, not a reservation or a theorem of future availability.

Add `manage.py status --config ABS`. It does not call ordinary `reserve`,
append a request/grant row, construct a candidate, call the checker or mutate
the store. Acquire the existing owner lock without creating a missing store;
if another writer owns it, return bounded `BUSY`. For initialized state,
require the selected schema/config and no nonempty sidecars, open SQLite
`mode=ro`/query-only under that lock, and read only fixed bounded fields:
U, A, remaining A-U, selected cap/tier thresholds, page/freelist counts,
active key plus its indexed request ID/phase, grant count, provider cut, and
at most sixteen client heads. No full history scan or attempt to recover a
journal. For absent/uninitialized state, report that explicitly without
manufacturing authorization or mathematical status.

Status is a snapshot observation, including when logical credits or new-work
metadata headroom are exhausted, and when a pending request blocks renewal.
It never asserts that historical contexts' live files are intact. Give
distinct reasons for ordinary quota, metadata headroom, physical supply,
active/pending, schema and sidecar failures so an operator knows whether an
explicit grant/cap expansion can help. Do not exempt existing `find` or
ordinary `info`; those paths retain their current accounting/side effects.

Both status and renew use their own finite supervisory profile: 10 seconds
wall, 5 seconds Job CPU, 128 MiB memory, eight active processes, 16-KiB request
envelope allowance, 64 KiB stdout/stderr/event each, at most 100,000 SQL VM
steps and bounded indexed rows. These are selected initial limits to qualify,
not measurements. Each explicit invocation has at most 1 MiB of retained
diagnostic files in a fresh selected scratch subdirectory; no auto-polling,
automatic retry, or permanent DB row per status poll. Repeated diagnostic
calls still consume real disk/CPU supplied by the caller and are not an
unlimited free service. Status's read-only claim concerns node state, not
absence of supervision evidence files.

## Conditional invariants versus qualification evidence

Given atomic SQLite transactions, writer exclusion, intact typed state and
the trusted runtime: ordinary reservation preserves `U <= A`; a committed
fresh grant leaves U unchanged and increases A/B monotonically; exact replay
does neither. Grants/status write no mathematical authority. Headroom guard
refusal before reservation consumes no ordinary credit. These are small
conditional state arguments suitable for unit/model tests.

SQLITE_FULL behavior, space needed by terminal/admin records and their
indexes, journal growth, timing, actual disk supply and observed cleanup are
empirical obligations. No proof of U/A monotonicity discharges them. Numeric
parser ceilings likewise do not certify a 4,096-request/256-stage long-run
reliability horizon. Record actual workloads/pages/bytes and extend the
qualification horizon deliberately; do not advertise indefinite operation.

## Small genuine renewal discriminator

Use one fresh prepared installation/store with two initial ordinary requests,
one initial mathematical stage and 144 MiB reserved-byte authorization.
No fabricated pending request or accepted context is used in this positive
test. Count any needed support build and its two compilations separately.

1. Normal bootstrap consumes one request, one stage and 136 MiB (8+128).
2. Submit a valid tiny source against the returned context. Its request
   reservation consumes the remaining request and 8 MiB, but stage allocation
   refuses `STAGE_QUOTA`; it must perform no second native stage or promotion.
   All three initial dimensions are now exhausted: `U=(2,1,144 MiB)`.
3. Status still reports that state. A new ordinary request refuses before
   reservation with no extra row/charge. Record actual failure CPU and bytes.
4. Owner grant G1 adds `(1 request, 1 stage, 136 MiB)`. Compare complete bounded
   ledger projections: only authorization/grant rows change. Exact G1 retry
   replays its original bytes with no second increment.
5. Submit the valid source under a NEW ordinary ID. It now completes one
   genuine native stage and returns the normal checked artifact. This is the
   second and last mathematical native stage, including bootstrap. End use is
   `U=(3,2,280 MiB)` and the renewed authorization is exhausted again.
6. Grant G2 adds `(1 request, 0 stages, 8 MiB)` and ordinary `info` succeeds.
   This demonstrates a second continuation without another native stage.
   Replay old ordinary success/refusal bytes and G1/G2 exactly; verify no
   reexecution, head movement, counter reset, file deletion or second grant.

Measure every call, database pages, journal/retained files and actual process
cleanup. The two grants are not mathematical contributions. The source result
is ordinary new checked work and must retain its exact original context and
native evidence. Missing/changed historical bytes, output loss and pending
uncertainty must not be repaired to force success.

Use separate native-free synthetic/unit controls for Boolean/negative/large
integers, all ceilings, grant-ID conflicts, unrecorded-refusal retry semantics,
pending fresh-grant refusal versus committed-grant replay, transaction rollback,
simulated caller output loss after commit, metadata-tier exhaustion/expansion,
status no-write behavior and schema rejection. Clearly label synthetic state;
do not turn it into native acceptance evidence. A live process/journal crash
claim needs its own reviewed discriminator, not this renewal success test.

This is enough to begin the small versioned implementation after the page-tier
test. It solves explicit bounded continuation at logical exhaustion. General
ordinary-operation reconciliation, archival/GC, in-place upgrades, large-corpus
retrieval and independently hosted replication remain separate critical-path
work; this document does not mark the usable-v1 goal complete.
