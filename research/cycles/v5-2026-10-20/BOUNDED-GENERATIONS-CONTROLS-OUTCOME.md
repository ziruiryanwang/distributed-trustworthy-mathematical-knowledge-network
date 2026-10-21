# Bounded generations controls01: independent actual audit

2026-10-21, `support_guest`.

Disposition: **PASS_EXACT_TWELVE_REGISTRY_AND_SYNTHETIC_FAILURE_CONTROLS**.
The sole selected run passes all twelve reviewed groups and clean outer closure.
It qualifies these real-registry and explicitly synthetic control-flow checks,
not actual service startup/positive actor closure, crash-process recovery,
reclamation, a physical-storage envelope or full v5.

## Exact evidence and bindings

Run root: `experiments/v5-local-checks/bounded-generations-controls-01`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` | 39739 | `4c639c42725abed7c0d4241e71c8d808da90ef9744e2d25d8bf400712bbc22f3` |
| Outer `RESULT.json` | 2135 | `c5d6438d0274e1a08b937cd3ddd10be750284020fba13d4a21785ef1b39476ee` |
| Inner `bounded-generations-controls-result.json` | 59393 | `97115b50d8d799b8a18e91b16efbef8355df28ae8c2ce30dbbb420358fe7dc2c` |
| `command/stderr.txt` | 1900 | `771a1ebae8779de627413013a918a6f1e99a03b78a50beb480b9a8d2e9013cfb` |

Stdout is empty. I rehashed all four selected canonical/snapshot sources, all
142 runtime pins and all 123 reported logical source entries. Every size/hash
matches; all 89 reported actual import origins belong to those selected paths.
The exact ordered twelve-method tuple extracted by AST from the saved test
source equals the report's selected list, the observation-key set and the
ordered twelve `... ok` stderr lines. Stderr ends `Ran 12 tests in 0.542s / OK`.
Inner status is PASS, tests 12, failures/errors/skips 0 and forbidden calls empty.

Used source pins are lifecycle
`6852b5a20d4b188d328c5554f40e0bdfb2b20f84943ac689350459a5e8b2f90d`,
composition `404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`,
tests `33d036c8cc63cd62ed0caadbd60ac12ef7032ca8a307c7f73aaf2eb175334573`.
The exact selected basis is documented in independent source review
`BOUNDED-GENERATIONS-REVIEW.md`,
`e0ecd34f0a9339b06df6fe467890c6d66d41ae487d7cbeafaf551f484f6a1c63`.
Selector `09aa9a5ef5490e91a7698398832a9b65c72f25a8f96b36ce3d99990d87af5fd1`
uses the unchanged installation in place, with release
`1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be`.
Its 142 pins are 121 SDK files, 18 selected Python runtime files and three
manifests. This is not a complete standard-library or hermetic-toolchain proof.

## Actual controls and retained state

The reported assertions demonstrate the selected configuration, slot/funding,
protected-path, monotone-horizon, allocation-before-path, identity/marker,
clock, intent, exhaustion and synthetic cleanup boundaries. For additional
independent corroboration, I opened all thirteen retained registry databases
using stdlib-only `mode=ro&immutable=1` and checked their final rows and fixture
files without importing any product. Each database hash was unchanged by the
read. Every registry retains exactly two slot rows.

| Case | Independently checked durable/retained outcome |
|---:|---|
| 1 | Empty registry, sequence/floor 0; all four configuration refusals reported. |
| 2 | Sequence 2/floor 0; two PROVISIONING/NONE/run-0 slots; last horizon `2000000000001`. No third generation. |
| 3 | Sequence 1, PROVISIONING/NONE/run 0; generation directory exists but failed marker remains absent. No recreated marker or refunded allocation. |
| 4 | RETIRING/UNKNOWN/run 1 with original `max_runs=1`; repeated reserve and retirement commit refused. No run directory or actor was constructed. |
| 5 | PROVISIONING/NONE/run 0; exact deliberate corrupt marker `CONTROL_WRONG_GENERATION_MARKER` remains. |
| 6 | Main unstarted generation and separate empty foreign-clock registry preserved; deterministic early/backward/expiry/model/session refusals and drift-floor assertion pass. |
| 7 | Sequence/floor 2; both never-started generations RETIRED/NONE/run 0. The exact unclassified file remains `PRESERVE_NO_RECLAIMER_SELECTED`; neither slot becomes FREE. |
| 8 | Floor 0 with earlier SEALING/UNKNOWN/run 1 and later RETIRED/NONE/run 0; unknown prefix blocks floor advancement. |
| 9 | Separate synthetic sequence-exhaustion registry retains `9223372036854775807`; ordinary call-cap registry remains empty. |
| 10 | Synthetic DB close failure still attempts lock close and preserves the original error; no registry/actor closure is invented. |
| 11 | Real INCOMPLETE/UNKNOWN/run 1 persists after reopen. Negative exact-type attachment, both synthetic close attempts and original-exception preservation pass. |
| 12 | Real RETIRING/RESERVED/run 1 persists. Grant/wake assertions, exact monitor scheduling branch, late-start phase refusal and retirement-closure refusal pass. |

No retained record in any case has a `closure_sha256`. No case creates a real
workspace or location-state directory. RESERVED in final case 12 is intentional:
resource-only teardown does not claim to close its synthetic actor or reopen
the registry; a later real reopen would conservatively convert that saved state
to UNKNOWN. It is not evidence of successful CLOSED-run recovery.

Cases 11 and 12 genuinely execute the selected Python control-flow branches,
but their resource/service/scheduler stand-ins remain synthetic. Case 11 enters
the real rejected-attachment branch and requires the provisional service/locator
close attempts despite the injected service-close exception. Case 12 invokes
the exact installed monitor coroutine on an unopened class shell, captures one
mocked scheduling attempt and closes the captured coroutine without running
real service cleanup. Its late `_started` call now refuses before touching
shell internals and cannot overwrite RETIRING. Neither case runs an event loop,
real task, service listener, Node or positive `_closed_run` acceptance.

Time bounds, crash phases, marker failure and MAX_SEQUENCE are controlled test
inputs, not real synchronized UTC, killed-process recovery or huge historical
workloads. The genuine zero-run retirement cases do not owe actor closure;
they must not be generalized to an UNKNOWN previously started generation.

No forbidden process/socket/Python deletion entrypoint was called. The result
records zero actual network/Node/native/proof/verifier calls and zero explicit
reclamation deletions, consistent with the reviewed source and guards. SQLite
native rollback-journal operations are explicitly not counted as Python unlinks
or reclamation. Mathematical acceptance, real-service composition, positive
actor closure, reclamation and physical-envelope adoption all remain false.

## Closure, charges and limits

Outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0, direct child
reaped, Job closed, no cleanup errors or termination request. Final Job has
two total processes, active 0 and terminated 0. The ordinary stderr test log
is within its cap; there is no unexpected stdout.

Inclusive Job CPU is 1.15625 s (0.65625 user + 0.5 kernel). Whole-wrapper CPU is
0.3125 s, giving **1.46875 known CPU seconds**. The 0.015625 supervision CPU is
nested inside the wrapper figure and is not added again. Whole wall time is
1.995652999728918 s; command-through-cleanup wall is 1.9392731999978423 s.
Peak Job private commit is 42143744 B / 40.19140625 MiB. These fit the original
60 CPU / 120 wall seconds / 384 MiB / two-process allocation. No timing retry,
new allocation, native work or repeated old suite was performed.

All used source/selector/selection/evidence bytes are now frozen. This audit
does not qualify the separately proposed reclaimer, actual sustained slot
recycling, real closed-service retirement/reopen, independent-host operation,
physical disk bounds or final v5. The reviewer performed only source/hash/JSON,
AST tuple extraction and read-only immutable SQLite inspection; no product
imports, test rerun, network, deletion, installation change or Git operation.
Root owns adoption of this scoped actual pass.
