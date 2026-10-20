# Stage one installed public startup request; no runtime or mathematical work.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedReleaseSha,
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
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'interface-view-actual-01-inputs\plan.json'
Require-Digest $basisPath '99492605f7b1c868f4661f614db7f764a81fd0c4a4a391d882855ad6adf1aa96'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local\v5-distribution-interface-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReviewedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 108) { throw 'RELEASE_PROFILE' }
$sdk = @($basis.sources.psobject.Properties | Where-Object { $_.Name -cmatch '^(v5|portable)/' })
if ($sdk.Count -ne 108) { throw 'BASIS_PROFILE' }
foreach ($property in $sdk) {
    $target = $release.sdk_sources.($property.Name)
    $row = $release.files.$target
    if ($null -eq $row -or $row.bytes -ne $property.Value.bytes -or
        $row.sha256 -cne $property.Value.sha256) { throw ('ACTUAL_SDK_CHANGED: '+$property.Name) }
}
Require-Digest (Join-Path $install 'distribution.py') $release.files.'distribution.py'.sha256
$expected = [ordered]@{}
foreach ($key in @('mixed_claims/imports_atomic.py', 'mixed_claims/interface_projection.py',
    'mixed_claims/authoring_atomic.py', 'client/workspace_evidence.py',
    'client/workspace_staged.py', 'client/semantic_reader.py',
    'transport/semantic_staging.py', 'transport/declaration_resilience.py')) {
    $expected[$key] = $basis.sources.('v5/'+$key).sha256
}
$adapter = Join-Path $projectRoot 'software/v5/distribution_interfaces/startup.py'
Require-Digest $adapter $ReviewedAdapterSha
if ((Get-Item -LiteralPath $adapter).Length -gt 131072) { throw 'ADAPTER_BOUND' }
$adapterBytes = [IO.File]::ReadAllBytes($adapter)
$name = 'installed-interface-startup-01'
$data = Join-Path $parent 'startup-inputs'
$operations = Join-Path $parent 'startup-operations'
$workspace = Join-Path $parent 'startup-commons'
foreach ($path in @($data, $operations, $workspace)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
New-Bytes (Join-Path $data 'startup.py') $adapterBytes
Require-Digest (Join-Path $data 'startup.py') $ReviewedAdapterSha
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$operations
    parameters=[ordered]@{
        schema='DMKN_V5_DISTRIBUTION_INTERFACE_STARTUP_V1'
        runtime_adoption=@{'$installed'='runtime_adoption'}
        foundation=@{'$installed'='foundation'}
        workspace_path=$workspace; workspace_config=$basis.parameters.workspace_config
        operation_limits=$basis.parameters.operation_limits; expected_sources=$expected
    }
    limits=$basis.limits; output_limits=$basis.output_limits
    owner=[ordered]@{root=$data; entry='startup.py'; sources=[ordered]@{
        'startup.py'=[ordered]@{bytes=$adapterBytes.Length; sha256=$ReviewedAdapterSha}
    }}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath; request_sha256=$requestSha; release_sha256=$ReviewedReleaseSha;
    runtime_invoked=$false; native_calls=0; proof_calls=0; argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'), '-I', '-S', '-B',
        (Join-Path $install 'distribution.py'), 'launch', $ReviewedReleaseSha,
        'run', $requestPath, $requestSha)} | ConvertTo-Json -Depth 8
