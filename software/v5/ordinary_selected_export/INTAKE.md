# Independently check a selected export at the destination

This companion gives the direct intake command for the inert bundle described in
[README.md](README.md). It uses the unchanged public owner interface; it is not
an executed example or a new acceptance mechanism. Export success and a matching
manifest hash establish data identity, not mathematical acceptance.

## Select the receiver and inputs

Use an approved final package from the [source handoff](../ordinary_release_bundle/README.md)
and its actual PROFILE hash, with approved Windows x86-64 Python 3.14.6 and Lean
4.34.0. Use an existing compatible initialized receiver, or first complete the
[init recipe](../ordinary_operator_kit/START-HERE.md#first-independent-use-init-find-preview-receive)
using the source handoff's final selector/profile overrides. Keep that receiver's
exact catalog/custody paths, store ID and original custody-limits JSON. Serialize
owner operations and stop its service before mutation. Do not use the sender's state.

Deliberately choose a successful report for this same receiver/profile, after
checking its operation and clean launcher closure. Select the parent from:

| Actual successful operation | Parent field |
|---|---|
| `init`, `INITIALIZED_LOCAL_OWNER` | `result.basis.local_root` |
| `intake-baseline`, `BASELINE_INTAKE_COMPLETE` | `result.local_root` |
| `receive`, `CHECKED` or `REUSED_LOCAL_ACCEPTANCE` | `result.admission.local_root` |
| `contribute`, checked contribution with durable publication bytes | `result.admission.local_root` |

An older eligible root can be chosen intentionally; there is no automatic newest
root or branch union. A sender's root, export report or preview is not a parent warrant.
Copy the exact bundle's `manifest.json` and all its `units/` files to an approved
receiver-local directory. Select the actual manifest SHA-256, for example from
the successful export's `manifest.sha256`, and verify the copied file matches it.
No producer report is required; never relabel an export report as production or intake.

All paths below are examples. Use absolute local paths without redirects/shared
hardlinks. Bundle, state, package, runtimes and fresh diagnostics must satisfy
[LAUNCHER.md](../ordinary_bounded_operations/LAUNCHER.md)'s separation rules.
Keep inputs/support protected and unchanged; the diagnostics parent must exist.

## Run one explicitly bounded intake

```powershell
$intakePython = 'C:\tools\Python314\python.exe'
$intakePackage = 'C:\commons-builds\transport-01\package'
$intakeProfile = 'REPLACE_WITH_APPROVED_FINAL_PROFILE_SHA256'
$intakeCatalog = 'C:\commons-state\receiver-catalog'
$intakeCustody = 'C:\commons-state\receiver-custody'
$intakeStore = 'REPLACE_WITH_EXISTING_RECEIVER_STORE_ID'
$intakeLimits = 'C:\commons-inputs\receiver-custody-limits.json'
$intakeParent = 'REPLACE_WITH_SELECTED_RECEIVER_LOCAL_ROOT'
$intakeBundle = 'C:\commons-inputs\selected-bundle'
$intakeManifest = "$intakeBundle\manifest.json"
$intakeManifestHash = 'REPLACE_WITH_SELECTED_MANIFEST_SHA256'
$intakeDiagnostics = 'C:\commons-work\intake-diagnostics-01'
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $intakeManifest).Hash.ToLowerInvariant() -cne $intakeManifestHash) { throw 'Bundle manifest mismatch.' }
& $intakePython -I -S -B "$intakePackage\run.py" `
  --profile-sha256 $intakeProfile --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\lean-4.34.0-windows' --diagnostics $intakeDiagnostics `
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  owner -- intake-baseline --catalog $intakeCatalog --custody $intakeCustody `
  --store-id $intakeStore --custody-limits $intakeLimits --parent-root $intakeParent `
  --bundle-directory $intakeBundle --bundle-manifest $intakeManifest `
  --bundle-manifest-sha256 $intakeManifestHash
```

There is **no `--output`**. The complete owner report is diagnostics
`child\stdout.txt`. The ceilings are examples, not fit guarantees. Intake reserves
60 CPU seconds per manifest batch, including reuse, plus controller/headroom costs;
120 CPU seconds therefore does not authorize two batches. Select a sufficient
finite allowance in advance or retain the refusal; do not automatically retry.

## Check completion before selecting publication

```powershell
$intakeRun = Get-Content -Raw -LiteralPath "$intakeDiagnostics\RUN.json" | ConvertFrom-Json
$intakeSupervision = Get-Content -Raw -LiteralPath "$intakeDiagnostics\SUPERVISION.json" | ConvertFrom-Json
$intakeReport = Get-Content -Raw -LiteralPath "$intakeDiagnostics\child\stdout.txt" | ConvertFrom-Json
if ($intakeRun.ok -ne $true -or $intakeRun.status -ne 'CLI_EXITED_ZERO' -or
    $intakeRun.profile_sha256 -cne $intakeProfile -or
    $intakeSupervision.status -ne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $intakeSupervision.child_exit_code -ne 0 -or $intakeSupervision.direct_child_reaped -ne $true -or
    $intakeSupervision.job_closed -ne $true -or $intakeSupervision.cleanup_errors -or
    $intakeSupervision.termination_requested -ne $false -or
    $intakeSupervision.final_job.active_processes -ne 0 -or $intakeSupervision.final_job.terminated_processes -ne 0 -or
    $intakeReport.ok -ne $true -or $intakeReport.operation -ne 'intake-baseline' -or
    $intakeReport.profile_sha256 -cne $intakeProfile -or $intakeReport.catalog -cne $intakeCatalog -or
    $intakeReport.custody -cne $intakeCustody -or $intakeReport.store_id -cne $intakeStore -or
    $intakeReport.close_errors -or $intakeReport.result.status -ne 'BASELINE_INTAKE_COMPLETE' -or
    $intakeReport.result.manifest_sha256 -cne $intakeManifestHash -or
    $intakeReport.result.selected_root -cne $intakeParent -or
    $intakeReport.result.local_root -cnotmatch '^[0-9a-f]{64}$') { throw 'Inspect retained intake/closure evidence before continuing.' }
$intakeNextRoot = $intakeReport.result.local_root
```

Inspect `result.batches`: they record the completed sequence of actual `CHECKED`
or `REUSED` admissions. This report has no receive-style `result.admission` field.
If intake stops, preserve `detail.status = BASELINE_INTAKE_STOPPED`, its batches,
`last_confirmed_root` and `possible_unreported_commit` when present. A failure can
follow a committed prefix or final admission; missing reports/unclean closure do
not establish rollback. Use explicit protected-owner status/recovery and context
selection before further work, never treat the prefix as whole-bundle completion.

For deliberate publication, use `context_root = $intakeNextRoot` and selected
exact `{name, export_id, unit_id}` records from the successful export helper's
`RESULT.json.targets` for this manifest (its `manifest.sha256` must match).
Choose rows explicitly; do not reconstruct IDs from names. Follow the direct
[publication recipe](../ordinary_reuse_workflow/README.md#3-publish-selected-accepted-outputs-directly)
with these values and this receiver's state/limits. The product independently
checks their accepted bindings; an export report supplies locators, not authority.

The export helper RESULT includes the source custody path: retain it privately
or transfer only the intended target rows, manifest and unit files. Publication
selects advertisements, not read permissions; serving exposes the entire serving
custody. Use a separate disclosure-approved store. No service, external publication,
license grant, source execution approval or transferable warrant follows from intake.
