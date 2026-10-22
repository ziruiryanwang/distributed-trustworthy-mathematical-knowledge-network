# Installed producer core and public contract: source checkpoint

Author: storage_integration_adapter, 2026-10-22. Source-only under root's
`INSTALLED-PRODUCER-SELECTION.md`. No import, syntax execution, constructor,
test, host, snapshot, request, build, proof or Git operation was performed by
this author. All used originals remain unchanged.

## Exact source set

Physical root: `software/v5/installed_production/`. Installed logical names
are unchanged. Five predecessor sources were copied once into the fresh overlay
and verified equal before editing; the sixth file is new. Unchanged package
initializers are reused from their existing exact selected paths, not copied.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `release_production/adoption.py` | 10818 | `dcedd229c64120beaaf755b2653ff923da2c896f6ed6dd8f103859f8becc2baf` |
| `release_production/producer.py` | 7883 | `a466726b79c9a5851ea4e085307aa5ba593c83e2881dc4e168446cbc4f573b1a` |
| `release_production/operator.py` | 26808 | `f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a` |
| `release_production/launch_contract.py` | 30932 | `ad2e63a2236d52b2507834dce32f77c1dc3fc55f198dbf39382cb1374a95c802` |
| `aggregate_lifecycle/producer.py` | 8947 | `ee5b11911ebb7d77c860c0b441de45257e43fea890b44af248bb669e0a7be7b7` |
| `aggregate_lifecycle/snapshot.py` | 22644 | `c38b6ffc14d47cb35e20eb128db098dda878c0194cbdfd7bb73ed5ce17b91666` |

Root owns `release_production/launch.py`; the distribution author owns its
fresh distribution successor. Their sources are not part of this table.

## Implemented boundary

- Public installed profile has its own schema/domain. Adoption accepts explicit
  V4; the component-only V3 fixture is neither migrated nor relabeled.
- Producer closure expands from 27 to 31: three current verifier dependencies
  and the shared contract. Current receiver verifier/trust files are retained.
- Generic lifecycle gets one protected selection method with its historical
  default. Exactly two generic snapshot call sites use that method. Public
  release subclass selects the new validator and overrides `_local_outer`.
  No callback injection, monkey-patching, evidence fallback, native or scheduler
  change is introduced.
- Shared contract defines the exact 13-field selection, true public outer
  result, fixed copied-entry argv, deterministic external-profile materializer,
  and pure metadata validator. Imports at module scope are stdlib-only.
- Core sources execute from pin-checked held bytes at stable installed origins.
  Entry checks the complete selected Python subtree at bootstrap/finalization.
  Its installed entry pin and actual copied entry bytes must agree. Both full
  `sys.meta_path` and `sys.path` are checked after product imports and at final
  rebinding, not only the last importer.
- Prior launch evidence is checked shallowly and in one-to-one order with inner
  attempts. Public run/preflight additionally require a completed request outer
  that names their exact input. Previous pending or failed finalization refuses
  continuation; no direct-owner bypass exists in this public lane.
- `completed_outer` rejects pending/failure markers. Current-parent
  `validate_worker_report` intentionally does not reject that parent's own
  pending marker, since the parent has not committed yet. It still rejects
  worker/core/failure markers. Root removes pending only at its final commit.
- Public limits agree with parent: output at most 1 GiB / 16,384 entries;
  runtime selection at most 256 pins / 512 MiB; lineage metadata at most
  256 distinct pins / 64 MiB. Conflicting pins are rejected before union.

## Shared API available to parallel authors

```text
SOURCE_MODULES                         # exact31 closed logical names
validate_production_metadata(manifest, descriptor, template) -> None
materialize_profile(root, manifest_pin, descriptor_pin, template) -> profile
read_selection(path, expected) -> (selection, pin)
validate_selection(selection, selection_pin, *, fresh_run) -> selected namespace
rebind_selection(selected) -> None
command(selection, copied_selection_pin) -> fixed argv
validate_worker_report(selection, copied_selection_pin, worker_pin) -> worker dict
completed_outer(outer_pin, *, pins=None) -> shallow completed-operation namespace
selection_for_owner(owner, selection_pin, configuration_pin, cfg, table)
outer_for_owner(owner, outer, selection, selection_pin, outer_pin)
```

`fresh_run=True` accepts the external original plan pin while requiring fresh
run/action output. False permits existing run/action output, for execution or
retained data; the entry/core separately enforce no-output-before-action.
`command` always binds the actual copied `RUN/selection.json` pin.

Public profile bytes must equal materialization of the adopted release template,
not merely claim the release's schema. The template pin is checked as parent
metadata, not added to the core constructor's repeated pin union. Thus expected
operative count remains 60. Exact assembly counts are still an independent gate.

## Review status and remaining verification

The design review passed its source-design scope. Independent source review is
in progress; this table is a checkpoint, not a source approval or executable
qualification. Two early review findings were fixed before this checkpoint:
parent/helper output-limit mismatch and runtime-over-metadata pin overwrite.
The later import-policy finding was also fixed by complete importer-list checks.

No full public producer, generic installed snapshot or proof is qualified by
this source. Root separately selects changed-boundary controls and actual
installation. These authored bytes should now remain stable pending concrete
review findings; do not spend time repeating prior component tests.

The reserve review found that the new entry/report maxima needed tightening.
Both are now bounded to64KiB in the helper, actual entry and parent. Existing
future maxima are diagnostics8MiB +inner result1MiB +outer2MiB +staging1MiB
+stdout1MiB +command64KiB +invocation64KiB =13.125MiB. Adding two64KiB public
files gives13.25MiB, inside the unchanged14MiB pre-layout reservation. This is
an initial-distinct-input-set plus future-maxima argument, not a total physical
read claim or a claim that the final session table lists all public evidence.
The helper separately remembers copied-entry and produced-report evidence in
its bounded shallow public-evidence table; no scheduler table/budget changes.
