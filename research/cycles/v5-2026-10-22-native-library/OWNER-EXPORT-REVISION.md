# Reuse the real producer environment instead of importing it twice

Root reports that owner-export01 terminated cleanly after an internal out-of-memory
panic at the unchanged 1,536 MiB process cap: 23.359375 known CPU seconds, peak
1,613,631,488 bytes, no bundle and no phase markers. The allocating phase is not
established. Preserve that failed snapshot and its evidence; do not rerun it,
raise RAM or modify its used worker source in place.

Root selects source-only `software/v5/ordinary_lean/OwnerExportCommand.lean`.
It imports `Lean.Elab.Command` and the existing `OrdinaryExport`, obtains the
current owner project's `getEnv`, then calls the same bounded `indexSource` and
`selected` functions. It never calls `importModules`, elaborates the existing
mathematical method again, starts another process, or changes acceptance rules.

This removes one explicit second environment construction from the producer
workflow. It does **not** establish a measured memory reduction: importing the
owner/compiler/helper closure and materializing selected units still costs memory.
Flushed markers distinguish entry, index completion, selected-export completion
and output completion before any further implementation change is justified.

## Private theorem bodies: exact Lean 4.34 source argument

- `Lean.Elab.Command`'s `MonadEnv` instance returns the current command state
  environment (`Command.lean:213–214`).
- `Environment.toKernelEnv` returns `env.checked.get` (`Environment.lean:649`),
  not a public-only declaration interface.
- A header **without `module`** selects `OLeanLevel.private`
  (`Elab/Import.lean:150–156`). `Environment.lean:2182` then sets `importAll`
  throughout the transitive import closure, independently of individual flags.
- Explicit `import all` is syntactically forbidden without `module`
  (`Parser/Module.lean:103`). With `module`, it does not automatically propagate
  through every ordinary transitive import: the same line2182 requires each
  imported edge's `importAll` unless global level is private.

Consequently the smallest correct driver for the already compiled legacy method
and complete Std proof records is a **legacy header with no `module`**:

```lean
import examples.ReadFootprint
import OwnerExportCommand

#ordinary_export DMKN.ReadFootprint.readsOnly_insertMany
  "<absolute controller-pinned inventory path>"
  "<absolute fresh output path>"
```

This is semantically the required all-private import, not a public axiom view.
The driver imports the retained compiled01 method artifact; it does not copy or
re-elaborate the method mathematics. The command requires the requested root's
actual kernel record to be `thmInfo`, then the existing closure exporter screens
all needed records. An incomplete public/axiom view must fail, not be accepted
as proof. The identifier denotes its exact original full native name; no search,
namespace guessing or intended-statement translation occurs.

## Trust and bounds

Only the owner-selected driver/runtime/import paths/artifacts and exact fixed
inventory are authorized. Root must pin them and run under the same finite outer
resource supervision. A normal source frontend loads its trusted import extension
state; this is an explicitly owner-controlled producer frontend, not a receiver
or a claim of hostile-source sandboxing. No peer source or binary may enter it.

Inventory input remains capped at 1 MiB and screened for bounded JSON depth and
unsigned integer tokens before parsing. The full output uses the existing inert
`DMKN_ORDINARY_EXPORT_BUNDLE_V1` shape and 64 MiB bound; exclusive `writeNew`
prevents overwrite. The same basis comparison, closure limits, original units
and subsequent controller canonicalization/receiver checks remain mandatory.

No runtime, compilation, method rerun or Git operation has been performed by
this source task. Root owns review, fresh selection and any actual execution.
