# Restricted guest: retain the adopted checker, rebuild the original module

Date: 2026-10-21. Author: core_growth. Source-only decision and self-review;
root owns runtime selection and adoption. Independent adaptive review is required.

## Decision and payoff

Use fresh `restricted_guest/build03.py` and `recipes03.py` for four project
compiles: original module relation, restricted-composition core, restricted
aggregate relation, unchanged guest entry. Reuse only the already adopted
Nanoda rlib/rmeta pair and the existing filtered dependency view. No Cargo,
dependency/general-checker rebuild, guest execution, proof or image adoption is
authorized by this note.

The competing three-compile route would need new adoption of two intermediate
module binaries from a historically failed operation. The existing independent
validator does not cover that claim. One small module compile is simpler than
creating a new artifact-adoption exception. The previous typed module compile
cost 4.984375 worker CPU seconds and 2.0924277 wall seconds; that is supporting
evidence of an affordable route, not a prediction for the original module.
The unchanged finite envelope remains sufficient for selection purposes.

This work advances the cost discriminator for exact-target certification. It
does not repeat a proof campaign, survey RAM or change mathematical acceptance.

## Historical failure remains a failure

`aggregate-guest-compile-01/RESULT.json` has SHA-256
`81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a`.
Its overriding `FINALIZATION-FAILED.json` has SHA-256
`d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54`.
The operation's effective status is `FAIL_FINALIZATION`, with
`REMAINING_TOTAL_ENVELOPE`. Its completed compiler child does not remove that
failure. Build03 requires the exact preserved failure marker; it never requires
that marker's absence or adopts the old raw success as an operation success.

The later `aggregate-artifact-validation-01` independently establishes only
source-bound ELF/map lineage. Its inner status is
`PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY`, expressly retaining
`old_failure_preserved=true`, `prior_budget_met=false`,
`prior_effective_status=FAIL_FINALIZATION`, and `mathematical_admission=false`.
It does not adopt every intermediate rlib. The new build therefore does not use
the old module rlib/rmeta at all.

The preceding restricted guest01/02 attempts failed before any compiler; their
sources and failure evidence remain untouched. This is a fresh successor, not a
silent retry or an edit to either consumed adapter.

## Reuse authority and source closure

The successful `bounded-parse-direct-build-01` separately adopted these exact
checker artifacts:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `libnanoda_lib-7f1af4fb875deccc.rlib` | 6360054 | `8ec342c7f606b9ccf34cdd5fbf4bf86cd75f6239fd2cd025c7d837d442cf5fde` |
| `libnanoda_lib-7f1af4fb875deccc.rmeta` | 2446327 | `d5266e9ea875433bff5b2c4f084ee48f64be6d5bb6104316a44096a85cc7d62e` |

Build03 copies them from that successful operation's `retained/libraries`, not
the failed original directory. The direct operation's selection and INPUT-MAP
contain matching pins; its result binds the exact original selection and clean
terminal attempt. Result SHA-256:
`694d205b63082ecd02536eb70b16ae08a271f06d66d5df95f296a51a607ce22b`.

The original module's full compiler-source closure is nine files in
`software/v5/modules/receipt/src`: `lib.rs`, `canonical.rs`, `input.rs`,
`foundation_static.rs`, `foundation_data.rs`, `commitments.rs`, `journal.rs`,
`policy.rs`, and `relation.rs` (117760 bytes total). `lib.rs` declares seven
modules; the static foundation includes `foundation_data.rs`. All nine match
the original native source map, the original guest project map and current
canonical source bytes. The validator's exact `bound_files` entries bind the
original project snapshots. Build03 also binds those snapshots and compiles
fresh copies of the corresponding canonical files.

Together with the already selected twelve RC/aggregate/entry files, the new
snapshot has exactly 21 compiler-source files. Native RC source/control adoption
is unchanged: exact compiled executable binding, forty passing controls,
twenty-six expected refusals and the two original-W/J comparisons. Native saved
selection JSON is compared by parsed value to the original selection; the result
binds the original selection's digest, not its reserialized copy.

The existing typed build's filtered dependency view is used in place: 236
libraries/macros, 311693039 bytes. No dependency recopy is needed. The retained
compiler closure remains 26 inputs, 395093004 bytes. All input bytes are rebound
before and after compilation by the selected adapter, with exact directory maps
excluding extra same-name libraries.

## Exact interface and recipe changes

Selection schema: `DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_V1`. Fresh name:
`restricted-guest-build-03`. Exactly seven selection fields remain:
`schema`, `name`, `adapters`, `production_sources`, `native_adoption`, `limits`,
`authorizes_four_compiles_and_retained_artifact_adoption`.

Result schema: `DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_RESULT_V1`. Success:
`PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY`. Recipe schema:
`DMKN_V5_RC_GUEST_FOUR_CRATE_RECIPES_V1`.

| Order/label | Crate | Source | Direct externs |
|---|---|---|---:|
| module | `dmkn_module_relation` | original `modules/receipt/src/lib.rs` | 11 |
| rc-core | `dmkn_rc_relation` | `restricted_composition/lib02.rs` | 10 |
| aggregate | `dmkn_aggregate_relation` | `restricted_composition/aggregate_lib.rs` | 11 |
| guest | `dmkn-aggregate-claim-guest` | unchanged `aggregate/main.rs` | 11 |

Recipes derive from the adopted typed recipes' matching module, aggregate and
guest profiles. Each source, emit option, metadata, output search path and map
path is replaced exactly once. Metadata uses `dmkn_v5_rc_guest03_`. Module links
the adopted original Nanoda pair; later crates link the fresh original module;
aggregate additionally links fresh RC core; guest links fresh aggregate. No old
typed project/output path remains in an argument. Libraries/macros still resolve
through the existing filtered view. The expected outputs are three rlib/rmeta
pairs plus one ELF (seven total).

Success counters require four actual compiler launches, exactly one module
compile and zero checker/dependency/Cargo/guest/proof/network calls.
The result additionally records the historical effective failure status and
the distinct retained Nanoda adoption. The maps keep exactly their old keys:

- INPUT-MAP: `inputs`, `existing_dependency_view`,
  `existing_dependency_files`, `copied_project_artifacts` (two artifacts).
- SOURCE-MAP: `source_snapshot`, `project`, `compiler_read_sources`, `adapters`.

## Preflight inspection performed

No builder import, syntax execution, test, compiler, guest or proof was run for
this review. Data-only reads/hash checks and source comparison established:

- Original failure marker, distinct source/ELF validator pins, scope and clean
  validator outer completion agree with the gates.
- Direct result's selection digest equals the pinned selection bytes; its
  exact terminal attempt, zero active/terminated processes and status agree.
- Direct selection/copy maps and current retained Nanoda bytes all agree.
- All nine original module sources plus the unchanged entry are present with
  matching pins in the validator's `bound_files`; current source hashes agree.
- Native saved/original selection equality, native/control binding and actual
  forty/twenty-six gate were already inspected; this successor retains them.
- The source/profile/metadata/emit/map/project-search replacement tokens occur
  exactly once in the retained recipes. Direct extern counts are 11/10/11 for
  the three retained bases; adding the RC extern yields the four counts above.
- Fresh build03 directory and attempt were absent at inspection. The adapter
  checks freshness again before output creation.
- Known mechanical helper-path replacement was corrected in unused build03:
  `common_build02.py` remains the pinned frozen helper, SHA-256
  `f28d18457b2ef465b14c44dd2fec15d4386f640f9bbdf627398d5dcf46a7f11c`.
  A full build02/build03 source diff showed no other accidental path replacement.

The envelope is unchanged: worker CPU240/wall300 seconds, 4096 MiB/six active
processes; ordinary controller40/finalizing total60 CPU seconds; total wall420;
fresh outputs256 MiB/2048 entries; command logs8 MiB. No runtime prediction,
RAM reservation or cryptographic cost-screen relaxation follows.

## Consumer coherence and final source pins

Narrow changed-interface review found root's unused selector03, assembler and
assembly selector consistent with 21 sources, four commands in the stated
order, seven outputs, one module compile and two retained project artifacts.
No extra SOURCE/INPUT-MAP fields were introduced. This is not a repeat of their
full prior review and does not adopt an image not yet built.

| File | SHA-256 |
|---|---|
| `software/v5/restricted_guest/build03.py` | `847589a36df894a022fe3dc8bf8251d32d49cfc605c2357a3311dd30ac1e8fbb` |
| `software/v5/restricted_guest/recipes03.py` | `e51b7b02d24c430599a021acaf92262fd7c49f6a3ebc2aa34287d6d5e29ccdef` |
| `research/cycles/v5-2026-10-20/Select-RestrictedGuestBuild03.ps1` | `e4f17794310792989df3f73706f78c67abec3c3ea1f83192161e65b1db958e8c` |
| `software/v5/restricted_guest/assemble.py` | `0ebc655842b1092f4314e27fa4f6e57e452303eae06b2e60b1b5a19bac46a957` |
| `research/cycles/v5-2026-10-20/Select-RestrictedGuestAssembly01.ps1` | `e1e745b6375ef7c3456fa30e9756aea6777ca813234f89e43b21b4671074c6ad` |

Next action belongs to root after independent source review: select, if still
useful, one fresh four-compile run. No later assembly, guest execution, proof,
installation or mathematical adoption follows automatically.
