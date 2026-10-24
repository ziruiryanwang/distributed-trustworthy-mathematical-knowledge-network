# Strict intake implementation checkpoint

2026-10-24. Root-authored source candidate, not runtime evidence or adoption.

`software/v5/ordinary_baseline/baseline_intake.py` implements the selected thin
intake over existing `OrdinaryAdmission.preflight/admit`. Its inert input parser
and census come from the independently authored `baseline_bundle.py`.

The first pass validates every selected evidence file and projects exact bindings
only for feasibility. The second pass rereads pinned bytes and invokes actual
admission against the last confirmed protected root. No projection, receipt,
saved cursor or externally asserted success can commit mathematics. The caller
may explicitly select any eligible compatible root; no historical ancestry is
needed for exact portable-unit reuse.

Known capacity checks include batch/native array limits, cumulative syntax and
binding metadata, exact custody addition including export locators, catalog
roots/operations/artifact reservations, per-batch introduced-binding record,
cumulative context names and bounded future parent-plan encoding. Existing
checks include the native worker's full 16-MiB plan wrapper, not only its module
array or the catalog's possibly different manifest ceiling. Existing
custody objects and locators are read back before they count as zero new quota.
Actual admission still stages every supplied unit, including reused units.

`IntakeBudget` reserves a fixed caller-selected per-batch CPU cap without refund.
Controller CPU is additionally charged live. Reserving a cap even for an
all-reused batch is conservative authorization accounting, not measured usage.
Observed worker CPU is separately labeled and never treated as proof of zero
expense after a missing final report. One invocation is single-use; a later
explicit invocation is a new allowance, not a silent retry.

The independent review clarified conservative-grant accounting: a clean successful
admission need not stop solely because complete CPU measurement is unavailable;
the whole reserved cap remains charged. Missing actual checking/commit/cleanup
authority still stops. Reports explicitly disclaim complete worker CPU observation.

On an error, `IntakeError.report` retains confirmed prefix observations and
marks an unreturned admission as a possible unreported commit. It does not
assert rollback. Existing protected status/context recovery remains the only
route to selecting a durable root after uncertainty.

No input-spool copy or progress database is added. Exact derived files are read
twice; mutation refuses when their pins no longer match. A conservative
`128 MiB + 2*log_cap` admission-call-spool reservation per predicted new batch
is separate from native snapshot reservations. It is an authorization bound,
not filesystem enforcement. Physical disk/database pages and hard controller
CPU/RSS containment remain actual runtime/supervisor obligations. Initial
`CallLimits.max_spool_bytes` is <=2 GiB; all callers may only lower its ceiling.

The reviewed A2 original-library correspondence is still a necessary integration
step. Intake deliberately returns `ordinary_library_registered: false`; this
source is not a deployable baseline workflow or a full-v5 milestone. No native
build, real catalog/store operation or test is selected here. Independent review
and focused inert controls precede any future actual integration selection.

## Completed changed-boundary control, not actual admission

Later on 2026-10-24, root selected and ran only the 24-case inert syntax/planning
control at `experiments/v5-local-checks/ordinary-baseline-controls-01` under
selection `87642e3e603716552f00a9cf0f759f78e4efa8e3b53ffdc13a89f1a6141574c7`.
Independent saved-outcome review13787595 verified all155 runtime pins and five
snapshots, expected cases, no forbidden calls and clean process closure. Root
read that review and the actual saved case results and adopts this limited result.

Final tested intake SHA-256:
`b5a17aa580f8d9cfdeaaded7d93c2b12ad6e19e5018bf5e7c087cb56760069d8`.
Elapsed4.1454236seconds;3.875known inclusive CPU seconds;53,825,536peak Job private
bytes. Existing package, protected state and retained input evidence are unchanged.
No native checking, durable commit/recovery or ordinary reference was exercised.
Used sources and evidence freeze; do not rerun this completed boundary.
