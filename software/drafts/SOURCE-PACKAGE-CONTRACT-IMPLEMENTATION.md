# Offline source-package contracts: implementation handoff

2026-09-21. **Authored, not imported, parsed, executed or qualified by the author.**
Root alone may execute after independent source, registry and exact-launch review.
Only this note and `tests/test_source_package.py` were authored; no builder,
product, runner, registry, allocation or retained evidence was modified.

## Selected source and proposed allocation

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/test_source_package.py` | 25,894 | `8B1CB07AA9FAB00F0DC1FED51662B948DC354003246C483FA9C089A9AFC1029B` |
| `release/package_source.py` | 14,011 | `8062FE2B4D9CC75279F512FC288727617CCC4017DEA1B74F5A1A10FD2286E837` |

The suite verifies the selected builder's byte count, SHA-256 and resolved module
origin before importing it directly by file path. No product/node/math module is
imported. All other imports are from the Python standard library. The external
`DTMKN_TEST_ROOT` must exist, be absolute, have no observed link/reparse ancestors,
and be disjoint from the installation tree. The suite and each method create a
fresh child directory, without deletion, cleanup retries or allocation reuse.

Proposed existing `run_state_contracts.py` registry entry:

```python
"test_source_package.py": {
    "scope": "offline source-package contracts; inert source fixtures and explicit path/change injection mocks; no native acceptance or authentic public CLI qualification",
    "tests": 10,
    "prefix": "source-package-contract",
    "sources": ("release/package_source.py",),
}
```

Exactly ten `test_` methods are authored; parameter cases are subtests, not hidden
new unittest methods. Proposed limits remain the existing 60-second wall,
30-second Job CPU, 512-MiB memory, eight-process profile, with 256-MiB / 4,096-file /
8,192-entry retained endpoint. Five common runner input roles plus one selected
builder plus the suite give seven ordered input pins; the launch is an eighth
supervisor pin. Root must generate, review and freeze a fresh launch separately.

## Independent fixture and coverage

Each ordinary source fixture has exactly 108 selected payloads: two entrypoints,
19 Python files, three Lean files, 75 assets, one lock, five operator documents,
two release files and one selected quickstart. The fixture names are independently
listed in the test, rather than obtained from the imported builder. Five common
manifests, two foundation files and 68 small object files give 75 assets; the six
locked code/native paths bring the lock to 81 rows. All are harmless synthetic
bytes. Their Python/Lean suffixes never cause execution or mathematical checking.

| Method | Intended discriminator |
| --- | --- |
| `test_01_archive_members_hashes_and_determinism` | Two real packages of identical bytes agree completely; independently reconstruct 108 manifest rows and hashes, 109 ZIP members, fixed metadata, external manifest/result bindings and explicit non-release flags. |
| `test_02_quickstart_export_repackage_and_exclusions` | Real ZIP extraction changes draft quickstart location to top-level `QUICKSTART.md`; extracted-tree repackage is byte-identical; sentinel runtime/state/tests/other draft contents are excluded. |
| `test_03_exact_selected_trees_reject_missing_and_extra` | Six fresh trees: missing and extra entries in each of `py`, `native`, `assets` refuse. No fixture file is deleted to create a missing case. |
| `test_04_asset_lock_paths_pins_duplicates_and_types` | Ten retained JSON variants exercise boolean schema/count, hash shape, duplicate path/key, traversal, uppercase object name, extra key, row count and required membership; two actual source trees have schema-valid but incorrect content hash/size pins. |
| `test_05_ambiguous_or_missing_quickstart_refuses` | Neither selected quickstart and both selected quickstarts each refuse. |
| `test_06_real_per_file_and_aggregate_byte_bounds` | Real 2-MiB input succeeds, real 2-MiB-plus-one input refuses; nine unlocked selected files of 2 MiB each cross the real 16-MiB aggregate bound. Limits and sizes are not mocked. |
| `test_07_windows_namespace_and_mocked_reparse_guards` | Drive-relative, relative, UNC, device, root, parent traversal, ADS, reserved name and trailing-dot/space spellings refuse; ordinary paths work; a narrowly mocked reparse attribute exercises its rejection branch. |
| `test_08_main_freshness_overlap_origin_and_mocked_alias` | Existing output is unchanged; lexical overlap in both directions, wrong selected entrypoint, and an explicitly mocked canonical output-parent alias refuse before output creation. |
| `test_09_observed_source_change_preserves_failed_output` | A hook at the second shape check mutates this method's owned README, with original bytes retained. Main refuses, preserves the already-written ZIP plus failure marker, and writes no success/external manifest. The ZIP still has the originally captured README. |
| `test_10_archive_member_corruption_preserves_failed_output` | An injected first-verification-read hook retains the original ZIP, then really appends an unselected member. Main refuses its changed member set, retains the altered ZIP/failure marker and writes no success/external manifest. |

Main-flow tests replace the packager's `__file__` with the inert fixture's selected
entrypoint when needed, and capture argv/stdout. They **do not execute that file**
and do not qualify authentic executable origin. The wrong-origin case leaves the
actual imported module origin unchanged and requires refusal. Authentic public
CLI invocation of the actual selected source remains a separate allocation.

The reparse and canonical-parent alias branches are explicitly mocked; no OS
alias, junction or symlink is created and no real alias/reparse qualification is
claimed. Source mutation and ZIP corruption are genuine owned-file writes, but
their timing is a deterministic injected boundary, not an independently timed
filesystem race. ZIP corruption here means an unexpected valid ZIP member, not
a CRC-bit-flip, truncation or torn write. The source-change ZIP is complete as a
ZIP but is only partial/uncommitted package output because revalidation failed.

## Retention and scope

All fixture files, malformed locks, original mutation/corruption bytes, package
outputs, captured main replies and ten per-method reports remain. Census hashes
every method's files before its report; it bounds entries at 4,096, files at 2,048,
each file at 2 MiB plus one byte, and per-method bytes at 64 MiB. Reports are capped
at 192 KiB. The suite's fixed construction is approximately 2,000 files, dominated
by the 18 small selected-tree copies (including the extracted source). The bound
test adds 22 MiB plus one byte of deliberately large input data; total retained
bytes are comfortably below the proposed 256-MiB endpoint. These are construction
estimates, not execution measurements; the runner's actual complete endpoint
census and Job accounting remain authoritative.

Every report asserts that no module under the product `py` directory was imported.
There is no subprocess launch, native tool, socket, database operation, dependency
installation or network call in the suite. A pass would qualify these narrow
packaging contracts under the selected runtime; it would not establish actual-
source packaging, public installation, mathematical validity, useful growth,
independent-host service, hostile-filesystem isolation or release readiness.
