# Native ordinary-abort harness: independent source and launch review

2026-09-21. **PASS at the source/exact-launch review gate; no remaining
actionable defect found in this cut.** This is not a native-run result, runtime
qualification, mathematical acceptance, or authorization to change the reviewed
allocation. Root owns execution and the subsequent independent outcome audit.

The complete design, final worker and coordinator, author handoff, test-only
outer profile, and relevant real supervisor/runner/checker/storage paths were
read. Review used source reads and inert PowerShell/.NET file/JSON/hash checks
only: no Python import, syntax execution, SQL query, build, or native launch.
Only this review file was authored; harness/product/evidence files were not
edited by the reviewer.

## Reviewed final bytes and exact allocation

Paths are relative to `software`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/ordinary_abort_native_worker.py` | 58,198 | `BB91D83F4C5A45FB869779A7B03528F884D92EF4527988A96FB20A10FB79EB30` |
| `tests/run_ordinary_abort_native.py` | 15,881 | `9590E2080859BBABA28868E78091681C65DAA2093B5D7D99340B220CD3141F45` |
| `qualification/ordinary-abort-native-launch-01.json` | 41,639 | `DA7458F89E93A6B184F1071152A31E9964AA6C6DB1ECA7FDCAE447A86B518033` |
| `drafts/ORDINARY-ABORT-NATIVE.md` | — | `9F9BD1BAE911C29DF9317C5D19B9D841C358D9B69C50C57F2604142D5557C3DE` |
| `tests/scenario_profile.py` | 4,619 | `B8B3E1B1C1485DE80AE9FB2371C32771A4F8505FC90D580E021442F227FBCF6A` |

Independent current-filesystem enumeration matched the launch's entire ordered
101-file product inventory, not merely its claimed count: four selected top-level
files, top-level Python sources, and all native/assets files. Every relative and
absolute path, byte count, and SHA-256 matched; there were no duplicate paths,
omissions, or extras. Product bytes total **3,478,260**. The recursive native/assets
selection contained 90 filesystem entries within the declared traversal bound.

The eight ordered inputs are the actual `D:\Python314\python.exe`, this
coordinator, this worker, `scenario_profile.py`, current `run_stage.py`, current
`supervise.py`, current `domains.py`, and the selected Lean executable. All pins
matched current files. They total 318,416 bytes; adding the launch gives exactly
nine outer pins / 360,055 bytes, within the unchanged 16-pin/64-MiB envelope.
No reparse point was found among the 130 distinct selected file/ancestor paths.

Both fixed output roots were absent, including an explicit parent-entry check:
`product-local/ordinary-abort-native-01` and
`software/qualification/ordinary-abort-native-01`. The launch has the reviewed
450-second wall/CPU, 6144-MiB, sixteen-process outer profile and 1-GiB,
16,384-file, 32,768-entry retained endpoint bounds. These checks are a
pre-execution observation; startup must still reauthenticate the immutable cut
and reject a changed pin or nonfresh root.

## Hook and original public authority

Worker lines 576–607 use the genuine installed `supervise.Transport.__call__`
without replacing launch, receipt writing, quiescence, or process cleanup.
The only override calls the original output-bound check first, then the test
observer. The runner adapter exposes the real installed runner path and returns
the exact genuine `run_stage.Job` object; its factory permits one construction
with ordinary limits `(450, 6144, 8)` (lines 200–204). It does not modify the
object, OS functions, limits, or stats. The additional capture behavior is
explicit pinned test code, not falsely claimed as product-module authority.

The observer (lines 219–326) selects only the known stage-1 receipt. It binds the
source bytes/root, domains, request/stage paths, complete fixed five-command
plan, runner/Python/Lean pins, and actual first-step command/cwd/Lean path.
Missing/in-progress JSON is bounded retry-at-next-public-poll observation;
unsupported structure, a missed first-step window, oversize, or query failure
cannot become a successful trigger. It performs at most two bounded receipt
reads per observation, at most 600 observations, and checks the 30-second
deadline at callback entry and again immediately before the final wait/trigger.

The leaf handle has query/synchronize rights only. Its executable image is
checked and `IsProcessInJob` names the exact captured original public Job.
An identical second running-receipt snapshot precedes the zero-time handle wait;
only `WAIT_TIMEOUT` qualifies as live. No `STILL_ACTIVE` exit-code shortcut,
process enumeration, stage-marker-only claim, artificial sleep, or native retry
is used. After qualification only bounded in-memory facts are retained before
the fixed exception is thrown into base cleanup.

Every nonselected handle is checked closed before returning; the selected
handle is held through original-tree cleanup, required to be signalled, and
checked closed in a finally path. The positive path requires balanced opened/
closed counts and no close error. Supplemental evidence is persisted after
cleanup and directly pins the observed stage bytes, plan, worker, request hash,
and actual original supervisor receipt (lines 610–636). No original evidence
is rewritten or supplemented with a fake thirteenth source pin.

Lines 637–696 require the genuine persisted failed-transport receipt to name
exactly the injected exception, the unchanged twelve source pins, exact raw
request and command, and all original whole-tree cleanup fields. The original
ordinary settle allowance remains **15 seconds**; recovery alone uses its
existing 5-second allowance. Observing a live child is not itself quiescence
authority. Actual base cleanup must reap the direct child, observe active zero,
and close the original Job without uncertainty.

## State, continuation, replay, and cost

The worker's snapshots use `mode=ro`, query-only connections, existing owner
locking, bounded reads of all ten tables, and nonempty-sidecar rejection
(lines 349–385). The only state-changing operations are the genuine selected
product calls. The harness does not create an accepted row, write SQLite,
delete a sidecar, remove a stale native lock, repair output, or refund a charge.

The post-interruption comparison at lines 682–695 admits only the real second
reservation, original owner-attempt record, charged stage 1, and active pending
request. It excludes context/artifact/head/publication changes and refuses an
ordinary terminal completion. Thus a sequential liveness observation followed
by a race cannot be relabelled as the intended pending case.

The first recovery's complete ten-table comparison permits only the selected
pending row's fixed refusal and active-slot clearing (lines 543–573). Work/call
file maps are checked across recovery. Exact ordinary refusal replay and both
owner recovery replays require unchanged tables, historical-only events, and
byte-identical responses. Original work/call bytes are also retained through
the complete sequence. Historical successful recovery forwards the actual
`accepted:true` reply; it does not make a new acceptance decision.

The deliberate fresh submission uses the same C0/source/root, not an automatic
retry. Its complete five-command capture/replay/inverse/replay plan, real native
receipts, stored artifact, exact request/response, and exact table delta are
required. It leaves C0 and P1 cut zero unchanged (lines 786–856). The actual
canonical polymorphic type/body, root identity and dependencies still require
independent post-run artifact inspection; fixture names and zero exits are not
substitutes for that audit.

The final count checks implement nine invocations: two preparation CLIs, four
ordinary calls (including the one direct public Transport call), and three
owner recovery CLIs. There are eight installed CLI invocations, three consumed
ordinary requests, three charged receiver stages, zero grants, and **408 MiB =
427,819,008 bytes** charged. Bootstrap plus fresh submission complete six normal
pipeline commands. The interrupted stage records one actually observed live
Lean command and **unknown**, not invented, completed-command count; its fixed
plan contains at most five commands. Two support compilations remain separate.
The interrupted admission supply event may be lost; actual product supply
checks stay enabled and the harness does not fabricate the missing sample.

## Outer predicates and remaining gate

The unchanged test-only outer-sixteen adapter changes only its reviewed empty
Job active-process field, checks full limit readback, and inherits real base
supervision. The coordinator retains exact output/event/pin checks, real whole-
tree cleanup, CPU/memory/wall/process predicates, and quiescent-only retained
census including room for final reports (lines 254–316). Worker aggregate CPU
includes nested descendants once; outside-coordinator costs remain separately
reported, not silently declared complete.

The outer `terminated_processes == 0` predicate is deliberately preserved at
coordinator line 283 and in base successful transport validation. The exposed
Win32 `TotalTerminatedProcesses` field is the Job limit-violation counter, not
a count of every deliberate `TerminateJobObject` action. Manual cleanup of the
selected inner public Job is not grounds to weaken outer resource predicates.
An actual nonzero outer counter or other resource failure must remain failure.

Three early review observations were repaired before this final cut: the late
observer deadline recheck, the ordinary settle-value mismatch, and direct
supplemental receipt pinning. No remaining change is requested by this review.
An authorized run may only reach `PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`.
Trigger miss, process/cleanup uncertainty, ledger mismatch, persistence failure,
or resource failure stops and preserves the prefix; no rerun or profile
relaxation is implied. The finite process-interruption claim does not cover
reboot, hot-journal repair, hostile sources, general availability, or useful
mathematical growth.
