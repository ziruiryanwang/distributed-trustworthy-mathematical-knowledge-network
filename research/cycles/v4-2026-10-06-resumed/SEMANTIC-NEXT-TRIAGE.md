# Next semantic step: checked named-definition dependencies

2026-10-06, source/theory triage; no launch, image change or product adoption.
Independent reviewer read current action-application-01 guest relation.rs,
journal.rs, main.rs, the beginning/checking flow of Nanoda inductive.rs, and
relevant held cert_capsule.py boundaries. This is not a whole-kernel audit.

## Decision

Prioritize an exact acyclic checked-definition DAG over another curated expansion
of F. It removes a recurring structural restriction for every already supported
type: acquired D1 may name exact acquired D0; D2 may name D1 without flattening
the entire semantic body into every new definition. A larger fixed whitelist
merely postpones that restriction. DAG sharing also preserves a meaningful
module boundary for later structured-library support.

This is more feasible than adding general inductive groups in the remaining
roughly2.5hours, but it is still a new checking relation and a multi-component
change. A deadline does not justify widening the current profile silently or
calling source-only design an implemented semantic capability. Finish selective
search, select the exact semantic contract, and pursue the minimum consequential
implementation only if the complete byte-binding path can be reviewed. Do not
spend the remaining window solely on packaging the restricted examples.

## Exact current obstructions

- relation.rs230-234 requires all constants in a contributed definition's type
  and value to be in reserved F. The def branch417-418 applies both checks.
- Definition identity270-276 uses transparent-definition-v1 and PROFILE_TAG;
  definition outputs429 carry an empty required_definitions vector.
- Current used-definition accounting455-489 collects direct constants from
  root expressions and selected Prop interfaces. It does not traverse named
  definition dependencies, because those dependencies are currently forbidden.
- cert_capsule.py320 rejects definition contexts outright; the source bridge626
  likewise forbids parents for a definition. Capsule projection, composition,
  host workflow and fragment transport inherit this model.
- journal.rs validates only definition members with empty requirements; parents
  are decoded against a single supplied image. main.rs uses that same image in
  every env::verify call. Old-to-new image import is therefore not already solved.
- Nonbaseline inductive declarations reach relation.rs441's rejection. This is
  a policy restriction, not absence of an inductive checker in Nanoda.

## Minimum DAG relation contract

1. **Dependency set and order.** For each safe transparent definition, collect
   all non-F constants from both its type and value. Every such constant must
   name an earlier supplied checked definition; no selected Prop axiom, theorem
   axiom, arbitrary data axiom, self-reference or later definition is permitted.
   Compute exact direct dependency IDs, enforce declaration-topological order
   and bounded closure size/edges/depth/bytes. Do not accept an owner-asserted
   dependency list without recomputation.
2. **Identity.** Preserve the exact old identity rule only for genuinely F-closed
   definitions satisfying all old premises. Dependency-bearing definitions use
   a new domain/profile-bound descriptor containing exact type, value, universes,
   reduction hints, safety and sorted direct dependency identities. The canonical
   name derives from this identifier; all references bind to exact supplied
   bodies. Exclude the definition's own name from its content-ID preimage as
   before. Keep reserved F names/redefinition protection unchanged.
3. **Actual checking.** Construct the exact environment and genuinely check every
   used semantic body with the existing checker. No receipt or descriptor turns
   a transparent computation-relevant body into an unchecked constant. A failed
   body, bad universe application or unresolved dependency rejects the operation.
4. **Transitive reachability.** Replace direct-only used-definition accounting by
   bounded closure traversal starting at output types/proofs and genuinely used
   selected Prop interfaces. Include each named definition's type and body
   dependencies. Reject unused supplied contexts under the chosen minimal policy;
   do not accidentally reject D0 because it is used only inside D1.
5. **Interface semantics.** Decide explicitly whether member requirement lists
   contain direct semantic roots or flattened transitive closure. Direct roots
   plus content-addressed validated DAG closure are sufficient in principle;
   declaring them direct is a schema/meaning change, not merely a larger cap.
   Legacy member semantics must retain their exact interpretation. Keep finite
   per-operation caps; arbitrary-depth mathematical construction does not mean
   one request can demand unbounded semantic material.
6. **Complete host path.** The capsule codec, identity computation, expected-target
   binding, projection/export, input composition, native source bridge, receiver
   validation and transport must agree on the new dependency semantics. Flat
   lists of repeated embedded contexts can erase the intended sharing benefit.
   Carry each demanded definition once per operation, with explicit named edges;
   durable cross-object CAS sharing can be an independently stated later boundary.

The conditional safety argument is induction over the dependency order: F is
fixed; each admitted definition is a well-typed conservative transparent extension
of the prior environment; the final proposition is checked in the resulting
environment with only genuinely certified Prop assumptions. The implementation
is not thereby formally verified; the actual check and byte-binding census are
still essential. Mathematical intention never enters this argument.

The representation advantage is also specific: if a new D_i adds O(1) syntax
referring to earlier IDs, n such definitions can use O(n) nodes/edges in the
shared closure instead of O(n^2) total independently flattened historical copies
for an appropriate chain. This does not guarantee linear conversion runtime or
eliminate demanded semantic closure. Certificates avoid theorem-proof ancestry,
not computation-relevant definitions needed by the chosen checking policy.

## Old receipts and semantic identities: migration must be explicit

A new guest can admit an immutable allowlist of exact legacy relation/image
identities only if it decodes each legacy journal with its original schema,
foundation and member semantics and invokes cryptographic verification against
that parent's actual adopted image. It cannot verify every parent against the
new image or accept any image named by an untrusted header. Bind image, relation
version, full journal and selected member indices together. Keep strict finite
rank descent/duplicate accounting across supported versions and require genuine
SDK discharge for a transferable certificate.

Preserving an old Prop interface identifier is justified only where its exact
old type/required-definition semantics are unchanged. Merely retaining PROFILE_TAG
while changing what required_definitions means is unsafe namespace overloading.
Prefer explicit legacy member decoding plus new dependency-bearing member domains;
do not require re-proving all old mathematics, and do not masquerade new objects
as having old certified semantics. Mixed-version receipt import itself needs a
positive old-parent/new-child test and a wrong-image/journal/profile negative.

## Why not add simple inductives at the same time?

Nanoda's check_inductive_declar genuinely builds/checks types and constructors,
checks positivity, reconstructs recursors and compares exported recursor rules;
the source includes explicit exclusion of surplus recursors. This is useful
existing machinery, not a reason to accept an inductive wire row unchecked.
Even a simple new List-like group introduces: canonical mutual/self-reference
identity, full type/constructor/recursor membership, uniform universe parameters,
safe recursor/elimination rules, projection metadata, exact dependency closure,
name collisions and interface commitments to the entire group. Existing roles,
journal member kinds, capsules and native bridge do not yet express that object.
Calling check_declar on one named member is not a complete group binding argument.

Thus keep new inductive groups outside this minimum DAG successor. The next
broader library slice should contain a real datatype and layered definitions,
with explicit positive and malformed/false-law controls. Checked definitions
alone still do not constitute general Lean/mathlib support. Retain that central
open requirement rather than hiding it behind another release label.

## Minimum decisive qualification if implementation is selected

Use D0 acquired from the existing boundary, a new D1 genuinely naming D0, and D2
genuinely naming D1, with one substantive acquired-law application and an exact
expected result. Inspect actual packet names/edges to rule out silent flattening.
Check once at a fresh receiver, with producer state unavailable. Pure contracts
must reject cycle, missing/mutated dependency, wrong name/ID, late reference,
hidden Prop-axiom dependency, universe mismatch and duplicate/over-cap closure.
An actual ill-typed semantic body must reach checker rejection. New relation
source, new image and old-receipt migration are separate acceptance facts.
No expensive new seal campaign is necessary merely to test local relation
execution, but local success is not a transferable receipt or full v4 completion.
