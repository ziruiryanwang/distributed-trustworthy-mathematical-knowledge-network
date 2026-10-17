# One selected compile-only operation. No retry; no produced executable call.
$ErrorActionPreference = 'Stop'
$clock = [Diagnostics.Stopwatch]::StartNew()
$self = [Diagnostics.Process]::GetCurrentProcess()
$selfCpu = $self.TotalProcessorTime.TotalSeconds
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'geometry17-snapshot-host-build-02'
$selection = Join-Path $checks ($name+'-selection.json')
$digest = 'f245889a729ff61726347cfad7673af1801a5e8104cd71f6d8c112af185d2b7c'
$builder = Join-Path $projectRoot 'software\v5\aggregate_geometry\build_snapshot.py'
$python = 'D:\Python314\python.exe'
$pins = [ordered]@{
    $selection = $digest
    $builder = '46be079429687e7ada877859111cf5b58d2bab1c6c0c6665146b487f3f8df1c7'
    $python = '03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38'
    'D:\Python314\python314.dll' = 'fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0'
}
foreach ($path in $pins.Keys) {
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pins[$path]) { throw ('LAUNCH_PIN:'+ $path) }
}
$outer = Join-Path $checks ($name+'-launch')
foreach ($path in @($outer,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
$competing = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^(rustc|cargo|lean|python[0-9.]*|(?:small|geometry17|aggregate|dmkn)[_-].*)\.exe$'
})
if ($competing.Count -ne 0) { throw 'HEAVY_PROCESS_OVERLAP_HOLD' }
$sample = Get-Counter '\Memory\Available Bytes','\Memory\Committed Bytes','\Memory\Commit Limit'
function CounterValue([string]$suffix) {
    $values = @($sample.CounterSamples | Where-Object {$_.Path.EndsWith($suffix,[StringComparison]::OrdinalIgnoreCase)})
    if ($values.Count -ne 1 -or $values[0].Status -ne 0) { throw 'MEMORY_COUNTER_MISSING_OR_FAILED' }
    $value = [double]$values[0].CookedValue
    if ([double]::IsNaN($value) -or [double]::IsInfinity($value) -or $value -lt 0 -or $value -gt [long]::MaxValue) {
        throw 'MEMORY_COUNTER_NOT_FINITE_NONNEGATIVE'
    }
    return [long]$value
}
$available = CounterValue '\available bytes'
$committed = CounterValue '\committed bytes'
$commitLimit = CounterValue '\commit limit'
if ($commitLimit -le 0 -or $committed -gt $commitLimit) { throw 'MEMORY_COUNTER_INCONSISTENT' }
$observation = [ordered]@{utc=[DateTime]::UtcNow.ToString('o');available_physical_bytes=$available
    committed_bytes=$committed;commit_limit_bytes=$commitLimit;commit_headroom_bytes=($commitLimit-$committed)
    required_physical_and_commit_bytes=2684354560;reservation=$false}
if ($available -lt 2684354560 -or ($commitLimit-$committed) -lt 2684354560) {
    [ordered]@{status='DEFERRED_NO_PROCESS_STARTED';memory=$observation} | ConvertTo-Json -Depth 4
    exit 2
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 10)+"`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
[void](New-Item -ItemType Directory -Path $outer)
SaveNew (Join-Path $outer 'START.json') ([ordered]@{schema='DMKN_GEOMETRY17_BUILD_LAUNCH_V1'
    selection_sha256=$digest;memory=$observation;outer_wall_seconds=450;controller_cpu_seconds=60
    controller_private_bytes=268435456;log_bytes=1048576;scope='ONE_COMPILE_ONLY_NO_RETRY'})
$child = $null
$errorText = $null
$killed = $false
$peakController = 0L
try {
    $arguments = '-I -S -B "'+$builder+'" "'+$selection+'" '+$digest
    $child = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $projectRoot `
        -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $outer 'stdout.txt') `
        -RedirectStandardError (Join-Path $outer 'stderr.txt')
    $null = $child.Handle
    while (-not $child.WaitForExit(200)) {
        $child.Refresh()
        $peakController = [Math]::Max($peakController,$child.PrivateMemorySize64)
        if ($clock.Elapsed.TotalSeconds -gt 450 -or $child.TotalProcessorTime.TotalSeconds -gt 60 -or
            $child.PrivateMemorySize64 -gt 268435456) { throw 'OUTER_CONTROLLER_ENVELOPE' }
        foreach ($log in @('stdout.txt','stderr.txt')) {
            if ((Get-Item -LiteralPath (Join-Path $outer $log)).Length -gt 1048576) { throw 'OUTER_LOG_BOUND' }
        }
    }
    $child.WaitForExit()
    if ($clock.Elapsed.TotalSeconds -gt 450 -or $child.TotalProcessorTime.TotalSeconds -gt 60) {
        throw 'FINAL_OUTER_CONTROLLER_ENVELOPE'
    }
    foreach ($log in @('stdout.txt','stderr.txt')) {
        if ((Get-Item -LiteralPath (Join-Path $outer $log)).Length -gt 1048576) { throw 'FINAL_OUTER_LOG_BOUND' }
    }
    if ($child.ExitCode -ne 0) { throw ('BUILD_EXIT:'+ $child.ExitCode) }
} catch { $errorText = $_.Exception.Message }
finally {
    if ($null -ne $child -and -not $child.HasExited) {
        $child.Kill(); $killed = $true
        if (-not $child.WaitForExit(10000)) { $errorText = 'OWNED_CONTROLLER_NOT_REAPED' }
    }
    $self.Refresh()
    $cpu = if ($null -ne $child -and $child.HasExited) {$child.TotalProcessorTime.TotalSeconds} else {$null}
    $code = if ($null -ne $child -and $child.HasExited) {$child.ExitCode} else {$null}
    $report = [ordered]@{schema='DMKN_GEOMETRY17_BUILD_LAUNCH_RESULT_V1';selection_sha256=$digest
        status=$(if ($null -eq $errorText) {'BUILD_PROCESS_EXITED_ZERO'} else {'FAIL'})
        process_id=$(if ($null -ne $child) {$child.Id} else {$null});exit_code=$code
        direct_child_reaped=($null -ne $child -and $child.HasExited);termination_requested=$killed
        child_controller_cpu_seconds_including_start_and_exit=$cpu;sampled_controller_private_peak_bytes=$peakController
        launch_supervisor_cpu_seconds=($self.TotalProcessorTime.TotalSeconds-$selfCpu)
        wall_seconds=$clock.Elapsed.TotalSeconds;error=$errorText
        accounting='COMPILER_JOB_CPU_SEPARATE;POWERSHELL_STARTUP_AND_FINAL_LAUNCH_REPORT_TAIL_EXCLUDED'
        authority='PROCESS_OBSERVATION_NOT_BUILD_ADOPTION_OR_MATHEMATICAL_ADMISSION'}
    SaveNew (Join-Path $outer 'RESULT.json') $report
    $report | ConvertTo-Json -Depth 5
}
if ($null -ne $errorText) { exit 1 }
