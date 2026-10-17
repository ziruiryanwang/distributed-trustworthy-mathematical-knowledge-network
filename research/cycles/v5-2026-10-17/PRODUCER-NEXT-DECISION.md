# Next producer decision: bounded po18, not a po19 cap ladder

Owner: `memo_tests_review`, 2026-10-17. **Source/design recommendation only.**
No implementation, product import, test, build, execution, proof, new machine
observation, allowance or Git operation is selected or performed by this note.
Root owns source selection and any subsequent finite operation.

## Decision

Implement a fresh, bounded **po18 / at most 256 segments** producer successor,
using the same actual A image, I/F/P, exact aggregate header and genuine I
premise. Preserve complete-composite verification at finish. Replace the
checkpoint argv fanout with one exact pinned dependency-list file. Obtain a
fresh execution capsule before deciding whether proof production is affordable.

This is the next source implementation, not a claim that the entire proof fits
the current machine or that a new certificate already exists. It addresses an
established obstacle while retaining the mathematical and cryptographic core.
It does not change the final deployable-v5 goal to merely producing a receipt.

Reuse these completed analyses, without repeating them:

- [SMALL-SEGMENT-DESIGN](../v5-2026-10-16/SMALL-SEGMENT-DESIGN.md): all count,
  capsule, argv, serialization and accounting seams.
- [PROVER-MEMORY-REVIEW](../v5-2026-10-16/PROVER-MEMORY-REVIEW.md): unchanged po19
  has a source-derived simultaneous-live lower bound of 5.330078125 GiB;
  C++ constructor allocations alone exceed 4 GiB.
- [FULL-PATH-FEASIBILITY-REVIEW](../v5-2026-10-16/FULL-PATH-FEASIBILITY-REVIEW.md):
  retained s113 non-memory quote, exact composite serialization argument and
  optional frontier-only-finish argument.

Root supplied the current read-only observation: total physical
16,434,516 KiB, available physical 3,776,736 KiB, available commit 5,593,372 KiB.
These are observations, not reservations. Available commit is approximately
5.334 GiB, effectively consumed by the po19 lower bound before its excluded
allocations. There is no basis for assuming retained-po19 capacity or freeing
other applications on the user's behalf. No additional capacity polling is
needed to choose the source design.

## Alternatives and scope

| Route | Decision and reason |
|---|---|
| Same po19 on an actually provisioned producer | Keep as a separate operator option, but current capacity does not justify selecting it. Raising a limit cannot supply memory. |
| Correct the retained SDK's Rust preflight unit mismatch only | Not this successor: even the corrected po19 lower bound is 4.43359375 GiB and C++ alone is 4.134765625 GiB. It requires an SDK successor/rebuild yet does not solve the 4 GiB obstruction. |
| Po18 with unchanged SDK and mathematical guest | Recommended source path: halves the row-scaled lower bound to 2.6650390625 GiB, with larger orchestration cost explicitly bounded below. This is not a peak-memory upper bound. |
| Po17/N512 | Defer: more checkpoints, recursive proving and input/output work, without an established need after po18. |
| Rewrite prover allocation schedule or stream prover state | Defer substantial backend/assurance work until there is evidence this narrower route is insufficient. |
| Wait indefinitely for memory | Not useful project progress. Design/build preparation can advance without a proof launch. Launch admission still requires adequate contemporaneous capacity. |

Historical successful base-I po18 proofs provide implementation context, not
an A-workload prediction. In particular, neither the approximately 3.29 GiB
historical peak nor 4 GiB as a proposed cap establishes future sufficiency.
Never infer that a halved lower bound is a halved actual peak.

The optional frontier-only finish has a defensible acceptance argument in the
prior review. Do not combine that assurance change with the first geometry
successor: preserving the existing composite cross-check isolates this change.
Its removal can be separately selected if its actual cost warrants doing so.

## Preserve exact mathematics; replace execution identity

The retained A is
`99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`.
Use its actual retained ELF and unchanged relation/checker libraries, expected
192-byte header, current wire and genuine I receipt. No guest/checker/SDK rebuild,
new foundation, weakened assumption rule or certificate-policy change is needed.

The session hash binds ELF, A, I/F/P, wire/header, cycles, po2 and ordered parent
hashes. The capsule hash additionally binds its exact complete segment vector.
Thus po18 **must** have a fresh capsule, session/capsule identity and operation
history. The old 113-segment po19 capsule remains valid preserved evidence;
it is neither reused with a different po2 label nor reclassified as a failure.

Use the existing fixed session row cap `2^26` for the prospective fresh layout,
with po2=18, N=256 and the unchanged assumption maximum M=8. This is a finite
attempt at a changed geometry, not a theorem that it finishes. In particular,
the SDK split threshold is `2^po2 - 25,000`, and padding, split/page overhead,
large instructions and the last segment matter. **Do not predict s=226 by
doubling 113.** The actual layout must supply s, per-segment geometry, bytes and
successful exact target claim before a proof request can be formed. First
limit/refusal stops; no automatic po17 retry or count/cycle escalation.

## Concrete successor envelopes

These are candidate implementation/admission limits, not funding, expected
costs or guarantees of completion. Keep distinct bounds for distinct objects;
keep the existing image/receipt/checkpoint `FILE_LIMIT=64MiB` unchanged and add
only separate `CAPSULE_LIMIT=96MiB` and `COMPOSITE_LIMIT=160MiB`. The selected
profile's smaller per-parent/artifact admission caps apply in addition to that
unchanged outer format bound.

| Boundary | Candidate value and rule |
|---|---|
| Actual segment count / assumption count | `1 <= s <= 256`; `0 <= m <= 8` |
| Complete stage DAG | `H=3s+m <= 776` host calls; `Q=H-1 <= 775` proof checkpoints |
| Stage keys | segment/lift 0..s-1; join 1..s-1; resolve 0..m-1; finish only 0 |
| Retained execution-segment bytes, sum | 96 MiB; individual decoding remains bounded separately |
| Whole capsule encode/read/decode | 96 MiB at snapshot host, stage host, adapter and controller |
| Snapshot output custody | 208 MiB / 288 entries: 96 MiB segments + 96 MiB capsule + 16 MiB diagnostic/control reserve; actual census still enforced |
| Parent receipt | At most 1 MiB each for this bounded producer profile; actual retained I receipt is 223,594 bytes |
| Every newly produced or retained/admitted checkpoint, and final succinct receipt | 512 KiB; enforce on request inventories and prior-success rows as well as new artifacts; actual size excess is refusal, not truncation |
| Stdout / stderr | 64 KiB each per stage |
| Dependency-list file | 256 KiB absolute ceiling, at most 257 rows; stronger per-kind caps below |
| Complete internal composite | 160 MiB dedicated serializer/decoder bound; never a published receipt |
| Per-host aggregate bytes read | 512 MiB, including manifest bytes and every actual read |
| Initial controller request-input inventory | 512 MiB, including capsule, all retained checkpoints, prior reports and snapshot evidence |
| Profile/installation pins | Separate existing 512 MiB inventory envelope; not memory usage |
| Continuations | At most 16 prior attempts, each report at most 1 MiB, aggregate prior reports at most 8 MiB; preserve existing lineage and first-failure rules |
| Candidate whole proof allowance maxima | 500,000 worker CPU seconds, 7,200 controller CPU seconds, 172,800 wall seconds, 2,304 MiB retained output, 8,192 entries |
| Candidate stage memory | Explicit 4,096 MiB cap under the existing owner-selected memory policy; no claim that current headroom or this cap suffices |

N and M are format limits; they do not require every request to fund their
maximum graph. Exact actual-s/m quoting is required before each continuation.
The broadened allowance is a new explicit schema/profile selection, never a
mutation/renewal of the retained 250,000-CPU allowance or a hidden default.
Preserve all external preparation/build/execution costs and failed attempts.

The 1 MiB parent cap is an intentional local operational restriction, not a
new mathematical acceptance predicate. Larger valid parent receipts require
a separately reviewed resource profile. This avoids pretending all eight
64 MiB old-format parents fit alongside the largest capsule/inventory.

## Dependency manifest: exact finite transport, not new authority

Use an explicitly new **`stage-manifest`** command, with no old-argv fallback.
Replace the trailing `[CHECKPOINTS...]` with
`DEPENDENCIES_PATH DEPENDENCIES_BYTES DEPENDENCIES_SHA256`. Keep the existing
at-most-eight parent operands. `stage` argv therefore has exactly `16+m`
arguments including the executable, independent of s. Check actual Windows
UTF-16 command length including quoting and NUL before dispatch; require at
most 32,767 units. A bounded number of arguments alone does not bound their
path lengths. This is a new command schema; old CLI bytes stay frozen.

The manifest is a create-new, fsynced ordinary file under the stage directory:

```text
schema: DMKN_AGGREGATE_DEPENDENCIES_V1
session_binding: lowercase SHA-256
capsule_binding: lowercase SHA-256
stage: exact stage-key string, e.g. join:1
dependencies: [{key: exact stage-key, file: {path, bytes, sha256}}, ...]
```

Required implementation rules:

1. Pin its exact bytes in the reservation, active input map and stage result;
   argv carries its independently expected size and SHA-256. The host reads
   once within the manifest cap, charges that read, and checks length/hash
   before parsing. A valid manifest is bookkeeping, never proof of mathematics.
2. Use exact typed JSON fields: unknown/duplicate fields, wrong types, boolean
   integers, invalid digest spelling, excess count and trailing data refuse.
   A JSON-specific bounded sequence deserializer counts rows incrementally,
   rejects a 258th row before appending it and never preallocates from an
   untrusted count hint. Do not reuse the bincode capsule visitor's requirement
   for an exact `size_hint`: JSON sequences normally provide none. Canonical
   JSON is produced by the controller; native
   semantic parsing need not reinvent Python's Unicode canonical serializer.
   Stage-key parsing requires exactly the canonical kind/index spelling and
   bounded index; alternative numeric spellings and unsupported kinds refuse.
3. Each path is absolute, normalized, ordinary/non-reparse and at most 512
   UTF-16 units. The separate encoded manifest-byte cap always applies. The
   concrete quote uses ASCII paths at most 256 characters and encoded pin rows
   at most 512 bytes; future paths not meeting that quote need exact recomputation.
4. Derive the ordered dependency keys from the actual bounded capsule and stage,
   in the host as well as controller. Require list equality, not just set
   membership. Reject duplicates, reordering, wrong stage, missing, extra or
   wrong-capsule dependencies before proving. Never follow transitive list files.
5. Read every dependency with ordinary-path checks, expected size/hash and the
   aggregate read budget. Compare checkpoint envelope key and capsule binding
   to its row, then perform unchanged SDK verification when consumed. Reject
   leftover cache entries. Pins and a checkpoint header are not substitutes
   for cryptographic verification.
6. Keep exact source/profile/session/allowance rebinding before and after each
   host call. Mutation after a read cannot change the bytes already checked;
   subsequent rebinding detects changed retained inputs and prevents a passing
   owner report. Do not claim filesystem immutability or hostile-source isolation.

Per-kind manifest caps: segment 2 KiB (empty list), lift 4 KiB (one row), join
6 KiB (two), resolve 4 KiB (one), finish 256 KiB (s segment rows plus final prefix).
All remain independently capped at 257 rows. These caps must be enforced by
both controller and host, not only used in a spreadsheet quote.

There are at most `4s+m-1` dependency rows over a full graph. Thus this design
does not replace argv fanout with repeated full inventory manifests: only
finish carries all segment proofs. Source-only tests must cover exact ordering,
size/hash binding, wrong-capsule rows and the 256/257/258 boundaries.

## Composite and input arithmetic

Keep the full finish dependencies: all s segment receipts **and** the final
resolved prefix, or final join/lift for m=0. Keep independent composite integrity,
exact target-claim comparison, fully resolved succinct-claim comparison and
the unchanged final `verify_aggregate(A,H,R)` call with dev mode disabled.

The prior fixed-integer bincode analysis gives 71 bytes of segment-checkpoint
overhead and 48 bytes of composite tuple overhead. The erased-claim assumption
is no larger than its admitted original receipt for this pinned SDK layout.
Therefore, under the candidate successful artifact/parent caps:

```text
composite <= 256*(524288-71) + 8*1048576 + 48
          = 142,588,208 bytes < 160 MiB.
```

Use separate `encode_composite/decode_composite` bounded at 160 MiB; do not
let that bound widen checkpoint, journal or final-receipt readers. The tuple,
decoded composite and reserialization can coexist: **serialized size is not
resident-memory size**. Charge their actual lifetime to the finish Job, and
drop obsolete serializations after their last check where the implementation
can do so without removing a verification. No 160 MiB composite is sent through
the evidence network. The published final succinct receipt is independently
limited to 512 KiB, below that network's 8 MiB terminal-receipt ceiling.

For the initial controller inventory, require the remaining fixed session and
snapshot-evidence inputs, excluding capsule/checkpoints/prior reports, to total
at most 20 MiB. With all 775 checkpoints at their cap:

```text
96 MiB capsule + 387.5 MiB checkpoints + 8 MiB prior reports
  + 20 MiB other fixed request inputs = 511.5 MiB < 512 MiB.
```

This fixed-remainder gate covers the image, wire, header, parents, adopted
snapshot-host binary and actual snapshot records; check the real sum rather
than assuming the new host is the old size. A candidate snapshot host at most
8 MiB, existing approximately 1.87 MiB ELF/wire/header, at most 8 MiB parents
and 128 KiB records fit this fixed envelope. Those extra caps are prospective
admission conditions, not predictions about a future build.

Finish's maximum dependency bytes are only `257*512KiB = 128.5MiB`, not the
whole 387.5 MiB checkpoint inventory. Even using the above 20 MiB remainder
as an overestimate, its read quote is
`96 + 20 + 128.5 + 0.25 = 244.75 MiB < 512 MiB`.
Every stage must use actual input lengths, not only this generic inequality.

The controller adds new reservation/stage-result/manifest files after request
validation. The current predecessor does not reapply its request-sum bound on
every insertion; do not misreport that as a perpetual 512 MiB input limit.
For the successor, make this finite explicitly: reservation and stage-result
records each at most 64 KiB; reservation refers to the manifest pin instead of
duplicating its row vector. Saved request/profile stay at most 1 MiB each.
At H=776 these two per-stage record kinds total at most 97 MiB. All manifest
caps together total at most 3,354 KiB. A separate 128 MiB active-administrative
pin allowance covers them and the two initial control records, preserving
unchanged full rebinding. It is charged to output too. Initial inputs plus
new administrative pins are therefore at most 640 MiB of pinned file bytes;
installation pins are separate. None of these figures is a RAM/Job bound.

## Whole-graph accounting: do not force an implausible tiny stage cap

Preserve the old 2 MiB per-stage administrative reservation. Add 256 KiB and
one entry for the new manifest rather than silently consuming its old margin.
This intentionally uses the maximum manifest bound for every stage when
reserving output, despite smaller enforced per-kind manifest limits.

```text
per-stage output reserve = 512KiB + 64KiB + 64KiB + 2MiB + 256KiB
                         = 2.875 MiB
per-stage entries        = 9
```

At H=776 and 17 total attempts, including a separate 4 MiB/four-entry
administrative envelope for each attempt:

```text
output = 776*2.875 + 17*4 = 2,299 MiB < 2,304 MiB
entries = 776*9 + 17*4 = 7,052 < 8,192.
```

That is a no-repeated-stage conservative successful-path quote, with only
5 MiB output slack at the generic maximum. It does **not** fund arbitrary
failed retries. Actual previous output, including partial failures, remains
charged; future admission uses remaining resources. Fewer actual segments,
smaller actual artifacts or fewer attempts can yield additional retained
headroom, but that is measured slack, not an automatic renewal.

Keep 16 prior attempts and 8 MiB aggregate prior reports. A concrete schedule
is an optional one-call prefix and subsequent batches of at most 64 calls;
H<=776 then needs at most 14 attempts, leaving three potential attempt slots,
not prepaid resources. With at most 775 retained rows, 64 stage pins, 16 prior
pins and two controls, each encoded row at most 512 bytes, a 16 KiB remainder
gives a report bound of 455,168 bytes, below 512 KiB. Sixteen such reports fit
8 MiB. Actual report encoding, failure diagnostics and path lengths are still
checked; the row bound is part of this concrete naming/batching profile.

At unchanged lift/join CPU caps of 250, resolve 600 and finish 300, the old
250,000 worker-CPU ceiling would force segment caps below 475 at s256,m1.
That is not evidence that a complete path is feasible. Propose, without funding:

| Stage | CPU cap / wall cap, seconds | Maximum count |
|---|---:|---:|
| Segment | 1200 / 240 | 256 |
| Lift | 250 / 150 | 256 |
| Join | 250 / 150 | 255 |
| Resolve | 600 / 600 | 8 |
| Finish | 300 / 120 | 1 |
| **Sum** | **440,050 CPU / 143,010 wall** | **776** |

These fit the prospective 500,000 CPU / 172,800 wall ceilings, leaving 59,950
worker-CPU seconds and 29,790 seconds of raw wall headroom. The remaining wall
time must cover controller and inter-call overhead too. The 7,200 controller
CPU cap is an explicit owner allowance, not a bound derived from file bytes.
No cap guarantees success; the historical 973.03125 po18 segment-CPU maximum
is context for avoiding an obviously restrictive cap, not an upper bound for A.

Rebinding all accumulated checkpoints remains O(H^2) byte-work. Even ignoring
attempt-boundary passes, two checks per stage imply a conservative
`H*(H-1)*512KiB` checkpoint-byte term, about 293.65 GiB at H=776; capsule,
installation, administration and continuation passes add more. This is not
negligible or a timing prediction. Preserve mutation detection in this narrow
successor; do not introduce an unreviewed caching framework to disguise cost.
Full-cost growth accounting must include this producer overhead and amortize
it over genuine reuse, rather than attributing receiver savings for free.

## Smallest source selection and constructor seams

Use one fresh package, proposed `software/v5/aggregate_small/`, without editing
frozen `production`, `aggregate_production`, `aggregate_resources`, SDK, guest
or existing receipt/evidence-client sources. Seven implementation/build files
are sufficient; a changed-boundary control file and concise API note can be
owned separately by root/reviewer:

| New file | Narrow predecessor and required delta |
|---|---|
| `aggregate_host.rs` | Snapshot host: N256, separate 96 MiB segment-sum/capsule bounds, unchanged actual guest/relation/session binding and diagnostics. |
| `stage_host.rs` | Current stage host: bounded N256 capsule decode, new exact manifest CLI/parser/expected dependencies, 160 MiB internal-composite helpers, unchanged final acceptance. |
| `producer.py` | Resource producer: own bounded stage-key/iterative graph-plan helpers, N256/Q775/H776, manifest lifecycle, explicit new schemas/allowance ceilings and metadata accounting, exact new snapshot/build adoption. |
| `__init__.py` | Export only the fresh producer; no legacy import monkey-patching. |
| `build_snapshot.py` | Exact one-link successor of retained snapshot recipe; fresh source/output names and pins, unchanged SDK/relation libraries. |
| `build_stage.py` | Exact one-link successor of retained stage recipe; fresh source/output names and pins. |
| `capability_snapshot.py` | Fresh finite po18/N256 layout adapter over unchanged actual A inputs; 96 MiB capsule, 208 MiB/288-entry custody and updated host/result bindings. |

Keep a single `AggregateProducer(profile)` public constructor in the new
package. Give the new profile/request/result/command records distinct schemas;
do not accept a former profile merely because most fields match. Profile hashes
bind exact new source pins, build records, mathematical image adoption,
operational ceilings and the owner-selected memory limit. P.Producer may still
supply the unchanged pinned supervisor/Job loader and pure parsing/pin helpers.
Do not borrow its old `stage_key/graph/missing_plan`, which enforce N128.

The new iterative missing-plan walk uses the same deterministic ordered DAG,
terminates after at most H unique nodes and emits dependencies in the original
order. Reuse exact image adoption and final predicate checks; update `_adopt_build`
and `_snapshot` to real fresh record formats, never fabricated adoption records.
Source closure must include every actually imported helper, not only the seven
new files. Keep strict same-profile/session/budget/history equality and
no-success-loss checks. A separately reviewed fresh no-host preflight adapter
is needed only after real new build/layout records exist; do not recopy/run the
old retained-po19 preflight as if it qualified this new path.

## Efficient execution order after root source selection

1. Implement the narrow successor and changed-boundary controls in parallel
   with independent source review. Reuse old seven policy controls, sixteen
   public-A controls and all passed predecessor evidence; test only new seams.
2. If root separately selects builds, link the two small native hosts against
   the retained SDK. No guest rebuild or proof is needed. They are independent
   build tasks but must share an explicit enclosing resource budget if concurrent.
3. Separately select **one complete po18 layout** using the same mathematics.
   Its information value is real s/bytes/geometry and exact completed claim.
   Stop on refusal; do not start proofs on a partial capsule or automatically
   widen N/bytes. Retain all failures and preparation costs.
4. Bind real build/layout records in the fresh constructor/request preflight;
   compute actual full-path composite/read/argv/report/output/CPU/wall quotes
   and screen actual memory capacity. This is not a second run of the old
   retained-po19 preflight: new geometry/host/manifest boundaries are the reason.
5. Only if separately funded and capacity-admitted, choose the cheapest real
   discriminator: **one actual full-po18 segment**, preferably existing
   `stage_limit=1` when completed layout shows segment0 has po2=18. If segment0
   is smaller, proving it does not test full-po18 memory; root must identify
   the least-cost existing-path discriminator from the actual layout before
   selecting a run. Do not add arbitrary-stage scheduling to this source
   successor merely for a pilot. No automatic five-call prefix, unchanged
   lift/join work or full-run launch is selected. One segment cannot establish
   full cost or worst-case memory of every later segment. No parallel segment
   proofs on this machine merely because tests can run in parallel; their
   multi-GiB live allocations would add. Continue successful checkpoints under
   the same finite allowance only by a separate decision, stopping on refusal.
6. A genuine finished A receipt is then an input to the already implemented
   terminal/mixed-evidence public path and substantive reciprocal reuse work.
   Do not rerun its completed synthetic tests to claim genuine A integration,
   and do not label one certificate as final v5 or a growth advantage.

This resolves the next source-design decision. Remaining uncertainty is
explicit and localized: actual po18 completion/size, proof-memory upper use,
artifact/stage costs and resulting amortization. These are the conditions a
targeted future operation can distinguish; another unchanged po19 failure or
an indefinite sequence of cap changes cannot.
