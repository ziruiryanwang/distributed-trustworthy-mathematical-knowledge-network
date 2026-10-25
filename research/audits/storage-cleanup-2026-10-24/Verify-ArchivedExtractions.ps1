# Read-only verification of explicit historical extraction candidates.
# Creates a NEW audit report only; never removes or changes a candidate.
param([Parameter(Mandatory=$true)][string]$ReportPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$auditRoot = Join-Path $projectRoot 'research\audits\storage-cleanup-2026-10-24'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_CWD_REQUIRED' }
if ([IO.Path]::GetFullPath($ReportPath) -cne (Join-Path $auditRoot 'ARCHIVE-VERIFICATION.json')) { throw 'REPORT_SCOPE' }
if (Test-Path -LiteralPath $ReportPath) { throw 'FRESH_REPORT_REQUIRED' }

function Assert-LocalPath([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    if (-not $full.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'PATH_OUTSIDE_PROJECT' }
    $entry = Get-Item -Force -LiteralPath $full
    while ($null -ne $entry) {
        if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw ('REPARSE:' + $entry.FullName) }
        if ($entry.FullName -ieq $projectRoot) { return $full }
        $entry = Get-Item -Force -LiteralPath ([IO.Path]::GetDirectoryName($entry.FullName))
    }
    throw 'MISSING_PROJECT_ANCESTOR'
}

function Hash-Stream([IO.Stream]$Stream) {
    $hash = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hash.ComputeHash($Stream))).Replace('-', '').ToLowerInvariant() }
    finally { $hash.Dispose() }
}

$null = Assert-LocalPath $auditRoot

function Assert-ZipName([string]$Name) {
    if ($Name.Contains('\') -or $Name.Contains(':') -or $Name.StartsWith('/') -or $Name.IndexOf([char]0) -ge 0) { throw ('UNSAFE_ZIP_ENTRY:' + $Name) }
    $trimmed = $Name.TrimEnd('/')
    foreach ($part in $trimmed.Split('/')) {
        if ($part -eq '' -or $part -eq '.' -or $part -eq '..' -or $part.EndsWith('.') -or $part.EndsWith(' ') -or $part.IndexOfAny([IO.Path]::GetInvalidFileNameChars()) -ge 0 -or $part -match '^(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)') { throw ('UNRECOVERABLE_ZIP_COMPONENT:' + $Name) }
    }
}

$plans = @(
    @{target='product-local\certified-v3-package-01\app'; archives=@('mathematical-commons-v3-base.zip','mathematical-commons-v3-contributor.zip')},
    @{target='product-local\certified-v4-package-01\app'; archives=@('mathematical-commons-v4-base.zip','mathematical-commons-v4-contributor.zip')},
    @{target='experiments\lean-feasibility\runtime\lean-4.34.0-windows'; archives=@('lean-4.34.0-windows.zip')}
)
$results = [Collections.Generic.List[object]]::new()
foreach ($plan in $plans) {
    $target = Assert-LocalPath (Join-Path $projectRoot $plan.target)
    $parent = [IO.Path]::GetDirectoryName($target)
    $prefix = [IO.Path]::GetFileName($target) + '/'
    $local = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::OrdinalIgnoreCase)
    $directories = [Collections.Generic.List[object]]::new()
    $stack = [Collections.Generic.Stack[string]]::new()
    $stack.Push($target)
    while ($stack.Count -gt 0) {
        $dir = $stack.Pop()
        $dirInfo = [IO.DirectoryInfo]::new($dir)
        $directories.Add(@{path=$dir.Substring($parent.Length + 1).Replace('\','/'); last_write_utc=$dirInfo.LastWriteTimeUtc.ToString('o')})
        foreach ($item in $dirInfo.EnumerateFileSystemInfos()) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw ('REPARSE:' + $item.FullName) }
            if (($item.Attributes -band [IO.FileAttributes]::Directory) -ne 0) { $stack.Push($item.FullName); continue }
            $key = $item.FullName.Substring($parent.Length + 1).Replace('\','/')
            if ($local.ContainsKey($key)) { throw 'CASE_ALIAS' }
            $local.Add($key, $item)
        }
    }
    $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    $files = [Collections.Generic.List[object]]::new()
    $archives = [Collections.Generic.List[object]]::new()
    $bytes = [long]0
    foreach ($name in $plan.archives) {
        $archivePath = Assert-LocalPath (Join-Path $parent $name)
        $archiveInfo = Get-Item -Force -LiteralPath $archivePath
        $archiveHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archivePath).Hash.ToLowerInvariant()
        $archives.Add(@{path=$archivePath; bytes=$archiveInfo.Length; sha256=$archiveHash; last_write_utc=$archiveInfo.LastWriteTimeUtc.ToString('o')})
        $zip = [IO.Compression.ZipFile]::OpenRead($archivePath)
        try {
            foreach ($entry in $zip.Entries) {
                $key = $entry.FullName
                Assert-ZipName $key
                if (-not $key.StartsWith($prefix, [StringComparison]::Ordinal)) { throw ('OUTSIDE_TARGET_ZIP_ENTRY:' + $key) }
                if (($entry.ExternalAttributes -band 0xF0000000) -eq 0xA0000000) { throw 'ZIP_SYMLINK' }
                if ($key.EndsWith('/')) { continue }
                if (-not $seen.Add($key)) { throw ('DUPLICATE_ZIP_FILE:' + $key) }
                if (-not $local.ContainsKey($key)) { throw ('ZIP_FILE_MISSING_LOCALLY:' + $key) }
                $file = $local[$key]
                if ($file.Length -ne $entry.Length) { throw ('LENGTH_MISMATCH:' + $key) }
                $auditStream = $entry.Open()
                try { $zipHash = Hash-Stream $auditStream } finally { $auditStream.Dispose() }
                $auditStream = [IO.File]::Open($file.FullName, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
                try {
                    $file.Refresh()
                    $checkedLength = $file.Length
                    $checkedTime = $file.LastWriteTimeUtc.ToString('o')
                    $checkedAttributes = [int]$file.Attributes
                    if ($checkedLength -ne $entry.Length -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'FILE_CHANGED_BEFORE_HASH' }
                    $fileHash = Hash-Stream $auditStream
                    $file.Refresh()
                    if ($file.Length -ne $checkedLength -or $file.LastWriteTimeUtc.ToString('o') -cne $checkedTime -or [int]$file.Attributes -ne $checkedAttributes) { throw 'FILE_CHANGED_DURING_HASH' }
                } finally { $auditStream.Dispose() }
                if ($fileHash -cne $zipHash) { throw ('CONTENT_MISMATCH:' + $key) }
                $file.Refresh()
                if ($file.Length -ne $checkedLength -or $file.LastWriteTimeUtc.ToString('o') -cne $checkedTime -or [int]$file.Attributes -ne $checkedAttributes) { throw 'FILE_CHANGED_AFTER_HASH' }
                $files.Add(@{path=$key; bytes=$entry.Length; sha256=$fileHash; archive=$name; last_write_utc=$checkedTime; attributes=$checkedAttributes})
                $bytes += $entry.Length
            }
        } finally { $zip.Dispose() }
        $archiveInfo.Refresh()
        if ($archiveInfo.Length -ne $archives[$archives.Count-1].bytes -or $archiveInfo.LastWriteTimeUtc.ToString('o') -cne $archives[$archives.Count-1].last_write_utc) { throw 'ARCHIVE_CHANGED' }
    }
    if ($seen.Count -ne $local.Count) { throw ('UNARCHIVED_LOCAL_FILES:' + $target) }
    $results.Add(@{target=$target; status='EXACT_ARCHIVE_PAYLOAD_MATCH'; files=$files.ToArray(); directories=$directories.ToArray(); archives=$archives.ToArray(); file_count=$files.Count; bytes=$bytes})
    Write-Output ('VERIFIED ' + $plan.target + ' files=' + $files.Count + ' bytes=' + $bytes)
}
$report = @{schema='DMKN_ARCHIVED_EXTRACTION_VERIFICATION_V1'; utc=[DateTime]::UtcNow.ToString('o'); authority='FILE_REDUNDANCY_ONLY_NOT_DELETION_AUTHORIZATION'; root=$projectRoot; candidates=$results.ToArray()}
$json = ConvertTo-Json -InputObject $report -Depth 10
$reportStream = [IO.File]::Open($ReportPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $encoded = [Text.UTF8Encoding]::new($false).GetBytes($json + "`n"); $reportStream.Write($encoded,0,$encoded.Length) } finally { $reportStream.Dispose() }
Get-FileHash -Algorithm SHA256 -LiteralPath $ReportPath
