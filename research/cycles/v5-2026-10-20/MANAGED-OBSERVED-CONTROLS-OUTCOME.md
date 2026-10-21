# Actual managed-observation control outcome

2026-10-21, support_guest. **PASS_SELECTED_FIVE_EXTRACTED_HELPER_CONTROLS.**
Saved-output audit only: no rerun, product import, process/network inspection,
credential access, build, proof, deletion or Git mutation. This reviewer authored
the controls; core_release independently reviewed their source and selector in
MANAGED-OBSERVED-CONTROLS-REVIEW. The present review is separate from root's
execution, not a claim of independent test authorship or owner-source adoption.

## Bound evidence

All paths below are under `experiments/v5-local-checks/managed-observed-controls-01`.

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` | 8259 | `f75d01f5fc25d42f01da17451328d82446af5e3860ab61aa8e568a36b48d3434` |
| `observed-controls-result.json` | 849 | `8bcaa7cb4cecc7865d0671c2a01b90e29f5ecf982bd366390c28f059ee7f3069` |
| `RESULT.json` | 2040 | `0984b6338964b31f80a34393fab4e7674b86cad26ef2897599cdc23e375887cb` |
| `command/command.json` | 692 | `5e9e7e2f6371d0a46b25e1586825e7177ca8316c8d7f6a718085532f9ff686a6` |
| `command/stdout.txt` | 851 | `ce134397439dc3d107ac545568e327fc30376886140f31bd7fd9097b8b8ae70f` |
| `command/stderr.txt` | 671 | `e28d2d6e98edbeb247aff4bb31fed71d7b407b0b9cbad498c7c2509fc4d485d2` |

Original selection file and saved selection have the same exact selected digest.
All four original sources and four saved snapshots were independently hashed
against the selection: runner44a7bf1b, controls1a68c001, owner1c022737 and actual
selected formal_features8822c818. All28 runtime rows (39150032 bytes) were hashed
once successfully. They equal the build-basis runtime map after removing only
`distribution-managed-contribution-01-input.json`; no additional SDK or large
payload sweep was performed. A read-only audit count expression initially needed
PowerShell array materialization; the corrected count is28. This did not execute
or alter the tested program, inputs or outputs.

The pinned runner was read. It verifies runtime before/after the operation and
checks unchanged selection/snapshots afterward; a binding failure would replace
the passing outer status. The control additionally pins owner/F snapshots before
compilation and afterward. The saved command uses canonical cwd, isolated Python
`-I -S -B`, the copied controls and the exact selected `--output` path.

## Observed result and actual extent

Inner result reports five explicitly selected groups, zero failures, zero errors
and zero skips. The complete stderr identifies all five as `ok`, ending with
`Ran 5 tests in 0.003s` and `OK`. Stdout equals the result's exact JSON bytes after
removing only its terminal CRLF. The known synthetic secret marker is absent from
the inner result, outer result, stdout and stderr.

Passed groups cover exact failed-final projection, partial/unrecognized reports,
strict scalar and32-row bounds, synthetic-secret redaction without str/repr, and
fixed no-reference/report-error/serializer-error fallback. Actual F.compact/need
were used; the temporary serializer fault restores the original function.

Only the exact three diagnostic constants and four helper definitions were AST
extracted from owner1c022737. No complete owner import, worker, real service,
SQLite or credential operation was performed. The callback and secret markers
are synthetic. In particular, this does not qualify primary-error preservation
inside the worker, real cleanup, strict CLOSED/seal behavior or the separately
identified cancellation race. Those are distinct source/integration boundaries.

## Operational closure and cost

Outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child exit0/reaped,
final active processes0, Job closed, termination_requested=false and no cleanup
errors. Final Job reports total_processes2 and terminated_processes0; the selected
active-process limit is1, not a claim that cumulative total_processes equals1.
No orderly service-stop message was sent because this is a pure helper run.

Selected limits were10 CPU seconds,30 wall seconds,128MiB, one active process and
1MiB each stdout/stderr. Observed logs are851/671 bytes. Job peak private commit
was25919488 bytes. Job CPU is0.671875 seconds (0.59375 user +0.078125 kernel), plus
wrapper CPU0.40625, totaling **1.078125 known CPU seconds**. Nested supervision
CPU0.015625 is already part of wrapper CPU and is not added again. Outer elapsed
wall is3.20901109976694 seconds; command-through-cleanup wall is3.154453699942678.
The unittest0.003-second figure is test-method time, not complete workflow cost.

Accept only this small diagnostic-helper result. No public contribution02,
new installation, storage guarantee, mathematical acceptance, independent-host
operation or full-v5 qualification follows. All used controls/source/snapshots
and outcome evidence remain frozen; no repeat is recommended.
