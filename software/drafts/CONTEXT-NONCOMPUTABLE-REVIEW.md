# Source-only review: native02 and the noncomputable source profile

2026-09-21. Independent review of retained text and source only. No product,
Python, Lean, database or compiler execution was performed. No installed product
or failed-run evidence was changed. Source identities below do not independently
reproduce or attest a compiler build.

## Finding

Changing only the fresh X/Y/Z declarations from `def` to `noncomputable def`,
with fresh allocation roots and unchanged mathematical bodies, foundation and
checker, is a principled source-profile correction. It suppresses optional
executable-code generation; it does not make these declarations unsafe or
bypass mathematical replay checking. This is approval of the proposed source
delta, not a claim that fresh03 has run or will pass.

The native02 capture contains the 97-byte ordinary `def BranchCompose` source
with body `g (f a)`, then `Unknown constant lcAny` and
`AGENT_CLIENT_SOURCE_ELABORATION_REJECTED` (retained stage stdout, lines
938-941). X did not reach successful source capture or replay. This failed
prefix supplies no X/Y canonical separation or successor-dependency result.

## Source basis

- Lean `Init/Prelude.lean:29-30` identifies `lcAny` as an unsafe axiom used as
  the marker for type dependencies erased by the code generator. Compiler
  `LCNF/Types.lean:23` constructs that marker. The submitted lambda body does
  not mention it. The retained error and these sources support a missing
  code-generation-environment capability, not an observed kernel rejection
  of the composition term; the log does not contain a compiler stack trace.
- `Lean/Elab/PreDefinition/Basic.lean:134-135,186-223` constructs the ordinary
  `defnDecl` with its name, universes, type and value. Its safety is controlled
  by the unsafe modifier, not by noncomputability. `addDecl` precedes optional
  compilation. A noncomputable modifier records environment metadata and
  makes `shouldGenCodeFor` false. The mathematical definition is not changed
  into an axiom or an opaque declaration.
- `AgentClient.lean:158-172` rejects source diagnostics, checks foundation and
  imported-declaration preservation, screens the root, and permits ordinary
  definitions. `BootstrapSupport.lean:78-82` still rejects unsafe/partial
  constants and nonpermitted axioms.
- `AgentReplayCore.lean:281-283,294-313` reconstructs ordinary definitions with
  `safety := .safe` and calls `addDeclCore` with `doCheck := true`. The proposed
  source-only correction changes neither this check nor allowed dependencies.
- The earlier `lean-definition-inspection` first/second fixture sources already
  use `noncomputable def` for similarly elementary function compositions.
  This is corroborating source-profile precedent, not a new execution result.

## Documentation and fresh-run boundary

Document that the reconstructed mathematical environment accepts supported
safe definitions through kernel-checked capture/replay and that this profile
uses `noncomputable def` when executable code is not requested. Ordinary
computable `def` may invoke unavailable compiler infrastructure. Do not describe
the environment as arbitrary Lean program compilation or a complete imported
Lean runtime. Do not add `lcAny` or other unsafe runtime axioms to the foundation
to accommodate this fixture.

Keep native02 failed and immutable. A fresh allocation must still bind exact
source capture to the canonical candidate and inverse replay, show separate
X/Y identities and branch closures, and show two substantive X application
sites in Z's reachable value. Those observations cannot be inferred from this
source review, and noncomputable metadata does not itself establish them.
No discovery, novelty, useful-growth or usable-v1 claim follows.

## Reviewed SHA-256 identities

Paths below are relative to the workspace root. Runtime paths begin
`software/runtime/lean-4.34.0-windows/src/lean/`.

| Source | SHA-256 |
| --- | --- |
| Runtime `Init/Prelude.lean` | `2a3163bdd830cd31f1f1bc9bc79ea6bdad6a3b2c6f334166792bbc73631f3b10` |
| Runtime `Lean/Compiler/LCNF/Types.lean` | `66faec7a6974d2ab29b302a06ceed44d5af1c40f009ac700a088eec6c1f8d0ae` |
| Runtime `Lean/Elab/PreDefinition/Basic.lean` | `46a2876ccbe1efc4cc491dc24658fea5e972544a64da888334fe2ffcc9c1a5c7` |
| `software/native/AgentClient.lean` | `c7c5e8e325d332a229570dcab409feb3927b7a5819de46c98c5777e0d0811183` |
| `software/native/AgentReplayCore.lean` | `a9a9547ed4e302ca12618680ddf62bd790cc1706a86136115e928370bffc4855` |
| `software/native/BootstrapSupport.lean` | `c859d52fe9d1fcfefbfd4704bdb49d9590f4fead1fa1f1446758302c1e4c3e90` |
| `experiments/lean-definition-inspection/fixtures/first.lean` | `a0332bc80a868490981c41429ebaa178abc7987b49ca8a29b83a2de01dc482ba` |
| `experiments/lean-definition-inspection/fixtures/second.lean` | `15092b70e8a7823ef564f4a55398c482e2e687a230f2f597fa1c7d493786c98d` |
| Native02 `state/work/56cbe9ec459f3994bae30d857387d716f6886aa5df30636fe569f60cc3dddf89/stage-0001/00.stdout.log` | `8844c96e3e5937f76d597bf4b8cf86913774a07b723857875aaf4acabae7e84d` |
