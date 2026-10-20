# Discovery-to-method-reuse: materialize selective formal conjunctions

2026-10-20, `core_search`. Source/theory only; canonical guard PASS. No code,
tests, imports, proof production, installation or Git mutation. Current basis:
installed release `c249d086`, 108-SDK map `a0d5fad8`; the 109-SDK withdrawal
successor changes no discovery algorithm. This is a recommendation, not adoption.

## Decision and present capability

Select **an opt-in profile of at most eight explicit atomic pairs** materialized
as ordinary authenticated postings. Reuse the store/planner; do not implement
another planner or repeat a passing publish/use campaign. Root selects later
implementation. Exact-type representatives do not fix distinct-type hot lists.

`module_export_adapter` already extracts authenticated formal export features;
`discovery_query.plan_partitions` chooses the rarest requested feature in each
of256 partitions. `candidate_query` uses indexed secondary membership probes,
survivor-only record/proof work; `search_session` bounds total work and exact-ID
duplicates. Positive pages do not prove omissions; full pages prove intervals.

Real method M (`bbf0845d...bb03fc0c5`) is accepted/custodied, not yet published/
discovered/reused. Existing `workspace.publish(packet,export_names,
retention_policy=...)` accepts its native packet without a new I certificate.
Query known Tree/leaf/node symbols, theorem kind and Eq result head: M matches
without its ID/name/type being known. Applicability still needs its four laws.

## Current cost theorem and obstruction

For selected snapshots j, partitions p, and k<=8 requested atomic predicates F,
write P(j,p,f) for the committed posting and
`A = sum(j,p) min(f in F) |P(j,p,f)|`.
With sufficient grants and a correctly built reachable index, full traversal
uses A positions, <=(k-1)A secondary probes and survivor-only record/proof work.
Point probes add logarithmic local-table factors; paths add local tree-height
factors. This bounds work, not relevance/service time/corpus coverage. Budget
exhaustion or incomplete candidate replies do not establish absence or recall.

Small intersections do not bound A. In each occupied partition take two lists
of n+1 distinct-type exports sharing exactly one target. Existing work is n+1
positions there, despite one survivor. Appending nonmatching exports to both
lists makes work grow without adding an applicable result. Fixed 256 partitions
do not remove this term; exact-type quotienting does not remove distinct types.
Arbitrary generalized-method discovery also cannot use an unknown exact type
hash as its universal selector. No finite feature scheme solves all mathematics.

## Bounded representation, exact source integration and improvement

Profile = canonical sorted/deduplicated list of t<=8 pairs of distinct atomic
SPECS, no nested pairs; never enumerate all subsets. First application pairs
`type-symbol(Tree.leaf)` with `type-symbol(Tree.node)` on known base `2b54d3be`;
the other three query predicates remain. This is configuration, not hardcoded
Tree logic. Extend the existing adapter in a fresh overlay: select the namespace
before unchanged atomic extraction, then emit c(a,b) iff both atoms occur.
Namespace binds canonical profile and distinct new feature schema; never place
namespace-dependent IDs inside that profile. Resolver recomputes all features.

Minimum integration: adapter.compile_query(specs), F.EXPORT_PAIR_SCHEMA and
explicit whitelist entries in `discovery_store` and
`authenticated_index`; fresh successor of current `interface_views/workspace_evidence`
stores the immutable profile in a new config schema and selects the adapter in
`Workspace.open`. Its existing publication path already calls that adapter/store.
Profile-aware forwarding replaces free `compile_query` calls in both
`workspace_atomic.find` and `direct_contacts.bind`; exact maps select successors.
No predecessor atomic/mixed openers, isolated sidecar or checker changes. Legacy
config/namespace remains byte-compatible; no new helper-origin dependency.

Keep existing128-feature/16KiB record caps: if added pairs overflow, explicitly
refuse this profile's admission, never truncate atomic features. Old profile
remains available. Profile changes require a fresh index/namespace, not mutation
of old snapshots. Store transactions already commit every extracted posting.
Thus posting iff pair is a source/build invariant, not proved by membership
alone; full page coverage is still only within a correctly built committed index.

Compiler: replace only the first canonical configured pair contained in F;
retain ALL other atoms, including endpoints of overlapping pairs. Expanded union
is exactly F and output has |F|-1<=7 terms. No eligible pair: unchanged atomics.
Keep legacy free compiler atomic-only; derive pair IDs internally, not by
accepting arbitrary remote pair plans. Let T be output singleton/pair terms:
`B = sum(j,p) min(S in T) |intersection(f in S) P(j,p,f)| <= A`.
In the example B is one/occupied partition. Canonical choice is not cost-optimal;
correlated pairs may not help. Ingest adds <=t postings,2t membership probes and
bounded pair hashing/export, besides existing authentication costs.
Unsupported pair means ordinary atomic search in that profile, with no promised
speedup. Unsupported provider namespace returns mismatch, not absence; existing
one-query/client policy requires a separately charged owner-selected fallback
operation, not a hidden retry or arbitrary remotely supplied profile.

## Full-cost decision and limits

For m searches over horizon H, select this profile only if weighted measured or
bounded search savings `sum(c_old,i-c_pair,i) > C_build + U*C_update + H*C_hold`
(U updates; hold includes replication/repair/storage; searches include failures).
Equivalently positive mean saving d needs `m*d` above these fixed/ongoing costs.
The inequality is not established for actual M by current evidence. A useful
query further needs a reachable correctly built snapshot containing an applicable
M and B plus reply/service work within its budgets. A capped query alone gives
neither relevance nor recall. Same-type representatives/declared-type hashes
cannot fix the distinct-type example; richer semantic patterns remain separate.

Give an equally optimized ordinary-sharing comparator the same improved index.
This lowers search q/service load for both, not certification's uncached-ancestry
margin. See `GROWTH-OPERATING-REGION.md` for the sustainable-demand interval.
Cheap native M reuse stays selected; its154-stage proof graph stays DEFER.
Only changed-boundary inert checks are later useful: overlap equivalence, hot
distinct-type lists, old-cut bounds, malformed extraction, legacy and cap refusals.
Another full proof or M publication campaign cannot settle this obstruction.
