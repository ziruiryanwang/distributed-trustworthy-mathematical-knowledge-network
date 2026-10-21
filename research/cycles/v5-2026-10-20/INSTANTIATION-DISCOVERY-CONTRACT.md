# Minimal conclusion-fingerprint contract

2026-10-20, core_growth. Source design only, not implementation or launch authority.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Basis: finalized `INSTANTIATION-DISCOVERY-SEAM.md` (`f5e68c211e14c808011f18e9527ce394465cba843c41c73ac084277d01d45ba5`)
and its independent review. Preserve all used sources. This is bounded candidate
filtering for raw syntactic instantiation, not unification or mathematical authority.

## Pure public surface

New logical module: `discovery/conclusion_fingerprint.py`.

```python
validate_fingerprint_profile(profile)  # fresh validated canonical profile
conclusion_spec(codec, owner_module_id, universes, declaration_type, profile)
goal_queries(codec, owner_module_id, universes, closed_goal, profile)
```

`conclusion_spec` returns one ordinary feature spec. `goal_queries` returns a
deterministically ordered list of 1..8 singleton spec lists: an OR of separately
funded ordinary queries, never one eight-conjunct query. No query argument is a
remote theorem identifier. The local owner_module_id only relocates its own
local symbol references. It must nevertheless identify the same symbols as the
candidate if the key-compatibility lemma is to apply.

An internal `_derive_conclusion(...) -> (spec, work)` may serve adapter extraction;
the public source helper returns its spec only. Reuse that same extraction
algorithm for indexing and public spec production; do not maintain two variants.
No I/O, model call, source execution, mutation of caller values or new cache.

## Explicit immutable profile and preallocation

Profile has exactly:

```json
{"schema":"DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_PROFILE_V1",
 "paths":[["arg"]]}
```

There are 1..3 paths, each a list of 0..12 edges. Empty path observes the root.
Edges are only `fn`, `arg`, `domain`, `body`, `type`, `value`, `struct`. Paths must
be distinct and already sorted by their compact JSON bytes; reject duplicate or
noncanonical order rather than silently changing a namespace. Return fresh lists.
Before serialization/copy, require exact dict/list/string types and bounded field,
path and edge counts; only then encode the at-most-36 fixed edge strings. Reject
unknown fields/schema. No generic recursive profile normalizer is needed.

For expression inputs, first bound owner_module_id to exactly 64 characters and
check its digest syntax; check the integer universe arity with the selected codec.
Then reuse unchanged `discovery.type_pattern._preflight` before whole-expression
serialization, deep copy or `codec.validate_expr(expr, universes)`. Its existing
limits are 1,000,000 JSON occurrences, depth256, list length256, scalar strings1024
characters, integers0..2^32-1, and estimated compact UTF-8 bytes <=16MiB-256.
Shared subtrees are charged per occurrence; cycles fail by bounded traversal.
Those preflight bounds do not replace codec syntax/scope validation. Reject bools,
foreign objects and malformed/oversized inputs; no truncation or partial keys.

## Exact observation and normalization

Validate the **whole** declaration type before stripping its leading `forall`
telescope; let its length be k and remaining conclusion be t. Source observation
starts at t with internal binder depth q=0. Goals are validated closed at term
depth zero and observed as supplied with k=0: never strip their leading forall.
Explicit universe parameters within the validated arity are allowed; dangling
term bvars are not. No open-context API or implicit wrapper is introduced.

Expression child slots are exactly the current adapter's semantic slots:

| Node | Valid edge and codec index | Depth change |
|---|---|---|
| app | fn=1, arg=2 | 0 |
| forall, lam | domain=2, body=3 | body only: +1 |
| let | type=1, value=2, body=3 | body only: +1 |
| proj | struct=3 | 0 |
| const, sort, bvar | none | 0 |

At every visited node, **before** looking for a child and at the final position,
if it is `bvar j` with q <= j < q+k return `["star"]` immediately for the entire
remaining path. A missing child at any other node returns `["absent"]`.
Otherwise the final token is:

- bvar j<q: `["local",j]`;
- constant: `["const",symbol]`, where symbol is the existing exact adapter form
  `{"kind":"foundation-name","name_hash":codec.hash_value("foundation-symbol",name)}`
  or `{"kind":"export","export_id":codec.export_id(module_id,name)}`;
- every other constructor: `["node",tag]`, tag one of sort/app/forall/lam/let/proj.

For constants, local references relocate to owner_module_id; external references
keep their own module/name. Omit constant universe arguments. Sort levels, binder
annotations and projection reference/index metadata are deliberately omitted.
Internal local indices are retained exactly. A bvar outside the two stated ranges
is an error, not STAR. Node position and child existence remain significant.

There is no beta/delta/iota/zeta/eta reduction, theorem transport, symbol-slot
renaming or definitional-equality normalization. Only the above observations and
exact local-reference relocation define the filter. Syntax-preserving universe
substitution does not alter its observations.

## Canonical feature encoding

Let validated P be the complete profile. Define:

```python
pid = codec.hash_value("conclusion-fingerprint-profile-v1", P)
value = codec.hash_value("conclusion-fingerprint-v1", {"profile_id": pid, "tokens": vector})
spec = {"tag": "conclusion-fingerprint", "profile_id": pid, "value": value}
key = existing_feature_id(namespace, spec)
```

Vectors follow P.paths order and have exactly its dimension. The existing final
feature hash binds the namespace; the namespace descriptor includes the complete
profile, foundation, policy and new feature schema. pid is explicit in each spec
so the active adapter can reject wrong-profile inputs, not merely silently miss.
Validate this new spec's exact three fields and 64-hex pid/value before hashing.
Never expose caller-supplied arbitrary token vectors as an indexing API.

For a closed goal vector v, enumerate masks0..2^d-1; bit i replaces v[i] by STAR.
Compute each spec, deduplicate by canonical spec bytes and return singleton lists
sorted by those bytes. No result-head, type-symbol, type-edge, declaration-kind or
other conjunct is added automatically. Caller-added constraints narrow coverage;
they are not covered by the default instantiation lemma.

## Exact successor map and integration

The basis is the adopted 111-entry `distribution-adaptive-01-input.json` map.
Create five fresh successors under `software/v5/instantiation_discovery/`, with
the same relative suffixes below, plus the new helper. Do not edit the listed
used predecessors. Old profiles remain byte/behavior-compatible in their modes.

| Logical SDK suffix | Current predecessor under software/v5/ | SHA-256 | Selected change |
|---|---|---|---|
| discovery/module_export_adapter.py | type_pattern/discovery/module_export_adapter.py | `336ae03bccbb5c700c36ab45f91235a23e27d15543f3eeddbb24d28c47f0f6ce` | New profile/tag branch, exact one posting, profile guard |
| discovery/formal_features.py | type_pattern/discovery/formal_features.py | `ae78289a5a49d6eec5b36dc929799e8cbd4beafa3c28b93bef4e10d0d09762ad` | Add feature-schema constant |
| discovery/authenticated_index.py | type_pattern/discovery/authenticated_index.py | `de29c02489dbac486b745662caf0ec2cd8d923a394aaf2728f9625c4fed3f05e` | Admit the new schema in existing snapshot descriptor validation |
| discovery/discovery_store.py | type_pattern/discovery/discovery_store.py | `2e7cae37ddec4dc6ec146acc7cfa89fff24e60f58dca08af900d0c3c626ed88c` | Admit new adapter schema; existing immutable persisted config |
| client/workspace_evidence.py | type_pattern/client/workspace_evidence.py | `051e130f12f5e6a640026a0ea34f7005192c15f3be2f5c3f667a4085687f95b9` | Explicit new workspace/profile branch before filesystem mutation |

New feature constant `EXPORT_CONCLUSION_FINGERPRINT_SCHEMA` has value
`DMKN_MODULE_EXPORT_CONCLUSION_FINGERPRINT_FEATURES_V1`. New workspace constant
`CONCLUSION_FINGERPRINT_SCHEMA` has value
`DMKN_V5_CLIENT_EVIDENCE_CONCLUSION_FINGERPRINT_WORKSPACE_V1`; its config requires
discovery_profile=P and otherwise retains ordinary evidence-workspace fields.
Old workspace modes refuse this profile, and the new mode refuses pair/pattern
profiles. Do not combine profiles in v1. Old adapter modes reject the new tag;
the new mode rejects whole-type-pattern tags and wrong pid values. Pair-profile
validation must reject both optional-profile tags. The adapter's immutable
profile binding includes its exact path/profile bytes, pid and mode flags.

On authenticated descriptor extraction add exactly one fingerprint spec, along
with inherited atomic features; retain the existing 128-feature cap. If adding
the required posting exceeds the cap, refuse the record, never omit the posting.
Charge preflight occurrence count plus telescope and observation visits in the
existing adapter work budget. After validation there are at most36 path edges
and3 final observations, plus k telescope visits; do not claim total O(36).

Unchanged dependencies include type_pattern.py (`b75277b55cdb25a22fbdc517bdc0bdf1173ced7c22c895fdc313a86f23857582`),
codec.py (`e01b7478640d72ad5e0634443c87d99a9bf91bc65d2fc2297355b92a27649f58`),
all direct/located adaptive helpers, transport, issuers and acceptance rules.
The future installed map would have112 entries: five replacements and one addition.
Documentation and focused controls are separate files, not additional SDK changes.

## Feeding the existing adaptive APIs

Create/open an explicitly matching fingerprint workspace. For each chosen
singleton query from `goal_queries`, compile through its actual adapter; direct
`next_query` or located `next_located_query` then uses its ordinary budgeted API.
Located routes use the compiled key as their query feature, never a raw vector.
The original envelope must prospectively fund whichever alternatives are chosen;
eight generated alternatives do not grant eight operations. Acquire desired
evidence/warrants before rotation because candidate/staging capabilities expire.
Locally choose order/early stopping; skipped alternatives are explicit incomplete
coverage. A new profile/namespace requires charged reindexing, not migration.

The key lemma remains only: for a closed, well-scoped raw capture-avoiding
instance g=sigma(t), the source key occurs in the generated goal-key family.
Hash-collision assumptions apply to encoded identities. Actual retrieval also
needs indexed reachable providers and enough funded work. It proves neither
applicability nor efficiency, and STAR-heavy buckets can be arbitrarily large.
