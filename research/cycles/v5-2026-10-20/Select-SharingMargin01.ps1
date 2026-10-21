# Prepare one reviewed serial matched pair, without launching any product code.
param([Parameter(Mandatory=$true)][string]$ReviewedAdapterSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path,[string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function Row([string]$path,[string]$expected) {
    Require-Digest $path $expected
    return [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$expected}
}
function New-Json([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$mapPath=Join-Path $checks 'distribution-terminal-i-01-input.json'
$mapRow=Row $mapPath 'd3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0'
$map=Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or @($map.sdk_sources.psobject.Properties).Count -ne 114) { throw 'SDK_BASIS' }
$sources=[ordered]@{}
$runner='tools/Run-V5-Check.py'
$sources[$runner]='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Require-Digest (Join-Path $projectRoot $runner) $sources[$runner]
foreach($property in $map.sdk_sources.psobject.Properties) {
    $entry=$property.Value
    $path=[IO.Path]::GetFullPath($entry.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\',[StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    Require-Digest $path $entry.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $entry.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative=$path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative)) { throw 'DUPLICATE_SOURCE' }
    $sources[$relative]=$entry.sha256
}
$extra=[ordered]@{
    'software/v5/standalone_validation/admission/pin_phase.py'='ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881'
    'software/v5/continuing_context/mixed_claims/imports_atomic.py'='45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad'
    'software/v5/incremental_native/mixed_claims/receiver.py'='5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b'
    'software/v5/continuing_context/client/workspace_atomic.py'='32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773'
    'software/v5/examples/mirror_method/method_query.py'='0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642'
    'software/v5/sharing_margin/actual.py'=$ReviewedAdapterSha256
}
foreach($key in $extra.Keys) {
    if ($sources.Contains($key)) { throw 'SUCCESSOR_COLLISION' }
    Require-Digest (Join-Path $projectRoot $key) $extra[$key]
    $sources[$key]=$extra[$key]
}
if ($sources.Count -ne 121) { throw 'EXACT_SOURCE_CENSUS' }
$prefix=Join-Path $projectRoot 'product-local/v5-distribution-terminal-i-01/terminal-i01-operations/installed-terminal-i-01-request'
$planRow=Row (Join-Path $prefix 'launch.json') '92b30d8f32827fa9063d2ea9015d552af31884f04a7fbc9e1bde6c3cb25f0ed0'
$basis=Get-Content -LiteralPath $planRow.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_CLIENT_LAUNCH_V1') { throw 'BASIS_PLAN_SCHEMA' }
$adoption=$basis.parameters.runtime_adoption
$preparationRow=Row $adoption.preparation_profile.path 'bf895df82f32122d51ef9a1bf20f83f8160571df20f13320f5e75cf3c35e455d'
$profile=Get-Content -LiteralPath $preparationRow.path -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
function Add-Pin($entry) {
    Require-Digest $entry.path $entry.sha256
    if ((Get-Item -LiteralPath $entry.path).Length -ne $entry.bytes) { throw 'RUNTIME_SIZE' }
    if ($runtime.Contains($entry.path) -and $runtime[$entry.path] -cne $entry.sha256) { throw 'RUNTIME_PIN_CONFLICT' }
    $runtime[$entry.path]=$entry.sha256
}
foreach($entry in @($profile.producer.python,$profile.producer.python_dll)+@($profile.producer.runtime_pins)) { Add-Pin $entry }
if ($runtime.Count -ne 18) { throw 'PYTHON_CLOSURE' }
foreach($entry in @($mapRow,$planRow,$preparationRow,$basis.parameters.foundation,
    $profile.producer.supervisor_manifest,$profile.producer.host,$profile.image,$profile.native_executable,
    $adoption.native,$adoption.receipt,$adoption.aggregate.executable)+@($profile.lean_runtime_pins)) { Add-Pin $entry }
$base=$basis.installation_root
$manifest=Get-Content -LiteralPath $profile.producer.supervisor_manifest.path -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $pin=$manifest.files.$relative
    Add-Pin ([ordered]@{path=(Join-Path $base $relative);bytes=$pin.bytes;sha256=$pin.sha256})
}
$recipe=Row (Join-Path $projectRoot 'software/v5/workloads/EvaluatorUniqueness.lean') 'e9beebfd492cfe3a809ee02fd1d010ca043ea33814161b580c5d62d97fcbb686'
$receipt=Row (Join-Path $checks 'module-base-production-01/finish-0/receipt.bin') '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47'
$bundle=Row (Join-Path $checks 'receipt-prepare-01/prepared/base/bundle.json') '09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926'
$packetPath=Join-Path $projectRoot 'product-local/v5-distribution-origin-01/mirror-method03-first/operations/47cbc7c244193477517c609adbfd0b72e163dc57958848d4f9e6f8149dd6fe16/delta/1/packet.json'
$packet=Row $packetPath 'efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b'
foreach($entry in @($recipe,$receipt,$bundle,$packet)) { Add-Pin $entry }
$name='sharing-margin-01'
$inputPath=Join-Path $checks ($name+'-input.json')
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach($path in @($inputPath,$selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_SELECTION_REQUIRED: '+$path) }
}
$inputValue=[ordered]@{schema='DMKN_SHARING_MARGIN_INPUT_V1';map=$mapRow;basis_plan=$planRow
    manifest=$profile.producer.supervisor_manifest;recipe=$recipe;receipt=$receipt;bundle=$bundle;packet=$packet}
New-Json $inputPath $inputValue
$inputSha=Digest $inputPath
$runtime[$inputPath]=$inputSha
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($profile.producer.python.path,'-I','-S','-B','{snapshot}\software\v5\sharing_margin\actual.py','--output','{output}','--input',$inputPath)
    limits=[ordered]@{cpu_seconds=300;wall_seconds=600;memory_mib=1024;active_processes=6;stdout_bytes=1048576;stderr_bytes=1048576}}
New-Json $selectionPath $selection
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;selection_sha256=(Digest $selectionPath)
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
