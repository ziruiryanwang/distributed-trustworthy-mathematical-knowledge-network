# One eligible owner-local import: source handoff

2026-10-23. Author: `portable_local_import`. Source only. No Python/importer,
compiler, Lean, test, SQLite inspection, migration or accepted-state write was
run. The only edited implementation is
`software/v5/ordinary_lean/legacy_catalog_import.py`; this checkpoint is its
handoff. Source self-review includes exact original support-map and snapshot
binding. Independent review and root selection remain separate.

The user workflow is one-time conversion of the already adopted local ordinary
library into portable discovery/reuse identities, retaining its actual checked
native snapshots. No certificate or accepted-proof replay is required. This
does not establish deployable v5 or general foreign snapshot acceptance.

## Exact controller seam

```text
import_legacy(source_directory, expected_source_manifest_raw, fresh_destination,
              implementation_raw, destination_store_id, correspondence_raw,
              *, parent_deadline, limits=ImportLimits(),
              catalog_limits=local_catalog.Limits())
```

The deadline is the caller's original absolute monotonic deadline, at most one
hour ahead. The same value bounds file I/O and the private destination grant;
it is never renewed. A result contains `local_root`, `basis_root`, `semantic_id`,
`foundation_id`, `implementation_id`, `import_id`, `source_root`, `names`,
`roots`, and `output_bytes`. Errors propagate; any destination is retained and
closed. An uncertain SQLite commit requires inspection of the exact activation
on reopen; the importer never retries it.

The source is explicitly restricted to
`experiments/v5-local-checks/ordinary-successor-admission-01/successor-admission/catalog`
under the canonical project root. Its eligibility and actual checking lineage
must already be adopted by the trusted root controller. The manifest and
correspondence are caller-selected canonical bytes, never peer self-description.
Pins, saved success files, argument prose, and digest equalities do not prove
that actual native checking occurred or that support implements S.

The exact source manifest fields are:

```text
schema = DMKN_ORDINARY_ELIGIBLE_LOCAL_SOURCE_V1
source_directory, store_id, profile_id, basis_id, selected_root
marker, database, fixed_seed, fixed_inventory
check_support: [pin, ...]
roots: [{root, record_sha256, check_lineage: [pin, ...], evidence: [pin, ...]}, ...]

pin = {path: absolute normalized path, bytes: unsigned integer, sha256: lowercase hex}
```

Roots are complete basis-first chain order; basis evidence is empty. Each later
evidence list is the original accepted unit order. No duplicate evidence path
or extra committed branch is accepted. Artifact pins are reconstructed from
the fully authenticated original root records, avoiding a competing artifact
manifest. Failed/interrupted operations and their files stay in V1 untouched.

The exact correspondence fields are:

```text
schema = DMKN_ORDINARY_SAME_RUNTIME_CORRESPONDENCE_V1
source_profile_id, semantic_id, foundation_id, implementation_id
kernel_support, adapter_support, basis_receiver_support, snapshot_support
snapshot_format, platform, seed_sha256, inventory_sha256
expression_contract_sha256, declaration_contract_sha256
adopted_argument: pin
```

The implementation and correspondence must retain V1's exact kernel, adapter
and basis support; fixed seed/inventory, S/F and both interpretation contracts
must equal the existing source-defined descriptors. `check_support` must include
the exact original `ordinary-native-admission-01/native-admission/PROFILE.json`
and actual file pins resolving every kernel, adapter and basis-receiver support
map leaf by filename, byte count and hash. The original three domain-separated
support digests are recomputed from that retained profile. Initial platform is exactly
Windows/x86_64/64-bit/little-endian and the unchanged Lean 4.34 ModuleData format.
Snapshot support is exactly `local_catalog.digest("ordinary-snapshot-support-v1",
{"source": {...}, "compiled": {...}})`, where each map contains the original
`BasisSnapshot` and `LocalSnapshot` source/object rows from the adapter support.
The root-selected concrete support-to-S argument remains an adoption premise,
not a `compatible` flag. The current controller support ID
must name the actual importer, translator, catalog and controller source cut.

## Storage and preservation

The importer reuses the existing ordinary-path/hex/hash primitives and pure
`legacy_identity_translation.translate_unit`/`basis_pairs`. It never calls V1
`LocalCatalog.open`, whose reservation recovery would mutate the source. It
holds the unchanged one-byte owner lock and uses SQLite `mode=ro`, rejects all
journal/WAL/SHM sidecars and active reservations, and verifies the exact source
marker/database, every selected original record, V1 root formula, operation,
artifact, full ordered basis/output binding census and ordered batch hash.

Fixed inventory+seed hashes are checked before parsing their inert JSON. Each
complete unit is read/transformed separately; both name maps grow only through
the pure translator's established import pairing. Original raw declaration
units stay byte-identical. Bounds cover selected unique files/input bytes,
output files/bytes, roots, units, names, nodes, record/summary bytes and deadline.
The default per-file cap is 128 MiB because the actual adopted
`libleanshared.dll` is 70,414,848 bytes. Native artifacts/support are hashed in
1 MiB chunks; this cap does not allocate a 128 MiB buffer. Aggregate selected
input/output caps default to 512 MiB each. The caller's supervisor must also
enforce its finite CPU/memory/whole-operation wall limits.

The catalog-author seam is:

```text
PortableCatalog._create_importing(..., parent_deadline=parent_deadline)
catalog._activate_import(grant, ordered_root_records_raw, import_record_raw,
                         source_recheck=source.assert_unchanged)
```

The catalog invokes the raising source callback after file flush/validation and
again immediately before activation in its single transaction. The source lock
remains held. No source API is given to the catalog; no native-worker grant is
created during import.

Both final callbacks rehash all selected source/support/evidence pins. This is
two additional linear SHA passes, explicitly charged to the same deadline;
neither invokes the kernel or parses proof terms again. The initial open avoids
a redundant full rehash after individually checking records/support.

For each root, the destination retains `source-record.json`, exact `chunk.olean`
and translated inert evidence under `imports/<id>/<ordinal>/`. `audit.json`
retains the complete selected source manifest, all old/new UnitIDs, evidence
hashes, unchanged raw-unit hashes, output pairs, basis pairs and root mapping.
`correspondence.json` retains its exact selected bytes. Imported root provenance
separates original check support from translation support, preserves original
module/parent module names, and uses the dedicated legacy local-root domain.

The original checking support IDs and hashes of retained check-support/lineage
records join the current implementation and translation support in the active
catalog's retained dependency set. Future withdrawal targets the active V2
store; archival V1 mutation is not a propagation protocol.

## Remaining verification

Root owns the exact eligible-source manifest, concrete support adoption,
supervised finite driver and any runtime selection. The catalog author owns
its private transactional seam. Independent source review and focused changed
boundary controls must precede any actual migration. No output directory or
test result is supplied by this source-only handoff.
