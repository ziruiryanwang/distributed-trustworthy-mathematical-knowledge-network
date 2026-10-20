# Stage exactly one public installed owner action. Never executes it.
param(
    [Parameter(Mandatory=$true)][ValidateSet('adopt','startup','withdraw')][string]$Action,
    [Parameter(Mandatory=$true)][string]$ReviewedReleaseSha,
    [Parameter(Mandatory=$true)][string]$ReviewedInputSha,
    [Parameter(Mandatory=$true)][string]$ReviewedAdapterSha,
    [string]$ReviewedPreviousResultSha = ''
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
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$inputPath = Join-Path $projectRoot 'experiments/v5-local-checks/distribution-coherent-01-input.json'
Require-Digest $inputPath $ReviewedInputSha
$inputMap = Get-Content -LiteralPath $inputPath -Raw | ConvertFrom-Json
$parent = Join-Path $projectRoot 'product-local/v5-distribution-coherent-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $ReviewedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 109 -or
    @($inputMap.sdk_sources.psobject.Properties).Count -ne 109) { throw 'RELEASE_PROFILE' }
foreach ($property in $inputMap.sdk_sources.psobject.Properties) {
    $target = $release.sdk_sources.($property.Name)
    $row = $release.files.$target
    if ($null -eq $row -or $row.bytes -ne $property.Value.bytes -or
        $row.sha256 -cne $property.Value.sha256) { throw ('SELECTED_SDK_CHANGED: '+$property.Name) }
}
Require-Digest (Join-Path $install 'distribution.py') $release.files.'distribution.py'.sha256
$adapter = Join-Path $projectRoot 'software/v5/distribution_coherent/integration_actual.py'
Require-Digest $adapter $ReviewedAdapterSha
if ((Get-Item -LiteralPath $adapter).Length -gt 131072) { throw 'ADAPTER_BOUND' }
$adapterBytes = [IO.File]::ReadAllBytes($adapter)
$data = Join-Path $parent ('integration-inputs-'+$Action)
$operations = Join-Path $parent 'integration-operations'
$workspace = Join-Path $parent 'integration-commons'
$domain = Join-Path $parent 'integration-trust'
$domainId = 'df43a6bcc5a28ba69ee34c5fabd9919aac3b657c80e807d58f30f489147ba9f0'
$name = 'installed-coherent-'+$Action+'-01'
foreach ($path in @($data, (Join-Path $operations $name), (Join-Path $operations ($name+'-request')))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
$parameters = [ordered]@{schema='DMKN_V5_DISTRIBUTION_COHERENT_INTEGRATION_V1'; action=$Action}
if ($Action -ceq 'adopt') {
    foreach ($path in @($operations, $domain, $workspace)) {
        if (Test-Path -LiteralPath $path) { throw ('FRESH_ADOPTION_REQUIRED: '+$path) }
    }
    $parameters.runtime_adoption = @{'$installed'='runtime_adoption'}
    $parameters.domain_path = $domain
    $parameters.domain_id = $domainId
} else {
    $previousAction = if ($Action -ceq 'startup') { 'adopt' } else { 'startup' }
    $previousName = 'installed-coherent-'+$previousAction+'-01'
    $previousPath = Join-Path $operations ($previousName+'/work/coherent-integration-result.json')
    Require-Digest $previousPath $ReviewedPreviousResultSha
    $previous = Get-Content -LiteralPath $previousPath -Raw | ConvertFrom-Json
    if ($previous.status -cne 'COMPLETED' -or $previous.action -cne $previousAction -or
        $previous.schema -cne 'DMKN_V5_DISTRIBUTION_COHERENT_INTEGRATION_RESULT_V1' -or
        @($previous.cleanup_errors).Count -ne 0) { throw 'PREVIOUS_RESULT_NOT_ADOPTED' }
    $closure = Get-Content -LiteralPath (Join-Path $operations ($previousName+'/RESULT.json')) -Raw | ConvertFrom-Json
    if ($closure.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
        -not $closure.result.job_closed -or -not $closure.result.direct_child_reaped -or
        $closure.result.final_job.active_processes -ne 0) { throw 'PREVIOUS_NOT_CLOSED' }
    $adoptPath = Join-Path $operations 'installed-coherent-adopt-01/work/coherent-integration-result.json'
    $adopt = Get-Content -LiteralPath $adoptPath -Raw | ConvertFrom-Json
    $trust = $adopt.trust_domain
    if ($adopt.status -cne 'COMPLETED' -or $trust.directory -cne $domain -or
        $trust.domain_id -cne $domainId -or $trust.support_id -cnotmatch '^[0-9a-f]{64}$') { throw 'ADOPTED_TRUST_BINDING' }
    if ($Action -ceq 'withdraw' -and
        ($previous.identity.domain_id -cne $trust.domain_id -or
         $previous.identity.support_id -cne $trust.support_id)) { throw 'STARTUP_TRUST_CHANGED' }
    $parameters.trust_domain = $trust
    if ($Action -ceq 'startup') {
        if (Test-Path -LiteralPath $workspace) { throw 'FRESH_WORKSPACE_REQUIRED' }
        $parameters.runtime_adoption = @{'$installed'='runtime_adoption'}
        $parameters.foundation = @{'$installed'='foundation'}
        $parameters.workspace_path = $workspace
        $configuration = $basis.parameters.workspace_config
        $configuration.schema = 'DMKN_V5_CLIENT_EVIDENCE_CONJUNCTION_WORKSPACE_V1'
        # Canonical compact ordering: declaration-kind precedes object-kind.
        # These are only compilation predicates, not claimed useful mathematics.
        $specs = @([ordered]@{tag='declaration-kind'; value='theorem'},
                   [ordered]@{tag='object-kind'; value='module-export-v1'})
        $profile = [ordered]@{schema='DMKN_MODULE_EXPORT_PAIR_PROFILE_V1'; pairs=,$specs}
        $configuration | Add-Member -NotePropertyName discovery_profile -NotePropertyValue $profile
        $parameters.workspace_config = $configuration
        $parameters.operation_limits = $basis.parameters.operation_limits
        $parameters.query_specs = $specs
        $expected = [ordered]@{}
        foreach ($key in @('admission/trust.py','admission/verifier.py',
            'aggregate_claims/aggregate_admission.py','client/runtime.py','client/remote_reader.py',
            'discovery/formal_features.py','discovery/authenticated_index.py','discovery/discovery_store.py',
            'discovery/module_export_adapter.py','client/workspace_evidence.py','client/workspace_atomic.py',
            'client/direct_contacts.py','mixed_claims/interface_projection.py')) {
            $expected[$key] = $inputMap.sdk_sources.('v5/'+$key).sha256
        }
        $parameters.expected_sources = $expected
    }
}
[void][IO.Directory]::CreateDirectory($data)
if ($Action -ceq 'adopt') { [void][IO.Directory]::CreateDirectory($operations) }
New-Bytes (Join-Path $data 'integration_actual.py') $adapterBytes
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$operations
    parameters=$parameters; limits=$basis.limits; output_limits=$basis.output_limits
    owner=[ordered]@{root=$data; entry='integration_actual.py'; sources=[ordered]@{
        'integration_actual.py'=[ordered]@{bytes=$adapterBytes.Length; sha256=$ReviewedAdapterSha}}}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath; request_sha256=$requestSha; release_sha256=$ReviewedReleaseSha;
    runtime_invoked=$false; action=$Action; argv=@(
        (Join-Path $install 'base\receiver\runtime\python\python.exe'), '-I','-S','-B',
        (Join-Path $install 'distribution.py'),'launch',$ReviewedReleaseSha,'run',$requestPath,$requestSha)} | ConvertTo-Json -Depth 8
