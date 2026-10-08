# V4 mental model, invariants and leverage estimates

2026-10-02 UTC. Root checkpoint before further implementation selection.
This consolidates existing design; it does not establish a new passing result.

## The object is reusable certified knowledge, not a global chain

Represent an object by an immutable logic/foundation and checking profile,
selected formal interfaces, an exact content commitment and a verification
certificate. A peer advertisement points to it; a locator points to a directory
view. Neither pointer is mathematical evidence. Independent agents choose work
and retain what helps them; no global task list, intention criterion or full
replicated theorem ledger is needed. Replicas collectively hold objects and
index metadata, while each reader downloads only selected material.

There are three independent obligations:

1. **Acceptance safety:** an accepted interface is derivable under its exact
   foundation/checker assumptions. Computational certificate soundness only
   certifies execution of the pinned checking relation. It does not prove that
   relation corresponds to Lean or that the foundation is consistent. The
   current independent Nanoda implementation and restricted support envelope
   remain explicit assurance/scope assumptions, not full Lean correspondence.
2. **Conditional availability/discovery:** a live covered directory copy can be
   reached, and a live holder can supply the object. A digest authenticates bytes,
   not their continued storage. Complete global absence cannot be inferred from
   bounded queries or network partitions.
3. **Economic usefulness:** acquired interfaces actually make later correct
   work easier, after all attributable production/search/maintenance costs.
   Truth, byte novelty, popularity and usefulness are not interchangeable.

## Proof reuse and cost separation

For a certified child, independently authenticate each explicitly selected
parent interface, verify its receipt, check the new proof relative to those
interfaces, and recursively discharge all cryptographic assumptions. Strict
rank descent prevents circular assumption justification. Final receipt
verification must reject unresolved assumptions. Receiver cost depends on the
final certificate and selected interface/type material, not the number of
ancestral proof steps. Its local Lean construction still pays for the selected
types and demanded definitional computation: succinctness cannot make arbitrary
interface size or evaluation cost disappear.

The current scheme already gives this restricted recursive-reuse shape, but
production is expensive. Saved v3 known prepare/production cost was42,781.21875
CPU seconds;72.2764% belonged to segment stages. Controller-only optimization
leaves that dominant segment work untouched. Its ceiling depends on the actual
controller share, not all non-segment time; the remaining27.7236% is not zero
and could itself contain meaningful savings. Reducing guest work targets the
largest observed category without assuming a guaranteed whole-workflow gain.

Typed rows preserve per-row authentication, use the same compact serializer
with an exact counted Write sink, and consume each authenticated Value into the
same private Serde representation. Shared construction/finalization preserves
the old mathematical checks. This removes one text buffer and lexical parse;
it does **not** remove serialization, structural hashing or proof checking.
Both algorithms remain linear in their parsed input apart from checker work.
The speedup is a constant-factor hypothesis, not an asymptotic cure. The10%
trace gate is a finite adoption threshold, not a prediction guaranteed by theory.
An all-input congruence claim needs more than passing examples; finite probes
challenge the source equivalence argument and lock concrete refusal boundaries.

Observed update,2026-10-02: the owned-row experiment passed its finite congruence
controls but failed the prospective efficiency gate. Retained AB used75segments
and19660800paddedrows versus66/17301504, despite1.1625%fewer guest instructions.
This is a rejected optimization, not a speedup. Proof-trace work includes more
than instruction count; the aggregate result alone does not identify the cause.
Keep memory/allocation, code-layout and other circuit work as hypotheses until
source/trace evidence discriminates them. Do not assume fewer JSON passes helps.

Changing image also changes same-image parent compatibility and discovery.
If an optimization costs extra investment J and saves s per future production,
it breaks even only after N*s>J (include paid recertification/reindexing). Do not
pay a full new campaign merely because a cross-build or trace screen succeeds.

## Maintained search invariant and scaling limit

Exact keys rendezvous through bounded routing. Partition a hot logical key by
bundle hash prefix; locator metadata names its current view/child replica sets.
Known-bundle lookup visits one child; a broad key query must visit each selected
child needed for its claimed coverage. Budget exhaustion means incomplete.
Skew, lease expiry, hash imbalance and malicious omission remain explicit.

For named n replicas, w committed copies, r attempted reads and at most f
unavailable replicas, worst-case live intersection requires w+r>n+f. With
n=3,w=2,f=1, up to three read attempts are necessary; two arbitrary attempts
can miss the surviving copy. This is a crash/omission result, not Byzantine
storage proof or a claim of independent physical failure domains.

The first split must fence **all** old replicas because old publication had
only one confirmed copy. Atomic fences pin indexed immutable selected-key cuts;
complete bounded pages establish their exact union. Copy each covered row to
two successor replicas, preserving expiry with2*epsilon skew margin. Activate
only after exact coverage; partial copies/fences remain durable and charged.
Refresh current-view locators before old redirect retirement. Fresh readers
then need current locators, not perpetual old history or universal view gossip.
All routing/referral/placement/query work shares one finite operation ledger.

With selected-key cap M per old replica and page opportunity B, union<=3M and
successor placements are O(M). Byte limits can shorten a page below B; successful
complete donor pagination needs at most sum_i max(1,m_i) responses, not generally
sum_i max(1,ceil(m_i/B)). Indexed seeks and serialization remain payable. The
work is local in one key, not constant cost. A one-split implementation does not
solve repeated splits, arbitrary membership churn or maintained routing tables.
Those must reuse established DHT maintenance rather than assume fixed contacts
represent a huge dynamic network.

## Existing mechanism reuse, inspected primary source

Read the full [libp2p Kademlia DHT specification](https://github.com/libp2p/specs/blob/master/kad-dht/README.md)
on2026-10-02 (document labels latest revision r2,2022-12-09). Relevant mechanisms:
XOR-distance routing and bounded concurrency; client/server separation for
heterogeneous/NAT-constrained nodes; provider ads distinct from value validation;
provider republishing/expiry; periodic routing-table refresh and bounded
bootstrap; pure record validation and stable conflict selection.

These directly justify paid locator/ad refresh and refusal to equate metadata
with truth. Its recommended k20/alpha10 and IPFS22h/48h timings are **not** our
qualified parameters. Its convergence language does not establish our partial
CAS view agreement, adversarial recall, topology maintenance or capacity fit.
V4's existing TLS/wire is not libp2p protocol interoperability. Use the primitive
model now; adopting a mature transport/DHT library needs a deliberate integration
choice instead of silently calling the current finite overlay Kademlia-complete.

## What faster growth would actually mean

Fix equal-quality endpoint and opportunities for local/direct A, exact reuse B
and non-oracle search/reuse C. All may choose a shorter direct proof. Let C_A,i
and C_C,i be total cost in one stated unit for endpoint i; let J be incremental
shared production/index investment and M be maintenance/failure cost. A finite
net advantage requires sum_i(C_A,i-C_C,i)>J+M. CPU, elapsed time, bytes and agent
work are reported separately, not combined by an unexplained conversion.

If per-use saving d>0 is representative, break-even population is greater than
(J+M)/d. If d<=0, the measured workload does not justify a growth advantage.
Hypothetical large popularity cannot erase that finding. Reuse frequency can
guide optional local ranking, but it is manipulable and never acceptance
authority. Broad mathematical novelty/usefulness is not decidable by a general
kernel check; demand-weighted held-out workloads are legitimate empirical
evidence, not a human-intention criterion inside the network.

Prioritize a substantive affordable endpoint and the highest recurring proved
work next. Aliases, repeated reflexivity and more audit documents are not growth.
