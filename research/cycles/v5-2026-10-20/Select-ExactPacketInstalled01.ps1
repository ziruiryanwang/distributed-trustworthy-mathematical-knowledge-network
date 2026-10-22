# Prepare one public installed exact-stage/I-import request. Never launches it.
param(
    [Parameter(Mandatory=$true)][string]$BuildInputSha256,
    [Parameter(Mandatory=$true)][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][string]$WorkloadReviewSha256
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }

function Ordinary([string]$path, [bool]$directory=$false, [bool]$fresh=$false) {
    $full = [IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $full.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) {
        throw ('EXACT_PATH_SCOPE:'+ $path)
    }
    $cursor = $full
    while ($cursor -and $cursor.Length -ge $projectRoot.Length) {
        if (Test-Path -LiteralPath $cursor) {
            $item = Get-Item -LiteralPath $cursor
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw ('EXACT_REPARSE_PATH:'+ $cursor)
            }
        }
        $cursor = [IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) {
        if (Test-Path -LiteralPath $full) { throw ('FRESH_OUTPUT_REQUIRED:'+ $full) }
    } else {
        $item = Get-Item -LiteralPath $full
        if ([bool]$item.PSIsContainer -ne $directory) { throw ('EXACT_PATH_KIND:'+ $full) }
    }
    return $full
}
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Pin([string]$path, [string]$expected, [long]$maximum=8388608) {
    [void](Ordinary $path)
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or
        (Get-Item -LiteralPath $path).Length -gt $maximum -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED:'+ $path)
    }
}
function Pinned([string]$relative, [long]$size, [string]$digest) {
    $path = Join-Path $projectRoot $relative
    Require-Pin $path $digest
    if ((Get-Item -LiteralPath $path).Length -ne $size) { throw ('EXACT_INPUT_SIZE:'+ $relative) }
    return [ordered]@{path=$path;bytes=$size;sha256=$digest}
}
function New-Bytes([string]$path, [byte[]]$raw) {
    [void](Ordinary $path $false $true)
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'EXACT_STAGED_BOUND' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
function Json-Bytes($value) {
    return [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
}

$cycle = Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
Require-Pin (Join-Path $cycle 'EXACT-PACKET-INSTALLED-SOURCE-REVIEW.md') $WorkloadReviewSha256
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$basisMapPath = Join-Path $checks 'distribution-managed-storage-01-input.json'
Require-Pin $basisMapPath 'a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4'
$basisMap = Get-Content -LiteralPath $basisMapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$mapPath = Join-Path $checks 'distribution-exact-packet-01-input.json'
Require-Pin $mapPath $BuildInputSha256
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-exact-packet-01'
[void](Ordinary $parent $true)
$install = Join-Path $parent 'Mathematical Commons v5'
[void](Ordinary $install $true)
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Pin $releasePath $ReleaseSha256
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $BuildInputSha256 -or
    $map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $map.base_role -cne 'mathematical-client-location-v1' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 129 -or
    @($map.sdk_sources.psobject.Properties).Count -ne 129 -or
    @($basisMap.sdk_sources.psobject.Properties).Count -ne 129) { throw 'EXACT_RELEASE_PROFILE' }
$selected = [ordered]@{
    'v5/evidence_network/transport.py'='b34032085bca3ddbd248afe57e655777a140d2c34b6f33ea61b80721a07b926c'
    'v5/placement/controller.py'='77820241984b9dc7ba5d2117a4b11bc89bf217b81697ed8d8ce90fff15e115f2'
    'v5/client/workspace_evidence.py'='3f39d9b594490f04e2737c0f0595c881785a9a6a168cf8fc679d25a5cdef700e'
    'v5/client/workspace_staged.py'='5d96c8cb891eabeb083b0bc501df1a7b268c21b73f4c17da7eb536d2428ad995'
    'v5/client/semantic_reader.py'='253b0ffb5825de15c239be785edcda7e15647038716679402cdf990b81f4128d'
    'v5/client/managed_owner.py'='9a459df2cf2c81b953044b4b5172aaefb9a3001cede6f3a1a23b29f8beb6dcb1'
}
$totalSources = [long]0
$changed = 0
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $logical = $property.Name
    $source = $property.Value
    $target = $release.sdk_sources.$logical
    $row = $release.files.$target
    $old = $basisMap.sdk_sources.$logical
    if ($target -cne ('sdk/'+$logical) -or $row.bytes -ne $source.bytes -or
        $row.sha256 -cne $source.sha256) { throw ('EXACT_SDK_MAP:'+ $logical) }
    if ($selected.Contains($logical)) {
        $expectedPath = Join-Path $projectRoot ('software/v5/exact_packet/'+$logical.Substring(3))
        if ($source.path -cne $expectedPath -or $source.sha256 -cne $selected[$logical] -or
            $source.sha256 -ceq $old.sha256) { throw ('EXACT_SDK_SUCCESSOR:'+ $logical) }
        $changed += 1
    } elseif ($source.path -cne $old.path -or $source.bytes -ne $old.bytes -or
              $source.sha256 -cne $old.sha256) { throw ('EXACT_UNCHANGED_SDK:'+ $logical) }
    Require-Pin $source.path $source.sha256 2097152
    $payload = Join-Path $install $target
    Require-Pin $payload $row.sha256 2097152
    if ((Get-Item -LiteralPath $source.path).Length -ne $source.bytes -or
        (Get-Item -LiteralPath $payload).Length -ne $row.bytes) { throw 'EXACT_SDK_SIZE' }
    $totalSources += $row.bytes
}
if ($changed -ne 6) { throw 'EXACT_SIX_SUCCESSORS' }
Require-Pin (Join-Path $install 'distribution.py') 'eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'

$original = Join-Path $projectRoot 'product-local/v5-distribution-terminal-i-01/terminal-i01-inputs/installed-terminal-i-01-request.json'
Require-Pin $original '9df159b6b10b8e14b4b36bfd0557cba8790c278224a7c318bd03e888d61a7565' 1048576
$basis = Get-Content -LiteralPath $original -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_INSTALLED_REQUEST_V1' -or $basis.name -cne 'installed-terminal-i-01' -or
    $basis.runtime_mode -cne 'aggregate' -or
    $basis.parameters.workspace_config.wire_profile.schema -cne 'DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V2' -or
    $basis.parameters.workspace_config.wire_profile.proof_form -cne 'mixed-or-certified-terminal-v2') {
    throw 'EXACT_REQUEST_BASIS'
}
$sourceRows = [ordered]@{
    'owner.py'=@('software/v5/exact_packet/installed_owner.py',19475,'ba555bb6cae82eb373af1180c5a7e530a3525649ce4305df16582b1eaa3d7685')
    'terminal_fixture.py'=@('software/v5/examples/terminal_i/owner.py',21432,'885138decc4950b307f71d6f98ca3ffbae4ba0bf6a1ee19454746f8e1b638e21')
}
$rawSources = [ordered]@{}
$ownerSources = [ordered]@{}
foreach ($key in $sourceRows.Keys) {
    $row = $sourceRows[$key]
    $pin = Pinned $row[0] $row[1] $row[2]
    $rawSources[$key] = [IO.File]::ReadAllBytes($pin.path)
    $ownerSources[$key] = [ordered]@{bytes=$pin.bytes;sha256=$pin.sha256}
    $totalSources += $pin.bytes
}
if ($totalSources -gt 67108864 -or $ownerSources.Count -ne 2) { throw 'EXACT_131_SOURCE_BOUND' }
$receipt = Pinned 'experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin' 223594 '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47'
$journal = Pinned 'experiments/v5-local-checks/module-base-snapshot-03/evidence/base.expected-journal' 184 '22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682'
$bundle = Pinned 'experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json' 53769 '09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926'
$foundationName = $release.roles.foundation
$foundation = $release.files.$foundationName
if ($foundation.bytes -ne 23313 -or $foundation.sha256 -cne '736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c') {
    throw 'EXACT_INSTALLED_FOUNDATION_ROLE'
}
Require-Pin (Join-Path $install $foundationName) $foundation.sha256
if ((Get-Item -LiteralPath (Join-Path $install $foundationName)).Length -ne $foundation.bytes) {
    throw 'EXACT_INSTALLED_FOUNDATION_SIZE'
}

$data = Join-Path $parent 'exact-packet01-inputs'
$operations = Join-Path $parent 'exact-packet01-operations'
$state = [ordered]@{
    provider_workspace_path=(Join-Path $parent 'exact-packet01-provider')
    workspace_path=(Join-Path $parent 'exact-packet01-consumer')
    domain_path=(Join-Path $parent 'exact-packet01-trust')
}
foreach ($path in @($data,$operations)+@($state.Values)) { [void](Ordinary $path $true $true) }
$operation = [ordered]@{
    wall_seconds=150;controller_cpu_seconds=90;calls=96;input_bytes=33554432;worker_cpu_seconds=20
    output_bytes=134217728;output_entries=1024
    acquisition=[ordered]@{requests=8;reply_bytes=4194304;verify_attempts=1;verification_input_bytes=2097152;worker_cpu_seconds=20}
    imports=[ordered]@{max_sources=1;max_members=8;max_receipts=1;max_calls=8192;submitted_bytes=33554432;data_bytes=8388608}
}
$admission = [ordered]@{native_cpu_seconds=10;receipt_cpu_seconds=10;wall_seconds=60;memory_mib=512}
$parameters = [ordered]@{
    schema='DMKN_V5_EXACT_PACKET_INSTALLED_OWNER_V1'
    action='explicit-temporary-adoption-exact-stage-and-i-import'
    runtime_adoption=[ordered]@{'$installed'='runtime_adoption'}
    foundation=[ordered]@{'$installed'='foundation'}
    receipt=$receipt;journal=$journal;bundle=$bundle;workspace_config=$basis.parameters.workspace_config
    operation_limits=$operation;admission_limits=$admission
    domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
}
foreach ($key in $state.Keys) { $parameters[$key] = $state[$key] }
# Keep room for installed role substitution in the launcher's65536-character bound.
$parameterJson = $parameters | ConvertTo-Json -Depth 64 -Compress
if ($parameterJson.Length -gt 49152) { throw 'EXACT_PARAMETER_BOUND' }
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1';name='installed-exact-packet-01';workspace_root=$operations
    parameters=$parameters
    limits=[ordered]@{cpu_seconds=180;wall_seconds=300;memory_mib=768;active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}
    output_limits=[ordered]@{bytes=268435456;entries=8192}
    owner=[ordered]@{root=$data;entry='owner.py';sources=$ownerSources};runtime_mode='aggregate'
}
$requestRaw = Json-Bytes $request
if ($requestRaw.Length -gt 1048576) { throw 'EXACT_REQUEST_BOUND' }
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
foreach ($key in $rawSources.Keys) {
    New-Bytes (Join-Path $data $key) $rawSources[$key]
    Require-Pin (Join-Path $data $key) $ownerSources[$key].sha256
}
$requestPath = Join-Path $data ($request.name+'-request.json')
New-Bytes $requestPath $requestRaw
$requestSha = Digest $requestPath
$prepared = [ordered]@{
    schema='DMKN_V5_EXACT_PACKET_INSTALLED_PREPARATION_V1'
    request=$requestPath;request_sha256=$requestSha;request_bytes=$requestRaw.Length
    release_sha256=$ReleaseSha256;build_input_sha256=$BuildInputSha256;review_sha256=$WorkloadReviewSha256
    sdk_sources=129;owner_sources=2;boot_sources=131;selected_source_bytes=$totalSources
    exact_product_sources=$selected;owner_source_pins=$ownerSources
    runtime_invoked=$false;new_crypto_production=$false
    argv=@((Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReleaseSha256,'run',$requestPath,$requestSha)
}
$preparedPath = Join-Path $data 'PREPARED.json'
New-Bytes $preparedPath (Json-Bytes $prepared)
[ordered]@{prepared=$preparedPath;prepared_sha256=(Digest $preparedPath);request=$requestPath;
    request_sha256=$requestSha;release_sha256=$ReleaseSha256;runtime_invoked=$false;argv=$prepared.argv} | ConvertTo-Json -Depth 8
