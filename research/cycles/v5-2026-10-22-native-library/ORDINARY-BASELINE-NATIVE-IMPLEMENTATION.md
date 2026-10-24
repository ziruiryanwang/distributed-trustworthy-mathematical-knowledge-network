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

## A2 artifact collector and explicit-map replay source

2026-10-24 continuation, separately selected by root in the same implementation
selection. Only fresh `software/v5/ordinary_baseline/BaselineArtifacts.lean` and
this checkpoint are changed. The producer `BaselineExporter.lean` above remains
byte-identical. No native build/run, source project import, copy, owner operation
or Git mutation occurred.

Artifact source SHA-256:
`0bd6e10626b790ec6dd616ca08edbd6786e36dbdcbeddc07bd39ed54f99ff050`.
Independent source review is requested; compilation and execution are not claimed.

### Stable API for the controller

CLI: `BaselineArtifacts sysroot request report`.

Both request variants use schema `DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1`:

```text
collect: {schema, mode:"collect", modules:[encodedName], project_search_paths:[path]}
replay:  {schema, mode:"replay", modules:[encodedName],
          artifacts:[{module:encodedName,
                      parts:[[olean, olean.server, olean.private],[ir.sig, ir]]}]}
```

Root `modules` has the existing 1–16 original-name grammar; each is imported with
the selected ordinary flags `import_all=0, is_exported=1, is_meta=0`. Every
transitive module, including runtime imports, must appear in a successful replay
map. Five original adjacent parts are required; legacy and missing-part layouts
are explicitly unsupported. All paths are absolute ordinary Windows drive paths.
The controller still validates authorization, file ancestors, aliases/reparses,
exact runtime/request identity and bounded whole-process execution.

The report schema is `DMKN_ORDINARY_BASELINE_ARTIFACT_REPORT_V1` with assurance
`INERT_ARTIFACT_CLOSURE_NOT_MATHEMATICAL_ACCEPTANCE` and exactly:

```text
{schema, assurance, mode, roots:[ImportRow], modules:[ModuleRow],
 module_count, part_count, direct_import_edges, artifact_bytes}

ImportRow = {module, import_all, is_exported, is_meta}
ModuleRow = {module, is_module:1, imports:[ImportRow],
             effective:{import_all,is_exported,is_meta,has_data,ir_phases},
             parts:[[path,path,path],[path,path]],
             part_bytes:[[bytes,bytes,bytes],[bytes,bytes]]}
```

Flags are integers 0/1, not bare JSON booleans. `ir_phases` is `runtime`,
`comptime` or `all`. Exact original direct-import flags come from the corresponding
private `moduleData.imports`; actual effective flags come from `header.modules`.
They are deliberately not conflated. Report ordering follows the native imported
module census. The `parts` matrix is directly compatible with the selected
runtime's `ImportArtifacts.toArrays`; name encoding remains the existing original
codec rather than assuming Lean's separate automatic JSON name format.

### Exact supported import behavior

Inspected selected-runtime `Environment.lean:109-175,1858-1917,2007-2246,2307-2450`,
`Setup.lean:25-110,188-215` and `Util/Path.lean:53-126` before implementation.
Private imports visit the full original import closure and load all available
modern `.olean` parts plus applicable IR parts. The selected five-part layout
preserves both semantic parts and IR without executing project extensions.
`moduleData` reflects the private main-module selection, while effective flags
are computed over the whole import graph. The collector checks their matching
module counts, complete private-data state and resolved direct imports.

Collection uses only explicit runtime-first approved roots and no inherited
`LEAN_PATH`. It imports once with `plugins := #[]`, `loadExts := false`, then
resolves the five-part candidate locators under that same path configuration.
Its report is **not proof that mutable files remained unchanged**. The controller
must validate approved roots, copy/hash/readback exact files to a fresh protected
snapshot and compare a fresh replay's complete structure before later semantic
correspondence. Same-size mutations are not detected by native metadata alone.

Replay builds the complete explicit `ImportArtifacts` map, validates all part
sizes before import and sets `searchPathRef := []`. The selected runtime falls
back to `findOLean` for a missing map key; an empty search path therefore refuses
instead of silently acquiring an omitted project **or runtime** module. Successful
replay additionally requires equality of supplied and actual module census, with
no unused map entries, and rechecks file type/size after import. Exact hashes,
immutable snapshot identity and matching original/replayed flags remain controller
obligations. A peer-provided replay report is not a registration authority.

The runtime's existing `ModuleSetup.importArts` is the preferred later ordinary
frontend connector: it can preserve the exact snapshot resolution independently
of ambient search order, with explicit plugin/dynamic-library policy. This source
does not execute that frontend or introduce source builds/plugin permissions.

### Bounds and evidence limits

Selected refusal ceilings: 4,096 modules, 20,480 parts, 64 MiB per part, 512 MiB
total artifact bytes, 65,536 direct-import edges and 16 MiB report. Root separately
approved 16-MiB replay requests so a full bounded matrix need not fit the original
1-MiB collect request. Native reading/parsing has the absolute 16-MiB ceiling;
collect's 1-MiB limit is enforced immediately after parsing its mode, before any
project import. The controller must prevalidate the selected mode's input cap.

Collection's module/artifact census limits are checked **after** the one native
import; they are not pre-import memory or deserialization limits. Replay's file
size/map bounds run first, but neither mode supplies a hard CPU/memory sandbox.
The later controller's whole-process envelope remains necessary. Report assembly
checks cumulative row bytes and final serialized bytes. Source/layout checks do
not prove mathematical validity, public-view correspondence, frontend usability,
snapshot lifetime or v5 readiness. No follow-on operation is authorized here.

## Shared collector core and strict reference matcher (source only)

2026-10-24 continuation, under the appended root implementation selection.
No compiler, native import, test, owner/catalog operation, snapshot copy or
package adoption was performed by this author. The exporter above is unchanged.

The unused artifact collector was split without changing its declarations or
root `main` behavior. `BaselineArtifactCore.lean` retains the complete old
pre-main source and namespace `OrdinaryLean.BaselineArtifacts`; the existing
`BaselineArtifacts.lean` now imports that core and retains only the same root
`main`. The core introduces no competing executable entry point. Both collector
request/report formats and their refusal ceilings remain unchanged.

| Source in `software/v5/ordinary_baseline/` | Current SHA-256 |
|---|---|
| `BaselineExporter.lean` (unchanged) | `403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e` |
| `BaselineArtifactCore.lean` | `6f160a089fd6e60c34654f7f90417155a94d921a78d7884dec949e4379fd5f28` |
| `BaselineArtifacts.lean` (thin wrapper) | `78abf44c6b2b17e065a03550e5b1af0dbc7020a8d7100bc7312832c73e3ddff7` |
| `OrdinaryReferenceBase.lean` (review candidate) | `5120d6bb7939e32b2c2cd45981dde015d9e041fd9d7a05e11cc453ce5fd3b30a` |

The matcher imports only the shared artifact core, which already imports
`OrdinaryExport` and its established dependencies. It does not import the
different `OwnerRebind` policy/helper or rebuild its dependencies merely to
validate an identity string. Its local identity validator checks exactly 64
lowercase hexadecimal characters; those strings remain controller-authenticated
labels, not cryptographic checks performed by the native program.

### Exact matcher interface

CLI: `OrdinaryReferenceBase inventory replay-map request report`.
All paths are absolute local paths. The first input is the separately pinned
581-row fixed inventory; the second is the collector's explicit replay request,
including runtime artifacts. There is no sysroot or ambient path lookup.

```text
Request = {
  schema:"DMKN_ORDINARY_REFERENCE_BASE_REQUEST_V1",
  semantic_id, foundation_id, context_root, snapshot_id, support_id,
  units:[{unit_id, unit:<complete raw original ordinary unit>,
          outputs:[{name:<encodedName>, export_id:<hex64>}]}],
  targets:[{name:<encodedName>, export_id:<hex64>}]
}
```

Every object uses exactly the selected fields. A current protected controller
must authenticate complete accepted unit/output/import warrants and exact
snapshot/support/input identities before this conditional matcher is relevant.
Neither this parser nor the matcher's report confers those warrants.

The report's exact top-level fields are:

```text
{schema:"DMKN_ORDINARY_REFERENCE_BASE_REPORT_V1",
 assurance:"CORRESPONDENCE_REQUIRES_CURRENT_PROTECTED_WARRANTS",
 semantic_id, foundation_id, context_root, snapshot_id, support_id,
 targets:[{name,export_id}], private_unit_ids:[unit_id],
 public_units:[{unit_id,outputs:[{name,export_id,kind,level_params,
                                projection,kernel_projection}]}],
 private_module_names:[encodedName], public_module_names:[encodedName],
 private_unit_count, private_name_count, public_unit_count, public_name_count,
 unit_array_bytes, encoded_nodes, private_scan_nodes, public_scan_nodes,
 private_edges, public_edges, checked_units:0, added_names:[]}
```

Both projection fields are exactly `full` or `erased_singleton_theorem`.
`projection` describes public frontend lookup; `kernel_projection` describes
the actual exported-import kernel record. No proof body is repeated in this
result. The zero checking/creation fields are intentional: this operation
compares a representation of already warranted mathematics; it calls neither
`checkBatch` nor `addDecl` and creates no mathematical declaration.

### What is compared, and why two public views matter

The request's complete units are decoded in dependency order under only the
fixed basis plus preceding complete outputs, with original descriptor roundtrip
and the existing allowed-declaration rule. Every private output must match its
complete original inventory in both private frontend lookup and the actual
private kernel map. Singleton descriptor/inventory equality is explicit;
inductive/generated completeness is inherited from the actual prior checking
warrant, not guessed by reconstructing a descriptor from installed records.

The fresh soundness audit identified a necessary distinction:
`Environment.toKernelEnv` returns `env.checked.get`; changing `setExporting`
does not select its map. Therefore a successful public `find?` comparison alone
does not establish what the kernel uses. The matcher now explicitly compares
both `publicEnv.setExporting true.find?` and `publicEnv.toKernelEnv.find?` for
every exposed whole-unit output and for all fixed-basis names.

`Export.compareSourceBasis` first matches the private kernel against the
unchanged fixed inventory. Contrary to the weaker type-only relation in a
different helper, the selected `BootstrapProbe.inventoryRow` includes normalized
theorem proof bodies (line 629). The new basis-view comparison then uses actual
matched private original records, not that other helper's theorem interface:

- Definitions, opaques and complete generated computational records match full
  original inventories, including hints, ordered universes and metadata.
- A full theorem matches the full original theorem inventory. Only an original
  singleton theorem with `all = [name]` may instead have a safe axiom-shaped
  public/kernel handle with the same original name, ordered universes and type.
  Private frontend basis records do not get this erasure exception.
- Only the fixed permitted foundational axioms retain axiom kind, exact
  original signature and safety. Quotient primitives retain quotient kind,
  exact original signature and the exact primitive discriminator. Neither
  case passes through the extension codec, which intentionally forbids new
  axiom/quotient extension units.

This preserves the selected checked seed's normalized semantics and adds exact
cross-view original correspondence; it does not replace the seed or enlarge
its allowed axioms. Basis comparisons use the existing per-expression codec
ceilings and the fixed 581-name inventory. The variable unit scan statistics
below do not count basis normalization/serialization work; enclosing process
CPU/memory accounting must still include it.

### Public closure and support-profile limit

Start from explicit target identity/name pairs and visit complete owning units.
For every selected unit, separately match its actual public frontend and
exported-import kernel records. Union their actual semantic references. A full
theorem in either view contributes its proof references; a permitted erased
theorem contributes only type references. Definitions, opaques, recursor rules,
inductive/group/constructor metadata, projection targets and implicit literal
roots retain their exact semantics. Non-inductive historical `all` fields
remain exact metadata but do not invent kernel dependency edges.

The selected profile requires each unit reached by that union to be usable in
both views. This is a sufficient conservative rule: it can refuse a hidden helper
needed by one retained full-proof view even if a more complicated separate-view
closure could support it. A hidden proof helper is omitted only when neither
actual reusable view needs it. The implementation does not silently claim to
support all private/public asymmetries or accept axiom-shaped computational
definitions. Only the derived complete public units become a later delta
frontier; private acceptance alone is insufficient.

Both imports use the exact replay map and empty search path, no plugins and no
extension loading. Private module census must equal the supplied map. The
public active census may be smaller, but every active module and every named
direct dependency must belong to the bound map. Part types and byte sizes are
rechecked after import; exact byte hashes, immutability and current protected
warrants remain live controller obligations. Same-size mutation is not detected
by native metadata alone.

### Matcher ceilings and review state

The whole request is at most 96 MiB; its raw complete-unit array at most 64 MiB;
one unit at most 8 MiB. At most 8,192 private units, 262,144 output names,
262,144 combined private/public per-unit distinct semantic references,
20,000,000 encoded nodes, 20,000,000 combined variable-unit semantic scan visits,
1,024 targets and 32 MiB serialized result are allowed. Public scan visits count
both actual maps, even when their matching records have identical structure.
The existing distinct per-unit codec limits remain in force. Replay keeps its
16-MiB matrix and 4,096-module/512-MiB artifact ceilings. Input files must be
ordinary single-link files; lexical depth, UTF-8 and integer guards precede JSON
parsing. These are refusal ceilings, not claims about local memory sufficiency.

Self-review removed an invalid namespace abbreviation and a record-type name
that would shadow Lean's `Unit`. Independent engineering and mathematical
reviewers received the current candidate hashes above. Their final dispositions
are pending, not assumed PASS. The root owns any subsequent fresh build/run
selection. No source-only result establishes snapshot correspondence at runtime,
ordinary delta operability, useful-growth advantage or deployable-v5 completion.

## First build failure and source-only repair02

Root subsequently selected build01. Its saved terminal result is a clean
`COMMAND_FAILED`, not a completed native build: `BaselineExporter.lean` compiled
to its `.olean`, `.c` and `.o`, but `BaselineArtifactCore.lean` failed because
`meta` is a reserved Lean identifier (the two local binders at lines 243/363).
The matcher had the same local binder at line 155. No collector/matcher import
or reference registration succeeded. Used source and all build outputs remain
preserved; do not alter those bytes to conceal the failed result.

Root selected three fresh source successors, implemented without compilation:

| Fresh source | SHA-256 |
|---|---|
| `BaselineArtifactCore02.lean` | `ff34631ed54114c3919c7f3aa50ced634c1e2bf66496a1ca2f8be12da74d9e0f` |
| `BaselineArtifacts02.lean` | `b77d489c2b8aee6551d422fc4f54b46d5ca7e00defb4adcc557e93a8681d287a` |
| `OrdinaryReferenceBase02.lean` | `252bf83fe5353daab8169a21310eeef1e4b6eed2617e8209d99a260a98192635` |

The only intended source delta is renaming those three `meta` local binders and
their uses to `metadata`, plus routing both executable wrappers' import to
`BaselineArtifactCore02`. Namespaces, API formats, mathematical relation, bounds,
paths and run behavior are unchanged. A source scan of declaration, parameter,
`let`, `for` and lambda binders found no other reserved-keyword binder in the
fresh files. This is not a compiler PASS. An independent reviewer was given all
three hashes for exact-delta review, not a repeated semantic audit.

The build owner was told to reuse the successful exact exporter `.olean/.c/.o`
from build01 and the retained unchanged five shared helpers; only the repaired
core and two executable source modules need compilation. No second build,
native import, admission, snapshot copy or report adoption was run by this
author. The original native candidate's source-theory review cleared its stated
dual-view correspondence assumptions; that review did not guarantee syntax,
successful compilation, runtime correspondence or final-v5 operability.

Independent narrow02 review subsequently compared all three fresh source diffs
and hashes: PASS for exactly the reserved local-binder renames and core import
routing, with no mathematical or report-schema delta. The earlier semantic
source argument transfers conditionally. This does not change the saved build01
failure into a successful build or select another compiler run.

Root also selected the fresh source-only ordinary library fixture
`software/v5/ordinary_baseline/DMKNBaselineFixture.lean`, SHA-256
`bb58ee2a0246e4d33c5c3ebf16df9ee4986be75756d3a3ba597b7f9ad60928d6`.
It contains a modern public Init import, generated `Flag` group, exposed
transparent `flip` using its recursor, hidden proof helper, public simp theorem
and scoped notation. Source syntax/visibility was compared with pinned runtime
examples; no fixture compilation was performed. The separate native-workflow
owner records its exact assumptions and finite future discriminator; no second
harness or duplicate tests were created here.
