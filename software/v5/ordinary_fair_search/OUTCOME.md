# Fair-search-controls01: saved-output audit

Disposition: **PASS for the selected 16 native-free changed-boundary controls**.
The single saved run completed all selected cases with zero failures, errors or
skips and clean reported process closure. No rerun was performed. Root owns
adoption; this is not an installed-v5, network, mathematical or growth result.

Reviewer: `/root/current_security_obstruction`, author of `fair_exchange.py` and
`fair_search.py`. Root independently reviewed that implementation. This agent
independently reviewed root's tests/bridge and now audits the saved execution
evidence; it does **not** represent this as an independent audit of its own code.
Only this outcome note was written; tested source and evidence remain unchanged.

## Evidence binding

Run directory: `experiments/v5-local-checks/fair-search-controls01/`.
The live selection, retained `selection.json` and outer report agree on SHA-256
`310ccdfbeeebfcdb50baa6225fa602d597bf3a33e65510dedb1cb7d46afc8539`.
All **17 source pins** match both their current source and retained snapshot;
the snapshot contains exactly 17 files. All **three selected Python runtime
pins** match. These are explicit pins, not a hermetic toolchain attestation.

The frozen supervisor manifest matches
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
Its `operator/commons.py`, `receiver/helpers/domains.py` and
`receiver/helpers/run_stage.py` each match manifest lengths/hashes. The selected
runner checks source/runtime pins before execution and retained source/runtime
bindings afterward; the actual report contains no final-binding failure.

| Saved evidence | SHA-256 |
|---|---|
| `RESULT.json` | `8af182f5ba19a73318cfc3e195731554621a1523def53c29ee6d7a62e5af5e00` |
| `suite/RESULT.json` | `93cc699535496e5aef3a0b4f35fdb3fa207e06abe0947ae3972dae6936085a53` |
| `command/stdout.txt` | `6e4e8272391cbc9f51e1811ea20d0786e06e615e92456c9632a49863eb56a040` |
| `command/stderr.txt` | `bdb4087593b6def39369fb3b3b10f198d4bd05f898d4263fa39cfc8b0d7e7717` |
| `command/command.json` | `9e4f4157287c8392f44d85ba1e951040113762a5105625f0855d01959d638070` |

The command uses selected `D:\Python314\python.exe -I -S -B`, the snapshot's
`test_fair_search.py`, the snapshot `software/v5` source root and fresh suite
output. Its cwd is the canonical project root. It is not invoking the current
mutable source by an unpinned relative path.

## Case census

The 16 `test_*` definitions in the retained source match 16 unique stdout `ok`
entries exactly, with no omitted or extra case. `suite/RESULT.json` independently
records `tests=16`, `passed=true`, `failures=0`, `errors=0`, `skipped=0`.

| Control | Saved result |
|---|---|
| Dirty close remains fatal | ok |
| External cancellation remains fatal | ok |
| Insufficient cleanup slice dials nobody | ok |
| Invalid membership never becomes a hit | ok |
| Nonprogress cursor does not suppress another provider | ok |
| Only explicitly allowed metadata refusal continues | ok |
| Owner-grant mutation refuses before dialing | ok |
| Refused connection can continue | ok |
| Request cap preserves partial offers | ok |
| Both first pages precede a second provider page | ok |
| Single use cannot renew a grant | ok |
| Stalled offer preserves later hit and full charge | ok |
| Stalled page preserves scan charge and later hit | ok |
| Unknown local failure remains fatal | ok |
| Unreturned connect reset remains fatal | ok |
| Unreturned connect timeout remains fatal | ok |

## Operational result and warnings

The outer record reports `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0,
direct child reaped, Job closed, no cleanup errors and zero final active
processes. It reports two total Job processes, within the three-process cap;
no process identity or native-work inference is made from that count.
No termination was requested. The selected limits were 60 wall seconds,
45 CPU seconds, 768 MiB, three active processes and 1 MiB per output stream.

Observed runner wall time: **2.3311728998 s**; supervision through cleanup:
**2.2522259997 s**; measured Job user-plus-kernel CPU: **1.390625 s**; separately
reported wrapper CPU: **0.078125 s**. Peak Job private commit was 26,779,648 bytes.
Output lengths (1,942 stdout / 1,529 stderr bytes) match the report. These are
this finite run's costs, not performance or real-network latency claims. The
supervisor explicitly describes wall/total-CPU/log limits as sampled, not hard
disk bounds.

Stderr is not empty: it contains four asyncio debug slow-task diagnostics for
the invalid-membership, nonprogress, JSON-refusal and round-order cases, at
0.136, 0.177, 0.111 and 0.107 seconds respectively. They name finished tasks
with `result=None`, not unhandled exceptions, leaked transports or test failures.
The harness dispatches the real provider/index/proof logic synchronously inside
the in-memory writer's `drain`; its session clock is artificial. These diagnostics
are consistent with that cooperative execution and local scheduling, without
identifying an exact CPU-versus-scheduling split.

In particular, **a 50-ms test attempt does not imply a hard 50-ms bound on local
synchronous work**. Async cancellation needs an event-loop opportunity. The
saved warnings neither invalidate the selected order/accounting assertions nor
justify a stronger wall-time-fairness claim. No warning suppression or new timing
campaign is selected by this audit.

## What the pass establishes

Under the synthetic in-memory transport fixtures, the selected implementation
provides the tested conditional later-provider opportunities while preserving
conservative settlement and fatal uncertain-cleanup boundaries. Real authenticated
metadata/query/session logic was exercised; no real TCP/TLS, native checking,
retained mathematical state or ordinary package/facade loading was exercised.
The peer facade and profile are pinned snapshots but remain source-reviewed,
not executed by this suite. A one-partition nonprogress case does not qualify
later-partition behavior. Discovery remains explicitly incomplete metadata,
not mathematical acceptance, proven relevance or evidence of creative knowledge
growth. Full deployable v5 remains unfinished.
