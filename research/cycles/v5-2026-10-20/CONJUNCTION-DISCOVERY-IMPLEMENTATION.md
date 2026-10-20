# Materialized formal pairs: selected discovery implementation

2026-10-20, `core_search`. Implements only the four discovery files selected in
CONJUNCTION-SELECTION. Source-only; no imports, tests, runtime/proof launches,
installation or Git actions. Used predecessors and installed release unchanged.

## Four selected source identities

Paths below are under `software/v5/conjunction_index/discovery/`.

| File | SHA-256 |
|---|---|
| formal_features.py | `3ae3fd9abb4e63124120c936f4b3805e7bcda9e95194497b2fe25b7e5e8623ba` |
| authenticated_index.py | `6c5ba1e563f26353b5d42da07558cb53a1a680e6258acc506291333bd3f17a20` |
| discovery_store.py | `c62f357d64ab52959e8d732d89dd8b92d434313a95cdec128f096235bb2c80c4` |
| module_export_adapter.py | `d1e8a437dec4ebe218ab1cc74e8e4bddd91ab4ade77f60e42dac9decb0d2c658` |

F adds only EXPORT_PAIR_SCHEMA; Store/authenticated_index add its explicit
allowlist/import, with storage, index, query and proof algorithms unchanged.
The adapter accepts keyword `discovery_profile=None`. The new profile schema is
DMKN_MODULE_EXPORT_PAIR_PROFILE_V1 with exact `schema,pairs` fields: 1..8 sorted
unique pairs, each two distinct existing atomic specs in canonical byte order,
8192-byte profile cap. Invalid/nested/noncanonical profiles refuse. No normalization
silently changes configuration. Namespace commits the profile and new schema.

Internals are immutable bytes, tuples and frozensets, copied from input. A saved
binding detects namespace/schema/profile/entry replacement before query or
extraction. Existing extraction runs once under the selected namespace; each
configured pair contributes three bounded work steps and at most one posting,
iff both ORIGINAL atomic keys occur. All atomic features remain; 128-feature,
16 KiB record and existing extraction-work caps refuse overflow. Described
atomic-pair specs are output metadata, not valid atomic query input.

`adapter.compile_query(specs)` accepts the unchanged 1..8 atomic specs, replacing
only the first canonical eligible pair. Every remaining atom stays, including
overlap endpoints. Legacy free compiler stays atomic-only; `pair_feature_id`
derives a pair key but does not adopt a profile. Resolver recomputes the complete
record. Default namespace, emitted records and empty pair loop retain old bytes.

## Independent review of adjacent client and selector changes

Narrow source PASS for growth's client successors: evidence workspace233562c6,
atomic workspaceeea95a6b, direct contacts88ce2581. Complete normalized-text
comparison against selected predecessors found only the expected differences:
profile validation before state creation, explicit new schema and persisted
profile, ordinary adapter selection/status, and two real compiler forwarders.
Existing publication still uses that same adapter/store. No admission, semantic
continuation, grant, acquisition or owner-flow change was found.

Root selector `Select-ConjunctionIndex.ps1` SHA
`f749eee1ec0994653fb65706b19484f23923fa5b01ce55354f90bed6fc8afff0`
pins basis64be70eb and rechecks its sources/runtime; requires exactly eight fresh
reviewed successors; refuses reused selection/output; selects only controls
under 60 CPU/90 wall seconds/512 MiB. It writes a selection, does not launch.
This is not a controls/runtime pass or final-v5 claim. Independent product review
and root's later exact selection remain required.
