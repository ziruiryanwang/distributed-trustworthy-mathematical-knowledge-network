# Exact-custody control selector: independent source review

2026-10-20. Reviewer: core_growth. Source review only; no selector, import,
test, build, proof or service was executed.

## Decision

**GO for staging after root supplies the final, independently reviewed fifteen
successor hashes.** No selector blocker found. This is not control-source
approval or execution approval: `tests/controls01.mjs` was still absent at this
review, so an executable selection cannot yet be completed. Root owns the
later finite launch decision and actual outcome adoption.

Reviewed selector:
`research/cycles/v5-2026-10-20/Select-ExactCustody01.ps1`, SHA-256
`d1a82c08684b7bb83ddc2c292685f285872292afce5dec873054ed2caf4d0955`.

## Binding and preservation argument

- Requires the exact canonical working directory. Writes only the new
  `experiments/v5-local-checks/exact-custody-controls-01-selection.json`, using
  `CreateNew`, and refuses an existing selection or output directory. It does
  not execute selected code or modify predecessors/installations.
- Pins baseline selection `92cad921f57e1f5ca6e93e0954198619ba8f75ed8ad0288dd2dd4e4b32d2a542`
  and its 154 source hashes, then pins current113 SDK map
  `ad2c15a27a51f749104ac09f9cafee210a108fb0bf46bafad8b2a9542f86d38f`.
  Each SDK source must remain beneath canonical `software/v5`, match its hash
  and byte length, and agree with any already selected physical path.
- The reviewed JSON argument is bounded to 16 KiB and must contain exactly the
  fifteen specified fresh `body_location` successors. Each source must match
  its supplied reviewed hash; no caller-selected extra path can enter here.
- The fixed baseline/map union contains 173 physical sources. Adding fifteen
  fresh successors gives **188 sources**. Baseline19 runtime pins plus map and
  retained Node executable give **21 runtime pins**. These totals are fixed
  indirectly by the pinned inputs rather than separate final count assertions.
- The selected command uses the baseline pinned Python with `-I -S -B` and the
  snapshot's exact control entry point. Retained Node is pinned to
  `b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3`.
  No downloaded runtime, shell-expanded command or live locator is selected.

## Execution-envelope interpretation

The proposed envelope is 45 Job CPU seconds, 90 outer wall seconds, 384 MiB
Job memory, at most three simultaneously active Job processes, and 1 MiB each
stdout/stderr. `tools/Run-V5-Check.py` snapshots pinned sources and directly calls
the frozen supervisor. That supervisor creates the selected Python child
suspended, assigns it to one Windows Job, and resumes it. The control's single
Node subprocess inherits that Job. Thus the intended worker tree is Python
plus Node: **three is an upper limit, not evidence that three workers are
necessary or observed**. The outer runner/controller is outside this child Job;
its CPU is reported separately and checked by the existing wrapper guard.

The frozen runner caps selections at 256 files, 2 MiB per source and 16 MiB
total, checks ordinary canonical paths, requires its own pin, and checks runtime
pins before and after execution. It finally compares both selection bytes and
snapshot bytes. The proposed188-source selection fits the count ceiling; actual
source-byte bounds remain runner-checked. The supervisor requires clean
descendant closure and reports termination/cleanup uncertainty. These are
resource and evidence controls, not a hostile-input security sandbox.

The current Python control source runs only eight selected changed-boundary
groups; it imports fixtures, not predecessor suites. Only after Python success
does it request one bounded Node control with a25-second timeout. The selector
review does not certify those unfinished controls or predict their result.

## Before launch

Root should retain the final reviewed source map and the resulting selection
hash; check the reported188/21 counts; obtain control-source approval including
Node vectors; and make one separate launch selection. A subsequent source
change invalidates its reviewed hash. No passing predecessor campaign should
be repeated, and no component result constitutes final v5 completion.
