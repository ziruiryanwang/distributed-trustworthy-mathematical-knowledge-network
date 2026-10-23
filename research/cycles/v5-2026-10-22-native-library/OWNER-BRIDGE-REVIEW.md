# Small owner-project bridge: use Lean's existing command environment

2026-10-22. Independent source review by `lean_workflow_trace`. No builds,
runtime imports, tests, product changes or Git operations. This resolves the
owner-side integration choice; it does not qualify an implementation.

## Recommendation

**Use one small trusted Lean command/helper, operating inside the owner's normal
project. Do not create a second source package system or make private checker
snapshots importable in that project.**

The minimal core is a function taking an existing `Lean.Environment`, inert new
declaration groups and exact dependency bindings; it returns a checked extended
`Lean.Environment` or an error. A trusted command wrapper can obtain `getEnv`,
run that helper, and update the command environment only after the whole batch
succeeds. Lean's normal frontend/build system then handles the ordinary project
module output. API spelling below is illustrative, not implemented:

```text
rebind(ownerEnvironment, compatibleDependencies, inertNewGroups, finiteLimits)
    -> checkedOwnerEnvironment

#commons_use "locally-acquired-capsule.json"
```

The command processes data, not peer source/tactics/plugins. Its own code is an
owner-installed trusted extension. Existing local `Init`/`Std` imports retain
normal notation, instances, namespace names and editor behavior. The owner
frontend remains a construction tool; independently checking the final inert
successor in the isolated receiver is still the mathematical acceptance step.

## Actual existing mechanisms

| Need | Available source/API |
|---|---|
| Get/update normal command environment | `Lean/Elab/Command.lean:213-215` implements `MonadEnv CommandElabM`. |
| Existing source authoring with an environment | `Lean/Elab/Frontend.lean:140` `Lean.Elab.process` takes source, `Environment`, options and filename. Existing `software/v5/authoring/native02/AuthorLean.lean:838-874` already imports an owner-selected frontend and invokes it. |
| Synchronous checked insertion preserving frontend maps | `Lean/Environment.lean:701-731` `Environment.addDeclCore`, fixed `doCheck := true`, finite heartbeats/recursion limits. |
| Normal namespace registration | `Environment.registerNamespace`, as used in `Lean/AddDecl.lean:53-68`. The helper can register the admitted exported names' ordinary namespace prefixes. |
| Kernel/private inspection | `Environment.toKernelEnv`, `Kernel.Environment.find?`. Inspect actual checked records, not just a public display interface. |
| Generated nested-recursor exposure | Frozen `product-local/auxiliary-frontend-source-13/native/AgentClient.lean` already contains the narrowly checked `addConstAsync`/`commitConst`/`commitCheckEnv` pattern for actual kernel-generated missing recursors. |
| Optional normal source instance registration | `Lean/Meta/Instances.lean:283` `addInstance` is an owner-authoring operation, not a mathematical acceptance rule. Existing standard-library instances need no reconstruction. |

The bridge does not need a daemon, a second package manager, a custom elaborator,
new recursion machinery or a cryptographic certificate. It does need the new
metadata-preserving inert format and the checked-declaration adapter already
selected by root.

## Avoid a misleading shortcut through `Lean.addDecl`

The convenient `Lean.addDecl` is **not** the right unqualified checker boundary:

- `Lean/AddDecl.lean:24-35` honors `debug.skipKernelTC`.
- Its normal path can report preliminary declarations before asynchronous
  checking completes (`:154-197`).
- On a checking error, `addAsAxiom` inserts fallback axioms so the frontend can
  continue reporting errors (`:210-240`).

Those are reasonable editor mechanisms, but are not the atomic checked import
contract. Use `Environment.addDeclCore(..., doCheck := true)` explicitly. Build
the candidate environment in a local variable and call `setEnv` once all
required groups and generated-record comparisons succeed. An error must not
leave a fallback axiom pretending to be the acquired result.

The helper must respect any normal asynchronous environment restriction. If
called from an inappropriate restricted branch, report it rather than clearing
the restriction or manufacturing a replacement environment. A top-level trusted
command is the straightforward first integration point.

## Dependency meanings: one check, not a new global registry

Before a referenced existing name can stand for an acquired dependency, bind it
to its actual meaning in this owner environment:

1. Check the selected kernel/profile and semantic dependency locks.
2. Obtain the actual required kernel records. Use the special documented
   fixed-basis projection only for the frozen normalized basis; use the new
   ordinary record projection for ordinary extensions.
3. Compare the record and its named dependency bindings. Traverse the required
   closure once with memoization to already matched immutable records; do not
   rescan unrelated imports for each lemma application.
4. Existing exact matched records are references, not declarations to add.
   New names are inserted only once. Any same-name semantic conflict refuses.

The match does not grant authority to arbitrary owner `.olean` files. It
establishes the intended correspondence for authoring. The ultimate exported
successor still faces independent checking in the receiver's grounded context.
Caching compatibility inside one immutable owner environment is an efficiency
device, not a transferable mathematical warrant or a bypass of changed inputs.

Ordinary Lean modules may expose a theorem as `.axiomInfo`: see
`Lean/AddDecl.lean:119-126` and `Environment.subsumesInfo:2268-2282`. Therefore
matching only `env.find?` in the public exporting view can reject a perfectly
ordinary compatible import or accidentally treat a genuine axiom as a proved
theorem. Prefer the actual kernel/private record. If the body is unavailable,
require the exact already-bound module/interface correspondence or return
missing evidence; do not invent the body or silently relabel arbitrary axioms.

The first bridge can deliberately require full actual records for its declared
supported workflow. Wider public-interface correspondence is a separate explicit
mode, not an accidental permissive branch. Failure here is a compatibility
limitation, never a proof that the acquired mathematics is false.

## New groups and ordinary visibility

Check safe definitions/theorems/opaque declarations and complete inductive
groups with their actual proof/type/value data. After insertion, compare actual
kernel-generated constructor and recursor records with the advertised ordinary
projection. Peer-generated `ConstantInfo` is not installed directly.

`Declaration.getNames` excludes some nested auxiliary recursors. The selected
high-level `addDeclCore` updates frontend names only for that list, so kernel
membership is not automatically normal source visibility. Reuse the existing
AgentClient repair pattern: for a required missing auxiliary, obtain its actual
checked `.recInfo`, expose that exact checked constant through the frontend's
async-map API, and compare it again. Do not insert caller data or expose an
unrelated existing private declaration. This is a known resolved predecessor
boundary; a new large investigation is unnecessary.

New namespace prefixes should be registered for normal `open Namespace` use;
fully qualified names alone are not complete ordinary source compatibility.
Original forall binder names must be retained for `(parameter := value)` calls.
The new codec addresses that loss; neither changing a constant's global name
nor merely preserving its type up to alpha-equivalence restores this API.

Existing standard notation and instances continue working because the bridge
retains the owner's normal imports. New peer attributes/notation/plugins are
not blindly executed. The owner can explicitly add familiar attributes using
normal source commands; later a bounded reviewed metadata adapter may automate
common instance/simp declarations. The first map/update-log workflow does not
need a universal registry serializer.

Direct kernel insertion does not automatically generate native executable code
for new definitions. They are available to kernel proof reasoning, but ordinary
`#eval`/compiled execution needs the owner-side compiler path (`compileDecl` or
normal source compilation). Keep that as an explicit owner construction feature,
not a kernel-proof rule, and do not promise full executable-package behavior
from a checked declaration alone.

## Why not an even cheaper interface-as-axiom bridge?

For a strictly private scratch authoring process, imported theorem statements
can be hypotheses, provided the final receiver discharges each exact dependency
from warranted mathematics. Existing AuthorLean uses this separation. It can
avoid checking a large imported proof twice.

But using that mode as the default persistent normal-project bridge would put
new axioms into the owner's source artifact. Outside our independent receiver,
`#print axioms` and ordinary consumers would see those assumptions rather than
portable checked library proofs. That is a material usability/trust contract
change, not merely an optimization. Keep it an explicit scratch mode, not the
first ordinary-project default. The proposed full checked rebind repeats only
the selected missing delta, while common accepted library work stays amortized.

## Scope and next implementation consequence

Select the small `rebind` helper once the inert codec/declaration adapter is
reviewed. Give it an explicit normal-project wrapper; reuse normal frontend
compilation rather than inventing owner module persistence. Test only changed
boundaries later: original named arguments, namespace visibility, hidden
auxiliary recursors, wrong dependency meaning, partial-group rejection, and
failure without fallback axioms. No runtime is selected by this note.

Do not import the isolated checker basis alongside ordinary `Init`; duplicate
definitions are refused by `finalizeImport`, even if their records are equal.
Do not weaken that rule or overwrite names to make an integration example pass.
The same exact inert evidence is what connects the two environments; their
binary module topologies intentionally remain distinct.
