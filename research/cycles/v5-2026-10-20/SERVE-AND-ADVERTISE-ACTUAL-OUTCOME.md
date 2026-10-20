# Advertised service actual-01: independent failure audit

2026-10-20, `core_release`. Canonical guard passed. Saved-evidence and source
inspection only; no rerun, imports, process launch, RAM investigation or Git
mutation. **Disposition: actual composition remains unestablished. Preserve
this failed attempt and do not repeat it merely with warmer files.**

## Verified outcome and identity

`experiments/v5-local-checks/advertised-service-actual-01/` records inner FAIL
and outer `COMMAND_FAILED`, child exit 1. The enclosing Job closed, reaped its
child and ended with zero active processes, no supervisor cleanup errors and no
supervisor termination request. This is clean enclosing containment, **not**
clean provider operation: provider location reported channel failure, forced
termination and return code 1. HTTP and workspace closed; the reader closed
normally with no forced termination.

All 113 selected sources match both originals and snapshots, and all 21 runtime
pins match. Saved/original selection SHA-256 is
`54ab4bf6209251540fcc6a51556044457a07a59a3eec943ebeeee6ac61898365`.
Outer result hash:
`dc583e558a18152f267520507341fb4ed7d4465430c603003d3933489f843b57`.
Actual result hash:
`25b7fb5625c7e16c566579a5415e3ea5e3d8262ffc412792944fdbc004f790dc`.

## Cause established by saved timings and source

The original inner deadline was 105 seconds. Its inferred start is
`2182076.4316047` on the saved monotonic clock. The reader's mandatory adopted
runtime precheck covered 5,896 files / 130,118,221 bytes and took
**59.864571 wall seconds, 4.9375 CPU seconds**. The evidence identifies this
verification phase as the dominant delay; it does not identify the underlying
filesystem/OS cause and does not justify a memory investigation.

The composed provider service began at `2182138.7768031`, or **62.3451984 s**
after that inner start. Its unchanged 41-second cleanup/final-status reserve
made its active cutoff `2182140.4316047`: only **1.6548016 s** remained for
HTTP plus provider startup and publication, despite the requested 45-second
active service. The provider's runtime precheck alone took **2.4752273 s**,
necessarily exceeding that remaining startup interval.

The source sets the active cutoff to the minimum of requested lifetime,
location lifetime minus two operation windows, and original deadline minus the
reserve. It correctly did not renew that deadline after the reader's cost.
Runtime pin verification is synchronous; the asyncio startup timeout can take
effect only after control returns to an await. The subsequent cancellation and
close intersected the shielded startup. Saved stderr's
`LOCATION_CONTROLLER_CLOSED_DURING_START` and the provider's zero IPC replies
are consistent with that failure path, not evidence of a protocol/authentication
or route-search defect.

Provider HTTP did bind, but there was **no provider READY, route dispatch,
health check, HTTP request, authenticated offer or page**. Only the reader
achieved role readiness; the two-role attempt count is not two successful
roles. Native/proof calls and mathematical acceptance remained zero/false.

Known whole-run CPU is `13.859375 + 0.875 = 14.734375` seconds. Recorded wall
time is **73.51401739986613 s**, within the original 120-wall/45-CPU enclosing
limits. No resource-limit termination is reported. All failed work remains
charged; the earlier inert-control PASS is not upgraded by this result.

## Decision

Agree with root's **no immediate rerun**. A warm-path repeat would add little
deployment evidence and would not resolve the already-known missing installed
location role. Preserve the unestablished ordinary-service integration question
for a separately reviewed fresh relocated optional-role boundary, after its
cheap source and lifecycle controls. That later selection must fund runtime
adoption/startup and teardown in one original envelope using this cost evidence;
it must not assume warm metadata access or silently renew a consumed budget.
This is a change of evidence target, not permission to relabel actual-01 as
passed or completed v5.
