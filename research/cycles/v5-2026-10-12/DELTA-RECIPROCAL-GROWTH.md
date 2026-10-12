# Consequential delta workload and its cost argument

This is the next implementation contract, not a guide or a release claim.
The shared goal remains the full decentralized v5. Mathematical admission is
independent of the local agent's reasons for selecting this workload.

## What the next contribution does

The retained first delta proves the parametric fold/map law for the actual
certified Tree module. A new ordinary Lean source,
`software/v5/workloads/DeltaFoldMapTwice.lean`, applies that law twice and uses
equality transitivity to justify replacing

    fold leaf node (map second (map first e))

by

    fold (fun a => leaf (second (first a))) node e.

The derivation is short because the earlier structural induction is reused,
not reconstructed. Its expression must actually reference the accepted first
delta. This is a composition/use example, not a claim of mathematical novelty,
optimal proof complexity or a generic speedup from naming another theorem.
The source is currently unrun. Its export and complete onward packet still
need actual independent checking.

## Analytic usefulness: no huge-tree timing experiment required

Define n(e) as the number of leaf and binary-node constructors in e. Consider
the explicit strict, pure reference evaluator that implements each map and fold
by one structural traversal, materializes each map result, and does no fusion.
Charge constructor case-analysis visits and intermediate tree-constructor
allocations separately from calls to first, second, leaf and node.

Structural induction shows n(map f e)=n(e). The pipeline therefore uses3n(e)
constructor visits and allocates2n(e) intermediate tree constructors. The fused
expression uses n(e) visits and allocates no intermediate Tree constructor.
Calls to first, second and leaf occur once per original leaf, and node once per
original binary node in both expressions. This establishes savings of2n(e)
visits and2n(e) intermediate constructors in THIS evaluator. It is linear,
not exponential. Peak space, retained values and compiler optimization are
separate measures; the argument does not claim zero total allocations.

The equally optimized local and ordinary-shared-library comparators may already
fuse these expressions. If so, their downstream evaluation cost is identical:
the network earns no incremental benefit from this transformation. The relevant
possible saving is obtaining a missing warranted method more cheaply, with
discovery, proof checking and failed work fully charged. A dependency edge does
not establish that the recipient could not have proved the result more cheaply.

## Which scalability statement the software must establish

Let G be the whole corpus, H the proof ancestry below certified frontiers, D the
complete uncertified delta DAG, I selected interfaces and S demanded semantic
bodies. With a fixed packet envelope B, a successful recipient verifies genuine
frontier receipts and checks D once in topological order. Its obligatory input
does not enumerate G or H. It DOES include all of D and the required I/S.
Increasing global corpus size therefore does not itself enlarge the admitted
packet; query coverage and provider availability remain conditional.

A chain cannot grow forever inside B without a new funded certificate or a
different proof. This follows directly from retaining every uncertified witness.
Do not call a local delta acceptance flag an ancestry cutoff. Selective sealing
is still needed for long-term growth, with its costs and availability charged.

## Evidence boundary for the next integrated operation

The endpoint is a later ordinary source using the actual first delta, then
publication of its complete packet through a replaceable index/custody provider,
and fresh receiving after its original producer is gone. Formal-export indexing
does not depend on proof packaging. A composite custodian can index its retained
exports and advertise the existing index role; that is not general standalone
custody discovery and does not prove retention or mathematical validity.

Record exact packets, statement/proof references, selected semantics, query
coverage, all attempts and provider costs. Include the first delta's proof in
the onward packet, and exclude theorem proofs BELOW its certified frontier.
The original base production cost, earlier failures and future retention costs
must not disappear from any full-cost comparison. Development build costs may
be amortized only under an explicit distribution/accounting horizon.

The existing full-cost inequality and three comparator routes in
`../v5-2026-10-07/GROWTH-WORKLOAD.md` remain controlling. This workload supplies
a usable capability and an analytic application-cost argument; it does not by
itself establish positive network-wide net benefit or inevitable useful growth.

## Source-only implementation of ordinary delta composition

Root assigned fresh `software/v5/delta/author_actual.py`; it is unrun and grants
no runtime permission. The harness composes existing public APIs rather than
introducing another checker or manufacturing receipt-backed handles. It reuses
the prior actual harness's pin/read/save helpers and the earlier receipt/source
harness's canonical proof-reference traversal helpers.

The finite endpoint is:

1. Construct a genuinely cold ReceiptVerifier and DeltaVerifier; admit the exact
   retained first child witness over the actual base receipt. This is the required
   live authority for a new composition operation, not a repeated isolated test.
2. Register the actual handle in DeltaImportSession. Authenticate the selected
   base bundle's group openings and committed semantic bodies, plus the accepted
   first delta's theorem opening. No below-frontier theorem proof is supplied to
   the frontend. The adopted fixed foundation remains a separate semantic input.
3. Author the pinned ordinary DeltaFoldMapTwice source exactly once through
   DeltaSourceOperation and DeltaOwnerPreparation. Inspect the actual exported
   local proof closure: the statement mentions the base Tree/fold/map; its proof
   has at least two occurrences of the exact first theorem. Require a distinct
   four-universe theorem and the exact selected root, not a wrapper annotation.
4. Require the complete onward packet to retain the original real frontier and
   exact first witness, plus the new rank-two witness whose parents are the base
   and first delta. Preparation success remains explicitly untrusted.
5. Close all origin operation/session/receiver/frontier/preparation owners. Read
   the retained packet afresh and admit it through new cold receiver/frontier
   instances. Require all three actual modules, open the new theorem group, and
   re-export the exact complete onward packet. This is same-host fresh-owner
   receiving, not independent-host operation or network qualification.

The proposed workload spends at most two cryptographic receiving calls, three
native delta calls and one ordinary Lean frontend job. It does not run a guest,
snapshot, prover, network request or automatic retry. Root's finite outer
selection must cover their disjoint CPU reservations plus controller and output
headroom; overlapping object-lifetime controller counters are not added together.
Both successes and failures retain exact evidence. Primary final reports are
sampled after closing owners, and FINALIZATION-FAILED overrides any earlier
candidate success report.

Configuration schema is DMKN_V5_ACTUAL_DELTA_AUTHOR_RETURN_V1. It pins the
preparation profile, original child/journal/receipt/base bundle, foundation,
root-selected source and roots, current native driver, and runtime/helper sources;
provides finite receiving/authoring/one-operation preparation allowances and one
overall monotonic deadline. The preparation profile must include the actually
loaded new harness, delta/actual.py and authoring/receipt_integration.py in addition
to DeltaOwnerPreparation's documented source requirements. The native driver
must use the newly compatible library, not the old native-library01 artifact.
Inputs source SHA-256 is
`a4e2d897f929e2e63c43c70f274a8f270d9bb783180a6677366ae50ad73df153`;
roots SHA-256 is
`7882f5358514ab6fbe98c212868e267cd9d0dc4a20561b2702d66530a868b2e9`.

The separate network agent owns custody/index transport integration. This
composition harness does not duplicate it, invent a receipt for a native delta,
claim scalable discovery from known IDs, or prove full-cost positive growth.
Its packet/export/reuse outputs are intended as exact inputs to that next genuine
circulation endpoint, so a passing authoring prefix need not be repeated.
