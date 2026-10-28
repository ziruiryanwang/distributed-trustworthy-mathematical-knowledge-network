# Complete only the unfinished operator controls

2026-10-28. Root-selected source-only continuation; execution remains separately
selected. Preserve `control_tests.py`, all kit implementation/map files and
`experiments/v5-local-checks/current-operator-controls01` unchanged.

## Preserved failure and its cause

The original controls01 process failed at `control_tests.py:390`. Its saved
`command/stderr.txt` shows that the helper raised `KIT_PARENT_SUCCESS`, while
the test expected `KIT_PARENT_OPERATION`. This is a test expectation error,
not evidence that the helper accepted an unwrapped report.

The actual retained receive report's `result` contains `operation: "receive"`.
Consequently, when presented without its enclosing report, it passes the
operation discriminator in `accepted_report`. It then fails the next required
wrapper check: it has neither `ok: true` nor `profile_sha256`. The correct first
refusal is `KIT_PARENT_SUCCESS`. The production helper must not be weakened or
changed to satisfy the mistaken expectation.

The original run remains **FAILED**. Its completed observations can be audited
individually, but neither this continuation nor a corrected expectation turns
the original run into a pass. Seven earlier groups/eight positive preparations
must not be rerun. The report-negative group had reached this final unwrapped
case; the subsequent ten approval/selection/pin cases and final integrity check
were never reached.

## Exact continuation

`control_remaining.py` loads the frozen test source only under SHA-256
`91b40f6273d27a842d2ed4d7496a2dca3de39373b84dea58a3d9a664b55644ab`.
It uses its inert test helper definitions under a private module name. It never
calls that file's `main` or `Controls.execute`, and does not alter its contents.

The continuation has exactly three groups:

1. Assert the genuine unwrapped result's observed shape, then require
   `KIT_PARENT_SUCCESS` and absence of prepared output.
2. Run only the ten unfinished cases from the frozen final group: false source
   approval, false project approval, missing project approval field, frontier
   without project, repeated and out-of-range target selections, duplicate output
   names, duplicate acquired target names, output/acquired overlap, and changed
   source pin. Each must refuse before writing a prepared directory.
3. Recheck the original 62 selected public input files plus the frozen test
   source unchanged. Preserve the same process/network/database prohibition and
   selected-file read/fresh-tree write restriction.

Expected continuation census: **0 positive preparations, 11 refused
preparations, 3 groups, 63 selected input files**. Reading/hashing package source
bytes for integrity is not a rerun of adapter preparation or mathematics. No
native/generated artifact, state database or bundle unit is opened. No product
module is imported. Small fresh negative fixtures and requests are retained.

## Selection and invocation

Root selects the same 62 external inputs listed by the frozen test, plus that
test source, and snapshots the new continuation/approved runner separately.
The exact inherited kit pins stay `prepare.py:359bd0e8…`,
`prepare_selected.py:9881e2ad…`, `compatibility.json:08129a60…`.

```text
python.exe -I -S -B control_remaining.py
    --source-root ABSOLUTE_CANONICAL_ROOT --output FRESH_REMAINING_DIRECTORY
```

Use the approved Windows Python and a root-selected bounded outer Job. The
60-second wall/30-second CPU checks are cooperative, not hard containment.
No automatic retry, deletion, overwritten evidence or retrospective run status
change is permitted. Source review, actual execution and actual outcome review
are separate. Passing these controls would complete the selected inert handoff
checks, not establish native correctness or final v5 readiness.
