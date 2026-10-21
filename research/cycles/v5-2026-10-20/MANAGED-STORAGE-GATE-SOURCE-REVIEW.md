# Independent source review: unwired managed-storage helper

2026-10-21, support_guest. **PASS_SOURCE_ONLY; no blocking helper defect found.**
Reviewed `software/v5/managed_storage/placement/storage_profile.py`,9331 bytes,
SHA-256 `3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90`.
Core confirmed this source pin. Reused contract246bafdf and runtime-profilee36470bb
under MANAGED-STORAGE-GATE-SOURCE-SELECTION. No imports, database connections,
tests, runtime probes, caller edits, adoption flag or installation changes.

## Integer envelope and coverage

The database expression simplifies exactly to `D(N)=139272*N+327680`, identical
to the settled P4096/S65536/A1 main+journal formula. All arithmetic uses Python
integers after exact F.uint checks: bool, float, string, null and unsupported
ranges refuse. Constants are not caller parameters and there is no occupancy,
deduplication, consumed-run or current-slot credit.

Registry pages64..4096 and all three reservations1..2^50 are checked. Exactly
two slots are required and both full reserved byte amounts, plus registry and
cleanup reservations, must fit the owner's amount. The registry database plus
131073 marker/lock bytes separately fits the registry reservation. Cleanup
progress is expressly not guaranteed; no max_sessions multiplier is invented.

Generation checks the selected slot and `1<=R<=slot.max_runs<=4096`, six exact
configured database-cap paths/ranges, and exactly five explicit nonnull Node
metadata integers. It charges all R Node main+journal envelopes and34816 bytes
of other files per run, plus all six persistent databases and131073 generation
marker/lock bytes. The exact result must fit the full slot reservation. File/
directory/entry counts14+6R,6+3R,20+9R match the contract; no loop over histories
or all runs is needed. Missing/null JS defaults are not silently substituted.

## Supplied-connection guard: what it does and does not establish

The guard neither opens nor closes a database. It accepts only an exact Python
sqlite3.Connection with isolation_level=None, no transaction, standard row/text
factories, one named main file and the selected TEMP_STORE=1 compile-option
observation. Before its profile-setting pragmas it refuses page_count above the
selected cap, a non-DELETE journal mode, or a nonempty database whose page size/
auto-vacuum is incompatible. It does not attempt VACUUM or format migration.

It sets4096/NONE/DELETE/FULL/MEMORY and ordinary cache spilling, sets the finite
page cap, and requires exact-type/value readbacks for the profile settings plus
positive spill readback and no transaction. No DDL/BEGIN/INSERT is issued. These
are connection configuration checks, not evidence that no previous statement
or recovery already wrote data. Caller must close/refuse on any failure.

Crucially, runtime/VFS identity, ordinary paths, same-profile hot-journal lineage,
original main/journal/lock bounds and absence of other writers must be established
before writable open. Even initial PRAGMA reads can recover a hot journal;
this supplied-connection helper cannot retroactively protect unknown old files.
No caller adoption boolean is accepted, and neither runtime nor physical
envelope adoption becomes true. The helper does not configure Node's separate
connection or establish whole-config/cross-role validity.

## Scope and handoff

The source note identifies the required fresh-manager/generation pre-write
insertion points, all seven Python openers and Node's pre-super.open obligation.
These remain future coherent integration, not current gates. Exact file caps,
Node identity serialization, immutable profile binding, caller lineage checks,
external-output accounting and preservation of prior charged failures remain
the existing contract's obligations. A source-only helper pass does not make
the apparent-stream bound a physical-allocation/free-space guarantee.

One nonblocking source-note wording correction was sent to the author: the
registry/generation envelope outputs carry calculation/adoption flags, whereas
database_envelope and node_metadata return plain inert component/value
dictionaries. The phrase "all pure outputs" overstates that output shape; this
does not affect the arithmetic or guard source above. No code change requested.

Root may use this reviewed helper in a separately selected caller/schema/Node
successor. No experiment, new test campaign, caller adoption, existing127 change
or actual storage qualification follows from this review.
