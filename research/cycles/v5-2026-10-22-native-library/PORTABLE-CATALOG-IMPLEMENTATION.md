# Portable catalog V2: implementation and importer handoff

2026-10-23. Author: `portable_integration_audit`. Root selected only the new
`software/v5/ordinary_lean/portable_catalog.py` and this checkpoint. Canonical
workspace guard passed. The adopted contract is `PORTABLE-CATALOG-CONTRACT.md`,
SHA-256 `26553e975ca5dbb788fe6a217e4ecf1e07144a74ac553fd4eae3604fa6ab993b`.

**Status: source implementation, unexecuted and awaiting independent review.**
No Python/Lean program, native worker, catalog operation, migration, test, Git or
network operation was run. The existing V1 catalog, helpers, snapshots and all
earlier evidence remain untouched. This is neither a migration result nor a
public V2 controller/CLI implementation.

## Purpose and boundaries

The ordinary-library route needs portable mathematical identities without
discarding its already checked native work. This file implements the V2 local
storage side of that separation. It does not redo proof checking, introduce
cryptographic certificates, or create a second persistent authority.

It imports only existing pure syntax/identity support and V1 filesystem/limit
utilities. It does not inherit V1 reservation/admission methods or open a V1
catalog. The storage implementation retains the existing Windows owner lock,
ordinary nonaliased paths, SQLite DELETE/FULL transactions, bounded local files,
sticky withdrawal and private live-grant discipline. This initial implementation
requires the implementation descriptor's platform to match the actual Windows
process architecture/word size; it makes no cross-platform snapshot claim.

The native worker and raw declaration-unit format are unchanged. A later V2
controller must bind its actual worker/support and exact input payloads to the
new grant. Its parent module comes from the authenticated plan, not from applying
the new root-hash formula to an old snapshot.

## Identity and native checking APIs

```text
PortableCatalog.open(directory, implementation_raw, store_id,
                     *, create=False, limits=Limits())

catalog.semantic_id / foundation_id / implementation_id / basis_root
catalog.context(local_root)
catalog.reserve_basis(fixed_names, *, seconds=120, output_bytes=...)
catalog.reserve_extension(parent_root, raw_v2_units, *, seconds=120,
                          output_bytes=...)
catalog._commit_checked(live_grant)
catalog.abandon(live_grant)
catalog.close()
```

`semantic_id` is S, `foundation_id` is F, `implementation_id` is I. S/F do not
contain local store or implementation identities. `basis_root` is a local
materialization handle, never an alias for F. On a fresh native store it is a
planned handle; `context(basis_root)` still refuses until the actual basis worker
has checked and committed it.

Native local roots use `ordinary_semantics.local_root_id(I_raw, store_id, kind,
parent_root, request_hash)`. The file exports two exact request functions:

```text
basis_request_id(S, F)
  = H("DMKN-ORDINARY-FIXED-BASIS-REQUEST-V2", [S,F,seed,inventory])

batch_id(ordered_portable_unit_ids)
  = H("DMKN-ORDINARY-BATCH-V2", ordered_portable_unit_ids)
```

`reserve_extension` reparses every immutable V2 envelope, checks S, matches every
complete direct import against its exact accepted name/portable-symbol map,
rejects overwrites, derives each actual output's export ID and preserves batch
order. It does not trust previously parsed mutable dictionaries. A reservation
grants no mathematical acceptance.

Each in-process `_Grant` binds its identifier, private output directory,
nonresumable deadline, root/parent/kind/request, immutable bindings bytes, ordered
input UnitIDs, and these immutable controller inputs:

```text
module_name_raw       # new output's native module name
parent_module_raw     # actual already-authenticated parent module name
parent_plan_raw       # actual ordered snapshot/module/path plan
```

The controller must bind its exact raw declaration units and worker result to
these values. `_commit_checked` is private and conditional on that actual clean
worker event. It checks the unchanged live grant, sole output-file census, size,
hash, durable flush, withdrawal/deadline and operation state, then atomically
inserts the root and completes the operation. No saved PASS file or constructor
supplies that precondition. Uncertain transaction outcomes close the catalog and
invalidate all live grants; reopen/inspect the exact root rather than replaying
the worker automatically.

## Root records and context

Every record has the exact fields:

```text
schema = DMKN_ORDINARY_LOCAL_ROOT_V2
local_root, parent_root, kind, semantic_id, foundation_id,
input_unit_ids, request_hash, bindings,
snapshot = {module_name, parent_module, relative_path,
            artifact_bytes, artifact_sha256, writer_origin},
origin, provenance
```

All new native records use:

```text
origin = native-check
provenance = {implementation_id, operation_id}
snapshot.writer_origin = native-check
snapshot.relative_path = operations/<operation_id>/chunk.olean
```

Imported records use a different origin and root domain, described below. Exact
field sets are enforced for both variants. Original and portable basis binding
formulas, the fixed 581-name cardinality, root formulas, request formulas,
operation linkage, snapshot identities, and duplicate/shadowed names are checked
where applicable. The trusted original fixed inventory and actual worker event
remain prerequisites; counting 581 arbitrary names alone is not their replacement.

`context` returns S/F/I, `local_root`, `basis_root`, exact `bindings`, `modules`,
`basis_module`, `root_module` and `retained_support`. These are internal
conditional controller data, not transferable warrants. Each module's parent
must be the previous module's **actual recorded name**. Snapshot bytes are
authenticated once per owner process under the existing local-immutability
premise. Cold context construction still traverses the selected lineage and a
fresh native worker still loads it; no constant-cost cold onboarding is claimed.

## Exact private importer seam

The separate importer owns the V1 read-only source lock/reader, source eligibility,
same-interpretation/support correspondence, original evidence reconstruction,
per-unit translation, copying and audit generation. None is implemented here.

```text
catalog, grant = PortableCatalog._create_importing(
    fresh_destination, implementation_raw, store_id,
    limits=Limits(), seconds=120, output_bytes=...,
    parent_deadline=<absolute monotonic parent deadline>)

selected_root = catalog._activate_import(
    grant, ordered_root_records_raw, import_record_raw,
    source_recheck=<trusted bounded raising source assertion>)
```

`grant.identifier` is a fresh import ID. `grant.directory` is the newly created
`imports/<import_id>` directory. Its deadline is the minimum of the selected
seconds allowance and the exact parent deadline; no flooring/rerounding or
renewal is needed. Normal `open`, context access and worker reservations refuse
`IMPORTING`. The private constructor is fresh-only: an interrupted destination
stays quarantined, not resumable authority.

The importer writes ordinary independent files, never hard links:

```text
imports/<import_id>/audit.json
imports/<import_id>/correspondence.json
imports/<import_id>/<ordinal>/source-record.json
imports/<import_id>/<ordinal>/chunk.olean
```

It may retain translated inert evidence and supporting audit data beneath that
same import directory. `source-record.json` contains the **exact original V1
record bytes**, not a reconstructed projection. The snapshot is an exact copied
original, including its embedded original module and parent-module names. The
full audit must retain complete evidence/mapping and source-support lineage as
required by the adopted contract. The catalog hashes the audit/correspondence
files; their presence is not proof of the importer's actual eligibility premises.

The exported imported-root function is:

```text
legacy_root_id(S, F, destination_store, import_id, source_v1_root, mapped_parent)
  = H("DMKN-ORDINARY-LEGACY-ROOT-V2",
      [S,F,destination_store,import_id,source_v1_root,mapped_parent])
```

Imported root records use the common root fields above, portable input UnitIDs,
the V2 basis/batch request hash, and:

```text
origin = legacy-translation
snapshot.writer_origin = retained-v1-check
snapshot.relative_path = imports/<import_id>/<ordinal>/chunk.olean
snapshot.module_name = local_catalog.module_name(source_v1_root)
snapshot.parent_module = local_catalog.module_name(source_v1_parent) or []

provenance = {
  import_id, ordinal, source_store_id, source_profile_id,
  source_root, source_parent_root, source_record_sha256,
  source_operation_id, source_check_support, translation_support
}
```

`source_check_support` is a sorted unique nonempty list of adopted original
support identities, including the original profile's kernel/adapter/basis
receiver support. Include other original checking/controller dependencies when
they belong to the selected lineage. `translation_support` is the separately
selected translator/importer support identity. Neither is relabeled as a fresh
native check by I.

The canonical `import_record_raw` has exactly:

```text
{
  schema: DMKN_ORDINARY_LOCAL_IMPORT_V2,
  import_id, semantic_id, foundation_id, implementation_id, store_id,
  source_store_id, source_profile, source_selected_root,
  source_manifest_sha256, correspondence_sha256, translation_support,
  source_check_support, retained_support,
  roots: [[new_local_root, SHA256(exact_new_root_record_bytes)], ...],
  audit: {relative_path, artifact_bytes, artifact_sha256}
}
```

`source_profile` is the exact original V1 profile dictionary. Its ID is derived
by the preserved V1 domain, not supplied as an unvalidated compatibility flag.
`roots` is in basis-to-selected-root order and hashes every supplied new record.
`audit.relative_path` must be `imports/<id>/audit.json`; the correspondence hash
binds `imports/<id>/correspondence.json`. `retained_support` must equal the sorted
union of source support, translation support and the current I's five named
support fields. Source-record files are checked against the imported provenance,
old root formulas, original artifact size/hash and exact ordered name census.
The actual per-unit identity translation remains the separate importer's gate.

## Atomicity, bounds and withdrawal

Activation requires the one unchanged live import grant and an empty destination
root/operation/import table. It validates the full destination chain, original
module relationship, all referenced snapshot bytes, original record bytes,
support/audit bindings, and aggregate bounds. A bounded ordinary-file traversal
counts and flushes **all** retained import files, including inert evidence and
audits. This exact charge joins native retained/reserved charges for subsequent
storage admission; imported history is not free storage.

`source_recheck()` is invoked after destination validation/flush, before the
transaction, and again immediately before changing activation inside the
transaction. It must assert the source's still-held lock, eligibility,
withdrawal/support state and unchanged selected source. It is trusted local
importer code, not peer-supplied code and not a boolean compatibility claim.
Deadline and destination withdrawal are rechecked after it.

One transaction inserts the import row, ordered roots and exact ACTIVE activation
record. Failure during that transaction closes the handle; uncertain completion
requires reopening and inspecting the exact activation. If activation is absent,
normal open refuses IMPORTING. If present, startup authenticates its import
record and complete selected imported lineage/files. Missing files refuse.
There is no implicit source mutation, V1 reopening, dual promotion or worker
replay. Whole-store withdrawal remains sticky. Owners must apply original-support
withdrawals to the active V2 store; the archived V1 WITHDRAWN file is not a
permanent second authority or an automatic global revocation service.

Native commits preserve the existing resource accounting and failed/interrupted
reservation charges. Import activation also has finite per-record, aggregate
root-record, root-count, name-count, file-count, artifact/storage and monotonic
deadline checks. Outer hard process/resource supervision is still required.

## Independent review and next discriminator

`admission_event_audit` is reviewing this source. `portable_local_import` has
received the exact seam/schema and is writing the separately selected importer.
Root is writing pure per-unit translation; no duplicate translator is added here.

Before a runtime selection, review especially: IMPORTING denial; immutable
native/import grant binding; source recheck timing; original-module preservation;
both record-origin variants; complete support retention; ordinary path/charge
checks; and uncertain-transaction behavior. Then use small source-selected
storage controls and the existing retained native parent. A new basis replay,
certificate run, broad requalification or duplicate discovery test is unnecessary.

Root reports the preceding separate portable-discovery controls01 passed all
four groups and inspected their result. This author did not rerun them or audit
their saved outcome in this catalog task.

## Source pins

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/portable_catalog.py` | `2d0e91b2920abb69304b920a676da202a5e2444ddec37805d19e953b69eebf35` |
| Reused, unchanged `software/v5/ordinary_lean/local_catalog.py` | `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751` |

The proof/syntax helpers retain their reviewed source selections; root must pin
the coherent assembly, implementation descriptor and any later experiment.
