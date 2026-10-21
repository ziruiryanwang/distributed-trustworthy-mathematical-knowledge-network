# After exact custody: expose already paid-for selective pair postings

2026-10-20, core_release. Source/theory decision only. No code import, parser,
test, build, network, native/proof execution or Git operation was performed.
Root owns implementation selection and adoption. This note does not adopt the
pending installed exact-custody outcome or declare v5 complete.

## Decision

**Do not build materialized conjunction storage again.** It is already in the
current source. The recommendation in GROWTH-OPERATING-REGION that treats its
absence as current is superseded by the source facts below; do not edit that
historical checkpoint to erase the discrepancy.

The next small discovery improvement worth selecting is an **opt-in,
route-preserving pair-query planner**. It exposes additional eligible pair keys
already materialized by the selected profile, within the existing eight-feature
query cap. Existing authenticated summaries then choose the least expensive
included anchor independently in each local partition. No new statistics RPC,
query generation, storage schema, distributed placement protocol or experiment
campaign is needed to establish its principle.

Do not change the default compiler or silently replace old route predicates.
Keep every legacy compiled feature and add only logically redundant eligible
pair keys. This is slightly less aggressive than replacing covered atoms, but
preserves existing rendezvous routes by construction and supplies a substantial
selectivity separation on a precise supported query class.

This is not a claim that the retained evaluator-method growth workload needs
multiple pairs: core_growth reports that its independently derived query can
use one declared-type-key plus declaration-kind. The improvement concerns the
architecture's supported multi-predicate discovery class, not observed useful
growth or a measured economic saving.

## Current sources, not historical implementations

Source map: `experiments/v5-local-checks/distribution-body-custody-01-input.json`,
SHA-256 `995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`.
This is the 114-source integration selection. Root's latest desk decides whether
its installed outcome has been adopted; its discovery mappings are the ones
reviewed here.

| Logical function | Selected physical source and SHA-256 |
|---|---|
| Profiles, extraction and query compilation | `software/v5/instantiation_discovery/discovery/module_export_adapter.py`, `508fe4449de8ffcdaccf6b06c1ceb133006cfdb91cc7a180e6e0ffd066a371ac` |
| Authenticated local planning/coverage | `software/v5/discovery/discovery_query.py`, `f9ce09ba74e7656a2f53d813489a43434258208198bcb4784c0e4eb682ac24e2` |
| Iterative direct queries | `software/v5/iterative_queries/client/direct_contacts.py`, `e243a094b9fdce2adef221514923bf6753d04b8cc3ed8ae60e392c0ebd804545` |
| Iterative located queries | `software/v5/located_queries/client/located_queries.py`, `419df8428528203858eff69da43c7e3ed7e5634d06007dc5e30ca2f33df82c4e` |
| Legacy one-shot remote query | `software/v5/conjunction_index/client/workspace_atomic.py`, `eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022` |

The adapter already supports a namespace-bound profile of one to eight canonical
atomic pairs, mutually exclusive with its type-pattern/fingerprint profiles.
Extraction retains the original atomic keys and emits each configured pair key
iff both atom keys occur. At most eight extra postings per export are incurred;
the existing feature/record/work limits remain. Store admission incrementally
updates immutable authenticated trees, not a whole-corpus rebuild.

The current `compile_query` accepts one to eight atomic specifications, replaces
only the first canonical eligible pair, and retains all other atoms. Summary
verification authenticates counts and roots for precisely those requested keys.
`plan_partitions` chooses the smallest authenticated count separately for each
of the fixed 256 ExportID-prefix partitions. No rarity information for an
unrequested eligible pair reaches that planner.

The old pair controls already establish a selected atomic-versus-pair scan
separation and old-snapshot isolation. Repeating those controls does not test
the newly identified multi-pair selection seam.

## Present supported cost and coverage statement

Fix a finite family of provider snapshots. Let `P(i,p,f)` be the posting set
for feature f, provider snapshot i and local partition p. For requested feature
set F, full conforming anchor traversal examines

    S(F) = sum_(i,p) min_(f in F) |P(i,p,f)|

rows before page/retransmission overhead. A selective final intersection alone
does not bound S(F). Candidate-only pages authenticate positives but do not
prove intervening scan coverage; normal pages authenticate consecutive anchor
intervals and the matches within them.

For at most a query-derived routes and r attempted providers per route, work
has the conditional form

    O(a*r*R(Peers) + a*r*H(k) + S(F)*log(B) + returned_bytes).

Here R is the actual routing cost under its separate network assumptions;
k<=8; H(k) is bounded summary decoding/authentication over k feature proofs and
256 partition descriptors per present feature; B bounds local posting capacity.
Record length and vector height also have fixed implementation caps. This is a
conforming-algorithm bound, not authenticated accounting of a malicious server's
CPU or every DHT wire byte. The client's original aggregate requests, bytes,
scan, provider, process and time allowances continue to bound authorized work.

If a,r,B and selected S(F) remain bounded as unrelated mathematics grows, no
global-corpus scan term is introduced. Those selectivity/routing assumptions
must be supplied, not inferred from hash sharding or a first-page limit. The
software does not promise all providers, all corpus entries or an arbitrary
mathematical-equivalence search have been covered. Even complete normal-page
coverage is complete only within the committed index, conditional on correct
construction: `build_assurance=NOT_PROVIDED`, `global_complete=false`.

## Exact proposed planner and its claims

Let A be the distinct requested atomic feature keys, n=|A|<=8. Let E be the
canonical list of eligible profile pairs whose two atom keys lie in A, m=|E|<=8.
Let L be the existing compiler output. If m>0, L has n-1 keys: the first pair
key and all atoms except that pair's endpoints. Otherwise L=A.

The optional planner computes:

1. Run the unchanged compiler, including all current profile/fingerprint checks.
2. Start F=L. Enumerate eligible pair keys in profile order, skipping keys
   already in F. Add keys until |F|=8 or all eligible keys are included.
3. Return canonical F together with legacy L, the added/omitted eligible keys,
   and an explicit status such as `ALL_ELIGIBLE`, `WIRE_CAP` or `NO_EXTRA_PAIR`.
   A caller never mistakes a cap-limited choice for a cost-optimal plan.

The exact external spelling is implementation work; the invariants above are
the contract. Inputs and returned metadata are bounded. No caller-selected raw
feature hash substitutes for the profile-derived eligibility check. Type-pattern,
fingerprint and unprofiled queries retain their old features and validation.

### Predicate preservation

For a correctly extracted record x, every added pair key is present iff its
two requested atomic keys are present. Thus

    matches(x,F) iff matches(x,L) iff every requested atomic predicate holds.

This is not arbitrary mathematical equivalence: it is the explicit pair
extraction rule. Committed indexes may still be incomplete/misconstructed;
acquisition recomputation authenticates returned records but cannot certify
unreturned objects. Mathematical acceptance remains a separate gate.

### Anchor-work dominance, not universal total-cost dominance

Since L is a subset of F, `min_(f in F) |P(i,p,f)|` cannot exceed the old minimum
for any provider partition. Therefore `S(F)<=S(L)` even before assuming correct
feature extraction. Exact equality of answer predicates uses that assumption.

The additional summary keys and response metadata cost something. This is not
a claim that every tiny query is faster. On a correctly built index, when all
eligible keys fit, the resulting anchor is as selective as the best of all
available requested atoms and all eligible configured pairs: the omitted first
pair endpoints cannot beat their intersection. No statistics roundtrip is
needed because all considered keys appear in the original ordinary summary.

For m>0, all keys fit whenever `n+m-2<=8`. In particular, every query with at
most four distinct atoms and every possible eligible pair fits (six pairs on
four atoms yields eight keys). For larger cases exceeding this bound, the
canonical cap-limited prefix remains no worse in anchor count than L, but a
more selective omitted key can exist. Do not claim optimality there.

### Large hot-key separation with unchanged stored records

Take requested predicates A,B,C and a profile whose first eligible pair is AB
and later eligible pair is AC. In each of the 256 local partitions place N
records satisfying A and B but not C, and N satisfying C but not A. Place one
additional record satisfying A,B,C in one partition. These are ordinary finite
posting-set conditions; a later control must use constructible valid exports,
not merely fabricate a provider count.

The old query is {AB,C}; its total anchor scan is `256*N+1`. The new query is
{AB,C,AC}; AC occurs only once, so the total anchor scan is one. The new ordinary
summary has one additional feature, with no extra query generation or provider
lookup. Unrelated one-sided corpus growth increases the old work and leaves
the new selected work fixed. Within actual object/posting quotas the ratio is
finite but can be large; an asymptotic family with scalable capacities has an
unbounded ratio. This is a theoretical selected-query separation, not measured
network latency or empirical growth evidence.

### Route and operation compatibility

Current `next_located_query` requires every configured route feature set R to
be a subset of the actual query features. An old valid route has R subset L;
because L subset F, it remains valid without changing its namespace, predicate,
stripe, route hash or provider advertisements. The owner should continue using
legacy `compile_query` output (or existing configured subsets) for route plans.
The optional richer F is for search, not an implicit advertisement migration.

Replacing L with pair keys while removing additional atoms would break this
property. Even mathematically equivalent route predicates have different exact
hashes; that more aggressive approach is rejected for this small change.

One immutable search session is constructed with F before its first request.
The same current authenticated offer/page code sees F and chooses anchors;
no already-active session is rebound after a summary. Existing acquisition,
reader, endpoints, trust and original envelope remain unchanged. All attempts,
larger summaries and any resulting refuses consume the existing allocation.

## Smallest product delta and discriminating verification

Root could select three successors: adapter with a new opt-in planner method;
current iterative direct-query helper; current iterative located-query helper.
The latter two accept a strictly validated opt-in and use the resulting F when
constructing their one session. Defaults retain existing results and reports.
Expose the finite planner status for opted-in callers. Legacy one-shot `find`
and `compile_query` need not change. Public facades already export these helper
functions; implementation review must confirm their signatures rather than
invent another orchestrator. No new store, index wire, page verifier, metadata
authority, route role, operator profile or proof path is required.

Before runtime, independently review these narrow claims:

- Legacy outputs and source-profile namespaces remain byte-identical.
- Pair additions are eligible, bounded, canonical and semantically redundant.
- Eight-feature overflow is explicit and never borrows a ninth generation/key.
- Every old valid route remains a legal unchanged subset of F.
- Direct and located operation factories use F before session creation, leave
  all bindings/budgets intact, and do not grant a caller raw-feature authority.

The smallest changed-boundary controls would check no-profile/default
compatibility, a realizable hot-first/rare-later pair separation, cap-limited
status, unchanged legacy routes, and direct/located session binding. Existing
real structural stores and deterministic/inert transport suffice for this seam;
no new Lean proof, general integration campaign, RAM survey or scaling benchmark
is justified by this decision. Root separately selects any execution.

## Why not the other proposed mechanisms now?

- **Profile selection alone:** a new profile containing only the rare pair can
  work, but changes the namespace and may require another indexed corpus/view.
  This proposal reuses all existing postings and one current namespace.
- **Eight alternative query generations:** adds offers/routing and can exhaust
  the envelope before selecting a winner. Not needed when all keys fit once.
- **Cost-based all-profile planning:** can need statistics for keys outside the
  eight-key query, plus new binding/coverage rules. Defer until cap-limited
  workloads demonstrate its necessity; no claimed solution in the prefix rule.
- **General triple/higher-order templates:** useful in principle when every pair
  is hot but their full intersection is rare; real extraction/storage/update
  costs and a fresh profile are required. No current supported workload selects
  that mechanism ahead of using already stored pairs.
- **Adaptive ExportID shards:** bounds storage units, not semantic fanout; see
  SHARDED-DISCOVERY-DECISION. Do not repeat that argument or implement all-shard
  traversal as a recall solution.
- **Remote selective placement and retention:** remain central future work, but
  add admission/ownership/repair lifecycles. Exact-body custody was the earlier
  concrete missing capability. This tiny planner has a proved local consequence
  before undertaking a speculative remote-write protocol.

The recommendation is narrow by design, not a reduced v5 acceptance bar. It
improves one central supported discovery class while growth's full-cost margin,
general succinct frontiers, sustained custody, public isolation and independent
deployment obligations remain open under their actual evidence.
