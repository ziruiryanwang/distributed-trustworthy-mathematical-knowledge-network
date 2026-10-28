# Independent saved-outcome audit: incremental-host controls

2026-10-28, growth_design_audit. Canonical guard passed. Saved source/JSON/log
inspection only; no control rerun, product import, SQLite/database open, network
or Git operation. Actual file assembly has its separate OUTCOME.md.

**PASS within the selected nine control groups.** The reviewed exact harness ran
once, reports all nine groups passed and completed cleanly. This qualifies the
bounded implementation paths tested, not process-crash/power-loss durability,
mathematical acceptance, a public deployment or the full v5 goal.

Evidence root: `experiments/v5-local-checks/incremental-host-controls01`.

| Binding | SHA256 |
| --- | --- |
| selection.json | `b1d0765c0f1700ad520b3929cae3e6810bad93b6dc2cd7039d02edb962963927` |
| RESULT.json, outer result | `fee918962c0a5f5986ac478ae757ffbec6d0ff4f01643883a59238f0242ac4a5` |
| checks/RESULT.json | `f6911595d587450a0057ee930ed9b6569eb0445b553e95466f505f1f4e01a9bc` |
| reviewed/executed control source | `bb1c34858e5f949867f229a8acb28608647403951acbcacd83c10b9b2e481d2b` |
| selected package PROFILE | `e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13` |

The outer result binds the actual selection hash. Both snapshotted
source/controller files match the selected pins. Saved stdout and
checks/RESULT.json parse to the same full result. The result binds the expected
fixture manifest and reviewed control source. Passing source assertions include
final fixture/package/helper/source pin checks and explicit closed-connection
checks for all 92 tracked SQLite connections. This audit did not independently
reopen those databases; their state assertions are evidence from the reviewed
successful harness. Plain descriptor inspection additionally confirms seven
fresh incremental hosts with the selected profile and partial policy, one
preserved static V1 seal, and no HOST.json for either failed initialization.

## Actual covered outcomes

- Exceptions after real evidence and preview commits left zero indexed targets;
  the index-commit exception left one. Each failure's corresponding progress
  list was still empty, so the unknown-commit branch was exercised. Exact
  retained support, reopening, service capture and a separately invoked
  idempotent completion all passed.
- One 64-target append and a following one-target append yielded 65 indexed
  targets with the stable descriptor. The prior snapshot
  `86e05c2f1753d299666adab0dda298f7d011cf8b1a290ccabde0f11cc90a9f9e`
  remained retained. The new snapshot was
  `2523f0004c1cfed935010dd1bce051fd09b177d1feb741335a890ed73b6644fb`.
  Exact support for all 65, duplicate no-growth and the per-call 65-target
  refusal passed.
- Pin/profile/namespace/policy/limit/target/manifest and lock refusals preserved
  empty stores. Index-capacity refusal preserved old indexed support plus
  authorized unindexed custody. Deliberate scratch digest corruption refused
  without overwriting the row. The corrupt root remains a negative-control
  artifact, not a usable host.
- Both initialization failures left unusable roots without descriptors; append
  and reinitialization refused. Static V1 preparation/service remained supported
  and rejected incremental append.

The service capture used a real reopened index and held-lock assertions but no
socket. Postcommit exceptions unwound Python normally; there was no process kill,
hot-journal recovery, power interruption or physical failure simulation. These
limitations match CONTROL-PLAN and CONTROL-REVIEW rather than being inferred
after execution.

## Closure and resource accounting

The saved outer status is COMMAND_EXITED_ZERO_AND_CLOSED with exit code 0,
direct child reaped, Job closed, final active processes 0, no cleanup errors,
no termination request and zero terminated processes. Logs contain 2,158 stdout
bytes and zero stderr bytes. Peak Job private commit was 37,130,240 bytes.

Measured Job CPU was 8.171875 seconds, plus 0.203125 wrapper CPU, for 8.375 known
CPU seconds. Do not add the nested harness timer (8.0625) again. Overall wall
time was 15.801809600001434 seconds; supervised time through cleanup was
15.765177399996901. The original outer envelope was 180 wall seconds,
110 CPU seconds, 768 MiB and one simultaneous Job process. All work closed
within that selection; no allowance was renewed and no failed run was retried.

Together with file assembly, cumulative known CPU is 10.0625 seconds across
these two distinct operations. Public launcher/service behavior remains a
separate prospective integration gate.
