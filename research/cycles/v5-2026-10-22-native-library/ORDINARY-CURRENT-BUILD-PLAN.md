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
