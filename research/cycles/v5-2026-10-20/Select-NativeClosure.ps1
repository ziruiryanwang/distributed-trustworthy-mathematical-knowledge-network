# Prepare exact small-check selection only. Does not import or execute product.
param(
    [Parameter(Mandatory=$true)][ValidateSet('controls','actual')][string]$Mode,
    [Parameter(Mandatory=$true)][string]$ExpectedInitSha,
    [Parameter(Mandatory=$true)][string]$ExpectedBindingSha,
    [Parameter(Mandatory=$true)][string]$ExpectedOwnerSha,
    [Parameter(Mandatory=$true)][string]$ExpectedAdapterSha
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
$basisPath = Join-Path $checks 'supplier-controls-01-selection.json'
Require-Digest $basisPath '76e8de0f264c2396b86176d9793ff5d6b0e68a0d15733f6b3bc702004045c262'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sources = [ordered]@{}
$retained = @(
    'tools/Run-V5-Check.py',
    'software/v5/admission/__init__.py',
    'software/v5/admission/bindings.py',
    'software/v5/aggregate_claims/__init__.py',
    'software/v5/aggregate_claims/bindings.py',
    'software/v5/modules/__init__.py',
    'software/v5/modules/codec.py'
)
foreach ($relative in $retained) {
    $expected = $basis.sources.$relative
    Require-Digest (Join-Path $projectRoot $relative) $expected
    $sources[$relative] = $expected
}
$adapter = if ($Mode -eq 'controls') { 'test_owner.py' } else { 'actual_check.py' }
$additional = [ordered]@{
    'software/v5/aggregate_claims/input.py' = 'd40b611e288fd73a060df021809e403f80b1e6c16ca8b81ff2fd528d1f2fe61f'
    'software/v5/native_closure/__init__.py' = $ExpectedInitSha
    'software/v5/native_closure/binding.py' = $ExpectedBindingSha
    'software/v5/native_closure/owner.py' = $ExpectedOwnerSha
}
$additional['software/v5/native_closure/' + $adapter] = $ExpectedAdapterSha
foreach ($entry in $additional.GetEnumerator()) {
    Require-Digest (Join-Path $projectRoot $entry.Key) $entry.Value
    $sources[$entry.Key] = $entry.Value
}
$runtime = [ordered]@{}
foreach ($entry in $basis.runtime_pins.psobject.Properties) {
    # Only retained Python support, no unrelated foundation data.
    if ($entry.Name -notlike '*\receiver\runtime\python\*') { continue }
    Require-Digest $entry.Name $entry.Value
    $runtime[$entry.Name] = $entry.Value
}
if ($Mode -eq 'actual') {
    $data = [ordered]@{
        'experiments/v5-local-checks/bounded-parse-native-build-02/native_aggregate.exe' = '2306e9f32292bdee6e6638a5f9c9cc9f1f9bc288c967a6443ec8862886e942c9'
        'experiments/v5-local-checks/module-base-snapshot-03/evidence/profile2-request.json' = 'ce554d4877e0b865690f565384381a188ce13166e960a55d39106159f46c067c'
        'product-local/v5-distribution-03/contributor-commons/operations/e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a/preparation/author-1/mixed-packet.json' = '6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb'
        'product-local/v5-distribution-03/contributor-commons/operations/e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a/delta/2/native-1/stdout.txt' = 'ced1681cfe5fa2f4a2c852a8b38136742c2d34ebb0b493e827070d58ba864258'
    }
    foreach ($entry in $data.GetEnumerator()) {
        $path = Join-Path $projectRoot $entry.Key
        Require-Digest $path $entry.Value
        $runtime[$path] = $entry.Value
    }
}
$name = 'native-closure-' + $Mode + '-01'
$selectionPath = Join-Path $checks ($name + '-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
$limits = if ($Mode -eq 'controls') {
    [ordered]@{cpu_seconds=20; wall_seconds=60; memory_mib=128; active_processes=2; stdout_bytes=1048576; stderr_bytes=1048576}
} else {
    [ordered]@{cpu_seconds=55; wall_seconds=75; memory_mib=384; active_processes=3; stdout_bytes=1048576; stderr_bytes=1048576}
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        ('{snapshot}\software\v5\native_closure\' + $adapter), '--output', '{output}')
    limits=$limits
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
