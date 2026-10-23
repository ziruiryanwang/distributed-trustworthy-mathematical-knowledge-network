# Focused installed extraction-supervisor controls

2026-10-23, `project_hook_design`. Canonical guard PASS. Source-only; no imports,
compilation, tests, native processes, package edits or Git operations performed.
Root owns the later exact selection and launch; independent review is pending.

## Purpose and bounded scope

The selected reusable library extractor already has mechanism evidence. The new
boundary is its public interactive supervisor, especially original-allocation
cleanup and created-but-unassigned CPU accounting. Test that boundary with tiny
Python children, not another Lean build/extraction or theorem workload.

Source: `software/v5/ordinary_library_support/protocol_controls.py`, SHA256
`de8b02fb654fc35f284474d325ce9934d1023df8369debedc8474635ea733ff0`.
It loads the actual selected package once using the pinned owner/bootstrap/profile
path, exactly as the independent preparation controls, with profile
`1801fee2c3e9e39cef35182478acc693c923fef32ebb47ae2d7099d9a7776d3e` at
`experiments/v5-local-checks/ordinary-library-support-assembly-01/package`.
No helper is mocked; the actual installed exchange and pinned Windows Job run.
One explicit fault wrapper raises before assignment while delegating all Job
accounting, termination and closing to the real backend. Its child remains
suspended and must be directly killed/reaped, never resumed.

## Five scenarios, no retries

| Scenario | Required observation |
|---|---|
| Clean success | Two distinct synthetic names receive exact FOUND/ABSENT replies; DONE, both EOFs, zero exit, exact retained transcripts, final CPU and clean Job/thread/pipe closure. |
| Wrong sequence | First request has sequence 1; exact `EXCHANGE_LOOKUP_BINDING`, retained failure and real child cleanup. |
| Trailing frame | Two good round trips, DONE, then another frame; exact `EXCHANGE_TRAILING_STDOUT_FRAME`, retained failure and cleanup. |
| Idle cancellation | First full round trip and second lookup establish active IPC; callback schedules cancellation 150 ms later. Exact `CONTROL_IDLE_CANCELLED`; cancellation deadline to completed cleanup is less than one second. |
| Preassignment failure, last | Real fresh Job remains total=0/active=0, but a real suspended child exists. Exact injected failure, direct reap, CPU null/accounting incomplete, poisoned worker CPU and conservative reservation—not measured zero. |

All children are the same selected script's early `--protocol-child` entrypoint,
with pinned Python and `-I -S -B`. Only the selected argv/cwd/environment/pipe
settings can launch. Names and one-byte DONE metadata are inert synthetic data;
there is no supplement, Lean process, mathematical acceptance or growth claim.
SQLite connections, owner opening/admission, peer exchange and networking are
guarded. Failure stops later scenarios; no automatic replay or allowance renewal.

Cancellation timing begins after observed IPC, not OS launch/import startup, so
normal startup variance cannot create a misleading latency failure. The child
waits in 50 ms intervals; normal success waits for the supervisor's stdin EOF.
The bad-sequence/trailing children stay alive for the supervisor to terminate,
avoiding broken-pipe races that could conceal the intended protocol error.
The remaining subsecond scheduling assertion is a real local observation, not a
universal OS real-time guarantee. Exhaustion or unexpectedly slow cleanup fails.

## Accounting and resource envelope

Proposed outer plan: 90 wall seconds, 40 total Job CPU seconds, 512 MiB, four
processes. The test controller has one 70-wall/30-CPU allowance, including load,
controller computation, completed child CPU and conservative unknown reservation.
Each operation receives a fresh 30-wall-second budget within that same deadline,
remaining CPU minus one second, 128 MiB, two processes and 4,096-byte log caps.
The actual exchange's existing cleanup reserve remains unchanged; no new deadline.

Each claimed operation is charged exactly once in `finally`. Finite reported Job
CPU enters `known_measured_child_cpu_seconds`; unknown accounting separately
reserves the full operation CPU allocation, even on an unexpected failure. The
known-zero empty Job is never substituted for the unassigned child's unknown
CPU. The final unknown case may consume almost all remaining allocation and thus
runs last. The outer Job can independently account its actual process tree; its
measurements must not be confused with this intentionally incomplete inner Job.

Every case checks the report's explicit 4,096-byte stdin/stdout/stderr caps, 1 MiB
frame and 32 MiB combined ceilings; retained stream files cannot exceed their
actual caps. These controls inspect cap enforcement configuration and actual
small transcripts; they do not claim to have executed every overflow boundary.
Reports also require direct-child exit/reap, zero active Job members, closed Job
handle and pipes, joined threads, no extra live threads and no cleanup errors.
`PROTOCOL-CONTROLS.json` retains all scenario charges; each attempted exchange
retains its own `EXTRACTION-SUPERVISION.json`. Source success is not run success.
