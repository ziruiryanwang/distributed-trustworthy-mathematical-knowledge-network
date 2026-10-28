# Point-query decision: resolve once, reuse exact search inputs

2026-10-28, query_scaling. Source-only decision; no code, runtime, planner run,
state/database access, imports or Git operation. **Use existing saved-query/spec
reuse first; select no new name index or catalog schema change now.** A real
remaining cost exists for repeatedly resolving previously unresolved names at
ever-growing local roots, but it is not a whole-network scan and has no safe
constant-cost implementation through the present schema and validation contract.

This reuses QUERY-PAYOFF-AUDIT, ordinary_symbol_query/SCALING-AUDIT, adopted
ordinary_advisory_query and GROWTH-LIFETIME-DECISION. The proof-snapshot read fix is
already complete and is not reopened. Current reply-capacity source-map pins match
the inspected advisory helper (`58e20183a71a58877a34e8c8ebd9fb384afe188bfced43d4e1b9c9eb1b66a47c`),
query (`8a5cbfeb6800ab53b84f34875872e8276797db60a762e297d5b9804f1c0be0d0`)
and catalog (`aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e`).

## A. Selected-context reconstruction remains

`advisory_context.py:133-148` opens its private reader, calls full `context(root)`,
then projects one through eight names. `portable_catalog.py:530-549` walks every
selected ancestor through the root primary key. It parses every complete record;
`:390-528` validates every binding, parent/module chain and relevant imported
source correspondence, checks duplicates/shadowing, builds the full name map and
module plan. Snapshot bytes are not opened by this advisory reader.

Let D be selected depth, M its metadata bytes, N its exact-name count, R all
catalog roots, and T all catalog operations. Ignoring fixed profile/setup costs,
this path performs O(M+N+D log R+D log T) work and retains O(M+N+D) data, plus
import audit/correspondence work. The root records contain binding *deltas*, so
this is one full selected union per query, not one full union per ancestor.
An imported catalog additionally validates its activation's selected imported
root during open (`:239-240`), even when the requested root is earlier. This can
repeat overlapping metadata work and limits the benefit of choosing an earlier
root inside that imported catalog.

The schema (`:216-223`) has `roots(id PRIMARY KEY,parent,record BLOB)`, not indexed
name rows. A point root lookup still returns a whole JSON record. SQL JSON filtering
does not supply a name index or avoid reading those record bodies. Stopping after
a requested hit skips present refusals for later corruption, duplicate/shadowed
bindings and invalid ancestry; absence requires the complete selected chain.
A projection-only traversal could reduce unrequested values/module-plan memory,
but current no-shadow validation still scans all names and retains a name set.
It does not remove the asymptotic cold cost. A separate source challenge confirms
these constraints.

With a fixed-sized addition followed by one fresh query at every growing root,
the sum of these selected metadata costs can be quadratic in the number of
additions. An initial large library instead pays a large cold lookup even at
small depth. Native batching reduces depth/setup but not the number of selected
names. Default catalog ceilings (4,096 roots, 1,048,576 names) bound supported
state; they do not establish cheap lookup for a genuinely large selected library.

## B. Unrelated same-store opening work is separate

Every fresh opener runs `UPDATE operations SET state='INTERRUPTED' WHERE
state='RESERVED'` (`portable_catalog.py:238`). The only operation index is its
`id` primary key; none leads with `state`. Therefore there is no existing indexed
seek for this predicate: opening can traverse O(T) operation rows even for a tiny
selected branch. This is a source access-path conclusion, not an executed query
plan. Native catalog defaults cap T at 8,192. Root lineage lookups themselves do
not scan unrelated branches; larger B-trees add lookup cost.

A SQLite index on `state` could make this recovery predicate selective and be
maintained by SQLite, without adding mathematical binding authority. It would
still be a persistent schema/storage change: O(T) initial construction, page and
state-update costs, and an explicit locked deployment/compatibility decision.
Adding it through changed catalog code changes controller support/implementation
identity. An auxiliary selected DDL step could preserve native bytes, but would
not make the change an existing-schema or free migration. It fixes B only. Do not
commission it from the larger A finding, and do not skip recovery silently.

Neither A nor B grows with an unselected worldwide corpus. Selected-provider
search separately uses existing feature-posting indexes and finite contact/page
budgets, with broad-posting worst cases already documented in QUERY-PAYOFF-AUDIT.

## Existing reuse relation and practical choice

For a valid selected chain with disjoint exact-name binding deltas Δ_i, define
`C_r = disjoint_union_i Δ_i`. The advisory result for requested keys K is
`C_r restricted to K`, together with ordered missing names. For an actually valid
descendant s, no-shadow extension gives
`C_s restricted to domain(C_r) = C_r`.
Thus a previously resolved exact SymbolID remains the same; a previous absence
can become a hit. This uses exact `name_key` and compatible semantics, not pretty
spelling or a claim of project equivalence. Native root IDs alone do not
authenticate skipped binding BLOBs or establish this descendant relation.

The existing public workflow already retains `RESULT.json`, BINDINGS and SPECS.
`find-query` can consume the saved query report or explicitly selected `specs`
(`ordinary_report_selection/prepare.py:389-435,577-610`; GUIDE investigator route).
Finding again with those exact symbols needs no new owner-context projection,
so it removes both A and B from repeated resolution. It still pays normal package
setup and selected-provider search costs. It is reuse of advisory search inputs,
not a cache asserting freshly checked current-root state or mathematical truth.

Report reuse requires the report's exact PROFILE to match the selected preparer
(`prepare.py:394`): never relabel an old report after an auxiliary package update.
Explicit direct specs are the existing alternative when deliberately selecting
the same exact IDs under compatible semantics. Their original selection remains
historical; they do not acquire current-root provenance. Missing-name results
cannot be reused as absence after growth. One through eight names form **one
conjunction**, not a batch of eight independent questions.

For a new name, use an already eligible small context containing it when that
context matches the intended interpretation. This requires no re-admission merely
to search that existing root. Constructing a new bounded context can cost actual
re-admission and is not a free remedy; imported opening has the caveat above.
Keep the established bounded-context/native-batching decision with those costs.

## Marginal-payoff disposition

For Q searches reusing U distinct resolved feature selections, existing reuse
reduces context preparations from Q to U. Re-running name resolution after every
unrelated extension is avoidable and supplies little extra search value. Adopt
this route before adding a persistent lookup structure or changing native support.
One large initial lookup is not itself evidence that a maintained index pays.

Reopen name indexing only for a useful recurring workflow that genuinely needs
many *new* name selections or fresh current-root validation on a growing library,
after pricing report/spec reuse, eligible contexts and batching. The required
relation would be an exact root-scoped projection equal to `C_r`, including
complete absence, append-only extension, import correspondence, withdrawal and
crash lifecycle. No present index establishes it; a persistent derivative would
need explicit maintenance/validation obligations even if advisory-only. No
asymptotic experiment is needed to rediscover the loops, and none is selected.
The genuine huge-local-library fresh-lookup gap remains acknowledged; this
decision does not declare the full scaling or v5 goal complete.
