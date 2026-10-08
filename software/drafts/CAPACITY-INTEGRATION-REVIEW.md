# Capacity integration 01: independent source and exact-launch review

2026-09-21. **Source and exact-launch review pass for this one four-test,
native-free allocation.** No deterministic API/assertion mismatch or
unallocated execution path was found. This is clearance for root's reviewed
single allocation, not evidence that the tests passed. No import, execution,
compilation, SQL connection/query, retry, or product-source edit was performed
by this reviewer. Only this review was authored.

## Exact cut and launch

The staged test is byte-identical to its draft. The test and explanatory note
were read completely, along with the new driver and relevant product paths.
The seven pinned `py/` files and Python identity match the cut previously
reviewed in [`CAPACITY-V3-TEST-REVIEW.md`](CAPACITY-V3-TEST-REVIEW.md).
The newly included `manage.py` and `build.py` entrypoints were inspected.

| Path relative to `software/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/test_capacity_integration.py` | 21400 | `7E21C14AC9DA45BBEA93CE228E3D63DA88C13A9D8BCBCC23323125B74643CE10` |
| `drafts/CAPACITY-INTEGRATION-TESTS.md` | 6890 | `5BE03982E0DBB73EE1C6D1874BB0B6EE56ADA8A29056741DEEC2B151A632736F` |
| `tests/run_capacity_integration.py` | 11698 | `B4DBAFFF498277787FC380AB7C33E200DA81B7EC29F3EFE0D8362A49365C3236` |
| `qualification/capacity-integration-launch-01.json` | 3028 | `3CDCB7324C936B579BB695AF41CC0AA00B6B1254396214FBC5609333C258CE65` |
| `manage.py` | 14269 | `DF319F00DBCF29702A04D6151564896AE4D040998AC5859CACE7CBE53580BB77` |
| `build.py` | 7957 | `4E28D64FDFB936F5EDD4FDB4531170B273AC6B48A5DFC0455149199849A82018` |

All twelve ordered launch paths, lengths and SHA-256 values were compared to
the actual files. Their order is Python, this driver, `run_stage`, `supervise`,
`domains`, `capacity`, `storage`, `admin_worker`, `node`, `manage`, `build`,
and this test. The transport additionally pins the exact launch. The Python
is `D:\Python314\python.exe`, 106208 bytes, SHA-256
`03168C01B7B7491423350E82C26FEE71F35B43694D1319D3C668BDA6903A0C38`.
`admin_worker.py` is authenticated by the launch but not exercised by these
four methods; do not infer additional administrative coverage from its pin.

Both `product-local/capacity-integration-01` and
`software/qualification/capacity-integration-01` were absent. Sixty-eight
full ancestor observations across the selected inputs, launch and output
parents found no reparse points. Paths are rooted under
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

The covered command uses that pinned Python with `-B -E -s -S`, the absolute
`software/tests/run_capacity_integration.py` path, and `--launch` naming the
absolute reviewed launch path. Root must preserve source bytes and fresh
roots until dispatch; the driver rechecks them. No changed cut, reused root,
automatic retry, extra method or increased grant is covered.

## Four methods and actual discriminators

### Configure capacity validation

The 36 malformed/boundary cases reach `manage.configure`'s real four initial
capacity validators. Expected refusal codes match current implementation.
Patches fail if pinning, build inspection, supply sampling, file opening or
directory creation is reached. Files are compared outside those patch scopes,
and selected state/scratch remain absent. Existing-directory resolution is
allowed before validation. This is a programmatic invalid-input test, not CLI
argument-parser coverage or successful configuration/build qualification.

### Configuration versus stage-plan schema

Actual domain readers accept configuration schema 3 and stage-plan schema 2,
reject the converse, and reject boolean/float spellings. `run_stage.execute`
reads and authenticates actual tiny plan files, calls the real stage reader,
and stops at a sentinel at `require_work`; schema 3 must fail sooner. Its
configuration reader and writes are fenced.

`build.build` similarly reaches a sentinel at `assets()` only after its real
stage-domain prefix has accepted schema 2. A deliberately empty test-only
installation supplies the required `py/` directory; it fabricates no asset
pin, compiled output, build receipt or mathematical acceptance. These are
behavioral prefix checks, not complete runner/build execution. The sentinels
occur before product writes, Job creation, compilation and native work.

### Actual SQLite FULL through the dispatcher

The real `Dispatcher.execute` reserves one request in a fresh, uninitialized
real store under the owner lock. Only mathematical preparation/completion
workloads are replaced. Preparation captures the post-reservation ten-table
state. Completion attempts at most twelve encoded records below 2 MiB each
inside the actual ordinary transaction, with a separate 30-MiB attempted-
payload assertion. The ordinary 6144-page tier is unchanged. SQLite itself
must raise `SQLITE_FULL`; no page count, exception or capacity limit is faked.

The wrapper on actual `terminal_refusal` requires confirmed rollback, no
active transaction, and table equality with the post-reservation snapshot
before allowing terminal-only persistence. The test requires exactly one such
call, exact `REFUSED/METADATA_SPACE` reply bytes, no checker/stage work, no
uncertainty flag, unchanged nonrequest/nonmeta tables, one retained 8-MiB
charge, and no active key. Replay must return the identical bytes with
preparation, reservation and supply fenced off, preserving table state.

Whether twelve inserts reach FULL is a falsifiable assertion of this cut.
Failure does not authorize more writes or smaller product caps. Passing
would establish this synthetic dispatcher failure path, not acceptance of an
authentic mathematical workload or ordinary behavior on an initialized node.

### Reservation/completion COMMIT uncertainty through node main

Four real stores cover before/after actual COMMIT for reservation and for
ordinary completion. The selected COMMIT is first or second respectively;
schema creation occurs before injection. The actual `node.main` performs
request reading, owner locking, store access and event-file persistence.
Configuration loading, preparation/completion, argv and stdout are explicitly
patched. The synthetic completion is a refusal, never invented acceptance.

All cases require BLOCKED/`TRANSACTION_OUTCOME_UNKNOWN`, zero secondary
`terminal_refusal` calls, zero checker/stage work, and response-hash binding
in the real event. Reopening checks actual durable outcomes:

| Error boundary | Used requests/bytes | Request and active slot |
| --- | --- | --- |
| Before reservation COMMIT | 0 / 0 | No request; unchanged baseline |
| After reservation COMMIT | 1 / 8 MiB | Pending; active key retained |
| Before completion COMMIT | 1 / 8 MiB | Pending; active key retained |
| After completion COMMIT | 1 / 8 MiB | Terminal refusal; active slot cleared by that committed operation |

The existing presentation asymmetry is accurately tested: reservation
uncertainty adds `state_outcome:"UNKNOWN"`; completion uncertainty omits it
but has the same explicit unknown-outcome code. This review neither silently
normalizes that field nor mistakes a committed ordinary clear for a forbidden
secondary error-path clear. Injections are synchronous Python boundary faults,
not crash, power-loss, fsync-failure or missing-output qualification.

## Resource and evidence envelope

The exact launch declares four tests, 60 worker wall seconds, 30 aggregate
Job CPU seconds, 512 MiB private commit, requested public-eight profile, and
65536-byte stdout/stderr/event limits. The driver retains the previously
reviewed suspended-start/Job attachment, bound transport, quiescence, source
snapshot and CPU-before-observation-copy logic. Coordinator work is outside
the worker Job; startup/final-write measurement exclusions remain explicit.
Auxiliary Windows processes must not be confused with mathematical workers.

The suite has 32-MiB per-method and 64-MiB aggregate retained ceilings;
traversals have 1024-entry/256-file/64-MiB bounds. Logical snapshots read ten
tables, at most 128 rows each, compacting BLOBs to length/hash. Tracked stores
are closed and each method attempts a bounded report before endpoint-size
assertions. The independent runner endpoint is 256 MiB/4096 files/8192 entries,
including reserved census/result space. These are endpoint assertions, not
hard transient disk quotas or a promise that the workload finishes in time.

The process/native/peer/Job fences apply after module imports. Trusted reviewed
sources, runtime, and an otherwise idle owner-controlled filesystem remain
assumptions; source-origin checks and mocks are not a hostile-code sandbox.

## Remaining scope

A future pass supports only these four bounded wiring tests. It does not
exercise terminal-only persistence failure returning
`TERMINAL_PERSISTENCE_UNCERTAIN`, full administrative/public CLI supervision,
real physical supply, successful configuration/build, native renewal, broad
crash recovery, mathematical soundness or useful knowledge growth. Actual
results and retained hashes still require an independent outcome audit.
