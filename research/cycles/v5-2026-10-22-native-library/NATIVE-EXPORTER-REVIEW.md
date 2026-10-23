# Native producer exporter: independent source review

Scope: the proposed installed-toolchain native producer route after command02
failed before observable export entry. This is not another memory investigation
or qualification of receiver acceptance. Root owns source selection, finite
build/execution and adoption. This reviewer has run no build or experiment and
has not edited implementation source or Git.

## Build adapters

Read complete `run_native_export_build.py` and
`select_native_export_build.py`. **No source blocker found in these adapters.**
The completed entrypoint review is recorded below; this build-adapter section
alone did not clear the entrypoint before that source became available.

The wrapper generates C and a local `.olean` for exactly six custom modules in
dependency order: OriginalExpr, OriginalDecl, CheckedExtension,
BootstrapSupport, OrdinaryExport and NativeOwnerExporter. It compiles those six
C files with installed `leanc -c -O0`, then links those objects with
`leanc -leanshared`. No Lean/Std source is rebuilt, no mathematical method is
re-elaborated, and the generated executable is not invoked by the build wrapper.
The first five helpers' source hashes are checked against previously reviewed
and used snapshots; code generation is a changed artifact boundary, not a repeat
of their old checks.

Installed `src/lean/Leanc.lean:36-43` explicitly recognizes and removes
`-leanshared`, selecting nonstatic upstream linker flags. Compiler/FFI obtains
the installed include/library directories; the wrapper removes inherited
LEAN/PYTHON settings and prefixes the installed executable directory. Generated
object arguments and output paths are passed as an argument vector, so the
canonical project's spaces do not require shell quoting. Actual C generation,
link success and symbol compatibility remain to be measured by the one selected
build, not inferred from this source review.

The selector authenticates the preserved prior selection, pins the selected
Python/Lean shared runtime, C compiler/linker and installed `.a` libraries, and
snapshots the exact six Lean sources and two adapters. Each observed selected
archive is within the inherited supervisor's per-file limit. It retains the
120 CPU-second, 180 wall-second and 1,536 MiB envelope, with six permitted active
processes for the compiler/linker child tree. A per-command 120-second timeout
does not renew that aggregate allowance. Direct exclusive logs survive outer
termination; failures prevent a BUILD-RESULT success record. Fresh paths do not
overwrite prior failures or compiled artifacts.

This is **explicit-pin owner-selected build evidence**, not a hermetic or
reproducible-toolchain proof: upstream headers, all imported runtime `.olean`
data, compiler configuration and operating-system dependencies are not fully
enumerated by the selector. The wrapper also retains ordinary compiler-related
environment variables outside its LEAN/PYTHON filter. These limits do not turn
trusted local build output into peer authority.

## Why this route changes the failed execution boundary

Installed `Lean/Compiler/LCNF/EmitC.lean:1007-1078,1084-1159` generates runtime
and imported-code initialization followed by the native `main` call. It does
not automatically re-elaborate the exporter source or reconstruct the exporter
modules' kernel declaration environment from `.olean` files. Executable code
initialization still has a cost; it is not zero-cost initialization or a claim
that every transitive initializer is inert.

Thus an entrypoint that imports only the selected mathematical module once,
with no source frontend or helper/compiler declaration import, has a concrete
source-level reason to avoid the failed private-all frontend boundary. The
selected method's private proof records and closure still must be loaded and
serialized. Any actual memory/CPU advantage remains unmeasured, and no source
argument guarantees that all arbitrary owner modules fit a small envelope.

| Reviewed adapter | SHA-256 |
|---|---|
| `run_native_export_build.py` | `b444f0f459d9b421053e9bd62c3186e2100a15a825458adfc1b76247f8afce19` |
| `select_native_export_build.py` | `013c9082aee6a009bed9363fb18b3d33ce92b0b487202228d3e88d67f6cfbe78` |

## Completed entrypoint review

Read complete `NativeOwnerExporter.lean` and `NATIVE-EXPORTER-ROUTE.md`.
**SOURCE_REVIEW_NO_BLOCKER_FOR_ONE_ROOT_SELECTED_BUILD.** The exact entrypoint
SHA-256 is
`b8506e25e6e324417c8bf47680349c7d1f4bb016185001d346870e01e04daaf1`.
The two adapter hashes above are unchanged at this final review. Actual export
requires a separately pinned and supervised execution selection after a
successful build; this review does not authorize that execution implicitly.

The entrypoint imports only OrdinaryExport as code. Native execution accepts
four absolute bounded paths, overwrites `searchPathRef` with installed runtime
then the selected method directory, and calls `importModules` exactly once for
the fixed retained `examples.ReadFootprint`. It uses explicit private level,
empty plugins and `loadExts := false`. There is no source frontend, `getEnv`,
helper `.olean` import into the mathematical environment, executable subprocess
or method recompilation in this runtime path.

Pinned `Lean/Environment.lean:2421-2452` explicitly permits constant-map access
without loaded extension state. That is the interface used here: `toKernelEnv`,
actual fixed-root `thmInfo` (not `axiomInfo`), then the unchanged bounded
`Export.indexSource` and `Export.selected`. The optional extension loader is
not needed for this kernel-record export; it is not being treated as valid
general-purpose elaboration state. Native shared-code initialization still
occurs before main, separately from the single owner declaration import.

Inventory lexical/byte checks and the inert bundle schema are unchanged.
Output is fresh/exclusive and at most64 MiB; the selected exporter retains its
own unit, edge, scan, source and grouping limits. Flushed markers are now
**before owner import**, after import, after indexing, after selected export and
after writing. These distinguish the next route's import and closure boundaries
without another diagnostic experiment. Caught errors produce bounded text and
exit1; catastrophic termination remains the external supervisor's responsibility.

The runtime executable, dependent DLLs, method artifacts, inventory and exact
search directories must be selected/authenticated by the later execution
controller. Native deserialization of owner-controlled `.olean` data is still
not a safe peer-input parser. A successful export remains inert claims to be
canonicalized and independently admitted through the existing checked receiver;
it establishes neither module certification nor the broader growth/release goal.

## Actual native build01 and separate actual-export adapter

**PASS_NATIVE_BUILD_ONLY.** Read the saved RESULT, BUILD-RESULT, selection and
all13 step records; inspected the26 corresponding empty stdout/stderr logs.
All nine snapshotted source hashes independently match the selected hashes,
including the six reviewed helper sources. Six code-generation steps, six
object compilations and the shared-library link each exit0. The resulting
executable is691,200 bytes and independently hashes to
`2cebc03232f9b3870afa2924c5ce595c33e03362205749ea08616e25850c0237`,
matching BUILD-RESULT. No actual owner export was part of this build.

The direct child exits0 and is reaped, final active processes0, Job closed and
cleanup errors empty. Cost:12.390625 Job CPU +1.046875 wrapper CPU =13.4375
known CPU seconds;12.678861000109464 outer wall seconds;678,518,784-byte peak
private commit. RESULT SHA-256 is
`c6775a49cedfe1889b9ca56fd4dcb7ce0fdbb377dad89ec3ec1b1165dc52f778`;
BUILD-RESULT SHA-256 is
`f5e6e708746ff54333fafd62f9565aa381ff17614bceea5e11da74d3058c8d00`.
No whole-toolchain rescan or runtime was conducted by this reviewer.

Read complete `run_native_owner_export.py` and
`select_native_owner_export.py`. **SOURCE_REVIEW_NO_BLOCKER_FOR_ONE_SEPARATE
ROOT_SELECTED_EXPORT.** The selector requires the successful exact build
selection identity and executable hash, and pins actual build records,
executable, selected shared runtime, retained ReadFootprint method and fixed
inventory. The runner clears inherited LEAN/PYTHON settings, prefixes the
installed DLL directory and directly invokes the native executable with the
four fixed selected paths. It performs no compilation, source elaboration,
receiver checking or catalog mutation. Fresh direct logs are retained; local
writer output is bounded before trusted local inspection. The inherited outer
limits remain120 CPU seconds,180 wall seconds,1,536 MiB and four active processes.

The actual finite selector/output must still be inspected by root before
launch. The earlier explicit-pin/nonhermetic import boundary remains unchanged;
build-record status text alone is not authority for an untrusted received binary.
This local selector relies on the owner-protected evidence just audited.

| Reviewed export adapter | SHA-256 |
|---|---|
| `run_native_owner_export.py` | `c3756d1989ec21d27f00edc417220ed1b90af5e7447de244fa9aa94e7f32e586` |
| `select_native_owner_export.py` | `d7b17218c5ff842d9fecaadb659b1fc27301bfe0e199f67508507dbdd5e7a566` |

## Actual native owner export01

**PASS_INERT_NATIVE_EXPORT_ONLY.** Independently read actual RESULT,
EXPORT-RESULT, direct logs and output census. All three selected source
snapshots match their selection hashes. The saved direct stdout contains all
five phase markers in order, through `OUTPUT_WRITTEN`; direct stderr is empty.
The retained method is actually imported and a fresh bundle is produced, not
fabricated from the predicted fixture or a prior source-frontend output.

A bounded standard-JSON data inspection of the exact saved bundle independently
confirms its six top-level fields, inert assurance string, one exact target
`DMKN.ReadFootprint.readsOnly_insertMany`,581 basis names and2,852 units. Its
42,202,667 bytes hash to
`dd85465ce6e670f2968c1fcb89ab733385575c2c6029a5f23306a499fc77ee3a`.
Recomputing compact JSON sizes for each unit gives42,142,071 total unit bytes,
matching the exporter report. The largest unit is963,145 bytes; no individual
unit exceeds8 MiB. This was saved-data inspection, not a product, native-checker
or exporter invocation.

Actual exporter diagnostics report73,274 imported source records,2,153 grouping
records,18,136 dependency edges and1,198,152 scanned expression nodes. These
internal counter values are reported diagnostics, not an independent traversal
of the source Lean environment. Fresh receiver checking remains necessary.

The direct child exits0 and is reaped, final active processes0, Job closed and
cleanup errors empty. Cost:11.234375 Job CPU +0.4375 wrapper CPU =11.671875 known
CPU seconds;12.748267400078475 outer wall seconds;1,168,179,200-byte peak private
commit. The source-motivated native route therefore actually completes inside
the unchanged1,536 MiB allowance where the two preceding producer frontend
routes did not. This is a finite workflow result, not a general asymptotic bound
or a matched performance benchmark against successful frontend execution.

Selection SHA-256:
`f3bcecc034b57a94378eec1dd8c4557e5d9022616f429a3d6e5210772e8f29d9`.
RESULT SHA-256:
`2287961b55238e0deb8d3e7e2c83444d511e20bb83d811d64c31df71ef258505`.
EXPORT-RESULT SHA-256:
`9058b3b6fb15d0ee1b541de50de6b2bd836521359dbb0f3a5f94eca1e72a7142`.

The real closure exceeds both the1,024-unit batch limit and the8 MiB evidence
envelope limit. Admission must split into ordered, separately granted batches,
accounting for complete envelope metadata, without raising the receiver caps.
The largest-unit census removes one possible indivisible-unit blocker; it does
not establish total metadata fit, topology correctness or admission success.
No checked native basis/extension, public contribution, downstream reuse,
succinct acceptance or growth result follows from export alone.
