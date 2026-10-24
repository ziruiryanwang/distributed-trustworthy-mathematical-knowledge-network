# Narrow baseline native build: source-only checkpoint

2026-10-24. `cold_intake_strategy`, under root's changed-native build adapter
selection. Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`;
the workspace guard passed. This assignment owns only `build_native.py`,
`select_native_build.py` and this checkpoint. Root owns all selections, launches,
Git and actual adoption. Neither new script has been imported or invoked; no
compiler, linker, binary import, test, owner/database or package operation ran.

## Why this build, and what it excludes

The next decision-changing integration requires the selected baseline exporter,
artifact collector and original-library correspondence matcher. Existing shared
Lean codec/export helpers already have a successful build. Recompiling those
helpers, rebuilding a whole package or replaying a large proof closure would not
resolve this changed-native boundary more efficiently.

The adapter stages the ten exact preserved `.olean`/`.o` files for
`OriginalExpr`, `OriginalDecl`, `CheckedExtension`, `BootstrapSupport` and
`OrdinaryExport`. It compiles only four new modules and links three executables.
It does not run any resulting executable, collect a user's library, replay an
artifact map, match declarations, initialize/open an owner, admit mathematics,
assemble a package or install a profile. Compilation necessarily imports the
explicitly selected shared objects and generated core; this is not arbitrary
library import or a native acceptance operation.

## Source and preserved input identities

| Source below `software/v5/ordinary_baseline/` | SHA-256 |
|---|---|
| `build_native.py` | `a2d2b12aa7ee9d3890ca307d3a71d6d22ad0a7274f1fe3da14e93bbbc984a868` |
| `select_native_build.py` | `bf11621bc9228cf602d5e707f4481264d731ec03065d1e2614c5dd204da226f9` |

Only the frozen `software/v5/ordinary_package/build.py` is imported for its
ordinary-path, exact-pin and fresh-write helpers, at
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.
The adapter has no dependency on previous package assembler/loader chains.

Shared object origin:
`experiments/v5-local-checks/ordinary-current-source-build-01/distribution/_build/extractor-objects`.
Its adjacent `EXTRACTOR-OUTPUTS.json` must equal
`f55d4c5b56fc299564b76d68c66d63d3090f439b44479b597b016113c4b53768`.
Only the ten named `.olean`/`.o` entries are reused; old generated C and executables
are not staged, compiled or linked.

Named runtime/toolchain pins are selected from the preserved
`ordinary-current-source-build-01.selection.json`, hash
`97a4c0d19aea620d067f9cf2a227706fd460654bf06b978cc201a2b7b2e8790b`.
Exactly 23 selected runtime files must match. Python, `lean.exe`, `leanc.exe`,
`clang.exe` and `ld.lld.exe` are required explicitly. These are named adopted
toolchain inputs, **not a complete transitive runtime authentication claim**.

Eight source files are pinned and snapshotted: the adapter, selector, four new
Lean sources, frozen builder and existing `tools/Run-V5-Check.py`. With the ten
shared objects, 23 toolchain files and two preserved manifests, the expected
input map is 43 files. Original inputs and snapshots are rehashed independently
before compilation and again after the build.

The mutable native draft hashes are intentionally not constants in the adapter.
The selector requires explicit `--build-sha256`, `--exporter-sha256`,
`--core-sha256`, `--collector-sha256` and `--reference-sha256`, verifies them
against the files actually read at selection time and rehashes all inputs before
creating the selection. Root must supply the **final reviewed** four native
hashes; this checkpoint does not select a still-changing matcher.

### Proposed exact operator invocation, not executed

Run only after root's final selection, from the canonical working directory.
The current source candidate values communicated by the native author are below;
any source change requires rereview and replacement with its actual final hash.

```powershell
& 'D:\Python314\python.exe' -I -S -B '.\software\v5\ordinary_baseline\select_native_build.py' --build-sha256 a2d2b12aa7ee9d3890ca307d3a71d6d22ad0a7274f1fe3da14e93bbbc984a868 --exporter-sha256 403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e --core-sha256 6f160a089fd6e60c34654f7f90417155a94d921a78d7884dec949e4379fd5f28 --collector-sha256 78abf44c6b2b17e065a03550e5b1af0dbc7020a8d7100bc7312832c73e3ddff7 --reference-sha256 5120d6bb7939e32b2c2cd45981dde015d9e041fd9d7a05e11cc453ce5fd3b30a
```

That command only prepares the selection. The separately authorized runner CLI is
`D:\Python314\python.exe -I -S -B tools/Run-V5-Check.py <absolute-selection-path> <exact-emitted-selection-sha256>`.
Its selection path is
`E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\ordinary-baseline-native-build-01.selection.json`.
Do not substitute an invented selection hash. Both stdout and stderr remain
inherited by the outer runner and are bounded at 1 MiB each; command summaries
and compiler diagnostics use those same logs, with no unbounded per-command log
copies. Neither invocation has been performed by this assignment.

## Exact compile and link boundary

| Module | Compilation | Linked candidate |
|---|---|---|
| `BaselineExporter` | `.olean`, generated `.c`, compiled `.o` | Shared five `.o` plus `BaselineExporter.o` |
| `BaselineArtifactCore` | `.olean`, generated `.c`, compiled `.o`; no `main` | Shared by the two following candidates |
| `BaselineArtifacts` | `.olean`, generated `.c`, compiled `.o` | Shared five `.o`, core and collector `.o` |
| `OrdinaryReferenceBase` | `.olean`, generated `.c`, compiled `.o` | Shared five `.o`, core and matcher `.o` |

The resulting fixed set is 15 files: four triples plus three `.exe` files.
The command sequence contains exactly 11 commands: four Lean code generations,
four C object compilations and three links. It uses the existing `leanc -O0`
object and `-leanshared` link pattern, with `Elab.async=false`. Builds are serial
within one finite Job to avoid a needless scheduler or extra peak memory.
Only newly compiled object and copied shared-object directories enter
`LEAN_PATH`; runtime `bin` supplies `PATH`. Inherited language/environment search
variables are removed. Standard Lean runtime lookup remains the named-runtime
premise, not a hermetic build claim.

The native author confirmed the matcher imports only `BaselineArtifactCore`
and the existing shared closure; there is no `OwnerRebind` or extra helper.
The selected sources currently use the legacy non-`module` output form. An
unexpected companion or unselected output refuses rather than being silently
added to the build. This is a boundary to verify in the actual first build,
not a claim that compilation has succeeded.

## One original budget and finite output

The selector proposes a distinct `ordinary-baseline-native-build-01` under the
existing `Run-V5-Check` runner: maximum 240 wall seconds, 180 inclusive CPU seconds,
1536 MiB and six active processes. It does not run the selection. Root's explicit
runtime decision remains required after final matcher/source reviews.

The adapter has cooperative checks at 210 wall seconds and 150 controller CPU
seconds. Every subprocess timeout uses the remaining time to that **same**
original deadline; no command creates or renews a grant. All compiler/linker
descendants inherit the one enclosing Job. Inclusive CPU/memory/process accounting
and final process closure are taken only from its actual saved result, never
inferred from this adapter's elapsed time or a child exit code.

Per generated file: 32 MiB. Aggregate generated files: 256 MiB. Shared copies:
128 MiB aggregate. Staged native source: at most 8 MiB. Metadata files are each
bounded by 2 MiB, with a cooperative 384-MiB spool authorization. Preflight
requires room for exact staged inputs plus the complete generated-file ceiling
and 6 MiB of normal metadata. Exact output-set/size checks follow each successful
command. These are sampled/cooperative checks, **not a hard during-execution
disk quota**. A failing compiler can leave partial output; it is preserved.

## Exact copies, completion and failures

The fresh build has `source/`, `shared/` and `objects/`. Every staged file is
stream-copied with source/copy hash and byte-count verification. `INPUTS.json`
records original sources, snapshot locators, exact shared/toolchain maps and
resource scope. `NATIVE-OUTPUTS.json` records all 15 generated pins.

Before final `BUILD.json`, the adapter rechecks all original inputs, all eight
source snapshots, staged native sources, copied shared objects, generated files,
metadata and exact directory censuses. The final receipt says
`BUILT_CANDIDATES_NOT_INSTALLED_OR_ADOPTED`; it is not a mathematical acceptance
or transferable certificate. A successful live return is still only a candidate
build, pending the outer Job outcome and independent saved-evidence review.

Failure writes a bounded best-effort `BUILD-FAILURE.json`, preserves partial
objects and completed-command observations, and never retries or asserts child
closure/rollback. A failure during the final receipt explicitly records that the
receipt may exist. Root must inspect the actual outer outcome rather than infer
success from a saved filename/status. No cleanup, old allocation renewal or
automatic next executable run follows this adapter.

## Remaining authority and next boundary

Independent engineering/source review is requested for these exact two files.
The matcher still requires its separate engineering and soundness reviews.
No selector invocation or actual build is commissioned by this note. Root may
then select one bounded build and audit its exact outputs. A small native
producer/collector/correspondence integration, protected registration and ordinary
delta use remain distinct work; this build must not be promoted into v5 delivery.
