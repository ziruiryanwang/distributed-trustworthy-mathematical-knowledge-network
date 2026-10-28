# Native02 correction and launch binding review

2026-10-28. Independent source/saved-data review only; no product import,
compiler/test execution, database operation, Git mutation or old-evidence edit.

**GO for the selected fresh native02 workflow.** This is clearance to collect
evidence, not a passing frontier outcome. Native01 remains a preserved failure.

The reviewer independently compared the workflow bytes: native_workflow02.py
adds only the 14 bytes `noncomputable ` to SETUP_P's `Above.d` definition.
Its type, value, dependency, assertions, stages and budgets are unchanged.
Pinned Lean `Elab/PreDefinition/Basic.lean:134-135,186-223` makes this skip
optional executable compilation while retaining the ordinary safe defnDecl,
its checked type and value, and reducibility for mathematical checking.
A blanket noncomputable section would not provide the same compiler avoidance.
No checker change or acceptance weakening is selected. The runtime must still
establish the positive, exact-parent false-candidate refusal and missing-name
outcomes; `KERNEL_REJECTED_OR_RESOURCE_LIMIT` does not identify a precise cause.

The reviewer also independently checked native02.selection.json against native01:
only the fresh run name, entrypoint and matching source path/hash change. All four
source pins and 164 external pins matched; the fresh output was absent at that
inspection. Limits remain 420 wall seconds, 260 Job CPU seconds, 2048 MiB,
eight processes and 4 MiB streams. The selected wrapper revalidates pins before
use. Root owns launch, closure and adoption.

| Bound file | SHA-256 |
|---|---|
| native_workflow02.py | `e5ac5c841b48431ce3d627a2b42ad751254350cea478c616dbae436edca5ed05` |
| demand-frontier-native02.selection.json | `d0e2e7ab4f6eae8234a8161356768133677f4aa95e7740ef875bf1b75a7eb0b9` |
| corrected ../ordinary_finite_map_refinement/BodyMath.lean | `276e64eada849a8ed46a23b6ceee122124ef99c0b91a57fdd97b619de3708b89` |

## Separate upcoming mathematical source

The corrected BodyMath bytes independently reproduce original Body.lean exactly
after removing five `noncomputable ` modifiers and the one scoped
`set_option bootstrap.genMatcherCode false in` line. The option now correctly
precedes fill's unchanged doccomment. The first unused variant placed the option
between doccomment and declaration; that pre-launch defect was corrected.
All statements, bodies and proofs remain unchanged. Pinned matcher/structural
source retains checked declarations while suppressing optional executable
generation, as detailed in NATIVE-CORRECTION.md. This supports the source choice,
not complete elaboration success or preservation of generated artifact IDs.
BodyMath is not an input to native02 and does not gate that independent run.

Source foundation: NATIVE-CORRECTION.md and the pinned Lean sources inspected
there; preserved actual failure: NATIVE-OUTCOME.md. Discovery remains a separate
review. No frontier or refinement runtime pass is claimed here.
