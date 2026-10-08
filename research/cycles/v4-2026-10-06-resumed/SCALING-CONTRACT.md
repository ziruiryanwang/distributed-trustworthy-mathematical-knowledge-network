# Scale is a service contract, not a theorem-count claim

Root,2026-10-06. This argument links the maintained-overlay implementation and
unchanged certified proof boundary. It does not infer Internet-scale behavior
from five local peers. Source selection: overlay02, intent_store and the exact
patched kad-dht16.4.5 dependency retained under maintained-overlay-01.

## Separate three sizes

Let N be reachable network participants, M retained mathematical objects and H
the transitive proof history behind a selected certified cut. For an operation,
let I be requested semantic interface bytes, P new/unsealed proof work, F the
number of distinct certified frontier members and Q the returned candidates.
N,M,H need not be known by the requester. They cannot simply be erased from
total network cost: storage, certification, placement and maintenance remain paid.

The receiving path requires selected interfaces, genuine frontier receipts and
P; it does not fetch H. Its actual costs include installation adoption, receipt
verification, full local proof checking and demanded definition evaluation.
This is independence from ancestral proof replay, not constant cost for any
mathematical statement. Wide frontiers, large definitions or expensive conversion
can still force a refusal or separately funded cut. A receipt authenticates the
adopted guest relation; it is not a formal proof that the guest implementation
agrees with all Lean4 behavior or that a formal foundation is consistent.

## Routing locality and its nonempty favorable regime

The patched routing trie splits only the bucket containing the local256-bit
routing identifier. Each split leaves one sibling leaf and descends one bit;
there are at most257leaves, each with at most k=20contacts:5140contacts, before
stricter process/datastore caps. This bound needs no corpus census. Actual peer
anchors add at most one stored peer per observed common-prefix length. They do
not discover an unobserved disconnected region by magic.

Under the usual healthy distributed-ID and maintained bucket-coverage model,
XOR routing can make logarithmic expected progress in N. More explicitly, if
live routing choices cover O(log N)relevant occupied identifier scales with a
bounded number of probes per scale, a lookup uses O(log N)probes until the terminal
neighborhood; returning Q candidates adds at least Omega(Q)work. The coverage,
delivery and load premises are substantive; neither random identities alone
nor a local trie-size bound proves them. Arbitrary256-bit positions alone give
at most256scales, not a derived probabilistic log-N theorem. Our fixed query-event/time/provider
caps truncate work rather than falsifying those premises. The returned status
always distinguishes exhaustion/budget/failure from global completeness.

A homogeneous benign network with bounded churn, enough routable contacts per
occupied region, independent moderate key load and funded refresh is a nonempty
operating regime. Public-IPv4 configuration implements direct-address transport;
loopback evidence tests protocol mechanisms, not those physical-network premises.
NAT-only, DNS, relay traversal, adversarial identity concentration and partition
healing without any surviving contact are not supplied by this transport profile.

## Result keys, hot keys and storage

Fragment/interface/exact-type keys enable directed retrieval without scanning M.
Constant keys are candidate discovery, not complete semantic theorem search.
A provider advertises a local bounded catalog: one returned provider need not
contain every theorem sharing a popular constant. Per-key provider caps imply
potentially incomplete views. Exact result/statement retrieval and exhaustive
discovery of arbitrarily many distinct matches are different service contracts.
Agents can use discriminating formal keys and bounded pages; no global perfect
relevance/novelty oracle is introduced. Hot-key partitioning or a richer semantic
search index would require separately implemented placement/query semantics;
it is not silently claimed here.

If A advertisements are each retained at r distinct participants, at least r*A
provider rows are stored in aggregate; if the total supported row capacity is C,
complete such placement requires r*A<=C, ignoring other metadata. Hot-key caps
give additional local constraints. The implementation safely refuses excess
rows, which does not preserve universal discoverability under overload. Object
bytes require real custody separately; a provider row is not a storage promise.

## Renewals and admission cannot outrun service

Let T be a homogeneous participating provider TTL, J maximum scanner delay,
d an upper bound on a renewal
job's complete service time, a active local provider rows and c available
renewal slots. Under bounded delivery/processing, fair queue service and no
extra interfering work, a conservative sufficient renewal margin is

`T/2 > J + ceil(a/c)*d + delivery_margin`.

This follows by waiting at most J after the half-life trigger, then at most
ceil(a/c)batches until the last due job completes. It is deliberately sufficient,
not necessary; short test leases can succeed without satisfying worst-case
service assumptions. With heterogeneous nodes, the generalized sufficient margin
is `T_remote_min - T_publisher/2 > J + ceil(a/c)*d + delivery_margin`.
The left side can be negative: a publisher's own long TTL cannot establish a
shorter-lived remote row's availability. Mathematical namespace compatibility
does not force matching TTL settings. The current config enforces basic interval/TTL consistency,
not this complete liveness certificate. Operators must budget renewal alongside
queries and new publications. Concurrency2 and bounded queue32 are implementation
limits, not evidence that every legal4096-key configuration meets every TTL.

Atomic local intent prevents withdrawn queued jobs from recreating local provider
rows. Already-sent advertisements can arrive later; remote TTL starts on receipt.
No universal withdrawal-plus-TTL global expiry bound exists under arbitrary delay.
An incomplete publication before self-row admission needs explicit owner retry;
successful local publication attempts are not proofs of a remote replica count.

## Reciprocal growth consequence

For supported workflows, reusable verified lemmas and constructions can reduce
the cost of exact formal outputs or enlarge the outputs attainable under a
fixed finite budget. Optional additions preserve old capabilities only if they
do not evict old data or consume required resources. New names alone prove no
growth. Source-free application and transparent definition compilation target
real construction overhead and vocabulary barriers; their final checks remain
mandatory. Recurrent cuts target growing replay cost, with funded-seal assumptions
and explicit chain/DAG distinctions in rollover-policy-01/THEORY.md.

Thus v4 must provide the actual contribute/discover/acquire/apply/check/return
operations, expose costs and failures, and state a feasible service envelope.
This design avoids mandatory per-node global ledgers, global status, intentions
and task lists. It does not promise unlimited useful growth from finite resources.
