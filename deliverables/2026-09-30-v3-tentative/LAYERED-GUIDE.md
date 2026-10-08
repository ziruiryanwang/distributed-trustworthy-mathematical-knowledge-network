# Tentative v3: a mathematics commons, layer by layer

Layered guide for the September 30, 01:00 Chicago tentative handoff. The
[support report](RESULTS.md) identifies the exact integration gates that passed.
The broader goal remains active. No second host, public deployment or license
has been selected.

## The idea in one paragraph

Each participant keeps only the mathematics and search information it chooses
to keep. A local agent can discover a formal theorem, acquire its exact bytes,
check a certificate under an explicitly adopted checking policy, and use the
theorem's formal interface in a new Lean proof. The resulting contribution can
be certified and offered back. Nobody must download all mathematics, read all
ancestor proofs, follow a shared research agenda or agree on human intention.

```text
ordinary Lean contribution -> certified bundle -> discoverable offer
                                      ^                  |
                                      |                  v
                             new proof using it <- acquire and check
```

This is not a blockchain with a mandatory ledger of every theorem. The content
graph can grow without global ordering or consensus on a latest state. Different
nodes can know different things. Index hints can be stale or incomplete; proof
acceptance must remain separate from those hints.

## Layer 1: the mathematical acceptance boundary

A theorem has a formal statement and a proof. In this experimental lane, a
pinned checker image checks a restricted proof relation derived from Lean
exports. A cryptographic receipt attests that this exact checker ran and its
claimed obligations were discharged. A receiver checks the receipt and the
statement binding. It does not trust the sender's reputation or a JSON field
saying "verified".

The implemented receipt backend is the pinned RISC Zero zkVM/recursive
Succinct-receipt path. A zkVM is a virtual machine whose execution can be
certified cryptographically. This backend choice does not discharge the
checker-correspondence or recursive-security assumptions discussed below.

The compact bundle contains four files:

| File | Meaning |
|---|---|
| capsule.json | The selected formal interface: what can be used |
| journal.bin | The complete finite collection's committed claim |
| receipt.bin | The cryptographic evidence for the adopted checker image |
| bundle.json | Exact file hashes and the selected collection member |

Selecting A from an A/B collection requires A's capsule, the full A/B journal
and the genuine full receipt. It does not require B's capsule or A's proof
ancestors. A child receipt recursively discharges its immediate certified
parent obligation before downstream acceptance. An unresolved proof checkpoint
is not a final theorem certificate.

The claim is conditional. If the adopted checker implements the intended
relation, the foundations are appropriate, hashes bind the intended bytes and
the recursive receipt construction/verifier is sound, acceptance establishes
the selected formal judgement. Cryptography proves execution of a program;
it does not prove that the program is a correct implementation of all Lean.
General Lean correspondence and construction-specific adaptive recursive
security remain production-assurance work, not completed formal proofs here.

Current supported mathematics is fixed-support Prop interfaces with same-image
recursion. `Prop` is Lean's sort of propositions; `same-image` means every
recursive certificate uses the same adopted checker executable identity.
The small `journal.bin` is a certificate's public claim, not a global ledger
of mathematics. General new definitions, arbitrary mathlib and all Lean features
are not supported by this certified profile. The older native v2 lane has a
different checking/replay model; do not silently mix their trust claims.

For example, suppose a certified parent says that a function with a left
inverse is injective. A left inverse undoes the function; injective means
distinct inputs cannot have the same output. An agent can apply that parent
twice to prove a theorem about a composition. Its formal interface is the
exact declaration name, universe parameters and quantified Lean type, not an
English paraphrase. The new certificate must establish the new proof and the
validity of the parents it relied on. This is assumption discharge. A later
receiver checks the final discharged receipt rather than repeating the entire
parent proof chain. The current child is this concrete composition example.

## Layer 2: exact content and custody

Content hashes identify exact objects. Acquisition checks the offered file
lengths/hashes and the discovery-key binding, retaining partial or failed data
in charged quarantine. Only complete successful transfer and structural
binding create visible custody. Custody means "I have these bytes," not "the
theorem is mathematically accepted." A separate real receiver check supplies
the latter boundary.

Having another holder can preserve access after the original service stops.
It is not a guarantee that every theorem will be retained forever. Retention,
leases, replication and maintenance consume resources; somebody must actually
operate holders. There is no magic storage implied by decentralization.

## Layer 3: bounded discovery, not a global search oracle

The local theorem index uses SQLite, typed keys and indexed postings. Exact interfaces,
formal type grouping, symbols and a bounded conclusion-shape feature can help
agents find candidates without opening every proof or scanning unrelated rows.
The shape feature is syntactic and bounded, not a decision procedure for
mathematical equivalence. Same-shape rubbish can still crowd out a useful result.

The routed extension separates two roles: an index keeps small advertisements;
a holder keeps the actual bundle. The author announces selected derived keys
through the public protocol. A fresh client starts with a few entry contacts,
follows admitted, strictly closer referrals and asks discovered rendezvous
indexes for holder hints. It then contacts a selected holder directly.

Think of the index as a card catalogue and the holder as the shelf containing
the object. Here a rendezvous index is a key-selected meeting point for those
cards, not a central catalogue of everything. A DHT (distributed hash table)
is a possible way to route among such indexes. V3 implements bounded routed
mechanics, not a fully maintained huge DHT or a blockchain consensus protocol.

One caller budget covers the whole operation. Failed attempts are charged;
timeouts and response limits do not reset at each hop. Address policy is
explicit, with literal IPv4 and pinned TLS. Default referral following is off.
TLS identity authenticates an endpoint, not a mathematician or the truth of
its results. Political attribution is not part of mathematical acceptance.

The initial profile has finite local tables, unsplit key partitions, explicit
leases and no automatic overlay repair. It is cooperative, not permissionless
internet availability. Malicious advertisements can waste bounded work or
destroy recall, but cannot authorize a false theorem by themselves. Any actual
small-topology pass tests mechanics, not logarithmic lookup in a huge real DHT.

"No result within this budget" never means "no such theorem exists." Global
freshness and universal cheap complete search are not promised under partitions,
hot keys, churn or finite local storage.

## Layer 4: independent agents and the contribution loop

Agent research strategy stays outside the core. An agent can use documentation,
skills or its own policy to decide what to investigate and when to search.
There is no required human-language/formal-math translation stage, root goal,
global unsolved-task list or human-intention acceptance criterion.

The contributor's prepare command checks selected parent receipts, imports their
body-free formal interfaces, elaborates ordinary Lean source and freshly checks
the exported root in the declared support context. It saves its own coherent
execution snapshot. READY means prepared, not certified. Advance operates on
that same saved state and original budget/deadline to create a final receipt.
No research checkpoint may be substituted to pretend public production passed.

The actual public producer now completed one chain: a TLS-acquired parent,
fresh verification, one packaged public prepare and all 122 stages of its own
public advance, including final verification. The child theorem proves that a
composition of maps with left inverses is injective; its Lean proof uses the
parent injectivity theorem twice. It is a real checked dependency, not merely
a citation in metadata. Parent proof histories were not preparation inputs.
The separate return then actually passed its independent audit: B supplied the
child to A and stopped; A freshly checked it and served that existing custody
to C; both services were stopped before C's fresh check. This needs no new
proof to make a replica useful. The support report records exact bytes and
costs. Existing passed work is reused as evidence for unchanged
components; expensive proofs are not repeated just to create network fixtures.

## Layer 5: useful growth and economics

Validity is not usefulness. Ten duplicate proofs do not automatically add ten
reusable capabilities. A theorem can be formally valid and still be trivial,
hard to discover, expensive to certify or unnecessary for an agent's next proof.
Heuristic ranking and observed reuse may help; they never replace Layer1.

In a fixed foundation, adding theorems does not enlarge its logical deductive
closure: they were consequences already. Practical growth means making useful
consequences accessible at lower resource cost and enabling independently
completed downstream work. Count those outcomes and their costs, not merely
files, advertisements, proof steps or popularity.

Certificates shift work toward producers. The completed AB campaign spent
about 69,638.921875 known CPU seconds, including retained earlier failed work.
Its cold verifier was history-independent, but that does not establish cheap
production or positive useful-growth advantage. The installed/network/public
workflow costs must be reported separately. This new child preparation and
production alone cost 42,781.21875 known CPU seconds. Warm local native caches are a
legitimate baseline; do not charge ancestral replay for every cached use.

For matched cold consumers, benefit requires their total saved search,
transfer, checking and downstream-use cost to exceed the extra production,
setup, failure, replication and maintenance cost. This is a falsifiable
amortization condition, not a promise of exponential growth. The release must
say explicitly if that empirical advantage remains unestablished.

## What mandatory costs were removed—and what remains unqualified

The mandatory work is local and selected: bounded metadata queries/referrals,
selected four-file bundles, and their final receipt checks. Corpus size and
transitive proof history are not mandatory operation inputs. A finite
collection journal, interface size and computation explicitly requested by
a proof still cost work. There is no assertion that all mathematics has
constant-size interfaces or that arbitrary theorem search is constant-time.

The central remaining assurance/economic gaps are broad faithful semantics,
affordable producer throughput, useful retrieval under saturation, viable
placement/maintenance under churn, and matched evidence of beneficial useful
accumulation. License, external publication and independently hosted testing
are separate handoff limits. The intended tentative v3 is a bounded experimental
release; its support report determines which paths are actually qualified.
It is not completion of the whole commons vision.
