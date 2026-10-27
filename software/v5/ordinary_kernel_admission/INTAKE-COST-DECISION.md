# Intake CPU refusal: shrink work units before changing the checker

Recommendation: retain the current implementation and preserve the accepted
1,024-unit prefix. After the separate operational audit/protected-context decision,
select only the remaining 1,627 exact units in four balanced complete-unit batches,
split across two explicit two-batch invocations. Keep the existing 60-second
per-operation and 300-second public CPU limits. Do not retry the failed large
batch, enlarge its allowance or rebuild the receiver merely to bypass this result.

This note analyzes saved JSON and source only. No product import, native process,
owner/status/recovery call, database, manifest creation, file deletion or Git action
occurred. Operational closure and prefix eligibility are independently owned by
intake_interruption_audit; manifest/continuation legality is independently reviewed
in INTAKE-CONTINUATION-OPTIONS. The recommendations below select no execution.

## Why a 60-second operation launched a 24-second child

Current `baseline_intake.IntakeBudget.operation` creates an ordinary
`OperationBudget(cpu_seconds=60)` **before public preflight**, then charges a
nonrefundable 60-second reservation to the whole intake. The operation budget
counts controller preparation and child CPU together. Immediately before native
launch, `ordinary_admission.OperationBudget.allowance` computes

\[
L_{\mathrm{child}}=\lfloor60-C_{\mathrm{operation,so\ far}}
 -W_{\mathrm{previous}}\rfloor-1.
\]

There has been no previous child in this operation, so `W_previous=0`. A recorded
child limit of 24 implies **34 < C_prelaunch <= 35 CPU seconds**. This is unrelated
to the separate 24-second **wall-time** cleanup reserve in the adjacent line.

The successful first batch received 37 child CPU seconds, implying 21 <
C_prelaunch <= 22. Its worker consumed 24.46875 seconds. The larger second batch
received only 24 and was stopped at 24.015625 observed CPU seconds. The saved
failed call had 196 wall seconds available and empty stdout/stderr. Thus the
immediate refusal is a native CPU ceiling after expensive preparation, not a
reported mathematical error, name collision, RAM event or wall deadline.
The failed child did not finish: 24.015625 is censored work, not its completion cost.

The 60-second reservation is also not a promise of 60 native seconds. Global
`IntakeBudget.check` uses controller CPU plus all 60-second reservations; the
controller part of each operation therefore appears both in live controller
accounting and inside its reserved combined-operation cap. This is conservative
authorization accounting, not additional CPU consumption or an accounting
undercharge. Do not silently reinterpret that cap or refund it from partial
worker observations.

## Observed costs isolate the bottleneck

The progress stream is under
`std-kernel-catalog01/intake-diagnostics/8f8bbda4ecc02ffccf9b67d7e50ca8b2`.
The following controller deltas come directly from adjacent saved checkpoints:

| Phase | Batch 0 | Batch 1 | Batch 2 |
|---|---:|---:|---:|
| Whole-manifest metadata planning | 8.15625 s | 13.5625 s | 13.9375 s |
| Actual reread/validation | 4.078125 s | 6.921875 s | Not reached |
| Public preflight | 3.953125 s | 6.953125 s | Not reached |
| Admit intent through confirmation/failure | 17.6875 s | 28.03125 s | Not reached |
| Observed native child CPU, separate from controller | 24.46875 s | 24.015625 s, stopped | Not reached |

Metadata completion records 35.78125 controller seconds including small surrounding
bookkeeping. Batch 0's operation controller total is 21.640625; batch 1's is
34.984375. These totals include the public preflight and subsequent admission;
the native allowance deduction excludes any controller work after launch.
Progress records update observed-worker accounting in `finally`, so the first
confirmation's zero worker field is not a zero-cost measurement.

The owner report records 104.234375 controller CPU seconds plus 48.484375 observed
worker seconds. Inclusive outer Job CPU is 153.375, with 1.59375 outer wrapper CPU:
154.96875 known CPU seconds. These scopes overlap; do not add nested figures again.
Most measured CPU is in the controller. The saved phases do not separately meter
custody, serialization, catalog reservation or individual parser calls, so no
precise measured attribution among those substeps is warranted.

## Remaining repetition is real, but changing it is not the cheapest next step

Source inspection confirms the already-adopted private parse reuse remains in
place. It removed earlier duplicate conversions; this failure is not evidence
that that earlier change was absent. The remaining portable strict-parse count
for a distinct new unit on the successful path is:

| Boundary | Parses |
|---|---:|
| Metadata file validation and private planning | 2 |
| Actual file validation | 1 |
| Public preflight | 1 |
| Independent actual admit planning | 1 |
| Admission staging and custody validation | 2 |
| Catalog extension reservation | 1 |
| Total | 8 |

The successful first two preparation paths plus metadata for all three batches
fed **252,696,640 encoded bytes** into these portable parser calls:
`2*44,912,843 + 6*9,997,243 + 6*17,147,916`.
This is a source-derived traversal count, not a measured byte-allocation total
or a promised speedup. Native decoding/checking, canonical serialization,
context validation, hashing, per-unit durable custody transactions and file I/O
remain separate work. The metadata pass drops each batch's proof trees, so this
does not require keeping the full library in memory.

A core/private ownership redesign might remove additional repeated parsing;
eliminating all four repeated operation parses after one parse would at most
remove those traversals, not all controller costs. It would need exact byte/parent
bindings, unchanged public defensive boundaries, durable custody, complete
inventory checks and focused review. A change to installed ordinary_admission
or catalog bytes changes implementation identity and currently requires fresh
checked state. Paying that integration and rich-prefix recheck now has lower
expected payoff than using existing smaller-batch semantics. No such source
change is proposed for this continuation.

An auxiliary-only intake redesign could avoid redundant public preflight or
preflight all retained files once per run, but actual `admit` must still freshly
validate its raw units and current protected parent. Moving the operation clock
after preparation merely hides cost from the 60-second cap; it does not optimize
the work. Do not label that move a performance improvement.

## Preferred operating strategy and its honest headroom

The accepted prefix is 1,024 units / 9,997,243 bytes. The unresolved suffix is
**1,627 units / 34,915,600 bytes**. Preserve all exact unit bytes, identities and
their dependency-respecting order. The largest retained suffix unit is 970,481
bytes; splitting evidence units or inductive groups is unnecessary and forbidden.

The continuation reviewer calculated these partitions from the original manifest
entries alone, halving each original suffix batch by bytes (zero-based original
positions):

| Chunk | Original half-open positions | Units | Raw bytes |
|---|---|---:|---:|
| A | [1024, 1644) | 620 | 8,552,756 |
| B | [1644, 2048) | 404 | 8,595,160 |
| C | [2048, 2477) | 429 | 8,899,687 |
| D | [2477, 2651) | 174 | 8,867,997 |

Each is contained in an original metadata-validated batch, so its additive
structural bounds inherit a simple subset argument. Global byte balancing would
reduce the largest chunk by only about 1.5% while crossing an old batch boundary;
that gain does not justify additional qualification here. All four are smaller
in bytes and unit count than the successful first batch. A
rough proportional model calibrated to that batch's 46.109375 combined operation
CPU seconds suggests about 41 seconds per 8.9-MB chunk, before accounting for
different proof complexity and context costs. **This is a planning heuristic,
not a bound:** Lean conversion/checking cost cannot generally be bounded linearly
by encoded byte length. Existing CPU/heartbeat/depth limits still stop expensive
mathematics safely; a single unexpectedly expensive unit could still fail.

Four batches in one intake reserve 240 seconds before actual controller charges.
Extrapolating the observed suffix read/planning/staging work gives roughly another
113 controller seconds, already incompatible with the unchanged 300-second
invocation cap. Even three larger ~11.6-MB batches would leave only about
7 seconds of coarse estimated global headroom after 180 reserved seconds and
that controller work. Neither is a sensible next selection.

Instead, two explicitly selected two-batch invocations reserve 120 seconds each.
Their rough ~55-65 controller seconds per invocation leave substantial reservation
headroom without changing any limit. Extra module restores/startup/commit costs
must remain charged; the model does not claim lower total CPU solely from using
more chunks. The benefit is avoiding another near-certain oversized operation
and preserving each genuinely accepted prefix for subsequent useful work.

The public intake API already accepts a separately selected manifest over the
same retained bundle directory. It need not copy/re-export/reconstruct raw units.
The first suffix selection must use the separately validated protected prefix;
the second must use the first invocation's actual accepted result root. Names,
imports, structural ceilings and all quota/capacity checks remain enforced by
normal intake. The continuation review owns the exact manifest obligations.

Supplying the original complete manifest at the prefix would reuse old units
mathematically but still reread, parse, restage and reserve 60 seconds for its
REUSED first batch. Selecting only the suffix avoids those costs. Source count
for that reused prefix is seven parses per raw unit rather than eight because
there is no extension reservation: about **69,980,701 encoded parser-input bytes**
and one unnecessary 60-second authorization reservation are avoided. Original
metadata/preflight timings illustrate the cost scale; they are not a measured
counterfactual for a new run against fuller custody.

## Evidence bindings and stop rule

| Evidence/support | SHA-256 |
|---|---|
| Installed ordinary_admission.py | `98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a` |
| Installed baseline_intake.py | `49b6f8f1e1f1cb55526b0f8787414e05619af3d19a28e65ad5372186a5171ca2` |
| std-kernel-intake01/RESULT.json | `8800b81ea98ae4a61b79d26dcbfe49972baf4979a61fdcd2f5bc03b914184095` |
| public-launch/child/stdout.txt | `dbb7d1f1e0f0361b9f263ed1ecbed1a3734b2502ad05889131fbf39ba0e2d07b` |
| Failed 22c8515b.../supervision-result.json | `060390bedef5b71ba3267c9c43afa297ac512ccde447158a6db61e9a01b182e2` |
| 0007-METADATA_COMPLETE.json | `1f81a135a792417620ad961874dc6549d22321b91de16d571e13f8a914751202` |
| 0019-FAILED.json | `7fae68e4d5af68c164e7912234d7e0a45febbbb7bffc23d6f504166ee27d70c7` |

The first separately selected continuation failure is another decision point;
no automatic retries, adaptive budget replenishment, hidden status calls or
promotion of failed artifacts follow. If small balanced batches still leave
controller work dominant or contain an individually expensive unit, inspect that
actual changed boundary before deciding between further finite partitioning,
operation-local validation reuse or selecting a smaller useful mathematical
closure. The purpose remains enabling the substantive concept contribution,
not maximizing the number of intake experiments.
