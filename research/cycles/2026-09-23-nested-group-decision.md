# Nested groups: reuse the existing design, qualify its missing implementation

2026-09-23. Bounded decision by `post_handoff_math_gap`; canonical guard passed.
Read-only source/specification inspection; no product changes, imports, Lean,
network, new harness or known-negative Rose execution. Source10 and its completed
delivery evidence remain frozen. This is not another release gate.

## Decision and deduplication

**Recommend implementing the existing nested-group contract next in a separately
selected successor, with one small positive reuse discriminator.** Do not reopen
source10 delivery or require arbitrary mathlib support. Root retains the choice
to commission implementation; this note launches nothing.

The conceptual solution already exists:

- [EXTRACT1: complete export and group recovery](../../notes/analyses/CP-001H-complete-export-and-group-recovery.md),
  especially “Recovering an actual inductive group,” specifies the actual
  completed-record recovery, generated inventory and source correspondence.
- [Pinned capture APIs](../../experiments/lean-feasibility/source-capture-notes.md),
  “Atomic inductive and quotient reconstruction,” maps that contract to the
  selected Lean 4.34.0 APIs and nested-recursion restoration.
- [Native group representation](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md#safe-inductive-groups-without-identifier-cycles)
  already defines auxiliary selector `[3,k]`; [V4](../../spec/OPERATIONAL-CORPUS-V4.md#foundation-and-representation-version-boundary)
  inherits native semantic constructors under NativeRules code 4.

These are selected paper/source-backed contracts, **not executable nested-group
qualification**. The old restriction note remains accurate but its proposed
negative-only diagnostic is superseded as a next action: static refusal is
already known. No new identity theory or repeated restriction audit is needed.

## Exact compatibility decision

Current `py/codec.py:374–398` constructs NativeRules `0x0003/1` with payload
`[0,4,[0,1,2,3,4,5],allowedAxioms]`, and a schema-2 foundation from that rule,
the pinned Lean commit, unchanged seed and reserved-name policy. The inherited
code-4 semantic grammar already includes nested groups. The finite source codec
explicitly refuses auxiliary selectors as “unsupported in this finite cut.”

Therefore the proposed implementation is **schema-preserving support expansion**,
not a new meaning for an existing selector. Retain:

- Group object `0x0018/2`:
  `[FoundationID,universeArity,numParams,orderedTypeDescriptors]`.
- Group-local type references `[5,i]` inside descriptors, with no group-local
  constructor/recursor references in inductive input.
- External member `[3,GroupID,selector]`; ordinary selectors remain unchanged.
  Existing auxiliary `[3,k]`, `k>0`, names the pinned kernel's first-type
  `DTMKN.i.<GroupID>.t0.rec_k`, not type index `k` and not `.t{k}.rec`.
- Existing normalized complete inventory record fields, including `numNested`
  and recursor-rule bodies; no new trusted metadata field is needed.

No GroupID cycle is introduced: descriptor identity is computed before member
names; generated records are checked consequences, not new axioms or independent
semantic declarations. Old ordinary-group bytes and names must remain identical.

Same FoundationID is justified **only if** these exact inherited interpretations,
normalizations, seed, Lean pin, axiom policy and reconstruction rules remain
unchanged. New adapter/build/source pins are nevertheless mandatory; old
acceptance receipts do not certify newly supported paths or a new installation.
Older finite implementations may refuse the newly usable objects; same foundation
does not mean every client implements the whole grammar. Document the support
boundary; no wire/schema negotiation redesign is needed for the first positive
local experiment.

If implementation instead changes selector assignment, nominal naming, descriptor
normalization, restored-rule semantics or admitted foundation, stop and select a
new NativeRules/Foundation interpretation (and new object schema if its grammar
changes). Never silently relabel old identities. A new version is **not** needed
merely because previously implemented coverage was a strict subset.

## Remaining implementation and proof obligations

Use EXTRACT1's completed-record route already present in the product. The
consequential missing work is at three seams, not just deletion of a guard:

1. **Capture and candidate codec.** Extend actual group-member/selector recovery
   to auxiliary recursors. Preserve ordered `all`, constructors, universe lists,
   counts, safety, types and rules. Classify through record kind, group ownership,
   the pinned generation rule and `numNested`; a matching `.rec_k` spelling alone
   is insufficient. Normalize and bind every member, including references inside
   auxiliary rule RHSs. Keep unexpected-name, `_nested`-escape and external-cycle
   rejection. Existing `BootstrapSupport.groupMembers/scanInfo` already provides
   actual owner grouping and rule-RHS traversal; reuse it.
2. **Canonical planner and receiver.** Extend `native_name`, reference validation,
   inventory membership and `AgentReplayCore.referenceName/receiveGroup` together.
   Construct only one safe `Declaration.inductDecl`; the checked kernel must
   generate all rules. Compare its actual before/after inventory bijectively with
   the normalized source inventory: no missing, duplicate, preexisting, unrelated
   or unexplained generated member. Check every existing recorded field, including
   universe/parameter/index/motive/minor/field counts, `numNested`, recursion and
   reflexivity flags, safety, K behavior, constructor selectors, types and rule
   RHSs. Do not install submitted `RecursorVal` records. Preserve exact equality,
   not merely equal statement types or weak `Expr` equality.
3. **Receiving/re-export boundary.** Auxiliary references must resolve in the
   reconstructed checked environment, source overlay and inverse export as the
   same GroupID/member selectors. Elaborator helpers remain separate checked
   declarations. Preserve the existing “generated external support is explained
   by descriptor dependencies” condition; a mismatch is not permission to import
   extra authority. Same input GroupID under a changed proof realization still
   requires actual compatible checking, as EXTRACT1 already states.

Group limits currently include 16 original types, 32 constructors per type and
1,024 exported members, alongside finite DAG/object/byte/stage budgets. Nested
generation can expand beyond original type count. Bound auxiliary counts and
inventory work before large allocation where possible, retain full output/Job
limits, and fail closed on kernel expansion exceeding them. Do not increase
existing limits simply to pass. The first coverage target is one safe single
nested group through already checked `List`, not general recursive-container
interoperability or an unbounded nested family.

The principal soundness risks are accepting invented generated membership,
omitting auxiliary computation/support, escaping temporary kernel names,
incorrect universe/selector transport and relying on imported authority. Main
operability risks are expanded closure/inventory size and high checked-generation
cost. Native checking protects target mathematics; exact correspondence remains
a separate obligation for claiming faithful import of the original interface.

## Minimal positive adoption discriminator

One fresh, bounded, data-only two-participant scenario; networking need not be
requalified. Keep the installed source10 baseline frozen.

1. A contributes exactly the new safe datatype
   `inductive Rose where | node : List Rose → Rose` through the ordinary source
   path. Require capture, canonical replay and inverse/fresh replay to agree on
   the actual complete nested inventory and stable package/GroupID. B receives
   only the ordinary package and checked interface, not A's source/environment.
2. B freshly admits it, then constructs `nodeCount : Rose → Nat` and
   `forestCount : List Rose → Nat` through the **received** main and auxiliary
   eliminators, using motives Nat, node case `1 + forestCount children`, empty
   case 0 and cons case `nodeCount head + forestCount tail`. Determine the exact
   explicit arguments from B's inspected generated types; this is a workload
   specification, not a claim that guessed source syntax has compiled.
3. B contributes the two small equations together, for example
   `∀ t, forestCount [t] = nodeCount t ∧ nodeCount (Rose.node [t]) = 1 + nodeCount t`.
   Naming both count definitions in the statement forces both into its reached
   closure. Inspect the actual canonical
   value/proof closure: the two count definitions must use the received group,
   including at least one actual auxiliary `[3,k]` reference. This excludes
   replacing Rose by a separately defined tree/forest encoding or satisfying
   the test with a constructor-only/reflexive wrapper. A then freshly checks B's
   successor package, with matching complete inverse/native evidence.

This positive path tests new vocabulary, elimination/computation and reciprocal
reuse. Add only changed-boundary negative controls: forged/wrong auxiliary
selector or ownership; omitted/altered rule/inventory member; temporary-name
escape. Each must refuse without accepted-head promotion. They can share the
already produced finite fixture; no old transport/custody/lifecycle campaign is
needed. Select exact work/CPU/bytes and stop conditions before execution.

Adopt only if the actual auxiliary path, exact correspondence, fresh receiver
checks, unchanged ordinary-group identities and existing resource envelope all
pass. Otherwise preserve the concrete failed boundary and defer this coverage
under the supported v1 scope; do not weaken equality or expand the foundation to
manufacture a pass. A successful Rose discriminator is narrow nested-group
coverage, not all Lean/mathlib support or evidence of useful/exponential growth.

## Handoff

The sealed source10 release remains usable within its declared scope. The next
choice is one bounded implementation of the **already specified** extension,
not more theoretical redesign. Root should first select its exact allowed source
delta and positive gate, or explicitly defer coverage. This memo stops here.
