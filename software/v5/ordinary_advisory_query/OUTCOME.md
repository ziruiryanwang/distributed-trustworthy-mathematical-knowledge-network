# Saved-outcome audit: advisory symbol queries

2026-10-28. **PASS for the selected advisory projection, package delta and inert
search handoff.** This audit read saved files only. It did not open protected
owner state, rerun controls, execute a query, start a service/find, invoke native
checking or change Git state. Full deployable v5 remains unfinished.

## Evidence and observed result

All experiment paths below are relative to `experiments/v5-local-checks/`.

| Saved artifact | SHA-256 |
|---|---|
| advisory-query-controls01/RESULT.json | `f24884527b39694257e3c8bde22bee2ced3c6ac56e733a25e24b9d3a14a6ca77` |
| advisory-query-controls01/controls/RESULT.json | `64c75e1ff19b150dcd38d4d0c6cd319a8b0257fb10bd61deec4a10711ad89be7` |
| advisory-query-assembly01/RESULT.json | `37422e8b773a077352d5755897080773e3611f01325db4d28b749cdd451fe9eb` |
| advisory-query-assembly01/distribution/ASSEMBLY.json | `556335ad043d995d0c5621a552b531ae9a95ea82a9d2752c7ae228227d109006` |
| advisory-query-positive-launch01/RUN.json | `4d7c9c65591e1071796f0899c4ab1ffc0e2b1be4f89652f67d1ac6fdd91459de` |
| advisory-query-positive-launch01/SUPERVISION.json | `a7261816417882d25494acdd74af0623468336d2b076e119b4247d051b9917db` |
| advisory-query-positive-launch01/child/stdout.txt | `f47ddc83c4da6b1e50a565b952e7c343d584d70ff36f04de1bb6f7af81f909d8` |
| advisory-query-positive01/RESULT.json | `b7f0507a91ad36eb80e0885b2a1adcbc47d281f2e6f7acb528a32593a7393c20` |
| advisory-query-positive-prepared01/RECEIPT.json | `50cdfdb2b99069d0ea2860747fc5fe9d4ae7226254673c5959f8299e5cdf93b3` |
| advisory-query-find-prepared01/RECEIPT.json | `660f5cca67836165de9c665d8ae777c8a4205eacf13b30ccd0afd214fe1c7123` |

Controls01 used selection `07e5a9439ba7d83e4abef68c21f501e1eb2baf379dc99482fe2c6690a3b8e07b`
and returned all four planned groups. Actual base native/import metadata validators
accepted the synthetic missing-snapshot advisory route, retained bad metadata,
audit and source-record refusals, and did not mark skipped snapshots verified.
The remaining groups exercised partial missing names, close failure and forbidden
custody/mixed inputs. Opening/SQL/activation were explicitly inert doubles. This
is not an actual imported-owner or mathematical-acceptance experiment. The control
author's expectations had the separate source review `3f875da3…` before execution.

Assembly01 used selection `60c4a4c23fdfc1604b17d26522dbf20a2947394751b415dcf7364ac419613ef4`.
The saved package has exactly **155 files**. This audit rehashed all 155 against
the assembly receipt. Relative to the selected original build receipt there are
five changed files (`LAUNCHER.md`, `PROFILE.json`, `profile.py`, `query.py`,
`run.py`), one added `advisory_context.py`, and 149 unchanged files. No installed
core or native payload changes appear in this delta.

The assembled PROFILE is
`135c182496294cb99d8553031b02c6ac19937848960e0711bedd5fe7e72ed828`.
The installation manifest remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`,
with implementation
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
Assembly is file-only, with zero native calls and no owner opening.

## Actual query and unchanged search input

The public launcher executed one `query.py` operation at B's existing root
`1b8761f807bba6c5ebe628636621a556e4271b955cc6cd3e836b9a5c5bc728ee`.
Its arguments contain catalog/store/root and symbol names, with no custody or
custody-limit arguments. The child returned `ok:true`,
`operation:prepare-symbol-query`, `query_kind:symbol-neighborhood`,
`owner_closure:CLOSED`, `custody_closure:NOT_OPENED`,
`snapshot_integrity:NOT_CHECKED`, `context_readiness:NOT_ASSERTED` and
`mathematical_acceptance:false`. Its final marker and stdout payload are identical
apart from the actual one-byte terminal LF.

The familiar Context name resolves to portable symbol
`cdc95dcc0dd80a749a1dab05a8c7af427e3b59f11aab8f6e20e70f2e9ef7f6c5`.
Its feature is
`f8ffc2e202594d6dd0d1fcb3ebae0e9df06117f766d04eedf72b0fd6eb28ff3b`.
Direct saved-byte comparison with `symbol-query-positive01` confirms identical
`BINDINGS.json`, `SYMBOL-NAMES.json` and `SPECS.json`; parsed context identities,
namespace, features and binding/name hashes also match exactly. The advisory
status changes are explicit and do not relabel the earlier query report.

Both inert preparations have matching file/input hashes and record zero commands,
no protected state opening and no mathematical acceptance. The new find preparer
consumed the actual new final report. Its 654-byte `config.json` is byte-identical
to `symbol-query-find-prepared01/config.json`, SHA-256
`463c3aee55ded3338098dca9f092b6532cd05c501f412deda3db601c6cb758f9`.
The configured `advisory-query-unexecuted-find01` output is absent. This campaign
therefore establishes the preparation handoff, not another executed search.

## Integrity, closure and costs

The saved control/assembly selection hashes match their outer reports. All 28
selected source/snapshot hash checks match, as do the control's 11 loaded-source
pins, both preparation receipts' selected inputs/outputs and the 155 package
pins. Control and assembly stdout exactly equal their saved payload plus CRLF;
query stdout equals its final payload plus LF. The reviewed helper and caller
remain at `58e20183…` and `8a5cbfeb…` respectively.

All three supervised operations exited zero, reaped their direct child, closed
their Job, ended with zero active processes, no cleanup errors and no requested
termination. Their stderr files are empty. The initial `LAUNCH.json` is the
pre-launch marker; the terminal `RUN.json` and supervision establish completion.

| Operation | Outer wall seconds | Known CPU seconds |
|---|---:|---:|
| Four control groups | 0.4934751 | 0.390625 |
| File-only assembly | 4.3795304 | 1.781250 |
| Actual advisory query | 1.5903415 | 1.453125 |
| Total | **6.4633470** | **3.625000** |

Known CPU is each outer wrapper's reported total plus its final child-Job CPU.
Inner controller and nested supervision figures are not added again. Inert
preparations, reasoning, source authoring and this audit are unmetered and are
excluded. These figures are operational costs, not a controlled speed comparison.

The source argument and synthetic missing-file controls support removal of the
generated-snapshot read path. The actual query has no per-file I/O telemetry;
its wall time does **not** independently measure snapshot bytes saved. Local
metadata hydration, imported metadata audits and package/runtime verification
remain. No global search completeness, useful-growth speedup, large-network
latency, independent hosting or final-v5 release claim follows from this pass.
