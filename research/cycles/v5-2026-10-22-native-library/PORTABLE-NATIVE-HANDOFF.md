# One native extension above the imported portable parent

2026-10-23. `portable_local_import`. Source-only handoff; no controller, test,
Lean, compiler, migration, native worker or catalog operation was launched.
The sole implementation edit for this task is
`software/v5/ordinary_lean/run_portable_extension.py`.

## Purpose and mathematical input

This discriminator checks the exact imported-snapshot/new-native-child seam.
It uses the adopted complete theorem
`DMKN.ReadFootprint.Consumer.snapshot_predicate_applyBatches` and introduces
exactly one new name:
`DMKN.ReadFootprint.Portable.snapshot_predicate_applyBatches_alias01`.

The input unit comes from the imported audit's unique target-name output entry,
never from a guessed ordinal. Its exact V2 UnitID/export is matched to the
protected parent binding. Its original universe parameters and type DAG are
retained in both descriptor and inventory. The new proof DAG has one constant
node naming the accepted target, instantiated with those same ordered universe
parameters. The complete external-name census resolves against the parent;
the resulting canonical V2 envelope is inert until actual checking succeeds.

This proves no novelty, discovery or useful-growth claim. It tests one new
kernel-checked unit above the retained native parent without rebuilding the
basis, recompiling helpers or replaying accepted proof terms. Existing native
snapshots are restored by the unchanged adopted worker. Reading/copying/hashing
retained evidence and parsing the one target unit are metadata costs, not proof
replay, and are still included in the operation's finite cost.

## Exact invocation and manifest

```text
python -I -S -B <selected snapshot>/software/v5/ordinary_lean/run_portable_extension.py
    <fresh output directory> <parent manifest path>
```

The output is under canonical `experiments/v5-local-checks`; the outer runner
supplies its source snapshot and `selection.json`. The source parent is fixed
to `ordinary-portable-import-01/portable-catalog`. Runtime is unavailable until
that import has actually completed and root has adopted its result.

The canonical parent manifest has exactly these fields:

```text
schema = DMKN_ORDINARY_PORTABLE_EXTENSION_PARENT_V1
source_directory, store_id, parent_root
implementation, source_manifest, correspondence, import_selection
directories: [relative path, ...]
files: {relative path: {bytes, sha256}, ...}
target_evidence: relative path
```

The four named records use `{path, bytes, sha256}` with absolute paths. They
are the actual import's `IMPLEMENTATION.json`, `SOURCE.json`,
`CORRESPONDENCE.json`, and preserved `selection.json`. `target_evidence` is
derived by selecting the exact target-name output in the imported `audit.json`;
the controller repeats that binding check. All source catalog directories/files
must be listed exactly, with no journal/WAL/SHM, redirection, hardlinks, omitted
entries or additional files. Bounds are 8192 files, 128 directories, 128 MiB per
file and 512 MiB copied bytes.

The driver acquires the existing source owner lock without rewriting it and
creates one fresh verified private copy at `<output>/portable-extension/catalog`.
It never opens the original catalog for mutation. The copied database is the
only extension destination. This preserves used experiment evidence; copying
the whole store is not the intended per-contribution product workflow or a
claim about scalable ordinary contribution cost.

## Source and runtime identity

The first import's implementation controller source map must include the final
`run_portable_extension.py` before that implementation identity is frozen. At
extension time, its controller-support hash is recomputed from the preserved
import selection's complete `sources` map. These six executing source files
must match both the extension selection and that preserved implementation map:

- `ordinary_evidence.py`
- `ordinary_semantics.py`
- `local_catalog.py`
- `portable_evidence.py`
- `portable_catalog.py`
- `run_portable_extension.py`

No new supporting executable controller file is introduced. The old
`ordinary-native-admission-01/sources/software/v5/ordinary_lean/run_native_admission.py`
is reused only through its already adopted exact adapter-support source hash:
bounded writer, clean-worker predicate, authored-file helper, and the unchanged
`--worker` entry. Original kernel/adapter/basis digests are recomputed and matched
to I; actual source, compiled objects and named runtime binaries are verified.
The exact old three build directories are censused to exclude module shadowing.
No helper build or compilation command is present.

The extension selection's `runtime_pins` must cover:

- The parent manifest and its four named metadata paths.
- Every actual path in `SOURCE.json`'s `check_support`, including original
  `PROFILE.json`, old sources/objects and named native binaries.
- The original native-admission `selection.json`, whose fixed SHA-256 is
  `ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f`.
- Its retained `sources/tools/Run-V5-Check.py`.
- The same original Python executable, `python314.dll`, and `python3.dll`.

Catalog files are authenticated by the pinned exact parent manifest. The old
worker path is already one of the support pins. The reused supervisor release
and its files are validated through the old runner's exact release commitment.
Native binaries and copied files are hashed in 1 MiB chunks. Selected unique
input bookkeeping is capped at 16384 files and 1 GiB.

## Actual-event boundary and preservation

The copied catalog is reopened under its exact original implementation/store
identity and limits. It must expose five modules and 3629 bindings, the recorded
import's exact source-manifest/correspondence hashes, and its selected final root.
The new live grant commits the one V2 UnitID, ordered batch hash, raw-unit output
census, immutable parent plan and actual stored parent module name. The plan's
`basis_module`/`root_module` come from the authenticated V2 context, never by
deriving an imported module name from its new portable local-root handle.

The single supervised call uses the original worker's `extend` path. A clean
Job exit is necessary; the report must name the exact new module and original
parent module, exactly the alias, exactly one checked unit and the exact bounded
artifact size. Selected inputs and source parent are reverified before the
private commit. The catalog independently validates the live grant and sole
artifact, then atomically commits a `native-check` origin under I. Reopen must
preserve the complete expected 3630-name map and six-module context.

The operation ceiling is selected by root: CPU 30–120 seconds, wall 60–180
seconds, memory at most 1536 MiB and at least three enclosing process slots.
The controller leaves 10 CPU/20 wall seconds for outer closure, passes only the
remaining fixed budget to one worker, and checks that the live grant does not
extend the original deadline. The worker receives two process slots, bounded
logs and an 8 MiB artifact reservation. No allowance is renewed.

Failures retain the private copy, logs, artifacts and charged reservation. An
uncertain commit closes the catalog; there is no retry or native replay. Only
an actual successful run can write `portable-extension/EXTENSION-RESULT.json`,
with status `PASS_ONE_ACTUAL_NEW_NATIVE_UNIT_OVER_IMPORTED_PARENT`. The result
explicitly excludes novelty, discovery, growth and release claims.

Independent source review and the root's later finite selection remain required;
this checkpoint contains no runtime result.
