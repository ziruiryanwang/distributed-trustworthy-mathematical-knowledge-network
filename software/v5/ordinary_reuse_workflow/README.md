# Extend received mathematics with your own Lean source

This recipe continues an actual successful ordinary `receive` with a locally
authored definition or theorem, checks that contribution, then indexes selected
accepted outputs. It uses the existing public commands and requires no producer
project or peer `.olean`. Your own Lean source still executes locally: approve
its execution under the account's actual permissions before running it. Read
[EXECUTION-TRUST.md](../ordinary_bounded_transport/EXECUTION-TRUST.md).

This is a source-only companion recipe, not a recorded successful run. Obtain an
approved package through the [current source handoff](../ordinary_release_bundle/README.md)
and complete its [init/find/preview/receive workflow](../ordinary_network_kit/START-HERE.md)
first. No existing owner or accepted theorem is supplied by this document.

## 1. Select the actual receive and its owner

Use the same final package/profile, approved Windows Python 3.14.6 and Lean 4.34.0,
owner paths, store ID and custody limits as the successful receive. The following
paths are examples; replace them with your selections. `C:\commons-work` exists;
every new input file, output leaf and diagnostic leaf below must be absent.
Keep them disjoint from package, runtimes, state and each other as required by
[LAUNCHER.md](../ordinary_bounded_operations/LAUNCHER.md). Use ordinary absolute
ASCII local paths for this source wrapper, with no links or shared hardlinks.
Serialize operations on this owner; stop its serving operation before mutation.

```powershell
$reusePython = 'C:\tools\Python314\python.exe'
$reusePythonRoot = 'C:\tools\Python314'
$reuseLean = 'C:\tools\lean-4.34.0-windows'
$reusePackage = 'C:\commons-builds\transport-01\package'
$reuseProfile = 'REPLACE_WITH_APPROVED_FINAL_PROFILE_SHA256'
$reuseCatalog = 'C:\commons-state\catalog-a'
$reuseCustody = 'C:\commons-state\custody-a'
$reuseStore = 'REPLACE_WITH_EXISTING_STORE_ID'
$reuseLimits = 'C:\commons-inputs\custody-limits.json'
$reuseWork = 'C:\commons-work'
$reuseReceive = Get-Content -Raw -LiteralPath 'C:\commons-work\receive-01\RESULT.json' | ConvertFrom-Json
```

Read the actual receive launch's `RUN.json` and `SUPERVISION.json`: require
`RUN.ok = true`, `RUN.status = CLI_EXITED_ZERO` and clean closure. Then check the
peer command report above **before using its fields**:

```powershell
if ($reuseReceive.ok -ne $true -or $reuseReceive.operation -ne 'receive' -or
    $reuseReceive.profile_sha256 -cne $reuseProfile -or
    $reuseReceive.catalog -cne $reuseCatalog -or $reuseReceive.custody -cne $reuseCustody -or
    $reuseReceive.store_id -cne $reuseStore -or $reuseReceive.close_errors -or
    $reuseReceive.final_budget_error -or $reuseReceive.result.cleanup_errors -or
    $reuseReceive.result.status -notin @('CHECKED', 'REUSED_LOCAL_ACCEPTANCE') -or
    $reuseReceive.result.local_acceptance_available -ne $true -or
    $reuseReceive.result.admission.status -notin @('CHECKED', 'REUSED') -or
    $null -eq $reuseReceive.result.target) { throw 'Select a complete successful receive for this owner.' }
$reuseParent = $reuseReceive.result.admission.local_root
$reuseTarget = $reuseReceive.result.target
if ($reuseParent -cnotmatch '^[0-9a-f]{64}$' -or
    $reuseTarget.export_id -cnotmatch '^[0-9a-f]{64}$' -or
    $reuseTarget.unit_id -cnotmatch '^[0-9a-f]{64}$') { throw 'Missing exact receive identities.' }
$reuseAcquired = @(@{name=$reuseTarget.name; export_id=$reuseTarget.export_id; unit_id=$reuseTarget.unit_id})
if (Test-Path -LiteralPath "$reuseWork\acquired-targets.json") { throw 'Choose a fresh input filename.' }
[IO.File]::WriteAllText("$reuseWork\acquired-targets.json", (ConvertTo-Json -InputObject $reuseAcquired -Depth 64), [Text.UTF8Encoding]::new($false))
```

`result.target` is the selected exact `{name, export_id, unit_id}` row;
`result.admission.local_root` is the post-receive context. Do not use the older
`result.parent_root`, a search match alone, or `NEED_GROUNDED_PREMISES` as acceptance.
`REUSED_LOCAL_ACCEPTANCE` is usable even though `mathematical_acceptance` is false:
it refers to an existing local warrant rather than a new checking event.

These report checks select inputs; the real product rechecks their mathematical
bindings against protected local state. Keep reports unchanged and implementation,
state and inputs protected. For several acquired targets, explicitly choose a
context in which all exact identities are warranted; the last report from another
branch or owner does not establish their union. This example uses one target.

## 2. Author and check an extension

Inspect the received declaration's actual type and relevant definitions before
choosing a useful extension. Write your own UTF-8 Lean **body** to
`C:\commons-work\own-extension.lean`. It is inserted after the generated imports
and reconstruction command; do not supply a module/import preamble or replace the
generated wrapper. Refer to the actual reconstructed declaration names. The
wrapper supplies `Init` and selected exact formal material, not the producer's
notation, attributes, instances, custom tactics or executable project.

Choose 1..32 completed output declarations, including new definitions if needed.
Their names must be fresh in the chosen context and distinct from acquired names.
Create `output-names.json` as a JSON **list of structured Lean names**. For example,
if your source actually declares `LocalWork.step`, the whole file is:

```json
[[[0,{"$bytes":[76,111,99,97,108,87,111,114,107]}],[0,{"$bytes":[115,116,101,112]}]]]
```

This illustrates only a chosen output name, not a supplied theorem or proof.
Use your actual name components: strings are UTF-8 byte arrays and numeric
components are `[1, n]`. Save JSON as UTF-8 without BOM and preserve array nesting.
Approve your completed source before launching the following direct command.
The current preparation kit has no `contribute` action.

```powershell
& $reusePython -I -S -B "$reusePackage\run.py" `
  --profile-sha256 $reuseProfile --python-runtime $reusePythonRoot --lean-runtime $reuseLean `
  --diagnostics "$reuseWork\contribute-diagnostics-01" `
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  owner -- contribute --catalog $reuseCatalog --custody $reuseCustody `
  --store-id $reuseStore --custody-limits $reuseLimits --parent-root $reuseParent `
  --source "$reuseWork\own-extension.lean" --acquired-targets "$reuseWork\acquired-targets.json" `
  --output-names "$reuseWork\output-names.json" --output "$reuseWork\contribution-01"
```

There are no `--project-authoring` arguments in this path. The controller obtains
the selected material from local custody and reconstructs it before your source
runs; you do not hand-encode dependency proofs. Singleton theorem references are
reconstructed from signatures without traversing proof-only ancestry. The full
selected local unit bytes are still fetched and parsed, and every declared import
must be warranted. Other groups can require bodies and further dependencies;
the new candidate's independent binding and admission checks remain unchanged.

Existing limits include 32 request groups, at most 1 MiB per acquired unit and
per request group, separate 4 MiB aggregate limits for acquired bytes and request
payload (including its header), 32 outputs and a 1 MiB source body.
Admission/candidate bounds also apply. Successful receive can
cover more material than this authoring path supports. An oversized closure,
unavailable frontend behavior, missing interpretation or name conflict can refuse;
do not enlarge caps, change identities or add axioms to force it through. A
separately approved ordinary-project route remains available for other workloads.

The allowance above is an example, not a fit guarantee. Inspect actual cost and
failure diagnostics; retain partial state/output and do not retry or renew an
allowance automatically. Failed reporting or closure can follow admission.

Require successful launch and closure again. The complete owner command report
is `contribute-diagnostics-01\child\stdout.txt`; `contribution-01\RESULT.json`
contains only its inner contribution result and cannot establish CLI/closure
success. Read the complete report and check it before selecting publication:

```powershell
$reuseRun = Get-Content -Raw -LiteralPath "$reuseWork\contribute-diagnostics-01\RUN.json" | ConvertFrom-Json
$reuseContribution = Get-Content -Raw -LiteralPath "$reuseWork\contribute-diagnostics-01\child\stdout.txt" | ConvertFrom-Json
if ($reuseRun.ok -ne $true -or $reuseRun.status -ne 'CLI_EXITED_ZERO' -or
    $reuseContribution.ok -ne $true -or $reuseContribution.operation -ne 'contribute' -or
    $reuseContribution.profile_sha256 -cne $reuseProfile -or
    $reuseContribution.catalog -cne $reuseCatalog -or $reuseContribution.custody -cne $reuseCustody -or
    $reuseContribution.store_id -cne $reuseStore -or $reuseContribution.close_errors -or
    $reuseContribution.result.parent_root -cne $reuseParent -or
    $reuseContribution.result.status -ne 'CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES' -or
    $reuseContribution.result.admission.status -ne 'CHECKED') { throw 'Inspect the retained contribution outcome before continuing.' }
$reuseNextRoot = $reuseContribution.result.admission.local_root
if ($reuseNextRoot -cnotmatch '^[0-9a-f]{64}$' -or
    $reuseContribution.result.local_root -cne $reuseNextRoot) { throw 'Contribution root mismatch.' }
```

## 3. Publish selected accepted outputs directly

Review `result.targets` and choose the outputs worth exposing. This example
selects target index 0 **only after you have reviewed that actual row**. A
contribution's `targets` already has exact `{name, export_id, unit_id}` records;
do not derive their hashes from source text or substitute output-name strings.
The current kit's publish form requires producer/intake reports, and its parent
helper does not accept a contribution report. Use direct `peer publish`; never
relabel a contribution as intake or receive.

```powershell
$reuseTargetIndex = 0 # Deliberate selection from the actual contribution result.
if ($reuseTargetIndex -lt 0 -or $reuseTargetIndex -ge @($reuseContribution.result.targets).Count) { throw 'Select an actual output row.' }
$reusePublish = @{
  context_root = $reuseNextRoot
  targets = @($reuseContribution.result.targets[$reuseTargetIndex])
  index = @{
    path = "$reuseWork\discovery-index-01"; create = $true
    limits = @{max_objects=4096; max_postings=262144; max_features=65536; max_snapshots=4097; max_logical_bytes=67108864; max_db_pages=32768}
  }
  max_unit_bytes = 8388608
  max_total_bytes = 33554432
}
if (Test-Path -LiteralPath "$reuseWork\publish-config.json") { throw 'Choose a fresh input filename.' }
[IO.File]::WriteAllText("$reuseWork\publish-config.json", (ConvertTo-Json -InputObject $reusePublish -Depth 64), [Text.UTF8Encoding]::new($false))
$reusePublishHash = (Get-FileHash -Algorithm SHA256 -LiteralPath "$reuseWork\publish-config.json").Hash.ToLowerInvariant()
& $reusePython -I -S -B "$reusePackage\run.py" `
  --profile-sha256 $reuseProfile --python-runtime $reusePythonRoot --lean-runtime $reuseLean `
  --diagnostics "$reuseWork\publish-diagnostics-01" `
  --wall-seconds 90 --cpu-seconds 60 --memory-mib 1024 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  peer -- publish --catalog $reuseCatalog --custody $reuseCustody `
  --store-id $reuseStore --custody-limits $reuseLimits `
  --config "$reuseWork\publish-config.json" --config-sha256 $reusePublishHash `
  --output "$reuseWork\publish-01"
```

The index above is a new ordinary index with explicit example limits and no
sparse-pair configuration. To reopen an existing index, use its exact path and
original limits/pair configuration with `create: false`; do not silently migrate
it. The command checks each target against the selected context and custody.

Require clean launcher success, then inspect `publish-01\RESULT.json`: outer
`ok = true`, `operation = publish`, matching profile/owner, no cleanup errors,
inner `result.status = INDEXED_LOCAL_TARGETS`,
`result.local_context = $reuseNextRoot`, and the actual `result.publications`.
Publication targets commit separately; partial success is retained on a later
failure. Indexing is not a new mathematical admission or remote receipt.

To make that index reachable, separately select the existing
[finite serve workflow](../ordinary_network_kit/START-HERE.md#provider-static-pair-access-and-finite-services)
with this same index/custody, `create: false` and its original limits. Approving
serve exposes all addressable custody contents, not only this selected target.
No service starts here. Another owner must independently receive/check the work.

The contribution's returned `result.admission.local_root` may also be selected
explicitly for another direct `owner contribute` in this same owner. It is not
a claim of the newest context or a merge of branches. Reuse the actual reports,
preserve unsuccessful attempts, and account for complete launcher/operation
costs; do not add nested native CPU to a supervisor total that already includes
it. This bounded workflow claims no automatic novelty, research acceleration,
universal frontend recovery or arbitrary-scale cold checking.
