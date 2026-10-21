# Correct only the failed structural request's output floor and fresh targets.
# Stages the request; never launches it. Preserve all attempt01 inputs/outputs.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ((Digest $path) -cne $expected) { throw ('PIN_CHANGED: '+$path) }
}
$parent = Join-Path $projectRoot 'product-local/v5-distribution-discovery-01'
$install = Join-Path $parent 'Mathematical Commons v5'
$releaseSha = '769506990ea10be5c6ce812e5cfd457922f4955ad4831bcdbc9d7a9ec9561108'
Require-Digest (Join-Path $install 'V5-RELEASE.json') $releaseSha
Require-Digest (Join-Path $install 'distribution.py') '6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6'
$basisPath = Join-Path $parent 'integration-inputs/installed-discovery-boundary-01-request.json'
Require-Digest $basisPath '9f991f1be08f59489e31736e222c4084f9e5c740db7f029429d8e35771284228'
$request = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
Require-Digest (Join-Path $request.owner.root 'installed.py') '58b3c2b128f38db54e30417cdf219ab89107d50f57abb5116093470b57f8f1ac'
$data = Join-Path $parent 'integration-inputs-02'
$request.name = 'installed-discovery-boundary-02'
$request.parameters.workspace_path = Join-Path $parent 'integration-commons-02'
$request.output_limits.bytes = 67108864
$run = Join-Path $request.workspace_root $request.name
$staged = Join-Path $request.workspace_root ($request.name+'-request')
foreach ($path in @($data, $run, $staged, $request.parameters.workspace_path)) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
[void][IO.Directory]::CreateDirectory($data)
$requestPath = Join-Path $data ($request.name+'-request.json')
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($request | ConvertTo-Json -Depth 64)+"`n")
if ($raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
$stream = [IO.File]::Open($requestPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
$requestSha = Digest $requestPath
[ordered]@{
    request=$requestPath; request_sha256=$requestSha; release_sha256=$releaseSha
    runtime_invoked=$false; mathematical_work_selected=$false
    argv=@((Join-Path $install 'base\receiver\runtime\python\python.exe'), '-I','-S','-B',
        (Join-Path $install 'distribution.py'), 'launch', $releaseSha, 'run', $requestPath, $requestSha)
} | ConvertTo-Json -Depth 8
