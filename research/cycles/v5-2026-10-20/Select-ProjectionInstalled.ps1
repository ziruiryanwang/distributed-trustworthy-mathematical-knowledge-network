# Stage one ordinary installed import-only run. Never execute or adopt authority.
param(
    [Parameter(Mandatory=$true)][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][string]$InputSha256,
    [Parameter(Mandatory=$true)][string]$ReviewedAdapterSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$sha) {
    if ($sha -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $sha) { throw ('PIN_CHANGED: '+$path) }
}
$parent = Join-Path $projectRoot 'product-local/v5-distribution-projection-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReleaseSha256
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1') { throw 'RELEASE_PROFILE' }
Require-Digest (Join-Path $install 'distribution.py') '0db784331ba5ac8966c9b4411385fd2fc734b384a2a5ed3729b74f4bb6bff0e3'
$inputPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-projection-01-input.json'
Require-Digest $inputPath $InputSha256
$inputMap = Get-Content -LiteralPath $inputPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($inputMap.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $inputMap.base_role -cne $release.base_role -or
    @($inputMap.sdk_sources.psobject.Properties).Count -ne 113) { throw 'INPUT_MAP' }
if ($release.build_input_sha256 -cne $InputSha256 -or
    @($release.files.psobject.Properties | Where-Object {
        $_.Name.StartsWith('sdk/v5/') -or $_.Name.StartsWith('sdk/portable/')
    }).Count -ne 113) {
    throw 'RELEASE_INPUT_BINDING'
}
$expected = [ordered]@{}
$changed = @('client/workspace_evidence.py', 'discovery/authenticated_index.py',
    'discovery/discovery_store.py', 'discovery/formal_features.py', 'discovery/module_export_adapter.py',
    'client/serve_workspace.py', 'client/serve_advertised.py',
    'discovery/conclusion_fingerprint.py', 'client/base_projection.py')
foreach ($relative in $changed) {
    $logical = 'v5/'+$relative
    $row = $inputMap.sdk_sources.$logical
    $installedKey = 'sdk/'+$logical
    $held = $release.files.$installedKey
    if ($null -eq $row -or $null -eq $held -or $held.sha256 -cne $row.sha256 -or $held.bytes -ne $row.bytes) {
        throw ('INSTALLED_MAP_MISMATCH: '+$logical)
    }
    $path = Join-Path $install $installedKey
    Require-Digest $path $row.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $row.bytes) { throw ('INSTALLED_SIZE: '+$logical) }
    $expected[$relative] = [ordered]@{bytes=$row.bytes; sha256=$row.sha256}
}
$ownerRoot = Join-Path $projectRoot 'software/v5/base_projection'
$adapter = Join-Path $ownerRoot 'installed.py'
Require-Digest $adapter $ReviewedAdapterSha256
$data = Join-Path $parent 'integration-inputs'
$workspaceRoot = Join-Path $parent 'integration-operations'
$name = 'installed-projection-imports-01'
foreach ($path in @($data, $workspaceRoot)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$workspaceRoot
    parameters=[ordered]@{schema='DMKN_V5_INSTALLED_PROJECTION_IMPORT_V1'; expected_sources=$expected}
    limits=[ordered]@{active_processes=4; cpu_seconds=60; memory_mib=384;
        stderr_bytes=1048576; stdout_bytes=1048576; wall_seconds=120}
    output_limits=[ordered]@{bytes=67108864; entries=1024}
    owner=[ordered]@{root=$ownerRoot; entry='installed.py'; sources=[ordered]@{
        'installed.py'=[ordered]@{bytes=(Get-Item -LiteralPath $adapter).Length; sha256=$ReviewedAdapterSha256}}}
    runtime_mode='aggregate'
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 32)+"`n")
if ($raw.Length -gt 1048576) { throw 'REQUEST_BOUND' }
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($workspaceRoot)
$requestPath = Join-Path $data ($name+'-request.json')
$stream = [IO.File]::Open($requestPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath; request_sha256=$requestSha; release_sha256=$ReleaseSha256;
    runtime_invoked=$false; mathematical_work_selected=$false;
    argv=@((Join-Path $install 'base/receiver/runtime/python/python.exe'), '-I','-S','-B',
        (Join-Path $install 'distribution.py'), 'launch', $ReleaseSha256, 'run', $requestPath, $requestSha)} | ConvertTo-Json -Depth 8
