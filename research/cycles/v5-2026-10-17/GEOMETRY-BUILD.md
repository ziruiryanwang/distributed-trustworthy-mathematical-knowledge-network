# Fixed-po17 snapshot: one-link build contract

**Current prospective build02 amendment:** after build01 deferred before any
process started, root selects the evidence-backed compiler-only1,536MiB cap in
GEOMETRY-COMPILE-ENVELOPE. Builder SHA is now
`46be079429687e7ada877859111cf5b58d2bab1c6c0c6665146b487f3f8df1c7`;
only its declared memory limit and actual Job constructor change. All other
fields, inputs, code and240CPU/300wall limits below remain. The matching
adopter changes its memory-limit literal only. Fresh selection is
`f245889a729ff61726347cfad7673af1801a5e8104cd71f6d8c112af185d2b7c`.
The original2GiB plan below is preserved history, not current launch authority.
GEOMETRY-RUNTIME records exact selection/outcomes. No proof limit changes.

2026-10-17, `v5_growth_decision`. Source implementation only, selected by
GEOMETRY-SELECTION. Canonical root guard passed. No imports, tests, compilation,
host/guest/proof execution or Git operations were performed.

Owned source: `software/v5/aggregate_geometry/build_snapshot.py`.
Current source is21,908 bytes, SHA-256
`d9ae9e237b7c191ece8d7862b116b56f372863e7dea68579eef8426dc043eaf6`.
Independent changed-boundary review is pending; root owns any exact launch.

## Scope

Exactly one `rustc` snapshot-host link. Reuse the already compiled corrected
RV32IM/zkVM/module-relation/aggregate-relation libraries. No Cargo, build scripts,
backend/native-circuit/relation/checker/guest rebuild, stage-host link or produced
executable invocation. The retained build and source bytes remain untouched.

The source reuses the already reviewed pinned build-helper chain from
`modules/native/proof_validation/control.py`, its existing phase controller,
file census and Windows Job implementation. It is trusted owner compilation,
not a security sandbox or reproducible-build theorem.

## Exact selector

The invocation is the pinned Python under `-I -S -B`, this source path, the
selection's absolute path and its independently supplied SHA-256. The builder
requires canonical cwd, no optimization and exact own-source location.

Selection has exactly:

```text
schema = DMKN_V5_GEOMETRY17_SNAPSHOT_HOST_BUILD_V1
name = geometry17-snapshot-host-build-NN
authorizes_compile_only = true
sources = three relative-path -> {bytes,sha256} entries below
runtime_pins = exact retained allocation-build01 selection's 1071-entry map
limits = exact limits below
```

The three sources are:

- `software/v5/aggregate_geometry/build_snapshot.py`.
- `software/v5/aggregate_geometry/aggregate_host.rs`, root-owned20,765-byte
  source, SHA `7f3fefab48c30ec414a54620391f4be1ca8e27de19a6f61c7091614d148cf5c3`.
- Unchanged `software/v5/aggregate/receipt.rs`,3631 bytes,
  SHA `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`.

Four refined library pins are **separate derived inputs**, not additions to
`runtime_pins` or the source map. The1071-map remains exactly2,320,491,997 bytes.
All four libraries are rebound before preparation, before the link and after
closure. The large1071 map is checked before preparation and at finalization;
there is no redundant third scan immediately before the sole compiler call.

| Limit | Value |
|---|---:|
| Inclusive compiler Job CPU |240 seconds|
| Compiler wall |300 seconds|
| Compiler Job memory |2048 MiB|
| Compiler active processes |6|
| Ordinary controller / final controller ceiling |40 /60 CPU seconds|
| Total operation wall |420 seconds|
| Fresh output / entries |536870912 bytes /8192|
| Command log |1048576 bytes|

These are explicit selected ceilings, not predictions or capacity reservation.
Root must check contemporaneous physical/true-commit headroom before any launch.
External supervision must account startup and final-report/exit tails excluded
by the builder's pre-final-report observations. No automatic retry is provided.

## Exact retained build and recipe

The builder binds seven immutable records under
`experiments/v5-local-checks/prover-allocation-build-01` and its two sibling
selection/attempt files. Their exact SHA-256 values are in `RECORDS`; it checks
the genuine successful five-step result, exact command sequence, clean command
closure, successful attempt binding and absence of a finalization-failure
override. Source-map and INPUT-MAP records anchor the already adopted prior
build; the builder does not rerun the old build or reread all180 source copies.

Actual refined inputs, all in the retained `lib/` directory:

| Library | Bytes | SHA-256 |
|---|---:|---|
| RV32IM |14287894|`62938a59d418d1f86695251493c43f59d5e929348d5261e49189243368ebcf52`|
| zkVM |18767176|`665a628527cba32f556546258815b5e0d164d8f32e846c3eb4d37fce3b18cde2`|
| Module relation |4217778|`2148c9df54394ff683f6cea79e3ebdc8cd1f3b90acb98b03b2df2cf5a24da697`|
| Aggregate relation |916670|`247e3eda17a5f1c5e0e4cf1984f6974dcac44cce5f316d5fef5f3d2b55b4a225`|

Use the **last command** in the retained `compile-commands.json`. Change exactly
four argument values:

1. Crate `small_aggregate_stage_host` -> `geometry17_aggregate_host`.
2. Metadata `dmkn_auxwords_a53940b67580e215_small_aggregate_stage_host` ->
   `dmkn_geometry17_aggregate_host` (retaining the `metadata=` argument prefix).
3. Old stage-source argument -> fresh
   `RUN/source/software/v5/aggregate_geometry/aggregate_host.rs`.
4. Old stage executable output -> `RUN/geometry17_aggregate_host.exe`.

Keep the old corrected-library directory in `-L dependency=...`, all seven
`--extern` arguments, native libraries, linker and flags unchanged. Three
refined libraries are direct host `--extern` operands; RV32IM is the corrected
zkVM's transitive dependency. The old command DAG explicitly binds that fourth
edge, instead of pretending the host had four direct refined operands.

The new explicit compiler environment must equal the retained last-step
environment with only the old run-prefix changed to RUN. Preserve
`CARGO_NET_OFFLINE=true`, telemetry opt-out, bounded threads and all other
values. `p.environment` creates fresh environment directories and records tool
metadata; its resulting environment is checked against that exact derived map.
Nothing is inherited from the launching shell.

## Saved records and adoption grammar

Five principal adoption records remain `result`, `attempt`, `selection`,
`source_map`, `command`. The new `source-map.json` is the flat exact three-source
map. `compile-command.json` contains one flat argv array, not a five-step list.
The source files are retained under `RUN/source/<relative-path>`.

`INPUT-MAP.json` has exactly `sources`, `runtime_pins`, `refined_libraries`,
`records`, `helper_pins`, `trust_boundary`. The records map is the seven exact
RECORDS entries; helpers are the existing pinned build ecosystem and cl/link/rc
metadata binaries. No old source map is misrepresented as fresh source bytes.

`environment-profile.json` has the existing helper's metadata fields:
`cargo_jobs`, `environment_keys_only`, `explicit_environment`, `host_binaries`,
`include_directories`, `library_directories`, `no_inherited_environment`,
`rayon_threads`. No `step_environments` field is needed for one command.

Successful RESULT schema/status are
`DMKN_V5_GEOMETRY17_SNAPSHOT_HOST_BUILD_RESULT_V1` /
`PASS_GEOMETRY17_SNAPSHOT_HOST_ONE_LINK_ONLY`. Its exact field set is:

```text
schema,status,selection_sha256,limits,
retained_result_sha256,retained_commands_sha256,
retained_environment_sha256,retained_selection_sha256,
runtime_pin_count,runtime_pin_bytes,refined_libraries,
backend_rust_crate_rebuilds,relation_rust_crate_rebuilds,
snapshot_host_links,stage_host_links,checker_rebuilds,
native_circuit_rebuilds,guest_rebuilds,host_calls,guest_calls,
proof_calls,network_calls,authority,source_map_sha256,commands_sha256,
environment_sha256,input_map_sha256,executable,job,commands,
controller_cpu_seconds,wall_seconds,output_census,sampled_peaks,accounting
```

Only `snapshot_host_links` is1. Other counters are0. Authority is
`SNAPSHOT_HOST_ONE_LINK_ONLY_NOT_MATHEMATICAL_ADMISSION`.
`commands` contains the actual one-command closed phase report; the command
label is `geometry17-aggregate-snapshot-host`. `job` is that phase's final Job
statistics, not a sum with the historical build. The exact executable pin and
all new record hashes are rebound after closure.

Failure adds explicit diagnostic fields and never matches the successful
adoption grammar. Finalization failure writes a separate overriding sentinel;
the adopter must reject that sentinel even if an earlier result/attempt says
PASS. Fresh run and attempt paths are required, with no overwrite or fallback.

The layout author has received this shared contract. Their new adoption boundary
must recognize the genuine one-link schema directly, not call the old five-step
stage-owner constructor or impersonate the old build result. Neither successful
compilation nor adoption authorizes executing the snapshot host. The separately
reviewed fixed17 layout is the next finite root decision.
