# Focused parse-reuse controls selected once

Root read the complete successor diffs, DESIGN, controls, TEST-PLAN, selector
and independent REVIEW `7889382967ad7d7f7a745a8258e0afc8812679af819ff9e6ef4cc2dba565b1db`.
AST-only parsing passed for all six new Python files. The generated exact
selection is `experiments/v5-local-checks/parse-reuse-controls01.selection.json`,
SHA-256 `5e9e52158134af517da07edd22f816b51326864c03ddfadeeb887457aa890b85`.
The independent reviewer recomputed all 22 source/external pins.

Select that single native-free run: seven source snapshots, fifteen external
pins, eleven focused groups; outer 60 wall / 45 Job CPU seconds, 512 MiB, one
process, 1 MiB per log; inner 45 wall / 30 CPU. All used sources now freeze.
No real owner/database/native/network operation or mathematical acceptance is
part of this run. Preserve first success or failure; no automatic retry.

File-only assembly source review `10876ce5972ef846327c6f282c0d0043f6d6bceb894196d8d534403fd9011696`
has also been fully read, but its execution remains conditional on independent
adoption of the actual controls. No package, initialization or Std intake follows
automatically. The current release stays unchanged and v5 remains active.
