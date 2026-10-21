# Base-projection controls01: independent saved-outcome audit

2026-10-20, adaptive_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**ASSERTIONS PASSED; CLEAN CONTROL-EVIDENCE QUALIFICATION ON HOLD.**
All eight selected unittest groups reported success and the enclosing Job closed
cleanly. However, saved stderr contains **19 unexpected asyncio self-pipe
TypeErrors** caused by the test socket guard. This is a harness defect, not an
established product defect. The run must not be relabeled as a clean control PASS.
Preserve all original inputs, outputs, used source and costs.

This audit read saved outputs and source/hash identities only. It did not import
or execute Python, restart a test, create a network, rebuild or produce a proof.

## Exact allocation and integrity

Operation: `experiments/v5-local-checks/base-projection-controls-01`.

| Evidence | SHA-256 |
|---|---|
| Original and saved selection | `faf0214a2cc7e0a0e345cf41ca519fcb675c325935dc1136ab92af055aeefe8a` |
| `RESULT.json` | `dcd766d6cfbc85881a470befeeb552b4c84785d194d002e535eac5dd1ead067c` |
| `controls-result.json` | `e9193385682036b7b7da5e8c4ff7bee3db4cc717edae17bbd8ca2a5072c43e7a` |
| `command/stderr.txt` | `15a7d65650a0fefd1e180109153937415d6fe8138aa7aa8d06ee1ccc26600140` |
| Used controls source | `ddbfaa67a375d2289f6fcf0e352386090ac0137df8f2cade49d02127f3860aa7` |

Checked every selected source against both its actual saved snapshot and current
source: **153 source entries, 153 snapshot files, zero mismatches**. All **19**
retained runtime pins also match. The four product sources match independent
implementation review `05085f04`, as does the executed controls source. The
command runs the exact snapshot with isolated Python flags under the canonical
cwd. The 45 CPU-second, 75 wall-second, 384 MiB, two-process and one-MiB log
limits are unchanged. No predecessor suite is selected.

## What ran and what the diagnostics mean

The structured result reports eight tests, zero failures/errors/skips. Saved
stderr names each selected group and reports `ok`, then `Ran 8 tests in 6.257s`
and `OK`. Saved preparation/service records and source assertions cover the real
structural custody/index, exact-base regeneration, namespace refusal, bounded
selection, borrowed ownership, partial/uncertain commit handling, explicit
reconciliation, latest-cut selection, V1/V2 service composition and cleanup
cases recorded in the implementation review.

In particular, the partial group retains actual quota refusal after a committed
prefix, an admission failure before work-counter reset, and an injected exception
after an actual commit; subsequent explicit reconciliations preserve idempotence
and charge new attempts. Normal V1/V2 HTTP compositions and advertised V2 report
their asserted selected views. These assertions are actual completed observations,
not omitted tests. They must nevertheless be separated from clean lifecycle
qualification because the test environment emitted unhandled asynchronous errors.

The 19 errors all take the following route in the retained Python runtime:

```text
asyncio/proactor_events.py: _loop_self_reading
asyncio/windows_events.py: recv
    isinstance(conn, socket.socket)
TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```

The control fixture replaced the module's `socket.socket` class with a Mock after
the event loop was created. Existing loop sockets still undergo later runtime
type checks. Creating the event-loop infrastructure first therefore did not make
that replacement safe. The loop's default exception handler logged the failure;
unittest did not convert it into a test error. There are also three ordinary
slow-task debug messages; those are distinct from the 19 TypeErrors.

The source reviewer accepted the guard's claimed post-infrastructure timing and
missed these later type checks. The saved-outcome review corrects that oversight;
it does not rewrite the earlier review or the raw unittest result.

## Termination and cost

The enclosing result is `COMMAND_EXITED_ZERO_AND_CLOSED`: child exit 0, direct
child reaped, Job closed, active processes 0, no cleanup errors, no termination
request and zero terminated processes. Total processes 2 fits the limit. Peak
Job private commit is 33,873,920 bytes. Observed logs are 53,409 stderr bytes and
0 stdout bytes.

- Inclusive Job CPU: **2.84375 seconds** (user 2.140625 + kernel 0.703125).
- Separate outer-wrapper CPU: **0.578125 seconds**.
- Known total CPU: **3.421875 seconds**.
- Outer wall: **10.650285600218922 seconds**.

Do not add nested wrapper supervision CPU 0.03125 again. Child wall-through-
cleanup 9.246182200033218 seconds and unittest 6.257 seconds are nested, not
additional total elapsed time. The failed clean-evidence gate does not refund
these costs.

## Consequence

Hold adoption as a clean new control qualification. No mathematical authority,
global recall, useful-growth advantage, live external service or final-v5 claim
follows from this allocation. No product change is justified merely by this
harness-induced runtime error.

Root has separately selected source-only preparation of a fresh controls02 guard
repair and fresh selector. Preserve the exact `socket.socket` type and avoid
interfering with existing loop recv/send infrastructure; block the selected
external-service creation paths instead. The fresh harness should record/fail on
unexpected loop exception contexts so an apparently successful unittest summary
cannot hide them again. Independent source review and a new explicit finite
selection must precede any execution. This audit authorizes no retry or build.
