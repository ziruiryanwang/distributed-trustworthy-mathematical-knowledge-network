# Type-pattern discovery: implementation checkpoint

Selected by TYPE-PATTERN-SELECTION; source only, not executed or adopted.
Fresh path: `software/v5/type_pattern/discovery/`. Frozen predecessors and the
installed candidate are unchanged. No import, test, proof, Git or runtime action.

## Implemented boundary

`pattern_spec(codec, owner_module_id, universes, type_expr)` constructs one
domain-separated whole-type key. Its optional profile is exactly
`{"schema":"DMKN_MODULE_EXPORT_TYPE_PATTERN_PROFILE_V1"}`.
Preflight counts repeated JSON occurrences, list/level/name structure and encoded
bytes before whole serialization; strict scalar bounds precede scalar encoding.
Cycles/shared DAG expansion meet finite bounds, not an object-identity cache.
Unchanged codec validation then checks scope, binder/universe/ref syntax.
One first-use symbol dictionary unifies local n with external(owner,n), including
references in projections. Foundation names and all other syntax stay exact.

Normalized references cannot enlarge the bounded input: the smallest valid
nonfoundation ref `["local",[["n",0]]]` is 19 bytes, while the largest possible
slot `["slot",999999]` is 15. Other syntax is unchanged. The 256-byte input
reserve exceeds the fixed `{universes,type}` wrapper; hash_value additionally
enforces the existing canonical 16 MiB limit. No unbounded normalized encoding.

The adapter adds one key only in the new namespace/profile and retains all
ordinary atomic features. Default/pair descriptor construction and valid output
logic remain unchanged; old modes reject pattern queries and pair atoms.
MAX_FEATURES remains 128 with explicit overflow refusal. The only remaining
changes here are the new schema constant and snapshot/store schema allowlists.
No receiver, transport, proof, semantic environment or existing record changes.

Workspace/configuration and README are independently owned by core_growth;
controls and source review by core_release. Root owns later source-map selection,
finite execution and adoption. Review can still require repairs before freezing.

## SHA-256 at this checkpoint

- type_pattern.py: `b75277b55cdb25a22fbdc517bdc0bdf1173ced7c22c895fdc313a86f23857582`
- module_export_adapter.py: `336ae03bccbb5c700c36ab45f91235a23e27d15543f3eeddbb24d28c47f0f6ce`
- formal_features.py: `ae78289a5a49d6eec5b36dc929799e8cbd4beafa3c28b93bef4e10d0d09762ad`
- authenticated_index.py: `de29c02489dbac486b745662caf0ec2cd8d923a394aaf2728f9625c4fed3f05e`
- discovery_store.py: `2e7cae37ddec4dc6ec146acc7cfa89fff24e60f58dca08af900d0c3c626ed88c`

No runtime outcome is claimed. Intended payoff is more discriminating discovery
from independently known local signatures; same-pattern hot buckets and semantic
generalization remain outside this change. Reindexing a separate namespace has
full inherited-posting cost, not only the new per-declaration posting.
