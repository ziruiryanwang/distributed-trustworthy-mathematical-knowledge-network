# Direct current-release builder: source checkpoint

2026-10-26. Implemented after root adopted the exact release-map gate. No
product import, build, compiler invocation or experiment has been performed.
The only Python invocation parsed source with standard-library `ast` and
hashed source bytes; it did not import or execute either builder.

## Exact inputs and delta

New `build.py`: 32,799 bytes, SHA-256
`86612e8c76cf7281e942ea9e55705ba53de85d2c6efb45950561532997055d03`.

Frozen predecessor `ordinary_bounded_operations/build.py`: SHA-256
`79a056932d5720e9ab964ee50a01d1b04569a60a5e6445df0070a2b6556b42f9`.

Exact selected `release.json`: SHA-256
`821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78`.

The successor changes only selection/assembly bookkeeping in the existing
`build` function, its introductory description and three selection constants
(source prefix, map pin, eight-document set). It is not a generic build engine.

- Load the pinned release's `build` section instead of the historical source
  map. Keep the fixed lower-builder path and SHA-256 unchanged.
- Require the source set to equal the union of the lower builder's unchanged
  47 fixed inputs, direct-copy sources and ordered compiler-lane sources.
- Derive the disjoint direct/receiver/authoring/query/extractor/manifest role
  sets; check their union against the manifest's prebuilt **names only**.
- Independently derive and check the 93 sources, 72 direct copies, 153 files
  before PROFILE, 117 auxiliary roles and eight documents against map counts.
  Fixed 45 noncompiled pins must match their selected source pins. Native
  auxiliary roles are exactly the declared 72 names.
- Use the map's already-combined 23 runtime pins and require the lower
  builder's nine named pins as an exact subset. Do not add those nine twice.
- Snapshot all 93 build inputs plus this actual builder and `release.json`.
  Recheck originals and snapshots before final profile commit.
- Assemble and verify the derived exact output-role set, with actual compiled
  outputs and the lower builder's actual INSTALLATION identity. Generate fresh
  PROFILE from the actual 117 auxiliary file pins. Prebuilt hashes do not
  become fresh-build acceptance conditions.

The lower builder, native workers, transforms, compilation order, compiler and
linker arguments, environment isolation, allowances, Job containment, accounting,
failure retention and PROFILE-last commit order are unchanged. The archive's
new support sources remain pinned by its outer manifest, avoiding self-hashes.

## Structural unchanged-function evidence

Standard-library AST parsing succeeded for both source files. Comparison used
`ast.dump(..., include_attributes=False)` so line-number shifts were ignored;
function bodies, arguments, constants and statements were compared structurally.
Top-level function-name sets and nested build-function-name sets are equal.

| Scope | Structurally unchanged functions |
|---|---|
| Top level | `need`, `bootstrap`, `relative`, `legacy_view`, `extractor_worker`, `query_worker`, `main` |
| Nested inside `build` | `check`, `mkdirs`, `copy_exact`, `read_json`, `child_grant`, `run_child` |

`build` is the only changed top-level function. There are no changed nested
functions. This is source-delta evidence, not execution or compiler correctness.
The receiver/authoring compile worker lives in the unchanged selected lower
builder; the extractor/query workers above are unchanged.

## Public contract retained

Invoke the selected Python with `-I -S -B`, then the new builder and required
`--source-root`, `--python-runtime`, `--lean-runtime`, `--output`,
`--wall-seconds`, `--cpu-seconds`, `--memory-mib` arguments. Output must be fresh.
No runtime download or source approval is implicit.

Successful output remains `<output>/package`, with the receipt at
`<output>/_build/BUILD-RESULT.json` and the same JSON result on stdout. Status
remains `BUILT_NOT_ADOPTED`; claim remains
`SOURCE_BUILD_AND_ASSEMBLY_NOT_OWNER_OR_MATHEMATICAL_ACCEPTANCE`.
Actual `profile_sha256`, `installation_manifest_sha256` and `implementation_id`
are recorded; counts become 153 files excluding PROFILE and 117 auxiliary
files. The retained `source_map_sha256` receipt key now names `release.json`.
Failure preserves partial output and original allowance accounting.

Independent changed-boundary review and root's explicit finite execution
selection are still required. This source checkpoint authorizes neither.
