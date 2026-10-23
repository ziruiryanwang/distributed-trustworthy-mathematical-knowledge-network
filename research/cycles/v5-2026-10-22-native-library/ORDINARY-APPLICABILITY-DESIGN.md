# Discover an unfamiliar vocabulary, then search its methods

2026-10-23. Current source-only design by `portable_integration_audit`, revised
after root and `ordinary_api_flow` challenge. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root's [source selection](ORDINARY-BODY-DISCOVERY-SELECTION.md) authorizes the
new adapter, not execution. No runtime was performed by this author.

## Decision and workflow

Use two stages rather than a new normalization engine:

1. Search transparent **definition bodies** from an independently supplied local
   formal property. This can discover an unfamiliar mathematical vocabulary.
2. Use its now legitimately learned exact ExportID in the existing type-symbol
   search to discover methods using that vocabulary.

For the actual example the consumer already has `hf : ∀x, P x → P (f x)`.
Stage 1 searches this property and may find the remote definition
`Stable f P := ∀x, P x → P (f x)`. Stage 2 searches Stable's exact learned
symbol and may find `stable_compose`. Neither Stable's name/ID nor its theorem's
ID is a stage-1 input. The local property must be selected before reading remote
candidates. No human-intention interface or global mathematical task list is needed.

The [prior reducer proposal](ORDINARY-APPLICABILITY-REDUCER-DEFERRED.md) is
deferred before implementation. No beta/delta/iota/zeta/eta reduction, universe
instantiation, recursive unfolding or general shape engine is needed here.

## Reuse and smallest implementation delta

Existing `type_pattern/discovery/type_pattern.py` already supplies bounded
whole-type private-symbol blinding and first-occurrence equality patterns.
That bijective-renaming relation misses arbitrary substitution, including
specializing two parameters to one term or a parameter to a lambda.

Existing `instantiation_discovery/discovery/conclusion_fingerprint.py` supplies
the appropriate weaker mechanism: observe 1–3 paths; source parameters give
STAR; an explicitly closed local goal gives at most eight separately funded
query alternatives. It distinguishes local-context variables from internal
binders. The new adapter ports that observer to the ordinary V2 DAG directly,
strips source **lambdas** rather than foralls, and binds exact full definition
evidence. Old source bytes/identities are not relabeled as ordinary V2.

The fixed new profile is:

```json
{
  "schema":"DMKN_ORDINARY_DEFINITION_BODY_PROFILE_V1",
  "paths":[
    ["body","body","arg","arg"],
    ["body","body","arg"],
    ["body","domain","arg"]
  ]
}
```

Path ordering is canonical compact-JSON ordering. V1 fixes this profile rather
than introducing a configurable extractor registry. Namespace binds S (which
already binds foundation F), profile ID, expression/evidence formats, feature
revision and record schema. It contains no local root or ImplementationID.
Limits can refuse a source; they never produce a partial or different key.

Root's additive branches use
`DMKN_ORDINARY_LEAN_DEFINITION_BODY_FEATURES_V1` and
`DMKN_FORMAL_FEATURE_RECORD_V4`. The new kind is
`ordinary-lean-definition-body-v1`. The generic fields and existing ordinary
locator remain. Object ID is the original ExportID; payload hash/length describe
the **complete evidence unit**, not a type preview. One definition emits one
namespaced `definition-body-fingerprint` key (profile ID plus observation hash).
No new mathematical identity, wire object, package or certificate is introduced.

## Source binding and public API

Source input is exact bounded portable V2 evidence. Reuse the selected reader
and S. Require descriptor kind 0, one inventory row of kind 1, and equality of
name, universe parameters, type DAG, value DAG, reducibility hint and all_names.
Require all_names to be exactly the singleton own name. Descriptor value is
`unit[1][4]`; inventory value is `unit[2][0][4][0]`. This prevents a source-bound
hint from silently selecting a different advertised body. Imported constants
resolve to declared exact portable symbols; the self name resolves to its exact
ExportID. No imported body is fetched or unfolded. Theorem/opaque/generated-group
body indexing is outside this V1 subset.

```text
OrdinaryBodyAdapter(semantic_id, *, limits=None)
describe(raw_evidence, expected_id=None)
extract(raw_evidence, expected_id=None)
resolve(record, raw_evidence)
compile_query(specs)                         # one fingerprint spec only
goal_queries(*, expression, universe_params, bindings, context_binders=0)
```

The query expression is a complete ordinary DAG for `forall Γ, property`.
Universe parameter names and exact sorted name→portable-symbol bindings are
explicit; their census must equal the expression's referenced constants. The
query's local context is syntactically closed, not asserted kernel-checked.

Candidate resolution must use the existing exact **evidence** acquisition route,
then recompute the entire record. `OrdinaryAcquisition.preview` assumes the old
V3/type-preview namespace and must not receive this body record. After learning
and admitting the desired definition, stage 2 uses the unchanged type-preview
and exact-symbol search interfaces. The body resolver itself grants no authority.

## Precise observer and nonexpanding resource contract

Strip exactly the source body's leading lambda prefix, counting k. Retain its
forall binders. Observe each fixed path from that body with internal depth q=0.
For a source bound-variable index i encountered anywhere along the path:

- `i<q`: an internal variable; final token is `LOCAL(i)`, otherwise a missing
  child gives ABSENT.
- `q<=i<q+k`: return STAR **before** checking any further path edge, because
  raw substitution can introduce children beneath a parameter.
- Otherwise refuse invalid scope.

For a query, validate its whole closed wrapper and strip exactly the explicit
context_binders count, each of which must be forall. Retain property-internal
quantifiers. Internal variables use the same rule. Γ variables yield CONTEXT
at a final position and ABSENT below them. Convert final CONTEXT to mandatory
STAR; enumerate keep-or-STAR for every other coordinate, deduplicating at most
eight alternatives. Return fewest-STAR alternatives first, then canonical spec
bytes as a deterministic tie-break. Alternatives are independent queries, not
one conjunction or an automatic broadcast. Generating them authorizes no network
work; the all-STAR fallback may have an enormous posting population.

Constants give exact portable-symbol tokens; other constructors give node tags.
The hint omits universes, literal values, binder names/info and projection
metadata, not their underlying evidence. Missing edges give ABSENT. Only entering
`body` of forall/lambda/let increments q. Ordinary array slots are app fn=1/arg=2;
lambda/forall domain=3/body=4; let type=2/value=3/body=4; projection struct=3.
Do not memoize observations by DAG node alone: the same node can occur at
different binder depths. The implementation simply walks the three short paths.

Complete query-input preflight runs **before** encoding or ordinary validators.
It iteratively bounds container/value occurrences, JSON byte size and depth;
strings and integers are bounded before scalar encoding. Shared Python objects
count at every supplied occurrence; cycles hit depth. Only ordinary literal
`$bytes` dictionaries are permitted. Then ordinary syntax/scope/name/universe
validation and exact binding-census checks run. No source or query is expanded
from a DAG into a tree.

For B bytes, n reader-validated nodes, k stripped lambdas and path lengths l_j,
the extra structural observations are `k+sum_j(l_j+1)`, with the sum here at
most 13. Query alternatives copy at most 24 tokens plus bounded tiny hashes.
Full input parsing, name processing, hashing and proof/index work remain charged;
this is not a wall-time SLA. The explicit default evidence Limits are 1 MiB,
32,768 expression nodes/8,192 level nodes per DAG, 256 DAG depth, 128 universe
parameters, 131,072 total unit nodes, one inventory row, 128 name parts/16 KiB
name bytes, 64 KiB literal bytes and 8,192 imports. Only componentwise tighter
trusted caller limits are accepted. Codec fields not changing feature semantics
still refuse on exhaustion; default 8 MiB ordinary evidence bounds are not
silently inherited for this search lane.
Exhaustion refuses before feature emission: **no CUT keys** and no
availability-dependent prefix keys. No external acquisition occurs inside
extraction. Diagnostics expose observations, source_lambdas, body_nodes,
path_visits, total_unit_nodes and the structural work sum, not a CPU cost estimate.

## Exact current property and the recall statement

After stripping `λ α f P`, the source is
`forall x : α, forall h : P x, P (f x)`. The configured paths observe:

| Path | Token | Reason |
|---|---|---|
| body/body/arg/arg | LOCAL(1) | x lies beneath both the x and h binders. |
| body/body/arg | NODE(app) | The conclusion argument is raw f x. |
| body/domain/arg | LOCAL(0) | Premise P x lies beneath x but outside h. |

The independently supplied property from hf yields this vector. The weaker
`∀x, P x→P x` gives ABSENT and LOCAL(1) in the first two coordinates, so it
does not share the exact key. Paths of length four are intentional; the earlier
depth-three proposal did not establish this distinction.

Parameter sharing is not proved: `∀x,P x→Q(f x)` may collide. Inspect and admit
the actual chosen definition. Nor are separately quantified x variables in
different subterms a single shared role inferred from their display name.

Under supported bounds, exact rigid identities and hash assumptions, a
well-scoped raw capture-avoiding instance of the stripped body yields query
alternatives including the source key. A path either reaches a substituted
parameter (STAR), or remains in unchanged syntax/binding; the existing optional
and context STAR cases cover both. This is syntactic candidate recall, not
proof that an instantiation exists, meets dependent types, discharges premises
or yields a true theorem. For example, substituting a lambda for f produces a
raw beta redex, not automatically the normalized property `P(f(g x))`.
Use actual hf as the stage-1 discriminator, not a hidden normalized equivalent.

## Assurance, cost and next check

Posting authentication means membership in one finite committed index. Exact
evidence reconstruction means correct source-bound hints. Only ordinary admission
and checked downstream application confer mathematical authority. A learned
ranker may order candidates; popularity or rank never substitutes for checking.

The scan driver is the charged stage-1 body bucket plus stage-2 exact-symbol
postings across the selected providers/partitions. Both queries, failed
candidates, exact evidence transfer and provider/index maintenance count.
Common-body/wildcard buckets and popular-symbol buckets can still be huge.
There is no universal sublinear search, mathematical-equivalence oracle or
global completeness. The [whole-cost note](ORDINARY-PRACTICAL-COST.md) supplies
the strong-comparator benefit condition; this change must improve it honestly.

The selected source is `software/v5/discovery/ordinary_body_adapter.py`, SHA256
`310980b1dab7339c68e4262c02bcff28b81cf61c08bf7c82c54b31966a4aaf32` at this author
checkpoint. Root owns additive generic index/schema branches. Independent source
review and separately authored controls remain in progress; no execution pass
is claimed. The next finite check should use actual retained Stable evidence,
an independently authored premise query, diverse decoys plus genuine collisions,
and stage-2 search using only the learned ID. Existing native/catalog campaigns
need no repetition for this metadata seam. Stop if selectivity/cost is unhelpful;
do not grow another normalization engine by inertia.
