# Admission controls: independent source review

2026-10-22. Reviewer: `lean_workflow_trace`. Source review only; no execution.

Reviewed full `software/v5/ordinary_lean/AdmissionChecks.lean` and its
`IMPLEMENTATION-ADMISSION-CHECKS.md`, the current CheckedExtension boundary,
and the root's amended control driver. **No blocking source-design defect
found; eligible for root-selected bounded compilation and controls, not
mathematical acceptance or deployment.** Compilation remains an actual gate.

The fixture explicitly imports owner-selected Init, with no plugins and
`loadExts := false`, at private visibility. It is conditional test mathematics,
not evidence that importing arbitrary serialized Lean state warrants it.
Its explicit search root must be selected/pinned by the outer caller. Current
executable/DLL pins are not a hermetic full-library identity, as the result
format correctly discloses.

Six positive units go through producer kernel construction, encoding, decoding
and a separate CheckedExtension batch. The cases cover original binder/universe
names, implicit binders, all reducibility-hint forms, native Nat literals, safe
opaque declarations, theorem reuse and a small generated inductive inventory.
The custom `all` companion is a metadata-fidelity test; it is not itself an
additional mathematical declaration or a demonstrated mutual-definition group.

Negative controls require specific rejection markers rather than arbitrary
exceptions. The invalid-proof case additionally requires an actual direct
kernel type-mismatch exception, so resource failure alone cannot stand in for
that selected mathematical rejection. The failed-prefix test inspects the
original immutable parent after failure; it does not claim durable transaction
or crash-recovery coverage. The generated-inventory tamper changes a constructor
field count and is checked against freshly generated actual kernel records.

One driver integration issue was identified and reported: main requires one
Lean sysroot argument. Root amended the optional admission invocation to supply
`LEAN.parent.parent`; it was absent and unexecuted in controls01. The current
driver also records partial stdout/stderr on a subprocess timeout. Root's new
`core` lane avoids repeating the previously successful method-source lane.

The possible `String.contains` API concern is resolved by pinned source:
`Init/Data/String/Search.lean:300` supports generic patterns, and its immediately
preceding example uses a String substring. This is not a Char-only call in the
pinned Lean version.

Reviewed hashes:

| File | SHA-256 |
|---|---|
| `AdmissionChecks.lean` | `5dd8e8144c5db57ab3fa44ac1c4f57459d6dd8ff5f916eb72d7379e2cf294637` |
| `run_checks.py` | `f04b168afde41748a435de5fa7833fa1ddb2aa9432eb7a97dcaa7d435306f20c` |
| `OriginalExpr.lean` narrowed imports | `8278826700b17f8a926bebcf36e0408540ddfa3e84637ce4c8ff8f37c9dce72b` |
| `OriginalDecl.lean` Declaration import | `e30b6827bd80e2f303860c87ffa88844bcbb8eed1d2eb10e405574542323583c` |
| `CheckedExtension.lean` Environment import | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |

The narrow import changes do not alter the documented codec/admission design.
This source review does not close outer hostile-JSON bounds, warranted-parent
onboarding, persistence/restart, owner-project rebinding or ordinary-library
reciprocal integration. Those remain separate central work, not reasons to
repeat these component controls after they have passed unchanged.
