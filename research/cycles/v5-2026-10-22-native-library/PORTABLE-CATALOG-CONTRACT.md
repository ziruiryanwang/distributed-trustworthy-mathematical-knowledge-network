# Portable catalog V2 and one-time local legacy import

2026-10-23. `successor_export`. Source-design only: no implementation,
migration, native execution, test, Git action or legacy artifact mutation.
This concretizes the final V2 choice in `ORDINARY-DISCOVERY-INTEGRATION-PLAN`.

## Decision and actual source boundary

Use one V2 catalog authority after a one-time, owner-local import of an eligible
V1 lineage. Do not maintain permanent bidirectional V2/V1 admission or make a
peer-supplied translation table authoritative. Keep the accepted native work.

The source supports this choice:

- `local_catalog.py:134-206` couples the V1 profile/basis to the marker and
  database. Its `open` updates stale `RESERVED` operations; it is **not a
  read-only importer** and must not be used to inspect an immutable V1 source.
- `context:223-266` validates snapshot hashes and original-name bindings, but
  derives module names from root IDs. V2 must store actual module names.
- `reserve_extension:317-344` checks exact imported symbols, no overwriting,
  complete unit inventory and bounded ordered batches. Preserve these checks
  with V2 identities, not a second promotion step.
- `_commit_checked:353-403` requires a live in-process grant, fresh exact output
  census and transactional insertion. It does not authenticate a saved PASS
  file. Preserve that actual-event precondition and uncertain-commit refusal.
- `OrdinaryWorkflowWorker.extend` reads only an explicit import plan and raw
  declaration units. It never interprets V1 profile IDs or envelope import IDs.
  `LocalSnapshot.restoreLocal` checks exact embedded module/import relationships;
  `checkAndWriteChunk` checks all new units and saves actual generated records.
- `run_successor_admission.py:451,504` currently derives both parent module and
  report comparison from the V1 root. Those two uses must instead take the
  authenticated plan's actual `root_module` after migration.

Thus the already built worker, Lean decoder, kernel checks and original snapshot
bytes can remain unchanged. This conclusion is specific to the selected ABI,
runtime and interpretation, not permission to load old snapshots under arbitrary
new binaries or to adopt someone else's `.olean`.

## Three identities, with no ambiguity

Use the existing exact `ordinary_semantics` descriptors and domains:

| Identity | Meaning | Contains local support? |
|---|---|---|
| `foundation_id = F` | Exact fixed seed, normalized inventory and initialization rules | No |
| `semantic_id = S` | Interpretation, F and mathematical extension policy | No |
| `implementation_id = I` | Selected actual controller/checker/snapshot/platform support intended to realize S | Yes |

The pure V2 authoring seam is already agreed with `preview_boundary_review`:

```text
{schema: DMKN_LEAN_ORDINARY_EVIDENCE_V2,
 semantic_id: S, imports: [[originalName, portableSymbolID], ...],
 unit: unchanged ordinary V1 declaration unit}
```

Use `portable_evidence.read_evidence` and `ordinary_semantics.export_id` /
`basis_symbol_id`. S commits F, so the envelope need not repeat F. No store,
implementation, path or materialization root enters a portable identity.

**`basis_root` is a local materialization root, not F.** Remove the ambiguous
V1 `basis_id` meaning from new APIs. It is valid for two local stores to have
different basis roots while recognizing identical portable basis symbols.

## Smallest coherent software surface

Select fresh `portable_catalog.py` and `legacy_catalog_import.py`; retain V1
modules and frozen runtime cuts unchanged. Reuse the audited path/size/hash,
Windows owner-lock and SQLite DELETE/FULL patterns, not a new storage engine.
The V2 catalog may share pure V1 utilities (`ordinary`, `read_bounded`,
`module_name`, limits and hex checks), but should not inherit V1 admission
methods whose implicit profile/basis assumptions differ.

Proposed internal APIs:

```text
PortableCatalog.open(directory, implementation_raw, store_id,
                     *, create=False, limits=...)
catalog.semantic_id / foundation_id / implementation_id / basis_root
catalog.context(local_root)
catalog.reserve_basis(fixed_names, *, seconds, output_bytes)
catalog.reserve_extension(parent_root, raw_v2_units, *, seconds, output_bytes)
catalog._commit_checked(live_grant)        # private, actual-worker prerequisite
catalog.abandon(live_grant) / close()

LegacyReadOnly.open(source_directory, expected_source_manifest)
import_legacy(source, selected_root, ordered_evidence_by_root,
              fixed_inventory, fresh_destination, implementation_raw,
              correspondence_record, limits, parent_deadline)
```

`context` returns portable `bindings`, `local_root`, S, F, I and the concrete
`modules`, `basis_module`, `root_module`. All are internal conditional controller
data, not transferable warrants. New grants retain exact V2 input UnitIDs,
batch hash, parent root and actual parent module in their immutable live binding.
The controller binds raw unit bytes to those inputs before launching the same
worker, and checks the returned parent module against the grant's plan.

V2 `reserve_extension` reparses immutable V2 bytes, matches S, resolves each
exact name/portable ID in the accepted prefix, derives export IDs and rejects
duplicate/overwritten outputs exactly as V1 does. New local roots use the
existing `ordinary_semantics.local_root_id` with I and store identity. A fresh
basis initialization remains the real pinned basis worker, not metadata import.

The SQL shape can remain small: `meta`, `roots`, `operations`, plus a single
`imports` row per imported lineage. Add an activation state to `meta`; no alias
authority or second promotion database is needed. Root records add:

```text
schema, local_root, parent_root, kind, semantic_id, foundation_id,
input_unit_ids, request_hash, bindings,
snapshot: {module_name, parent_module, relative_path,
           artifact_bytes, artifact_sha256, writer_origin},
origin: native-check | legacy-translation
```

Use explicit exact field sets for each `origin` variant. `native-check` binds I
and the actual operation. `legacy-translation` binds an import ID, the original
V1 store/profile/root/record hash/operation, original check-support lineage and
translation-support identity. It must never say the new controller rechecked
that snapshot. Retain original record bytes in the import audit, rather than
copying their fields selectively and losing origin evidence.

All relative artifact paths are catalog-generated, bounded and checked under
the same ordinary nonaliased-directory rules. Native-produced chunks remain
under `operations/<grant>/chunk.olean`; migrated copies may use
`imports/<import-id>/<ordinal>/chunk.olean`. Different physical paths are safe
only because artifact bytes and embedded module relationships remain identical.

For migrated root handles use a fresh domain, for example
`DMKN-ORDINARY-LEGACY-ROOT-V2`, binding S, F, destination store, import ID,
original V1 root and mapped parent. Do **not** use the new-native-check root
formula and thereby imply new checking. These are local handles only.

The public V2 owner-request/bundle/controller labels require a separate explicit
version: S, F and local context root, instead of reinterpreting `profile_id` or
`basis_id` in V1. Raw Lean groups/units need not change. Current V1 commands and
the immediate reciprocal test are not retroactively relabeled.

## Exactly what the importer verifies

The initial operation handles one selected V1 ancestor **chain**, not arbitrary
branch merging. It migrates every binding/unit in that chain's actual snapshots,
not merely the target's authoring closure. Otherwise retained native snapshots
would contain declarations missing from their advertised portable context.

1. Acquire the source's existing owner lock without rewriting its byte, and
   read SQLite through read-only mode. Require no unresolved rollback journal,
   WAL/SHM sidecars or stale active reservation; recovery is a separate source
   operation, not a side effect of migration. Retained FAILED/INTERRUPTED history
   is allowed and preserved. Validate exact marker/profile/store/selected-root
   lineage, source ordinary paths, bounds and current eligibility.
2. Verify every selected record, root/parent relationship, actual artifact size
   and SHA-256, and full binding census. Recompute V1 basis and extension root
   formulas and original ordered batch hashes. An expected digest alone is not
   proof of an actual past check: the selected source must already be an eligible
   protected local catalog with the independently adopted original check lineage.
3. Read the exact fixed inventory and every retained V1 evidence unit belonging
   to the selected chain, using the known per-root ordered manifests. Reparse
   with V1 rules, recompute each UnitID/export, check imports against the prior
   V1 prefix and compare the complete ordered output bindings and batch hash
   with that root's accepted record. Missing evidence, extra units, shuffled
   batches or an incompatible accepted name refuse; do not manufacture inputs
   from types or infer proof identities from theorem names.
4. Initialize the translation with each V1 fixed-basis symbol paired with
   `basis_symbol_id(S,F,originalName)`. For each accepted unit in dependency
   order, keep `canonical_json(unit)` **byte-identical**, retain every original
   name and import ordering, and replace only envelope schema/profile and each
   external symbol ID by its already established portable counterpart.
5. Reparse the V2 result, derive its new UnitID/exports and compare its exact
   output-name census with the original. Record old/new UnitIDs, original
   evidence hash, unchanged unit hash and old/new output pairs. All imports
   must already be mapped; cycles/unknown parents refuse. Preserve generated
   groups atomically. New evidence is inert data, not a migration certificate.
6. Copy the selected original snapshots into the fresh destination with exact
   before/after byte/hash checks. Store their **original module names and original
   parent module names**, even though their catalog root handles are new. Do not
   rebuild, rewrite, deserialize, relabel or recheck those files during import.
7. Bind original and translated records, full mapping/evidence manifest and
   snapshot origins into one bounded import record. Preserve V1 failed evidence
   in its original archive; migration does not rewrite or erase it.

The correspondence record must name the actual adopted V1 kernel/codec/basis
support, unchanged seed/inventory, S's exact source-defined interpretation and
snapshot compatibility. A `compatible=true` field or implementation descriptor
claim cannot establish this premise. Retaining the same native checker and ABI
makes the initial argument narrow; cross-runtime changes are out of scope.

## Why identifier translation preserves meaning

Let `K_j` be the accepted V1 environment after unit j and `B_j` its exact name
map. Let `T_j` pair its already warranted symbols with portable symbols. The
claim is **same resolved declarations under new identifiers**, not equality of
the V1 and V2 hash values and not an arbitrary equivalence between declarations.

Base: F fixes the same ordered foundation construction and normalized inventory
as the adopted V1 basis. Each original basis name therefore resolves to the
same actual accepted declaration on both sides of `T_0`.

Step: the canonical raw unit is unchanged; its syntax references original Lean
names, not envelope symbol hashes. Its complete external reference census is
unchanged. Each envelope import is mapped to precisely the same already accepted
declaration by the induction hypothesis. The interpretation and kernel primitive
rules are unchanged by the explicit S correspondence premise. Consequently the
accepted unit's judgment and actual output declarations have the same meaning;
their V2 export IDs bind that very unit and those same names. No proof replay is
needed to rename these metadata references.

This argument fails if units/names are rewritten, import mappings substitute
different declarations, foundation/primitive rules change, original support is
ineligible, or the exact accepted evidence cannot be recovered. In those cases
refuse this import. A separately authorized native check may supply new evidence,
but is not an automatic fallback or reason to repeat the successful corpus.

## Atomic activation, interruption and withdrawal

The destination begins `IMPORTING` and is rejected by every normal V2 `open`,
context and reservation path. Only the bounded private importer can populate
its staged rows/files. No worker grant or accepted prefix is exposed there.

After all copied files, canonical evidence and manifests are flushed and
validated, and the source is still locked/eligible and unchanged, one SQLite
`BEGIN IMMEDIATE` transaction inserts/finalizes the complete selected root chain,
its import record and the `ACTIVE` activation row. Existing DELETE/FULL and
uncertain-commit handling apply. Check exact activation record on reopen; never
blindly repeat import or native work after an uncertain commit. If activation
did not occur, the destination is retained quarantine and the original source
is unchanged. If it occurred, all required referenced immutable files already
exist. Startup still checks their existence/hashes; a crash causing missing
durable files yields refusal, not silent partial acceptance.

After cutover, V2 is the sole operational authority; V1 is a read-only historical
archive. V2 retains the full original support dependency set plus migration and
current controller support. Sticky whole-store withdrawal applies on open,
context and immediately before promotion. A known withdrawal of any retained
support must quarantine this store as well; migration never launders its origin.
The initial implementation does not claim automatic propagation from arbitrary
later edits to an archival V1 `WITHDRAWN` file. Owner support-withdrawal operations
must target the active V2 store. This is an explicit local operational requirement,
not a second permanent catalog authority or global revocation consensus.

## Bounds, payoff and smallest discriminators

Migration cost is linear in selected-chain retained evidence bytes plus snapshot
copy/hash bytes and bounded map/index operations. It visits proof-bearing evidence
to derive content IDs but never checks those proof terms. Retain per-root unit
order and stream one unit at a time; impose aggregate bytes, nodes, roots, names,
output storage and one nonrenewing parent deadline. The cost is one-time local
onboarding, never charged anew to each search or ordinary accepted reuse.

Focused future controls should cover: exact translated import preservation;
changed unit/import/order refusal; missing accepted evidence; module-name
preservation across imported parent/new child; wrong original support or
withdrawal; crash before activation and uncertain commit inspection. One real
small new extension above the migrated actual parent can test integration; no
basis replay, broad native campaign or certificate production is justified.

This design fixes identity fragmentation and duplicate authority. It does not
solve existing cold full-context loading, one-chain branch merging, global index
completeness, world-scale availability or useful-growth claims. Those remain
separate release issues; portable IDs alone establish none of them.
