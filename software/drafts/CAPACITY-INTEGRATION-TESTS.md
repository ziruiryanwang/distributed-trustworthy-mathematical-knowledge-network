# Four bounded version-3 integration tests

Source-only handoff, 2026-09-21. The author inspected the current integrated
product sources and authored [`test_capacity_integration.py`](test_capacity_integration.py).
No import, compilation, Python/Lean execution or SQLite query was performed
by the author. Root owns staging, independent source/launch review and execution.
There is no claimed passing result or automatic retry authorization.

## Staging and boundary

Stage this standalone suite at `INSTALL/tests/test_capacity_integration.py`,
with the integrated `manage.py`, `build.py` and `py/{capacity,storage,domains,
node,run_stage}.py`. No earlier test suite or driver is imported. The test
checks Windows, `-B -E -s -S` and SQLite 3.50.4 before product imports, then
checks each selected module's origin. Root must separately pin exact sources
and runtime: an origin check does not authenticate bytes.

`DTMKN_TEST_ROOT` must name an existing absolute, non-reparse directory outside
the installation. Neither may contain the other. The test creates one fresh
`capacity-integration` child, refuses reuse and retains all its evidence.
No native checker, peer module loader, process creation or Windows Job creation
is permitted: the relevant entrypoints are fenced to fail. These are test
tripwires, not an OS sandbox against arbitrary modified imports.

## Exactly four methods

1. **Configure rejects invalid capacity before side effects.** Call the real
   `manage.configure` with each of its four fresh-capacity fields malformed:
   booleans, negative, float, string, null, huge integer and unsupported boundary
   values. Expect the field's actual refusal code. Pinning, build inspection,
   supply observation, directory creation and file opening are patched to fail
   if reached. Check no state/scratch directory or file-byte change. This tests
   the programmatic entrypoint's validation, not CLI argument parsing or a
   successful configuration/build.

2. **Configuration and stage-plan readers stay distinct.** Call actual Domains
   readers: configuration schema 3 accepts and 2 refuses; stage-plan schema 2
   accepts and 3 refuses; boolean/float spellings refuse. Additionally execute
   bounded real `run_stage.execute` prefixes using tiny retained plans and a
   sentinel at `require_work`, after domain validation but before any stage
   write. Call the real `build.build` prefix with an explicitly test-only empty
   installation domain and stop at its asset-inspection boundary. Wrap the
   stage reader and fence the config reader to verify both actual call sites.
   These are behavioral prefix checks, not regex/source-text assertions; they
   do **not** qualify a complete stage plan, support build or native runner.

3. **Actual SQLite-full failure reaches dispatcher terminal-only handling.**
   Use a real version-3 store and real `Dispatcher.execute`. Patch preparation
   to capture the post-reservation state, and patch completion to attempt at
   most twelve near-2-MiB records in one actual ordinary transaction. Require
   SQLite itself to raise `SQLITE_FULL`; no exception or page count is mocked.
   A wrapper around the actual `terminal_refusal` checks rollback is confirmed,
   no transaction remains and all ten tables equal the post-reservation
   snapshot. Require the actual dispatcher result `REFUSED/METADATA_SPACE`,
   one terminal-only completion, unchanged nonrequest/nonmeta tables, one
   retained 8-MiB request charge and no stage/checker work. Exact replay must
   return the same bytes and preserve tables with reservation and supply
   observation fenced off. If twelve bounded writes do not reach SQLite-full,
   fail the test; do not add writes or lower product caps to force success.

4. **Node entrypoint preserves uncertain reservation/completion outcomes.**
   On four fresh real stores, inject errors immediately before or after actual
   COMMIT for reservation, then completion. Call actual `node.main` with
   patched argv, configuration loading and in-memory stdout; use real request
   files, actual owner locking/store transactions and actual event-file writes.
   Preparation and completion workloads are explicitly synthetic, and the
   completion response is a refusal, never fabricated acceptance. Require
   `BLOCKED/TRANSACTION_OUTCOME_UNKNOWN` and no secondary `terminal_refusal`
   attempt. Reopen to check actual absent/pending/terminal state and charges.
   An after-COMMIT normal completion may already have cleared its own active
   key; that committed operation is distinct from a forbidden error-path clear.

The current reply contract has a documented inconsistency: reservation
uncertainty through `node.main` includes `state_outcome:"UNKNOWN"`; completion
uncertainty is explicit through the same unknown-outcome code but omits that
field. The test asserts the chosen current contract, not an invented uniform
field. Uniform presentation is a follow-up, not a change authorized here.

## Synthetic state, resource limits and evidence

The store fixtures are real but uninitialized. Patched preparation deliberately
bypasses mathematical prerequisites; no initialized flag, context, artifact,
proof, supervisor receipt or accepted reply is fabricated. Storage's physical
supply is mocked and labelled. The real-full test exercises genuine SQLite
allocation/rollback/classification, not an authentic mathematical workload.
COMMIT injections are synchronous boundary errors, not power-loss, process-kill,
fsync-failure, missing-stdout or general crash-recovery qualification.

The deliberate large workload is at most twelve records below 2 MiB each:
less than 24 MiB of attempted encoded record payload, with a separate hard
assertion at 30 MiB. There is no fill-until-success loop and no repetition of
the older tier stress suite. The other methods use only small fixtures.
Retained endpoint ceilings are 32 MiB per method and 64 MiB for this suite.
Root must separately select its finite wall/CPU/memory/process launch envelope;
these assertions are not OS disk quotas or transient-journal bounds.

Logical snapshots cover all ten fixed tables, at most 128 rows each, with BLOB
length/digest representations. File observation has a 1,024-entry/256-file/
64-MiB-per-traversal bound. All stores are closed, and each method attempts a
bounded `observations.json` before retained-size assertions; report bytes count
toward the limits. Databases, request/event files and surviving sidecars remain.
Observation/close errors fail the test. A report is not evidence that its test
passed; root must bind the actual unittest outcome and supervisor record.

Passing this suite would support only the four listed wiring contracts. It
does not qualify native renewal, final public CLI/supervisor behavior, full
source pin authentication, mathematical correctness, sustained capacity or
the project's usable-v1 goal.
