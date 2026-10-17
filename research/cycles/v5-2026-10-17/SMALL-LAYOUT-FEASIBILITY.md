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

## Appendix: po18 producer memory and the smallest useful correction

2026-10-17, `memo_independent_review`; source/data review only. This appendix
preserves the original layout conclusions above. The selected BASE+FIRST layout
has since completed with 167 po18 segments, one genuine I premise and a
32,965,324-byte capsule. Execution success is not a certificate or proof-memory
qualification. No SDK edit, build, proof, experiment or Git mutation was made
for this analysis. `SDK` is the retained source root identified above; `CXX`
means `SDK/risc0/circuit/rv32im-sys/cxx`.

### Decision at the observed capacity

**Do not select an unchanged 4 GiB proof worker on the strength of the old
2,729 MiB lower bound.** At root's observed approximately 2,780 MiB physical and
4,797 MiB system-commit headroom, already identified simultaneous payloads
exceed free physical memory before the capsule, runtime and thread stacks.
This does not prove allocation failure: virtual memory can page, and available
commit differs from free physical memory. It does rule out a justified promise
of resident, efficient execution at that observation. Neither a larger CPU
allowance nor repeated attempts creates memory headroom.

The high-payoff next candidate is a **host-side Rust witness-allocation unit
correction**, not another guest or layout redesign. It removes exactly 459 MiB
of requested vector payload at po18 while retaining the same trace prefix,
guest image, circuit, verifier and statement. It needs a fresh reviewed SDK
artifact and downstream relinks; it is not a flag on the frozen executable.
Alternatively, use a genuinely provisioned producer with adequate headroom.
Neither route is selected by this appendix, and neither yet proves a 4 GiB
upper bound or full-operation affordability.

### Accounted persistent payload, including the previously omitted FRI

Let N = 262,144, D = `computeMaxDataPerRow()` and A = `computeTotalAccum()`.
The prior source argument establishes D >= 198 and A >= 84, not equalities.
`CXX/zkp/taps.cpp::TapManager::done` groups columns by their exact back-offset
vectors. `prove/rv32im.cpp` supplies only `{0}` and `{0,1}`. Thus there are two
ordinary combos and one additional check combo: exactly three, not a quantity
that grows with the theorem or segment count.

The following are distinct simultaneously retained requested payloads, not
allocator-inclusive process memory:

| Persistent item | Bytes |
|---|---:|
| Data and accumulation table/coefficient/expanded matrices | 24(D+A)N |
| Current Rust auxiliary vector | 2,448N |
| C++ auxiliary array | 612N |
| Check raw array and separate expanded matrix | (64+256)N |
| Three data/accum/check Merkle trees | 768N |
| Lookup tables | 80N + 263,168 |
| Three combo columns | 48N |
| Initial FRI coefficients | 16N |
| All FRI round matrices/trees/outputs, plus final copy | 81(N+N/16+N/256) + 1,024 |
| C++ and Rust row metadata | N times their two `RowInfo` sizes; 16N on the selected ABI |

For a FRI round of input degree r, `prove/fri.cpp` allocates 64r bytes of
evaluations, 16r bytes of Merkle nodes and r bytes of output coefficients.
The next round aliases that output; do not count it twice. The retained
parameters are expansion 4, extension 4, fold 16 and minimum degree 256.
Po18 therefore has exactly the three degrees N, N/16, N/256, terminating at
64. All rounds are built and retained together. Their combined payload,
including the final copy, is 22,644,736 bytes (21.595703125 MiB).

Excluding row metadata and small arrays, the table sums to

`[24(D+A)+4,292]N + 81(N+N/16+N/256) + 264,192`.

Using only the proved D/A minima gives **2,922,220,544 bytes =
2,786.8466796875 MiB**. The two 8-byte row-metadata arrays add 4 MiB, giving
**2,790.8466796875 MiB**, still before small arrays and host state. CPU pinning
is a view, and the inspected NTT/expansion routines work in place: no additional
full matrix copy should be invented for those operations. The CPU witness and
check dispatchers use row-local contexts and `parallel_map`; their large
`RegImpl` array types are views into the existing matrix through casts, not
fresh per-thread copies of the entire matrix.

### What still prevents a useful whole-process upper bound

This is a concrete remaining accounting list, not an assertion that FRI is
unknown or that all omitted work is an arbitrary extra matrix:

1. **Exact circuit maxima D/A.** `rv32im/emu/blocks.cpp:86-129` computes D from
   all 43 instantiated block layouts and A from their recursively visited
   argument counts. Their definitions are finite and independent of the guest,
   but this review has not completed that layout/argument census. Replacing
   the existing minima by equalities would understate memory.
2. **Small circuit objects and transcript/verification lifetime.** The exact
   tap total including the check group is E = D+A+44: the extra 28 come from
   four back-tapped ordinary accumulation columns and the 24 top columns.
   `poly_group.cpp` retains 36E bytes of tap arrays and 4(D+A+16) bytes of
   combo selectors; `prove.cpp` retains 32E bytes of eval arrays and four
   `DivideInfo` records, plus globals/mixes. Merkle query scratch is fixed by
   `4*(8*steps+columns)` per tree. In addition there are vectors/maps/object
   overhead, two E-element temporary vectors, interpolation scratch, and
   transcript capacity/copies. `rv32im/ffi.cpp` verifies while its C++ prover
   remains live; `rv32im/src/prove.rs` copies the transcript into Rust and
   verifies before that prover is destroyed. Those verifier allocations and
   all transcript capacities still need a bound.
3. **Host capsule and parent state.** `aggregate_small/stage_host.rs:449-468`
   decodes the entire capsule into 167 segment objects and retains them across
   `prove_segment`; it drops raw capsule bytes, not those objects. Encoded
   32,965,324 bytes is not a proved decoded-memory bound. Header/wire, verified
   parent receipt copies, ordered assumptions and the manifest/cache also
   contribute. The earlier raw-plus-decoded acquisition peak is a separate
   phase, not automatically additive to the proof peak.
4. **Preflight-phase state.** `SegmentContext::new` clones selected partial
   image/read/write records. `preflight/emu.rs` creates its `PagedMemory`, a
   `Vec<Option<PageDetails>>`, instruction cache and page state; `paging.rs`
   allocates boxed per-page `MemoryInfo` arrays. These coexist with Rust
   row/aux buffers during preflight. The context/emulator are dropped before
   the C++ constructor (`zkvm/.../prove/prover_impl.rs:218-246`), so the
   correct expression is a maximum of phase peaks, not a sum of all live
   objects ever seen. Heap retention can nevertheless keep committed memory.
5. **System/allocator and threads.** `core/util.h::parallel_map` creates up to
   `hardware_concurrency()` threads, then joins them. The worker process-count
   cap does not cap thread stacks. Stack commitment, loaded image/runtime,
   allocation rounding/fragmentation and freed-block retention depend on the
   exact build/runtime/OS. Other applications' changing headroom is separate.

Thus a schematic bound is `host + max(decode, preflight,
prover-persistent + proof/verification scratch) + allocator/runtime`, with the
terms above still to be instantiated. The existing observed base-I po18 peak
3,534,692,352 bytes (about 3,371 MiB) is useful feasibility context, **not an
upper bound for this aggregate or a reason to infer fit at today's headroom**.
No memory-limited probe is needed to rediscover the already known obstruction.

### Exact unit correction and ownership argument

The affected source is `SDK/risc0/circuit/rv32im/src/prove/preflight.rs`:
`compute_max_wit_per_row` at lines 36-58 computes the maximum of witness
**byte** sizes times row multiplicities; `MAX_WIT_PER_ROW` at line 60 is 612.
Line 159 uses `rows * MAX_WIT_PER_ROW` as a count of **u32 elements**.
Line 179 truncates the vector length but leaves its allocation capacity live.
A fresh successor can instead express the maximum in u32 words, with explicit
divisibility/overflow conditions, allocating 153N zeroed words rather than
612N. Do not edit the retained file in place or use unsafe layout access.

The refinement argument is local: `preflight/trace.rs:105-134::add_block`
asserts witness-size divisibility by `sizeof(u32)`. Each new row reserves
`count_per_row * witness_bytes / 4 <= 153` words, including the Globals row;
the row buffer has N entries. Consequently every successful old trace accesses
only the first 153N words. Both allocations zero that entire accessible prefix;
the same writes, row metadata, offsets, truncated length and witness values
follow. An oversized row count already refuses through the row indexing; no
new out-of-bounds trace is admitted by the reduction.

FFI uses `preflight.aux.as_ptr()` and **length**, not capacity, in
`rv32im/src/prove.rs:63-75`. The vector remains owned and immobile through the
synchronous call. `CXX/prove/rv32im.cpp:120-130` copies exactly that supplied
length into its independently allocated 153N-word array. The pointer can change
between implementations; its lifetime, alignment, length and contents may not.
The corrected allocation therefore changes no accepted trace bytes, C++ circuit
constraints, verifier parameters, guest ELF/image A, statement, geometry or
existing capsule. Its host-library/executable hashes and producer profile do
change. Identical accepted mathematical claims are required; byte-identical
proof files are not assumed without establishing the prover's determinism.

Requested-payload saving is `4*(612-153)N = 1836N = 459 MiB` at po18. The
identified-payload lower bound above becomes **2,331.8466796875 MiB** after
including row metadata. This is not a prediction of actual peak, and a 459 MiB
reduction in requested payload is not a guarantee of the same decrease in OS
peak working set. It is a structural saving on every po18 segment, not just
the selected theorem. The same correction does not make po19 fit under 4 GiB;
the prior C++-only impossibility remains.

There is no supported zero-rebuild shortcut: public `PreflightResults.inner`
is `pub(crate)` (`zkvm/src/host/server/session.rs:147`), and its public methods
only return index/po2/counts. `shrink_to_fit` is allocator-best-effort, not a
hard upper bound, even if exposed. Switching to private `preflight_cxx` is a
different emulator path; CUDA/Metal selection is compile-time and unavailable
in the retained Windows CPU artifact. Those alternatives have larger assurance
cost than correcting this one allocation unit.

### Minimal fresh rebuild frontier and decision-changing follow-up

Retained target fingerprints and
`experiments/v5-local-checks/proof-validation-integration-build-01/compile-commands.json`
show the conservative dependency frontier:

`risc0_circuit_rv32im -> risc0_zkvm -> dmkn_module_relation -> dmkn_aggregate_relation -> small stage host`.

For the selected stage host this means **four Rust rlib rebuilds and one final
executable compile/link**, not one host-only relink. Only the first crate's
allocation source changes; dependent sources remain byte-pinned. The module
relation directly names `risc0_zkvm`, so mixing its old crate identity with a
new zkVM dependency is not an admissible shortcut. Reuse the unchanged nanoda
checker rlib, C++ rv32im/recursion/keccak native archives, other pinned Rust
dependencies/proc macros, exact toolchain/target/feature/link settings, and
retained generated `preflight_opt_gen.rs`/build-script output where the new
recipe supports it. No C++ circuit rebuild, guest rebuild, capsule reexecution,
new image or old receipt regeneration is logically required. The existing
snapshot executable can remain frozen and continue to identify the retained
capsule. Rebuilding the old `commons-local-prover` executable is unnecessary
unless separately selected.

This is a dependency-frontier count, not a promise that moving a Cargo target
directory will perform exactly five commands. Paths/fingerprints/build-script
environment can trigger more work. A fresh explicit build recipe must bind the
retained Cargo.lock, source snapshot, generated inputs, library closure and
compiler environment without mutating the old target; ordinary crate metadata
and direct-dependency compatibility must be checked before launching. The used
`aggregate_small/build_stage.py` specifically requires unchanged old libraries,
so it cannot be silently reused as authority for this new chain.

Generic independently funded proof renewal remains architecturally practical:
bounded po18 segment stages limit peak dependence on selected execution size,
while the staged DAG charges total work and retained checkpoints. It does not
make arbitrary useful contributions affordable, and 502 quoted stages for this
actual frontier are not funded work or positive full-cost growth. Prefer the
allocation refinement plus a justified producer envelope over repeated
memory-bound attempts or another smaller-geometry/cap ladder. Once separately
selected, the narrow discriminator is old/new trace-prefix equality and one
genuine segment accepted by the unchanged verifier, with actual memory/time
accounting; no broad already-passing campaign needs repetition. Full recursive
completion, public reciprocal use and a full-cost benefit region remain open.

Additional reproducibility pins (prior pins remain in PROVER-MEMORY-REVIEW):

| Source | SHA-256 |
|---|---|
| `CXX/prove/fri.cpp` | `0ed0036c1497c5958cf5b7a33c1f20082d177f9666120030018e3fb519f6cb5e` |
| `CXX/zkp/taps.cpp` | `1057d69e8e9069ef14bb6417f91f453d835cfe403a02e311e3c47686d1b83a8a` |
| `SDK/risc0/zkvm/src/host/server/session.rs` | `804d7b7ea33b76a4a7e2e107ff28646e69bca232dae9a2e8f66361666fdb5a8d` |
| `software/v5/aggregate_small/stage_host.rs` | `975e68dfbc8d091733cee72a18d81fb45617886585f1806fe9425cf4aa847955` |
