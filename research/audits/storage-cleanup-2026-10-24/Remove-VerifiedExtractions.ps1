# Owner-selected removal of exactly three archive-verified historical copies.
# Preserves all recovery ZIPs, evidence, manifests and current software.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$VerificationSha256)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$auditRoot = Join-Path $projectRoot 'research\audits\storage-cleanup-2026-10-24'
$reportPath = Join-Path $auditRoot 'ARCHIVE-VERIFICATION.json'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_CWD_REQUIRED' }
$allowed = @(
    (Join-Path $projectRoot 'product-local\certified-v3-package-01\app'),
    (Join-Path $projectRoot 'product-local\certified-v4-package-01\app'),
    (Join-Path $projectRoot 'experiments\lean-feasibility\runtime\lean-4.34.0-windows')
)
function Assert-Path([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    if ($full -cne $Path -or -not $full.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'UNEXPECTED_PATH' }
    $entry = Get-Item -Force -LiteralPath $full
    while ($entry.FullName -ine $projectRoot) {
        if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw ('REPARSE:' + $entry.FullName) }
        $entry = Get-Item -Force -LiteralPath ([IO.Path]::GetDirectoryName($entry.FullName))
    }
    if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'PROJECT_REPARSE' }
}
function Save-New([string]$Path, [object]$Value) {
    $encoded = [Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $Value -Depth 8) + "`n")
    $stream = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($encoded,0,$encoded.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
Assert-Path $auditRoot
Assert-Path $reportPath
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $reportPath).Hash.ToLowerInvariant() -cne $VerificationSha256) { throw 'VERIFICATION_PIN' }
$verification = Get-Content -Raw -Encoding UTF8 -LiteralPath $reportPath | ConvertFrom-Json
if ($verification.schema -cne 'DMKN_ARCHIVED_EXTRACTION_VERIFICATION_V1' -or $verification.root -cne $projectRoot -or $verification.candidates.Count -ne 3) { throw 'REPORT_SCOPE' }
$processed = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$records = [Collections.Generic.List[object]]::new()
foreach ($candidate in $verification.candidates) {
    $target = [string]$candidate.target
    if (-not ($allowed -ccontains $target) -or -not $processed.Add($target) -or $candidate.status -cne 'EXACT_ARCHIVE_PAYLOAD_MATCH') { throw 'TARGET_ALLOWLIST' }
    Assert-Path $target
    $parent = [IO.Path]::GetDirectoryName($target)
    foreach ($archive in $candidate.archives) {
        Assert-Path $archive.path
        if ([IO.Path]::GetDirectoryName($archive.path) -cne $parent -or [IO.Path]::GetExtension($archive.path) -cne '.zip') { throw 'ARCHIVE_LOCATION' }
        $item = Get-Item -Force -LiteralPath $archive.path
        if ($item.Length -ne $archive.bytes -or (Get-FileHash -Algorithm SHA256 -LiteralPath $archive.path).Hash.ToLowerInvariant() -cne $archive.sha256) { throw 'RECOVERY_ARCHIVE_CHANGED' }
    }
    $fileMap = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($file in $candidate.files) { $fileMap.Add($file.path, $file) }
    $dirMap = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($dir in $candidate.directories) { $dirMap.Add($dir.path, $dir) }
    $stack = [Collections.Generic.Stack[string]]::new()
    $stack.Push($target)
    $count = 0
    $dirCount = 0
    $bytes = [long]0
    while ($stack.Count -gt 0) {
        $dir = $stack.Pop()
        $dirCount++
        $dirKey = $dir.Substring($parent.Length+1).Replace('\','/')
        if (-not $dirMap.ContainsKey($dirKey)) { throw 'NEW_DIRECTORY' }
        $dirInfo = [IO.DirectoryInfo]::new($dir)
        if (($dirInfo.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or $dirInfo.LastWriteTimeUtc.ToString('o') -cne $dirMap[$dirKey].last_write_utc) { throw 'CHANGED_DIRECTORY' }
        foreach ($item in $dirInfo.EnumerateFileSystemInfos()) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw ('REPARSE:' + $item.FullName) }
            if (($item.Attributes -band [IO.FileAttributes]::Directory) -ne 0) { $stack.Push($item.FullName); continue }
            $key = $item.FullName.Substring($parent.Length+1).Replace('\','/')
            if (-not $fileMap.ContainsKey($key)) { throw ('NEW_FILE:' + $key) }
            $expected = $fileMap[$key]
            if ($item.Length -ne $expected.bytes -or $item.LastWriteTimeUtc.ToString('o') -cne $expected.last_write_utc -or [int]$item.Attributes -ne $expected.attributes) { throw ('CHANGED_FILE:' + $key) }
            $count++; $bytes += $item.Length
        }
    }
    if ($count -ne $candidate.file_count -or $count -ne $fileMap.Count -or $dirCount -ne $dirMap.Count -or $bytes -ne $candidate.bytes) { throw 'CENSUS_CHANGED' }
    $running = @(Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($target + '\',[StringComparison]::OrdinalIgnoreCase) })
    if ($running.Count -ne 0) { throw 'TARGET_EXECUTABLE_RUNNING' }
    $number = $processed.Count
    $intent = @{target=$target; files=$count; bytes=$bytes; directories=$dirCount; verification_sha256=$VerificationSha256; archives=$candidate.archives; utc=[DateTime]::UtcNow.ToString('o'); status='VALIDATED_REMOVAL_INTENT'}
    Save-New (Join-Path $auditRoot ('REMOVE-' + $number + '-INTENT.json')) $intent
    # Only this explicit, validated strict descendant is removed. All contained
    # entries have just been checked, and research writers are held throughout.
    Remove-Item -LiteralPath $target -Recurse -Force
    if (Test-Path -LiteralPath $target) { throw 'TARGET_STILL_PRESENT' }
    foreach ($archive in $candidate.archives) { if (-not (Test-Path -LiteralPath $archive.path -PathType Leaf)) { throw 'ARCHIVE_MISSING_AFTER_REMOVAL' } }
    $record = @{target=$target; files=$count; bytes=$bytes; utc=[DateTime]::UtcNow.ToString('o'); status='REMOVED_RECOVERABLE_FROM_RETAINED_ZIPS'}
    Save-New (Join-Path $auditRoot ('REMOVE-' + $number + '-RESULT.json')) $record
    $records.Add($record)
    Write-Output ('REMOVED ' + $target + ' files=' + $count + ' logical_bytes=' + $bytes)
}
Save-New (Join-Path $auditRoot 'REMOVAL-RESULT.json') @{schema='DMKN_ARCHIVED_EXTRACTION_REMOVAL_V1'; verification_sha256=$VerificationSha256; results=$records.ToArray(); utc=[DateTime]::UtcNow.ToString('o')}
