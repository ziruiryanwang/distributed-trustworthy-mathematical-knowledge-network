# Five-layer scenario shape: source and exact-launch review

**PASS for the reviewed source cut and the exact launch identified below.** No unresolved pre-execution blocker was found after the corrections below. This is not execution success or authorization to retry the failed native allocation. Root alone executes. The reviewer performed no import, compilation, Python/Lean execution, SQLite query, or source edit.

The complete adapter, worker, driver, proposal, and legacy diagnostic helper were read, including the legacy helper's top-level dependencies. Revised driver code and final worker pin/origin indices were rechecked. The original `run_stage`, `supervise`, and `domains` interfaces were checked against their previously reviewed sources.

## Reviewed pins

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `software/tests/scenario_profile.py` | 4619 | `b8b3e1b1c1485de80ae9fb2371c32771a4f8505fc90d580e021442f227fbcf6a` |
| `software/tests/scenario_shape_worker.py` | 10412 | `650197fda0718df011178c8a2a4b83ee9f9daed747c49587f659480c33fb9dc0` |
| `software/tests/run_scenario_shape.py` | 13090 | `50ed8212fba3529b8b8ce78a96491a69ed8b8b6a3c1fb3bb8c7b643370db888b` |
| `software/drafts/SCENARIO-PROFILE.md` | 6570 | `6b2603778c6a2db161ace3f9b5ac5423bb8b76ca81eb72ab534df7627ab81b48` |
| `experiments/lean-operation-integration/lifecycle_node_02.py` | 8951 | `e7eb8a078c5f0521da2686a99d9f7dc9cebb04cd8b0a215fe0da1cd52db38901` |

Required input order is Python, driver, worker, profile, original `run_stage`, original `supervise`, legacy diagnostic helper, original `domains`; the launch itself is an additional supervisor pin. Final worker `CODE[6]` is `domains`, and `run_stage.domain_module is domains` plus exact origin checks bind that transitive dependency. The legacy import defines its own old CLI but does not execute it; this control invokes only its bounded Job-local PID/image diagnostic.

## Principal checks

- The adapter requires explicit sixteen, constructs a base Job while empty, verifies original CPU/memory/flags, changes only `ActiveProcessLimit`, reads back every declared extended-limit field, and rechecks that no process has been assigned. It neither patches imported classes/globals nor changes installed product profiles. The Transport's temporary eight is only a local constructor-validation argument; construction launches nothing.
- The fixed chain is worker → wrapper → node stand-in → runner stand-in → leaf. Wrapper and runner create unchanged requested-eight/requested-one Jobs around their children, with suspended assignment/resume. All five application processes remain held until membership evidence is recorded.
- Each request-bound child-written barrier contains its actual PID and checks its OS parent. Coordinator validation requires five distinct PIDs, the outer supervisor's direct PID, matching launched-child records, exact commands/flags/cwd, and the proper parent chain. Bounded Job queries require the expected application PIDs and their Python image paths in the outer/public/leaf Jobs, with limit readbacks 16/8/1.
- The wrapper belongs to the outer Job, not the public child Job; its NULL-handle query is deliberately for its current containing Job. Public and outer observations must fit their aggregate bounds. Auxiliary PIDs are recorded separately; neither exactly ten total PIDs nor a one-PID observed leaf maximum is required. Auxiliary image lookup failures remain explicit data, not guessed identities.
- Normal completion requires exact response/event/shape binding, successful direct-child waits, local zero-active counts/Job closure, and outer quiescence. Timeout requires all request-bound shape evidence first, no release/event, the specific `PUBLIC_WALL_LIMIT`, requested whole-tree termination, and outer reaping/zero-active/closure. An arbitrary failure is not accepted as timeout success.

No checker, native compiler, package reader, or database is invoked. This is a process-shape stand-in, not the real native workload or a hostile-code sandbox. It cannot establish an exact universal maximum for auxiliary OS processes or qualify a subsequent native run by itself.

## Finite allocation and failure evidence

The source fixes two sequential calls. Per call: 15 Job CPU seconds, 512 MiB, requested outer sixteen, 64-KiB output/event bounds, 1024-byte request bound; normal wall allowance 20 seconds and intended timeout 8 seconds. Aggregate allowance is 40 measured seconds and 30 outer-Job CPU seconds. Local public/leaf Jobs request 30 CPU seconds and 256 MiB but remain enclosed by the smaller outer CPU grant. PID buffers hold at most 16 entries and image buffers 2048 characters. Barriers/reports are exclusively and atomically published with 64-KiB bounds.

Count each disjoint outer Job's CPU once, never add nested observations again. Coordinator CPU is measured separately; startup and final persistence remain excluded. Census requires every started tree to be quiescent and reserves space for final records within 8 MiB / 128 files / 256 entries. These are endpoint/polling checks, not hard transient disk or exact auxiliary-PID bounds.

Two source-review defects were repaired: available CPU/cleanup facts now enter the result **before** observation-copy persistence can fail, and child-directory setup now occurs inside post-allocation failure handling. The separate `domains` pin and origin/identity checks are present in the final cut. Missing final observations remain unknown rather than zero; failure prefixes and files are preserved.

The strongest planned outcome is `PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`. The exact-launch check is recorded below. After execution, independently audit both PID/barrier/command chains, observed memberships, exact normal/timeout predicates, actual CPU/cleanup, retained hashes, and the claim boundary. Frozen native-01 data and sources must remain unchanged.

## Exact-launch addendum

Read and checked `software/qualification/scenario-shape-launch-01.json`: **2287 bytes**, SHA-256 **`0bb71cd5f58e6db641708472a1afdefcdb0a7c1f20c5bf2a00d97b5d38663a1e`**. All eight ordered input pins match actual paths, lengths, and hashes (193,105 bytes combined); the immutable launch is the ninth supervisor pin. Schema/field set, two-call allocation, exact limits, 8-MiB/128-file/256-entry retained bounds, and zero-native scope agree with the reviewed worker constants. No input or bound was silently substituted.

`software/qualification/scenario-shape-01` remained absent at this check, with no reparse point in its existing parent ancestry. **No remaining blocker for this exact prospective native-free launch was found.** Actual normal completion, intended timeout, process membership, cleanup, and cost remain unobserved until root executes and the outcome is separately audited.
