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

At2026-10-17T23:27:08.9125143Z the selected launcher returned
`DEFERRED_NO_PROCESS_STARTED`: available physical3,804,200,960B and true commit
headroom2,961,518,592B, below its3,221,225,472B requirement. No launch directory,
build run or attempt was created; no Python/compiler/host/guest/proof started.
The enclosing shell reported exit1 for this deliberate deferral. No geometry
build or layout allocation was consumed. Source checkpoint is Git `c83345f`.

Root selects only a source/retained-evidence assessment of a smaller compiler
envelope in GEOMETRY-COMPILE-ENVELOPE.md. This cannot change proof limits or
renew a failed build: no compiler attempt has occurred. The original selection
and used launcher remain preserved. No automatic poll or retry is scheduled.

## Build02: evidence-backed compiler-only envelope

Root read/adopts GEOMETRY-COMPILE-ENVELOPE `6fa3aa38` and complete changed review
`59030d053383534dd85d87b37cf0787d6a2b43ef0d827aa1693bc197d490ea23`.
Only three source literals change: builder declared/actual compiler memory cap
and matching adopter cap become1536MiB. Original host/helper bytes, all other
budgets, unchanged1,071 runtime pins and four corrected libraries remain.
Historical snapshot link peak932.637MiB and corrected stage-link peak1183.090MiB
justify one contained attempt, not a compiler peak theorem or guaranteed fit.

Root selects one new conditional call of Launch-GeometryBuild02.ps1,
SHA `cf63602e5d4a85b80905d56aacedd7df4bc95b6d9a01b64c564a4cde500e84db`,
using exact new selection
`f245889a729ff61726347cfad7673af1801a5e8104cd71f6d8c112af185d2b7c`.
Require immediate >=2,684,354,560B available physical **and** true commit plus
no heavy overlap:1536MiB compiler + unchanged1GiB margin. All other checks and
tail accounting remain the reviewed original launch boundary. First failure
stops; no automatic retry/cap change. This does not alter proof or layout caps.

Build01 selection/used launcher are retained unchanged and superseded, not
reused with new bytes. The revised builder/adopter are still unused at this
selection. No executable invocation/layout/proof follows automatically.

### Build02 actual outcome, independent audit pending

The single launch completed exit0 in root session3977. Immediate headroom at
2026-10-17T23:30:31.5562334Z was3,658,031,104B available physical and
3,324,321,792B true commit. No competing heavy process was admitted.

- Builder RESULT:
  `a44a521bfebf8c0c72cdcac28a36143b2f8b58f168936674275efb4162a38360`.
- Launch RESULT:
  `5ca2e81c227a25881d0395a877ed1f2b2e10ed05ab17f07cff2cb93981334041`.
- New host:6,631,424B,
  `4606258931a7c793c66e5002ee864bbfb8f7f9d81850b88bf1256126ac254869`.
- Compiler Job133.734375CPU seconds; peak983,511,040B; final0active/terminated.
- Python controller including startup/exit7.078125CPU seconds; launcher7.375CPU.
  Known disjoint sum148.1875CPU seconds; outer153.7786227wall seconds.
  Builder's6.921875controllerCPU is contained in Python's value, not added again.

Only one snapshot host was linked. No executable/guest/proof was invoked.
All used builder/host/helper/selector/launcher and input/output bytes freeze.
Independent saved-outcome review remains necessary; the raw process/build
PASS does not itself select the layout or qualify the final v5.

### Actual build adoption and layout-data preparation

Root read/adopts GEOMETRY-BUILD-OUTCOME
`68af53904cbce8532e2ffe582c8eff08bd8a907ddd0516522ce0db6a8e31ebd3`.
The one-link executable46062589 is now adopted for a future snapshot operation,
not mathematics. Actual audit discloses the owned VCTIP post-build cleanup and
all separate administrative output/tail accounting; no historical toolchain
census or passing build was repeated.

Root also read/adopts GEOMETRY-LAYOUT-REVIEW source checkpoint1b51e00c and the
complete wrapper/selector/plan. Select one **data-only** call of selector
`e276434c9b896909596f51482276b972f8e928cc1a411b99bd00cf8ea8bf9fc4`, using
actual build02 and actual RESULT a44a521b. This writes only fresh packet,
profile, configuration and outer selection under experiments/v5-local-checks.
No Python import, native host, execution layout or proof runs in this step.
Exact generated-map review and a separate launch decision remain required.
