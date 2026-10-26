# Build one package and realize checked vocabulary

The [root README](../../../../README.md) controls this source distribution. Paths
below are examples, not historical inputs. Select ordinary absolute drive paths
without symlinks/reparse points/shared hard-linked files. Inputs/support/state
must be protected against concurrent modification. Every output leaf must be
absent with an existing parent, separate from inputs, runtimes and state. Preserve
failures and inspect committed prefixes; never assume a failed report rolled
back state or automatically renew an allocation.

## Build once; apply all five overlays

```powershell
$investigatorPythonRoot = 'C:\tools\Python314'
$investigatorPython = "$investigatorPythonRoot\python.exe"
$investigatorLean = 'C:\tools\Lean434'
$investigatorSource = 'C:\commons-source'
$investigatorBuilds = 'C:\commons-builds'
$investigatorWork = 'C:\commons-work'
& $investigatorPython -I -S -B "$investigatorSource\software\v5\ordinary_bounded_operations\build.py" `
  --source-root $investigatorSource --python-runtime $investigatorPythonRoot --lean-runtime $investigatorLean `
  --output "$investigatorBuilds\native-01" --wall-seconds 600 --cpu-seconds 600 --memory-mib 2048
if ($LASTEXITCODE -ne 0) { throw 'Inspect the retained failed build.' }
$investigatorBuildReceipt = "$investigatorBuilds\native-01\_build\BUILD-RESULT.json"
$investigatorBuilt = Get-Content -Raw -LiteralPath $investigatorBuildReceipt | ConvertFrom-Json
```

These finite ceilings are examples, not promises of success or memory needs.
Require terminal `BUILT_NOT_ADOPTED`, the expected `package` path, actual PROFILE
hash equal `profile_sha256`, and clean successful retained diagnostics. The build
receipt precedes PROFILE creation: the receipt's mere existence is insufficient.
Review/select the actual built inputs before applying fair:

```powershell
$investigatorBuildHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $investigatorBuildReceipt).Hash.ToLowerInvariant()
& $investigatorPython -I -S -B "$investigatorSource\software\v5\ordinary_fair_search\assemble.py" `
  --source-root $investigatorSource --base-package $investigatorBuilt.package `
  --base-profile-sha256 $investigatorBuilt.profile_sha256 `
  --base-build-receipt $investigatorBuildReceipt --base-build-receipt-sha256 $investigatorBuildHash `
  --output "$investigatorBuilds\fair-01" --wall-seconds 120 --cpu-seconds 90
if ($LASTEXITCODE -ne 0) { throw 'Inspect the retained fair assembly.' }
```

Apply these rows **one at a time after inspecting the preceding success**:

| Source directory under `software/v5` | Previous output | Fresh output |
|---|---|---|
| `ordinary_contact_federation` | `fair-01` | `contact-01` |
| `ordinary_sparse_access` | `contact-01` | `sparse-01` |
| `ordinary_transport_release` | `sparse-01` | `transport-01` |
| `ordinary_exact_module` | `transport-01` | `exact-01` |

For each row require the predecessor's terminal exit zero, `ASSEMBLY.json.status`
equal `ASSEMBLED_NOT_ADOPTED`, expected package path and matching actual PROFILE.
Set the three row variables, review the selected source/map, then execute:

```powershell
$investigatorStage = 'ordinary_contact_federation' # Select one row.
$investigatorPrevious = 'fair-01'
$investigatorNext = 'contact-01'
$investigatorReceipt = "$investigatorBuilds\$investigatorPrevious\ASSEMBLY.json"
$investigatorPreviousResult = Get-Content -Raw -LiteralPath $investigatorReceipt | ConvertFrom-Json
$investigatorReceiptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $investigatorReceipt).Hash.ToLowerInvariant()
$investigatorOverlay = "$investigatorSource\software\v5\$investigatorStage\OVERLAY.json"
$investigatorOverlayHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $investigatorOverlay).Hash.ToLowerInvariant()
& $investigatorPython -I -S -B "$investigatorSource\software\v5\$investigatorStage\assemble.py" `
  --source-root $investigatorSource --base-package $investigatorPreviousResult.package `
  --base-profile-sha256 $investigatorPreviousResult.profile_sha256 `
  --base-receipt $investigatorReceipt --base-receipt-sha256 $investigatorReceiptHash `
  --overlay $investigatorOverlay --overlay-sha256 $investigatorOverlayHash `
  --output "$investigatorBuilds\$investigatorNext" --wall-seconds 120 --cpu-seconds 90
if ($LASTEXITCODE -ne 0) { throw 'Inspect the retained overlay failure.' }
```

The five overlays copy existing native bytes, not rebuild them. Their allowance
checks are cooperative, not a hard sandbox. Fresh supported builds can have
different generated identities; the assemblers require the supported complete
source/role layout and immediate receipt chain, not arbitrary binaries.
Do not substitute historical PROFILE/receipt hashes. Check the final result:

```powershell
$investigatorFinal = Get-Content -Raw -LiteralPath "$investigatorBuilds\exact-01\ASSEMBLY.json" | ConvertFrom-Json
$investigatorPackage = "$investigatorBuilds\exact-01\package"
if ($investigatorFinal.status -ne 'ASSEMBLED_NOT_ADOPTED' -or
    $investigatorFinal.package -cne $investigatorPackage -or
    (Get-FileHash -Algorithm SHA256 -LiteralPath "$investigatorPackage\PROFILE.json").Hash.ToLowerInvariant() -cne $investigatorFinal.profile_sha256) { throw 'Final receipt/profile mismatch.' }
$investigatorProfile = $investigatorFinal.profile_sha256
```

Keep the final package unchanged. Assembly is not independent native acceptance.
The [bounded build guide](../../ordinary_bounded_operations/README.md) and
[launcher guide](../../ordinary_bounded_operations/LAUNCHER.md) explain their
limits; this document overrides their historical final-stage choices.

## Select this package's operations

Use the existing [network request forms](../../ordinary_network_kit/START-HERE.md)
and examples with the **current selector**:

```powershell
& $investigatorPython -I -S -B "$investigatorSource\software\v5\ordinary_investigator_bundle\prepare_selected.py" `
  --package $investigatorPackage --profile-sha256 $investigatorProfile `
  --request 'C:\commons-requests\request.json' --output 'C:\commons-requests\prepared-01'
```

It recognizes the exact-module interface's 45 noncompiled and 72 native role
names. It checks the 45 known source bytes; it does **not** validate the native
artifacts or independently approve the package. Preparation writes inert inputs,
not an executed operation. Run selected arguments through this final `run.py`.
Earlier selectors correctly refuse the three changed module payloads; do not
weaken those maps. Update/recovery instructions retain this same-package rule.

## Initialize and independently receive

No pre-existing mathematical Lean project is needed. Initialize with the request
form in the network guide, selecting fresh catalog/custody, a local store ID and
explicit persistent custody limits. An example limits file is:

```json
{"objects":4096,"exports":32768,"logical_bytes":67108864,"db_pages":32768}
```

Use the current selector and final launcher, not the guide's historical ones.
Require `INITIALIZED_LOCAL_OWNER` and `result.basis.status = CHECKED`; retain the
actual `result.basis.local_root`. The store ID is a local label, not a credential.
Serialize all owner operations and keep original limits/IDs, not guessed latest
roots. Distinguish a change to mathematical checking/identity from a module-support
change. The exact-module overlay retains the mathematical installation and can
use its existing compatible checked context. Old-support anchors refuse and need
a fresh compatible realization; this alone does not require a new owner or
reintake. Changes to mathematical implementation follow the explicit recovery/
rechecking policy, not silent state migration.

To receive mathematics either use the network guide's separate find/preview/
receive commands, or the included [offline intake guide](../../ordinary_selected_export/INTAKE.md).
Apply this guide's final package/selector to both. Offline input is an actual
inert `manifest.json` plus its `units/`; no producer project/native artifact is
required. Supply independently selected manifest identity and exact target rows
`{name, export_id, unit_id}` from a successful contributor/export report.
Targets preserve structured names; do not guess IDs from dotted names. If no
actual handoff exists, begin local work instead of inventing one.

For offline completion require `BASELINE_INTAKE_COMPLETE`, matching selected
manifest and `result.selected_root`, all successful checked/reused batches, and
select the receiver's actual `result.local_root` (not the producer's root).
Intake reserves 60 CPU seconds per batch plus controller/headroom work. Choose
the finite whole allocation prospectively; 120 seconds does not authorize two
such batches. The intake guide specifies partial-prefix handling.

## Realize a selected vocabulary

Use the same owner/context to turn actual exact targets into a registered local
Lean module. Save a nonempty list of at most 32 target rows. With variables bound
to the actual owner, original limits, checked context and target file:

```powershell
& $investigatorPython -I -S -B "$investigatorPackage\run.py" `
  --profile-sha256 $investigatorProfile --python-runtime $investigatorPythonRoot --lean-runtime $investigatorLean `
  --diagnostics "$investigatorWork\module-envelope-01" --wall-seconds 180 --cpu-seconds 120 --memory-mib 2048 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  owner -- export-module --catalog $investigatorCatalog --custody $investigatorCustody `
  --store-id $investigatorStore --custody-limits $investigatorLimits --parent-root $investigatorContext `
  --module-targets $investigatorTargets --output "$investigatorWork\module-01"
if ($LASTEXITCODE -ne 0) { throw 'Inspect module generation and closure.' }
```

Require `CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR`, policy
`ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2`, matching `source_context_root` and
selected targets. Retain actual `anchor_id`, `module_name`, complete
`import_directories` and `supported_runtime`. An AnchorID is a local exact
realization binding, **not** a mathematical context root or a remote warrant.
Export does not accept new mathematics or create a new context root.

Cold realization checks a selected complete closure within the existing
32-unit/4-MiB native delta bound; successful intake need not fit this limit.
An explicit compatible `--module-anchor` permits a later requested extension to
reuse the registered chain and check only its new delta within those same caps.
Complete realized imports, exact context bindings and support checks still apply;
this is not permission to omit missing semantics or import peer binaries.
Covered targets can yield `REUSED_LOCAL_MODULE_ANCHOR` without a new native run
after local registration/artifact checks. Do not perform an immediate warm call
merely as ceremony. Wrong-support/missing/changed anchors refuse; there is no
automatic cold fallback, cap increase or axiom shortcut.

## Common completion checks

For every launched owner/peer operation require zero terminal exit and diagnostics
`RUN.json` with `ok:true`, `status:CLI_EXITED_ZERO` and the selected profile.
`SUPERVISION.json` must report `COMMAND_EXITED_ZERO_AND_CLOSED`, zero child exit,
`direct_child_reaped:true`, `job_closed:true`, no cleanup/termination request and
zero final active/terminated processes. Read the complete `child/stdout.txt`
report: `ok:true`, expected operation/profile/catalog/custody/store and no
close/budget error. Only then select result fields. Neither `MODULE.json` alone
nor an inner success phrase supplies that closure evidence.

Next: [ask questions](QUESTIONS.md) or [continue and return work](CONTINUE.md).

