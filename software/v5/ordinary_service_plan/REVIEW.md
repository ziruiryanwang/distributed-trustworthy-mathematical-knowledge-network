# Independent service-plan review

Verdict: **GO FOR THE SELECTED SOURCE BOUNDARY; NO EXECUTION OR ADOPTION CLAIM**
(2026-10-26). Reviewer read the complete authored source/README and the final
two-line supervisor-schema/error delta. No unresolved source blocker remains
for the finite serve-only contract. The complete test source and exact proposed
selection are now also reviewed below; root must still select execution.
This review is not a passing test,
fresh service result, deployment, mathematical claim or completed v5.

Exact reviewed inputs:

| File | SHA-256 |
|---|---|
| `service_plan.py` | `3245a5f50d694ef5ca9714c6408e9cfc93b1378606398c433cdda4a4e113ee01` |
| `README.md` | `1c2ff344b62dec784eed7958e6a37c87c4856008a0b5e63af120b9e3a8780668` |

Reviewer owns only this file. No product code, state, Git, import, runtime or
network operation was changed or invoked by this review.

## Design basis inspected

- This directory's `CONTRACT.md`.
- `research/cycles/v5-2026-10-26-local-discovery/SERVICE-LIFECYCLE-DECISION.md`.
- Actual default package `run.py`, `peer.py`, serving path of `peer_api.py`,
  provider status/counter implementation, and the selected `commons.py`/Windows
  Job supervisor implementation. These were read as source, not imported.

No central design blocker is identified for a finite service-only plan. Reusing
the existing supervisors and retaining all uncertainty is substantially smaller
than adding an independently designed daemon or concurrent owner state.

## Checked implementation boundaries

1. The public entry has one finite serve-only grammar, strict bounded JSON,
   an externally hash-selected plan and package, no arbitrary shell,
   executable override, injected supervisor, test-double switch or implicit
   source/disclosure approval. The companion itself must be independently
   approved; it is not self-authenticated by its own executable bytes. The
   injected `_sequence` callables are private deterministic-test seams, not CLI,
   JSON or remotely reachable authority overrides.
2. Known launcher/supervisor source bytes and actual manifest roles are verified
   before execution. The complete public peer checks remain active. The runtime
   identity is not silently generalized beyond the supported package.
3. Before creating output, `validate_paths` inspects directly/indirectly selected paths:
   package/runtimes/companion/plan/config/custody limits; catalog/custody/index;
   nested TLS cert/key and optional authoring-offer file. It rejects overlap with
   writable outputs/state and preserve ordinary-path/no-reparse/no-hardlink
   requirements. Stable selected inputs are rechecked for every epoch.
4. The output root is fresh and atomically claimed. Different plans still rely
   on the real catalog lock; no invented cross-catalog custody lock or resume
   protocol follows from that claim.
5. All N epoch allowances are reserved from the original aggregate authorization.
   CPU uses the outer per-epoch Job once (which includes the nested launcher and
   peer), plus the final sequencer separately. Nested log files also consume log
   allowance; outer captured stdout alone does not bound them. Simultaneous
   memory/process caps reflect nesting. Report bytes are separately bounded.
6. The original monotonic horizon starts at `execute` before preflight; a child is
   launched only with room for its selected allowance and retained cleanup.
   Existing supervisor cleanup can exceed its sampled ceiling while ensuring
   process termination. The runner reports that limitation and cannot launch the
   next epoch after overshoot or uncertain closure. Eligibility is checked after
   input revalidation and durable INTENT, then again immediately before supervise.
   Final cost fields explicitly end before final-result fsync and stdout printing;
   cooperative accounting is not advertised as a hard whole-runner ceiling.
7. Each epoch retains intent before launch and fresh paths. Both outer and inner
   actual supervisor reports must show exact zero/closed state, no termination
   request, zero active/terminated descendants and empty cleanup errors. Outer
   supervision is called directly with constructed serve-only argv, not loaded
   from a caller-provided report. Both reports bind exact selected limits and
   the actual expected supervisor schema; contradictory error fields refuse.
8. RUN and actual peer reports are validated, including correspondence of stdout and
   RESULT where both exist. The peer can fail writing its report after previous
   bytes were produced; stale success cannot authorize continuation.
9. Validation requires exact state/profile/config/semantic/implementation binding,
   `LEASE_FINISHED`, quiescence,
   cleanup/budget/write-error absence, stable nonzero ready endpoint, true
   whole-custody/exclusive approval, zero remaining tasks/connections/reservations,
   and coherent integer provider counters. Root's explicit prepaid-schedule
   clarification permits the next already-authorized epoch after ordinary
   per-request failures or provider quota exhaustion, if complete service-level
   terminal/accounting/closure checks pass. It stops on accept/cleanup failure or
   unknown counters. It never grants an additional epoch or larger quota; the guide does not
   describe lease expiry as proof of useful/uninterrupted service.
10. A failed/missing report, changed input, exhausted budget or uncertain cleanup
    is terminal, not retry/resume authority. Aggregate reports separate observed
    CPU/counters from reserved caps; payload is not total network traffic.

## Resolved issue and explicit premises

The initial complete-source review found that `clean_supervision` did not require
the versioned supervisor schema. Author added exact
`DMKN_V4_OWNER_COMMAND_REPORT_V1` and rejects an `error` key on a purported clean
report. Reviewer read that final two-line delta and checked its resulting hash.
The unchanged actual supervisor already emits that schema.

The three hardcoded supervisor hashes were compared directly with the actual
default package files: `commons.py` `6ea16154...`, `domains.py` `651db5f6...`,
and `run_stage.py` `bdd2cbc2...`. Full hashes are present in the reviewed source.
Known launcher/interface pins match the selected source identities. Every epoch
rechecks selected plan/config/custody limits, interface sources, nested TLS/offers
and launcher bootstrap support; the unchanged child checks its complete package.

Cross-epoch storage immutability and all-writer exclusion remain operator
premises. The helper neither hashes the databases as snapshots nor holds an owner
lock through the gaps. README states this directly; no publication window or
cross-catalog serialization is promised. Local trusted code/OS/approved runtime
and protected-state assumptions still apply. Native Job nesting has a reviewed
source path and explicit extra process/memory budget; its actual public two-lease
operation remains a separate finite evidence gate, not a source-review result.

CPU from a failed launched attempt is kept separately when the outer supervisor
returned a final counter; otherwise completeness is false, not a zero-cost claim.
Completed-epoch counters do not purport to account for an unreadable failed peer
report. Logs reserve inner and outer stream caps plus bounded metadata; they are
not a hard disk quota. Provider counts are protocol observations, not availability
or mathematical-growth evidence.

No passing test or genuine two-lease operation is inferred from this review.

## Complete test and exact-selection review

**GO for root to select the one proposed controls01 execution.** Reviewer read
the complete `test_service_plan.py`, complete TEST-PLAN and unchanged runner
source; no test import or execution was used to reach this verdict.

| Selected source | SHA-256 |
|---|---|
| `test_service_plan.py` | `19f36bab1519df2bea566abfe780b46e0fe08f3872f1471de26c2eeeabd726a9` |
| `TEST-PLAN.md` | `6338cdeb09bc127e8b9e8ba778840c1a92e141421b48060b1498d4bd392fa756` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |
| `experiments/service-plan-controls01-selection.json` | `0f2463f0b64da80907bd923e14b92b7496e692f54c9b177cbe6c3e98401e81be` |

The fourth source snapshot is the already reviewed service implementation above.
Read-only hash checks matched all four source selections and all 163 external
pins. An ignore-independent file census (`rg --files -uuu`) exactly matched the
154 selected default-package paths; the other nine pins are three Python and six
Lean runtime files. No selected external pin is an old owner/custody/index state.
The output `experiments/v5-local-checks/service-plan-controls01` was absent at
review. The selection retains the default PROFILE, not the fresh archive-build
PROFILE. No selection bytes were edited by this reviewer.

The five groups cover schema/reservations, real report-shape mutations, finite
sequencing, filesystem/indirect input paths and report agreement, then one actual
public two-lease invocation plus an existing-output refusal. In particular:

- Supervisor schema omission/mismatch and contradictory error, termination
  requests, unsettled children, wrong identities, unknown cleanup and absent
  reports cannot satisfy the synthetic validator controls.
- Original-clock controls spend the horizon in preflight, input validation and
  durable intent. They inspect actual invoke ordering and prohibit an unintended
  next epoch. Ordinary request failure/exhaustion stays explicitly prepaid.
- The actual empty fixture uses the real custody/catalog/index constructors,
  closes their handles before serving, never initializes a basis, and never writes
  a checked root/operation. Table counts are read, not fabricated. The public
  helper path requires zero accepted attempts and payload, zero native worker
  CPU, and empty final mathematical roots/operations.
- Only new synthetic files are hardlinked for the path-refusal case. Fake TLS and
  offer files are path-test inputs, never executed or served by the actual case.
- The two actual one-second leases bind only `127.0.0.1:38194`. No client,
  third-party endpoint, native build/check, external publication or scheduled task
  is selected. A port collision is a retained failure, not a retry authority.
- The second helper invocation must refuse the already claimed output before an
  epoch, preserving the completed result hash and the two-directory census.

The exact outer selection is 240 wall seconds / 200 inclusive Job CPU seconds,
1536 MiB / eight processes, 4 MiB stdout / 1 MiB stderr. Inside it, the test's
cooperative deadline is 220 seconds / 60 CPU; the plan authorizes two 50-second,
80-CPU outer epochs around 35-second, 20-CPU public leases, with the original
160-second horizon. The experiment's stronger enclosing limits can terminate
before all plan allowances are consumed. That is deliberate and cannot count
as a passing plan. Inclusive outer Job CPU contains test/helper/launcher/peer
work; nested counters must not be added to it.

On a test subprocess timeout the harness kills/reaps its direct helper and
raises; the enclosing reviewed Job retains responsibility for descendants.
No second helper/epoch follows that error. Actual supervisor quiescence must be
audited after execution; source review does not substitute for that observation.

The selection runner snapshots and rechecks its inputs and checks the external
pins after the run. Its independently hash-bound historical test supervisor is
an experiment dependency only. The service companion itself loads supervision
from its approved ordinary package, not from that historical test directory.
