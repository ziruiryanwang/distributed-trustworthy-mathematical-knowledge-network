# Small native ordinary-abort discriminator

Prospective source-only design, 2026-09-21. No harness, launch, product edit,
import, SQLite query, compilation or native execution is supplied here. This
tests the seam in [ordinary-abort review](ORDINARY-ABORT-RECOVERY-REVIEW.md),
after its implementation and native-free contracts receive independent review.

## One finite claim

A genuinely initialized node can retain a charged ordinary submission whose
real Lean child was observed alive in its original public Job, terminate that
tree through the original supervisor, and publicly abort the resulting intact
pending request without promoting outputs or refunding work. The node can then
complete a deliberate fresh checked submission. Both interrupted refusal and
already-terminal success remain exactly replayable through the appropriate
public interfaces, even though their requests have native stage rows.

This is a process-interruption case, not host reboot, hot-journal repair,
hostile-source isolation, universal availability, discovery or useful growth.
The test hook is explicit trusted qualification code. Its observation is not
the original quiescence authority: the unmodified base supervisor produces
that authority through its real cleanup and receipt path.

## Fixed inputs and nine invocations

Use a fresh integrated schema-3 installation with reviewed ordinary recovery,
fresh locally built support, one client `local`, no peers/offers and the usual
five common packages. Configure `--initial-requests 3 --initial-stages 3
--initial-reserved-mib 408 --initial-metadata-mib 32`; retain product request,
stage, native and public-supervisor limits unchanged. No owner renewal is needed.
Real physical-supply checks remain enabled; no accepted state or database row
is manufactured.

Store this exact UTF-8/LF source, including its final LF, once in driver inputs:

```lean
universe u
noncomputable def AbortCompose (A B C : Sort u)
    (g : B -> C) (f : A -> B) (a : A) : C :=
  g (f a)
```

Use root `AbortCompose` and the actual bootstrap context C0 for both submission
attempts. This safe noncomputable fixture has no sleep, `#eval`, import, tactic,
added axiom or proof-check bypass. It is an input until the successful pipeline
actually checks its captured and reconstructed declaration.

Let U be used `(requests, stages, reserved MiB)`; authorization A is always
`(3,3,408)` after configuration. All ordinary IDs below are distinct except the
explicit exact replay. Retain/reuse original raw bytes, not reconstructed JSON.

| # | Invocation | Required result | U after |
|---:|---|---|---|
| 1 | Installed `build.py` | Fresh support stage and two real compilations | absent |
| 2 | Installed `manage.py configure` | Immutable fresh config, no database yet | absent |
| 3 | Public ordinary `init`, owner | Genuine checked C0/S0, stage 0 | (1,1,136) |
| 4 | Direct original public Transport call, `submit-interrupted` | One test-hook trigger during observed real Lean execution; authentic failed-transport quiescence receipt; intact pending request/stage 1 | (2,2,272) |
| 5 | Installed `manage.py recover`, `recover_ordinary` selecting #4 | Fixed interrupted refusal, active clear, no promotion | (2,2,272) |
| 6 | Public ordinary byte-exact replay of #4 | Exact #5 refusal; historical, no native work | (2,2,272) |
| 7 | Public ordinary `submit-fresh`, same C0/source/root | Actual full checked artifact, stage 2 | (3,3,408) |
| 8 | Installed recovery byte-exact replay of #5 envelope | Exact #5 refusal, historical-only, no mutation | (3,3,408) |
| 9 | Installed `recover_ordinary` selecting #7's actual receipt | Exact #7 success bytes, historical-only, no mutation despite stage row | (3,3,408) |

Totals: **nine invocations, eight installed CLIs plus one directly supervised
public worker call**. They comprise two preparations, four ordinary calls
(three reservations plus one replay), and three owner recovery calls. #4 uses
the same installed `node.py` command, working directory, flags, twelve pins,
request/event locations and unchanged ordinary-eight supervisor profile as
`manage.py request`; it is not described as an invocation of that CLI.

Each owner envelope contains exactly `op:"recover_ordinary"`, `client:"owner"`
and `args:{client:"local", request_id:..., supervisor_receipt:ABS}`. #5/#8 select
the original #4 receipt, never #6's clean retry receipt. #9 selects #7's original
successful call receipt. No additional status, inspect, publish, grant or retry
is included; bounded readonly snapshots supply the state observations.

## Minimal test-only observation/termination hook

Reuse `supervise.Transport.__call__` unchanged. Subclass only
`output_within_bounds(directory)`: always call its original implementation first,
then perform the bounded observation below. Once qualified, raise one fixed
test exception, for example `OrdinaryAbortFaultInjected`. The base method's
existing catch invokes `quiesce(..., terminate=True)`, reaps its actual direct
child, observes whole-Job active zero, checks Job close, and writes the genuine
`supervisor.json`. Do not override quiescence, receipt writing or command launch.

The public Job is a local variable in the base method, not an attribute available
to the output callback. Use one explicit test-only runner adapter whose `Job`
factory constructs and returns the **genuine installed `run_stage.Job` object
unchanged**, retaining that exact object for observation. Permit exactly one
construction with the expected ordinary-eight limits. Do not subclass its
limits, wrap/fake its stats, replace OS functions or modify installed modules.
The adapter's runner-file binding points to the actual installed runner used
by the factory; its extra capture behavior belongs to the separately pinned
qualification worker and must be disclosed as such, not passed off as unchanged
module authority. Root approved this adapter shape for further design review.

Bind #4 to a fixed fresh `scratch/calls/call-abort-original` directory and its
exact raw request. Its known request key determines only
`state/work/<key>/stage-0001/stage.json`; do not enumerate arbitrary processes,
requests or stages. Genuine bootstrap already used stage 0, and no other writer
is active. Stage existence is an observation, not a manufactured reservation.

### Bounded candidate observation

- Allow at most 600 hook observations and at most 30 elapsed seconds from the
  original call's entry. Each invocation performs at most two reads of the
  selected stage receipt, at most 256 KiB each. Base 50-ms polling is unchanged;
  add no inner retry/sleep loop. These ceilings limit observation attempts,
  not the entire supervisor's cleanup/persistence duration.
- Missing files, a bounded decode failure caused by an in-progress JSON rewrite,
  or a not-yet-running first step mean “not observed yet.” Record bounded counts
  and continue to the next base poll. Oversize input, unsupported valid structure,
  changed immutable binding, exhausted observer budget or Win32 query failure
  are failed qualification, not successful triggers.
- Authenticate the selected stage plan once when available, within 1 MiB,
  against exact domains, request/stage paths, runner/Python/Lean pins, source
  digest/root and fixed submission pipeline. For the candidate receipt require
  the same stage/domain/plan bindings, status RUNNING, exactly the first step,
  index 0, status RUNNING, a positive integer PID, and the exact pinned Lean
  command/working directory from that plan. Cache only immutable plan facts;
  a cached live receipt is not continuing liveness evidence.
- Open a process handle for that PID with query and synchronize rights only
  (`PROCESS_QUERY_INFORMATION | SYNCHRONIZE` suffices on the selected profile).
  Keep the handle itself: PID text alone is not a stable process identity.
  `QueryFullProcessImageNameW` must match the actual pinned Lean executable;
  `IsProcessInJob` must succeed and report membership in the **exact captured
  original public Job**, not merely some Job or the native inner Job.
- Re-read the selected receipt with the same bound and require the same
  authenticated RUNNING first-step snapshot/PID/command. Require
  `WaitForSingleObject(handle, 0) == WAIT_TIMEOUT` after the other checks.
  `GetExitCodeProcess == STILL_ACTIVE` alone is unsuitable because that integer
  may also be a process exit code. The unchanged receipt check plus exact Job
  membership avoids interpreting a later step or unrelated reused PID as the
  selected first Lean child.
- On that observation, set a one-way trigger flag and retain its bounded facts
  and receipt bytes in memory; immediately raise the fixed exception. Do not
  perform a filesystem census, SQLite query, fsync, source check or second
  native action between qualification and the throw. Trigger at most once.

This is sequential observation, not an atomic freeze of Lean execution. The
child may finish between observation and Job termination. Therefore post-cleanup
state must still be intact **pending** to pass; a terminal outcome, missed
window or ordinary completion is not relabelled as the intended interrupted
case. No automatic rerun, artificial sleep or source complexity inflation is
authorized to force a successful trigger.

### Handles, receipt and failure accounting

Close every nonselected candidate handle before the callback returns; check
`CloseHandle` results and report failures. Retain the selected leaf handle
through the base call's cleanup, then require it to be signalled and close it
exactly once. Close it in a `finally` path even when base supervision fails.
Failure to verify or close it makes the qualification fail, regardless of the
original Job receipt. The test adapter never closes or terminates the public
Job itself; the base supervisor owns that lifetime.

Only the fixed injected exception plus exactly one recorded live-child trigger
can count as the expected #4 failure. Catch its resulting `SupervisorFailure`,
but independently retain/read the actual persisted original receipt. Require
the existing recovery quiescence fields, empty cleanup errors and no
output/evidence uncertainty; deliberate termination is allowed. No fabricated
event or completed stage receipt is needed. Preserve partial native JSON/logs
and any stale stage lock verbatim.

Persist the captured hook facts/snapshot after original-tree cleanup, binding
them to its request, plan, original receipt and qualification-source hashes.
Their persistence failure stops the experiment. The original receipt keeps its
exact twelve ordinary source pins because recovery authenticates that set;
the hook is instead covered by the outer pinned worker and its supplemental
evidence. Never append a fake original pin or rewrite the original receipt to
claim the hook was product code.

## Native, state and preservation obligations

After #4's complete quiescence, observe all ten tables read-only under the
existing owner lock. Require the real original attempt binding, active key,
pending exact request, stage-1 charged row, and no new artifact/context/head or
publication from #4. A nonempty SQLite sidecar, missing receipt or terminal row
stops this case; no sidecar deletion, row repair or exception injection is used
to obtain the desired state. The native-stage reservation preceded the observed
child by the actual checker/store path, not a test-created row.

Take original work/call file length/hash inventories only after quiescence.
Across #5, the exact permitted logical delta is the selected request's fixed
refusal plus active=NULL. U, authorization, grants, stages, attempts, previous
responses and all existing mathematical records/files remain unchanged. Recovery
scratch evidence is new, separately counted output. #6/#8/#9 preserve every
control table and all preexisting work/call bytes; new transport/recovery evidence
is permitted. No checker/stage allocation occurs in those calls. #9 must forward
the original `accepted:true` success bytes, not invent a new acceptance decision.

#7 is a genuine five-command capture/replay/inverse/replay submission against
C0 with the same source bytes as #4. Independently audit the actual safe
polymorphic composition type/body, canonical/root identity, allowed dependencies
and native receipts. It remains a private artifact: head C0 and provider cut
zero are unchanged. No returned fixture name or zero process exit alone proves
this binding.

Exactly three receiver stages are charged: bootstrap 0, interrupted submission
1, successful submission 2. Bootstrap completes one pipeline command and #7
completes five. The interrupted stage has **at least one actually observed live
Lean command**, but do not invent its final completed-command count. Preserve
the observed prefix and report what final retained evidence really establishes;
its fixed plan contains at most five serial commands. Support building is
separate, one stage/two compilations. These are not OS-process counts.

Final node charges are `3*8 + 3*128 = 408 MiB = 427819008 bytes`, with no grant,
refund or reset. A completed output from the interrupted stage does not alter
that accounting or promote a mathematical result.

## Reuse, bounds and exit

Adapt the fresh native-renewal coordinator/worker shape, without importing or
running that old driver and without creating another generic framework. Put
the hook in the pinned new worker rather than a new product module. Preserve
the existing `scenario_profile` outer-sixteen adapter and its measured worker
tree; the captured **inner original public Job remains ordinary-eight**.
Keep product limits unchanged, including recovery's 30-second wall/15-second
CPU/256-MiB profile. The observer's 30-second/600-attempt gate can stop earlier
but never extends the original allowance.

Proposed fresh roots are `product-local/ordinary-abort-native-01` and
`software/qualification/ordinary-abort-native-01`. Both must be absent. Reuse
the 450-second wall/CPU, 6144-MiB, sixteen-process outer test profile and 1-GiB,
16384-file, 32768-entry combined retained endpoint envelope, subject to root's
separate reviewed allocation. Bind the actual integrated product manifest;
do not borrow old source hashes or compiled support. The same selection pattern
is expected to have 101 product files, but actual exact inventory verification
is required before launch, not an assumed fact of this note.

The eight outer input pins can retain the existing shape: interpreter, new
coordinator, new worker including hook, scenario profile, installed-source stage
runner, supervisor, domains and Lean executable; launch is the ninth. Original
call authentication separately binds the actual twelve installed ordinary pins.
The three recovery wrappers bind their genuine mode/request/grant/source inputs
under the existing at-most-sixteen-pin profile. All failed-prefix work and hook
observations belong to the same retained/resource accounting. Outer Job CPU
includes nested workers once; record outside-coordinator costs separately.

Elapsed-time-only interruption is simpler but does not discriminate whether
native work was running; a stage marker alone is also insufficient. Source
sleep/code-generation dependencies and debug/suspend-process instrumentation
add unnecessary mechanisms. The selected live-handle/Job hook uses existing
supervisor failure handling and explicitly accepts an inconclusive missed
window instead of claiming guaranteed timing.

Any unexpected source failure, missing binding, trigger miss, state mismatch,
cleanup uncertainty or persistence failure stops the nine-call sequence and
retains the prefix. Initial success label is only
`PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`. A later independent audit must check
the actual native observation, authentic original receipt, exact state/replay
deltas and genuine successful pipeline. No execution is authorized by this
design note.
