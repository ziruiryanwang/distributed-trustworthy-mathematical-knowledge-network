# Stage real reader/contributor requests after the explicitly withdrawn adoption.
# Expected failures are not mathematical work. This script does not launch them.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedReleaseSha,
    [Parameter(Mandatory=$true)][string]$ReviewedWithdrawalResultSha,
    [Parameter(Mandatory=$true)][string]$ReviewedContributorSha
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
$parent = Join-Path $projectRoot 'product-local/v5-distribution-coherent-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$operations = Join-Path $parent 'integration-operations'
$data = Join-Path $parent 'integration-inputs-denials'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReviewedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 109) { throw 'RELEASE_PROFILE' }
Require-Digest (Join-Path $install 'distribution.py') $release.files.'distribution.py'.sha256
$withdrawPath = Join-Path $operations 'installed-coherent-withdraw-01/work/coherent-integration-result.json'
Require-Digest $withdrawPath $ReviewedWithdrawalResultSha
$withdraw = Get-Content -LiteralPath $withdrawPath -Raw | ConvertFrom-Json
if ($withdraw.schema -cne 'DMKN_V5_DISTRIBUTION_COHERENT_INTEGRATION_RESULT_V1' -or
    $withdraw.status -cne 'COMPLETED' -or $withdraw.action -cne 'withdraw' -or
    @($withdraw.cleanup_errors).Count -ne 0) { throw 'WITHDRAWAL_NOT_ADOPTED' }
$closure = Get-Content -LiteralPath (Join-Path $operations 'installed-coherent-withdraw-01/RESULT.json') -Raw | ConvertFrom-Json
if ($closure.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    -not $closure.result.job_closed -or -not $closure.result.direct_child_reaped -or
    $closure.result.final_job.active_processes -ne 0) { throw 'WITHDRAWAL_NOT_CLOSED' }
$startupPath = Join-Path $parent 'integration-inputs-startup/installed-coherent-startup-01-request.json'
$startup = Get-Content -LiteralPath $startupPath -Raw | ConvertFrom-Json
$trust = $startup.parameters.trust_domain
if ($trust.directory -cne (Join-Path $parent 'integration-trust') -or
    $trust.domain_id -cne $withdraw.identity_before_withdrawal.domain_id -or
    $trust.support_id -cne $withdraw.identity_before_withdrawal.support_id -or
    $withdraw.withdrawal_marker -cne (Join-Path $trust.directory 'WITHDRAWN') -or
    -not (Test-Path -LiteralPath $withdraw.withdrawal_marker -PathType Leaf)) { throw 'WITHDRAWN_DOMAIN_BINDING' }
$readerBasisPath = Join-Path $projectRoot 'product-local/v5-distribution-02/controls/relocated-remote-01-request.json'
$contributorBasisPath = Join-Path $projectRoot 'product-local/v5-distribution-02/contributor-controls/installed-contribution-01-request.json'
Require-Digest $readerBasisPath 'dce01a835daec6f7f80f1977d7c1d90b4a79a4f1d30ab75cbe276a38aae8b23e'
Require-Digest $contributorBasisPath '49c8817e41e585143954f45b0871e0b0cee0caffcdd5d55742e842c511ea65fb'
$readerBasis = Get-Content -LiteralPath $readerBasisPath -Raw | ConvertFrom-Json
$contributorBasis = Get-Content -LiteralPath $contributorBasisPath -Raw | ConvertFrom-Json
$contributorPath = Join-Path $projectRoot 'software/v5/distribution_coherent/examples/contribute.py'
Require-Digest $contributorPath $ReviewedContributorSha
$contributorBytes = [IO.File]::ReadAllBytes($contributorPath)
Require-Digest $contributorBasis.parameters.source.path $contributorBasis.parameters.source.sha256
if ((Get-Item -LiteralPath $contributorBasis.parameters.source.path).Length -ne
    $contributorBasis.parameters.source.bytes) { throw 'RETAINED_SOURCE_SIZE' }
$readerName = 'installed-coherent-reader-denied-01'
$contributorName = 'installed-coherent-contributor-denied-01'
foreach ($path in @($data,(Join-Path $operations $readerName),
    (Join-Path $operations ($readerName+'-request')),(Join-Path $operations $contributorName),
    (Join-Path $operations ($contributorName+'-request')))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$readerParameters = [ordered]@{
    workspace_path=$startup.parameters.workspace_path
    workspace_config=$startup.parameters.workspace_config; create_workspace=$false
    operation_limits=$startup.parameters.operation_limits; trust_domain=$trust
    query=$readerBasis.parameters.reader.query
}
# No caller schema: this deliberately exercises the BUILT-IN schema injection.
# Retained query permits only loopback:1. No contact is expected or authorized.
if ($readerParameters.query.egress_policy.mode -cne 'loopback-test' -or
    $readerParameters.query.contacts.provider.host -cne '127.0.0.1' -or
    $readerParameters.query.contacts.provider.port -ne 1) { throw 'READER_QUERY_NOT_LOCAL_ONLY' }
$contributorParameters = $contributorBasis.parameters
$contributorParameters.schema = 'DMKN_V5_CONTRIBUTE_EXAMPLE_WITHDRAWAL_V1'
$contributorParameters.runtime_adoption = @{'$installed'='runtime_adoption'}
$contributorParameters.foundation = @{'$installed'='foundation'}
$contributorParameters.workspace_path = $startup.parameters.workspace_path
$contributorParameters.workspace_config = $startup.parameters.workspace_config
$contributorParameters.create_workspace = $false
$contributorParameters.operation_limits = $startup.parameters.operation_limits
$contributorParameters | Add-Member -NotePropertyName trust_domain -NotePropertyValue $trust
$readerRequest = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$readerName; workspace_root=$operations
    parameters=$readerParameters; limits=$startup.limits; output_limits=$startup.output_limits
    owner=$null; runtime_mode='aggregate'
}
$contributorRequest = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$contributorName; workspace_root=$operations
    parameters=$contributorParameters; limits=$startup.limits; output_limits=$startup.output_limits
    owner=[ordered]@{root=$data; entry='contribute.py'; sources=[ordered]@{
        'contribute.py'=[ordered]@{bytes=$contributorBytes.Length; sha256=$ReviewedContributorSha}}}
    runtime_mode='aggregate'
}
[void][IO.Directory]::CreateDirectory($data)
New-Bytes (Join-Path $data 'contribute.py') $contributorBytes
$selected = @()
foreach ($pair in @(@('reader',$readerRequest),@('run',$contributorRequest))) {
    $command, $request = $pair
    $path = Join-Path $data ($request.name+'-request.json')
    New-Bytes $path ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
    $sha = Digest $path
    $selected += [ordered]@{command=$command; request=$path; request_sha256=$sha;
        expected='TRUST_WITHDRAWN_BEFORE_WORKSPACE_OR_CLIENT'; runtime_invoked=$false;
        argv=@((Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',
            (Join-Path $install 'distribution.py'),'launch',$ReviewedReleaseSha,$command,$path,$sha)}
}
$selected | ConvertTo-Json -Depth 8
