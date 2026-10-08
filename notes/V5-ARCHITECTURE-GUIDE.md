# A theoretical guide to the mathematical commons

## What this guide describes

This is the complete **candidate architecture for v5**, written on October 8,
2026. It explains the system as a whole: what mathematical objects it shares,
how agents find and trust them, how new contributions return to the network,
what makes the design scalable, and what would justify useful growth.

It is not a claim that the whole architecture is already delivered. The source
and audited development baseline is Git checkpoint `fdfcd80`. Some mechanisms
have implementations and focused evidence; others remain design obligations.
[Section 16](#16-what-exists-and-what-is-still-missing) makes that boundary explicit.
This writing task does not audit or adopt a later background proof result.

Read sections 1–3 for the overall picture, 4–11 for the mechanisms, and 12–16
for the theoretical guarantees, limitations and release requirements. An
undergraduate reader needs only basic ideas about functions, proofs and graphs;
specialist terms are explained where introduced.

## 1. The idea in one page

The commons is a **decentralized library of reusable, formally warranted
mathematics**. It is not one giant language model, one giant database installed
on every computer, or a blockchain on which participants vote about truth.

A local agent can follow this cycle:

```text
Choose its own investigation
        |
        v
Search independent indexes for formal candidates
        |
        v
Locate and acquire selected objects from custodians
        |
        v
Verify mathematical certificates and authenticate needed interfaces/bodies
        |
        v
Use the imported mathematics to check a new contribution
        |
        v
Publish its objects, arrange custody, and advertise them to indexes
        |
        +----> another independent agent can repeat the cycle
```

Each arrow has its own failure conditions and resource limits. Finding an entry
does not mean it is true. Verifying a result does not make it useful. Possessing
a valid certificate does not ensure that its definitions remain downloadable.

The architectural division is therefore:

- **Validity:** is this exact mathematical content warranted under the adopted
  formal rules?
- **Discovery:** which available results might help with this formal problem?
- **Availability:** can the selected bytes actually be obtained when needed?
- **Usefulness:** does reuse expand what an agent can accomplish, or lower its
  cost, compared with an appropriate alternative?

These questions interact, but must not be collapsed into one reputation score
or one network consensus decision.

### What the system does not require

There is no mandatory global research agenda, list of unsolved problems, root
goal, human-intention field or human-language/formal-language translation layer.
Agents choose their own work. They may use people, LLMs, proof search or any
other method locally; none is a mathematical acceptance authority.

An agent can submit a perfectly valid result that nobody requested. A result
does not become invalid because it is uninteresting, duplicated or unexpected.
Storage admission, advertising and ranking may still refuse to spend resources
on it. **Mathematical validity and a right to consume somebody else's resources
are different things.**

## 2. The layers and their responsibilities

This layering separates hard correctness requirements from useful but fallible
search and investment strategies. It is a division of responsibilities, not a
requirement to implement the layers in numerical order.

| Layer | Main responsibility | Must not be mistaken for |
|---|---|---|
| Formal foundation and acceptance policy | Specify the logic, permitted declarations, exact checker and certificate profile | A vote about truth or an assertion that every Lean feature is supported |
| Immutable mathematical objects | Name modules, declarations, types and computational bodies unambiguously | A complete archive of every proof or every publication event |
| Verification and modular reuse | Establish valid imports; check new work without mandatory ancestral theorem-proof replay | A guarantee that arbitrary computation or proof search is cheap |
| Custody and transport | Store, locate and transfer exact selected objects within operational limits | Mathematical authority or perpetual availability |
| Discovery | Search versioned formal features through replaceable indexes with explicit coverage | Complete semantic search over all mathematics |
| Local-agent interface | Connect acquisition, live verified imports, ordinary Lean authoring and contribution | A centrally prescribed research strategy |
| Growth and investment policy | Allocate search, certification, indexing and replication effort where justified | A universal measure of mathematical value |

Resource accounting, security isolation, version compatibility and recovery
cut across every layer. They are not optional decorations added after correctness.

### The participating roles

A participant may act as a consumer, contributor, index provider, custodian,
location/routing peer or proof-producing service. One machine can perform
several roles, but none must be performed by everyone.

A lightweight consumer should not need to store the whole corpus, operate a
public server, or produce expensive cryptographic proofs. An independently
operated index should be replaceable without changing mathematical validity.
A proof service may be untrusted: its output must pass the recipient's own
verification rules. Connectivity relays are a deployment role still requiring
an implemented, reviewed path; they are not supplied by the word "decentralized."

## 3. What represents the whole body of knowledge?

The network-wide library is a **logical union of distributed objects**, not a
physical lump that every node must download. A node keeps the parts relevant
to its roles, interests, budgets and retention commitments.

There need not be a node that knows every existing object. Nor can an open
network under arbitrary partitions guarantee that everyone knows its current
complete state: an unreachable participant might hold an unpublished or unseen
result. A search report must describe the views actually consulted, not claim
omniscience.

The core records are:

| Record | Meaning |
|---|---|
| Module specification | An immutable collection of declaration groups under an exact foundation and semantic policy |
| Module identifier, or ModuleID | A cryptographic commitment to that specification's summary |
| Declaration/group opening | Selected interfaces plus evidence that they belong to that module commitment |
| Computational body | An exact definition or rule needed to interpret or compute with selected interfaces |
| Proof witness | Material demonstrating a module's validity; used by a checker or prover |
| Certificate, called a receipt in the implementation | A portable cryptographic warrant for a precise checked module conclusion |
| Discovery record | Search metadata about an object; not a mathematical warrant |
| Custody/location record | A claim about where bytes might be obtained, possibly with a retention horizon |

The current module summary commits to its foundation ID, semantic-policy ID,
ordered group root and group count. A Merkle root is a compact hash commitment
to many records; an *opening* authenticates selected records without transmitting
the whole collection. Hash binding relies on the adopted hash assumptions.

ModuleID identifies exact canonical mathematical syntax, not arbitrary semantic
equivalence. Two different encodings of equivalent mathematics may have different
IDs. Two valid proofs of the same committed module can have the same ModuleID.
Exact proof witnesses, certificate encodings and certificate ranks are not all
part of mathematical identity.

Names inside a module are structured names, not ambiguous dot-split text. A
reference identifies the owning module, the declaration and its universe
instantiation. A universe is a level used by Lean's type system to distinguish
types of types. Renaming a displayed binder is not permission to reorder
universe parameters or change their meaning.

Local names are represented relative to their module. After commitment they
can be exposed under a module-qualified namespace. This avoids requiring a
module's hash to contain that same hash as a literal self-reference. Independent
authors can both write a declaration named `Tree` without a global name registry.

## 4. What "correct mathematics" means here

Fix a foundation \(F\), a semantic policy \(P\), and an adopted implementation
profile \(A\). These are three related but different choices:

- \(F\) identifies the base mathematical environment.
- \(P\) identifies permitted mathematical constructions and interpretation rules.
- \(A\) identifies the concrete checker, guest image, verifier parameters and
  local software trusted to implement those rules.

The target mathematical judgment is:

\[
\operatorname{Valid}_{F,P}(M):
\quad M\text{ is a well-formed, checked extension of valid imported environments.}
\]

For a theorem this includes a proof of its claimed type. For a definition it
includes a well-typed computational body. For a new inductive datatype it
includes the whole checked declaration group and the appropriate constructor
and recursion rules. Checking only a list of claimed theorem types is not enough.

The software cannot prove its own entire trust basis correct simply by running
itself. The acceptance argument is conditional on the foundation, the checker
semantics and their implementation. Formal derivability under an inconsistent
foundation would not provide the intended assurance. Cryptography does not
establish consistency of a chosen foundation.

The current candidate uses a narrow adopted Lean-compatible foundation and a
revised Nanoda-based checking relation, with an ordinary Lean frontend. It is
**Lean-based, not a claim to support all Lean or Mathlib**, and its complete
checker-to-Lean correspondence is a remaining assurance obligation.

### The certificate argument

The guest is the checking program whose execution is certified. The receiver
locally adopts its identity; a peer cannot make a new program trustworthy merely
by supplying its hash. Abstractly, the intended guarantee is:

\[
\operatorname{Verify}_{A}(J,\pi)=\mathrm{accept}
\quad\Longrightarrow\quad
\exists w:\ \mathcal R_A(w,J)\text{ succeeds with its required premises discharged}.
\]

This is a computational soundness claim under the selected proof system's
assumptions and security parameters, not a logically infallible implication.
The relation \(\mathcal R_A\) must, separately, faithfully establish
\(\operatorname{Valid}_{F,P}(M)\). A succinct proof of a buggy checker remains
a proof of that buggy checker's execution.

The present profile is the 184-byte `DMKNM002` existential journal. It binds
the image, foundation, policy, ModuleID, group root/count and certificate rank.
It certifies **the existence of a checked witness**, not that arbitrary Lean
source or proof bytes shown alongside it were the witness used. Computational
bodies and interfaces remain committed. The old 216-byte profile is not silently
reinterpreted as this one.

The concrete receiving gate accepts the selected real Succinct/Poseidon2
receipt form, disables development mode, verifies the full successful
application claim with no unresolved assumptions, and checks the exact adopted
image and journal/module bindings. The guest's `env::verify` creates a premise
obligation; subsequent proof composition must actually discharge it. A fake
receipt, unresolved claim or integrity-only check cannot replace that gate.

### Why recursive certificates need a well-founded graph

A module may use certificates for earlier modules. That creates a directed
acyclic graph of certificate premises. Independent branches and shared parents
are allowed; a single global chain is unnecessary.

For the current certificate instance, rank is zero with no parents and otherwise
one plus the maximum parent rank. Exact premise journals, not just names or
rank numbers, are verified. Finite descending ranks rule out circular
"A is valid because B is valid; B is valid because A is valid" support.

Assuming sound certificate verification and a faithful relation, induction on
rank gives the architectural argument: valid parents plus a correctly checked
local extension yield a valid child. This needs the actual recursive,
branching composition to be covered by the cryptographic trust case.

That trust case needs an explicit security/attack horizon; one-shot soundness
is not automatically a guarantee for unlimited adaptive checks and joins. A
credible engineering case can combine precise assumptions, scoped mathematical
arguments, adversarial tests, differential checking and independent review.
It need not pretend that every implementation line has a completed formal proof.

Rank is not a date, global block height or mathematical identity. Different
witnesses for the same module can produce different certificate instances.
The current import session chooses an exact journal; it cannot mix ranks and
premises from different instances merely because their ModuleIDs agree.

## 5. Reusing mathematics without downloading its proof history

The crucial separation is between **why a declaration is valid** and **what is
needed to use its mathematical meaning**.

### Opaque theorem interfaces

Suppose module A contains a difficult theorem \(T\), and B needs to use it.
If A's valid certificate warrants the exact type of \(T\), B can instantiate
that interface without downloading A's original theorem proof. B must still
prove the new obligations in its own argument.

This resembles calling a function through a trustworthy interface, except that
the mathematical warrant is independently verifiable, rather than just a
promise from the library author.

Here a theorem proves a proposition in Lean's `Prop`. Omission of its imported
proof relies on the supported proof-irrelevance semantics and the revised
checker's sealed-theorem representation. This is not a general permission to
erase arbitrary computational data.

An **Opaque data declaration** is different: its original body is checked and
committed, while downstream type conversion preserves opacity rather than
unfolding its implementation. It must retain that declaration kind; it is not
a new arbitrary axiom or an absent transparent definition.

### Transparent definitions

Knowing that a definition is valid is not always enough to compute with it.
For `double n := n + n`, a type-conversion check may require unfolding the body.
Its certificate does not magically supply those bytes or perform that computation.

The candidate relation therefore uses authenticated, demand-driven import data:

1. Verify the selected owner's certificate.
2. Authenticate selected declaration-group openings.
3. Retain each declaration's original kind and reduction behavior.
4. If checking requires a missing declaration or body, return a typed demand.
5. Acquire the exact committed material within the same overall budget, or stop.

A missing transparent body must not be replaced by an axiom, a dummy value,
artificial opacity, or a conclusion that an equality is false. "Need more data"
and "invalid mathematics" are distinct outcomes.

New definitions and theorem proofs are checked. A certified imported body need
not be re-proved merely because it is imported, but its hash, interpretation and
any computation using it still require work. Inductive groups are imported
atomically where their constructors and recursors have joint obligations;
arbitrary externally supplied recursor equations are not accepted on trust.

### Compatible branch merging

Two branches can share the same certified module and add different results.
Their union is usable only when exact references, foundations, policies,
universe assignments and group metadata agree. An exact shared dependency is
coalesced; an incompatible interpretation is rejected or kept in a separate
environment. A merge is not a majority decision.

Namespace separation prevents accidental name collision; it does not establish
logical compatibility across different policies. Translation between foundations
requires an explicit checked interpretation or a separately justified bridge.

## 6. Two validation costs, and why certification should be selective

There are two distinct kinds of expensive work:

- Producing a proof or certificate once.
- Checking and using the result at each recipient.

The implemented receipt route uses a RISC Zero-based succinct-proof backend.
It is not justified to call every accepted receipt a particular SNARK or to
assume that a compression scheme's name settles its security. The exact backend,
recursive rules, parameters, guest and verifier all matter.

The producer prepares an exact witness, executes the checking guest to obtain a
coherent execution capsule, and processes proof stages such as segment, lift,
join and premise resolution. These are internal proof-production operations.
Only a final fully verified, resolved receipt is a portable warrant. An execution
capsule, completed segment, build success or progress report is not one.

Staged production retains successful work within a finite operation; it need
not reexecute the guest for each stage. The producer can run separately from
the recipient. Outsourcing production does not outsource mathematical trust
provided the recipient performs its own correctly adopted verification.

### Proposed economical complement: bounded proof deltas

A small new theorem may be cheaper to check directly than to certify
cryptographically. The candidate economic design therefore also proposes a
packet containing a **bounded set of ordinary new proof witnesses above genuine
certified frontiers**. A frontier is a set of already certified modules where
ancestral proof replay stops.

The recipient would verify the frontiers and check every uncertified delta in
dependency order. The packet must include its complete uncertified dependency
closure. Merely limiting its depth is insufficient: a shallow graph can have
enormous branching. Total bytes, nodes, edges, bodies, verification calls and
checking resources need aggregate limits.

When that packet becomes too expensive, an agent can choose a smaller proof,
fund certification of an intermediate module, or stop. It cannot silently
download unlimited ancestry or treat an earlier sender's success flag as a proof.

This v5 delta route is **a design, not an integrated implemented capability**.
It requires a distinct local `VerifiedDelta` authority class; it must not
impersonate the current receipt-backed `VerifiedModule`. The current guest
requires genuine parent receipts and does not automatically seal an arbitrary
uncertified delta graph. Aggregate sealing needs another sound relation or a
careful identity-changing repackaging. Individually certifying selected
intermediates is the conservative alternative.

For a fixed target, let \(C_D\) be the cost of direct delta checking, \(C_R\)
receipt verification/use, and \(S\) the additional total cost of creating and
maintaining a seal. Sealing saves the chosen resource valuation when

\[
n(C_D-C_R)>S.
\]

If \(C_D\leq C_R\), more recipients do not rescue that comparison. Cheap native
checking of a small theorem is not evidence that receipts are automatically
more efficient. Counts must represent actual uncached work, not repeated visits
to a library that already accepted the result.

## 7. The local-agent interface and ordinary Lean authoring

The network should provide dependable operations, not control the research
strategy. An agent can be taught these operations through API documentation
or a skill. Its decision about when to search, which candidate to try, and how
to prove remaining obligations can remain outside the core protocol.

Some integration nevertheless belongs in the system: object identity, valid
import lifetimes, budget sharing and preventing a source-level assumption from
escaping as an accepted theorem cannot safely be left to prompt wording.

The current public seams are:

| Operation family | Role |
|---|---|
| `SearchSession` and search client | Bounded discovery with shared costs and coverage records |
| Located acquisition workflow | Obtain selected module material and real receipt bytes from approved contacts |
| `ReceiptVerifier.receive` | Verify the exact receipt and return a live, registered local handle |
| `ImportSession` | Hold exact selected verified parents, authenticated groups and bodies |
| `SourceOperation` | Prepare ordinary Lean authoring context and convert the new export into an untrusted child request |
| `OwnerPreparation.author` / `snapshot` | Supervise source execution and parent-aware capsule preparation |
| `Producer.run` | Produce a receipt under a separately funded finite operation |

This table is an interface map, not a runnable end-to-end tutorial or a claim
that the full positive chain has already passed.

A **live handle** is an in-process record registered by the actual verifier.
It is not a transferable certificate, and saving its JSON does not preserve
acceptance. Closing or expiring the originating verifier invalidates its handles.
A fresh process receives and verifies the certificate again under its own policy.
The import session's exact receipt/profile cache avoids redundant work inside
that operation; a cache indexed only by theorem name would be unsafe.

Ordinary Lean source elaboration is a producer activity. The frontend reconstructs
the selected environment and exports new kernel-level declarations for independent
checking. It temporarily represents imported theorem and opaque-value interfaces
as tightly bound authoring assumptions; no new free local axiom may escape. The
final relation retains their original kinds, and real parent verification
supplies their mathematical authority.

There is an important current asymmetry: the checker supports missing-body
demands, but stock Lean elaboration does not have this custom lazy-import
semantics. The authoring adapter therefore acquires a bounded selected
definition/body dependency closure before elaboration, or refuses. It may need
more semantic data than the final checking relation. Those extra costs must
not be hidden behind "lazy imports."

An LLM's weights can guide this workflow, but are not the authoritative library.
Continuous training is optional local infrastructure. It neither replaces exact
retrieval nor provides a checkable warrant for a remembered mathematical claim.

## 8. Discovery: finding a result whose ID is not already known

The kernel acceptance layer need not understand human-language mathematics at
all. A natural-language assistant may be useful locally, but the protocol sees
exact formal objects and warrants. Removing that interface from the core does
not remove the separate, difficult question of finding useful formal work.

Exact-address retrieval answers "Who has object X?" Mathematical discovery
answers "What might help with this kind of statement?" A distributed hash
table alone does not answer the second question.

Independent providers build indexes of formal features: for example, symbols
in a declared type, the shape of its conclusion, declaration kind and exact
dependency references. Feature extraction is versioned and bounded. It need
not normalize arbitrary expressions or decide mathematical equivalence.

An agent formulates a conjunction of known features, asks several suitable
providers, and merges candidates. It need not know the target ModuleID or an
index snapshot ID in advance: a provider offer supplies a committed snapshot
and a bounded partition plan. Relevance ranking, learned search and richer
matching can be replaceable additions; none becomes mathematical authority.

In the current v5 adapter, a searchable object is an individual exported
declaration, identified by its `ExportID` (module plus structured relative name).
Features must describe that declaration, not the union of unrelated exports
from its module. Deduplication retains the pair of object identity and metadata
record identity: a bad first metadata claim must not hide an honest alternative
claim for the same declaration. Candidates still require an understood formal
vocabulary; the index is not an oracle that discovers every useful abstraction.

### Authenticated snapshots and two search modes

A snapshot commits to an immutable index view. The implemented index divides
posting sequences by namespace, feature and object-ID partition, with
authenticated counts and records. Compact representations reduce overhead
without changing the committed content.

The client distinguishes two useful interfaces:

| Mode | What the client verifies | What it cannot conclude |
|---|---|---|
| Authenticated interval page | Every ordinal in a specified interval of a selected committed posting sequence is present, including examined nonmatches | That the entire corpus was indexed or every relevant theorem was found |
| Positive-candidate reply | Each returned record belongs to the committed snapshot and matches the advertised feature predicate on that record | That omitted positions were searched, that the cursor proves coverage, or that zero hits means no match |

Positive-only replies can greatly reduce transmission of nonmatches. They do
not prove cheap provider work: an unselective query can still scan a very large
posting intersection. Provider work counters are claims, not cryptographic
proofs of effort and not grounds for giving back an unlimited search budget.

There are four separate assurance levels:

1. A record is included in the provider's committed index.
2. Its features truthfully describe the exact acquired mathematical object.
3. A stated region of that index was searched completely under its feature rule.
4. The index truthfully includes a specified source corpus.

Current authenticated pages address defined parts of the first and third.
Recomputing features after acquisition checks the second for selected objects.
The fourth requires an additional index-construction/coverage argument.
None establishes global completeness over disconnected or unpublished work.

### Hot keys and large indexes

Partitioning prevents one physical posting structure from being the only unit
of storage and service. Selective conjunctions and choosing a small anchor
posting list can reduce actual work. Replication can spread serving load.

But a fixed 256-way partition scheme only divides a growing load by a constant.
It does not prove unlimited scale, and object-ID prefixes alone do not guarantee
balanced load against chosen inputs. Adaptive partitioning, appropriate placement,
load control and useful query selectivity need explicit operating assumptions.
Pagination and returning only the first few hits are not solutions to the entire
hot-key problem.

The honest response to exhausted search is "these providers/regions were
searched within this budget," not "this mathematics does not exist."

## 9. Location and transport: no indispensable directory

Indexes and custodians must themselves be discoverable in the full architecture.
The present location implementation finds **index providers** through
domain-separated rendezvous keys, maintained advertisements and authenticated
peer connections. It does not yet implement generic unknown-custodian discovery
for arbitrary modules or receipts. The integrated acquisition path tries adopted
index contacts without assuming they also provide custody; separately configured
custodians can be used through lower-level interfaces. A future exact-object
custody locator must remain distinct from index-role rendezvous.

The resulting endpoint descriptor is still a hint. It might be stale, unreachable,
malicious or unable to supply the advertised object. A channel identity says
which key is at the other end; it does not say that its mathematics is correct
or that two different keys belong to independent operators.

The v5 source includes bounded Kademlia/libp2p location adapters and local
integration controls. This is more than an exact-ID dictionary, but not yet
evidence for worldwide bootstrap, adversarial routing resilience or every
network configuration. Bootstrapping needs initially reachable contacts; no
protocol discovers peers while possessing no communication path to them.

The current "reader" role suppresses some publication duties but still listens
and participates in routing. It is not yet the lightweight, non-serving client
role described as a deployment objective in section 2.

Under suitable membership, reachability, routing-table and honest-enough
maintenance assumptions, Kademlia-style routing has logarithmic expected
lookup behavior in peer count. This is a statement about exact-key routing,
not logarithmic semantic search, guaranteed availability or worst-case delay
under attacks and partitions.

All learned-address dials need the owner's egress policy. Otherwise a malicious
descriptor could redirect the client toward private/local services. The current
public profile is conservative: selected public numeric IPv4 endpoints and
ports, HTTPS under owner/system CA trust, and separately authenticated peer
channels for the location exchange. Channel identity does not automatically
bind the HTTPS operator to that same peer key. Redirects, executable handlers
and peer-selected verifier configurations are not accepted as convenient fallbacks.

DHT event counts are not wire-byte measurements. Handshakes, background
maintenance and framing consume additional resources. The resource model must
state what is measured, reserved or still unmetered.

## 10. Custody, retention and recovery

Someone must store the data that future agents need. Receipts can remove the
need to retrieve old theorem proof histories, but cannot reconstruct a lost
transparent definition, group opening or certificate from its hash.

Custody therefore distinguishes exact immutable content from claims about
validity and continued service. Current stores retain structurally checked
module material and receipt bytes. Custody alone is not acceptance. A stored
receipt must still pass the receiver's adopted verification route.

For the full architecture, custody agreements need an object set, retention
horizon, resource allowance and actual servicing/repair policy. A meaningful
availability set includes all selected interfaces and computational bodies
needed for the promised use, not only a top-level receipt. Maintaining objects
indefinitely without funded capacity is not an architectural guarantee.

For one object at a specified observation time, with \(r\) independent replica
unavailability events each of probability \(p\), simultaneous unavailability has
probability \(p^r\). This is not a lifetime permanent-loss bound or a guarantee
for the whole set of required objects. Independence is a hypothesis. Shared
operators, disks, regions, software and funding can correlate failures;
multiple peer IDs do not prove fault independence.

Repair must observe loss, acquire from a surviving copy, check exact content,
establish replacement custody and update advertisements. It must have capacity
before the last usable copy disappears. Erasure coding is a possible later
tradeoff, not an implemented rescue from total loss or a free repair mechanism.

Indexes and custodians should fail independently: an index can advertise an
object it does not store, and another provider can serve a retained snapshot.
Continuing a known snapshot and switching to a different snapshot are distinct
operations with distinct coverage. Neither is permission to reset the client's
overall budget.

Renewal, expiry and repair are operational state. They may be logged locally
for recovery and accountability; they do not require a global ledger of every
mathematical result. Immutable data and mutable service promises have different
lifecycles.

Index snapshots also consume storage. A portable cursor is usable only while
someone retains its exact snapshot; immutability does not imply perpetual
service. Snapshot leases, garbage collection and retained-cut replication still
need a complete operating policy. Maintaining a DHT hint is not repairing the
mathematical content to which it points.

### Sustainable service is part of availability

For each provider, query work, publication/indexing work, renewal and repair
must fit the resources the operator actually supplies. In one common work unit,
a necessary average-capacity condition has the form

\[
\lambda_q c_q+\lambda_u c_u+c_{\mathrm{maintenance}}<C_{\mathrm{service}}.
\]

Here \(\lambda\) denotes admitted operation rates and \(c\) their work costs;
maintenance is expressed per unit time. Storage and bandwidth need their own
constraints. Average spare capacity alone is not a latency guarantee: bursts,
scheduling, contention and capacity reserved for repair matter. Replication
can reduce read pressure only by paying additional storage, transfer and upkeep.

## 11. One complete example: discover, extend, and return

Consider a library of finite trees with leaves and binary nodes. `map f` changes
leaf values; `fold leaf node` interprets the tree in another mathematical domain.
A useful generic theorem is a fusion law: under explicit compatibility
conditions, interpreting and then transforming equals transforming the
interpretation itself.

This example exercises reusable mathematics rather than just moving files.
The complete candidate workflow is:

1. **A publishes a method.** A defines the tree datatype and operations, proves
   generic laws, and creates exact modules. Every new group/body is checked.
   A or a separately funded prover obtains the required real certificates.
2. **Custodians retain it.** Selected holders store the certificates, group
   records and bodies, with explicit retention limits. Indexes derive formal
   features from the offered interfaces.
3. **B searches independently.** B wants a related tree transformation without
   knowing A's new target module ID. It can query generic features, such as
   theorem kind and a foundation equality-result head, or exact symbols from
   a shared base module it already knows. Exact new-module symbol keys cannot
   be derived from display names alone: they include their owner's identity.
   Location finds index contacts; bounded search returns candidates and coverage.
4. **B acquires and verifies.** B recomputes selected features, verifies the
   chosen receipts, authenticates interfaces, and fetches necessary semantics.
   An invalid candidate is rejected; an exhausted budget is reported separately.
5. **B develops an extension.** In its live import session B authors an ordinary
   Lean proof of a map/fold or transport composition law. The result must use
   the imported method substantively and discharge its own hypotheses. No
   imported theorem proof history is required for the certified import route.
6. **B makes the result transferable.** It prepares the exact child and real
   parent premises, then follows an implemented certificate route. A future
   implemented delta route could supply bounded ordinary proof material instead;
   that option must not be pretended to exist now.
7. **C reuses B's result after A leaves.** An alternative index and surviving
   custodians provide the required objects. C independently verifies them and
   performs another warranted use through public interfaces.

The last step tests decentralization and reciprocal accumulation together.
It cannot be demonstrated merely by copying a file into C's private state or
giving C an acceptance flag created by B.

Publication itself spans separate state changes: retain content, update an
index, advertise service. It is not a globally atomic transaction. A crash can
leave accepted-but-unindexed or indexed-but-unavailable objects. Reconciliation
must expose those states rather than treating one successful advertisement as
completion of the whole publication cycle.

For a strict evaluator, replacing `fold (map f tree)` by the corresponding
fused fold can remove a materialized intermediate tree. Both can remain linear
in input size. This is an algorithmic argument about a specified evaluator,
not an exponential speedup, a claim about Lean's runtime, or proof of the
network's economic advantage. A strong local optimizer is allowed the same
fusion once it possesses the method.

## 12. What scalable verification and search can actually guarantee

Keep three sizes separate:

- \(G\): the global mathematical corpus.
- \(H\): ancestral theorem-proof witness material behind selected certificates.
- \(I,B,L\): selected interfaces, required computational bodies/semantics, and
  the new local proof/checking work.

The objective is to avoid mandatory work proportional to \(G\) for every query
and to \(H\) for every certified import. It is not to eliminate \(I,B,L\).

### A conditional no-proof-ancestry argument

Suppose the implementation verifies real selected certificates, authenticates
each installed interface/body, checks all new declarations, and never fetches
imported opaque theorem proofs. Its receiving-and-use work decomposes as

\[
T\ \leq\ T_{\mathrm{search/acquire}}
  +\sum_{j=1}^{n_v}V_j
  +T_{\mathrm{authenticate}}(I,B)
  +T_{\mathrm{check}}(L,I,B).
\]

Here \(n_v\) counts actual verification attempts, including failures and any
rechecks. Terms include wrapper/pinning work, demand rounds, parsing, rebuilding
environments and failed acquisition attempts in their appropriate categories.
Certificate production is a separate cost, not hidden in the receiver bound.

There is no compulsory summand proportional to \(H\): those theorem-proof bytes
have no entry point in this import algorithm. If extra ancestral proofs are
added while the selected interfaces, semantics and certificate profile remain
fixed, the receiver need not inspect them.

This is an architectural cost decomposition under explicit assumptions, not
a measured timing formula. Type conversion can be expensive; demanded semantics
can grow; the number of selected owners can grow. Uniformly bounded per-step
terms would give linear total receiving work over a sequence of extensions,
but the uniform bounds must be justified, not assumed for all mathematics.

### Representation can defeat an otherwise good design

Let \(t_0=a\) and \(t_{n+1}=f(t_n,t_n)\). A shared syntax graph needs only
\(O(n)\) distinct nodes, but its expanded tree has \(\Theta(2^n)\) occurrences.
This can inflate an interface even when no ancestral proof is downloaded.

The current codec still uses bounded expression trees in important paths.
Its caps provide refusal behavior, not a solution to this representation cost.
A proposed canonical semantic DAG preserves shared syntax through commitment,
transfer, parsing, correspondence and indexing. Merely compressing wire bytes
and expanding them again before checking does not solve the problem. This
successor representation remains design work, with explicit identity/version
migration and correspondence obligations.

### Search locality is not universal cheap search

For a selective feature conjunction, work can depend on a relevant posting
region and the returned answers rather than the entire corpus. But if a query
matches everything, enumerating all answers already costs at least their output
size. Even a zero-result intersection can be expensive without useful selectivity.

Finite query budgets provide bounded participation and honest incompleteness.
They do not prove a relevant result will be found inside the budget. Large-scale
claims need routing assumptions, feature selectivity, load placement, maintenance
capacity and actual implementation costs in addition to the local safety bounds.

For a simple coverage calculation, suppose \(n\) providers advertise a route,
\(r\) can help, and the client samples \(b\leq n\) uniformly without replacement.
Then

\[
\Pr(\text{find a helpful provider})
=1-\frac{\binom{n-r}{b}}{\binom n b}
\leq \min(1,br/n).
\]

Even ideal uniform sampling cannot give constant recall with a fixed budget
when the useful fraction tends to zero. Actual Kademlia selection is not
guaranteed to be uniform; an eclipse attack can be worse.

A useful sufficient assumption is stronger: after every previous all-failure
history, the next funded attempt has conditional success probability at least
\(p>0\). Multiplying conditional failure bounds gives success probability at
least \(1-(1-p)^b\) over \(b\) attempts. Independence is not required if that
conditional bound really holds. Useful scope advertisements, selective routing
and retained replicas are ways to try to sustain \(p\); the implementation does
not presently establish it universally. Merely obtaining a peer ID is not
"success" in this model.

## 13. What counts as growth?

The philosophical position is deliberately modest: **formal validity is
independent of intention; practical mathematical knowledge is warranted
capability available to a bounded reasoner**.

The unrestricted logical consequences of a fixed foundation do not expand each
time someone publishes a theorem already derivable from it. What can expand
is our ability to obtain and apply those consequences with finite resources.
Making a difficult theorem reliably accessible is real progress in that sense.

Let

\[
\operatorname{Reach}(a,K,b,q)
\]

mean that specified agent/method \(a\), using accessible warranted knowledge
\(K\), achieves a formally accepted outcome \(q\) within resource budget \(b\).
This is not an oracle for the best possible proof search. It describes an
identified method or observed run.

Growth may mean that more outcomes become reachable at the same budget, or
that existing outcomes become reachable with less cost. A finite evaluation
family can expose this change. Its choice belongs to evaluation, not a global
task list or a human-intention field in mathematical acceptance.

A generic method can support many distinct instances. But theorem counts,
dependency edges and renamed variants alone do not demonstrate new capability.
Useful comparisons identify the actual premises discharged, transformation
enabled, costs paid and available baseline methods.

One helpful analytical model is a **resource-constrained directed hypergraph**:
a reuse step connects a set of prerequisites to a newly warranted capability,
with acquisition/checking/application costs. A hyperedge, unlike an ordinary
edge, can require several inputs together. Two lemmas can be valuable jointly
while neither is useful alone. Consequently a greedy ranking of individual
theorems does not automatically have the approximation guarantees that require
diminishing returns. This model explains complementarity; it is not an oracle
for mathematical value or a mandated distributed scheduling mechanism.

### Duplicate and low-value material

Exact content addressing identifies and permits coalescing exact duplicates;
deliberate replicas still exist. Formal syntax features,
known equivalence/transport proofs, usage signals and learned ranking can help
organize the rest. Arbitrary mathematical equivalence is not generally decidable,
so a universal perfect "same mathematics" filter is not assumed.

The network can preserve validity while allowing local diversity of usefulness
judgments. One index may specialize in algebra; another in efficient decision
procedures. A niche result need not be globally popular to be worth retaining.
Usage frequency is a fallible signal for ranking, replication or certification,
not a proof of truth, novelty, independent demand or future usefulness.

Nothing in the protocol guarantees exponential discoveries. It seeks favorable
conditions for compounding reuse while bounding unhelpful work. Claims about
sustained rates need additional models of agent capability, demand and service
resources; a growing theorem counter cannot supply those models.

## 14. A defensible full-cost growth argument

Compare the network with an **equally optimized local library**: same initial
mathematics, checker, representation, caches, optimizer and application requests.
The baseline can prove a generic method once and cache it; it is not forced to
rediscover the theorem for every instance. A remote genuinely new discovery is
not donated to that independent baseline for free.

It is helpful to distinguish three routes: independent local development,
ordinary shared proof packages with local checking, and receipt-backed sharing.
Otherwise savings from sharing can be incorrectly attributed to cryptography.

For recipient library \(i\), let \(D_i\) be the incremental baseline cost and
\(R_i\) its network reuse cost. Let \(F\) contain additional fixed creation,
certification and publication costs; \(M\) contains service, retention, repair,
failed search and failed production costs over a stated horizon. Subtract costs
common to both alternatives before comparing.

CPU seconds, bytes and storage duration are different units. Either report a
resource vector/Pareto comparison, or adopt explicit nonnegative prices \(w\):

\[
\sum_i w\!\cdot(D_i-R_i)>w\!\cdot(F+M).
\]

This inequality is the break-even condition, not evidence that demand exists.
For a simple sufficient region, suppose the avoided baseline cost is at least
\(d\) per distinct recipient library, reuse plus variable service costs at most
\(r+m\), and additional fixed cost at most \(f\), all in one declared valuation.
If \(d>r+m\), then

\[
N>\frac{f}{d-r-m}
\]

suffices. The proof is addition of those per-library inequalities. The difficult
practical work is justifying the inputs and ensuring service capacity, not
running a planet-sized experiment to demonstrate the algebra.

Peak memory is usually a capacity constraint, not a bill added across sequential
requests. Payments between peers should not double-count physical resource
consumption. A warm-cache recipient is not another full cold-validation saving.
Bounds, measurements and forecasts must be labeled separately.

### Two useful optional policies with narrow theorems

**Bounded exploration.** An agent may reserve fraction \(1-\eta\) of an isolated,
preemptible processor for its unchanged local method, and \(\eta\) for
network-assisted alternatives. A local computation needing \(C\) processor
seconds then finishes within \(C/(1-\eta)\) in that model even if exploration
fails. At \(\eta=0.1\), this is approximately 11.1% dilation. Memory, I/O,
provider costs and scheduling interference are not covered by that CPU argument.

**Rent versus certify.** For one fixed target, assume each additional direct-check
cost \(\delta_i\geq0\) is known before route choice, and a successful seal can
be bought for known total incremental cost \(S\). Accumulate direct-check costs
while their next sum stays at most \(S\); otherwise buy before that request.
The total incremental cost is at most twice
\(\min(S,\sum_i\delta_i)\): if no seal is bought the rule is optimal; if one
is bought, prior rental is at most \(S\), so total is at most \(2S\).

These are conditional owner strategies, not implemented global policies. A
failed or unavailable seal, unknown costs, correlated cache changes or many
operators buying redundant seals can invalidate the second model. Neither
theorem shows that the chosen mathematics itself is useful.

## 15. Security, operational reliability and evolution

The design assumes mostly cooperative participants while refusing to build on
false or malicious mathematical claims. Separate protections address different
failures:

| Failure | Required response |
|---|---|
| False theorem or forged certificate | Independent adopted verification; no imported authority from metadata |
| Altered definition/group or wrong universe binding | Exact commitments and semantic correspondence checks |
| Missing material or exhausted checking budget | Explicit incomplete/demand outcome, not acceptance or a claim of falsehood |
| Malicious index omission or stale advertisement | Explicit coverage, alternative providers and bounded retry choices; no global no-match inference |
| Routing eclipse, Sybil identities or unavailable peers | Diversity/admission/routing defenses and availability assumptions; identities alone do not establish independence |
| Resource-exhausting input | Aggregate limits before expansion where possible, accountable attempts, process containment |
| Malicious source, tactic or parser exploit | A genuine isolation/security design; proof validity alone does not sandbox execution |
| Crash or ambiguous process completion | Preserve reservations/evidence, refuse uncertain promotion, explicit recovery |
| Unsound checker/image discovered later | Local profile revocation and revalidation; immutable storage does not mean eternal acceptance |

### One operation must have one real budget

A search changing providers, a demand for another body, or a failed proof stage
must not create fresh unbounded resources implicitly. Owner-created deadlines,
attempt limits and byte/CPU reservations follow the workflow. Unknown outcomes
retain conservative charges instead of disappearing from accounting.

Preparation and production can have distinct explicitly funded allowances;
they are not free continuation of a search. All costs still belong in a
whole-workflow comparison. Resource refusal is an ordinary outcome, not a reason
to bypass mathematical checks.

Current Windows Jobs supervise resources and process closure. They do **not**
isolate filesystem/network access or protect an owner process from malicious
Python in that process. Byte pins do not prove hermetic toolchains, safe DLL
loading or a correct OS. Public hostile-input deployment needs a stronger,
reviewed isolation boundary.

### Recovery and availability state

Immutable content can be checked after restart. Persisted "accepted" flags do
not recreate live verifier handles. Durable reservations and partial proof stages
aid recovery but must be reconciled with actual process outcomes and exact inputs.
Atomicity across network transfer, disk custody and live session mutation is not
assumed: a failed call may leave useful bytes on disk without creating authority.

### Updates without a central mathematical authority

Every operator adopts a supported checking profile and update policy. Release
signatures can authenticate software publishers; they cannot prove checker
correctness. A replacement image is not trusted merely because a peer advertises
it as newer. Old/new certificate formats require explicit compatibility rules.

Content identity can sometimes remain stable across implementation repairs if
its mathematical semantics are unchanged; changing semantics or representation
may require new identities. In either case, acceptance under a revoked profile
must not be silently inherited. Different policies can coexist, with boundaries
visible to consumers.

Political attribution is secondary. Operational identities remain useful for
authenticated connections, updates, retention promises and abuse control, but
mathematical acceptance does not depend on an author's fame or vote count.

### Why no blockchain consensus is required

Immutable compatible contributions need no total publication order. Nodes can
accumulate a set of independently checked modules and resolve exact dependencies.
Conditional eventual dissemination means that connected, adequately resourced
participants following the same policies can learn the same retained objects;
it does not mean simultaneous global state or identical local acceptance under
different budgets.

A ledger might later help with payments, scarce-resource commitments or an
operator's audit trail. Those would be separate service mechanisms. Consensus
does not prove mathematical validity, semantic relevance, data availability or
useful growth, and should not be inserted into the core merely for resemblance
to a blockchain.

## 16. What exists and what is still missing

The following is a map of the last audited development checkpoint, not a claim
that a later background process succeeded. Earlier source-plan documents often
retain prospective or historical wording; exact evidence and current selections
take precedence over those old status paragraphs.

| Area | Present candidate and evidence | Still required for the full architecture |
|---|---|---|
| Module semantics | Immutable module/group/body model; conditional checking and selected native controls; profile2 relation and real prover/receiver sources | Complete scoped checker correspondence/security case and genuine certified modular end-to-end use |
| Receipt production | Guest/host builds, execution capsule and retained genuine proof-prefix work; bounded staged producer | Final-result audit and fresh positive v5 receipt admission, followed by certified child/return integration |
| Ordinary authoring | Imported-context frontend compiled/linked; five conditional native controls; worker20 and preparation9 mock-only groups audited | Real receipt-backed authoring through the public controller, actual worker/native process envelope and genuine parent-aware child path |
| Discovery | Formal module-export features, committed snapshots, compact summaries, interval pages, positive candidates and bounded public/local controls | Broad useful retrieval, truthful corpus-coverage claims where offered, adaptive/load-aware huge-network operation |
| Location and acquisition | Bounded maintained index-role location; local location evidence used old-policy metadata, not current-profile mathematical admission | Generic unknown module/receipt custodian discovery; lightweight clients; public bootstrap/connectivity, adversarial routing and sustained maintenance |
| Custody | Structural stores and exact object/receipt acquisition; earlier v4 provider-loss evidence remains a baseline | Integrated v5 redundant service, content repair/retention funding, snapshot leases/GC, publication reconciliation and provider-loss continuation |
| Economical proof sharing | Receipt path implemented in components; selective-sealing argument and native-delta design | Integrated v5 delta verifier/transport and carefully justified sealing interoperability |
| Compact semantics | Canonical semantic-DAG proposal; current tree expansion is bounded/refusable | Implementation, migration and correctness/cost evidence across the full data path |
| Growth | Parametric fold/fusion workload and full-cost conditional models | Supported positive-benefit region against equally optimized comparators, with usable reciprocal applications and all service/failure costs |
| Release | Local Git checkpointing and retained evidence; frozen v4 unaffected | Reproducible self-contained supported distribution, secure updates/isolation, independent security review, deployment evidence and license decision |

These are central unfinished obligations, not peripheral polish. A certificate
alone would not close discovery or growth. A larger local peer simulation would
not establish independent operation. Storage compression would not establish
more attainable mathematics. Conversely, the lack of a planet-sized test does
not prevent deriving conditional bounds or testing the specific assumptions
that matter.

The local Git repository preserves selected source and documentation; ignored
runtime installations, proof artifacts and experiment evidence remain essential
separate data. A clone alone is not yet a reproducible self-contained release.

The integrated release target is:

> A fresh independent agent discovers an unfamiliar reusable formal method,
> acquires and verifies only the required material, produces a substantive
> extension through ordinary supported interfaces, and makes that extension
> discoverable and usable by another fresh agent after the original providers
> disappear—with a justified trust case and full resource accounting.

The project should be judged against that complete cycle and its six obligations:
validity, scalable discovery, availability, useful growth, public operability
and final release. None is waived by a version label.

## 17. Source map and further reading

### Project sources

- [Goal and preserved requirements](../GOAL.md) and
  [v5 plan/release obligations](../research/cycles/v5-2026-10-07/PLAN.md).
- [Module relation](../research/cycles/v5-2026-10-07/MODULE-RELATION.md),
  [current receipt format](../software/v5/modules/receipt/README.md) and
  [public admission boundary](../software/v5/admission/README.md).
- [Verified-import/authoring contract](../research/cycles/v5-2026-10-07/VERIFIED-IMPORT-AUTHORING-CONTRACT.md),
  [authoring API](../software/v5/authoring/API.md),
  [preparation API](../software/v5/preparation/API.md) and
  [producer API](../software/v5/production/API.md).
- [Discovery contract](../research/cycles/v5-2026-10-07/DISCOVERY-CONTRACT.md),
  [search API](../software/v5/transport/SEARCH-API.md) and
  [evolving integration record](../research/cycles/v5-2026-10-07/DISCOVERY-INTEGRATION.md).
- [Growth model and workload](../research/cycles/v5-2026-10-07/GROWTH-WORKLOAD.md),
  [bounded native-delta design](../research/cycles/v5-2026-10-07/DELTA-FRONTIER-NATIVE-SEAM.md) and
  [compact semantic DAG proposal](../research/cycles/v5-2026-10-07/COMPACT-SEMANTIC-DAG.md).
- [Independent assurance record](../research/cycles/v5-2026-10-07/ASSURANCE.md),
  [decision ledger](../research/cycles/v5-2026-10-07/DECISIONS.md) and
  [prior pause/background-run handoff](../research/cycles/v5-2026-10-07/PAUSE-HANDOFF.md).

### Related foundations, not substitutes for our assurance work

- [Lean's proof-validation guidance](https://lean-lang.org/doc/reference/latest/ValidatingProofs/):
  why proof checking and hostile-source execution are different concerns.
- [Lean4Lean](https://arxiv.org/abs/2403.14064): relevant work on validating the
  metatheory of a Lean checker; not a proof of our modified implementation.
- [Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf):
  exact-key decentralized routing under its model, not semantic search.
- [Authenticated data structures](https://cs.brown.edu/cgc/stms/papers/authDataStr.pdf):
  evidence about committed data, not proof that a corpus is globally complete.

These references explain reusable ideas. No new upstream security audit or
literature survey was performed for this guide. Project-specific trust and
implementation claims come from the linked source and evidence records.

## Bottom line

The candidate is a decentralized, proof-carrying mathematical library whose
agents remain independent. Certificates separate warranted reuse from proof
ancestry; authenticated interfaces preserve meaning; replaceable indexes make
discovery possible; custody keeps required bytes available; and explicit
resource models determine whether sharing really pays.

The hard problem is making those mechanisms work **together**, affordably and
under stated trust and availability assumptions. That is the architecture's
promise to establish—not a promise of perfect global knowledge, free checking
or inevitable exponential growth.
