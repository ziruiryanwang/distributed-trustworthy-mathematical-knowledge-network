# Hosting payoff: grow one independent custodian without promising atomic batches

2026-10-28, query_scaling. Independent source/theory challenge. No product code,
runtime, imports, owner/database access, native work, sockets or Git operations.
Root owns selection. Current source map is `80d46cbedad723a90a87db80c4b5ac1dd6054526911c643c425ede48ce00f713`.

## Recommendation

**Select a small stopped-host append capability for a fresh independent inert
custodian, with explicitly permitted partial publication. Prefer the stable
descriptor design raised by root over an exact-generation append/recovery
protocol, if independent ordering review confirms the conditions below.** Keep
the existing owner publication route for an investigator who already maintains
checked state, and stable shards for genuinely stable or separately routed
collections. Do not implement a producer redesign, daemon, automatic ingestion,
general migration or a new distributed transaction protocol in this step.

Absent append is a real missing capability for that independent hosting role.
It is not the central obstacle to creating concepts or repeatedly reusing them:
current owners already develop and publish incrementally. Its expected payoff
is avoiding artificial lifetime-64-target generations, duplicate retained
storage and needless mathematical-owner coupling at an untrusted custodian.
That is a concrete deployability increment, not evidence of useful discovery,
novelty, global completeness or end-to-end delta-cost publishing.

This narrows the earlier `CONTINUOUS-USE-DECISION.md` deferral. Contact refresh
has now been adopted, but finishing that feature alone would not justify the
next feature. The positive reason is that the already supported independent
custodian role otherwise has no inexpensive same-store growth operation despite
having suitable incremental custody/index primitives. The smaller partial-write
contract substantially reduces the extra mechanism needed to provide it. No
actual high-rate custodian trace or elapsed-time speedup is claimed.

## Minimum role that earns this work

A curator receives operator-selected inert bundles from several contributors,
retains earlier exact units and selected target previews, and makes them available
through one deliberately configured endpoint between bounded updates. The curator
need not have a Lean environment accepting those contributors' mathematics. An
investigator can continue developing definitions and consequences in a separate
owner while the curator serves previously contributed work. Recipients still
discover, acquire and independently check what they use.

The curator promises immutable object identities, fixed local quotas and honest
operation outcomes. It permits any validated committed subset of an approved
input batch to become visible. It does **not** promise an all-or-nothing batch,
an exact public generation independent of the index snapshot, continuous service,
complete dependencies, acceptance of every arriving contribution, or an unlimited
single-node corpus. These weaker publication semantics are explicit and useful;
they do not weaken recipient mathematical acceptance.

The supported input boundary is an existing manifest and its exact unit files,
plus exact chosen target rows. Merely owning a new theorem in a live project is
not yet such an input. The following producer costs must remain visible.

## End-to-end input cost

The current public `produce-baseline` route loads the private compiled environment,
censuses it, and exports the full selected dependency closure outside its fixed
seed. It does not stop at a remote host's warm cache. The Python adapter then
binds the writer and writes **all** resulting unit files (`baseline_production.py`
268-279). `PRODUCER.md`/source `ordinary_producer_package/README.md` 61-69 states
this restriction. Append cannot remove that upstream work.

The inert manifest format itself is less restrictive. Selected `baseline_bundle.py`
261-265 says batch validation does not check dependencies against an environment;
`make_manifest` 335-355 measures the supplied bounded units. A supplied delta can
therefore omit old dependencies. That is structural permission, not evidence
that the existing native producer efficiently materializes that delta. Missing
dependencies must be available elsewhere if a recipient needs them. Repeating
dependencies for self-contained availability is an operator policy with real
cost, not a compulsory property of every host input.

For cycle i, distinguish genuinely new stored bytes d_i from supplied bytes
b_i=d_i+u_i, where u_i are already held bytes nevertheless included in the input.
Both append and shard preparation validate the supplied b_i. Duplicate insertion
avoids new storage but still parses/hashes and compares bytes and locators. If
the native producer emits a growing closure every cycle, sum(b_i), its production
and transfer cost can still grow quadratically even when host storage grows only
by sum(d_i). Claiming O(d_i) for the full pipeline would be false.

The smallest useful first workflow therefore reuses already materialized inert
bundles, or receives explicitly bounded delta files from contributors. Its cost
ledger includes their original production and transfer once, any repeated
materialization/transfer when it actually happens, curation, host work, discovery
failures and recipient checking. A new native exporter is not required to make
the host append operation useful, but append must not be presented as fixing
that exporter's closure cost.

## Fair comparison of existing alternatives

| Route | What grows with repeated contributions | Best use and remaining cost |
| --- | --- | --- |
| A1. Rebuild a complete immutable generation | Revalidates, copies and reads back every included unit; repeats target indexing | Appropriate for a small stable release. Rebuilding the whole accumulated corpus each cycle is an expensive policy, not the only current alternative. |
| A2. Prepare only new immutable shards and refresh contacts | New-byte work can already be linear; roots, service sessions, advertisements and shard selection accumulate | Appropriate when shards have useful topic/retention boundaries or a few publishers suffice. Artificial generation splits can increase fanout and omit historical coverage under bounded routing. |
| B. Stop and append to one independent inert host | Validates all supplied bytes, stores new identities, updates affected index paths, then resumes service | Avoids lifetime target-list and endpoint multiplication without needing a mathematical owner. Still pays fixed starts, writes, duplicate checks, outages and finite capacity. |
| C. Existing retained mathematical owner, incremental publish and finite serve | Already appends selected previews to one index; additionally authenticates selected local context and serializes owner use | Best default for a checked investigator who already needs the owner. A second custodian is optional when schedules and disclosure permit this role. |

For A1, retained bytes after i updates are N_i=N_0+sum_{j<=i}d_j. A repeated
complete-copy policy pays at least sum_i N_i, including n*N_0 and a quadratic
term for equal nonzero additions. The present host actually reads, validates,
copies and reads back those bytes. That bound is **not** a lower bound for A2
or C, so it cannot by itself establish append's superiority over current software.

For A2, delta-only manifests can avoid repeated base copying. With T distinct
indexed targets and q<=64 targets per host, retaining all selected targets needs
at least ceil(T/q) current V1 generations. Each generation needs a service/root
obligation; it need not have a separately running process at all times, but
serializing generations on one endpoint trades simultaneous coverage for a
schedule that consumers must somehow discover. A same-topic collection whose
relevant shard is unknown can require contacting many shards. Useful semantic
routing can avoid that fanout; it cannot be assumed merely because a contact
directory exists.

Current contact routing permits 16 endpoints per exact route, and refreshed
slot quotas sum to that same bound. A single route could thus hold at most 1024
disjoint V1 target positions if every endpoint hosted one full 64-target shard;
this is an illustrative limit of that configuration, **not** a network-wide
capacity theorem. Multiple routes/direct contacts remain possible and cost
selection/curation. Replacing old advertised shards with new ones changes
discoverability of retained history. A per-query cap bounds work by allowing
incomplete coverage; it is not a scalable coverage mechanism.

For B, a defensible normal host-work expression is

    sum_i [K_i + V(b_i) + W(d_i) + I(a_i, p_i) + O_i + R_i + C_i].

Here K_i is software/bootstrap work, V selected validation/readback including
duplicates, W new storage, a_i<=64 newly selected targets per call, I affected
index work at current posting sizes p_i, O database opening, R actual recovery,
and C cleanup/reporting. The current index updates a 256-bit feature-map path,
an eight-bit partition path and logarithmic vector paths for each feature; it
does not enumerate every historical record. SQLite lookups, page splits, retained
authenticated nodes/snapshots and physical journal recovery still depend on
database/storage state. This is not a constant-I/O or wall-time bound.

For C, `publish(create:false)` already retains the index across calls; 64 is a
**per-call** target limit. Each target commits separately and duplicates return
`new:false`. However, `owner.catalog.context(root)` walks the selected lineage,
checks its bindings and authenticates selected artifact bytes. The artifact
cache begins empty on a fresh catalog open, so fresh owner publication may pay
cumulative selected-artifact hashing even though index writes are incremental.
This is byte authentication, not native mathematical replay. Charge it as
T_context(selected lineage/artifacts), along with original checking/contribution
cost. Do not impose that role solely to substitute for inert storage when no
checked owner is otherwise needed.

## Opens, outages and costs append does not remove

Normal dedicated-host restart does not scan the retained corpus. V1 reads its
bounded seal, opens custody and compares metadata counters, opens the index for
preflight, closes it, then opens the index again through `api.serve`. Store open
checks configuration/quotas and stored metadata; exact requested objects are
checked when served. The separate cross-check confirms even optional paired
index opening checks bounded metadata rather than all rows. SQLite journal
recovery and OS/storage work are not thereby bounded independently of bytes.

Append therefore removes repeated *preparation* or artificial shard obligations,
not a nonexistent proof replay at every service start. Batching updates is the
first control when fixed verification/open/cleanup costs dominate small deltas.
Both B and C still pause their respective provider during writes. For a regular
failure-free schedule with service time L and update/start/close time U+S, local
service duty is L/(L+U+S); this is conditional arithmetic, not an availability
claim. Independent redundant custodians may help availability and cost more.

Append does not reduce the number of relevant or misleading candidates in a hot
feature, cure missing abstractions, make failed search free, remove recipient
checking, or improve query routing across independently operated collections.
One larger host can reduce endpoint overhead yet concentrate load/failure.
Stored snapshots and old authenticated tree nodes continue growing until quota
refusal. Real capacity sharding/retention remains necessary; the improvement is
removing an artificial 64-target lifetime split, not providing infinite storage.

## Minimum implementation contract: challenge atomic generations first

The earlier `NEXT-CENTRAL-DECISION.md` proposed bounded intent/progress and explicit
recovery because V1 binds exact custody counts and the latest index snapshot in
HOST.json. That is a coherent way to preserve the V1 generation promise, but
preserving that promise in a new role is not automatically necessary.

Root's smaller alternative is preferable for the role above: a **fresh V2 stable
descriptor** pins the software/semantic namespace, original store limits and
explicit partial-disclosure policy, while the existing stores retain their own
configuration and counters. It does not pretend to pin mutable content counts
or a current index head. Existing V1 files and profile semantics stay frozen.

Under the independent ordering review, minimum requirements are:

1. The same exclusive host lock covers each append and each service; supported
   commands never overlap them. The initial stores/descriptor must be completely
   initialized before the host can be used. Fixed quotas remain enforced.
2. Each input unit is validated and committed with its locators before its preview
   is committed; a selected index record is committed only after its corresponding
   preview/evidence is durably available. Exact duplicates are idempotent and
   conflicting identities refuse. Full input disclosure includes unindexed units
   and partial writes. There is no deletion or name-shadowing update.
3. An interrupted or failed append may leave a visible subset; it never earns a
   COMPLETE report by inference. Later service opens SQLite normally, after the
   lock is available, and serves the actual retained index snapshot and objects.
   The descriptor hash is a configuration/policy selection, not a content hash.
4. An explicit later duplicate append can reconcile/retry selected immutable
   inputs within a fresh allowance; there is no automatic retry. Reports and
   service readiness must distinguish actual current snapshot from the outcome
   of a previous operation. Corruption or uncertain opening/closure still refuses
   according to the existing protected-storage/runtime premise.

If these conditions hold, the application has no cross-database all-or-nothing
promise to recover. A pending marker, immutable intent, generation receipt and
new recovery command are not justified merely to recover a promise the role does
not make. Per-object transactions and SQLite recovery are still real required
mechanisms; arbitrary power-loss durability is not proven by source ordering.
This is a recommendation about the useful contract, not a completed safety review.

If review finds that a committed index can outlive the requisite custody under
the supported interruption model, address that exact ordering/durability seam.
If a user actually needs an exact generation, use the more elaborate bounded
intent/suffix-reconciliation proposal. Do not copy full databases or scan all
historical targets at every update to obtain either contract.

## Evidence that changes the decision

No large performance experiment is needed to establish the 64-target V1 limit
or the existence of incremental primitives. The next source decision needs the
independent review of the simpler ordering/partial-publication contract. A later
finite changed-boundary check should distinguish old-object preservation, new
target visibility, exact duplicates, interruption between the three commit stages,
capacity refusal and correctly reported partial/unknown outcomes. Repeating
mathematical theorem campaigns would not resolve those questions.

Defer or narrow the feature if the actual operator only maintains a small static
mirror, already has a suitably scheduled checked owner, or expects the feature
to cure repeated producer closure export. Choose A2 when useful shard boundaries
keep query fanout and maintenance small. Prefer B when repeated independent
ingestion and same-collection retention would otherwise multiply generations or
create an otherwise unnecessary mathematical owner. Require a separate payoff
argument before adding generation transactions, remote writes or lifecycle
automation. These conditions keep the implementation subordinate to the role.

## Source anchors and cross-check

- Selected `ordinary_dedicated_host/custodian.py` 71-81, 167-278 and 284-374:
  lifetime target seal, complete supplied-bundle preparation, bounded normal open.
- `ordinary_registration_refresh/peer_api.py` 1070-1147: existing incremental
  owner publication; 1150 onward and `ordinary_sparse_access/peer.py`: service
  role and owner serialization.
- `ordinary_sparse_access/discovery_store.py` 57-159, 197-274 and selected
  `discovery/authenticated_index.py`: metadata opens, idempotence, snapshots and
  affected-path updates.
- `ordinary_multi_source/ordinary_acquisition.py` 79-297: custody metadata opens,
  atomic/idempotent selected inserts and exact getters.
- `ordinary_lean/portable_catalog.py` 171, 319-331, 407-528, 530-547: per-open
  artifact cache, selected lineage/artifact authentication.
- `ordinary_binding_reuse/baseline_bundle.py` 261-355; producer source/docs cited
  above: input-format permission and the separate producer materialization cost.
- `ordinary_contact_federation/contact_directory.py` 31, 165 and
  registration-refresh `peer_api.py` 543-564: endpoint and refresh-route limits.
- `HOSTING-COST-CROSSCHECK.md`, SHA256
  `c4f3de927405087879130bc9fa6582ce220d368ca1623dc9e7c86c3542e91995` independently
  checks the narrow source cost claims. Prior decisions retained:
  `ordinary_usable_distribution/CONTINUOUS-USE-DECISION.md` and
  `ordinary_directory_kit/NEXT-CORE-DECISION.md`. Their original deferrals remain
  historical evidence, not claims that the new role has already been implemented.
