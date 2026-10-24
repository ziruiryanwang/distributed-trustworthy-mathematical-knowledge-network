# Current ordinary package: source-complete build plan

2026-10-23. `practical_path_audit`; canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source/data planning only: no project-code execution, compilation, owner opening,
package mutation, networking or Git operation. Root selects any implementation
and validation separately. This is one build plan, not another qualification ledger.

## Decision

Use **one thin, parameterized build orchestrator with three stages**:

1. Run the existing repository-source base builder unchanged in fresh storage.
2. Build `MissingImportExporter.exe` in a separate fresh native-code lane from
   six repository Lean modules, including the existing exact legacy-header view.
3. Assemble one current package directly from that base's generated artifacts,
   the new extractor and the exact source map below; generate its profile last.

Do not replay the historical overlay chain, accept an experimental output as a
required source, or modify the frozen base builder merely to avoid a small
orchestration layer. The user-facing command should take repository, Python
runtime, Lean toolchain, fresh output and one original resource allowance. No
`E:`/`D:` drive, historical selection file, existing owner or existing package
is a prerequisite of that command. The historical files below are comparison
evidence for this plan, not inputs to the proposed build.

This is source-complete buildability for the currently supported Windows/runtime
profile, **not** a claim of cross-platform support, hermetic compilation,
bit-for-bit reproducibility, unchanged implementation hashes or final v5 readiness.

## Exact reference and census

The current reference is `ordinary-project-return-assembly-01/package`, profile
`0d8a9ec4d3509e60f8e3155313b1023230c7f9b4f36f103e55464d2c866ae1b5`.
Its full deliverable map, excluding the outer profile and assembly receipt, is:

| Class | Count | Enumeration below |
|---|---:|---|
| Copied repository sources/assets | 51 | 19 installed + 32 auxiliary |
| Generated compiled artifacts | 74 | 8 receiver modules + 65 authoring parts + 1 extractor |
| Generated installed manifest | 1 | `installation/INSTALLATION.json` |
| Total | **126** | 37,507,787 reference bytes |

`PROFILE.json` is an additional generated required package descriptor. Build
logs/receipts and `_build` intermediates are not runtime payloads. The reference
`ASSEMBLY.json` is a local receipt, not required source or mathematical authority.

Read-only comparisons established:

- All 47 repository inputs recorded by `ordinary-source-package-build-01` still
  match their saved source pins; no reconstruction from ignored snapshots is needed.
- All current 65 authoring parts and eight installed receiver `.olean` files
  equal that original base build's selected outputs.
- Every direct-copy payload below matches its named repository source, including
  renamed module03/worker03 and the two foundation assets.
- The four lower sources used for the old native extractor also still match the
  repository. The old native `.o` files are therefore replaceable build outputs,
  not irrecoverable source inputs.

No Git operation was used: root must ensure every selected source/asset is included
in the eventual source distribution. A file's presence and `.gitignore` eligibility
do not establish that a clean clone contains it.

## Complete direct-copy payload map

All paths in source columns are relative to the canonical repository. Braces
below enumerate a finite set; they are not filesystem discovery globs. Expand
them into exact records before implementation, reject duplicates and require
the expanded counts to equal the census above.

### Installed direct payloads: 19

| Logical output | Repository source |
|---|---|
| `installation/lean-src/{OriginalExpr,OriginalDecl,CheckedExtension,LocalSnapshot,BootstrapSupport,BasisSnapshot,OrdinaryWorkflowWorker}.lean` | `software/v5/ordinary_lean/{same}.lean` |
| `installation/lean-src/OrdinaryExport.lean` | `software/v5/ordinary_package/receiver_source/OrdinaryExport.lean` |
| `installation/py/{ordinary_admission,ordinary_evidence,ordinary_semantics,portable_evidence,portable_catalog,local_catalog}.py` | `software/v5/ordinary_lean/{same}.py` |
| `installation/supervisor/{commons,run_stage,domains}.py` | `software/v5/ordinary_package/supervisor/{same}.py` |
| `installation/foundation/seed.json` | `software/assets/foundation/seed-verified.json` |
| `installation/foundation/inventory.json` | `software/assets/foundation/seed-inventory-json.json` |

Foundation bytes remain the existing selected assets; this is not a new basis
generation step. Their hashes are respectively
`a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`
and `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`.

### Auxiliary direct payloads: 32

| Logical output | Repository source |
|---|---|
| `owner.py` | `software/v5/ordinary_module_package/owner.py` |
| `profile.py` | `software/v5/ordinary_module_package/profile.py` |
| `author_worker.py` | `software/v5/ordinary_project_package/author_worker.py` |
| `peer.py` | `software/v5/ordinary_peer_package/peer.py` |
| `peer_api.py` | `software/v5/ordinary_resilient_package/peer_api.py` |
| `module_worker.py` | `software/v5/ordinary_module_bridge/module_worker03.py` |
| `module/OrdinaryModule.lean` | `software/v5/ordinary_module_bridge/OrdinaryModule03.lean` |
| `authoring/py/ordinary_contribution.py` | `software/v5/ordinary_project_return/ordinary_contribution.py` |
| `authoring/py/{completion_api,library_completion}.py` | `software/v5/ordinary_library_package/{same}.py` |
| `authoring/py/{library_extraction,supervised_library_exchange}.py` | `software/v5/ordinary_library_support/{same}.py` |
| `authoring/py/retained_preparation.py` | `software/v5/ordinary_library_support02/retained_preparation.py` |
| `authoring/py/{module_closure,module_export}.py` | `software/v5/ordinary_module_bridge/{same}.py` |
| `authoring/py/{ordinary_preview,owner_request,portable_candidate,portable_owner_request,portable_preview}.py` | `software/v5/ordinary_lean/{same}.py` |
| `support/custody/module_store.py` | `software/v5/custody/module_store.py` |
| `support/transport/{clients,http_provider,ordinary_acquisition}.py` | `software/v5/transport/{same}.py` |
| `support/discovery/{authenticated_index,candidate_query,discovery_query,discovery_store,formal_features,ordinary_export_adapter,search_session,summary_wire}.py` | `software/v5/discovery/{same}.py` |

Important exact successor choices are `retained_preparation` from **support02**,
`peer_api` from **resilient_package**, `ordinary_contribution` from **project_return**,
and module/native worker **03**, not similarly named earlier versions. Module03
SHA is `9002e54d73fc884ebce50b8c782757801a0d0abd6cc6c0fee6ed83a455f8536f`;
worker03 SHA is `35b24343be54ce26ea36c0bfad4c4e81ea869e35fcd24a7892dfd3ad4f4585a6`.

## Complete generated payload map and compilation lanes

### Receiver lane: eight shipped `.olean` files

Use the existing base builder's order:

```text
OriginalExpr, OriginalDecl, CheckedExtension, LocalSnapshot,
BootstrapSupport, OrdinaryExport, BasisSnapshot, OrdinaryWorkflowWorker
```

The source for each is its installed direct-copy source listed above. Outputs
are exactly `installation/lean-lib/<name>.olean` for these eight names. Keep the
receiver-specific `ordinary_package/receiver_source/OrdinaryExport.lean`
(`ecab2be2...`), not the newer owner-side exporter. Keep its current semantic
checker, foundation policy, support groups, module ordering and local acceptance
protocol. Compiled companions/intermediates not in the installed manifest remain
build-only; do not add them to that trust boundary casually.

### Authoring lane: 13 modules times five shipped parts

In the existing base builder's order:

```text
OriginalExpr, OriginalDecl, CheckedExtension, BootstrapSupport,
OwnerRebind, OwnerConstruction, OwnerUseCommand, OrdinaryExport,
SuccessorExport, SuccessorExportCommand, PortableOwnerConstructCommand,
PortableConstructExportCommand, PortableContributionExportCommand
```

Each originates from `software/v5/ordinary_lean/<name>.lean`. Apply the base
builder's exact `public_source` header transformation **only** to the first four
names: public imports and public section, with post-import body bytes retained.
Its `PUBLIC_HASHES` binds all four transformed source hashes. The remaining nine
sources are already in their selected form and are copied unchanged.

For each name, ship all five existing parts under `authoring/helpers/`:
`.olean`, `.olean.private`, `.olean.server`, `.ir`, `.ir.sig`. This gives 65
artifacts, with the existing private/exported import distinction retained. The
current compiler produces all five; final package census must satisfy the current
loader, not silently treat an absent part as equivalent support.

### Native extraction lane: one shipped executable, six source modules

Freshly build this dependency order, without reading prior `.o` or `.olean` files:

```text
OriginalExpr, OriginalDecl, CheckedExtension, BootstrapSupport,
OrdinaryExport, MissingImportExporter
```

All six original sources are `software/v5/ordinary_lean/<name>.lean`. The first
four are their **legacy original** source view, not the public authoring view.
For `OrdinaryExport`, use exactly `run_missing_import_build.py:legacy_view`:
remove the initial `module` wrapper/public section and turn its three public
imports into ordinary imports, preserving remaining lines. Its selected generated
source hash is
`3e046d40150127fa1d480b1f4a678dea47a93353eb67b01c542b9ea3df2dcedc`.
`MissingImportExporter.lean` remains unchanged, SHA
`7efb8bfa768a97ebcced687fd2a5acb0227e65eb2260e82d1726d8f361b27fbb`.

Use the established command shapes: Lean `-R <source> -o <module.olean>
-c <module.c> <module.lean>`, then `leanc -c -O0 <module.c> -o <module.o>`,
and one `leanc -leanshared <six object files> -o MissingImportExporter.exe`.
Only `authoring/bin/MissingImportExporter.exe` is shipped. Source views, `.c`,
`.o`, temporary Lean artifacts and build receipts stay under fresh build storage.

Do not run the old adapters directly: both `run_native_export_build.py` and
`run_missing_import_build.py` require experiment-specific roots or prior files.
Reuse their source transformation and compiler procedure in a parameterized
stage; do not inherit the old script's ambient PATH or per-command timeout policy.
Use selected runtime paths and one remaining parent allowance throughout.

Keeping this native lane separate duplicates four small lower compilations but
leaves the tested base builder untouched. Sharing code-generation output with
the receiver lane can be a later build-only optimization if worthwhile; it is
not needed to make the first source-complete build operable.

### Module03 is not a package-build artifact

The package ships `module/OrdinaryModule.lean` and `module_worker.py` as exact
source bytes. Worker03 invokes the selected Lean runtime's `--run` in three
sequential phases. Per-user generated `DMKNBridge_<hash>` five-part modules are
operation outputs, not inputs or payloads of the release build. A release build
must not pre-export the earlier test theorem, copy its native module, or run an
owner operation merely to package module03.

### Manifests and identities

Generate `installation/INSTALLATION.json` through the unchanged
`software/v5/ordinary_lean/ordinary_installation.py` assembly relation from the
actual new receiver outputs and explicit runtime pins. Generate the final outer
profile from the actual 98 auxiliary payload records and new installed-manifest
hash; retain the current owner schema/helper-path/worker fields. Final-file
publication follows full verification, with partial outputs preserved on failure.

The reference implementation ID is
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
Compiled bytes can differ with build paths/toolchain details even when intended
source semantics are identical. Derive hashes and IDs from actual outputs; never
stamp this old ID/profile onto new bytes. If new support changes the installation
identity, old owner state is not thereby authorized for use with it. Keep the
reference package/state intact and validate fresh support separately. Semantic
identity/foundation/checking rules remain unchanged by this build plan.

## Required source and runtime inputs beyond shipped copies

The orchestrator also needs the frozen base `ordinary_package/build.py`,
`ordinary_lean/ordinary_installation.py`, all listed authoring/native Lean sources,
its new finite source map and its own selected source. The base builder stages its
47 existing inputs, including older entrypoint/support versions that its temporary
base package uses; keep those tracked inputs unless a later reviewed integrated
builder eliminates them. No historical `selection.json`, package, source snapshot,
local database or generated binary is a build prerequisite.

Supply the complete supported Python 3.14.6 and Lean 4.34.0 Windows distributions
at explicit roots; do not silently download or rebuild Lean/Std. Preserve the base
builder's named runtime checks. Native code generation additionally needs the
actual bundled `leanc.exe`, `clang.exe`, `ld.lld.exe`, `lld.exe`, `libclang-cpp.dll`,
`libLLVM-22.dll`, `zlib1.dll`, `libLake_shared.dll`, and the selected Lean import
libraries (`libLake_shared.dll.a`, `libInit_shared.dll.a`,
`libleanshared{,_1,_2}.dll.a`, `libleanmanifest.a`). The existing native selector
lists these named files; copy its names/expected supported pins into a versioned
build profile rather than reading its prior experiment selection. Lean headers,
installed `.olean`/IR and other bundled compiler/system dependencies remain part
of the declared full toolchain premise. These named checks are not a complete
hermetic dependency census. C compiler tools need not be required for end users
running an approved prebuilt package; distinguish build and runtime requirements.

## Why thin orchestration, not another overlay chain?

| Choice | Benefit | Cost / disposition |
|---|---|---|
| Rewrite/extend one integrated builder immediately | One implementation can emit everything directly. | Reopens tested receiver/authoring staging, source pinning, supervision and manifest code; larger review surface before a demonstrated need. Defer. |
| Thin three-stage orchestrator plus one exact current assembly map | Reuses the tested two-lane builder, removes the only historical compiled dependency, emits one current package. | Requires a small parameterized extractor stage and current-map assembler. **Recommended.** |
| Caller supplies an approved extractor binary and pin | Cheap offline assembly/cache hit. | Only an optional explicit cache/packaging mode; it is not a source-complete build unless a complete source recipe is also provided. An arbitrary executable cannot be trusted from its filename or self-reported hash. |

One original allocation covers source staging, base compilation, extractor build,
final copying and manifest commit; derived child grants decrease, failed stages
do not retry automatically, and failure retains outputs. Keep compilation lanes
sequential on this PC by default; source review/map checks can proceed in parallel.
No RAM tuning, resident checker or cryptographic certificate is part of this work.

## Small machine-readable map, if root selects implementation

One versioned file next to the eventual orchestrator is sufficient, not a new
research registry. It should contain these finite records:

- Exact copy map: 51 `logical_output -> repository_path + source hash` records.
- Three ordered module lists and explicit transform IDs with selected source and
  transformed-source hashes; no arbitrary build commands supplied by a peer.
- Exact allowed output groups/counts and generated-manifest rules.
- Named build/runtime profile and the expected package entrypoint/schema versions.

The map is versioned build input. Actual generated-artifact hashes and receipts
are per-build output. Keep these distinct. Check that all logical names are unique,
all repository paths remain inside the selected source root, no required input
is under ignored experiment/product/runtime output trees, and every current
payload is accounted for exactly once. The final implementation must not consult
the reference profile on the developer's disk to discover missing sources.

## One decision-changing validation, after source implementation/review

Select one **clean-source build-to-relocated-use discriminator**, not another
repeat of all earlier mathematical/network campaigns:

1. Provide only the selected repository source/assets and explicit full runtimes
   to fresh build storage. The old experiments and packages must be unavailable
   as inputs, rather than merely unused by convention. An isolated input manifest
   or appropriate filesystem/process restriction should establish this boundary;
   a text scan of paths alone is weaker evidence.
2. Build once under a finite aggregate allocation. Require all three compile lanes
   clean, complete source/transform/output accounting, a current-loader-compatible
   126-payload map and actual manifests. Copied sources must match exactly;
   generated hash differences are reported, not hidden or declared equivalent.
3. Relocate only the runtime package, without `_build` or source checkout. Under
   the newly derived support identity, run the smallest supported public smoke
   that exercises fresh receiver checking and ordinary authoring/module use;
   verify the newly built extractor's supported local protocol path as part of
   this finite smoke. Reuse an already reviewed workload's mathematical design,
   not its old acceptance flags or live owner state. This is the changed native
   build boundary, so one such validation is not a repeat timing campaign.

Root should choose the exact small smoke after the current return result, avoiding
the still-unimplemented mixed-Init match route. A package load alone would not
establish compiled interoperability; conversely global peers, scalability and a
new growth benchmark are unnecessary to answer whether this build route works.
Passing establishes the selected source-complete build and use boundary only;
release licensing, platform scope, hostile-source isolation and independent
deployment remain distinct obligations.

## Source implementation checkpoint, 2026-10-23

Root selected source-only `software/v5/ordinary_distribution` after this plan.
The new `source-map.json` expands all 51 copies and pins their 67 distinct
repository inputs (including the base builder's 47), the three ordered lanes,
exact transformed hashes and 14 additional named native compiler/library pins.
Its SHA-256 is
`b021ae3225fe85a874cea82266c0c380d08fc755fee4fc282872f0f506f298bf`.
The unchanged base builder remains
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.

The new `build.py` stages those selected inputs into fresh `_build/inputs`,
invokes the unchanged base builder under its existing supervisor in
`_build/base`, builds the six native modules sequentially from fresh legacy
source, then assembles the current 126 payloads directly into sibling
`package/`. The actual installed manifest is generated by the base builder's
unchanged assembler and copied with full file-map/support-digest checks;
the actual 98-record outer profile is committed last. Module03/worker03 remain
source copies. No installed owner or reference package is opened.

The CLI requires explicit source, Python runtime, Lean runtime, output and
wall/CPU/memory inputs. One original allowance covers all work. Each supervised
child receives a remaining grant after reserving cleanup and supervisor CPU;
the base receives a smaller inner grant. Complete outer child Job CPU is charged
once, including nested compiler work. Unknown final CPU consumes the selected
grant and stops. Clean outer and nested base Job closure is checked. Source and
named runtime pins are rechecked before final profile commit. Output failure is
preserved, with no retries or cleanup of prior evidence.

`README.md` documents the command, runtime/build distinction, package relocation,
resource premises and source-only status. Only source/data reading, hashing and
these new-file edits have occurred. No import, test, compilation, build, package
mutation or runtime qualification was executed for this implementation. The
independent source review and later root selection remain separate.

## Minimum relocated-use discriminator: source design only

Root requested this design after the implementation checkpoint. No harness,
state, compilation or operation is selected by this section. Its purpose is to
answer one changed-boundary question: can the newly built receiver, authoring
artifacts and extractor interoperate through the current package after relocation,
using a fresh owner under the newly derived support identity?

Use **six public `owner.py` commands plus one ordinary Lean consumer compilation**.
Initialize one owner, then use two explicit branches from its returned basis.
The module branch contains only fresh definitions/theorems whose proof closure
does not contain an installed-Init theorem. The separate library branch exercises
the newly compiled extractor and combined receiver acceptance. No extra status,
wrong-profile, network, growth, negative-module-collision or project-return
campaign is needed to decide this build boundary.

### Reused designs and inputs

Reuse the source design of `ordinary_package/lifecycle_check.py` and its
`continue_lifecycle.py` correction for initialization and the already-passing
two-unit caller body. Reuse `ordinary_module_package/public_native_check.py`
and `ordinary_module_bridge/native_check03.py:normal_consumer` for module export,
runtime/artifact binding and a normal private/exported module consumer. Reuse
`ordinary_library_support02/native_check02.py` for the exact missing-library
refusal, extraction protocol and proof-bearing completion assertions.

These are design references, not executable dependencies: their hardcoded old
owner paths, hashes, utility path gates and fixed allowances must not carry into
the new smoke. A new small parameterized harness should take only the relocated
package, its actual new profile hash, explicit supported runtimes and a fresh
smoke directory. The selected harness/supervisor are test machinery; no product
Python helper may be imported from the source checkout or old build. Root must
choose and record the exact clean-input boundary with the build selection.

Relocate exactly the 126 runtime payloads and `PROFILE.json`, preserving hashes,
into a fresh directory separate from `_build`, the source snapshot and state.
Verify the full 127-file map before use. Read the new build receipt to select
the profile/installed-manifest/implementation hashes; never assume the old
reference IDs. Only the relocated package, declared full runtimes, small test
fixtures and fresh operation outputs belong to the smoke input closure.
Use a fresh local store ID and fresh catalog/custody; reuse the documented finite
custody limits `{objects:512,exports:4096,logical_bytes:134217728,db_pages:16384}`.

### Exact operation sequence and decisive checks

Every owner command gets the same selected profile/runtime/store/custody arguments,
its own fresh output if required, and a grant derived from the original remaining
smoke allowance. Structured names use the existing portable name encoding.

| Step | Operation and selected input | Required outcome |
|---|---|---|
| 1 | `init` on fresh catalog/custody | `INITIALIZED_LOCAL_OWNER`, basis `CHECKED`; save returned basis root **B** and new implementation ID. |
| 2 | `contribute --parent-root B`, acquired targets `[]`, exact two outputs below | `CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES`; exactly two checked units, two target/previews, new root **A**; all evidence/publication pins verified. |
| 3 | `export-module --parent-root A`, target is the exact returned `applyTwice_eq` `{name,export_id,unit_id}` | `CHECKED_PROOF_COMPLETE_LOCAL_MODULE`; selected theorem and its fresh definition form the two-unit closure; five artifact parts, exact module manifest, runtime identity and clean three-phase worker; no new catalog acceptance. |
| 4 | One ordinary Lean compile of a fresh consumer importing only Init and the just-returned module | Exact theorem application and independent `rfl` reduction both elaborate; require clean process closure, empty diagnostics and nonempty required module parts. |
| 5 | `contribute --parent-root B`, acquired `[]`, exact `Nat.add_zero` caller below | Expected `CONTRIBUTION_CANDIDATE_NEEDS_INTERPRETATIONS`, missing set exactly `Nat.add_zero`, acceptance absent. Retain candidate, request, preparation and authoring supervision; charge this expected refusal. |
| 6 | `extract-std --parent-root B`, retained step-5 directory plus exact request/candidate hashes; modules `[Std.Data.Internal.List.Defs]` | `EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED`, one supplemental theorem/one consumer; exact retained candidate unchanged, required protocol closure, `mathematical_acceptance:false`. |
| 7 | `complete --parent-root B`, step-6 candidate/supplement/prepared-binding pins and original output target | `CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES`, exactly two checked theorem units, new root **C**; consumer proof contains `Nat.add_zero` and binds the actual supplemental export ID. |

Step 2 source is the existing lifecycle body with the already-established
visibility correction, not a new mathematical workload:

```lean
namespace CommonsPackageExample

@[expose]
def applyTwice {a : Type u} (f : a -> a) (x : a) : a := f (f x)

theorem applyTwice_eq {a : Type u} (f : a -> a) (x : a) :
    applyTwice f x = f (f x) := rfl

end CommonsPackageExample
```

Outputs are `CommonsPackageExample.applyTwice` and
`CommonsPackageExample.applyTwice_eq`. Step 4 uses the module name returned by
step 3, validates its fixed `DMKNBridge_` plus 64 lowercase hex grammar, and uses
the selected Lean runtime with `LEAN_PATH` containing only its installed library
and the new exported-module directory. Its body has two theorem statements
`CommonsPackageExample.applyTwice f x = f (f x)`, proved respectively by
`@CommonsPackageExample.applyTwice_eq a f x` and `rfl`. It follows the existing
consumer's `module`/public-import/public-section form. No original authoring
source, package helper modules, old exported module or scratch-axiom module is
placed on that consumer path.

Step 5 source and step 6 module selection are the existing supported extractor
fixture, unchanged:

```lean
theorem CommonsLibraryExample.add_zero (n : Nat) :
    Nat.add n Nat.zero = n := Nat.add_zero n
```

Step 5–7 use **B**, not A or a guessed latest root. The `Nat.add_zero` branch
is not exported with module03: its installed-theorem collision remains outside
this supported smoke. Step 3–4 occur before that branch exists. Completion must
verify the actual supplemental theorem evidence, the consumer's import/export
identity, its proof constant reference, durable evidence/preview pins and native
admission. Compiler success or a supplementary JSON file alone is insufficient.

### Accounting, final evidence and limits

A reasonable prospective envelope is one smoke allowance of 300 wall/180 CPU
seconds within a separately selected 330 wall/210 CPU/2048 MiB/eight-process
outer Job, with sequential 1536 MiB native calls. Initialization may use at most
120 wall/90 CPU; later calls at most 75 wall/40 CPU, always decreased to fit the
original remaining allowance and cleanup reserve. These numbers are a proposal,
not an executed selection or permission to retry. Root can choose a tighter
reviewed envelope before any launch. No machine memory setting changes or
package/support/extractor rebuild belongs to the smoke; the small local export
and consumer compilation are the intended public-use operations themselves.

Use one aggregate accounting owner. Charge each complete child process tree once;
do not add its nested native samples again. Any missing final CPU sample consumes
that command's selected grant and stops. The one expected missing-library refusal
must still have clean tree closure and complete accounting. Other failures stop
the sequence and retain actual accepted outcomes, partial output and diagnostics.

Final evidence should contain the relocation map, actual new identities, seven
command/grant/closure records, fresh B/A/C root bindings, the two independent
proof-use checks, exact native output pins and total wall/CPU cost. Recheck all
127 relocated package files, selected runtimes and immutable input/output pins;
never rewrite used artifacts. Subsequent owner commands already reopen the fresh
state, so a separate status command adds no decision-changing evidence here.
Passing establishes this one clean-source-build/relocated-use boundary, not broad
library coverage, arbitrary project imports, novelty, global growth or final v5.

## Relocated smoke source checkpoint and compatibility hold, 2026-10-23

Root adopted the seven-step design and selected source-only implementation in
`software/v5/ordinary_distribution/relocated_smoke.py`. The CLI requires
`--package`, `--profile-sha256`, `--python-runtime`, `--lean-runtime`, fresh
`--output`, `--wall-seconds`, `--cpu-seconds` and `--memory-mib`; it needs no old
utility script or source checkout. Only the relocated installation's pinned
supervisor/Job helpers are imported. All product operations use the public CLI,
and the normal consumer uses a fixed child mode of this selected harness.

Root's later prospective selector supersedes the earlier numeric proposal:
**360 wall / 240 CPU / 1536 MiB inner**, within **420 wall / 300 CPU /
2048 MiB / eight-process outer**. Both are still finite and unexecuted for this
smoke. Each command has a smaller remaining grant with a 25-second cleanup
reserve and 62 CPU seconds reserved for the unchanged supervisor's controller
plus final work; complete child Job CPU is charged once. Unknown accounting
charges its full grant and stops. The one expected missing-library refusal
requires the exact exception, no acceptance and clean complete process closure.

The harness binds the whole 127-file relocated tree, actual new identity,
named runtime and selected installed-Std module parts before operations. It
checks basis initialization as **456 checked seed units, 581 inventory names,
zero retained nonbasis unit IDs**, rather than confusing that count with ordinary
extension inputs. The module request/report uses structured names while the
public manifest uses the fixed string module name and full target records;
the harness checks those respective encodings. Every actual native artifact,
retained candidate, complete proof import, preview/evidence file and immutable
input is pinned and rechecked; report data preserves acceptance before later
assertions. No extra owner status, retry or package rebuild is included.

Independent source review found a real release compatibility blocker before any
smoke execution: the shipped `ordinary_library_support/library_extraction.py`
still requires the former native extractor SHA
`9700c6c2944d327a648e3fcf83453ee1aa019d2f05c182feec13e78211711dc7`
and size 697344 at its two executable checks. The new clean-source build's
extractor has different bytes, so this frozen helper would refuse it even though
the new outer profile pins those actual bytes. The successful assembly is not
therefore public-use qualification. Root holds all actual smoke work and owns
any separately selected narrow explicit extractor-profile binding successor.
The used builder, map and newly built package stay frozen; this harness does not
weaken their checks, rewrite the old pin, change the fixture or claim readiness
to run against the incompatible package. Only source reads/edits occurred here.

### Final ordinary-command accounting hardening, 2026-10-23

Independent source review identified that the unchanged supervisor's final-sample
resource-status rewrite applies only to a zero exit. The smoke harness now checks
each ordinary command's final complete Job CPU, wall time through cleanup and
both observed log lengths against that record's own limits, including the one
expected exit-1 missing-library refusal. Values must be finite/nonnegative, log
lengths integral, and caps valid; a status string alone is insufficient. This is
a source-only harness assertion, not a supervisor/product edit or a new operation.
The extractor compatibility HOLD and all frozen build/package bytes remain intact.
