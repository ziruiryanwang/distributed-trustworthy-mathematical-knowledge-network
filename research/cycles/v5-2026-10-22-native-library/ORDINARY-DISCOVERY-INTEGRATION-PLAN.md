# Ordinary discovery: implementation path after the reciprocal Lean boundary

2026-10-23. `ordinary_discovery_path`. Source-only plan; no runtime, code change,
network request, Git action, migration or new acceptance was performed. Root owns
selection. This updates the implementation status of `ORDINARY-DISCOVERY-SEAM.md`,
not its full specification. All paths below are relative to the canonical root.

## Recommendation and payoff

Finish the current real ordinary consumer/export/admission boundary, then connect
it to the **existing authenticated index and search transport**. Do not build a
second index or revive certificate production. The next observable behavior is:

> B asks about known `Std.ExtHashMap` and `insertMany` meanings, without A's name,
> UnitID or ExportID; obtains A's advertised method and exact inert evidence;
> uses its already warranted library plus checked missing units; and returns a
> new independently checked result through the same publication interface.

The current fixtures establish compatibility, not autonomous discovery or growth.
A real unknown-ID search needs an input that does not contain A's answer and an
auditable record that candidates came from the query, not a hidden target lookup.
The query and user-local objective can be fixed before provider results arrive.

The first slice need not repeat initial Std/basis onboarding. Use the accepted
library context and charge that historical cost separately. Test only the new
query/preview/acquisition linkage and actual missing contribution. Replaying
2,852 accepted units would not validate this linkage better.

## What exists, and the precise gaps

| Existing source | Actual reusable contract | Required successor |
|---|---|---|
| `software/v5/ordinary_lean/ordinary_preview.py:136,202,234` | Bounded V1 preview parsing, generation from inert evidence, exact evidence/header/type-binding comparison. All results explicitly deny mathematical acceptance. | Portable V2 envelope/locator support after the identity decision below. Reuse its DAG/name grammar; do not write a second Lean parser. |
| `software/v5/ordinary_lean/ordinary_semantics.py:53,86,175,198,204` | Exact foundation/semantic descriptors and proposed V2 unit/export/basis identity functions. | Connect them to actual local warrant lineage and V2 previews. These helpers alone do not establish a portable accepted library. |
| `software/v5/discovery/formal_features.py:142,174` | Strict record validation and domain-separated record identity. | One new ordinary record branch, strict locator validation and fresh hash domain; retain old record bytes/domains. |
| `software/v5/discovery/discovery_store.py:58,210` | Adapter-driven record admission, exact advertised-byte binding, immutable snapshots and postings. | Permit the ordinary feature schema. No algorithm change. |
| `software/v5/discovery/authenticated_index.py:366` | Snapshot validation and authenticated maps/vectors. | Permit that same feature schema. No Merkle format change. |
| `software/v5/discovery/candidate_query.py:129`, `discovery_query.py`, `search_session.py`, `summary_wire.py` | Bounded conjunction queries, positive membership or examined-range claims, aggregate sessions and offers without a known snapshot ID. | Reuse unchanged through the coherent schema-aware assembly. |
| `software/v5/transport/clients.py:25-89`, `http_provider.py:178-241` | `SearchClient.offer/page/candidates` and provider routes parameterized by namespace/features and the shared validators. | Reuse for ordinary searches. Exact selected module assembly must load the new validators, not historical copies. |
| `software/v5/location/protocol.py:40-54`, `observed_route.py:19` | Namespace/feature rendezvous and bounded provider-location operations. | No ordinary-math schema change in this low-level key computation. Connect after direct-contact query works. |
| `software/v5/ordinary_lean/local_catalog.py:223,317` | Protected V1 context/warrant checks, exact dependencies and no-overwrite admission. | Keep its successful acceptance semantics. Add an explicit portable identity bridge or select a coherent V2 catalog successor; never reinterpret V1 profile IDs in place. |
| `software/v5/ordinary_lean/owner_request.py:87` | Point-lookup selected authoring closure from an actually warranted local context. | Call only after acceptance; not a network proof-acquisition algorithm. Its callbacks still require a parent-operation I/O budget. |

Add one `ordinary_export_adapter.py` following the existing adapter protocol:
`namespace`, `feature_schema`, `describe(raw, expected_id=None)`, `extract(...)`
and `resolve(record, raw)`. Its ordinary preview is **advertised metadata**, not
a certified module group opening. The adapter extracts kind, exact type-symbol,
result-head and binder-domain-head features with the existing finite 128-feature
and eight-conjunct bounds. Type DAGs remain shared; do not expand proof bodies or
all definitions during indexing. Explicit profile refusal is preferable to
silently truncating a type's feature set.

This is still one adapter plus three schema-aware index successors. The new work
outside that index seam is the necessary ordinary acquisition/acceptance bridge,
not a hidden change to the index's trust model.

## Settle portable identity without redoing successful checking

V1's current profile includes local binaries/controller/support and consequently
changes mathematical IDs between compatible builds. The new `ordinary_semantics`
functions remove that coupling, but neither `ordinary_preview` nor `LocalCatalog`
currently consumes V2 evidence. A V1-only index can test local plumbing; it must
not be presented as a globally interoperable identity solution. Avoid making a
large V1-only public interface that needs immediate replacement.

The smallest candidate for investigation is a **protected owner-local identity
bridge**, leaving the accepted V1 catalog, snapshots and native checker unchanged:

1. Select the exact existing V1 profile and exact S/F descriptors. Record why the
   selected ordinary unit interpretation and foundation implement the same
   judgment; a string or hash asserting compatibility is insufficient.
2. Starting from an eligible protected V1 root, translate retained evidence in
   dependency order: preserve each `unit` value exactly, change only the envelope
   schema/semantic field and external import IDs. Fixed basis identities map to
   `(S,F,name)`; ordinary references map to already translated exact exports.
3. Bind every translated output to its exact existing V1 warranted name/symbol,
   exact original input and unchanged original checking lineage. The bridge is a
   local protected mapping, not a transferable acceptance certificate. Include
   its adapter/support identity in the warrant justification. Withdrawal or
   ineligibility of the original support disables dependent aliases.
4. For a genuinely new V2 unit, resolve all portable imports through active local
   bridge entries. Construct a V1 checking envelope with the *same unit* and
   corresponding local imports, use unchanged actual checking/promotion, and
   only then add new V2-to-V1 output bindings. No peer alias is authority.

The preservation argument is induction over the unit DAG: the basis meanings
are fixed, the unit syntax does not change, and each external reference denotes
the same already warranted declaration. The local snapshot still records its
real original writer/profile; no relabeling of native artifacts is necessary.
Missing proof dependencies and incompatible meanings still refuse or require
genuine new checking. This is a proposed design, not adopted source or a proved
whole-Lean refinement.

This bridge may be less work/risk than changing all successful catalog internals
at once. It also needs a bounded persistent mapping and active-lineage checks;
do not hide them in an untrusted JSON alias dictionary. Compare its concrete
implementation size against a V2 catalog successor before selecting either.

**One-time translation is not proof-free indexing:** a V2 UnitID commits to all
direct imports, including proof dependencies, so translating the producer's
IDs may require visiting its retained proof-dependency DAG, not just the 387
authoring-semantic groups. That is a bounded local data transformation, not
rechecking their proofs and not work on every search. Reuse exact evidence lookup
metadata; do not rescan the entire global corpus. Do not promise that a subset's
IDs can be translated from its type alone.

## Acquisition: one actual missing seam, not an existing certified client

`transport.clients.AcquisitionClient.export` at line 121 requires
`EXPORT_RECORD_SCHEMA`, `module_id`, `relative_name`, a group index and
`encode_opening`. `ReceiptAcquisition` and `evidence_network` additionally expect
certified ModuleSpec/packet profiles. They **cannot be reused unchanged** for
ordinary UnitIDs. Their comments saying "ordinary client" describe the owner
application, not this new ordinary-Lean evidence format.

Select a narrow ordinary preview/evidence route, with independent explicit wire
schemas. It can reuse existing Endpoint/TLS, bounded header/body reads, explicit
contacts, reservation/failure accounting and provider lifetime patterns. It must
not pretend an inert ordinary unit is a module receipt or call certificate
admission to establish its truth.

The minimal two typed fetches are:

- `preview(record object_sha256, object_bytes) -> exact preview bytes`;
- `evidence(semantic_id, unit_id, max_bytes) -> exact canonical inert envelope`.

The selected provider offers only locally retained exact bytes. No remote source
compilation, path selection, arbitrary URL forwarding or native-artifact import.
An unavailable byte object is an acquisition failure, not a negative mathematical
answer. Keep provider addresses outside semantic identity. Use content-addressed
local retention so another provider can return the same bytes later.

Before sending, reserve one outer deadline and finite suballocations for index
requests, previews, evidence acquisition, checking and output storage. Sum of
suballocations must fit the parent grant. Include failed candidates and unknown
dependency acquisitions; moving to another provider must not renew the budget.
Bound received bytes before allocation/parsing, not only after download.

For a first source boundary, the same typed fetch callback may read a bounded
local retained object by UnitID. That proves no networking result; it isolates
identity/acceptance integration before changing transport. Then bind it to the
existing public HTTP mechanics rather than designing a new network stack.

## First query-to-accepted-result sequence

1. Producer publishes a proof-free preview generated from its accepted inert
   evidence, through `Store.admit`; its ordinary evidence remains separately
   available. Index admission alone is never mathematical admission.
2. Consumer resolves its already warranted `Std.ExtHashMap` and
   `Std.ExtHashMap.insertMany` to exact shared portable symbols. Form conjunction:
   theorem kind + those two symbols, optionally result-head `Eq`. Do not include
   A's namespace, `ReadsOnly`, `Avoids`, theorem name, UnitID or ExportID.
3. `SearchSession` and `SearchClient.offer` obtain a provider-selected snapshot.
   Existing counts select an anchor and partitions; bounded candidate requests
   return records with positive membership evidence. Inspect the returned types
   and premises; the index does not choose the agent's research objective.
4. Fetch a selected preview, require exact record size/hash and recomputed feature
   equality, then fetch its exact UnitID evidence. Recompute header/type bindings
   using the ordinary preview resolver. Each of these checks still returns
   `mathematical_acceptance=false`.
5. Query the protected local warrant map for dependencies. Reuse eligible accepted
   meanings. Acquire/check only missing units in dependency order, under the same
   aggregate grant. Bind portable/local IDs explicitly. Native checking and exact
   output inventory, not the advertisement, permit the local commit.
6. Feed those now-warranted targets to `owner_request.prepare` and the selected
   ordinary authoring command. Export the consumer's real theorem and independently
   admit it. Generate its preview and publish through the same API.

The existing initial recovery includes A as well as Std. For an immediate search
integration it may be a **cache-hit** consumer: that exercises query selection,
preview/evidence binding, local reuse and contribution without repeating A's
admission. Report it as such. A later genuinely missing-contribution check should
use the new successor theorem above an already accepted base, not manufacture a
fresh Std onboarding just to make the workflow appear independent.

## Scalability and evidence claims

Feature extraction costs O(selected type DAG nodes/edges), not proof ancestry.
For a partition and smallest posting-list count `a`, candidate search scans at
most its configured allowance `s <= a`, with at most `k-1` membership probes per
examined ID (`k <= 8`) and proofs only for surviving bounded results. B-tree and
Merkle costs remain; this is not constant-time or logarithmic semantic discovery.

The current eight-bit partitioning gives 256 partitions. It does not itself
bound a planet-scale hot posting list. Selective predicates, specialist provider
corpora and budgets are the present scaling tools. New index data structures are
justified only if a relevant real query cannot be selective enough. Exhaustion
returns an explicit partial outcome; never a false complete/absent verdict.

Positive candidate pages authenticate returned metadata membership, **not omitted
negatives**. Examined-range pages authenticate the stated finite snapshot range,
not that the provider indexed every theorem or extracted every feature honestly.
Recomputing one preview's features checks that candidate only. Multiple providers
improve options, not a theorem of global completeness.

Use one bounded changed-boundary test set: real unknown-ID query; wrong shared
meaning; preview/header/import tampering; alternative metadata for one export;
failure charging; and actual resulting ordinary acceptance/reuse. Old index,
projection, basis and helper campaigns need not repeat. Identical old record
domains should be checked as source invariants or small compatibility controls,
not another broad test campaign.

For growth, retain the equally optimized ordinary-library baseline from
`PAYOFF-AUDIT.md`. A successful query and returned theorem show reciprocal
capability. They do not show mathematical novelty, autonomous usefulness or a
net savings. Charge indexing, previews, failures, one-time identity translation,
initial checks, persistent storage and publication alongside saved local work.

## Proposed next source assignments

1. Root keeps the current consumer/successor acceptance as the immediate priority.
2. One author selects the identity bridge versus catalog V2 using a concrete
   source-sized plan, then implements the chosen route and V2 preview support.
3. In parallel, one author implements the adapter plus exactly three index schema
   changes against that fixed preview/identity interface; a reviewer checks the
   trust boundaries once, not duplicative architecture essays.
4. Root connects one typed acquisition callback and actual ordinary consumer.
   Only after that resolves is a narrow transport successor selected.

No step selects another certificate campaign, all-corpus scan, global task list,
LLM trainer or new consensus mechanism. None claims completion of full v5.

## Final source-sized choice: a V2 catalog with one-time legacy import

Root requested a concrete comparison after reading this plan. Inspecting the
actual worker changes the recommendation: **select a coherent V2 catalog with an
explicit one-time owner-local V1 warrant import, not permanent bidirectional
V2-to-V1 admission.** Preserve the native context in either design.

The decisive fact is `OrdinaryWorkflowWorker.lean:160-178,211-237`: its extension
input is a local module-loading plan plus raw declaration units. It does not
interpret V1 `profile_id`, external symbol IDs, or portable evidence envelopes.
`LocalSnapshot` likewise receives concrete local module names/paths. Thus a V2
Python catalog/controller can continue using the **same already built native
checker** and original snapshot bytes; native rechecking/rebuilding is not an
intrinsic cost of choosing V2. The old materialization names must be preserved,
not recomputed from new portable or local-root IDs.

| Mutation surface | Permanent dual-ID bridge | Coherent V2 plus one-time import |
|---|---|---|
| Public preview/evidence/index | New V2 parsing, previews and adapter regardless. | Same work. |
| Local acceptance | V1 `LocalCatalog` unchanged, but every new portable input needs translation before reservation and every committed output needs a second protected portable promotion. | Successor of `local_catalog.py`: separate S/F/I; V2 evidence/domain functions in `reserve_basis/reserve_extension`; local root and record creation in `_reserve/_commit_checked`; preserve grant, lock, no-overwrite and withdrawal rules. |
| Persistence | New alias store plus exact linkage to the existing store, lock ordering, crash-between-promotions recovery, bidirectional ambiguity rules and two eligibility lookups on use. | One catalog authority after import. Records explicitly distinguish original native-check lineage from identity-translation lineage and retain snapshot origin. No second acceptance promotion for future units. |
| Existing snapshot use | Map V2 names through V1 root/module plans on every use. | Change `context` at lines 223-266 to read the retained exact `module_name/parent_module` and writer origin, rather than deriving every artifact's name from its new record root. New chunks use new local-root module names. |
| Controller | Wrap `prepare_bundle`, reservation and final promotion with both identity systems indefinitely. | Version the Python ordinary controller's envelope/dependency calculations and report-parent binding. Parent module comes from the authenticated plan, not `module_name(newParentRoot)`. Actual clean-worker and exact-input/output checks stay unchanged. |
| Authoring | Keep V1 request/export labels internally, translating every publication. | Version `owner_request` and the small command/header plumbing once for explicit S/F/local-context labels; keep matching rules and raw unit format. |
| Historical migration | Still required to derive portable IDs for current knowledge. | Same dependency-order identity translation, but performed once into fresh V2 records; preserve V1 store read-only. |

The dual bridge is locally smaller only if one counts edits to existing files and
ignores its new durable cross-store protocol. That is the wrong complexity
measure for the final product. A read-only translation table is useful migration
evidence; a second permanent warrant authority is not needed merely to retain the
successful native work.

Bound the V2 change: one homogeneous current semantic contract; one selected
implementation per new catalog; sticky whole-store withdrawal initially; one
explicit legacy-import operation; no arbitrary mixed-version live upgrade.
During import, preserve every old checker/writer origin and record translation as
translation, **not a new native check**. A fresh V2 store must remain unusable
until the entire selected migrated lineage is validated and atomically activated.
Keep the old store intact if import fails. Verify exact old output bindings and
all needed retained evidence before deriving V2 bindings; no network alias input.

Implementation order: pure V2 evidence/preview functions and fresh catalog schema;
explicit source-reviewed legacy import of the already accepted selected lineage;
controller/owner-label integration; then index adapter integration. The raw Lean
codec, kernel extension checker, built worker and accepted artifacts remain
unchanged. If source review exposes a native assumption tying restored modules
to V1 hashes beyond the inspected plan, stop at that exact dependency rather than
starting a blanket recheck. No operation is selected by this recommendation.
