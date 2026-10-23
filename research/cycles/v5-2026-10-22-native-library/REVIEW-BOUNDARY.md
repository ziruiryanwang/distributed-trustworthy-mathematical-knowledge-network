# Independent review: ordinary admission metadata and snapshot deltas

2026-10-22. Reviewer: `lean_workflow_trace`. Source only. Read the complete
`ACCEPTANCE-BOUNDARY.md` and `PERSISTENCE-BOUNDARY.md`, and the actual pinned
Lean/BootstrapSupport source passages below. No code, test, build, proof,
installation, runtime import or Git mutation.

## Disposition

**The checked-kernel plus protected-local-snapshot direction is justified, but
do not implement it by treating the old seed codec as an exact ordinary-record
codec.** Three concrete decisions must enter the first source contract:

1. Preserve normal source API metadata for new declarations, especially binder
   names; choose an explicit semantic normalization distinct from native record
   identity.
2. Bind the old normalized fixed basis as that exact basis, with a checked
   source-to-semantic correspondence; do not call it byte-identical to normal
   `Init` declarations.
3. Define a stage2 snapshot boundary so repeated commits do not serialize all
   earlier in-process additions while claiming to serialize only the new delta.

These are finite adapter corrections, not reasons to abandon the proposed lane
or begin another prover/backend investigation. The axioms, builtin-name pinning,
untrusted `.olean` exclusion, actual generated-inventory checking and protected
catalog requirements in the two notes remain appropriate.

## Finding 1: old normalization loses real authoring API information

`software/native/BootstrapSupport.lean` deliberately implements a normalized
seed language:

| Source location | Actual transformation |
|---|---|
| `descriptorJson:576-603` | Saves universe arity, not original ordered universe names. Definition hints and definition/theorem/opaque `all` metadata are omitted. |
| `decodeDescriptor:857-900` | Creates `indexedParams`, definitions with `.regular 0`, and default singleton `all`. |
| `withHeight:368-378` | Replaces every definition's hint by a recomputed `.regular` height, regardless of original `.abbrev`/`.opaque`/`.regular` kind. |
| `encodeExpr:515-556`, `decodeDag:819-826` | Erases lambda/forall/let binder names; reconstruction uses `x`. The let `nondep` flag becomes false; expression metadata is erased. |
| `inventoryRow:610-642` | Normalizes definition/theorem/opaque `all` to singleton. Nonregular definition hints refuse unless a height override is supplied. |
| `sameConstant:346-365` | Does not compare definition hints. It is not an exact complete native-record comparator. |

The previous seed result is not invalidated by this observation: the
normalization was intentional and separately bound. But an exact round-trip
through that normalized language does not establish exact ordinary Lean
record preservation.

The most immediate usability failure is **named arguments**. The pinned
`Lean/Elab/App.lean:81-83` implements `findNamedArg?` by comparing a supplied
argument name to the theorem type's binder name. If a peer theorem is exposed
from a normalized snapshot alone, ordinary expressions such as
`Std.ExtHashMap.getElem?_insert (m := m) (k := k) (a := a)` lose those public
parameter names. Positional applications being possible does not preserve the
normal source API promised by the new lane.

The pinned `Lean/Declaration.lean:17-43` documents that reducibility hints affect
kernel reduction order/performance, not the set of permitted unfoldings. Its
`:121-134` explicitly says definition `all` metadata is not used by the kernel.
Universe-parameter renaming and binder alpha-renaming likewise need not change
mathematical meaning. This is therefore primarily a compatibility/identity and
performance issue, **not evidence that the old seed theorem was unsound**.
Hints nevertheless cannot silently change when exact compatible records and
ordinary performance are being promised.

`Lean/Expr.lean:404-421` says the let `nondep` flag is an elaborator feature not
verified by the kernel. It should be preserved for ordinary record fidelity,
never promoted to an independently proved theorem. `Expr.mdata` is
definitionally equal to its payload (`:438-446`); it may remain explicitly
normalized away without claiming a full byte-for-byte native-expression match.

## Minimum new extension fields and checks

Reuse the old name, level, primitive-literal and expression-DAG logic, but wrap
or extend it with a newly versioned ordinary-declaration format. Do not change
the frozen seed bytes or their earlier evidence.

| New ordinary data | Minimum contract |
|---|---|
| Ordered original `levelParams : List Name` | Unique, bounded, exact names. Decode the level/expression DAG under this list. Merely replacing a finished declaration's `levelParams` without substituting the expression's parameters is wrong. |
| Lambda/forall binder names and binder annotations | Preserve names in the type and body expression representation; retain existing binder annotations. This supplies normal named-argument and display behavior. |
| Let binder name and `nondep` | Preserve as authoring metadata; kernel checking, not the flag, establishes validity. |
| Definition `hints` | Exact tagged union `.opaque`, `.abbrev`, or `.regular UInt32`. For new ordinary records do not call old `withHeight` unconditionally. |
| Def/theorem/opaque `all` | Preserve exact bounded names and bind their advertised scope. These fields are not proof premises by themselves. Any claim that a whole mutual block is present needs an actual census. |
| Safety flags | Ordinary extension allows only safe definitions and nonunsafe opaque/inductive declarations; no caller-selected unchecked insertion. |
| Inductive group descriptor | Exact original levels, ordered type and constructor names/types, number of parameters, complete atomic group. Do not independently trust peer constructors/recursors. |
| Generated inventory | Compare actual generated types, constructors, recursors, rules, counts, flags and group metadata using the specified ordinary projection. Old singleton normalization cannot serve as an exact original inventory. |
| Metadata normalization ID | State what is retained and what is erased (for example `mdata`); use it consistently in source binding, deduplication, snapshot identity and re-export. |

A caveat for a seemingly cheap sidecar: old `internExpr` (`:507`) interns the
already normalized JSON node. Two occurrences with distinct original binder
names can collapse to one normalized node. Therefore one binder name per old
normalized node is not generally enough to recover original names. Prefer a
binder-aware DAG whose node key includes these fields. Alternatively specify a
bounded occurrence-aware overlay; do not assume a lossy normalized DAG can be
made exact by attaching one name afterward.

There is existing encoder machinery to reuse: the selected
`software/v5/authoring/native02/AuthorLean.lean:181-234` `dumpExprAux` already
has fields for binder names, annotations and let `nondep`; declaration dumps
at `:281-311` carry original levels, hints and `all`. However its default
`dumpExpr:257` goes through `removeMData:153-175`, which erases binder names and
normalizes `nondep` as well as deleting metadata. The new adapter should reuse
the full-field patterns with deliberate normalization, not assume its default
stream is already metadata-preserving. Similarly use `Expr.equal`, not ordinary
`BEq Expr`, for exact expression memo keys: `Lean/Expr.lean:804-819` documents
that the former includes binder names/annotations whereas the latter uses alpha
equivalence and ignores annotations.

This is a format/adapter extension, not a new proof checker. A new application
still passes every decoded declaration through `addDeclCore` against the exact
warranted parent. Semantic equality or metadata correspondence is never a
replacement for checking the new proof value.

## Finding 2: fixed normalized basis versus an ordinary project

The exact existing 456-unit basis is a sensible reusable bootstrap candidate.
However it was generated with the normalized fields above. The receiver's
basis records therefore need not be literally equal to the normal project's
original `ConstantInfo` values, even though the mathematical contents have
the intended correspondence.

The first implementation must choose and document a matching rule:

- Bind the frozen basis ID to its actual checked output. Never silently rewrite
  it into another basis with the same ID.
- For producer-side ordinary project matching, compare the selected semantic
  projection of every shared basis declaration: exact constant names, types,
  values/computation structure and ordered universe interpretation, with only
  the explicitly allowed normalization. A package name or version is not this
  check. Pin builtin meanings through the existing exact basis profile.
- Keep any original authoring metadata binding separate from that semantic
  identity. Normal owner-side `Init` can provide notation and original binder
  names while the receiver uses its semantically corresponding checked basis.
- Check the new exported proof in that actual receiver environment. Do not
  infer compatibility merely because it compiled in the producer project.

The selected normal-name lane thus avoids global relocation, but still needs a
small explicit source-to-accepted-environment bridge. Do not advertise the old
normalized seed as exact ordinary-library metadata preservation. Fresh extension
records can preserve the metadata listed above from the start.

For declarations not in the fixed basis, the conservative first merge rule is
exact ordinary projected record equality under exact semantic dependency locks.
If later wider alpha/proof-witness equivalence is desired, that is a new explicit
rule, not an accidental consequence of reusing the old comparator.

### Selected lowest-scope integration route: isolated checker plus checked rebind

**Keep checker snapshots internal. Do not import their basis alongside ordinary
`Init` in the user's project.** This is not only a metadata mismatch risk:
`Environment.finalizeImport:2338-2343` rejects duplicate constants unless
`subsumesInfo` permits them, and `subsumesInfo:2268-2282` handles theorem/axiom
pairs, not arbitrary duplicate definitions. A new metadata-preserving basis
under a different snapshot module name does not make duplicate `Nat`/`String`
definitions legal in the normal module import graph.

The smallest justified route is an explicit owner-authoring bridge:

1. The isolated mathematical checker uses its protected checked basis and local
   snapshots, with no peer binary imports.
2. The normal owner authoring project keeps its existing pinned Lean module
   graph, notation, typeclasses and plugins; it does not load checker snapshots.
3. Before using acquired declarations in that project, compare every required
   pre-existing meaning against the accepted semantic projection and exact
   dependency locks. A failed match means conflict/isolation, not name-based
   substitution.
4. Reconstruct **only new declarations** from the inert metadata-preserving
   ordinary format into the owner project via checked `addDeclCore`. This may
   check the small new delta again but does not replay the old library. Any
   generated owner-side module binds the existing normal import graph, not the
   checker basis snapshot. Its API binder names remain intact.
5. Export the newly authored successor back as inert evidence and independently
   check it in the mathematical receiver. The owner frontend, its loaded
   plugins and ordinary `.olean` artifacts never become mathematical authority.

The bridge is conditional until implemented and checked. It is preferable to
rewriting module topology or every source dependency merely to make private
acceleration snapshots double as public source packages. A later new exact
basis can improve correspondence, but it cannot remove this duplicate-import
constraint by itself. The old seed remains a usable fixed semantic anchor,
not a drop-in replacement `Init.olean`.

## Finding 3: snapshot stage2 is not automatically the last delta

The pinned `Lean/Environment.lean:1857-1884` implementation of `mkModuleData`
serializes `kenv.constants.foldStage2`. It does not compute a difference against
the most recently committed root. `setMainModule` (`:1183`) changes the header;
it does not move existing stage2 constants into the imported stage1 map.

`mkEmptyEnvironment` (`:1530`) starts with a stage2 map. After initialization,
the full basis is therefore stage2 and can be saved as the initial snapshot.
After importing a saved parent, `finalizeImport` (`:2361`) creates an SMap with
imported constants in stage1 and subsequent additions in stage2. That provides
the desired delta boundary **once**. If the same in-memory environment checks
D1, commits it, then checks D2, another `mkModuleData` still sees D1 and D2 in
stage2 unless the wrapper deliberately changes the boundary.

The simplest correct first contract is:

1. Restore/import the exact committed parent snapshot closure.
2. Check one bounded batch of new declarations.
3. Serialize and commit that batch's stage2 data, checking its census.
4. Before beginning another independently committed batch, re-import the new
   parent snapshot (or end the process and restore it next session).

Multiple individual declarations within one batch are fine. A later persistent
process can adopt a justified delta-writer or snapshot-compaction strategy if
startup cost warrants it, but it must not claim O(new-data) snapshots just
because it changes the module name. Whole-prefix snapshotting is sound under
proper binding but has different storage/import costs and duplicate behavior.

The persistence author was notified directly. This affects implementation and
cost claims, not the basic theorem that locally protected snapshots avoid
rechecking already warranted proofs.

## Review conclusion and targeted controls

Proceed with the new ordinary admission/persistence seam after these finite
schema/identity/staging decisions are recorded. There is no source evidence
requiring another cryptographic proof or a new universal checker first.

The first focused implementation controls should include one theorem with
distinct named parameters, two alpha-equivalent expressions with different
binder names, definitions with different hint kinds, actual group metadata,
the fixed-basis projection match, and two consecutive committed deltas. These
are source-review-derived discriminators, not authorization to run tests now.

The representative quotient-backed map family in `WORKFLOW-TRACE.md` remains
the practical compatibility target. A successful tiny metadata check alone
must not be promoted into ordinary-library interoperability or final-v5
completion.
