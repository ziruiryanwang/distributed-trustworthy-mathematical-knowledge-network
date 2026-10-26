# Independent review: optional sparse positive search

2026-10-25. Reviewer: `ordinary_routing_gap`. Source/theory review only; no
implementation, tests, build, state mutation, Git operation or shared-ledger edit.
The canonical-root guard passed. Existing used sources and evidence are preserved.

## Disposition

**GO for a separately selected source implementation of the reviewed contract.**
There is no unresolved architectural blocker to this narrow successor. This is
not a runtime selection, implementation approval, growth result or v5 release
approval. The code must still close the concrete seams and falsifiers below.

I independently prefer the **fresh, opt-in, at-most-eight fixed pairs maintained
inside `Store.admit`** over incremental prefix-cache maintenance for the first
implementation. The reason is the smaller correctness and operating state
machine, not a belief that eager materialization always pays. Existing atomic
stores and V1 queries must remain usable unchanged. A provider should buy this
physical index only for a plausible repeated-query workload; it is not the
default investment for all worldwide contributions or a retrofit for arbitrary
huge existing stores.

The selected obstruction is real: the existing positive-only protocol requires
`next - start <= charged.scanned`. A sparse access path cannot report the late
AB hit under a small scan allowance without an explicit new protocol. The
contract correctly changes only the opt-in V2 traversal/accounting semantics,
not mathematical identities or the proof obligation on positive records.

## Reviewed identities and scope

Completely read:

- `SPARSE-ACCESS-CONTRACT.md`, SHA-256
  `e31815e98ee1adab0505922656ecfb051bb223f49c19a18963af70517a81230b`.
- `NEXT-PAYOFF-REVIEW.md`, SHA-256
  `119a1dceca87a2bf4b8438c7aaa11a6515cec8efbbeb359d00f49b5d7faae23e`.

Source basis is
`experiments/v5-local-checks/contact-federation-assembly01/assembled/package`,
whose PROFILE SHA-256 is
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`.
I independently recalculated PROFILE and the hashes of `candidate_query.py`,
`discovery_store.py`, `search_session.py`, `fair_search.py`, `http_provider.py`
and `peer_api.py` in that selected package. Reviewed the
candidate protocol, Store admission/snapshot/schema, SearchSession accounting,
FairSearch dispatch/settlement, provider route/reservation sites and ordinary
API/CLI configuration sites. No saved campaign was rerun.

## Independent comparison of maintenance choices

| Question | Fresh fixed pairs, transactional maintenance | Bounded incremental prefix maintenance |
|---|---|---|
| Authoritative state | One committed Store sequence and equal cache watermark | A base Store cut plus per-pair covered prefix, readiness and catch-up state |
| Update cost | Every new admission tests at most eight pairs and adds at most sixteen oriented rows | A separately funded maintenance operation pays when selected; ingest need not maintain the pair immediately |
| Existing corpus | Requires a deliberately populated fresh index; no free conversion | Can scan a chosen atomic ordinal prefix incrementally, avoiding a whole-store rewrite |
| Failure semantics | One transaction commits base and cache or neither | Partial progress can be valid; exact prefix coupling and incomplete-query fallback must be specified |
| Capacity consequence | Pair quota can refuse new metadata admission to that selected Store | Lag/quota can make pair access unavailable while base admission continues |
| Added public operation | Optional immutable creation/reopen configuration only | Maintenance selection, limits, progress and readiness reporting |

Both are viable. Prefix maintenance is attractive once actual deployments need
to add access paths to existing large corpora or decouple ingestion from cache
capacity. It is not intrinsically unsafe or disproved. However, the current
source has no `admitted_seq` index: a naive catch-up query over all objects is
not a bounded-locality design. A future prefix builder should drive an existing
atomic posting order and commit its exact covered prefix with each row batch.

The fresh option removes that entire partial-readiness lifecycle now. We have
no selected deployed migration obligation justifying its extra complexity. Its
cost is explicit: rebuilding N old objects requires N paid admissions, and a
full pair quota can block indexing on this particular Store. That tradeoff is
acceptable only because the feature is optional and the atomic profile remains.
Do not later present this choice as solving adaptive indexing at global scale.

## Correctness argument and boundaries

### Transactional cache invariant

For each fixed pair {a,b} and partition p, the committed oriented rows must be
exactly the matching admitted objects, carrying their immutable atomic ordinals
and admission sequence; the reverse orientation must carry the same relation.
`completed_seq == Store.meta.seq` holds initially and after every commit.

The proposed induction is valid under the existing SQLite durability and
serialized-owner model: the empty store satisfies it; a duplicate is a no-op;
a new immutable record inserts its original postings and precisely its matching
pairs in one transaction; rollback leaves the prior prefix intact. Cache tables
and metadata must be initialized with the enabled Store's initial state, not
silently created by a later opener. Exact immutable configuration equality is
required on reopen. A namespace and sequence number alone would not bind a
separate copied cache to this particular history; keeping it in the same DB
avoids that additional protocol.

Constant-size watermark checks detect specified readiness/configuration
failures, **not arbitrary deletion of an unvisited row**. There is no remote
proof of complete intersection maintenance. This limitation is acceptable for
positive-only discovery: sound hits remain independently checked, while honest
search-efficiency and local exhaustion rely on the maintained invariant.

### Old-cut safety and locality

For an old snapshot with anchor count c, the SQL seek must use the leading
`(anchor, companion, partition)` key and `start <= anchor_ordinal < c` directly.
Filtering later rows by `admitted_seq` only after retrieving them would not
provide the claimed old-cut locality. Under append-only admission, a later
matching object cannot have an anchor ordinal below c. Checking the old
companion count, admission cut and exact object/posting binding supplies the
remaining defenses; inconsistent cached rows fail rather than become ordinary
negative matches. No OFFSET, temporary sort, third-feature reanchoring or
unbounded catch-up belongs in this path.

### Positive soundness and honest incompleteness

Every accepted V2 hit must retain canonical record validation, the whole
requested conjunction, partition binding and the original atomic-vector proof
at its actual ordinal. It therefore has the same committed-metadata positive
soundness as V1. This is not mathematical acceptance, honest feature extraction
or complete search of the provider or network.

The new cursor is an original atomic position, not a number of examined atomic
rows. Removing the V1 delta bound is warranted only in explicitly bound V2.
Keep strict monotonic hit order/ranges, all charge ceilings and
`hits <= proofs <= record_loads <= scanned`. Charge a driver attempt before its
seek, including a completed empty seek. An interrupted seek cannot advance to
the anchor boundary; an unreported byte-limited candidate must remain eligible
for a later request. Sparse termination never adds a `Coverage` interval.

Disabled/no-eligible-pair atomic fallback may share the V2 request and **same**
I/O meter, original deadline and response cap. Calling V1 `page` afresh would
renew these allowances and is not an acceptable implementation. Corrupt enabled
state is an integrity error, not a reason to silently fall back or claim empty.

## Concrete integration obligations before source approval

The contract correctly identifies a multi-file boundary. These are necessary,
not optional polish:

- Keep ticket operation `candidates`. Current `_reserve`, `_take`,
  `_conservative_rows`, `accept` and FairSearch `_abandon` special-case this
  exact operation. A new operation label would miss charging branches and can
  fall through into authenticated `Coverage` handling.
- Select V1/V2 verifier from the held request schema, never the response schema.
  Success, malformed/proof-invalid reply, deadline and abandonment all retain
  the full reserved `scanned` allowance. Provider reports cannot refund it.
- Freeze FairSearch's candidate mode; update its route dispatch and the exact
  `support/transport/fair_exchange.py` read-only route allowlist. Preserve original absolute deadlines,
  provider rounds and conservative cleanup. Unknown legacy routes produce
  bounded charged incompleteness, not automatic V1 retry or new grant.
- Expose optional mode through both `peer_api.find` and the nested
  `directory_find.search`. Their current exact-field validators reject extra
  fields. Directory hints must not choose or alter the mode.
- Forward exact optional pair configuration through `_index`, `serve` and the
  separate `peer.py` publish/serve index validator. Defaults remain unchanged;
  serve never creates or migrates the store.
- Extend provider closed route tables, request validation, response reservation
  and effective timeout dispatch together. The existing offer schema remains
  unchanged; readiness is not a new authenticated offer claim.
- Charge both orientations' canonical row bytes to the pair allowance and once
  to total logical storage, with combined physical allocation still capped by
  `max_db_pages`. Include attempted pair work even when the transaction rolls
  back; durable counters and already spent CPU are different quantities.
- Preserve publication partial-success semantics. Custody may already contain
  the preview before `index.admit` refuses, and earlier targets may have
  succeeded. Only the failing metadata transaction rolls back, not accepted
  mathematics, prior custody or the whole multi-target call.
- Include all new/changed payloads in package/profile selection. Ordinary
  record features, namespaces, Merkle roots and the common admitted prefix's
  snapshot IDs must not depend on the physical pair configuration.

These seams are visible in the actual source; they are why a SQL-only patch is
insufficient. They do not require a new research planner, global cache policy,
certificate campaign or native mathematical stage.

## Conditional payoff and minimum falsifiers

Let a be the selected atomic anchor count and r its intersection with the chosen
companion at the pinned snapshot. A ready ordered access path has r candidate
rows rather than a; a successful full traversal needs at most r rows and one
empty terminal seek, apart from interruption/repeated-page overhead. Indexed
navigation, remaining feature probes, proofs and bytes are still paid. For the
n A-only / n B-only / one late AB family, r=1 and a=n+1. This is a genuine
algorithmic removal of a finite-grant obstruction, not a claim of constant-time
search or net mathematical growth.

A useful deployment region requires repeated query savings to exceed initial
population, per-admission maintenance, storage, service and failed-query costs
in an explicit resource measure. Fixed eight pairs cannot accelerate arbitrary
new queries. A frequent pair may have r=a and provide no selectivity saving;
a rarely requested pair may never repay construction. The source-derived
investigator use case justifies trying this optional feature, not asserting a
measured workload distribution or default rollout.

After source review, the proposed tiny inert discriminator is sufficient:
two A-only, two B-only and late AB in one partition; V1 under two scan units
misses, while V2 under one driver unit returns the same committed AB at its
original ordinal. Changed-boundary controls must also cover both orientations,
ordinary default behavior/common-prefix identities, old snapshot after append,
extra conjunct rejection, missing/inconsistent enabled state, quota and
interruption rollback, valid atomic fallback, byte-limited nonadvance,
schema/cursor/proof tampering, aggregate settlement and public mode/configuration
forwarding including a legacy unsupported route.

Do not inflate this into a giant-corpus or native-proof run. Do not repeat prior
contact/mathematics campaigns. If implementation requires implicit rebuilds,
renewed grants, silent partial caches, weaker positive verification or changed
discovery identities, stop and reconsider the design rather than redefining a
pass. After the finite seam is implemented and checked, reassess the next
highest-payoff obstacle; this cache must not become an open-ended subsystem.
