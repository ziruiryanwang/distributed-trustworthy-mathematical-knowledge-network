# Independent challenge: skipping addition for exact installed units

2026-10-26. Source-only review; no implementation, native execution, product
import, owner-state access, experiment, Git mutation or frozen-file edit.
Canonical guard passed. Read RECEIVED-VOCABULARY-QUERY, the independent
EXACT-INSTALLED-RELATION and EXACT-INSTALLED-INTEGRATION, and the relevant actual
codec, checker, native module, protected closure/controller/store and rebinder.

## Decision

**No unresolved principle-level blocker to the proposed conservative relation.**
It is sufficient under the existing protected-acceptance, pinned-kernel/codec and
immutable-import premises. It is not sufficient merely to remove
`INSTALLED_NON_THEOREM_OR_GROUP_COLLISION`, compare names/types, or call
`OwnerRebind.matchRow` in isolation. The following guards are indispensable.
Actual private/public equality for the retained AllClosure dependencies remains
unknown; this review does not authorize implementation or predict that result.

Let `U=(D,R)` be a complete already warranted unit, `N` its output names, and
`S` the basis plus registered anchor names plus preceding selected unit names.
Skipping `addDeclCore` is justified only if the installed interpretation of
every selected record equals the warranted one, with dependencies interpreted
in `S`, rather than whatever else happens to be installed.

## Bypass risks and their minimum defenses

| Risk when addition is skipped | Required defense |
|---|---|
| Valid descriptor paired with unrelated matching inventory | Bind descriptor to rows independently of shape parsing: singleton descriptor-derived `ConstantInfo` row equality; generated descriptor reconstructed from the selected actual inductive/constructor records and compared canonically. |
| Truncated or mixed generated inventory | Authenticate the entire original accepted unit and every sibling's warranted identity. All selected names must be present; same group owner, ordered `all`, constructor lists/owners/indices and generated metadata must agree. No prefix matching or partial-group regeneration. |
| Correct recursor type but altered computation | Compare full recursor rows, including ordered rule constructors, field counts, RHSs, motive/index/minor counts, `k` and safety. Exact inductive/constructor signatures alone are insufficient. |
| Ambient helpers silently supply meaning | Scan matched actual type/body/rule and group references against `S`, allowing only the current complete inductive unit's internal names. Preserve primitive/literal profile premises; a name scan does not itself prove those semantics. |
| Exact private body but unusable or different public declaration | Require concrete exact non-theorem records in the actual private/exported environments and both fresh imports. Definition/opaque axiom-shaped stubs fail; the existing theorem exception stays theorem-specific. |
| Same name resolves differently in kernel and frontend | Compare both selected kernel and frontend records. Missing/hidden kernel collisions or differing records fail; do not expose/promote an existing private record as a repair. |
| Success report or anchor silently broadens the relation | Reconstruct matched/added units from the exact request; derive a distinct non-theorem realization tag; bind new policy/support bytes through controller, store and native plan. Preserve old-anchor incompatibility across support changes. |

Concrete source basis for these objections:

- `P/installation/lean-src/OriginalDecl.lean:357` only checks singleton census or
  inclusion of inductive types/constructors. `decodeUnit` does **not** prove
  descriptor/inventory coherence or complete recursor generation. Its inventory
  parser mostly checks shape/bounds, so it cannot inherit a kernel-add result
  when that call is skipped.
- `CheckedExtension.checkBatch:99` normally supplies checked insertion, exact
  actual generated rows and a bounded stage-two census. The new match branch
  must not claim that these ran for matched units.
- `P/authoring/py/module_closure.py:226` actually fetches the complete unit,
  verifies its exact target/UnitID binding, and warrants every output before the
  restricted dependency planner builds the protected request. That is the
  relevant completeness premise; custody bytes or a preview alone are not.
- `OwnerRebind.groupScope:320` explicitly inherits complete accepted-group
  membership. `matchRow(.exact)` compares rows but neither proves that premise
  nor reconstructs the descriptor. The existing abstract-definition mode is
  outside this proposal.
- `P/module/OrdinaryModule.lean:211` currently checks frontend lookups; a generic
  successor must also account explicitly for the kernel lookup used by checking.
  Its `classifyUnits:260` currently lacks `S` as an input. The successor must
  receive or reconstruct the basis/anchor prefix and advance it in request order,
  not scan against every final output name or the whole ambient environment.

Here `P` is the unchanged package
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`.

## Complete groups do not require a global census

I specifically challenged whether an installed group's membership must be found
by enumerating the entire imported environment. It need not, under the stated
premise that `R` is the complete accepted output of `D` under the same pinned
generation semantics. Reconstruct `D` with bounded selected lookups; compare
every selected actual row and all group relationships. Unrelated extra installed
records receive no selected bindings and cannot be used through the restricted
dependency set. There is no need to prove that the environment contains no other
similarly grouped names to establish the meanings of this selected vocabulary.

Do not invoke `BootstrapProbe.groupMembers` over the ambient corpus as a hidden
implementation of this step. `makeUnit`'s descriptor reconstruction logic is
reusable with a selected bounded member map, not its whole-environment collection
path. If the complete accepted-unit premise cannot be authenticated, refuse;
neither matching the supplied prefix nor parser inclusion checks repair it.

The safe initial fragment is singleton safe definitions/opaques with exact
`all=[name]`, complete supported inductive units, and the unchanged separate
singleton-theorem branch. Mutual ordinary metadata stays refused. Public opaque
stubs stay refused. Keeping an actual added module delta avoids inventing an
all-installed-module workflow during this change.

## Persistence, payoff and stopping point

The integration proposal's three payloads are coherent: native module relation,
Python partition/controller policy and anchor realization validation. Worker and
closure can remain unchanged if the report field sets and protected phase binding
remain unchanged. Both private/public add passes and both fresh imports remain
mandatory; a new matching branch must not weaken new-declaration checks.
Only added declarations belong to the output module's own header.

Registered anchors may later use their existing lighter header/kind checks only
because the original complete relation was established and the exact protected
artifact/import chain and support identity persist. A saved hash or a caller's
new realization string does not independently establish that event. No old anchor
is relabeled or silently reinterpreted under the successor.

The owners have been sent the two implementation-sensitive clarifications:
selected kernel/frontend agreement and dependency-prefix threading. Their source
relation already includes them; no further speculative mechanism is needed.
The decision-changing next uncertainty is actual exact correspondence for the
four candidate installed units, not another architecture-wide audit. A bounded
comparison or mixed realization, if root later selects it, should preserve a
mismatch as a meaningful refusal. No larger limits, identity substitution,
body erasure, general renaming or acceptance-policy relaxation follows.
