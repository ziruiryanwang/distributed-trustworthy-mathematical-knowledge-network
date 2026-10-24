# Current ordinary distribution source build

This source-only implementation builds the current ordinary package from 67
fixed repository source/assets plus this builder and `source-map.json`. It
does not need an existing installation, experiment output, selection file or
owner database. It has not yet been executed or qualified. A completed build
would establish assembly only; mathematical use and release adoption remain
separate decisions.

Supply complete supported Windows x86-64 Python 3.14.6 and Lean 4.34.0
distributions. Invoke the selected Python with `-I -S -B`, using absolute paths
and a fresh output whose parent exists. For example, in PowerShell:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_distribution\build.py' `
  --source-root 'C:\commons-source' `
  --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\lean-4.34.0-windows' `
  --output 'C:\commons-builds\current-01' `
  --wall-seconds 600 --cpu-seconds 600 --memory-mib 2048
```

The example allowance is an explicit caller choice, not a measured requirement
or a promise that the build fits it. Allowed ranges are 120–3600 wall seconds,
100–3600 aggregate CPU seconds and 256–8192 MiB. Compilation is sequential.
There is no automatic retry, allowance increase or memory tuning. Failure leaves
partial output and logs for inspection; choose new storage for a separately
authorized new attempt.

One original allowance includes source/runtime verification, snapshotting,
the unchanged base builder, fresh extractor compilation, final copies and
verification. Both child grants come from the remaining allowance. Before each
child, the controller reserves 25 wall seconds for cleanup/final work and 62
CPU seconds for the existing supervisor's at-most-60 controller CPU seconds
plus final work. The base builder receives a smaller inner allowance. Unused
reserve remains within the original allowance. Insufficient remainder refuses
launch. Complete child Job CPU is charged once; nested native totals are not
added again. Missing final CPU accounting charges the full child grant and
stops. Clean closure of both base and native Jobs is required, including the
base builder's nested compiler Job. The cooperative controller checks its own
CPU and wall use; an enclosing owner Job is recommended for hard containment
of that controller too. Existing supervisor limits are sampled, not a hard
disk quota or hostile-source sandbox.

The three stages are:

1. Snapshot the selected files and run the unchanged pinned
   `ordinary_package/build.py` using only that source snapshot. It compiles
   eight receiver modules and thirteen authoring modules, and generates the
   installed manifest through unchanged `ordinary_installation.py`.
2. Build six legacy-view modules from fresh source, generate C, compile every
   object with `leanc -c -O0`, and link `MissingImportExporter.exe`. The native
   lane does not use previous object or interface files. The existing exact
   `public_source` and `legacy_view` transformations are checked against their
   selected transformed hashes.
3. Assemble the exact current map directly: 51 source/asset copies, 74 newly
   generated native artifacts, and the newly generated installed manifest.
   Verify all 126 payloads, all source/runtime pins and the actual support
   digests. Write the additional 98-entry auxiliary `PROFILE.json` last.

Successful output has this layout:

```text
current-01/
  package/             Runtime package: 126 payloads plus PROFILE.json
  _build/              Input snapshot, intermediate base/native builds and logs
    BUILD-RESULT.json  Actual profile hash, installed manifest hash and implementation ID
```

Relocate only `package/`; `_build/` and the source checkout are not runtime
dependencies. Keep complete external runtime distributions available at explicit
runtime roots when using the package. The emitted profile and installation
manifest contain logical names and actual hashes; they do not embed source or
build paths. Build receipts retain those paths for provenance. Compiled bytes
and therefore implementation identity may differ from earlier builds. Do not
reuse old owner state merely because its source version looks similar.

`source-map.json` is the versioned input map: all 67 source hashes, the base's
47 inputs, 51 destination-to-source records, three ordered compilation lanes,
transform hashes, output counts and extra native compiler pins. The fixed base
builder also pins the supported Python/Lean runtime files. These named checks
are not a complete hermetic toolchain census: Lean headers, installed libraries,
compiler/system dependencies and immutable owner storage remain premises.
Native C compiler tools are needed to build from source; ordinary use of a
qualified prebuilt package need not install that compiler toolset separately.

Module03 and worker03 are exact source copies; the build does not export a
module or check an old theorem. No foundation, semantic checker, owner state,
network behavior, certificate policy, license or publication decision changes.
The next useful validation is one separately selected clean-source build and
relocated public-use check under its newly derived identity.
