# Exact-module investigator route, through received vocabulary

2026-10-26. Source-traced recipe, **not an executed end-to-end trial**. This guide
stops at the first missing turnkey operation: bounded type-only source extraction
over a received module. Approved ordinary Lean plus an external supervisor can
perform it; there is no missing mathematical protocol. The separate
[integration contract](../ordinary_received_query/CONTRACT.md) is pending.

## Inputs and distribution boundary

Start with an explicitly approved **current source checkout** and approved
Windows x86-64 Python 3.14.6 and Lean 4.34.0 distributions. No existing mathematical
Lean project is needed. The checkout must include the bounded builder, the four
predecessor overlay sources/maps, and this folder's `assemble.py`, `OVERLAY.json`
and three selected payloads. Preserve them on owner-controlled storage.

The verified workflow source ZIP does **not** include these newer exact-module
files or the fixed-basis query companion. Its manifest does not validate an
augmented extraction. No new archive/union verifier is supplied here. The current
checkout is an explicit approved input, not a claim of portable compact delivery.
No historical experiment installation, PROFILE or private state is required.

Select paths before executing anything. Existing parents, source and runtimes
are required; every output/diagnostic/state leaf below must be absent. Use
ordinary absolute local-drive paths without redirects/shared hardlinks, with
outputs outside support/state/input paths. Follow the
[launcher separation and execution boundary](../ordinary_bounded_operations/LAUNCHER.md).
Hashes select bytes, not an author or permission to execute arbitrary code.

```powershell
$exactPythonRoot = 'C:\tools\Python314'
$exactPython = "$exactPythonRoot\python.exe"
$exactLean = 'C:\tools\lean-4.34.0-windows'
$exactSource = 'C:\approved-commons-checkout'
$exactBuilds = 'C:\commons-builds'
$exactWork = 'C:\commons-work'
```

All allowances are examples, not success promises. Preserve failures and partial
outputs; do not automatically retry, renew a grant or edit expected pins.

## Build, four base overlays, then the exact overlay

Build once through the existing public entry:

```powershell
& $exactPython -I -S -B "$exactSource\software\v5\ordinary_bounded_operations\build.py" `
  --source-root $exactSource --python-runtime $exactPythonRoot --lean-runtime $exactLean `
  --output "$exactBuilds\native-01" --wall-seconds 600 --cpu-seconds 600 --memory-mib 2048
if ($LASTEXITCODE -ne 0) { throw 'Inspect the retained failed build.' }
$exactBuildReceipt = "$exactBuilds\native-01\_build\BUILD-RESULT.json"
$exactBuilt = Get-Content -Raw -LiteralPath $exactBuildReceipt | ConvertFrom-Json
```

Require `status = BUILT_NOT_ADOPTED`, `package = <native-01>\package`, a matching
actual package PROFILE SHA-256 and successful retained build/closure diagnostics.
The receipt is written before PROFILE, so receipt existence alone is insufficient.
Select/approve the successful actual build, not its historical example hashes.
Apply fair overlay with that **build** receipt:

```powershell
$exactBuildReceiptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $exactBuildReceipt).Hash.ToLowerInvariant()
& $exactPython -I -S -B "$exactSource\software\v5\ordinary_fair_search\assemble.py" `
  --source-root $exactSource --base-package $exactBuilt.package `
  --base-profile-sha256 $exactBuilt.profile_sha256 `
  --base-build-receipt $exactBuildReceipt --base-build-receipt-sha256 $exactBuildReceiptHash `
  --output "$exactBuilds\fair-01" --wall-seconds 120 --cpu-seconds 90
if ($LASTEXITCODE -ne 0) { throw 'Inspect the retained fair assembly.' }
```

Next apply the following rows **one at a time**, not automatically after failure:

| Source directory under `software/v5` | Immediate predecessor output | Fresh output |
|---|---|---|
| `ordinary_contact_federation` | `fair-01` | `contact-01` |
| `ordinary_sparse_access` | `contact-01` | `sparse-01` |
| `ordinary_transport_release` | `sparse-01` | `transport-01` |
| `ordinary_exact_module` | `transport-01` | `exact-01` |

Set these three variables to one row. For its predecessor require successful
terminal exit and `ASSEMBLY.json.status = ASSEMBLED_NOT_ADOPTED`, matching actual
`package` and PROFILE bytes. Review the selected overlay source/map, then use:

```powershell
$exactStage = 'ordinary_contact_federation' # Replace with one row above.
$exactPrevious = 'fair-01'
$exactNext = 'contact-01'
$exactReceiptPath = "$exactBuilds\$exactPrevious\ASSEMBLY.json"
$exactPreviousResult = Get-Content -Raw -LiteralPath $exactReceiptPath | ConvertFrom-Json
$exactReceiptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $exactReceiptPath).Hash.ToLowerInvariant()
$exactOverlay = "$exactSource\software\v5\$exactStage\OVERLAY.json"
$exactOverlayHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $exactOverlay).Hash.ToLowerInvariant()
& $exactPython -I -S -B "$exactSource\software\v5\$exactStage\assemble.py" `
  --source-root $exactSource --base-package $exactPreviousResult.package `
  --base-profile-sha256 $exactPreviousResult.profile_sha256 `
  --base-receipt $exactReceiptPath --base-receipt-sha256 $exactReceiptHash `
  --overlay $exactOverlay --overlay-sha256 $exactOverlayHash `
  --output "$exactBuilds\$exactNext" --wall-seconds 120 --cpu-seconds 90
if ($LASTEXITCODE -ne 0) { throw 'Inspect the retained overlay failure.' }
```

All these overlays copy native bytes, without rebuilding. Their time checks are
cooperative, not hard containment. The exact overlay validates the predecessor's
complete selected payload map and receipt, then changes exactly three payloads.
It accepts compatible fresh generated native identities; no old experiment
receipt is an input. After checking final success:

```powershell
$exactFinal = Get-Content -Raw -LiteralPath "$exactBuilds\exact-01\ASSEMBLY.json" | ConvertFrom-Json
$exactPackage = "$exactBuilds\exact-01\package"
if ($exactFinal.status -ne 'ASSEMBLED_NOT_ADOPTED' -or $exactFinal.package -cne $exactPackage -or
    (Get-FileHash -Algorithm SHA256 -LiteralPath "$exactPackage\PROFILE.json").Hash.ToLowerInvariant() -cne $exactFinal.profile_sha256) { throw 'Final receipt/profile mismatch.' }
$exactProfile = $exactFinal.profile_sha256
```

Keep package bytes unchanged. The old bounded-transport `prepare_selected.py`
rejects this package's three changed roles as `SELECT_UNKNOWN_INTERFACE`.
**Do not use that preparer or edit its pins.** Direct public commands suffice
for the following steps.

## Common operation checks

For every command below require zero terminal exit, diagnostics `RUN.json` with
`ok:true`, `status:CLI_EXITED_ZERO` and the selected profile, and
`SUPERVISION.json` with `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit zero,
`direct_child_reaped:true`, `job_closed:true`, no cleanup errors or termination
request, and zero final active/terminated processes. Then read the full
`child/stdout.txt` owner report. Require `ok:true`, expected operation, exact
profile/catalog/custody/store, and no close/budget error. Only then select its
`result` fields. A partial file or an inner PASS does not establish completion.
Failed reporting can follow an actual commit; never infer rollback.

## Initialize directly, without a Lean project

Save a new UTF-8 `C:\commons-inputs\custody-limits.json` using an editor:

```json
{"objects":4096,"exports":32768,"logical_bytes":67108864,"db_pages":32768}
```

These are explicit persistent example limits, not arbitrary-size capacity.

```powershell
$exactCatalog = 'C:\commons-state\catalog'
$exactCustody = 'C:\commons-state\custody'
$exactLimits = 'C:\commons-inputs\custody-limits.json'
$exactStore = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
& $exactPython -I -S -B "$exactPackage\run.py" `
  --profile-sha256 $exactProfile --python-runtime $exactPythonRoot --lean-runtime $exactLean `
  --diagnostics "$exactWork\init-01" --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  owner -- init --catalog $exactCatalog --custody $exactCustody `
  --store-id $exactStore --custody-limits $exactLimits
if ($LASTEXITCODE -ne 0) { throw 'Inspect initialization before continuing.' }
```

There is no `--output` for init/intake. The store ID is a local opaque label, not
a credential. Preserve exact state/ID/limits and serialize owner operations.
After the common checks, require `result.status = INITIALIZED_LOCAL_OWNER` and
`result.basis.status = CHECKED`. Read the actual report and select its root:

```powershell
$exactInit = Get-Content -Raw -LiteralPath "$exactWork\init-01\child\stdout.txt" | ConvertFrom-Json
$exactParent = $exactInit.result.basis.local_root
if ($exactParent -cnotmatch '^[0-9a-f]{64}$') { throw 'Missing checked basis root.' }
```

## Independently receive an offline concept bundle

Obtain actual inert `manifest.json`, all its `units/` files and chosen exact
target triples from an available contributor or the existing
[selected-export companion](../ordinary_selected_export/README.md).
Its successful `RESULT.json.targets` supplies the rows and `manifest.sha256`
identifies the manifest. A producer bundle's public terminal `result.targets`
supplies equivalent target metadata. Preserve structured names and exact
`{name, export_id, unit_id}` values, not guesses from dotted names. The metadata
is not authority: intake/module export independently check its bindings.

This is explicit external data, not an experimental fixture. If no real handoff
exists, stop at that supply condition; software cannot invent useful content.
Choose target rows and save a nonempty JSON list (at most 32) in
`C:\commons-inputs\module-targets.json`. No producer project or peer binary is
needed at this receiver.

```powershell
$exactBundle = 'C:\commons-inputs\received-bundle'
$exactManifest = "$exactBundle\manifest.json"
$exactManifestHash = 'REPLACE_WITH_SELECTED_MANIFEST_SHA256'
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $exactManifest).Hash.ToLowerInvariant() -cne $exactManifestHash) { throw 'Manifest mismatch.' }
& $exactPython -I -S -B "$exactPackage\run.py" `
  --profile-sha256 $exactProfile --python-runtime $exactPythonRoot --lean-runtime $exactLean `
  --diagnostics "$exactWork\intake-01" --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  owner -- intake-baseline --catalog $exactCatalog --custody $exactCustody `
  --store-id $exactStore --custody-limits $exactLimits --parent-root $exactParent `
  --bundle-directory $exactBundle --bundle-manifest $exactManifest --bundle-manifest-sha256 $exactManifestHash
if ($LASTEXITCODE -ne 0) { throw 'Inspect intake and any committed prefix.' }
```

Intake reserves 60 CPU seconds **per batch**, plus headroom/controller work.
This example's 120-second ceiling does not authorize two batches. Choose an
adequate finite allowance prospectively or retain refusal. Apply the common
checks and [exact intake report checks](../ordinary_selected_export/INTAKE.md#check-completion-before-selecting-publication).
Require `BASELINE_INTAKE_COMPLETE`, matching manifest and
`result.selected_root = $exactParent`; inspect actual checked/reused `batches`.
Then select the resulting context, not the producer's root:

```powershell
$exactIntake = Get-Content -Raw -LiteralPath "$exactWork\intake-01\child\stdout.txt" | ConvertFrom-Json
$exactContext = $exactIntake.result.local_root
if ($exactContext -cnotmatch '^[0-9a-f]{64}$') { throw 'Missing completed intake root.' }
```

## Realize the selected warranted vocabulary

```powershell
$exactTargets = 'C:\commons-inputs\module-targets.json'
& $exactPython -I -S -B "$exactPackage\run.py" `
  --profile-sha256 $exactProfile --python-runtime $exactPythonRoot --lean-runtime $exactLean `
  --diagnostics "$exactWork\module-envelope-01" --wall-seconds 180 --cpu-seconds 120 --memory-mib 2048 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  owner -- export-module --catalog $exactCatalog --custody $exactCustody `
  --store-id $exactStore --custody-limits $exactLimits --parent-root $exactContext `
  --module-targets $exactTargets --output "$exactWork\module-01"
if ($LASTEXITCODE -ne 0) { throw 'Inspect module generation.' }
```

After common closure/owner checks require result status
`CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR`, policy
`ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2`,
`source_context_root = $exactContext` and exact selected target rows. The full
report is `module-envelope-01/child/stdout.txt`; `module-01/MODULE.json` alone
does not establish closure. Retain its actual fields:

| Result field | Later input/meaning |
|---|---|
| `source_context_root` | Same owner's explicit context; export adds no new mathematical acceptance/root |
| `anchor_id` | Local exact `--module-anchor`; not a context root or remote warrant |
| `module_name`, all `import_directories` | Exact Lean import/complete registered chain, not peer executable approval |
| `supported_runtime` | This export's actual Lean/installation identity, not arbitrary downstream-project validation |
| `targets` | Exact selected realized bindings; not every declaration in the owner's context |

Cold export still checks its selected complete closure within the existing
32-unit/4-MiB delta bound; intake success need not imply realization fits. Do not
raise caps or add axioms to force success. Later reopening uses this same public
export command with actual `--module-anchor`, fresh output/diagnostics and covered
targets. It may return `REUSED_LOCAL_MODULE_ANCHOR`, zero native/fetch calls,
after protected registration/artifact checks. Do not repeat that immediately as
ceremony. Old-support anchors refuse, and a copied peer `.olean` is not eligible.

## First turnkey obstruction: received-vocabulary source extraction

The next desired step is to write an independently chosen law in this vocabulary,
without proving it, and obtain its type AST under bounded approved execution.
The mathematics and protocol already support this. The missing shipped part is
the **operator-facing execution/import glue**, not another AST, module or trust
relation. Source inspection reached these concrete boundaries:

- Final `run.py`, selected from `ordinary_contact_federation/run.py:23-42`, accepts
  only `owner`, `peer`, `query`. Query accepts `native-type`, `bindings` or
  `context-root`, not Lean source/import/AnchorID extraction options. Its target
  `ordinary_query_context/query.py:101-115` requires an already produced AST.
- `ordinary_basis_query/query.py:93-99,136-157` fixes Init/helper imports and the
  581-row basis binding. It intentionally has no received-module option.
- The packaged `author_worker.py`, selected from
  `ordinary_project_package/author_worker.py`, can invoke approved Lean source
  with helper/project paths, but uses `subprocess.call` without supplying its
  own time/memory/process/log envelope. Its docstring presumes an enclosing Job.
- The shipped supervisor's `commons.py` has a reusable `supervise` function,
  which the public launcher loads, but its standalone `main` is the historical
  compact-release CLI with fixed receiver/profile roles, not a generic approved
  Lean argv CLI. Calling the function needs an approved caller that binds support,
  paths, imports, limits, outputs and closure; that is what the pending test does.
- The other shipped supervisor's `run_stage.py` CLI is not a drop-in substitute:
  `execute:310-324` requires the actual executing files at
  `domains.install/py/{domains.py,run_stage.py}`. The current package places them
  in `installation/supervisor/`. Its `execute:443-445` also requires stage-local
  LEAN_PATH snapshots. A new legacy-layout wrapper/staging recipe would itself
  need explicit selection and review; simply changing the source path does not
  make this existing package compatible.

An operator **can** supply a separately approved external process-tree envelope
and exact import selection, use `OwnerQueryCommand`, then call the existing
public context query. The source recipe is
[RECEIVED-QUERY-COMPOSITION](../../../research/cycles/v5-2026-10-26-local-discovery/RECEIVED-QUERY-COMPOSITION.md).
That is legitimate composition, not fundamentally impossible Lean execution.
The [current test-only contract](../ordinary_received_query/CONTRACT.md) is
pending evidence, not a shipped AnchorID-to-question command. Finish that work
before deciding whether a small successor to the basis companion is justified.

This trace stops here rather than inserting a hypothetical command into a full
guide. Existing [contribute/publish](../ordinary_reuse_workflow/README.md) and
[finite serving](../ordinary_service_plan/README.md) interfaces remain available;
their post-question composition has not been traced across this missing turnkey
edge here. Packaging extra files alone cannot supply the envelope. No native
build, test, owner operation, service or archive was run for this document.
All work remains local/unpublished, and the license remains undecided.
