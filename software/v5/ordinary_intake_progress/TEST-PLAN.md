# Focused intake progress controls

Source/test preparation only under CONTRACT.md. Root owns runtime selection,
integration and Git. No test, product import, owner call, database opening or
native operation has run for this plan. The canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision being tested

Can the selected intake emit bounded, durable intent/observation records while
preserving its existing admission sequence and honest failure report? These
controls do not establish a new mathematical acceptance rule or diagnose the
cause of the earlier interrupted intake. A progress record is never a warrant,
resume cursor or substitute for protected status/context validation.

Use the actual predecessor and successor `_plan_all` and `intake` control flow.
Load the five pinned pure evidence/identity/catalog helper modules plus those
two intake sources. This uses the real `PortableCatalog._write_fresh`, including
exclusive creation, flush and fsync; neither catalog's `open` may run.
The admission, manifest, custody, catalog and
native results are explicitly small doubles. A fake `CHECKED` return supplies
only a test observation. No real owner, protected state, SQLite or Lean is used.

The predecessor is the adopted package's `reference/baseline_intake.py`, SHA-256
`9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142`.
Real ordinary path checks and exclusive disk writes apply only beneath the
fresh control output. All subprocess, SQLite-connection and socket entry points
are forbidden during controls. Prior sources and the eleven-group parse-reuse
suite remain untouched and are not rerun.

## Focused obligations

1. Compare a small successful intake with the predecessor. Require identical
   read/planning/preflight/admit ordering and counts, admitted input bytes,
   resource reservations, observations and output projections (apart from the
   additive `progress_directory`). A fixed observation-clock double makes the
   original resource fields exactly comparable; the outer harness uses real time.
2. Inspect exact scalar records for entry, metadata boundaries, actual-read and
   preflight boundaries, admission intent, returned prefix and terminal outcome.
   Require contiguous fresh filenames, the exact schema, explicit uncertainty,
   monotone record numbers and finite nonnegative cost observations. No raw proof,
   generated native input, aggregate proof tree or arbitrary exception string
   belongs in an intermediate record.
3. Exercise the explicit record/count/total-byte limits and the 64-batch maximum
   with tiny doubles. Validate the no-sink `_plan_all` default separately, without
   creating diagnostic paths or changing its returned metadata.
4. Refuse nonordinary, reused and colliding diagnostic paths without overwriting
   retained bytes. Use real fresh file paths; a simulated redirected-path stat
   is labelled a path-check double if creating an actual link is unnecessary.
   Inject a write/fsync failure and require any written prefix to remain.
5. Fail a diagnostic write before synthetic admission. Require no new admit
   call, the correct previously confirmed prefix and no invented unreported
   commit. Do not retry within a control scenario.
6. Fail logging after a genuine synthetic admit return. Require its root and
   observations to be recorded in the thrown `IntakeError` before the logging
   error, the original worker-cost observation to remain and uncertainty false
   for that returned call.
7. Make a later synthetic admit raise. Require the earlier confirmed prefix,
   `possible_unreported_commit=true`, the original exception as cause and error,
   and preserved original error when terminal diagnostic logging also fails.
   Metadata/preflight failures remain before-admit outcomes with uncertainty
   false. Terminal success logging failure must not undo a confirmed prefix.

## Agreed interface and exact expectations

The private sink is `_Progress(owner.directory, parent_root, budget, calls)`;
its `record(event, *, batch=None, manifest_sha256=None,
selected_root_validated=False, last_confirmed_root=None, confirmed_batches=0,
possible_unreported_commit=False)` writes a fresh numbered JSON file under
`owner/intake-diagnostics/<random-32-hex>`. `_plan_all(..., progress=None)` keeps
its no-sink default; the selected intake supplies its private two-scalar callback.

Every record has exactly these fields: `schema`, `authority`, `sequence`,
`event`, `batch`, `selected_root`, `manifest_sha256`, `selected_root_validated`,
`last_confirmed_root`, `confirmed_batches`, `possible_unreported_commit`,
`wall_seconds`, `controller_cpu_seconds`, `native_cpu_reservation_seconds`,
`observed_worker_cpu_seconds`, `worker_cpu_accounting`.

Expected schema is `DMKN_BASELINE_INTAKE_PROGRESS_V1`; authority is
`DIAGNOSTIC_OBSERVATION_NOT_WARRANT_OR_RESUME_CURSOR`; worker accounting is
`PARTIAL_OBSERVATION_NOT_COMPLETE_MEASURED_CPU`. A `BATCH_CONFIRMED` observation
precedes the existing finally-block worker-cost addition. Thus the two synthetic
successes show 0 and 1.25 observed worker seconds at those records and 2.5 at the
terminal record. This is explicitly partial accounting, not elapsed-to-death or
complete native/custody CPU measurement.

The two-batch successful stream contains exactly 19 records. The 64-batch stream
uses all-reused tiny doubles, respecting the unchanged spool ceiling, and has
515 records. A direct extra writer call uses the conservative 516th slot;
the next call must fail without creating a file. Separate direct controls
exercise the 2,048-byte record and 1,056,768-byte total bounds. Artificial private
counter/encoder changes test these guards; they are not a hostile in-process
threat-model claim. Existing native spool plus diagnostic reservation must fit
the original allowance. No spool-cap increase occurs.

Success and `IntakeError` expose `progress_directory` only as a diagnostic
location. It is `None` when sink construction failed. All old result fields,
including the original cause/error and confirmed/uncertain prefix, retain their
prior meaning. Tests exercise this convention and compare every old field with
the predecessor where the mathematical call path is unchanged.

The seven saved group names are `unchanged_calls_and_no_sink`,
`exact_scalar_progress`, `derived_record_byte_spool_bounds`,
`ordinary_fresh_exclusive_partial_paths`, `pre_admission_diagnostic_failure`,
`post_return_and_terminal_failure_preserve_prefix`, and
`original_error_uncertainty_and_existing_refusals`.

## Prospective finite execution

Use `tools/Run-V5-Check.py` directly, one fresh `intake-progress-controls01`
allocation, no nested supervisor. Proposed outer envelope: 60 wall seconds,
45 inclusive Job CPU seconds, 512 MiB, one process and 1 MiB per stream. The
small harness itself checks 45 wall / 30 CPU seconds cooperatively. No
capacity increase or timing comparison is sought.

Only fresh control fixtures, progress records and `RESULT.json` may be written
under that allocation's `controls` subtree. Preserve the first success/failure
and all partial writes. Success requires the exact expected groups, no forbidden
call, explicit double-authority and `mathematical_acceptance=false`, plus normal
runner closure. Root must separately pin and select the final reviewed sources.

Exact prospective command:

```text
D:\Python314\python.exe -I -S -B
  {snapshot}/software/v5/ordinary_intake_progress/controls.py
  --output {output}/controls
```

There are nine external input pins: the six package Python files listed in
`controls.py:PINS`, plus `D:\Python314/python.exe`, `python314.dll`, and
`python3.dll`. Five source snapshots suffice: the existing runner, `controls.py`,
the successor `baseline_intake.py`, this plan and CONTRACT. Root may additionally
snapshot the independent review. No selector program, native executable, live
store, reconstructed Std tree or proof fixture is needed.

Require terminal `PASS_FOCUSED_INTAKE_PROGRESS_INERT_CONTROLS`, exactly seven
groups, no forbidden calls, the explicit
`SYNTHETIC_ADMISSION_CATALOG_CUSTODY_MANIFEST_NO_MATHEMATICAL_ACCEPTANCE` label,
and `mathematical_acceptance=false`. The existing runner must also report zero
exit, reaping, closed Job, zero active/terminated processes, empty cleanup errors
and stderr. Preserve the first failure without retry or reinterpretation.
