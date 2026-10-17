# Next frontier investment: one complete-execution opportunity before a rewrite

2026-10-16. Requested source-only decision by `memo_tests_review`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No code, build, execution, proof, runtime selection or Git mutation is made here.

## Recommendation

**After the current client boundary is resolved, prefer one deliberately funded
execution-only capability attempt over immediately implementing typed rows.**
Use the already adopted memo image and retained two-delta mathematics. Change
only the selected execution geometry and diagnostic mode in a fresh owner
adapter; do not rebuild the guest, rewrite its relation, repeat I production or
start a proof campaign. The proposed single envelope is given below.

This is a bounded value-of-information judgment, not a numerical expected-value
calculation: neither completion probability nor whole-run typed-row savings is
known. A complete execution would expose the actual layout needed for the next
central trust-boundary decision. An immediate typed-row rewrite first requires
a substantial new parser/correspondence refinement, implementation, differential
controls, build and another image adoption, yet still might not produce that
layout. Existing failed prefixes do not establish that this rewrite is necessary
to obtain it. Its stronger long-term representation argument remains reserved
in [AFFORDABLE-FRONTIER-DECISION](AFFORDABLE-FRONTIER-DECISION.md).

The attempt must be treated as **one named capability investment**, not the next
rung of a doubling loop. If it fails, preserve it and make a new source/design
decision. This note selects no retry, larger cap, proof funding or success claim.
It does not replace the affordable recurring seal requirement with willingness
to pay arbitrarily for one certificate.

## Concrete jointly admissible envelope

The smallest simple extension proposed here doubles the previous power-of-two
session allowance and raises segment size by one bit. “Smallest” means this
specific conservative, no-format-change configuration; it is **not** a proved
minimum sufficient budget. The required full execution cost is still unknown.

| Dimension | Proposed single selection | Source/decision basis |
|---|---:|---|
| Guest/image | memo A `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60` | Adopted build/assembly; no guest change |
| Mathematical input | retained 215,540-byte two-delta wire, three exact members, one genuine I premise | Only the already selected A slot is rebound as before |
| Session argument named `cycles` | `2^26 = 67,108,864` | Existing host/stage format allows `1..2^28`; SDK actually interprets this as a hard row limit |
| Segment `po2` | `19` | Existing host/stage accepts `12..20`; avoids retaining the previous 128 × `2^18` geometry |
| Diagnostics | `stats` | Supported host mode; no additional deterministic PC sampling campaign |
| Segment count | at most 128 | Unchanged host and staged-producer format bound |
| Retained segment bytes, combined | at most 64 MiB | Unchanged `SegmentStore` checked sum |
| Complete capsule bytes | at most 64 MiB | Separate unchanged serialization/write bound |
| Diagnostic bytes | at most 8 MiB | Unchanged host bound |
| Inner native timeout | 120 seconds | Existing screen timeout retained; not a completion prediction |
| Enclosing aggregate CPU/wall | 180 / 240 seconds | Existing finite screen allowance retained, not increased |
| Enclosing memory/processes | 3,072 MiB / 3 active processes | Existing allowance retained; native threads are charged inside the process/Job |
| Native stdout/stderr | 1 MiB each | Existing screen log bounds |
| Screen evidence payload census | 144 MiB / 160 entries | Existing inner screen bound; excludes separately accounted source snapshot/outer wrapper metadata |
| Guest executions / proof calls | at most 1 / exactly 0 | No fallback, proving or automatic continuation |

The unchanged snapshot executable is
`experiments/v5-local-checks/aggregate-host-build-01/aggregate_host.exe`, SHA-256
`b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1`.
The current memo image file is 1,745,920 bytes with SHA-256
`98686ced7979d55685c648f441f7ffbe40712e327a1311f9cb076a0c7250e773`;
its executable image ID above is a different identity.
Retain the same actual I receipt, expected H/member semantics, native preflight,
parent verification, input/output bindings and clean-closure requirements.

The current `aggregate_host/snapshot.py` hard-codes `2^25`, `18`, and
`pc-samples`. It is used/frozen and cannot implement the proposal by changing a
configuration file. Root would need a fresh narrowly selected adapter with the
new literal geometry/mode and corresponding report fields, a fresh configuration,
selection and output path. No Rust source, format, mathematical limits, guest
image, staged checker or receipt acceptance needs changing for this screen.
Exact source/launch review remains necessary.

## Why cycle, segment and storage limits must be considered together

The previous memo failure was `33557665 >= 33554432`, with 128 retained
segments, every retained segment at `po2=18`. Increasing only the session cap
while keeping that geometry risks the unchanged 128-segment callback refusal
before the new cap can be useful. Raising the hard row limit to `2^28` with
the maximum `po2=20` is not a coherent claim of 268-million-row capacity:
128 full such segments contain only `2^27` padded rows. The declared format
maxima are independent validation ceilings, not a promise that every maximum
combination can finish and be saved.

The retained SDK gives a more precise explanation than treating `cycles` as
machine instructions:

- `zkvm/src/host/server/exec/executor.rs::execution_limit` translates the
  session argument to `RowLimit::Hard` and selects the requested segment po2.
- `circuit/rv32im/src/execute/executor.rs::get_rows` adds already padded segment
  rows to current used rows. `run_segment` checks the hard session bound before
  continuing instructions; `split_segment` charges `1 << segment_po2` rows.
- For this geometry the default split threshold is `2^19 - 25,000`, which is
  above `2^18`; ordinary nonterminal size-triggered splits round to `2^19`.
  The aggregate guest does not explicitly pause. The proposed 128-segment
  format therefore has the nominal padded-row capacity `128 × 2^19 = 2^26`,
  whereas the previous geometry had only `2^25`.

These facts establish compatible geometry and remove a known unchanged ceiling;
they do not prove that this mathematical computation finishes before any limit.
Actual consecutive indices and each segment's po2 are still checked. No argument
here replaces those checks with a predicted segment count.

The saved prefix has 24,582,405 segment bytes. It is **not** legitimate to scale
that by two and assert the full execution will fit 64 MiB: later page accesses,
read/write records, different segment boundaries and execution phases can change
bytes per row. Likewise a segment sum at 64 MiB leaves no room for the complete
capsule's extra fields. Segment custody and capsule serialization are separate
enforced bounds; either can refuse. The small fixed inputs plus two 64 MiB
payload limits, 8 MiB diagnostic and two 1 MiB logs leave more than 5 MiB within
the 144 MiB inner census for configuration/header/report overhead. The fresh
adapter must retain the existing exact small-field bounds and final census.

The capsule writer materializes all resolved segments and its serialized output.
Neither bincode's byte limit nor row/count limits prove a total decoded-heap
bound. The 3 GiB enclosing memory limit is an explicit finite refusal boundary,
not assurance that the operation fits it. Keep actual allocation/exit/closure
failure distinct from mathematical rejection. These Job controls are not a
hostile-input OS sandbox.

No elapsed-time estimate is extrapolated from the approximately six-second
failed screen. The retained CPU/wall allowances bound the investment; they do
not quote successful runtime. Switching `pc-samples` to `stats` avoids repeating
diagnostic work but is not a benchmark or a measured speedup claim.

## What a successful execution would actually unblock

A valid outcome requires all of the following in the same selected operation:
exit 0 and clean closure; exact A/H/ELF/WIRE/parent bindings; halted successful
guest with exact committed H; exact verified assumption order; a **complete**
consecutive segment census; complete `DMKNAS01` capsule inside its byte bound;
and matching capsule/session bindings and evidence. A file left behind on a
failed exit is not automatically adopted. Partial segments remain diagnostic
data, never a resumable session or a proof.

If adopted, the capsule would supply three presently missing concrete inputs:

1. Actual successful execution row/instruction/padding statistics, segment sizes
   and the complete serialized witness. This makes the next proof plan a plan
   over observed finite artifacts rather than a capped prefix.
2. An immutable exact session from which the existing staged-host design can
   prove without acquiring a new whole guest execution. The stage host still
   performs charged per-segment SDK witness reconstruction and preflight.
3. An exact basis for deciding whether to pay for the first genuine A receipt
   and then exercise the already specified no-sealed-witness public import/reuse
   route. Execution alone is not that receipt and does not clear that route.

The source-only staged host accepts this capsule geometry unchanged. For actual
segment count `s` and this one verified premise (`m=1`), its full dependency
graph has `3s + 1` calls: `s` segment, `s` lift, `s-1` join, one resolve and one
finish. Thus the current maximum is 385 calls, 384 involving a prover operation.
Finish verifies both the complete segment composite and final resolved succinct
claim against exact A/H before writing a receipt. These counts say nothing
about their CPU, memory or wall cost. In particular, a `po2=19` segment cannot
be priced from old `po2=18` mean timing by multiplying blindly.

The aggregate stage host is currently a reviewed source/build candidate, and
the Python aggregate producer remains specified rather than implemented.
A successful screen would not magically supply either a production executable
adoption or an orchestrator. Use the already written
[AGGREGATE-PRODUCER-PLAN](../v5-2026-10-12/AGGREGATE-PRODUCER-PLAN.md), not a new
duplicate controller design, if root selects that work.

## Proof funding is a separate later gate

There is **no proof allowance in this recommendation**. Before any stage starts,
root must separately adopt the exact producer/host and complete capsule, fix one
finite whole-route budget and continuation policy, and disclose what costs are
still uncertain. No successful screen renews the old proof allocations.
No capability receipt is to be called a profitable service merely because it
has been produced.

The first A image also needs the explicit support decision already described in
[IMAGE-LIFETIME-DECISION](../v5-2026-10-12/IMAGE-LIFETIME-DECISION.md): keep this
exact memo A supported through the intended reciprocal milestone if funding
proceeds. Its capsule and future receipt cannot be relabeled for a typed-row A'.
If root already intends to replace memo A before any genuine import use, do not
pay heavily for its proof; choose the representation work first instead.

The full-cost comparator, optimized ordinary-library baseline, justified cold
events, custody/service costs and conditional benefit region remain exactly
those in [NEXT-AGGREGATE-COST-DECISION](../v5-2026-10-12/NEXT-AGGREGATE-COST-DECISION.md).
No new growth theory is needed for this decision. A successful small-workload
seal may have no economic advantage at all, while still supplying necessary
trust-boundary operability evidence.

## Non-automatic terminal decisions

| Observed terminal outcome | Permitted conclusion and next decision |
|---|---|
| Complete adopted capsule | Actual layout is known; independently decide exact producer implementation/adoption and finite proof funding, or retain capsule without proving |
| Hard row cap reached | This geometry still did not finish; no total-work estimate, cap ladder or partial-session continuation; decide whether the reserved typed-row refinement is justified |
| Segment/capsule byte/count or memory refusal | A coupled representation/custody constraint is now concrete; do not merely raise the cycle argument or claim an affordability gain |
| Semantic/header/assumption mismatch | Stop and investigate the exact assurance/input boundary before any funding; resource enlargement is irrelevant |
| Dirty closure, output or binding failure | Preserve complete evidence and charges; no artifact adoption based on a favorable inner field |

Compared with the typed-row rewrite, this one screen is a smaller immediate
implementation commitment and directly targets the missing complete-layout
fact. That is the reason for the recommendation, not a guarantee of success.
After its terminal outcome there should be one explicit next decision, not an
indefinite optimizer queue or indefinite client polishing while A stays open.

## Source anchors

| Source | SHA-256 |
|---|---|
| `software/v5/aggregate_host/aggregate_host.rs` | `7548e5b2092f3ece5d9ef93cef6c7ccd7d5e01ad123053f28e836558617857ca` |
| `software/v5/aggregate_host/snapshot.py` | `d99656a17891983e2ae5ee0afb78fd4695b0ac4746a58aade34977b36fd2f442` |
| `software/v5/aggregate_production/stage_host.rs` | `5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

The SDK source inspection used the retained host-build tree at
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8`.
The selected compiled runtime remains the existing pinned host, not a newly
built binary inferred from this source inspection. Current execution/cost
evidence is [MEMO-SCREEN-DECISION](MEMO-SCREEN-DECISION.md); it stays failed and
unchanged. Source reading/data decoding is not another campaign.

## Root-selected source implementation

2026-10-16, `memo_independent_review`; canonical guard PASS. Root selected a
fresh `software/v5/aggregate_host/capability_snapshot.py`. The initial exact
copy matched frozen `snapshot.py` SHA-256
`d99656a17891983e2ae5ee0afb78fd4695b0ac4746a58aade34977b36fd2f442`.
An `apply_patch` edit then changed only the docstring and capability labels,
the native arguments from `2^25 / 18 / pc-samples` to `2^26 / 19 / stats`, and
their report fields. The report explicitly includes `diagnostic_mode="stats"`
and scope `ONE_MEMO_IMAGE_CAPABILITY_ATTEMPT_NOT_OPTIMIZATION_OR_SPEEDUP`.
Existing configuration/result schemas and success status remain compatible;
none of those status fields is mathematical acceptance.

Final fresh source: **9,657 bytes**, SHA-256
`9f914e2c5c5c86d3bd1f4efbdc45a16fadec67f14df082b82a2d506e98d506b5`.
Read-only exact diff confirms no other change. The predecessor hash was
rechecked unchanged. Host/image/wire/header/genuine-I binding and pre/post
validation, one execution/zero proof calls, 128 segments, 64 MiB capsule bound,
8 MiB diagnostics, 1 MiB logs, 144 MiB/160-entry final census, and 120-second
native timeout are preserved. SegmentStore's separate 64 MiB combined bound
remains in the unchanged host. No Rust, guest, checker or mathematical code
was edited, and no product/test code was executed, imported or compiled.
No Git mutation occurred.

Root owns the fresh exact configuration/selector, independent source/selection
review, and finite outer Job. Available physical memory is a separate scheduling
constraint: root will serialize this actual launch after client03 rather than
overlap their memory allocations. Source preparation is parallel; this appendix
does not launch the operation or grant proof funding/automatic continuation.
