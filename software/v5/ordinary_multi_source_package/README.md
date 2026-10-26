# Receive exact mathematics from several approved holders

This optional update lets one receive operation obtain different requested
objects from different holders. It changes **where exact bytes come from**, not
what counts as a proof. Discovery, preview/evidence validation, local preflight
and mathematical admission keep their existing authority boundaries.

**Source integration only until its assembly and offline preparation gates are
separately selected and adopted.** The current investigator source archive is
unchanged and does not contain this update. Work remains local and unpublished;
the license is undecided. This guide is outside the built package and supersedes
its preserved historical receive guidance only for this optional update.

If one approved source already has a complete bundle, ordinary direct import or
a complete mirror can be simpler. Multiple suppliers help when one disappears
or different holders have different requested objects; they cannot invent a
missing preview, recover lost bytes or make cold proof checking free.

## What changes, and what does not

The file-only overlay replaces exactly:

- `peer_api.py`;
- `support/transport/http_provider.py`;
- `support/transport/ordinary_acquisition.py`.

The new package has a new PROFILE digest. Its other 150 payloads, all eight
existing documents, native INSTALLATION, owner/loader and module-anchor support
remain byte-identical. Under the existing protected-state assumptions, a reviewed
transport-only change therefore does not inherently require fresh mathematical
state or replay of already checked mathematics. This is a source/identity
argument, **not a claimed execution of an old-state reopen**.

Keep the old installation and reports intact. Close services and serialize owner
operations. Reuse the same catalog, custody, store ID and original persistent
limits only when the checking implementation, semantics and selected support
really are unchanged. Never edit adoption markers, anchor records, old PROFILEs
or reports to force compatibility. See [update and recovery](../UPDATE-AND-RECOVERY.md)
for checker changes or suspected state compromise.

## Assemble a fresh package

Use the approved Windows x86-64 / Python 3.14.6 / Lean 4.34.0 profile. Assembly
executes approved file-only utilities, not Lean, product code or state. It does
not authenticate the source or supply a filesystem/network sandbox.

The base is the **immediate exact-module package** from the
[investigator build route](../ordinary_investigator_bundle/guides/BUILD-MODULE.md),
with its actual terminal `ASSEMBLY.json` and PROFILE. Do not start from an earlier
transport package or manually patch an existing package. The source root must
be independently approved and contain this supplement, the tested
`ordinary_multi_source` payloads and the predecessor helper/compatibility files
at their original paths. Until a fresh consolidated source distribution exists,
the old investigator archive alone is insufficient; do not modify its verified
extraction or manifest to pretend otherwise.

Bind these variables to independently selected real locations and hashes:

```powershell
$multiPython = 'C:\tools\Python314\python.exe'
$multiSource = 'C:\approved-commons-source'
$multiBasePackage = 'C:\commons-builds\exact-01\package'
$multiBaseReceipt = 'C:\commons-builds\exact-01\ASSEMBLY.json'
$multiOutput = 'C:\commons-builds\multi-01' # must not exist
$multiBase = Get-Content -Raw -LiteralPath $multiBaseReceipt | ConvertFrom-Json
if ($multiBase.status -cne 'ASSEMBLED_NOT_ADOPTED' -or
    $multiBase.package -cne $multiBasePackage) { throw 'Wrong immediate base receipt.' }
$multiReceiptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $multiBaseReceipt).Hash.ToLowerInvariant()
$multiOverlay = "$multiSource\software\v5\ordinary_multi_source_package\OVERLAY.json"
$multiOverlayHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $multiOverlay).Hash.ToLowerInvariant()

& $multiPython -I -S -B "$multiSource\software\v5\ordinary_multi_source_package\assemble.py" `
  --source-root $multiSource --base-package $multiBasePackage `
  --base-profile-sha256 $multiBase.profile_sha256 `
  --base-receipt $multiBaseReceipt --base-receipt-sha256 $multiReceiptHash `
  --overlay $multiOverlay --overlay-sha256 $multiOverlayHash `
  --output $multiOutput --wall-seconds 120 --cpu-seconds 90
if ($LASTEXITCODE -ne 0) { throw 'Preserve and inspect the failed assembly.' }
```

Computing a hash here binds already approved input; it is not independent
authentication. The assembler preserves failed output and will not overwrite it.
Its time checks are cooperative; use an approved outer Job for hard containment.

Read the new terminal `ASSEMBLY.json`. Require `ASSEMBLED_NOT_ADOPTED`, exactly
three `changed_or_added` destinations, `unchanged_payloads = 150`,
`auxiliary_files = 117`, `files_excluding_profile = 153`, and the same
`installation_manifest_sha256` as the base. Match its new PROFILE digest to
`package/PROFILE.json`. Retain the receipt and select that **new actual digest**
for every operation on the new package. Assembly alone is not mathematical or
deployment qualification. Do not modify its payloads afterward.

```powershell
$multiAssembled = Get-Content -Raw -LiteralPath "$multiOutput\ASSEMBLY.json" | ConvertFrom-Json
$multiPackage = "$multiOutput\package"
if ($multiAssembled.status -cne 'ASSEMBLED_NOT_ADOPTED' -or
    $multiAssembled.package -cne $multiPackage -or
    $multiAssembled.installation_manifest_sha256 -cne $multiBase.installation_manifest_sha256 -or
    $multiAssembled.unchanged_payloads -ne 150 -or
    $multiAssembled.auxiliary_files -ne 117 -or
    $multiAssembled.files_excluding_profile -ne 153 -or
    (Get-FileHash -Algorithm SHA256 -LiteralPath "$multiPackage\PROFILE.json").Hash.ToLowerInvariant() -cne
      $multiAssembled.profile_sha256) { throw 'Final assembly/profile mismatch.' }
$multiProfile = $multiAssembled.profile_sha256
```

## Choose one of two configuration routes

### A. Reports already belong to the new PROFILE

Use the existing [network request forms](../ordinary_network_kit/START-HERE.md),
but replace their historical selector with this matching selector:

```powershell
& $multiPython -I -S -B "$multiSource\software\v5\ordinary_multi_source_package\prepare_selected.py" `
  --package $multiPackage --profile-sha256 $multiProfile `
  --request 'C:\commons-requests\receive.json' `
  --output 'C:\commons-requests\prepared-multi-01'
```

Here `$multiPackage` and `$multiProfile` are the selected new package path and
actual new PROFILE digest, not the base values. Preparation writes inert configs
and arguments; it does not execute receive or check mathematics. Only `receive`
gains these optional top-level **request** fields:

```json
{
  "acquisition_sources": ["holder-a", "holder-b"],
  "attempt_timeout_ms": 2000,
  "finalization_reserve_ms": 5000
}
```

Add all three to an otherwise complete receive request, or omit all three for
the old single-source behavior. Labels must be distinct, already approved in
that request's `contacts`, and number between 1 and 8. Both times are integers
between 1 and 60,000 milliseconds; booleans are not integers here. Other action
schemas and PROFILE-exact report requirements remain unchanged. Inspect the
prepared config/hash and launch only its selected finite operation.

### B. Existing owner or selected reports belong to the old PROFILE

The preparer deliberately rejects historical parent/find reports with a different
PROFILE. **Do not rerun initialization to obtain a new-profile parent report.**
Do not edit historical reports, relax their checks, or merely change the selector
map. Instead use the supported public receive-config interface below.

Independently select and retain:

- the closed existing catalog/custody, original store ID and custody-limits file;
- the actual successful local parent root and its original report/closure evidence;
- one exact inert `{provider, snapshot_id, record}` selection from a successful
  selected find report or explicit metadata handoff, with the original bytes/hash;
- approved contacts, including the discovery-origin label and chosen holders.

An old find report is only a source of inert exact metadata. Its truth, freshness
or provider availability is not promoted by copying that selection into a config.
An old parent report does not itself reopen state: the public entry checks the
actual catalog's implementation and `receive` resolves the requested local root
before network I/O. Do not substitute an AnchorID or the producer's local root.

Construct a **new** config. The following shows every top-level field; the four
variables for actual contacts, exact selection, parent root and destination must
be bound to the independently selected values above, not invented examples:

```powershell
if ($multiParentRoot -cnotmatch '^[0-9a-f]{64}$') { throw 'Select an actual local parent root.' }
$multiConfig = [ordered]@{
  contacts = $multiContacts
  selection = $multiSelection
  parent_root = $multiParentRoot
  dependency_policy = 'selected-unit-only'
  limits = [ordered]@{
    requests = 16; reply_bytes = 16777216
    units = 32; unit_bytes = 4194304; total_bytes = 4194304
    missing = 128; preflights = 33; locator_bytes = 4096
  }
  acquisition_sources = @('holder-a', 'holder-b')
  attempt_timeout_ms = 2000
  finalization_reserve_ms = 5000
}
$multiConfigBytes = [System.Text.UTF8Encoding]::new($false).GetBytes(
  ($multiConfig | ConvertTo-Json -Depth 100 -Compress))
$multiConfigStream = [System.IO.File]::Open($multiConfigPath,
  [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
try { $multiConfigStream.Write($multiConfigBytes, 0, $multiConfigBytes.Length) }
finally { $multiConfigStream.Dispose() }
$multiConfigHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $multiConfigPath).Hash.ToLowerInvariant()
```

The config path must be a new absolute file in a protected existing directory,
outside state and package paths. The policy initially avoids ancestor acquisition:
missing grounded premises return a nonacceptance result, not automatic expansion.
Choose `bounded-closure` only when you deliberately authorize finite dependency
acquisition and select suitable original limits. The example limits are maxima,
not a promise that every target fits. Failed attempts consume their full response
cap, so a large `unit_bytes` can exhaust the aggregate byte grant quickly.

Use the new actual package/profile and unchanged original state fields:

```powershell
& $multiPython -I -S -B "$multiPackage\run.py" `
  --profile-sha256 $multiProfile --python-runtime $multiPythonRoot --lean-runtime $multiLeanRoot `
  --diagnostics $multiDiagnostics --wall-seconds 120 --cpu-seconds 90 --memory-mib 1024 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  peer -- receive --catalog $multiCatalog --custody $multiCustody `
  --store-id $multiStoreId --custody-limits $multiCustodyLimits `
  --config $multiConfigPath --config-sha256 $multiConfigHash --output $multiOperationOutput
if ($LASTEXITCODE -ne 0) { throw 'Read the complete retained result before deciding what happened.' }
```

Diagnostics and operation output must be fresh absolute directories with existing
parents, disjoint from one another, the package, runtimes and state. Select the
whole finite allocation prospectively; it is not renewed per holder. Jobs impose
resource limits, not privilege isolation. Approval of the trusted local software
and runtimes remains required. Subsequent direct owner commands can use the
actual resulting local root; no historical report needs rewriting.

## Read outcomes correctly

For each demanded preview, locator or evidence unit, the explicit list replaces
acquisition order. The discovery provider is not silently prepended. Each selected
holder is tried at most once for that key. One network deadline is derived from
the original operation/ledger minus the finalization reserve; per-attempt slots
also reserve bounded connection-close opportunities. This does not guarantee
that an arbitrary proof can finish in the reserve.

Fallback occurs only for the narrow classified connection/EOF/own-timeout cases
or framed HTTP404/503, after normal failed-ticket settlement. TLS/CA/pin errors,
HTTP400, malformed data, wrong identities, exhausted budgets, local retention or
settlement failures and cancellation remain terminal. A malicious reply can stop
this conservative policy even if another holder has correct bytes. No refunds,
new ledger, referrals, implicit contact expansion or global scan occur.

At least one chosen source must supply **each requested kind**. An evidence-only
holder does not supply a required exact preview merely because its evidence could
be used to derive one elsewhere. Suppliers' preview and evidence still undergo
exact validation and binding. Source availability is never mathematical authority.

Read the complete outer and child reports, not only a success line. Require clean
outer closure (`RUN.json` success; `SUPERVISION.json` zero exit, reaped child,
closed Job, zero active/terminated processes, no cleanup/termination request),
matching selected profile/state/config and no final budget/close errors.

| Receive outcome | Meaning |
|---|---|
| `CHECKED` | Actual local admission reported a new checked result; retain its actual root and acceptance fields. |
| `REUSED_LOCAL_ACCEPTANCE` | Existing compatible local acceptance is available; this is not a new native proof check. |
| `NEED_GROUNDED_PREMISES` | Selected-unit-only acquired no ancestors and performed no admission; decide locally what to do next. |
| `PEER_ACQUISITION_SOURCES_EXHAUSTED` | The selected holders did not supply this demanded key within this policy; not proof of global absence. |
| Any other failure | Inspect exact error, acquisition/accounting and any retained admission outcome; do not blindly retry or assume rollback. |

The optional `source_acquisition` report preserves discovery origin, policy and
bounded per-holder call/success/unavailable counts plus last availability reason.
Calls are method invocations, not necessarily begun network requests. The shared
`network`/`acquisition` ledger is authoritative for actual charged requests/bytes;
failed attempts charge the full reserved cap. Retained bytes may remain inert
after failure. If admission committed before a later report/cleanup failure,
that outcome is not erased by the outer failure.

This update supplies a bounded usable acquisition path, not a new mathematical
trust system, global completeness guarantee, uptime guarantee, measured research
speedup or final worldwide v5 release.
