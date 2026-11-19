# File-only profile-phase preparation. Does not invoke Python or the producer.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][string]$BuildOutcomePath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildOutcomeSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$parent=Join-Path $projectRoot 'product-local\v5-distribution-installed-producer-01'
$install=Join-Path $parent 'Mathematical Commons v5'
$work=Join-Path $parent 'v-continuation01'
$inputs=Join-Path $work 'inputs'
$profileOutput=Join-Path $work 'profile'
function Ordinary([string]$path,[bool]$directory=$false,[bool]$fresh=$false) {
    $full=[IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $full.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'CANONICAL_PROJECT_PATH' }
    $cursor=$full
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item=Get-Item -LiteralPath $cursor
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or
                ($cursor -cne $full -and -not $item.PSIsContainer)) { throw 'ORDINARY_PATH_REQUIRED' }
        }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) { if (Test-Path -LiteralPath $full) { throw 'FRESH_OUTPUT_REQUIRED' } }
    elseif ([bool](Get-Item -LiteralPath $full).PSIsContainer -ne $directory) { throw 'PATH_KIND' }
    return $full
}
function Digest([byte[]]$raw) {
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($raw))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}
function Pin([string]$path,[string]$expected,[long]$maximum=8388608) {
    [void](Ordinary $path)
    $size=(Get-Item -LiteralPath $path).Length
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $size -le 0 -or $size -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected -or
        (Get-Item -LiteralPath $path).Length -ne $size) { throw 'EXACT_PIN_REQUIRED' }
    return [ordered]@{path=$path;bytes=$size;sha256=$expected}
}
function NewJson([string]$path,$value) {
    [void](Ordinary $path $false $true)
    $raw=[Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $value -Depth 32 -Compress)+"`n")
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'GENERATED_JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    $row=Pin $path (Digest $raw) 1048576
    if ($row.bytes -ne $raw.Length) { throw 'SAVED_INTENDED_BYTES' }
    return $row
}
[void](Ordinary $parent $true)
[void](Ordinary $install $true)
[void](Ordinary $work $true $true)
# The root-selected outcome pin records adoption; prose is not parsed as authority.
$outcome=Pin $BuildOutcomePath $BuildOutcomeSha256 1048576
$manifestPin=Pin (Join-Path $install 'V5-RELEASE.json') $ReleaseSha256
$manifest=Get-Content -LiteralPath $manifestPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V4' -or
    @($manifest.sdk_sources.psobject.Properties).Count -ne 144 -or
    @($manifest.preparation.source_pins).Count -ne 109 -or
    $manifest.production.descriptor.path -cne 'production/ARTIFACTS.json' -or
    $manifest.production.profile_template.path -cne 'production/PROFILE-TEMPLATE.json') { throw 'EXACT_INSTALLED_PRODUCER_ROLE' }
$originals=@($outcome,$manifestPin)
foreach($relative in @('distribution.py','base/receiver/runtime/python/python.exe',
    'production/ARTIFACTS.json','production/PROFILE-TEMPLATE.json')) {
    $selected=$manifest.files.$relative
    $row=Pin (Join-Path $install $relative.Replace('/','\')) $selected.sha256
    if ($row.bytes -ne $selected.bytes) { throw 'RELEASE_ROLE_LENGTH' }
    $originals+=$row
}
$python=Join-Path $install 'base\receiver\runtime\python\python.exe'
$distribution=Join-Path $install 'distribution.py'
# No complete verification is claimed here. The real public profile command
# checks its complete selected release before materialization; root audits build.
[void][IO.Directory]::CreateDirectory($work)
[void][IO.Directory]::CreateDirectory($inputs)
$pending=Join-Path $work 'PROFILE-PREPARATION-PENDING.json'
try {
    $pendingPin=NewJson $pending ([ordered]@{schema='DMKN_INSTALLED_V_PROFILE_PREPARATION_PENDING_V1';status='PENDING'})
    $request=NewJson (Join-Path $inputs 'profile-request.json') ([ordered]@{
        schema='DMKN_RELEASE_PRODUCER_PROFILE_REQUEST_V1';output_directory=$profileOutput})
    $argv=@($python,'-I','-S','-B',$distribution,'producer-profile',$ReleaseSha256,$request.path,$request.sha256)
    foreach($row in $originals) { $actual=Pin $row.path $row.sha256; if($actual.bytes -ne $row.bytes) { throw 'ORIGINAL_SIZE_CHANGED' } }
    $report=NewJson (Join-Path $work 'PROFILE-PREPARED.json') ([ordered]@{
        schema='DMKN_INSTALLED_V_PROFILE_PREPARATION_V1';status='PREPARED_NOT_EXECUTED';release=$manifestPin
        build_outcome=$outcome;originals=$originals;request=$request;profile_output=$profileOutput;argv=$argv
        runtime_invoked=$false;constructor_calls=0;snapshot_calls=0;proof_calls=0;V_success_required_for_profile=$false
        completion_rule='Valid_only_without_PROFILE-PREPARATION-PENDING.json_or_PROFILE-PREPARATION-FAILED.json'})
    foreach($row in @($request,$report,$pendingPin)) { $actual=Pin $row.path $row.sha256; if($actual.bytes -ne $row.bytes) { throw 'GENERATED_SIZE_CHANGED' } }
    if ((Test-Path -LiteralPath $profileOutput) -or @(Get-ChildItem -LiteralPath $work -Force).Count -ne 3 -or
        @(Get-ChildItem -LiteralPath $inputs -Force).Count -ne 1) { throw 'FRESH_PROFILE_OUTPUT_AND_PREPARATION_CENSUS' }
    [ordered]@{prepared=$report;request=$request;runtime_invoked=$false;argv=$argv}|ConvertTo-Json -Depth 6
    Remove-Item -LiteralPath $pending -ErrorAction Stop
} catch {
    try { [void](NewJson (Join-Path $work 'PROFILE-PREPARATION-FAILED.json') ([ordered]@{
        schema='DMKN_INSTALLED_V_PROFILE_PREPARATION_FAILURE_V1';status='FAILED';error=$_.Exception.Message;runtime_invoked=$false})) }
    catch { throw 'PROFILE_PREPARATION_FAILURE_MARKER_UNCONFIRMED_PENDING_RETAINS_FAILURE' }
    throw
}
