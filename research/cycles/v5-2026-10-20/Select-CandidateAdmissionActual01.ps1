# File-only selection of one actual refusal/continuation test. Never launches it.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ActualOwnerSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$WorkloadReviewSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsOutcomeSha256
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }

function Ordinary([string]$path, [bool]$directory=$false, [bool]$fresh=$false) {
    $full = [IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $full.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) {
        throw ('CANDIDATE_PATH_SCOPE:'+ $path)
    }
    $cursor = $full
    while ($cursor -and $cursor.Length -ge $projectRoot.Length) {
        if (Test-Path -LiteralPath $cursor) {
            $item = Get-Item -LiteralPath $cursor
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw ('CANDIDATE_REPARSE_PATH:'+ $cursor)
            }
        }
        $cursor = [IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) {
        if (Test-Path -LiteralPath $full) { throw ('FRESH_OUTPUT_REQUIRED:'+ $full) }
    } else {
        $item = Get-Item -LiteralPath $full
        if ([bool]$item.PSIsContainer -ne $directory) { throw ('CANDIDATE_PATH_KIND:'+ $full) }
    }
    return $full
}
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Pin([string]$path, [string]$expected, [long]$maximum=8388608) {
    [void](Ordinary $path)
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or
        (Get-Item -LiteralPath $path).Length -gt $maximum -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED:'+ $path)
    }
}
function New-Bytes([string]$path, [byte[]]$raw) {
    [void](Ordinary $path $false $true)
    if ($raw.Length -eq 0 -or $raw.Length -gt 2097152) { throw 'CANDIDATE_STAGED_BOUND' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
function Json-Bytes($value) {
    return [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
}
function Capture([string]$path, [long]$size, [string]$digest) {
    Require-Pin $path $digest 2097152
    $raw = [IO.File]::ReadAllBytes($path)
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { $observed = [BitConverter]::ToString($hasher.ComputeHash($raw)).Replace('-','').ToLowerInvariant() }
    finally { $hasher.Dispose() }
    if ($raw.Length -ne $size -or $observed -cne $digest) { throw ('CANDIDATE_SOURCE_CAPTURE:'+ $path) }
    return ,$raw
}

$cycle = Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
Require-Pin (Join-Path $cycle 'CANDIDATE-ADMISSION-REVIEW.md') '65d455127b4d21f51ef3212a6ac3518d9138e32e67e308586de07586ea61a4ec'
Require-Pin (Join-Path $cycle 'CANDIDATE-ADMISSION-ACTUAL-REVIEW.md') $WorkloadReviewSha256
Require-Pin (Join-Path $cycle 'CANDIDATE-ADMISSION-CONTROLS-OUTCOME.md') $ControlsOutcomeSha256
$mapPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-exact-packet-01-input.json'
Require-Pin $mapPath '328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561'
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    @($map.sdk_sources.psobject.Properties).Count -ne 129) { throw 'CANDIDATE_EXACT_BASE_129' }
$parent = Join-Path $projectRoot 'product-local/v5-distribution-exact-packet-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$base = Join-Path $install 'base'
Require-Pin (Join-Path $install 'V5-RELEASE.json') 'ffecdc80e2dc57f062aac0aadf37be2a9dadafa24539b34a2e702c0ec24ee4bb'
Require-Pin (Join-Path $base 'RELEASE-MANIFEST.json') 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
$basisPath = Join-Path $parent 'exact-packet01-operations/installed-exact-packet-01/plan.json'
Require-Pin $basisPath 'd5251f83b924240d7b46b7427f0bf6ea37cd3eed491624e9d6e9ea70cc82024f'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_CLIENT_LAUNCH_V1' -or $basis.installation_root -cne $base -or
    $basis.name -cne 'installed-exact-packet-01') { throw 'CANDIDATE_EXACT_ACTUAL_BASIS' }

$overrides = [ordered]@{
    'v5/delta/custody.py'=@('software/v5/offer_enumeration/delta/custody.py','e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634')
    'v5/admission/clean_refusal.py'=@('software/v5/candidate_admission/admission/clean_refusal.py','7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7')
    'v5/admission/verifier.py'=@('software/v5/candidate_admission/admission/verifier.py','ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea')
    'v5/aggregate_claims/aggregate_admission.py'=@('software/v5/candidate_admission/aggregate_claims/aggregate_admission.py','ce2cfc95f08699c679128448d9d9f5131cf54acbefa91225db2689a2b1574f5c')
    'v5/client/workspace_evidence.py'=@('software/v5/candidate_admission/client/workspace_evidence.py','e81407b9296d14a3f3f2f1a1c8554efa2747829fa6a2639fc29215c7ed29cb44')
    'v5/client/managed_owner.py'=@('software/v5/candidate_admission/client/managed_owner.py','3fb4e619ddff115220eee4b6d594a41b2d051e6f8b6c731d63cca15b2c8555a3')
}
$selected = [ordered]@{}
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $logical = $property.Name
    if ($logical -cnotmatch '^(v5|portable)/[A-Za-z0-9_./-]+$' -or
        @($logical.Split('/') | Where-Object { $_ -in @('','.','..') }).Count -ne 0) {
        throw 'CANDIDATE_LOGICAL_PATH'
    }
    $row = $property.Value
    Require-Pin $row.path $row.sha256 2097152
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw 'CANDIDATE_BASE_SOURCE_SIZE' }
    $selected[$logical] = [ordered]@{path=$row.path;bytes=$row.bytes;sha256=$row.sha256}
}
$changed = 0
foreach ($logical in $overrides.Keys) {
    $exists = $selected.Contains($logical)
    if ($exists -eq ($logical -ceq 'v5/admission/clean_refusal.py')) { throw 'CANDIDATE_REPLACEMENT_OR_ADDITION' }
    $path = Join-Path $projectRoot $overrides[$logical][0]
    Require-Pin $path $overrides[$logical][1] 2097152
    if ($exists) {
        if ($selected[$logical].sha256 -ceq $overrides[$logical][1]) { throw 'CANDIDATE_FRESH_SUCCESSOR' }
        $changed += 1
    }
    $selected[$logical] = [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$overrides[$logical][1]}
}
if ($selected.Count -ne 130 -or $changed -ne 5 -or
    @($selected.Keys | Where-Object { $_.StartsWith('v5/') -and $_.EndsWith('.py') }).Count -ne 109 -or
    @($selected.Keys | Where-Object { $_.StartsWith('portable/') }).Count -ne 21) { throw 'CANDIDATE_SOURCE_CENSUS' }
$ownerPath = Join-Path $projectRoot 'software/v5/candidate_admission/actual_owner.py'
Require-Pin $ownerPath $ActualOwnerSha256 2097152
$selected['owner/owner.py'] = [ordered]@{path=$ownerPath;bytes=(Get-Item -LiteralPath $ownerPath).Length;sha256=$ActualOwnerSha256}
$helperPath = Join-Path $parent 'exact-packet01-inputs/terminal_fixture.py'
Require-Pin $helperPath '885138decc4950b307f71d6f98ca3ffbae4ba0bf6a1ee19454746f8e1b638e21'
if ((Get-Item -LiteralPath $helperPath).Length -ne 21432) { throw 'CANDIDATE_FIXTURE_HELPER_SIZE' }
$selected['owner/terminal_fixture.py'] = [ordered]@{path=$helperPath;bytes=21432;sha256='885138decc4950b307f71d6f98ca3ffbae4ba0bf6a1ee19454746f8e1b638e21'}
$captured = [ordered]@{}
$sources = [ordered]@{}
$sourceBytes = [long]0
foreach ($logical in $selected.Keys) {
    $row = $selected[$logical]
    $captured[$logical] = Capture $row.path $row.bytes $row.sha256
    $sources[$logical] = [ordered]@{bytes=$row.bytes;sha256=$row.sha256}
    $sourceBytes += $row.bytes
}
if ($sources.Count -ne 132 -or $sourceBytes -gt 67108864) { throw 'CANDIDATE_132_SOURCE_BOUND' }

# Reference adopted installed assets; do not copy or rebuild the distribution.
$parameters = $basis.parameters
$parameters.schema = 'DMKN_V5_CANDIDATE_ADMISSION_ACTUAL_OWNER_V1'
$parameters.action = 'explicit-temporary-adoption-terminal-refusal-and-continuation'
foreach ($key in @('receipt','journal','bundle','foundation')) {
    $row = $parameters.$key
    Require-Pin $row.path $row.sha256 1048576
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw 'CANDIDATE_FIXTURE_SIZE' }
}
foreach ($row in @($parameters.runtime_adoption.native,$parameters.runtime_adoption.receipt,
                   $parameters.runtime_adoption.aggregate.executable,$parameters.runtime_adoption.preparation_profile)) {
    Require-Pin $row.path $row.sha256 134217728
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw 'CANDIDATE_RUNTIME_SIZE' }
}
if ($parameters.operation_limits.acquisition.verify_attempts -ne 1) { throw 'CANDIDATE_ORIGINAL_ATTEMPTS' }
$parameters.operation_limits.acquisition.verify_attempts = 2
$fresh = Join-Path $projectRoot 'experiments/v5-candidate-admission-actual-01'
[void](Ordinary $fresh $true $true)
$code = Join-Path $fresh 'selected-code'
$operations = Join-Path $fresh 'operations'
$roots = [ordered]@{v5=(Join-Path $code 'v5');portable=(Join-Path $code 'portable');owner=(Join-Path $code 'owner')}
$parameters.provider_workspace_path = Join-Path $fresh 'provider'
$parameters.workspace_path = Join-Path $fresh 'consumer'
$parameters.domain_path = Join-Path $fresh 'trust'
$parameters.domain_id = ([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
if (($parameters | ConvertTo-Json -Depth 64 -Compress).Length -gt 49152) { throw 'CANDIDATE_PARAMETER_BOUND' }
$plan = [ordered]@{
    schema='DMKN_V5_CLIENT_LAUNCH_V1';name='candidate-admission-actual-01'
    installation_root=$base;workspace_root=$operations;source_roots=$roots;sources=$sources
    owner_entry='owner.py';parameters=$parameters;limits=$basis.limits;output_limits=$basis.output_limits
}
$planRaw = Json-Bytes $plan
if ($planRaw.Length -gt 1048576) { throw 'CANDIDATE_PLAN_BOUND' }
# All inputs are checked/captured before any fresh output is created.
[void][IO.Directory]::CreateDirectory($fresh)
[void][IO.Directory]::CreateDirectory($operations)
foreach ($logical in $captured.Keys) {
    $target = Join-Path $code $logical.Replace('/','\')
    [void](Ordinary $target $false $true)
    [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target))
    New-Bytes $target $captured[$logical]
    Require-Pin $target $sources[$logical].sha256 2097152
}
$planPath = Join-Path $fresh 'plan.json'
New-Bytes $planPath $planRaw
$planSha = Digest $planPath
$prepared = [ordered]@{
    schema='DMKN_V5_CANDIDATE_ADMISSION_ACTUAL_PREPARED_V1'
    plan=$planPath;plan_sha256=$planSha;plan_bytes=$planRaw.Length
    workload_review_sha256=$WorkloadReviewSha256;controls_outcome_sha256=$ControlsOutcomeSha256
    source_review_sha256='65d455127b4d21f51ef3212a6ac3518d9138e32e67e308586de07586ea61a4ec'
    sdk_sources=130;owner_sources=2;boot_sources=132;source_bytes=$sourceBytes;selected_originals=$selected
    runtime_invoked=$false;new_proof_production=$false;rebuild=$false
    argv=@((Join-Path $base 'receiver/runtime/python/python.exe'),'-I','-S','-B',
        (Join-Path $roots.v5 'client/launch.py'),$planPath,$planSha)
}
$preparedPath = Join-Path $fresh 'PREPARED.json'
New-Bytes $preparedPath (Json-Bytes $prepared)
[ordered]@{prepared=$preparedPath;prepared_sha256=(Digest $preparedPath);plan=$planPath;
    plan_sha256=$planSha;source_bytes=$sourceBytes;runtime_invoked=$false;argv=$prepared.argv} | ConvertTo-Json -Depth 8
