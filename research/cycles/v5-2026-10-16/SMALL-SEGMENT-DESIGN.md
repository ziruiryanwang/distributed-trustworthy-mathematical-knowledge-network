# Smaller aggregate segments: exact orchestration change map

Status: **SOURCE-ONLY ALTERNATIVE; NOT SELECTED OR FUNDED**. No implementation,
import, build, native call, guest execution, proof or Git operation was performed.
Owner: `memo_tests_review`; root chooses the route. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision in brief

The same memoA guest can in principle be executed with po18 or po17 without
changing its mathematical relation, image ID, expected journal or genuine I
premise. It cannot reuse the **po19 execution capsule** as if its segments were
smaller. Segment boundaries, memory commitments, indices and capsule bytes change;
po2 is explicitly included in the session binding. A smaller-geometry run would
therefore need a fresh finite execution selection and a new capsule, while the
successful 113-segment po19 capsule remains preserved.

This is a larger change than merely raising `SEGMENT_LIMIT`: the current
orchestrator, internal composite serializer, command transport, aggregate
resource ceilings and continuation accounting have coupled limits. Prefer an
actually provisioned, independently bounded higher-memory producer if it can
use the retained capsule unchanged. That choice does not follow merely from
raising a configured cap; root must establish actual provisioned capacity.

## Semantics preserved, and what does not follow

Snapshot host `aggregate_host/aggregate_host.rs:267` binds exact ELF, A, I/F/P,
wire/header hashes, selected cycles/po2 and ordered parent hashes. Stage host
`aggregate_production/stage_host.rs:271` reconstructs that same binding. Changing
po2 is therefore a fresh execution identity, not a new mathematical identity.
The final predicate remains verification of a real, fully resolved receipt for
the same adopted A and exact 192-byte journal, with dev mode disabled.

The SDK execution splitter uses threshold `2^po2 - 25,000` at both po18 and po17,
not a constant fractional occupancy. See the retained SDK
`risc0/circuit/rv32im/src/execute/executor.rs:196`, `:442`, `:512`, `:633`, `:956`
and `risc0/circuit/rv32im/src/lib.rs:46` below
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/`.
Completed segment padding, paging/split overhead and the final segment change.
Thus **226 or 452 segments are illustrations, not count theorems** obtained by
doubling/quadrupling113. The retained 59,244,544 padded rows do not establish
that a fresh smaller layout finishes under the same `2^26` row cap. Oversized
instructions can also refuse; the existing cap cannot be assumed sufficient.

Independent memory work belongs to `AGGREGATE-FUNDING-DECISION.md` and its review;
this note does not duplicate it. Halving a memory lower bound does not prove
that total memory fits. Historical successful po18 base-I stages are relevant
implementation context, not a proof that this A workload fits.

## Count/index source map

Let N be a selected maximum segment count and M=8 the unchanged assumption cap.
For actual s<=N and m<=M, the current linear proof DAG has:

\[
H(s,m)=3s+m,\qquad Q(s,m)=H-1=3s+m-1.
\]

H counts host calls including one finish; Q counts proof stages/checkpoints.
There are s segments, s lifts, s-1 joins, m resolutions, one finish. Finish
requires all s segment receipts **and** the resolved prefix; retaining only the
prefix would weaken the selected validation workflow.

| Current source boundary | Current value | Fresh N=256 envelope | Fresh N=512 envelope |
|---|---:|---:|---:|
| Snapshot `SEGMENT_LIMIT`, `aggregate_host.rs:26` |128|256|512|
| Stage decoder/argument bound, `stage_host.rs:25,66,235,285` |128|256|512|
| `production.producer.stage_key`, `producer.py:98` max index |127|255|511|
| `production.producer.graph`, `producer.py:103` max segments |128|256|512|
| Aggregate request/prior inventory, `aggregate_production/producer.py:328,387` |391|775|1543|
| Aggregate request stage limit, `:336` |392|776|1544|
| Snapshot adapter result count, `capability_snapshot.py:147` |128|256|512|
| Snapshot adapter final entry cap, `:166` |160|N+32 prospective reserve|N+32 prospective reserve|

N=256/512 here are concrete **bounded alternatives**, not promises of complete
execution at po18/17. The exact selected count cap must be checked against the
future row/custody allocation; reaching it is a stop, not automatic expansion.
The N+32 entry allowance preserves the old cap's nominal32-entry margin;
it is a proposed reserve, not a measured future file count.

The old `production/producer.py` is used/frozen. Do not edit it or monkey-patch
its globals. The minimal fresh aggregate successor owns its bounded
`stage_key/graph/missing_plan` helpers and its checkpoint parser calls the new
stage-key helper. Keep the existing graph order and exact dependency checks.
The old support constructor may still supply pinned supervisor/Job functions.
The recursive missing-plan walk is O(N) deep; N=512 is below the usual Python
recursion ceiling but still needs an explicitly bounded-depth implementation or
preflight, not an unbounded future N extension.

## Byte and command boundaries that count widening alone misses

| Boundary | Exact current constraint | Consequence for a smaller-layout successor |
|---|---|---|
| Snapshot retained segment sum |64MiB, `aggregate_host.rs:139`|A new layout duplicates state/page records differently. Do not infer its size from the37,187,089-byte po19 capsule. If widened, change sum and capsule serialization bounds together, with an explicit fresh custody budget.|
| Snapshot capsule encode/read |64MiB, host `:22,103,303`, adapter `:148`, stage `:22,276`, controller `:310`|All corresponding snapshot/decoder/input bounds must agree. `P.file_pin` independently caps individual files at128MiB; exceeding that needs another fresh helper, not an unnoticed parser bypass.|
| Snapshot output bytes |144MiB, adapter `:166`|Both individual segment files and the combined capsule are retained. Budget at least selected segment-sum cap + capsule cap + diagnostics/control reserve. For64+64, current144MiB is the existing envelope; for128+128, a272MiB envelope would preserve the16MiB margin, subject to exact selection.|
| Per-stage total input |512MiB, stage `READ_LIMIT`, controller `:397,512`|Finish includes all segment checkpoints; controller continuation separately includes **all** retained checkpoints, reports and selected snapshot evidence. These are different sums.|
| Internal composite assembly |64MiB via common `encode/decode`, stage `:316`|Finish serializes the complete CompositeReceipt before verifying it. A small final succinct receipt does not remove this internal bound. At512KiB/segment,226 nominal segments reserve113MiB before assumptions/metadata.|
| Command-line transport |One argv element per checkpoint, controller `stage_argv`, stage `:298`|Windows CreateProcess command line is limited to32,767 UTF-16 code units including terminator. Increasing Rust's argument-count check does not increase the OS limit.|

A representative **hypothetical**, uncreated output root
`experiments/v5-local-checks/aggregate-production-po18-01` under the canonical
root would yield **33,030 characters for the quoted dependency paths alone** at
s=226, before executable, image, capsule and other arguments. At s=452 this is
66,026. These ASCII path counts include quotes/spaces; no program was executed.
Shorter owner-chosen paths might fit some finite case, but do not solve a robust
N=512 interface. A separately bounded/pinned checkpoint-list operand is the
minimal prospective transport seam; it must retain exact ordered dependencies,
ordinary-path and total-read checks. No manifest decoder is designed or selected
here. Likewise, a separately bounded internal composite buffer can preserve the
SDK's unchanged composite verification, but its extra live memory must be charged.
Removing that verification or trusting the capsule is not an acceptable fix.

## Aggregate cost/continuation bounds

With per-stage artifact cap a, log caps l_out/l_err, the current conservative
new-output reservation is

\[
B_{new}=\sum_{k\in missing}(a_k+l_{out,k}+l_{err,k}+2\mathrm{MiB})+4\mathrm{MiB},
\quad E_{new}=8\lvert missing\rvert+4.
\]

The fixed2MiB term is existing controller policy, not actual artifact size.
It must not be silently removed to make a quote fit. At a=512KiB and each log
cap64KiB, the stage reservation is2.625MiB. For m=1:

| Actual s (illustrative except113) | H host calls | Q checkpoints | Output reserve | Entry reserve | Checkpoint-only inventory at512KiB |
|---:|---:|---:|---:|---:|---:|
|113|340|339|896.5MiB|2724|169.5MiB|
|226|679|678|1786.375MiB|5436|339MiB|
|256|769|768|2022.625MiB|6156|384MiB|
|452|1357|1356|3566.125MiB|10860|678MiB|
|512|1537|1536|4038.625MiB|12300|768MiB|

Current allowance ceilings are250000workerCPU,3600controllerCPU,86400wall,
2048MiB output,8192entries. The illustrative po17-sized cases fail output,
entry and complete-inventory512MiB envelopes at those conservative artifact
caps. At N=512,M=8, the generic maximum1544 host calls reserves4057MiB and12356
entries; a prospective4096MiB/16384-entry output envelope fits **one** such
reserved pass but is not proof that CPU/memory/attempt-tail bounds fit. Its
checkpoint-only inventory at512KiB is771.5MiB, so512MiB controller input is
insufficient. Widening all input reads to1GiB would be a separate resource
selection; alternatively smaller justified artifact caps might avoid it.

The exact CPU expression is

\[
C=s c_{seg}+s c_{lift}+(s-1)c_{join}+m c_{resolve}+c_{finish}.
\]

At lift/join250CPU, resolve600CPU, finish300CPU and m=1, fitting250000CPU requires
`c_seg <= 249350/s - 500`. At s=226 this is603.3186CPU; at s=256 it is474.0234;
at s=452 it is51.6593; at s=512 the recurrence stages alone already exceed the
ceiling. Historical po18 segment maximum973.03125CPU is **not** a lower bound
on new work, but it prevents pretending that reducing its cap to603 guarantees
completion. More segments exchange memory for more lifts/joins, parent checks,
capsule decoding and fixed process/controller overhead; they do not establish
a net cost improvement.

Current same-allowance history permits at most16 prior attempts (17 including
current), each report<=1MiB and aggregate prior reports<=8MiB. Do not raise this
merely to perform one stage per attempt: batch stages inside finite attempts.
For679 calls,17 attempts require an average at least39.94 calls/attempt;
for1537, at least90.41. After a separately authorized five-stage prefix, the
remaining16 attempts would need average42.125 or95.75 calls respectively.
Keep all failures and successful checkpoints charged, exact profile/session/
budget identity, no-success-loss rules, and first-failure stop semantics.
Changing geometry means a new lineage with **carried prior costs**, not resetting
old expenditure or relabeling the retained po19 capsule as a failed experiment.

Controller work is also not constant: every stage rebinds all accumulated input
pins and walks retained output (`producer.py:458,479,499,568`). At roughly fixed
artifact sizes, these repeated checks contribute O(H²) cumulative bytes/entries,
in addition to O(H) process calls and capsule reads. Existing3600controllerCPU
may or may not suffice; count widening is not a complexity improvement. This
is a disclosed cost, not permission to weaken final binding checks or start a
new caching mechanism without a concrete need.

## Minimum prospective refinement and present stop

If root chooses smaller geometry, select fresh source successors only: snapshot
host+adapter+build recipe, aggregate stage host+build recipe, and aggregate
controller/count helpers. Reuse unchanged receipt/native relation/SDK/guest
artifacts and their prior reviews. Exact build selectors/source maps, host
adoption parsers and snapshot result/configuration bindings must identify the
new host/adapter bytes; the current builder pins cannot be borrowed unchanged.
The mathematical receiver/acceptance rules need not change.

Before any expensive proof, obtain one complete newly bounded layout and derive
the exact s, bytes, finish input/composite/argv bounds and full remaining-graph
quote from it. That execution would answer an actual changed-geometry question,
not repeat the successful po19 experiment. No such execution is selected now.

**Present recommendation:** retain this alternative; finish the provisioned
producer-memory decision first. Reusing the existing capsule on an actually
adequate bounded producer avoids all geometry changes above. Neither route
proves economical growth or completes v5 merely by producing a receipt.
