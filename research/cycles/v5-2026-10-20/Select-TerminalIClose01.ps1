# Select only the corrected failed close-lifecycle assertion, not nine passed tests.
param([Parameter(Mandatory=$true)][string]$ReviewedControlSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$basisPath = Join-Path $checks 'terminal-i-controls-01-selection.json'
Require-Digest $basisPath 'b43f3eb450219760ae80a91e29b316743b9a517b34c99d688129c067877037ec'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 122) { throw 'ORIGINAL_SOURCE_CENSUS' }
$key = 'software/v5/terminal_i/controls_close.py'
Require-Digest (Join-Path $projectRoot $key) $ReviewedControlSha256
$sources[$key] = $ReviewedControlSha256
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
}
if (@($basis.runtime_pins.psobject.Properties).Count -ne 20) { throw 'ORIGINAL_RUNTIME_CENSUS' }
$name = 'terminal-i-close-control-01'
$path = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$basis.runtime_pins
    argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\terminal_i\controls_close.py','--output','{output}')
    limits=$basis.limits
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$path;sha256=(Digest $path);sources=$sources.Count;runtime_pins=20;executed=$false} | ConvertTo-Json
