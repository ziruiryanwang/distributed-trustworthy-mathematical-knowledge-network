# Growth-boundary resource audit

Date: 2026-09-20. Reviewer: `growth_boundary_triage`. Scope: independent arithmetic and resource-claim review, not expansion-protocol composition or implementation qualification. No implementation, executable model, native replay or benchmark was run.

## Reviewed cut and result

The initial held [triage note](../growth-boundary-triage.md) is 13,048 bytes, SHA-256 `90D25D128A45A40E5BCCD861783944A0892FB9AC732E8FB07F3F1528A041280B`. I read the complete cut and independently checked its numerical consequences against the selected H/N/O sources. I then fully reread the repaired 13,331-byte cut, SHA-256 `47B00C28B368F6AF037C7679629611B2A687C6FA0B8C6B5AD793E1A26E5A19E2`. The arithmetic passes; both source-precision findings below are closed at the repaired cut. No remaining blocking arithmetic/resource-claim finding was identified within this review's scope.

This review concerns a negative operating-envelope result: specified bounds cannot justify an unchanged larger-scope schedule. It does not prove universal impossibility, supply a new controller, or establish actual sustained mathematical growth.

## Findings on the initial cut

| ID | Finding | Required repair |
|---|---|---|
| GROW-RES-001 | The highest-carry precondition says two **completed** 2,048-target runs. H/O allow only one completed incumbent at a size; a colliding run is ready, not another completed tier. | Say one completed 2,048-target run plus one disjoint `READY_FOR_CARRY` run of the same size. Counts are unchanged. |
| GROW-RES-002 | The sixteen-day calculation describes 80-call successful jobs without explicitly calling 80 the reserved envelope. The preceding 64-call countercase correctly concerns actual stipulated lookup work; the two arguments should not be conflated. | Name the 80-call-per-job **reservation envelope**. Its sixteen-day quota arithmetic is not a lower bound requiring every actual job to use all sixteen possible group operations. |

Both findings are precision repairs, not counterexamples to the numerical conclusions when their intended premises are used.

## Independent checks

**Serial highest carry.** One parent owns `16392 = 8 + 8*2048` keys; the other owns `16384 = 8*2048`, borrowing the common eight. Their union has 32,776 keys and four selected rows per key. All change publication-scope owner. Thus 131,104 moves require 262,208 individual DROP/PUT calls under O's selected one-row-at-a-time procedure, exceeding one 262,144-call grant by 64 before any other duties. For H's generic batching alternative, 262,208 is the row-mutation count, not necessarily the call count. The note preserves this distinction and does not infer a universal elapsed deadline from funding buckets.

**Actual full-64 lookup case.** `32776*64 = 2097664`, whereas eight complete grants supply `8*262144 = 2097152`. The shortfall is exactly 512 calls before renewal or placement. This defeats that actual-cost case in eight complete grants; it does not require every permitted lookup to reach its ceiling.

**Reserved refresh envelope.** N's other shares sum to `40000 + 4096 + 32000 + 22128 = 98224`, leaving 163,920 calls or 2,049 reserved 80-call jobs per grant. Sixteen such shares give 32,784 jobs, eight more than the 32,776-key inventory; fifteen give only 30,735. Total reserved job work is 2,622,080 calls. These are count inequalities, not a supplied sixteen-day scheduler, lease argument or recovery promise.

**Conservative retained stock.** N's extrapolated recipe gives 151,104 group generations at 4 KiB, or 590.25 MiB, and 262,208 row generations at 2 KiB, or 512.125 MiB. Their sum is 1,102.375 MiB, exceeding the 1,024-MiB cap by 78.375 MiB. Adding the unchanged 256-MiB remainder gives 1,358.375 MiB before extra side-scope stock. An upper-bound recipe exceeding capacity fails to certify fit; it does not prove that every actual trace reaches that bound. The note correctly requires a new paid, jointly compatible argument before invoking earlier reclamation, more reuse or smaller representations.

**Claim boundary.** The note supplies neither the continuing physical old/new renewal peaks nor a full carry/refresh/reclamation calendar. It expressly leaves those unselected and does not infer them from spare average calls. Sixteen days does not itself change a retain-all-generation stock bound. Its native/reciprocal execution gates remain NOT RUN. The independent-provider consumer chain is left to the separate composition review; nothing in this arithmetic review certifies that chain or end-to-end usability.

## Optional corroboration, outside the note's required case

For a distinct insertion-only state with completed sizes `1,2,4,...,2048` totaling 4,095 targets and one new singleton, the full carry chain has target participation `2+4+...+4096 = 8190`. If the incumbent 2,048 run alone owns the eight common keys, those move only in the final carry. The chain therefore moves `4*(8*8190+8) = 262112` placement rows and needs 524,224 unbatched DROP/PUT calls under the same serial procedure. Two complete daily grants leave only 64 calls for all other work. This separate corroborating count is not a supplied starting-state maintenance/calendar witness, is not needed by the reviewed note, and must not be promoted to an actual two-day completion or elapsed-time theorem.

## Re-review record

At repaired cut `47B00C28B368F6AF037C7679629611B2A687C6FA0B8C6B5AD793E1A26E5A19E2`:

- GROW-RES-001 is closed: the note specifies one completed incumbent plus a disjoint actually published `READY_FOR_CARRY` run, preserving the unique-completed-tier invariant.
- GROW-RES-002 is closed: the note explicitly identifies the 80-call-per-job reservation envelope and denies that every actual job must consume all 80 calls.
- The complete reread confirms unchanged figures and intact funding-interval, upper-bound-stock, no-new-schedule and unperformed-execution boundaries.

No frozen H/N/O source was changed by this review. A later editorial status/link change still requires a cut-specific reread; this audit does not preapprove unseen edits.

### Final editorial reread

I fully reread final source SHA-256 `9C35640D8FE15690E478AA1B05CD75DBC1E216F0B2182F89D0017993C268143A`, 13,820 bytes. Reversing only the header status and final review-link/history paragraph in memory reconstructs exactly the prior 13,331-byte `47B00C28B368F6AF037C7679629611B2A687C6FA0B8C6B5AD793E1A26E5A19E2` cut. Thus no reviewed body, premise or figure changed. Both findings remain closed and all scoped resource-claim conclusions above apply to the final source. The optional corroboration's powers-of-two list in this audit was made explicit; its arithmetic and claim limits are unchanged.
