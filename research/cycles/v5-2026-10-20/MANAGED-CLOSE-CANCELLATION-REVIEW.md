# Selected monitor cancellation can defeat orderly close

2026-10-21. Independent support_screen source-only finding. No runtime,
imports, tests, builds, database access, credential access or product edits.
The canonical workspace guard passed. This checkpoint does not attribute the
actual contribution01 failure to this race.

## Disposition

**REACHABLE SOURCE DEFECT.** An ordinary early close of a successfully started,
otherwise healthy placement service can cancel an in-flight monitor status
exchange. The selected locator correctly treats the interrupted framed exchange
as unsafe, marks its channel failed and kills its still-live child. The selected
service then correctly refuses orderly CLOSED. Thus a service-initiated close can
cause its own strict close failure; neither the failed-channel rule nor the
strict CLOSED predicate is the defect.

The minimal repair direction is cooperative monitor quiescence before the
existing locator stop/close sequence, with a finite join inside the original
deadlines/reservations, followed by bounded failed cleanup on expiry. Startup
abort remains a distinct path. Root has separately selected that source-only
successor in `MANAGED-CLOSE-DRAIN-SELECTION.md`; this review does not authorize
execution or adopt an implementation.

## Exact selected basis

The authoritative 127-entry input is
`experiments/v5-local-checks/distribution-managed-contribution-01-input.json`,
SHA-256 `33bd99d7c3a1db865a6abcb92c96b5df2d0923a793535135e133aebc54aacc0c`.
Logical paths were resolved through that map, not guessed from directory dates.
The following physical source lengths and SHA-256 values were directly checked.
Paths are relative to `E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Logical source | Physical source | Bytes | SHA-256 |
|---|---|---:|---|
| `v5/client/serve_placement.py` | `software/v5/retained_advertisement/client/serve_placement.py` | 22670 | `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa` |
| `v5/placement/advertisement.py` | `software/v5/retained_advertisement/placement/advertisement.py` | 23256 | `5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510` |
| `portable/location/controller.py` | `software/v5/portable_runtime/location/controller.py` | 15884 | `4dc0824d758e72fce591dbd9dddb9e487bcd0506cfaf4a71e894b0166b84e064` |
| `portable/location/controller_services.py` | `software/v5/body_location/portable/location/controller_services.py` | 5854 | `eeb82d5dd6fe34915d07b2927e7ddd44ee2b5b80278dbf4d2889b87222ad1501` |
| `v5/client/serve_generations.py` | `software/v5/bounded_generations/client/serve_generations.py` | 8896 | `404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687` |
| `v5/placement/lifecycle.py` | `software/v5/supervised_generations/placement/lifecycle.py` | 38399 | `bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f` |

The causal trace below needs the first four files. The unchanged composer
provides the public close propagation; the lifecycle hash preserves the exact
selected strict consumer identified in the already sealed actual audit.

## Reachability argument

1. `PlacementService._start` first starts the read provider and locator, completes
   one health check, starts intake, marks `_started`, then creates the monitor
   (service lines 166-187). In a normal successfully started service, `_start_task`
   is done. No outstanding startup is needed for this race.
2. The monitor waits on `_wake`, checks wake/deadline, then directly awaits
   `advertisement.health` (231-242). Health calls the exact location's
   `command("status", {}, until=until)` without shielding or another task boundary
   (advertisement 360-370). Its absolute `until` is at most the original service
   deadline and the operation interval measured when health begins.
3. `ServiceLocationProcess` inherits `LocationProcess.command` unchanged
   (service controller class declaration at 21; overrides concern startup,
   role validation and report). The base command acquires a lock, reserves its
   sequence/bytes, writes the framed command, then awaits stdin drain and the
   bound reply (controller 178-199). These are genuine suspension points.
4. A trusted owner may call `close()` while the monitor is suspended after the
   write. Nothing in `close()` acquires the locator command lock or waits for
   health first. Its tracked close task sets `_closing` and `_wake`, then
   unconditionally cancels every pending monitor/start task (service 253-272).
   `_wake.set()` prevents future iterations but cannot itself finish the
   already-entered status await. Setting it and then cancelling does not give
   the monitor a cooperative completion opportunity.
5. Cancellation propagates through health into the command's inner
   `except BaseException` (controller 200-204). It sets `channel_failed=True`;
   if the child is still live it also sets `forced_termination=True` and calls
   `kill()`. The command releases its lock in `finally`. The monitor's explicit
   `CancelledError` branch re-raises rather than assigning a health failure;
   `_closing=True` prevents its `finally` from creating another close task.
6. The close coroutine can successfully gather that cancelled monitor; this
   does not repair the channel. It skips the stop command when `channel_failed`
   (service 303-307), attempts locator teardown, then requires both
   `not channel_failed` and `not forced_termination` (319-323). Consequently
   `location_closed` cannot be true for this interleaving, even if process reaping
   succeeds. Final service status cannot be CLOSED (350-360).

The witness schedule is therefore: successful startup; monitor status frame
written; reply outstanding; ordinary owner close; monitor cancellation delivered
at drain/read. It requires no pre-existing fault, exhausted command cap,
maintenance expiry or exceptional latency. It proves existence, not frequency.
The command lock serializes commands but cannot serialize an external cancellation.
Public `GenerationServices._close_handle` awaits service close and then asks the
manager to assert strict closure (composer 111-122); it does not bypass this gate.

Not every close fails: cancellation while the monitor is only awaiting `_wake`
does not enter the command handler. Cancellation while acquiring the locator
lock is outside the inner send/read failure block. A completed monitor is not
cancelled. These cases do not refute the reachable after-write case.

## Repair obligations, not an implementation

- Set `_closing` and `_wake` first; do not initiate more health work. Allow the
  existing monitor await to finish before revoking its grant, stopping the read
  provider, sending locator stop or closing stores. Health performs post-reply
  live/authority/deadline checks, so changing those dependencies first would
  manufacture another health failure.
- Give the join an explicit cutoff no later than the original service/stop/outer
  allowances and an operation-sized cap. A health command already has an
  absolute operation deadline; waiting for it must not replace that deadline or
  renew service authority. `open` already reserves two operation intervals,
  two provider drains, locator teardown and margin (service 79-88). The concrete
  repair must account for its wait inside those existing reservations, not
  merely wait until the final outer instant and starve teardown.
- On a healthy reply, the monitor exits at its next wake test, then the unchanged
  stop/close path can run. A real health error, refusal or expired operation must
  remain failed. On join expiry, explicitly record uncertainty and perform only
  bounded cancellation/cleanup; retain the existing controller channel poisoning
  and strict failed outcome. Do not clear flags, suppress genuine health errors,
  accept a forced kill as orderly stop, or detach unowned shielded work.
- Separate monitor quiescence from startup cancellation. A pending `_start_task`
  can be awaiting `location.start()` or its first health operation; interrupting
  incomplete startup is an abort, not the normal successful-start close witness.
  Inherited location `start()` already records failure on cancellation
  (controller 163-171). Do not blanket-convert both tasks into a success drain or
  advertise CLOSED for interrupted startup.
- A still-live monitor or startup task must prevent store closure and a clean
  report, even if bounded cancellation did not finish. The predecessor's final
  `idle` predicate tracks intake, retained/read actors and busy flags, but does
  not explicitly check monitor/start completion (service 329-339). The successor
  must make this liveness condition explicit, particularly if it introduces a
  shielded join. This is a repair safety obligation, not evidence of a second
  observed actual01 fault.

## Small deterministic control

Support_guest independently confirmed the same selected trace and suggested the
following focused boundary. Root selects any eventual implementation/runtime.

Use the real selected service monitor/close, advertisement health and inherited
locator command methods. Keep startup's first status exchange successful. On a
subsequent monitor status, use an explicit Event/barrier at the I/O boundary after
the status frame is written and before its bound reply is delivered. Start close
only after that barrier; use a second observable barrier at monitor join/close
entry to establish ordering, not a timing sleep. Release exactly one correctly
sequenced status reply while the original operation deadline is still valid.

Expected successor result: no premature cancel/kill or stop while the status is
held; status reply consumed once; no additional health iteration after wake;
stop follows status; monitor/start tasks done; strict CLOSED only if all ordinary
cleanup predicates also pass. The predecessor schedule should demonstrate the
channel-failed consequence if a separate, explicitly selected comparison is
needed; it must not become a repeated broad campaign.

Add one bounded negative companion: withhold or fail that reply, retain the
original operation/close deadline, and require a failed/uncertain result, no
renewed allowance, no clean store closure while any tracked actor remains live,
and eventual bounded containment. Cancelled callers must not orphan the tracked
close task. Capturing booleans/counters is sufficient; no credentials are needed.

A scripted pipe/process is synthetic I/O, not actual Node/network qualification.
It can establish orchestration and framing/cancellation behavior only if the real
command method and flags are retained. Replacing `command` with an always-healthy
stub or hard-coding a clean report would remove the very failure boundary under
test. Genuine installed behavior remains a separate later integration gate.

## Actual01 causal limit

`MANAGED-CONTRIBUTION-PUBLIC-OUTCOME.md` remains sealed at SHA-256
`2615e89927a18ba88301f724b3025bd52a1eb6e185110733c0e36fc0b4b84e42`.
It established the separate source-allowance defect (4 MiB source allowance versus
the existing 16 MiB route reservation), one charged INCOMPLETE request, no host
custody and a separate `GENERATIONS_CLOSE_UNPROVEN` outcome. It did not retain
the actual service final report or a locator command/result transcript.

Therefore the source race is a justified repair target, but **not an established
cause of contribution01's closure failure**. Successful supervisor reaping does
not prove service-level orderly close; a remaining SQLite journal does not prove
this race; health intervals and maintenance settings do not recover a missing
interleaving. No failed run, charge, source or installation is rewritten here.
