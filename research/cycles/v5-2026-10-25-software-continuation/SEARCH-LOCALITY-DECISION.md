# Ordinary search locality: routing is necessary but not the selectivity remedy

2026-10-25. `search_locality_argument`; bounded source/theory challenge for root.
Read the canonical guard, AGENTS, current GOAL and this cycle's PLAN. No runtime,
experiment, network, product edit, Git mutation or paper-study duplication.
Only this checkpoint is new. Full v5 remains unfinished.

## Decision

**For a huge network, the principal unresolved query-work issue in the selected
ordinary package is within-provider selectivity, not merely endpoint routing.**
Routing is nevertheless a distinct missing public operation: current `peer find`
accepts at most 64 explicit endpoints and cannot discover an unknown provider.
A bounded route bridge is justified as an operability repair if it reuses the
existing location workflow. It is not sufficient evidence of scalable useful
discovery, and should not trigger a new DHT campaign or broad network rewrite.

The smaller high-payoff selectivity remedy already exists in principle in this
repository: explicitly configured materialized feature pairs. It was developed
for the earlier module-export lane, but **is not in the adopted ordinary package**.
Port only that metadata mechanism if root selects a real two-feature investigator
query as its demand. No new proof technology or semantic search engine is needed.
Do not automatically port every older type-pattern/fingerprint mechanism.

This is not an argument to implement all gaps now. Source reasoning proves the
hot-list failure without a large corpus experiment. It also prevents a successful
route-to-provider demonstration from becoming an accidental substitute for
the actual large-network requirement.

**Prioritized next decision after resumption:** close the bounded ordinary
route-to-supported-endpoint seam first if the parallel audit finds a reusable
binding. That is an observed missing user operation; materialized-pair investment
is conditional on an actual investigator query, not merely the existence of the
favorable family below. Keep the selectivity counterexample as a separate release
obligation. On root's later pause instruction this source-only task is complete;
no implementation or further review is started.

## Exact selected source and observations

Package: `experiments/v5-local-checks/fair-investigator-assembly01/assembled/package`.
PROFILE SHA-256: `ea7a958db31ac070aa59be1c1e3c50d4b195cfd982c63658bd80de15ef3c6d01`.
Paths in the following list are relative to that package.

- `peer_api.py:102-120,180-205`: endpoints/providers are explicit configuration,
  maximum 64; `FairSearch` receives no route lookup or referral authority.
- `support/discovery/ordinary_export_adapter.py`: ordinary query specs are kind,
  exact portable type-symbol, result/binder head and exact declared-type key.
  `compile_query` hashes 1–8 atomic conjuncts. `namespace_for` binds ordinary
  semantics, feature revision and exact-type profile. It has no pair profile,
  pattern matcher, pair-planning call or learned semantic ranking.
- `support/discovery/discovery_query.py:70-76`: for each of 256 partitions choose
  the minimum-count queried feature, tie-breaking by key; emit numerical
  partition order. Hash partitioning does not make individual features selective.
- `support/discovery/candidate_query.py:129-227`: drive exact ordinal postings;
  probe other feature memberships with indexed SQL; load records and construct
  proofs only for surviving candidates. This is a genuine useful optimization,
  not a full-table scan. It still visits the chosen anchor's rejected IDs.
- `support/discovery/discovery_store.py:210-262`: append each admitted record
  to every emitted feature posting, one content-ID-prefix partition; commits
  are immutable snapshots. The stored source does not materialize conjunctions
  absent from the ordinary adapter's emitted features.
- `support/discovery/fair_search.py:192-228`: offer every selected provider and
  rotate providers page-by-page; within one provider, continue its current
  partition until exhausted/nonprogress before moving to the next. The existing
  fair scheduler does not rotate partitions within a provider.

The positive candidate path deliberately does not authenticate scan completeness.
Its advisory cursor and even authenticated posting counts do not prove that an
indexer included all relevant mathematics or extracted every feature honestly.
No recommendation below changes this boundary or mathematical acceptance.

## One failure scenario, with an ordinary investigator interpretation

An investigator knows two existing formal symbols A and B and asks for methods
whose declared type mentions both. The complete type/name/UnitID of a useful
method is unknown. This is a legitimate current query; exact-type lookup is not
a substitute unless the investigator already has the full desired formal type.

At a reachable, correctly built provider let one partition contain n records
with A but not B, n records with B but not A, and one useful record with both,
appended last to both postings. Other queried kind/head features, if any, are
nonselective over these records. Both atomic anchors have size n+1. The current
candidate path must examine n rejected anchor IDs before reaching the useful
one. If the aggregate scan allowance is at most n, it finds nothing, even with
perfect routing and a healthy honest provider. This is an inventory family and
source consequence, not a claim that this distribution has been observed in
today's library. Unrelated statements can populate both lists; no malicious
actor, invalid theorem or exponential proof history is needed.

Uniform hash distribution does not fix the asymptotic issue. Distribute the
same kind of independent distractors through all 256 fixed partitions: total
anchor work still grows linearly with n. More providers can spread storage and
load, but searching all of their same broad local lists preserves aggregate
work. A route key made from the query also does not create a selective local
posting unless an advertised provider has explicitly prepared that intersection.

There is a separate scheduling failure: a large first nonempty partition can
consume a provider's grant before an easy matching later partition is visited.
Rotating partitions or ordering by authenticated anchor count can reduce that
particular missed-opportunity case. Neither eliminates the n+1 anchor failure
when the relevant pair is crowded within one partition. Therefore another
fairness-only patch should not be sold as the core asymptotic remedy.

## Conditional cost statement

Let Q be a query of d <= 8 feature keys. For provider i and partition p, let
L(i,p,f) be the correctly built snapshot's posting for feature f and define

`s(i,p) = min_{f in Q} |L(i,p,f)|`,
`S(Q) = sum over selected (i,p) of s(i,p)`.

This is the driver's full selected-domain work bound, not a guarantee that a
bounded call completes. With B-tree lookup cost O(log T) for T provider posting
rows, h surviving records, record-size bound b and vector height at most log L,
the current candidate path has model cost

`O(summary + d*S(Q)*log T + h*(b + log L))`,

apart from encoding, fixed proof-map traversal and per-page overhead. Actual
wire cost need not include rejected records in positive-only mode; this is why
the older authenticated-all-rows wire lower bound must NOT be copied onto the
current candidate path. Selected request, CPU, byte and timeout limits can stop
the operation earlier; they bound resources by returning incompleteness.

Routing adds its own cost. Under maintained live routing coverage with bounded
probes per occupied identifier scale and admissible load, an existing XOR lookup
can have O(log N) expected probes for N reachable participants. This condition
does not bound S(Q), relevant-provider coverage, or source acquisition. Neither
random identifiers alone nor a finite local route table establishes the premises.

### Existing remedy, adapted rather than reinvented

For explicitly selected atoms A,B, emit an additional feature P exactly when
both occur in an ordinary record. Commit the selected pair profile to a fresh
ordinary discovery namespace and derive P canonically. Retain all atomic
features; query compilation may replace {A,B} with P, preserving other atoms.
This respects the existing eight-key wire cap and the old module-lane pattern.

For each selected provider/partition, truthful construction gives

`L(i,p,P) = L(i,p,A) intersection L(i,p,B)`.

Replacing A,B with P therefore preserves the candidate predicate, and

`s'(i,p) <= s(i,p)`.

The proof is immediate: |A intersection B| is no greater than either |A| or
|B|, and unchanged conjunct counts remain available. In the example above,
s' = 1 while s = n+1. The number of examined IDs no longer depends on unrelated
A-only or B-only growth. This is a useful conditional locality guarantee without
claiming semantic completeness, universal relevance or a global-size-free total
database cost. B-tree/key traversal and storage still grow with the provider's
index, and a large genuine pair intersection remains expensive.

The ordinary namespace differs from the earlier ModuleSpec export namespace.
Do not import that adapter wholesale or relabel old snapshots. Its symbols,
opening format and acceptance boundary are different. Reuse the pair derivation
and predicate-preservation argument while using the current ordinary adapter's
own bounded preview extraction and exact portable symbols.

### Costs and adoption conditions

- Up to k explicitly configured pairs add at most k postings per admitted
  record, with k <= 8 as the already documented old-lane bound. Existing
  128-feature/record/storage/work caps must continue to refuse overflow.
- Pair derivation costs bounded membership checks after atomic extraction.
  Persistent hash/index updates, storage, replication and a one-time fresh
  index build remain real. No powerset enumeration or hidden migration.
- New-profile providers/clients must agree on the exact profile/namespace.
  Ordinary metadata remains untrusted until structural resolution; mathematical
  validity still requires its unchanged separate acceptance path.
- Materialization is economically justified only if expected saved query work
  exceeds build, update, storage and service costs for that profile. No such
  demand frequency has been measured here. A small optional profile makes an
  investigator-selected tradeoff possible; it does not prove whole-network gain.
- Selective pairs are not a semantic expressivity solution. Theory transport,
  variable instantiation, equivalent formulations and useful-but-unmentioned
  concepts can remain undiscovered. The source audit gives no reason to block
  the narrower remedy until arbitrary mathematical equivalence is solved.

## Smallest decision-changing falsifiers, not a campaign

Before a route integration is adopted, require it to return an actual supported
ordinary HTTP endpoint from a bounded existing location result without accepting
peer-selected CA files, server trust, local paths or extra resource allowances.
If the old location protocol cannot supply that binding, an inert JSON handoff
alone has not implemented unknown-provider discovery. Root's parallel routing
audit owns that question; this task does not duplicate its implementation.

If an ordinary paired-feature successor is selected, the smallest decisive
controls are two disjoint boundaries:

1. Actual ordinary adapter: three bounded inert previews with A-only, B-only and
   both A,B; establish exactly which one emits P and that the profile changes
   namespace without changing ordinary mathematical IDs. These are metadata
   controls, not newly verified mathematics.
2. Existing Store/candidate code with clearly labeled synthetic records: two
   A-only, two B-only and one AB record in one partition, AB appended last.
   A scan grant of two cannot reach AB under the atomic profile; the pair driver
   reaches the same record in one scan. Include a disagreement/tampered-pair
   resolution refusal. No thousands-of-record fixture or native build is needed.

Failure of exact intersection extraction, namespace isolation, current ordinary
resolution or preserved aggregate allowances rejects the successor. Passing
these controls would establish only this changed boundary. It would not show
global scale, frequent real query demand, useful growth or complete v5.

## Reused theory and no duplicated growth study

Read existing `research/cycles/v5-2026-10-07/DISCOVERY-CONTRACT.md` for the
truthful-build premise, minimum-anchor and fixed-partition limits;
`research/cycles/v4-2026-10-06-resumed/SCALING-CONTRACT.md` for conditional routing;
`software/v5/conjunction_index/CONJUNCTION-INDEX.md` and actual
`software/v5/pair_planning/discovery/module_export_adapter.py` for the existing
materialization/profile implementation; and
`research/cycles/v5-2026-10-20/PAIR-PLANNING-COST-COROLLARY.md` for the crucial
distinction between complete-coverage and positive-only cost claims.

No new causal growth model, literature search or mathematical novelty experiment
was performed. No execution is selected by this checkpoint. Root decides the
next marginal-payoff action against the parallel routing finding and actual
investigator behavior, rather than treating this as automatic engineering work.
