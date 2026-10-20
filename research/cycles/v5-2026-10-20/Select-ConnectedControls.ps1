# Prepare only projection/dispatch/import controls; no installation or test.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedBuilderSha,
    [Parameter(Mandatory=$true)][string]$ExpectedTestSha
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
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$inputPath = Join-Path $checks 'distribution-03-input.json'
$inputSha = 'd71ab60ff1be199e86278fa10fe9a84a6161b822343ad90a35594d0e98a40042'
Require-Digest $inputPath $inputSha
$inputValue = Get-Content -LiteralPath $inputPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $inputValue.sdk_sources.psobject.Properties) {
    $path = $property.Value.path
    if (-not $path.StartsWith($projectRoot+'\software\v5\', [StringComparison]::Ordinal)) {
        throw 'SDK_INPUT_SOURCE_SCOPE'
    }
    $relative = $path.Substring($projectRoot.Length+1).Replace('\','/')
    Require-Digest $path $property.Value.sha256
    if ($sources.Contains($relative) -and $sources[$relative] -cne $property.Value.sha256) {
        throw 'CONFLICTING_SOURCE_PIN'
    }
    $sources[$relative] = $property.Value.sha256
}
$extra = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/distribution_complete/distribution.py' = '8cf3b4dfa448481a9facb0cb0ae892ad07305c6fd1d75bbdcafac149e575ac4f'
    'software/v5/distribution_complete/select_inputs.py' = '7c836fc33fa8af75a60e94241495dbd45a06cec5a81dde5c6aa441666688ed25'
    'software/v5/distribution_complete/test_complete.py' = '5852436bfde11cb4f7737dfde4209e68a7acb52ffd0e47c1ebf7f3abc1982c7a'
    'software/v5/client/supplier_resilient/workspace_evidence.py' = 'a7c4979c35e904f096cba23b7fcb5cb8361e4679fc16d37d2fcec69041afd5ab'
    'software/v5/staging_members/workspace_staged.py' = '1a0922c395eb233f6fb4f1e8b10b5c538d69d445c732a9ae492539b568877f8d'
    'software/v5/client/supplier_resilient/semantic_reader.py' = '9b82de53bdcc8db74908622fc43c965a7b003111a752a8f579d25b5964dffe60'
    'software/v5/transport/acquisition_resilience.py' = '43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d'
    'software/v5/client/serve_advertised.py' = '80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed'
    'software/v5/distribution_connected/distribution.py' = $ExpectedBuilderSha
    'software/v5/distribution_connected/test_distribution.py' = $ExpectedTestSha
}
foreach ($property in $extra.GetEnumerator()) {
    Require-Digest (Join-Path $projectRoot $property.Key) $property.Value
    if ($sources.Contains($property.Key)) { throw 'EXTRA_SOURCE_COLLISION' }
    $sources[$property.Key] = $property.Value
}
$basisPath = Join-Path $checks 'advertised-service-controls-01-selection.json'
Require-Digest $basisPath 'e450cbe5590f28e5b857d50eb3c48fa71488f1b1742070e59f7f62946010c3fc'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
Require-Digest $inputValue.base_manifest.path $inputValue.base_manifest.sha256
$runtime[$inputPath] = $inputSha
$runtime[$inputValue.base_manifest.path] = $inputValue.base_manifest.sha256
$name = 'connected-distribution-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
$selected = [ordered]@{
    schema = 'DMKN_V5_LOCAL_CHECK_V1'; name = $name
    sources = $sources; runtime_pins = $runtime
    argv = @($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\distribution_connected\test_distribution.py', '--output', '{output}')
    limits = [ordered]@{
        cpu_seconds=20; wall_seconds=60; memory_mib=128; active_processes=2
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath; sha256=(Digest $selectionPath)
    sources=$sources.Count; runtime_pins=$runtime.Count; executed=$false} | ConvertTo-Json
