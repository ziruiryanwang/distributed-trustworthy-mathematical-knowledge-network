# CP-001O checkpoint: published-batch normalization

Date: 2026-09-20. Status: selected owner-local continuation after two independent source reviews and fresh integration review; exact artifacts are bound by the [five-file manifest](CP-001O-SHA256-MANIFEST.md). [V6/I](../../spec/OPERATIONAL-CORPUS-V6.md) remains the network/native specification. This is a bounded continuation of H's owner-local index organization, not a new wire version. Frozen H/N and optional J/K/L/M remain unchanged. Concept only: no implementation, extraction, native replay, executable model or benchmark.

## Missing choice and selected continuation

Select the [batch-normalization contract](../../research/modules/reciprocal-operability/batch-normalization-contract.md), held source `34DA63220B9483E7CB7E825CBB21092AAD1F27E43F8F9B052EE14A3760714DB0`, for finite explicitly admitted disjoint pending batches, including already-published inputs. Its proposal-stage header is historical authorship state; this checkpoint supplies selection authority only at the stated scope.

H permits arbitrary bounded simultaneous batches but specifies power-of-two completed tiers and equal-size whole-run merging. An unsplit twenty-target run's descendants have sizes 20·2^k, never powers of two. Treating arbitrary sizes as completed tiers instead also fails: seven disjoint runs of sizes 1,3,5,7,9,11,13 have 49 targets and no equal-size pair, yet seven occupied sizes exceed floor(log2 49)+1 = 6. These counterexamples concern normalization and the settled-level claim, not native theorem validity or the separate logarithmic successful-doubling argument.

N's eight twenty-target scopes are explicitly pending. Its finite routing/supply witness remains valid. This amendment supplies a possible paid continuation, not retroactive evidence that those pending inputs were already consolidated. No frozen source is silently corrected.

## Exact contract and invariants

One owner-authorized invocation freezes exact provider/foundation/extractor, semantic targetRefs, current descriptors/features, owner/borrower ledger, actual groups/rows, guards and finite resources. Its target set must be disjoint from other logical runs/pending inputs. An overlapping input is refused by this operation without deleting existing publication or custody; a general overlap/deduplication mechanism is not selected.

Canonical greedy partition consumes consecutive targets in largest-fitting power-of-two blocks: 20 becomes 16+4. Each immutable child FeatureScope contains its complete emitted-token union, including borrowed tokens. Mathematical artifacts, proof instances and public target postings are not rewritten merely to reorganize index ownership.

For each parent-owned key, retain its actual eligible anchor and assign the key to the unique child containing that anchor, or use the source's deterministic eligible replacement rule. Other children borrow. Keys with an outside owner stay borrowed; no copied receipt creates a second owner. Outside borrowers of a moved key resolve the provider-wide versioned owner entry. Entering the transition invalidates earlier settled-coverage assertions before mutation, not only at final partition commit. Unversioned copied references require a paid complete repair plan or refusal.

The physical migration uses existing G/F group operations. ProviderAd2 has no scopeID; scopeID belongs to the immutable group. Identical eligible signed ads can retain bytes but still require actual old-group DROP/new-group PUT. At a same-holder key, DROP precedes PUT; an availability gap is possible. Lost outcomes remain unresolved and charged. Parent, child, intermediate and uncertain groups, snapshots, pins and retirement tails count until their real release.

Only after the required ownership and borrowed obligations settle does the guarded local partition commit replace the parent by its children. A child colliding with a completed tier is READY_FOR_CARRY, not a second completed incumbent. Normalization and successive carries share H's one handoff allowance; retained tails do not become free just because only one migration is in flight.

A changed publication-scope owner invalidates the affected N commitment and requires readmission. The unaffected main owner's cut can remain valid under its own guards. This is distinct from N's ordinary physical-holder movement within one unchanged publication obligation. Neither rule grants new resources.

## Finite argument and explicit limits

Consider a finite nonempty disjoint pool of M targets after successful dyadic normalization, with no new arrivals into this admitted pool. Let R count all logical dyadic completed and ready runs and Q count ready runs. A successful equal-size carry replaces two runs with their doubled union, decreasing R by one. Installation into an empty tier preserves R and decreases Q. Therefore the natural-number lexicographic potential (R,Q) strictly decreases on each successful step.

If the funded steps actually settle, processing all ready runs leaves at most one completed run of each power-of-two size. Conservation of target mass makes this exactly M's binary expansion: popcount(M) completed runs, at most floor(log2 M)+1. If R0 is the postnormalization dyadic run count, exactly R0−popcount(M) carries occur. An unresolved migration is not a successful decrease; unavailable service or exhausted authority may stop progress.

Normalization's split and owner transfers are charged separately. Within this fixed insertion-only epoch, a key starting in a child of size m has at most floor(log2(M/m)) subsequent successful doubling-owner transfers. Failed calls, extra copies, independent anchor changes, withdrawal, further splitting and repair are additional work. This is neither a sustained-arrival stability theorem nor a promise of logarithmic elapsed time.

The settled count concerns the normalized pool's logical frontier. It excludes unnormalized pending inputs and physically retained ancestors. Both still consume real stock. This amendment supplies neither a global partition of mathematics nor semantic novelty or usefulness judgments.

## Same-slot nonempty continuation

Take two already-published twenty-target scopes A and B among N's eight existing pending scopes, not forty extra targets. Retain the full 2,048-target main run, its 16,392 refresh keys and all original service duties. Total target mass stays 2,208.

A becomes A16+A4 and occupies empty tiers. B becomes B16+B4; the occupied tiers cause real carries A4+B4→C8 and A16+B16→C32. The selected forty-target cohort settles as 32+8; six other twenty-target inputs remain pending. The main run is untouched.

Each side target has eight unique tokens plus eight common tokens borrowed from the main owner, with four actual depth-zero copies. Splitting A and B moves 640 rows each; the carries move 256 and 1,024. This is 2,560 row moves, 5,120 DROP/PUT mutations, and a conservative 10,240 calls including one OPEN and lawful empty CLOSE per move. No cross-holder batching or free anchor repair is presumed.

The source specifies a separately admitted compatible extension of N's finite case:

| Dimension | Joint conditional bound |
|---|---|
| Calls | Use only 10,240 genuinely uncommitted calls from N's 22,128 reserve; leave 11,888. Existing committed repair/tail work cannot be displaced. Parent ceiling remains 262,144/day. |
| CPU | N's full-parent-call accounting plus at most 512 added non-RPC seconds gives 27,514.6 < 28,800 seconds. |
| Metadata | Add 32 MiB for actual group/row generations and all other stipulated records: 908.375 MiB < 1 GiB. |
| Counts | At most 93,248 groups, 138,816 rows and fifteen all-state scope records, including retained parents. |
| Resident memory | Conservatively add all 32 MiB metadata and 16 MiB planning workspace to N's joint 1.75 GiB: 1.796875 GiB < 2 GiB. |
| Traffic/I/O | Existing call traffic remains within the parent grant; explicitly supply up to 128 MiB additional local I/O. An absent numerical I/O ceiling is not free service. |
| Calendar | An actually supplied 2,048-second phase after N's 71,008.4-second point ends at 73,056.4 before residual maintenance pauses; 13,343.6 seconds remain. Per-call and local-work progress are premises. |

The single mutation occurrence yields to due maintenance; a paused lookup still counts. Favorable actual empty-group CLOSEs occur before the next renewal window, keeping the side renewal ceiling at 5,120. Failure can leave additional active/uncertain groups needing real renewal and readmission. Closing an empty group is not physical tail reclamation. Repetition requires actual settlement and fresh joint admission, not leftover hours or the one-time arithmetic.

This is a nonempty paper composition at the original scale. The same real workload's RAM, I/O, native fit, service times and lifecycle have not been measured. Backlog, insufficient grants, missing inventory, overlap, changed support and unresponsive holders all have explicit non-success outcomes.

## Review and evidence boundary

Root independently read the held source, checked the H owner/borrower and binary-tier premises, and recomputed the finite proof and stated arithmetic. Separate [composition](../../research/modules/reciprocal-operability/audits/batch-normalization-composition-audit.md) (`8981879A…`) and [resource/lifecycle](../../research/modules/reciprocal-operability/audits/batch-normalization-resource-audit.md) (`283A0DD0…`) audits fully reread the same held cut and report no blocking issue within their scopes. The coordinated clarification from `85BD9595…` to `34DA6322…` makes transition-start coverage invalidation and the conservative simultaneous resident bound explicit; it changes no numerical grant or mathematical acceptance rule.

A fresh [integration review](../../research/modules/reciprocal-operability/audits/batch-normalization-selection-audit.md), independent of the source, both source reviewers and root, checked candidate checkpoint `BD9B5AEA697A6C094264E271D7E6A6741C2F1A99E90BE11F40073D400D53C3E2`, the final source and both source audits, finding no blocking integration issue. Its final section records the separate editorial-selection reread. The [five-file manifest](CP-001O-SHA256-MANIFEST.md) binds source, three audits and this checkpoint; the review itself does not claim to validate a subsequently emitted manifest. Mutable navigation and control ledgers remain outside the freeze.

All six native and eight reciprocal execution gates remain NOT RUN. The [reviewed readiness handoff](../../research/modules/qualification-readiness/README.md) is unchanged. Actual complete BOOT1 construction, export, checked use and separately replayed derived contribution remain decisive evidence dependencies and need authorization. This checkpoint does not establish operational software, sustainable growth or completion of the whole-project goal.
