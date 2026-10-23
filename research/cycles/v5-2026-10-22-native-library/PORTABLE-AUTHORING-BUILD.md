# Portable authoring: minimal retained-helper build plan

2026-10-23, `portable_integration_audit`. **Source-only proposal, not a runtime
selection.** No build, native process, test, source-template specialization,
store operation or accepted-state change has run in this assignment. Root owns
the exact finite selection and launch. The source and callback refinements in
[PORTABLE-AUTHORING](PORTABLE-AUTHORING.md) remain subject to their own review.

## Consequential next boundary

Build only the two new V2 command wrappers. They import the retained compiled
construction, codec and exporter helpers, so no old mathematical library,
foundation, checker or exporter needs recompilation/replay. This answers one
question: do the new explicit S/F/local-context wrappers compile with the exact
retained interfaces? It is not native authoring, final acceptance or growth.

Use the existing `software/v5/ordinary_lean/run_selected_compile.py`, SHA-256
`ba3b7e3f611c519487ff0437b400055b5f22ed8ba61decb07efa76219519706f`, under
`tools/Run-V5-Check.py`, SHA-256
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
No new compile driver or selector is needed to express this plan.

Module order, with no other module names in the requested compile list:

1. `PortableOwnerConstructCommand`, source SHA-256
   `250a8dd1292c1dd5d228d69eaeb7abdbb5f0e9ad96c48a8b32d80203c27619b2`.
2. `PortableConstructExportCommand`, source SHA-256
   `8251bc13836fde6620203752b9378bfafccefeef16587788221dec7ad7e95a8b`.

For each module, the retained driver invokes exactly:

```text
<canonical-root>/software/runtime/lean-4.34.0-windows/bin/lean.exe
  -DElab.async=false
  -R <new-output>/sources/software/v5/ordinary_lean
  -o <new-output>/lean-build/<Module>.olean
  <new-output>/sources/software/v5/ordinary_lean/<Module>.lean
```

The driver clears inherited `LEAN_PATH`, `LEAN_SYSROOT` and `LEAN_SRC_PATH`, sets
an explicit search path, and uses canonical-root cwd. It creates one fresh
`lean-build` directory, has a 45-second timeout per module, requires zero exits,
and emits a compile-only result. Root must choose an original outer envelope
covering both child timeouts plus bounded cleanup; no native use is implicit.
The existing 120 CPU / 195 wall seconds / 1536 MiB / 3 active-process envelope
from the retained four-module build is a conservative upper envelope, not a
prediction or a request to spend it. A smaller root-selected envelope is fine.

## Exact retained directories and search precedence

Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`.
All following directories are relative to its `experiments/v5-local-checks/`:

| Search order after the new output directory | Retained directory | Required selected modules |
|---|---|---|
| 1 | `ordinary-deferred-import-helpers-01/lean-build` | `OrdinaryExport`, `SuccessorExport`, `SuccessorExportCommand` |
| 2 | `ordinary-construct-helpers-02/lean-build` | `OwnerConstruction` |
| 3 | `ordinary-abstract-helpers-01/lean-build` | `OwnerRebind`, `OwnerUseCommand` |
| 4 | `ordinary-public-remaining-01/lean-build` | `BootstrapSupport`, `CheckedExtension`, `OriginalDecl` |
| 5 | `ordinary-public-expr-sync-01/lean-build` | `OriginalExpr` |

Each module's `.olean`, `.olean.private`, `.olean.server`, `.ir` and `.ir.sig`
must remain available and pinned as one retained family. In particular, the
newest deferred-import directory must precede older `SuccessorExport` and
`OrdinaryExport` copies: it contains `selectedDeferred`. The older
`ordinary-successor-core-build-01` directory is unnecessary because every module
needed from it is now supplied by the first directory; omitting that search
entry avoids an obsolete fallback without recompiling anything.

The underlying pinned Lean/Init/Std runtime remains the same explicit installed
toolchain, not a hermetically hashed transitive installation. No new claim of
hostile-source isolation follows from resource supervision.

## Reusable prior pins

The retained deferred-helper build has these exact control files:

| File under `experiments/v5-local-checks/ordinary-deferred-import-helpers-01` | SHA-256 |
|---|---|
| `selection.json` | `9aaa09f0ab872816e41e796a5e5927e3cbd2a32445f29bb277e01c9a0d4e6793` |
| `RESULT.json` | `9fb5850986d7d8dde4058cab438a90dfdc6510124eb4da35bde88ebe8179637d` |

Their bytes were read and hashed, not executed. The saved result records
`COMMAND_EXITED_ZERO_AND_CLOSED`, selection hash equality, exit 0 and no cleanup
errors. The selection's `runtime_pins` is the exact existing mapping for the
runtime and every required artifact in search directories 2–5. Reuse that whole
mapping or the exact selected entries; do not replace hashes by current files
without comparison. It also includes old unused helper artifacts, whose presence
does not authorize rebuilding or importing an obsolete version first.

For orientation, these are the required older public `.olean` entries already
present in that pinned mapping; their companion hashes are in the same mapping:

| Relative directory/module | SHA-256 of `.olean` |
|---|---|
| `ordinary-construct-helpers-02/lean-build/OwnerConstruction` | `c0b69cc9e78194f4b02323a026314985687d075998c87a9e2eb2515f60844151` |
| `ordinary-abstract-helpers-01/lean-build/OwnerRebind` | `aa5b116bb2c04dfe9799ed89c96edf08c4d0ca47eb3ed770ff166f888aa46226` |
| `ordinary-abstract-helpers-01/lean-build/OwnerUseCommand` | `e2ccf780480e6aa73cc7fe5ec65f1a5335fffc63db6da7c53ba4c19ced329f91` |
| `ordinary-public-remaining-01/lean-build/BootstrapSupport` | `c02b2276ae18ac44252caedc6afd4c953200d9e98ccb14f729c62d091f977e09` |
| `ordinary-public-remaining-01/lean-build/CheckedExtension` | `1d486d4e6820c7c38c7ec5c70e6c496a12faa4b09589c5dc37ed7933a85fe89f` |
| `ordinary-public-remaining-01/lean-build/OriginalDecl` | `26ad96f8b74cdb00bf845e20bdf5464f65063cd93493879b47e7f6c5094350a9` |
| `ordinary-public-expr-sync-01/lean-build/OriginalExpr` | `70a68712dcdb13b3b52f607d6d14f019190138d0db30609d31fe7f0d3998bcb4` |

Add these newly read/hash-pinned required outputs from directory 1 to that
mapping, plus its exact selection/result pins:

| Filename under `ordinary-deferred-import-helpers-01/lean-build` | SHA-256 |
|---|---|
| `OrdinaryExport.olean` | `f256cf564eceb36831bacf70e70cc267cfa6bccefe29ffe84aab78744523092f` |
| `OrdinaryExport.olean.private` | `3de108349b9341d98fcd5289fae48cadab9b186b667831bab6cbcbde333f6405` |
| `OrdinaryExport.olean.server` | `12edfdddf052c899bb0da310383fe1c02bc4b17316dc02417a3e50d44366bc4a` |
| `OrdinaryExport.ir` | `eade748b2688b51ee4d4f3ddbd2382ab8e94652a601f246043ff6973c9dcf0d5` |
| `OrdinaryExport.ir.sig` | `005c81f6f0644084c6bde102c07857ef3e3c3d417557f1173809fccc4622403b` |
| `SuccessorExport.olean` | `c36f5024ee621bfbf0545eb9b1873fcd26d27c37d798ed437f2de2ac0c07de46` |
| `SuccessorExport.olean.private` | `ea853498a6091565634cf2a42f8121f5dd591fc2a1c097df9defd034dad9e164` |
| `SuccessorExport.olean.server` | `49973563a0d8a4333e3fa0ad8e525ec81a82948a8100684c67ad523deea141b9` |
| `SuccessorExport.ir` | `213519a76a13e86d349d827e2ae6422e4aaa904a3c1af58de0d72a183b0416fc` |
| `SuccessorExport.ir.sig` | `e235e32ad339c6a187d9da440ec7efa63e8daa833e3124bd6efaff07b8897518` |
| `SuccessorExportCommand.olean` | `b6bde62879a086dd4686f1b0fc3d72d5f3000a4bb46e4cc359b808d07a6683df` |
| `SuccessorExportCommand.olean.private` | `c567b9792dee7f27b52d8ef79cf51a4a65a5b438037aa4a71eaa3b7b8836a9b2` |
| `SuccessorExportCommand.olean.server` | `5821c6bee7376e04522bca2f1c9b8491d7f18c8815342ee4c80610d12728610a` |
| `SuccessorExportCommand.ir` | `058aa5bc0d0ad0fc9ea32ee3f3a75682ac11d789ab6e9daa38d2e7825a67dfec` |
| `SuccessorExportCommand.ir.sig` | `1b0e12b7564e879e8865d8cb195145d25463916a2419a91e3366741d8c59c8cf` |

## Separate future integration producer

New source-only template:
`software/v5/ordinary_lean/examples/PortableMethodProducer.lean`.
SHA-256: `10048582b4719ddaca68c3f9758c33b7274ca2dd0a3c23a0baacaa60a1524233`.
It defines an elementary reusable invariant-preservation method:

```lean
def Stable {α : Sort u} (f : α → α) (P : α → Prop) : Prop :=
  ∀ x, P x → P (f x)

theorem stable_compose {α : Sort u} {f g : α → α} {P : α → Prop}
    (hf : Stable f P) (hg : Stable g P) :
    Stable (fun x => f (g x)) P :=
  fun x hx => hf (g x) (hg x hx)
```

The file uses the V2 construct/export commands and explicit sentinel strings
for five owner-selected fields: request directory, S, K, F and fresh candidate
output. It is not runnable as a selected operation until the protected controller
replaces each complete quoted sentinel literal exactly once with a bounded
Lean-quoted value in a fresh
source. No path, context or deadline is silently allocated by the template.
Root must pin the original template and specialized bytes before future use.
Do not import this producer module into the future independent consumer.

The producer may start from a finite basis-only request (one fixed warranted
target is enough for the command's nonempty target requirement). That request
is bookkeeping, not evidence that the producer reused a remote method. The
subsequent consumer must instead discover and acquire the actual `Stable`/
`stable_compose` contribution, construct its handles and independently author a
triple-composition or iteration extension. Its request must follow the actual
discovered exact IDs. Final checking and durable republishable custody are
required on both sides; neither this producer's compile nor its inert export
is mathematical admission.

This is a small generic workflow discriminator, not evidence of a new theorem,
growth superiority, planet-scale discovery or public deployment. No consumer
proof is prewritten here. The template is deliberately excluded from the
two-wrapper build: product/native admission integration and future authoring
runtime require root's separate selection.
