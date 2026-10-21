# Stage a reviewed two-owner method-use request; no runtime is invoked.
param([Parameter(Mandatory=$true)][string]$ReviewedSourcesJson)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$expected, [long]$maximum=8388608) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or $item.Length -le 0 -or $item.Length -gt $maximum -or
        $expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function New-Bytes([string]$path, [byte[]]$raw) {
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$basisPath = Join-Path $projectRoot 'experiments/v5-local-checks/interface-view-actual-01-inputs/plan.json'
Require-Digest $basisPath '99492605f7b1c868f4661f614db7f764a81fd0c4a4a391d882855ad6adf1aa96'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_CLIENT_LAUNCH_V1') { throw 'BASIS_SCHEMA' }
$mapPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-body-custody-01-input.json'
$mapSha = '995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be'
Require-Digest $mapPath $mapSha
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-body-custody-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releaseSha = '8e93486cadb5806d6470d7a8920803a9a4bad39260dd72f3be3498f699eeeb1e'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $releaseSha
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $mapSha -or
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
$required = @('owner.py','contribution.py','method_query.py','MirrorInvolution.lean.in','MirrorInjectivity.lean.in')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedSourcesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne $required.Count -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) {
    throw 'EXACT_REVIEWED_SOURCE_SET'
}
$rawSources = [ordered]@{}
foreach ($key in $required) {
    $source = if ($key -ceq 'contribution.py') {
        Join-Path $projectRoot 'software/v5/examples/contribution.py'
    } else { Join-Path $projectRoot ('software/v5/examples/mirror_method/'+$key) }
    Require-Digest $source $reviewed.$key 131072
    $rawSources[$key] = [IO.File]::ReadAllBytes($source)
}
$packet = [ordered]@{
    path=(Join-Path $projectRoot 'product-local/v5-distribution-interface-01/evaluator-commons/operations/121800ebd03cd37174e81c1d1bbed5f5e0aec4715d968612db9d7f6f1ba7dad3/preparation/author-1/mixed-packet.json')
    bytes=498641; sha256='efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b'
}
Require-Digest $packet.path $packet.sha256 $packet.bytes
if ((Get-Item -LiteralPath $packet.path).Length -ne $packet.bytes) { throw 'PACKET_SIZE' }
$data = Join-Path $parent 'mirror-method01-inputs'
$operations = Join-Path $parent 'mirror-method01-operations'
$firstWorkspace = Join-Path $parent 'mirror-method01-first'
$secondWorkspace = Join-Path $parent 'mirror-method01-second'
$providerWorkspace = Join-Path $parent 'mirror-method01-provider'
$firstDomain = Join-Path $parent 'mirror-method01-first-trust'
$secondDomain = Join-Path $parent 'mirror-method01-second-trust'
foreach ($path in @($data,$operations,$firstWorkspace,$secondWorkspace,$providerWorkspace,$firstDomain,$secondDomain)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$config = $basis.parameters.workspace_config
$config.packet_envelope.deltas = 3
$config.packet_envelope.edges = 8
function Operation-Limits([int]$acquisitionCpu, [int]$calls) {
    return [ordered]@{
        wall_seconds=210; controller_cpu_seconds=120; calls=$calls; input_bytes=67108864
        worker_cpu_seconds=(45+$acquisitionCpu); output_bytes=134217728; output_entries=1024
        acquisition=[ordered]@{requests=128;reply_bytes=33554432;verify_attempts=2
            verification_input_bytes=67108864;worker_cpu_seconds=$acquisitionCpu}
        imports=[ordered]@{max_sources=1;max_members=8;max_receipts=1;max_calls=8192
            submitted_bytes=33554432;data_bytes=8388608}
    }
}
# Each grant starts only at its own predeclared stage. These are separate owners,
# not retries. The shared outer Job bounds total actual work even when inner
# maxima cannot all be spent: controller maxima240 + worker maxima210 > outer300.
$parameters = [ordered]@{
    schema='DMKN_V5_MIRROR_METHOD_OWNER_V1'
    action='explicit-temporary-adoption-and-method-circulation'
    runtime_adoption=@{'$installed'='runtime_adoption'}; foundation=@{'$installed'='foundation'}
    packet=$packet;workspace_config=$config
    first_workspace_path=$firstWorkspace; second_workspace_path=$secondWorkspace
    provider_workspace_path=$providerWorkspace
    first_domain_path=$firstDomain; second_domain_path=$secondDomain
    first_domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
    second_domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
    first_operation_limits=(Operation-Limits 50 192);second_operation_limits=(Operation-Limits 70 256)
    author_limits=[ordered]@{cpu_seconds=45;wall_seconds=90;memory_mib=768}
    admission_limits=[ordered]@{native_cpu_seconds=10;receipt_cpu_seconds=10;wall_seconds=60;memory_mib=512}
    first_template=[ordered]@{path=(Join-Path $data 'MirrorInvolution.lean.in')
        bytes=$rawSources['MirrorInvolution.lean.in'].Length;sha256=$reviewed.'MirrorInvolution.lean.in'}
    second_template=[ordered]@{path=(Join-Path $data 'MirrorInjectivity.lean.in')
        bytes=$rawSources['MirrorInjectivity.lean.in'].Length;sha256=$reviewed.'MirrorInjectivity.lean.in'}
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
foreach ($key in $required) {
    New-Bytes (Join-Path $data $key) $rawSources[$key]
    Require-Digest (Join-Path $data $key) $reviewed.$key
}
$ownerSources = [ordered]@{}
foreach ($key in @('owner.py','contribution.py','method_query.py')) {
    $ownerSources[$key] = [ordered]@{bytes=$rawSources[$key].Length;sha256=$reviewed.$key}
}
$name = 'installed-mirror-method-01'
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1';name=$name;workspace_root=$operations
    parameters=$parameters
    limits=[ordered]@{cpu_seconds=300;wall_seconds=600;memory_mib=1024
        active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}
    output_limits=[ordered]@{bytes=268435456;entries=8192}
    owner=[ordered]@{root=$data;entry='owner.py';sources=$ownerSources}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath;request_sha256=$requestSha;release_sha256=$releaseSha
    runtime_invoked=$false;new_crypto_production=$false;argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$releaseSha,'run',$requestPath,$requestSha)} | ConvertTo-Json -Depth 8
