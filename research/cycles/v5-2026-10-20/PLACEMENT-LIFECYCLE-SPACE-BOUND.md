# Finite storage envelope for two placement generations

2026-10-21, core_growth. Source-only response to
`PLACEMENT-NETWORK-REPAIR02-SELECTION.md`; complements
`PLACEMENT-LIFECYCLE-SEAM.md`. No product execution/import, test, build,
deletion, operating-system change, cloud use or Git mutation. Read-only upstream
SQLite source was fetched into memory; no external code was executed.

## Decision

**Use an explicitly supported SQLite/storage profile and a conservative finite
disk envelope. An operating-system quota is not intrinsically required for
this trusted-owner, closed-SQL service.** Keep normal cache spilling and durable
DELETE rollback journals. Do not switch the main journal to MEMORY, disable
cache spill, demand more RAM or launch a storage-filling experiment.

The present sources do not yet establish that profile for every connection:
the six Python stores request MEMORY temporary storage but do not check page
size; the selected Node metadata store fixes 4096-byte pages but does not set
MEMORY temporary storage. Runtime/VFS correspondence is also not established
by this note. These are narrow prospective guards, not a reason to delay core
certificate/growth work with another resource investigation.

If an operator instead requires an unconditional hard physical quota across
unknown VFS behavior, arbitrary local writers or unbounded diagnostics, use a
real quota/container boundary. A page cap alone never provides that guarantee.

## Actual source boundary

Resolve installed logical sources through `sdk_sources` in
`experiments/v5-local-checks/distribution-terminal-i-01-input.json`
(SHA-256 `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`).
The proposed generation has these persistent SQLite files:

| File | Selected implementation |
|---|---|
| `workspace.sqlite` | `software/v5/terminal_i/client/workspace_evidence.py` |
| `modules/modules.sqlite` | `software/v5/custody/module_store.py` |
| `packets/evidence-packets.sqlite` | `software/v5/terminal_i/evidence_network/custody.py`, inherited `software/v5/delta/custody.py` |
| `index/discovery.sqlite` | `software/v5/selective_placement/discovery/discovery_store.py` |
| `placement.sqlite` | `software/v5/selective_placement/placement/ledger.py` |
| `placement-routes.sqlite` | `software/v5/placement_network/placement/advertisement.py` |

They select DELETE, FULL synchronous, MEMORY temporary storage and finite
`max_page_count`; none selects WAL, ATTACH, VACUUM or explicit SQL savepoints.
The placement-only path creates no mathematical operation payloads. SQL and
schema are trusted local code; peers cannot submit SQL or executable triggers.
An error exits/rolls back the transaction rather than continuing a failed
statement repeatedly in the same transaction.

Each permitted run separately creates Node `metadata.sqlite`. Its actual base
implementation is the installed
`product-local/v5-distribution-terminal-i-01/Mathematical Commons v5/base/overlay/quota_store.mjs`.
It sets/checks 4096-byte pages and a page cap, selects DELETE/FULL/EXCLUSIVE,
and performs bounded key operations and startup census. Its limits include
at most 65,536 rows, 128 MiB charged logical bytes and 65,536 pages; these maxima
are not recommended allocations. Batches are bounded. It lacks `temp_store`.

The selected controller requires **fresh Node state and evidence paths on every
run**. Thus startup schema/census before the first network operation concerns a
fresh, empty store, not all prior metadata. `max_runs` bounds how many such
paths can exist within one generation; a failed startup still consumes a run.

## Supported profile

For every generation/registry database and every Node run, require:

- Verified page size `P = 4096`, immutable finite page cap `N`, DELETE journal
  mode, FULL synchronous and effective MEMORY temporary storage.
- Fresh supported schema, `auto_vacuum = NONE`, no VACUUM, ATTACH, backup/page
  relocation, extension loading, triggers or caller-supplied SQL. No explicit
  savepoint/retry loop. Implicit statement rollback remains allowed.
- Exact adopted SQLite source/build and VFS behavior corresponding to the
  pager argument below. The reported SQLite version alone is not a guarantee
  about a modified build. In particular, `SQLITE_TEMP_STORE=0` can defeat the
  requested memory-temporary mode; readback alone must not silently override
  the adopted build's effective behavior.
- Ordinary managed files, one owning service, finite known file inventory,
  finite output lengths, no symlink/reparse alias and no unrelated writers.
  Existing files must already satisfy the profile, including any hot journal.
  Unknown files or profiles fail closed rather than being deleted or adopted.
- A documented upper bound `S` on SQLite's effective journal-header sector
  size, and filesystem allocation quantum `A`. Page size, hardware sector size
  and filesystem cluster size are different quantities.

Fresh Python stores can be checked immediately after construction and before
exposure. The adopted runtime must establish their initial default profile;
checking after a write is not retroactive containment for an unknown build.

For Node the smallest future change is a fresh successor of
`software/v5/portable_runtime/location/intent.mjs`: immediately after
`await super.open()`, set/check effective `temp_store=MEMORY` and the supported
profile before the existing intent scan or network work. No bundled-vendor
rebuild is needed. The fixed empty-store initialization that precedes this
guard needs a small separately justified startup allowance under that adopted
runtime. This route is valid only because the selected controller requires a
fresh store; it must not be generalized to reopening an arbitrary large store.
Alternatively a future base-store successor can establish the profile before
all initialization, eliminating that startup exception.

This note selects neither change. Root owns any fresh source selection.

## Conservative rollback-journal bound

The source argument uses upstream SQLite **3.50.4**, not an assumed statement
about every installed Node/Python version. For a particular database let `N`
be its page cap and `P` its verified page size. Under the profile above:

1. The main database's apparent length is at most `N P`.
2. A main-journal page record contains one original page plus an 8-byte
   page-number/checksum overhead. `pager_write` journals an original page only
   when its `pInJournal` bit is clear; successful journaling sets that bit.
   Therefore at most `N` original-page records are appended in a transaction.
   Page relocation is excluded: `sqlite3PagerMovepage` has an error path that
   can clear this bit, invalidating an unconditional page-once argument.
3. One header is opened initially. A cache spill can write an additional header
   through `syncJournal(..., 1)`. The first such sync can be needed merely to
   leave WRITER_CACHEMOD. Subsequently a spill requiring sync must follow a new
   old-page journal record: sync clears every NEED_SYNC flag; newly appended
   pages only acquire that flag before WRITER_DBMOD; large-sector propagation
   cannot create it without an already flagged page. No page relocation is
   available to reintroduce flags. Thus a conservative header count is `N+2`.
   Commit uses `syncJournal(..., 0)` and adds no new header. Any error terminates
   the operation; it is not an unlimited header-creation retry.
4. Each header plus preceding alignment consumes at most `2S` bytes. Reserve
   another `S` conservatively for the old-header invalidation boundary. No
   ATTACH means no super-journal pathname trailer. A stale journal from an
   interrupted supported operation is bounded by the same envelope; exclusive
   mode may retain/rewrite that high-water file, not accumulate one per commit.

Consequently a sufficient journal allowance is

    J(N,P,S) = N(P+8) + 2S(N+2) + S.

For file-allocation rounding `round_A(x) = A ceil(x/A)`, reserve

    D(N,P,S,A) = round_A(NP) + round_A(J(N,P,S)).

This is a conservative **data-stream** bound, not a measurement, optimal bound,
free-space reservation or universal SQLite theorem. Filesystem metadata, owner
registry/locks, startup exception and capped outputs are charged separately.
Filesystem snapshot/COW retention, OS paging, antivirus logs and other software
are outside a managed-directory allocation and require their own policy.

The reviewed pager clamps its effective sector size to at most 65,536 bytes.
Using that maximum is sound under the pinned-source premise but pessimistic:
`D` is roughly 34 times the capped main DB length at 4096-byte pages. A supported
VFS bound `S <= 4096` gives roughly four times the main DB length. Adopt the
smaller value only from actual selected VFS/source behavior; do not infer it
from page size or a typical disk. Small service page caps are preferable to
turning a worst-case allowance into a new RAM/performance tuning project.

Temporary-file exclusion is substantive. SQLite can create **implicit** statement
journals even without explicit SQL SAVEPOINT. In this source, btree passes
`sqlite3TempInMemory` to the pager; `subjInMemory` selects a nonspilling memory
subjournal. Sorter setup likewise uses that effective setting to avoid external
PMA spill. Thus the supported MEMORY-temp profile excludes disk statement/sort
temporary files, while the main rollback journal remains durable on disk.
Memory-allocation failure may refuse an operation; it is not permission to
silently switch to unbudgeted disk files. The normal dirty-page cache may still
spill to the main database after journal synchronization.

## Whole generation, including every run

Let `N_1,...,N_6` be the six persistent page caps, `N_node` the selected Node
cap, `R` the prepaid generation run count and `E_run` a finite non-SQLite run
file allowance. Reserve

    B_generation = sum_i D(N_i,P,S,A)
                 + R [D(N_node,P,S,A) + E_run]
                 + E_generation.

`E_run` must include the fixed empty-startup exception, two identity/adoption
files (each at most 1024 bytes on the selected read path), controller config and
source map (each at most 16,384 bytes), capped terminal/supervisor diagnostics,
closure record, file rounding and bounded directory metadata. Channel totals
are bounded at 1 MiB in each direction, frames at 64, and retained stderr at
65,536 bytes, but **these memory/protocol bounds do not cap a wrapper's disk log
automatically**. Give any persisted transcript an explicit finite byte cap;
otherwise do not claim this envelope.

`E_generation` covers marker/config/lock, provisioning record and their bounded
metadata. No unbounded owner-side audit history may sit outside these charges.
The source/runtime installation is one fixed shared overhead, not a copied
installation per run. If an operator chooses extra archives, budget them
separately rather than calling the generation reclaimed.

For the two-slot lifecycle:

    B_total = B_fixed_installation + B_registry + B_cleanup
            + B_generation_0 + B_generation_1.

All `R` run envelopes remain reserved even if only one run is active; crash
journals and previous evidence do not disappear when a process stops. Registry
storage obeys the same SQLite profile. Cleanup headroom must suffice while both
slots are full. Failed provisioning/deletion remains charged and blocks a third
slot. This converts per-operation bounds into a lifetime bound without a log
compactor or cross-generation references.

## What this resolves, and what remains

The lifecycle can have a finite supported data allocation using existing SQLite
page caps plus explicit overhead, without an OS change or more RAM. A free-space
check is still advisory: another application can consume space afterward, so
disk-full handling remains refusal/recovery, not a capacity promise.

Before adopting an actual physical-envelope claim, bind the chosen Python and
Node SQLite/VFS implementations, add the tiny profile guards and finite output
caps, and have the reviewer check this argument against those exact sources.
Use a single tiny changed-boundary fixture for guards/failure handling if needed;
do not run a full-volume saturation test to estimate a worst-case bound.

Until then, existing placement runs retain their existing scoped guarantees;
they are not retroactively qualified for this prospective lifecycle envelope.
No inference of mathematical soundness, independent replicas, public deployment
or net useful-growth benefit follows from a storage bound. Return engineering
attention to certified reuse, selective placement and their full-cost benefit.

## Primary-source anchors

- [SQLite 3.50.4 pager.c](https://www.sqlite.org/src/raw/src/pager.c?ci=version-3.50.4):
  `MAX_SECTOR_SIZE`, `sqlite3SectorSize`, `journalHdrOffset`, `writeJournalHdr`,
  `syncJournal`, `pagerStress`, `pager_open_journal`,
  `pagerAddPageToRollbackJournal`, `pager_write`, `pagerWriteLargeSector`,
  `openSubJournal`, `sqlite3PagerMovepage`.
- [SQLite 3.50.4 btree.c](https://www.sqlite.org/src/raw/src/btree.c?ci=version-3.50.4):
  write-transaction `sqlite3PagerBegin(..., sqlite3TempInMemory(...))`.
- [SQLite 3.50.4 memjournal.c](https://www.sqlite.org/src/raw/src/memjournal.c?ci=version-3.50.4):
  negative spill threshold means no disk spilling.
- [SQLite 3.50.4 vdbesort.c](https://www.sqlite.org/src/raw/src/vdbesort.c?ci=version-3.50.4):
  effective temporary-in-memory mode and external sorter setup.
- [SQLite 3.50.4 vdbe.c](https://www.sqlite.org/src/raw/src/vdbe.c?ci=version-3.50.4):
  implicit statement-transaction opening; absence of explicit SAVEPOINT alone
  does not remove statement journals.

These upstream source anchors support the conditional argument; they are not
evidence that the currently installed binaries use the same source/build.
