# Stage one explicit temporary-trust installed query boundary; never execute it.
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
$inputPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-adaptive-01-input.json'
Require-Digest $inputPath $ReviewedInputSha
$inputMap = Get-Content -LiteralPath $inputPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-adaptive-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReviewedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $ReviewedInputSha -or
    @($release.sdk_sources.psobject.Properties).Count -ne 111 -or
    @($inputMap.sdk_sources.psobject.Properties).Count -ne 111) { throw 'RELEASE_PROFILE' }
foreach ($property in $inputMap.sdk_sources.psobject.Properties) {
    $target = $release.sdk_sources.($property.Name)
    $row = $release.files.$target
    if ($target -cne ('sdk/'+$property.Name) -or $null -eq $row -or
        $row.bytes -ne $property.Value.bytes -or
        $row.sha256 -cne $property.Value.sha256) { throw ('SELECTED_SDK_CHANGED: '+$property.Name) }
    $payload = Join-Path $install $target
    Require-Digest $payload $row.sha256
    if ((Get-Item -LiteralPath $payload).Length -ne $row.bytes) { throw 'SDK_PAYLOAD_SIZE' }
}
Require-Digest (Join-Path $install 'distribution.py') '6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6'
$adapter = Join-Path $projectRoot 'software/v5/located_queries/installed02.py'
Require-Digest $adapter $ReviewedAdapterSha
if ((Get-Item -LiteralPath $adapter).Length -gt 131072) { throw 'ADAPTER_BOUND' }
$adapterBytes = [IO.File]::ReadAllBytes($adapter)
$data = Join-Path $parent 'adaptive-integration02-inputs'
$operations = Join-Path $parent 'adaptive-integration02-operations'
$workspace = Join-Path $parent 'adaptive-integration02-commons'
$domain = Join-Path $parent 'adaptive-integration02-trust'
$name = 'installed-adaptive-boundary-02'
foreach ($path in @($data, $operations, $workspace, $domain)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$expected = [ordered]@{}
$changed = [ordered]@{
    'client/direct_contacts.py'='e243a094b9fdce2adef221514923bf6753d04b8cc3ed8ae60e392c0ebd804545'
    'client/workspace_validated.py'='901ffd191131a8eb293c4f11ca8a890a5edd800d3d90156dc298ff13ac15a4be'
    'client/semantic_reader.py'='ec040740ad00b913c3061156d019f40887f926bf7be1ef144b116fa366c47c0b'
    'evidence_network/transport.py'='5808c0e253b203cdf38bd2069c593888ea4814d47f756871237c38eb3e0caab7'
    'client/located_queries.py'='419df8428528203858eff69da43c7e3ed7e5634d06007dc5e30ca2f33df82c4e'
}
foreach ($key in $changed.Keys) {
    $row = $inputMap.sdk_sources.('v5/'+$key)
    if ($null -eq $row -or $row.sha256 -cne $changed[$key]) { throw ('CHANGED_SOURCE_PIN: '+$key) }
    $expected[$key] = $row.sha256
}
$operationLimits = $basis.parameters.operation_limits
$operationLimits.wall_seconds = 150
$operationLimits.controller_cpu_seconds = 90
$operationLimits.acquisition.requests = 6
$operationLimits.acquisition.reply_bytes = 4096
$parameters = [ordered]@{
    schema='DMKN_V5_ADAPTIVE_INSTALLED_V1'; action='explicit-temporary-adoption-and-query'
    runtime_adoption=@{'$installed'='runtime_adoption'}; foundation=@{'$installed'='foundation'}
    domain_path=$domain
    domain_id='78e17f0b96c982481e90bc74a2e6c504bb5fc840c3ab7554d0aa6c14e8a94231'
    workspace_path=$workspace; workspace_config=$basis.parameters.workspace_config
    operation_limits=$operationLimits; expected_sources=$expected
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
New-Bytes (Join-Path $data 'installed.py') $adapterBytes
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$operations
    parameters=$parameters
    limits=[ordered]@{active_processes=4; cpu_seconds=120; memory_mib=512;
        stderr_bytes=1048576; stdout_bytes=1048576; wall_seconds=240}
    output_limits=[ordered]@{bytes=67108864; entries=4096}
    owner=[ordered]@{root=$data; entry='installed.py'; sources=[ordered]@{
        'installed.py'=[ordered]@{bytes=$adapterBytes.Length; sha256=$ReviewedAdapterSha}}}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath; request_sha256=$requestSha; release_sha256=$ReviewedReleaseSha;
    runtime_invoked=$false; explicit_temporary_adoption=$true; argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'), '-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReviewedReleaseSha,'run',$requestPath,$requestSha)} | ConvertTo-Json -Depth 8
