# Prepare one genuine direct-I public-facade workload. No launch or proof here.
param(
    [Parameter(Mandatory=$true)][string]$BuildInputSha256,
    [Parameter(Mandatory=$true)][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][string]$WorkloadReviewSha256
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
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
function Pinned([string]$relative, [long]$size, [string]$digest) {
    $path = Join-Path $projectRoot $relative
    Require-Digest $path $digest
    if ((Get-Item -LiteralPath $path).Length -ne $size) { throw ('INPUT_SIZE: '+$relative) }
    return [ordered]@{path=$path;bytes=$size;sha256=$digest}
}
$cycle = Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
Require-Digest (Join-Path $cycle 'TERMINAL-I-WORKLOAD-REVIEW.md') $WorkloadReviewSha256
$original = Join-Path $projectRoot 'product-local/v5-distribution-body-custody-01/mirror-method01-inputs/installed-mirror-method-01-request.json'
Require-Digest $original 'b4f42e958a6a5e3e9e5ab8ea9965d97babc2067cc044faf564b64bbfa741473a'
$basis = Get-Content -LiteralPath $original -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_INSTALLED_REQUEST_V1' -or $basis.name -cne 'installed-mirror-method-01' -or
    $basis.runtime_mode -cne 'aggregate') { throw 'REQUEST_BASIS' }
$mapPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-terminal-i-01-input.json'
Require-Digest $mapPath $BuildInputSha256
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-terminal-i-01'
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
$sourceRows = [ordered]@{
    'owner.py' = @('software/v5/examples/terminal_i/owner.py',21432,'885138decc4950b307f71d6f98ca3ffbae4ba0bf6a1ee19454746f8e1b638e21')
    'congruence_query.py' = @('software/v5/examples/terminal_i/congruence_query.py',2415,'07a323edd3b10f94f6fc7f9790191b1145666b547b4575c70c4a7261b3d8fadd')
    'circulation.py' = @('software/v5/examples/mirror_method/owner.py',29546,'43c3a2eeebcccdfa05c00855887068d98084755e6c5169168dab3787d3208978')
    'formal_terms.py' = @('software/v5/examples/mirror_method/method_query.py',4589,'0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642')
    'contribution.py' = @('software/v5/examples/contribution.py',5146,'ce82e170e1fad04beeb0be8722c89d748e381762b4957dfaf7b5850e2a57495c')
}
$rawSources = [ordered]@{}
$ownerSources = [ordered]@{}
foreach ($key in $sourceRows.Keys) {
    $row = $sourceRows[$key]
    $pin = Pinned $row[0] $row[1] $row[2]
    $rawSources[$key] = [IO.File]::ReadAllBytes($pin.path)
    $ownerSources[$key] = [ordered]@{bytes=$pin.bytes;sha256=$pin.sha256}
}
$template = Pinned 'software/v5/examples/terminal_i/TernaryCongruence.lean.in' 551 '586f33a0623679a7fedef12b453d269e54c2206ded4bc48142b91568351824b3'
$rawSources['TernaryCongruence.lean.in'] = [IO.File]::ReadAllBytes($template.path)
$receipt = Pinned 'experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin' 223594 '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47'
$journal = Pinned 'experiments/v5-local-checks/module-base-snapshot-03/evidence/base.expected-journal' 184 '22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682'
$bundle = Pinned 'experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json' 53769 '09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926'
$data = Join-Path $parent 'terminal-i01-inputs'
$operations = Join-Path $parent 'terminal-i01-operations'
$state = [ordered]@{
    provider_workspace_path = (Join-Path $parent 'terminal-i01-provider')
    first_workspace_path = (Join-Path $parent 'terminal-i01-first')
    second_workspace_path = (Join-Path $parent 'terminal-i01-second')
    first_domain_path = (Join-Path $parent 'terminal-i01-first-trust')
    second_domain_path = (Join-Path $parent 'terminal-i01-second-trust')
}
foreach ($path in @($data,$operations)+@($state.Values)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$config = $basis.parameters.workspace_config
if ($config.wire_profile.schema -cne 'DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V1' -or
    $config.wire_profile.proof_form -cne 'mixed-or-certified-terminal-v1') { throw 'V1_PROFILE_BASIS' }
# Exact public_profile(image, terminal_i=True) delta; no product import is run.
$config.wire_profile.schema = 'DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V2'
$config.wire_profile.proof_form = 'mixed-or-certified-terminal-v2'
$config.wire_profile | Add-Member -NotePropertyName terminal_i_packet_schema -NotePropertyValue 'DMKN_CERTIFIED_TERMINAL_I_V1'
$template.path = Join-Path $data 'TernaryCongruence.lean.in'
$parameters = [ordered]@{
    schema='DMKN_V5_TERMINAL_I_OWNER_V1';action='explicit-temporary-adoption-and-terminal-i-circulation'
    runtime_adoption=$basis.parameters.runtime_adoption;foundation=$basis.parameters.foundation
    receipt=$receipt;journal=$journal;bundle=$bundle;template=$template;workspace_config=$config
    operation_limits=$basis.parameters.first_operation_limits
    author_limits=$basis.parameters.author_limits;admission_limits=$basis.parameters.admission_limits
    first_domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
    second_domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
}
foreach ($key in $state.Keys) { $parameters[$key] = $state[$key] }
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1';name='installed-terminal-i-01';workspace_root=$operations
    parameters=$parameters;limits=$basis.limits;output_limits=$basis.output_limits
    owner=[ordered]@{root=$data;entry='owner.py';sources=$ownerSources};runtime_mode='aggregate'
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
foreach ($key in $rawSources.Keys) {
    New-Bytes (Join-Path $data $key) $rawSources[$key]
    $expected = if ($key -ceq 'TernaryCongruence.lean.in') { $template.sha256 } else { $ownerSources[$key].sha256 }
    Require-Digest (Join-Path $data $key) $expected
}
$requestPath = Join-Path $data ($request.name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath;request_sha256=$requestSha;release_sha256=$ReleaseSha256;
    runtime_invoked=$false;new_crypto_production=$false;argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReleaseSha256,'run',$requestPath,$requestSha)} | ConvertTo-Json -Depth 8
