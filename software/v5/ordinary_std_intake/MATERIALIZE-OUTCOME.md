# Retained Std materialization: independent failed-outcome audit

2026-10-26. `current_acceptance_challenge`.

**FAILED_CLOSED_AT_COOPERATIVE_CPU_LIMIT.** No complete materialized bundle was
produced. The public initialization/intake successor must remain held: this run
supplies no new usable unit files and no mathematical acceptance. The earlier
successful saved-writer diagnostic and failed public producer retain their
original, different outcomes.

## Terminal evidence

Run: `experiments/v5-local-checks/std-materialize01`.
Selection SHA-256:
`acfc0bb967acf790749ce3f88cb7f4ff8a69301c753bfc03f139a58585eaecb9`.

| Saved file | SHA-256 |
|---|---|
| `RESULT.json` | `a8ea122ba65d1f11793b2c6c1f838c8c9b9f01babcc9e8b63b78bc195031e623` |
| `command/stdout.txt` | `190a67b332cd41aa954b7ea7622cf758e39a5c2b01083944dcd9884208a7578b` |

The complete 163-byte stdout reports `FAIL`, phase `BIND_ONCE`, and
`ValueError:STD_MATERIALIZE_FIXED_90_WALL_70_CPU`. Its final process observation
is **70.015625 CPU / 79.04565110011026 wall seconds**. Since wall was below 90
and CPU exceeded 70, the recorded cooperative CPU condition refused. There is
no saved internal binder completion, timed binding result or per-unit frontier.

The outer supervisor reports `COMMAND_FAILED`, child exit 1, a reaped child,
closed Job, zero final active/terminated processes, no cleanup errors and no
termination request. Stderr is empty. This is an orderly failure, not an outer
forced termination or a missing terminal record.

- Overall wall: **79.9715823000297 seconds**.
- Inclusive Job CPU: **70.515625 seconds** (66.234375 user, 4.28125 kernel).
- Separate outer wrapper CPU: **0.8125 seconds**.
- Total known CPU: **71.328125 seconds**.
- Peak Job private commit: **592,408,576 bytes**.

The inner final CPU and inner supervisor observations are included in the Job
charge, not added again. The original outer 120-wall / 90-CPU / 1,792-MiB /
one-active-process limits remained unchanged. Cumulative two processes is not
two simultaneously active workers.

## Preserved inputs and actual output

Independently rehashed all twelve selected external inputs and all six actual
source snapshots: zero mismatches. The actual materializer snapshot remains
the reviewed `450b6d41...` source, binder `e4b52c2f...`, helper `42670eb6...`.

The new `materialized` directory contains only an empty `units` directory:
**zero unit files and zero files of any kind**. There is no new manifest or
`MATERIALIZATION.json`. The code had not reached the file-writing phase.
These empty directories are retained; no deletion or state repair occurred.

Independently rehashed all 708 old partial unit files and compared every length
and hash to the adopted saved manifest. All still match; 6,389,257 bytes give
the original aggregate
`82df4b3e84e8e53a21ab87f94507f0ba8ecbf8c82fbc6fad1e3b0459d6bae4d0`.
The saved complete manifest retains hash
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.
The old public producer still has no manifest and remains failed.

## Source-only discrepancy analysis

The earlier diagnostic reported a completed binder measurement of 28.125 CPU
seconds, whereas the new whole process exhausted its 70-second cumulative
allowance before returning from the phase labeled `BIND_ONCE`. This is a real
failure of the expected envelope. It is **not** a matched 28-versus-70 binder
benchmark: the new `binding_cost` assignment follows the failed call and was
never saved. The phase label does not locate the failing internal callback or
separate setup CPU from binding CPU.

Read-only source comparison finds:

- Exactly one unchanged `bind_writer` call in each entrypoint, using identical
  pinned writer, inventory, target request, support modules and defaults.
- The helper loaded by the new materializer is not named `__main__`; its old
  diagnostic main never executes. There is no hidden second binder call.
- The new and old budget callbacks each perform the same two clock reads,
  elapsed comparisons and success-path guard. The new exception prefix is
  constructed only when the guard fails. The binder itself controls callback
  placement, and its selected bytes did not change.
- New pre-binding setup reads one 468,097-byte saved manifest, loads the frozen
  helper and creates the two fresh directories. Existing pinned input and
  708-partial reads are retained. No new unit writes, fsyncs, complete portable
  reread or post-binding census can explain this failure: they were unreached.

Therefore no deterministic added inner-loop instrumentation or duplicated
validation path has been identified from the changed source. The evidence does
not identify a root cause, internal progress or hardware explanation. CPU time
is not instruction count, and these separate operations are not a controlled
performance comparison. Do not attribute the discrepancy to RAM, scheduling,
the binder algorithm or a particular input phase without additional evidence.

## Consequence

Retain this failure and its full charge. Do not run public intake against the
empty output, repeat native export, increase limits or silently retry. The
next decision must first explain what new evidence or implementation change
would resolve the actual obstruction at sufficient payoff. An unchanged rerun
would not by itself diagnose the cause. The original cost precedent justified
the attempt; it did not guarantee completion or authorize a renewed allowance.

This review used saved-file reads, hashes and source reasoning only. No binder,
native worker, product command, owner-state operation or network call was run.
