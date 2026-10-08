# One hot-key split: conditional retained-ad visibility

2026-09-30 UTC. Owner: /root/census_review. Canonical root:
E:\Distributed Trustworthy Mathematical Knowledge Network.

**DESIGN_ONLY_QUIESCENT_TRANSITION_NOT_IMPLEMENTED.** No runtime, source,
wire/schema adoption or sealed-v3 change is selected. The first proposed
discriminator is quiescent and finite, not continuous service under arbitrary
churn. This checkpoint is separate from the direct type-diversity successor.

## Decision and inspected boundary

The smallest defensible next directory seam is one explicitly identified,
owner-fenced split of one key: immutable bounded snapshot pages, successor
placement confirmation, and old-view redirects retained through a declared
horizon. Refuse activation if cuts, copied records, capacity or leases are
missing. Do not implement an entire overlay or a central mathematics server.

Read existing cert_route.py, cert_route_store.py and the routed-peer CONTRACT
under product-local/certified-routed-peer-source-03 and
experiments/certified-routed-peer-01. Relevant existing facts:

- target supports only unsplit-v1/partition0; locate returns up to three
  discovered authenticated endpoints, not maintained replica-set membership.
- announce reports visibility after just one contacted replica confirms the
  ad for each selected key. Three chosen endpoints do not imply three copies.
- Ordinary find returns at most four rows, ordered by mutable expiry/sequence.
  A successfully posted ad outside that prefix is not confirmed. This is not
  exact-record status or exhaustive migration pagination.
- Leases are 60..3600 seconds. Refresh mutates expiry; explicit expiry deletes
  rows. Existing queries are not immutable multi-page migration snapshots.
- Existing finite quotas, bounded SQL and shared budgets are useful machinery.
  Their passed tests need not be repeated to investigate this different gap.

Counterexample: P confirms a only at O0, receives ANNOUNCEMENTS_VISIBLE, and O0
fails. O1/O2 never stored a. Every surviving node is correct and every request
bounded, but no surviving directory returns a.

## 1. Exact read/write-set intersection

For an explicitly named replica universe U, let W be replicas that actually
committed the exact ad and qualifying lease, R the nominal attempted read set,
and F the unavailable replicas. The elementary storage-reachability condition is

    (W intersect R) minus F is nonempty.

It means a queried live copy exists, not that a finite broad-key reply includes
it, or that its advertised mathematical holder is available.

Given only n=|U|, w=|W|, r=|R| and |F|<=f, the worst-case sufficient and tight
condition is w+r>n+f: |W intersect R|>=w+r-n, of which f can fail. If the
inequality fails, choose minimally overlapping sets and fail their intersection.

If R instead counts successful responders, R and F are disjoint and w+r>n
suffices. Obtaining r successes may need r+f attempts. For n=3,f=1,w=2, two
predetermined attempts do not suffice: W={0,1}, R={1,2}, F={1}. Up to all three
attempts do; two successful responses also do, but cannot be charged as only
two attempts in this example. Failed requests/referrals stay on one ledger.

The availability model is correct cooperative replicas plus crash/omission
faults. Distinct TLS identities are not independent machines, fault domains or
Sybil resistance. Malicious replicas can lie about storage and destroy recall;
directory claims never replace the separate mathematical certificate check.

## 2. Real partition split and exact view identity

V0 has one unsplit logical key and old replicas O={O0,O1,O2}. V1 has two child
buckets with p(a)=first bit of a.bundle_id and three replicas per child.
All holders of one bundle select the same child. This partitions row storage;
moving the unchanged key to other replicas would only be relocation.

A separately tagged directory target binds namespace, key, view ID, partition
policy and partition. Existing theorem/type/shape identities and namespace
stay unchanged; existing unsplit targets must not be silently reinterpreted.
New wire/store/cursor versions require explicit adoption.

Broad queries that know only the key must query both children for coverage.
Exact known-bundle lookup can choose its child. Hashing does not prove balanced
load: all actual rows may fall in one child. Enforce real per-child and
per-node quotas; a split may fail to provide enough capacity.

Immutable descriptor X binds schema, namespace/key, exact parent V0 ID,
old endpoints, V1 ID, partition function, both child endpoint sets, maximum
old-view validity E0, redirect horizon, lease/skew policy and all limits.
Its transition ID is a digest of these exact bytes. Activation is a separate
append-only record, not a rewrite of X.

Each old replica has a durable compare-and-set successor slot for V0; a
different X is refused. Operators deliberately choose the same X. Conflicting
choices block progress: this slice has no leader election, globally latest
view, consensus-complete log or automatic conflict resolution.

## 3. State machine: first transition is all-old fenced

The delivered old publication policy has only one confirmed copy. A future
W2 policy could support a different live-transition argument but cannot
retroactively protect old one-copy ads. Therefore the first executable seam
must obtain a complete fenced cut from **every named old replica**.

| State | Permitted work and invariant | Completion |
|---|---|---|
| OPEN(V0) | Existing writes/reads; no split claim. | Owner selects X. |
| FENCED(V0,X,cut) | Atomic persistent fence, no more old insert/refresh, selected-key rows pinned against expiry; old reads continue. | Three old fence records collected. |
| COPYING(X) | Bounded complete donor pages; exact union; charged child insertion and exact confirmations. | Coverage predicate holds. |
| READY(X) | Copies/leases/capacity confirmed; not an active public split yet. | Activation and redirect records confirmed at all old members. |
| ACTIVE/DRAINING(X) | Explicit V1 writes; version-aware old reads learn X; old records retained through promised horizons. | Separate bounded retirement after horizon. |
| RETIRED(V0,X) | Reclaim old data within limits. | No assumption all bootstrap contacts learned V1. |
| BLOCKED(X) | Missing/conflicting cut, lease, quota, ACK, deadline or coordinator crash. Preserve evidence and old reads. | Separate finite continuation/diagnosis, never a hidden retry. |

Fencing is an owner-authorized local action, not a publisher's remote power to
retire a shard. One transaction commits X, the write fence and immutable cut
before returning. A write racing that transaction either commits before the
cut and belongs to it, or observes the fence and refuses with X.

There is no instantaneous global close. A write accepted by a not-yet-fenced
member belongs to that member's later cut. Only after all three fence commits
can no named old member admit an old write. Stale writers must process a
redirect/refusal, not mislabel it successful placement. Publishers may be
temporarily refused; continuous-write liveness is not claimed.

If an old member disappears before its complete cut is obtained, transition
progress blocks: it could hold the only copy of a previously successful ad.
The first discriminator tolerates the selected replica loss only after
successor coverage/activation. It is not a general churn protocol.

Coordinator crash leaves persisted fences and partial records. Another
operator may continue the same X/cuts under a separately charged finite
selection; automatic failover is not provided. No implicit rollback/reopening
can admit writes beyond the frozen cut. Partial activation remains explicitly
incomplete, even if some readers already learn X. No permanent coordinator
must sit on later lookup paths.

## 4. Immutable paged cuts and exact coverage

Do not scan all ads, all peers or the corpus. Fencing one key pins its existing
rows instead of making a whole-database snapshot inside one transaction.
A fresh successor store needs transactional per-key counts and an index on
(view_id,target,sequence). No silent source03 store migration is selected.

Each cut binds store ID, V0, X, namespace/key, maximum sequence, row count and
fence-record digest. Refresh/deletion cannot mutate pinned cut rows. A cursor
binds that cut, previous sequence, per-page limits and the same operation
budget identity. Each page reads at most B rows by indexed increasing sequence
within the cut. Completion requires its exact distinct row count and a final
end marker; an empty cut still returns one bounded terminal response.
Wrong cut, gap detected by count, duplicate/out-of-order sequence, changed row
or missing terminal evidence refuses completion.

This is a correct-server completeness contract, not an adversarial proof:
authenticated transport cannot prove that a dishonest server disclosed all
its rows. Union donor rows by namespace/key/bundle/holder; exact offer and
endpoint bytes must agree, and maximum retained expiry is preserved. Conflicting
descriptors refuse. With old per-key cap M, union size N<=3M; pages are at most

    sum over old i of max(1, ceil(m_i/B)).

That is bounded selected-key work, potentially expensive, not constant-time
migration. The adapter bounds union memory/disk by these caps before starting.

For every still-covered row a, READY requires two actual child copies among
its three named replicas, bound to X, partition, exact bytes and sufficient
lease. Each insertion enforces row/payload/page quotas atomically. A capacity
preflight is not a reservation: either implement an explicit expiring charged
reservation or tolerate later quota refusal. The test below selects explicit
reservations; production may instead refuse late insertion.

Existing provisional POST is insufficient. A subsequent exact-record status/
read confirms local commitment after transport completion. First-four broad
find cannot substitute. This small point-status seam is new.

Call the observation PLACEMENT_CONFIRMED_UNTIL_SCOPED_HORIZON, not unqualified
durability. Joint ACKs are authenticated observations of bytes/leases at the
chosen endpoints, not future availability, bundle custody, global consensus
or mathematical truth. If capacity or coverage fails, preserve partial copies,
charges and old pinned rows; do not activate in hope of later repair.

Pinned donor rows, union/transcript records, reservations, rollback journals,
temporary pages and later expiry all consume resources. Query is not a free
garbage collector.

## 5. Lease mathematics, skew and stale readers

Operation deadlines use monotonic time. Cross-node absolute lease comparisons
assume |C_i(t)-t|<=epsilon, no backwards clock jump, over the declared horizon.
Current source checks local regression, not a global skew bound. Unavailable
or violated skew assumptions invalidate timing-based cutover claims.

An absolute expiry e may disappear as early as real e-epsilon, or remain
until e+epsilon. To preserve every possible old validity interval, two new
confirmations must each satisfy

    e_new >= e_old_max + 2*epsilon.

A conservative local observation of safe expiry is C_now>=e_old+2*epsilon.
Records provably expired before the promised observation are not preservation
obligations. A record expiring mid-query does not satisfy a full-duration
guarantee.

Extended directory retention is a paid metadata lease, not silent renewal
of a publisher's promise to serve the bundle. If the new expiry cannot fit
lease limits/capacity, refuse or wait for safe expiry; do not quietly weaken
coverage. The holder remains an independent availability assumption.

Let E0 be V0's immutable maximum advertised view-validity time and D the
reader's maximum duration. Retain old redirects through local expiry

    E_redirect >= E0 + D + 2*epsilon.

The slowest allowed reader may start at real E0+epsilon; the fastest old
replica expires at E_redirect-epsilon. This inequality covers the entire
reader operation. V0 cannot be reissued with a later E0. A client keeping it
beyond E0 must report VIEW_EXPIRED/INCOMPLETE, not demand indefinite forwarding.
Validity intervals are half-open: start requires local time strictly below
E0, and completion must precede the absolute deadline. Boundary equality is
not a promise of service after an expiry.

Per-record horizon H_a is explicit: two child ACKs must each expire at least
H_a+epsilon. Covering the whole stale window requires H_a>=E0+D+epsilon.
Not every short-lived old ad has that promise. Preserving its original lease
and guaranteeing the whole stale window are different conditions.

The first profile supports exactly one transition. A stale *version-aware*
client may follow X once; a v1 binary that cannot parse X is unsupported and
must refuse, not report an empty old result as globally complete. Chained
transitions need a separately bounded hop/retention policy.

## 6. Conditional theorem and counterexamples

Fix an ad a in a completed donor cut. Assume all three old members fenced,
their cuts were completely copied, correct stores retain commitments, READY
and activation conditions hold, a has two confirmed live-lease copies among
three child replicas, at most one named replica is unavailable to this client,
old X records survive the stale interval, admitted finite entry paths reach
the required endpoint sets, and one ledger affords all attempts.

A stale client attempting up to all three old endpoints learns X despite one
failure. Attempting up to all three endpoints of a's child intersects its two
copies since 2+3>3+1. Therefore at least one accessible child contains a during
its guaranteed interval. A client already holding X skips old-view resolution.
This is conditional bounded directory reachability.

For an actual bounded broad query to return a, additionally require that a
lies within its row/byte/candidate opportunity at one contacted copy, or use
its already-known exact ID. Fill every broad reply prefix with other live rows
and the transition invariants can all hold while the useful candidate remains
unreturned. Type diversity addresses some prefix duplication, not directory
intersection or general useful recall.

Cut coverage follows locally: a successful old write either remains in its
member's immutable cut or has expired outside the claim; every member's cut
is enumerated; the exact union yields successor placements. After its fence
each member refuses old writes. Excluding one unfenced one-ACK member breaks
this proof: it can accept a new ad after another member's snapshot. A two-ACK
descriptor alone does not close this concurrent-write hole.

Failure of both child copies is outside f=1. A network partition separating
the client from all copies likewise violates the stated caller-relative
availability premise even if the machines are physically healthy.

## 7. One finite ledger and the smallest implementation seam

All entry referrals, old-view requests, child enumeration, exact confirmations
and selected acquisition use one caller ledger. Reserve each attempted RPC,
maximum request/reply/header bytes, scanned rows and candidate entries before
dispatch. Keep one absolute deadline. Failures are not refunded. Client follows
referrals; servers do not create invisible recursive fanout.

After entry location, a stale broad query needs at most three old plus six
child attempts. Exact known-partition lookup needs at most six. Entry referrals
and acquisition are additional explicit reservations. These bounds do not mean
the existing four-find cap already supports this mode: a separately versioned
finite query budget is needed; lower budgets return honest incompleteness.
Never instantiate a fresh Budget at each child.

Maintenance has its own prospectively selected ledger, not hidden consumer
work. With N union rows, no retries and optional capacity reservation at all
six children, the selected scheme charges:

- Three fences and all bounded donor pages.
- Six actual capacity reservations.
- 2N placements and 2N exact confirmations.
- Three activation writes and three activation confirmations.
- Every local SQL/page/byte/transcript operation and later expiry.

Thus RPC count is 15 + pages + 4N. It can exceed normal route caps; refuse or
adopt a separate finite maintenance profile prospectively, never bypass limits.
No proof of hard disk isolation follows from main-database or payload quotas.

Smallest next selection, if separately authorized: a fresh inert ad-store
schema plus local owner-transition adapter for one key, implementing fence/cut,
bounded immutable page cursor, tagged binary-child target, exact-record status,
charged admission/lease coverage, and activation/one-hop reply. Use fake
transport and virtual clocks. Reuse existing descriptor/endpoint validation
and budget patterns. Do not add automatic overlay maintenance, cryptography,
native Lean, TLS deployment, source04 diversity routing or new certificate
fixtures. Continuous publication and public protocol qualification are later
separate gates.

Proposed later commissioning location (not created or selected here):
experiments/certified-directory-transition-01/CONTRACT.md. Keep the first seam
experiment-local: source author owns only new directory_store.py,
directory_client.py and SOURCE-NOTES.md; independent reviewer owns tests.py,
TEST-PLAN.md and SOURCE-REVIEW.md; root owns CONTRACT, any finite runner,
selection and outcome adoption. Those two modules model the fresh inert store
and one-transition caller, using explicitly bound existing validation helpers
only if separately reviewed. No product source, used AdStore, cert_route.py,
type-diversity successor or namespace is an allowed edit. This leaf proposal
is a scope recommendation, not present implementation authority.

## 8. Frozen finite trace/oracle, NOT RUN

Nine logical directory stores: O0/O1/O2, L0/L1/L2, R0/R1/R2. One retained
bundle holder H, publisher P and consumer C. C has only cached V0's old set;
X reveals six child contacts for this one key, not an all-network roster.

Synthetic ads a,b have bundle-ID first bits 0,1. O0 stores a,b; O1 stores b;
O2 is empty. Thus a has one old copy and the two-row O0 quota is full.
Each child has a two-row quota and receives only its one selected ad.
B=1. Virtual UTC epsilon=1; both old expiries=300; E0=200; D=10;
redirect expiry=212; confirmed child expiry=302. No actual cryptography,
credentials, sockets or independent-host claim is part of this oracle.

| Step | Event | Expected result |
|---|---|---|
| 0, t=90 | C caches V0; P previously saw a only at O0. | No fault tolerance yet. |
| 1, t=100..102 | Fence O0/O1/O2 separately. Refresh b at O1 before its fence, holding expiry at 300; repeat after fence. | First belongs to O1 cut; second refuses. Three fence RPCs. |
| 2, t=103..106 | O0 two one-row pages, O1 one page, O2 empty terminal page. | Four page RPCs; exact cuts/counts; union={a,b}. |
| 3, t=107..112 | Six charged expiring child capacity reservations. | Capacity refusal prevents READY. |
| 4, t=113..120 | Put/confirm a at L0,L1; b at R0,R1. | Four puts plus four exact reads; expiry=302 and exact partition/bytes. |
| 5, t=121..126 | Persist/confirm activation/redirect at O0/O1/O2. | Six RPCs. Maintenance total=27, no retries. |
| 6, t=130 | O0 becomes unavailable. | Sole old a copy lost, child copies survive. |
| 7, t=131 | C tries O0 (fails), O1 (X), then L2 (empty), L0 (a), R2 (empty), R0 (b). | Six charged query attempts; four child scan reservations; one ledger/deadline. Return unverified hints, not global completeness. |

The two injected stale-writer requests in step 1 belong to P's one separately
bounded two-attempt ledger; they are not free fixture changes. Maintenance's
27 plus P's two plus C's six make **35 attempted RPCs across the three actors**.
The prior retained state in step 0 is declared input, not freshly published
for free within that total. Each actor has one budget; total test supervision
must encompass all three, without adding nested counters twice.

The times fix a virtual order, not a prediction that real HTTP takes one
second. Freeze exact serialized request/reply/header/log sizes and finite
CPU/wall/storage/page/VM budgets before any runtime selection. Twenty-seven
RPCs is not permission for unbounded bytes. A proposed 32-RPC maintenance cap
would cover this no-retry trace only; distinct byte/time/local-step caps must
be derived from the selected adapter, not asserted by this design. Six
reservations include unused L2/R2 capacity; it remains charged until explicit
release/expiry. Acquisition from H is outside this directory-only trace and
requires a separately reserved request and actual later qualification.

Required counterexample traces, separately bounded:

1. Lose O0 before its fence/cut: abort, do not claim preservation of a.
2. Accept a write after an acknowledged fence: invariant failure.
3. Omit O0's second page, swap a cursor/cut or mutate pinned expiry: refuse.
4. L1 quota refusal or expiry=300: no READY; one copy or insufficient skew
   margin is not coverage.
5. Instead lose L0 after activation: L2/L0/L1 attempts reach a at L1, charging
   the failure. Losing L0 and L1 is outside the one-failure premise.
6. Drop redirects at local 200 and let a slow-clock client start at E0:
   stale-window guarantee fails. Retention through 212 is required here.
7. Conflicting X, second-hop X2, old cursor on child or wrong partition:
   refusal/incompleteness, not success with renewed budget.
8. Exhaust budget after left child: right remains unqueried/incomplete.
9. In this negative trace, fix the child quota to one and both IDs' first bits
   to zero: two rows cannot fit; split blocks rather than assuming balance.
10. Crash coordinator after partial activation: preserve exact partial state;
    no automatic rollback, active-all claim or unpaid continuation.

## 9. Bootstrap and the remaining central gap

Finite independently configured entry contacts are compatible with
decentralization. They need not contain all mathematics or be a mandatory
unique server. But a node with no live/admissible contact cannot discover an
unknown network from nothing. This contract assumes a bounded entry path to
V0 during the stated horizon or an independently adopted V1 descriptor.
The small trace tests stale cached-view recovery, not natural bootstrap.

After redirect retirement, fresh discovery still requires maintained entry/
rendezvous state leading to V1. This contract does not prove propagation,
membership convergence or reachability of that state. Keeping every old root
forever hides unbounded maintenance; assuming everyone learned V1 hides the
same gap. Later work must specify paid replicated view-location refresh/repair
and bounded successor chains before a sustained huge-network claim is valid.

A partitioned consumer cannot distinguish “no theorem exists” from “a matching
theorem exists only in unreachable peers.” Leases, hashes, signatures and
directory quorums do not remove that information limit. Return scoped results
and explicit exhaustion, never globally fresh or complete system status.

Concrete progress here is a falsifiable single-transition contract: no silent
loss of its covered retained ads, explicit refusal when coverage is missing,
and costs shared across stale/current views. Continuous writes during split,
sustained churn repair, useful broad recall and net growth advantage remain
central unimplemented obligations.

## Separate narrow producer-cost sanity check

At root's request, read the two new small derived files
PUBLIC-PRODUCTION-ATTRIBUTION.json and PRODUCER-PRIORITY-FROM-ACTUAL-COSTS.md
in this checkpoint's directory, without reopening their twelve campaigns.
Their internal arithmetic agrees: 122 stages across twelve slices and six
kinds; slice and kind totals both 39,827.3125 nested stage CPU; enclosing
Jobs 42,528.453125; difference 2,701.140625; saved public-controller sum
2,699.5625. The adopted known prepare/production subtotal 42,781.21875
minus nested stage CPU is 2,953.90625, or 6.9046799888%; segments are
72.2763858849% of that known subtotal. Advance subtotal minus enclosing Jobs
is 155.796875; the earlier saved outer samples sum to 155.765625, confirming
the retained 0.03125 terminal-tail difference and why saved samples must not
replace adopted terminal accounting.

Consequently, with measured stage costs fixed, eliminating every known
non-stage component cannot save 10% of this particular known subtotal.
The note correctly declines a universal future-cost bound, causal benchmark,
net growth claim or addition of nested counters. This is arithmetic/scope
support for prioritizing dominant guest/proved work, not a new audit of
stage identities, old source files or their recorded hashes. No runtime or
historical qualification was repeated. Only this new design checkpoint was
written; sealed guides, used sources and evidence remain unchanged.

