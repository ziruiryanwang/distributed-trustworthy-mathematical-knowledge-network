# Four-helper build: independent saved-output audit

2026-10-26. **PASS for compilation and clean closure of this selected build.**
No rerun, product import, owner/database operation or installation was performed
by the reviewer. This establishes compiled auxiliary artifacts, not mathematical
acceptance, semantic controls, useful reuse, growth acceleration or full v5.

Run: `experiments/v5-local-checks/demand-frontier-build01`.

| Evidence | SHA-256 |
|---|---|
| selection.json | `ea004555402e276fa7f06e2afb680cb9edbfa14ed8afc26992d18f7861e5a538` |
| RESULT.json | `db5fc91c1d154923a5300235d6a012ce7faffedca78e6903e222e0dffd734b3a` |
| native/BUILD.json | `afeb2fb9e3af2c4d9d86154bafe1c1b594bffc67fe06aacb34ed43e81bded001` |

The saved outer selection is byte-identical to the reviewed selection. All nine
source snapshot hashes match. Both staged and snapshot copies of all four Lean
sources match the BUILD source pins and prior source review. All 20 emitted
artifact lengths and hashes match BUILD, totaling 3,319,784 bytes. The exact
source/artifact file censuses are four and twenty, with no missing or extra files.
The recorded four per-command results match BUILD and each exits zero in the
selected dependency order: OwnerConstruction, PortableOwnerConstructCommand,
PortableConstructExportCommand, PortableContributionExportCommand.

Actual stdout records these four compilations and the final
FOUR_AUTHORING_HELPERS_COMPILED_NOT_TESTED_OR_INSTALLED status. Stderr is empty.
The outer result reports child exit zero, child reaped, Job closed, zero active
processes and no cleanup errors or termination request. Its selected limits are
120 wall seconds, 90 aggregate Job CPU seconds, 1536 MiB, four active processes
and 1 MiB per stream. Ten total processes over the run do not exceed the bound
of four simultaneously active processes.

Measured outer wall time is 6.2117749 seconds. Job CPU is 5.375 seconds and outer
wrapper CPU is separately 0.515625 seconds; the nested supervision CPU field is
not added again. Peak Job private commitment is 885,776,384 bytes. stdout/stderr
are 389/0 bytes. Native BUILD wall time is 5.497397 seconds and is contained in,
not added to, outer wall time.

The original PROFILE and INSTALLATION were independently rehashed and remain
`60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b`
and `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
The selected build performs no receiver compilations, owner opens or package
changes. Output artifacts remain unused pending root's exact file-only assembly
selection and separate control evidence. No old anchor migration follows.

One reviewer-only read/hash command initially concatenated two source paths
incorrectly in PowerShell; it wrote no files and ran no product code. A corrected
bounded read checked all eight source copies and all nine snapshot pins, with
zero mismatches. This command error is not a build failure or an artifact repair.
