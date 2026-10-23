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
