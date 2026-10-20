# Typed rows: four-target compile outcome

2026-10-20, `core_release`. **PASS: four changed targets compile; no tests or
mathematical admission yet.** Saved-evidence audit only, no compiler/run restart,
dependency rebuild, proof, broad runtime scan, RAM investigation or Git mutation.

## Selection and preflight correction

Fresh selection02 hashes to
`0eaf0bd562b1d501412e415394d4ce33acb2c20c44df028bca64bbdfa24846a3`.
Compared with original selection01, its only semantic change is the run name.
All 39 original and saved source files match selected size/hash, totaling 646,734
bytes. Saved selection and source map are semantically identical to selection02;
their JSON key order/serialization differs, so raw selection hashes differ.

The preserved first invocation is not a failed compiler: root reported
`PINNED_PYTHON` before run creation. Source places that gate before output/Job/
compiler creation, and neither `typed-rows-build-01/` nor its attempt file exists.
The required existing `D:\Python314\python.exe` and `python314.dll` independently
match their adopted hashes `03168c01...` and `fde89cdb...`. The correction changes
invocation identity/name, not selected compiler sources, checks or budgets.
That first controller's CPU was not separately measured; it is not zeroed out
or included in the successful02 accounting below.

## Actual build and closure

`typed-rows-build-02/RESULT.json` reports
`PASS_TYPED_ROWS_FOUR_COMPILES_ONLY`, authority `COMPILE_ONLY_NOT_ADMISSION`.
The four recorded rustc commands use fresh checker, module, aggregate and controls
roots; all project externs refer to fresh02 outputs, with retained dependency
libraries. No stale previous project rlib link occurs. Each command exited zero,
reports `COMMAND_COMPLETED`, has empty cleanup errors and zero active processes
afterward. Log hashes match. Compiler warnings are retained, not errors.

Final Job: 89.984375 CPU seconds, zero active processes, zero terminated
processes, ten total historical processes. Disjoint controller CPU is 1.875,
hence 91.859375 known CPU seconds; wall 55.23716570017859 seconds. Use the final
inclusive Job value, not a second addition of per-command CPU. Final-report and
process-exit tail are excluded as declared by the builder. No finalization-failed
marker or cleanup/final-check error exists; attempt marker binds the exact result.
Sampled output census is 22,019,680 working bytes / 105 entries. The reported
pruned OS-created alias is not traversed/deleted by this audit.

Tests/native/guest/proof/network calls are all zero. One checker and the three
other fresh targets compiled; external dependencies were not rebuilt. A compiled
test binary is not a passing test result or evidence of proof cost improvement.

## Independently verified output bytes

| Output | Bytes | SHA-256 |
|---|---:|---|
| `libnanoda_lib.rlib` | 12,157,952 | `45d8e9695998bf55de56b81514e2d6fc2b8216b470796ab358617baaee76292c` |
| `libdmkn_module_relation.rlib` | 5,568,974 | `3d84f087ed1d3e18a0d8e912843744e4abf1d252273d0c79bb598363fa64f9ef` |
| `libdmkn_aggregate_relation.rlib` | 910,912 | `a4c83cc45d7822e803186ddac71258afff9d135e3c6d889250c1c1dce20d0e97` |
| `typed_rows_tests.exe` | 2,677,248 | `83c27079595e36855c484be61d462810088fab7608eb2d1d598ac88c8b5d1c00` |

All paths above are under `experiments/v5-local-checks/typed-rows-build-02/`.

| Evidence | SHA-256 |
|---|---|
| `RESULT.json` | `add627e4fe4bdc102c79eeea745233d95cbfd56f48f58b118fe276adb6c00794` |
| `selection.json` | `b4da69c0b7b925415931f11adb31c690d2f0ae18f57eddc4b74fcbd44d57cb4` |
| `source-map.json` | `c0d929c6cea7d3b27744abd88ff6d2f29e899627033680db2b60772196df2e9d` |
| `compile-commands.json` | `2e681166de1bc29870cdd7f56fe2f82fca670825daa1aa8e52565282d534047f` |

Root may now make its separately reviewed finite eight-control selection. This
audit neither launches that operation nor releases/adopts a new receipt image.
