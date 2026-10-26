# Exact private names require a kernel-only admission path

2026-10-26. Source-only diagnosis and repair recommendation.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Checkpoint: `research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.
No implementation, Lean/native execution, owner/status call, database access,
Git change or retry. The separate actual-evidence audit owns outcome adoption.

## Decision

The native receiver should check its declarations through the supported
**`Lean.Kernel.Environment.addDeclCore`**, retaining exact names, all current
checks, and the current checked-kernel trust premise. It should persist the
resulting exact kernel records directly. This native workflow does not need an
elaborator's asynchronous declaration-registration table.

Preserve the existing `CheckedExtension.checkBatch : Environment -> ...` API
and its frontend metadata behavior for authoring/rebinding callers. Add a
separate internally selected, kernel-typed path for native snapshot admission.
Share one private validation/checking loop between the two fixed checked
adapters; do not create two independently evolving acceptance implementations,
an unchecked callback API, a peer-selectable mode or a global runtime patch.

This is a small compatibility correction in principle, with a likely three-file
product footprint: `CheckedExtension.lean`, `LocalSnapshot.lean`, and
`OrdinaryWorkflowWorker.lean`. Its implementation and targeted evidence require
separate root selection. It does not make the failed intake acceptable afterward.

## Concrete failure and causal source path

The saved native diagnostic is
`experiments/v5-local-checks/std-catalog01/admission-calls/ab49ae0949ff479e3f124209bdd967005f87dda7dd82ae3a35c0ca27d99e2c36/supervision/stderr.txt`,
2,864 bytes, SHA-256
`2c101abd5788e4483b62131c69b9fe7899bfcc2985201e8d0a225ccfcf892db5`.
It reports `Lean.AsyncConsts.add`, `Lean.Environment:463`, including:

```text
_private.Std.Data.DHashMap.Internal.Defs.0.PSigma.casesOn._arg_pusher
vs. _private.Init.Data.Array.Basic.0.PSigma.casesOn._arg_pusher

List.mem_cons_self
vs. _private.Init.Omega.IntList.0.List.mem_cons_self
```

These are different exact Lean names. `Lean.privateToUserName` intentionally
erases `_private.<module>.0`. Thus each pair becomes the same user-facing name.
That is suitable for one elaborating module's namespace bookkeeping, but not a
uniqueness condition on exact declarations collected from many original modules.

The actual path is:

1. `OrdinaryWorkflowWorker.extend` restores the protected local parent and
   decodes inert units with the existing explicit allowed-name set.
2. `LocalSnapshot.checkAndWriteChunk` invokes `CheckedExtension.checkBatch`.
3. The checker scans actual declared expressions, rejects ungrounded references
   and overwrite, then calls `current.addDeclCore ... (doCheck := true)`.
4. This is **`Lean.Environment.addDeclCore`**, not the kernel-only API. Its
   `Environment.lean:701-731` implementation calls the checked native addition
   first, then registers every declaration in private and public `AsyncConsts`
   tables. Synchronous checking still performs this asynchronous-system
   bookkeeping; the existing comment about bypassing asynchronous checking does
   not mean it bypasses registration.
5. `AsyncConsts.add` at lines 459-469 looks up
   `privateToUserName aconst.constInfo.name` in `normalizedTrie`. A collision
   prints the reported panic. Both visibility tables explain repeated messages.

The panic site supplies an `Inhabited AsyncConsts` fallback containing the old
table. Therefore a worker can continue far enough to leave a report/artifact
after this diagnostic; their existence cannot establish a clean accepted run.
The controller's `ADMISSION_NATIVE_DIAGNOSTIC` refusal must remain. Do not suppress
stderr, reinterpret the report as acceptance, or promote its uncommitted bytes.

This is a mismatch between a multi-origin receiver and an elaborator-local name
invariant. It is not evidence that the original private declarations are equal,
that the portable identity scheme collided, or that the Lean kernel rejected
their mathematical content. No resource increase can remove this deterministic
normalized-name collision. The first interrupted intake's cause remains unknown.

## Supported API and preservation argument

The installed runtime exposes:

```lean
Lean.Kernel.Environment.addDeclCore
  (env : Lean.Kernel.Environment)
  (maxHeartbeats maxRecDepth : USize)
  (decl : Declaration) (cancelTk? : Option IO.CancelToken)
  : Except Lean.Kernel.Exception Lean.Kernel.Environment
```

`Lean/Environment.lean:293-298` documents this as checking and adding the
declaration; it is the `lean_add_decl` native entrypoint. It has no `doCheck`
switch. The adjacent `addDeclWithoutChecking` is a different API and must never
be used. This recommendation retains the project's existing trusted Lean kernel
and runtime premise; it is not a new formal verification of the native kernel.

For a warranted kernel environment `K` and exact declaration `d`, the required
step remains the checked judgment:

\[
\operatorname{kernelAdd}(K,d)=\operatorname{ok}(K')
\quad\text{and}\quad
\operatorname{generatedInventory}(K',d)=\operatorname{expectedInventory}(d).
\]

No name, universe, body, reference, imported export ID, unit ID, expected row or
foundation changes. Continue to reject exact-name overwrites and ungrounded
references, axioms/unsafe/partial additions, mismatching generated rows, missing
or extra generated names, and every existing byte/node/name/kernel/census limit.
The stage-two census still bounds actual in-process new records. The remaining
state transition is exactly the checked kernel transition needed for the next
unit and for persistence. The removed table is a frontend index, not a premise
of the checked judgment.

`quotInit` alone is still not a warrant: the actual protected parent, exact
foundation/runtime/implementation selection and existing trust-level-zero restore
premises remain required. An arbitrary caller-supplied kernel environment cannot
establish them. The adapter selection belongs to fixed trusted code, never peer
data, and no returned kernel result is coerced into a frontend environment.

Persistence already writes `checked.added`, the actual checked `ConstantInfo`
records, with exact `constNames`, no extra names/extensions and the authenticated
single-parent import. It need not inspect normalized user names. On restoration,
`Environment.finalizeImport:2334-2346` keys its imported constant map by full
`cname`; it does not normalize private names. Thus different private origins can
coexist as imported protected records. Existing import/lineage/byte and exact-name
rules remain; this does not permit a duplicate *exact* name. No new ancestor
proof replay is introduced by the proposed path.

## Minimum refactor that preserves both consumers

The source-level shape should be:

1. Factor the existing finite loop into **private** plumbing over an environment
   state, a projection to `Kernel.Environment`, and a fixed checked-add adapter.
   Keep all existing checks in that one loop, in the same order. There must be no
   public/custom callback argument or unvalidated checker selection. Private is
   code organization, not protection from a hostile in-process caller; the
   existing trusted-controller/nonhostile-process premise stays explicit.
2. Preserve `checkBatch`'s public parameters/result type. Its adapter uses the
   exact existing `Environment.addDeclCore ... (doCheck := true)` and returns
   its full actual `Environment`, with public/private visibility, extensions,
   asynchronous state and realization metadata preserved as before.
3. Add `checkKernelBatch` with a `Kernel.Environment` parent/result and the fixed
   `Kernel.Environment.addDeclCore` adapter. Its result contains the actual
   kernel state, ordered generated records and checked-unit count. It cannot be
   passed accidentally to an API expecting a frontend `Environment`.
4. Factor snapshot serialization into one private writer used only after a
   successful corresponding checked result. Add a dedicated kernel-typed native
   snapshot entrypoint/result, keeping the current frontend-oriented signatures
   available. Both writers preserve the exact existing `ModuleData` contract,
   fresh-file validation, quotas, serialization and parent identity.
5. Change only `OrdinaryWorkflowWorker.extend`'s native path to project the
   already protected restored parent once to its kernel state and call that
   kernel snapshot entrypoint. Same-process native continuation, if needed,
   carries a kernel state. Do not wrap it back into a frontend environment.

This costs a modest refactor rather than a new mathematical authority. If actual
source implementation expands beyond those three product files and focused
controls, stop and explain the new dependency before proceeding. Native support,
source pins, installation/profile/implementation identity and package outputs
will change and require the established update/adoption rules; this is not an
auxiliary-only update like progress logging.

## Why the tempting broader changes are unsuitable

`Environment.ofKernelEnv` at lines 642-646 explicitly describes a temporary
environment that should not leak into elaboration. It resets asynchronous and
realization metadata and installs the same kernel state in public and private
base views. A blanket replacement inside the shared `checkBatch` could alter
authoring visibility/realization semantics. Actual callers include
`OwnerConstruction`, `OwnerRebind.exposeAdded`, the independent private/public
module checks and reference-module paths. The native snapshot path does not
justify changing those contracts.

Resetting that wrapper after each declaration also treats a frontend data
structure as a disposable workaround and could retain within-group problems.
Renaming private constants would change exact expression/reference identities
throughout the DAG and require a substantially different correspondence theorem.
Patching Lean's private trie, disabling kernel checks, ignoring diagnostics or
splitting batches to dodge particular names is neither necessary nor a general
solution. Using kernel-only typed checking addresses the actual layer mismatch.

## Smallest future evidence and practical alternative

Before any repeat of the large workload, independent source review should check
the two fixed adapters, shared loop equivalence, native-only routing, exact
serialization and unchanged frontend callers. One later bounded changed-boundary
control can use two distinct exact private names with an identical normalized
suffix, followed by a dependent declaration using each exact name. It should
check complete inventories, serialize/restore the new records, and then refuse
an exact overwrite, a wrong expected row and an actually invalid proof. A
further checked extension after restore verifies usable exact-name continuation.
A public/private normalized pair is a useful second shape if cheap. This proposal
selects none of these executions, and the large failed intake is not the minimum
first discriminator. Do not reproduce a noisy panic merely for demonstration.

Successful controls would support this compatibility boundary only; actual rich
intake, warm authoring and affordability remain separate decisions. Preserve
failed state and use protected recovery before any later reuse as required.

If the narrow typed path cannot be maintained economically, ordinary approved
Std use remains the practical alternative. It can support the finite-map theory
locally with explicit approved-library trust. It must not be advertised as strict
independent grounding or used to fabricate commons warrants. There is presently
no reason to commission another certificate mechanism or larger-resource run.

## Exact inspected source pins

The following source bytes agree with the actual
`intake-progress-package01/distribution/package/installation/lean-src` copies:

| Source under `software/v5/ordinary_lean` | Bytes | SHA-256 |
|---|---:|---|
| `CheckedExtension.lean` | 7,055 | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |
| `LocalSnapshot.lean` | 10,377 | `488a76f4b8599a95bdc748c5e89187bc55e23f63d34cf52952702d93ff68795c` |
| `OrdinaryWorkflowWorker.lean` | 12,271 | `442c2d479d4df6b1c7ee456cb521b8c760b54258a3f8d5fb71a15fa391c77f9b` |

Runtime source is under
`software/runtime/lean-4.34.0-windows/src/lean/Lean`:

- `Environment.lean`: 137,725 bytes, SHA-256
  `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86`.
- `PrivateName.lean`: 1,932 bytes, SHA-256
  `21569296df3d69ca3f48dd109ed875c040509f9f693419e44cea9fa130b08179`.

These are source/data observations and an architectural recommendation, not an
implemented repair, a qualified new package or final-v5 completion.
