# Stage a single installed public method check; no Lean/native/prover invocation.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedAdapterSha,
    [Parameter(Mandatory=$true)][string]$ReviewedLeanSha
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected, [long]$maximum=8388608) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or $item.Length -le 0 -or $item.Length -gt $maximum -or
        $expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function Pin([string]$relative, [string]$expected, [long]$bytes) {
    $path = Join-Path $projectRoot $relative
    Require-Digest $path $expected $bytes
    if ((Get-Item -LiteralPath $path).Length -ne $bytes) { throw 'EXACT_PIN_SIZE' }
    return [ordered]@{path=$path; bytes=$bytes; sha256=$expected}
}
function New-Bytes([string]$path, [byte[]]$raw) {
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
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
$releaseSha = 'c249d086928e62a00ec194f1b556c6cffa918c1106159102e32a8617c9fbadf0'
$releasePath = Join-Path $install 'V5-RELEASE.json'
Require-Digest $releasePath $releaseSha
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 108) { throw 'RELEASE_PROFILE' }
Require-Digest (Join-Path $install 'distribution.py') $release.files.'distribution.py'.sha256
$receipt = Pin 'experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin' '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47' 223594
$bundle = Pin 'experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json' '09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926' 53769
$reference = Pin 'experiments/v5-local-checks/receipt-source-integration-01/evidence/preparation/snapshot/child-input.json' '88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1' 113220
$adapter = Join-Path $projectRoot 'software\v5\evaluator_method\actual.py'
$lean = Join-Path $projectRoot 'software\v5\workloads\EvaluatorUniqueness.lean'
Require-Digest $adapter $ReviewedAdapterSha 131072
Require-Digest $lean $ReviewedLeanSha 32768
$adapterRaw = [IO.File]::ReadAllBytes($adapter)
$leanRaw = [IO.File]::ReadAllBytes($lean)
$name = 'installed-evaluator-method-01'
$data = Join-Path $parent 'evaluator-inputs'
$operations = Join-Path $parent 'evaluator-operations'
$workspace = Join-Path $parent 'evaluator-commons'
foreach ($path in @($data, $operations, $workspace)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
# One I admission (10 CPU), then one packet with the I claim and one native
# witness (10+10 CPU); author gets45, total worker reservation75. No cache
# hit is presumed. Existing settings are fresh caller policy, not old state.
$config = $basis.parameters.workspace_config
$config.packet_envelope.deltas = 1
$config.packet_envelope.edges = 1
$limits = [ordered]@{
    wall_seconds=180; controller_cpu_seconds=60; calls=32; input_bytes=16777216
    worker_cpu_seconds=75; output_bytes=134217728; output_entries=1024
    acquisition=[ordered]@{requests=1; reply_bytes=1048576; verify_attempts=2
        verification_input_bytes=16777216; worker_cpu_seconds=30}
    imports=[ordered]@{max_sources=1; max_members=1; max_receipts=1; max_calls=4096
        submitted_bytes=8388608; data_bytes=4194304}
}
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
New-Bytes (Join-Path $data 'actual.py') $adapterRaw
New-Bytes (Join-Path $data 'EvaluatorUniqueness.lean') $leanRaw
Require-Digest (Join-Path $data 'actual.py') $ReviewedAdapterSha
Require-Digest (Join-Path $data 'EvaluatorUniqueness.lean') $ReviewedLeanSha
$request = [ordered]@{
    schema='DMKN_V5_INSTALLED_REQUEST_V1'; name=$name; workspace_root=$operations
    parameters=[ordered]@{
        schema='DMKN_V5_EVALUATOR_METHOD_ACTUAL_V1'
        runtime_adoption=@{'$installed'='runtime_adoption'}
        foundation=@{'$installed'='foundation'}
        workspace_path=$workspace; workspace_config=$config; operation_limits=$limits
        receipt=$receipt; bundle=$bundle; reference_witness=$reference
        source=[ordered]@{path=(Join-Path $data 'EvaluatorUniqueness.lean'); bytes=$leanRaw.Length; sha256=$ReviewedLeanSha}
        receipt_limits=[ordered]@{cpu_seconds=10; wall_seconds=60; memory_mib=512}
        author_limits=[ordered]@{cpu_seconds=45; wall_seconds=90; memory_mib=768}
        admission_limits=[ordered]@{native_cpu_seconds=10; receipt_cpu_seconds=10; wall_seconds=60; memory_mib=512}
    }
    limits=[ordered]@{cpu_seconds=180; wall_seconds=240; memory_mib=1024
        active_processes=4; stdout_bytes=1048576; stderr_bytes=1048576}
    output_limits=$basis.output_limits
    owner=[ordered]@{root=$data; entry='actual.py'; sources=[ordered]@{
        'actual.py'=[ordered]@{bytes=$adapterRaw.Length; sha256=$ReviewedAdapterSha}
    }}
    runtime_mode='aggregate'
}
$requestPath = Join-Path $data ($name+'-request.json')
New-Bytes $requestPath ([Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n"))
$requestSha = Digest $requestPath
[ordered]@{request=$requestPath; request_sha256=$requestSha; release_sha256=$releaseSha
    runtime_invoked=$false; proof_calls=0; reservation_cpu=[ordered]@{receipt=10; packet=20; author=45}
    argv=@((Join-Path $install 'base\receiver\runtime\python\python.exe'), '-I', '-S', '-B'
        (Join-Path $install 'distribution.py'), 'launch', $releaseSha, 'run', $requestPath, $requestSha)
} | ConvertTo-Json -Depth 8
