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
