# Typed-row controls selection: source-only contract review

Reviewer: `core_search`, 2026-10-20. **CLEAR for the specified selection seam.**
This checks the new selector against the build result format, retained local
runner and control wrapper. It does not duplicate the independent test/runner
review, adopt the live build outcome or authorize execution. No test, native
checker, compiler, guest, proof or selector was run in this review.

## Exact reviewed inputs

| File | SHA-256 |
|---|---|
| `research/cycles/v5-2026-10-20/Select-TypedRowsControls.ps1` | `c82c45dd701ed2849c670222952028f8f24315dec8cb1761e11dbf926b2c51ca` |
| `software/v5/typed_rows/run_controls.py` | `60e9f67454b5e305f5379c4856177498f9aa2309df037fe6e78f12dc7bcb56b0` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

## Checked contracts

- The selector reads only `typed-rows-build-02/RESULT.json`, requires the
  caller-supplied exact result digest, the builder's actual success tag
  `PASS_TYPED_ROWS_FOUR_COMPILES_ONLY`, selected build digest `0eaf0bd5...`,
  and absence of the build finalization-failure override. This matches the
  builder's emitted fields; it is not a guessed alternate result schema.
- The binary is exactly that build's `typed_rows_tests.exe`. Its caller-supplied
  digest must match actual bytes and the result's output pin; its actual size
  must match the result's `bytes` field. The retained `artifacts.pin` helper
  really emits `path`, `bytes`, `sha256`, so the size/digest lookup is correct.
- The pinned advertised-service selection is used only as the existing outer
  Python/runtime basis. Its `argv[0]` names the installed v4 Python, and the
  selector requires that path in its copied/rechecked runtime pins. This is
  correct for `Run-V5-Check.py` and the wrapper; the separate compile
  controller's `D:\Python314` identity is not substituted into this lane.
- Build result, test binary and all three mandatory fixtures are additional
  runtime pins. Their exact paths/digests match `run_controls.py` and the
  compiled controls' environment-variable reads: delta packet `54c7dac7...`,
  aggregate input `7e21d092...`, and expected aggregate output `01d7c9cc...`.
  The wrapper supplies those variables explicitly and rechecks the files;
  the outer runner checks its selected runtime pins before and after the job.
- Exactly the owner runner and control wrapper are source-snapshotted. The
  wrapper path contains the runner-generated `sources` component, satisfying
  the wrapper's source-origin condition. `{output}\evidence` is fresh beneath
  the selected run directory and matches the wrapper's path checks.
- The command arguments match the wrapper's parser: exact binary and digest,
  fresh output, and `--expected-tests 8`. The wrapper runs the selected Rust
  binary once with `--test-threads=1`; it does not filter or skip the retained
  positives. Its suite check requires eight distinct success lines, exit zero
  and no failed, ignored, measured or filtered tests.
- Limits are exactly 40 cumulative worker CPU seconds, 90 outer wall seconds,
  512 MiB and three active processes, with 1 MiB outer stdout/stderr ceilings.
  The wrapper's 60-second child timeout cannot renew the enclosing Job. The
  stated bound contains wrapper and native child; no compiler/prover starts.
  This is a prospective finite envelope, not a prediction of success.
- Selection schema/keys, safe name, source pin values and command placeholders
  match `Run-V5-Check.py`. The selector validates canonical cwd, refuses an
  existing selection or output directory, and writes one new UTF-8 manifest
  with exclusive-create and a durable flush. It never starts the test.

## Decision boundary

Root subsequently prepared, but did not launch, the exact plan
`experiments/v5-local-checks/typed-rows-controls-01-selection.json`, SHA-256
`4c648a97e777e0c2bcdf547f80107fb9bcdcea8e7a265c07874fe7c6ce361700`.
Read-only inspection confirms its schema, name, two source pins, 24 runtime
pins, installed-Python command, fixture/binary paths, eight-test argument and
40 CPU / 90 wall / 512 MiB / three-process limits match the reviewed selector
and wrapper. Its build result pin is
`add627e4fe4bdc102c79eeea745233d95cbfd56f48f58b118fe276adb6c00794`;
its 2,677,248-byte binary pin is
`83c27079595e36855c484be61d462810088fab7608eb2d1d598ac88c8b5d1c00`.
Actual result fields match those pins and the expected build selection,
report the builder success tag, and have no finalization-failure override.
This is narrow selection consistency, not a replacement for the independent
build-outcome audit. **Exact prepared plan also CLEAR at this review seam.**

No concrete selector/build-output/wrapper mismatch was identified. Root still
needs the actual independently reviewed successful build and the separate
test/runner clearance before choosing a one-shot run. A source-review CLEAR
is not an executed eight-test PASS, mathematical admission, performance or
full-v5 release evidence. No old run is repeated or old evidence rewritten.
