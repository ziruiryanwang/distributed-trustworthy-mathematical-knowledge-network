# Baseline usefulness: preserve the ordinary project, not just its constants

2026-10-24. Root source/theory checkpoint. The preview capability is adopted in
Git `43c6ff0`. No baseline implementation, native experiment, trust-policy change
or new resource grant is selected by this note.

## The decision that must precede more code

Strict baseline intake is promising, but intake alone does not make a useful
ordinary Lean background. There are two independent obstacles in the current
module bridge:

- Its bounds cannot materialize the already recorded 2,852-unit example.
- `OrdinaryModule04.classifyUnits` refuses every installed definition/group
  collision, and the writer intentionally does not reproduce arbitrary frontend
  extension state. Raising bounds does not resolve either semantic compatibility
  or the practical loss of library notation, instance/simp registries and tools.

The extension-state point is a source-derived workflow concern, not a new
experiment showing that every kind of frontend metadata is absent. Ordinary
Lean imports the generated module's actual dependencies; metadata already
provided by those dependencies remains available. Current root import is Init,
not a user's general library. The public path must preserve a useful selected
background rather than assume a collection of constants is a full replacement
for its original project.

## Three different routes

**A1: strict admission followed by regenerated modules.** Independently check
missing inert units, then realize the warranted background through the current
module bridge. This preserves strict mathematical assurance. It needs a coherent
baseline capacity profile and exact installed-definition/group correspondence;
it also needs an honest account of unsupported frontend metadata. It may be
appropriate for source-free consumers without an existing familiar library.

**A2: strict admission followed by correspondence to an approved local project.**
The user already has and approves a native Lean library for ordinary authoring.
Independently check the relevant baseline units in the commons, then establish
exact correspondence between those warranted meanings and the selected local
library artifacts. Emit only the unfamiliar received delta, importing that
approved background. The ordinary project retains its existing library tooling.

This would not require trusting a compiled library's mathematical claims if the
needed baseline is independently warranted and its correspondence actually
checked. Artifact approval is still necessary for local execution/deserialization
safety. Approval alone must never satisfy mathematical correspondence. No peer
binary, saved PASS or unverified signature is a substitute for that relation.

**B: approve the compiled baseline as a mathematical premise.** This avoids
strict baseline checking, but changes the assurance claim. It requires a distinct
explicit policy and cannot display strict seed-derived acceptance. B remains
unselected; the user's willingness to consider compromises does not silently
adopt any particular library or trust policy.

A2 may offer better payoff than rebuilding familiar backgrounds or implementing
B. It is a candidate to audit, not an established implementation or free import.

## Conditional correspondence obligation for A2

Let K be the protected independently checked context, L the approved local
library environment, and U a complete selected extension with exact dependency
identities. Let D contain every semantic dependency needed by U, closed under
types, definition bodies, computation rules, generated groups and the fixed
implicit-support policy. The proposed local warrant must establish:

1. Every selected baseline unit in D is already warranted in K, with complete
   output census and exact dependency identities. Whole groups are not split.
2. The selected artifact/import graph produces the same relevant interpretation
   in L: exact names, universes, safe kinds, types, transparent bodies and
   generated rules. Type signatures alone are insufficient for definitions.
3. The existing theorem-specific public proof-erasure relation remains confined
   to independently warranted theorems with a full exact private match. It does
   not become an opaque-definition or arbitrary-axiom exception.
4. Private and public imports are checked separately. U's actual public kernel
   check and fresh emitted-module rereads remain mandatory. Extra ambient
   declarations in L do not authorize references absent from the selected exact
   dependency closure.
5. Only owner-selected immutable artifacts and the complete selected import
   graph are loaded. Cached correspondence is tied to exact artifact bytes,
   semantic IDs, support policy and the protected checked context. A changed
   dependency invalidates that cache rather than silently retaining its status.

Under these premises, transferring the relevant warranted interpretation from K
to L is a correspondence argument, not adoption of L's unchecked proof claims.
The new delta can be checked in that interpretation. This is still conditional
on the kernel, codecs, importer and protected local storage; hashes identify
artifacts but do not prove correspondence. The argument must account for actual
Lean reduction/visibility semantics before code is selected.

## Current action and stop rule

The bundle author specifies strict finite intake using existing admission and
explicit protected roots, without a new generic cursor scheduler. The native
author compares A1 and A2 against actual bridge/import code. The independent
reviewer challenges group completeness, hidden definitions, implicit rules,
public correspondence and the all-matched case. Root owns the final choice.

Do not launch a large import, broaden resource caps, copy a user's library,
or rebuild the checker merely to produce another passing milestone. Select
the smallest consequential implementation only after a coherent route reaches
normal project use, not merely a larger accepted database. Reuse the existing
271.15625-CPU-second historical cold result as evidence that one-time strict
checking can be plausible; it is not a prediction of total baseline cost.

## Resolved source refinements and next integration boundary

Later on 2026-10-24, the revised realization contract separates the full private
checked proof closure from the derived public reusable interface. The actual
public representation controls its edges: an allowed erased singleton theorem
needs its type dependencies publicly; a full public theorem conservatively
retains proof dependencies too. Public definitions and generated computational
groups still require exact full records. Independent review clears this
sufficient relation; no abstract-definition relaxation was selected.

Root also inspected the pinned runtime's `Lean/Environment.lean` and
`Lean/Setup.lean`: `importModulesCore.loadData/loadIR` use exact `ImportArtifacts`
when present and otherwise fall back to name-based search. `EnvironmentHeader`
records effective module imports, while `ModuleData.imports` preserves the direct
flags. Ordinary modules use multipart `.olean/.olean.server/.olean.private` and
`.ir.sig/.ir` data; available parts may be loaded opportunistically. Hence a map
covering only the direct project modules is not a complete import binding.

For A2, snapshot all selected transitive semantic and frontend artifact parts,
preserve original module names and import flags, then run correspondence against
that snapshot. Require the actual imported module census to equal its selected
closure and disallow unbound name-search fallback outside explicitly pinned
runtime/snapshot support. A normal future consumer must use the same controlled
resolution. A later local project rebuild cannot silently change the reference.
Do not assume that a `.olean` hash alone binds optional parts or runtime imports.
Owner-approved arbitrary native plugins remain an execution premise; neither
this snapshot nor `loadExts := false` is a hostile-code sandbox.

Fresh producer/binder/intake source is now selected in the implementation
selection, with no runtime. The next reference/delta implementation must reuse
these importer mechanisms, not launch another full compiler/library campaign.

There is also an existing ordinary frontend connector: pinned
`Lean/Setup.lean:188-215` defines the `--setup` CLI's `ModuleSetup.importArts` as
pre-resolved artifacts of transitive imports. Prefer assessing this native
mechanism before inventing another authoring loader. Its explicit direct imports,
module flag, empty plugins/dynlibs and bounded owner-written setup document can
bind a normal source compile to the selected artifact map. A map still needs
closure validation; missing entries otherwise permit name-search fallback.
Merely adding a snapshot directory behind the current runtime-first project
search path is insufficient: a changed runtime `.olean` could shadow the copied
bytes. This is a source-derived integration direction, not an implemented or
tested setup-file path. Root shared it with the artifact-connector author.
