# Semantic growth decision: compile finite definition composition into the held profile

2026-10-06 resumed. Canonical root only. Source/theory investigation; root selects
the source-only successor `experiments/definition-compiler-01/CONTRACT.md`.
No build, guest migration or runtime is implied by this note.

## Decision

Implement a bounded **untrusted transparent-definition compiler**. It takes an
explicit closed type/body expression referencing F and selected acquired canonical
F-closed definitions. Replace each contributed constant occurrence by that
definition's exact body under simultaneous universe instantiation. Preserve the
expression DAG, do not beta-normalize or replace term arguments. The resulting
type/body refer only to F, acquire a new existing-format content-derived definition
ID, and can be supplied to the existing `--local-definition`/`apply` path.

This safely enables finite iterative semantic construction under the unchanged
image. It is stronger than merely applying another theorem or choosing a seal:
an agent can construct a new function/type from acquired definitions, export its
exact portable implementation, prove an actual law about it, and let another agent
repeat that operation. Each receiving proof still checks the actual compiled body.

It does not implement native named dependency DAGs, opaque data views, new
inductives or unlimited cheap semantic growth. The resulting identity denotes
the compiled expression, not the original symbolic DAG. Certificate cuts still
do not eliminate required data/definition bodies.

## Exact current obstruction

Under `experiments/action-application-01/project`:

- `guest/src/relation.rs:230` computes exact F-closure; lines 416-417 apply it
  independently to every contributed definition's type and value. A safe D2
  whose body names an otherwise valid D1 is currently rejected.
- `companion/cert_capsule.py:319` requires empty nested definition context,
  safe nonopaque body and all reachable type/value constants in fixed support.
  Lines 325-329 bind its ID to F/profile/universes/type/value/hints/safety.
- `companion/proof_compose.py:80` projects every contributed definition and calls
  that inspector. Removing the host restriction alone would not change the guest.
- `companion/cert_workflow.py:320` requires no selected contexts for native
  definition capture; `cert_capsule.py:625` repeats that boundary at the bridge.
- `companion/cert_application.py:189` supports proposition output only. However
  its existing context path imports safe canonical definition capsules, emits
  actual `def` rows before propositions and runs the unchanged complete guest.
- `guest/src/relation.rs:510` genuinely invokes Definition checking for intrinsic,
  selected and output definitions; a compiler success label cannot replace it.

The fixed image has 43 authenticated declaration records (66 reserved names),
not a complete Lean/mathlib universe. New type constructions must remain
expressible with these primitives and lambda/Pi/let/application syntax.

The earlier GROWTH-MECHANISM recommendation to use a new profile is correct for
**preserving named contributed dependency references**. It does not establish
that every useful finite semantic composition requires a new image. Compilation
into the existing F-closed sublanguage is a separate, safe option.

## Formal translation contract

Let selected D_i have closed generic bodies v_i and types T_i, free expression
variables absent, universe parameters u_i explicit, constants only in F. They
need not be trusted before compilation: the output remains an untrusted candidate.
Let e be a closed proposed type or value, referencing only F and the selected D_i.
Define E on ordinary expression constructors homomorphically, except

`E(D_i.{levels}) = v_i[levels/u_i]`.

Universe substitution is simultaneous. The actual levels are first translated
in the caller environment, then substituted once in the closed imported body.
No replacement is recursively resubstituted under the callee's variable names.
This prevents universe-name capture when source and target parameter names
coincide. Exact universe arity is mandatory for every replaced constant.

Term arguments remain ordinary application nodes. Since each v_i is expression-
closed, insertion at any surrounding binder depth needs no de Bruijn shifting.
Internal bvars remain bound by their original lambdas/Pis/lets. Free bvars in
either input root or a selected body are rejected. No user-supplied theorem
axiom/body-free data constant is accepted as a definition source.

Every contributed source body is already syntactically F-closed, so replacement
terminates after one semantic expansion level per operation. Repeating operations
constructs finite chains: the previous output is again an F-closed source. A
within-plan arbitrary dependency-DAG parser is unnecessary for this first slice.
It would increase ambiguity and cycle handling without adding finite expressivity.

Conditional typing preservation is the ordinary transparent-definition unfolding
and universe-substitution theorem: if the selected definitions are well typed and
`F+D |- e : T`, then `F |- E(e) : E(T)`. The implementation does not claim to have
machine-proved this metatheorem. More importantly, acceptance does not need to
trust the compiler: the unchanged guest independently checks `E(v) : E(T)`.
If the compiler is wrong it may produce a different or rejected candidate; its
output ID binds exactly the produced body, not a desired natural-language meaning.
The caller can independently pin an expected output capsule to test translation.

The compiler must return an explicit source/output correspondence record:
source plan hash, selected capsule hashes/IDs, output canonical capsule/hash/ID,
exact substitution count and structural resource counters. This is audit data,
never mathematical evidence. Exact source meaning correspondence is stronger
than final output well-typedness and needs separate source review/tests; final
checking alone cannot prove an arbitrary compiler faithfully met an intended plan.

## Sharing, positive family and real obstruction

Hash-consing shares equal emitted nodes across source graphs. Cache keys include
source graph, expression/level node and exact universe substitution. No beta
normalization occurs, so `app(shared-f,shared-f)` remains a constant-size extra
node rather than duplicating normalized function bodies.

For a monomorphic endofunction a define D0=a and
`D_(k+1) = fun x => D_k (D_k x)`. Once Dk is F-closed, compilation replaces both
occurrences by the same emitted closed body node. With fixed type and universe
instantiation the number of distinct syntax nodes grows by O(1) per level, hence
O(n) for Dn rather than the size of the fully beta-expanded tree. This is a
concrete positive region for compositional representation. It does not mean
evaluating Dn at x avoids its 2^n black-box a calls or that all checker conversion
is linear. Repeated prior artifacts each retained independently can still occupy
O(n^2) total payload across the whole history without shared external storage.

Let W be distinct `(source node, universe substitution)` states reached, S input
bytes and O output bytes. Structural translation is O(S+W+O) expected hash-map
work with bounded schema arities/string processing, plus exact canonical projection
and validation. Number of input DAG nodes alone does not bound W: polymorphic
uses at different levels can require distinct copies; hash-consing merges only
identical emitted structures. Enforce total input/output bytes, imported nodes,
emission states, traversal work, nesting and number of selected definitions.
Guest type checking and demanded conversion have their own resource caps.

`letE` sharing or parametric interfaces can sometimes reduce repetition further,
but introducing binders needs a new capture-avoiding transformation and should
not be mixed into this first no-bvar-substitution compiler. Foundation-dependent
new inductive declarations remain impossible in this selected image; replacing
them with encodings may alter computational behavior and is not a general fix.

## Smallest meaningful integration, not another wrapper theorem

1. Acquire an actual existing theorem fragment whose capsule exposes a reusable
   definition D. Its metadata is a discoverable candidate, not trusted typing.
2. Supply D's exact capsule and an explicit new closed definition expression to
   the compiler. It returns canonical E, e.g. a genuinely new composed operation.
3. Use E as ordinary `--local-definition` context while applying a substantive
   acquired law, proving an actual law about E. Existing acquired law capsules
   keep their old D context; conversion may unfold both independently checked
   F-closed definitions. New E never impersonates D's prior ID or receipt.
4. Final guest checks the full proof and both needed bodies. New output's type
   commits to E; the existing fragment transport carries that exact capsule and
   proof. A new consumer can extract E and compose again without producer state.

No artificial proposition is needed for the **definition admission** logic;
intrinsic definitions are checked data. The currently selected network transport
is proposition-fragment oriented, so standalone definition-only advertising is
not gained by this compiler. Carry E in a substantive law now; a separate object
transport change is required if standalone definition exchange becomes central.

The semantic advance is finite constructability with honest bounded costs, not
unbounded named-DAG locality or measured net global growth. It is worth implementing
because it removes an actual F-closed authoring barrier without changing the
cryptographic relation. Broad foundation migration remains a later explicit task.

## Reassessment: ordinary source authoring versus broad mathematical semantics

2026-10-06 after actual D0->D1->D2 and finite-semigroup-02 qualification.
Root requested central triage; this annex selects no runtime or new guest image.

**Decision:** distinguish two barriers. Ordinary Lean source authoring reduces
the cost of expressing supported mathematics; it does not enlarge the accepted
semantic language. Broad interoperable Lean mathematics is a central unresolved
growth requirement, not a peripheral feature to hide behind a version label.
The current restricted release can be a substantial v4 advance without satisfying
the final general commons goal. Do not promise all mathlib, and do not require
all mathlib at once to make the next substantive advance.

The source evidence is concrete. The held full `cert_workflow.py` already has
owner-source capture/elaboration at lines318-389 and `prepare` at572 onward;
it is not true that all ordinary source support must be invented. The compact
receiver deliberately omits native/Lean assets and refuses native escalation.
Definitions captured through the full path must still have empty imported
contexts and F-closed bodies. The guest's F-closure checks apply independently
of which host frontend produced a packet. Its43authenticated records do not
include List. The working transparent compiler removes one finite composition
barrier, but cannot silently create a primitive inductive declaration.

Formally, if a desired ordinary Lean term names a declaration c outside the
adopted authenticated F, and c is not a permitted checked contributed object,
reformatting its source or generating the same AST leaves that obligation
unsatisfied. A translation into encodings may exist, but must supply its own
type/meaning correspondence and cost analysis. Church-encoding every unsupported
structure is not automatic compatibility with ordinary List or mathlib theorems.
Names and hashes cannot stand in for a missing inductive/recursor rule. Likewise,
an `.olean` file is not an accepted succinct warrant for all its declarations.

| Barrier | Correct next consequence | What it does not establish |
|---|---|---|
| Source authors must currently construct low-level application plans for the compact lane | Document/expose the already existing full owner-source lane and exact capsule names; optionally generate local Lean declarations from acquired inert capsules under its existing checks | Broader F, cheaper conversion, or safe execution of peer-supplied source |
| Fixed support excludes ordinary mathematical structures | Select a bounded representative library dependency slice and inspect its declaration forms before choosing an extension | Universal mathlib admission from a larger name allowlist |
| Repeated inlining can burden semantic bodies and storage | Use the previously designed exact acyclic checked-definition DAG as the next semantic protocol boundary | Removal of demanded definitions or new inductives for free |
| A new semantic relation changes the assurance namespace | Adopt a fresh image/foundation/profile with explicit compatibility or migration witnesses; keep old receipts valid only under their original policy | Reusing old receipts as certificates for a stronger unchecked relation |

The next **broadening acceptance contract** should use an independently chosen
ordinary Lean library module that requires both a genuine structured datatype
and layered reusable definitions, then acquire it, author a new substantive law
in ordinary source and return a result another consumer can use. Select the
module for the obstruction it exercises, not because a new wrapper theorem is
easy to prove. Inspect the demanded declaration closure first: transparent
definitions/theorems, inductive groups and generated recursors have different
checking obligations. No central task list or human-intention field is introduced;
this is a finite release qualification instrument.

At that boundary require: exact dependency identities; safe declaration checking
or an explicitly adopted authenticated base; no arbitrary proposition/data axioms;
generic universe correctness; real recursor/elimination behavior; body availability
where conversion demands it; explicit size/frontier limits; actual malformed-body
and false-law refusals; and unchanged independence from *theorem proof ancestry*
behind certified cuts. Source-authoring success is not receiving acceptance.
Cost includes the demanded semantic closure, so an enormous imported module is
not claimed constant-time merely because its proof history is certified.

**Priority:** finish the selected query-to-use/return path and publish its exact
restricted API/costs. Reuse the existing full source capability rather than
inventing another source generator that does not broaden semantics. Then make
the checked semantic-dependency/library slice the next central engineering
selection, ahead of additional finite-table examples, attribution or economic
automation. It may require a new relation and careful migration; that makes it
substantial work, not a reason to call the current F43 envelope globally general.
This annex does not authorize a costly image/proof campaign before that source
and declaration-contract decision is reviewed.
