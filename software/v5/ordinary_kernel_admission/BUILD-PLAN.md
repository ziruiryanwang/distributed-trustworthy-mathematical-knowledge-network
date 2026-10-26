# Finite receiver build, source only

This implements the already selected integration footprint; no runtime is selected
by this plan. The successor has exactly the existing eight receiver modules.
Root selects the reviewed three source successors, this builder, existing file
helpers and existing supervisor through `tools/Run-V5-Check.py`. No new selector,
product loader, owner database, fixture or installation assembly is involved.

The build snapshots these sources into `native/lean-src` and creates
`native/lean-lib` under one fresh local-check output:

| Modules | Source | Object action |
|---|---|---|
| OriginalExpr, OriginalDecl, BootstrapSupport | Exact current receiver package | Copy pinned .olean |
| CheckedExtension, LocalSnapshot, OrdinaryWorkflowWorker | Selected successor snapshots | Compile |
| OrdinaryExport, BasisSnapshot | Exact current receiver package | Compile |

Compile order is CheckedExtension, LocalSnapshot, OrdinaryExport, BasisSnapshot,
OrdinaryWorkflowWorker. `OrdinaryExport` is the receiver copy, not the authoring
copy. `LEAN_PATH` names only the fresh object directory. The ordinary Lean runtime
library remains implicit in the pinned executable's sysroot. Inherited LEAN and
PYTHON variables and PATH are scrubbed; fixed Lean/Python bin paths are installed.
Compiler arguments retain the established `-DElab.async=false -R ... -o ...`.

## Selection inputs

The fixed predecessor package is
`experiments/v5-local-checks/intake-progress-package01/distribution/package`.
PROFILE SHA-256 is
`b850b12a96667b9a31984fe86fc0330517db9b5172bd6e63982782c10ee3ae47`;
INSTALLATION SHA-256 is
`a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb`.
The builder verifies both and checks their binding without loading the package.
It validates selected original source/object, supervisor and runtime bytes against
INSTALLATION, which remains externally pinned selection rather than peer input.

Root's existing local-check selection should snapshot these six sources:

- `tools/Run-V5-Check.py`.
- `software/v5/ordinary_kernel_admission/build.py`.
- The three successor Lean sources in that folder.
- `software/v5/ordinary_fair_search/assemble.py`, SHA-256
  `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`.

External pins cover the two manifests, five reused receiver sources, three reused
receiver objects, three installed supervisor sources, and nine named runtime
files from INSTALLATION. This is 22 external pins. Runtimes are `D:\Python314`
and `software/runtime/lean-4.34.0-windows`. The builder rechecks inputs after the
compiler closes; the outer runner independently rechecks its complete selection.
Changing any reviewed source before launch requires an updated exact selection.

The proposed invocation shape is:

```text
D:\Python314\python.exe -I -S -B
  {snapshot}/software/v5/ordinary_kernel_admission/build.py
  --source-root {snapshot}/software/v5/ordinary_kernel_admission
  --output {output}/native
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1024
```

Proposed outer limits: 240 wall seconds, 150 Job CPU seconds, 1280 MiB,
four processes, 1 MiB per log stream. The finite inner Job uses the remaining
original allowance, with 24 wall seconds and one CPU second reserved for cleanup
and recording. Five compiler calls are sequential because their imports depend
on earlier outputs; no fixture or expensive mathematical intake runs with them.
Root may select a smaller finite envelope after review. There is no automatic
retry, enlargement or continuation upon failure.

## Outputs and acceptance boundary

`INPUTS.json` preserves actual input paths/pins and compile order.
`SUPERVISION.json` and `compile/` retain command, logs, CPU and closure evidence.
`BUILD.json`, written last, gives the actual source/object map for all eight
modules, all emitted compiler companions and cost accounting. Emitted companions
are retained as build evidence; the later installation still selects only eight
`.olean` files. Every required object must exist, extra module names are refused,
each object/companion is at most 64 MiB and their total is at most 128 MiB.
These are validation bounds, not a hard disk quota; the cooperative compiler is
contained by the existing Job and outer process limits. Inputs and failed partial
outputs are preserved without deletion.

A build passes only with clean native closure, zero stderr, all eight expected
objects, unchanged copied prerequisites and unchanged source/runtime bindings.
Compilation establishes no mathematical acceptance or package adoption.

The separate control owner should use this exact fresh `native/lean-lib` tree
for `KernelAdmissionChecks.lean`; that fixture remains outside the eight-module
receiver layout. Focused native controls follow a separately reviewed selection.
Only after their actual audit should the existing `ordinary_installation.assemble`
primitive create a fresh implementation identity/package from these exact bytes.
The 117 auxiliary PROFILE file rows and authoring helpers remain unchanged;
PROFILE's installation binding changes. Old owner state stays frozen.
