# Single ordinary Std export: independent saved-outcome audit

2026-10-26. Reviewer: `current_acceptance_challenge`.

**Disposition: FAILED public baseline production, with successful bounded native
extraction and clean closure.** The one selected `std-export01` operation did not
produce a complete consumable bundle. Do not adopt its partial files as a library,
retry the operation, raise limits, or infer mathematical acceptance. This audit
performed only saved-file/source reads, hashes and a bounded output census: no
product import, binder execution, native command, state access or repeated test.

## Selection and unchanged inputs

The frozen allocation is
`experiments/v5-local-checks/std-export01.selection.json`, 44,371 bytes, SHA-256
`77c077d4f97856d9db5da99e3f56bc9f653e165a23c49a3075c11d2728618227`.
Its actual RESULT binds that same hash. All **176 external pins and six saved
source snapshots** were independently rehashed after completion: zero mismatches.
This includes the complete 154-file installed package, selected runtime files and
target-module companion pins. The prior allocation review remains the source of
the prospective envelope; it was selected before this first operation, not raised
after failure.

The actual command is the installed public `run.py owner -- produce-baseline`
with explicit approved project selection, fresh diagnostics/output and 144-MiB
spool authorization. Saved project/request bytes select installed
`Std.Data.HashMap.Lemmas` and exactly `Std.HashMap.isEmpty_insert`, with the real
installed `lib/lean` root. There is no state argument or automatic intake.

The profile is
`ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67`;
installation manifest is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The actual installed native exporter is 809,472 bytes, SHA-256
`fe2ba97bb77794a7583ab328f1b9b14d7406ea21b31be3f1fada21e87e30a287`.
It is not interchangeable with an older historical exporter binary. These pins
establish selected byte identity, not transitive toolchain hermeticity or truth.

## Actual terminal outcome and accounting

All report paths below are relative to
`experiments/v5-local-checks/std-export01/`.

| Report layer | Terminal status | Measured wall seconds | Inclusive subtree CPU seconds | Peak Job private commit bytes |
|---|---|---:|---:|---:|
| Outer `RESULT.json` | `COMMAND_FAILED`, exit 1 | 117.4110786002 whole operation; 116.909900 through command cleanup | 87.953125 | 919,453,696 |
| Public `public-launch/SUPERVISION.json` | `COMMAND_FAILED`, exit 1 | 116.2981706001 through cleanup | 87.218750 | 900,796,416 |
| Native `bundle/supervision-result.json` | `COMMAND_EXITED_ZERO_AND_CLOSED`, exit 0 | 29.6120984000 through cleanup | 18.421875 | 869,711,872 |

Each of these three supervision reports records direct child reaped, Job closed,
zero final active processes, zero terminated processes, no termination request
and no cleanup errors. Their cumulative process counts (8, 6 and 4) are not
simultaneous active counts and do not diagnose a process-limit refusal.

Known whole-operation CPU is **89.078125 seconds**: outer inclusive Job 87.953125
plus outer runner 1.125. Do not add the nested Job measurements or their wrappers
again. Owner-reported cost is 68.718750 controller CPU plus 18.421875 worker CPU,
with 116.0600377000 wall seconds. Public RUN reports 0.687500 wrapper CPU and
116.3005336002 seconds through its report; these are nested observations, not
additional whole-operation charges. No finer phase CPU breakdown was saved.

The outer prospective limits were 150 wall / 110 inclusive CPU seconds / 1792 MiB
and four active processes. Public child limits were 120 wall / 90 inclusive CPU
seconds / 1536 MiB and three active processes. The internal native grant was
90 wall / 86 CPU seconds / 1536 MiB and four active processes, still constrained
by the enclosing Jobs. Stream and spool reservations were unchanged. None of
these reports identifies a forced process, memory or stream-limit termination.

Public RUN correctly says `ok:false`,
`OPERATION_INTERRUPTED_OR_UNSUCCESSFUL`, mathematical disposition `NOT_INTERPRETED`.
Owner stdout reports `BASELINE_PRODUCTION_WRITE_EVIDENCE: ADMISSION_OPERATION_BUDGET`,
`accepted:null`, `mathematical_acceptance:false`. Saved FAILURE records:

- Phase `WRITE_EVIDENCE`; `CatalogError / ADMISSION_OPERATION_BUDGET`.
- Native entered, accounting complete and closure known; actual native CPU
  18.421875 seconds, equal to its charged amount, not the 86-second grant.
- `manifest_write_attempted:false`, `manifest_may_exist:false`.
- Preserve outputs; no automatic retry or rollback inferred.

This is a **cooperative operation-budget refusal**. The installed
`OperationBudget.check` uses the same error for either its wall deadline or
controller-plus-worker CPU condition. The saved error does not distinguish those
branches; this audit does not label it specifically CPU exhaustion. In particular,
the reported owner CPU sum is 87.140625 seconds, below the public 90-second cap.

## What native extraction and the partial files establish

The approved exporter diagnostic records import completion, then:

- Source index: 39,939 records and 1,233 grouping records.
- Selected export: 2,651 units, 16,226 edges, 1,102,333 scanned nodes and
  38,094,420 unit bytes.
- Writer output: 38,154,768 bytes.

The saved writer's actual length independently matches the reported output size;
its SHA-256 is
`5a2f721127cfef3ae39613c1ec723b2f710cc410c872650fb2acfd7d04078b7a`.
The internal closure counts above are **native diagnostics**, not an independent
decode or mathematical check of every writer entry. The audit deliberately did
not parse the full nested 38-MB writer or rerun binding merely to certify failure.

Installed producer source sets `WRITE_EVIDENCE` only after `bind_writer` returns;
it then writes and reads back per-unit files. `FINALIZE_INPUTS`, the pre-manifest
PRODUCTION observation and manifest-last publication follow later. Thus the saved
phase supports that binding returned in this invocation, but does not establish
that final evidence, final input checks or the publishable manifest completed.

The independent recursive file census finds **718 bundle files / 45,373,288 bytes**:
708 files directly in `units/`, totaling **6,389,257 bytes**, maximum 67,391 bytes;
the other ten are the writer, input/inventory/selection/failure/supervision records
and three supervision files. `manifest.json` and `PRODUCTION.json` are actually
absent. All 708 unit filenames have the expected 64-lowercase-hex plus `.json`
shape and none is a reparse-point file. This is a partial census, not a complete
2651-unit export, recipient reconstruction or filename-to-semantic-ID proof.

All 708 partial unit files were independently hashed. For a compact reproducible
census commitment, sort these names in ascending order and concatenate UTF-8
rows `filename<TAB>decimal-byte-length<TAB>lowercase-raw-SHA256<LF>`, with no BOM.
The resulting SHA-256 is
`20ceedff36118ce3b0ea20c47385ec33bc53610cc94b62c3fd132a5a68a98100`.
The commitment records the inspected partial bytes without creating another copy.

## Practical conclusion and next decision boundary

The current approved native path can extract this actual Std target within its
bounded grant. **The full installed producer is not yet practically qualified
for that target under the selected operation envelope:** it stopped before a
complete inert bundle existed. The large total controller cost, post-native failure
phase and partial evidence output justify examining binding/materialization and the intended
ordinary-library reuse boundary before selecting more runtime. They do not prove
a particular asymptotic bottleneck or predict that larger allowances would help.

The 2,651-unit closure does not alone prove every recipient route impossible:
producer batching, recipient-relative missing-unit admission and cold exact-module
realization have different limits and prior-knowledge assumptions. See the
separately scoped source-only `RECIPIENT-BOUNDS.md`; no receive, merge, source
bridge, unknown-ID discovery, theory growth, full-cost benefit or deployment gate
was executed here. A standard-library theorem being extracted is not new
mathematical knowledge and is not mathematical acceptance by a fresh recipient.

The run is closed and charged. Keep all used sources, inputs, package bytes,
diagnostics and partial output frozen. Root owns the architectural decision and
any future separately selected work; this outcome authorizes no retry, intake,
new experiment or limit increase. Full v5 remains unfinished, local/unpublished.

## Saved evidence identities

SHA-256 values, relative to the run directory:

| File | SHA-256 |
|---|---|
| `RESULT.json` | `dacd8b434fe5a54e6084eb9be8d38bedbdf0b14f3ae3b8d2752287a0205b545d` |
| `public-launch/RUN.json` | `5a362a50badb3086555de4aa4252abee37eecbc75acf5eb66b2ad8e24d668078` |
| `public-launch/SUPERVISION.json` | `4951e46733032700684438971e95a5f9d84ebcb00aa4bab3e5e26725a16c5728` |
| `public-launch/child/stdout.txt` | `18241b34bebeadc1bfb167d6bf05eec9a63e507c73017a558a94970acecfc911` |
| `bundle/FAILURE.json` | `095ff3da1752fd0343edcda6e69d0338165f20e162a754c417081498168e7f48` |
| `bundle/supervision-result.json` | `bdb752bd8e92f2b751c26de466d8282f7889b0225b9e715573eb2672414da868` |
| `bundle/supervision/stderr.txt` | `e838767368809f42d7174ebdb699b2f46abdecd478548d0785bc4d1f131b4ea0` |
| `bundle/SELECTION.json` | `1c03b97a57fb5e313227250b4713dcb2c92063e1119ae2bfe77928b39c2581f2` |
| `bundle/inventory.json` | `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0` |
| `bundle/request.json` | `bcb647fa96824cc82aebda1dab151a88d678ca3d8756cd150e0103e9f41993bd` |

