# V5 growth critical path: from a real seal to an economical usable commons

2026-10-16. Decision-focused source/theory review, not a runtime selection.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This checkpoint creates no product source, proof, test, Git or deployment change.
The full deployable v5 goal remains active.

## Decision in brief

1. Complete the already selected memo-guest integration and unchanged-cap screen.
   Its outcome answers a specific feasibility question, not the growth question.
2. On success, implement the minimal aggregate producer already specified in
   [AGGREGATE-PRODUCER-PLAN](../v5-2026-10-12/AGGREGATE-PRODUCER-PLAN.md), quote the
   complete finite seal path, and make one explicit capability-investment decision.
   Reuse the genuine I receipt and completed capsule; do not rerun either.
3. Use the already implemented combined real-A reciprocal harness once genuine A
   authority exists. Do not split it into duplicate local and network campaigns.
4. The next product-core source after those boundaries is a **fixture-free local
   workspace/client facade**, composing the existing search/acquire/admit/import/
   author/publish/custody APIs. Add route-cost accounting there, not another
   experiment-only ledger or a new mathematical checker.
5. Screen failure must not automatically select another optimizer. Preserve it,
   identify one decision-changing cause, and continue source work on that client
   seam over the existing genuine-I/bounded-delta route. This does not replace the
   required scalable A route or qualify v5 without it.

The important correction is that a real A receipt enables the growth mechanism;
it does not demonstrate that the mechanism is economical. The current small
mathematical example is valuable integration evidence but is not a favorable
certificate-economics workload.

## Reused results, not a fresh general theory

The controlling [growth workload](../v5-2026-10-07/GROWTH-WORKLOAD.md) already
defines warranted resource-bounded capability, the three comparators, full-cost
break-even, the conditional no-proof-ancestry receiver bound, and the narrowly
applicable rent-or-buy argument. This note does not replace or re-prove them.

[DELTA-RECIPROCAL-GROWTH](../v5-2026-10-12/DELTA-RECIPROCAL-GROWTH.md) already
justifies fold/map composition and its exact traversal saving for the specified
unfused evaluator. An equally optimized baseline may perform the same fusion;
that saving cannot be credited again to our network.

[REAL-A-RECIPROCAL-PLAN](../v5-2026-10-12/REAL-A-RECIPROCAL-PLAN.md) deliberately
has no positive net-benefit gate. Its useful new fact is removing FIRST's proof
from the author/recipient path using a genuine aggregate warrant, while SECOND
remains ordinary locally checked mathematics and circulates after origin loss.
The same note records that it is same-host evidence, not independently operated
deployment. Keep these distinctions.

The [image-lifetime decision](../v5-2026-10-12/IMAGE-LIFETIME-DECISION.md) is also
economically necessary: a seal's useful life is its supported, available,
nonrevoked life, not the lifetime of its hash. Stabilize the selected A image
through the reciprocal milestone; do not immediately optimize it away.

## Exact software seams that are still missing

Source inspection gives a more useful priority order than another broad feature
list:

| Seam | Actual present state | Smallest consequential next change |
|---|---|---|
| Repeatable certified-frontier advancement | Genuine I exists; no complete A capsule/receipt yet. Aggregate stage host and producer plan exist, but no Python aggregate producer. | Adopt the new screen if successful; implement the specified small staged controller, with complete-path funding and no automatic retries. |
| Ordinary reciprocal operation | Existing mixed components are callable. `mixed_network/reciprocal_actual.py` is an approximately 800-line exact-fixture campaign with hard-coded workload/query setup, loopback policy, cold owners and evidence assertions. | One local-owner facade taking user-selected formal query, local source, roots, profiles, budget and custody policy, without BASE/FIRST/SECOND fixture constants or reference packets. |
| Reuse rather than repeated setup | `mixed_claims/receiver.py` already caches exact receipt/profile claims inside one live owner. Each new `receive` still checks its native delta witnesses, and `describe`/`members`/opening calls perform live-origin/install checks. | Facade first looks up and reuses an existing **live exact handle** in its bounded owner session. Do not submit an already admitted exact object again merely because the caller made another API request. No checker/cache rewrite is required for this first improvement. |
| Reopen and recovery | `mixed_network/custody.py` persists exact untrusted packets in SQLite; handles are deliberately owner-local and disappear on close. | Reopen retained bytes, then obtain fresh authority under the current adopted profile. Persisted success JSON must never become a handle. Restart-safe trusted caches, if later desired, require a separate trust/update design. |
| Economic decision | Existing budgets enforce ceilings, but ceilings and `observed_success_worker_cpu` are not complete physical resource accounts or a routing quote. | Emit one cost envelope per user operation, linked to nested results without double counting; expose uncertainty/failure and cache-state distinctions. Use these records to decide which route/seal is worth funding. |
| Continued public service | Existing custody/index/location components can serve acquired bytes; the combined harness checks origin disappearance. | A persistent owner lifecycle with bounded retention, publication reconciliation and restart/re-advertisement, using existing stores; do not turn a finite fixture into an unbounded service by removing its deadline. |

The facade is not an autonomous agent research policy. The local agent still
chooses what to investigate, which candidates to try, and what proof to author.
No natural-language intention, global root goal or compulsory task list enters
the mathematical protocol.

### Minimal CommonsClient/Workspace contract and exact proposed source

The proposed fresh source paths are:

```text
software/v5/client/__init__.py
software/v5/client/workspace.py
software/v5/client/test_workspace.py
software/v5/client/API.md
```

They do not exist at this review checkpoint. Root must select them before any
implementation. Begin with one implementation module, not a new package per
operation. Reuse `MixedLocatedHandoff`, `MixedAcquisition`, `MixedDeltaVerifier`,
`MixedImportSession`, `MixedSourceOperation`, `MixedOwnerPreparation`, existing
stores and provider lifecycles. Do not import `reciprocal_actual.Campaign`: its
fixture-specific assertions and evidence setup are not the product controller.

`Workspace` owns retained bytes/configuration and store opening/closing;
`CommonsClient` owns one finite operation session and its **actual live issuers**.
The first implementation keeps I-only and A-capable adopted profiles explicit;
it neither substitutes one for another nor selects A without a genuine receipt.

```text
Workspace.open(root, owner_profile, create=False) -> workspace
workspace.operation(finite_budget) -> CommonsClient
  find(formal_query, coverage_request) -> candidate/coverage records
  acquire(candidate, route, requested_limits) -> exact bytes + live local warrant
  import_context(live_warrants, openings, demanded_bodies) -> ordinary Lean context
  author(context, local_lean_source, roots, requested_limits) -> untrusted contribution
  publish(contribution, semantics, retention_policy) -> availability hints
  report() / close()
workspace.serve(finite_service_allowance) / status() / close()
```

These names are an implementation proposal, not an already shipped API.
Publication is not admission: a provider may retain structurally checked bytes,
and recipients still verify them. A local agent wanting to use its new result
must acquire local authority through the normal checking boundary.

`acquire` can return an already live exact result from the same client only after
the issuer revalidates it. Cache identity binds its exact warrant J, evidence
and selected profile, not ModuleID alone. The optimization avoids another full
`receive`, not the issuer's live/profile/semantic-opening checks. This distinction
matters: a cached helper call has zero new receipt/native worker calls but can
still incur considerable controller hashing, reads and resource charges. A
same-process cache entry is not portable to another client, issuer or restart.

`report` must distinguish helper calls, full receives, actual mathematical worker
calls, cache hits, reserved limits, observed physical costs and unmeasured costs.
Bind them to one operation and its exact profile/input identities. Persist its
report as an audit record only. Existing enclosing Job CPU is inclusive; nested
worker/owner observations are a breakdown, not extra additive charges. Existing
`observed_success_worker_cpu` omits failed/other work and cannot be the total.
No public route-choice heuristic may promote an unverified result.

New controls target only facade boundaries: exact same-live-handle reuse without
another full receive, wrong profile/issuer refusal, closure/expiry, cold reopen
that rechecks retained evidence, failure-cost propagation, and no hidden grant
renewal. Existing component contracts are reused, not rerun. A genuine endpoint
test should cover a newly authored contribution through this facade, not repeat
the unchanged exact-fixture reciprocal campaign.

Store exact content, profiles and attempts, not borrowed authority. Reuse only
live exact owner-bound handles; closing, expiry or profile invalidation makes
them unusable. On restart use retained evidence to reverify, not old JSON claims.
Do not extend an old operation's allowance or silently turn a warm use into a
fresh budget. An explicit new user operation is allowed with earlier costs kept.

Candidate and route failures return their actual bounded status. A missing
candidate is not mathematical nonexistence; an unaffordable witness is not false;
a provider's advertised certificate cost is not a successful proof guarantee.

## A concrete benefit region that compares both serious alternatives

Fix a horizon T, resource prices w >= 0 for additive resources, initial
mathematics and cache states, selected algorithms, and an evaluation family of
formally accepted endpoints. Peak memory remains a feasibility constraint. Use
vectors/Pareto bounds instead when no defensible common valuation is available.

Let L be optimized independent local development, O ordinary shared libraries
with shared proof DAGs and locally checked imports, and V the v5 route. All may
cache a generic method once and use the same downstream optimizer. Any initial
method is available to every route; a genuinely remote missing discovery is not
given to L for free. O may distribute exactly the same new reusable mathematics
as V; this is what isolates certification from mere sharing.

For a selected finite sequence of useful endpoint events, write

    Cost(j) = F_j + M_j(T) + sum_i c_(j,i),       j in {L,O,V}.

F contains comparator-specific creation/installation/certification fixed work;
M contains retention, repair, indexing, provider work and failures not already
charged to events. Event cost includes search, acquisition, validation, semantic
material, actual application and its controller overhead. Cancel truly common
costs; do not count the same physical transfer or nested CPU twice.

V beats **both** alternatives exactly when

    sum_i (c_(L,i) - c_(V,i)) > (F_V-F_L) + (M_V-M_L)
    sum_i (c_(O,i) - c_(V,i)) > (F_V-F_O) + (M_V-M_O).

This is two obligations. A sharing win against L does not imply a certificate
win against O. A certification win on costly imports does not imply the queried
mathematics was useful. The endpoint comparison and the two costs are separate.

A directly implementable sufficient region is the following. For N eligible
events assume justified lower per-event margins d_L,d_O > 0 **after** variable
service, controller and failed-search overhead, and upper additional fixed
costs f_L,f_O >= 0 over T. Then

    N > max(f_L/d_L, f_O/d_O)

suffices. This is the earlier break-even result specialized to the intersection
of the two required regions. Every bound needs its source: analytic operation
bound, measured implementation cost, or explicitly uncertain forecast. Negative
or unsupported margins cannot be repaired by making N very large.

An eligible event is actual otherwise-uncached work, not a theorem name, page
view, peer ID or repeated use of a warm library. Include warm events too when
they incur extra v5 overhead: their margin may be zero or negative. No identity
scheme is required for the local accounting; a claim about independently costly
population demand needs evidence beyond self-reported peer counters.

### How proof size yields an honest, nonempty conditional region

For a declared ordinary comparator O that must transfer L_i bytes of its best
supported uncached proof package over throughput at most B_i, transfer latency
is at least L_i/B_i. Suppose v5's **entire comparable acquisition-to-ready
latency**, including selected semantics, receipt/native verification and control,
has justified upper bound v_i. Then L_i/B_i > v_i is a sufficient latency
improvement for that event. CPU and total-cost margins still need their own
bounds. The claim does not apply to a preaccepted local library, a different
short proof, or a better supported ordinary compression that removes L_i.

This region is relevant when proof ancestry H is large but selected interfaces,
demanded semantics and unsealed delta closure are small. Merely making the global
corpus large does not create that region. The current tiny native fixture has
checks around hundredths of a CPU second and does not establish d_O > 0.
Do not generate an enormous artificial ancestry merely to manufacture a win.
First extract the actual route constants from the required integration and
state the threshold symbolically where ordinary-case constants remain unknown.

## Historical cost and the next rational investment are different questions

Use three separate accounts; no erased cost and no sunk-cost fallacy:

| Account | Includes | Correct decision/use |
|---|---|---|
| Historical project account | All retained production, failures, builds, screening, analysis/setup and service costs where known; unknown tails labeled | What this project has actually spent. It is never rewritten by a later success. |
| From-genesis operational comparison | The costs each route would actually incur from the stated common initial state, including needed seals and maintenance | Whether a repeatable deployment has positive full-cost benefit. Development costs are included or amortized only under an explicit scope/horizon. |
| Forward decision at t0 | Only future costs and benefits that differ between the available actions, with current artifacts/caches explicitly supplied as initial state | Whether to fund the next A seal or use an existing receipt now. Past expense is not paid again and is not evidence that further spending is wise. |

The [prior cost decision](../v5-2026-10-12/NEXT-AGGREGATE-COST-DECISION.md) records
a base-production subtotal including carried stages of 127,958.078125 worker
CPU seconds plus 691.15625 controller CPU seconds: **128,649.234375 CPU seconds**.
This is not the entire project bill. The A cost is still unknown; neither a
screen pass nor I's per-segment average supplies its actual price.

At the current decision point I is already available, so do not fund it again.
When two future routes legitimately reuse the same accepted base, its already
incurred cost cancels from their *forward* comparison. A from-genesis comparison
against a route that never needed that certificate cannot cancel it. For any
claimed per-event margin upper bound d_max > 0, recovering that historical
subtotal alone would require N*d_max > 128649.234375; this necessary condition
is not a sufficient profit argument and supplies no observed d_max or demand N.

The first genuine A operation may rationally be a bounded capability/assurance
investment even when the tiny fixture is not profitable. Label and cap that
purpose. Repeated operational seals require the margin/capacity conditions above.

## Sustainable reciprocal growth imposes a service condition too

Cost amortization alone is insufficient. In a declared stationary additive-work
model, let lambda be the rate of new sealed frontiers, P their mean producer
work, and Q_p sustainable allocated prover capacity. Necessarily

    lambda * P < Q_p

for slack in that service. Analogous inequalities apply to search, receiving,
custody writes and repair; each charges actual work and failed requests. These
are necessary load conditions, not sufficient latency guarantees: burst
envelopes, queue scheduling, dependencies and correlated failures matter.

If a frontier receives n genuinely otherwise-uncached useful uses during its
supported horizon and has net per-use validation margin d > 0, its fixed sealing
and maintenance investment f requires n*d > f. A fast producer without enough
use is wasteful; popular mathematics with insufficient service capacity is not
operable. Sealing should therefore remain optional and local, with finite quotes
and supported horizons. There is no need for consensus on global usefulness.

At fixed resources and a positive lower work cost per distinct admitted event,
indefinite exponential event growth is impossible: the work demand eventually
exceeds capacity. Expanding capacity, lower per-event cost, or improved reusable
capability can change that bound. This does not prohibit large increases in
resource-bounded mathematical capability; it prohibits treating theorem counts
as a perpetual physical free lunch.

## Is orchestration consuming the project?

There is a concrete warning, not a claim that safety checks are unnecessary.
The retained ordinary author used 3.625 child CPU seconds but its owner lifetime
was 42.140625 CPU seconds; the enclosing operation failed later and cannot be
called a successful workflow. The real-A plan also notes 5,896 location-runtime
file pins (130,118,221 bytes) per installation verification. These are material
whole-route costs, not negligible paperwork. They do not prove which individual
function is dominant or justify removing an integrity check.

The new direct four-crate build reusing retained dependencies is the right kind
of correction. The next correction should be **composition into an ordinary
product lifecycle**, not growing a new supervision stack for each experiment.
Use the existing bounded owners and immutable installations. First reuse live
handles and installation lifetimes as permitted today; only then consider a
separately reviewed startup-integrity boundary if repeated hashing remains
consequential. Never turn a saved source hash into protection against a mutable
or hostile installation without stating that changed trust assumption.

Keep one mutable decision checkpoint per seam and one independent review per
new boundary; cite prior theory and tests. Do not rerun passing controls or
rewrite frozen evidence. A new cost log earns its place only if a public API
uses it or it changes the next investment decision. This checkpoint should be
consumed into a source selection, not extended into another general guide.

## Recommended root selections

- **Now:** finish the one selected guest build/assembly/screen; no larger cap or
  new optimizer is implied. Source-design the thin facade independently.
- **If the screen passes:** adopt a stable A0, implement the existing aggregate
  producer plan and complete-path quote, then decide explicitly on one capability
  receipt. Do not begin expensive proving with an unfunded finish/retention tail.
- **Once genuine A is adopted:** run the already reviewed combined reciprocal
  operation once. Capture route constants; do not add another synthetic growth
  benchmark merely to get a passing score.
- **If it fails:** preserve failure; choose one cause-supported correction or
  explicitly defer A funding. Advance the facade over the existing I/delta path
  without calling that a replacement for scalable proof ancestry cutoff.
- **Next product increment:** implement the fixture-free workspace facade,
  retained-byte reopening and operation-cost report with live authority only.
  Then exercise a real independently authored contribution through that API;
  avoid repeating unchanged mathematical fixtures as separate campaigns.

Public hostile-input isolation, restart-safe profile updates, supported portable
installation, license/security decisions and genuinely independently operated
evidence remain release obligations. None is waived here; neither should they
displace the present certificate-to-usable-client critical path.

## Independent contract and I-only source review

Later 2026-10-16. Root selected
[PRODUCT-INTEGRATION-SELECTION](PRODUCT-INTEGRATION-SELECTION.md), refining the
earlier proposed sequence: build an explicit I-only network mode and portable
location seam before the ordinary facade, rather than a local-only vault. This
review read [WORKSPACE-CLIENT-CONTRACT](WORKSPACE-CLIENT-CONTRACT.md) and the three
fresh `software/v5/frontier_network/` files. It ran no source, test, compiler,
network, verifier or Git operation.

### Contract corrections and disposition

The draft now preserves one query/handoff per finite client, one acquisition
for that client's lifetime, explicit new grants rather than hidden renewals,
fail-stop propagation after entered issuer failure, and retained bytes rather
than persisted authority. It distinguishes full receives from live helper reuse
and actual costs from reservations; it does not claim net growth from a faster
API. These are supported design choices, not test results.

A concrete review finding was adopted: `author(context, ...)` must accept an
opaque same-client context wrapper retaining its real live `MixedImportSession`
and exact selection/revision. Saved/caller-created context JSON is never
authority. The facade constructs the actual `MixedSourceOperation` from that
session, whose binding and liveness must still pass. Closing or changing its
representation invalidates the wrapper.

The originally proposed local-only increment would have needed another material
vault and left actual distributed use inaccessible. Root instead selected the
small permanent I-only profile. A configured **real** A owner would technically
permit I-only packets without consuming any A receipt, but adding that unused
installation/image/lifetime dependency is unnecessary. The explicit I-only mode
uses the actual available mathematical boundary without manufacturing A
authority or converting to the older delta protocol.

### Exact fresh source reviewed

| Relative path under `software/v5/frontier_network/` | SHA-256 |
|---|---|
| `__init__.py` | `be3c5dc2dc3d93a0928d0bc828434dd523b4a0a9374aec7af4c9989ca839368a` |
| `custody.py` | `e702e4ff35f00bc357beeb7289fa5a09846aef87578b51012bb390c1cd2df763` |
| `transport.py` | `9a857a62706451ce168dba3e92694f2ca31b9c4fe2e78c1b9011e74c1bd81b3a` |

No concrete semantic blocker was found in these bytes within the existing
trusted-owner/controller model. The argument is a restriction of already checked
semantics, not a new soundness proof of the underlying checker:

- The sole exact profile binds fixed I/F/P, `aggregate_image=None` and supported
  claim tags `[0]`, with distinct wire/offer/custody schemas, proof-form and
  profile-hash domain. Its store has a fresh database name/configuration; it does
  not migrate or reinterpret earlier A-capable or legacy stores.
- `PacketStore.inspect` revalidates that sole profile and calls the unchanged
  mixed parser with **literal** `aggregate_image=None`. Every tag-1 claim is
  refused before expensive mathematical processing; tag-0 exact Js, ranks,
  parents and closure retain the existing restrictions. Zero terminal claims
  remain possible when a bounded native derivation needs none; no false I
  receipt authority is inferred from the profile name.
- Custody inherits only legacy `put/get/status/close`: `put` calls the overridden
  `self.inspect`, then preserves exact blob equality, transaction/readback,
  quota and profile-keyed offer behavior. Constructor, inspect and offer are
  fresh. Mathematical ModuleIDs, Js and mixed packet bytes are unchanged.
- Provider construction accepts the new exact store type and matching F/P.
  Inherited HTTP dispatch/framing invokes that store's methods; offer requests
  bind the new profile, and returned packet bytes are still only untrusted data.
- Acquisition requires exact `MixedDeltaVerifier`, exact `ReceiptVerifier` as
  owner 0, no owner 1, no aggregate image, and matching fixed I/F/P. Constructor,
  offer verification and report override the older lexical profile/form paths.
  `MixedAcquisition.admit` remains unchanged: custody parse/readback precedes
  reservation/receive; genuine I checks, all native delta checks, final custody
  readback and live-handle promotion remain mandatory.
- Inherited `from_search` constructs the new concrete acquisition through `cls`
  but retains the same one-shot exact handoff, origin-bound candidate/contact
  checks, immutable prepayment and original deadline. Close still closes its
  shared budget/verifier; no facade may close it between promised live uses.

The contract's inheritance table originally described inheriting mixed
`inspect`; author corrected it to the actual safer override above. The reviewed
source already used the literal no-A parser call; its hashes are unchanged.

This review clears a source seam for separately selected changed-boundary
controls, not runtime or deployment. Portable location must still preserve the
same actual class identities required by the inherited handoff. The facade,
ordinary enclosing launcher, integration, recovery and actual public operation
remain unfinished. This I-only mode bounds unsealed ancestry; it does not
replace affordable genuine A frontier advancement or establish either of the
two full-cost benefit margins.
