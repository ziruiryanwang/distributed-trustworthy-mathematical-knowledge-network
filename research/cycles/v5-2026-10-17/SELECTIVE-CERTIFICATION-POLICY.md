# Selective certification: bounded renewal, not popularity-triggered proving

2026-10-17, `memo_tests_review`. Source/theory only; canonical guard and AGENTS
read. No imports, tests, execution, proof, product changes or Git. This extends,
not repeats, fixed-target D21 in `v5-2026-10-07/GROWTH-WORKLOAD.md` and the
full-route comparator in GENUINE-TERMINAL-GATE. Root owns implementation selection.

## Decision

**The mathematical/evidence primitives support a local adaptive policy; current
software does not yet implement the complete repeatable sealing lifecycle.**
Keep two independent triggers:

1. **Economic:** a locally funded operator judges that certification's complete
   incremental cost is justified by eligible use. Usage estimates may guide it,
   but do not inherit a proof of positive return or D21's competitiveness.
2. **Capacity:** the next exact backward closure will exceed a packet, native
   work, proof-production or custody bound. Seal a suitable exact frontier with
   explicit funding, choose another supported derivation, or refuse/defer.
   Crossing this threshold does not itself make sealing economically beneficial.

No global score, human-intention field, mandatory investigation list or identity
vote belongs in mathematical admission. This is an optional resource decision
by a payer, not a new validity predicate.

## Actual hooks and the remaining seam

| Existing source/API | What the policy can actually use |
|---|---|
| `mixed_claims.packet.parse_packet` / `Envelope` | Counts and validates exact backward closure before verification; default maxima include 16 deltas, 32 frontiers, 8 claims, 32 MiB packet, 16 MiB witness, 250,000 rows. Delta count alone is not a capacity estimate. |
| `client.workspace_evidence.acquire/admit_local(...expected_exact_journal=J)` | Admit either mixed evidence or a standalone A-member for the same exact J; shared finite allowance, explicit live cache behavior. |
| `mixed_claims.imports_atomic.MixedImportSession.use_aggregate_member(...resolutions={J:"incoming"})` | Explicitly replace the native representation of exact J with its certified frontier; `_merge` preserves semantic identity and records a representation revision. |
| `client.workspace_mixed._context_data`, inherited by the evidence client | Exposes that choice through public `import_context` warrant/resolution rows. A READY materialized view is sealed; make the choice before it is frozen or in a fresh context/operation, not by mutating a live view. |
| `MixedImportSession.onward_packet` and atomic authoring | Serializes only selected backward closure. An A frontier has no serialized native parents, so subsequent deltas need not carry that ancestral proof history. Required transparent semantics remain separate. |
| `aggregate_claims.input.encode` | Already supports I and A claims, exact frontiers, ordinary witness frames and exact newly checked targets. Only `from_legacy_packet` provides a packet convenience conversion; no generic mixed-packet conversion exists here. |
| `aggregate_small.operator` / `AggregateProducer` | New reusable supplied-profile/request preflight and finite run; real build/capsule adoption, actual graph quote, first-failure stop and retained charges. Source candidate, not evidence that a proof completes. |
| `export_evidence`, `retain_semantics`, `publish`, `reconcile` | Circulate an admitted terminal without losing selected semantic custody; no permanent availability or free renewal promise. |

Client reports expose nested actual costs, submission counts and live-cache hits,
not the counterfactual cost of an equally optimized ordinary DAG route. A provider
fetch count does not establish a recipient cache miss, independent demand, or
an avoided check. Do not multiply all local uses by a cold-check cost.

**Minimal central missing mechanism:** a bounded, reusable *mixed evidence to
seal request* adapter over the existing parser and encoder, followed by generic
snapshot/build-result adoption. It must select an exact target and its backward
closure, retain ordered genuine receipts, preserve witness bytes and target J,
emit new H/openings/wire, and create fresh capsule/session/request identities.
No checker rewrite is needed. Current `frontier_snapshot.py` is a pinned
BASE+FIRST fixture derivation, not that general API. A small owner-side advisor
can then propose WAIT / SEAL / REFUSE against explicit resource quotes; it must
not dispatch automatically or reset failed costs. Do not build a global demand
registry or claim an adaptive optimizer is already present.

## A finite renewal model that differs from fixed-target rent-or-buy

Consider one growing chain of exact targets and `m` blocks of `b` extensions.
Both routes receive the same initial admitted mathematics, new proof-DAG nodes,
semantic representations, compression and local caching optimizations. An
ordinary recipient visits each distinct missing DAG node once, never an expanded
proof tree. Alternative shorter proofs, accepted caches or prefetching are
allowed but their actual effects/costs must be included; the following hypotheses
must be rechecked if they eliminate the stated missing work.

Assume for this finite workload:

- Every newly requested target has `q > 0` genuinely otherwise-uncached admissions.
  This is a workload parameter, **not observed demand in our project**. Warm
  applications are permitted in both routes and charged equally; they earn no
  invented cold-check saving.
- Each distinct missing chain node costs at least `d > 0` to acquire/check under
  the chosen ordinary implementation after its optimizations. The sealed route
  can process each tail node for at most the same `d`. These are justified model
  bounds, not a universal lower bound on mathematical proof complexity.
- A successful seal after each block costs at most `K(b)`, including production,
  failures, adoption, incremental distribution and retention/repair over this
  finite service horizon. Additional whole-path receipt/member/controller/service
  cost is at most `c >= 0` per admission. Common semantics/search/authoring costs
  cancel only when actually equal; otherwise put their difference in K or c.
- The whole tail of at most b nodes, interfaces and demanded semantics fits every
  relevant bound; prior seals remain valid/available. Certification is feasible
  under a reserved peak-memory and service envelope. No changing image, unpriced
  archival obligation, correlated failure or external subsidy is hidden.

Certify each completed block only when the next block is to begin. Before that
renewal, the last target of a block is still received as b native deltas. Thus
the maximum tail is b, not b-1, and there are at most m-1 seals. Conservatively
charge m seals. With no baseline cache of those ancestors, ordinary cold work is

`q*d*(mb)*(mb+1)/2`.

Sealed tail work is at most `q*d*m*b*(b+1)/2`. Subtracting all extra certification
and receiving costs gives the sufficient full-cost advantage lower bound

`D >= q*d*b^2*m*(m-1)/2 - q*c*m*b - m*K(b)`.

**Proof:** target number k requires k distinct otherwise-missing nodes in the
ordinary route; their sum is `mb(mb+1)/2`. Within each sealed block the missing
tail lengths are exactly 1 through b, giving `m*b(b+1)/2`. The remaining terms
are the assumed additional costs. No DAG node is charged twice within one
baseline admission, and no warm cache is discarded to obtain this difference.

Consequently a nonempty finite conditional benefit region exists when an
admissible workload has

`m > 1 + 2*c/(d*b) + 2*K(b)/(q*d*b^2)`.

This is **a family-level capability/cost result**, not evidence that our current
small FIRST workload has positive d, enough q or affordable K. A huge global
corpus does not imply a long selected missing chain. If all readers retain the
ancestral DAG, their new missing work may be one node; the quadratic comparison
then vanishes and certification may strictly lose. Retention of every historical
target for ever is also not free: if its incremental cost grows with m, substitute
that cost before claiming this region. Finite rank/count and resource bounds
still limit each instantiation; no inevitable infinite/exponential growth follows.

### Choosing a feasible batch interval

If justified bounded-shape producer costs satisfy `K(b) = k0 + k1*b`, the sealed
route's steady per-extension extra cost in this renewal model is

`k0/b + k1 + q*c + q*d*(b+1)/2`.

For positive k0, q and d its continuous minimizer is
`b* = sqrt(2*k0/(q*d))`; compare the adjacent admissible integers and boundaries.
All byte/row/semantic/latency limits constrain b, not just the default maximum16.
This derives an implementable *conditional choice*, not an online guarantee:
estimating q or future costs from past observations makes the deployed selector
a heuristic. D21 is not applicable to this coupled, changing-target renewal
problem. With zero eligible cold demand, there is no claimed economic benefit;
continued publication may still require a separately funded capacity renewal.

## Finite-resource scheduling condition

A strict bounded-tail design cannot wait for a slow proof at a completely full
tail while promising unlimited continued extension. In a simple serial branch,
let L be the largest actually feasible tail, let a selected seal start at tail b,
and suppose at most `B + ceil(lambda*t)` further deltas arrive in any interval t.
If that seal completes within reserved latency tau, then

`b + B + ceil(lambda*tau) <= L`

is sufficient to keep the tail admissible until its exact frontier becomes
available. This follows by adding the arrival bound to the initial tail; after
promotion, only post-frontier deltas remain. Subsequent cycles need the same
conditions and nonoverlapping funded service capacity. This is not an assertion
that current proof jobs have a known successful latency bound. Without it, use
backpressure/refusal or pause publication; a timeout cap is not a completion SLA.
For DAG branches and variable rows/bytes, apply corresponding resource-vector
arrival bounds or conservatively serialize; a delta-count formula alone fails.

## What funding the first genuine A proof establishes

It can close a central executable seam: actual A verification, exact terminal
dissemination, ordinary semantic import, substantive SECOND authoring and onward
custody. It also gives one real production cost and receipt size. This is a
legitimate **bounded capability/assurance investment**, not a prediction of
economic return. It does not establish q, ordinary-route d, future K(b), successful
renewal latency, A-parent renewal operability or positive network growth.

Proceed with that one integrated gate only after feasible layout/adoption and
explicit funding. Do not repeat proofs merely to fit the batch-cost model.
The next generalization should remove fixture-specific sealing preparation and
record exact target/cache-state/cost-basis events sufficient for a local advisor;
counterfactual estimates must be labeled, unknown terms must block guaranteed
benefit claims, and ordinary DAG sharing remains a first-class comparator.

## Independent review: exact cuts and usable cost intervals

2026-10-17, `v5_growth_decision`; source/theory only. The chain inequality above
is sound under its hypotheses. Its extension to general DAGs needs an exact
cut condition, not an assumption that certifying one target removes all history.

Let G have exact-J vertices and child-to-premise edges, and let S be the set of
genuinely verified, available members whose native representations are replaced
by certified frontiers. Form G_S by deleting outgoing parent edges of S. For a
new target t and old native ancestor set O, the finite-cut hypothesis is: for
every u in O minus S, every path in G from t to u contains a member of S.
Let V_native be G's vertices using native evidence before this promotion;
preexisting I/A certified leaves are not in V_native. The selected native set
is exactly Reach(G_S,t) intersect (V_native minus S): no old native proof
history outside that remaining set must be replayed. Conversely, an
uncovered path can leave its old ancestors in the selected closure. This is a
reachability statement, conditional on valid receipt/member admission and exact
representation replacement, not a new mathematical soundness assumption.

Small counterexample: T depends on certified X and native Y; Y depends on old Z.
Replacing X alone leaves T -> Y -> Z. Even if Y occurs in X's aggregate header,
that does not help until Y's exact membership opening is available and its
certified representation is actually selected. All demanded cut members need
their openings and semantic custody; certificate bytes do not supply definition
bodies. The existing full member list and B.opening support this without a new
wire format. A DAG advisor must count the actual remaining closure and apply
resource-vector arrival bounds, not reuse the chain's nominal b automatically.

For more practical conservative inputs, let d_L>0 lower-bound ordinary missing
node cost and d_S>=0 upper-bound sealed-tail node cost. Retain the same finite,
fully otherwise-cold q-admissions-per-target workload and n=mb targets. Write
K(b,H) for the complete incremental per-seal bound over explicit service horizon
H. The same distinct-node summation gives:

`D >= q*d_L*mb*(mb+1)/2 - q*d_S*m*b*(b+1)/2 - q*c*mb - m*K(b,H)`.

The original result is its d_L=d_S special case. The sufficient inequality is
useful only for m,b,H satisfying all actual production, custody, semantic and
latency constraints; growth of retention cost with H must remain inside K.
An owner can supply independently justified lower/upper intervals instead of
an implausibly exact common node price. Unknown bounds imply no guaranteed
economic recommendation; estimates can still support an explicitly heuristic
one. For fixed H and affine K, the steady sealed-cost minimizer uses d_S in
`sqrt(2*k0/(q*d_S))` when d_S>0, then checks feasible integers and boundaries.
No current demand, calibrated cost bound or automatic proof dispatch follows.
