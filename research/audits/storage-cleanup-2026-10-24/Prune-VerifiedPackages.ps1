# Exact two-package cleanup after the observed completed comparisons.
# Read INTERRUPTED-VERIFICATION.md. No Lean/runtime tree is a target here.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$auditRoot = Join-Path $projectRoot 'research\audits\storage-cleanup-2026-10-24'
$cutoff = [DateTime]::Parse('2026-10-25T04:09:00Z').ToUniversalTime()
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_CWD_REQUIRED' }
function Assert-Path([string]$Path) {
    if ([IO.Path]::GetFullPath($Path) -cne $Path -or -not $Path.StartsWith($projectRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'PATH_SCOPE' }
    $item = Get-Item -Force -LiteralPath $Path
    while ($true) {
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'REPARSE' }
        if ($item.FullName -ieq $projectRoot) { return }
        $item = Get-Item -Force -LiteralPath ([IO.Path]::GetDirectoryName($item.FullName))
    }
}
function Save-New([string]$Name,[object]$Data) {
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $Data -Depth 8)+"`n")
    $stream = [IO.File]::Open((Join-Path $auditRoot $Name),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
Assert-Path $auditRoot
$plans = @(
    @{version='v3'; folder='certified-v3-package-01'; bytes=[long]2444576373; base='e985b03c2abef3d9a74a6b6ef3d36a690046824c27d0c6e09acd7780037428df'; contributor='fba95cb4bfb74c2c9286f91cc6cff27dbf542b407c6dfacc10b7a7f218cea7c4'; base_map='549e28794298509697203041ab90272df0a5843bbbbb1e94abdf9495b6f8ee5d'; contributor_map='d91ce6ce9c17070df60fdfdd9888ebb4268dc2d6663294205777f49bb957fc2d'},
    @{version='v4'; folder='certified-v4-package-01'; bytes=[long]2444835804; base='773edc7f05ce3c6d3f5224801327c276cfbdd6a1b3c4d36f2197a3d49f238399'; contributor='6160546271798a695fd8e823b73fe68426079f1e0a0af40152c5fa84346bf4ed'; base_map='857a49267ed4ad0a70576d16c0e4c80eaf66c2c57390a7a5a1fd334d8cbea5e0'; contributor_map='c7c00b38458519e2c07f0c6acfe7a999e7ce4cbe52e6531b32b641a644d602c3'}
)
$results = [Collections.Generic.List[object]]::new()
foreach ($plan in $plans) {
    $parent = Join-Path $projectRoot ('product-local\'+$plan.folder)
    $target = Join-Path $parent 'app'
    Assert-Path $target
    $maps = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::OrdinalIgnoreCase)
    $backups = [Collections.Generic.List[object]]::new()
    foreach ($component in @('base','contributor')) {
        $archivePath = Join-Path $parent ('mathematical-commons-'+$plan.version+'-'+$component+'.zip')
        $mapPath = Join-Path $parent ($component.ToUpperInvariant()+'-FILES.json')
        Assert-Path $archivePath; Assert-Path $mapPath
        $archiveHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archivePath).Hash.ToLowerInvariant()
        if ($archiveHash -cne $plan[$component]) { throw 'RECOVERY_ARCHIVE_PIN' }
        $mapHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $mapPath).Hash.ToLowerInvariant()
        if ($mapHash -cne $plan[$component+'_map']) { throw 'RECOVERY_MANIFEST_PIN' }
        $map = Get-Content -Raw -Encoding UTF8 -LiteralPath $mapPath | ConvertFrom-Json
        $members = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::OrdinalIgnoreCase)
        foreach ($prop in $map.files.PSObject.Properties) { $members.Add($prop.Name,$prop.Value); $maps.Add($prop.Name,$prop.Value) }
        $zip = [IO.Compression.ZipFile]::OpenRead($archivePath)
        try {
            $count = 0
            foreach ($entry in $zip.Entries) {
                if ($entry.FullName.EndsWith('/')) { continue }
                if (-not $members.ContainsKey($entry.FullName) -or $entry.Length -ne $members[$entry.FullName].bytes) { throw 'MANIFEST_ARCHIVE_CENSUS' }
                $count++
            }
            if ($count -ne $members.Count) { throw 'MANIFEST_ARCHIVE_COUNT' }
        } finally { $zip.Dispose() }
        $backups.Add(@{archive=$archivePath;sha256=$archiveHash;manifest=$mapPath;manifest_sha256=$mapHash})
    }
    $stack = [Collections.Generic.Stack[string]]::new(); $stack.Push($target)
    $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    $directoryPaths = [Collections.Generic.List[string]]::new()
    $bytes = [long]0
    while ($stack.Count -gt 0) {
        $dir = [IO.DirectoryInfo]::new($stack.Pop())
        if (($dir.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or $dir.LastWriteTimeUtc -ge $cutoff) { throw 'DIRECTORY_CHANGED_AFTER_VERIFICATION_BEGAN' }
        $directoryPaths.Add($dir.FullName.Substring($parent.Length+1))
        foreach ($item in $dir.EnumerateFileSystemInfos()) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'REPARSE_ENTRY' }
            if (($item.Attributes -band [IO.FileAttributes]::Directory) -ne 0) { $stack.Push($item.FullName); continue }
            $key = $item.FullName.Substring($parent.Length+1).Replace('\','/')
            if (-not $seen.Add($key) -or -not $maps.ContainsKey($key) -or $item.Length -ne $maps[$key].bytes -or $item.LastWriteTimeUtc -ge $cutoff) { throw ('EXTRA_OR_CHANGED_FILE:'+ $key) }
            $bytes += $item.Length
        }
    }
    if ($seen.Count -ne 13004 -or $seen.Count -ne $maps.Count -or $bytes -ne $plan.bytes) { throw 'COMPLETE_CENSUS_REQUIRED' }
    $running = @(Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($target+'\',[StringComparison]::OrdinalIgnoreCase) })
    if ($running.Count) { throw 'TARGET_EXECUTABLE_RUNNING' }
    Save-New ($plan.version+'-PRUNE-INTENT.json') @{target=$target;files=$seen.Count;bytes=$bytes;directories=$directoryPaths.ToArray();archives=$backups.ToArray();unchanged_since_utc=$cutoff.ToString('o');basis='OBSERVED_COMPLETE_SHA_COMPARISON_PLUS_HELD_WRITERS_AND_UNCHANGED_METADATA';utc=[DateTime]::UtcNow.ToString('o')}
    # Target is the explicit app child above, not its package parent or root.
    Remove-Item -LiteralPath $target -Recurse -Force
    if (Test-Path -LiteralPath $target) { throw 'TARGET_STILL_PRESENT' }
    foreach ($backup in $backups) { if (-not (Test-Path -LiteralPath $backup.archive -PathType Leaf) -or -not (Test-Path -LiteralPath $backup.manifest -PathType Leaf)) { throw 'BACKUP_MISSING' } }
    $result = @{target=$target;files=$seen.Count;bytes=$bytes;status='REMOVED_RECOVERABLE_FROM_RETAINED_ZIPS';utc=[DateTime]::UtcNow.ToString('o')}
    Save-New ($plan.version+'-PRUNE-RESULT.json') $result
    $results.Add($result)
    Write-Output ($result | ConvertTo-Json -Compress)
}
Save-New 'PRUNE-RESULT.json' @{results=$results.ToArray();status='TWO_VERIFIED_PACKAGES_REMOVED_LEAN_COPY_RETAINED';utc=[DateTime]::UtcNow.ToString('o')}
