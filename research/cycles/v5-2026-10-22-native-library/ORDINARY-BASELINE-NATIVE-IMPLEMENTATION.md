# Baseline producer: selected native source checkpoint

2026-10-24. `project_intake_native`; canonical guard PASS. Implements only the
native file assigned by [root's source selection](ORDINARY-BASELINE-IMPLEMENTATION-SELECTION.md).
No native build, test, artifact import, owner/catalog access, package adoption or
Git mutation. The file is source-complete for independent review, not compiled
or runtime-qualified. The full deployable-v5 goal remains unfinished.

## Actual source

`software/v5/ordinary_baseline/BaselineExporter.lean`

SHA-256:
`403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e`

This is a parameterized successor of `ordinary_lean/NativeOwnerExporter.lean`,
reusing unchanged `OrdinaryExport` and complete original declaration codecs.
The approved-project module/path grammar and native filesystem spelling rule
come from the already reviewed `MissingImportExporter.lean`. No predecessor
source or installation was edited. The binder author and root received the
exact interface; the independent reviewer received this source hash.

## Interface

CLI: `BaselineExporter sysroot inventory request output`.
All four are absolute bounded local paths; output must not already exist and is
created with `writeNew`. Phase messages go to stderr. On failure the executable
returns 1 with a bounded diagnostic; output existence is not a success warrant.

The request has exactly:

```text
schema = "DMKN_ORDINARY_BASELINE_EXPORT_REQUEST_V1"
project_search_paths = explicit ordered approved Windows local drive roots
modules = original-codec formal module names
targets = original-codec formal declaration names
```

Limits are the selected 1-MiB request; 1–16 roots/modules with the existing
approved-project grammar; 1–1,024 distinct nonbasis targets. The native layer
checks root shape/directories, module filesystem grammar and duplicate names.
The controller must additionally authenticate canonical duplicate-free request
bytes, exact executable/runtime/inventory, explicit owner approval and ordinary
non-reparse paths/ancestors. A module name is not permission to import a peer's
binary. These are selected local inputs, not a hostile-binary sandbox.

The fixed inventory must have 581 distinct names. Exact inventory identity is
still authenticated by the controller and pure binder using the selected
`S.INVENTORY` hash; a 581-name JSON shape alone cannot establish it. Nonbasis
target checking precedes project import. The existing `Export.selected` performs
actual selected-library correspondence to the fixed inventory before exporting
any nonbasis closure.

Output is the unchanged inert writer envelope:

```text
schema = "DMKN_ORDINARY_EXPORT_BUNDLE_V1"
assurance = "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"
targets, basis_names, units
stats = {source_records, selected_units, dependency_edges,
         scan_nodes, unit_json_bytes}
```

The binder independently checks expected targets, exact basis and every complete
unit, then derives existing V2 seed-bound imports/IDs and the companion manifest.
Producer diagnostics, counters and hashes are never mathematical authority.

## Checking and resource boundary

One selected private environment is imported using runtime-first explicit search
paths, `plugins := #[]`, `loadExts := false`, no inherited `LEAN_PATH`, helper
environment, source directory, build script, dynamic stop or catalog callback.
Targets must actually exist as complete safe private records; axiom-shaped,
unsafe, partial or miskeyed target records refuse. The existing exporter rejects
unsupported selected dependencies/semantics and serializes complete groups.

The concrete successor retains the predecessor's **eager** `Export.indexSource`
census. It does not claim the shared scheduler's optional lazy-index behavior or
streaming/constant-memory export. Existing finite limits remain 262,144 source
records, 65,536 group records, 8,192 selected units, 262,144 edges, 20,000,000
source scan nodes, 8-MiB individual unit and 64-MiB aggregate unit bytes. The
final writer envelope independently remains at most 64 MiB. Portable V2 wrapper
overhead may exceed the binder's own caps and refuse; no limit is raised.

The bound on source scan nodes is different from the binder's encoded-node
accounting. All eager indexing, source import, serialization and output costs
belong in the later selected whole-operation resource envelope. Source functions
alone do not hard-bound controller/native CPU or memory. No runtime allowance is
created by this checkpoint.

## Relation to ordinary-library reuse

The independently reviewed
[realization contract](ORDINARY-BASELINE-REALIZATION-CONTRACT.md) at
`258846eb77c5da80c2cd03fe7a79e2fbed386304e8a5cc7ec75295d51f33c9e1`
separates full private proof closure from the exact actual-public interface
closure. It preserves full public computational equality and the existing narrow
singleton theorem-erasure rule, while avoiding needless public exposure of
private proof-only helpers. It requires immutable original artifact snapshots
and controlled future module-name resolution.

This exporter does **not** implement that reference matcher, artifact snapshot,
protected registration or ordinary delta integration. A mutable approved project
path remains extraction permission, not a warm semantic anchor. Root has selected
only producer/binder/intake source at this stage. A usable baseline workflow still
requires the later coherent ordinary-use integration; successful export alone
would establish neither mathematical acceptance nor practical growth benefit.
