# Native owner exporter: selected structural change

The existing `--run` worker loaded its helper/frontend environment and then the
private mathematical owner environment. The replacement current-environment
command also exhausted its fixed allowance before entering its export command.
Both failures remain preserved; neither is retried or assigned a larger cap.

`software/v5/ordinary_lean/NativeOwnerExporter.lean` instead executes compiled
helper code and constructs one private mathematical environment, dynamically
importing only `examples.ReadFootprint` and its dependencies. It does not load
helper `.olean` declarations into that environment. Installed Lean's C emitter
and `Leanc.lean` support this separation; native runtime initialization and the
owner environment still cost memory. There is no unmeasured fit or speed claim.

The controller-facing API is exactly:

```text
NativeOwnerExporter.exe <sysroot> <methodDir> <inventory> <output>
```

All four paths must be absolute. The controller must authenticate runtime,
executable/custom build closure, retained method artifacts and fixed inventory.
The source overwrites `searchPathRef` with runtime then method directory, passes
empty plugins and `loadExts := false`, requests `.private`, and requires the
actual target theorem record rather than an axiom-only public view. Flushed
markers distinguish import, indexing, closure export and final output phases.
Unchanged `Export.indexSource` and `Export.selected` enforce existing bounds.
Inventory parsing is bounded at 1 MiB, depth 64 and unsigned UInt64 tokens;
the complete unchanged inert bundle is bounded at 64 MiB and written exclusively
with `.writeNew`. Output is not a receiver warrant or mathematical acceptance.

The installed Windows toolchain has `lean.exe`, `leanc.exe`, clang, Lean headers
and upstream shared import libraries. The custom compiled closure, in order, is
`OriginalExpr`, `OriginalDecl`, `CheckedExtension`, `BootstrapSupport`,
`OrdinaryExport`, `NativeOwnerExporter`. All six C/object outputs must be linked;
linking main alone leaves custom symbols/initializers unresolved. Parent owns
the exact bounded build selection and runner, using the supported shape:

```text
lean -R snapshot -o build/M.olean -c build/M.c snapshot/M.lean
leanc -c -O0 build/M.c -o build/M.o
leanc -leanshared <six object files> -o NativeOwnerExporter.exe
```

The runner must control `LEAN_PATH`, `LEAN_SYSROOT` and `LEAN_CC`, and supply the
pinned Lean bin directory for runtime DLL discovery, without changing global
user environment. No method re-elaboration, upstream rebuild, certificate,
receiver admission or catalog mutation is selected here. This checkpoint records
source rationale only; build and actual export are separately selected actions.
