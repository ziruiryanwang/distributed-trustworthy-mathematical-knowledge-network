# Next priority: certify the needed frontier, then close real public reuse

2026-10-17, `memo_independent_review`. Canonical guard passes. This checkpoint
combines source/data analysis with the narrowly selected adapter implementation;
it is not runtime, proof funding or v5 acceptance. Root selected implementation
in [SELECTIVE-FRONTIER-SELECTION](SELECTIVE-FRONTIER-SELECTION.md).

## Decision

**The highest marginal-payoff next step is a genuine certificate for exactly
BASE + FIRST, followed by the already designed public FIRST-to-SECOND reuse
path. Do not enlarge the old three-member proof budget first.**

The actual po18 layout02 stopped after 256 segments at
67,112,097 >= 67,108,864 session cycles. It produced no capsule or proof; its
4.71875 known CPU seconds remain charged. Layout01's earlier adapter failure
and 0.59375 known CPU seconds also remain charged. Neither failure is a passed
or completed instance of the smaller selection.

The public terminal gate needs a genuine warrant for FIRST and its BASE
semantics. B is then supposed to author SECOND using FIRST twice. Certifying
SECOND in the starting aggregate pays for an additional proof that B and C do
not select. Removing that descendant is a justified scope-of-certification
decision, not weakening the target theorem or abandoning its premises.

This decision does not assert that the smaller po18 execution fits. That is
the remaining inexpensive layout uncertainty; no source-derived cycle upper
bound has been established. It also does not solve the backend's memory
problem by itself: each full po18 segment still has the same proving geometry.

## Source argument, with an exact mathematical target

The actual memo guest's recipes select
`software/v5/bounded_parse/aggregate_lib.rs`, which selects the exact-journal
`bounded_parse/aggregate_relation.rs`. The latter has these relevant rules:

1. `check_reader` admits one or more newly checked deltas.
2. `Graph.delta` requires every exact premise already established, checks the
   ranks, and derives the new rank as one plus the greatest parent rank.
3. `Graph.closure` requires the target to be a newly checked exact delta and
   rejects any included node outside the target's backward dependency closure.
4. The only new-mathematics path remains `module_relation::check_validated`.
   Receipt assumptions remain verified by the unchanged guest wrapper.

FIRST's retained witness has one exact parent, J_BASE. The graph
`BASE -> FIRST`, with target J_FIRST, therefore satisfies the same structural
closure/rank rules. SECOND is a descendant, not a premise. Keeping SECOND
while merely changing the target to FIRST would correctly fail closure.

The receiving target is the **whole 184-byte J_FIRST**, SHA-256
`07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da`,
not merely its ModuleID. J_BASE remains
`22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682`.
A, I, foundation, policy, these exact Js, the genuine I parent receipt and
FIRST's proof witness stay unchanged. H, wire, count-dependent membership paths,
capsule and session identities change. No old proof checkpoint is reusable under
the new session identity.

Read-only inspection of retained bytes gave:

| Item | Exact retained/selected extent |
|---|---:|
| Old wire, counts assumptions/frontiers/deltas/targets = 1/1/2/1 | 215,540 bytes |
| FIRST frame length word / payload offsets | 625 / 629 |
| Unchanged FIRST witness, 1,355 rows, rank 1, one BASE parent | 113,220 bytes |
| SECOND frame length word / payload offsets | 113,849 / 113,853 |
| Omitted SECOND witness, 1,009 rows | 101,687 bytes |
| New wire, counts 1/1/1/1 | 113,849 bytes |
| New H | two members, maximum rank 1, seal height 1 |

FIRST's frame SHA-256 is
`88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1`,
byte-identical to the retained ordinary `child-input.json`. Removing 101,691
wire bytes is not a measured time saving and cannot predict cycle count in a
segmented VM. See the separate [layout diagnosis](SMALL-LAYOUT-FEASIBILITY.md)
for paging/segment overhead; do not interpret the failed boundary's 3,233-cycle
overrun as the remaining work needed to halt.

## Concrete implementation completed, awaiting independent review

Only fresh `software/v5/aggregate_small/frontier_snapshot.py` was created:

- 13,788 bytes; SHA-256
  `e734200f76510b73fdb6cd3346d07dfc085ff1eabfce183db97ce0eda5f6a00d`.
- Imports the frozen `capability_snapshot02` as a direct sibling, avoiding the
  package initializer/producer dependency closure. Reuses its strict finite
  owner-record decoding, host-build adoption and exact pin helpers.
- Uses the existing `aggregate_claims.input.encode`; no new planner, guest,
  Rust host, producer or verifier is introduced.
- Checks original counts, all three exact J pins/ranks, original memberships,
  claim/frontier/target fields, both frame extents and EOF. Re-encodes the full
  original wire and requires exact equality before selecting the smaller graph.
- Preserves FIRST's raw witness and checks its single exact BASE parent, row
  count, rank and derived ModuleID. The unchanged native host remains responsible
  for actual mathematical checking; these Python comparisons are not admission.
- Computes a fresh two-member commitment and both fresh paths. Count is in the
  hash domains, so even unchanged members cannot reuse the old sibling hashes.
- Preserves the existing producer-consumed configuration/result field schemas.
  A separate `selection-derivation.json` discloses old synthetic H, old actual H,
  new H, exact target, omitted descendant, input pins and new paths. Its bytes
  are rebound during finalization and included in the retained-output census.
- Preserves the actual one-call execution path and po18/N256/2^26 limits,
  96 MiB capsule, 208 MiB / 288-entry output cap, and no automatic retry/proof.

The source has not been imported, executed or compiled by this author. Root owns
the exact launcher selection and reviewer clearance. No used predecessor bytes,
Git index, branch, native binary or evidence files were changed.

I also inspected the possible repeat of layout01's timing-float failure:
`aggregate_small.producer` uses `production.producer.parse`, whose operational
JSON decoder accepts finite fractional timing fields; it does not route build
records through the mathematical integer-only parser. The old float seam is
therefore not a source-proven producer blocker. Actual adoption is still needed.

## Efficient order of the remaining central work

1. Review this exact adapter and its fresh root selector. If selected, run one
   complete layout for the new H with the existing bounded hosts. On refusal,
   preserve it and re-decide from the actual cause; do not start a cap ladder.
2. If a complete capsule is adopted, form its exact producer profile/request
   using retained build/image evidence. This is a real integration boundary,
   not another synthetic-control suite. Perform preflight before funding proof.
3. Review capacity, then select one actual full-po18 segment as the affordable
   proving discriminator. A smaller tail segment cannot establish full-po18
   behavior. Success is one checkpoint, not a universal memory bound or funding
   for the whole DAG; continuation needs full cost and capacity accounting.
4. If feasible and separately funded, retain successful stages toward one fully
   resolved A receipt. No replays of already successful stages or new guest run
   should be necessary. Require the unchanged final real A/H verification.
5. Use that receipt in the single combined
   [genuine public terminal gate](GENUINE-TERMINAL-GATE.md). Its execution adapter
   can be prepared in parallel with proving; do not rerun the prior I-only path.

The old GENUINE-TERMINAL-GATE's **three-member H and paths are superseded only
for the new source selection**. Its public endpoint and workload stay: B finds
FIRST without its ID, verifies A, imports BASE/FIRST, authors SECOND by two FIRST
uses, publishes it; C checks A plus the new delta after the origin disappears,
then retains source-ready semantics after B's provider disappears. The new
adapter must consume the actual adopted two-member H/paths, not stale hardcoded
ones. SECOND remains retained mathematics, so this is genuine integration and
dependent reuse, not a claim of new global mathematical discovery.

### Native manifest controls: useful but not today's blocker

[NATIVE-MANIFEST-GATE](NATIVE-MANIFEST-GATE.md) needs a complete adopted po18
capsule. Neither failed layout qualifies. Its stale layout01/unchanged-H
references must not be used as actual inputs for the selected two-member case.

The ten proposed `finish:0` controls exercise distinct native boundaries and
have a sound no-prove control-flow argument. They are not mandatory mathematical
premises for the next layout; the manifests are owner-produced local operation
records, not peer trust warrants. Do not put a broad replay ahead of the genuine
capsule. Once it exists, the exact-manifest/wrong-checkpoint-magic control M10 is
the smallest real native parsing/binding-path discriminator. M3 (object-only
nested pin) and M9 (incremental row bound) are the most distinctive new malformed
input checks. Root may select those or the finite ten-case gate after cost
review, but neither its success nor the Python controls substitutes for an
actual segment proof, final receipt, public reuse or growth evidence.

## What this changes for growth and global scale

Selective certification is itself an important architecture rule: certify a
requested backward closure or justified reusable frontier, not all available
descendants or a globally synchronized corpus. Receipt aggregation may provide
more members as an amortized service decision, but unsolicited extra members
are not prerequisites for trusting FIRST. This removes needless producer work
without relocating it into every consumer's ancestral proof replay.

The growth comparison remains three-way: optimized independent local L,
ordinary shared proof DAG/library/cache O, and certified V. All use the same
mathematics and receiver endpoint. O may omit SECOND from its FIRST delivery,
compress proofs, cache them, and use the same reusable method. V may not claim a
win merely by comparing its two-member closure with an unnecessarily flattened
three-member O route. Charge new certification, service, failed discovery and
retention; separately disclose all retained development failures. Do not erase
their costs or relabel the smaller case as completion of the old experiment.

For justified positive event margins d_L and d_O and additional fixed/service
cost upper bounds f_L and f_O, the established sufficient region remains
`N > max(f_L/d_L, f_O/d_O)`. Nonpositive margins cannot be rescued by large N.
Genuinely eligible cold demand must be justified; artificially resetting warm
consumers is not demand. This small fold-map case may have no positive margin.
Its purpose is to close the implementation prerequisite, after which full-cost
benefit needs a supported workload/region, not another theorem-count metric.

No component pass closes the complete release obligations: faithful checker and
crypto correspondence, scalable useful discovery/coverage, availability/repair,
full-cost useful growth, ordinary portable operation/hostile-input isolation,
updates and deployment assurance remain. The selected small frontier is a
direct step toward that software, not a qualified-v5 substitute.
