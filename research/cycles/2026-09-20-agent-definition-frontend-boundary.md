# Agent definition frontend: kernel mathematics versus executable compilation

Date: 2026-09-20  
Status: source-grounded diagnosis and proposed authoring convention; runtime retry remains root-controlled  
Owner: `bounded_domains_author`; no fixtures/client code changed and no experiments launched

## Observed boundary

The retained [A2 failure](../../experiments/lean-agent-api/runs/attempt-01/A2/02.stdout.log) records an error on the ordinary definition in this agent-owned source:

```lean
universe u
def ClientSmoke.identityData (A : Sort u) (x : A) : A := x
theorem ClientSmoke.reflexive (A : Sort u) (x : A) : @Eq A x x := @Eq.refl A x
```

The returned diagnostic is `Unknown constant lcAny`, at line 2, column 4, followed by `AGENT_CLIENT_SOURCE_ELABORATION_REJECTED`. The client therefore emitted no successful capture for this source. Do not interpret this error as a counterexample to the definition's mathematical typing, or count the following theorem as a completed positive control.

The same retained stage successfully described 16 checked declarations and captured the separate zero-universe identity theorem with its `#check` information message. Those successes do not establish ordinary executable-definition support.

## Exact pinned source basis

All source paths below are relative to `experiments/lean-feasibility/runtime/lean-4.34.0-windows/src/lean/`. The selected Lean version is 4.34.0, commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.

| Pinned source | Relevant behavior |
|---|---|
| `Lean/Compiler/LCNF/Types.lean:23` | Compiler `anyExpr` is `mkConst lcAny`; this is a compiler-side support constant, not a theorem-specific dependency chosen by the agent. |
| `Lean/Elab/PreDefinition/Basic.lean:134` | `shouldGenCodeFor` requires both a non-theorem declaration and absence of the explicit noncomputable modifier. |
| `Lean/Elab/PreDefinition/Basic.lean:214` | `addNonRecAux` calls `addDecl decl` before the code-generation condition. The ordinary definition is built as a `Declaration.defnDecl` with its actual type, value, safety and reducibility hints earlier in this function. |
| `Lean/Elab/PreDefinition/Basic.lean:217` | The explicit noncomputable modifier records a frontend/compiler property; it does not change the definition into an axiom or an opaque declaration. |
| `Lean/Elab/PreDefinition/Basic.lean:222` | `compileDecl decl` is called only if `compile && shouldGenCodeFor preDef`. |
| `Lean/CoreM.lean:730` | `compileDecls` schedules or performs backend compilation separately from declaration admission. Its failure branch at lines 759–765 restores compiler state, marks declarations noncomputable, and rethrows when `logErrors` is true. |

These source paths explain the separation between constructing/checking a mathematical declaration and generating executable code for it. The observed error is consistent with compilation over a deliberately reconstructed minimal mathematical environment, which does not restore all runtime/compiler support from the producer's environment. No claim is made that the failed process produced an independently accepted definition before reporting the error.

## Selected minimal authoring convention

Use an explicit `noncomputable def` for definitions whose purpose is formal mathematical reuse. For the retained positive control, the proposed source change is only the explicit modifier on `ClientSmoke.identityData`; retain the definition itself and record the changed fixture. The corresponding runtime result is not asserted here before the reviewed retry.

This is a source-level code-generation choice, not proof weakening. For the ordinary nonrecursive definition path above, the kernel still receives a safe definition with the supplied type and body, while `shouldGenCodeFor` prevents the backend call. The mathematical body remains available for kernel reduction and later canonical capture/replay. The word `noncomputable` here does not assert that this particular function is mathematically uncomputable; it requests no executable implementation.

All normal acceptance gates remain: no `sorry`, no unsupported axiom dependency, supported closed declaration closure, canonical export, independently checked replay and actual-output correspondence. Source capture alone remains insufficient. An unused source definition may be omitted from the selected root's published closure; accepting that source is not evidence that the omitted definition itself was exported and independently replayed.

## Alternatives not selected

- **Inventing `lcAny` or importing unchecked compiler declarations:** changes the reconstructed environment and foundation assumptions without qualification. It is unnecessary for mathematical definitions.
- **Assuming a `compiler.enable` switch:** no such option was found in the inspected pinned compiler-option definitions. Do not propose an undocumented switch as a fix.
- **Setting `compiler.postponeCompile`:** `Lean/Compiler/Options.lean:44` describes an internal separate-compilation option. `Lean/Compiler/LCNF/Main.lean:142` and `:169` gate postponement on `env.header.isModule`; `toDecl` and `checkMeta` already run at `:164` and `:166`. It is not a general disable-compilation switch for this reconstructed environment.
- **Using `noncomputable section` merely to hide the error:** `Lean/Elab/PreDefinition/Basic.lean:137` changes compilation's `logErrors` based on section context. The call may still occur and its failure be suppressed. Explicit `noncomputable def` is a clearer, narrower path that avoids the backend call for this definition.
- **Replacing the global `compileDeclsRef` with a no-op:** the mutable hook exists in `Lean/CoreM.lean:723`, but intercepting it changes process-wide compilation behavior and introduces asynchronous/restoration concerns. It is unnecessary when the supported source modifier supplies the required boundary.
- **Removing the definition from the positive control:** would conceal the capability gap rather than test the selected mathematical-definition authoring path.

## Client-facing consequence

The [API document](../../experiments/lean-agent-api/AGENT-API.md) now states the explicit-definition convention, distinguishes implicit seed binders from explicit external reconstructed binders, and exposes the existing `describe` operation for any admitted reference. No proof strategy is imposed.

This client cut supports a finite mathematical authoring/replay workflow; it does not promise arbitrary executable Lean definitions, metaprograms, tactic extensions, producer metadata, or code evaluation. Agent-owned source remains executable input in principle and is not sandboxed. The noncomputable convention is not a security isolation mechanism. A general executable frontend would require separate work on compiler/runtime environment support and its trust boundary.
