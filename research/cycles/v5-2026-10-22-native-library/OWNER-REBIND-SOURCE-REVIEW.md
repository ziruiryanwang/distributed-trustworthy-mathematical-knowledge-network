# Independent owner-rebinding source review

2026-10-23. Reviewer: `admission_event_audit`. Source-only; no runtime, tests,
compilation, implementation edits or Git operations. The completed recovery
outcome audit is not repeated here.

Reviewed primary sources:

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/OwnerRebind.lean` | `a7fbb85189fbee3d816c822d56bb8642e48e24f8952776ec9439fea12b6f6e01` |
| `software/v5/ordinary_lean/owner_request.py` | `b6f39083728304c49f99cd8c223b5e44b3fa89a4c6a1092ec7eefdeddabfcd17` |

Supporting sources inspected: the existing evidence/ordinary declaration and
checked-extension contracts, `BootstrapSupport` basis/group functions, actual
Lean 4.34 `Environment.addDeclCore`, `addConstAsync`, `commitConst`,
`commitCheckEnv`, and namespace-extension implementation. Also read
`OWNER-REBIND-PLAN.md` and `OWNER-REBIND-IMPLEMENTATION.md`.

## Disposition

**No blocking semantic defect found in the selected conditional design.**
The combination can support ordinary authoring without requiring the original
proof body of every existing theorem. It does not establish whole-owner
soundness or replace the independent receiver acceptance event.

This is not a compilation pass: root reports build01's concrete module/import
packaging failure. Repairing the public support import assembly is a separate
necessary step. Its final exact source/compiled map and any changed matching
semantics must be reviewed before adoption. No memory-cap change follows from
this source review.

## Why theorem interfaces are sufficient here

Let `K` be the protected accepted context and `O` the owner authoring environment.
The precondition is a stable controller-authenticated mapping from selected
native names to their warranted symbols in `K`. The helper is not allowed to
derive this mapping from an owner declaration, a supplied hex ID or an arbitrary
dictionary.

For a selected theorem, the request producer derives mode 0 only from kind 2
of exact evidence whose computed export ID matches that protected mapping.
`matchRow` then requires the owner record to be a safe theorem or existing
axiom-shaped handle with exactly the selected original universe parameters and
type packet. Its type dependencies must already have corresponding warranted
meanings. No new axiom is inserted and no owner proof is promoted.

An arbitrary owner assumption **without** the accepted theorem warrant cannot
pass the preparation precondition. Conversely, an existing axiom-shaped handle
with exactly the type of an already warranted theorem is not inherently an
error: it is a usable authoring name for independently warranted mathematics.
Confusing those cases would either weaken trust or unnecessarily reload private
proof histories. The final exported successor must still be checked against
actual `K`, not against the owner's assumptions.

The fixed basis is explicitly different: exact pinned inventory bytes identify
the accepted profile; theorem rows use its existing normalized type/arity
correspondence, while permitted basis axioms and quotient primitives retain the
fixed name/kind/policy checks. The known normalized basis projection is not
misrepresented as exact original binder/hint equality.

## Correspondence and closure checks

- **Evidence identity:** `owner_request.prepare` validates exact fixed inventory
  bytes and basis ID, rereads each bounded raw ordinary evidence envelope, checks
  its profile and target ExportID, and checks all unit/import symbols against
  the stable protected lookup. Same spelling alone is not accepted identity.
- **Selected dependencies:** existing theorem rows follow types only; definitions
  and non-theorem opaques include value bodies; inductive/constructor/recursor
  rows retain structural references and recursor rules. Missing units additionally
  schedule their full construction dependencies. The request keeps exact complete
  generated units, not selected fragments of a group.
- **Ordering:** one selected group graph is topologically ordered. Overlapping
  units, unclosed references, cycles and partial owner-group hints refuse.
  Coalescing an already scheduled group does not discard identity checks: the
  scheduling lookup has already matched the requested symbol to the same stable
  context.
- **Actual owner membership:** the Lean helper independently classifies every
  group as wholly present or wholly absent. Partial presence refuses. Incorrect
  absence hints cannot authorize installation or overwrite: absent groups require
  full construction data; existing groups must match their selected semantics.
- **Transparent/data meaning:** mode 1 rejects axiom/theorem substitutions and
  compares the exact ordinary inventory row, including type, value, metadata,
  generated rules and universes where applicable. Same type/different body fails.
  The theorem-interface rule is not silently extended to opaque data values.
- **Reference closure:** matching a record is followed by actual semantic scans.
  Ordinary singletons may use only earlier bound names. Complete generated
  groups additionally permit their own members, require one actual common group
  owner, and retain exact accepted generated inventory. Helper-local name lists
  alone do not prove group completeness; that comes from the authenticated,
  previously accepted unit supplied by the controller.
- **Missing declarations:** decoding and the explicit construction-reference scan
  admit only prior bound names and the allowed inductive self-types. The unchanged
  checked-extension code performs actual checked addition and generated-inventory
  comparison. Unrelated owner declarations cannot become new premises merely by
  being present in the surrounding environment.
- **Targets:** requested symbol IDs must equal the bound mapping; both kernel
  presence and usable frontend presence are checked with the appropriate
  theorem-interface, exact semantics or normalized basis rule.

## Atomic caller-visible update

`rebindPrepared` keeps a local candidate initialized from the immutable owner,
requires a top-level owner, and never calls `setEnv` or `modifyEnv`. Failure in
a later group or target check returns no candidate environment to the caller.

Actual Lean `addDeclCore` returns a new environment and new frontend-map values.
The recursor exposure path only handles records returned by the actual new
checked batch. `addConstAsync` creates fresh promises and maps on that candidate;
both `commitConst` and `commitCheckEnv` are resolved before retaining `mainEnv`.
This does not mutate the old owner's name map or expose unrelated private
records. Namespace registration likewise returns an updated candidate extension.

The eventual command must install the returned environment **once after complete
success**, with no fallback installation on exceptions. That command and its
request-byte authentication are not implemented by these two files. No claim
about atomic filesystem/catalog changes follows from this environment property.

## Resource and practical observations

The selected closure is bounded by distinct names/groups/edges, raw acquisition,
payload and expression work, not by a census of every owner/library constant.
The helper charges cumulative semantic scans and both construction scans across
missing groups; independent CPU/wall/memory supervision remains necessary.
Repeated stage-two census work in one-unit checked additions is a real cost for
many missing groups, but not a reason to add another batching framework before
the intended few-method-declaration integration works.

One cheap prelaunch improvement is advisable: compare
`PreparedRequest.materialized_units` with the selected helper's
`maxCheckedUnits` (default 1024). The preparer permits 8192 total groups, which is
appropriate for existing semantic correspondence, but an all-missing request
over 1024 groups is predictably refused later. Reject that known oversize plan
before native work. This is an efficiency observation, not a mathematical
acceptance bypass and not a blocker for the intended few missing declarations.

Preparation still obtains retained full evidence for selected groups, including
proof syntax for existing theorems, although it neither traverses their proof
ancestry nor transmits their proof bodies in interface rows. The docstring
correctly discloses this limit. Failed network retrieval accounting and bounded
receiving are caller obligations; checking `len(raw)` after callback return is
not a network download cap.

## Remaining integration obligations

The authenticated context-to-callback relation, immutable prepared files,
raw-byte lexical limits, pinned helper/runtime assembly and single final command
environment update must be wired by the trusted controller. A fabricated
`Prepared`, `context_id`, callback or symbol string is not an independent warrant.

The next useful evidence is actual ordinary source use followed by inert export
above this warranted boundary and independent checking of the substantive
successor. Cheap changed-boundary negatives should cover unbound theorem stubs,
same-type/different-body definitions, unbound semantic references, partial groups,
wrong target identities and late failure without caller-visible new names.
Recursor frontend exposure needs a runtime discriminator only if the selected
workflow actually takes that path. This source review establishes none of those
runtime outcomes, discovery effectiveness, growth advantage or final v5 readiness.
