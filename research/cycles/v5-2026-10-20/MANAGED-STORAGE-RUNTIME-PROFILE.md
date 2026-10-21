# Managed storage: concrete runtime profile and pre-write seam

2026-10-21, core_release. Source/theory phase under
MANAGED-STORAGE-IMPLEMENTATION-SELECTION. **Feasible with small source guards;
the current stores cannot yet adopt the envelope.** No product edit is selected
by this note. The actual public-contribution fault takes implementation priority.

## Decisive result

The installed Python uses SQLite3.50.4, matching the earlier SPACE-BOUND source
argument. Installed Node24.16.0 uses SQLite3.53.0. A targeted official-source
check finds the same relevant pager/temp-file mechanisms in that version.
Use conservative `P=4096`, `S=65536`, and **A=1 for apparent managed data-stream
bytes**, not an invented filesystem allocation quantum or physical-disk quota.

Both actual builds report `TEMP_STORE=1` and `DEFAULT_AUTOVACUUM`. Therefore:

- `temp_store=MEMORY` is supported under the reviewed build premise.
- **Explicitly set/read `auto_vacuum=NONE` before the first schema write.**
  The earlier bound excludes page relocation; the current default cannot be
  relied on. A check after initialization is too late to establish this profile.
- Do not diagnose this by creating test files. Upstream btree initialization
  explicitly exempts `:memory:` from default auto-vacuum, so an in-memory
  auto-vacuum observation would not identify the file-backed default anyway.

This is an actionable source correction, not a need for more RAM, a disk-filling
experiment, a quota service or rebuilding Python/Node themselves.

## Exact diagnostic evidence

Two original native `-c`/`-e` invocations failed at parsing because Windows
PowerShell stripped embedded quotes. Neither established a SQLite connection.
Root explicitly authorized one corrected stdin-fed invocation per runtime;
both then succeeded, using only `:memory:` and read-only version/source/compile
queries. Python elapsed0.2143seconds; Node0.1336seconds. No product modules,
filesystem databases, services, child helpers or persistent settings were used.

Current127 installation:
`product-local/v5-distribution-managed-contribution-01/Mathematical Commons v5`.

| Runtime | Actual SQLite version | Actual sqlite_source_id |
|---|---|---|
| Installed isolated Python |3.50.4|`2025-07-30 19:33:53 4d8adfb30e03f9cf27f800a2c1ba3c48fb4ca1b08b0f5ed59a4d5ecbf45e20a3`|
| Installed Node24.16.0 |3.53.0|`2026-04-09 11:41:38 4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b`|

Both report `DEFAULT_PAGE_SIZE=4096`, `DEFAULT_SECTOR_SIZE=4096`,
`DEFAULT_AUTOVACUUM`, `TEMP_STORE=1`, `THREADSAFE=1`, `MUTEX_W32`,
`DEFAULT_WORKER_THREADS=0` and `MAX_PAGE_SIZE=65536`. Neither reported
`ENABLE_ATOMIC_WRITE` or `ENABLE_BATCH_ATOMIC_WRITE`. Python reports
`COMPILER=msvc-1944`; Node reports `COMPILER=clang-19.1.5`. These are identifying
observations, not a proof of compiler correctness or binary/source equivalence.

Relevant exact release identities:

| Installed file | SHA-256 |
|---|---|
| Python executable |`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`|
| `python314.dll` |`fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0`|
| `DLLs/_sqlite3.pyd` |`b0c4edff6d60f300373ec929ab915f95ee601bf167e04d28e4e9e28a8e536fe0`|
| `DLLs/sqlite3.dll` |`3557565665e608cd24726730e52690a131efcb0e2d5090337b2e05fb89d49c76`|
| Node executable |`b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3`|

These rows come from the adopted127 release manifest; they identify its selected
runtime closure. The DLL's Windows version resource says Python3.14.6. No claim
of a reproducible upstream-to-binary build is made or required implicitly.

## Targeted source correspondence

The existing 3.50.4 argument in SPACE-BOUND remains the Python source basis.
For Node, read official SQLite source at exact source-id4525003a, not a moving
latest branch. Relevant observed mechanisms:

- `pager.c`: `MAX_SECTOR_SIZE=0x10000`; `sqlite3SectorSize` clamps the VFS value
  to this maximum. Thus S=65536 does not depend on the PC's cluster/sector size.
- `pager_write` journals an old page only when its pInJournal bit is absent;
  `pagerAddPageToRollbackJournal` appends P+8bytes and sets that bit. The prior
  no-relocation/error-abort premises are still substantive.
- `pagerStress` invokes `syncJournal(...,1)` only for NEED_SYNC or
  WRITER_CACHEMOD. The same existing header-count argument applies subject to
  its explicit no-relocation and no-unbounded-retry premises; this note does
  not claim a new independently machine-proved pager theorem.
- `btree.c` passes `sqlite3TempInMemory` into `sqlite3PagerBegin`.
  `openSubJournal` uses `nSpill=-1` for in-memory subjournals.
  `memjournal.c` spills to disk only when its spill threshold is positive.
- `main.c`: with compile-time TEMP_STORE=1, effective memory mode is exactly
  `db->temp_store==2`. `vdbesort.c` disables external-PMA setup in that mode.
- `os_win.c`: `szChunk` controls optional file-size rounding. The supported
  ordinary default VFS profile must have no application file-control chunk
  override; otherwise NP is not automatically the main apparent-file bound.
- Node24.16.0 `src/node_sqlite.cc` opens DatabaseSync with
  `sqlite3_open_v2(..., nullptr)` for the VFS argument. Its default URI flag
  does not select an alternative VFS for our ordinary absolute paths. Trust
  still requires no previously registered replacement VFS or extension.

Trusted-runtime premises must be **explicitly adopted**: the exact pinned
binaries implement the stated source mechanisms, normal default Windows VFS
semantics, and the closed local SQL/serializer code. A matching source-id,
compile-option string or passing PRAGMA readback does not prove those premises.
The project may use this ordinary engineering TCB; do not imply it is a formal
end-to-end verified build. Preserve `physical_envelope_adopted=false` until root
has reconciled these premises with the actual gate and independently reviewed it.

## Smallest enforceable guard seam

For the six Python stores and manager registry: in a fresh selected successor,
configure the connection **before BEGIN/schema DDL**, then require page4096,
auto_vacuum0, DELETE, FULL, effective MEMORY temp mode, finite exact page cap,
and supported runtime/source/profile. Retain ordinary cache spilling; do not
set the durable main journal to MEMORY. Reject rather than migrate any existing
store whose persisted auto-vacuum/page/profile is incompatible.

For Node, `body_location/portable/location/intent.mjs` currently calls
`super.open()` first. The base `QuotaDatastore.open` has already created the
schema and committed before returning; connection-specific MEMORY mode also
cannot be established permanently by a separate preparatory connection.
Therefore a post-super guard alone is **not sufficient** for this profile.

Use either a fresh managed-only `open()` override preserving the base schema,
counter census and transaction logic but placing the small guard before its
DDL, or a separately selected exact base-store successor. The override avoids
rebuilding the bundled runtime and avoids a new startup-exception proof. Do not
monkey-patch DatabaseSync globally, change old used stores or run VACUUM to adopt
them. Root chooses this seam after reconciling the guest's writer contract.

On reopen, an existing supported-store binding must establish that any hot
journal was produced under the adopted profile. SQLite recovery can occur before
an after-open guard, so that guard cannot retroactively contain an unknown old
journal. This is a new-profile compatibility boundary, not automatic migration.
The manager's exact marker/config/profile binding must move before its writable
registry open; the generation composer already checks its generation marker
before opening services. Reject oversized main/journal metadata before reopen
under the new profile, without scanning mathematical payloads.

Remaining non-SQLite details are in MANAGED-STORAGE-GATE-CONTRACT: pre-write
identity/adoption serialization caps, exact lock lengths, bounded marker and
config/source-map outputs, and every prepaid run. Keep external public-operation
reports separately bounded; they are not lifetime-free because they live outside
the managed generation. Those source obligations do not justify a further
runtime campaign before the actual contribution blocker is repaired.

## Official read-only sources

- [SQLite pager, exact Node source-id](https://www.sqlite.org/src/raw/src/pager.c?ci=4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b)
- [SQLite btree](https://www.sqlite.org/src/raw/src/btree.c?ci=4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b)
- [SQLite main/temp-store selection](https://www.sqlite.org/src/raw/src/main.c?ci=4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b)
- [SQLite memory journal](https://www.sqlite.org/src/raw/src/memjournal.c?ci=4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b)
- [SQLite sorter](https://www.sqlite.org/src/raw/src/vdbesort.c?ci=4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b)
- [SQLite Windows VFS](https://www.sqlite.org/src/raw/src/os_win.c?ci=4525003a53a7fc63ca75c59b22c79608659ca12f0131f52c18637f829977f20b)
- [Node24.16.0 SQLite binding](https://raw.githubusercontent.com/nodejs/node/v24.16.0/src/node_sqlite.cc)

Fetched source was read as inert text only; none was executed or installed.
