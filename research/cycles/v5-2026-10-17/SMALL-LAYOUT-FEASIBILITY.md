# Small-layout failure: exact cause and smallest next decision

2026-10-17, `memo_tests_review`. Source and saved-evidence analysis only.
No product imports, tests, builds, guest executions, proof operations, SDK edits,
cap changes or Git mutations were performed. Root owns adoption and any fresh
operation. The canonical workspace guard passed.

## Decision

**Do not repeat the same po18/N256 execution or jump to N512.** Its failure is a
real geometry/resource obstruction, not an adapter defect. The existing SDK
counts padded segments and repeated segment machinery toward the session limit.
The exact failed execution was still nonterminal after all 256 segments.

First examine the **smallest exact target-preserving aggregate witness** needed
by the ordinary client gate: BASE plus FIRST, without the unnecessary SECOND
descendant. This preserves the target `J_FIRST`, not the old three-member
aggregate header or witness identity. Root's separate semantic review must
establish the exact target, admitted parent and complete FIRST dependency
closure. It must not replace FIRST with an easier theorem or discard its own
dependencies. A new header, wire and capsule are required; the actual A image,
checker, policy and po18/N256 implementation can remain unchanged if the source
contract confirms the smaller witness is supported.

The existing failure does **not** prove that this smaller witness fits. A single
fresh execution-only layout, if separately selected after that source check,
would resolve its concrete segment count at very small cost relative to proving.
No proof, automatic retry or larger envelope follows from this recommendation.

## 1. Exact saved comparison

Both diagnostics bind the same actual guest image
`99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`,
ELF SHA-256
`98686ced7979d55685c648f441f7ffbe40712e327a1311f9cb076a0c7250e773`,
215,540-byte wire SHA-256
`2aea63ff488a4c012233742306c71526aea37c67d9f8d214e94c0d95d1200cb4`,
the same exact aggregate header and the same genuine I receipt. This is a
geometry comparison, not a new mathematical result.

| Saved quantity | Completed po19 layout | Failed po18 layout02 |
|---|---:|---:|
| Retained segments | 113 | 256 |
| Rows per retained segment | 524,288 | 262,144 |
| Sum padded rows | 59,244,544 | 67,108,864 |
| Sum padding rows | 2,837,968 | 6,375,638 |
| Sum rows excluding recorded padding | 56,406,576 | 60,733,226 |
| Recorded machine instructions | 81,348,253 | 75,132,143 |
| Retained segment bytes | 37,186,652 | 49,437,484 |
| Complete execution capsule | Yes; not a certificate | No |
| Proof operations | 0 | 0 |

The po18 error is exactly
`Session limit exceeded: 67112097 >= 67108864`.
It has null `session_stats` and null `result`, and status
`FAILED_NO_ACCEPTED_CAPSULE`. All 256 segment rows are po18. Their individual
padding lies between 24,411 and 24,999 rows. Native diagnostic execution took
approximately 2.736 seconds; this is not proof-production timing or an end-to-end
cost claim. Enclosing operational accounting is owned by SMALL-REVIEW.

Evidence paths, relative to the canonical root:

- `experiments/v5-local-checks/small-aggregate-layout-02/evidence/diagnostic.json`,
  SHA-256 `5e9beb1eeb3e4b9c0849309d2501f4a8733715e0d0c30c16bedd6e015c2b5784`.
- `experiments/v5-local-checks/frontier-capability-execution-01/evidence/diagnostic.json`,
  SHA-256 `241e109547b5a23c1ddd4c0eece335d4b053d83ce284f19fc139541f1b7132a4`.

Arithmetic here was recomputed directly from the saved JSON using PowerShell;
no native or product code was imported. Neither diagnostic nor prior failure
was edited. The failed raw segments are not a complete capsule and cannot be
promoted into a proof request by inventing a final session state.

## 2. Why the limit is exhausted

Let `SDK` denote the retained source at
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8`.
The source facts below concern this exact implementation, not every zkVM.

In `SDK/risc0/circuit/rv32im/src/execute/executor.rs`:

1. `ExecutionLimit::segment_threshold` (lines 196–205) is
   `2^po2 - max_insn_rows`, with default `max_insn_rows = 25,000` for po18 and
   po19 (`rv32im/src/lib.rs:46`). The reserve protects a final large instruction.
2. `run_segment` (lines 399–488) resumes, checks the session limit **before**
   the next machine step, and splits when current estimated rows exceed that
   segment threshold. At suspension it rounds the actual used-row count up to
   a power of two. The configured exponent is a maximum, not a rule that every
   final segment must have that exponent.
3. `split_segment` (lines 509–555) adds `2^actual_segment_po2`, not just
   nonpadding rows, to the completed session count. It then resets the pager,
   instruction/preflight counters and block tracker.
4. `get_rows` (lines 956–958) returns

   `completed padded rows + current segment_used_rows`.

The native SDK wrapper maps `ExecutorEnv.session_limit(Some(x))` to
`RowLimit::Hard(x)` in
`SDK/risc0/zkvm/src/host/server/exec/executor.rs:516–526`.
Thus the cap called "cycles" in our interface is operationally a limit on this
SDK row accounting. It is not an instruction budget or only useful guest work.

At the start of the attempted next segment,

`completed padded rows = 256 * 262,144 = 67,108,864 = cap`.

The reported 3,233-row excess is the fresh segment's accounting after resume,
before another ordinary `step` can pass the hard-limit check. It is **not**
evidence that only 3,233 rows of useful computation remained. Since the executor
did not take its already-terminal return, the saved computation had not halted.
For this same execution and splitting policy, any successful completion requires
**at least 257 segments and more than 67,108,864 padded rows**. This is the
concrete lower bound; it is not a finite upper bound on the eventual count.

### There is repeated nonpadding work too

The completed po18 prefix already has **4,326,650 more nonpadding rows** than
the entire completed po19 run. Therefore it is incorrect to explain the saved
row-count difference solely by additional final padding. That observation alone
does not attribute the difference to one subroutine or establish a useful-work
fraction.

The SDK explains why smaller segments can add nonpadding rows:

- `execute/pager.rs:346–351` clears page cache/table/state at each split.
- `execute/block_tracker.rs:229–251` initializes fixed table blocks and a fresh
  PC-decode cache; first use of each instruction address is counted again.
- `execute/block_tracker.rs:345–356` adds page-in, page-out, page-uncle and
  table blocks to the row estimate. `pager.rs:605–608` includes page-cache
  touches plus two reserved pages.
- `executor.rs:550–554` resets those segment-local structures after each split.

More boundaries can therefore charge repeated authentication, tables and
decoding even if the guest's mathematical algorithm has not changed. The saved
diagnostics do not decompose the 4,326,650-row difference into those categories;
do not claim an exact paging attribution without additional evidence.

Likewise, `81,348,253 - 75,132,143 = 6,216,110` is only the difference between
the two recorded machine-instruction totals. It is **not** a proved number of
remaining guest instructions in the po18 run. Segment geometry can affect
machine bookkeeping; the final phase may have different cost density. Scaling
113 to 226, or extrapolating the partial instruction ratio to approximately
278 segments, is not a sound completion bound.

## 3. Alternatives and why not take them first

| Candidate | Source-based disposition |
|---|---|
| Same input and N256 with a few extra session rows | Does not solve the segment-count obstruction. It merely allows progress into a 257th segment that the controller cannot admit. |
| N288/N320/N512 and a larger row cap | A new bounded attempt could be legitimate, but none is proved sufficient by these saved counts. It expands the proof DAG, custody, manifests, serialization and whole-operation envelope. Do not silently widen one constant. |
| Smaller default split reserve | The circuit-level `ExecutionLimit::with_max_insn_rows` exists, but the retained `ExecutorImpl.execution_limit` does not expose it through `ExecutorEnv`. A smaller reserve can cause a large instruction to overshoot and refuse. A safe bound for this workload is not established; this is a new host/SDK execution path, not an unchanged-host tuning flag. |
| Mixed po18/po19 geometry | The circuit-level `run_segment(limit)` API can in principle take per-call limits, but the retained zkVM wrapper uses one fixed environment limit and its `run_segment` is crate-private. Its ordinary supported path already permits a naturally smaller last segment. No per-phase mixed-geometry knob exists on our selected host. Moreover any po19 proof revives the proven >4 GiB constructor obstruction under the candidate 4 GiB cap. |
| Po17 | Reduces row-scaled memory but increases splitting/recursive work; there is no demonstrated need before trying the smaller exact witness. |
| Rewrite witness encoding or guest algorithms | May genuinely reduce rows, but changing the codec/checker generally changes A and requires new correspondence/build/acceptance work. It is not a free reuse of the selected image. An already-supported smaller aggregate witness is materially simpler. |
| Fix retained Rust preflight over-allocation | Useful independent backend work, but no effect on this execution-row failure. The prior source proof still shows po19 C++ allocations alone exceed 4 GiB. |
| Remove the producer's complete-composite finish | Does not affect execution layout or segment count. It is a separate assurance/source choice, already analyzed in FULL-PATH-FEASIBILITY-REVIEW, not a cure for this failure. |

For example, N512 with M8 would permit `H = 3*512 + 8 = 1,544` host stages,
versus 776 at N256/M8. This is not an automatic acceptable price for avoiding
one target-selection check. Even a smaller count-cap successor must recalculate
actual `s,m`, dependency-row limits, capsule retention, complete-composite
bound, input inventories, output census and every stage/whole-operation quote.
The old selected caps and failed evidence stay unchanged.

## 4. Next gate and stopping rule

The smallest worthwhile next gate is semantic, not a broad new benchmark:

1. Establish from the existing aggregate relation that BASE plus FIRST proves
   the **same exact `J_FIRST`** that the public consumer needs. Preserve the
   complete FIRST module and genuine admitted base; SECOND may be omitted only
   because it is a descendant not required by FIRST. Explicitly distinguish
   target identity from the changed aggregate header and DAG identity.
2. Use the unchanged codec and supported relation to define a fresh smaller
   input. Verify the target/header binding and actual guest image before any
   execution selection. Do not shorten an arbitrary byte string and infer
   validity from size alone.
3. If selected, retain a fresh one-execution capsule under the existing bounded
   po18/N256 implementation. A successful capsule supplies actual `s,m`, row
   counts, sizes and final target binding for a proof-feasibility quote. Failure
   stops that operation and remains charged; it does not trigger a cap ladder.
4. Only then choose finite proof work. The 2.6650390625 GiB po18 source lower
   bound from PROVER-MEMORY-REVIEW is still **not** a peak-memory upper bound or
   proof that the candidate 4 GiB cap suffices. Reuse prior controller tests and
   native-manifest source review; do not repeat passing controls or launch the
   manifest gate without its required complete capsule.

If the target-preserving smaller witness is unavailable or still exceeds the
envelope, root must make a new explicit resource/architecture decision. At that
point compare a precisely coupled larger count profile, a justified execution
optimization and an actually provisioned external producer. Do not report
another narrow component pass as the deployable-v5 outcome.

## Reused analysis

- [PROVER-MEMORY-REVIEW](../v5-2026-10-16/PROVER-MEMORY-REVIEW.md): memory lower
  bounds; no repeated po19 experiment is useful under a 4 GiB cap.
- [SMALL-SEGMENT-DESIGN](../v5-2026-10-16/SMALL-SEGMENT-DESIGN.md): geometry,
  count, identity and orchestration coupling.
- [FULL-PATH-FEASIBILITY-REVIEW](../v5-2026-10-16/FULL-PATH-FEASIBILITY-REVIEW.md):
  complete-composite versus optional frontier-only finish.
- [PRODUCER-NEXT-DECISION](PRODUCER-NEXT-DECISION.md): original finite N256
  design; its actual completion uncertainty is now resolved negatively for the
  old full witness, without rewriting its historical selection.
