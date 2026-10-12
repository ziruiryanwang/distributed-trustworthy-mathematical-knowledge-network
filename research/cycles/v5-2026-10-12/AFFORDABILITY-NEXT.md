# Affordable aggregate certification: the next engineering decision

2026-10-12. Source/theory checkpoint by the base/aggregate author. This note
selects no runtime, source mutation, new cryptographic profile or proof budget.
Used sources and every successful or failed operation remain frozen. Root owns
implementation selection and execution; independent assurance remains required.

## Recommendation

Finish the already selected native aggregate boundary. Do **not** then launch
an unchanged whole-aggregate success screen simply hoping that it fits the old
guest ceiling. The retained one-child guest already exceeds that ceiling. A
new aggregate run is informative only if it answers a concrete additional cost
question or screens a justified fresh intervention.

Prioritize two small representation changes, in this order:

1. Eliminate the aggregate wrapper's second parse/allocation/drop of each delta.
   This needs no mathematical-checker change, new identity or weakened guard.
2. Replace construction of the discarded canonical theorem-proof tree with an
   otherwise identical validation-only traversal. This needs a new checker
   source binding and a careful correspondence argument, but no proof-checking
   shortcut or change to committed theorem interfaces.

Keep full bounded native deltas usable while this proceeds. The expensive seal
is a selective investment, not a prerequisite for each new contribution. The
aggregate mechanism is necessary to avoid mandatory *intermediate certificate*
production on long chains, but does not itself make proving the new mathematics
cheap. Its production cost must still support a justified benefit region.

## What the actual evidence says

| Retained evidence | Consequence | It does not establish |
|---|---|---|
| Base snapshot03 completes in 110 segments at po2=18; reported row upper bound 28,835,840 | This base can execute within its selected 2^25 ceiling | Measured exact rows, or cost of a child/aggregate |
| Base production adds 325 stages: 126,105.625 worker CPU seconds and 688.375 controller CPU seconds | Present certification is a substantial resource investment | A future seal costs the same, or produces positive net growth |
| First-child snapshot stops at `33557665 >= 33554432` | The selected child did not finish at 2^25; it has no completed snapshot/segment count | A quantified excess, a completed child receipt, or a whole-program bottleneck profile |
| Corrected two-delta packet already passes cold genuine base receipt plus actual native checks | Ordinary reciprocal contributions have a real cheap bounded route | Unlimited native ancestry or affordable aggregate proving |
| Native aggregate build01 compiles both relation rlibs but fails final linking | Source is buildable through the library boundary; use link-only repair | Any aggregate native control pass or guest execution |

Base production's carried worker subtotal is 127,958.078125 CPU seconds when
the earlier retained stages are included. Neither subtotal is the full project
cost. Nested worker/controller/outer counters must not be summed twice. Native
0.03125-second observations are timer-quantized small-call evidence, not an
estimate of guest cycles or proof production.

Sources: [base audit](BASE-PRODUCTION-AUDIT.md),
[base snapshot result](../../../experiments/v5-local-checks/module-base-snapshot-03/evidence/RESULT.json),
[failed child stderr](../../../experiments/v5-local-checks/receipt-source-integration-01/evidence/preparation/snapshot/snapshot-command/stderr.txt),
[corrected packet operation](../../../experiments/v5-local-checks/delta-reprepare-01/evidence/RESULT.json),
[aggregate implementation](AGGREGATE-IMPLEMENTATION.md).

The old guest02/guest03 partial instruction samples are useful historical
diagnosis, not current aggregate attribution. They must not be presented as
percentages of current execution, proof time or total growth cost. The prior
[frontend plan](../v5-2026-10-07/FRONTEND-COST-PLAN.md) and
[representation decision](../v5-2026-10-07/REPRESENTATION-COST-DECISION.md)
already led to moved Value constructors/extraction, owned row decoding,
validated size counting, profile2's existential conclusion and exact static
foundation comparison. Those are not new proposed optimizations.

## Separate three costs before choosing an intervention

For a batch B with delta witnesses W_i, a useful decomposition is

    E(B) = E_wire + E_graph + E_membership + E_assumptions
           + sum_i (E_parse,i + E_bounds,i + E_binding,i
                    + E_correspondence,i + E_native,i).

Here E is guest execution work under a specified metric, not native CPU. The
actual prover then has a different cost function

    P(B) = P_segments(E(B), actual segment layout)
           + P_lifts + P_joins + P_assumption_resolution + P_finish.

The aggregate route removes separate intermediate application seals and their
composition overhead. It still pays for every new proof checked inside the
batch. A constant-factor reduction in parsing need not reduce segment count;
a reduced segment count need not make fixed setup/recursion costs negligible.
Neither E nor P alone includes discovery, authoring, custody and failed work.

For a proposed representation optimization, let f be the fraction of the old
execution work actually spent in its removable operations. Even perfect
elimination can reduce that execution metric by at most f. Before measuring f,
we can prove an operation is redundant, but cannot claim a particular overall
speedup. This is a reason to make small safe removals and use phase evidence,
not a reason to launch many undirected screens.

## Intervention 1: parse each aggregate delta once

Current source is explicit:

- `aggregate/census.rs::charge(bytes)` calls strict `parse_validated(bytes)`,
  charges the resulting tree, and drops it.
- `aggregate/relation.rs` immediately invokes
  `module_relation::check_bytes(bytes)`, which strict-parses the same bytes again.
- `modules/receipt/src/relation.rs::check(value)` is already a public route to
  the same private `check_bound(value)`, preceded by `canonical_size(value)`.

The fresh successor can parse once, charge the census over `&Value`, then move
that exact Value into the **unchanged** public `module_relation::check`.
It must not expose a caller-supplied unchecked parse token, hash or authority.

Let P(b) be the current strict parser including `canonical_size`, C(V) be the
aggregate census, S(V) be `canonical_size`, and R(V) be the unchanged relation
body. On successful parsing, P(b)=V implies S(V) succeeds. The current order is

    V := P(b); C(V); drop(V); U := P(b); R(U).

The proposed order is

    V := P(b); C(V); S(V); R(V).

For fixed bytes and the pinned parser feature set, both parses produce the
same Value. The census only reads it. Thus both routes have the same successful
journal, exact returned parent journals and semantic checks; on non-resource
input failures they accept the same set. Diagnostic wording/timing and resource
exhaustion behavior are not an equality promise. Every aggregate graph, exact
EOF, image, rank, policy, membership and whole-input budget check stays.

Removed work: one strict raw JSON parse, one complete tree construction and
one corresponding destruction per delta. **Neither canonical-size traversal
is removed:** the safe public Value route retains its check. Original and new
routes each retain one tree during mathematical checking, so this is primarily
allocation/CPU reduction, not a claim to halve peak memory. It does not turn the
existing parse-then-census into global node-before-allocation enforcement.

The acceptance argument uses existing APIs, not a substituted checker or an
assumed equivalence between distinct mathematics. New code yields a new guest
image, so its receiver adoption must still bind the exact new image. Legacy
module journals, content identities and policy remain unchanged.

Minimum changed-boundary validation: an independent source proof of this call
sequence; compare exact conclusions/premises/census on the retained actual
two-delta input; focused duplicate-key, positional-record, noninteger, trailing
input and aggregate-budget refusals. Reuse existing native mathematical fixtures
and their negative proof, without Lean reauthoring, base proof repetition or an
entire unchanged network campaign. No implementation is selected by this note.

## Intervention 2: validate a theorem proof without building its unused tree

In `modules/native/checker/src/module_correspondence.rs::match_declaration`, a
new ordinary theorem calls `inventory.expression(...)` for its proof and drops
the returned canonical Value. The theorem proof is deliberately not part of
ModuleSpecID. Nevertheless this traversal is **not** currently removable: it
checks syntax/reference interpretation before the actual native mathematical
checker separately checks the proof.

A fresh validator must preserve the exact reachable traversal and assertions:
allowed tags and record fields, valid/backward row references, owner-qualified
versus foundation constants, relative-name checks, ordered universe parameters,
binder style and name bounds, `nondep=false`, per-call depth and cumulative
expansion-work limits. Preserve traversal of levels and constant references as
well as expression children. The kernel/native proof check remains unchanged.

Proof obligation: by induction on strictly earlier expression/level references,
`validate_expression(owner,index,parameters,depth)` succeeds exactly when the
old tree-producing call succeeds, with the same work-counter increment. Its
level and reference validation helpers have corresponding lemmas. The induction
must include cumulative counter state and all constructors; success-domain
equality alone without resource accounting is insufficient. Only the discarded
return Value is absent. Types and committed definition/opaque bodies still need
their exact correspondence comparisons and must not use this shortcut.

Let U be the old unfolded proof occurrence count and L its copied name/string
material. The first conservative validator retains O(U) traversals and the same
depth/work refusal envelope, while removing O(U+L) constructed output material
and its destruction. Auxiliary recursion space becomes O(depth), excluding
the already present input inventory and any retained small helper temporaries.
This is an allocation reduction, **not yet an O(unique DAG nodes) algorithm**.
It need not dominate total guest/native/prover cost.

Next, only if justified, a memoized validator could compute reachable-node
validity, maximum expanded depth and a saturated unfolded-work count. The key
must include immutable owner and ordered-universe interpretation; the unfolded
count must preserve multiplicities and current global work limits. Processing
irrelevant/unreachable rows or treating repeated visits as free can change the
accepted set. This is a stronger simulation proof, not part of the minimal fix.

The minimal source change touches the correspondence checker and therefore needs
a fresh checker/aggregate build binding and independent review. It is more
consequential than Intervention 1; do not edit a used checker or replace the
legacy I image's authority. Differential checks should include all syntax kinds,
owner/universe failures and limit edges, in addition to the actual retained
proofs and real invalid-proof refusal.

## Lower-priority changes and explicit non-solutions

| Candidate | Possible benefit | Required boundary before implementation |
|---|---|---|
| Compare canonical type/body trees against native DAG traversal without first rebuilding another Value tree | Fewer temporary allocations; still proportional to compared occurrences | Exact same interpretation, comparison and limit semantics |
| Reuse one immutable imported/foundation context across deltas | Avoid repeated reconstruction of shared premises | Prove no mutable inference/cache state can change binding, universes, atomic groups, body demands or proof checking |
| Canonical typed arenas with bulk commitments | Asymptotic representation improvement for highly shared types/bodies | Explicit content-format migration and correspondence proof; many tiny hashes can be worse than bulk hashing |
| Supported accelerated hash/prover backend | Potentially large implementation-specific gains | Compatible execution, proving, recursion, verifier parameters and exact image adoption; never force an unsupported SDK path |
| Larger guest/proof budgets | May allow completion | Does not establish affordability; needs a separately justified full-cost budget, not automatic renewal |

The fixed foundation and imported theorem proofs are already excluded from new
kernel proof checking when valid premises are supplied. Repeating "skip their
proofs" is not an optimization still waiting to be implemented. Current repeated
cost includes parsing, exact comparison, correspondence and environment setup.

Neither a successful native run nor a membership path is an aggregate receipt.
Caching another process's success flag cannot replace recursive soundness.
Dropping duplicate-key, universe, body, policy or rank checks is not an economic
optimization. SNARK/STARK succinctness lowers selected *receiver* work, while
prover expense remains a separate supply-side constraint.

## The minimum useful guest screen

An unchanged two-delta guest at the same 2^25 ceiling should not be a blind
pass/fail allocation. One child already failed there; the aggregate does more
representation/graph work and includes a second child. This is a strong
engineering warning, not a strict cycle-monotonicity theorem across new
compiler layouts and images.

A justified next screen must be one of:

- A single fresh aggregate image with selected, independently reviewed
  representation changes, using the already retained mathematical packet, to
  test completion and actual execution segmentation under a prospective bound.
- One bounded phase-informative diagnostic for that image, only if phase
  attribution is needed to choose the next change. The supported executor's
  instrumentation must be inspected first; record aggregate framing/census,
  each mathematical relation, assumptions and commitment phases separately
  where feasible, with bounded outputs preserved on failure.

Instrumentation itself is not the adopted production relation. If it changes
the image or adds work, label that distinction and account for the perturbation.
An old PC prefix, sampled SDK field of ambiguous units, or a failure with no
phase markers is not an exact cycle attribution. If useful phase evidence
cannot be obtained under a small finite envelope, the source-proved removals
can still be reviewed before spending another guest run.

The screen must retain exact source/runtime/image/input/journal/assumption
bindings, the old failed boundary, and actual closure/limits. It runs no segment
proof, lift, join or recursive proof campaign. Failure does not automatically
increase the cap. Completion provides feasibility and real segment data, not
full v5 admission or an assumed affordable seal. Only then should root consider
a separately finite proof-production selection tied to a workload benefit bound.

## Connect implementation to growth, without repeating the old theorem

[DELTA-SEALING-POLICY](DELTA-SEALING-POLICY.md) already gives exact-frontier
marginal accounting, and [GROWTH-WORKLOAD](../v5-2026-10-07/GROWTH-WORKLOAD.md)
gives the strong optimized-local comparator and fixed-target rent-or-buy result.
The actionable consequence here is to obtain a defensible production bound
for **one actual aggregate packet rewrite**, not use base proof cost or a usage
counter as a surrogate.

For that rewrite, record selected receiver bytes/checks/demanded semantics before
and after sealing; keep still-required branch frontiers in both routes. Compare
full additional production/failed-work/service cost S+M with justified aggregate
recipient savings. A nonempty region exists when some matched cache/horizon
class has a positive per-use margin d and enough distinct costly uses N satisfy

    N * d > S + M.

This condition becomes a software decision only when d, S and M are measured
or bounded for the proposed route. If d<=0, increasing popularity never fixes
it. If S is unbounded or a successful seal unavailable, the fixed-target
competitive guarantee does not apply. These limits favor an affordable default
native route plus selective genuine seals, not proof generation for every
publication and not unsupported claims of inevitable exponential growth.

The present central deliverable is therefore: trustworthy aggregate-DAG
functionality **and** a justified affordable supply path, alongside useful
decentralized discovery. Finishing only the receipt mechanism, only the source
theorem, or only a cheaper representation does not finish v5.
