# Ordinary Lean discovery: smallest coherent seam

2026-10-22. `ordinary_payoff_audit`. Source/theory only; no runtime, tests,
builds, Git mutation or discovery implementation. Root owns subsequent exact
fresh-source selection. Canonical root only.

## Decision

Reuse the current authenticated posting/query engine, bounded search sessions,
partition planning and provider-selected coverage. Add an ordinary-declaration
adapter and three small coherent schema extensions. Do not redesign the index,
build another DHT, require cryptographic theorem certificates, or index proofs.

Use **bounded advertised-type previews** for search. Their index commitments
authenticate what a provider advertised, not whether that type actually belongs
to the advertised mathematical object. After selecting a candidate, acquire its
exact inert unit, bind the preview to that unit's expected header, and check the
missing extension against warranted local dependencies. This explicit preview
assurance is sufficient for safe discovery and avoids a new Merkle-opening
protocol or downloading every candidate's full proof before choosing it.

No mathematical trust is relaxed. A misleading but committed preview can waste
bounded search effort; it cannot become an accepted declaration. The existing
coverage language already concerns committed metadata, not complete mathematics.

## Actual reusable code and mandatory changes

Paths below are relative to `software/v5/discovery/`. Existing used sources
remain frozen; a later root selection must identify fresh successor files or a
fresh coherent module set, not silently change a previously qualified install.

| File/seam | Decision |
|---|---|
| New `ordinary_export_adapter.py` | Ordinary preview shape, original-expression DAG traversal, environment-locked feature extraction, query compilation and inert evidence locator. No proof checker or network authority. |
| `formal_features.py:142-177` | Add explicit ordinary feature/record schema constants, strict new locator validation, and a new record-ID hash domain. Preserve old shapes/domains unchanged. |
| `discovery_store.py:59-60` | Permit the ordinary feature schema. Existing adapter extraction, byte/hash binding, atomic admission and posting machinery remain reusable. |
| `authenticated_index.py:366-381` | Permit that same ordinary schema in snapshot validation; preserve snapshot format, Merkle algorithms and coverage claim. |
| `candidate_query.py`, `discovery_query.py` | Reuse unchanged: they call shared record/snapshot validators and operate on feature IDs, hashes, ordinal ranges and budgets. |
| `search_session.py` | Reuse unchanged for index requests: aggregate reservations, failure charging, duplicate/alternative-metadata handling, unknown-SID offers and coverage are already implemented. |
| `summary_wire.py` | Reuse unchanged; its header/expanded validation delegates to the same snapshot/query boundary. |
| `module_export_adapter.py` | Keep unchanged for its existing restricted certified-module format. Do not relabel an ordinary unit as one of its certified module openings. |

Thus the minimal discovery logic selection is **one new adapter plus three
schema-aware successors**, with the unchanged engine dependencies loaded from
that coherent successor module set. Python relative imports must not accidentally
resolve the old `formal_features` during a new ordinary call. An isolated module
assembly can reuse unchanged file bytes; no alternate tree algorithm is needed.

The ordinary evidence envelope and protected controller bindings below are
necessary integration interfaces, not additional index-engine mechanisms. They
must be owned by the ordinary admission/export integration rather than invented
as a second mathematical authority inside the search adapter.

## Identity: exact meanings without hashing the entire local environment

`OriginalDecl.lean:352-386` currently defines an inert unit as
`[unitFormat, descriptor, expectedInventory]`. It has no profile/dependency
identity wrapper yet. Names alone cannot provide cross-environment semantic
identity. The controller/exporter should bind an immutable evidence envelope:

```text
OrdinaryEvidence := {
  schema,
  profile_id,
  imports: sorted [(ordinary_name, external_symbol_id)],
  unit: OriginalDecl unit
}

UnitID := H("DMKN-ORDINARY-EVIDENCE-V1", canonical(OrdinaryEvidence))
ExportID := H("DMKN-ORDINARY-EXPORT-V1", [profile_id, UnitID, ordinary_name])
```

Here the adopted profile fixes the kernel/basis/axiom policy and expression and
declaration interpretation. `imports` binds the direct external semantic
references of the unit, not every declaration installed on the contributor's
machine. It contains exact distinct names, in deterministic order, with no
unbound or silently unused entry. The original unit retains native names and
its exact mdata-erased ordinary projection. Hashes do not establish validity.

The direct-reference census includes descriptor types and bodies and the needed
generated records/rules. References to members of the same generated group are
internal, not recursive hash imports. The complete expected output census fixes
that local group. The actual checked output must later equal it. No new name is
allowed to overwrite a parent binding.

For ordinary nonbasis declarations, `external_symbol_id` is the referenced
`ExportID`. For a selected basis declaration, use a distinct tagged identity
binding the exact accepted basis ID, profile and native name. The basis's known
normalization correspondence must remain the one established by the ordinary
controller; indexing does not establish it. A basis-name hash with no basis
binding is insufficient.

Consequences:

- Adding unrelated knowledge to a local environment does not rename old symbols.
- Same spelling with different checked unit, profile or dependency meaning gives
  different symbol IDs. Search does not silently conflate the two.
- A different proof or API metadata may yield a different conservative unit ID.
  Quotienting those identities by theorem equivalence is not required here.
- Mutual/inductive groups have one unit ID and member-specific export IDs; no
  cyclic definition of each member's own hash is necessary.
- The initial implementation may hash more metadata than mathematical meaning
  strictly requires. That can reduce deduplication, not justify unsound merging.

The required cryptographic assumption is collision resistance for content and
index binding, not succinct proof soundness. Mathematical soundness comes from
the protected ordinary acceptance path.

## Preview and record contract

Proposed new names are intentionally distinct from the existing module format:

```text
feature_schema = DMKN_ORDINARY_LEAN_TYPE_FEATURES_V1
record_schema  = DMKN_ORDINARY_LEAN_FEATURE_RECORD_V1
preview_schema = DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V1
locator_schema = DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V1
```

A preview contains:

```text
{
  schema: preview_schema,
  profile_id,
  unit_id,
  export_name,
  header: [declaration_kind, original_level_params, original_type_DAG],
  type_bindings: sorted [(referenced_native_name, exact_symbol_id)]
}
```

It deliberately does not contain the proof, full imported closure, owner file
paths, provider URL, executable metadata, or a `verified` flag. Its native names,
levels and DAG use the selected ordinary codec format, not the old relocated
syntax. `type_bindings` covers exactly constants and projection-structure names
reachable in this type; binder names are not symbols. A type reference to a
member of its own unit uses that unit's computed member export ID.

The generated record retains the engine's normal fields:

```text
{schema, namespace, kind: "ordinary-lean-export-v1", object_id: ExportID,
 object_sha256: SHA256(previewBytes), object_bytes: len(previewBytes),
 features: sortedUniqueFeatureIDs,
 locator: {schema: locator_schema, profile_id, unit_id, export_name}}
```

`object_id` denotes the intended export; `object_sha256` binds this exact preview.
Multiple different previews claiming one export can therefore have different
RecordIDs. `SearchSession._prepare_candidates` already preserves alternative
metadata and does not grant the first provider authority. A single provider's
immutable store rejects same-ID conflicting records (`OBJECT_RECORD_CONFLICT`);
it must not silently overwrite old snapshots. Corrected advertisements can use
another independently selected index snapshot/store policy later. This is not
a reason to make the first-seen preview authoritative at clients.

Strict new-record validation must check exact keys, schema/kind pair, bounded
original name shape, profile/unit IDs, object-ID derivation and existing sorted
feature/record-byte bounds. The record hash uses a new domain; the old two record
domains remain byte-for-byte unchanged. No generic arbitrary-locator dictionary
or permissive fallback is needed.

The preview parser is a bounded metadata parser, not a second Lean kernel.
Start with a selected finite raw-byte/type-node/name/literal/work envelope,
require canonical JSON, closed-root syntactic scope and backward DAG references,
and traverse each reachable node once. Preserve sharing. Existing index limits
of 128 features, 16 KiB records and at most eight query conjuncts remain adequate
mechanism bounds; exceeding them gives an explicit indexing-profile refusal,
not mathematical invalidity or silent truncation. The larger ordinary acceptance
codec may accept declarations outside this initial search profile.

Because the source arrays contain integers and bounded UTF-8 name bytes, the
controller can parse the Lean-produced structured unit and hash one specified
canonical JSON byte encoding. Do not require the runtime's pretty printer and
Python JSON encoder to coincidentally emit identical text. The unit's existing
encode/decode projection checks remain separate from byte canonicalization.

## Minimal features and unknown-ID query

The namespace commits to `{profile_id, ordinary unit/expr formats, normalization,
feature_schema, feature extraction revision, partition_bits: 8}`. It must not
include one changing local accepted root or a provider ID.

The first feature set can use the existing kinds of structure:

- object kind and declaration kind;
- exact bound type symbols;
- result head after leading universal binders and application peeling;
- binder-domain heads;
- supported structural type edges, if the same bounded traversal extracts them.

The adapter owns its feature-ID domain and tagged symbol format. Native Nat and
String literals are supported DAG leaves, not grounds for rejecting an otherwise
valid ordinary type. If literal-kind features are included, give them an explicit
schema entry. Do not invent an implicit constant reference that the type did not
contain, or claim features prove arbitrary semantic equivalence.

For the chosen workload B already knows its local `Std.ExtHashMap` and
`Std.ExtHashMap.insertMany` meanings. A query can conjunct those exact two symbol
IDs with theorem kind (and optionally the known `Eq` result head). A's general
footprint theorem has all of these in its type: its observation parameter has
domain `ExtHashMap`, and its equality compares applications across `insertMany`.
The query contains neither A's namespace/name, its ExportID, its UnitID, nor its
unfamiliar `ReadsOnly`/`Avoids` symbols.

This is a real unknown-ID search specification. It does not guarantee A is the
first match in a large corpus. The returned proposition and assumptions must be
inspected, and broader plans may need more selective structure or local ranking.
A fixture containing just A is compatibility evidence, not evidence of broad
recall, selective hot-key performance or a search advantage over an optimized
ordinary library. No new learned ranker is justified by this source seam alone.

## Resolution and mathematical acceptance state machine

`describe(preview)` computes metadata and declares `mathematical_acceptance=false`.
`resolve(record, preview)` checks the exact preview hash/size, namespace/profile,
derived export identity and recomputed feature record. Its result is:

```text
assurance = COMMITTED_ADVERTISED_TYPE_PREVIEW
mathematical_acceptance = false
next_gate = ACQUIRE_AND_CHECK_ORDINARY_EXTENSION
locator = {profile_id, unit_id, export_name}
```

This is a new resolver, not replacing the certificate-only output in the old
certified adapter. It makes no claim that a unit exists or matches the preview.

The protected controller then:

1. Acquires bounded inert evidence matching the exact UnitID, never a peer binary.
2. Checks the profile and complete direct dependency identities. Any accepted
   local reuse comes from protected warranted bindings, not matching names alone.
3. Compares the selected expected-inventory header and its derived type-symbol
   bindings with the advertised preview. A mismatch refuses this claim before
   spending kernel-check work where possible.
4. Independently checks each missing unit and compares actual generated records
   with the expected inventory, under the already selected admission rules.
5. Only then commits the accepted local root and permits checked owner-project
   rebinding. Old accepted mathematics can be reused; stale operational grants
   cannot. Strict ancestry-free requests still need their own applicable evidence.

An index cannot call `checkBatch` with a caller-invented parent and bypass this
controller. Successful preview or group hash verification is never a warrant.
Conversely, no certificate is needed for a missing unit that is actually checked
locally against warranted imports.

## Aggregate budgets and coverage are retained, not reset at the new seam

`SearchSession` already shares request/page/provider/snapshot/inflight/byte and
candidate/scan allowances across index providers, charging malformed replies
and failed attempts. Its existing operations do **not** include preview or proof
acquisition. Fetching those outside any aggregate allowance would create a new
resource hole.

The smallest integration need not redesign `SearchSession`: the parent operation
can reserve finite index, preview and evidence subbudgets up front, whose sums
fit one total resource/deadline grant. All preview attempts, duplicates, bad
hashes and candidate failures consume the preview allocation. Evidence checking
uses its separately reserved allocation. No automatic refresh occurs on changing
providers or candidates. The same outer deadline applies throughout. A later
shared dynamic pool is optional, not required to establish a bounded operation.

Transport must enforce byte ceilings while receiving; a parser checking length
after an unbounded download is insufficient. Source execution, proof checking
and disk writes require their own actual process/storage bounds. Search counters
do not replace those controls.

Keep the current honest claims: complete examined intervals apply only to the
selected committed metadata snapshot; positive-only candidate pages do not
establish omitted-negative coverage; neither establishes all mathematics has
been indexed. Recomputing features from a preview does not prove that the
preview is truthful, and checking one candidate does not establish provider-wide
feature extraction correctness.

## Implementation acceptance discriminators, not an experiment campaign

After root selects fresh source, review these specific changes before execution:

1. An ordinary profile can index and retrieve the producer theorem using only
   consumer-known bound symbols. A correctly bound same display name under a
   different unit/profile does not match that exact-symbol query. A dishonest
   preview may falsely advertise the wanted binding, but cannot pass the later
   dependency/header/admission checks on that basis.
2. An unrelated local environment extension does not change existing feature IDs.
3. Preview mutation, false imported binding, wrong unit header and fake accepted
   flag never skip acquisition/checking. Failed acquisitions remain charged.
4. Alternative previews for one ExportID do not let a malicious first response
   suppress a later genuine one at the client.
5. Old record/snapshot schemas still use their original domains and validators.
6. Original ordinary binder/literal/projection DAGs are traversed without tree
   expansion or proof-body reads; profile-bound refusal is explicit.

These are the changed-boundary conditions. Do not rerun all historical index
campaigns or claim growth from them. The subsequent central result must combine
this seam with actual ordinary admission, source use, persistence and reciprocal
publication, with the ordinary-package comparator from `PAYOFF-AUDIT.md` intact.
