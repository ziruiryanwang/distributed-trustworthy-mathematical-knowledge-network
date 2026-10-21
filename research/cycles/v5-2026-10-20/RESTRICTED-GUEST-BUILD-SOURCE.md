# Restricted-composition guest build source

2026-10-21, growth. Source-only implementation under root's
`RESTRICTED-COMPOSITION-GUEST-PREPARATION.md`; independent review remains due.
No Python product import, syntax check, compiler call, guest execution, proof,
RAM survey or retained-evidence rewrite was performed by this assignment.

## Implementation and reuse

`software/v5/restricted_guest/recipes.py` derives exactly three explicit rustc
commands from the retained typed guest recipes, preserving their recorded
target/profile/SDK flags. It does not reconstruct or run Cargo's graph:

| Label | Crate | Fresh source root | Outputs |
|---|---|---|---|
| rc-core | dmkn_rc_relation | restricted_composition/lib02.rs | rlib, rmeta |
| aggregate | dmkn_aggregate_relation | restricted_composition/aggregate_lib.rs | rlib, rmeta |
| guest | dmkn-aggregate-claim-guest | aggregate/main.rs | ELF |

The 12-source snapshot uses the corrected native `lib02.rs` and
`foundation02.rs`, seven remaining RC production files, unchanged aggregate
header/membership, and unchanged guest entry. Native build01's missing
parenthesis and failed outcome remain untouched. Actual build02 and all 40
native controls, including the 26 intended refusals, must pass before root
can select this build.

The builder copies only the four original module/Nanoda guest artifacts
(11,986,341 bytes) into an isolated project-library search directory. It uses
the existing exact 236-file filtered dependency view (311,693,039 bytes) in
place. No module, general checker, standard library, SDK or dependency is
rebuilt. The original broad dependency directory is not put on the search
path. The 26 retained compiler inputs are also pinned. This specifically
avoids repeating setup that already succeeded.

The native original module helper correspondence uses the pinned
`proof-validation-integration-build-01/source-map.json`, not the new RC-only
native map. The original guest artifacts and source-map are separately
pinned. Native differential controls remain implementation evidence, not
receipt authority or a proof of all mathematical refinement obligations.

## Selector interface

The root-authored selection has exactly these fields:

```json
{
  "schema": "DMKN_V5_RC_GUEST_THREE_CRATE_BUILD_V1",
  "name": "restricted-guest-build-01",
  "adapters": {"two relative source paths": {"bytes": 1, "sha256": "..."}},
  "production_sources": {"12 relative source paths": {"bytes": 1, "sha256": "..."}},
  "native_adoption": {
    "build": {"path": "absolute native RESULT.json", "bytes": 1, "sha256": "..."},
    "controls_outer": {"path": "absolute controls RESULT.json", "bytes": 1, "sha256": "..."},
    "controls_inner": {"path": "absolute controls evidence/result.json", "bytes": 1, "sha256": "..."}
  },
  "limits": {},
  "authorizes_three_compiles_and_retained_artifact_adoption": true
}
```

The placeholders are explanatory, not executable selection bytes. Native
paths are fixed to `restricted-composition-build-02` and
`restricted-composition-controls-01` under `experiments/v5-local-checks`.
Native result/selection/source-map/attempt links and clean final Job state
must agree; the actual inner controls must identify the compiled executable.

The exact limits are worker CPU 240 seconds, worker wall 300 seconds,
4096 MiB, six active processes, ordinary-controller CPU 40 seconds,
finalizing-controller total CPU 60 seconds, total wall 420 seconds,
268,435,456 fresh bytes, 2,048 fresh entries and 8,388,608 command-log bytes.
The 60-second controller limit includes earlier controller CPU; it is not
another 60-second allocation. The reused filtered view is read/pinned, not
charged as fresh copied output.

## Saved interfaces and outcomes

- `INPUT-MAP.json`: `inputs` (absolute paths to byte/hash pins),
  `existing_dependency_view` (typed retained directory),
  `existing_dependency_files` (236 relative pins),
  `copied_project_artifacts` (four basename pins).
- `SOURCE-MAP.json`: `source_snapshot`, `project` (12 relative pins),
  `compiler_read_sources` (same 12), `adapters` (two relative pins).
- `RECIPES.json`: schema `DMKN_V5_RC_GUEST_THREE_CRATE_RECIPES_V1`, basis
  `RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV`, and `recipes`
  (three rows with label/name/argv/source/output/metadata_output/
  fresh_metadata/kind).
- `RESULT.json`: schema `DMKN_V5_RC_GUEST_THREE_CRATE_BUILD_RESULT_V1`.
  Successful status is `PASS_RC_GUEST_THREE_CRATE_COMPILES_ONLY`; `outputs`
  contains five basename pins. Actual launched compiler count must be three.
  Failure, cleanup failure or finalization override prevents successful
  adoption. Build success is not image assembly, execution or certification.

The builder preserves failure accounting, closes the shared worker Job,
checks zero surviving/terminated processes for success, rechecks all selected
inputs and snapshots, and records output census plus controller/worker
accounting. The source-closure count is explicitly a declared static closure,
not an assertion that dep-info was independently parsed.

## Source pins for review

| File | Bytes | SHA-256 |
|---|---:|---|
| restricted_guest/build.py | 22182 | 79a19fb822cbaed734f737e723ac9a2eabcfc8b0f13256ca1814ed728dcdff02 |
| restricted_guest/recipes.py | 4415 | b2fc5d26e4504c4caf8a41c62ff47048daf13dd2c3653af8a67f7ef8e09903ed |

Root retains ownership of selection, invocation, assembly, outcome adoption
and Git. The prospective paired execution thresholds remain those in the
preparation note; this source checkpoint changes none of them.
