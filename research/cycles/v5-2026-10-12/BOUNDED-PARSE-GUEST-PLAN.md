# Smallest sound bounded-parse guest build

2026-10-12. Source-only feasibility requested by root. Canonical project:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No build implementation, compiler/Cargo invocation, cache mutation, guest run,
image adoption or proof is selected by this note. Native qualification and the
separate image/certification investment decision remain prerequisites.

## Decision

Only **three project compilation units need new mathematical source output in
principle**: module relation, aggregate relation, then the unchanged guest entry
linked to the new aggregate. The native checker and external dependencies do not
depend on those changed units. Their compiled artifacts exist.

However, the retained operation did **not record exact per-rustc argv/environment
recipes**. Its Cargo command was not verbose; saved unit graphs, fingerprints,
artifact messages and dep-info do not together constitute such a recipe. Base,
who prepared the earlier guest continuation, also knows of no separate retained
rustc command log/build plan. Therefore a purported exact three-command replay
would currently contain newly inferred compiler behavior.

Recommendation: use one fresh, offline Cargo successor with the small reviewed
source overlay and retained lock, private writable output/cache state, and one
changed-graph validation. Reuse the compiler, SDK, standard-library sources and
selected source/archive material read-only. Replace broad repeated SDK copies
and census with an explicit input-closure manifest and bounded output accounting.
Do not claim that this fallback reuses compiled dependency artifacts: without a
new justified recipe or compatible private Cargo cache it may rebuild them.

This is an economical fallback, not a conclusion that thin compilation is
impossible. A future deliberately derived thin-build recipe is a separate build
design with its own compatibility obligations, not recovered historical evidence.

## What the retained evidence actually contains

Let `B` denote `experiments/v5-local-checks/aggregate-guest-compile-01` and `P`
denote `experiments/v5-local-checks/aggregate-guest-build-01/project`.

| Evidence | Established fact |
|---|---|
| `B/commands/build-aggregate-guest/command.json` | One offline Cargo build, exit0 and clean owned-Job closure; 222.640625 worker CPU seconds /197.9885544 phase wall seconds |
| Its `stdout.txt` | Cargo compiler-artifact/build-script/diagnostic messages and final build-finished:true; actual project artifact paths and feature/profile fields |
| Its `stderr.txt` | Compilation progress and warnings, not verbose per-rustc invocations |
| Build01 `commands/offline-aggregate-graph/stdout.txt` | 297-unit graph, including project targets, target/host dependencies, features, profiles and extern-edge attributes |
| `B/GRAPH-COMPARISON.json` | Corrected four lexical source-path fields, no external package/feature/profile/edge changes in that historical graph comparison |
| `B/target/.rustc_info.json` | Saved successful compiler identity and target-probe outputs; not a recording of each compilation |
| `B/target/.../.fingerprint/*/*.json` | Dependency fingerprints, rustflags and hashed profile/path/config identifiers; not full compiler argv, complete environment or strong hashes of all output rlibs |
| `B/SOURCE-MAP.json` | Project, std and retained source/tool provenance; not a complete hash manifest of the new target's compiled dependency outputs |

The original operation remains `FAIL_FINALIZATION`: its controller resource
accounting failed after compilation. The separately adopted
`aggregate-artifact-validation-01/validation/RESULT.json` establishes the retained
source-bound ELF and map without relabeling that resource failure. Its authority
is not a blanket retrospective hash adoption of every intermediate rlib.

Selected anchors, all read without running project code:

| Record | SHA-256 |
|---|---|
| Cargo `command.json` | `d914a4fe3a605a9de832c275b8b51b9abdfdba7a973d2204673eab5490cb6f05` |
| Cargo stdout | `8e54baefabfa6abc5461af0b6a9b126960203df9bf4e45ae9a9feccd4ad0328b` |
| Cargo stderr | `4c62b4fde0f3eac140525a7d8620b929eb7d769ceeeae45167f9335358bc2e94` |
| Raw297-unit graph | `2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609` |
| Compiler-info cache | `19c9c5fc1339e83206226d6f2868a8729b6f7bdb9cfc4c0bc4fa1c30476743f7` |
| Environment profile | `7e1b195a0e075eec9ba8f0d7f8e65c83a9a3cebfc3332e7910d9909be2581ff5` |
| Independently adopted artifact-validation result | `a9d60ab02a01f87bed72c0ee9053e56e698a6c8f5dae93d6f1ba9b3cc3b3da6f` |

Hashes identify these records; they do not by themselves prove compiler or
mathematical correctness. Current directory names/fingerprints must not be
promoted into cryptographic output identity evidence that was never recorded.

## Exact known toolchain, target and profile

The saved compiler reports Rust1.90.0-nightly, commit
`35f6036521777bdc0dcea1f980be4c192962a168`, 2025-06-29, LLVM20.1.7,
host `x86_64-pc-windows-msvc`. The target is `riscv32im-risc0-zkvm-elf`, not native
Windows and not a generic riscv32 target. Tools are under
`experiments/scale-crypto-01/runs/run-01/rust`:

| Tool | Retained SHA-256 |
|---|---|
| `bin/cargo.exe` | `fa896442658543c197ae639b89ad28666bd6e058aac31058f182b6d95704c634` |
| `bin/rustc.exe` | `9d4ba43cfc3d62c1aa8c3047fbde3b1121ce4603b589e7f710fcc0b3f8e983c2` |
| `bin/rustc_driver-ecefa69f0eda2d36.dll` | `ae185e6cb8a5168fa16b35115f985cfd8d771d1982c0039b92c7253e31475d1b` |
| `bin/std-7b882922f1f4358d.dll` | `e688d9efcaa3637023e22a1e5abe1380864e4d8475ee1cfed79065d2378d7b7e` |
| `lib/rustlib/x86_64-pc-windows-msvc/bin/rust-lld.exe` | `6113300d0b4e0478e7fd16d41593652eb103c617f6dbf0d7524f1a6e647fa150` |

These five rows are useful anchors, **not an asserted complete loaded-runtime
closure**. Any selected build must also bind its actual host libraries, imported
helpers, subprocess tools and standard-library/SDK inputs. Debugger scripts,
PDBs and unrelated SDK examples need not be rehashed to justify a compiler run.

Known common project profile: edition2021, release opt-level3, LTO enabled,
overflow checks enabled, panic abort, debuginfo0/strip-debuginfo,
debug assertions and incremental compilation disabled. Retained guest flags:

```text
-C passes=lower-atomic
-C link-arg=-Ttext=0x00200800
-C link-arg=--fatal-warnings
-C panic=abort
--cfg getrandom_backend="custom"
-C link-arg=-Map=<fresh output>/guest-link.map
```

The new map must have a fresh path. Never let a copied old link argument overwrite
the retained map. Standard-library construction used:

```text
-Z build-std=alloc,core,proc_macro,panic_abort,std
-Z build-std-features=compiler-builtins-mem
```

Its source library is the retained
`experiments/general-checker-guest-02/prepare-01/std-candidate/lib/rustlib/src/rust/library`,
selected through `__CARGO_TESTS_ONLY_SRC_ROOT`. The caller must preserve the
reviewed relationship between that root, its Cargo.lock and the compiler. Using
the native recipe's precompiled sysroot or native serde dependencies would not
be this guest build.

## Three-unit reverse dependency closure

In the saved graph, units78,79,80 are respectively aggregate library, guest binary
and module library. Unit141 is the unchanged checker. Let C be the changed source
units and let R(C) be C plus all units transitively depending on C. Under fixed
toolchain/profile/features and unchanged external inputs:

```text
C = {module, aggregate}
R(C) = {module, aggregate, guest bin}
```

This is a dependency argument for possible compiled reuse, not a claim that a
fresh Cargo target automatically recognizes it. Relocated package/source paths,
metadata and Cargo fingerprints can invalidate a cache even when the relevant
mathematical source is unchanged.

All three units have public+noprelude edges to the custom target's `alloc`,
`compiler_builtins`, `core`, `panic_abort`, `panic_unwind`, `proc_macro`, `std`.
Their ordinary extern edges are:

| Unit | Ordinary externs |
|---|---|
| module | nanoda_lib, risc0_zkvm, serde, serde_json |
| aggregate | new dmkn_module_relation, risc0_zkvm, serde_json |
| guest bin | new dmkn_aggregate_relation, new dmkn_module_relation, risc0_zkvm, serde_json |

The target artifact directory already contains `libnanoda_lib-7f1af4fb875deccc.rlib`,
`librisc0_zkvm-d0646bed92fd0a22.rlib`, `libserde-8b3577d8ed5052bf.rlib`,
`libserde_json-71b80176eee68a68.rlib` and all seven listed standard libraries.
These names/lengths were inspected, not adopted as a complete immutable cache.
Their transitive dependency artifacts, metadata and any proc-macro/host-runtime
requirements must also be resolved before a thin command can be selected.

The whole saved graph is reachable from the bin:111 target build units,21 target
run-custom-build units,145 host build units and20 host run-custom-build units.
That is **not**111 mandatory new target compiles for the changed source; it is
the closure a clean Cargo build currently knows. Actual build messages contain
41 build-script executions. No saved build-script message advertises linked_libs
or linked_paths, but some carry generated env/cfg/output directories. This
observation is not permission to discard generated-source/metadata obligations.

The pinned target serde_json is1.0.151/default,std. Target serde is1.0.229 with
alloc/default/derive/rc/serde_derive/std; host serde has a different feature/profile
unit. RISC0 zkvm is5.0.0 from the retained SDK checkout with only its std feature.
Do not substitute the native1.0.145 serde_json recipe. Keep the exact lock and
graph-feature equality, not merely a permissive version constraint.

## Why an inferred thin command is not yet selected

The graph answers which units depend on which others. It does not preserve full
rustc invocation spelling, crate metadata/disambiguators, emit/output options,
complete Cargo environment, build-script-expanded flags or LTO/bitcode decisions.
Those omissions matter particularly for custom build-std and cross-target linking.
The compiler-info cache and fingerprint hashes do not invert those details.

A newly derived explicit recipe could be valid after reviewing those obligations
and pinning every consumed artifact. It must not search an uncontrolled directory
and accidentally link both old and new module/aggregate crates. It would create
a new image even if its mathematical relation is unchanged. Its justification
would be new, not evidence of exact historical command recovery.

As an alternative planning aid, a future separately selected Cargo build-plan
or command-recording route might recover commands for a fresh workspace. It has
not been run here; compatibility with this pinned nightly/build-std path and
dynamic build-script outputs must first be established. Do not spend another
speculative build campaign merely to avoid a modest known offline compile.

## Minimal fresh offline Cargo fallback

1. Make a small fresh project snapshot preserving the old relative layout, exact
   lock and unchanged project-source pins. Add the six reviewed bounded_parse
   production files. Change only the new wrapper manifests' lib paths to
   `bounded_parse/module_lib.rs` and `bounded_parse/aggregate_lib.rs`; retain the
   old guest main and checker. Do not change old manifests, sources or caches.
   Select only `--bin dmkn-aggregate-claim-guest`, not tests/examples/all-targets.

2. Keep the old SDK/stdlib/toolchain inputs read-only. Use a fresh writable
   CARGO_HOME, target, temporary directories and no-credential environment.
   Seed only lock-required registry/index/git/archive data from retained exact
   evidence, not the whole unrelated SDK/cache. Reused archives need their
   recorded digest and safe bounded extraction; unchanged read-only source
   inputs need an explicit justified source binding. This is a selective
   provenance check, not an exemption from checking consumed bytes.

3. Validate the **new changed graph once**. Compare its whole normalized graph
   against the297-unit predecessor with only explicit project relocation and
   the two changed lib source roots. Package versions, external source IDs,
   target/host distinctions, features, profiles and edges must remain equal.
   This is necessary changed-boundary validation, not rerunning the old graph
   unchanged. Stop on any unexplained difference; no opportunistic lock update.

4. Run one separately selected offline, locked release build with the existing
   build-std options, guest flags and fresh map/output destinations. It may
   recompile dependencies. For any optional private-cache seeding, use genuine
   independent copies or a proven copy-on-write facility; never hardlink mutable
   Cargo files or use the old target directory as a writable target. No such
   cache optimization is currently proposed for implementation.

5. Record actual new compiler commands during this build (e.g. reviewed bounded
   verbose logging), plus artifact identities, generated build-script inputs and
   outputs, feature/profile graph and final ELF/map. This prevents today's missing
   recipe problem from recurring. Enforce enough bounded log space for the
   selected297-unit build rather than silently truncating required provenance.

6. Check only the explicitly selected input closure and new output tree at
   finalization. Do not repeatedly traverse every historic experiment, registry
   source tree, SDK example, debugger file or PDB. Reuse adopted prior evidence
   for unchanged provenance while explicitly rebinding bytes actually selected
   as new compile inputs. A retained manifest hash alone does not prove current
   files still match it. Resource bounds and finalization get their own budget.

Record the finished ELF and map separately from success of the entire resource
operation. A resource failure must remain a failure even if a later independent
operation adopts a usable artifact, as already done for the predecessor.

## Adoption and cost stop conditions

The original full dependency build's222.640625 worker CPU seconds provides a
useful scale estimate, not an upper bound for new work. Its large repeated
controller census/rebind cost is the obvious avoidable build-workflow overhead.
No numerical speedup or smaller guest cycle count follows from this plan.

The six bounded-parse files select only the new aggregate guest's embedded module
relation. They do not require recompiling or relabeling the existing standalone
module receipt image I. A new aggregate ELF/image A needs explicit policy
adoption; old receipts cannot be relabeled with its image. Whether to produce
multiple images or certificates at all remains root's separate investment choice.

Before implementation: root reads/adopts this plan, native outcome and image/cost
decision; assurance checks the exact source/graph/build contract. Before runtime:
root selects fresh source pins, destinations, input closure and finite resources.
Before any proof: separately inspect new guest execution/cost evidence. None of
these later gates is silently selected here. All original failures/artifacts stay
preserved, and a successful guest build is not final v5 or mathematical admission.

## Concrete source/API proposal, awaiting root approval before implementation

Root read/adopts the feasibility direction and assigns fresh source only under
`software/v5/bounded_parse_guest/`. Assurance independently read the original
15,211-byte plan at `9ae754e609af53266f9e7fa2ad21adaf7923426bd663d64c2b94f5ad3c69c1d3`
and found no conceptual blocker. The following details need root's approval;
no builder or new manifests have yet been written by this author.

### Five new files; exact project snapshot

| Owned new file | Responsibility |
|---|---|
| `Cargo.toml` | Same aggregate package/version/dependencies/profile; `[lib] path="../bounded_parse/aggregate_lib.rs"`, unchanged bin at `../aggregate/main.rs` |
| `module/Cargo.toml` | Same module package/version/dependencies; `[lib] path="../../bounded_parse/module_lib.rs"` |
| `checker/Cargo.toml` | Same checker package/version/dependencies and `../../modules/native/proof_validation/lib.rs` target |
| `graph.py` | Pure strict graph relocation/equality and deterministic lock/graph cache-input selection; no subprocess or import-time filesystem work |
| `build.py` | Root-selected bounded graph/build controller, explicit input manifest, private state, before/after rebinds and final artifact accounting |

The snapshot has exactly32 Rust source files: six reviewed bounded_parse files;
six unchanged receipt input/foundation_static/foundation_data/commitments/journal/
policy files; three aggregate header/membership/wire files; unchanged aggregate
main; fourteen checker/src files; and proof_validation lib/module_correspondence.
With the three manifests and two adapters this is37 selected authored/reused files.
The38th file is the exact47,716-byte old aggregate Cargo.lock, SHA-256
`13381f3226dfb40e766fda448adaa4a75f407da0d31114964d1278991a6f1b7c`.
No old lib/relation/canonical/census files, native driver, test controls or old
builder are copied as project compilation inputs. Existing `cfg(test)` references
are harmless in the selected release build and do not justify copying tests.

Before compilation, all new wrapper lib/main paths must resolve to exact files
inside the fresh project snapshot. No old project root may survive in those
source targets. Three local package IDs relocate; four target source paths have
explicit expected lexical spelling. The std/SDK source roots remain unchanged.

Proposed pure APIs are `expected_graph(old_graph, new_run)`,
`verify_graph(old_graph, new_graph, new_run)`, and
`cache_inputs(old_graph, project_lock_bytes, std_lock_bytes, retained_seed_map)`.
The first two retain whole-graph canonical equality including all edges/profiles,
allowing only the explicit local package/source-root and private-cache relocation.
They require297 units and unchanged1.0.151/default,std serde_json semantics.
The third uses strict TOML parsing at runtime, not regex extraction, and returns
an exact relative-path-to-pin map with counts and bytes.

### Exact private Cargo cache:359 files, no Git

Read-only record analysis gives:

- 160 registry versions occur in the297-unit compiled graph. All160 matching
  archives are in the retained seed, totaling13,640,297 bytes. Each archive's
  recorded digest must equal its matching retained lock checksum.
- The project and std lock union contains220 registry versions but198 distinct
  package names. Copy one sparse-index cache entry for each of these198 names,
  totaling9,755,696 bytes, plus the exact registry config.json. The standard
  Cargo name-to-index-path rule determines each path; no directory wildcard.
- Neither lock nor the graph selects a Git package. Copy no git/checkouts/db data.
- 40 inactive locked-version archives are absent even in the old seed. They were
  unnecessary for the successful old target. Do not require all220 archives;
  retain all198 names' index metadata for offline resolution and only the160
  actually compiled versions' archives. Unexpected additional dependency demand
  is a bounded refusal, never permission to fetch or expand the selection.

All359 source paths already exist in the pinned
`experiments/general-checker-guest-03/prepare-03/CARGO-HOME.json` seed map. The
controller derives this exact set from the fixed graph/locks, validates the
counts/aggregate sizes, then copies with fresh-exclusive creates into private
CARGO_HOME. It records byte/digest checks on source and destination. Cargo performs
normal bounded private extraction. No registry/src tree, old target, full index
or old history is copied. Root accepts this359-file selection principle.

### Read-only SDK, std and tool closure

Select13 SDK package-root subtrees derived from the saved graph: binfmt,
build_kernel, circuit/{keccak,recursion,rv32im,rv32im-sys}, core, groth16,
zkos/{common,v1compat}, zkp, zkvm and zkvm/platform. Add all SDK Cargo.toml files
for resolver metadata and root Cargo.lock/config/toolchain metadata when present.
Selecting from the retained map, not recursively recopying the tree, gives982
files/43,906,906 bytes. Preserve complete selected subtrees, including generated
templates/circuit/kernel assets, not only .rs files. Any independently identified
cross-subtree include/build input must receive an explicit additional retained
pin before selection; it must not be silently omitted or used to justify an
unbounded whole-SDK census.

The selected std source map has2192 files/37,544,099 bytes, including its exact
lock and workspace/build metadata. Reuse it in place, read-only; do not duplicate
the std snapshot. This bounded compile-input set is distinct from the unrelated
registry/SDK/history trees previously repeatedly traversed.

Select the retained compiler executable/dlls, Cargo, rust-lld and host rustlib
.rlib/.rmeta files:27 entries/423,009,292 bytes from the recorded124-entry runtime
map. Exclude PDBs, debugger/documentation files and unused tools. Bind the existing
rustfmt executable pair, clang plus its two DLLs, exact MSVC/Windows host-link
library pins from the retained build recipe, and recorded cl/link/rc tools. Reuse
the existing supervised helper chain and Windows OS/system-DLL trust boundary;
do not advertise this as a hermetic toolchain or hostile-build-script sandbox.

Implementation must preserve source/input rebinds before and after. Each rebind
walks these explicit map entries, not recursive `retained()`/`runtime_map()`/
`cache_seed_map()`/whole-SDK enumeration. Project/cache copies can be verified as
they are written; final identity checks retain hashes, not only mtimes. During
worker execution, `budget.refresh()` censuses **only the new run tree**, never
historical SDK/std/cache/experiment trees.

### Controller contract and budgets

Proposed root selection schema: `DMKN_V5_BOUNDED_PARSE_GUEST_BUILD_V1`, containing
name `bounded-parse-guest-build-NN`, exact37-file `sources` map, exact limits,
native-comparison RESULT pin, and explicit build/owned-telemetry-cleanup boolean.
Fixed retained record hashes in the adapter identify graph, lock, source/seed/tool
maps and successful native build02/comparison lineage. Require the adopted ten-
control/two-native comparison status and bind the six production pins through
its build/source-map lineage, not merely a free-standing PASS string.

Two Cargo invocations only: one `--unit-graph -Z unstable-options` with the existing
release/bin/target/build-std/locked/offline options; after exact equality, one
offline locked release build with `-vv --message-format=json`. Use explicit
no-credential environment, private TEMP/TMP/profile/CARGO_HOME/target, existing
guest flags and fresh link map. Bounded verbose stderr retains actual compiler
commands; structured stdout retains all actual artifact/build-script messages.
No command logs may be silently truncated while claiming complete recipes.

Proposed fresh finite allocation:

| Resource | Limit and basis |
|---|---|
| Shared graph/build worker CPU |480 seconds, a little over twice the retained222.64-second full compile; a finite engineering allowance, not a proven runtime bound |
| Shared worker wall |600 seconds including graph and build; no reset between commands |
| Job memory/active processes |4096MiB/eight, preserving the previously working compile profile; old observed peak about1.20GB |
| Controller CPU |90 seconds total; stop ordinary work at70, reserving20 for final input checks, output census, report and closure |
| Total wall including preparation/finalization |780 seconds, with no retry or renewed deadline |
| Fresh output tree |3GiB/32,768 entries, versus old982,259,007 bytes/13,261 entries; no repeated historical-tree charge/census |
| Per-command combined logs |32MiB, ample bounded headroom for297-unit verbose recipes; exceedance refuses rather than truncates |

Controller rebind/output costs are charged separately from inclusive worker Job
CPU. Source pin/copy loops check controller limits between bounded entries. At
finalization, require quiescent closed Job, exact source/cache/tool rebind, unchanged
lock, completed single-bin Cargo artifact, bounded ELF/link map, saved graph/command
evidence and final budgets. Save result/attempt by fresh-exclusive
creation; a last-tail overrun gets an overriding failure marker. No new budget
is created on failure and no partial pass licenses assembly or proof.

These numbers are a source proposal for root/reviewer judgment, not runtime
selection. Root owns later exact launch and any new-image/proof investment.

## Approved source implementation, ready for independent review

Root read and approved the complete contract above for source implementation;
assurance separately cleared that contract. Five fresh files now implement it.
No Python project import, Cargo/compiler call, test, guest execution, proof,
cache change or Git operation was performed by this lane. Actual execution and
adoption remain root-owned, separately selected work.

| Fresh file under `software/v5/bounded_parse_guest/` | Bytes | SHA-256 |
|---|---:|---|
| `Cargo.toml` | 751 | `7eaa23cdc5aaf4c8fd1b8e1924a1cb4f702d7af8d04cdd06a33df23dfa5c0ad1` |
| `module/Cargo.toml` | 570 | `0435d18fdfb878290b291e62978643975fe2887c79873f50d6d4fa7332dba15c` |
| `checker/Cargo.toml` | 438 | `56364af430400d805de9be09d842b70e2f3bc3de9a14ff8082b18bcbcc1ff543` |
| `graph.py` | 8668 | `090744c1b479474399912c2180e8cca8e1e12afe050689f6c310af4c57136c87` |
| `build.py` | 24272 | `514b5f743ee7acef21c02719d98aa2b910e67a4966231527a1d4b83ac450f584` |

The pure graph APIs remain exactly `expected_graph(old_graph, new_run)`,
`verify_graph(old_graph, new_graph, new_run)` and
`cache_inputs(old_graph, project_lock_bytes, std_lock_bytes, retained_seed_map)`.
Internal canonicalization replaces dependency indices with full target
identities; it tolerates ordering changes but no package/feature/profile/edge
change. The four explicit project targets preserve Cargo's lexical `..` spelling.
Only the two library source roots, three local package directories, four local
source paths and private Cargo cache location change. No pre-normalization of
arbitrary target paths hides an unexpected graph difference.

The prospective root-only entry point is:

```text
D:\Python314\python.exe -I -B -S <canonical-root>\software\v5\bounded_parse_guest\build.py <selection-path> <selection-sha256>
```

It accepts only `DMKN_V5_BOUNDED_PARSE_GUEST_BUILD_V1`, with the six exact fields
specified above. `sources` has the fixed37-file key set, each value exactly
`{"bytes": ..., "sha256": ...}`. The `limits` object is exactly the source's
`LIMITS`. The name matches `bounded-parse-guest-build-[0-9]{2}` and both its fresh
run directory and attempt marker must be absent. `native_comparison` is exactly:

```json
{
  "path": "E:\\Distributed Trustworthy Mathematical Knowledge Network\\experiments\\v5-local-checks\\bounded-parse-native-compare-01\\RESULT.json",
  "bytes": 8960,
  "sha256": "ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20"
}
```

The builder pins native build02 RESULT/source-map and its original and saved
selections. These selections have equal JSON values but different byte hashes
because the existing build adapter reserialized its saved copy. Therefore the
new builder compares JSON equality while separately binding the original
selection's hash to native RESULT; it does not falsely require byte equality.
The six production source pins and every unchanged source available in that
native map are bound to that lineage. Native/compare attempt markers and absence
of overriding finalization failures are required again at finalization.

### Closure and supervision implementation

The source enforces the approved38 snapshot files,359 cache files,982 SDK files,
2192 std files and27 compiler entries, including their approved aggregate sizes.
It additionally binds98 exact existing host-tool/link-library digests from the
retained native recipe, the old guest profile's rustfmt executable pair,
clang+two DLLs, cl/link/rc, Python/DLL and all actually imported supervisor helpers.
`INPUT-MAP.json` records the resulting absolute-path byte/digest manifest;
`SOURCE-MAP.json` records the fresh project map and four resolved target paths.
No runtime hash is inferred merely from an executable name.

The SDK include/build inspection found no missing active cross-subtree input:
the library README, assembly, v1compat ELF and circuit `.inc` inputs are inside
selected subtrees. In the unchanged non-prove graph, rv32im-sys preprocesses only
`cxx/rv32im/witness/block_types.h` and `cxx/rv32im/base/rv32im.inc`; neither has
another `#include`. Build-kernel's embedded metal headers are inside its selected
subtree. Prove-only GPU/kernel/zkr generation branches are not activated by this
graph. This is a source inspection, not a hermetic read-access proof; independent
review must still challenge the selected-input boundary.

One narrow strengthening beyond the original prose is included: the builder
requires Cargo `config`/`config.toml` absent along every workspace ancestor and
inside the fresh private Cargo home, recording those absences in INPUT-MAP.
The existing nonfresh ancestors were checked read-only and are currently absent.
The pinned SDK's own `.cargo/config.toml` remains selected resolver metadata;
the Cargo invocation working directory is the fresh wrapper, not SDK.

The single worker Job has a480-second native user-time cap and4096MiB/eight
processes. A local `InclusiveJob.stats()` override additionally enforces480
**inclusive kernel+user** CPU seconds at every existing phase polling point
(approximately0.1-second intervals), and finalization checks that same bound.
This distinction repairs an independent-review finding: the frozen phase helper
otherwise compares inclusive CPU against its600-second wall setting. The new
wrapper does not change frozen helper bytes. Polling can observe a small overrun;
any observed or final overrun refuses, rather than claiming a strict zero-overshoot
OS guarantee. Finalization reads raw stats to permit cleanup and failure evidence.
Both commands use that same Job and the same600-second phase clock. Ordinary
controller checks stop at70CPU seconds; finalization uses the same starting CPU
counter with a90CPU ceiling. The780-second total wall deadline never renews.
Output census is restricted to the new run tree and enforces3GiB/32768entries;
per-command combined logs are32MiB and are never silently truncated. The build
adds `-vv --message-format=json` so actual recipes are retained this time.

Before and after compilation, exact selected inputs are hashed individually;
the copied project and cache seeds are also rebound. Finalization closes the
Job, requires quiescence and the480CPU cap, checks unchanged locks/source/cache,
then creates RESULT and attempt by exclusive writes. A last-tail overrun creates
an overriding FINALIZATION-FAILED marker; no partial success licenses proving.
The source uses none of the old whole-SDK/history/runtime/cargo-seed census
helpers. A successful operation means only
`PASS_BOUNDED_PARSE_EXACT_GRAPH_GUEST_BUILD_ONLY`, not v5 completion or image,
receipt, cost or mathematical acceptance.
