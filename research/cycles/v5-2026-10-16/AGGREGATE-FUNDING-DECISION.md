# Aggregate funding decision: do not launch an infeasible po19 proof

Owner: `v5_growth_decision`, independent source/data-only review, 2026-10-16.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This note is a funding recommendation, not execution authority. No product import,
proof, native execution, build, test or Git operation was performed for it.

## Decision

**Do not fund the proposed five-stage aggregate prefix, or the full A proof,
under the current 4,096 MiB stage ceiling.** A lower bound from the retained CPU
prover source already exceeds that ceiling. Testing this predictable refusal has
low decision value. The freshly implemented aggregate controller and one-link
host remain useful; their passing controls/build do not establish proof feasibility.

The bound is not a doubling of a historical process peak. It counts disjoint,
simultaneously live allocations in the backend actually linked by the host.
Independent challenge is assigned to `memo_independent_review`; root owns adoption.

## Exact object and backend

Reuse the complete A capsule from
`experiments/v5-local-checks/frontier-capability-execution-01`:

- A image ID `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`;
- 113 segments, one genuine I premise, segment exponent 19;
- capsule 37,187,089 bytes, SHA-256
  `7996306944a51e0eec597266819871115f4bdea1f799c944442e472869465ffd`;
- session binding `bdd42310ed62504e78e4da164b633da7751597eda74eb00b873a06c552268649`;
- capsule binding `28908f4aaf31d289c374047129dbf5c1e65c36def34ea877a59366b3185732f9`.

The linked SDK source root, abbreviated `SDK/` below, is
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/`.
It is the retained vendor source, not an assumed current upstream release.
The host links `librisc0_zkvm-e4b4822463e0ff62.rlib` from the same retained build.
The current stage host calls `get_prover_server(...).prove_segment(...)` with
development mode false. On this non-CUDA Windows build, RV32IM chooses the CPU
prover, not a GPU or dual prover.

## Source-derived memory obstruction

Let `n = 2^po2`. The following are live together during construction/use of the
CPU prover. Each row below is a lower bound, not a total-memory prediction.

| Disjoint allocation | Lower bound in bytes |
|---|---:|
| Retained Rust preflight `aux` capacity | `2448 n` |
| C++ prover's separate `aux` | `612 n` |
| Data table, coefficient table, fourfold expanded table | `4752 n` |
| Accumulation table/coefficient/expanded storage, counting only `AccumTop` | `576 n` |
| **Subtotal** | **`8388 n`** |

At po19 the subtotal is **4,397,727,744 bytes = 4.095703125 GiB**, already
102,760,448 bytes over 4 GiB. It excludes row descriptors, the other accumulation
columns, check-polynomial arrays, Merkle trees, FRI arrays, lookup tables, thread
stacks, the decoded capsule, executable/runtime state and the process wrapper.
Thus even this deliberately weak lower bound rules out the current profile.

Derivation and source anchors:

1. `SDK/risc0/circuit/rv32im/src/prove/preflight.rs:39` computes the maximum
   `size_of::<Witness>() * count_per_row` **in bytes**. `P2BlockWitness` is
   204 bytes and its per-row count is three, so the maximum is at least 612.
   At line 159, however, `vec![0u32; rows * MAX_WIT_PER_ROW]` allocates that many
   **u32 elements**, giving at least `4 * 612 * n` bytes. The later `truncate`
   changes length, not allocation capacity; the returned `PreflightContext`
   remains live through `prove_preflight` and `prover.prove(&preflight.inner)`.
   The retained generated binding explicitly asserts the 204-byte size at
   `target/x86_64-pc-windows-msvc/release/build/risc0-circuit-rv32im-sys-93d06bb7698b10ee/out/bindings.rs`
   below `experiments/general-checker-host-05/build-01/`.
2. `SDK/risc0/circuit/rv32im-sys/cxx/rv32im/witness/block_types.h` gives
   `P2Block, 3` and `P2IntRounds, 2`; `witness/poseidon2.h` gives the 204-byte
   structure (three 32-bit words plus two 24-element field arrays).
   `cxx/rv32im/emu/blocks.cpp:76` divides witness size by `sizeof(Fp)` before
   computing its maximum. `cxx/prove/rv32im.cpp:117` allocates a separate C++
   `uint32_t` aux array of `n * computeMaxWitPerRow()` words: at least `612 n`
   bytes. It is not a view of the Rust aux allocation.
3. `cxx/rv32im/circuit/poseidon2.h:49` has `P2IntRoundsBlock` with
   `1 + 24 + 21 + 21 + 24 = 91` field-sized registers. With two blocks and
   two validity flags, plus major/minor selectors `6 + 8`,
   `computeMaxDataPerRow()` is at least 198. The selector count follows from
   43 named block kinds plus Empty. `cxx/prove/prove.cpp:67` allocates both
   `n x cols` table and coefficients, while `cxx/prove/poly_group.cpp:28`
   allocates `4n x cols` expanded storage. These are retained together, hence
   `4 * (1 + 1 + 4) * 198 n = 4752 n` bytes.
4. `cxx/rv32im/circuit/top.h:34` contains `AccumTop`: seven one-hot bits,
   one register and four four-register extensions, i.e. at least 24 field
   cells. `computeTotalAccum()` includes this plus further accumulation
   storage. Applying the same six-table-row factor gives at least `576 n`.
5. `cxx/hal/cpu/hal.cpp:55` backs each buffer by a separate `new char[size]`
   and zeroes it. `hal/hal.h:162` allocates matrix bytes, rather than lazily
   representing them. `cxx/core/util.h:91` uses up to hardware-concurrency
   threads, joined per call; limiting process count does not limit these
   threads or remove the arrays. No second simultaneous segment is needed
   for the obstruction.

Relevant SDK entry path: `zkvm/src/host/server/prove/mod.rs:85` obtains a
preflight result and passes it to `prover_impl.rs:243`; that implementation
constructs the RV32IM prover while the preflight result is retained.
The witness-allocation unit mismatch is a potential optimization lead, not
permission to modify the retained SDK or evidence. Even repairing it does not
by itself prove the remainder fits; the other large arrays need accounting.

### Independent challenge strengthens the obstruction

The independently assigned reviewer found a stronger lower bound, and this
owner re-read the relevant `InstLuiBlock::addArguments` source. That function
always contributes two pulls and one push. Nine instances per row give at least
27 arguments, so `computeMaxAccumPerRow()` is at least
`4 + 4 * ceil(27/2) = 60`. Including `AccumTop` gives at least 84 accumulation
columns. The group tables therefore require at least
`24 * (198 + 84) n = 6768 n` bytes. Add C++ aux `612 n`, checkRaw `64 n`, its
expanded table `256 n`, and three distinct Merkle trees `3 * 256 n`:

`M_CPP >= 8468 n`.

At po19 this is **4,439,670,784 bytes = 4.134765625 GiB in the C++ constructor
alone**. This proof does not depend on the Rust allocation mismatch. Repairing
that mismatch, shrinking the preflight vector, or dropping it as soon as copied
cannot by itself make this backend fit 4 GiB. Including the current Rust aux
gives the stronger combined lower bound **5,723,127,808 bytes = 5.330078125 GiB**,
still excluding several live arrays and overhead. This is not an 8 GiB
sufficiency proof. The independent [PROVER-MEMORY-REVIEW](PROVER-MEMORY-REVIEW.md),
SHA-256 `2a6bf2fbfdf6267f1aa18aded422b4f99817764538e6ae6ede81c4e9d9070843`,
preserves their source anchors and aliasing checks for root adoption. Shared
views such as `gs.expTable` are not counted twice; `checkRaw` and its coefficient
view are counted once, and the three counted Merkle trees are distinct.

## Numeric full-path quote, conditional on a different feasible backend/profile

This shows why a syntactically fitting request is not sufficient. It does **not**
recommend running the present profile, nor predict actual A cost.

For `s = 113, m = 1`, the graph has 340 host calls / 339 prover calls:
113 segments, 113 lifts, 112 joins, one resolve and one finish.
The following CPU caps fit the current aggregate worker ceiling:

| Kind | Count | CPU cap each | Reserved CPU |
|---|---:|---:|---:|
| Segment | 113 | 1700 | 192100 |
| Lift | 113 | 250 | 28250 |
| Join | 112 | 250 | 28000 |
| Resolve | 1 | 600 | 600 |
| Finish | 1 | 300 | 300 |
| Total | 340 | | **249250** |

Whole allowance: worker at most 250000 CPU seconds; controller at most 3600;
wall at most 86400 seconds; retained output at most 2 GiB / 8192 entries;
at most 17 attempts, with all earlier attempts and successful checkpoints
carried forward. The controller enforces exact same-profile/session/budget
lineage; ordinary continuation cannot silently increase any cap.

Example per-stage wall caps 420 / 150 / 150 / 600 / 120 seconds respectively
sum to 81930 seconds. This leaves 4470 seconds for controller and between-call
work inside the day, but is not a proof of completion: enforced ceilings can
refuse a legitimate expensive stage, and controller CPU does not bound all
wall-time waiting. The illustrative CPU quote leaves only 750 worker CPU
seconds beyond a successful path at every cap, so costly failed retries would
need actual successful-stage slack, not a renewed allowance.

Example artifact cap 1 MiB per stage and stdout/stderr cap 1 MiB each give the
controller's conservative output expression `340 * 5 MiB + 4 MiB = 1704 MiB`
and entry expression `340 * 8 + 4 = 2724`. Repeated attempts also retain report
tails, control files and charged actual failures; those must remain inside the
same allowance. These caps exceed historical ~224–235 KiB proof artifacts but
are still caps, not guarantees of A artifact size.

Fixed per-host read bytes are image 1,745,920 + wire 215,540 + H 192 + capsule
37,187,089 + I receipt 223,594 = **39,372,335 bytes**. Finish reads all 113 segment
proofs plus final resolution, so at 1 MiB each its host-read bound is
**158,909,999 bytes**, below 512 MiB. The separate request inventory limit also
counts every retained checkpoint, prior report and adopted snapshot records;
that check must be calculated from the exact future request, not inferred from
the finish bound. Its nominal 340 MiB of artifacts leaves about 134 MiB after
the fixed data, but duplicated evidence pins and reports still matter.

Historical base I production (po18; 110 segments, no premises) cost
127958.078125 worker CPU seconds and 691.15625 controller CPU seconds including
its carried prefix. The 325-stage later portion had maximum observed segment
973.03125 CPU / 129.9140678 wall seconds and peak Job private commit up to
3,534,692,352 bytes; lift/join maxima were 187.359375/199.59375 CPU seconds.
Those observations are **context, not A predictions or success bounds**.
The current po19 obstruction is established separately above.

## Prospective stop rule

**Current stop point: before segment zero.** There is no rational five-stage
pilot inside a memory envelope already contradicted by source.

After a separately reviewed feasible backend/profile is selected, a minimal
prefix can have decision value. It must reuse the adopted capsule if geometry
is unchanged, retain successes, and stop on the first native refusal, missing
artifact, exceeded envelope, uncertain closure, invalid binding, or exhausted
allowance. It must not automatically retry or enlarge budgets. Continuing is
conditional on exact remaining-graph envelopes fitting remaining resources,
not a single sample's mean extrapolation. A successful prefix does not establish
full production cost or a positive growth benefit.

## Next architecture choice

The 4 GiB producer ceiling is a local implementation choice, **not a project
requirement that every lightweight participant produce succinct proofs**.
Making it universal would unnecessarily dictate the backend and discourage
specialized providers. The current source-level choice should be:

| Route | Implementation/refinement cost | Recurring tradeoff | Decision now |
|---|---|---|---|
| Explicitly provisioned higher-memory producer profile | New bounded controller/resource policy; same mathematical guest, retained SDK and complete capsule | Preserves 113-segment graph; needs real available memory/commit headroom | **Preferred source-only next design if an adequate operator profile is intended** |
| Smaller po18/po17 segments | Fresh bounded snapshot/stage/controller geometry; new capsule, same guest | Less per-segment memory but more lifts/joins, checkpoints and repeated host preflight | Supported alternative; complete bound mapping before choosing |
| Correct Rust preflight units only | SDK successor, rebuild and renewed correspondence/qualification | Saves wasted Rust memory but C++ alone still exceeds 4 GiB at po19 | Not a solution to the present 4 GiB obstruction |
| Stream/reuse C++ prover buffers | Substantial backend lifetime/algorithm changes and new assurance work | Potential lasting memory savings, possibly extra recomputation | Defer unless producer capacity/operating economics justify that investment |

Root's read-only capacity observation at this decision was about 2.86 GiB free
physical memory and 3.79 GiB free virtual/commit availability on a 15.67 GiB
machine. It is not a reservation or a permanent hardware limit, but it prevents
assuming a larger producer can safely launch now. Do not alter other processes,
pagefile or system settings as a workaround. No larger resource allocation is
authorized by this note.

For smaller segments, 226 is only a rough illustration from twice the old
segment-row capacity, not a derived future segment count. At `s=226,m=1`, the
graph would have 679 host calls / 678 proving calls, and the 1 MiB artifact/log
quote above would reserve 3399 MiB, exceeding 2 GiB. Smaller separately justified
log/artifact limits could repair that particular envelope (512 KiB artifact,
64 KiB each log gives `679 * 2.625 MiB + 4 MiB = 1786.375 MiB`), but CPU,
capsule size, finish reads and full inventory still require a new calculation.
Do not change only the number 128 and assume the full pipeline is ready.
The disjoint `memo_tests_review` assignment maps these geometry bounds.

The preferred source change is an **explicit, preselected finite producer
resource policy**, not automatic budget escalation. Bind the chosen ceilings
into profile/attempt identity, preserve same-budget continuation, and separately
screen an actual selected backend/segment geometry against a source-bound
resource quote. A dedicated producer may have larger resources; a receiver must
not inherit those producer requirements.
Cap increases remove an implementation obstruction but do not supply resources
or prove affordability. Actual execution still needs an exact finite selection.

### Minimal generic profile-only refinement

Root requested the smallest policy change, not a generic memory predictor.
The recommended fresh successor has:

- A distinct aggregate `PROFILE_V2` schema and one **required** local-owner field
  `stage_memory_ceiling_mib`, an exact integer in `1..8192`. There is no missing-
  field fallback or ambient-environment override. Selecting 4096 preserves the
  old ceiling explicitly; old V1 used bytes remain frozen.
- The unchanged per-stage request field `memory_mib`, now checked against that
  chosen profile ceiling. All other `P.COMMON` limits, stage CPU/wall ceilings,
  total allowance bounds, input/output bounds and graph rules stay unchanged.
- The existing full canonical profile encoding remains hashed into `profile_id`
  and checked for mutation. Prior reports already require exact `profile_id`,
  session, allowance, budget, carry and complete prior-history equality.
  Therefore a larger ceiling creates a new profile; it cannot silently extend
  an earlier same-allowance history. Reuse of independently produced valid
  cryptographic checkpoints remains a separately explicit owner decision.
- No new memory estimator, capsule parser, backend patch, trust protocol or
  automatic scheduling choice. In particular, `session.po2` is a geometry
  **upper cap**, not in general every segment's actual exponent. Do not embed
  `8468 * 2^session.po2` as a universal product refusal. The refusal established
  above concerns the retained actual capsule/backend quote; future exact segment
  floors belong in the separate owner selection/resource analysis.
- A required field does not constitute proof of resource availability. The
  8192 maximum is an admissible supervisor policy ceiling, **not a claim that
  8 GiB suffices for the selected proof**, and no run is selected now.

This reuses the actual preserved helper
`product-local/v4-library-commons-02/commons-v4/operator/commons.py`:
`CEILINGS.memory_mib = 8192` (line 24), `limits_checked` (line 115), and
`supervise` (lines 166–195) pass the chosen integer to the retained Job class.
The standalone stage CLI's different limit is not on this invocation path.
No SDK, supervisor or Job rebuild is needed for this policy-only change.

Focused future controls need cover exact missing/wrong schema/boolean/out-of-
range refusal, equality at the owner ceiling, refusal above it, unchanged
non-memory limits, profile mutation and same-allowance profile/budget mismatch.
They should inspect the captured limit passed to the synthetic supervisor;
allocating multi-gigabyte memory or producing a real proof is unnecessary to
test this policy refinement. Root owns source selection and any controls.

The distinction matters to the final architecture: receiver succinctness does
not imply cheap or low-memory proof production. Producer capabilities and
capacity admission must be explicit, replaceable and separate from mathematical
acceptance. This is still one capability investment, not proof of economic or
sustained useful growth.
