param([Parameter(Mandatory=$true)][string] $Name)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
if ($Name -notmatch '^ordinary-[a-z0-9-]+$') { throw 'Selected operation name required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$priorPath = Join-Path $local 'ordinary-construct-helpers-02\selection.json'
if ((Hash-File $priorPath) -ne 'faf57e3d64a1cd0098a0b1aa703a7972f74cc7c910487682b6f32d68596c959e') { throw 'Retained helper selection changed' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$priorResult = Join-Path $local 'ordinary-construct-helpers-02\RESULT.json'
$result = Get-Content -LiteralPath $priorResult -Raw | ConvertFrom-Json
if ($result.result.status -ne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or $result.selection_sha256 -ne (Hash-File $priorPath)) { throw 'Successful retained helper build required' }
$build = Join-Path $local 'ordinary-construct-helpers-02\lean-build'
$pins = [ordered]@{}
foreach ($entry in $prior.runtime_pins.PSObject.Properties) { $pins[$entry.Name] = $entry.Value }
foreach ($file in Get-ChildItem -LiteralPath $build -File) { $pins[$file.FullName] = Hash-File $file.FullName }
$pins[$priorPath] = Hash-File $priorPath
$pins[$priorResult] = Hash-File $priorResult
$sources = [ordered]@{}
$modules = @('OrdinaryExport','SuccessorExport','SuccessorExportCommand','ConstructExportCommand')
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/ordinary_lean/run_selected_compile.py') + @($modules | ForEach-Object { 'software/v5/ordinary_lean/' + $_ + '.lean' })) {
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
$previous = $build + ';' + $prior.argv[6]
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$Name;sources=$sources;runtime_pins=$pins
    argv=@('D:\Python314\python.exe','-I','-S','-B','{snapshot}\software\v5\ordinary_lean\run_selected_compile.py','{output}',$previous) + $modules
    limits=[ordered]@{cpu_seconds=120;wall_seconds=195;memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
if ($pins.Count -gt 256) { throw 'Runtime pin bound' }
$path = Join-Path $local ($Name + '.selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $local $Name))) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$path;sha256=(Hash-File $path);execution='NOT_STARTED'} | ConvertTo-Json
