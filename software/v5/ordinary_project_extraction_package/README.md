# Approved local-project proof completion

This is a v5 development path, not the final release. The currently selected
package and its exact evidence are linked from
[`ordinary_distribution/CURRENT.md`](../ordinary_distribution/CURRENT.md).

## What it adds

A contributor can author a proof using a normal Lean project. If the receiving
commons lacks an imported lemma, the retained contribution reports the missing
names. `extract-project` can recover their complete proofs from locally approved,
already compiled modules. `complete` then independently checks the resulting
extension. Neither an imported binary nor an extraction success is mathematical
authority for the receiver.

The workflow is:

1. Use `contribute` with an explicitly approved authoring project. Keep its
   retained files if the result needs missing interpretations.
2. Select only the compiled module roots needed to find those missing proofs.
3. Run `extract-project` on that exact retained candidate and the same parent.
4. Run the existing explicit `complete` operation with the returned pinned
   candidate, supplement, prepared bindings and original output names.

Do not rerun authoring simply to recover an already retained proof. Do not change
the parent in step 3 or 4. An accepted result on a different branch is not an
implicit rebase permission.

## Local selection document

The document has exactly three fields:

```json
{"modules":[[[0,{"$bytes":[77,121,76,105,98]}]]],"project_search_paths":["E:/MyProject/.lake/build/lib/lean"],"schema":"DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1"}
```

The module in this example is `MyLib`. Names are structured Lean names, not
source strings. Supply canonical UTF-8 JSON (sorted object keys, compact
separators, no trailing newline) and its exact SHA-256. The local operator selects
these bytes; a peer must not select executable support through a candidate.

There are at most 16 ordered search roots and 16 modules. The supported path
profile is ordinary absolute Windows drive directories, without redirects,
dot components or search-list separators. Modules use ASCII identifier
components, not paths. See the exact
[contract](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PROJECT-INTAKE-NATIVE.md)
for grammar and limits. Paths must contain compiled private artifacts produced
by the supported Lean 4.34.0 toolchain. This command never invokes Lake, downloads
dependencies, compiles project source or enables imported plugins/extensions.
The installed runtime search root precedes the approved project roots.
Project module components may contain up to 96 ASCII bytes; the existing
installed-Std mode retains its 64-byte component limit.

The public operation adds these explicit arguments to the existing owner options:

```text
extract-project
  --parent-root <unchanged receiving context>
  --retained-contribution <retained directory>
  --retained-request-sha256 <REQUEST.json hash>
  --retained-candidate-sha256 <candidate.json hash>
  --project-extraction <selection JSON file>
  --project-extraction-sha256 <exact selection hash>
  --output <fresh directory>
```

The usual profile, runtime, catalog, custody, store and resource-limit options
remain required. Run the packaged `owner.py` with supported Python `-I -S -B`.
`--library-modules` remains exclusive to `extract-std`; authoring selection is
not extraction selection. Do not run this standalone source file as if it were
a packaged installation.

## Concrete extraction and completion commands

Start with an already initialized, locally approved node and an actual retained
`CONTRIBUTION_CANDIDATE_NEEDS_INTERPRETATIONS` result. The paths below are examples:
replace them and the identity placeholders with your selected installation
and existing store. Do not invent a new store ID or take the package/profile
selection from a peer. Use the exact parent of the retained request, not the
latest catalog head. The working directory must exist; `extracted` and
`completed` must not yet exist. Do not run another operation on the same owner
concurrently. These commands are documentation, not a request to repeat a saved
research allocation.

```powershell
$commonsPython = 'D:\Python314\python.exe'
$commonsPackage = 'E:\MathCommons\package'
$commonsRetained = 'E:\MathCommons\work\retained-contribution'
$commonsSelection = 'E:\MathCommons\approved-project-extraction.json'
$commonsExtracted = 'E:\MathCommons\work\extracted'
$commonsCompleted = 'E:\MathCommons\work\completed'
$commonsParent = '<exact retained parent root>'
$commonsCommon = @(
  '--profile-sha256', '<locally approved package PROFILE.json SHA-256>',
  '--python-runtime', 'D:\Python314',
  '--lean-runtime', 'E:\Runtimes\lean-4.34.0-windows',
  '--catalog', 'E:\MathCommons\state\catalog',
  '--custody', 'E:\MathCommons\state\custody',
  '--store-id', '<existing store ID>',
  '--custody-limits', 'E:\MathCommons\custody-limits.json',
  '--parent-root', $commonsParent,
  '--wall-seconds', '90', '--cpu-seconds', '60', '--memory-mib', '1536'
)
$commonsRequestHash = (Get-FileHash -Algorithm SHA256 -LiteralPath "$commonsRetained\REQUEST.json").Hash.ToLowerInvariant()
$commonsCandidateHash = (Get-FileHash -Algorithm SHA256 -LiteralPath "$commonsRetained\candidate.json").Hash.ToLowerInvariant()
$commonsSelectionHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $commonsSelection).Hash.ToLowerInvariant()
& $commonsPython -I -S -B "$commonsPackage\owner.py" extract-project @commonsCommon `
  --retained-contribution $commonsRetained --retained-request-sha256 $commonsRequestHash `
  --retained-candidate-sha256 $commonsCandidateHash --project-extraction $commonsSelection `
  --project-extraction-sha256 $commonsSelectionHash --output $commonsExtracted
if ($LASTEXITCODE -ne 0) { throw 'Extraction failed: preserve its output; do not continue.' }
```

The limits shown are finite examples, not a guarantee that a selected module
fits. Each explicit command is separately charged. Hashing the local selection
records which bytes you approved; it does not make untrusted artifacts safe.

Inspect `EXTRACTION-RESULT.json`. Only its successful inert result can supply the
next command's exact pins. Keep the same `$commonsCommon` parent and all files
unchanged. This second command is the separate mathematical admission step:

```powershell
$commonsExtraction = Get-Content -Raw -LiteralPath "$commonsExtracted\EXTRACTION-RESULT.json" | ConvertFrom-Json
if ($commonsExtraction.status -ne 'EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED' -or
    $commonsExtraction.mathematical_acceptance -ne $false -or
    $commonsExtraction.parent_root -ne $commonsParent) { throw 'Unexpected extraction result.' }
& $commonsPython -I -S -B "$commonsPackage\owner.py" complete @commonsCommon `
  --candidate "$commonsExtracted\candidate.json" --candidate-sha256 $commonsExtraction.pins.candidate.sha256 `
  --supplement "$commonsExtracted\supplement.json" --supplement-sha256 $commonsExtraction.pins.supplement.sha256 `
  --prepared-bindings "$commonsExtracted\prepared-bindings.json" `
  --prepared-bindings-sha256 $commonsExtraction.pins.prepared_bindings.sha256 `
  --output-names "$commonsExtracted\targets.json" --output $commonsCompleted
if ($LASTEXITCODE -ne 0) { throw 'Completion failed: inspect and preserve its result and any recorded admission.' }
```

For a successful completion, retain `RESULT.json`, `ADMISSION.json` and their
evidence. `CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES` means checked local
completion with reusable publication bytes; it does not mean those bytes were
automatically announced, replicated or made globally discoverable. Inspect any
recorded admission even on a later command failure; do not assume rollback.

## Source-complete build recipe

[`build.py`](build.py) and [`source-map.json`](source-map.json) define the clean
build from the repository source root plus complete supplied Windows Python
3.14.6 and Lean 4.34.0 distributions. The map pins 71 project inputs; the recipe
also pins/stages itself and the map. It builds receiver support, ordinary
authoring support, the extractor and the context-query command, then emits
134 payloads and `PROFILE.json`. It retains the module-anchor04 bridge and
context-bound query implementation.

The recipe accepts `--source-root`, `--python-runtime`, `--lean-runtime`,
`--output`, `--wall-seconds`, `--cpu-seconds` and `--memory-mib`; invoke it with
the selected Python `-I -S -B` and a fresh output directory. It needs no previous
installation, experiment directory, generated module or retained shared object.
Named runtime pins require the full distributions; they are not a hermetic
authentication of every toolchain file. No downloads occur.

The current changed-only development assembly reused exact paid-for helper
objects to avoid rebuilding them. That optimization is separate from the clean
recipe. The clean recipe is source-reviewed, **not newly executed here**, and
does not promise byte-identical native binaries across build locations. A fresh
build's `_build/BUILD-RESULT.json` and `package/PROFILE.json` describe its actual
outputs; build success alone does not adopt the package or qualify a node.

## What success and refusal mean

`EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED` means only that the resulting inert
inputs fit the unchanged completion planner. The next mathematical decision
belongs to `complete`. The exact original candidate, selected parent, target
names and claims remain bound throughout. Local selection metadata is not a
signature over every transitive project artifact and does not establish whole-
project semantic equivalence.

The combined public boundary remains 32 units, 4 MiB input and 131072 encoded
nodes. Project extraction receives the capacity left after the retained
candidate. It can refuse early on a full budget, or later when aggregate encoded
nodes, wrapper bytes or other final planner limits are exceeded. Failed work is
retained and charged; there is no automatic retry or silent quota increase.
Whole inductive groups stay indivisible. Missing private proof data, unsafe or
partial declarations, incompatible foundations and collisions remain refusals.

Importing a module may load its transitive private environment. This does not
make arbitrary cold library intake cheap. When collaborators need the same large
approved background, ordinary pinned-library sharing remains an important
default/comparator. This adapter targets a bounded missing extension; it is not
a generic bulk-ingestion scheduler or a measured useful-growth result.

The facade change deliberately changes module-anchor support identity. Existing
registered anchors are not silently migrated. The mathematical installation and
acceptance relation are otherwise unchanged; package integration and actual
runtime evidence must be recorded separately before adoption.
