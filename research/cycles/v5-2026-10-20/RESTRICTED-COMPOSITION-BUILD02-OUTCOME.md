# RC native build02: independent actual outcome

2026-10-21, core_release. One read-only terminal audit; no compilation, control,
guest, proof or network execution was performed by this audit.

## Disposition

**PASS_RC_THREE_COMPILES_ONLY, independently corroborated.** The corrected RC
core and aggregate libraries and the explicit native controls executable were
built successfully from the selected15-file closure. All three actual compiler
commands exited0 and the owned Job closed cleanly. The executable has not been
run by this build; compilation is not mathematical or receipt acceptance.
Failed01 remains preserved and is not relabeled or refunded.

| Record under experiments/v5-local-checks | SHA-256 |
|---|---|
| restricted-composition-build-02-selection.json | `659c780e902b69cfb039b854abae05d6a570c389f463dc8bfc6fff9bfa455244` |
| restricted-composition-build-02/RESULT.json | `24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd` |
| restricted-composition-build-02-attempt.json | `cd176fb134beaa59ad5d4289083be72ba92fdb956ef8dc231196d4fab1ccfdc9` |
| restricted-composition-build-02/source-map.json | `32e95e4b67377ac2f8b6cf1b7087a006c675c15db98f954415ab996f7393ac04` |
| restricted-composition-build-02/compile-commands.json | `50460299a3ccabae56d4ec83173c31c360d19003951d972fbc052b079825359a` |
| restricted-composition-build-02/rc-native-compile-job.json | `70b374cb8f2c3888344def99edb1ecc7c913c8b54504d28f43be81ef8671e3b3` |

Independent read/hash checks matched each of the15 canonical source files and
each saved snapshot file to the selected byte size/SHA. The snapshot has exactly
15files; external selection, saved selection and source map agree. All174 retained
compiler/runtime pins match. The original retained compiler recipe was the
same one independently hash-checked in the immediately preceding failure audit.

Each actual argv was checked against its own command.json and the saved compile
plan, then independently derived from the retained aggregate recipe. The three
exact roots are lib02.rs, aggregate_lib.rs and controls_root02.rs. Distinct02
metadata, retained module/serde externs, new-run library search and explicit RC
core/aggregate edges match the reviewed builder. The third compile has fat LTO,
not `--test`; no command launches the resulting binary. There is no Cargo,
dependency/checker rebuild or optional extra command.

All six log hashes/sizes match. Only the controls compile emitted stderr:
3,548bytes, SHA `31b9d6c2d6576ec47709b4127b2b0e8a2e1f54c86cf18fb533c9a137574da4ee`.
It contains nine dead-code warnings from the source-identical private units
included for boundary tests, not errors. The production libraries compiled
without diagnostics. The warnings do not establish that production paths omit
those checks: real positive/graph controls link the separately compiled libraries.

## Exact outputs

All output sizes/digests were independently checked against RESULT:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| libdmkn_rc_relation.rlib |1719004| `1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b` |
| libdmkn_aggregate_relation.rlib |1050594| `be8bdcb4c815e5c610145e5fea28a6d6601fe8dd9ae8cd04f3bf35c5b9dbcbba` |
| restricted_controls.exe |2570240| `9711910d7c0a32a08df3233bad2416fe0a88a89dae392e4fe71986e95b83e559` |

The finalized attempt binds the exact successful RESULT, whose selection digest
matches the external selection. No FINALIZATION-FAILED override exists.

## Accounting and closure

Per-command inclusive Job CPU is6.84375,2.609375 and47.34375seconds, summing to
the final56.796875seconds without double counting. The disjoint controller uses
2.171875seconds: known measured CPU is58.96875seconds. Total recorded elapsed
time is64.69191950000823seconds. The documented final report/exit tail remains
excluded; these build costs are not checker/guest economics measurements.

The final Job and closure record agree: zero active processes, zero limit
terminations, empty cleanup errors and `closed:true`. The only selected explicit
cleanup is the exact pinned owned VCTIP telemetry process, with exit observed;
no unrelated user application was stopped. Peak Job private commit is
758,042,624bytes. The sampled output census is5,500,376bytes/69entries. Its
same-run INetCache alias is reported/pruned from traversal, not followed outside
the run. Neither this sampled census nor the Job is a hostile-input sandbox.

## Next boundary

Root can now separately select the reviewed one-shot40-case/26-refusal native
controls. Their actual result must establish same-J original-W correspondence
and the selected composition boundaries before a guest build is adopted.
This build alone establishes no guest image, execution saving, certificate,
receiver adoption, useful-growth result or final-v5 release. Source-only matched
wire preparation and one snapshot-host relink adapter can proceed without
repeating this passing build or expanding into a public producer campaign.
