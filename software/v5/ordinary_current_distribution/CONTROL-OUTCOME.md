# Independent actual focused-control outcome

2026-10-28. **PASS_SELECTED_SEVEN_GROUPS.** Saved-output audit only of
`experiments/v5-local-checks/current-distribution-controls01`; no test rerun,
product import, compiler, state/database, service or Git operation occurred.
The 87-source mapping review was not repeated.

The actual selection SHA is the cleared `40014e2a...`, with test snapshot
`95861889...`, builder `d14f2910...` and map `65fde356...`. Both source snapshots
match their selection pins; the recorded selection digest matches outer RESULT.
The runner completed its final external-pin binding checks without a binding
failure. Command stdout parses identically to controls/RESULT; stderr is empty.
The initial unusable snapshot selection remains never executed.

All seven intended groups report success: exact map/closure, all selected lane
transforms and changed-byte refusals, stale census/missing role/wrong receiver
lane, one synthetic positive and the following three synthetic negatives.

| Actual fixture | Saved outcome |
|---|---|
| Positive | Three synthetic stages, each sampled/charged 0.25 CPU seconds; actual retained package map is exactly 154 files, PROFILE has 117 auxiliary entries and the result has eight documents. Every actual package length/hash matches BUILD-RESULT. |
| Wrong map pin | No synthetic-build output directory, no stage record and no PROFILE. |
| Wrong core origin | STAGING failure `DISTRIBUTION_CORE_IMPORT_PATH`; zero completed stages/child charge, retained partial source/core fixtures, no PROFILE. |
| Unknown child CPU | Failure `DISTRIBUTION_CHILD_NOT_CLEAN:receiver-authoring-job`; exactly one stage record, absent CPU sample, full original 237-second grant charged, incomplete-CPU flag retained, no later stage or PROFILE. |

The last fixture's 237 seconds and the positive's 0.75 seconds are **synthetic
accounting values**, not observed processor time. The selected test's real
process/database traps and mocked Job boundary define its source-reviewed scope.
Actual native, owner, network and compiler execution remain outside this result.
The retained marker binaries/installation/PROFILE are explicitly fixture data
and must never be adopted as software.

Outer status is COMMAND_EXITED_ZERO_AND_CLOSED: zero child exit, direct child
reaped, Job closed, no termination request or cleanup error, zero final active
and terminated processes. The reported total process count is two. Peak Job
private commitment is 29,421,568 bytes. Whole-run wall is **15.98457 seconds**;
3.703125 inclusive Job CPU plus 0.171875 outer-wrapper CPU gives **3.875 known
CPU seconds**. Nested supervision counters are not added again.

| Decisive saved evidence | SHA-256 |
|---|---|
| outer RESULT.json | `4185a5a56b5fb999dba95057fe4460016b3e003f48627905eec1142606f37c7e` |
| controls/RESULT.json | `0c4a42c924b33a37db357167907b2bba9fd226e8dad918331a168f654178e617` |

This qualifies the finite changed controller boundary using actual selected
source and a real file-only installer. It does not qualify native compilation,
a deployable newly built package, mathematical acceptance or full v5. Preserve
the used source, positive/negative fixtures and exact results; no rerun follows.
