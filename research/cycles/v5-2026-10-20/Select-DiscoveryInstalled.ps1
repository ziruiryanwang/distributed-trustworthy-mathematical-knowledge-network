# Stage one ordinary installed structural boundary check. Never execute it here.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedReleaseSha,
    [Parameter(Mandatory=$true)][string]$ReviewedInputSha,
    [Parameter(Mandatory=$true)][string]$ReviewedAdapterSha
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
function New-Bytes([string]$path, [byte[]]$raw) {
    if ($raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew,
        [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$basisPath = Join-Path $projectRoot 'product-local/v5-distribution-interface-01/startup-inputs/installed-interface-startup-01-request.json'
Require-Digest $basisPath 'b046a7ce829bf8d1e5e50f9a2cb3f58e76807949f5cf455046a10bae9ccddfe1'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$inputPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-discovery-01-input.json'
Require-Digest $inputPath $ReviewedInputSha
$inputMap = Get-Content -LiteralPath $inputPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-discovery-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReviewedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 110 -or
    @($inputMap.sdk_sources.psobject.Properties).Count -ne 110) { throw 'RELEASE_PROFILE' }
foreach ($property in $inputMap.sdk_sources.psobject.Properties) {
    $target = $release.sdk_sources.($property.Name)
    $row = $release.files.$target
    if ($null -eq $row -or $row.bytes -ne $property.Value.bytes -or
        $row.sha256 -cne $property.Value.sha256) { throw ('SELECTED_SDK_CHANGED: '+$property.Name) }
}
Require-Digest (Join-Path $install 'distribution.py') '6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6'
$adapter = Join-Path $projectRoot 'software/v5/type_pattern/installed.py'
Require-Digest $adapter $ReviewedAdapterSha
if ((Get-Item -LiteralPath $adapter).Length -gt 131072) { throw 'ADAPTER_BOUND' }
$adapterBytes = [IO.File]::ReadAllBytes($adapter)
$data = Join-Path $parent 'integration-inputs'
$operations = Join-Path $parent 'integration-operations'
$workspace = Join-Path $parent 'integration-commons'
$name = 'installed-discovery-boundary-01'
foreach ($path in @($data, $operations, $workspace)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$configuration = $basis.parameters.workspace_config
$configuration.schema = 'DMKN_V5_CLIENT_EVIDENCE_TYPE_PATTERN_WORKSPACE_V1'
$configuration | Add-Member -NotePropertyName discovery_profile -NotePropertyValue (
    [ordered]@{schema='DMKN_MODULE_EXPORT_TYPE_PATTERN_PROFILE_V1'})
$expected = [ordered]@{}
foreach ($key in @('modules/source_rows.py','discovery/type_pattern.py',
    'discovery/module_export_adapter.py','discovery/formal_features.py',
    'discovery/authenticated_index.py','discovery/discovery_store.py',
    'client/workspace_evidence.py')) {
    $row = $inputMap.sdk_sources.('v5/'+$key)
    if ($null -eq $row) { throw ('MISSING_CHANGED_SOURCE: '+$key) }
    $expected[$key] = [ordered]@{bytes=$row.bytes; sha256=$row.sha256}
}
$parameters = [ordered]@{
    schema='DMKN_V5_INSTALLED_DISCOVERY_BOUNDARY_V1'; workspace_path=$workspace
    workspace_config=$configuration; expected_sources=$expected
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
New-Bytes (Join-Path $data 'installed.py') $adapterBytes
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$operations
    parameters=$parameters
    limits=[ordered]@{active_processes=4; cpu_seconds=60; memory_mib=384;
        stderr_bytes=1048576; stdout_bytes=1048576; wall_seconds=120}
    output_limits=[ordered]@{bytes=33554432; entries=1024}
    owner=[ordered]@{root=$data; entry='installed.py'; sources=[ordered]@{
        'installed.py'=[ordered]@{bytes=$adapterBytes.Length; sha256=$ReviewedAdapterSha}}}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{
    request=$requestPath; request_sha256=$requestSha; release_sha256=$ReviewedReleaseSha
    runtime_invoked=$false; mathematical_work_selected=$false
    argv=@((Join-Path $install 'base\receiver\runtime\python\python.exe'), '-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReviewedReleaseSha,'run',$requestPath,$requestSha)
} | ConvertTo-Json -Depth 8
