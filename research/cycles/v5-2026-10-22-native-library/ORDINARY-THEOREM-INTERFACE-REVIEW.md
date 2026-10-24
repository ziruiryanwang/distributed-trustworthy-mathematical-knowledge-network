# Exact installed theorem reuse: independent conditional review

2026-10-23, `theorem_interface_audit`. Source/theory only. Canonical guard PASS
using the documented process-local execution-policy fallback. Read AGENTS, GOAL,
the current NOW entries, and the complete existing-declarations note. No Lean
execution, Python import, owner opening, experiment, build or Git mutation.

Reviewed decision: `ORDINARY-MODULE-EXISTING-DECLARATIONS.md`, SHA256
`638016b64f9567d80cd741b89dd0f50fa13b626987b26efd30bca77b1e757ccd`.

## Disposition

**Conditional clearance in principle.** The final theorem-only interface rule is
sufficient for mathematical warrant under the hypotheses below. A common module
origin is not a necessary premise. The selected full proof, its exact dependency
bindings and the unchanged foundation supply the warrant. The public signature
supplies a locally usable name for that already proved object.

This is not a proof that the proposed successor is implemented, a machine-checked
refinement theorem, or an interoperability result. Retain the separate private
mathematical and actual exported-environment compatibility gates. Two details
must be explicit in the implementation contract: singleton means `all = [name]`
as well as one output, and matching concerns the actual selected records after
import resolution, not a record merely found in some supplying module.

The useful workflow is a mixed closure containing an ordinary installed theorem
and genuinely new commons declarations. Re-exporting already available standard
theorems alone adds no mathematical capability. Existing closure collection,
canonical codecs, checked insertion and phased rereads provide the required
mechanisms; no provenance service or general proof-equivalence engine is needed.

## Why the rule works, and which direction it establishes

Let F be the unchanged selected foundation. Let U1,...,Un be the finite selected
dependency order, with genuine existing warrants for their complete canonical
evidence and every exact import SymbolID. For a selected singleton theorem c,
these premises give `Gamma |- p : T` and `Gamma |- T : Prop`, uniformly in its
declared universe parameters. A private installed `thmInfo` must have exactly
that selected inventory, including p and singleton metadata. Its dependencies
must already have the selected meanings, not just the selected spellings.

For a public safe `axiomInfo c : T`, interpret every occurrence `c.{levels}` by
the warranted theorem instantiated at the same ordered levels. Apply the same
interpretation throughout dependent types and terms. This is the usual
substitution of a proved term for a constant assumption. No new hypothesis is
added to F. The argument is inductive rather than circular because imports are
already interpreted and the complete selected closure is finite and ordered.

The public axiom supplies no body-reduction rule that the interpretation needs
to preserve. Existing computational declarations and recursor rules must retain
their selected interpretation; the same applies to the foundation's primitive,
literal and quotient rules. Subject to these premises, a public checked term
using only the selected fragment has an interpretation under F. Unrelated names
in installed Init are outside this conclusion and never become decoder inputs
just because they exist in the loaded environment.

Proof irrelevance supports equality of proofs of the same proposition in
dependent positions. It does not prove that their evidence bytes or IDs agree,
and it does not establish identical reduction behavior or checking cost after
proof-body erasure. The basic proved-term substitution is the justification;
proof irrelevance is not a substitute for the independently checked p or for
matching the meaning of T. A raw `thmInfo` tag from a native file is not a warrant
that its type is Prop or that its body checks.

The direction relevant to soundness is public use interpreted by already proved
objects. The converse, that every private proof will still check using exported
handles, is false as a general compatibility claim. The preserved private pass
establishes the selected mathematical meanings; the separate public pass must
establish compatibility for the actual additions. Neither gate replaces the other.

## Source facts that constrain the argument

All Lean paths here are below the pinned runtime
`software/runtime/lean-4.34.0-windows/src/lean/`.

- `Lean/AddDecl.lean:123` exports an ordinary module theorem as a safe
  `axiomInfo` carrying the same `ConstantVal`, while retaining private
  `thmInfo`. `forceExpose` is the explicit exception. Its asynchronous and
  error-recovery branches are not acceptance evidence; the project checker
  deliberately uses `addDeclCore ... (doCheck := true)` instead.
- `Lean/Environment.lean:1858` writes different private/public constant views.
  `writeModule:1901` writes the three module parts. Full private equality therefore
  cannot establish public availability merely by implication.
- `Lean/Environment.lean:2250-2283` permits duplicate compatible theorem records
  with different proofs. Its own comment explicitly notes that theorems can be
  unfolded for `Acc.rec`. A private term requiring reduction through such a proof
  can lose that conversion when the public record is an axiom handle. Refuse a
  failed public check; do not infer compatibility from proof irrelevance.
- `finalizeImport:2334-2360` may replace a selected duplicate theorem record while
  `const2ModIdx.insertIfNew` retains the first supplier. `getModuleIdxFor?` alone
  does not identify the full record that won. Compare the final actual private
  and public records, including key/name agreement, and bind the used artifacts
  through the existing protected lifecycle. No origin scan is required.
- `OriginalDecl.lean:123` retains full original theorem bodies, ordered universe
  names, computational bodies, hints and group metadata. Its `allOf:77` requires
  membership of self, not `all = [self]`; `decodeUnit:357` requires one inventory
  output for an ordinary declaration, which alone does not establish a singleton
  mutual-block claim. The matching branch must explicitly require both.
- `CheckedExtension.lean:99` rejects overwrites and performs checked insertion.
  Keep it unchanged for additions. `module_closure.py` already binds actual
  evidence bytes, all import identities, proof-only dependencies and topological
  order; an installed match must not become a new evidence-traversal boundary.

## Minimal implementable obligations

1. **Preserve exact authority and closure.** The existing protected controller
   must still validate the unchanged semantic/foundation IDs, actual canonical
   evidence, UnitIDs/ExportIDs, all import SymbolIDs and genuine local warrants.
   Decode only against F and preceding selected outputs. Bound and retain full
   evidence even for matched installed theorems. A callback or custody record
   that merely asserts acceptance does not meet this premise.
2. **Classify actual records conservatively.** For each reusable existing unit,
   require one output, descriptor/output name agreement and `all = [name]`.
   Run the existing safety/name screening; actual map key and record name must
   agree. Require exact private inventory equality using the original codecs
   with only their existing mdata erasure. Do not infer equality from signatures,
   definitional equality, origin metadata or Lean's duplicate-import acceptance.
   Existing grouped/partial collisions remain refused; completely absent groups
   may still follow the already supported unchanged full checked-insertion path.
3. **Allow only the specified public theorem representation.** A matched
   private selected theorem may resolve publicly either to the same complete
   theorem inventory or to safe `axiomInfo` with exactly the original name,
   ordered universe parameters and encoded type. Match this in the actual public
   view, without realizing an extra declaration on demand. No definition/opaque,
   unsafe record, missing public name or differently shaped theorem qualifies.
   Existing definition/opaque reuse retains full required public computation and
   metadata. The special existing fixed-basis relation stays confined to F.
4. **Preserve both checks and the environment invariant.** Walk dependencies
   in order in both relevant views. Extend the interpretation only after the
   required match succeeds; use unchanged checked insertion for absent units.
   Validate exact inventories of additions privately and publicly. A successful
   public check cannot authenticate a private proof or admit ambient Init names.
   Conversely a private success cannot waive failed public typechecking,
   conversion or missing computation. The initial F correspondence must retain
   its existing meaning/primitive obligations; a row count is not that relation.
5. **Write and report what actually happened.** Keep distinct matched and added
   sets. Write only added declarations and require the module's own census to
   equal that set. Both actual rereads must verify the complete selected
   matched/added relation and target resolution. Preserve existing runtime,
   approved-import, byte-binding and final-report-last controls. Report matched
   units as matched, not newly kernel-checked; an all-matched result needs no
   manufactured empty module. Exact evidence IDs stay bound to the retained
   proof units, not to the serialized public signatures.

These are local obligations on a bounded selected closure. They do not require
checking all installed Init, accepting extra axioms, changing the foundation,
changing the core checker, or trusting remote native modules. The existing
selected-runtime and correct-codec/kernel assumptions remain explicit.

## Decisive refusal cases

| Case | Why it must refuse |
|---|---|
| Public safe `axiom False`, no selected checked proof of False | A safe flag and valid signature do not discharge the proof premise. |
| Identical type text `P`, but selected `P := True` and installed `P := False` | Meaning differs despite spelling. Exact preceding dependency matching fails. |
| Same theorem name/type but a different private proof or ExportID | It may prove the same proposition, but it is not the selected full evidence identity. Proof irrelevance does not equate IDs. |
| Same number of universes, changed order/names/type encoding | This narrow exact interface rule has no renaming or definitional-equivalence clause. |
| Selected `def n : Nat := 0` represented by an axiom or by `n := 1` | The theorem exception does not apply to computational data; required body semantics are absent or changed. |
| One inventory row but `all` names another mutual member; partial group presence | One serialized row is not sufficient evidence of the promised singleton/group scope. |
| Private proof checks, public proof requires erased theorem-body reduction or hidden transparent computation | Mathematical warrant survives; ordinary compatibility is unestablished. Public failure remains a failure. |
| Matching row exists in one module but a different final private/public record is selected | The consumer uses the selected map entry. A supplier index does not repair a mismatch. |
| Match found but evidence is unavailable, cyclic, has a changed import ID, or relies on an unmatched ambient name | The selected full-warrant interpretation cannot be completed. |

Refusal for a different valid proof, alpha-equivalent signature or merely
definitionally equal body is conservative identity policy, not a declaration
that the underlying mathematics is false. Resource/unavailability refusals must
also retain their existing non-invalidity classification.

## Honest export claim and next decision

The resulting claim may be: under the pinned local runtime and unchanged F, the
selected exact warranted proof closure has a checked ordinary-module realization;
specified installed names realize matched selected declarations, and newly added
records were privately checked and found compatible with actual public imports.
The full selected proofs remain retained and independently identifiable.

The bridge module need not physically repeat proof bodies belonging to matched
installed declarations. Its public handles are not new axiom evidence, original
proof bytes, or independently authenticated native modules. A peer cannot accept
a downloaded `.olean` merely from this claim; ordinary import still uses the
local compiled-library trust boundary. Later commons admission must continue to
check the contribution's actual selected closure, including any ordinary-project
dependencies outside this export. No unrestricted consumer/project-wide theorem,
source-attribute restoration, executable-code equivalence, proof-independent cold
cost or useful-growth advantage follows from this interface result.

The saved mixed `Nat.add_zero` / new-theorem closure is adequate motivation for a
small successor if root selects it. Its new evidence need concern the changed
matching/public-interface boundary; this review does not request a general
equivalence mechanism, origin infrastructure or another completed campaign.

## Rechecked source pins

| File | SHA256 |
|---|---|
| Runtime `Lean/AddDecl.lean` | `7e6e74107d8f0116dff7cde2de3e60ed556bbab3ca56309311ea90dfc931bd40` |
| Runtime `Lean/Environment.lean` | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |
| `software/v5/ordinary_lean/OriginalDecl.lean` | `bfb5fc910808d9dc178977cfa6edeacf0b5cbfe7bd99bc6277ee11a456d516c1` |
| `software/v5/ordinary_lean/OriginalExpr.lean` | `8278826700b17f8a926bebcf36e0408540ddfa3e84637ce4c8ff8f37c9dce72b` |
| `software/v5/ordinary_lean/CheckedExtension.lean` | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |
| `software/v5/ordinary_module_bridge/OrdinaryModule03.lean` | `9002e54d73fc884ebce50b8c782757801a0d0abd6cc6c0fee6ed83a455f8536f` |
| `software/v5/ordinary_module_bridge/module_closure.py` | `9bc94955611c1afecb83dc978a728ce9c7bfc7e9ba75ae28d8dd8b8d2fd10281` |

Pins establish which source was inspected, not binary/source reproducibility or
a fresh runtime outcome. Existing used source and evidence were not changed.
