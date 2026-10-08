# Scale dataflow: certified interfaces without compulsory proof histories

2026-09-27. Author: v3_growth. Status: proposed dataflow and cost contract,
not implemented, executed or cryptographically qualified. Root has paused
installed/growth launches for the central scale redesign. Frozen source16's
reader gain remains a finite engineering result, not this contract's evidence.

This note owns selective retrieval, local views, availability and whole-loop
cost. [Scale requirements](SCALE-REQUIREMENTS.md) own the current priority;
the parallel certificate and Lean-interface notes own the acceptance relation
and importer. Earlier native-full-witness obligations remain facts about the
old profile, not restrictions on designing an explicitly different profile.

## Decision in one paragraph

A scalable node should retrieve a selected exact mathematical interface and
its transferable validity certificate, then hydrate only the selected types,
definitions and inductive/group information needed by its own work. Remote
theorem premises are **sealed** in this scale profile. Their proof histories
are not an implicit fetch fallback. If unchanged source needs transparent
computation through an old theorem body, the scale profile may refuse that
operation; a local agent can instead use a separately certified equation or
transport lemma. A separately selected, fully charged transparent/native audit
route remains possible. No central index, global ledger, complete corpus copy,
or universally current global status is required for mathematical acceptance.

## Five different questions

The following are separate predicates, not a single status named verified:

| Question | Evidence or state needed | What it does not establish |
|---|---|---|
| Did a search service return the desired exact object? | Untrusted candidate followed by an authenticated exact descriptor | Validity, completeness of search, or availability |
| Does the selected statement follow under the chosen foundation/profile? | Accepted exact certificate and all public-input bindings | That its original proof/source can be fetched |
| Does a downloaded byte object match the selected object? | Canonical typed commitment/length/chunk checks | Mathematical correctness without the certificate boundary |
| Can this local task actually use the interface now? | Compatible certified imports plus all demanded semantic data within budget | Compatibility with every ordinary Lean program |
| Can another peer fetch the data later? | A storage/service arrangement with explicit failure assumptions | Permanent availability merely because a certificate exists |

For example, `CERTIFIED` and `DATA_UNAVAILABLE` can both hold for one object.
An absent body is not a proof of mathematical falsehood. A resource refusal is
not a failed theorem. Useful operational statuses must retain these distinctions.

## Object decomposition

For artifact a, distinguish these committed roles. This is a specification of
roles, not a new wire schema or a claim that current product fields support it.

- **Interface I(a):** declaration kind, exact universe parameters, exact type,
  semantic dependencies and their typed identities, foundation/profile binding,
  and commitments to any associated definition/group content. An interface can
  itself be a shared syntax DAG. Its exact interpretation cannot be supplied
  by a peer's pretty-printed text or a name alone.
- **Validity certificate C(a):** a transferable certificate for the pinned
  acceptance relation and this exact interface, including grounded validity of
  its permitted premises. No implicit source-author trust is introduced.
- **Computational data D(a):** explicitly selected definition bodies, inductive
  descriptors, constructor/recursor interfaces and other data permitted by the
  scale profile's reduction policy. These objects need exact semantic binding,
  not merely storage membership. A declaration with a body is not necessarily
  allowed to unfold in every profile.
- **Witness/archive W(a):** original proof bodies, checking witnesses and other
  replay material. These are useful for native audit, certificate regeneration,
  learning and recovery, but are not mandatory receiving input for sealed use.
- **Presentation/source P(a):** names, source text, comments and convenience
  metadata. These may assist agents; they do not determine mathematical validity.

These sets need not be disjoint in storage. One immutable content-addressed
chunk may be referenced in several roles. Role overlap must not silently grant
extra trust or make archive retrieval an obligatory part of sealed admission.

An accepted interface is not a substitute Lean proof term by itself. The
certificate-aware importer and later certificate composition are a **new
acceptance boundary**. Exact remote proof premises must not become arbitrary
user-supplied axioms just because they appear in a locally loaded environment.
The [existing trust analysis](../../audits/succinct-checking-2026-09-24/TRUST-DESIGN.md)
already explains why checking a receipt and then calling unchanged full-replay
`submit` would move, rather than solve, the bottleneck.

## A crucial Lean limitation: not every proof body is computationally irrelevant

The source-backed [CP-001H analysis](../../../notes/analyses/CP-001H-proof-computation-and-reconstruction.md)
at Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` distinguishes
frontend theorem opacity from native kernel behavior. The C++ kernel's value
classification includes theorem bodies; native delta reduction can unfold them.
Accessibility/well-founded recursors can use proof-valued major premises while
computing data. The note gives a paper countercase in which replacing one proof
of the same proposition by another changes whether the concrete conversion
algorithm exposes a constructor. This is a source-backed mechanism and paper
countercase, not a newly executed test here.

Consequently, the scale guarantee must be a profile guarantee, not the false
statement that deleting every old Lean proof body preserves every old program.
The selected direction has these rules:

1. Remote theorem premises used through this profile are sealed. Neither the
   type checker nor elaborator can silently turn a reduction demand into full
   ancestral proof hydration. The exact sealing/import semantics require the
   separate Lean-interface specification and tests.
2. A source term requiring forbidden proof-body reduction can fail elaboration
   or checking in this profile even when it worked in native-full mode. Report
   a compatibility/refusal condition, not that its mathematical statement is
   false. Distinguishing every such cause automatically is not presumed.
3. A separately certified propositional equation can support a new explicit
   proof/transport without being installed as a new definitional equality rule.
   Finding that equation or repair is local agent work; success is not guaranteed.
4. Transparent audit/replay is an explicit alternative operation with separate
   bytes, costs and support claims. Its success does not qualify the sealed path.
5. `D` below is not a loophole: collecting all old theorem witnesses and calling
   them reduction data fails the contract. Proof/history absence is tested at
   the actual storage and network boundary, not inferred from a favorable label.

The same caution applies to proof-containing definitions. Fetching an explicitly
needed definition's finite descriptor is different from recursively downloading
the proofs referenced inside it. Sealed proof references stay sealed. A profile
which cannot check/use that definition without forbidden reduction must refuse
or require an explicitly different certified interface/equation route.

## Demand-driven hydration protocol

An illustrative one-result flow is as follows. These operations are proposed
API semantics, not names of current callable commands.

1. **Discover a candidate.** Query any local cache or chosen peers. The response
   is advisory: a content identifier, a compact descriptor and candidate holders.
   Search ranking, advertisements and natural-language matching are not trusted.
2. **Select exact meaning and profile.** Retrieve bounded canonical interface
   material. Bind its universe/type/declaration identities to a locally supported
   foundation, checker relation, import/reduction profile and certificate scheme.
   Incompatible data is not rewritten into the current profile without evidence.
3. **Authenticate validity.** Verify a directly bound certificate, or verify a
   certified collection/context root plus the selected interface's membership.
   A plain signed or Merkle-rooted catalog is not a validity certificate.
4. **Register locally.** Record the exact accepted interface/certificate/policy
   binding. This establishes logical reliance under the chosen assumptions; it
   does not assert that all material for every future computation is present.
5. **Hydrate as required.** For a requested declaration, universe/type check,
   unfolding or generated-group operation, fetch only the permitted referenced
   objects needed for that operation. Hash-check each object against its typed
   commitment before use. Shared objects are fetched once per local cache life.
   No parser prefetch or dependency walker is allowed to expand witness edges
   merely because they occur in a complete archive manifest.
6. **Perform new work.** The local agent elaborates/proves using the certified
   interfaces and the profile's available semantic data. New acceptance must
   certify this checking step and its direct certified premises compositionally,
   not reconstruct every parent's proof history.
7. **Contribute.** Offer the exact new interface/certificate and its needed data
   separately from optional full witness/archive material. Local storage and
   replication decisions remain explicit. Publication does not guarantee future
   service by the publisher or by anyone else.

Use independently authenticated chunks/DAG nodes with bounded length, fanout,
depth and total hydration budgets. A byte-level Merkle tree can authenticate a
selected chunk without fetching a huge file, but syntax validation may require
adjacent/referenced chunks. A protocol must define its canonical chunk/object
boundaries; accepting an arbitrary hash-matching byte slice as a complete Lean
declaration is not meaningful. Avoid allocation before bounded length checks.

Missing, corrupt, incompatible, exhausted or unsupported data leads to refusal
or a recoverable incomplete operation. It never leads to a fabricated default
body, unchecked placeholder, waived premise, or mathematical rejection based
solely on absence. Interrupted fetches must not promote partial state to accepted
usable state. Separately valid certificate evidence may remain cached.

## A quantitative contract that does not hide history

For a fixed receiver task q, let:

- N be unrelated network corpus/history size;
- H be total ancestral proof/witness bytes of the selected lemmas;
- k be the number of directly selected certified premises;
- I be newly read exact interface/type bytes, including their needed semantic
  references rather than only the size of a root hash;
- D be newly demanded, permitted definition/group bytes, as distinguished above;
- L be authenticated lookup/membership bytes for the selected immutable views;
- C be certificate bytes, and V(lambda, C, x) their actual verification work;
- p be the new local proof/certificate witness and K(p; I, D) its checking work.

Cold receiving bandwidth should have the form

    B_receive(q) = O(I + D + L + C),

and receiving work should be bounded in terms of parsing/authenticating those
bytes, permitted local reduction and V. Neither expression contains a mandatory
linear H or N term. Whether L is logarithmic in a particular catalog depends on
its actual authenticated data structure; a generic semantic search is not
promised logarithmic merely because the result store is content-addressed.

Subsequent contribution additionally costs reading the new output/proof,
K(p; I, D), and real certificate generation for that new step and its k direct
certified premises. The prover must not secretly re-expand H to regenerate the
new certificate. Actual recursion/aggregation costs and soundness assumptions
belong to the certificate design and must be measured, not assigned zero here.

Three nonvacuity conditions are essential:

- **Fixed-task history expansion:** increase unused ancestral witness material
  while keeping selected interfaces, permitted computational bodies and the
  downstream task fixed. The sealed receiver must not read the extra witnesses.
- **Unrelated growth:** add unrelated objects/certified snapshots without changing
  selected immutable views. One selected fetch/use cannot force a global scan,
  global revalidation, or update replay. Search over a newly selected larger
  view can have its own declared index-dependent cost.
- **No hidden transfer:** charge caller, importer, certificate prover, child
  processes and cache misses. A tiny verifier surrounded by full native replay
  or a prover that reloads all histories does not meet the whole-loop contract.

No universal constant-time theorem follows. A chosen statement/output of b
explicit bytes costs at least Omega(b) to read or emit. A selected definition
can be huge; a new proof can require expensive reduction; k can be huge; an
agent's proof search can fail. The requirement removes mandatory *irrelevant
historical* work, not work genuinely requested by the task.

For m tasks on one node with compatible immutable caches, unique hydration can
be bounded by the bytes in the union of their demanded interface/definition
objects, plus authenticated-access and certificate costs. This is an
amortization claim conditional on retaining and safely reusing those objects,
not an assumption of free infinite storage. Eviction and different trust-domain
caches can cause repeated work and must be counted.

## Certified checkpoints are optional views, not one global ledger

A node can publish an immutable finite catalog root R and, optionally, a
certificate establishing the precisely stated invariant for the interfaces
committed by R. Another node verifies that certificate once, then fetches a
selected leaf/interface with an authenticated membership path. A valid hash
without a usable membership/interface binding is insufficient for reuse.

The certified invariant must be explicit. For example, every mathematical
interface leaf in this designated tree is valid under profile F is stronger
than this tree contains one valid result. Neither statement implies that the
tree contains *all* network knowledge. A tree mixing advisory advertisements
and valid interfaces must not grant the former the latter's authority.

Recursive checkpoint extension can avoid replaying prior updates only if the
new certificate proves the required grounded invariant and exact transition.
Independent per-object certificates are a simpler permissible organization;
no checkpoint batching is mandatory. Several compatible certified roots can
coexist. Their selected joint environment still needs the interface design's
exact consistency/composition checks; matching names are not enough.

A receiver subscribes to selected peers/topics/roots or performs queries when
needed. It need not subscribe to every result or even know every node exists.
An immutable old snapshot remains an old snapshot, not secretly the latest one.
There is no generally meaningful globally current complete head in an
asynchronous decentralized network without extra assumptions and machinery.

If results arrive at aggregate explicit information rate r and a node has
usable intake rate b < r, that node cannot consume all of them continuously
without an ever-growing lag or loss. Cryptographic summary checking does not
let its user read every theorem statement for free. Thus the system's earlier
aspiration to be updated about the whole system should mean access to
authenticated selected summaries and demand-driven knowledge, not compulsory
complete local awareness. Even the former is conditional on reachability.

## Search correctness is narrower than mathematical correctness

An untrusted index can omit a useful lemma, return a stale snapshot, lie about
popularity or offer unavailable holders. These harm discovery/liveness; they
cannot make an invalid theorem pass the independent certificate boundary.
An exact match check must still bind a returned interface to the user's selected
formal query semantics where such semantics exist.

Merkle inclusion proves inclusion in one committed snapshot, not exhaustive
answers to arbitrary mathematical/semantic questions. Some declared finite
queries, such as a range over a canonically ordered authenticated index, can
carry completeness/nonmembership evidence for *that index and query*. A root
over untrusted or incomplete index contents still does not prove coverage of
all valid mathematical results. Approximate vector/LLM ranking remains advisory.

The first useful version need not solve generic complete theorem search. It
needs multiple usable discovery routes, exact candidate identification and a
correct independent reuse path. Heuristic value estimates and agent preferences
may improve ranking without becoming new mathematical acceptance criteria.

## Availability, archival and fault behavior

Certificate soundness is not data availability. Even a proof of knowledge of
an acceptance witness at certification time does not establish that a future
receiver can fetch it. A protocol cannot guarantee retention after every holder
deletes its copy or every contact becomes unreachable.

State availability promises conditionally: at least one reachable holder retains
the exact needed objects and supplies them within the receiver's bandwidth,
budget and supported protocol. Replication/erasure coding can improve this under
a stated failure model, but neither creates unconditional perpetual availability.
They are independent storage policies, not a mathematical truth election.

At least some holders should retain witnesses if native audit, proof inspection,
reproving under a new scheme, or repair after a certificate-system defect is a
promised capability. Ordinary sealed consumers need not become those archivists.
Archive commitments aid exact retrieval but are not custody promises. Loss of
an archive may leave old certificate-backed logical reliance possible while
preventing future migration or independent full replay; report that limit.

Availability needed for ordinary reuse can differ from archival availability:
a theorem's interface/certificate and the selected computational definitions
may remain available after its full proof is lost. Conversely, a valid stored
certificate with a missing essential definition is not a usable local library.
The local accepted-interface registry and usable-data inventory must be separate.

Exact caches are keyed by foundation, certificate relation/verifier parameters,
import/reduction profile, exact interface and the relevant semantic environment.
Bytes can be content-shared across profiles, but an acceptance assertion cannot
be transferred between them solely because an artifact hash matches. Changed
proof-system assumptions, checker bugs or import policies require an explicit
local trust/migration decision; an old immutable mathematical descriptor is not
proof of acceptance under the replacement profile.

## Minimum falsifying tests before a scale claim

These specify the next central discriminator, not an execution allocation.

| Case | Required observation |
|---|---|
| Fixed lemma interface with growing ancestral proof bodies | Cold receive, actual downstream Lean use and recursive contribution do not read/transfer ancestors; real certificates, not mocks |
| Same selected objects with growing unrelated corpus/history | No compulsory global scan/replay; disclose any selected-index logarithmic or cache cost |
| Selected definition genuinely needed | Only permitted authenticated definition/group support is requested; no hidden witness-closure walker |
| Proof-sensitive computation | Sealed profile refuses or uses an explicit certified equation/transport path; it never secretly fetches historical theorem bodies |
| Missing needed definition/chunk | Controlled unavailable/incomplete operation, no unchecked state promotion |
| Tampered interface, leaf, chunk, context/profile binding | Rejection before mathematical reliance or use of corrupt content |
| Valid root plus wrong/missing membership/interface | Refusal; root validity alone cannot install an arbitrary theorem |
| Valid stale/partial catalog | Correctly scoped snapshot result, no false claim of globally latest/complete search |
| Warm repeated tasks and cache eviction | Exact reuse reduces unique hydration; eviction/revalidation costs remain visible |
| New contribution from two independently certified premises | Actual composition joins exact interfaces without flattening proof history |

Report receiver/prover/interface/definition/witness bytes separately, inclusive
CPU and memory, certificate size, fan-in, failures and genuine task outcome.
Matched native-full and sealed trials need the same selected formal endpoint,
not a weaker statement in the cheaper arm. If the sealed profile cannot express
the endpoint, that is a support failure, not evidence of a speedup.

## Consequences for the current v3 decision

The current full-package native route does not satisfy the new scale guarantee.
The source16 local reader saving does not change this conclusion. Do not spend
the paused growth campaign merely to claim that the architecture scales.

The most consequential implementation slice is a real certified sealed lemma
that a fresh node can actually use and compositionally re-certify while its
ancestral witness store is inaccessible. Pair it with one demanded-definition
case and one proof-sensitive refusal. This exposes the certificate/import/data
boundary before introducing a global routing service or more elaborate rankings.

If a real certificate backend or sound Lean import boundary cannot be completed
by the tentative deadline, the honest release remains native-full with an
explicit scale gap and this proposed successor contract. A mock verifier or
trusted-peer assertion must not be published as the missing scalable acceptance
mechanism. No new code, runtime, experiment, deployment or success is reported
by this note.

## Reused references

- [Current scale requirements](SCALE-REQUIREMENTS.md).
- [Current-v2 succinct trust-boundary analysis](../../audits/succinct-checking-2026-09-24/TRUST-DESIGN.md).
- [Earlier cryptographic assessment](../../SNARK-ASSESSMENT.md), with its older
  native-only prioritization superseded by the explicit scale requirement.
- [Proof-sensitive computation and reconstruction](../../../notes/analyses/CP-001H-proof-computation-and-reconstruction.md),
  including its pinned Lean source references and scope limitations.
- [Cooperation and technology reuse](../../COOPERATION-TECHNOLOGY-REUSE.md):
  authenticated routing roots do not prove mathematical truth, completeness,
  freshness or availability; a public blockchain is not required for this role.
- [Growth design](GROWTH-DESIGN.md): useful-growth hypotheses and finite measured
  outcomes must remain distinct from a claim of exponential accumulation.
