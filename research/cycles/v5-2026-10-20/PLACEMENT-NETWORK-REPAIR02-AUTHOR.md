# Placement service02: exact close repair

2026-10-21, core_release. Implemented only the fresh service selected by
`PLACEMENT-NETWORK-REPAIR02-SELECTION.md`. No runtime, product import, test,
networking, retry, Git mutation or edit to used sources.

Fresh `software/v5/placement_network02/client/serve_placement.py`:
**20422 bytes**, SHA-256
`319ddf075d2bd62c6e408dcc497fc5c507d277787637b0089aa60fbc65c96430`.
Frozen predecessor remains19750 bytes,
`07c60c4f33401d41694228d0f6bde35d9148e769947b75211e9ed4098ec68674`.
Read-only text comparison confirmed exactly these two replacements after
normalizing line endings; no other source differences.

1. Startup reserve becomes `2*drain + 2*operation + cleanup_seconds + 5`.
   Both intake and read shutdown drains are reserved; all other active/stop
   minima and authority checks remain. Active service may shorten, never extend.
2. Complete locator close uses `location_until = self._outer -
   self._drain_seconds - 2`, with a positive-remaining precheck, absolute
   `asyncio.timeout_at(location_until)` around the existing `location.close()`,
   and explicit postawait deadline check before accepting closed state.

The underlying locator still shields its own close task, retains six-second
native teardown, and performs complete runtime plus role-file verification.
No file check, adoption binding, public API, CPU/traffic allowance or original
outer deadline changes. The final read drain, stored-state actor checks and
original-outer-deadline refusal remain intact.

If the fixed cutoff is already expired, the precheck refuses before creating an
unawaited close coroutine. Timeout/cancellation still becomes the existing
closed `location_close` uncertainty and cannot produce successful closure.
The original locator's shield prevents cancellation from silently skipping its
mandatory final verification. Synchronous validation may overrun asyncio's
timer; the explicit postcheck prevents accepting that overrun, and the original
external Job remains the hard containment. A missed cutoff is failure, not an
extension or automatic retry. Existing error cleanup semantics are unchanged.

Conservative accounting uses both existing up-to-one-second monitor/start
joins. For `A <= T-(2D+2O+C+5)`, after those joins, intake drainD, stopO and
native teardownC, validation begins by `T-D-O-3`. Thus at least **O+1** remains
before `T-D-2`, conditional on timely scheduling and bounded prior phases.
This is an allocated interval, not a filesystem-throughput guarantee. Earlier
close can use additional original slack without minting another allowance.

Root owns adapter02's distinct reply-budget/diagnostic corrections and its
selection. Independent reviewer owns the changed-boundary source decision.
Failed01 and passing controls remain frozen; no repetition is selected here.
