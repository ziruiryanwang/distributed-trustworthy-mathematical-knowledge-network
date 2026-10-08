# Target-profile01: bounded diagnostic interpretation

2026-09-21. Read-only source/data review; no imports, execution or optimization.
The target reply is `REFUSED / INPROCESS_TIME_LIMIT`, not mathematical invalidity.
The public process was reaped, active-zero and Job-closed. No target canonical
value exists to audit: event metrics report six canonical package reads,
1,684,634 bytes, zero package-cache hits, **zero stage allocations and children**.

## What was actually measured

The 16,849-byte `dispatcher-profile.json` beneath public call
`call-a0e7408509984c0a8ac13dd44abb83e3` has SHA-256
`C3790F13CD0E228C361CB8D14EF86D0AC5CBCC75DBAFD600F703D1BCBDC4D301`.
It contains 48 selected rows from 643 entries, recording **220.21875 process-CPU
seconds** around dispatcher construction/execute. Public-Job CPU is 220.390625
seconds; public wall is 229.651264 seconds. These overlapping measurements are
not summed. Startup, final reporting and child CPU are outside the profile;
there were no native children in this request.

| Actual function | Calls | Exclusive CPU s | Cumulative CPU s |
| --- | ---: | ---: | ---: |
| `codec.dumps`, line 66 | 41,162 | 0.109375 | 191.3125 |
| Its recursive `visit`, line 71 | 17,905,545 | 94.140625 | 191.203125 |
| `codec._header`, line 56 | 17,905,545 | 39.265625 | 57.140625 |
| `Store.__init__`, line 133 | 7 | 0 | 96.34375 |
| `make_foundation`, line 360 | 7 | 0 | 67.921875 |
| `source_codec.read_package`, line 956 | 6 | 0.046875 | 174.921875 |
| `Checker.union`, line 243 | 1 | 0 | 217.984375 |

These cumulative rows overlap; constructor, foundation, decoding, commitment,
package and union times are not independent buckets. Subcall graphs were
disabled, so aggregate serialization cost cannot be apportioned exactly among
callers from this sidecar.

Source inspection explains the prefix: `submit` first validates/joins its six
inherited packages. Each reader constructs a foundation, checks objects and
plans closure; union constructs another Store, adds objects and makes a plan.
`loads` re-encodes, `cid` serializes, and Store insertion/getters preserve
commitment checks. Seven `make_plan` calls appear; their 19.96875 cumulative
seconds are also nested, not a separate saving estimate.

The checker tests a **120-second elapsed-time budget**, excluding child waits,
at checkpoints. Its stage-entry checkpoint follows context reconstruction and
precedes allocation, explaining a late cooperative refusal without a target
stage. It is not a 120-CPU-second hard interrupt.

Per-call profiling with a process-time timer can materially distort this
tens-of-millions-of-calls workload. Its overhead is unmeasured and included in
diagnostic cost. This is an instrumented, truncated prefix—not an unprofiled
whole submission. No normal-runtime bottleneck shares, native-check shares,
avoidable-work fraction or predicted speedup follow.

## Prior negative result and next decision

`experiments/lean-package-efficiency/AUDIT.md` retains **FAIL** for constructor
template adoption: first reads regressed 15.26% and 19.66%, breaching the frozen
10% ceiling, despite 21.03% median fifteen-package reader-wall improvement.
Its finite equality/refusal checks passed; candidate memory also increased.
Current constructor activity neither reverses that decision nor qualifies the
old candidate for this six-package context.

Recommend one separately authorized, freshly frozen **unprofiled conformance
allocation**, using the audited unmodified installation read-only, exact target
bytes, fresh matched vocabulary onboarding, and unchanged five-request/four-stage/
552-MiB and time limits. Do not resume this failed allocation, widen limits,
modify mathematics, or adopt an optimization. This distinguishes profiler-induced
infeasibility from the actual unresolved source/export gate. Success still
requires full canonical **value** and candidate/inverse audit; failure retains
its exact boundary. Only afterward consider a separately qualified, unprofiled
optimization comparison preserving cold-first-read safeguards and every check.
