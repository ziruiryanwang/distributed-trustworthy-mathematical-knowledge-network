# Source repair: cooperative health drain before locator stop

2026-10-21, core_release. **Source authored; no runtime, build, installation,
or contribution outcome is claimed.** This follows root's
MANAGED-CLOSE-DRAIN-SELECTION and its explicit adjacent startup-margin approval.

## Exact successor

- New service: `software/v5/managed_close_drain/client/serve_placement.py`,
  24566 bytes, SHA-256
  `c815331f035618b36f504d604a1fb75d8682439f0488453c72e9801a63d78bd8`.
- Preserved selected predecessor:
  `software/v5/retained_advertisement/client/serve_placement.py`,
  SHA-256 `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa`.
- Unmodified health implementation: advertisement5aa23ee7.
- Unmodified IPC safety implementation: controller4dc0824d.

Only four source blocks change: the activity cutoff; an immediate constructed
grant-deadline check; the monitor/startup close block (startup cancellation itself
preserved); the store-idle condition. Root explicitly approved the grant check
before review/adoption; the unused earlier039c source pin is superseded.

## Defect and ordering argument

The original close cancels the monitor. If its status command has already
written an IPC frame, cancellation enters the existing command's BaseException
handler, sets channel_failed, and terminates the child. Those are correct frame
safety actions, but an orderly service close should not itself trigger them for
a healthy in-flight status operation. This is a reachable source defect; the
lost component report from contribution01 does **not** establish that it caused
that particular failure.

Close now sets closing and wakes the monitor, then joins the tracked monitor
under shield. In one cooperative asyncio event loop, once wake is set, a monitor
waiting on wake exits without starting health; a monitor already executing health
finishes that single request and exits at its next loop test. No new task or
command reservation is created. Advertisement health is still checked against
the original active grant both before and after the command; the grant is not
revoked until the original subsequent intake/retained drain.

The join cutoff is the minimum of the original service deadline, the original
locator stop deadline, and close-time plus one configured locator operation.
The current health request's own cutoff is no later than the service deadline
or its earlier start-time plus that same operation interval. Thus an already
issued healthy request receives its existing allowance, not an extension.
The join is shielded so reaching the join timeout does not first poison the
command by incidental cancellation. A cancelled monitor, raised monitor error,
or missed join cutoff records cleanup uncertainty under `_monitor_task`.
An ordinary health error caught inside the monitor still sets
PLACEMENT_SERVICE_HEALTH_FAILED; close cannot erase it.

## Original finite reservation

Write D for the original service grant deadline, S for the stop cutoff, O for
the outer cutoff, d for the existing intake/read drain interval, o for one
locator operation, and c for locator cleanup. Open continues to reserve

`O - active_end >= 2*d + 2*o + c + 5`.

The necessary adjacent correction also requires

`active_end <= S - d - 2*o - 1`,

instead of merely `S - 2*o`. This shortens feasible service activity and never
extends S, O, grants, command counts or resource budgets. A short independent
locator deadline otherwise need not leave the existing intake drain before
stop. Subject to prompt cooperative scheduling and bounded underlying calls,
a close begun by D has one operation for monitor drain, d for intake/retained
drain, one operation for stop and one second of slack before S. Remaining outer
reservation still covers locator cleanup and read drain. Construction floors
the selected remaining interval, but the grant constructor samples a later
clock. Flooring alone therefore does not establish D <= active_end. The new
immediate check requires that exact inequality before provider/journal creation;
any violated margin uses the existing partial-construction cleanup and refuses.
The already charged grant is not renewed, repaired or lengthened.

These are sufficient reservation inequalities, not a hard-real-time OS guarantee.
The existing post-deadline checks and external whole-process containment remain
necessary for nonpreemptible synchronous validation, delayed scheduling, or
cancellation-resistant code. A caller that closes after its original active
deadline does not gain a new successful-close promise.

## Failure containment and stores

On monitor join failure, close requests cancellation and uses asyncio.wait with
timeout at most one second and no later than O. Unlike awaiting a cancellation-
resistant task through wait_for/gather, this wait does not require that task to
acknowledge cancellation before returning. The original cleanup continues, and
its error record remains even if cancellation later finishes successfully.
This is bounded attempted recovery, not conversion of failure into CLOSED.

Before advertisement/controller/workspace stores close, both tracked monitor
and startup tasks must now be absent or done, in addition to the original
intake/retained/read quiescence and busy checks. A still-live task prevents those
stores from closing and adds live_actor_prevents_store_close. Outer containment
owns any actor which remains alive. No journal or authority is silently cleared.

The locator's channel_failed/forced_termination/returncode conditions, exact
STOPPED requirement, original_outer_deadline check, final seven cleanup flags,
and health failure test remain strict and unchanged. Startup still receives
the original cancellation attempt and original one-second allowance; this patch
does not claim to redesign startup's cancellation-resistant behavior.

## Minimal remaining evidence

Independent screen review owns source adoption. Guest controls should exercise
the real extracted monitor/close/health/IPC methods with explicitly synthetic
framed I/O: a healthy in-flight reply, a genuine failing reply, and a resistant
pending actor that cannot authorize store closure. A small source arithmetic
check covers the tighter startup cap. These are deterministic changed-boundary
controls, not actual network/runtime or mathematical-growth evidence. Root
alone owns any later selection, build and installed contribution02.

No old source, installation, grant, failed result or historical evidence was
edited; no RAM survey, proof campaign or heavy experiment was performed.

