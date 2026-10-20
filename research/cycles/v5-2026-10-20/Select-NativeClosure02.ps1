# Fresh image-binding preparation; no checker, resource or target change.
param([Parameter(Mandatory=$true)][string]$ExpectedAdapterSha)
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
$basisPath = Join-Path $checks 'native-closure-actual-01-selection.json'
Require-Digest $basisPath 'caa49ae420a08ba24bef620479cf7f28476076407a0fcbeb2a1323152f754870'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($entry in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $entry.Name) $entry.Value
    if ($entry.Name -ne 'software/v5/native_closure/actual_check.py') {
        $sources[$entry.Name] = $entry.Value
    }
}
$adapter = 'software/v5/native_closure/actual_check02.py'
Require-Digest (Join-Path $projectRoot $adapter) $ExpectedAdapterSha
$sources[$adapter] = $ExpectedAdapterSha
$runtime = [ordered]@{}
foreach ($entry in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $entry.Name $entry.Value
    $runtime[$entry.Name] = $entry.Value
}
$name = 'native-closure-actual-02'
$selectionPath = Join-Path $checks ($name + '-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
$selected = [ordered]@{
    schema=$basis.schema; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\native_closure\actual_check02.py', '--output', '{output}')
    limits=$basis.limits
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
