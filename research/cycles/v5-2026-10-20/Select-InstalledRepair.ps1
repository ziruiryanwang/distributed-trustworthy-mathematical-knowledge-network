# Select only reviewed, fresh changed-boundary work. Never runs the command.
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('distribution-controls','runtime-controls','build')]
    [string]$Mode,
    [Parameter(Mandatory=$true)][string]$ExpectedSourceSha,
    [string]$ExpectedTestSha,
    [string]$ExpectedInputSha
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: ' + $path)
    }
}
function Save-NewJson([string]$path, $value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew,
        [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'distribution-controls-01-selection.json'
Require-Digest $basisPath 'b8828e68483c57cbad17b29c88ef80e45afbe471c57312bc227d41385a6b492a'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$limits = [ordered]@{cpu_seconds=20;wall_seconds=60;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
if ($Mode -eq 'runtime-controls') {
    $sourceKey = 'software/v5/runtime_efficient/admission/pin_phase.py'
    $testKey = 'software/v5/runtime_efficient/test_pin_phase.py'
    $name = 'installed-pin-phase-controls-01'
    Require-Digest (Join-Path $projectRoot $sourceKey) $ExpectedSourceSha
    Require-Digest (Join-Path $projectRoot $testKey) $ExpectedTestSha
    $sources[$sourceKey] = $ExpectedSourceSha
    $sources[$testKey] = $ExpectedTestSha
    foreach ($relative in @('admission/verifier.py','mixed_claims/receiver.py','mixed_claims/imports_atomic.py')) {
        $key = 'software/v5/runtime_efficient/' + $relative
        $sources[$key] = Digest (Join-Path $projectRoot $key)
    }
    $argv = @($basis.argv[0],'-I','-S','-B',("{snapshot}\" + $testKey.Replace('/','\')),'--output','{output}')
} else {
    $sourceKey = 'software/v5/distribution_complete/distribution.py'
    Require-Digest (Join-Path $projectRoot $sourceKey) $ExpectedSourceSha
    $sources[$sourceKey] = $ExpectedSourceSha
    if ($Mode -eq 'distribution-controls') {
        $testKey = 'software/v5/distribution_complete/test_complete.py'
        Require-Digest (Join-Path $projectRoot $testKey) $ExpectedTestSha
        $sources[$testKey] = $ExpectedTestSha
        $selectorKey = 'software/v5/distribution_complete/select_inputs.py'
        $sources[$selectorKey] = Digest (Join-Path $projectRoot $selectorKey)
        $name = 'installed-complete-controls-01'
        $argv = @($basis.argv[0],'-I','-S','-B',("{snapshot}\" + $testKey.Replace('/','\')),'--output','{output}')
    } else {
        $name = 'distribution-build-03'
        $inputPath = Join-Path $checks 'distribution-03-input.json'
        Require-Digest $inputPath $ExpectedInputSha
        $value = Get-Content -LiteralPath $inputPath -Raw | ConvertFrom-Json
        if ($value.distribution_source.sha256 -cne $ExpectedSourceSha) { throw 'BUILD_SOURCE_BINDING' }
        $destination = Join-Path $projectRoot 'product-local\v5-distribution-03\Mathematical Commons v5'
        if (Test-Path -LiteralPath $destination) { throw 'FRESH_INSTALLATION_REQUIRED' }
        $argv = @($basis.argv[0],'-I','-S','-B',("{snapshot}\" + $sourceKey.Replace('/','\')),
            'build',$inputPath,$ExpectedInputSha,$destination)
        $limits = [ordered]@{cpu_seconds=60;wall_seconds=180;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
    }
}
foreach ($key in $sources.Keys) { Require-Digest (Join-Path $projectRoot $key) $sources[$key] }
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
Save-NewJson $selectionPath ([ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources;
    runtime_pins=$runtime; argv=$argv; limits=$limits
})
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;executed=$false} | ConvertTo-Json
