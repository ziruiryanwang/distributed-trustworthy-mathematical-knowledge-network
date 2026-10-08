# A complete first local mathematical contribution

This companion supplies an actual formal input, not a schematic graph. It uses
the existing Iter definition: given a type A, a function f:A -> A, a natural
number n and a value a:A, apply f n times to a. Its ModuleID is
`af026e83f6f01326e947ab436c6f4041997a40332bb71c6be154ff7c0df24036`.
It has no named-module imports. Foundation dependencies still exist and are
checked under the adopted release policy.

The steps below provision an owner, pack the input, retain it in a fresh local
node, stop that node, lower the retained module, and genuinely check it. They
do not need a second machine, bootstrap service, account or research-task list.
They do start one temporary loopback service; this is not an Internet test.

This is a source-reviewed operator recipe, not a claim that this exact standalone
command sequence was executed. Actual release evidence is reported separately.
The broader guide is `START-HERE-LIBRARY.md` inside the adopted installation.

## Set three absolute paths

Use an extracted, adopted Windows installation and a new owner-controlled work
directory outside it. `$handoff` contains this file and the two companion JSON
files. Set these three paths to real locations before running the blocks in
order in one PowerShell session. Do not place work under the installation or
use a work directory from a failed earlier attempt.

```powershell
$install = 'C:\absolute\adopted-commons-v4'
$handoff = 'C:\absolute\2026-10-07-v4'
$work = 'C:\absolute\fresh-commons-starter'
$releasePin = 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
$ErrorActionPreference = 'Stop'
foreach ($p in @($install, $handoff, $work)) {
  if (-not [IO.Path]::IsPathRooted($p)) { throw 'Use absolute paths.' }
}
if (Test-Path -LiteralPath $work) { throw 'Choose a new work directory.' }
New-Item -ItemType Directory -Path $work | Out-Null
$python = Join-Path $install 'receiver\runtime\python\python.exe'
$library = Join-Path $install 'operator\library.py'
$owner = Join-Path $work 'owner'
$packRequest = Join-Path $handoff 'STARTER-PACK.json'
$ownerRequest = Join-Path $handoff 'STARTER-OWNER-REQUEST.json'
$moduleID = 'af026e83f6f01326e947ab436c6f4041997a40332bb71c6be154ff7c0df24036'
$packOut = Join-Path $work 'packed'
$lowerOut = Join-Path $work 'lowered'
$checkOut = Join-Path $work 'checked'

function Pin([string]$p) {
  (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Common([string]$step) {
  @('--manifest', (Join-Path $install 'RELEASE-MANIFEST.json'),
    '--manifest-sha256', $releasePin,
    '--evidence', (Join-Path $work ('evidence-' + $step)),
    '--cpu-seconds', '180', '--wall-seconds', '300',
    '--memory-mib', '1024', '--active-processes', '8',
    '--stdout-bytes', '1048576', '--stderr-bytes', '1048576')
}
```

The release pin above is the selected library02 manifest, not a generic example.
Match it to the final handoff's adopted release. A self-computed hash of an
untrusted download alone does not establish trustworthy software. The allowances
are finite ceilings, not a promise that any workload will complete within them.

## Provision and pack

```powershell
$common = Common 'provision'
& $python -I -S -B $library @common provision --owner $owner --request $ownerRequest --request-sha256 (Pin $ownerRequest)
if ($LASTEXITCODE -ne 0) { throw 'Provision failed; preserve its evidence.' }
$bridge = Join-Path $owner 'library-bridge.json'
$node = Join-Path $owner 'library-node.json'
$checkConfig = Join-Path $owner 'definition-owner.json'
$bridgePin = Pin $bridge
$nodePin = Pin $node
$checkPin = Pin $checkConfig

$common = Common 'pack'
& $python -I -S -B $library @common pack --config $bridge --config-sha256 $bridgePin --request $packRequest --request-sha256 (Pin $packRequest) --out $packOut
if ($LASTEXITCODE -ne 0) { throw 'Pack failed; preserve its evidence.' }
$packed = Get-Content -LiteralPath (Join-Path $packOut 'result.json') -Raw | ConvertFrom-Json
if ($packed.status -ne 'PACKED_UNVERIFIED_MODULE' -or $packed.module_id -ne $moduleID) { throw 'Unexpected packed result.' }
```

Provisioning must report `CONFIGURED_NOT_STARTED`. Packing only constructs a
canonical content-addressed recipe; it does not mathematically verify it.

## Offer into local custody, then stop

Create a UTF-8 command file with an absolute source path and final newline.
`publish:false` retains the recipe locally without advertising provider hints.
There are no bootstrap peers in this starter configuration.

```powershell
$commands = Join-Path $work 'offer-stop.jsonl'
$offer = @{ id = 'starter-offer'; request = @{
  operation = 'offer'; source = (Join-Path $packOut 'module.json'); publish = $false
} } | ConvertTo-Json -Depth 8 -Compress
$stop = @{ id = 'starter-stop'; request = @{ operation = 'stop' } } | ConvertTo-Json -Depth 8 -Compress
if (Test-Path -LiteralPath $commands) { throw 'Command file must be fresh.' }
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($commands, ($offer + "`n" + $stop + "`n"), $utf8NoBom)
$common = Common 'offer'
& $python -I -S -B $library @common node --config $node --config-sha256 $nodePin --commands $commands --commands-sha256 (Pin $commands) --create
if ($LASTEXITCODE -ne 0) { throw 'Node operation failed; preserve its evidence.' }
$nodeEvents = @(Get-Content -LiteralPath (Join-Path $work 'evidence-offer\stdout.txt') | ForEach-Object { $_ | ConvertFrom-Json })
$offered = @($nodeEvents | Where-Object { $_.id -eq 'starter-offer' })
if ($offered.Count -ne 1 -or $offered[0].status -ne 'OK' -or $offered[0].result.status -ne 'IMMUTABLE_CUSTODY_UNVERIFIED' -or $offered[0].result.offer.module_id -ne $moduleID) { throw 'Expected exact fresh custody was not established.' }
```

The explicit inner-response check matters: an individual node command can fail
even when the process subsequently stops cleanly. The final public-wrapper record must report
`COMMAND_EXITED_ZERO_AND_CLOSED`. Never equate custody or publication with proof.
Use `--create` only for this first start; omit it on later reopening of the same
state. Do not edit generated pinned configuration files while using that state.

## Lower and check retained mathematics

```powershell
$common = Common 'lower'
& $python -I -S -B $library @common lower --config $bridge --config-sha256 $bridgePin --module-id $moduleID --out $lowerOut
if ($LASTEXITCODE -ne 0) { throw 'Lower failed; preserve its evidence.' }
$lowered = Get-Content -LiteralPath (Join-Path $lowerOut 'result.json') -Raw | ConvertFrom-Json
if ($lowered.status -ne 'LOWERED_UNVERIFIED' -or $lowered.mathematical_acceptance -ne $false) { throw 'Unexpected lower result.' }

$common = Common 'check'
& $python -I -S -B $library @common check --config $bridge --config-sha256 $bridgePin --module-id $moduleID --check-config $checkConfig --check-config-sha256 $checkPin --out $checkOut
if ($LASTEXITCODE -ne 0) { throw 'Native check failed; preserve its evidence.' }
$checked = Get-Content -LiteralPath (Join-Path $checkOut 'result.json') -Raw | ConvertFrom-Json
if ($checked.status -ne 'LOCAL_NATIVE_MODULE_VERIFIED_NOT_TRANSFERABLE' -or $checked.mathematical_acceptance -ne $true -or $checked.transferable -ne $false) { throw 'No expected native acceptance.' }
```

The optional separate `lower` call makes the status distinction visible. The
`check` action performs its own lowering and genuine native check; it does not
trust the earlier output. A successful local report is not a transferable
cryptographic certificate. Another receiver must check the mathematical input
or verify separately supplied compatible certificate evidence. This starter
contributes a reusable definition, not a new law or novel research result.

Retain operation evidence and immutable recipe custody. Full flattened outputs
are working caches; permanently storing every flattened prefix is not required
by the named-recipe architecture. No automatic cache deletion is performed here.

## Exact source of the example

`STARTER-PACK.json.plan` is structurally identical to the already exported
`experiments/named-library-01/fixtures01/plans/D0.json` (2265 bytes,
SHA-256 `2e82b9d1c80f1e8b2a29927d034b0947a310182e5924a17a424968aed2b71a6f`).
Its imports are the exact empty array from the existing D0 descriptor (2441
bytes, SHA-256
`da92c4ba280781e137c42d5bc0265388faa10cca96d0ef2acddd20a971a3831f`).
No new mathematical expression was authored for this companion. The provisioning
request is the finite loopback example in the installed public guide. Final
handoff integrity must bind these companion files separately from the frozen
product archive; adding them does not change the adopted release manifest.
