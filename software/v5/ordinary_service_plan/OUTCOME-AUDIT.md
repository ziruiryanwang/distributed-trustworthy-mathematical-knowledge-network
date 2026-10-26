# Independent service-plan controls outcome audit

2026-10-26. Verdict: **PASS — selected five-group controls and actual finite
two-lease service orchestration; not continuous availability or final v5.**

The single selected `service-plan-controls01` execution returned zero and closed
its process tree. Both genuine public leases finished cleanly. The deliberate
second helper invocation refused the existing output before launching an epoch.
No mathematical object was accepted, no native mathematical operation occurred,
and no client sent a request in this test. There is no unresolved blocker within
this selected evidence boundary.

This is a saved-output audit, not a rerun. The reviewer read the nested reports,
compared retained streams, inspected the relevant tested source, independently
checked input pins and exact package census, and queried the retained SQLite
tables through standard-library read-only immutable connections. No product
module was imported, no production state was written, and no used source,
selection, result, Git state or shared ledger was changed. The only authored
file is this audit. Prior source/test review is [REVIEW.md](REVIEW.md).

## Exact evidence and input closure

All evidence below is beneath
`experiments/v5-local-checks/service-plan-controls01/` unless stated otherwise.

| Evidence | SHA-256 |
|---|---|
| `selection.json` | `0f2463f0b64da80907bd923e14b92b7496e692f54c9b177cbe6c3e98401e81be` |
| Outer `RESULT.json` | `bc937a6f31d1bab075a432d508c20bafe2cfe343791f2217311a082811e5f026` |
| `suite/RESULT.json` | `fb97e87b379463d78564caf07d170749f5b651ada5729c8920a310786aba9e9e` |
| `suite/public/plan.json` | `76093a82095e75860ff60a38572f838a09d644a9ee0bd8331cbfe8c514262dee` |
| `suite/public/config.json` | `71b90d96494b6c048150050f83e71ff34c9dbafa7a53b228e1fcd5a2289006ca` |
| `suite/public/custody-limits.json` | `0f53ce08d967594d83249177805edb4e7f6cacac9c035ca32610f2a1c5a4a267` |
| `suite/public/service-plan/RESULT.json` | `7026aa4cde772df73758833ee205bc00174b3a568bbf6d977f1e93cc0a5adbd7` |
| `suite/public/resume-refusal.stdout` | `d9e2a474aa88a14a9104184d77ba999838ec7aef6fe073f82fbf7597e8a57fa4` |

The retained selection equals the original
`experiments/service-plan-controls01-selection.json` by SHA-256. All four
selected source originals **and** their four execution snapshots still match:

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_service_plan/service_plan.py` | `3245a5f50d694ef5ca9714c6408e9cfc93b1378606398c433cdda4a4e113ee01` |
| `software/v5/ordinary_service_plan/test_service_plan.py` | `19f36bab1519df2bea566abfe780b46e0fe08f3872f1471de26c2eeeabd726a9` |
| `software/v5/ordinary_service_plan/TEST-PLAN.md` | `6338cdeb09bc127e8b9e8ba778840c1a92e141421b48060b1498d4bd392fa756` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

All **163 external pins** matched independently after execution: the complete
**154-file default package**, plus three Python and six Lean runtime files.
An ignore-independent `rg --files -uuu` census matched the selected package
paths exactly, with no extra or missing file. This is a named-file pin boundary,
not a hermetic proof of every runtime/OS dependency.

The actual package remains
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`,
with PROFILE
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`
and installation manifest
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The test did not substitute the newer archive-installation package. Actual
service reports bind implementation
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`
and semantics
`9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7`.

## Five groups and their limits

1. **Strict inputs and up-front reservations:** 52 recorded refusals cover
   malformed/duplicate JSON, booleans and invalid fields, insufficient aggregate
   reservations, unsupported scope, endpoint and disclosure approval errors.
2. **Report binding and prepaid client failure:** 62 recorded refusals exercise
   supervisor schema/error/closure, report identities, provider accounting and
   missing reports. The clean synthetic quota-exhaustion case passes: ordinary
   failed requests may consume their already prepaid allowance without granting
   another epoch or converting a client failure into a whole-plan denial of
   service. This is a synthetic validator result, not actual loaded service.
3. **Original allowance and finite sequencing:** 13 deterministic cases include
   two clean epochs, two prepaid exhausted epochs, and stops for missing/unclean
   reports, changed inputs, original-horizon/CPU exhaustion, spending time in
   preflight/input checks/durable intent, failed completion recording and an
   observed aggregate excess. Recorded invocation lists show no automatic retry
   or new allowance after those terminal outcomes.
4. **Paths, pins and report agreement:** 13 recorded refusals cover stale pins,
   state/input/output overlap, indirect TLS/offer paths, nonordinary paths,
   a synthetic hardlink, existing output, disagreeing reports and duplicate
   fields. The preflight control created no output.
5. **Actual public operation:** two one-second loopback leases at
   `127.0.0.1:38194`, followed by one actual helper invocation that refuses the
   same output. There were no clients, TLS handshakes or mathematical commands.

The first four groups use pure validation/sequencing seams and synthetic files
or reports. Only the fifth group establishes actual public service execution.
The suite reports `PASS` after all five groups; this does not independently
exercise live quota exhaustion, packet loss, malicious clients or crash recovery.

## Actual two-epoch bindings and closure

The output has exactly `epoch-0001` and `epoch-0002`. Each retains INTENT,
COMPLETE, outer command/supervision, inner LAUNCH/RUN/SUPERVISION, child streams,
and service READY/RESULT. In both epochs:

- INTENT binds the selected config, PROFILE and unchanged operation/epoch caps.
  Outer argv/cwd agree with the actual command record; inner argv agrees with
  LAUNCH and the child command record. The only product operation is `peer serve`.
- Both supervisor reports have schema `DMKN_V4_OWNER_COMMAND_REPORT_V1`, status
  `COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, direct child reaped, Job closed,
  no termination request, no cleanup error, and zero final active/terminated
  processes. The outer epoch counts four lifetime processes; the nested inner
  Job counts two. These are nested observations, not additive process totals.
- RUN is successful and binds the expected diagnostics, PROFILE and installation.
  Its mathematical disposition remains `NOT_INTERPRETED`; historical LAUNCH's
  prelaunch `NO_CHILD_LAUNCHED` is not mistaken for the terminal outcome.
- The actual service reports `LEASE_FINISHED`, quiescence and clean cleanup.
  All numeric provider counters are zero, `accepting` is false,
  `admission_exhausted` is false and `mathematical_acceptance` is false.
- Retained outer stdout equals inner RUN as parsed JSON; inner child stdout
  equals service RESULT. Actual helper stdout likewise equals its saved RESULT.
  All retained stderr streams are empty. COMPLETE rows agree with these reports.

The plan result is `FINITE_PLAN_FINISHED`, `finished = 2`, with exactly two known
attempts and complete attempt-CPU accounting. No sampled limit was triggered.

## Existing-output refusal and no mathematical acceptance

The second helper invocation returned the retained `NO_EPOCH_LAUNCHED` report:
`SERVICE_PLAN_FRESH_PATH`, zero completed epochs, empty attempt list and zero
known attempt Job CPU. The executed test asserts exit code 1, equality of the
completed RESULT's before/after SHA-256, and the unchanged exact two-epoch census.
The source rejects the existing output in `validate_paths` before loading the
launcher or creating output; `output_path` remains unset, so it cannot write a
replacement final result on this path.

There is no separately saved full-tree before-image. Thus the preserved evidence
supports the asserted result/census preservation plus the reviewed no-write
control flow, not an independently reconstructable before/after comparison of
every byte in every state directory.

Fresh state was created using the genuine custody/catalog/index constructors,
without native initialize, a basis, copied historical owner state or fabricated
accepted roots. Both actual service reports have native worker CPU zero.
Independent read-only post-run SQLite inspection found:

| Retained table | Rows |
|---|---:|
| Catalog `roots` | 0 |
| Catalog `operations` | 0 |
| Custody `objects` | 0 |
| Discovery index `objects` | 0 |

These facts agree with the executed test's own checks. The service-plan pass is
not mathematical acceptance, contribution, discovery or growth evidence.

## Actual cost and authorization

The enclosing selected limits were 240 wall / 200 inclusive Job CPU seconds,
1536 MiB, eight active processes, 4 MiB stdout and 1 MiB stderr. The plan retained
its original 160-second horizon and two prepaid epochs: each outer epoch
50 wall / 80 CPU / 640 MiB / four processes; each public operation
35 wall / 20 CPU / 512 MiB / three processes. Its aggregate reservation was
220 CPU seconds, eight accepted attempts, 2 MiB reply payload and 44 MiB logs.
The enclosing experiment's stricter CPU ceiling was intentional; it did not
renew or expand the plan authorization.

| Measurement | Actual |
|---|---:|
| Whole selected check elapsed | 7.381859200075269 s |
| Outer supervision through cleanup | 7.12967860000208 s |
| Whole check inclusive descendant Job CPU | 3.984375 s |
| Check wrapper CPU, separate | 0.5625 s |
| Known combined CPU at outer accounting boundary | **4.546875 s** |
| Outer peak Job private commitment | 98,447,360 bytes |
| Outer lifetime processes / final active | 14 / 0 |
| Outer stdout / stderr | 30,304 / 0 bytes |
| Epoch 1 / epoch 2 inclusive outer Job CPU | 1.15625 / 1.3125 s |
| Sum of epoch Job CPU | 2.46875 s |
| Helper runner CPU before final report | 0.265625 s |
| Helper wall before final report | 5.121350700035691 s |
| Completed epoch streams | 6,352 bytes |
| Accepted attempts / response payload | 0 / 0 bytes |

The suite's 6.663580700289458 wall seconds and 0.984375 controller CPU seconds,
and all helper/epoch/inner/peer CPU counters, are already inside the enclosing
Job; do **not** add them to 4.546875 again. Epoch logs are 1,980 inner plus 1,196
outer bytes apiece. The helper's own CPU subtotal is 2.734375 seconds, but excludes
its final-result fsync/stdout work; the enclosing check includes the child work
through its closure. No figure purports to include human/agent review cost or
every OS activity. This audit's read-only diagnostics are not part of the test.

## Disposition

Adopt only the finite serve-only scheduling result against the pinned default
package and its stated trusted-code/protected-state premises. Existing source
limitations remain: no lock held across inter-epoch gaps, operator exclusion of
other writers, cooperative main-runner CPU limits, sampled wall/log limits,
bounded cleanup that may exceed a sampled epoch ceiling, no resume or automatic
retry, and no guarantee of uninterrupted or useful service. Independent-host
operation, sustained service under clients, broader deployment assurance and
the full useful-growth/final-v5 objective remain separate obligations.

Preserve this run and all selected bytes. No rerun, new epoch, product adoption,
release or further campaign is authorized by this audit.
