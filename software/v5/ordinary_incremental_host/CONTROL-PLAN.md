# Incremental-host focused controls

2026-10-28. Source only. No imports, syntax execution, SQLite opens, native work
or test run occurred while writing these controls. Root separately selects one
reviewed package, exact pins, fresh output and outer process allowance.

The selected file-only assembly is
`experiments/v5-local-checks/incremental-host-assembly01/distribution/package`,
PROFILE SHA256 `e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`.
The control source requires that exact package/path and profile. Its completed
file assembly does not authorize executing these controls.

`control_tests.py --package <selected package> --profile-sha256 <exact pin>
--python-runtime <selected runtime> --lean-runtime <selected runtime>
--output <fresh canonical experiments/v5-local-checks child>` follows the
existing profile-pinned control loader. The actual new custodian helper, existing
evidence/preview codecs and both SQLite stores execute. No mathematical owner is
constructed and no native process runs. The file has an internal 150-wall/
90-CPU-second ceiling; a later root selection must supply hard outer bounds and
enough report/closure reserve. These ceilings are not measured performance.

All database opens are intercepted and restricted to that fresh output tree.
All created files, databases and deliberately failed/corrupted scratch roots are
retained. No input fixture, package file or old owner/store is modified. Profile,
helper, harness and selected fixture bytes are rechecked before a passing result.
Connections must all have closed. The harness does not reset or silently retry a
failed group. The explicit idempotent completion inside each interruption case
is a named second operation testing an intended contract.

## Exact retained inert fixture

Use `experiments/v5-local-checks/observation-growth-produce01`, manifest SHA256
`d31ee8536962cff8c60c856f107594610d7b82f851c518ec37a838885f3bb4b6`.
Its existing evidence has 47 units, 695,269 bytes and 68 exact output identities.
The harness reads those pinned files, then creates ordinary bounded manifest
projections over exact selected bytes in its own scratch output. It does not
generate 65 new theorems or repeat the producer/checker. One smallest supplied
unit is sufficient for the commit controls; the original distinct identities
support the 64-plus-1 cumulative-index boundary. Projection can omit dependencies
because this is inert hosting, never mathematical acceptance.

## Changed-boundary groups

- Raise a Python exception immediately after the real evidence, preview, or
  index insertion returns from its SQLite COMMIT. The helper must report failure
  and incomplete/unknown progress, close its stores/lock, and preserve the
  committed prefix. Reopen the real stores and verify exact evidence/locators,
  preview presence and index support. A service capture must report the current
  snapshot and must not assert that the failed append completed. An explicit
  second append completes the selected immutable inputs idempotently.
- Append 64 then 1 distinct retained target, with at most 64 targets per call.
  Check all 65 records have their exact custody support, the old snapshot is
  still retained, duplicate append changes neither counters nor snapshot, and
  the stable descriptor bytes remain unchanged. A 65-target *single call* refuses.
- Wrong descriptor pin, selected profile/namespace/partial policy, store limits,
  target/manifest pins and real one-process OS-lock contention refuse. Temporary
  descriptor mutations occur only in one empty scratch host and are restored;
  reopening verifies that the actual stores stayed empty.
- An index with capacity one accepts its first target and refuses its second
  after approved custody support has committed. The first indexed record remains
  usable and the permitted unindexed support remains servable as inert data.
- Deliberately corrupt one scratch evidence-row digest, then repeat the exact
  input. Actual duplicate insertion must refuse without overwriting the row.
  This is a defensive corruption control, not a claim that supported calls can
  manufacture a hash collision. The corrupt root is preserved and not served.
- Inject index-creation failure and failure after empty-store closure but before
  descriptor installation. Preserve the marked root without HOST.json; append
  and reinitialization must refuse. No initialization recovery is implied.
- Preserve the static V1 prepare/serve contract and refuse append against V1.

The service capture replaces `peer_api.serve` with a short asynchronous function
that reopens the **real** index under the helper's held OS lock, captures its
actual snapshot/counters and closes it. It neither listens nor dials. Application
network entry points and native subprocess entry points are failing sentinels;
asyncio's event-loop machinery is left intact. This is not an OS network sandbox.
The later public lifecycle integration remains distinct from these controls.

## Claims deliberately excluded

These are **postcommit exception injections with orderly Python unwinding**.
They establish persistent legal prefixes after actual commits; they do not
simulate kill/termination, a hot journal, physical power loss or incomplete
SQLite recovery. The source invariant relies separately on existing SQLite and
protected-storage premises. Do not label a passing suite as process-crash or
power-failure qualification. One-process two-handle lock contention is not a
hostile-writer isolation or independent-machine availability test.

No mathematical correctness, upstream delta producer cost, query usefulness,
large-corpus speedup or full-v5 completion is established. Existing transport,
theorem, grounding and broad parser campaigns are not repeated.
