# One ordinary Lean check using the retained compiled context

2026-10-28. Source-only route assessment. Root owns copying, finite selection,
launch and actual-outcome adoption. No module was imported or compiled and no
artifact was copied while preparing this note.

The proposed route is supported by the retained command and compiler source:
reuse the five existing module artifacts, create one candidate wrapper and run
the existing `author_worker.py --project-author-worker` once. No new driver,
grounding, library extraction, owner state, publication or networking is needed.

## Why the module relocation is faithful

The successful contribution02 command used:

- Source: `contribution/owner-source/FiniteMapRefinement/Contribution.lean`.
- `-R`: `contribution/owner-source`.
- `-o`: `contribution/lean-build/OrdinaryProducer.olean`.

Lean's installed `src/lean/Lean/Shell.lean:541` computes `mainModuleName` from
the source filename and root directory, independently of the `-o` destination.
`Lean/Util/Path.lean:146` removes the root and source extension, then joins the
remaining path components. The compiled module is therefore
**`FiniteMapRefinement.Contribution`**, despite the output stem
`OrdinaryProducer`. Preserve all five companions byte-for-byte under
`SCRATCH/library/FiniteMapRefinement/Contribution` with their original suffixes.
Do not compile a copy of the original source wrapper.

That wrapper publicly imports Init and Std.Data.HashMap.Lemmas and publicly
meta-imports PortableOwnerConstructCommand and PortableContributionExportCommand.
Its one construction/export command ran during original elaboration. Importing
the compiled result does not rerun those source commands. The construction
context is an ordinary local `EnvExtension`, initialized to `none`, with a
main-module equality guard; it is not an instruction to reconstruct old state
on every module import. Existing helper compiled modules must remain available
for the retained import closure. They are owner-trusted local code.

## Runtime-code and trust boundary

`FiniteMapRefinement.Context (A : Type u)` is a public inductive defined directly
in that successful module, with five constructors. It is parametric in `A` and
does not mention the reconstructed `FiniteMapEffects.Plan`. The earlier failure
arose when new executable code depended on that reconstructed Plan without its
compiled code. The sealed proposal instead instantiates Context with its own
newly defined `ResetEffects.Plan`; its recursion on Context can use the retained
module's ordinary generated code. Keep `.ir` and `.ir.sig` with the three olean
companions; do not strip private artifacts or recreate the Context type.

This resolves the prior code-generation obstruction in principle. It does not
predict that every proof in the unchecked proposal will elaborate. One bounded
compile is the appropriate remaining discriminator; failure should be inspected
at its actual diagnostic before selecting a source repair.

The retained module also contains scratch-authoring theorem signatures. The
candidate's intended retained dependency is **only Context**, so final theorem
axiom-closure output matters: imported scratch axioms must not occur in its
endpoint proofs. A local compiled-source check trusts the selected local olean
artifacts; it is not receiver admission or a portable warrant. It cannot replace
the product's eventual actual-parent checking/publication path.

## Small, exact inputs

All relative paths below are under the canonical root. The artifact directory is
`experiments/v5-local-checks/finite-map-refinement-contribution02/contribution/lean-build`.
Total relocation is **284,272 bytes**.

| Original suffix after `OrdinaryProducer` | Bytes | SHA-256 |
|---|---:|---|
| `.olean` | 186120 | `18ca04ed89427382e3d32756db15d455f3cc2031d144b0d57d845c09c4570c96` |
| `.olean.private` | 83320 | `c5fa08ec1df4690b3a7d26ccf6a7d873083302a8b559e9bffa52c44e336c6e13` |
| `.olean.server` | 7344 | `ed2702c01e1ccfaff5939387da734fe10a620147c801d96857954466f0bb8019` |
| `.ir` | 7312 | `eb51bd273d0fdc2e491cf29540226a955ebbca3bea85334a6b4dcadf6a867a39` |
| `.ir.sig` | 176 | `1162987eab76a4e4d796c37ae1e1dbcdb4d4c97f655cd137248df480f7e7ba1e` |

Additional fixed input identities:

- `Proposed02.lean`, 10458 bytes, root's selected one-line proof correction:
  `ee736d991afd9bf95b8a56d8f0555b24c6e6563c58ac02395b9f17648f42b404`.
  The original `Proposed.lean` stays preserved; it is not the compile input.
- `software/v5/ordinary_project_package/author_worker.py`, 4458 bytes:
  `19f9375fdf4b12cac05baeece6a750aa0d2d363112f51876d451f54c71ab2b02`.
- Original wrapper source:
  `caa848b218ea5d3eafda60b6b4962895a239e4a4c52c29354655dd4575a8146d`.
- Original `contribution/AUTHORING-SUPERVISION.json`:
  `2b7b404326597380c7b1e48642c84865befecad08e90e937ad08aeb9db5a8c88`.
- `software/runtime/lean-4.34.0-windows/bin/lean.exe`:
  `a8040e2cab341c12116ab591fed9f761816f5f6b08554f6cc1680e86dfbba0a2`.
- Approved `D:\Python314\python.exe`:
  `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.

Reuse `experiments/v5-local-checks/frontier-launcher-package01/distribution/package/authoring/helpers`
and the same installed Lean runtime. Its exact package PROFILE is
`efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45`.
The profile enumerates 70 helper companion files (14 modules, 21,200,496 bytes);
select those existing pins, with no helper rebuild or runtime recopy. The runtime
executable hash is not a complete library/DLL identity: keep root's existing
approved runtime selection and full runtime inventory policy in force.

## Wrapper and existing worker invocation

Root can create a fresh source root `SCRATCH/source`, with candidate module
`SCRATCH/source/ResetEffects/Check.lean`. Prefix the exact proposal bytes with:

```lean
module
public import FiniteMapRefinement.Contribution
public section

```

After the unchanged proposal, append:

```lean
#print axioms FiniteMapRefinement.Context
#print axioms ResetEffects.guarantee_iff
#print axioms ResetEffects.contextual_iff
#print axioms ResetEffects.skip_not_refined_by_reset
#print axioms ResetEffects.write_then_reset_false
```

Select the resulting exact wrapper bytes/hash. Invoke the frozen worker with
isolated Python `-I -S -B`, entry `--project-author-worker`, and these eight
positional arguments, each absolute:

| Argument | Selected value |
|---|---|
| lean | Existing approved `bin/lean.exe` |
| source | `SCRATCH/source/ResetEffects/Check.lean` |
| build | Fresh existing empty `SCRATCH/build` directory |
| helpers | Existing selected package `authoring/helpers` directory |
| candidate | Fresh absent `SCRATCH/unused-candidate.json` |
| root | `SCRATCH/source` |
| cwd | Fresh `SCRATCH` directory |
| project search path | `SCRATCH/library` |

The worker prepends helpers and the Lean runtime library before the scratch
project search path. It runs one Lean process with `-DElab.async=false` and the
selected `-R` root, writing `build/OrdinaryProducer.*`. The candidate argument is
only required to be absent; this plain wrapper has no export command, so no
candidate JSON should be expected. No product controller should be invoked just
to create one.

Root should use the existing bounded command supervisor and retain stdout,
stderr, closure/CPU accounting, wrapper hash and five copied-input hashes. Check
exit status and diagnostics, inspect all printed endpoint axiom closures for
unexpected assumptions (including `sorryAx`), and verify outputs/input integrity.
No automatic retry or expansion into a theory/grounding campaign is selected.
