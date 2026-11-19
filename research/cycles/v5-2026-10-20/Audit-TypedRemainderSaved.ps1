# Read-only saved terminal evidence audit. No product imports, runtime or writes.
$ErrorActionPreference='Stop'
$auditRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if((Get-Location).Path -cne $auditRoot){throw 'CANONICAL_WORKDIR'}
$innerPath=Join-Path $auditRoot 'experiments\v5-local-checks\typed-general36-remainder-02'
$outerPath=Join-Path $auditRoot 'experiments\v5-local-checks\typed-general36-remainder-owner-02'
function Need($ok,$why){if(-not $ok){throw $why}}
function Doc($path){Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json}
function Same($a,$b){
    if($null -eq $a -or $null -eq $b){return ($null -eq $a -and $null -eq $b)}
    if($a -is [pscustomobject] -and $b -is [pscustomobject]){
        $an=@($a.PSObject.Properties.Name|Sort-Object);$bn=@($b.PSObject.Properties.Name|Sort-Object)
        if(($an -join '|') -cne ($bn -join '|')){return $false}
        foreach($n in $an){if(-not (Same $a.$n $b.$n)){return $false}};return $true
    }
    if($a -is [array] -or $b -is [array]){
        if(@($a).Count -ne @($b).Count){return $false}
        for($j=0;$j -lt @($a).Count;$j++){if(-not (Same @($a)[$j] @($b)[$j])){return $false}};return $true
    }
    if($a -is [string]){return $a -ceq $b}
    if($a -is [bool]){return $a -eq $b}
    # Exact binary64 equality matches the frozen Python JSON consumer. No tolerance.
    return [double]$a -eq [double]$b
}
function CheckPin($pin){
    $item=Get-Item -LiteralPath $pin.path
    Need ($item.Length -eq $pin.bytes) ('SIZE:'+$pin.path)
    Need ((Get-FileHash -LiteralPath $pin.path -Algorithm SHA256).Hash.ToLowerInvariant() -ceq $pin.sha256) ('HASH:'+$pin.path)
}
function Clean($p){
    Need ($p.status -ceq 'COMMAND_EXITED_ZERO_AND_CLOSED' -and $p.child_exit_code -eq 0 -and
        $p.direct_child_reaped -eq $true -and $p.job_closed -eq $true -and @($p.cleanup_errors).Count -eq 0 -and
        $p.termination_requested -eq $false -and $p.final_job.active_processes -eq 0 -and
        $p.final_job.terminated_processes -eq 0) 'CLOSURE'
    Need ($p.final_job.cpu_seconds -le $p.limits.cpu_seconds -and
        $p.wall_seconds_through_cleanup -le $p.limits.wall_seconds) 'PROCESS_COST'
}
$result=Doc (Join-Path $innerPath 'RESULT.json');$outer=Doc (Join-Path $outerPath 'RESULT.json')
$op=Doc (Join-Path $outerPath 'operator-result.json');$sel=Doc (Join-Path $outerPath 'selection.json')
$req=Doc $op.request_document.path;$prefix=Doc $req.prior_attempts[0].path
CheckPin $op.production_result;CheckPin $op.profile_document;CheckPin $op.request_document
CheckPin $op.entry_source;CheckPin $req.prior_attempts[0]
Need ((Get-FileHash -LiteralPath (Join-Path $outerPath 'selection.json') -Algorithm SHA256).Hash.ToLowerInvariant() -ceq
    'c4057ee011de495a9ed40dd3351867b069cc5355958200092d33861ccc9d2a97') 'SELECTION_HASH'
Clean $outer.result
$expanded=@($sel.argv | ForEach-Object {$_.Replace('{snapshot}',(Join-Path $outerPath 'sources')).Replace('{output}',$outerPath)})
Need (Same $expanded $outer.result.argv) 'OUTER_ARGV';Need (Same $sel.limits $outer.result.limits) 'OUTER_LIMITS'
Need ($outer.result.cwd -ceq $auditRoot) 'OUTER_CWD'
Need (Same (Doc (Join-Path $outerPath 'command\stdout.txt')) $op) 'OUTER_STDOUT'
Need ((Get-Item -LiteralPath (Join-Path $outerPath 'command\stderr.txt')).Length -eq 0) 'OUTER_STDERR'
foreach($key in @('allowance_id','budget','carried_external_costs')){
    Need (Same $req.$key $prefix.$key) ('SAME_LINEAGE:'+$key)
    Need (Same $req.$key $result.$key) ('RESULT_LINEAGE:'+$key)
}
Need (Same $req.checkpoints $prefix.retained_checkpoints) 'PRIOR_CHECKPOINT_INVENTORY'
Need (Same $req.prior_attempts $result.prior_attempts) 'PRIOR_PIN'
Need ($result.profile_id -ceq $prefix.profile_id -and $result.session_id -ceq $prefix.session_id) 'PROFILE_SESSION'
$chargeMap=@{prior_allowance_worker_charge='worker_cpu_charge_this_attempt';prior_allowance_controller_cpu='controller_cpu_seconds';
    prior_allowance_wall='wall_seconds';prior_allowance_output_charge='output_charge_this_attempt';prior_allowance_entry_charge='entry_charge_this_attempt'}
foreach($key in $chargeMap.Keys){Need (Same $result.$key $prefix.($chargeMap[$key])) ('PRIOR_CHARGE:'+$key)}
$inventory=@{};foreach($row in $req.checkpoints){CheckPin $row.file;$inventory[$row.key]=$row.file}
$keys=New-Object System.Collections.Generic.List[string]
for($i=2;$i -lt 36;$i++){$keys.Add("segment:$i");$keys.Add("lift:$i");$keys.Add("join:$i")}
$keys.Add('resolve:0');$keys.Add('finish:0')
Need ($result.stages.Count -eq $keys.Count -and $keys.Count -eq 104) 'STAGE_COUNT'
$cpuSum=0.0;$wallSum=0.0;$proofCount=0;$stageGroups=@{};$stderrNonempty=0
for($i=0;$i -lt $keys.Count;$i++){
    $stagePin=$result.stages[$i];CheckPin $stagePin;$stage=Doc $stagePin.path;$key=$keys[$i]
    Need ($stage.stage -ceq $key -and $stage.status -ceq 'PASS_BOUND_HOST_STAGE') ('STAGE:'+$key)
    $parts=$key.Split(':');$kind=$parts[0];$n=[int]$parts[1];$stageDir=Join-Path $innerPath ($kind+'-'+$n)
    Need ($stagePin.path -ceq (Join-Path $stageDir 'RESULT.json')) 'STAGE_LOCATION'
    Clean $stage.process;CheckPin $stage.reservation;CheckPin $stage.artifact;CheckPin $stage.bound_stdout.dependency_manifest
    $reserve=Doc $stage.reservation.path;$deps=Doc $stage.bound_stdout.dependency_manifest.path
    $cmd=Doc (Join-Path $stageDir 'command\command.json');$stdout=Doc (Join-Path $stageDir 'command\stdout.txt')
    Need (Same $stdout $stage.bound_stdout) ('STDOUT:'+$key)
    Need (Same $cmd.argv $stage.process.argv) 'COMMAND_ARGV';Need (Same $cmd.limits $stage.process.limits) 'COMMAND_LIMITS'
    Need ($cmd.cwd -ceq $stage.process.cwd) 'COMMAND_CWD';Need (Same $reserve.argv $stage.process.argv) 'RESERVATION_ARGV'
    Need (Same $reserve.limits $stage.process.limits) 'RESERVATION_LIMITS'
    Need ($reserve.profile_id -ceq $result.profile_id -and $reserve.allowance_id -ceq $result.allowance_id -and
        $reserve.session_id -ceq $result.session_id -and $reserve.stage -ceq $key) 'RESERVATION_IDENTITIES'
    Need ($stage.worker_cpu_charge -eq $stage.process.final_job.cpu_seconds -and
        $stage.worker_cpu_charge -le $reserve.worker_reserved) 'STAGE_COST'
    $wantDeps=@()
    switch($kind){
        'lift'{$wantDeps=@("segment:$n")}
        'join'{$wantDeps=@(('join:'+($n-1)),"lift:$n")}
        'resolve'{$wantDeps=@('join:35')}
        'finish'{$wantDeps=@(0..35|ForEach-Object{"segment:$_"})+@('resolve:0')}
    }
    Need (Same @($reserve.dependency_keys) @($wantDeps)) ('DEPENDENCY_KEYS:'+$key)
    Need (Same @($stdout.dependency_keys) @($wantDeps)) 'STDOUT_DEPENDENCIES'
    Need ($deps.stage -ceq $key -and $deps.session_binding -ceq $req.session.session_binding -and
        $deps.capsule_binding -ceq $req.session.capsule_binding) 'DEPENDENCY_BINDING'
    Need (@($deps.dependencies).Count -eq $wantDeps.Count) 'DEPENDENCY_COUNT'
    for($d=0;$d -lt $wantDeps.Count;$d++){
        Need ($deps.dependencies[$d].key -ceq $wantDeps[$d] -and
            (Same $deps.dependencies[$d].file $inventory[$wantDeps[$d]])) ('DEPENDENCY_PIN:'+$key)
    }
    Need ($stdout.aggregate_image -ceq '9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865' -and
        $stdout.header_sha256 -ceq $req.session.expected.sha256 -and $stdout.session_binding -ceq $req.session.session_binding -and
        $stdout.capsule_binding -ceq $req.session.capsule_binding -and $stdout.segments -eq 36 -and $stdout.assumptions -eq 1 -and
        $stdout.output_bytes -eq $stage.artifact.bytes -and $stdout.output_sha256 -ceq $stage.artifact.sha256 -and
        $stdout.mathematical_admission -eq $false -and $stdout.guest_execute_calls -eq 0) 'STDOUT_IDENTITIES'
    Need ($stdout.application_receipt_created -eq ($kind -ceq 'finish') -and
        $stdout.proof_stage_calls -eq [int]($kind -cne 'finish')) 'PROOF_KIND'
    if($kind -cne 'finish'){
        $raw=[IO.File]::ReadAllBytes($stage.artifact.path)
        Need ([Text.Encoding]::ASCII.GetString($raw,0,8) -ceq 'DMKNAP01' -and [BitConverter]::ToUInt32($raw,8) -eq 1) 'CHECKPOINT_MAGIC'
        $binding=([BitConverter]::ToString($raw,12,32)).Replace('-','').ToLowerInvariant()
        $ln=[int][BitConverter]::ToUInt64($raw,44);Need ($ln -ge 1 -and $ln -le 7) 'CHECKPOINT_KIND_LENGTH'
        Need ($binding -ceq $req.session.capsule_binding -and [Text.Encoding]::ASCII.GetString($raw,52,$ln) -ceq $kind -and
            [BitConverter]::ToUInt32($raw,52+$ln) -eq $n -and [BitConverter]::ToUInt64($raw,56+$ln)+64+$ln -eq $raw.Length) 'CHECKPOINT_HEADER'
        $inventory[$key]=$stage.artifact
    }
    $cpuSum+=$stage.worker_cpu_charge;$wallSum+=$stage.process.wall_seconds_through_cleanup;$proofCount+=$stdout.proof_stage_calls
    if(-not $stageGroups.ContainsKey($kind)){$stageGroups[$kind]=[ordered]@{count=0;cpu=0.0;wall=0.0}}
    $stageGroups[$kind].count++;$stageGroups[$kind].cpu+=$stage.worker_cpu_charge;$stageGroups[$kind].wall+=$stage.process.wall_seconds_through_cleanup
    if((Get-Item -LiteralPath (Join-Path $stageDir 'command\stderr.txt')).Length -gt 0){$stderrNonempty++}
}
Need ($cpuSum -eq $result.worker_cpu_charge_this_attempt -and $proofCount -eq 103 -and
    $result.retained_checkpoints.Count -eq 108 -and $inventory.Count -eq 108) 'TOTAL_COUNTS'
foreach($row in $result.retained_checkpoints){Need (Same $row.file $inventory[$row.key]) 'FINAL_INVENTORY'}
CheckPin $result.receipt;Need (Same $result.receipt $stage.artifact) 'FINAL_RECEIPT'
$markers=@(Get-ChildItem -LiteralPath $innerPath,$outerPath -Recurse -File | Where-Object {$_.Name -like '*FINALIZATION*'})
Need ($markers.Count -eq 0) 'NO_FAILURE_MARKERS'
$outFiles=@(Get-ChildItem -LiteralPath $innerPath -Recurse -File);$entries=@(Get-ChildItem -LiteralPath $innerPath -Recurse)
$outBytes=($outFiles|Measure-Object -Property Length -Sum).Sum;$reportBytes=(Get-Item -LiteralPath (Join-Path $innerPath 'RESULT.json')).Length
Need ($result.output_charge_this_attempt -eq $outBytes-$reportBytes+2*1048576) 'OUTPUT_CHARGE'
Need ($result.entry_charge_this_attempt -eq $entries.Count-1+2) 'ENTRY_CHARGE'
$sourceCount=0
foreach($row in $sel.sources.PSObject.Properties){
    $original=Join-Path $auditRoot $row.Name;$copy=Join-Path (Join-Path $outerPath 'sources') $row.Name
    Need ((Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash.ToLowerInvariant() -ceq $row.Value) 'ORIGINAL_SOURCE'
    Need ((Get-FileHash -LiteralPath $copy -Algorithm SHA256).Hash.ToLowerInvariant() -ceq $row.Value) 'COPIED_SOURCE';$sourceCount++
}
[ordered]@{status='READ_ONLY_SAVED_EVIDENCE_CHECKS_PASS';stages=$keys.Count;proofs=$proofCount;retained=$inventory.Count;
    stage_cpu=$cpuSum;stage_wall=$wallSum;groups=$stageGroups;stderr_nonempty=$stderrNonempty;files=$outFiles.Count;entries=$entries.Count;
    bytes=$outBytes;charged_bytes=$result.output_charge_this_attempt;charged_entries=$result.entry_charge_this_attempt;
    sources_original_and_copied=$sourceCount;failure_markers=$markers.Count;receipt=$result.receipt;
    outer_known_cpu=$outer.result.final_job.cpu_seconds+$outer.wrapper_cpu_seconds;
    inner_allowance_cpu=$result.prior_allowance_worker_charge+$result.worker_cpu_charge_this_attempt;
    inner_allowance_controller=$result.prior_allowance_controller_cpu+$result.controller_cpu_seconds;
    inner_allowance_wall=$result.prior_allowance_wall+$result.wall_seconds;
    inner_allowance_output=$result.prior_allowance_output_charge+$result.output_charge_this_attempt;
    inner_allowance_entries=$result.prior_allowance_entry_charge+$result.entry_charge_this_attempt}|ConvertTo-Json -Depth 6
