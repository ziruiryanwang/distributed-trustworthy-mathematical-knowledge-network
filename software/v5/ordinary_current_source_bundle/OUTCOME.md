# Actual source handoff and next build selection review

2026-10-28. **PASS_EXACT_SOURCE_HANDOFF_AND_RELOCATION.** The independent
source review remains the unchanged REVIEW (`79a59a84...`). This supplemental
audit reads saved bundle evidence and the proposed build selection only; no
packing, verifier/test execution, compiler, product import, state or Git action
occurred here.

## Actual bundle01

The run is `experiments/v5-local-checks/current-source-bundle01`, bound to the
cleared `cb39b2bc...` selection and exact `d90ad245...` control source. Command
stdout equals the saved controls RESULT; the external receipt equals its
reported receipt. The isolated relocated verifier's saved stdout equals the
reported VERIFIED_EXACT_SOURCE_NOT_BUILT result. Both stderr files are empty.

All seven groups passed: exact current pack/path census, actual relocated public
verification, wrong manifest hash, missing current source, extra source, changed
map bytes and obsolete overlay entrypoint refusals. The retained missing/extra/
changed-map fixtures contain their intended exact mutations; the successful
extraction remains unchanged.

| Actual artifact | Binding |
|---|---|
| source.zip | 3,071,941 bytes; SHA `68c5683ef349c6522cd3e12d9fb6fe161e358a91781a956b1335b2832c9e0bc0` |
| SOURCE-MANIFEST.json | 14,194 bytes; SHA `3d869c88151bdc414ddcc9d93c41c2f000eb874b7bbb17c643d5349d01672218` |
| Source payload | 95 files / 3,040,663 bytes; 96 archive/extracted files including manifest |

Independently reread the actual ZIP: exactly the sorted 96 expected members,
stored compression, fixed timestamp/mode metadata, no comments/extras, and exact
byte equality to the extraction. Every extracted payload length/hash matches
the manifest and the actual file census is exact. No utility verification or
product code was rerun by this audit.

Outer COMMAND_EXITED_ZERO_AND_CLOSED reports zero exit, direct child reaped,
Job closed, no termination request/cleanup error, zero final active/terminated
processes and four total processes. Actual wall is **2.750298 seconds**;
0.90625 inclusive Job CPU + 0.140625 wrapper CPU = **1.046875 known CPU seconds**.
Nested counters are not added again. Peak Job private commitment is 39,948,288
bytes. Outer RESULT SHA is `80b2bd3cc9bc56208f8c75e11c3cc2ef5f8de1c26d635d357bd828bf563c6c7f`;
controls RESULT SHA is `82659cc0e184cc6dc0593ec59c629deb0e63bc0453075d60708e7b5b8e9767b4`.

This establishes the exact current source handoff and relocated public verifier,
with no native build or mathematical acceptance. Preserve all successful and
negative fixtures and the already adopted source review.

## Exact fresh native-build selection

**SOURCE GO**, not launch or build acceptance, for
`experiments/v5-local-checks/current-distribution-build01-selection.json`, SHA
`b08498d1a894b1bfb2dd61b0b42cd1e2e552a1f875a1223128d91e2c4134888c`.

The complete selection has exactly the current builder and frozen runner as
snapshots, and 121 external pins: all **96 files of the actual verified
extraction**, the **23 selected runtime files**, and the two immediate actual
bundle results. Independent set/pin comparison found no missing extraction
member; the runtime pins match the extracted helper/map's complete named runtime
selection. The two source snapshot pins match their actual inputs.

Argv runs the byte-identical snapshotted builder with `--source-root` pointing to
`current-source-bundle01/controls/relocated-source`, separate explicit Python/
Lean runtime roots, and fresh `{output}/distribution`. The builder checks its
executing bytes against the extracted builder and obtains every preserved helper,
lane and core source from that extracted root. No canonical intermediate native
build, wrapper, runner change or old-owner operation is needed.

The original public allowance is **480 wall / 380 aggregate CPU seconds /
2048 MiB**; the enclosing Job is **540 wall / 440 CPU seconds / 2304 MiB /
eight processes**, with one MiB per output stream. These are within both existing
validators and retain the reviewed child-remainder/cleanup reserve logic. The
fresh run path was absent at review. Earlier build costs motivate feasibility;
they do not prove this changed composition will complete.

Root alone selects the one launch. Actual qualification still requires all
three native stages, final PROFILE/INSTALLATION and exact 154/117/8 census,
actual computed support identities and clean enclosing closure. A new support
identity does not authorize opening old owners. On failure preserve output and
costs; no automatic retry, allowance increase or rich-Std/network replay follows.
