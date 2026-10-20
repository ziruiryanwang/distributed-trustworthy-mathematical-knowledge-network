# Prepare one installed public service check. Does not launch or copy runtimes.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedReleaseSha,
    [Parameter(Mandatory=$true)][string]$ExpectedAdapterSha
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
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$installation = Join-Path $projectRoot 'product-local\v5-distribution-connected-01\Mathematical Commons v5'
$releasePath = Join-Path $installation 'V5-RELEASE.json'
Require-Digest $releasePath $ExpectedReleaseSha
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne '557269158f76933177eae962cb97c2862a8512709dbee9842051649552573309') {
    throw 'EXACT_CONNECTED_RELEASE'
}
$basisPath = Join-Path $checks 'advertised-service-controls-01-selection.json'
Require-Digest $basisPath 'e450cbe5590f28e5b857d50eb3c48fa71488f1b1742070e59f7f62946010c3fc'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$adapterKey = 'software/v5/distribution_connected/installed_service_check03.py'
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
}
$sources[$adapterKey] = $ExpectedAdapterSha
foreach ($key in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $key) $sources[$key]
}
$runtime = [ordered]@{}
$baseRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4'
$installedPython = Join-Path $installation 'base\receiver\runtime\python\python.exe'
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
    # The enclosing runner retains its original runtime. The selected child
    # uses the byte-identical installed Python and its own pinned dependencies.
    if ($property.Name.StartsWith($baseRoot+'\receiver\runtime\python\', [StringComparison]::Ordinal)) {
        $relative = 'base/'+$property.Name.Substring($baseRoot.Length+1).Replace('\','/')
        $installedFile = Join-Path $installation $relative
        $row = $release.files.psobject.Properties[$relative].Value
        if ($null -eq $row -or $row.sha256 -cne $property.Value -or
            (Get-Item -LiteralPath $installedFile).Length -ne $row.bytes) {
            throw 'INSTALLED_RUNTIME_MAP'
        }
        Require-Digest $installedFile $property.Value
        $runtime[$installedFile] = $property.Value
    }
}
if (-not $runtime.Contains($installedPython)) { throw 'INSTALLED_PYTHON_PIN_REQUIRED' }
$runtime[$releasePath] = $ExpectedReleaseSha
$entryPath = Join-Path $installation 'distribution.py'
$entrySha = '8e34df2a98fc3bf017f3d57ea2f92211bbcf156ee801479cbfaf9261f76763a6'
Require-Digest $entryPath $entrySha
$runtime[$entryPath] = $entrySha
$name = 'installed-connected-service-03'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($installedPython, '-I', '-S', '-B',
        '{snapshot}\software\v5\distribution_connected\installed_service_check03.py',
        '--installation', $installation, '--release-sha', $ExpectedReleaseSha,
        '--output', '{output}\evidence')
    limits=[ordered]@{
        cpu_seconds=120; wall_seconds=600; memory_mib=512; active_processes=6
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath; sha256=(Digest $selectionPath)
    sources=$sources.Count; runtime_pins=$runtime.Count; executed=$false} | ConvertTo-Json
