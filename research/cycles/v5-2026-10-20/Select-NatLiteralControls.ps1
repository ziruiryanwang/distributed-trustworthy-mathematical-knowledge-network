# Select focused importer controls using the unchanged bounded local supervisor.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedSourceSha,
    [Parameter(Mandatory=$true)][string]$ReviewedControlsSha
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'conjunction-index-controls-01-selection.json'
Require-Digest $basisPath 'c0942a6150e1d4e4ebddd3384b0c21b8433d1974547cf915d6c0bc9602e1dd03'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or
    $basis.name -cne 'conjunction-index-controls-01') { throw 'BASIS_SCHEMA' }
$sources = [ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/modules/__init__.py'='1c69237f05e6b86129605789da098235453d00b2f0139502cdbe9206d5891946'
    'software/v5/modules/codec.py'='e01b7478640d72ad5e0634443c87d99a9bf91bc65d2fc2297355b92a27649f58'
    'software/v5/modules/model.py'='0636ec3909629ee58adffa2ee8a6ced865b4898a16ba9874680228eeb774b4a6'
    'software/v5/modules/source_rows.py'='60c7255d9bf65236d684a77e2890c00567dba5bc2f72b81d13c933af237913f4'
    'software/v5/nat_literals/source_rows.py'=$ReviewedSourceSha
    'software/v5/nat_literals/controls.py'=$ReviewedControlsSha
}
foreach ($relative in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $relative) $sources[$relative]
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$name = 'nat-literal-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\nat_literals\controls.py', '--output', '{output}')
    limits=[ordered]@{
        cpu_seconds=30; wall_seconds=60; memory_mib=256; active_processes=2
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{
    path=$selectionPath; sha256=(Digest $selectionPath)
    sources=$sources.Count; runtime_pins=$runtime.Count; executed=$false
} | ConvertTo-Json
