# Heterogeneous index profiles: compatibility and the smallest bridge

2026-10-20, core_growth. Source/theory decision only; no runtime, build, new proof
or code change. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Installed source map: `distribution-adaptive-01-input.json` (`a74eaf51`).
The new fingerprint successor preserves the namespace rule examined here.

## Decision

**Default-namespace consumers cannot discover specialist-only publications.**
An atomic feature spec can be queried inside a matching specialist namespace,
but that is different from querying the old default atomic namespace. This is
intentional and previously documented profile isolation, not a broken hash or
mathematical acceptance rule. Nevertheless, requiring every independent agent
to pre-coordinate every operator's pair/path profile is a practical interoperability
gap for the intended heterogeneous commons.

Prefer an **owner-selected bounded base-index projection**, sharing existing
mathematical custody, as the smallest principled compatibility bridge. Keep
specialist profiles isolated and optional. This is a recommendation for root's
next selection, not an implemented capability or authority to change used bytes.
A bounded advisory profile catalogue is useful later, but alone does not make
default clients discover specialist-only data or change their fixed namespace.

## Exact current source trace

| Boundary | Current behavior |
|---|---|
| `type_pattern/discovery/module_export_adapter.py:104-128` | Complete descriptor includes foundation, policy, feature schema and selected profile; its hash is the namespace. `feature_id` hashes namespace plus spec. All inherited atomics therefore change keys too. |
| `type_pattern/client/workspace_evidence.py:54-125` | One immutable workspace config constructs one adapter and one index. Specialized configs require the full explicit profile. No default-index alias or projection is created. |
| `workspace_evidence.py:609-672`, inherited mixed publication | A publication encodes selected module openings and admits them into `workspace.index`. It does not insert into another namespace. |
| `type_pattern/discovery/discovery_store.py:189-259` | Every record, posting, snapshot and proof context binds that index namespace. `Store.admit` re-extracts actual source bytes with its adapter; it does not accept arbitrary claimed features. |
| `client/serve_workspace.py`, `client/serve_advertised.py:270-310` | Ordinary service opens the one configured workspace, constructs a provider with `workspace.index`, and derives the location namespace from that same index. No alternate index is selected. |
| `transport/http_provider_receipts.py:210-238` | Offers to a live provider using another namespace return `NO_OFFER / NAMESPACE_NOT_SERVED`. Candidate/page requests also validate exact namespace. |
| `iterative_queries/client/direct_contacts.py`, `located_queries/client/located_queries.py` | Search and acquisition use the workspace adapter. Successive generations retain the same bound namespace; they are not profile-switching calls. |
| `portable_runtime/location/protocol.py:40-61,156-175`; `maintained_roles.mjs:300-316` | Routing keys include exact namespace and features. The provider serves descriptors only for its configured namespace and an explicitly advertised route. |

Let D be the common base descriptor and p a specialized profile. Write
N0 = H(D), Np = H(D,p), and key(N,a) = H(N,a). Subject to the existing collision
assumption, p changes N and therefore every atomic key. Neither a connected DHT
nor knowledge of the provider's HTTP endpoint changes these checks. A network can
be physically connected while its discovery views remain partitioned by profile.

The namespace is not the module/export identity. `encode_opening` contains only
the common object schema, module ID, relative name and opening. `export_id` hashes
module ID plus name. The same exact mathematical export can therefore be indexed
in multiple namespaces without creating another theorem, definition or proof.
Its index record ID and index proof are namespace-specific and cannot be reused.

## What consumers can actually learn

There is **no public full discovery-profile description endpoint** in the selected
HTTP routes. The location descriptor has a closed field set: namespace, role,
route key, nonce, peer ID, endpoints and assurance flags. It carries neither
the pair list nor fingerprint paths. Snapshot descriptors add `feature_schema`,
partition bits, root, local cut, previous snapshot and coverage claim, but not
the full profile. Export records have hashed feature IDs, not an invertible
profile definition. Wire/custody profile IDs are a different concern and do not
describe discovery feature extraction.

The workspace owner knows its complete persisted config. Another owner may
receive that profile out of band and construct the same adapter before querying.
The whole-type profile currently has a fixed schema-only body, so compatible
software can enumerate that known mode; arbitrary pair/path choices cannot be
recovered from their namespace hash. Guessing a particular known configuration
is not a general profile-discovery protocol.

Prior documentation is explicit: `CONSOLIDATED-RELEASE-SEAM.md:67-72` requires
providers and consumers to retain matching profile configuration;
`type_pattern/README.md:69-99` rejects cross-profile record acceptance and charges
all duplicate inherited postings when both profiles are served. Thus the current
software supports **explicitly configured federation**, not automatic heterogeneous
profile negotiation. This limitation must not be hidden by saying that all
atomic features "remain available" without adding "in that same namespace."

## Proposed bridge: an independently maintained base projection

Use the existing default `ModuleExportAdapter` and `Store`, not an alias that
rewrites namespaces or accepts a specialist record as a base record.

1. An owner selects a finite list/batch of retained `(module, relative_name)`
   exports and an explicit bounded destination base index. No corpus scan or
   automatic every-profile replication is required.
2. Read each actual held opening from the module store, encode the same public
   export bytes, and call the base index's ordinary `admit` with the exact export
   ID. This rederives base features and authenticated index state. Keep the source
   specialist index, custody bytes and mathematical warrants unchanged.
   Materialization is a separate explicit owner operation from serving. A later
   service renewal reopens a retained projection; it does not automatically
   rebuild it or project contributions received since its last selected batch.
3. Serve that base index together with the same module/packet custody through an
   explicit owner-selected provider role. Existing `CompositeProvider(index=...,
   custody=..., packets=...)` already supports this separation at the low level.
   The ordinary service wrapper currently hardwires `workspace.index`; a small
   public projection/service composition is the missing operational seam. The
   existing owner-run entry can compose `Workspace.open`, a separate quota-bounded
   `Store`, and this provider without inventing another network/core mechanism.
   It must keep the actual workspace open exactly once under its exclusive lock
   and pass that workspace's original custody objects to the provider. A second
   process cannot concurrently reopen the same workspace merely to serve the
   other profile. Select exactly one index in a service invocation; switch views
   only through a later explicit invocation after ordinary close. Metadata
   preparation without this actual service/routing binding is not discoverability.
4. Advertise only the owner-selected base routes of the actually served base
   index. Keep existing egress, TLS, lifespan, maintenance, hard containment and
   advisory-not-authoritative descriptor rules from `SERVE-AND-ADVERTISE-DECISION`.
   Base and specialist discovery may use successive bounded service selections;
   simultaneous dual serving, a multi-namespace router or a second mathematical
   custody copy is not required by this first bridge.
5. Record each committed target-index snapshot/partial outcome and charge reads,
   extraction, index hashes, metadata, postings, retention and serving. Existing
   idempotent `Store.admit` permits bounded reconciliation. No cross-database atomic
   publication, all-corpus coverage, eventual catch-up or automatic renewal follows.
   Serving reports the selected index namespace and cut, and the explicit partial
   batch/coverage outcome. Do not label the projection current with all source
   publications, especially after a quota refusal or later source additions.

For any selected export x successfully projected and retained in base snapshot S,
the ordinary base query predicate is evaluated against the base extraction of
x's original bytes. A base consumer can now find x under the same routing,
availability, budget and query-coverage assumptions as any other base export.
Resolved mathematics is unchanged and still passes actual receipt/native admission.
The projection establishes compatibility, not global completeness or selectivity.

This bridges unknown theorem IDs: the base consumer needs its ordinary formal
features, not x's ID or p. An independently operated indexer could supply the
same bridge for a funded selected corpus. No required central index, global
profile registry, common research agenda or proof authority is introduced.

The cost is real: the base projection duplicates base postings/metadata and may
serve large popular buckets. It need not duplicate packets, semantic bodies,
certificates or proof computation. Set explicit quotas; stale/missing projected
exports are incomplete coverage, never mathematical falsity. It is not necessary
to project every specialist profile into every other specialist profile.

## Why a catalogue alone is insufficient; later extension boundary

A bounded advisory catalogue could expose complete locally supported profile
descriptors and their namespace hashes at already authorized contacts. Consumers
must validate a known closed schema, recompute the namespace, refuse unknown
feature algorithms, and explicitly fund any chosen profile. Never load remote
code, silently switch a workspace's immutable adapter or renew authority/budgets.

Such a catalogue helps choose a useful specialist after a contact is known. It
does not explain how a base-only DHT lookup finds a specialist-only provider in
the first place, nor how one current client switches namespaces. A shared/base
advertisement or another explicit bounded rendezvous and a separately scoped
multi-profile consumer design would still be needed. Defer those extra changes
until the simple owner-selected base bridge is decided; do not redesign the
global lookup protocol merely to expose one profile configuration.

## Minimal next evidence if root selects implementation

No new theorem or provider-scale experiment is required. Reuse one exact opened
export; place it in two real structural indexes with different profiles; show a
default query finds only its correctly regenerated base projection, wrong-namespace
records still fail, and the exact export ID/opening stays unchanged. Inspect the
ordinary service selector to ensure it binds the selected base namespace to the
actual served index while sharing original custody. One focused changed-boundary
control can establish this; it must not be claimed as useful growth or global recall.

Selected current pins used for navigation: adapter `336ae03b`, index store
`2e7cae37`, ordinary service `89723f2e`, advertised service `80d6c074`, receipt HTTP
provider `4e00afb1`, evidence transport `5808c0e2`, location protocol `cb336e51`.
