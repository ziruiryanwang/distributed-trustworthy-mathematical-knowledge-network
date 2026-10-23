# Trust boundaries and lower-cost verification architecture

Author: `/root/storage_outcome_audit`, 2026-10-22.
Status: source/theory audit for the whole-architecture reassessment. This is
not implementation selection, runtime qualification, a new trust adoption or
release acceptance. No test, build, snapshot or certificate was run for it.

## Decision in one paragraph

Retain the independent mathematical checker and exact module identities, but
do not require a cryptographic certificate for every new contribution. Treat
native proof witnesses, locally checked warrants and transferable validity
certificates as different evidence routes through one mathematical dependency
DAG. Check only demanded, previously ungrounded deltas; reuse established local
warrants; selectively certify reusable frontiers for cold consumers. Preserve
an explicit **ancestry-free receiving profile**: when no acceptable certified
or already checked frontier exists, return `NEED_CERTIFICATE` or a bounded
unavailability result, rather than secretly downloading the proof history.
This is an architecture recommendation, not a claim that every arbitrary new
result already has cheap cold acceptance.

## The central distinction

An advertised type is not a proved theorem. Consider an adversary advertising
`h : False`. A consumer can check that `False.elim h : P` has the expected type
in the environment containing `h`; this proves only the conditional judgment

```text
h : False |- False.elim h : P.
```

It does not establish `|- P`. A content hash, a well-formed declaration, a
signature, a Merkle opening, a reputation score or a successful downstream
type-check cannot discharge the premise `h`. Proof irrelevance makes proof
identities irrelevant to many downstream uses; it does not establish that an
inhabitant of the proposition exists.

Every accepted premise therefore needs a grounding route under the consumer's
adopted policy. The useful design question is **where and how often that
grounding is paid for**, not whether a downstream checker can simply omit it.

There are two different requirements:

- No operation scans the entire mathematical corpus or all historical proofs.
- Every arbitrary, previously unseen, uncertified contribution is cheap for a
  completely cold consumer.

The first is achievable through demand locality and certified cuts. The second
does not follow from the first and is not supplied by ordinary modular
type-checking. We do not claim a general impossibility theorem or quantitative
lower bound for every conceivable proof system. We identify the missing
evidence in this protocol.

## Exact object and authority separation

| Object | What it establishes | What it does not establish |
|---|---|---|
| Semantic module descriptor and ModuleID | Exact public declarations, types, universes, kinds, relevant bodies/commitments and group structure under a policy | That any theorem proof exists |
| Native witness and exact parent warrants | Data from which the checker can establish a conditional valid extension | That arbitrary advertised parents are valid |
| Locally checked warrant | The local checker established the result from currently accepted premises | A transferable proof for an unrelated cold node |
| Cryptographic validity certificate | Under its cryptographic/checker assumptions, the committed relation accepted with all parent assumptions discharged | Correctness of a buggy relation, data availability, usefulness or optimality |
| Snapshot manifest / content-store root | Integrity and membership relative to a committed finite set | Mathematical validity of its members |
| Operational report, signature or provider identity | Origin, execution accounting or authentication according to its mechanism | Mathematical truth without an explicitly adopted attestation policy |

Semantic identity can be proof-independent while warrant identity is not.
Different valid proofs and parent choices may justify the same public module.
Do not collapse exact parent journals into ModuleIDs when constructing or
checking an existing recursive certificate. Conversely, do not force political
attribution or proof-discovery provenance into the mathematical statement.

## A compositional acceptance argument

Fix a semantic policy `P` and foundation `F`. A policy includes the intended
logic and permitted axioms, module/namespace/group interpretation, supported
declaration semantics, and the adopted checking/verification stack. A local
deployment also needs a current authorization state for that stack. An
identifier supplied by a peer does not adopt its own policy.

Let `B` be a finite set of presently grounded boundary warrants. Each is
justified by the exact adopted foundation, an earlier local checked result
whose authority remains valid, or an actually verified transferable
certificate. Let `D` be a finite acyclic set of new delta-witnesses. For each
`d` in `D`, suppose:

1. Its parent references identify exact warrants in `B` or earlier `D`.
2. Descriptor openings, canonical correspondence and public output binding
   are checked, not accepted from sender flags.
3. The union of imported declarations is a compatible environment under `P`:
   names do not shadow the foundation, common identities have identical
   semantics, universes and reduction metadata are preserved, and atomic
   inductive/recursive groups are respected.
4. The checker validates every new local declaration against precisely that
   environment, forbids unapproved axioms, and treats missing needed semantics
   as a demand or refusal, never a successful conversion or a new axiom.
5. The checker and its representation/import rules satisfy their claimed
   semantic soundness property.

Then every accepted delta in `D` is warranted under `F,P`. The argument is
induction over a topological ordering: boundary warrants establish the base;
compatibility and conditional checking establish each extension. This is
the same logical argument whether a particular boundary is established
locally or by an adopted certificate. It is not a machine-checked theorem
about the complete current implementation.

Strict ranks can witness acyclicity but are not themselves validity proofs.
The current certificate construction additionally needs a suitable
**adaptive, branching, multi-claim recursive soundness** assumption, as well
as collision-resistant binding, verifier/image correctness and the semantic
checker argument. A simple rank induction does not prove that an adversary
cannot forge the cryptographic base of the induction. A sequential IVC result
cannot automatically be cited as a proof for arbitrary independent joins.

### Cost consequence, with its limits

For a selected dependency DAG above established cut `B`, an ideal memoized
native traversal costs

```text
acquisition and parsing of selected new witnesses
+ sum of conditional-check costs for distinct new deltas
+ selected interface/body authentication and computation
+ boundary-certificate verification costs not already validly cached.
```

It need not repeat a shared ancestor once per downstream path. This avoids
tree expansion of a shared DAG; it is not a claim that each delta has constant
checking cost. Type conversion may be expensive, statements and needed
transparent definitions may be large, and a restart-based demand checker can
redo earlier work. The present implementation must be judged by its actual
restart/cache behavior, not this ideal accounting expression.

For a cold receiver using a valid certificate for the selected cut, the
ancestral theorem proof terms behind that cut are absent from its work. It
still pays for the certificate, selected public interfaces, relevant semantic
data and new proof checking. If there is no valid cut, an optional native route
may have to ground an uncached dependency closure. This is **not** the user's
ancestry-free receiving guarantee and must be visibly a different choice.

No global environment root, total-order ledger or consensus over all modules
is required by this argument. Compatible independently checked modules can
coexist. Search/custody operators can be untrusted with respect to truth while
still being able to omit data, waste bounded resources or impair availability.

## Checked caches and snapshots

A verified cache is a major low-cost tool, but its authority is local state,
not an untrusted serialized Boolean named `verified`.

A reusable cache entry must bind at least the exact semantic conclusion and
evidence route, foundation/policy, checker or verifier adoption, and relevant
parent authority. It must be invalidated or refused when its trust domain is
withdrawn, its supporting bytes are replaced, or policy compatibility changes.
The exact implementation may use an owner-scoped handle, immutable generation
and denial checks instead of revalidating every ancestor on every lookup.
Persisted reuse additionally needs crash/recovery and tamper assumptions; it
cannot be implemented by trusting a downloaded database's acceptance column.

A checked snapshot is a collection of such grounded conclusions plus their
exact semantic metadata. It can save a node's repeated start-up/checking work.
A fresh unrelated node has four honest choices for that snapshot:

1. Check its relevant proof witnesses itself.
2. Verify an adopted validity certificate covering the selected snapshot members.
3. Already possess matching locally grounded warrants.
4. Explicitly trust a signer/operator/hardware attestation as a different policy.

A hash or digital signature alone is not option 2. A snapshot from a trusted
software distribution may be useful operationally, but that is a deployment
trust decision, not independent mathematical verification from cryptography.
Current source already contains owner-scoped caches and trust withdrawal;
this audit does **not** report their absence. Cross-process persistent checked
snapshots would need their own scoped design before being treated as shipped.

## Lower-cost evidence routes

| Route | Real opportunity | Required boundary / limitation |
|---|---|---|
| Compact ordinary proof terms and DAG sharing | Replace redundant construction history with a short mathematical derivation; share subterms and established lemmas | A short term referencing ungrounded lemmas is still conditional; compressed input must have bounded decoding |
| Better abstractions and theorem transport | One parametric proof supports many instances; proof discovery need not be repeated | Its hypotheses and exact types still need checking; representation reduction is not by itself net useful growth |
| Proof-producing tactics / verified reflection | Expensive search finds an answer; a small certificate or proved decision procedure validates it | The proof of the procedure and its imported premises must be grounded; evaluation cost and native-evaluation trust must be explicit |
| Specialized mathematical certificates | SAT/unsatisfiability traces, arithmetic witnesses or algebraic identities may be much cheaper to check than to find | Each certificate format has a precise soundness theorem and domain; it is not automatically a universal Lean module certificate |
| Local checked cache / native mixed DAG | Amortize repeated checks and avoid certifying low-demand contributions | Cold external nodes do not inherit this local authority for free |
| Selective generic zkVM certificates | A third party can pay once to establish a reusable cut for many cold receivers | Potentially high proving cost; correct relation/public binding; recursive assumptions and verifier implementation |
| Specialized proof-system/checker arithmetization | Remove generic-machine overhead for a stable validation relation | Significant engineering and assurance cost; no claimed advantage until bounded cost and trust arguments exist |
| Trusted checkpoint, quorum or TEE | Cheap consumer acceptance under chosen attestation assumptions | Changes the trust policy; signatures are not mathematical proofs and peer count is not operator independence |
| Optimistic/fraud-proof acceptance | Avoid up-front proving when watcher coverage and disputes are credible | Requires data availability, a capable honest watcher, a challenge/adjudication model and a finality policy; not the same immediate assurance |

These routes are complements, not exclusive brands. In particular, succinct
cryptography is not the only kind of succinct mathematical evidence. A new
short proof can replace a long historical derivation; the protocol should
permit a different witness for the same public module when its exact semantic
dependencies and policy allow it. It must not require that the witness reproduce
the producer's actual discovery history.

Reflection must not be described as free computation. A proved evaluator can
reduce checker work relative to an enormous expanded proof, but some evaluation
still happens. An unchecked external answer or trusted-native evaluation mode
requires its own soundness/trust accounting.

### Optimistic and attestation alternatives in more detail

Accepting first and challenging later cannot supply the same unconditional
local guarantee as immediate checked proof. In the `h : False` example, every
descendant remains conditional on the absence of an undetected invalid premise.
If fraud is discovered, downstream warrants need invalidation; irreversible
external reliance is not undone by changing a database flag.

An interactive execution-dispute protocol can make a final disputed transition
cheap to adjudicate. Someone must still have the data, detect the bad claim,
participate before deadlines and reach an available adjudicator. A decentralized
network has no automatic common challenge window or universally observed
finalization event. Such a lane can be useful under explicit trust assumptions,
but it must not silently replace proof-carrying admission for arbitrary peers.

A quorum can reduce reliance on one checker/operator if a threshold of genuinely
independent parties is honest and has checked the claim. Sybil peer identifiers
do not supply that premise. TEE attestation instead depends on the attested
program, hardware/vendor, isolation and rollback assumptions. Both may be
optional service policies; neither removes the semantic checker requirement.

## Does current proof-of-execution certify unnecessary work?

The inspected module relation already proves **existence of a checked witness**,
not the producer's full historical execution. It does not run LLM search, Lean
elaboration, peer discovery, storage repair or operational log validation in
the mathematical guest. Those activities must not be newly moved into it.

`software/v5/modules/receipt/src/relation.rs` currently performs:

- Bounded decoding/canonical checks and exact adopted foundation-row matching.
- Module/group commitments and exact parent journal/opening checks.
- Exact parent rank, group and demanded-body census checks.
- Canonical-descriptor-to-native-row correspondence.
- Actual independent conditional checking of all new local declarations.
- Binding of the resulting public journal.

The guest entry point must then discharge every returned parent claim before
the final receipt is accepted. Skipping commitment/correspondence checks because
an untrusted host claims to have done them would let the receipt prove a
different theorem from the one shown to the consumer.

The aggregate relation currently repeats the same module check for each delta,
binds exact earlier warrants, verifies target closure, and commits its selected
members. This is logically appropriate for that certificate statement. It is
not a theorem that the current encoding or grouping is cost-optimal.

Promising source-level cost reductions to investigate in principle are:

1. Keep large proof search and elaboration outside the proof relation.
   This is already the current separation, not a new discovery.
2. Avoid certifying contributions until an actual cold-use demand or justified
   amortization opportunity exists; pool useful deltas behind selected cuts.
3. Allow smaller module boundaries or alternate proof witnesses where semantics
   permit, rather than certifying unrelated declarations merely because they
   share a source file. Recursive/inductive groups remain atomic.
4. Replace redundant parsing/serialization or repeated foundation material with
   a simpler verified relation representation. Exact semantic/input binding
   must be restored inside the trusted relation; a faster host cannot assert it.
5. Consider specialized certificates/reflection for recurrent mathematical
   subproblems before commissioning a new universal proof-system implementation.

None of these is yet a measured producer speedup. A new relation/image needs
new adoption and compatibility analysis; existing receipts cannot silently
acquire a new interpretation. The current source includes duplicated traversals
and fixed foundation handling, but reading that fact is not a cost attribution.

The actual typed-renewal02 evidence distinguishes the costs particularly well:
the native V conditional-check subprocess used 0.015625 Job CPU seconds, each
observed aggregate verification used 0.046875, and the complete installed
operation used 84.5625 known CPU seconds. These are nested, non-additive scopes.
They show why we must measure complete workflows and investigate operational
overhead; they do **not** prove how much of that overhead is removable or imply
that cryptographic production has the same cost. V remains locally checked,
not newly certified or published by that operation.

## Recommended protocol contract

Expose evidence availability separately from mathematical advertisement:

```text
advertised exact module
  -> candidate evidence routes
     -> already-valid local warrant
     -> adopted certificate + exact selected openings
     -> explicit bounded native checking from grounded frontier
     -> request/sponsor certificate production
  -> accepted local warrant, or a precise bounded nonacceptance result.
```

Discovery can advertise uncertified work; advertisement is not admission.
The consumer chooses acceptable evidence classes and a cumulative resource
budget before work starts. Any capable party may produce the requested
certificate, subject to access to the witness; the original author need not
fund every future consumer. A request for certification neither proves utility
nor entitles a requester to free unbounded computation.

At minimum distinguish `INVALID`, `MISSING_SEMANTICS`, `NEED_CERTIFICATE`,
`UNSUPPORTED_POLICY`, `UNAVAILABLE` and `BUDGET_EXHAUSTED`. A refusal to pay for
verification is not a mathematical counterexample. Missing proof data is not
proof of falsity. The ancestry-free profile must not silently downgrade to
an attestation or a full native ancestor replay.

Selective certificates should be attached to useful cuts, not automatically
to every edge. Any scheduling/ranking heuristic stays outside acceptance.
The economics audit must include producer costs, failed requests, certificate
verification, native checking, custody, indexes and operational overhead.
Rarity of demand is a reason not to prepay certification, not a reason to admit
unproved premises. This architecture requires no mandatory global research
agenda, intention interpreter, attribution ranking or global ledger.

## Highest-payoff next decision

Before another proof campaign, root should decide whether the public client
can make the above evidence-route choice using the **existing** mixed
native/certified machinery, with precise ancestry-free refusal semantics and
ordinary contributions discoverable before optional sealing. Inspect only the
missing public seams, not rebuild the mathematical checker. Separately choose
one reusable cut whose expected repeated cold use plausibly amortizes its
certificate cost. The economics and demand-protocol companion audits should
supply that selection; this note does not authorize a runtime experiment.

The crucial release claim is not “all checking is cheap.” It is:

> A consumer can accept a supported, certificate-covered mathematical interface
> without replaying ancestral theorem proofs; locally grounded work composes
> safely; cold uncertified work is never misrepresented as already warranted;
> and certification can be paid selectively where its total benefit justifies it.

## Evidence used and historical boundaries

- `software/v5/modules/receipt/src/relation.rs`, read completely for this audit.
- `software/v5/aggregate_claims/relation.rs`, read completely across two views.
- `software/v5/aggregate_claims/API.md`, exact-warrant/recursive-assumption
  contract; its early source-only status is historical, not current absence
  of genuine A* receipt evidence.
- `research/cycles/v5-2026-10-20/COLD-CERTIFICATION-ASSURANCE.md`, current
  conditional-checking/import source audit. Its older trust-withdrawal debt
  is superseded by the implemented withdrawal successor.
- `research/cycles/v5-2026-10-07/ASSURANCE.md`, inspected acceptance-chain and
  recursive-assurance sections; its initial missing-module statements describe
  that earlier date, not current capabilities.
- `research/cycles/v5-2026-10-07/MODULE-RELATION.md`, inspected exact
  import/merge/demand sections; architecture obligations, not all claims of
  implementation completion.
- `research/cycles/v5-2026-10-20/TYPED-RENEWAL-ACTUAL02-OUTCOME.md`, independently
  adopted genuine U receipt -> ordinary Lean V -> native V admission evidence.
- Current `software/v5/client/workspace_mixed.py`, cache-bearing source locations;
  current `software/v5/validation_phase/admission/trust.py`, withdrawal and
  scoped-validation locations, used only to avoid claiming those mechanisms
  are missing, not as a new whole-source audit.

No universal mathematical-proof lower bound, numerical recursive-security
bound, universal theorem-equivalence procedure, global search completeness,
permanent availability or inevitable exponential growth is asserted.
