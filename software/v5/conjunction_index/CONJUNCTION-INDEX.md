# Optional paired-feature discovery indexes

This profile addresses a narrow search problem: two individual feature lists
can both be huge while their intersection is small. A provider can explicitly
index that intersection as one additional feature. The ordinary authenticated
index and finite query budgets then search the smaller list.

This changes discovery metadata, not mathematical identity or validity. A
candidate still needs normal structural resolution, mathematical verification
and applicability checks. A result containing two symbols need not apply to
your proof. Providers do not gain mathematical authority.

## Explicit adoption; no migration or silent fallback

Use the selected conjunction discovery and client successors together. Preserve
the current interface-only authoring, trust withdrawal and other selected source
overlays in the installed source map; do not replace them with old predecessors.

The new workspace schema is
`DMKN_V5_CLIENT_EVIDENCE_CONJUNCTION_WORKSPACE_V1`. It has exactly the existing
evidence-workspace configuration fields plus `discovery_profile`:

```python
{
    "schema": "DMKN_MODULE_EXPORT_PAIR_PROFILE_V1",
    "pairs": [[atomic_spec_a, atomic_spec_b]],
}
```

Configure 1–8 pairs. Every pair contains two distinct existing atomic feature
specifications, sorted by `formal_features.compact`; the pair list is similarly
sorted and has no duplicate pairs. The serialized profile is at most 8,192
bytes. Nested pairs and remotely supplied executable extractors are forbidden.
Malformed/noncanonical profiles refuse rather than being silently repaired.

The feature schema and profile enter the discovery namespace. Providers and
consumers must explicitly use the same profile to share that namespace. A new
profile requires a fresh index/workspace: reopening an old workspace with a
changed config refuses. Immutable historical snapshots retain their original
namespace. No query automatically crosses to an old namespace or another profile.

Legacy `DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1` accepts its original fields only;
its default namespace, records and query keys remain unchanged. Atomic/mixed
workspaces retain their existing configuration. Evidence, resilient, staged and
validated descendants inherit the new evidence profile through `Workspace.open`.

## Ordinary configuration and query example

Suppose an agent already knows the export identities of a shared `Tree` type
and its node constructor, but not the identity of a useful theorem about them.
These are formal vocabulary identities, not the sought theorem's identity.

```python
from discovery import formal_features as F
from client.workspace_validated import Workspace

tree = {"tag": "type-symbol", "symbol": {
    "kind": "export", "export_id": tree_export_id}}
node = {"tag": "type-symbol", "symbol": {
    "kind": "export", "export_id": node_export_id}}
profile = {"schema": "DMKN_MODULE_EXPORT_PAIR_PROFILE_V1",
           "pairs": [sorted([tree, node], key=F.compact)]}
config = {**ordinary_evidence_config,
          "schema": "DMKN_V5_CLIENT_EVIDENCE_CONJUNCTION_WORKSPACE_V1",
          "discovery_profile": profile}
workspace = Workspace.open(fresh_directory, config, create=True)
specs = [{"tag": "declaration-kind", "value": "theorem"}, tree, node]
route_features = workspace.adapter.compile_query(specs)
```

`ordinary_evidence_config` still contains the existing wire policy, envelope,
storage and operation limits. Close the workspace through its ordinary lifecycle.
Use the unchanged runtime/grant/issuer setup before making mathematical calls.
Persist this exact config and use `create=False` on ordinary restart.

Both `client.find(..., specs, ...)` and `direct_contacts.bind(client, ..., specs,
...)` compile through the workspace's adopted adapter. The public query remains
1–8 atomic specs. The compiler replaces only the first canonical configured pair
whose two atoms occur in the query, and keeps every other atom. It does not
greedily select multiple pairs or claim the chosen pair is globally optimal.
If no pair matches, it uses atomic keys in this SAME adopted namespace.

Location route plans must use subsets of `route_features` above, not keys from
the legacy free compiler or another workspace profile. Existing service entry
points open the configured evidence/staged/validated workspace; no new server
or transport is required. Direct contacts also require matching namespaces.
A mismatch, missing route, incomplete coverage or exhausted allowance does not
mean there is no mathematical result. Choose another explicit profile/operation
only through ordinary owner configuration; there is no automatic fallback.

## What improves, and what it costs

Extraction retains all atomic features and adds a pair key exactly when both
constituents occur. On correctly built snapshots, replacing those two query
atoms therefore preserves the candidate predicate. Membership authentication
alone does not prove correct extraction or global coverage; ordinary candidate
resolution recomputes the export record from its authenticated declaration.

For each selected provider/partition, the new scan driver is the minimum of the
chosen pair's intersection size and all remaining atomic list sizes. It cannot
exceed the previous minimum atomic-list size on the same corpus. It can stay
constant as unrelated records enlarge both atomic lists. It is NOT necessarily
the size of the full query intersection, and does not guarantee fast search
for unconfigured combinations or enormous matching sets.

Each export adds at most eight pair postings. Existing 128-feature, 16-KiB
record, storage and work limits remain: overflow refuses, never truncates.
Build/update work, storage, replication and retention can outweigh saved query
work, especially for rarely queried pairs. Configure only explicitly justified
pairs; do not enumerate all feature subsets. The same improvement belongs to an
equally optimized ordinary shared-library baseline, so it is not by itself
evidence of profitable certification or accelerated mathematical discovery.

The nine selected structural/inert controls passed once; see
`research/cycles/v5-2026-10-20/CONJUNCTION-OUTCOME.md`. They exercise real
Store/query and workspace persistence, with explicitly synthetic hot-list
records and inert client-call fixtures. This tested successor is not yet in
a new installed distribution and does not establish useful growth or final v5.
