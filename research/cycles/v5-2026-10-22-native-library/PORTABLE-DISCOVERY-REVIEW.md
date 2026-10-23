# Portable ordinary discovery: independent source review

2026-10-23. Reviewer: `portable_integration_audit`. Canonical workspace guard
passed. This is a source-only review of the new adapter and its three shared
schema changes. No Python/Lean program, test, catalog, migration, network or Git
operation was run. Reading source, comparing retained text and hashing files do
not establish runtime qualification.

## Disposition

**No blocking defect found in the reviewed source boundary.** Proceed to a small
changed-boundary control using the existing Store/Query implementation, subject
to root's separate source/runtime selection. This is not approval of portable
catalog migration, receiver admission, deployment, search quality or growth.

The selected approach has a useful narrow role: an agent can ask for known formal
symbols and receive an unfamiliar portable export's advertised type without
knowing its export ID. It reuses the existing authenticated posting lists instead
of introducing a parallel index or requiring proof certification. The next
decision-changing evidence is that this adapter actually traverses that existing
store/query path and binds returned metadata correctly.

## Identity and authority argument

For a V3 record, generic validation checks the exact record fields and then:

1. `portable_preview.read_locator` checks the exact V2 locator shape and native
   name grammar, returning a detached locator.
2. The record namespace must equal `namespace_for(locator.semantic_id)`.
3. Its object ID must equal the export ID computed from that semantic ID, unit
   ID and exact export name.
4. The record hash uses the separate `DMKN-FORMAL-FEATURE-RECORD-V3` domain.

Thus changing the locator's semantic ID, unit ID or name without changing the
corresponding namespace/object identity refuses. A matching namespace/ID remains
only a well-formed advertisement: it does not establish that the unit exists.

The namespace commits to the semantic ID, preview/evidence/unit/expression
formats, no-conversion normalization, feature schema/revision and eight-bit
partition profile. It does not commit to an implementation, local context,
provider or machine path. This supports identical portable indexing across local
implementations only when they really share the selected semantic contract.

`OrdinaryExportAdapter` accepts only the currently selected semantic ID.
Generic V3 metadata validation can validate claims for another semantic ID;
that is deliberately not adoption of those semantics. No peer selects a local
module path or executable implementation.

`resolve(record, raw)` validates the record, reparses the exact preview bytes,
recomputes all features, hash, byte count, locator and identity, and requires
equality of the complete record. It does not trust a previous description,
mutable preview wrapper or success flag. Its result explicitly denies
mathematical acceptance.

The four distinct gates remain intact:

| Gate | What it establishes | What it does not establish |
|---|---|---|
| Existing index proof | Membership of the exact selected metadata record in a committed index | Correct extraction, evidence existence or truth |
| Adapter resolution | Exact record-to-preview byte/feature binding | Preview-to-evidence binding |
| Portable preview resolution | Exact selected header/bindings match the inert evidence | Independent proof checking or catalog authority |
| Protected ordinary admission | Applicable semantic/import checks and native extension checking | Global coverage, usefulness or novelty |

Conflicting preview claims for one export can yield different record hashes.
The existing Store refuses a conflicting same-object record rather than
overwriting history. This preserves its invariant, but does not make the first
advertisement mathematically authoritative. Invalid/poisoned discovery metadata
still requires rejection at the later evidence gate and alternative-provider
handling; this adapter does not solve discovery omission or availability.

## Bounded extraction argument

The reused preview parser checks a finite, closed, root-reachable expression DAG
with backward references and the exact explicit const/projection-name census.
The adapter's node positions agree with that parser: application function at
index 1, forall domain/body at indices 3/4, and const/projection name at index 1.

For expression node `i`, the adapter computes `spine[i]` once: the already
computed function spine for an application, otherwise `i`. The head descriptor
of each visited terminal is also memoized. Leading forall bodies have strictly
decreasing indices, so this walk cannot revisit a binder or cycle. Explicit
type-symbol features come from the checked census, not from proof-body imports.

Let `n` be expression nodes, `b` type bindings and `q` leading forall binders.
Ignoring bounded name-byte processing and hashing, extraction is
`O(n + b + q)` time and `O(n + b + f)` auxiliary space, where `f <= 128` is
the number of distinct features. It does not expand a shared expression tree or
load imported proofs. The implementation's reported feature/traversal counter is
`n + b + 2*q + 3`; this is not a count of all parser instructions or CPU cost.
The parser's universe work and serialized input bytes remain additional costs.

The 129th distinct feature refuses explicitly, while duplicate features are
deduplicated. The 16 KiB generic record limit and finite preview bounds remain.
These are indexing-profile limits, not verdicts that the mathematics is invalid.
Result/binder heads are syntactic: no beta/delta/let reduction, semantic
equivalence or implicit literal dependency is claimed.

This removes global-corpus size and ancestral proof length from **feature
extraction**, not from every search/acquisition operation. Posting selectivity,
provider coverage and charged query budgets remain separate obligations.

## Compatibility and existing-engine integration

Compared the three shared files to the retained discovery source at
`product-local/v5-split-reader-source-01/v5/discovery`.

- `formal_features.py` adds only two ordinary constants, the V3 schema/locator
  branch and its separate record-hash domain. The V1/V2 validation branches and
  domains remain. The entire `NamedModuleAdapter` tail is text-identical to the
  retained baseline.
- `discovery_store.py` adds the new schema to its import and adapter allowlist.
  Store configuration, admission, snapshots, postings and query implementation
  are otherwise unchanged. The existing default schema is still omitted from
  persisted configuration exactly as before; the new nondefault schema is stored.
- `authenticated_index.py` adds the schema import and snapshot allowlist entry.
  Snapshot and Merkle commitment domains/encodings are unchanged.

The adapter itself imports only `formal_features` eagerly. Ordinary helpers are
loaded on adapter construction or on a V3-record branch. Therefore valid old
V1/V2 paths do not gain an ordinary-helper dependency. A V3 assembly still must
ship the coherent helper set explicitly; lazy imports do not make unsupported
V3 records usable in an old helper-free installation.

Source inspection of the actual engine shows the intended path is available:
`Store.admit` invokes the supplied adapter; `_seal` uses its feature schema;
`summary` authenticates requested feature postings; `discovery_query` validates
snapshots through the extended validator and records through V3 validation.
`candidate_query` likewise reaches generic record validation without a hardcoded
old record-kind gate. Its positive-hit proofs still do not prove scan coverage.
The session remains a bounded caller-driven accounting layer, not mathematical
acceptance or a global research planner.

## Minimal recommended changed-boundary controls

These are recommendations for the author/root, **not tests run by this review**.
Use a fresh bounded index store, not a mathematical catalog or an existing node's
state. Reuse already tested preview syntax fixtures/helpers and the real engine.

| Control | Required discrimination |
|---|---|
| Unknown-ID actual Store/Query path | Compile a conjunction from known portable type symbols and declaration kind before inspecting the unfamiliar export's ID. Admit one matching preview and a few relevant nonmatches using actual `Store.admit`; obtain/verify a summary, select partitions with `Q.plan_partitions`, obtain/verify pages, and resolve the returned preview. Do not choose the partition or request by the expected result's ID. Assert the advertised match and continued `mathematical_acceptance=False`. |
| Existing positive-only candidate path | Against the same store/summary, obtain/verify a bounded candidate page and compare its hits with the exhaustive page on this finite fixture. Keep its no-verified-scan-coverage claim. This discriminates integration without rerunning the old generic query suite. |
| Changed binding/conflict boundaries | Mutate semantic ID, unit ID, export name, namespace, expected export ID, preview hash/size or claimed features and require the applicable V3/resolve refusal. Admit identical bytes idempotently; refuse a changed preview for the same export without replacing the first snapshot. One unsupported-S claim can pass generic metadata syntax while constructing that unsupported adapter refuses. |
| Shared DAG and feature limits | A small application spine shared by multiple leading binder domains must produce exact expected head/symbol features and the stated linear work counter. Check a projection head and literal head. A finite fixture crossing 128 distinct features must refuse rather than truncate. No large-scale benchmark is needed. |
| Old valid-byte/lazy-import preservation | In an isolated import context with ordinary helpers unavailable, check fixed valid V1 and V2 records, their exact predeclared hash domains/bytes and an old-schema snapshot. The new adapter must not be imported merely by those old paths. Do not dynamically derive expected old values from the implementation under test. |

These controls do not need Lean, native artifact loading, proof production,
catalog migration, networking or a rerun of the preceding 15 portable-preview
controls. Later actual unknown-method discovery must use real published previews
and the ordinary evidence/acquisition/admission path; this finite integration
control alone cannot establish useful reciprocal growth.

## Exact reviewed pins

Paths below are relative to the sole canonical root.

| Source | SHA-256 |
|---|---|
| `software/v5/discovery/ordinary_export_adapter.py` | `fb732a01996a821ff52f95dcb8fbd6a7a89f9aecbbb6492e24198dcf79132600` |
| `software/v5/discovery/formal_features.py` | `7dbcb626c54e5303927b71b9e2993921030ddf88212221bc96f1463c822dc417` |
| `software/v5/discovery/discovery_store.py` | `993c8322173f913fad96e09c77b851a8748d7a7b1f172d37372a7d20a0e09b4e` |
| `software/v5/discovery/authenticated_index.py` | `b0301e39a6d2149e27b43336bd37bfd30fbf130953e29677f7217b460fa9c9e7` |
| `software/v5/discovery/discovery_query.py` | `f9ce09ba74e7656a2f53d813489a43434258208198bcb4784c0e4eb682ac24e2` |
| `software/v5/discovery/candidate_query.py` | `b5d87baa539ce734b95891ea7358db96f137b39520151fd05c8e8272efe2d639` |
| `software/v5/discovery/search_session.py` | `e82c628eb75a584b33e637d4758cc9e789c3953ef4fb86b7d6e5111e3fd425cf` |
| `research/cycles/v5-2026-10-22-native-library/PORTABLE-DISCOVERY-IMPLEMENTATION.md` | `6d32fd2781e9cc882f69a3d7c4e4f070516e0f4826328c51f73699025b24f4b6` |
| `software/v5/ordinary_lean/portable_preview.py` | `b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d` |
| `software/v5/ordinary_lean/ordinary_preview.py` | `0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6` |
| `software/v5/ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `software/v5/ordinary_lean/ordinary_semantics.py` | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| Retained baseline `formal_features.py` | `547e43d3efb3ec0067ea6b65d215a1c5147255e0713c2024668ae9a75d4fb43d` |
| Retained baseline `discovery_store.py` | `1eee0bc573c77d1e5e6a61ae125a29df6ca179c04f525fe8210036b75b14555d` |
| Retained baseline `authenticated_index.py` | `076298a5d0c3a7f47870d5c24775ffa0d2bdf9106cfbcad060ebd16225fc4734` |

All predecessor source/evidence and local acceptance state remain unchanged by
this review. Root owns adoption and any subsequent execution selection.
