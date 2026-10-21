# Stage one reviewed installed custody operation. No runtime is invoked here.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedReleaseSha,
    [Parameter(Mandatory=$true)][string]$ReviewedAdapterSha
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function New-Bytes([string]$path, [byte[]]$raw) {
    if ($raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$basisPath = Join-Path $projectRoot 'experiments/v5-local-checks/client-split-check-01-plan.json'
Require-Digest $basisPath '099d8c14d205bca0d7c14db7ed8c415fb3c7306522c8312ca0562358481ed5fc'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$inputPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-body-custody-01-input.json'
$inputSha = '995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be'
Require-Digest $inputPath $inputSha
$inputMap = Get-Content -LiteralPath $inputPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-body-custody-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReviewedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $inputSha -or
    @($release.sdk_sources.psobject.Properties).Count -ne 114 -or
    @($inputMap.sdk_sources.psobject.Properties).Count -ne 114) { throw 'RELEASE_PROFILE' }
foreach ($property in $inputMap.sdk_sources.psobject.Properties) {
    $target = $release.sdk_sources.($property.Name)
    $row = $release.files.$target
    if ($target -cne ('sdk/'+$property.Name) -or $null -eq $row -or
        $row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) {
        throw ('SELECTED_SDK_CHANGED: '+$property.Name)
    }
    $payload = Join-Path $install $target
    Require-Digest $payload $row.sha256
    if ((Get-Item -LiteralPath $payload).Length -ne $row.bytes) { throw 'SDK_PAYLOAD_SIZE' }
}
Require-Digest (Join-Path $install 'distribution.py') 'eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
$adapter = Join-Path $projectRoot 'software/v5/body_location/installed01.py'
Require-Digest $adapter $ReviewedAdapterSha
if ((Get-Item -LiteralPath $adapter).Length -gt 131072) { throw 'ADAPTER_BOUND' }
$adapterBytes = [IO.File]::ReadAllBytes($adapter)
$packet = $basis.parameters.packet
if ($packet.bytes -ne 658554 -or
    $packet.sha256 -cne '6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb') { throw 'PACKET_BASIS' }
Require-Digest $packet.path $packet.sha256
if ((Get-Item -LiteralPath $packet.path).Length -ne $packet.bytes) { throw 'PACKET_SIZE' }
$data = Join-Path $parent 'custody-integration01-inputs'
$operations = Join-Path $parent 'custody-integration01-operations'
$domain = Join-Path $parent 'custody-integration01-trust'
$workspaces = [ordered]@{
    p=(Join-Path $parent 'custody-integration01-p')
    q=(Join-Path $parent 'custody-integration01-q')
    r=(Join-Path $parent 'custody-integration01-r')
}
foreach ($path in @($data, $operations, $domain)+@($workspaces.Values)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$expected = [ordered]@{}
foreach ($key in @('client/body_custody.py', 'client/workspace_evidence.py',
    'client/semantic_reader.py', 'transport/acquisition_resilience.py',
    'client/located_queries.py', 'client/serve_advertised.py')) {
    $row = $inputMap.sdk_sources.('v5/'+$key)
    if ($null -eq $row) { throw ('CHANGED_SOURCE_MISSING: '+$key) }
    $expected[$key] = $row.sha256
}
$operationLimits = $basis.parameters.reader.operation_limits
$operationLimits.wall_seconds = 210
$operationLimits.controller_cpu_seconds = 120
$operationLimits.worker_cpu_seconds = 30
$operationLimits.acquisition.requests = 40
$operationLimits.acquisition.reply_bytes = 16777216
$parameters = [ordered]@{
    schema='DMKN_V5_EXACT_CUSTODY_INSTALLED_V1'; action='explicit-temporary-adoption-and-located-body'
    runtime_adoption=@{'$installed'='runtime_adoption'}; foundation=@{'$installed'='foundation'}
    packet=$packet; domain_path=$domain
    domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
    workspace_paths=$workspaces; workspace_config=$basis.parameters.reader.workspace_config
    operation_limits=$operationLimits; expected_sources=$expected
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
New-Bytes (Join-Path $data 'installed.py') $adapterBytes
$name = 'installed-exact-custody-01'
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$operations
    parameters=$parameters
    limits=[ordered]@{active_processes=6;cpu_seconds=150;memory_mib=512;
        stderr_bytes=1048576;stdout_bytes=1048576;wall_seconds=300}
    output_limits=[ordered]@{bytes=134217728;entries=4096}
    owner=[ordered]@{root=$data;entry='installed.py';sources=[ordered]@{
        'installed.py'=[ordered]@{bytes=$adapterBytes.Length;sha256=$ReviewedAdapterSha}}}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath;request_sha256=$requestSha;release_sha256=$ReviewedReleaseSha;
    runtime_invoked=$false;explicit_temporary_adoption=$true;argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReviewedReleaseSha,'run',$requestPath,$requestSha)} | ConvertTo-Json -Depth 8
