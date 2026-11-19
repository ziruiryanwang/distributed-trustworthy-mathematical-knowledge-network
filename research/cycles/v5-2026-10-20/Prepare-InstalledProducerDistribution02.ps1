# File-only two-source successor of adopted installed-producer01. No builder invocation.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$DistributionSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$EntrySha,
    [Parameter(Mandatory=$true)][string]$ReviewPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReviewSha
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$basisRoot=Join-Path $checks 'installed-producer-distribution-01'
$out=Join-Path $checks 'installed-producer-distribution-02'
$parent=Join-Path $projectRoot 'product-local\v5-distribution-installed-producer-02'
$runName='distribution-installed-producer-build-02'
$originals=[ordered]@{}
function Ordinary([string]$path,[bool]$fresh=$false) {
    if ([IO.Path]::GetFullPath($path) -cne $path -or -not $path.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'CANONICAL_PATH' }
    $cursor=$path
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item=Get-Item -LiteralPath $cursor
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or
                ($cursor -cne $path -and -not $item.PSIsContainer)) { throw 'ORDINARY_PATH' }
        }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh -and (Test-Path -LiteralPath $path)) { throw 'FRESH_OUTPUT_REQUIRED' }
}
function Pin([string]$path,[string]$sha,[long]$max=8388608) {
    Ordinary $path
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or $item.Length -le 0 -or $item.Length -gt $max -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $sha) { throw ('PIN:'+ $path) }
    $row=[ordered]@{path=$path;bytes=$item.Length;sha256=$sha}
    if ($originals.Contains($path) -and ($originals[$path].sha256 -cne $sha -or $originals[$path].bytes -ne $item.Length)) { throw 'PIN_CONFLICT' }
    $originals[$path]=$row
    return $row
}
function Document([string]$path,[string]$sha) {
    [void](Pin $path $sha)
    return Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
function NewJson([string]$path,$value) {
    Ordinary $path $true
    $raw=[Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $value -Depth 64 -Compress)+"`n")
    if ($raw.Length -eq 0 -or $raw.Length -gt 8388608) { throw 'OUTPUT_BOUND' }
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { $sha=([BitConverter]::ToString($algorithm.ComputeHash($raw))).Replace('-','').ToLowerInvariant() } finally { $algorithm.Dispose() }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    return Pin $path $sha
}
foreach($path in @($out,$parent,(Join-Path $checks $runName))) { Ordinary $path $true }
$review=Pin $ReviewPath $ReviewSha 1048576
$basis=Document (Join-Path $basisRoot 'input.json') '8eb52bb87cc662ac0f2b5787694e237c55e8a7c76831cd0bee2c498b1fd12c2f'
$prior=Document (Join-Path $basisRoot 'build-selection.json') '992fae91e50044821ac4e9b4a90fb2e3af6f8dc550d8036ce090593f99d0f2ec'
$template=Document $basis.production.profile_template.path $basis.production.profile_template.sha256
$outcome=Pin (Join-Path $projectRoot 'research\cycles\v5-2026-10-20\INSTALLED-PRODUCER-DISTRIBUTION-OUTCOME.md') '604a073aecd902d99e4e25e32e92a6ae85f6d939b2e316c2b09f5118a366f9de'
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V4' -or @($basis.sdk_sources.psobject.Properties).Count -ne 144 -or
    $template.schema -cne 'DMKN_RELEASE_PRODUCER_PROFILE_TEMPLATE_V1' -or @($template.support_profile.runtime_pins).Count -ne 49) { throw 'EXACT_PRIOR_SHAPE' }
$distributionRel='software/v5/installed_production02/body_location/distribution.py'
$entryRel='software/v5/installed_production02/release_production/operator.py'
$distribution=Pin (Join-Path $projectRoot $distributionRel.Replace('/','\')) $DistributionSha 1048576
$entry=Pin (Join-Path $projectRoot $entryRel.Replace('/','\')) $EntrySha 65536
$oldEntry=$basis.sdk_sources.'v5/release_production/operator.py'
if ($oldEntry.sha256 -cne 'f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a' -or
    $basis.distribution_source.sha256 -cne 'afbea96badbead846aecc2d3014c19d38375cd2605c225ab0799ebde0ce48774') { throw 'EXACT_PREDECESSORS' }
$newMap=[ordered]@{}
foreach($row in $basis.sdk_sources.psobject.Properties) { $newMap[$row.Name]=$row.Value }
$newMap['v5/release_production/operator.py']=$entry
$replaced=0
foreach($row in $template.support_profile.runtime_pins) {
    if ($row.path -ceq 'sdk/v5/release_production/operator.py') {
        if ($row.sha256 -cne $oldEntry.sha256 -or $row.bytes -ne $oldEntry.bytes) { throw 'TEMPLATE_OLD_ENTRY' }
        $row.sha256=$entry.sha256;$row.bytes=$entry.bytes;$replaced++
    }
}
if ($replaced -ne 1) { throw 'EXACT_TEMPLATE_REPLACEMENT' }
$basis.sdk_sources=$newMap;$basis.distribution_source=$distribution
$runtime=[ordered]@{}
foreach($row in $prior.runtime_pins.psobject.Properties) {
    if ($row.Name -cne (Join-Path $basisRoot 'input.json') -and $row.Name -cne $basis.production.profile_template.path) { $runtime[$row.Name]=$row.Value }
}
if ($runtime.Count -ne 21) { throw 'PRESERVED_BUILD_RUNTIME21' }
[void][IO.Directory]::CreateDirectory($out)
$pending=Join-Path $out 'PREPARATION-PENDING.json'
try {
    [void](NewJson $pending ([ordered]@{status='PENDING'}))
    $templatePin=NewJson (Join-Path $out 'producer-template.json') $template
    $basis.production.profile_template=$templatePin
    $inputPin=NewJson (Join-Path $out 'input.json') $basis
    $runtime[$templatePin.path]=$templatePin.sha256;$runtime[$inputPin.path]=$inputPin.sha256
    $sources=[ordered]@{}
    foreach($row in $prior.sources.psobject.Properties) {
        if ($row.Name -cne 'software/v5/installed_production/body_location/distribution.py') { $sources[$row.Name]=$row.Value }
    }
    $sources[$distributionRel]=$DistributionSha
    if ($sources.Count -ne 3 -or $runtime.Count -ne 23) { throw 'EXACT_BUILD_CLOSURE' }
    $selection=NewJson (Join-Path $out 'build-selection.json') ([ordered]@{
        schema='DMKN_V5_LOCAL_CHECK_V1';name=$runName;sources=$sources;runtime_pins=$runtime
        argv=@($prior.argv[0],'-I','-S','-B',('{snapshot}\'+$distributionRel.Replace('/','\')),'build',$inputPin.path,$inputPin.sha256,(Join-Path $parent 'Mathematical Commons v5'))
        limits=$prior.limits})
    [void][IO.Directory]::CreateDirectory($parent)
    $report=NewJson (Join-Path $out 'PREPARATION.json') ([ordered]@{
        schema='DMKN_INSTALLED_PRODUCER_DISTRIBUTION_SUCCESSOR_PREPARATION_V1';status='PREPARED_NOT_EXECUTED'
        review=$review;prior_build_outcome=$outcome;input=$inputPin;template=$templatePin;selection=$selection
        sdk_sources=144;unchanged_sdk_sources=143;changed_sdk_sources=1;unchanged_core_sources=31;preparation_sources=109
        installation_parent=$parent;build_executed=$false;originals=$originals
        completion_rule='Valid_only_without_PREPARATION-PENDING.json_or_PREPARATION-FAILED.json'})
    foreach($row in @($originals.Values)) { [void](Pin $row.path $row.sha256) }
    if (@(Get-ChildItem -LiteralPath $out -Force).Count -ne 5 -or @(Get-ChildItem -LiteralPath $parent -Force).Count -ne 0) { throw 'FINAL_CENSUS' }
    [ordered]@{preparation=$report;input=$inputPin;selection=$selection;build_executed=$false} | ConvertTo-Json -Depth 6
    Remove-Item -LiteralPath $pending -ErrorAction Stop
} catch {
    [void](NewJson (Join-Path $out 'PREPARATION-FAILED.json') ([ordered]@{status='FAILED';error=$_.Exception.Message;build_executed=$false}))
    throw
}
