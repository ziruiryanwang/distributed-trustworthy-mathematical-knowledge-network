# Capacity version 3: bounded native-free contract suite

Source-only handoff, 2026-09-21. This note accompanies
[`test_capacity_v3.py`](test_capacity_v3.py). The author has read/reviewed the
source, but has not imported, compiled or executed it, queried its databases,
or observed a passing result. Root owns staging, source/launch clearance and
execution. A later outcome record must distinguish source review from actual
qualification.

## Scope and prerequisites

The suite calls the real staged `capacity`, `storage` and `admin_worker`
implementations. Stage the test as `INSTALL/tests/test_capacity_v3.py` and
the reviewed version-3 modules as `INSTALL/py/*.py`. The test checks module
origins for those three modules plus `domains` and `node`. It requires
Windows, Python flags `-B -E -s -S`, and SQLite 3.50.4 before importing product
modules. The staged domain reader must accept **configuration schema 3**;
this is not a request to change unrelated mathematical or stage-plan schemas.
Source/module hashes and the Python runtime identity remain root's launch
record obligations; checking `__file__` is not a cryptographic source pin.

`DTMKN_TEST_ROOT` must name an existing absolute directory outside the
installation, with neither directory containing the other. The suite creates
one new `capacity-v3` child and refuses reuse. It checks existing path ancestors
for symlinks/reparse points. Root supplies a fresh, trusted, otherwise idle
fixture domain. No test deletes or repairs retained evidence.

This is a sequential unit-contract suite, not a multi-writer concurrency or
dispatcher qualification. Most calls use `ControlStore` directly against a
fresh real SQLite database under the single test process's exclusive fixture
ownership. The suite does not hold the production owner lock around every
direct store call. The administrative calls do use the actual administrative
locking/opening path, and a separate method exercises real lock contention.

## What is real and what is synthetic

Schema creation, SQL transactions, grant/request rows, page counts, database
files, stored response bytes, readonly opens and administrative `run` calls
are real. Synthetic fixtures may set `initialized=1` and create an empty P1
snapshot to reach the administrative prerequisite. Synthetic request envelopes
and actual `stage` reservations exercise accounting without running native
work. No fixture creates a context, proof, accepted mathematical response or
native acceptance evidence.

`storage.physical_supply` and `admin_worker.physical_supply` return explicitly
labelled mock observations. The capacity-helper method instead calls the real
`capacity.physical_supply` logic with mocked Win32 functions and real temporary
directory arguments. Thus none of this suite's supply observations reports
the host's actual volume/free space. The separately allocated real
`physical_supply(..., enforce=False)` probe belongs to root's own reviewed
execution, not this suite.

Calling the native checker path or `subprocess.Popen` during a test raises an
assertion. These fences are regression tripwires, not an OS sandbox or a proof
that arbitrary modified imports cannot execute code. Root must stage/review
the actual selected sources and apply the launch envelope independently.

## Twelve methods and their discriminators

| Method topic | Concrete discriminator |
| --- | --- |
| Initial/grant parsers | Exact integer/type rejection, unsupported fields/caps, malformed and duplicate JSON, invalid identifiers/configuration, empty increases, and a valid cap-only envelope. No supply observation is invoked. |
| Schema creation/rejection | Fresh user version 3 and exactly ten expected tables; existing synthetic versions 0, 2 and 4 refuse before any database-byte change. |
| Small quotas and replies | Actual request/stage charging reaches `(2,1,144 MiB)`; another request refuses and both exact old ordinary refusals remain replayable without table changes. |
| Two renewal cycles | Two actual grant transactions change only `authorization` and `owner_grants`; continued synthetic reservations reach `(4,2,288 MiB)` without refunds or mathematical acceptance. |
| Exact grant replay/conflict | With another request pending and credits exhausted, exact bytes replay before any supply check; the same ID with changed whitespace conflicts. All tables remain unchanged. |
| Grant count and refused IDs | An unrecorded pending-state refusal does not occupy its ID; that same envelope later succeeds. Exactly 64 successful grants fit, the next refuses, and the first remains replayable. |
| Metadata headroom/expansion | Nine real near-2-MiB records exceed the 4,096-page admission threshold. Reservation refuses without table changes; a cap-only 32-to-64-MiB expansion restores admission while preserving consumed counters. |
| Readonly administrative status | Actual `admin_worker.run` reports uninitialized and pending/exhausted stores; hashes and lengths of all selected state files are unchanged after each call. |
| Absent state and BUSY | Status creates no missing state/database. With a real existing lock held, a second handle must produce `BUSY`; this is not a mocked exception. |
| Restricted terminal completion | Acceptance-bearing replies, overlarge metadata refusals, wrong active keys and completion inside an ongoing transaction refuse. After actual precommit rollback, only the pending response/phase and active slot change; charges remain. |
| Uncertain commits | Inject errors immediately before and immediately after the real COMMIT call, for renewal and ordinary completion. Both report unknown outcome and block further terminalization on that connection. Reopening distinguishes committed from uncommitted state; exact renewal/ordinary replay resolves the committed cases. |
| Physical-supply helper | With Win32 responses mocked, cover same/different volumes, exact/insufficient free-space thresholds, enforce-false reporting, filesystem/drive restrictions, and validation before OS query. |

The two-handle Windows lock check is a falsifiable platform assumption. If it
fails, retain the failure and review the locking model; do not silently replace
it with a mock or launch an unallocated second process.

COMMIT injections are synchronous Python errors around actual SQLite calls,
not power loss, process termination, journal corruption, failing fsync, or
lost stdout after worker exit. They test conservative store/event handling
of ambiguous call results. The suite calls administrative `run`, not its CLI
`main` or the launcher, so administrative stdout/event persistence and Job
quiescence remain separate obligations.

## Resource and evidence envelope

There are exactly twelve unittest methods. Eleven have an 8-MiB retained
fixture ceiling; the metadata-pressure method has a 24-MiB ceiling. The
aggregate retained suite ceiling is 128 MiB. These are endpoint assertions,
not OS disk quotas, transient-journal caps or process memory limits. Root's
supervisor must enforce its separately reviewed time/memory/process envelope
and preserve failure evidence.

The metadata-pressure method makes nine deliberately bounded near-2-MiB
record insertions, about 18 MiB total. It does not repeat the older ~70-MiB
SQLite tier stress workload. No method materializes authorized native-stage
byte grants as files. The 64-grant method reopens the store between successive
small grants so each real connection keeps its own SQL-VM-step budget.

Logical snapshots read the ten fixed tables with a 128-row-per-table limit;
BLOBs are represented by byte length and SHA-256 rather than retained again.
Filesystem observation allows at most 1,024 enumerated entries and 256 files,
with at most 128 MiB hashed per traversal. Every test closes tracked stores
and writes a bounded `observations.json` containing fixture hashes, explicit
synthetic/nonacceptance labels, mocked supply calls and any close/observation
errors. Reports are attempted before retained-size assertions, and report
bytes count toward the fixture and aggregate ceilings. A report may therefore
exist for a failed test; the separate unittest exit/result is authoritative.
If the filesystem cannot accept the report, the suite must fail, not invent
missing evidence.

All fixture databases remain, including failed/old-version/ambiguous-commit
fixtures. File-byte equality claims concern content and length, not timestamps
or a filesystem crash-consistency theorem. Native throughput, maximum lifetime
authorization, broad corruption recovery, physical disk reservation, live
multi-process races and mathematical soundness are not certified here.

## Handoff and acceptance boundary

Root should pin this source and its note, stage the corresponding reviewed
version-3 modules, obtain an independent source/launch review, and execute
only within the granted envelope. No automatic retry or fixture reuse is
authorized by this note. Record actual method results, process exit, retained
bytes, hashes and any failed assumptions. Passing this suite supports the
listed local control-store contracts only; it neither replaces the separately
reviewed native renewal discriminator nor completes the project's usable-v1
goal.
