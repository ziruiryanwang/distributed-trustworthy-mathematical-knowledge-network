# Two finite supervised-generation selections: source only

2026-10-21, core_release. Root assigned this preparation-selector source after
receiving the supervised-generation implementation. No selector invocation,
allocation, product import, process launch, deletion, installation or Git action.
Independent source review and root's exact finite preparation/launch remain.

`Select-SupervisedGenerations01.ps1`: 7783 bytes, SHA-256
`c7f8c7ec5db2db496b5788eafb0911d2a2270b0a7dee778d7e22f82321825992`.
Derived from the frozen `Select-BoundedReclamation01.ps1` preparation pattern;
the predecessor remains unchanged. This script prepares selection JSON only.
It does not invoke the unchanged `tools/Run-V5-Check.py` runner.

## Interface and exact source map

`-Mode Controls|Crash -ReviewedSourcesJson <reviewed exact JSON hash map>`.
Canonical working directory is mandatory. Both modes refuse existing selection,
input or operation-output paths and use exclusive CreateNew writes. They do not
reset/reuse any predecessor allocation or output.

The caller-reviewed map has exactly four keys:

- `placement/lifecycle.py` and `placement/sessions.py` from the fresh
  `software/v5/supervised_generations/` directory.
- `placement/reclaim.py` from the unchanged `software/v5/bounded_reclamation/`.
- `tests.py` for Controls, or `crash_smoke.py` for Crash, from
  `software/v5/supervised_generations/`.

All four are hashed before preparing the selection. The fixed unchanged runner
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`
is the fifth snapshot source. Canonical relative paths are preserved. The script
does not hardcode still-unreviewed adapter/test hashes; root supplies their final
adopted hash map after independent source review.

## Runtime scope and costs

Both modes authenticate the adopted installed release `1fd0ae63...`, its original
build input `8ba37072...`, and all 121 SDK source bindings against both maps.
They reuse exactly the 18 installed Python runtime pins from frozen selection
`04522d4b...`; that selection is read only as authenticated Python-pin metadata,
not as an instruction to rerun its workload. Common runtime-pin count is
121 + 18 + 3 metadata files = **142**. There is no recursive runtime scan or
842-MB distribution rehash.

Crash additionally pins the frozen v4 manifest `a93714ec...` and its exact
operator, Job and domains sources, then the freshly prepared input: **147**
runtime pins. No Node, Lean, receipt, basis-proof or placement-config fixture is
opened/selected. The two fresh names and outer budgets are:

| Mode | Allocation name | CPU seconds | Wall seconds | MiB | Processes |
|---|---|---:|---:|---:|---:|
| Controls | `supervised-generations-controls-01` | 30 | 60 | 256 | 2 |
| Crash | `supervised-generations-crash-01` | 30 | 120 | 256 | 4 |

Each stdout/stderr bound is 1 MiB. Controls invokes installed Python with
`-I -S -B`, the snapshot `tests.py`, `--output {output}` and exact `--release-sha`.
The controls author explicitly confirmed this CLI and exact 121+3 module map.

Crash writes `DMKN_SUPERVISED_CRASH_INPUT_V1`, with exactly the three additions
`v5/placement/lifecycle.py`, `v5/placement/sessions.py` and
`v5/placement/reclaim.py`, each with reviewed bytes/SHA-256. It invokes installed
Python `-I -S -B`, snapshot `crash_smoke.py`, `--output {output}`, `--input` and
`--input-sha`. The root-owned adapter retains its separate original 90-second
deadline and inner 10 CPU / 30 wall / 128 MiB / two-process Job plus 25 seconds
of prospective cleanup; these are not renewed by the selector.

Any actual control pass or real quiescence/retirement claim requires the separate
reviewed execution and outcome audit. Source preparation alone establishes none.
