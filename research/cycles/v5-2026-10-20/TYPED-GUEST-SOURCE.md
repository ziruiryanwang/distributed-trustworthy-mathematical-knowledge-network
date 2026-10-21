# Typed guest: four-crate source preparation

2026-10-21; core_growth. Source-only work selected by
`CENTRAL-RENEWAL-IMPLEMENTATION-SELECTION.md`. No Python product import, build,
guest execution, test, proof, RAM survey or Git mutation was performed.

## Ready for independent review

| New file | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/typed_guest/recipes.py` | 8907 | `c938f63f27dd01d7f08a0f3693048d3a6882fca00b6c8220a934f07b3513fb42` |
| `software/v5/typed_guest/build.py` | 23040 | `95903977ce10180480587163102a3c7c4ce98df9191dee93072be71747b2a9ba` |

Both are fresh successors; the used proof-memo and typed-native sources remain
unchanged. Root owns the selector, assembler and any operation selection.

## Exact integration interface

- Selection schema: `DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_V1`.
- Run name: `typed-guest-build-01`; fresh run and attempt record are mandatory.
- Seven selection keys: `schema`, `name`, `adapters`, `production_sources`,
  `retained_artifacts`, `limits`,
  `authorizes_four_compiles_and_retained_artifact_adoption`.
- Two adapters: the new build and recipe files above, exact byte/hash pins.
- Result schema: `DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_RESULT_V1`.
- Successful status: `PASS_TYPED_GUEST_FOUR_CRATE_COMPILES_ONLY`.
- Recipe schema: `DMKN_V5_TYPED_GUEST_FOUR_CRATE_RECIPES_V1`.
- Source map keys: `source_snapshot`, `project`, `compiler_read_sources`,
  `adapters`.

`project` is the exact 37-file selected source snapshot. It is derived from the
adopted 39-file native typed source selection by removing its builder and two
test entry/control files, then adding the unchanged aggregate guest entry.
The old `bounded_parse/census.rs` remains selected historical comparison support;
it is not part of the production guest's 36-file reachable source closure.

`compiler_read_sources` is that source-inspected 36-file closure, following the
existing source-map interface convention. It is **not an observed dep-info
measurement**; the result explicitly records
`DECLARED_STATIC_SOURCE_CLOSURE_NOT_DEPINFO_OBSERVATION`. Rust dep-info is emitted
by the four unchanged-style recipes but not parsed into an unverified claim.
The copied source tree is checked for exact selected file membership before
compilation and again during finalization.

## What changes in compilation

The recipe retains the exact 297-unit graph, target, 236 dependency artifacts
(107 matched target rlib/rmeta pairs and 22 host macro DLLs), O3/fat-LTO guest
profile, overflow checks, panic-abort and genuine aggregate entry. Total retained
artifact bytes remain 311693039; compiler runtime selection remains 26 files.

Only three crate roots change to `typed_rows/checker_lib.rs`, `module_lib.rs`
and `aggregate_lib.rs`. The fourth compile uses unchanged `aggregate/main.rs`.
Fresh outputs, metadata `dmkn_v5_typed_guest01_*`, exact dependency order and
extern mappings prevent linking the old project libraries. There is no Cargo,
graph rerun, third-party compilation, backend/C++ build or source-rule change.

The selected source closure includes the typed parser/correspondence and literal
legacy fallback, exact foundation data, retained kernel, module semantics and
aggregate header/membership/wire. Native typed source/equivalence evidence is
explicitly pinned rather than repeated. The builder binds the adopted native
build/selection/source-map/attempt, normal eight-control closure and matching
native test binary identity. Those controls establish only their previous native
scope, not that this new guest has built or become faster.

## Limits and failure boundaries

Retain the predecessor's finite build limits: 240 inclusive worker CPU seconds,
300 worker-phase wall seconds, six processes, 4096 MiB Job allowance; ordinary
controller 40 CPU seconds, finalization ceiling 60, whole adapter 420 wall seconds;
512 MiB sampled output envelope, 4096 entries and 8 MiB command log cap. These are
resource ceilings, not forecasts or a request to scan/reconfigure PC memory.

Each selected dependency and source is rebound before copying and after closure.
Output uses fresh files/directories. Normal/failure finalization closes the shared
Job, preserves actual compiler counts and requires no live/terminated children
for success. A finalization override remains authoritative. Failed work is not
retried or erased. Outer root supervision still owns process-exit/report tails;
sampled disk bounds are not an OS quota or hostile-input sandbox.

The builder produces a user ELF and link map, not an assembled image, certificate,
accepted theorem or measured speedup. Root's new assembler must bind this exact
result and actually compute A-prime before a newly bound matched execution.
The complete-proof decision and reusable prefix/final endpoint are in
`CERTIFIED-RENEWAL-NEXT.md`, not implicitly authorized by compilation success.

## Narrow author review

The new recipe was compared against the retained recipe: source roots, run name
and metadata change; graph/profile/dependency logic does not. The builder's
changed evidence and source-selection blocks were reread, as was root's matching
selector. One 63-character selector evidence-hash typo was reported to root
before execution; its correction belongs to root. No syntax/runtime test was
performed under this source-only assignment. Independent source review and a
fresh root runtime selection remain required.
