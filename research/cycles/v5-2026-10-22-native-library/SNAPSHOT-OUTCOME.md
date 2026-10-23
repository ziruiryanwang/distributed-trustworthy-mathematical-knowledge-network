# Actual ordinary snapshot controls01 outcome

2026-10-22. Source author's read-only saved-evidence review, **not an independent
software audit**. Root independently inspected logs/results and owns adoption.
No rerun, runtime import, code modification or Git operation in this review.

**PASS for the seven selected conditional-fixture snapshot controls.** Selected
LocalSnapshot compiled and the seven exact markers completed in one operation.
Evidence root: `experiments/v5-local-checks/ordinary-snapshot-controls-01`.

All seven saved source files match their selection hashes. All six selected05
compiled-core/source pins also independently match. The selection digest equals
the result's `selection_sha256`. The actual runner contains both reviewed repairs:
partial-timeout log retention and exact ordered marker/complete-line validation.
Its commands compile only LocalSnapshot and run only LocalSnapshotChecks, using
the exact compiled05 prerequisites rather than rebuilding/rerunning old suites.

The stdout contains each marker exactly once in the selected order:

- `two-chained-deltas-without-intermediate-restore`;
- `exact-map-restore-without-ancestor-checking`;
- `restored-theorem-supports-new-consumer-proof`;
- `incomplete-import-plan`;
- `wrong-parent-plan`;
- `existing-output-refused`;
- `uninitialized-parent-refused`.

The source confirms the first two commits use the actual returned environment,
without an intervening import; restore receives only the local plan, compares
exact stored records and moves ancestors into stage1. The subsequent kernel call
checks only new C using restored B. These are meaningful selected boundary
controls, not a claim that accepting unfamiliar peer mathematics is now solved.

Saved artifacts are exactly `basis.olean`7528B, `first.olean`1144B,
`second.olean`1112B. The refused uninitialized-parent path is absent. Existing
file preservation is explicitly asserted by the executed test. Both compilation
and controls exit0. The outer report records direct child reaped, zero active
processes, closed Job, no cleanup errors, and no requested termination.

Known cost:2.796875 Job CPU +0.421875 wrapper CPU = **3.21875 CPU seconds**;
outer wall3.1676758001558483 seconds; peak Job private commit974704640 bytes.
No supervision subinterval is added twice. These fixture figures do not estimate
real Std closure admission, full-network growth or large-library startup cost.

The output explicitly says conditional Init-subset fixture, no catalog authority,
no basis adoption and no public deployment. Artifact loading avoids proof replay,
not reading/mapping selected proof-value bytes. Protected catalog integrity,
profile/digest authentication, real basis initialization, withdrawal integration
and a genuine reciprocal ordinary workflow remain separate required work.

| Evidence | SHA-256 |
|---|---|
| selection.json | `c6b2a95c4e3fa144f7d33afd55494e1db2a29eea478b17076dc8e228a6b2377b` |
| RESULT.json | `cecd07c3ed9d73e79233592e55d8e10160ccd8d14bcc438564fbc29ada358f6b` |
| CHECKS.json | `390123211d9704947435d449cb1cf8151c97b410403a7166fe59fb3ca66c9aa9` |
| snapshot-controls.stdout.txt | `89cb72f29a96207055135185791028460e88834f3f7487f5658ba1fba3672189` |

Keep the successful source snapshot, compiled file and outputs frozen. The next
source work is the actual selected-basis writer and controller integration, not
another snapshot-controls campaign.
