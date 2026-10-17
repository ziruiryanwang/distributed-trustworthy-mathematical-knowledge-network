# Actual client mathematics and import review

2026-10-16. Independent reviewer: `memo_tests_review`.

## Disposition

**PASS for the proposed mathematics and inspected source boundary.** The seed
fusion theorem and consumer paired-fold projection have valid mathematical
arguments using the retained foundation and base module. The owner inspects the
actual root theorem's exported proof closure, rather than treating a textual
name or a constant anywhere in an export as evidence of reuse. No blocking
mathematical/source finding was identified.

This is not executed Lean elaboration, native acceptance, actual reciprocal
operation, growth benefit, cryptographic assurance or launch clearance. No
project module was imported, no native process/test was run, no Git mutation
was made, and no previously used evidence was changed. PowerShell was used only
to read source/data and compute file identities. Root owns selection and runtime;
the separate lifecycle reviewer owns operational/resource inspection.

## Reviewed identities

Paths below are relative to the sole canonical root,
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/client/actual_owner.py` | 22521 | `2f2f07aa6ac91618120b210abec99ddbef4818332bd2d7915e6b0c837efc1016` |
| `software/v5/client/actual_assets.py` | 10738 | `0cef5f4e8ff7590d52f51d73f3fa42ca23ab4ace4a75eeff16dd0df49f68ef87` |
| `software/v5/authoring/AuthorLean.lean` | 42799 | `00f90c7f449d1228227d89fc251283061ccfa59791e5bd563e058b3d41f1f78e` |
| `software/v5/modules/source_rows.py` | 15320 | `60c7255d9bf65236d684a77e2890c00567dba5bc2f72b81d13c933af237913f4` |
| `software/v5/authoring/context.py` | 10243 | `a6d0b794204fb92dd43b7b63d38cd4f4dd15dff5d7f33d0254c4f1cbc1650541` |
| `software/v5/mixed_claims/authoring.py` | 23676 | `8b09cb1b8f0466a5049ed53f7b28098b6022234e3681786b2f4a9f542cd83e1b` |
| `experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json` | 53769 | `09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926` |
| `experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json` | 23313 | `736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c` |

The inspected ordinary-owner source was fresh/unexecuted at this review. Later
source edits require a changed-boundary review, not silent transfer of this
disposition. The argument also used the retained source blueprint
`software/v5/workloads/FoldFusion.lean`; the proposed operation does not import
that blueprint or borrow its saved proof output.

## Exact mathematical boundary

The selected base module is
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
Its actual bundle declares:

- `Tree`, `Tree.leaf`, `Tree.node`, `Tree.rec`;
- `Tree.below`, `Tree.brecOn.go`, `Tree.brecOn`, `Tree.casesOn`;
- `fold.match_1`, `fold._f`, `fold`;
- `map._f`, `map`; and
- `binary_congr`.

All names are under `CommonsV5`. There is no base `fusion` or
`project_summary`. A fresh local `ClientV5` theorem is therefore an extension,
not republication of either theorem already in the admitted base. This does not
claim novelty in mathematics or in other participants' libraries.

The retained foundation's decoded declaration census includes `Eq`, `Eq.refl`,
`Eq.rec`, `Eq.trans`, `Eq.casesOn`, `Eq.ndrec`, `Eq.symm`, `rfl`, `HEq`, `PUnit`,
`PProd`, `Prod`, their constructors/recursors, and **both `Prod.fst` and
`Prod.snd`**. Product and both projections have two universe parameters. There
is no `congrArg` declaration in this census. The plan's suggestion that using
a lambda avoids a missing named `Prod.fst` dependency is unnecessary: the named
projection is already present. The proposed lambda is nevertheless valid.
This documentation correction was sent to the plan author; no extra test is
needed for it.

## Why the two proofs are valid

Let `fold l n` interpret a tree by mapping leaves with `l` and combining child
interpretations with `n`. Given functions `h : B -> C`, `leafB`, `leafC`,
`nodeB`, and `nodeC`, assume

\[
h(\operatorname{leafB}(x))=\operatorname{leafC}(x),\qquad
h(\operatorname{nodeB}(x,y))=
\operatorname{nodeC}(h(x),h(y)).
\]

The seed theorem asserts

\[
h(\operatorname{fold}(\operatorname{leafB},\operatorname{nodeB},e))=
\operatorname{fold}(\operatorname{leafC},\operatorname{nodeC},e).
\]

Structural induction on `e` proves it. The leaf case is precisely the first
assumption after unfolding `fold`. In the node case, the second assumption
gives the first equality; imported `binary_congr nodeC ihl ihr` substitutes the
two induction hypotheses; `Eq.trans` composes them. No associativity,
commutativity, extensionality, classical choice or additional axiom is required.
The source explicitly chooses `Tree.rec`, reducing reliance on elaborator
eliminator-selection metadata for the reconstructed inductive.

For projection, instantiate fusion with the intermediate algebra `B × C`,
paired leaf map, componentwise paired node map, target algebra `B`, and
`h = fun pair : B × C => pair.1`. The leaf and node preservation obligations
reduce by beta reduction and product projection; each is `rfl`. This yields
the stated equality of the first projection of the paired fold with the
`B`-only fold. The intermediate universe is `max v w`, and the target universe
is `v`; polymorphic fusion admits this instantiation. Both generated theorem
types genuinely use all three declared universe parameters.

The owner has explicit `autoImplicit false`, `noncomputable section`, and
`universe u v w`. The source contains no numeric/string literals, `simp`,
`congrArg`, or new axioms. Product notation is supported by the pinned Init
frontend and retained foundation. Exported `.proj` expressions have an explicit
representation in both the native exporter and `SourceRows` decoder.

The theorem supplies a reusable equality; it does **not** by itself prove an
operational saving or compel a consumer to avoid calculating the second
component. A later rewrite/optimization strategy and an explicit resource model
are needed for that claim. This operation is a reciprocal-use gate, not the
full-cost growth comparison.

## Import and actual-use evidence

`prefix()` opens the exact relocated base namespace. `projection_source()`
validates the discovered module digest and directly applies
`DMKN.Mod.«<discovered>».ClientV5.fusion`; it does not declare an axiom, copy the
seed proof, or receive the seed ModuleID as a search input. Consumer discovery
uses the known base `fold` export and formal theorem/`Eq` features. After
candidate resolution it checks the returned relative method name and binds
the acquired warrant to that discovered ModuleID.

The consumer takes the exact base/fusion journals from the acquired warrant's
members and openings/bodies from `semantic_material(warrant)`. It does not take
the original base bundle as its authoring input. Both modules' selected groups
and their transparent semantic dependencies are supplied, rather than only a
public `fold` declaration whose auxiliary definitions are unavailable.

The existing context builder checks references and body commitments, produces
typed missing-data demands, and orders imported groups by dependencies. The
native frontend checks foundation descriptors against pinned Init and installs
imported definitions with their bodies. Imported theorem interfaces become
temporary frontend axioms **inside untrusted preparation**; that is not a new
mathematical acceptance mode. The final mixed/native relation must discharge
their admitted parents. The exporter skips imported boundary declarations and
rejects newly introduced local axioms.

`inspect_author()` binds the source bytes, requested roots, export, produced
packet and decoded local spec. It starts from the selected theorem's actual
`env.local_proofs[Address.of(env.module, root)]`, reads its proof body, and follows
local proof/value dependencies with finite visit/declaration limits. It requires
the exact external base `binary_congr` edge for the seed and exact acquired
fusion edge for the successor. It separately checks the root theorem's type
references the base `Tree` and `fold` and has three universe parameters.

The decoder validates the name/level/expression index domains, backreferences,
name-role partition, local declaration census and expression expansion limits
before this traversal. The proof inspection therefore does not mistake an
unrelated export row, name-table entry or source-text occurrence for proof use.
Its traversal includes type subterms inside a proof expression: it establishes
the reported proof-closure reference, not a general theorem of semantic
indispensability. For these fixed source terms, projection is visibly a direct
application of the acquired fusion result, so this distinction is not a blocker.

Both preparation and this inspection explicitly return non-authority. Actual
seed admission occurs at the fresh consumer; successor admission occurs on
the cold client. A passing inspection alone cannot substitute for either.

## Remaining actual checks, without duplicate experiments

The smallest selected client operation must still establish:

1. Successful elaboration/export of these exact generated sources under the
   pinned frontend and imported reconstructed context.
2. Native acceptance of the acquired seed and retained successor, with the
   declared actual proof-reference inspections passing.
3. Successful publication, packet-only semantic reconstruction, fresh owner
   admission and service cleanup, as judged by the lifecycle/actual reviewers.

There is no reason to launch a separate mathematics-only test first: these
checks belong to the one integrated operation already proposed. The cold phase
is fresh client/owner authority in the same Python process/host, as its source
correctly states. Native delta ancestry above I is still checked at reception;
zero ancestor theorem-proof bytes in ordinary frontend import does not imply
constant cold verification cost for arbitrarily long unaggregated chains.
Affordable frontier advancement and full-v5 release remain open.

## Actual operation 01: preparation failure, no mathematics reached

Root requested a terminal-only inspection of the existing
`product-local/v5-client-owner-runs/client-actual-01` output. Its plan identity is
`dad9f1d436c71f836d467fe14713d38e975563bd067836996eb292ec0d9b60d2`.
The saved owner/assets snapshots exactly match the two source identities above.
No launch or rerun was performed by this reviewer.

**Disposition: FAIL before any mathematical operation.** `RESULT.json` records
`COMMAND_FAILED`, child exit 1. `BOOT-FAILED.json` records
`CLIENT_BOOT_OR_OWNER_FAILED` with `StructureError: EXACT_RECORD_FIELDS`.
The actual traceback reaches `Strategy.__init__ -> Assets.__init__` at
`C.fields(params["assets"], RETAINED)`. The selected codec requires its second
argument to be a set of field names; the supplied `RETAINED` object is a dict.
Thus `set(value) == names` is false even though the plan's asset names are the
expected eight names. This is an adapter schema-validation defect, not a
mathematical rejection or evidence of bad input mathematics.

The failure precedes asset receipt/bundle loading, `Strategy.run`, seed workspace
creation, finite-grant construction, owner construction, receipt verification,
source authoring and native delta admission. The output's `work` directory is
empty. There is no source-request, exported Lean proof, owner actual-result or
fresh mathematical acceptance evidence to audit. Consequently **zero client
receipt/native/author calls were reached**, and neither proposed theorem has
executed evidence from this operation. The earlier mathematical argument is
unchanged; its source-only disposition did not establish executable adapter
correctness.

Exact retained outcome identities:

| Relative to `client-actual-01` | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2253 | `342303c66d75ac3d7987d7ad72eae74b4640417d498f12a742d3ecf8b8bf448c` |
| `BOOT-FAILED.json` | 87 | `c99ab7e76b9858a8a895eec36c74935906186f7044aff90a1f227da8ecf44bc9` |
| `command/stderr.txt` | 1830 | `3ac74b9eee0d5e714f89879ab0c441f771d204f9d4593a718ecf4c180834aaa4` |

The operational result reports direct child reaped, final active processes zero,
no termination requested, and no cleanup errors. Lifecycle adoption and any
fresh successor selection remain root's/separate reviewer's responsibility.
No actual proof-reference check passed; do not relabel this operation as a
mathematics or reciprocal-use pass.
