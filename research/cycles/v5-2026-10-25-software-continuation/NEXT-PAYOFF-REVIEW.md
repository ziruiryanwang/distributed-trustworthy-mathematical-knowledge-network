# After contact lookup: make a useful relation query selective

2026-10-25. `concept_software_bridge`; source/theory-only next-payoff review.
Canonical guard passed. No code, tests, build, network, Git, shared-ledger or
paper mutation. This checkpoint does not adopt the contact campaign's results;
root is handling those separately. Full deployable v5 remains unfinished.

## Specific recommendation

**Next resolve and implement bounded ordinary relation-query selectivity, not a
new concept-generation subsystem.** The promising route is provider-local
materialized pair access paths over the existing atomic feature postings,
with an explicitly versioned sparse-positive candidate protocol. Prefer this
over adding paired features to every mathematical-discovery record/namespace,
provided the separate source contract closes readiness, maintenance and quotas.

This is not a recommendation for another toy growth experiment. It removes a
demonstrable resource obstruction on a query an investigator developing concepts
can already express. A local pair cache is a database access path, not a new
mathematical concept, novelty score or evidence of research acceleration.

## The actual investigator workflow

An investigator has encountered an interface and an operation, knows their exact
portable symbols, and wants to know what existing work connects them before
choosing whether to refine the interface, restrict the operation or investigate
something else. Search for declarations whose types mention both symbols; inspect
the returned statements, independently acquire/check useful mathematics, then use
the existing approved ordinary Lean project and return path for new definitions
and consequences. No global research task or mandatory compatibility predicate.

This is not invented demand solely to favor a two-feature benchmark. The current
paper supplement's `Witness.lean` contains `old_law_does_not_lift : ¬ Stable qG f`
(line 68) alongside positive stability laws and projection/partition theorems.
Someone knowing `qG` and `f`, but not this theorem's name or exact formulation,
can legitimately seek statements mentioning both. A broad relational query can
expose an obstruction as well as a candidate proof. This is a source-derived
workflow example, **not an observed user query frequency or instruction to rerun,
export or publish the paper artifact**.

The current ordinary adapter already supports that exact-symbol conjunction:
`ordinary_export_adapter.py:60-92,132-219`. It indexes declared-type symbols,
not proof-only occurrences. The shipped query helper also supports exact type
keys and checked-context bindings. Do not implement a duplicate authoring/query
interface. Likewise, exact-type lookup is a useful alternative when the desired
complete statement is known; it is not equivalent to asking what relations exist
between two concepts. General theorem instantiation, unfamiliar vocabulary and
semantic equivalence remain separate, unsolved retrieval questions.

## Why this outranks another growth mechanism now

The latest paper explicitly treats ordinary persistent libraries as a legitimate
implementation. Its exact examples explain how new combinations can motivate
new concepts, including a simpler concept incomparable with an older one. They
do not establish that a new scheduler, relation workbench or refinement score
improves real investigators' decisions. `PLURAL-SCOPE-PAYOFF-CHECK.md` also rejects
inferring symbolic-library cost savings from its concrete-object information
bound. The [paper/software checkpoint](PAPER-SOFTWARE-IMPLICATIONS.md) already
separates these claims.

The existing public loop supports definition/theory authoring, inert inspection,
optional source offers, independent intake and return. Current evidence gives no
newly absent creative-authoring operation that would justify another module or
agent platform. The best additional software support for this particular loop
is therefore to retrieve relevant existing relational evidence within a finite
budget. This preserves independent inquiry without pretending the index creates
the research question or decides what mathematics matters.

## The existing source-level obstruction

For the selected provider/partition, let `L_A` and `L_B` be the authenticated
atomic posting lists for the two query features. Current `candidate_query.page`
chooses the minimum-count atomic anchor and examines its ordinal positions in
order, probing secondary membership before loading/proving surviving records.
This is genuinely better than transmitting all rejected records, but still
visits the chosen anchor's rejected IDs.

Take `n` A-only records, `n` B-only records and one AB record last in both lists.
Both anchors have `n+1` entries, so the current algorithm visits `n+1` IDs to
reach the hit. A scan allocation at most `n` misses it despite an honest live
provider, perfect routing and valid records. The earlier
[selectivity audit](SEARCH-LOCALITY-DECISION.md) gives this family and the exact
current source trace. No huge local experiment is necessary to establish it.

### Why a transparent server-only patch is not enough

Current `candidate_query.verify_page` explicitly requires

`response.next - request.start <= response.charged.scanned`.

Each hit's anchor ordinal must also lie in that advanced range. Jumping from
ordinal zero to a sparse hit at ordinal `n` while charging one visited cache
row is therefore rejected. Charging the skipped ordinal distance instead keeps
the old finite scan barrier even if CPU work was saved. SearchSession reserves
the full requested scan allowance against its aggregate examined budget and
never refunds it from unauthenticated provider counters.

Consequently **new opt-in sparse-positive wire/accounting semantics are needed**.
Do not silently remove this V1 condition or claim zero client change. The
mathematical/index namespace, atomic records, snapshot roots and membership
proofs need not change merely because traversal accounting changes. Explicit
request/reply version selection and unsupported-version outcomes remain part
of the separate integration decision; no renewed fallback grant is permitted.

## A narrow design with a useful conditional argument

For an explicitly selected pair `{A,B}`, maintain a provider-local ordered
access path to objects in `L_A ∩ L_B`, retaining each original atomic ordinal
and admission sequence. Initially use it only when the existing authenticated
minimum atomic anchor is A or B. Support that anchor's order, or decline the
optimization. This restriction avoids a new planner that sorts arbitrary
pair results into a third feature's order; the counterexample is already fixed.

Require the cache to be bound to this provider store/namespace and known complete
through the selected snapshot's local cut before it can claim a local end of
that access path. Retain the original snapshot's atomic-count ceilings and
object-admission cutoff. A newer cache must not leak later admissions into an
old snapshot. An absent/incomplete cache selects the existing bounded scan or
explicit incomplete/unavailable outcome, not a claimed empty mathematical corpus.

Every emitted hit still carries the original atomic vector proof at its actual
ordinal, binds the canonical record and partition, and checks that the record
contains every requested atomic feature. Thus a bad cache cannot create an
accepted positive record without defeating the unchanged proof/record checks;
omission remains possible and unverified, exactly as the positive-only contract
already says. Correct local cache maintenance is separately necessary for the
honest-provider search-efficiency/recall argument, not a cryptographic theorem.

**Conditional cost statement.** Let `a` be the original atomic anchor size and
`r` the selected pair intersection size in this snapshot/partition. Assume a
complete ordered pair access path, bounded indexed seeks, and the retained
snapshot/proof checks. Full traversal visits at most `r <= a` candidate rows,
plus bounded seeks and any remaining query-feature probes. In the family above,
`r=1` while `a=n+1`: unrelated A-only/B-only additions do not add visited pair
rows. SQL tree navigation and Merkle proof height can still grow logarithmically;
this is not constant total work or universal semantic-search scalability.

Sparse continuation must keep the original anchor ordinal as a position, but
must not call the skipped distance a verified scan. Charge actually attempted
cache/record probes, SQL VM work, hashing, proof reads, bytes and deadlines;
reserve the selected per-page work allowance conservatively in the client even
if a provider claims less. Preserve hit order, original range bounds, strict
progress or termination, duplicate handling and explicit unverified coverage.
Simply deleting the old delta check without defining those semantics is not
an implementation.

## Reuse, costs and why not the old paired-feature profile

Reusable seams are the current `candidate_query._ReadIO` resource meter,
snapshot descriptor loading, ordinal/secondary probes, canonical record checks
and `authenticated_index.vector_get/verify_vector`; SearchSession's conservative
ticket accounting; and FairSearch's bounded positive-only pagination. Existing
pair-profile code supplies the elementary conjunction predicate/benefit argument,
not the ordinary adapter, schema or a ready-made local cache.

The old `conjunction_index`/`pair_planning` lane embeds its profile in feature
schema/namespace, adds paired features to records, and expects matching client
profiles and fresh indexes. Porting it remains a valid fallback, but at very
large scale it introduces profile fragmentation, additional committed data and
cross-profile handoff work. A local access path keeps atomic discovery identity
and route keys stable while providers choose different optimizations. It does
still require new sparse-protocol client support plus bounded local cache
lifecycle; it is **not proven cheaper in total implementation effort** merely
because commitments are unchanged.

Build/catch-up, update, retained cache bytes, consistency checks and unsuccessful
queries must all be charged. For a stated resource unit, choose the cache only
when expected accumulated query savings exceed those costs. A first one-off
query need not repay construction. Limit the number of configured pairs and
cache space; do not enumerate all pairs or hide a whole-corpus rebuild inside
the first bounded query. Correct readiness/fallback and crash behavior are the
separate source-contract owner's current challenge, not assumed completed here.

## Smallest decision-changing falsifier and stop condition

First adopt a precise sparse protocol/cache contract, with no runtime. Then one
small inert changed-boundary test is sufficient to challenge its key premise:
two A-only, two B-only and one AB record in one partition, AB appended last.
V1 with a scan allowance of two cannot emit the hit; the new access path must
emit the **same original committed record** at its original anchor ordinal
while visiting one pair candidate and respecting all remaining allowances.
No native proof work, mathematical-growth experiment or giant corpus is needed.

Also require the smallest old-snapshot/later-append and incomplete-cache controls:
the earlier snapshot must exclude a later AB object, and an unready cache must
not masquerade as exhausted complete access. Tampered ordinal/proof, exhausted
SQL/probe allowance and unsupported protocol must remain bounded failures.
If this requires namespace-changing commitments anyway, an unbounded catch-up
on request, weakened hit verification or a new owner grant, reject this design
and reconsider the explicitly profiled alternative. A bounded tiny test does
not establish query demand frequency or net growth; no such claim is selected.

Do not replace this with a larger peer-count test, partition-fairness-only patch,
conjecture scheduler, compulsory scope card, universal equivalence index or
another certificate campaign. They do not remove this precise present barrier.
Once this workflow works, reevaluate the next actual obstacle; do not turn local
cache optimization into an open-ended new subsystem.

## Read sources

- Current `papers/PAgE-2027/paper/blue-sky-final/main.tex`, especially Sections
  2, 4 and 5; paper `research/PLURAL-SCOPE-PAYOFF-CHECK.md`; final completion
  note's explicit analytical/not-empirical boundary.
- `papers/PAgE-2027/artifacts/scoped-adequacy-lean/Witness.lean` and the existing
  ordinary operator kit's authoring/search handoff, without rerunning either.
- Adopted package `support/discovery/candidate_query.py`, `search_session.py`,
  `discovery_store.py`, `ordinary_export_adapter.py`, and `fair_search.py`.
- `software/v5/conjunction_index/CONJUNCTION-INDEX.md` and
  `software/v5/pair_planning/discovery/module_export_adapter.py`.

Root's current contact successor changes transport/API composition, not the
candidate/store/atomic adapter contract audited here. The new contact campaign
does not remove this next selection's separate implementation/review obligations.
