$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$proposalPath = Join-Path $projectRoot 'software\v5\modules\native\proof_validation\integration\BUILD-PROPOSAL.json'
if ((Get-FileHash -LiteralPath $proposalPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'da8129fadd3913cf9d36fd196b259b157662065443773a78fcfea9b20346ed6e') { throw 'REVIEWED_PROPOSAL_PIN' }
$selection = Get-Content -LiteralPath $proposalPath -Raw | ConvertFrom-Json
if ($selection.authorizes_compile_only -ne $false -or $selection.name -cne 'proof-validation-integration-build-01' -or $selection.sources.psobject.Properties.Count -eq 0) { throw 'INERT_PROPOSAL_REQUIRED' }
$sourceCount = 0
foreach ($row in $selection.sources.psobject.Properties) {
    $path = Join-Path $projectRoot $row.Name
    if ((Get-Item -LiteralPath $path).Length -ne $row.Value.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $row.Value.sha256) { throw ('SOURCE_PIN:'+ $row.Name) }
    $sourceCount++
}
if ($sourceCount -ne 33) { throw 'EXACT_33_SOURCES' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$path = Join-Path $local ($selection.name+'-selection.json')
foreach ($candidate in @($path,(Join-Path $local $selection.name),(Join-Path $local ($selection.name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $candidate) { throw ('NOT_FRESH:'+ $candidate) }
}
$selection.authorizes_compile_only = $true
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$path;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant();sources=$sourceCount;compiler_calls=4;executed=$false} | ConvertTo-Json
