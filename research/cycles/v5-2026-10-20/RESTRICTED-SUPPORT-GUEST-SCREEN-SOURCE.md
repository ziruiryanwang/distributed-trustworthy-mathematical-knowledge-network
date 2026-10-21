# Support guest assembly and fixed matched screen: source ready

2026-10-21, support_screen. Selected by RESTRICTED-SUPPORT-GUEST-SELECTION.
Source changes only: no syntax parse, import, fixture preparation, native call,
build, assembly, guest execution, test, proof, network or Git operation. All used
predecessor sources and evidence remain unchanged. Root owns actual selection
and adoption; the future image/build outputs do not exist by this source note.

| Fresh source | Bytes | SHA-256 |
|---|---:|---|
| software/v5/restricted_support_guest/assemble.py | 19217 | e9084fd418e393825bcf8ec6658ac5e3991532b60e92d0039ce4cc8f38216659 |
| software/v5/restricted_support_guest/matched_pair.py | 20222 | 6a7112acd0a64aadc90d86a3bfac77e7754525a2fa2805d2872c5757be965bcf |

Both adapters were read back completely. The guest author's final build/recipes
sources were read and their interface corroborated; no new supervisor, profiler,
host or dependency tree is introduced.

## Assembly boundary

The assembler adapts frozen restricted_guest/assemble.py and reuses only the
same pinned bounded_parse_guest/assemble.py utilities and retained driver/kernel.
It accepts exactly restricted-support-guest-build-01/RESULT.json via:

```text
python -I -S -B <snapshot>/software/v5/restricted_support_guest/assemble.py
  --guest-result <absolute build RESULT.json>
  --guest-result-sha256 <root-adopted actual digest>
  --output <selected outer run>/assembly
```

Required build schema/status are DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_RESULT_V1
and PASS_RC_SUPPORT_GUEST_THREE_CRATE_COMPILES_ONLY. The selection/recipes use
their matching THREE_CRATE schemas. There are exactly three commands, in order
rc-core/aggregate/guest, twelve production sources and five fresh outputs.
Original-module/checker/dependency compiles and execution/proof calls must be0.
No result is converted into an old four-crate schema.

The adapter binds actual command records/logs, source snapshot/map, selection,
native adoption pins, artifacts and clean terminal attempt. It checks the
retained guest03 module/Nanoda adoption identity, the exact copied two-file
module view, and each actual recipe's fresh metadata, selected source, complete
search-path list and project extern edges. Aggregate must link fresh support
RC; guest must link that fresh aggregate. No guest03 outputs search path is
permitted. Five output files and the exact user-ELF/link map are pinned.
The236-file dependency view is adopted through the reviewed build, not rehashed
here as another dependency audit.

One retained assembler call produces the actual image ID. Result schema is
DMKN_V5_RC_SUPPORT_GUEST_IMAGE_ASSEMBLY_RESULT_V1; success remains
PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY. Actual image bytes and assembler output
are checked. Inputs are rebound; an overriding build failure remains forbidden.
The future pair requires the exact root restricted-support-guest-image-assembly-01
and clean outer assembly completion. No current image digest is invented.

## Same-fixture pair boundary

The new pair imports frozen restricted_composition/matched_pair.py,26523bytes,
SHA6deb0711c94fb6baba44e17a216befcd2ff8e945ede64148f7f7d54e0e241af6,
for bounded files/JSON, retained supervisor/host adoption and full segment
statistics. It reuses the frozen pure prepare_execution.py and its existing
source closure. The inherited main execution/accounting path changes only
native/image adoption and result/config schemas.

```text
python -I -S -B <snapshot>/software/v5/restricted_support_guest/matched_pair.py
  --input <absolute configuration> --input-sha <exact digest>
  --output <selected outer run>/pair
```

The schema is DMKN_RC_SUPPORT_MATCHED_EXECUTION_INPUT_V1, with the same exact
keys as the predecessor: schema, fixture, receipt, controls, general, restricted.
Each arm retains host_build {result,attempt,selection,source_map,command} and
assembly {result,outer,guest_result,guest_attempt}. All leaves are file pins.
The controls field retains {result,outer,selection}, now with result pointing
to restricted-support-controls-01/command/stdout.txt, not an absent evidence file.

Exact native records are hard-bound: stdout b9ac046a (4073bytes), outer b1ebc253
(1890bytes), original selection6f855719 (8140bytes), and support build RESULT
e26e29de (16962bytes). The new guest's native_adoption must equal these build and
control pins. The exact adopted stdout contains all30 passing controls and12
intended refusals, including full-J/ordered-pending comparisons. The first
predicted J must match both its actual module and full journal SHA0ba261cd.
This reuses native evidence; it does not rerun the controls.

The exact original fixture remains84727bytes, SHA019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a.
Fixture definition source remains b6f20143. The retained preparer preserves
the exact first original W and RC frame, base-I receipt850c33b2 and journal22fe722c,
general image9d5072a6, identical members/parent claims and H except its A bytes.
The old restricted snapshot host is additionally fixed to e3f35fb1. Its reuse
is limited to this native-differential-qualified fixture, following
RESTRICTED-SUPPORT-BUILD.md; it is not broad adoption of new-core inputs.

The restricted image function is new and accepts only the actual support
three-crate build and matching new assembly/clean outer evidence. The general
image function remains the frozen adopted typed-four-crate path. Both actual
hosts verify the genuine fixed-I boundary and execute their selected image.
No old-A receipt is relabeled or uncertified recursive boundary introduced.

## Fixed screen and full accounting

The original general-then-restricted order, host limits, clean Job gates,
diagnostic/capsule checks, every segment byte/hash, row totals and final output
census are unchanged. SDK row_count already includes padding; no double count
is added. The requirements remain all of:

- Restricted padded rows at most75% of general.
- Restricted at most64 segments, each at mostpo18.
- No preparation-plus-execution known-CPU regression.

All adapter validation, helper loading, preparation and final rebinding are in
the controller interval. Per-arm controller plus host Job CPU is measured;
remaining shared preparation/validation CPU is charged fully to both standalone
arms and once to pair total. Hence the common charge cancels only in the
inequality, not in reported complete cost. The outer owner captures startup and
final report/exit tail and must not double-add nested Jobs. One-time build and
assembly remain separately priced investment costs. No timings are retried.

Result schema DMKN_RC_SUPPORT_MATCHED_EXECUTION_RESULT_V1 retains
PASS_RC_INVESTMENT_SCREEN / FAIL_RC_INVESTMENT_SCREEN and original failure
semantics. A failed screen ends this shortcut investment; a pass is not proof
funding, a certificate, reciprocal-use adoption or a full-v5/growth claim.

## Root selector compatibility

Read Select-RestrictedSupportGuestAssembly01.ps1 and Select-RestrictedSupportPair01.ps1.
Their3/17 source closures include all required frozen helpers; command lines,
schemas and intended roots agree. Root was notified to include two copied
module artifacts in the assembly runtime pins and the native support build
RESULT in pair runtime pins, since these new adapters explicitly bind them.
Those root-owned selector changes and independent source review are separate.
Actual build/image records must be adopted and pinned before the respective
future selections. No target regeneration or additional host build is needed.
