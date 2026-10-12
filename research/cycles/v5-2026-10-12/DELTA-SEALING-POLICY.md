# Bounded reuse and selective aggregate sealing

2026-10-12. Theory/source investigation only; no new runtime, implementation,
proof budget or release claim. This extends, rather than repeats, the fixed-target
rent-or-buy theorem in [GROWTH-WORKLOAD, D21](../v5-2026-10-07/GROWTH-WORKLOAD.md)
and the [native-frontier argument](../v5-2026-10-07/DELTA-FRONTIER-NATIVE-SEAM.md).

## Decision

Keep native deltas for affordable ordinary contributions. Enforce the entire
uncertified closure envelope. Use an already available genuine seal when its
complete receiving route is preferable. Produce a new seal only with a finite
funded allocation and an explicit cost/availability justification.

**The central remaining mechanism is an aggregate-DAG certificate.** With the
current profile2 guest, a chain cannot advance its certified frontier in cheap
large jumps: certifying its last node requires real receipts for every preceding
uncertified parent. A packet of native successes is not such a receipt.

## Current evidence and the immediate policy

The retained `delta-actual-01` operation reports real cold base receipt admission,
one actual child check and a clean invalid-proof refusal. This note reads those
records; their independent outcome audit is a separate assignment.

| Recorded quantity | Value and scope |
|---|---|
| Complete one-delta wire packet | 560,792 bytes; receipt hex is included |
| Uncertified witness | 113,220 bytes, 1,355 rows, 11 bodies/openings, one parent |
| Genuine base receipt | 223,594 raw bytes |
| Positive receipt/native workers | 0.03125 CPU seconds each, at this timer resolution |
| Whole positive-plus-controls harness | 7.578125 owner CPU; enclosing Job 8.125 CPU; outer wall 10.733341 seconds |
| Base production's 325 new stages | 126,105.625 worker CPU + 688.375 controller CPU, excluding earlier retained work |

Sources: [actual RESULT](../../../experiments/v5-local-checks/delta-actual-01/evidence/RESULT.json),
[packet census](../../../experiments/v5-local-checks/delta-actual-01/evidence/accepted/1/request.json),
[outer RESULT](../../../experiments/v5-local-checks/delta-actual-01/RESULT.json),
[base audit](BASE-PRODUCTION-AUDIT.md). Nested counters must not be added twice.
The harness includes pinning, openings, negative controls and reporting; neither
its total nor 0.03125 seconds is a measured standalone marginal receipt saving.
The base production cost is not a justified prediction for a future child seal.

For an actual packet and local envelope, the policy is:

1. Authenticate the offered route by its real verifier; never trust an offer,
   popularity counter, stored success flag or local delta handle as a seal.
2. Native-check only the complete selected closure within aggregate byte,
   graph, parser, CPU, memory, output and lifetime limits. Cache hits are exact
   same-profile live authority, not additional independent expensive uses.
3. If it cannot fit, return `NEEDS_SEAL`, missing-material or resource-incomplete
   as appropriate. The refusal guarantees no unsound fallback, not future service.
4. Current single-module sealing is eligible only when every exact direct parent
   journal already has a genuine profile2 receipt. Otherwise its quote must
   include all missing intermediate certificates, or declare that route unavailable.
5. Before funding, evaluate a *specific packet rewrite*: replace selected native
   witnesses with exact-journal certificates and remove only ancestors no longer
   required by any selected branch. Recompute the complete resulting envelope.

For a funding domain, horizon T, fixed nonnegative resource prices w and actual
cache class, let C_i(F) be full selected receiving/service cost with frontier F.
For candidate v, define its per-use marginal saving by

    d_i(v | F) = w · [C_i(F) - C_i(F ∪ {v})].

This is a difference of complete routes, not a sum of nominal ancestor sizes.
It includes added receipt checks/bytes, remaining semantics and all still-needed
shared ancestors. A candidate is prospectively beneficial if justified bounds give

    Σ_i d_i(v | F) > S_v + M_v(T),

where S_v includes all additional production/failed-work/publication costs and
M_v includes added custody, repair and service overhead. Existing common costs
cancel only in this marginal decision; they remain in project-wide full-cost
growth accounting. Observed demand is not promised future demand. For no-demand-
forecast operation, D21's factor-two rule applies only to its stated fixed-target,
known-before-service incremental costs and available-successful-seal assumptions.
Overlapping DAG targets do not inherit that guarantee independently.

An important concrete example: the second fold/map theorem directly imports both
the base and first delta. Sealing the first delta does not remove the base receipt
from that particular packet. With the present hex transport, replacing its
113,220-byte witness by an additional receipt of b bytes saves wire space only if
2b plus new metadata is smaller than the removed witness/openings. No first-delta
receipt size has been measured. A large usage count cannot fix a negative margin.

## Why periodic single-module sealing is insufficient

Consider v_0 certified and a chain v_i importing v_(i-1), with no alternative
derivations or identity-changing repacking. Current `main.rs` calls
`env::verify(journal.image, parent_bytes)` for **each direct parent**.
To obtain a profile2 receipt for v_k therefore requires one for v_(k-1), and so
on through v_1. By induction, k new nodes require k intermediate certificates
before the checkpoint v_k exists. Calling only every kth node a checkpoint does
not divide certificate production cost by k.

Native deltas still avoid certification for low-use branches and permit bounded
experimentation immediately. But indefinite advancement of a fixed-size window
on this chain eventually certifies each node under this route. Cheap individual
checking, finite packet caps and expensive per-node certification are not by
themselves a scalable growth strategy.

The desired aggregate route checks all k new mathematical extensions inside one
new guest execution and produces **one application receipt**, with recursive
assumptions only for already certified boundary claims. It removes intermediate
certificate production, not the necessary checking/proving of new mathematics.

## Proposed aggregate certificate: exact compatibility boundary

Let I be the currently adopted module image `9dfd5892…`, and A a newly built and
independently adopted aggregate guest image. Do not change or impersonate I.

The aggregate guest reuses the exact current `relation::check_bytes`. Its
184-byte internal module journals J retain `J.image = I`, foundation, semantic
policy, ModuleID, group root/count and rank **unchanged**. These bytes label the
existing conditional module relation. A receipt under A is a different warrant
for that relation's conclusions, not a receipt under I.

This preserves mathematical identities and existing parent/opening bytes without
claiming that an old verifier accepts a new image. It also avoids an unnecessary
global rewrite of content addresses. Current `ReceiptVerifier`, `checked_receipt`
and old guest parent rules correctly reject an A receipt as an I receipt; they
must remain unchanged. A new exact aggregate receiver and explicitly selected
native-frontier successor are required.

Initial trust profile: exactly one fixed (I, foundation, semantic policy,
conditional-checker source) tuple and one actual A. No caller-selected arbitrary
image or foundation. Software upgrades need a new adopted profile; an old buggy
foundation/checker cannot be repaired by merely wrapping its receipts in A.

### Public statement and membership

Proposed fresh 192-byte aggregate journal, distinct magic/profile:

    magic[8], version:u32,
    aggregate_image:A[32], relation_image:I[32],
    foundation[32], policy[32], members_root[32],
    member_count:u32, maximum_member_rank:u64, seal_height:u64.

All integers use a specified fixed endian encoding, with exact lengths and
domain-separated hashing. Sort members by ModuleID; reject repeated ModuleIDs
(including conflicting ranks/journals). A leaf commits `(index, exact J bytes)`;
node hashes commit ordered children; bind count/index and specify deterministic
odd-leaf handling. A recipient verifies the real A receipt and a bounded leaf
opening, then uses J's existing group Merkle opening and body commitments.
Thus it obtains one module without downloading all sealed witnesses or all members.

Export the accepted closure's journals, including authenticated frontier members,
not only the last target. The host supplies nonempty designated target journals;
the guest requires that every submitted graph node is reachable backwards from
those targets. Every designated target must be a newly checked delta. Membership
claims concern valid modules, not proof provenance or arbitrary omitted ancestors.

For m sealed members and a selected declaration group g, receiver work is one
receipt verification, O(log m) membership hashes, the group opening and required
interfaces/semantics. No mandatory term reads the sealed proof histories. Neither
large definitions nor expensive conversion becomes constant-time.

### Guest input and verification algorithm

Use a fresh framed input, not receipt-shaped JSON flags. The host supplies actual
receipt witnesses separately through SDK assumptions. Guest input carries:

- Declared aggregate image A, fixed-profile header, finite global envelope and
  unique assumption descriptors: either `(I, exact legacy J)` or
  `(A, exact earlier aggregate journal)`.
- Selected legacy frontier journals or selected member openings under an earlier
  aggregate descriptor. Verify each unique aggregate assumption once even when
  it supports several selected members.
- Bounded ordered frames of complete ordinary delta witnesses, plus target IDs.

The envelope is enforced by compiled maxima, not freely enlarged remote limits.
An initial source profile can bound 8 unique receipt assumptions, 32 frontier
members, 16 deltas, 128 parent edges and at most 48 exported members, with a
16 MiB aggregate witness-byte budget and the existing row/body/parser bounds
applied globally as well as per witness. These are design starting caps, not
an assertion that the current guest cycle or memory allowance can execute them.

Algorithm:

1. Check exact framing/EOF, header, sums with checked arithmetic, counts, parser
   depth/nodes, unique assumption descriptors, source-profile I/foundation/policy.
2. For each legacy descriptor call `env::verify(I,J)`. For each aggregate
   descriptor call `env::verify(A,H)`, validate H's aggregate profile/image/domain,
   and verify every selected member opening. Insert only the actual authenticated
   J bytes into a private graph. Reject duplicate/alternate module instances.
3. Process each delta frame with unchanged `relation::check_bytes`. Require the
   returned J to use I and the fixed foundation/policy; require every returned
   exact parent J already in the graph. The existing relation checks all local
   proofs, openings, definitions, inductive groups and exact parent-rank increment.
   Reject duplicate modules; record its exact returned edges and conclusion.
4. Check complete target reachability, no unused assumption/selected member/delta,
   and aggregate census. The bound applies to actual submitted material, including
   eventual refusals. Construct the sorted Merkle commitment to graph members.
5. Set `seal_height = 1 + max(parent aggregate heights)`, with default max 0;
   reject overflow. Set maximum member rank from actual journals. Commit the
   complete fresh aggregate header with the supplied A field.

As in the current guest, its own image cannot be embedded as a self-hash. The
receiver must verify the actual adopted image A and require the committed A field
to equal it. Only then do the guest's A-parent verifications use the adopted image.
Legacy I is an already known fixed compiled/adopted input, not this self-hash.

The new member set is deliberately bounded. This is not a permanently growing
global commitment. A later batch imports only selected members from earlier
aggregate receipts and exports its new bounded closure. Independent batches and
branches can therefore advance without a global synchronized environment root.

### Conditional soundness, branching and recursion

Assume sound application verification under I and A, the actual recursive
multi-assumption composition, collision-resistant commitments, and correctness
of the pinned conditional module relation. Induct first on seal_height for
aggregate frontier claims, then on the finite topological delta order. Legacy
frontiers are verified premises; aggregate member openings inherit valid
conclusions from lower-height aggregates. Each new relation conclusion has all
its exact premises established. Therefore every committed member is valid under
the fixed policy. Merkle binding then transfers that conclusion to a recipient's
selected opening. There is no inference from a native success flag.

Seal height and mathematical rank are different. Height grounds aggregate-proof
recursion; rank grounds local mathematical dependency order. A batch may import
a low-rank member of a high-height aggregate. Do not silently relabel either.

Compatible branches share exact module-qualified definitions and can supply
different selected groups. The unchanged relation checks the actual combined
context, universes, demanded bodies and atomic recursive declaration groups.
Same ModuleID with conflicting exact journals is conservatively refused, as by
the current delta API; arbitrary semantic equivalence is not solved. Different
I/foundation/policy domains refuse rather than being merged by hashes or votes.

## Host, receiver and resource feasibility against actual sources

Current [guest main](../../../software/v5/modules/receipt/src/main.rs) is the
small wrapper being replaced, not the mathematical relation. Current
[module_host](../../../software/v5/modules/receipt/src/bin/module_host.rs)
couples every receipt to one 184-byte I journal, checks every parent with that
same image and caps parents at 8 and proof segments at 128. Those checks cannot
be bypassed by a new CLI flag or by renaming A as I.

A fresh aggregate host must:

- Verify each typed frontier receipt using its actual permitted I or A image and
  matching exact journal; deduplicate *claims*, not only receipt byte digests.
- Supply and fully resolve all real SDK assumptions. Reuse the reviewed generic
  segment/lift/join/resolve/finish mechanism and assumption-claim ordering only
  after separating its old one-image/application decoder. Final verification
  must use non-dev mode, the selected receipt scheme and actual A.
- Bind fresh snapshot/checkpoint domains to A, full framed-input hash, exact
  expected aggregate header, unique frontier claims/receipts, limits and ordering.
  Old capsules/checkpoints must not become valid by path reuse.
- Keep the existing bounded stage/cycle/segment/memory/output limits unless a
  separately justified new finite profile is selected. A 16-delta envelope is
  not evidence that 16 expensive guest checks fit 128 segments.

Parse/check/drop one witness frame at a time; retain only bounded journals,
edges, selected frontier openings and commitment state between checks. This
avoids deliberately storing k simultaneous expression trees. It does not prove
an allocator/SDK resident-memory bound: dictionary overhead, caches, temporary
copies, semantic bodies and foundation rechecking remain charged. Aggregate
prover work includes the sum of all new checker executions; each presently
replays its fixed 413-row foundation. Batching does not justify O(1) proving.

The current first-child guest snapshot exceeded 2^25 cycles. It would be unsound
project planning to extrapolate the 0.03125 native CPU observation into a cheap
aggregate proof. First implement/review the pure aggregate relation and narrow
native changed-boundary controls; then use one selected aggregate execution-only
screen to determine actual rows/segments and preservation of bounded memory.
Do not authorize a full proof merely because the controller specification fits.

A new `VerifiedAggregateMember` must be minted only after real A verification
and exact membership binding, with owner/profile/deadline revocation. A fresh
delta receiving/import successor can accept these authenticated frontiers via
an explicit typed route; the old exact ReceiptVerifier gate remains intact.
One aggregate receipt may discharge several members without repeated crypto
verification. Outgoing packets retain genuine aggregate receipt/header/openings,
not local member handles. Formal indexes can keep ModuleIDs; proof-form/image and
coverage descriptors must distinguish the new route. Discovery and retention are
separate obligations, not consequences of this certificate.

## Amortization and service-capacity consequence

For a deliberately simple chain model, assume one batch of k new contributions
has additional seal cost `S(k) = S0 + s k`, and every contribution has λ cold
recipient uses. Charge native processing c per uncertified node, sealed-frontier
service v per use, equal semantics and cache policies, instantaneous successful
checkpoint availability, and additive resource prices fixed in advance. Requests
arriving at within-batch positions 1,…,k−1 check that many deltas; position k uses
the new seal. Other common costs and maintenance must be added separately.

The average additional cost per contribution is then

    A(k) = s + S0/k + λ v + λ c (k−1)/2.

This follows by dividing `S0+s k + λ[k v+c Σ_(j=1)^(k−1) j]` by k. For λc>0
the continuous minimum is `sqrt(2S0/(λc))`; choose a feasible neighboring integer
under the packet/proof/latency caps. These are modeled coefficients, not fitted
current measurements. For nonlinear actual S(k), compare finite feasible k using
the actual quoted/bounded expression instead. No batch larger than the owner
envelope is admitted merely because an optimizer suggests it.

Under identical linear-checking assumptions, k separate certificates pay
`k(S0+s)` versus aggregate `S0+s k`: fixed overhead saving `(k−1)S0`. Actual
recursive proving/receipt-size/service costs may violate this model and must be
charged. The current one-module guest has no right to claim this batch saving.

If contributions needing this continuing route arrive at rate ρ and allocated
proving supply is μ priced work units per unit time, necessary sustainable
capacity is `ρ(S0/k+s) < μ`. This average condition is not sufficient for bounded
latency without burst, queue and repair reserves. If no feasible k meets the
capacity and deadline constraints, stop accepting new *service commitments*,
seek additional explicitly funded supply or keep work local; do not weaken
mathematical acceptance or pretend an unavailable seal exists.

This establishes a conditional linear-cost continuation path with bounded
receiver closure. It proves neither positive discovery demand nor useful
knowledge growth. Full-cost superiority still uses all three comparators in
GROWTH-WORKLOAD: optimized local development, ordinary shared checked libraries,
and the certified network. Each can reuse already obtained methods/caches.

## Minimal implementation consequence and available measurements

Existing APIs already expose exact packet bytes, actual member journals, complete
closure material, parser census, fixed envelopes and reservations; retained
per-stage reports expose actual worker costs. They do **not** expose a reliable
future seal quote, complete per-use counterfactual cost, certified independent
demand, aggregate-DAG receipt route, durable cross-profile cache or funded
availability guarantee. `report().reserved_worker_cpu` is not consumed CPU;
`observed_success_worker_cpu` intentionally excludes failed work.

Minimum next additions are (a) an inert local `sealing plan` giving exact target/
profile/closure, eligible current route or aggregate-route requirement, proposed
post-seal packet census and explicit cost/horizon assumptions; and (b) the new
aggregate relation/host/member receiver described above. Neither should create a
global usage ledger or mutate mathematical admission based on popularity. Record
one local accountable funding reservation per selected immutable plan; reused
external seals are reverified before cancelling an unnecessary unstarted plan.
No permissionless protocol can prevent all independent duplicate proving without
extra coordination assumptions, and no factor-two network-wide bound is claimed.

The next decisive software claim is: a genuine aggregate receipt over a small
branching/two-delta workload lets a fresh receiver accept a selected member and
author its extension with zero sealed-witness downloads, while altered member,
wrong-image, missing-premise, cyclic/rank-invalid and unresolved-assumption cases
refuse. Its proof budget is separately selected only after the execution screen.
