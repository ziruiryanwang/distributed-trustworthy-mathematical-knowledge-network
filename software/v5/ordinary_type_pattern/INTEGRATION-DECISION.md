# Optional whole-type patterns in one ordinary product

2026-10-28. query_scaling; source-only design requested by root. This checkpoint
changes no implementation, selected package, guide, index, owner or native bytes.
No imports, controls, runtime, database access or Git operations were performed.

## Decision

Recommend one fresh successor package with an explicitly selected discovery
configuration, not a second whole-package product. Preserve the exact profile as
the default. Proposed configuration values are `exact-v2` and `type-pattern-v1`,
under an optional `discovery_profile` field. These are design names, not an API
already present. Missing means `exact-v2`; unknown values refuse. Never infer a
mode from a peer record, a pattern-looking spec, an existing database or an old
report. Selecting pattern mode creates a different namespace and requires a
fresh index. It does not overwrite, migrate or relabel the exact index.

Implement the choice as an explicitly configured instance of the existing
`OrdinaryExportAdapter` class. This matters: `OrdinaryAcquisition.__init__`
requires `type(adapter) is OrdinaryExportAdapter`, not a structural interface
or subclass. A separate adapter class would require an avoidable transport trust
boundary change. The class's old constructor call must retain the exact old
namespace, specs, record bytes and extraction/refusal behavior. In pattern mode,
use the new `pattern.py` helper and add its one required whole-type feature to
all the existing feature specs, rehashed under the new namespace.

There are two distinct identities: the new package's `PROFILE.json` pins its
software; `discovery_profile` selects the index/query relation inside that
software. The latter is not a freely supplied source path, adapter name, hash,
feature limit or semantic contract. Neither identity conveys mathematics.

| Choice | Consequence | Decision |
| --- | --- | --- |
| One package, exact default, explicit pattern configuration | Small adapter/factory/config changes; one loader, one source map and one operator guide; separate namespace and index per choice | Recommended |
| Separate exact and pattern package profiles | Some caller changes disappear, but two full package/compatibility/host-seal selections must be maintained; copying and silently changing the adapter default risks losing old-record readability | Not simpler overall |
| A second adapter class in one package | Requires widening the acquisition exact-class check as well as the same config and validator work | Avoid for this boundary |

## Selected evidence and unchanged support

The comparison baseline is the actual 160-file directory assembly at
`experiments/v5-local-checks/name-directory-assembly01/distribution/package`,
whose assembly receipt is SHA-256
`32a82749f9cac1113e6529a1e82bafe1750fddc39ceb7efe2b0c1c233aeb741d`.
Its PROFILE is
`7687d5276d8a7edc0beeb7066e4cbaae16529b0e88d8a0728b003dad04a4dd34`;
installation manifest remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
The actual directory integration is separate evidence, not evidence that the
pattern changes below have run. The preceding current kit remains the adopted
kit until root completes its coherent successor adoption.

Inputs are LAW-SHAPE-DECISION, this directory's SELECTION/CONTRACT, and
`pattern.py` SHA-256
`356d98e317381a95799b5ba59c2809e256dee75e4676c693c4fb60b474767b11`.
The port's exact variant relation, DAG reasoning, and existing bounds are not
reproved or enlarged here. No Lean/native rebuild, installation/core change,
proof/certificate change, owner schema migration or additional theorem episode
is needed for this integration.

The package already contains `installation/foundation/inventory.json`:
823,690 bytes, SHA-256
`c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`.
This is exactly `ordinary_semantics.INVENTORY`, committed by the installation
manifest and fixed by `NativeInstallation.open`. It is not an owner catalog.
Read its bounded exact bytes from the selected installation; pass them through
`pattern.prepare_inventory` before use. Its 581-name immutable process-local
table may be reused across that invocation's extractions. Do not accept another
inventory, a serialized prepared table, a foundation inferred from preview
spelling, or an owner-dependent inventory path. Exact-only mode need not prepare
this table. An offline pattern query needs no owner, runtime attachment or Lean
process to read and verify this fixed file.

## Adapter and record contract

Keep exact `namespace_for(semantic_id)` and all its descriptor fields byte-for-
byte equivalent when no mode is supplied. Add an explicit pattern choice whose
descriptor retains the semantic ID, syntax/preview/evidence formats, exact-type
profile and partition policy, and additionally binds the pattern `PROFILE_ID`
under a new feature revision. Retain the 128-feature cap. A namespace must bind
the relation and required feature policy, not the package path, implementation
ID, source hash, provider, current context or configurable inventory. A future
pattern profile change gets another namespace.

Extend spec/feature/query helpers with an explicit mode, or add an instance
`compile_query(specs)` that delegates with the selected mode. Keep old module
entrypoints exact by default. `declared-type-pattern` is accepted only in pattern
mode, with exactly `{tag,value}` and a lowercase 64-hex value. Require that its
selected namespace is the pattern namespace of the approved semantic contract.
An exact-mode caller presenting that tag refuses; it must not get an empty or
silently broadened query. Pattern-mode queries may also use old tags, compiled
under the new namespace. The one-to-eight conjunction limit does not change.

In `describe`, preserve all existing object-kind, declaration-kind, type-symbol,
head and exact-type features. Only the pattern branch calls
`preview_pattern(raw, prepared_inventory, limits)` and adds the returned spec.
Its extra parse and DAG work are real costs. Include the returned structural
work/counters without calling them physical CPU or omitting byte/parse costs
from the broader bound. The same bounded raw preview remains the object; its
ExportID, preview hash/length and locator stay unchanged. Record schema can
remain `DMKN_FORMAL_FEATURE_RECORD_V3` and feature schema can remain
`DMKN_ORDINARY_LEAN_EXPORT_FEATURES_V1`: the namespace distinguishes the feature
relation. Record IDs and every feature ID necessarily differ in pattern mode.

One non-obvious validator change is necessary. `formal_features.validate_record`
routes V3 records to `ordinary_export_adapter.validate_record_locator`; that
function currently requires the single exact namespace even when a caller has
already checked its own namespace. In the fresh successor, recognize exactly
the old exact and new pattern namespaces for the locator's semantic ID. First
accept the old namespace on the old path; lazily consult the new profile only
for a nonexact namespace. Preserve all locator syntax, kind and ExportID checks.
Do not accept any syntactically valid namespace. No new record schema, generic
record validator change, or wider acquisition class check is necessary.

This generic recognition does not claim correct feature extraction. Generic
records contain feature hashes, not enough information to validate the pattern
claim by themselves. `Store.admit` still calls the selected adapter's extraction;
`resolve` still demands selected-namespace equality and exact rederived record
equality. Authenticated search still proves membership in a provider-selected
index, not truth of the theorem or semantic fidelity of its advertised type.

| Input and selected operation | Required result |
| --- | --- |
| Old exact V3 record, new package, default/exact adapter | Same locator validation, record ID and rederivation result as before |
| Old exact index, same limits/access-pair config, new exact adapter | Existing Store config matches; old snapshots/postings remain unchanged |
| Old exact record supplied to pattern `preview`, `receive` or resolve | Refuse selected-namespace mismatch before remote acquisition; do not translate features |
| New pattern record supplied to exact operations | Refuse selected-namespace mismatch |
| Valid V3 record with either known namespace passed to generic metadata validation | Recognize its structural/locator contract only; no extraction, membership or mathematics inferred |
| V3 record with any other namespace | Refuse locator namespace |
| Exact database opened with pattern adapter, or pattern database with exact adapter | Existing `STORE_CONFIG` mismatch; no migration or second initialization |
| Existing V1/V2/V4 record handling | Unchanged dispatch and schemas; this work modifies only ordinary V3 recognition |
| Same preview newly admitted into a fresh pattern index | Recompute all features; create new record/postings/snapshot in that namespace |

## Minimal public integration surface

The following are future fresh-source roles; the used baseline files remain
frozen. One centrally reviewed selector should validate the mode and construct
the same adapter class, preparing the inventory once when required. Do not
scatter mutable global mode switches across modules.

| Role | Smallest necessary change |
| --- | --- |
| `support/discovery/ordinary_export_adapter.py` | Explicit instance mode, mode-bound namespace/spec/query helpers, required extra feature, exact-or-pattern V3 locator recognition |
| New `authoring/py/ordinary_type_pattern.py` | Package the selected `pattern.py` under a distinct import name; pure helper remains file/owner/network-free |
| `profile.py` | Add helper to AUTHOR/required pinned census/import identity checks; retain installed inventory and native/core pins |
| `peer_api.py` | Shared mode selector/factory; apply to find, directory-find, directory-serve, preview, receive, publish and serve; pass selected adapter into `_index`; bind mode/namespace in reports |
| `discovery_store.py` | No implementation/schema change: constructor already binds adapter namespace/feature schema into exact stored config; admit already reextracts and validates |
| `ordinary_acquisition.py`, provider, authenticated search, pair access | No implementation change expected: same adapter class and V3 schema; namespaces and feature IDs flow through existing paths |
| `custodian.py` | Explicit prepare/serve mode, pass it through `_index` and internal `api.serve`, require selected namespace to equal sealed namespace |
| `host.py`, `peer.py`, `run.py` | Existing pinned JSON config transport is sufficient; no new CLI option or worker/native launch is needed for the mode |
| Offline pattern query companion | New bounded helper taking selected raw V2 preview or native query AST, fixed inventory and pinned source closure; emit explicit specs/provenance |
| Existing `query.py` and name-directory files | No change required: their exact/native/symbol/history contracts continue; do not relabel their result schemas |
| Operator companion and compatibility map | Accept and preserve explicit mode in applicable requests/configs; validate pattern specs only for pattern mode; carry selected mode from request through preview/receive; refresh exact known-source inventory for the new package |
| Source map, file assembly, kit catalog/guide | Pin fresh Python roles and companions; assemble from current 160-file baseline; publish one coherent current guide only after adoption |

Use a top-level `discovery_profile` on the listed peer operations. Keep the
nested index config's existing path/create/limits/access_pairs shape. `_index`
receives the already selected adapter instead of unconditionally constructing
an exact one. Its existing default-call compatibility can remain exact where
needed during implementation, but no pattern branch may omit this argument.
Validate selection before dialing. Wrong-profile index opens already fail
closed at the stored configuration check; they are not migration attempts.

`directory-find` must propagate its selected mode into the internally generated
find configuration and compile route subsets in that same namespace.
`directory-serve` maps only one explicitly selected namespace per invocation.
Do not infer the mode separately for each route or combine exact and pattern
namespaces in one search/session. Existing contact endpoints can be selected
explicitly for either service; serving both namespaces means separate selected
indexes and service endpoints/leases, not new mixed-namespace wire routing.

`inspect` and `authoring-offers` operate on exact portable identities after a
preview, not on a discovery record's feature namespace; they need no new mode
to fetch the same locator/evidence/offers. Their exact-ID behavior and received
mathematical checks remain unchanged. A pattern preview may lead to them by
the existing explicit selection of an actual binding/ExportID.

Dedicated host prepare/serve config must select the same mode. The existing
seal already binds `namespace` and `profile_sha256`; the selected mode must
reconstruct exactly that namespace. No seal-field/schema expansion is needed
merely to duplicate the mode label. The sealed namespace may be reported as
provenance, but it must not silently choose the mode when the caller omitted it.
Keep the existing exact package-profile check: an old sealed host cannot be
silently resumed under changed software. Its frozen package remains usable;
a successor host is a separately selected fresh preparation, with its copying
and indexing cost retained. This limitation is distinct from the Store's ability
to reopen an ordinary exact index under unchanged config.

## Offline query and operator workflow

A new packaged companion is preferable to expanding the owner-opening query
command. It pins the new software profile and captures the necessary small
source closure: ordinary_evidence/semantics/portable_evidence, ordinary_preview,
portable_preview, formal_query, ordinary_type_pattern, formal_features and the
adapter's namespace/spec helpers. Check installed core source pins against the
installation manifest and helper pins against PROFILE; reject preloaded product
modules and execute only captured approved bytes. Read the already shipped
inventory directly, verify its exact hash/size, and use the existing pure APIs.
No `NativeInstallation.open`, runtime attachments, owner or proof is required.

Accept exactly one explicitly selected, hash-pinned V2 preview or native query
AST. Produce a small `SPECS.json` containing the pattern singleton and a distinct
result schema recording input kind/hash, package profile, semantic/foundation
identity, `discovery_profile`, namespace, pattern PROFILE_ID and extraction
costs. Optional existing-kind conjuncts can be composed explicitly within the
normal eight-spec limit. Refuse partial/malformed/oversized input before output
commit. Do not invent portable bindings for native names or make the result
look like `prepare-query`/`prepare-symbol-query` or a current-owner report.

Initially the operator's existing explicit-spec path is enough: select
`type-pattern-v1`, supply these specs, choose the pattern provider endpoints and
run ordinary find -> preview -> inspect/receive. Extending `query_report`
recognition is not necessary: initially require explicit `specs` for pattern
mode and retain existing `query_report` recognition for exact mode. The current
preparer's tag whitelist needs one
mode-gated tag, and its exact request field validators need the explicit mode
for find/preview/receive/publish/serve. If a report supplies a selected record,
the user's requested mode must agree with its namespace; it must not be inferred
from untrusted report text. Keep current package-profile/report compatibility
and explicit prior-profile selection rules intact.

The current operator wrapper also requires an exact direct-source compatibility
map; merely adding a tag to prepare.py is insufficient. Refresh its known-role
map and wrapper pins along with the new package. Dedicated host already uses
explicit JSON config examples; update those examples within the same current
guide instead of inventing a parallel product entrypoint. Historical guides and
used kits remain historical, not silently repointed.

## Feature exhaustion, persistence and cost

Let m be the number of distinct existing exact-profile specs for a selected
preview. Pattern mode requires m+1 features, all compiled in its new namespace.
Under collision resistance, the new tag supplies a distinct feature. If m <=127,
the new record can fit the existing 128-feature ceiling. If m=128, extraction
must raise an explicit pattern-profile-exhausted refusal; no old feature or new
pattern key may be dropped and no exact-mode fallback may occur. Inputs already
refused by existing syntax, bounds or old extraction still refuse. No limit is
raised to 129, and generic `MAX_FEATURES`, posting quotas, wire/record byte caps
and pair-access budgets remain unchanged. Hash-collision assumptions should not
be hidden behind a claim of unconditional distinctness.

`Store.admit` extracts before `BEGIN IMMEDIATE`, so exhaustion adds no record,
posting or snapshot for that target. This is not a claim of whole-operation
rollback: current publish creates/opens the index and puts the inert preview in
custody before admit; earlier targets are separately committed. Their retained
cost/output stays in a partial-failure report. Dedicated host preparation may
likewise retain custody/index contents after a later target refuses; without a
final host seal it is not a completed host, and the failed directory is not
reused. Do not silently skip refused targets or label the selected corpus complete.

Fresh pattern indexing duplicates the entire record/posting namespace, not just
one posting per already indexed object. Retain both indexes only by explicit
operator choice. Existing configured access pairs are profile-local feature-ID
pairs; old hashes cannot be transplanted into the new namespace. Omit pair access
or explicitly compile the intended pairs for the selected profile. No all-pairs
expansion is needed. Pattern equality remains an advisory full-type variant
relation; bucket selectivity, inspection savings and net payoff depend on the
actual corpus and are not established by this design.

## Later focused integration checks

The already selected pure DAG controls are a separate boundary. A later finite
integration selection should test only the new seams: exact default byte/record
stability; both directions of namespace mismatch; known V3 namespace recognition
and unknown refusal; same adapter exact-class acquisition; pattern native/preview
query agreement through the packaged inventory; explicit mode propagation through
direct/directory find, preview/receive and host seal checks; old exact Store reopen
versus wrong-mode refusal; m=127 success/m=128 refusal and retained partial state;
and fresh relocated operator/package profile pinning. Reuse inert controls where
possible. No full proof, old theorem campaign, native build or worldwide discovery
experiment is justified merely to qualify these source/config changes.

Source trace: ordinary_formal_query/discovery/ordinary_export_adapter.py
(`namespace_for`, `validate_record_locator`, `OrdinaryExportAdapter.describe`);
discovery/formal_features.py (`validate_record`, `record_id`);
ordinary_multi_source/ordinary_acquisition.py (`OrdinaryAcquisition.__init__`);
ordinary_multi_source/peer_api.py (`_index`, publish/serve, find/directory routes,
preview/receive and exact-ID inspection); ordinary_sparse_access/discovery_store.py
(`Store.__init__`, admit); ordinary_dedicated_host/custodian.py (prepare, seal,
serve); ordinary_name_directory/profile.py and source-map.json;
ordinary_reply_capacity/operator/{prepare.py,prepare_selected.py,compatibility.json};
ordinary_parse_reuse/ordinary_admission.py (`ADMISSION_FIXED_BASIS_BYTES`).
