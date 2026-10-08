# SQLite page-tier falsification controls

Source-only handoff, 2026-09-21. The author read the complete
[operating-envelope proposal](../drafts/OPERATING-ENVELOPE.md), authored this
note and `test_sqlite_tiers.py`, and performed no execution, import, compilation,
SQLite query or test. There are **five unittest methods**. Their results remain
unknown until a separately reviewed and supervised root execution.

## Decision being tested

The proposed default database has 4096-byte pages and an 8192-page total cap
(32 MiB). Ordinary writes have a 6144-page ceiling (24 MiB), terminal-only
writes 7168 pages (28 MiB), and administration 8192 pages. New ordinary
reservation additionally requires allocated `page_count <= 4096` (16 MiB).
The tiers are an allocation policy, not a proved bound on storage amplification.

Before implementing that policy in product version 3, try to falsify these
narrow claims on the selected SQLite 3.50.4 runtime:

- Actual allocated pages prevent lowering a connection ceiling beneath them;
  opening at the ordinary ceiling would therefore be the wrong replay policy.
- Opening at the durable total cap permits indexed historical request/grant
  reads after terminal/administrative allocation exceeds the ordinary tier.
- A real `SQLITE_FULL` can be followed by observed rollback and exact preservation
  of an earlier committed pending request, its active key and consumed counters.
- After that verified rollback, a small terminal-only refusal can change only
  the pending request's terminal fields and active slot, with no promotion.
- Atomic cap-only expansion can restore the admission margin without refunding
  consumption or changing mathematical state.
- Near-limit BLOBs, a real index split and sixty-four bounded grant rows have
  measurable storage behavior rather than an assumed byte-to-page ratio.
- Query-only status observation does not change database or sidecar bytes.

Passing these examples would support only this tested workload. Failure should
stop the proposed product change until its cause or numerical policy is reviewed.
There is no automatic repair, smaller retry, substitute assertion or native run.

## Deliberately synthetic schema

Every test creates its own database. No production module, product schema,
native checker, supervisor receipt, accepted context or mathematical object is
imported or fabricated. The schema is a minimal hypothetical storage workload:

| Table | Synthetic purpose |
| --- | --- |
| `state` | One row containing consumed U, authorized A, durable cap, grant count and active request key |
| `requests` | Exact opaque request bytes, pending/terminal phase and bounded refusal bytes |
| `filler` | Up to 2-MiB zero BLOBs supplying measured page pressure; not mathematical records |
| `visible` | Explicitly `synthetic-unpromoted` rows and a separate indexed sort key |
| `owner_grants` | Bounded historical administrative BLOB pairs and unique sequence 1..64 |

The combined `state` row permits direct SQL checks of `0 <= U <= A` and the
selected ceilings. This is **not** a replacement for the proposed product's
separate authorization/meta tables, their transaction discipline or parser.
The schema does not assert every production cross-table invariant. Initial
used requests/reserved bytes correspond to one synthetic old terminal refusal
and, where required, one synthetic pending request. No stage or native work is
represented as accepted. Filler/index records are storage fixtures only.

Large terminal response fixtures are valid JSON marked `synthetic:true` and
`status:REFUSED`; their padding is intentional storage pressure, not useful
content. The real emergency refusal in the full-database test is separately
small, bounded by 4096 bytes, and is not a truncated successful response.

## Five exact tests

### Allocated high-water, lowering and replay

Under the ordinary ceiling, commit eleven 2-MiB filler rows plus one 1-MiB row
(23 MiB of payload, with real measured overhead). Increase only the connection
ceiling to the terminal tier. Complete the synthetic pending request with a
`1 MiB - 64 bytes` refusal and clear its active key. At the administrative tier,
commit sixty-four grant rows, each containing 4096 request bytes and 4096 response
bytes. Require actual pages to exceed 6144 but not 8192.

Attempt `PRAGMA max_page_count=6144`; require its returned ceiling to equal
actual `page_count`, not the impossible requested lower cap. Close, reopen and
explicitly restore the selected durable total cap of 8192. Read the exact old
request and grant responses through indexed ID/raw predicates; require byte
equality and an unchanged complete bounded logical projection.

Finally close the writable connection, require absent/empty sidecars and hash
every fixture file. Open `mode=ro`, enable `query_only`, read bounded status
fields, and attempt an update that must produce real `SQLITE_READONLY`. After
closing, require the entire file-name/size/SHA-256 map to be identical. No test
relies on whether a connection pragma persists across opens.

### Real full transaction, rollback and terminal-only completion

Commit the pending request and eleven 2-MiB filler rows (22 MiB payload) under
the ordinary ceiling. Capture all logical rows, representing BLOB values by
length and SHA-256 to keep evidence bounded. In one new transaction:

1. Insert a synthetic unpromoted visibility row.
2. Write a near-1-MiB terminal response and clear the active key provisionally.
3. Attempt a new `2 MiB - 64 bytes` visibility BLOB.

The third step must raise an actual SQLite error whose base code is
`SQLITE_FULL`; a mocked exception, another error or unexpected success fails.
Record whether SQLite already ended the transaction, call rollback safely in
either case, then require no open transaction and exact equality of the entire
logical projection with the committed prefix. In particular the request remains
pending, its response is NULL, its old active key remains, and no visibility row
survives. This checks observable transaction outcome, not crash durability.

Only after those checks, raise the connection ceiling to 7168 and commit one
small refusal plus the active clear. Require an exact logical delta: only that
request's phase/response and the active field change; U, A, fillers, grant rows
and all other state remain unchanged. The visibility table stays empty.

### Cap-only expansion and restored admission

Commit nine 2-MiB fillers (18 MiB payload). Require actual pages above the
default 4096-page admission threshold, observe the guard refusal without any
logical write, then provisionally raise the connection ceiling and roll back a
durable cap update. Require the old durable cap and entire state to survive:
a pragma change alone is not an owner grant.

Explicitly restore the old connection ceiling, then raise it for a fresh
transaction that adds exactly one synthetic cap-only grant and atomically
changes only cap/grant-count fields to 16384/1 (64 MiB). U and A are unchanged.
The new admission threshold is 12288 pages (48 MiB); require that actual pages
fit, set the new ordinary ceiling to 14336, and commit one real synthetic
pending reservation with its normal 8-MiB request charge. This demonstrates
usable storage headroom without any native or renewal-product qualification.

### Near-limit rows and an observed index split

In one transaction write a `2 MiB - 64 bytes` synthetic record, sixty-four small
synthetic records whose unique indexed keys are 768 bytes, and a
`1 MiB - 64 bytes` refusal response. Obtain the index root page from
`sqlite_schema`. After commit, read its page-type byte using the SQLite file
format: the initially empty index root must change from leaf-index `0A` to
interior-index `02`. This directly observes a split; row count or file growth
alone is not called an index-split measurement. No optional `dbstat` extension
is assumed.

Then commit sixty-four bounded grant rows and assert exact stored payload
lengths, row counts and `PRAGMA integrity_check(1) == 'ok'`. The record and
response bounds are inclusive schema ceilings; the chosen fixtures are slightly
below them so row encoding overhead is not mistaken for payload length.

### Persisted SQL-state invariants and their limits

Attempt negative, over-authorized, nonintegral, nonnumeric, over-ceiling and
unsupported-cap assignments. Require real constraint failures and unchanged
state after rollback. Also require an overflowing SQLite arithmetic expression
to fail the integer/type invariant instead of persisting a REAL counter.

Then explicitly demonstrate a limitation: Python `True` and the string `"2"`
can be bound into an INTEGER-affinity column and stored as integers. Roll back
those demonstrations. A persisted SQL type check **cannot** enforce the original
input token type. Exact integer validation in the eventual parser remains an
independent obligation; these observations must not be misreported as parser
qualification.

## Execution contract and finite allocation

The test requires `-B -E -s -S` and SQLite version exactly `3.50.4`. Root owns
the separate runner and supervision; this module launches no process, thread,
service or native compiler. Proposed external worker allocation is 60 seconds
wall, 30 seconds Job CPU and 512 MiB memory. Those values are root's selected
limits, not measurements or implicit grants from this source note.

Set `DTMKN_TEST_ROOT` to the existing absolute directory
`E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\sqlite-tiers-01`.
It must not overlap the software installation or traverse reparse points. The
test exclusively creates its `sqlite-tiers` child and one directory per method.
Existing suite/fixture roots refuse; nothing is overwritten or removed.

All five databases, observations and any sidecars remaining at the endpoint are
retained. SQLite's ordinary DELETE-journal lifecycle still removes journals after
commit/rollback; sampled journal sizes are not preserved journal contents. Aggregate fixture
accounting is bounded to **256 MiB and 128 entries** at sampled checkpoints and
after each report. This is an observed endpoint/sampled bound, not a hard
filesystem reservation. Root's outer census must additionally count runner
evidence and final reporting overhead within its own selected envelope.

The exact intended successful workload has **37 large-payload write attempts**
totalling **70 MiB minus 320 bytes**. The code stops before more than 64 such
attempts or more than 96 MiB of attempted payload. Failed attempts still count.
Each large payload is at most 2 MiB. Separate small rows include two independent
sixty-four-grant fixtures (128 grant rows total, 1 MiB exact grant-BLOB payload)
and sixty-four small indexed records. They are not hidden in the large-write
counter. No fill-until-success/unbounded allocation loop is used.

Every connection has a 3-MiB SQLite value/row length limit and a progress callback
every 100 VM instructions. The suite interrupts an individual method after its
callback-accounted VM work exceeds 500000; sub-callback work is not claimed
exactly counted. An interruption fails rather than replacing `SQLITE_FULL`.
Each method has at most 256 retained sample rows; each JSON report is at most
1 MiB. All observations are explicitly synthetic and carry no supervisor or
mathematical acceptance claim.

## Evidence and failure boundary

Each method retains `observations.json`, including sampled pages/freelist,
connection ceilings, transaction state, database/journal bytes, aggregate
retained bytes, actual SQLite error code, B-tree split observation where
applicable, status hashes, workload counters and cleanup errors. Journal size
is also sampled from progress callbacks without issuing recursive SQL. Peaks
are **sampled peaks**: a failed statement can allocate and roll back between
samples. They do not certify all transient pages/journal bytes were observed.

Observations are written during teardown even after ordinary assertion failure;
all connections are explicitly rolled back if needed and closed. The independent
unittest outcome, not the presence of an observation file, determines pass/fail.
OS termination or report-persistence failure may prevent teardown; the outer
supervisor must retain whatever actually exists and must not invent success,
zero cost or cleanup. No data is deleted to satisfy an envelope.

An unexpected storage-full location, inability to lower/reopen as assumed,
rollback mismatch, unavailable terminal write, wrong index-page observation,
status-byte mutation, version mismatch or resource overrun stops qualification.
It authorizes diagnosis, not silent fixture modification or a larger retry.
Even a complete pass does not establish crash recovery, physical reserve,
production schema compatibility, indefinite operation, native correctness or
renewal qualification. The next decision remains a reviewed product change
followed by separately allocated product-level controls.
