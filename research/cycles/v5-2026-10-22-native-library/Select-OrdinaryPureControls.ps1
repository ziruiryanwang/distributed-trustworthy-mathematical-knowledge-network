param(
    [Parameter(Mandatory=$true)][string] $Name,
    [Parameter(Mandatory=$true)][ValidateSet('portable','deferred','translation','combined')][string] $Kind
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
if ($Name -notmatch '^ordinary-[a-z0-9-]+$') { throw 'Selected operation name required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$prior = Get-Content -LiteralPath (Join-Path $local 'ordinary-owner-consumer-04\selection.json') -Raw | ConvertFrom-Json
$pins = [ordered]@{}
foreach ($path in @('D:\Python314\python.exe','D:\Python314\python314.dll','D:\Python314\python3.dll')) {
    $expected = $prior.runtime_pins.$path
    if (-not $expected -or (Hash-File $path) -ne $expected) { throw 'Retained Python pin mismatch' }
    $pins[$path] = $expected
}
if ($Kind -eq 'portable') {
    $entry = 'portable_identity_checks.py'
    $helpers = @('ordinary_evidence.py','ordinary_preview.py','ordinary_semantics.py','portable_evidence.py','portable_preview.py','semantic_identity_checks.py',$entry)
} elseif ($Kind -eq 'translation') {
    $entry = 'legacy_translation_checks.py'
    $helpers = @('ordinary_evidence.py','ordinary_semantics.py','portable_evidence.py','legacy_identity_translation.py',$entry)
} elseif ($Kind -eq 'combined') {
    $entry = 'combined_admission_checks.py'
    $helpers = @('ordinary_evidence.py','run_successor_admission.py',$entry)
} else {
    $entry = 'deferred_import_checks.py'
    $helpers = @('ordinary_evidence.py','run_successor_admission.py',$entry)
}
$sources = [ordered]@{'tools/Run-V5-Check.py'=(Hash-File (Join-Path $projectRoot 'tools/Run-V5-Check.py'))}
foreach ($helper in $helpers) {
    $relative = 'software/v5/ordinary_lean/' + $helper
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$Name;sources=$sources;runtime_pins=$pins
    argv=@('D:\Python314\python.exe','-I','-S','-B',('{snapshot}\software\v5\ordinary_lean\' + $entry))
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=256;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$path = Join-Path $local ($Name + '.selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $local $Name))) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$path;sha256=(Hash-File $path);execution='NOT_STARTED'} | ConvertTo-Json
