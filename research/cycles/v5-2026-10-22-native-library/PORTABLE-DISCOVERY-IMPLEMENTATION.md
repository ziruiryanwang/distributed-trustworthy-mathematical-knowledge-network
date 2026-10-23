# Portable ordinary discovery adapter

2026-10-23. Root-selected source-only implementation. No tests, runtime, network,
catalog operation, migration, Git mutation or mathematical acceptance performed.
Frozen experiments and all ordinary V1 helpers remain unchanged.

## User path and minimal change

An agent should query known formal meanings, inspect an unfamiliar method's type,
and acquire the selected result without already knowing its ID. Reuse the existing
authenticated posting lists, candidate queries, sessions and transport. Add only
the portable ordinary metadata adapter and three schema-aware development changes:

- `software/v5/discovery/ordinary_export_adapter.py`: new adapter.
- `formal_features.py`: distinct V3 record branch/domain and strict locator checks.
- `discovery_store.py`: allow the ordinary feature schema.
- `authenticated_index.py`: allow the same schema in snapshot descriptors.

No new search engine, acceptance mode, proof production or global corpus scan is
introduced. Existing old record schemas, feature domains, snapshot encoding,
default store behavior and valid-input behavior are retained.

## Schema and API

```text
feature schema: DMKN_ORDINARY_LEAN_EXPORT_FEATURES_V1
record schema:  DMKN_FORMAL_FEATURE_RECORD_V3
record kind:    ordinary-lean-export-v2
record domain:  DMKN-FORMAL-FEATURE-RECORD-V3
feature domain: DMKN-ORDINARY-LEAN-EXPORT-FEATURE-V1
```

The record has the existing exact base fields plus the portable V2 locator:

```text
{schema, namespace, kind, object_id: ExportID,
 object_sha256: SHA256(exactPreviewBytes), object_bytes,
 features: sortedUniqueFeatureIDs,
 locator: {schema: DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2,
           semantic_id: S, unit_id: UnitID, export_name}}
```

`namespace_for(S)` commits to S, the exact preview/evidence/unit/expression formats,
feature schema/revision, syntactic normalization policy and eight-bit partition
profile. S already commits to F. Local I, context roots, providers and paths do
not enter this namespace. New records must have the exact namespace derived from
their locator's S and the exact ExportID derived from S/UnitID/name. Native names
are validated by `portable_preview.read_locator`, not a new name parser.

Public surface:

```text
OrdinaryExportAdapter(semantic_id, *, limits=None)
  .namespace, .feature_schema
  .describe(previewBytes, expected_id=None)
  .extract(previewBytes, expected_id=None)
  .resolve(record, previewBytes)

namespace_for(semantic_id)
feature_id(namespace, spec)
compile_query(namespace, specs)  # one to eight conjuncts
```

`limits=None` uses the existing portable preview limits. This concrete adapter
recognizes only the current selected S; constructing it with an unsupported S
refuses. Generic record parsing remains advertisement validation, not semantic
adoption. All methods returning descriptions/resolution explicitly deny
mathematical acceptance.

The ordinary helpers are imported only when constructing the new adapter or
validating a V3 record. Loading/using old valid V1/V2 discovery paths does not
require ordinary modules. A coherent new assembly must make the selected
`ordinary_evidence`, `ordinary_preview`, `ordinary_semantics`, `portable_evidence`
and `portable_preview` modules available, along with these four discovery files.
There is no implicit `sys.path` mutation or loading of peer-specified code.

## Initial feature profile and cost argument

The minimal features are object kind; declaration kind; every exact bound type
symbol; result head; and leading-universal-binder domain heads. A symbol has
`{kind: portable-symbol, symbol_id}`. Constant/projection heads include that exact
symbol. Other heads are syntactic tags, including native Nat/String literals.
No implicit type-symbol for literals is invented. There are no proof-import,
name-spelling, type-edge, learned-ranking or logical-equivalence features in this
first slice. Let reduction and definitional conversion are not performed.

The existing preview reader establishes bounded closed/root-reachable DAG syntax
and the exact type-binding census. The adapter emits type-symbol features directly
from that census. For backward-indexed expression node i, define:

```text
spine[i] = spine[functionChild(i)]  if i is an application
           i                     otherwise
```

Every entry is computed once in serialized order. Terminal head descriptors are
also memoized, including exact name-to-symbol lookup. Following leading forall
bodies visits a decreasing sequence of DAG indices. Thus extraction does not
expand shared terms or repeatedly walk shared application prefixes: its graph
work is O(type-DAG nodes + bindings + leading binders), with bounded encoded-name
processing and feature hashing. `work` reports adapter feature/traversal steps,
not all parser instructions or wall/CPU cost.

More than128distinct features causes explicit
`ORDINARY_FEATURE_PROFILE_EXHAUSTED`; no feature is silently dropped. Existing
16KiB record and finite preview limits also remain. An indexing-profile refusal
does not reject the mathematics. The global corpus size and imported proof
ancestry do not enter this extraction cost. Posting-list size/selectivity and
provider coverage remain separate search limitations; this is not a claim of
logarithmic semantic search or worldwide completeness.

An unknown-ID query can conjunct theorem-kind and the known portable symbols for
`Std.ExtHashMap` and `insertMany`, optionally a known result head. No unfamiliar
method name, UnitID or ExportID is required. Whether that query is selective enough
in a real corpus remains to be justified; source compatibility is not a growth
or retrieval-quality result.

## Distinct assurance boundaries

1. Authenticated index membership commits a provider's selected **record**.
2. Adapter `resolve(record, previewBytes)` recomputes the entire record, features,
   exact preview hash/size and locator from the raw preview. It binds only those
   bytes, not the underlying evidence or mathematical truth.
3. `portable_preview.resolve(previewBytes, evidenceBytes)` binds the selected type
   and type-symbol bindings to exact inert evidence, still not acceptance.
4. The protected controller resolves permitted S/F and eligible exact imports,
   independently checks all new units and commits actual checked mathematics.

No earlier success substitutes for a later gate. The adapter does not claim index
membership itself; `resolve` uses assurance
`EXACT_PREVIEW_RECORD_BOUND_NOT_EVIDENCE_OR_MATHEMATICAL_ACCEPTANCE` and directs the
caller to acquire exact portable evidence. Two conflicting previews may claim
the same ExportID but have distinct record hashes. Existing stores continue
refusing a same-object conflicting record rather than silently rewriting a
snapshot; clients do not acquire a first-provider mathematical authority.

## Evidence status and next step

This implementation is unexecuted. Root reports that the preceding **separate**
portable identity/preview controls02 passed15groups under selection `2fd4f2db`;
that does not test this new adapter or the three new schema branches. Root owns
later source review and focused integration selection. No broad tests are
authored by this assignment. Next useful evidence is one bounded real
unknown-ID query, exact preview binding and continued ordinary reuse—not another
kernel/basis/certificate campaign or a second index implementation.
