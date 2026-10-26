# Ask about a received concept without proving a new theorem

2026-10-26. Source/data-only next-use decision; complete. No product imports,
native execution, owner-state opening, network, experiment or Git mutation.
The unchanged selected package is
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`.
Root owns any later implementation/runtime selection.

## Decision

**The public components can compose for compatible received definitions, but the
retained `RepairTheory.ClosureBridge.AllClosure` exposes an earlier obstruction:
the module exporter refuses its nonbasis Init definition/group collisions.** Its
closure is small; a larger cap or another query wrapper would not resolve this.
Do not claim a successful received-vocabulary query for this example.

Before selecting implementation, root should resolve the exact declaration
correspondence of this actual target closure. Existing exact row/group matching
is the first reuse candidate. Declaration equality can justify reuse when the
representation already matches; equal names or types cannot. A general importer,
new representation, identity migration or renaming scheme is not selected here.

The separate fixed-basis query work is unaffected. It intentionally refuses this
vocabulary, and its wrapper qualification does not qualify the richer route.

## One retained concept, used only as data

The source declaration is at
`experiments/v5-local-checks/concept-theory-b-export-01/sources/software/v5/concept_episode/TheoryB02.lean:81`:

```lean
@[expose] def AllClosure (o : OrderData α) (rs : List (Repair α)) : Prop :=
  ∀ r, r ∈ rs → IsClosure o r
```

Here `Repair` is an idempotent operation and `IsClosure` requires extensivity and
monotonicity in the supplied order. This is a concept used to develop the retained
repair/closure theory, not an invented theorem to satisfy a query API.

Its inert unit is
`experiments/v5-local-checks/concept-theory-b-export-01/bundle/units/52c32f0b4de89b9fed93bd099499dd7d029c6bc62e5de32bfeeaa25b08c9e3dd.json`.
Read-only inspection matched its 5,712-byte length and SHA-256
`fe0d8a292f3532f7da7a4a74ac41de7b267457193c8f417f7210e7a33767e90f`
to the retained `bundle/manifest.json`. It has one kind-1 definition row. Following
that manifest's complete nonbasis import graph against the selected installed
581-row inventory gives ten units, 21 rows and 62,079 manifest-declared raw bytes,
with no missing names and no kind-2 theorem rows. This is an inert graph census,
not reconstruction, acceptance or a complete native resource-fit claim.

A concrete next question would ask whether deleting the head of a list preserves
`AllClosure`:

```lean
forall {A : Type u} (o : RepairTheory.ClosureBridge.OrderData A)
  (r : RepairTheory.Repair A) (rs : List (RepairTheory.Repair A)),
  RepairTheory.ClosureBridge.AllClosure o (List.cons r rs) ->
  RepairTheory.ClosureBridge.AllClosure o rs
```

This question is illustrative unexecuted syntax, with explicit universe `u` and
no proof, new declaration or novelty assertion. The investigator wants to seek
consequences of a received abstraction before choosing which ones to prove.

## What already composes, and where this example stops

Let `P` denote the unchanged package named above. A successful independent
`receive` must first supply an explicit local warranted context and exact target
triple, with retained complete evidence. Custody or preview alone is insufficient.
For a compatible target the existing sequence is:

1. Use public `P/run.py ... owner -- export-module --catalog ... --custody ...
   --store-id ... --custody-limits ... --parent-root ... --module-targets ...
   --output ...`. The target file contains the actual `{name, export_id, unit_id}`
   from receive. `P/owner.py:447` and `:543` dispatch this operation.
2. Retain the locally generated module's exact artifacts and returned
   `module_name`/`import_directories` (`P/authoring/py/module_export.py:345`).
   Create a **fresh operator-approved local Lean workspace** if none exists;
   import that module and the package's built `OwnerQueryCommand` helper. No
   producer project, peer executable module or preexisting user project is needed.
3. Under an operator-provided equivalent finite execution envelope, run the
   selected Lean on `#ordinary_type_query [u] "FRESH_ABSOLUTE_PATH" : ...`.
   `software/v5/ordinary_formal_query/OwnerQueryCommand02.lean:68` elaborates and
   checks a type inside `withoutModifyingEnv`; it does not add a theorem or axiom.
4. Feed the successful inert type JSON to public `run.py ... query --
   --native-type ... --context-root ...` with the same protected owner selection;
   use the resulting specs in the existing bounded find operation. Context
   binding uses exact locally warranted symbols; it does not establish a foreign
   source project's equivalence (`P/query.py:197`).

The public local-query recipe exists in
`software/v5/ordinary_query_package/README.md:19`. The package launcher itself
accepts already extracted `native-type`, not local source/import options
(`P/run.py:42`). Therefore step 3 still needs the stated operator envelope; the
fixed-basis companion does not accept bridge imports. This is a later operational
boundary, not the first obstruction for `AllClosure`.

The module exporter fetches exact selected owner/custody records and follows all
nonbasis imports (`P/authoring/py/module_export.py:176`, `module_closure.py:187`).
`AllClosure` imports `List.instMembership` and `Membership.mem`; its ten-unit
closure also includes the `Membership` and `List.Mem` generated groups. These
are not in the fixed 581-row inventory, although the corresponding declarations
already exist in imported Init. The pinned runtime's `Init/Prelude.lean:1751`
defines `Membership`, and `Init/Data/List/Basic.lean:843` defines the list instance;
the Init import chain includes both.

`P/module/OrdinaryModule.lean:260` classifies any already present selected group.
Only an exact singleton theorem can take its installed matching branch; other
definitions/generated groups fail `INSTALLED_NON_THEOREM_OR_GROUP_COLLISION`
at line 278. Thus, assuming earlier warrants/custody checks succeed, this cold
module export refuses before producing the module. Neither the 106-unit bundle
size nor the absence of a producer project causes that refusal. No native run
was needed to identify this branch. An anchor is not a substitute for an absent
already-created compatible local module.

## Why contribution reconstruction is not a query workaround

The current `ordinary_contribution.py` validates 1..32 **new output names**
at line 149, always adds an export footer at line 234, then binds and admits
the candidate at lines 520 and 539. Its successful public operation cannot end
with only a question. Injecting a query then intentionally failing, or adding an
irrelevant output to make it finish, is not the requested public sequence.

It does contain useful existing machinery: protected target selection, exact
custody retrieval, `portable_owner_request.prepare`, finite source construction
and supervision. However, its scratch construction is expressly **not semantic
correspondence** (`software/v5/ordinary_lean/OwnerConstruction.lean:5`). At lines
177-180 an existing same-name safe record stops demand traversal without a body
comparison. This is appropriate for a receiver-interpreted candidate whose new
proof is later independently checked, but cannot establish that a query was
elaborated over the selected received definitions. Calling it "owner-derived"
does not erase that distinction.

The reviewed source and installed copies of `ordinary_contribution.py` both hash
to `09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8`;
both `portable_owner_request.py` copies hash to
`cf4a899642128f99839010248b5817a0e00e79411cfae36c4be654f85a6fc242`.
This trace is therefore not silently using an uninstalled successor.

## Smallest reuse-based choice versus ordinary project work

Existing matching already supplies the relevant principle:
`OwnerRebind.matchRow(..., .exact)` compares full non-theorem inventory rows
(`software/v5/ordinary_lean/OwnerRebind.lean:179`), and `rebindPrepared` checks
complete groups, dependencies and exact basis rows before exposing targets
(`:345`). `OrdinaryExport.compareSourceBasis:69` likewise compares the selected
foundation's actual records. The public module path already has inventory and
fresh-import checks. Reusing these exact comparisons for a supported collision
would be narrower than inventing a different semantic mechanism.

**Their existence is not a finding that these ten retained units match the
installed Init records.** That actual correspondence, public visibility and
atomic-group conditions must be reasoned through first. If they match, consider
the narrowest verified reuse of the existing declarations, then continue with the
ordinary module/local-query sequence. If they differ or are unavailable, preserve
the refusal; do not substitute name/type equality, discard bodies, expand the
basis implicitly or silently rename symbols. Renaming, if actually necessary,
needs an explicit checked correspondence/new artifact decision, not a search-ID
alias.

An exact-rebinding query adapter is another possible reuse composition, but is
not already public: `#ordinary_use` accepts the older V1 request header
(`OwnerUseCommand.lean:140`), while the current portable command dispatches the
best-effort constructor. It would need deliberate portable context binding and
proof-free execution glue. Do not select it merely because the functions exist,
and do not relabel V2 headers as V1 to pretend the route is already supplied.

Ordinary approved Lean work remains the comparator and fallback. A new local
workspace can contain locally reviewed definitions and ask the question directly;
no preexisting user project is assumed. That route pays its own authoring,
environment-correspondence and execution costs. Merely recreating a same-named
definition does not bind it to the received ExportID. An explicitly asserted
local interpretation can yield advisory receiver-interpreted search, with that
limit stated; later project-return/contribution admission still checks completed
outputs independently. The existing project-return path does not supply missing
query correspondence or eliminate the module-export collision.

The practical payoff of closing the supported exact route is that an investigator
can receive a new abstraction, formulate candidate laws/connections in its actual
vocabulary, search, and only then decide what to prove or contribute. This is
support for concept/theory development; it is not evidence of novelty, faster
discovery, broader recall or a whole-cost advantage. Stop at this decision: no
new mechanism, implementation or experiment is selected by this note.
