# One native exporter build, then decide actual export separately

Root, 2026-10-22. The real participant workflow is ordinary project publication
and checked incremental reuse. The failed source frontends have not produced a
real closure. Their failure does not justify another certificate or a larger
memory budget.

The next consequential question is whether one actual producer proof environment
fits the existing envelope when helper/compiler code is native, rather than also
represented as a large imported declaration environment. Source inspection of
the installed compiler supports this distinction: generated C calls module
initializers for code; it does not call `importModules` for its helper closure.
The new entrypoint will explicitly import only the retained producer module.
There is no measured memory benefit yet.

Select one native **build only** after combined source review: OriginalExpr,
OriginalDecl, CheckedExtension, BootstrapSupport, OrdinaryExport and a tiny
NativeOwnerExporter. Use `lean -c` for custom module code generation, `leanc -c
-O0` for their objects, and `leanc -leanshared` for one executable. No upstream
Lean/Std code or mathematical fixture is rebuilt. Code generation is a new build
boundary, not repetition of the passed codec/admission suites.

Build scope: 120 CPU seconds, 180 wall seconds, 1536 MiB and six simultaneous
processes, fresh immutable native-export-build01. Runtime/compiler and relevant
shared import-library pins are explicit but not a hermetic build proof. Direct
logs retain build failures. Preserved source source-identity checks cover the
five reused helper modules. Build success alone cannot authorize mathematics.

Only after reviewing actual successful build output may root select an actual
native export within the original 120 CPU / 180 wall / 1536 MiB envelope. It must
use the same real ReadFootprint artifact and inventory, keep actual proof records,
emit import/index/closure/write phase markers, and produce inert claims only.
No native admission is permitted without that real bounded closure.

Stop this route if the single producer import itself is infeasible under the
envelope. Do not renew allowances or repeat the same frontend. A later redesign
would need a genuinely different selected-evidence acquisition boundary.

In parallel, root read/adopts OWNER-REBIND-PLAN's distinction between warranted
theorem interfaces and authoring views. Proof-value equality is unnecessary for
using an already accepted opaque theorem. Exact propositions and dependency
meanings remain mandatory; definitions need their computational semantics. A
downstream export must stop at actual accepted symbol IDs, and final independent
admission still checks new proofs. This changes no live acceptance policy yet.

No public deployment, stable public profile, growth benefit or v5 completion is
claimed by either source selection.
