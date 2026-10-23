# Ordinary type-preview implementation checkpoint

2026-10-22. Owner: `admission_event_audit`. Source-only selection from root.
Implemented only `software/v5/ordinary_lean/ordinary_preview.py`; no tests,
runtime, Git changes, frozen-source edits, index-engine edits or admission.

Source SHA-256:
`0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6`.

## Small public API

```text
preview_from_evidence(Evidence | bytes, export_name, limits=DEFAULT_LIMITS) -> bytes
read_preview(canonical_preview_bytes, limits=DEFAULT_LIMITS) -> Preview
describe(canonical_preview_bytes, limits=DEFAULT_LIMITS) -> metadata
resolve(canonical_preview_bytes, Evidence | bytes, limits=DEFAULT_LIMITS) -> metadata
```

`preview_from_evidence` uses the exact unit's selected expected inventory row.
It emits the six-field preview specified in `ORDINARY-DISCOVERY-SEAM.md`:
schema, profile ID, unit ID, export name, header `[kind, levelParams, typeDAG]`,
and sorted exact type bindings. It does not emit the declaration's proof/value
body, other inventory rows, unrelated imports, owner paths or executable metadata.
Terms genuinely present inside the mathematical type are preserved, not erased.

`Evidence.document`, `.unit_id` and `.census` are never treated as trustworthy
cached fields: both extraction and resolution reread immutable `Evidence.raw`
through the existing `read_evidence`. Raw-byte input avoids forcing callers to
parse twice before this boundary. For resolution the exact domain-separated
UnitID is checked before parsing the acquired evidence.

## Reused grammar and exact reference rule

The module reuses `ordinary_evidence`'s canonical JSON reader, name/ID/parameter
checks and `_dag_references` expression validator. Its reliance on those private
helpers is explicit internal coupling; later source selection must pin the
compatible module set. No new general expression parser or kernel is introduced.

The additional traversal only marks reachable expression and universe indices.
It rejects orphan nodes, preserving the invariant that the reused all-node
reference census equals the root-reachable type census. Every node is processed
once in this reachability pass; shared DAGs are not expanded into trees. Native
Nat/String leaves and projection-structure references are supported. Binder and
level-parameter names do not become semantic symbol references.

For each type reference, an own-unit member uses
`export_id(profile_id, unit_id, member_name)`; an external reference uses its
exact evidence import binding. No basis-name hash or spelling-only identity is
invented. Binding names must equal the sorted unique type reference keys exactly.
Standalone preview validation does not establish that claimed symbol IDs are
true; `resolve` recomputes all bindings and the full header from exact evidence
and requires byte-for-byte preview equality.

## Limits and assurance

Default preview profile: 1 MiB canonical bytes; at most 65536 combined type DAG
nodes, including at most 8192 universe nodes; 4096 type bindings; 256 name parts
and universe parameters; 65536-byte names/literals. Existing lexical depth,
integer, closed-root scope and backward-edge checks apply. The separate evidence
reader retains its unchanged 8 MiB and other defaults. Limits are trusted local
configuration, never obtained from the preview.

`describe` returns `mathematical_acceptance: false` and
`ADVERTISED_TYPE_PREVIEW_NOT_EVIDENCE_BOUND`. It intentionally does **not** claim
an authenticated index commitment: this module has not inspected any index.

`resolve` returns `mathematical_acceptance: false` and
`EXACT_EVIDENCE_HEADER_BOUND_NOT_MATHEMATICAL_ACCEPTANCE`. Successful resolution
means only that these exact inert bytes carry the advertised header and bound
IDs. Warranted dependency matching, native checking, generated-inventory equality
and protected promotion remain required. `Preview.document` is mutable parsed
data; public describe/resolve entry points consume raw bytes and reparse them.

The raw wire format has no acceptance flag; fake extra fields are refused.
Operational metadata carries the explicit false value outside that wire format.
Neither shape validation nor evidence binding establishes the declaration's
existence in an accepted library, proof validity or provider coverage.

## Next integration boundary

Independent source review and one root-selected changed-boundary check remain.
Useful discriminators are wrong unit/profile/header/binding, mutated cached
Evidence fields, own-unit inductive-member references, shared DAGs and literal
leaves, orphan nodes, exact profile bounds, and explicit false acceptance.

The later coherent index adapter should reuse these APIs and the existing engine
with its separately selected ordinary schema seam. No fake certified locator or
new index data structure is needed. Preview/evidence acquisition still requires
parent-operation aggregate budgets; these parsers do not bound an unbounded
network download or reset any candidate allowance. This component is not yet
executed or integrated and is not a discovery/growth/v5 result.
