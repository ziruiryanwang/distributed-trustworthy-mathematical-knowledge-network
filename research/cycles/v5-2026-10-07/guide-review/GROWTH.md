# Growth, usefulness and sustainable reuse: guide contribution

Documentation-only synthesis, 2026-10-08 UTC. Read against the current
`PAUSE-HANDOFF.md`: v5 is unfinished and paused. This note starts no experiment,
monitors no background proof and changes no product source. Paths below are
relative to the sole canonical project root.

## What we mean by mathematical knowledge growth

A proved theorem does not enlarge the unrestricted consequences of the same
foundation. If the foundation F already proves p, then adding p as a reusable
lemma leaves its deductive closure unchanged. A safe explicit definition can
likewise be eliminable without being practically dispensable. What changes is
what a finite agent can **find, justify and use at an affordable cost**.

This avoids the logical-omniscience mistake: being a consequence of one's
axioms is not the same as possessing a usable proof or knowing how to obtain it.
The commons is intended to accumulate accessible, independently warranted
capabilities, including definitions, general methods, algorithms and theorems.
It need not settle whether mathematical objects are discovered or invented.
Formalist, structuralist, realist and constructive interpretations can share
the operational contract. Assurance remains conditional on the adopted formal
foundation, implementation and cryptographic assumptions; none is made sound
by popularity or a network vote.

For precision, fix a checking policy P, a particular agent/procedure, an
accessible library K and a finite resource vector b. Write

```text
Reach(K, b, q): this specified agent can produce a P-accepted solution to q
               within b, using the declared procedure and access conditions.
```

An observed or analytically justified expansion of the attained frontier is a
growth result: more selected endpoints become achievable, or the same endpoints
need fewer resources. This is not an executable oracle for optimal reasoning.
The evaluation family of endpoints is an external scientific instrument, not a
required task list, protocol goal or human-intention field. Agents choose their
own investigations. Mathematical admission is independent of their intentions.

Keep five questions separate: validity, exact object identity, availability,
discoverability and downstream benefit. A valid but redundant theorem remains
valid. A useful theorem can temporarily be unavailable. A frequently cited
theorem need not save work. A content hash recognizes exact identity, not all
mathematical equivalence; universal semantic novelty/usefulness is not assumed
decidable. Definitions can be useful compression, while excessive unfolding or
abstraction can also make reasoning harder.

Sources: `research/cycles/v4-2026-10-02/PHILOSOPHY-OF-GROWTH.md`;
`research/cycles/v5-2026-10-07/GROWTH-WORKLOAD.md`, "What grows".

## A concrete example and three fair comparisons

The selected v5 example is a polymorphic binary tree, its map and fold, and a
generic fold-fusion law. A fold interprets leaves and combines child results.
If h preserves both interpretations, structural induction gives

```text
h (fold leafA nodeA e) = fold leafB nodeB e.
```

The premises are `h (leafA x) = leafB x` and
`h (nodeA x y) = nodeB (h x) (h y)`. At a leaf use the first premise; at a node
use the second and the two induction hypotheses. A later agent can instantiate
the law for numeric aggregation, leaf collection or paired summaries, while
proving the actual applicability premises. A false premise cannot be replaced
by a popularity score or a successful search response.

For a specified strict evaluator, fusing map followed by fold avoids allocating
the intermediate mapped tree. Both versions are linear traversals, not an
exponential speedup. A good ordinary optimizer may already perform this fusion.
The law's algorithmic merit is therefore different from the network's merit.

Compare equal starting mathematics, representations, optimizers, checkers,
cache states and application requests:

1. Independent optimized local libraries, discovering/caching a generic method
   once per library, not once per instance.
2. Ordinary decentralized named-module sharing, with local proof checking and
   caches. This tests whether succinct certification adds anything beyond sharing.
3. The certified-module/discovery route, including its production and services.

Allow every route existing generic methods and legitimate shortcuts. Do not
pretend a warm cache is cold, count repeated use as independent installations,
or infer an optimal proof-search lower bound from one slow tactic. A dependency
edge proves use, not necessity or causal benefit. Compare downstream outcomes,
not publication of the very object whose usefulness is being assessed.

Source: `research/cycles/v5-2026-10-07/GROWTH-WORKLOAD.md`, method family and
strong comparisons; `research/cycles/v4-2026-10-06-resumed/APPLICATION-AND-NET-GROWTH.md`.

## When reuse really pays

For recipient i, let D_i be the selected baseline's cost of attaining/using the
method, and R_i the network search, acquisition, authentication, installation
and application cost. Let F be additional fixed production, generalization,
certification and publication costs. Let M include retention, replication,
repair, failed searches/proofs and background services over a stated horizon.
Shared costs cancel. Count physical resource use once, rather than adding a
provider's bill and its recipient's payment for the same work.

For explicit nonnegative prices w on additive resource coordinates, net benefit
means exactly

```text
sum_i w · (D_i - R_i) > w · (F + M).
```

If each of N distinct recipient libraries avoids at least d, its variable
network/service cost is at most r+m, fixed cost is at most f, and d > r+m, then
`N > f/(d-r-m)` suffices. This follows simply by summing the margins. It is a
conditional theorem, not evidence that demand N exists or that the measured
margin is positive. More recipients cannot repair a negative per-recipient
margin. Without prices, retain resource vectors/Pareto comparisons; do not add
seconds to bytes. Peak memory is a constraint, not an additive bill across
sequential uses. Latency and shared-resource interference require their own model.

Succinct receipts have the same investment structure. Against a specified cold
ordinary proof-package verifier, if each installation saves at least delta > 0
in the chosen valuation, added maintenance is at most m0+N*m with m < delta,
and added certification costs f, then `N > (f+m0)/(delta-m)` suffices. These
hypotheses may be justified analytically or experimentally, with provenance
visible. They must include the **whole** receiving route, not just its inner
cryptographic verification time. The selected small workload's cheap warm
native checks do not currently establish a positive receipt margin.

Source: `research/cycles/v5-2026-10-07/GROWTH-WORKLOAD.md`, break-even and D08.

## Two kinds of scale, and what a certificate does not compress

Let G be the whole network corpus and H the selected ancestral theorem-proof
DAG. Search should not require enumerating G or contacting every participant.
Certified reuse should not require downloading and replaying H. These are
different problems. Neither permits ignoring the selected theorem types,
transparent definitions, inductive interfaces or computation actually demanded.

The intended receiving/use decomposition is

```text
T <= n_v V + T_open(I) + T_check(L, I, S) + A.
```

Here n_v counts actual certificate-verifier calls, including failures/repeats;
V bounds one call; I is all selected interface/opening data; S is all demanded
semantic data; L is the new local proof work; A covers complete acquisition,
including failures. Include transitively demanded owners and restart passes.
The producer's certification cost is separate and remains payable.

Conditional justification: genuine adopted certificates ground imported
theorems; exact commitments authenticate their interfaces and needed bodies;
the checker validates new declarations; the import route never reads old opaque
theorem proofs. Partitioning that route's work gives the displayed expression
without a mandatory H replay term. Grounded, rank-decreasing composition and
the adopted certificate/checker soundness assumptions are essential; hashes
alone do not suffice. Holding I, S and the other terms fixed, adding ancestral
proof witnesses creates no new import operation. If those terms are uniformly
bounded, N successful extensions need only linear aggregate receiving work,
plus actual maintenance. This contrasts with a specified cold replay algorithm,
not an optimized accepted cache, and is not constant-time arbitrary mathematics.

Representation is another central limit. Repeated shared syntax can expand
exponentially if encoded as a tree: `t_(n+1) = f t_n t_n` has a linear-size DAG
but exponentially many expanded occurrences. A proposed canonical semantic DAG
preserves sharing through commitments, normalization and indexing. It is not
implemented; transport compression followed by tree expansion does not solve
this problem. Even perfect syntax sharing cannot make arbitrary conversion cheap.

Sources: `research/cycles/v5-2026-10-07/GROWTH-WORKLOAD.md`, D10;
`research/cycles/v5-2026-10-07/COMPACT-SEMANTIC-DAG.md`;
`software/v5/authoring/API.md`; `software/v5/admission/README.md`.

## Bounded exploration without a central research agenda

Search/ranking can be heuristic while acceptance stays exact. The existing
discovery API bounds a complete session across providers, pages, bytes, failed
attempts and time. Its positive-candidate route authenticates returned committed
records, not omitted intervals, honest metadata, mathematical truth or global
completeness. Ordinary pages authenticate selected snapshot intervals, still
not the global corpus. Exhaustion means incomplete/unknown, never nonexistence.
Common-feature intersections may remain linear at a provider.

A useful local strategy is to preserve an unchanged direct reasoning route and
spend at most H_search on optional discovery/application. If it fails and the
baseline remains available, total additive cost is at most
`H_search + baseline cost + switching/setup cost`. That bound requires real
containment and no destructive interference with the baseline. Merely prompting
an LLM to be economical does not enforce it. A stronger two-route scheduled
bound exists under preemption and isolation, but is not the present implemented
portfolio guarantee.

Local usage, witnessed downstream completion, costs, uncertainty and diversity
can guide which candidates or small bundles to investigate. Complementary
lemmas can have zero benefit separately and positive benefit jointly, so ordinary
submodular/greedy guarantees cannot be assumed. Retain bounded exploration of
low-history candidates; it does not guarantee finding every rare valuable idea.
Older CACHESEL1 mechanisms are prior work, not a newly integrated v5 policy.
No global popularity ledger, mandatory tasks or natural-language interface is
needed for these choices. Documentation can teach agents a strategy; the network
must supply accurate authority, cost and incomplete-result boundaries.

Sources: `research/cycles/v4-2026-10-06/GROWTH-MECHANISM.md`, Mechanism D and
complementarity; `software/v5/transport/SEARCH-API.md`.

## Selective certification and sustainable custody

An optional proposed route checks a complete bounded native delta DAG above
genuine certified frontiers. Every frontier receipt is verified; every delta's
actual dependency journals must already be established; the target must match
the adopted profile even with zero parents. Aggregate bytes, nodes, edges,
semantics and checking work are bounded. Depth alone is insufficient. Beyond
that envelope, refuse or obtain a genuine seal; never allow an arbitrarily long
unsealed history to masquerade as constant-cost reuse. This design is not yet
implemented, and broadens the native trusted computing base.

Once both native and sealed routes exist, a local rent-or-buy rule has a useful
conditional guarantee. For one fixed target/profile/horizon, let delta_i >= 0
be the extra native cost known **before** request i, and S > 0 the complete cost
of an available successful seal. Rent while accumulated extra cost plus delta_i
is at most S; otherwise seal before the request. Prior rent is at most S, so
the incremental cost is at most `2*min(S, sum delta_i)`. Adding the same common
per-request cost preserves a factor-two bound for total cost.

The assumptions matter: a budget does not guarantee successful proving; unknown
post-payment deltas permit arbitrary overshoot; failures and delayed service cost
money; a warm cache is not a fresh rental; overlapping targets/cache changes
break the simple model. Independent operators buying duplicate seals do not
inherit a network-wide factor-two bound. The rule optimizes investment for
selected uses, not the mathematical usefulness of those uses. It remains a
proposed owner policy, not a current v5 service or observed growth result.

Availability is a separate paid service. A hash cannot reconstruct lost bytes,
and a valid receipt cannot make an offline custodian answer. Operators need
finite storage/service epochs, retained exact interfaces/bodies/evidence,
replicas, index refresh, repair and an explicit admission/renewal policy. Stop
advertising unfunded promises. A provider-loss demonstration needs an actual
alternative index/custodian or already retained local data. No perpetual global
availability, universally fresh global view or correctness from custody status
follows from decentralization. Purely reconstructible caches may be discarded
only while preserving the exact dependencies/evidence needed for reconstruction;
the v4 accounting result did not implement automatic eviction.

Sources: `research/cycles/v5-2026-10-07/DELTA-FRONTIER-NATIVE-SEAM.md`;
`research/cycles/v5-2026-10-07/GROWTH-WORKLOAD.md`, D21;
`research/cycles/v4-2026-10-07/GROWTH-OPERATING-REGION.md`.

## What exists, and what must not be claimed yet

| Item | Status at the documentation pause |
|---|---|
| Bounded formal discovery and authenticated candidate/interval APIs | Implemented source with scoped controls; not universal recall or mathematical admission |
| Lean authoring over selected module interfaces and demanded bodies | Frontend compiled/linked; five conditional native controls passed; no genuine receipt-to-child endpoint established |
| Public fixed worker and owner author/snapshot controller | Implemented; independently audited 20 and 9 focused controls passed using mock native calls, not mathematical handles |
| Bounded public producer and receiving API | Implemented source; base production was live at pause; no terminal result or positive profile-2 admission adopted in this guide |
| Proof-ancestry-free composition | Precise conditional architecture obligation; genuine base/recursive-child/cold-admission integration still required |
| Native bounded deltas, selective sealing policy, compact semantic DAG | Proposed, not implemented |
| Full-cost v5 useful-growth advantage | Conditional models and substantive workload; positive end-to-end net benefit not yet established |
| Globally workable v5 release | Unfinished: availability/deployment, integration, assurance and growth obligations remain open |

The next substantive evidence is the genuine discover/acquire/admit/author/
certify/contribute/reuse loop, followed by a defensible full-cost operating
region against the strong baselines. Neither mock controls, a shorter metadata
reply nor a new receipt count replaces it. The network may support compounding
reuse; there is no present theorem or experiment showing sustained exponential
useful growth. Fixed resources, maintenance, semantic complexity, redundancy and
changing demand prohibit inferring that claim from a branching dependency graph.

Current-state sources: `research/cycles/v5-2026-10-07/PAUSE-HANDOFF.md`;
`research/cycles/v5-2026-10-07/PLAN.md`;
`software/v5/production/API.md`; `software/v5/preparation/API.md`;
`software/v5/authoring/API.md`; `software/v5/admission/README.md`.
