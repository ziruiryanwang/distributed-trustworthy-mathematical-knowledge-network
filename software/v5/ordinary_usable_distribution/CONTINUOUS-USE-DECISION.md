# Continuous use: use bounded operating cycles before adding a host updater

2026-10-28. Independent source-only audit by release_direction. No product/runtime
execution, new test, owner access, Git or external deployment. The current kit is
not repeated or repackaged by this note.

## Decision

**Current APIs can support sustained ordinary investigation and repeated sharing
through explicit update/serve cycles. Do not implement a daemon or stopped-host
append operation yet.** Use the mathematical owner's already incremental
contribute/intake -> publish -> finite serve path for evolving collections. Use
the dedicated inert host for stable selected libraries or bounded publication
generations. These roles have different lifecycle costs.

The highest-payoff immediate step is to make this repeated operating contract
explicit in the product's operating plan, preserving actual owner serialization,
finite allowances and observable freshness. This source audit resolves its main
safety/cost argument; it does not justify another repeated theorem experiment.
If a concrete independent custodian later needs frequent low-cost delta ingestion
without mathematical checking, a stopped-host update is a real candidate. It is
not required merely because finite service calls exist.

This conclusion is narrower than saying the final system already has a general
continuously growing inert hosting service. It does not: the dedicated host has
no append, refresh, removal or repair operation, and indexes at most64 chosen
targets per generation. Do not market that role as an unbounded live aggregator.

## What the actual implementation permits

| Route | Existing behavior | Sustained-use consequence |
|---|---|---|
| Ordinary investigator | Retained owner accepts a new contribution/intake against a selected checked parent; later reports select the resulting root. | Investigations can continue repeatedly; no fresh owner per result is required. |
| Ordinary publication | `peer_api.publish` checks selected local target bindings, reads those units and appends previews to an existing index when create=false. Duplicate identical records return new=false. | No complete corpus re-publication is required for each new result. |
| Ordinary service | `peer.py` holds the same OrdinaryAdmission owner lock throughout service and cleanup. | Updates and service on that owner are serialized. Local research outside its protected inputs can continue, but admission/publication waits for a service gap. |
| Dedicated preparation | Fresh root; every selected manifest unit is read, validated, copied and read back; selected target previews are indexed; a final seal commits the generation. | New complete generations cost work proportional at least to their included bytes, not just their new contribution. |
| Dedicated service | Holds its own host lock, opens the sealed stores and serves one finite lease. | An investigator's separate owner is not locked. The same existing generation may be served repeatedly under fresh explicit allowances and outputs. |

Fresh output/diagnostic directories are required for each operation. This does not
require fresh owner/catalog/custody or index directories. Reusing those retained
stores through their public existing-open paths is supported. Never confuse a
fresh operation leaf with resetting mathematical knowledge.

## Minimal repeated cycle using the current public API

Choose a retained owner, index, stable contact endpoint and explicit finite phase
budgets. Each cycle is:

1. Finish and inspect the prior serve's actual cleanup. Do not rely only on elapsed
   lease time, a saved READY file or apparent process disappearance.
2. Contribute or intake the selected new work using the retained owner and actual
   latest selected parent. Obtain a complete successful report. Ordinary local
   source investigation need not be inside this service schedule; frozen selected
   source inputs must still remain stable while the product reads them.
3. Publish the chosen accepted targets to the same index with `create:false` and
   its actual original limits. Retain each successful target publication if a
   later target fails; the public batch is not one atomic publication transaction.
4. Start the next finite serve using that existing index and custody. Reuse the
   deliberate endpoint/TLS selection if appropriate; record this invocation's
   actual readiness and finite deadline. Clients issue new searches or use the
   exact retained snapshot/objects that remain available, under their own budgets.

The existing operator companion prepares these calls; no new internal API or
private database edit is needed. Repeated prior-profile selections remain scoped
to their existing explicit extraction policy. A new allowance is an operator's
new operation, not renewal hidden inside the preceding operation.

Serial owner access prevents the supported publisher from mutating stores while
its provider reads them. The provider drains/closes before the owner lock is
released. Existing per-object identity checks and client admission remain active.
This proof relies on protected local storage and cooperating supported commands;
it does not cover arbitrary concurrent same-account mutation.

If uninterrupted public service is required, independent custodians can use
overlapping schedules or stable dedicated copies. That needs actual retention,
capacity and scheduling arrangements. A local role decomposition or two processes
on one computer is not independent availability evidence.

## Startup cost is not a hidden full-corpus scan in the dedicated route

I traced the entire dedicated serve path, not just its advertised interface:

- `custodian._read_seal` validates the bounded seal and at most64 target rows.
- `custodian.serve` opens custody, compares its stored object/export/logical-byte
  counters with the seal, opens the index, compares stored latest-snapshot and
  object count, closes that preflight handle, then invokes the existing provider.
- `OrdinaryStore.__init__` checks configuration, file/page bounds, sidecars and
  metadata counters. `status` is one selected metadata row. It does not enumerate
  or reparse every retained evidence object.
- Discovery `Store.__init__` checks configuration, quotas and metadata. The
  dedicated route has no pair-access index configured. It does not enumerate all
  records/postings on normal open.
- Exact-object responses verify the selected bytes and identity; they do not
  replay all stored proof dependencies. Ordinary client parsing/checking remains
  separate. The provider obtains an index snapshot for its selected offer.

There is still fixed package/runtime verification, SQLite opening, possible journal
recovery and OS I/O. Let K be selected software/bootstrap work, R_i the actual
database recovery/open work for cycle i, t<=64 its sealed target count, and X_i
its served/requested data and index work. A defensible form is

    T_serve(i) = K + O(t) + T_metadata(i) + R_i + X_i + T_cleanup(i).

This is not a hard constant wall-time bound: storage access, file size metadata,
recovery and loaded system conditions remain relevant. There is no mandatory
normal-path term that parses every retained unit's DAG at every restart.
An append feature would therefore remove full *generation preparation* repetition,
not an imaginary full-corpus recheck at every existing service restart.

## Costs and availability of the existing evolving-owner route

Let A_i be actual admission/contribution cost, P_i publication cost, S_i start/close
cost and L_i the selected serving duration. Total resource consumption is the sum
of the actual bounded phase costs, including failures; it is not reduced to L_i.
Publication includes the chosen context's reconstruction/loading cost, selected
unit bytes and index updates:

    P_i = T_context(m_i) + T_selected_units(i) + T_index_updates(i) + T_local_overhead(i).

Do not claim T_context is constant: publish calls `owner.catalog.context(root)`,
and the context/history metadata can matter. Existing deliberate batching and
smaller compatible selected contexts remain the first controls. There is no
newly established global-size-independent cost theorem for that whole owner path.

Under a failure-free periodic schedule with bounded update time U, startup/cleanup
time S and serving time L, local service duty is L/(L+U+S). Work arriving just
after an update can wait roughly one cycle before exposure. These expressions
state the tradeoff, not measured availability: failures, burst arrivals and
unbounded investigation time invalidate fixed-latency conclusions. Research need
not finish every cycle; the update batch can include only completed selected work.

This is reasonable when update cadence is modest compared with service intervals
and a checked contributor already maintains the owner. It avoids both a new
concurrency model and unnecessary duplicate custody. It is not an architecture
for an inert high-rate aggregator that must accept every arriving unit immediately.

## The real limitation of immutable generation turnover

If an inert curator repeatedly recreates a complete retained corpus after each
equal-size new delta b, the minimum cumulative bytes ingested over n generations
are b*n*(n+1)/2, apart from an initial base. Fresh host preparation actually loops
over those bytes and readbacks, so that cost is real for that chosen policy.
This is not a lower bound on the existing software as a whole: incremental owner
publication already avoids it, and a curator can batch changes or expose selected
bounded stable collections rather than rebuilding all history every time.

Delta-only fresh hosts avoid recopied base bytes but create more retained roots,
ports/processes or scheduling/contact obligations. Bounded per-query providers and
incomplete coverage do not magically make those costs disappear. A rolling window
of retained objects is a different retention promise, not permanent accumulation.
Finite custody/index/snapshot quotas eventually refuse further growth; no finite
node provides infinite preservation. Sharding, retention and future repair remain
explicit operating requirements whichever update API is used.

## Why stopped-host append is deferred, and what would make it worthwhile

Its useful workload is a dedicated custodian repeatedly receiving bounded deltas
while preserving its previous collection and endpoint, without maintaining a
mathematical owner. This avoids full generation copies and needless kernel work
by an untrusted index/custody role. Existing idempotent custody insertion and
incremental index admission are the right primitives; a daemon, new TLS protocol,
continuous writer/reader concurrency or certificate engine is not necessary.

But a safe public update is not just exposing those two insertion calls:

- The current host seal fixes exact custody counts and index latest/object count.
  Any partial committed append makes ordinary serving under that old seal refuse.
- Custody and index are separate SQLite databases; individual transactions and
  readbacks do not make the whole multi-object update atomic across them.
- A failure after custody insertion but before indexing/sealing must preserve
  which bytes were disclosed, which targets were indexed and what can be served.
  A still-present old HOST.json is not a rollback or readiness warrant.
- A prospective update needs an explicit persistent intent/progress design, exact
  old-head selection, fixed delta/capacity bounds, idempotent resumable steps, new
  head publication rules and a policy for interrupted/unfinishable updates.
  Service must not silently expose partial undisclosed content. Recovery cannot
  relabel old seals, remove the lock, increase the old grant or pretend a batch
  succeeded. A new bounded recovery selection is distinct from automatic retry.
- Copying the entire old databases to make each update atomic would reintroduce
  the very corpus-size cost that motivates the feature. Concurrent refresh is
  a larger problem and is not the minimal option.

No current investigator trace establishes a need for this extra state machine.
The ordinary maintained-owner path has the necessary update primitives already.
Therefore do not select append implementation now. Reconsider when the role's
actual delta cadence/retained corpus cost or a required availability policy beats
the existing batched-owner/stable-host alternatives, and resolve interruption
semantics before any experiment. The present asymptotic observation identifies a
future boundary; it is not permission to assume its workload and invest blindly.

## Source and software updates are separate from content updates

New mathematical work yields new selected immutable identities and compatible
context continuations. It does not require rebuilding the software distribution.
The current source recipe directly supplies software builds; changed native
identities are not automatic owner migrations. Auxiliary package changes can use
the scoped prior-report selector where applicable, but dedicated seals remain
PROFILE-bound. Keep their approved original package or prepare an explicitly
selected successor generation. No hidden rebind or universal upgrade operation
exists. This distinction prevents ordinary mathematical growth from triggering
unnecessary package churn.

## Source anchors

- Current selection: `ordinary_reply_capacity/source-map.json`.
- Owner service serialization: `ordinary_sparse_access/peer.py:223-226,249-253,274-283`.
- Incremental publish and finite service: `ordinary_multi_source/peer_api.py:827-889,893-1009`.
- Fresh generation ingestion/seal: `ordinary_dedicated_host/custodian.py:167-278`.
- Seal checks and metadata-only service preflight: same file `284-374`.
- Custody open/status/idempotent put/selected get: `ordinary_multi_source/ordinary_acquisition.py:79-297`.
- Incremental index/open: `ordinary_sparse_access/discovery_store.py:57-159,221-274`.
- Bundle finite ceilings: `ordinary_binding_reuse/baseline_bundle.py:40-79`.
- Exact HTTP offer snapshot: `ordinary_reply_capacity/http_provider.py:456`.

These source conclusions do not replace actual execution evidence or establish
worldwide reliability, measured throughput, independent operators or final v5.
