# Existing installed declarations: exact reuse without a larger foundation

2026-10-23, retained_preparation. Source/theory only; canonical guard PASS.
No code, runtime, owner opening, build, package or Git changes. This investigates
the next library-usability gap, not the current bridge's implementation review.

## Decision

**Exact reuse is defensible in principle.** A name collision need not force
rejection when the complete installed declaration is the same selected, locally
warranted mathematical object under already matched dependencies. Treat it as a
derived interpretation of an existing checked unit, not an additional axiom or
an enlarged fixed foundation. Equal names or equal theorem statements alone do
not establish that interpretation or preserve the original ExportID.

First use the cheaper alternative: if an approved ordinary package already
supplies every needed result, import that package normally. Nat.add_zero already
comes from installed Init; re-exporting it solely to produce a bridge artifact
adds no mathematical capability. The matching seam matters for a **mixed**
commons result that uses such a name and also contains genuinely new local
declarations. It must not force users to rename standard mathematics or discard
useful accepted proofs merely because ordinary Init already contains them.

## Conditional preservation argument

Let F be the unchanged fixed foundation, Gamma the selected warranted context,
and Delta the local installed module environment. For the bounded selected unit
closure, maintain a partial relation R between Gamma's exact SymbolIDs and
Delta's actual records. Initially R is only the existing full fixed-basis
correspondence, with exactly its already selected normalization/primitive rules.

For each dependency-ordered unit U, require:

1. Complete canonical evidence, original UnitID/ExportIDs and every group output
   are warranted by Gamma. Every direct import has its exact recorded SymbolID,
   and has already been related by R. Include proof-only imports and recursor
   rules, not merely names occurring in statement types.
2. The original descriptor round-trips through DeclCodec. Every existing output
   record has exactly the selected ordinary full inventory row under the existing
   mdata-only expression normalization. Reject axiom, unsafe or partial records;
   require actual name-key agreement and complete all-or-none group presence.
3. No additional name becomes an allowed decoder reference merely because Delta
   contains it. Every new checked declaration uses only F plus already related
   selected units, subject to the current literal/kernel semantics.

If U is absent, unchanged kernel checking constructs it. If it is fully present
and matches, extend R without redeclaring it. Validity of the matched declarations
then transfers from their genuine checked warrants through the already-related
dependencies. Induction over the closure preserves derivability under F. No
premise says that *all* of installed Init is checked or accepted by the commons.

This is a relative assurance argument, not a machine-checked refinement theorem.
It relies on correct canonical codecs, the selected kernel/literal semantics,
protected genuine warrants, immutable installed artifacts and the usual identity
hash assumption. A fabricated callback claiming acceptance defeats its premise;
custody possession cannot replace Gamma's warrant. Full matching is sufficient,
not necessary: an equivalent theorem with a different proof can legitimately
fail this exact-identity route. That conservative refusal is preferable to
inventing an unproved equality between distinct ExportIDs.

## What full equality must retain

`OriginalDecl.lean:inventoryRow` already retains kinds, original universe-parameter
names, types, theorem/definition/opaque values, definition reducibility hints,
mutual-block metadata, inductive parameters/indices/constructors, constructor
metadata, generated recursor rules and safety flags. `OriginalExpr.lean` erases
only Expr.mdata. Use this ordinary inventory for selected **extension** matching.

Do not use `OwnerRebind.matchRow`'s mode-0 theorem interface or
`matchBasisRow`'s authoring projection: they intentionally accept signature-shaped
handles and omit theorem values. Nor may the fixed foundation's special normalized
height override from `Export.compareSourceBasis` be generalized to arbitrary
extensions. Different extension reducibility hints or group metadata must refuse
unless a new explicitly justified semantic relation is separately adopted.

Locally warranted full units already supply the descriptor-to-generated-inventory
relationship. Syntax-only inventory equality without that checked warrant would
not prove that a purported generated group was legitimately constructed.

## Public visibility is a separate, real obstacle

Private exact matching does **not** imply ordinary public-import compatibility.
An installed theorem may expose only a signature handle, or a definition required
for conversion may be hidden. The present bridge demands full exported inventories
for its new declarations; it cannot silently reuse a weaker authoring-mode test.

The smallest conservative successor should require the existing matched names to
pass exact required public-view checks too, otherwise refuse. If normal Init's
public theorem representation lacks its full proof, a later explicitly specified
interface-erasure relation could use the private checked proof plus a linked
public signature of the **same authenticated module origin**. That requires
separate assurance of matching levels/types, opacity and artifact-origin linkage;
it is not acceptance of an arbitrary same-typed axiom. No such relation is
implemented here. Missing transparent computation must not be hidden by it.

Both private and public views must resolve each selected reference consistently.
An actual normal consumer remains a useful targeted compatibility discriminator,
not a substitute for the identity argument. Ordinary consumers may choose to
trust additional Init declarations themselves; later commons admission still
requires those contributions' actual dependency closure under the commons policy.

## Concrete minimal implementation seams, if later selected

- Keep `module_closure.collect_closure` unchanged: still collect all warranted
  selected nonbasis proof units above F. An installed match must not stop evidence
  traversal or silently add a new collector boundary.
- Reuse `DeclCodec.decodeUnit/encodeDescriptor` against the preceding selected
  allowed-name set, then classify each full unit as absent, fully exact-matched
  or conflicting/partial. Begin with singleton theorem/definition/opaque units;
  keep generated-group collision refusal until its full matching gate is reviewed.
- Use `DeclCodec.inventoryRow` for actual private records and
  `CheckedExtension.allowedDeclaration`/`requireName` safeguards. Call unchanged
  `CheckedExtension.checkBatch` only for absent units; never disable `doCheck`
  or suppress `OVERWRITE_OR_DUPLICATE` inside the kernel-checking routine.
- Track separate `matched` and `added` inventories. Module writer/header census
  must contain only `added` records; target resolution may include matched imports.
  Existing `checkInventories`, `checkWrittenHeader` and private/public rereads need
  explicit two-category handling, not a changed expected-count assertion.
- `Environment.getModuleIdxFor?`, `allImportedModuleNames`, `header.moduleData`
  and `setExporting` provide origin/view inspection. Preserve approved installed
  import/artifact restrictions; do not load peer native modules or initialize
  untrusted extensions merely to inspect a same-named record.

When all selected targets match existing approved imports, return a local exact
resolution manifest rather than manufacturing an empty module. When some are
new, write only those additions and retain the matched import bindings in the
manifest. Cache identity must bind exact selected closure, matched origin/artifact
support and policy, not mutable context_root. Initial cost still includes selected
proof closure acquisition/matching; no proof-independent cold cost is claimed.

Recommended next decision: finish the current genuinely new-name bridge first.
Then, only if its mixed-standard-library reuse is the next actual blocker, select
one singleton exact-match successor and one mismatch/public-visibility refusal.
Do not grow a general declaration-equivalence engine or replay Nat.add_zero alone
as a useful-growth benchmark. No implementation or new experiment is selected by
this note; actual matching and public compatibility remain to be established.

## Pinned visibility analysis and minimum theorem-interface rule

2026-10-23, project_hook_design; separately assigned source-only continuation.
No Lean/Python/project import, owner operation, build or experiment was run.
This section resolves the public-visibility uncertainty above. It does not select
implementation, and it deliberately avoids new per-origin machinery.

### What the selected Lean sources actually do

In the selected Lean 4.34.0 source, `Lean/AddDecl.lean:111` onward represents a
normal module theorem privately as `thmInfo` and exports a safe `axiomInfo` with
the same `ConstantVal` (name, ordered universe parameters and type). This is
intentional proof-body erasure. The low-level `forceExpose` option can preserve
a full theorem, but ordinary theorem elaboration does not request it.

The saved mixed collision request already contains exactly two singleton theorem
units, in dependency order:

- `Nat.add_zero`, UnitID
  `2951fcf2eb813a9c4472c8a58f6ff51d1389363f9c2d2cace207ca28319887ae`;
- new `CommonsLibraryExample.add_zero`, UnitID
  `6f0a5a17f40dbca4e4f0eabb86c6d6a2dfd0eeb0056d36e81373a2e185cd51c8`.

The request is preserved at
`experiments/v5-local-checks/ordinary-module-native-03/collision-refusal/request.json`,
SHA256 `0070f06dc523bf03194c7a5a4b015d9e908e5ccb26ae6a68078cf429ec188032`.
It records the full original `Nat.add_zero` proof, not just its signature.
`Init/Core.lean:747` declares that theorem by `rfl`. The `@[expose] section` at
line 21 does **not** establish full theorem visibility: `MutualDef.lean:1345`
onward applies that section rule to definitions, with separate rules for
abbreviations and non-Prop instances. The theorem export erasure remains.
Thus requiring full private/public inventory equality for every matched theorem
would predictably reject normal installed theorem interfaces. This is a source
prediction; no new native visibility measurement is being claimed.

`Environment.mkModuleData` selects full kernel constants for the private part,
but public-view records for the exported part. `writeModule` saves exported,
server and private data in that order. `finalizeImport` similarly builds separate
private and public maps. This explains why private full matching and ordinary
public usability are distinct checks rather than interchangeable observations.

### Origin linkage is sufficient, not logically necessary

The earlier proposed same-origin condition is stronger than the mathematical
interface rule needs. Let `p : T` be a complete singleton theorem independently
warranted in the selected context Gamma under fixed foundation F. Let R already
interpret every direct dependency of that theorem with its exact recorded
SymbolID. An exported safe handle with the exact name, ordered universe parameters
and original encoded type T can be interpreted by that already warranted theorem.
This does not assert that the handle's native bytes contain p or originate from
the module that originally proved p.

Formally, write `Sig(c)` for name, ordered universe-parameter list and the original
encoded type, erasing only the already specified expression metadata. The narrow
proposed rule is:

\[
\frac{\Gamma\vdash_F p:T\quad R\text{ covers the exact dependencies}
\quad \operatorname{Sig}(c)=\operatorname{Sig}(p)
\quad c\text{ is a safe theorem-interface handle}}
{R[c]\text{ may denote the selected proved theorem }p:T}.
\]

The warrant comes from the numerator's checked complete proof, **never** from
the public handle alone. Substituting the already proved term for an assumed
theorem constant is the ordinary theorem-interface justification. Lean's Prop
proof irrelevance and theorem opacity support ordinary use; this is not a
general claim that proof bodies are never operationally unfolded. In particular,
the selected implementation should retain its separate authoritative private
checking pass and its exported-environment compatibility pass. A public conversion
failure remains a refusal, not permission to fabricate transparent semantics.

For this conservative successor, require the actual private installed theorem's
complete inventory to equal the exact warranted inventory as before. Require
the public view to be either that same complete theorem inventory, or a safe
`axiomInfo` with exactly the selected theorem signature. The singleton/full
private checks establish that this really is a theorem of Prop; this exception
must not be applied to arbitrary selected definitions merely because their
public representation is also axiom-shaped.

Consequently no additional theorem axiom enters F. The selected ExportID remains
the ID of the complete separately retained proof unit; the erased native handle
is only a usable local interpretation of its interface. It must never be
serialized as new axiom evidence, relabeled as full original proof bytes or used
to infer a checked UnitID from a signature.

### Minimal implementation relation, without provenance machinery

For each selected singleton unit, after decoding with only the fixed basis and
preceding selected outputs allowed:

1. If its output is absent in both views, retain unchanged private and public
   `CheckedExtension.checkBatch` checks and exact added-inventory validation.
2. If it is present, require the complete private installed inventory to match
   the exact selected warranted inventory; preserve all original values, levels,
   hints, safety and singleton metadata. No name-only or statement-only private
   matching is allowed.
3. A matched theorem may have the exact public theorem inventory or the safe
   theorem-signature projection just specified. Match each signature field with
   existing original codecs; do not use a generic authoring projection as a
   substitute for the theorem-specific private/full precondition.
4. A matched definition or opaque declaration must retain the complete required
   public inventory. Do not introduce a general definition-body-erasure rule.
   Grouped/mutual declarations, absent-public names, mismatches and partial
   presence keep conservative refusal until separately justified.
5. Never insert matched installed records as new stage-two declarations. Write
   only actual additions; retain separate matched/added inventories in the
   pending/final reports and check them on both rereads. Keep the original
   exact selected closure, acquired warrants and identity accounting unchanged.

The private pass is the mathematical gate. The public pass checks that the
ordinary environment really supports each added record under the deliberately
interpreted imported interfaces. Public mathematical types and transparent
definitions must still match their selected meanings. A same-named public
`axiom False` without a checked selected proof of False fails the first premise;
a same-named type whose computational dependencies differ fails R. These are the
counterexamples to mere signature/name trust, not reasons to require political
provenance or an all-library trust policy.

An optional origin annotation must not be mistaken for assurance: in
`Environment.finalizeImport`, `const2ModIdx` retains the first supplying module,
while duplicate theorem records may replace the selected constant via
`subsumesInfo`, whose theorem comparison deliberately ignores proof bodies.
Therefore `getModuleIdxFor?` alone cannot prove exact full-record origin. If a
later feature genuinely needs origin, it must inspect matching module data and
the actual selected record. The narrow interface rule above needs neither a
global origin scan nor new runtime-artifact provenance infrastructure.

### Source pins and resulting decision

Inspected selected runtime source SHA256 values:

- `Lean/Environment.lean`:
  `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86`;
- `Lean/AddDecl.lean`:
  `7e6e74107d8f0116dff7cde2de3e60ed556bbab3ca56309311ea90dfc931bd40`;
- `Lean/Elab/MutualDef.lean`:
  `73a278e79b6fa2a355c3076c40eec8f0cd607c8b68f21e1fa344b56d14e6c3b9`;
- `Init/Core.lean`:
  `6218a9825a0ce51a6bbe3949ec7a86c4406f4f216bd3cd1262736cfc1c997c54`.

These source pins document the reasoning, not a compiler/source-reproducibility
or exhaustive binary-runtime audit. The existing selected runtime premise remains.
The minimum useful successor is exact private singleton reuse plus theorem-only
public interface interpretation, with full computational matching for other
kinds. The already saved mixed standard/new-theorem closure is a suitable finite
changed-boundary discriminator if root later selects it. No new theorem fixture,
general proof-equivalence engine or per-origin machinery is needed to make that
decision. This is compatibility progress, not a mathematical-growth benchmark.
