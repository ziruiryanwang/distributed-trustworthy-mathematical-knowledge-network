# Next local proof decision: one fixed po17 route, not a cap ladder

2026-10-17. Owner: `v5_growth_decision`. Source/theory and saved-data analysis
only. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The workspace guard passed. No product import, build, execution, proof, profile
mutation, allowance, Git operation or new machine observation was performed.
Root owns selection; this is a recommendation for independent challenge.

## Decision

**Select the source design for a fixed po17/N512 successor, beginning with one
fresh execution-only layout of the unchanged A/H2 mathematical target.** Reuse
the corrected backend libraries already compiled. If the layout succeeds and
the new host/adoption path is reviewed, the first expensive discriminator is
exactly one genuine maximum-po17 segment under a 2 GiB worker cap, conditional
on a contemporaneous 1 GiB physical AND commit headroom margin. It is not a
full-path funding decision, a peak upper-bound claim or permission to raise caps
after failure.

This is preferable now to waiting indefinitely, redoing the circuit memory
census, trying the same po18 job at several caps, or changing the mathematical
guest. Natural availability of at least 5 GiB physical AND commit headroom could
make the already reviewed 4 GiB po18 one-segment route cheaper; that is a
conditional alternative, not a reason to poll or terminate the user's apps.
No such headroom has been demonstrated by the latest observation.

The local proof route is **not conclusively impossible**. It is presently
unqualified. Smaller geometry creates a principled, bounded way to resolve a
material uncertainty. The full deployable-v5 goal remains unchanged.

## Evidence that must not be repeated or relabeled

- Exact A remains `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`.
- Selected H2 contains BASE and FIRST; it has the same exact J_FIRST target as
  the integrated terminal-to-extension workflow. Its header SHA-256 is
  `49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e`.
  The exact wire is 113,849 bytes, SHA-256
  `898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500`.
- The complete selected-frontier po18 capsule has 167 segments and one genuine
  I premise, 32,965,324 bytes, SHA-256
  `6e41621e2595c252328eaf5f34862c6d6f913caecb68117406bcd616a61b44a5`.
  Reading its saved diagnostic confirms **all 167 segments are po18**. There is
  no naturally small last segment available as a cheap existing-capsule probe.
- Its execution records 43,778,048 padded rows and 4,205,234 padding rows.
  These are not proof work or a po17 execution bound. The earlier old full
  three-member po18 failure at 256 segments remains failed, not a complete
  capsule or a valid prefix to promote into this different session.
- Corrected five-step build `prover-allocation-build-01` completed and was
  independently audited. Result SHA-256 is
  `ac259e9db55275a0a8404e9cf881fd3779f2e7259ccfe134c8e93e3b180b4102`.
  New stage executable SHA-256 is
  `263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c`.
  It was not invoked. Known compilation cost is 348.875 CPU seconds, not proof
  cost; the five-step build must not be rerun merely to change two host constants.
- Root's latest supplied observation is 3,768,412 KiB available physical and
  3,505,344 KiB WMI free-virtual memory. The latter is **not adopted as an exact
  available-commit measurement**. It neither supplies a reservation nor clears
  a 4 GiB worker. The established PerfInfo-style measurement, not a relabeled WMI
  number, belongs in any immediate launch check.

Reuse [LOCAL-MEMORY-DECISION](LOCAL-MEMORY-DECISION.md),
[SMALL-LAYOUT-FEASIBILITY](SMALL-LAYOUT-FEASIBILITY.md),
[SMALL-SEGMENT-DESIGN](../v5-2026-10-16/SMALL-SEGMENT-DESIGN.md) and
[FULL-PATH-FEASIBILITY-REVIEW](../v5-2026-10-16/FULL-PATH-FEASIBILITY-REVIEW.md).
Their historical selections are not new launch authority.

## Supported geometry and unchanged cryptographic acceptance

Here `SDK` denotes
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8`.
The relevant exact source facts are:

| Boundary | Retained source fact |
|---|---|
| Public execution setting | `risc0/zkvm/src/host/client/env.rs:173-186` documents `segment_limit_po2`; `risc0/zkp/src/lib.rs:36-39` defines supported public bounds 13 through 24. Po17 is interior, not an unsupported undersized trace. |
| Lift geometry | `risc0/circuit/recursion/src/lib.rs:47` gives `LIFT_PO2_RANGE=12..=24`. `control_id.rs:85` includes `lift_rv32im_m3_17.zkr` in the Poseidon2 table. The difference between minimum lift12 and minimum public execution13 is real; neither is a reason to change the chosen17. |
| Lift selection | `zkvm/src/host/recursion/prove/mod.rs:620-639` decodes the actual seal's po2; `prove/zkr.rs:47-62` selects that exact lift program and control ID. Do not relabel a po18 seal as po17. |
| Allowed receipt controls | `zkvm/src/receipt/succinct.rs:274-311` includes lifts from12 through the selected maximum. `receipt.rs:881` sets the default maximum22. Thus the unchanged default control root already includes17. |
| Recursive proving geometry | `zkvm/src/host/recursion/prove/mod.rs:57` fixes `RECURSION_PO2=18`; `prove/zkr.rs:34,54` uses it for recursion programs. RV32IM po17 does **not** halve lift/join/resolve memory. |
| Actual chosen finish | `software/v5/aggregate_small/stage_host.rs:515-539` checks the full composite, the exact successful claim and unchanged `verify_aggregate`; no extra shrink/Groth16 conversion is used by this path. |

**Change execution geometry, not the allowed-control root.** Retain
`ProverOpts::succinct().with_dev_mode(false).with_prove_guest_errors(false)` and
the adopted verification context. In particular, do not add
`with_max_segment_po2(17)` as an optimization: changing the allowed set/root is
a different trust/configuration change and can break compatibility with the
already genuine I premise. Lowering the execution setting needs no such change.

The final receiver still checks the same predicate `Accept(A,H2,R)`: a genuine
succinct Poseidon2 receipt, exact journal H2, exact adopted image/policy/context,
successful execution and no unresolved assumptions. Its soundness assumptions,
checker correspondence and permitted foundation are unchanged. New execution
and checkpoint identities do not create new mathematical authority.

### Fresh execution is required

The retained public `ExecutorImpl` constructs from an image or ELF and exposes
`run`/`run_with_callback`. Its per-segment stepping is `pub(crate)`
(`zkvm/src/host/server/exec/executor.rs:225-352`). The retained `Segment`
interface exposes its geometry/info and stored execution witness, not a public
completed-capsule resegmentation operation (`host/server/session.rs:119-145`).
No supported high-level API to turn this completed po18 capsule into a new
complete po17 session was identified. Do not invent one from private splitting
machinery or edit the old segment metadata.

The narrow supported route is **one fresh execution** from the same ELF, wire,
H2 and ordered genuine parent receipt. The session binding includes po2; the
capsule binding includes the resulting segment vector. Therefore both must
change even when the mathematical output is identical. Save fresh evidence and
charge execution cost. The old capsule remains usable in its old lineage.

## Why 2 GiB is a reasonable bounded discriminator, not a guarantee

The corrected po18 identified simultaneous requested-payload lower bound is
2,331.8466796875 MiB. It is not a peak upper bound. Using the same already
derived source accounting at N=131,072, including the selected ABI's two
row-metadata arrays, gives the po17 lower bound

`[24(198+84)+4292-1836+16]N + 81(N+N/16+N/256) + 263680`

`= 1,222,690,816 bytes = 1,166.048828125 MiB`.

The FRI terminal copy is512 bytes here rather than1024 at po18: its three
retained round degrees are N, N/16, N/256 and terminal degree32. This is why
the fixed constant differs. D>=198 and A>=84 remain minima, not equalities.
The corrected auxiliary-vector saving at po17 is229.5 MiB. No repeated
43-block template census was needed to obtain this geometry comparison.

A 2 GiB cap leaves about881.951 MiB above those identified minimum payloads.
The SDK explicitly describes roughly linear segment-memory scaling. The
retained uncorrected base-I po18 peak of3,371 MiB is additional practical
context. Neither fact proves that the decoded larger capsule, real D/A,
preflight, verifier/transcript overlap, threads and allocator fit that margin.
Do not halve the historical process peak and call it a theorem.

The experiment is justified as a **contained answer to that remaining question**:
its allowed allocation is below contemporaneously available capacity with the
explicit margin, it uses a materially smaller trace, and first refusal stops.
2 GiB is a fixed selected candidate, not the first rung of a2/2.5/3/4 GiB retry
ladder. One maximum-po17 segment success would establish only that segment on
that exact build and host state. It would not establish every stage's peak.

### Recursion: retained practical evidence and the remaining gap

Read-only extraction from all108 lift and108 join stage reports in the already
audited `experiments/v5-local-checks/module-base-production-01` gives:

| Kind | Highest saved Job private commit | MiB | Exact stage result SHA-256 |
|---|---:|---:|---|
| Lift |1,549,381,632|1,477.60546875|`lift-99/RESULT.json`: `c58c17a49893bd06e410b6eae58b5c5c7f5a0b167e5c90023d452e4bdc5bcc7e`|
| Join |1,585,057,792|1,511.62890625|`join-104/RESULT.json`: `07c89c8c6dc86ddeefa54f8059e34366472cba64c76754a8884b8a00b8ef2e5c`|

These are exact historical maxima in that retained sample, not guarantees for
the aggregate host, its larger capsule or the different lift17 program. The
unchanged recursion backend and approximately536 MiB margin above the larger
observation make a later bounded recursion prefix plausible, not qualified.
No genuine same-backend resolve memory qualification was identified; the base
session has zero assumptions. **Resolve and complete finish remain gates.**
A segment-only pass must not be advertised as complete-lane feasibility.

Do not run unrelated recursion benchmarks now. If segment0 succeeds and root
selects a next prefix, the actual first lift/next segment/lift/join supplies
useful new pipeline evidence. Resolve should consume the actual joined claim
and genuine I premise when that chain exists. Any separate earlier resolve
discriminator needs its own genuine compatible conditional claim and justification.

## Count and work: what smaller segments cost

Keep the current hard session row ceiling2^26 and choose exactly po17 with
N512/M8. The same nominal ceiling permits at most512 full-size po17 segments;
successful termination within it is **not proved**. Any refusal ends this layout
operation. Do not automatically raise the row ceiling, N, capsule cap or retry
at po16.

The SDK's threshold is `2^p-25000`: 237,144 at18 and106,072 at17. In a toy model
with unchanged intrinsic rows and no repeated paging/table work, the segment
count ratio is237144/106072 ~=2.235689 and total padded-row ratio~=1.117844.
This explains the tradeoff; it is **not an estimate with a proved error bound**.
The saved po19/po18 comparison already demonstrates repeated nonpadding work.
Do not extrapolate a guaranteed334 or374 segments from the retained167.

For actual segment count s and assumptions m, the unchanged ordered graph has

`H=3s+m` host calls, `Q=H-1` proof checkpoints:

`s segment + s lift + (s-1) join + m resolve + 1 finish`.

At512/8, H=1544 and Q=1543. Actual H2 still has m=1, so its maximum is1537 calls
and1536 checkpoints. The format maximum does not fund this work.

## Coupled finite envelopes, not one changed constant

The following are design bounds, conditional on successful admission of each
actual artifact. They are not measured output sizes, runtime budgets or
automatic larger allowances. Keep safe refusal when the actual layout/records
do not fit. In particular, obtain actual s before choosing full-path work.

| Boundary | Recommended design consequence |
|---|---|
| Geometry/count | Fresh po17/N512; M8, same2^26 row ceiling. Update snapshot, stage decoder, graph, stage keys, request/adoption and lifecycle bindings together. |
| Capsule/segment retention | Keep96 MiB capsule and96 MiB retained-segment sum initially. N512 does not mathematically force a larger capsule bound. A real overflow is refusal, not permission to truncate or enlarge. |
| Snapshot custody | Keep208 MiB bytes; allow at most544 entries (512 segments plus32 diagnostic/control margin). Enforce actual census. No `P.file_pin`128 MiB relaxation is needed for a96 MiB capsule. |
| Artifact | Keep512 KiB per checkpoint/final receipt and1 MiB per parent. Larger valid outputs safely refuse. |
| Full composite | If retaining the existing defense-in-depth finish, use a dedicated288 MiB limit, not old160 MiB. At maximum, `512*(524288-71)+8*1048576+48 =276787760 bytes <288 MiB`. This is serialized length, not decoded peak memory. |
| Native total read | Keep512 MiB. With the current noncapsule20 MiB fixed-input envelope, capsule96 MiB,513 half-MiB dependencies and256 KiB manifest, maximum relevant host envelope is372.75 MiB. |
| Controller active inventory | Separate it from native read limit;1 GiB is a sufficient finite bound for `20+96+1543/2+8=895.5 MiB` of fixed inputs, capsule, all checkpoint artifacts and prior reports. Keep administrative accounting separate. Do not silently change native `READ_LIMIT` alongside this controller-only change. |
| Manifest | At most513 dependency rows.256 KiB can remain if the actual chosen paths/rows pass the encoded-size bound; supported longer Unicode paths can safely refuse. For prospective selected rows <=400 encoded bytes,513 rows plus1 KiB header use206224 bytes. No claim that every512-UTF16-unit path fits. |
| Command line | Existing dependency-manifest transport already removes checkpoint argv fanout. Preserve actual32767-UTF16-unit command-line check; no old argv mechanism needs redesign. |
| Per-attempt administrative/report limits | Keep128 MiB administrative limit,64 KiB individual admin records,1 MiB report and8 MiB prior-report total when using batches of at most256 host calls and prospectively bounded encoded rows. See calculation below. Larger unsupported records refuse. |
| Source/build input adoption | Pin the new host/build/adapter/source closure and actual refined libraries. Reuse old checker/guest/native-circuit identities. Source count, profile bytes, fixed-input20 MiB and installation512 MiB checks must pass actual maps; no synthetic records or old build-schema impersonation. |

The native372.75 MiB bound uses the existing fixed-session-envelope admission,
which is an operational restriction. It does not assert that arbitrary maximal
image/wire/eight-parent sizes simultaneously fit20 MiB. The actual selected H2
files must pass that unchanged restriction.

### Full graph quote and bounded batching

With current selected per-stage ceilings1200/250/250/600/300 CPU seconds and
240/150/150/600/120 wall seconds, the conservative graph quotes are

`CPU=1700s+600m+50`, `wall=540s+600m-30`.

At512/8 these are875250 worker-CPU seconds and281250 summed stage-wall seconds.
For H2 at512/1, they are871050 CPU and277050 wall seconds. These deliberately
loose cap sums are not expected durations. They show that a universal N512
full-path reservation does **not** fit the old500000-CPU/172800-wall maxima.
Do not enlarge full funding before the actual layout and first proof evidence.

The current reserve per host stage is
`0.5+0.0625+0.0625+2+0.25=2.875 MiB` and9 entries. A finite maximum-graph
schedule `1 + 6*256 + 7 =1544` calls uses8 attempts, within the existing
16-prior-attempt limit. Its conservative reserve is4471 MiB/13928 entries,
including4 MiB/four entries per attempt. Thus old2304 MiB/8192-entry maxima
cannot promise the entire worst-case path. An explicitly selected full-path
ceiling of4608 MiB/16384 entries would cover this arithmetic, but is **not
selected here**. Actual smaller-s quotes may require less. Failed output and
all earlier preparation remain charged.

For <=256 calls/attempt, even two64 KiB admin records per stage plus per-kind
2/4/6/4/256 KiB manifests stay comfortably below128 MiB. The256 KiB finish
manifest is a once-per-attempt maximum, not a repeated256 KiB actual record.
Admin limits therefore need not be doubled solely because lifetime H doubled.

For the eight-attempt maximum schedule, cumulative inventory counts sum6927.
If each selected encoded pin/checkpoint row is<=400 bytes and each fixed report
remainder is<=32 KiB, all eight successful reports together are bounded by
`(6927+1544+36+16)*400+8*32768 <3.502 MiB`. A single report has at most1543
inventory rows,256 stage pins,7 prior pins and2 controls, hence remains below
1 MiB under the same bounds. This is a prospective chosen-path bound to check,
not evidence that arbitrary failure text/paths meet it. Keep terminal refusal
if actual serialization exceeds the recorded limits.

The existing repeated rehash/census still has O(H^2) artifact-control work.
At maximum N512 it is worse, not a scalability improvement. Controller CPU
must be separately quoted and metered; a larger byte envelope does not provide
CPU time or memory. Do not add an unrelated caching rewrite before the layout
or claim po17 improves end-to-end growth merely because it lowers peak payload.

## Fastest safe source/build frontier

Prefer a fresh, explicitly named successor package; do not edit used
`aggregate_small`, `aggregate_lifecycle`, `prover_memory` or their evidence.
Root should assign exact new names/owners. Minimize irreversible work in this order:

1. **Snapshot source first.** Successor of `aggregate_small/aggregate_host.rs`:
   only fixed17, N512, fresh result/domain identification and matching count
   bounds. Keep receipt verification, A/ELF/header/wire/parent binding and
   capsule encoding intact. Pair with a fresh selected-target snapshot adapter
   using the existing generic preparation rather than hardcoded fixture
   impersonation. Selected H2 is data, not a new guest.
2. **One snapshot-host link**, separately selected after review, reusing the
   four corrected backend/relation Rust outputs from the successful allocation
   build and the unchanged native circuit/static inputs. No Cargo, backend,
   relation, guest or checker rebuild. Adapt the exact recipe to the fresh host
   source/output and explicit new-library edges; retain build provenance.
3. **One execution-only layout**, if separately selected. Same ELF/wire/H2/I,
   fixed17/512/2^26/96 MiB; retain per-segment rows, bytes, final successful
   claim and new session/capsule bindings. Failure stops this route. This is
   the first genuinely decision-changing runtime; it should precede building
   unused full proof orchestration.
4. **Stage/controller successor only after a useful complete layout.** Copy the
   current native manifest/complete-composite path with fixed17/count512 and
   dedicated288 MiB composite bound. Preserve all pure/native binding and
   recursion checks. Controller uses actual s, the separated1 GiB inventory
   ceiling, count/quote rules above and bounded batch sizes; lifecycle/adoption
   explicitly recognizes the new snapshot/build schemas and sources.
5. **One stage-host link** to the already corrected libraries, with fresh build
   evidence. This is not another five-step allocation rebuild. The existing
   `prover_memory.adoption` deliberately expects its exact five-step build and
   executable; do not forge that schema for a single-link successor. A new
   small adoption boundary must bind the reviewed refined dependency build
   and the new exact link, source map, runtime map and executable.
6. **One focused changed-boundary control selection**, covering17/512 count
   boundaries, exact new snapshot/adoption identities, composite/read envelope
   split, malformed/oversized manifests and no-valid-receipt-on-refusal. Reuse
   already passing unchanged transport/checker tests; do not repeat campaigns.
   A genuine no-host preflight must pass actual profile/source/input maps.
7. **Only then one genuine segment**, not a whole proof campaign. Require the
   selected first segment actually has maximum po17 geometry. With the current
   ordered graph, `stage_limit=1` then means precisely segment0. If segment0 is
   smaller, do not call it maximum-po17 evidence or silently dispatch later
   stages; root must select an explicit supported maximum-segment discriminator.

The snapshot and stage links may share one reviewed source build recipe, but
they remain distinct selected operations. Do not compile the later stage host
before the layout supplies useful actual data merely because parallel slots
are available. Parallelize independent source/review work; serialize heavy
local jobs under the headroom policy.

### Proposed first-proof admission/stopping conditions

- Exact independently reviewed source/build/profile/snapshot pins and actual
  complete new capsule; non-dev verifier and original allowed-control root.
- One selected segment stage;2 GiB Job memory, existing1200 CPU/240 wall stage
  ceiling as a maximum candidate, separately bounded controller/tail/output.
  A smaller actual quote may be chosen; no increase follows from refusal.
- Immediately before launch: at least3 GiB available physical and3 GiB
  available commit measured by the established mechanism, plus no heavy project
  overlap. The1 GiB margin covers controller and unrelated activity; it is a
  launch rule, not an OS reservation or promise against later interference.
- Exact new allowance/attempt; carry all preparation, old failed work and the
 348.875 CPU-second corrected build. No implicit funding of H remaining stages.
- First failure, cap exhaustion, closure uncertainty or binding mismatch stops.
  Keep failed evidence. A successful checkpoint remains an untrusted artifact
  requiring its ordinary cryptographic consumption; it is not A/H2 admission.
- After success, compare actual segment cost/peak and actual graph quote before
  selecting the next genuine recursion prefix or full chain. Any later budget
  must explicitly preserve prior success/cost lineage; do not increase a
  same-allowance budget that the existing continuation equality forbids.

## Full-cost and architectural consequences

Po17 is a **local producer feasibility profile**, not a new default for every
network participant. The scalable receiver still receives a succinct final
receipt and selected semantic interfaces without replaying this producer's
ancestral proof history. Producer effort and receiving efficiency are different
cost centers; neither can be hidden inside the other.

Smaller geometry adds execution boundaries, lifts, joins, capsule reads,
process launches and current quadratic controller work. The useful-growth
inequality must charge all of them, along with refinement builds/layouts and
failed search/preparation. Holding receiver benefit fixed, larger certification
cost raises the reuse count required to amortize publication. One certificate
would remove a central implementation blocker but would not prove net useful
growth or final global deployability.

Preserve complete-composite verification for this first geometry successor.
The existing source argument permits a separately selected frontier-only finish
under unchanged recursive-soundness assumptions, but removing it neither fixes
segment memory nor warrants combining two assurance changes prematurely.

If the fixed po17 layout or2 GiB genuine stage fails, do not spend the rest of
the day sweeping caps or exponents. The **ordinary terminal staged-acquisition
integration source is already finished**, independently reviewed (`4ec3db28`)
and committed (`cba2e78`), with its100-source closure checked. This status update
from root supersedes the earlier pending-source description. Do not assign
that completed work again or repeat its controls.

The highest-payoff unfinished integrated endpoint is the genuine runtime path:
demand-only acquisition, actual A admission/import, substantive SECOND
authoring, publication/custody, and the strong local comparator with full-cost
accounting. Its A dependency is real; fake admission or native-only reuse is
not a substitute. This review has not conclusively blocked all local proof
production, so it does not invent another peripheral source task as a fallback.
A failed fixed17 discriminator must instead trigger a distinct, evidence-based
producer decision: identify whether execution count, capsule/host retention,
RV32IM proof state, fixed recursion or accounting is the actual blocker before
selecting the smallest relevant change. Preserve the already integrated client
for the eventual actual receipt; no repeated stale census follows.

## What this checkpoint resolves

It selects a principled next **design**, establishes SDK/receipt compatibility,
isolates the fresh-execution requirement, identifies the finite N512 coupling
and retained recursion evidence, and supplies an economical stopping sequence.
It does not claim a new host, capsule, checkpoint, A receipt, runtime pass,
full-cost advantage or v5 release. Independent review and root selection are
the next authorities; the preserved artifacts remain unchanged.
