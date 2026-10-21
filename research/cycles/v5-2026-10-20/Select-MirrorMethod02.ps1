# Prepare a fresh use of the unchanged owner01 after a separately adopted repair.
# No build, proof, launch, old-state mutation or allocation renewal occurs here.
param(
    [Parameter(Mandatory=$true)][string]$BuildInputSha256,
    [Parameter(Mandatory=$true)][string]$ReleaseSha256
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
function Require-Pin($pin) {
    Require-Digest $pin.path $pin.sha256
    if ((Get-Item -LiteralPath $pin.path).Length -ne $pin.bytes) { throw 'PIN_SIZE' }
}
function New-Bytes([string]$path, [byte[]]$raw) {
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$originalPath = Join-Path $projectRoot 'product-local/v5-distribution-body-custody-01/mirror-method01-inputs/installed-mirror-method-01-request.json'
Require-Digest $originalPath 'b4f42e958a6a5e3e9e5ab8ea9965d97babc2067cc044faf564b64bbfa741473a'
$request = Get-Content -LiteralPath $originalPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($request.schema -cne 'DMKN_V5_INSTALLED_REQUEST_V1' -or $request.name -cne 'installed-mirror-method-01' -or
    $request.runtime_mode -cne 'aggregate' -or $request.owner.entry -cne 'owner.py') { throw 'REQUEST_BASIS' }
$mapPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-validation-01-input.json'
Require-Digest $mapPath $BuildInputSha256
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-validation-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReleaseSha256
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $BuildInputSha256 -or
    @($release.sdk_sources.psobject.Properties).Count -ne 114 -or
    @($map.sdk_sources.psobject.Properties).Count -ne 114) { throw 'RELEASE_PROFILE' }
foreach ($property in $map.sdk_sources.psobject.Properties) {
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
if (@($request.owner.sources.psobject.Properties).Count -ne 3) { throw 'OWNER_SOURCE_CENSUS' }
$rawSources = [ordered]@{}
foreach ($key in @('owner.py', 'contribution.py', 'method_query.py')) {
    $pin = $request.owner.sources.$key
    $path = Join-Path $request.owner.root $key
    Require-Digest $path $pin.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $pin.bytes) { throw 'OWNER_SOURCE_SIZE' }
    $rawSources[$key] = [IO.File]::ReadAllBytes($path)
}
foreach ($key in @('first_template', 'second_template', 'packet')) { Require-Pin $request.parameters.$key }
$rawSources['MirrorInvolution.lean.in'] = [IO.File]::ReadAllBytes($request.parameters.first_template.path)
$rawSources['MirrorInjectivity.lean.in'] = [IO.File]::ReadAllBytes($request.parameters.second_template.path)
$data = Join-Path $parent 'mirror-method02-inputs'
$operations = Join-Path $parent 'mirror-method02-operations'
$destinations = [ordered]@{
    provider_workspace_path = (Join-Path $parent 'mirror-method02-provider')
    first_workspace_path = (Join-Path $parent 'mirror-method02-first')
    second_workspace_path = (Join-Path $parent 'mirror-method02-second')
    first_domain_path = (Join-Path $parent 'mirror-method02-first-trust')
    second_domain_path = (Join-Path $parent 'mirror-method02-second-trust')
}
foreach ($path in @($data, $operations)+@($destinations.Values)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
# Every operational/worker/query/census limit and all mathematical inputs stay
# byte-value identical to the pinned original request. Only fresh paths/IDs and
# the later release selection differ; no failed grant is continued or enlarged.
foreach ($key in $destinations.Keys) { $request.parameters.$key = $destinations[$key] }
$request.parameters.first_domain_id = ([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
$request.parameters.second_domain_id = ([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
$request.parameters.first_template.path = Join-Path $data 'MirrorInvolution.lean.in'
$request.parameters.second_template.path = Join-Path $data 'MirrorInjectivity.lean.in'
$request.owner.root = $data
$request.workspace_root = $operations
$request.name = 'installed-mirror-method-02'
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
foreach ($key in $rawSources.Keys) { New-Bytes (Join-Path $data $key) $rawSources[$key] }
foreach ($key in @('owner.py', 'contribution.py', 'method_query.py')) {
    Require-Digest (Join-Path $data $key) $request.owner.sources.$key.sha256
}
Require-Pin $request.parameters.first_template
Require-Pin $request.parameters.second_template
$requestPath = Join-Path $data ($request.name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath;request_sha256=$requestSha;release_sha256=$ReleaseSha256;
    runtime_invoked=$false;new_crypto_production=$false;argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReleaseSha256,'run',$requestPath,$requestSha)} | ConvertTo-Json -Depth 8
