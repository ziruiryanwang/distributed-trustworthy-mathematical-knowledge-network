# Prepare the exact small source-map delta; no build/install/runtime launch.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedBuilderSha,
    [Parameter(Mandatory=$true)][string]$InputSchema,
    [ValidateSet('mathematical-client-v1','mathematical-client-location-v1')]
    [string]$BaseRole = 'mathematical-client-location-v1'
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Pinned-Row([string]$relative, [string]$expected) {
    $path = Join-Path $projectRoot $relative
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: ' + $path)
    }
    [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$expected}
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'distribution-03-input.json'
if ((Digest $basisPath) -cne 'd71ab60ff1be199e86278fa10fe9a84a6161b822343ad90a35594d0e98a40042') {
    throw 'DISTRIBUTION03_INPUT_CHANGED'
}
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V2' -or
    $basis.base_role -cne 'mathematical-client-v1' -or
    $InputSchema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3') { throw 'CLOSED_SUCCESSOR_INPUT_SCHEMA' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) {
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 103) { throw 'BASIS_SDK_CENSUS' }
$sources['v5/client/workspace_evidence.py'] = Pinned-Row `
    'software/v5/client/supplier_resilient/workspace_evidence.py' `
    'a7c4979c35e904f096cba23b7fcb5cb8361e4679fc16d37d2fcec69041afd5ab'
$sources['v5/client/workspace_staged.py'] = Pinned-Row `
    'software/v5/staging_members/workspace_staged.py' `
    '1a0922c395eb233f6fb4f1e8b10b5c538d69d445c732a9ae492539b568877f8d'
$sources['v5/client/semantic_reader.py'] = Pinned-Row `
    'software/v5/client/supplier_resilient/semantic_reader.py' `
    '9b82de53bdcc8db74908622fc43c965a7b003111a752a8f579d25b5964dffe60'
$sources['v5/transport/acquisition_resilience.py'] = Pinned-Row `
    'software/v5/transport/acquisition_resilience.py' `
    '43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d'
$sources['v5/client/serve_advertised.py'] = Pinned-Row `
    'software/v5/client/serve_advertised.py' `
    '80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed'
if ($sources.Count -ne 106) { throw 'SUCCESSOR_SDK_CENSUS' }
$basis.sdk_sources = $sources
$basis.distribution_source = Pinned-Row `
    'software/v5/distribution_connected/distribution.py' $ExpectedBuilderSha
$basis.schema = $InputSchema
$basis.base_role = $BaseRole
$target = Join-Path $checks 'distribution-connected-01-input.json'
if (Test-Path -LiteralPath $target) { throw 'FRESH_INPUT_REQUIRED' }
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($basis | ConvertTo-Json -Depth 64)+"`n")
if ($raw.Length -gt 8*1024*1024) { throw 'INPUT_BYTE_BOUND' }
$stream = [IO.File]::Open($target, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$target; sha256=(Digest $target); base_role=$BaseRole;
    sdk_sources=$sources.Count; build_executed=$false} | ConvertTo-Json
