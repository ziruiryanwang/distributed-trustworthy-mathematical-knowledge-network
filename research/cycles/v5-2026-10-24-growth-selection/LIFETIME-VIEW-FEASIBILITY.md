# Local lifetime views: exact restriction first, not assumed proof erasure

2026-10-24. `growth_user_economics`; bounded source/theory investigation.
Canonical guard passed. No implementation, runtime, store opening, experiment,
download or Git operation. The separate session author owns finite-session
design. This note compares local views with existing batching/project contexts.

## Decision

**Do not implement a theorem-interface-only receiver projection now.** Existing
signature-only authoring deliberately depends on final checking against the
real accepted context; it is not an already justified replacement for that
context. Logical cut, preservation of the native checker's success, and ordinary
frontend compatibility are distinct obligations.

An **exact dependency-closed local subenvironment** is feasible in principle
under explicit strengthening and local-warrant premises. It can omit unrelated
branch history. Without a qualified missing-body mechanism or a new conditional
acceptance relation, it must conservatively retain full records, including
theorem values and their dependencies. It therefore does not generally remove
old proof-only ancestry. Current catalog/import interfaces also cannot load such
a subenvironment merely by passing a shorter list.

For repeated work in a moderate context, compare batching and the separately
investigated finite session first. For unrelated-history overload, first use a
smaller already warranted parent and ordinary re-admission of selected retained
evidence in batches. This costs selected checking again but needs no new warrant
kind. Select a new protected projection only if it beats that honest baseline
and the relevant closed subset is demonstrably much smaller than the parent.

## What the present implementation actually supplies

| Source | Existing boundary | Consequence |
|---|---|---|
| `ordinary_lean/LocalSnapshot.lean`, `writeCheckedBatch` | Saves complete actual `checked.added` records and exactly one parent import | Delta snapshots avoid cumulative copying, not full-parent imports |
| Same file, `importArtifacts` / `restoreLocal` | Validates the complete one-parent module chain; imports root with private level, plugins/extensions disabled | Removing a chain entry is not supported selective loading |
| `OrdinaryWorkflowWorker.lean`, `extend` | Restores that parent, then enumerates all kernel names for decoding | A smaller incoming proof alone does not remove whole-context name work |
| `portable_catalog.py`, `_context_rows` / `context` | Reconstructs root-chain bindings and authenticated module plan | No current demand-sized root-membership lookup is supplied by this API |
| Same file, `reserve_extension` / `_commit_checked` | Binds an exact parent plan to a clean checking event and commits a one-parent native-check chunk | A projected parent is a controller/persistence change, not a serializer option |
| `portable_owner_request.py` | Selected evidence traversal omits recursive proof-only acquisition for singleton theorem signatures | Still reads the theorem's full raw evidence and validates all import IDs |
| `OwnerConstruction.lean`, `demand` | Checks an axiom-shaped scratch signature for a missing warranted theorem | Establishes signature well-formedness only; not theorem acceptance |
| `OwnerRebind.lean` | Matches selected owner interfaces/semantics; leaves final acceptance to the receiver | Correspondence is not a proof that the whole owner environment is sound |

`OWNER-BASIS-PROJECTION` already computes selected semantic closure for authoring
correspondence. It retains types, definition/opaque bodies, complete generated
metadata and implicit literal support, while omitting theorem proof scans.
Its receiver still has the original complete foundation/context. Reusing its
closure algorithm for receiver acceptance would change that premise.

## The proof-erasure trap

CP-001H and its independent audit inspect Lean native source at historical pin
`293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`. At **that pin**, native
`constant_info::has_value(false)` includes theorem values, unlike genuine opaque
declarations. Native conversion can unfold those theorem values. The frontend's
theorem-opacity policy is different.

Its paper countercase uses a theorem proving `Acc R x` as the major premise of
a Nat-valued accessibility recursor. A constructor-backed theorem exposes a
reduction to zero; an equally valid opaque-backed proof leaves that computation
stuck. A previously usable `Eq.refl 0` body then lacks its original conversion
route. The audit is source/paper evidence, not an executed failure.

**This note does not establish current bundled Lean 4.34 C++ behavior from that
old pin.** No current native source correspondence or preservation theorem was
established here. The retained example is sufficient to reject a generic claim
that "theorem" means its value can always be erased without changing acceptance.
Current pinned preservation would need its own source argument before selection;
no new dependency download or experiment is justified merely to repeat history.

Proof irrelevance permits reasoning about equality of proofs of a proposition.
It does not promise that the concrete conversion algorithm synthesizes whatever
intermediate proof makes a Nat-valued computation reduce. It also does not turn
a same-type transparent definition into the same mathematical operation.

## Three different projection possibilities

### A. Exact closed restriction: principled, but not proof-ancestry-free

Fix one eligible locally warranted context K, its exact semantic/foundation and
implementation/support state, and selected new units U. Start with all external
references of U's full types and values, not merely its output types. Retain the
fixed supported foundation and close selected records under:

- Their types, exact universe parameters, referenced constants and projections.
- Full definition, opaque and theorem values when retaining those exact records.
- Complete mutual inductive groups, constructors, recursors and reduction rules.
- Implicit primitive/literal support required by the qualified kernel profile.

Preserve declaration kind, names, reducibility metadata, generated inventory,
dependency ordering and exact binding identities. No names are merged or rebound.
Cycles inside generated metadata require group-level treatment, not arbitrary
individual declaration sorting. The profile's primitive initialization is not
established just by setting a Boolean or copying an arbitrary axiom signature.

Under a justified strengthening property, the resulting S has the same meaning
for every retained declaration as K. New checks over S use the same selected
semantics. This is a local reuse argument: the source records already have a
valid warrant and remain eligible. It is not a cold peer-import rule.

The conservative closure can reach a large fraction of K through theorem values.
Thus it can remove *unrelated* declarations but cannot promise removal of all
proof-only ancestors. Reusing already warranted exact records avoids checking
their proofs again; finding, authenticating and loading their bytes still costs.
No constant-time or same-resource acceptance theorem follows from strengthening.

### B. Interface cut: logically meaningful, not the current receiver API

If K warrants `c : P`, a derivation made with a local hypothesis `h : P` can be
interpreted in K by substituting c for h, provided every remaining declaration,
universe, dependency and primitive has the stated compatible interpretation.
This is ordinary cut/substitution. It neither assumes P without a warrant nor
identifies arbitrary same-named constants.

A scratch checking environment can represent h by an assumption, as the existing
authoring helper does. But using the resulting check as *final* acceptance would
need a protected interpretation/cut boundary and persistence semantics that the
current clean-worker/full-parent contract does not provide. Ordinary rechecking
in K remains the current discharge step and retains its context cost.

Such an abstraction may refuse old computations that depended on unfolding c.
It must not claim equality of native success sets or frontend behavior. Checked
equation/transport lemmas can sometimes repair a particular application; CP-001G
BRIDGE1 and CP-001H already explain the real premises and costs. They do not
provide a free, universal bridge or authorize changing the accepted definition.

### C. Exact records with missing dependencies: not a safe shortcut

Keeping a full theorem `ConstantInfo` but dropping its proof-only dependencies
does not produce the exact closed restriction in A. A future reduction may
follow its body into absent records. Native lookup failure is not an implemented
typed `NeedBody` protocol and cannot be interpreted as safe opacity.

The older specialized module checker distinguishes missing values, sealed Prop
interfaces and real opaques. That separate relation does not make the current
ordinary Lean worker a demand-fetching checker. Adding such behavior would
require auditing every relevant lookup/reduction and preserving kind/identity,
not copying its missing-body label into `LocalSnapshot`.

## Costs and the smallest actual missing boundary

Let C be the exact closed subset selected by A. A first projection made by
restoring K still pays K's import/metadata/integrity cost once. Subsequent uses
can pay for C instead, only if a separately retained protected projection is
available. This can amortize for many similar uses with C much smaller than K;
it cannot help create a view when the initial construction itself cannot fit.

A demand-sized construction without first loading K requires **root-bound
indexed access to eligible exact declarations, group membership and dependency
metadata**. Current root records contain binding arrays; `context()` assembles
them by walking the chain. Existing selected evidence helpers still parse full
units and obtain their warranted bindings through a supplied controller lookup.
Calling that callback a point lookup does not make the underlying implementation
sublinear. Rebuilding the index or closure from all K on every use loses the gain.

The minimum new implementation would therefore span, not merely edit one loader:

1. A protected root/support-scoped lookup/closure source, with costs paid during
   admission or one explicit migration; no authority from an untrusted side index.
2. An exact-record/group projection writer authenticated against eligible K,
   importing only its complete selected base and producing no new mathematical
   declarations. Retention, size and failure accounting apply to these artifacts.
3. A distinct catalog origin and restore plan binding that projection to K and
   current support eligibility, with protected byte integrity and withdrawal.
4. A successor-check/commit rule separating the logical warranted context from
   the physical imported subset; it must preserve exact input and output IDs,
   overwrite checks, groups, crash atomicity and final peer evidence semantics.

Current `LocalSnapshot` permits only actual checked extensions with a single
parent import. `_commit_checked` cannot label a subset-copy event `native-check`
and silently give it the old parent's complete binding map. This is a genuine
new local acceleration boundary, even if it introduces no new mathematical axiom.

Residual costs include initial acceptance, complete selected closure bytes,
projection maintenance/retention, exact support checks, new proof conversion,
final evidence publication and failures. Large atomic groups or semantically
central definitions can keep C large. Explicitly refused projection is not
evidence that the original result is false or that the full route must fail.

## Comparison and next action

- **Existing batches:** share restoration across already available new units;
  smallest change, but do not remove irrelevant K or its memory footprint.
- **Existing bounded branches:** choose a smaller eligible parent and normally
  acquire/check selected retained evidence into it. Repeated selected checking
  is a cost, not weakened trust; current parent/batch machinery already supports
  the basic route. It does not guarantee a small proof closure.
- **Finite session:** can avoid repeated K restoration while K fits; its event,
  cancellation and persistence feasibility belongs to the separate assignment.
- **Exact protected projection:** useful chiefly for stable, small relevant C
  inside much larger K; requires the new lookup/origin/strengthening boundary.
- **Interface-only final checking:** potentially smaller C, but changes the
  acceptance relation and operational compatibility; not selected here.

No scaling run is needed to distinguish these explicit source loops and semantic
obligations. First compare the session result with batches and bounded branches.
Reopen exact projection for a concrete case where unrelated K prevents affordable
use, retained exact closure C fits, and one-time projection beats ordinary
selected re-admission. A small theorem-only interface demonstration would not
answer that question. Do not launch a proof-erasure campaign.

Read with GROWTH-LIFETIME-DECISION, ORDINARY-PRACTICAL-COST, OWNER-BASIS-PROJECTION,
OWNER-REBIND-PLAN/IMPLEMENTATION, PORTABLE-AUTHORING, and the cited CP-001G/H
analysis/audits. Their authoring, historical native and current persistence
claims retain their different scopes. No full-v5 or broad-growth gate is closed.

## Grounded interface-cut discriminator

2026-10-24, current_scale_obstruction. Source/theory follow-up; no runtime,
protected-state opening, implementation or Git mutation. This reopens B on a
different success criterion: accept only the new work that checks with old
theorem bodies unavailable. Preservation of all old native successes is NOT
required. The proof-opacity countercase above therefore does not defeat this lane.

**Decision: a genuinely promising local acceptance alternative, not a loader
optimization.** It can remove old theorem proof-only ancestry even when exact
restriction and smaller-parent re-admission cannot. No cryptographic production
is required. Existing code supplies much of the small checker; protected summary,
membership and persistence boundaries are missing. Do not declare them impossible
merely because their warrant is not the existing full-parent native event.

### A restricted, useful interpretation

Let K be one already eligible local context under the selected fixed foundation.
Construct H from that exact foundation, never an arbitrary authoring environment.
For each selected old theorem c, its locally warranted entry must bind original
name, exact ExportID, declaration kind, universe parameters and complete type P.
Check the signature is well formed and propositional; insert only an internal
safe axiom c:P. Recursively provide type dependencies. Every such assumption must
map to an earlier exact theorem in K; no peer signature, same-type alternative,
uncommitted result or circular collection of assumptions can discharge it.

Keep demanded non-theorem meanings concrete: exact safe definition/opaque bodies,
types, universes and reducibility; complete inductive/constructor/recursor groups
and reduction metadata. Reconstruct their declarations with actual kernel checks
in H and compare the generated full inventories with K's accepted inventories.
Follow their semantic dependencies, stopping only at warranted theorem signatures.
Refuse partial groups, incompatible generated metadata or construction requiring
a hidden theorem body. Primitive/literal/quotient behavior comes from the exact
fixed basis, not from arbitrary signatures or `quotInit` alone.

For the first acceptance slice, permit new singleton safe definitions and theorems;
defer NEW inductive groups/opaques rather than silently treating them as signatures.
Check complete new types AND values with `addDeclCore ... doCheck := true`, preserve
the original exact descriptors/inventories, and require each new name absent from
the whole selected K, not just absent from H. This already supports new predicates,
operations and derived laws over existing structures; it is not the final language
scope or a restriction on what investigators may invent in their ordinary projects.

The implementation-specific obligation is an interpretation J:H->K: basis and
concrete records preserve their full rules, while each temporary axiom denotes
its exact warranted theorem. For expressions, prove typing and every conversion
rule used in H are preserved by J; then extend J in order by each new checked
definition's exact body or theorem's proof. This gives a warranted extension of K.
It need not prove the converse, equal reduction cost, or identical native-checker
success sets. A failed H check is an explicit lane refusal, not falsity in K.
The fixed primitive rules, universe substitution, proof irrelevance, projections
and recursor rules must be covered by this refinement; generic cut prose alone is
not its completed assurance. No source-level argument here is a Lean-checked proof.

### Actual source fit, and the essential differences

`OwnerConstruction.demand` already kernel-checks axiom-shaped theorem signatures
and reconstructs non-theorem groups through `CheckedExtension.checkBatch`.
`OwnerRebind.scanSemantics` retains concrete bodies/group metadata but omits theorem
proofs; `OriginalDecl.inventoryRow` checks exact generated records. These are useful
mechanics, not an existing final acceptance API. In particular `constructPrepared`
retains its supplied owner and accepts existing records after `requireSafe`; it
does not establish that every surviving assumption has a warrant. Reusing that
arbitrary owner as H would invalidate the argument. Start from the fixed basis,
census all temporary assumptions, and close all new type/value references.

`portable_owner_request.prepare` still fetches full old evidence and checks every
import ID; `PortableCatalog.context` still walks all roots and hashes/import-plans
their artifacts. Neither gives the intended bound. At successful native admission,
derive protected compact theorem interfaces and exact non-theorem group records
from the checked bound input/output, and transactionally record their correspondence
to accepted IDs. An old UnitID hash alone cannot authenticate a separately supplied
short type. Past records need one explicit paid construction/migration; a cold peer
cannot manufacture these summaries. Retain original evidence separately for others.

A persistent root-scoped name map must support exact membership AND freshness
without rebuilding K. Structural sharing can charge updates per added binding;
copying K's entire map into every root simply moves the quadratic cost. Bind summary
bytes, group completeness, map root and support/withdrawal eligibility to protected
commits. Retain a conservative support set/epoch rather than recursively reopening
every old proof for each use. This changes local warrant retention: its validity
must not silently depend on rehashing all omitted snapshot bodies on each call.

Keep the current supervised clean-process-exit event and original resource grant;
no live daemon/session protocol is needed. A distinct cut-checked catalog origin
must bind the exact old root/map, selected warrant frontier, scratch closure,
checked new units and immutable result. Temporary assumptions are NEVER published
as new mathematical axioms or mislabeled `native-check` snapshots. Current
`LocalSnapshot`/`_commit_checked` cannot perform this promotion unchanged.
Future cut calls must restore from compact warranted metadata, not the complete
one-parent olean chain. Ordinary evidence remains an inert complete new proof claim;
another owner still grounds its imports independently. Ordinary full-parent use is
a separate route. Review conformance to `ordinary_semantics`' insertion contract
before claiming unchanged acceptance-profile/identity semantics; no laundering of
a new warrant under an old implementation ID is justified by this note.

### Payoff and the next decision

Let A be once-paid summary/index construction, S_i selected semantic closure,
U_i new work, and M_i root lookup/update/support cost. The proposed lifetime cost
is A + sum_i [M_i + load/check(S_i) + check(U_i) + commit_i], plus retention,
failed attempts and export costs. It omits mandatory replay/read of old theorem
proof-only ancestry, not proof terms embedded inside concrete definitions, large
selected groups, or semantically necessary types. No universal small S_i follows.
It beats existing batches/small roots only when avoided restore/re-admission cost
exceeds A, repeated semantic reconstruction and added maintenance. Small contexts
and one final aggregate batch can remain cheaper; ungrounded cold import is unsolved.

The smallest next step is one bounded source acceptance/restore contract plus its
independent semantic challenge, NOT a scaling or certificate experiment. Fix the
singleton output slice above, a protected compact-map event, and all J obligations;
trace existing `TheoryB02.same_constraints_same_run` structurally through exact
Repair/OrderData/List meanings and the signatures of `run_settles`, `run_extensive`
and `run_below_settled`. That source uses the laws as proofs, so it is a concrete
candidate, not a claim its exported closure already passes H. If the trace cannot
retain exact generated semantics without loading proof bodies, explicitly narrow
or stop. If it succeeds in principle, select a small SOURCE implementation of this
changed boundary for review; do not repeat the already completed theory episode.

### Independent challenge of the grounded cut lane

2026-10-24, current_security_obstruction. Read the appendix and actual
`OwnerConstruction`, `OwnerRebind`, `CheckedExtension`, `LocalSnapshot`,
`ordinary_admission`, `portable_catalog` and `ordinary_semantics` sources.
Source-only: no native operation, state opening or implementation change.

**GO for the bounded acceptance/restore contract; not yet GO for final acceptance
implementation or unchanged-profile adoption.** This is a meaningful alternative
to expensive certification and full-parent restoration, not defeated by historical
proof-opacity incompleteness. A new catalog rule is a cost to justify, not a veto.

The conditional mathematical argument is precise: if H is well formed, every
nonfoundation assumption h:P has an eligible earlier witness J(h):J(P) in K,
and J preserves the used typing/conversion rules, then H |- e:Q implies
K |- J(e):J(Q). For a Prop conclusion this is an actual warranted proposition,
not merely successful execution or a well-formed assumption. Extend the argument
declaration by declaration, forbidding overwrites in the whole logical K.
This proves a positive direction only. It neither makes all old computations
work without theorem bodies nor bounds the size of demanded concrete semantics.

Concrete pollution counterexample: supply the existing construction helper an
owner containing safe `axiom bad : False`; it survives selected target demands.
`CheckedExtension.checkBatch` can then check `theorem q : False := bad`, because
it verifies reference existence in its parent, whose warrant is a precondition.
`OwnerRebind` matches selected records, not an exhaustive clean-parent census.
Thus neither helper is a final receiver as written. The proposed fresh exact
basis, exhaustive assumption census and complete type/value reference closure
close this example. `isUnsafe = false`, `quotInit = true`, a symbol hash or a
mode-0 row alone do not. Bind theorem kind and Prop-typed signature to the actual
earlier warrant; no caller may choose an additional undischarged assumption.

Definitions need more than same-type witnesses: their full bodies, reductions,
universe substitutions, generated group rules and implicit primitive behavior
must be preserved by J wherever concrete in H. The appendix correctly requires
this. Theorem-only outputs are a smaller initial assurance slice if singleton
definitions prevent closing that argument; definitions must not be advertised
as supported merely because a theorem-only probe passes. New inductive groups
remain outside the proposed first slice, not forbidden mathematics in the system.

Recursive reuse requires a well-founded event order: each cut event may depend
only on already committed eligible warrants, never itself or a mutually pending
event. Bind the exact logical-root membership and negative name-freshness checks
to the same protected transaction as the new event and map update. Otherwise a
true theorem from another incompatible branch, or an existing name omitted from
H, can be laundered into the selected root. A persisted peer-like PASS cannot
supply this event; interrupted workers must not create eligible map entries.

A protected persistent name map plus conservative store-wide support eligibility
can make lookup proportional to selected entries instead of ancestors. This is
not supplied by current `context()`: it walks roots and hashes their artifacts.
The new contract must explicitly make summary/event records durable authority,
charge their construction/retention, and state integrity and recovery premises.
Under one unchanged implementation, withdrawal of the supporting store/epoch can
invalidate all dependent cut results conservatively. A support upgrade, imported
foreign origin or more selective revocation needs explicit dependency coverage;
renaming an epoch cannot wash away previously invalidated checking support.

Public return is a separate boundary. Preserve complete new proof units and exact
import bindings as ordinary inert claims; never export scratch assumptions as new
axioms or scratch oleans as accepted snapshots. A recipient without grounded
premises still pays its own acquisition/checking cost. Existing full-parent
catalogs cannot restore a new cut-origin record unchanged. In particular the
semantic descriptor says `kernel-checked-extension-of-warranted-parent`: decide
and justify conformance of this interpretation rule, or version the contract;
do not silently retain an old implementation identity or promise native success.

The highest-payoff discriminator is the proposed existing-theory structural trace
plus one explicit recursive restore/commit contract. Count summary migration,
index updates, demanded definition checks and public return costs. The payoff
region is real in principle when avoided ancestry dominates these costs; it is
not evidence of faster discovery, cheap cold import or universal cheap checking.

## Existing theory cut trace

2026-10-24, current_scale_obstruction. Source/data only; canonical guard passed.
Read retained public export JSON, not a catalog, custody database or native module.
No compiler, project-code import, new mathematics, harness, benchmark or Git action.

**Positive discriminator:** the actual `same_constraints_same_run` proof composes
six existing theorem interfaces without requiring their proof values. Twenty
concrete nonbasis units suffice for its selected semantic closure. This supports
a scalar-theorem first lane for further laws over this theory; it does not claim
an implemented cut receiver, a valid fresh target admission or universal coverage.

### Exact public evidence, not just the source's apparent dependencies

Input is `experiments/v5-local-checks/concept-theory-b-export-01/bundle/`.
Its previously audited manifest SHA-256 is
`680cd98f8d1d31ef251b1e78b1cdae7a60bbe2b733e95193b0fe52cb9855c302`.
The selected `units/0be846200d7809eaa68cf06cf23ef362052d4d3f4a5db4892c7f369691393e83.json`
is 13,776 bytes; raw SHA-256
`f47ae493eb89d7c052f62b039d9f929195b9e02f72aa38acaa597e4195774556`.
Its export ID is `fb3598ea1e9b841c081a756f1aaeb144a1f4d7154ba5b9503644d5971017b20c`.
It is one theorem descriptor/inventory, with original universe parameter `u`,
61 type-DAG nodes, 115 body-DAG nodes and 15 direct import bindings. The data trace
decoded encoded names, const/projection references, and the seven relevant type
DAGs; it did not invoke the project's parser/checker. All 27 selected unit files'
lengths/raw hashes were matched to the manifest; this is binding, not acceptance.

Trace rule: begin with all target imports; stop at the fixed basis; for an old
theorem follow its TYPE references only; for a non-theorem follow its whole exact
unit import census and retain the complete group. Match names to the saved bundle's
actual inventories. This is a bounded data dependency traversal, not an optimal
conversion-demand analysis or a root-membership lookup.

| Selected old input | Actual contents |
|---|---|
| Six theorem signatures | `Iff.mp`, `Iff.mpr`, `OrderData.antisymm`, `run_extensive`, `run_below_settled`, A's `run_settles` |
| Five concrete groups | `Repair`, `OrderData`, `IsClosure`, `Membership`, `List.Mem`, each with its complete saved constructors/recursor |
| Fifteen concrete definitions | `Repair.apply`, `OrderData.le`, `AllClosure`, `Fixed`, `Follows`; `run`, `run._f`, `run.match_1`; `Safe`, `Safe._f`, `Safe.match_1`; `Settled`, `Settled._f`; `List.instMembership`, `Membership.mem` |

Names without a full namespace use `RepairTheory` and its `ClosureBridge` namespace.
These twenty concrete units have ZERO direct imports of nonbasis theorem units.
Their whole nonbasis dependency subgraph therefore needs no old theorem bodies.
Foundation leaves encountered include `List.brecOn`, `List.below`, `List.casesOn`,
`List.cons/nil`, `And`, `Eq`, `Iff`, `PProd`, `True`, `Unit` and `outParam`.
The proposed checker still starts from the ENTIRE exact 581-name fixed basis;
this trace does not authorize replacing it by those fourteen encountered names.

### The actual proof uses interfaces, not computation on their witnesses

Writing R_r(x)=run r x and C_r(y)=Settled r y, let the original hypotheses be
hr:AllClosure o r, hs:AllClosure o s, sr:Safe r, ss:Safe s, and
same:forall y, C_r(y) iff C_s(y). The saved DAG has this exact application shape:

1. `run_settles s ss x` supplies C_s(R_s(x)). Apply `Iff.mpr` to
   `same (R_s(x))` to obtain C_r(R_s(x)).
2. `run_extensive o s hs x` supplies o.le x R_s(x). Apply
   `run_below_settled o r hr x (R_s(x))` to these two proofs; obtain
   o.le R_r(x) R_s(x).
3. Swap r/s, use `Iff.mp` and the corresponding hypotheses, obtaining
   o.le R_s(x) R_r(x). Apply `OrderData.antisymm` to conclude R_r(x)=R_s(x).

Each application type agrees by direct binder substitution in the saved signature
DAGs. The six theorem result types do not depend on their proof arguments. The
target body contains only 10 lambdas, 79 applications, 14 const nodes, 10 bvars,
one sort and one forall binder type: no projection, recursor, let or literal node.
Its constant references are precisely the above laws and the named type/operation
interfaces. Thus this derivation needs neither theorem-value unfolding nor a
Nat-valued eliminator on a theorem proof. This is stronger than inferring opacity
from the keyword `theorem`; it is a concrete typed composition argument. The
recursive computations occur in retained `run`/`Safe`/`Settled` definitions, not
in hidden old proof values. Concrete reconstruction still preserves their bodies.

### Honest comparator and remaining gate

For this one target, full old ancestry is 35 units / 260,401 bytes; including the
target gives 36 units / 274,177 bytes, all outside the fixed basis. The semantic
cut selects 26 old units: twenty concrete units / 141,349 bytes and six theorem
interfaces (their original FULL files total 58,773 bytes; those are not projected
interface sizes). Nine older proof-only theorem units disappear: List's two
membership lemmas, `below_fixed`, `IsClosure.extensive/monotone`,
`OrderData.refl/trans`, `Repair.stable`, and `run_preserves`. Do not compare against
all 106 units for B's twelve targets to inflate the benefit. The largest selected
concrete file is 13,845 bytes; this is modest, not evidence of a global-scale cost.
One existing bounded batch/small-root route can handle this finite full closure.

The specific remaining check is that the current exact-basis kernel reconstruction
of these twenty concrete units reproduces every saved generated inventory, after
which the six grounded axiom-shaped signatures and this exact target pass the
fixed `addDeclCore` boundary. No missing proof-body dependency was found; native
success and the new interpretation/commit/restore contract were NOT executed here.
The earlier accepted final B root already contains this target: a new implementation
must reject it as a fresh name or report existing reuse, never claim this trace is
a new contribution. A differently selected warranted premise context is required
for a future replay gate. This scalar slice can extend existing concepts with laws;
it does not itself admit a newly invented `structure` or establish research speedup.

## Full-cost source discriminator

2026-10-24, current_scale_obstruction. Source/evidence comparison only; canonical
guard passed. No repeated dependency trace, native operation, protected-state
opening, implementation or Git mutation. Read the finite GROUNDED-CUT-CONTRACT,
ORDINARY-PRACTICAL-COST and the existing checking/catalog/baseline-intake sources.

**Decision: the structural benefit region survives, but this case does not prove
a CPU saving. Select at most a nonaccepting scratch-check discriminator before
building a new persistence/index backend.** The eventual cut lane must beat the
best available bounded native route for its intended workflow, not an imagined
baseline that kernel-rechecks all accepted proofs on every call.

| Route | Costs actually retained |
|---|---|
| Current native extension | `context()` walks roots/bindings; fresh owner hashes selected artifacts; `restoreLocal` imports the selected chain; worker enumerates all parent kernel names; only NEW units undergo `checkBatch`. |
| Existing aggregate batch | One selected native restoration and final new-name census for many already available units; metadata/staging/check/commit costs still apply. |
| Existing smaller parent | Real selected closure re-admission/setup once, then restoration of that smaller warranted context; proof-only dependencies required by its full proof units remain. |
| Proposed cut event | Root/support membership, selected summaries, actual concrete-definition/group rechecking, signature checks, new theorem checking, exact result/public-proof retention and distinct commit. |

Native snapshots already store deltas. Their reuse does NOT kernel-replay old
proof derivations. `_verified_artifacts` avoids repeated hashing within one owner
process, not across every fresh CLI; OS caches can further change actual I/O time.
No source argument here asserts every old proof byte is deep-copied/resident.
The known repeated costs are the explicit lineage/binding/name loops and selected
integrity reads; Lean loading cost and peak memory need their own bounds/evidence.

Scratch construction is not cheap merely because its bytes are fewer. Definitions
can contain costly conversions, inline proofs and large inductive rules. Literal
reuse of `OwnerConstruction.demand` calls `checkBatch` per concrete group, whose
before/after stage-two censuses revisit the growing scratch prefix. That can add
quadratic selected-name visits. The traced twenty concrete units have no nonbasis
theorem imports and can in principle use ONE existing bounded `checkBatch` before
the six signatures; general alternating semantic dependencies may not permit that.
This is a source simplification to review, not a selected optimizer or CPU result.

### The comparison that must stay positive

Compare the same successfully warranted endpoints under one unchanged foundation,
with equal cache/batch opportunities and original input availability. Initial
grounding of shared old mathematics cancels only when genuinely shared. For a
finite history define, in one additive resource or explicit fixed resource prices:

    Native = min_allowed_partition [branch_setup + sum(context + new_check + commit)]
    Cut = summary_and_index_setup + sum(lookup_update + concrete_recheck
          + signature_check + new_check_H + cut_commit) + extra_retention_failures.

Publication/service costs cancel only if actually equal; original complete proofs
must remain obtainable for other receivers. New checking costs in H and K need not
be equal. Failed cut attempts, deliberate later native fallback, migration reads,
retained index nodes and support changes stay charged. Peak RAM and deadlines are
separate feasibility constraints, not interchangeable terms in a CPU sum.

A structural family remains: old grounded contexts/selected full-proof closures
have many names, while recurring new laws use a stable small computational
vocabulary and a few old theorem TYPES. Existing native source pays linear selected
context-name work; bounded scratch reconstruction plus a persistent point map can
avoid that term even after charging its own setup/updates. For sufficiently many
uses, a positive per-use margin amortizes setup. This is a conditional model, not
proof that the current finite configured limits contain a measured winning case.
If exact selected proof ancestry itself is large, merely choosing a smaller native
root may not remove it; if unrelated history is the only problem, a small root may
solve it more cheaply. No useful theorem-discovery rate follows from either fact.

Batching receives full credit. The proposed one-theorem event cannot outperform
one final native batch merely by comparing against many needless native launches.
Its intended region needs separately available/durable results across real reuse
boundaries, or a native parent that is itself too expensive to restore. Likewise,
a protected metadata cache/index could also accelerate the native path; do not
credit all index savings uniquely to cut. If metadata alone dominates, evaluate
that simpler native improvement before committing to new mathematical authority.

### Minimum decision-changing implementation, and stop rule

After root selection and source review, a fresh DIAGNOSTIC worker can consume the
already traced fixed-basis inputs, twenty exact concrete units, six interfaces and
the exact target; reconstruct/check H, then check the target's actual inventory.
It emits bounded diagnostic observations only: no accepted root, cut event, new
public theorem, scratch-olean authority, root map, migration or database. A packet
assembled from the retained public export is an explicit conditional test input,
NOT a locally grounded warrant. It may establish kernel compatibility and selected
construction cost, never membership/freshness or recursive persistent acceptance.
Use the existing supervision/codec/checker boundaries; no new network or harness
framework is needed. This paragraph commissions no execution or source edits.

One such boundary is useful because a generated-group or type mismatch can kill
the route before backend work. Existing B intake measurements checked a different
67-unit endpoint and are not a matched restore-only baseline; do not subtract them
from this diagnostic. A later cost comparison, if needed, must isolate the same
endpoint/batching conditions and charge summary construction, not repeat the whole
concept episode. No giant synthetic library is required to rediscover known loops.

Stop before backend implementation if the exact scratch check fails for a required
supported feature, or if the only credible use region is already served by one
cheap native batch/small root. Proceed only when semantic compatibility survives
and a stated workload/resource bound leaves a positive FULL-cost margin or resolves
a genuine feasibility limit. A small byte count or successful diagnostic alone is
not that margin. If uncertain constants alone decide the sign, permit one bounded
matched discriminator; otherwise resolve the source/model issue first. Never fund
an expanding optimization campaign merely because the cut architecture is elegant.
