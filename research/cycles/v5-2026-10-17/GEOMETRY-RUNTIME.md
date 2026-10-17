# Fixed-po17 runtime decisions and outcomes

## One snapshot-host link: conditional selection

2026-10-17, root. The full deployable-v5 objective is unchanged. This is one
bounded prerequisite, not a substitute release or a proof certificate.

Root read/adopts independent GEOMETRY-REVIEW checkpoint
`6cd32b56701f8e8a8fad19f609771f81256d22599bd7f4bf64652028543d2fb2`:
host/builder/layout sources, exact build selection and corrected launcher pass
source review. The launcher additionally passes PowerShell syntax parsing,
without execution. All used predecessor evidence remains frozen.

Select **one** compile-only call of Launch-GeometryBuild01.ps1,
SHA `02f6cb195af46db2db16fbbdccadda5a675af3717ca1bd2d4f3aaef83c054d5a`,
against build selection
`9c3f00c28766c3f873bd7e782d0e0389e9b989839613b2c4a7eb7c061255fccd`.
The immediate gate requires at least3GiB both available physical memory and
true commit headroom, and no competing heavy process. Insufficient headroom
returns DEFERRED without creating a run/attempt or starting Python/compiler.
It supplies no permission to change system settings or stop user applications.

The single compiler Job is240CPU/300wall/2048MiB/six processes. Builder
controller40/60CPU and total420wall,512MiB/8192 output,1MiB command logs remain
unchanged. The enclosing hidden-process launcher checks450wall/60controllerCPU,
256MiB sampled controller private memory and1MiB logs, including terminal
CPU/wall/log checks;450 seconds is an outer cleanup/watchdog envelope, not a
renewal of the builder's420 seconds. Controller memory observation is not a hard
Job memory cap. Only its own child may be terminated; the compiler retains its
existing kill-on-close Job boundary. Failure is retained without automatic retry.

The launch report's actual child CPU includes Python startup and exit; it
**replaces**, rather than adds to, the builder's overlapping controller CPU.
Compiler Job CPU and launch-supervisor CPU are separate. PowerShell startup
and final launch-report tail are explicitly excluded, never asserted zero.

No produced executable invocation, guest execution, proof or stage-host build
is selected here. Successful compilation requires a saved-outcome review.
Any layout requires its own actual profile/source/runtime/input plan and
separate finite selection. Any subsequent proof requires the complete useful
layout and its own resource/assurance decision.

## Current outcome

Not yet invoked at this checkpoint. The previous observational memory check
was below the gate on true commit, not on physical availability. No allocation
has been consumed by a geometry build or layout.
