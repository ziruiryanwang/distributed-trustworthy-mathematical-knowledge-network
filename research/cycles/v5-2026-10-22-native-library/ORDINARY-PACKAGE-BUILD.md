# Ordinary package builder: source-ready checkpoint

2026-10-23. Implements only the selected two-lane source build/package boundary.
No build, test, Python import, native/runtime launch, install or Git operation
was performed by this author. Existing core, assembler, authoring helper,
promoted source and old evidence bytes were not edited.

New source: `software/v5/ordinary_package/build.py`, SHA-256
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.
The root-owned `ordinary_package/INTERFACE.md` defines its output contract;
the detailed source audit is `ORDINARY-REPRODUCIBLE-PACKAGE-PLAN.md`.

## Entry point and exact inputs

Run with the explicitly selected Windows Python using `-I -S -B`:

```text
build.py --source-root REPOSITORY_ROOT --python-runtime PYTHON_DISTRIBUTION
         --lean-runtime LEAN_DISTRIBUTION --output FRESH_PACKAGE_ROOT
         --wall-seconds 360 --cpu-seconds 260 --memory-mib 2048
```

The numbers illustrate the root's proposed next finite validation, not a launch
authorization. `build(source_root, python_runtime, lean_runtime, output, *,
wall_seconds, cpu_seconds, memory_mib)` is the corresponding Python entry.
`SOURCE_FILES` is the sorted exact repository-relative source/asset selection;
`source_paths(source_root)` only constructs its absolute paths and performs no
IO/import/compilation. Root can use that list in its unchanged launch selector.

The source set includes the builder itself, unchanged assembler and six core
Python files, the two exact foundation assets, all required Lean inputs,
promoted receiver exporter and three supervisor files, six authoring Python
helpers, eight existing namespace-package support files, and the separately
owned `owner.py`, `profile.py`, `author_worker.py`. It never recursively copies
a repository. All inputs are hashed, copied to `_build/inputs`, read back and
checked again before completion. Executing an exact-byte builder snapshot is
allowed; its bytes must equal source-root's selected builder. A fresh output
may sit beneath the repository but cannot contain a selected input or overlap
either runtime. No build input is resolved from an old experiment/product path.

The four promoted historical inputs have fixed size/SHA assertions. The nine
named runtime files are fixed to the selected Lean 4.34.0/Python 3.14.6 bytes;
same-version alternate builds are refused, not automatically adopted. Complete
Lean/Python libraries remain externally supplied runtime premises. This is not
cross-platform support or hermetic toolchain attestation.

## Native and resource boundary

One child Python worker, under the unchanged selected `commons.supervise` and
`run_stage.Job`, compiles all modules sequentially:

- Receiver: OriginalExpr, OriginalDecl, CheckedExtension, LocalSnapshot,
  BootstrapSupport, preserved OrdinaryExport, BasisSnapshot,
  OrdinaryWorkflowWorker.
- Authoring: public OriginalExpr, OriginalDecl, CheckedExtension,
  BootstrapSupport, OwnerRebind, OwnerConstruction, OwnerUseCommand, current
  OrdinaryExport, SuccessorExport, SuccessorExportCommand,
  PortableOwnerConstructCommand, PortableConstructExportCommand,
  PortableContributionExportCommand.

The worker's `LEAN_PATH` contains only its current lane's fresh output directory.
Python/Lean environment variables are removed and PATH names only the selected
Python/Lean binary directories. Lean uses `-DElab.async=false`. It does not load
old helpers, invoke Lake or accept arbitrary module lists. The four public
source files use the exact existing header transform; expected generated hashes
are asserted and `_build/PUBLIC-SOURCE-MAP.json` records original/generated/body
hashes. No generated receiver-source substitution is made.

The original monotonic deadline starts before input staging and covers both
lanes, assembly and final profile commit. The one Job receives only the remaining
wall allowance minus a 25-second cleanup/finalization reserve and remaining CPU
minus two seconds. It bounds child-tree CPU, memory, active processes and logs.
No module receives a renewed allowance. Full observed Job CPU is charged once;
controller `process_time` already includes supervision-wrapper CPU, so that
wrapper value is not added twice. Failure retains final/last observations and
marks incomplete final worker accounting. The Python controller's CPU/wall
checks remain cooperative; a root-selected outer Job supplies hard containment
of the controller itself. Existing supervisor cleanup semantics are unchanged.

After clean child closure, each lane receives a flat exact-name census: all
required `.olean` files, only the approved `.olean.private`, `.olean.server`,
`.ir`, `.ir.sig` companions, bounded sizes, no other files/directories/redirects.
Actual companion outputs are inventoried rather than assuming exactly five per
module. Every authoring helper is pinned, including optional companions.

## Assembly and final marker

The unchanged assembler receives a fresh canonical plan and the original
absolute deadline. Installation layout remains `py/`, `lean-src/`, `lean-lib/`,
`foundation/`, `supervisor/`. Its `lean-lib` contains only the eight receiver
`.olean` files; authoring is adjacent, not added to the core schema.

The auxiliary payload is exactly the shared descriptor contract:
`authoring/helpers`, `authoring/py`, eight `support/` files and the three root
entry points. Sources/helpers/installed files and named runtimes are verified
before finalization. `PROFILE.json` has only the five agreed fields and
package-relative auxiliary paths, and is encoded with the existing evidence
canonical JSON function. It is written through a fresh same-directory pending
file and non-overwriting Windows rename, after all build/assembly receipts.
It contains no absolute build paths. Absolute provenance paths appear only in
excluded `_build` evidence. A failed build preserves partial output and never
retries, removes files, opens a mathematical owner or grants acceptance.

`BUILT_NOT_ADOPTED` means source compilation and assembly only. Fresh compiled
bytes/implementation identity are recorded; no promise of binary identity with
old retained helpers or migration of existing stores is made. Descriptor pins
identify owner-selected support, not peer evidence or mathematical truth.

## Proposed finite validation

Independent source review first, including the separately owned CLI/profile/
worker and the exact shared payload set. Root can then select one new clean
build under its proposed outer 420 wall seconds/300 CPU seconds/2048 MiB and
inner 360 wall/260 CPU/2048 MiB. This is a fresh package boundary, not a replay of
an old module campaign. Preserve the first outcome without automatic retry.

Audit its actual source map, four generated hashes, exact lane outputs,
supervision/CPU records, installation manifest/support groups, complete auxiliary
census, relative descriptor, and lack of retained helper dependencies. A separate
selected package-only init/status/caller-authored multi-output contribution is
the next lifecycle validation, not part of the build. No certificates, peer
service, old admission replay or large growth benchmark is needed for this gate.

## Independent validation-selector review

Reviewed root's `software/v5/ordinary_package/select_build_check.py`, SHA-256
`f33c2625d922d60a3215a1f60867ee0b7850877bb935e663da054ac20bb8dadc`.
Source-only; neither mode, build, lifecycle nor an import/test was executed here.
No remaining selector blocker identified after the following pre-use corrections.

The build branch calls the builder's exact `source_paths(ROOT)` and fixed
runtime-pin table, uses the agreed CLI, and pins every canonical source input
as a runtime attachment, including both foundation assets outside the preserved
runner's v5 snapshot scope. Reading `tools/Run-V5-Check.py` confirms those root
paths are verified before and after the child; v5 source snapshots are also
checked after execution. The builder separately verifies source and staged bytes.
The corrected outer build envelope is 420 wall seconds/300 CPU seconds/2304 MiB,
above the unchanged inner 360 wall/260 CPU/2048 MiB; no grant is renewed.

The initial lifecycle selector trusted profile keys without enforcing the
package payload allowlist, read descriptors before bounding them, and lacked
a per-write growth cap. Root corrected these before use. The reviewed version
bounds/pins descriptor reads first, rejects duplicate keys, checks exact profile
fields/layout and required/allowed auxiliary modules, and requires the exact
installed payload names. It validates pin types, 128 MiB per-file and 256 MiB
aggregate bounds before creating the fresh destination. Every copy is capped
at its pinned size before writing and is hash/size checked afterward.

Relocation therefore selects only the runtime payload: it cannot include
`_build`, source snapshots or owner/catalog/custody state. The eight required
installed `lean-src` files remain intentional receiver payload, not a dependency
on the repository. Runtime distributions stay external; each relocated payload
gets a before/after outer-run pin. Fresh exclusive outputs preserve a partial
copy on failure; neither branch launches a command, deletes data or retries.
This review covers selector binding/copying, not the separately reviewed
builder/CLI/lifecycle semantics or any actual runtime result.
