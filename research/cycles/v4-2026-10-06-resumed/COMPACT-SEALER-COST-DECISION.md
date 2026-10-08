# Compact source-free sealer: cost and discriminator decision

2026-10-06 15:04 UTC. Source/theory-only decision by the mechanism agent.
No product change, build, proof, preparation or benchmark was launched. Root
selects adoption and any finite runtime; independent review remains separate.
The current user milestone is 11:00 Chicago / 16:00 UTC. Existing operations'
original deadlines do not change with that milestone.

## Central conclusion

A compact source-free sealer is useful: it can close a genuinely checked,
native-fast fragment into a transferable certified frontier without source
elaboration. The existing full `prepare-seal` / `advance` implementation supplies
the mathematical route. Compact packaging alone does not make proof production
cheap, and no current evidence supports promising a small segment count for a
small statement. Select a fresh zero-frontier input and measure its snapshot
shape once before selecting any expensive stage campaign. Do not reprove the
old n=41 fragment, repeat a completed campaign, or treat preparation as a cut.

The present rollover advisor is **not directly compatible with native-fast
evidence**. Its strict legacy local-execution schema and positive integer
`segments` requirement reject the native backend's extra backend field/null
segment count. This is safe refusal, not a mathematical failure. Never replace
unknown segment count by zero/one, strip the backend to suggest guest execution,
or label historical measurements as valid complete-route bounds.

## Exact implementation basis

Read-only sources:

- `product-local/v4-operator-integration-01/commons-v4/contributor/cert_stages.py`:
  `sequence`, `reserve`, `begin_attempt`, `Session.capture`, `Session.advance`.
- Adjacent `cert_workflow.py`: `prepare_seal`, durable initial state and main.
- Adjacent `profile.json`: the limits below, read as JSON data.
- `experiments/rollover-policy-01/rollover_policy.py`: `evidence` and `advise`;
  adjacent `THEORY.md` supplies the conditional recurrent-cut/quote arguments.
- `experiments/certified-seal-01/SEAL-OUTCOME.md` and
  `deliverables/2026-09-30-v3-tentative/RESULTS.md`: actual retained cost evidence.
- `experiments/action-application-01/project/companion/APPLICATION-API.md` and
  its pure test fixture: supported explicit proof/target grammar.
- `FULL-SEALER-PATH.md`: adopted full-source pins, wire/profile compatibility
  and source-free command path. Scale agent independently owns compact closure.

The unchanged mathematical identifiers are image
`5275d4fb567412d65ec0a9a01fa2fc2e5b12e1825a4ea247ab79880ef153b80a`
and foundation
`4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80`.
The cut must certify the exact fragment's capsule/journal, definition context,
rank and authenticated frontier, not a renamed theorem or a substituted easier
statement. Local-native assurance is not transferable cryptographic authority.

## Stage and funding calculation

For actual snapshot shape n>=1 segments and a>=0 distinct assumptions, the
sequence has n segment proofs, n lifts, n-1 joins, a resolves, finish and verify:

`s(n,a) = 3*n + a + 1`.

There are `3*n+a-1` ordinary workers, each reserving 1800 CPU seconds, and
two short final workers, each reserving 300 seconds. Each invocation also charges
600 controller seconds. Preparation verifies a frontier of a distinct receipts
and captures the guest once, with at most 300 seconds reserved per short worker.

For m advance invocations and one prepare invocation, a sufficient **booked
CPU envelope, conditional on all workers succeeding within their own caps**, is

`Q(n,a,m) = 600*(m+1) + 300*(a+1) + 1800*(3*n+a-1) + 600` seconds.

This is not an estimate of typical consumption and not a proof that the workers
finish. Actual measured worker charges replace their maximum reservations after
clean closure; controller charges do not shrink to measured controller CPU.
Do not add nested worker CPU again to an inclusive outer Job measurement.
Disjoint outer wrappers, installation/adoption, network distribution, continued
custody and failures remain additional costs in a complete economic quote.

Illustrative arithmetic, not selected campaigns:

| Actual shape | Stages | Ordinary-worker envelope | Q with one advance |
|---|---:|---:|---:|
| n=1, a=0 | 4 | 3600 CPU s | 5700 CPU s |
| n=2, a=0 | 7 | 9000 CPU s | 11100 CPU s |
| n=3, a=0 | 10 | 14400 CPU s | 16500 CPU s |
| n=41, a=1 | 125 | 221400 CPU s | 223800 CPU s |

The one-advance column ignores invocation wall feasibility; it is CPU arithmetic
only. Splitting into m calls adds `600*(m-1)` to that column. The current profile's
operation ceiling is 120000 CPU seconds. Thus the old n=41,a=1 input lacks a
worst-case full-stage funding guarantee under that ceiling even though measured
workers might be much cheaper. Its original 2400-second preparation allocation
has no next ordinary-stage room after another controller charge: the observed
601.96875 plus 600 plus 1800 exceeds 2400. It must not be reopened under a copied
run or relabeled larger original allowance.

Other exact caps: 4 GiB memory, eight active processes, 12 GiB working bytes,
8192 entries, guest 2^26 cycles, segment exponent 19; invocation wall 7200 seconds,
stage wall/deadline reserve 600 seconds; initial operation deadline at most
86400 seconds ahead. These are refusal/containment boundaries, not availability
or successful-completion theorems. In particular, total CPU funding does not
guarantee a wall-clock deadline: processor availability/controller wall overhead
and each serial stage's completion must be accounted for separately.

## No-progress READY must not drive a retry loop

`advance` adds its 600-second charge before trying a stage. `reserve` can then
stop the loop normally, yielding READY and exit zero with no completed stage.
Repeated calls burn resources without changing the mathematical state.

The minimum advisory/controller contract is:

1. Bind the exact clean closed record, original run/profile/allowance/deadline,
   snapshot shape and ordered completed prefix. Failed/incomplete/uncertain
   attempts are not implicitly resumable; COMPLETE is terminal.
2. Before launching another invocation, require
   `charged_so_far + 600 + reserve(next_kind) <= original_allowance` and at
   least 600 seconds plus explicitly chosen launch slack before the **original**
   deadline. This prevents a predictably unfunded zero-progress call.
3. Select a finite stage slice and outer CPU/wall/storage envelope. A full-cost
   bound must include all remaining stages and planned future controller charges,
   not just the next stage's reserve. Unknown bounds stay estimates/abstentions.
4. After closure, require either COMPLETE with its actual final cold verification
   and committed bundle, or a strictly longer valid stage prefix. READY with an
   unchanged prefix is a stop/advice result, never authorization to retry itself.
5. Retain actual charges/failures. A quote revision, package relocation, owner
   change or new advisor output is not allowance renewal. A genuinely new
   operation requires explicit new authority and retains prior costs in any
   claimed end-to-end economic comparison.

Preflight is necessary, not sufficient: time can elapse before the inner check.
The inner refusal remains authoritative. A read-only advisor cannot lock a run
or enforce owner serialization. One owner must serialize advancement.

## Minimum genuinely new discriminator

Use one prospectively fixed zero-frontier, no-definition proposition with an
explicit proof term and a mathematically different type from the old identity,
square-block and Iter/D1/D2 fixtures. A suitable candidate is:

```lean
(P Q R : Prop) -> (Q -> R) -> (P -> Q) -> P -> R
```

with proof `fun P Q R g f p => g (f p)`. This uses sorts, Pi/lambda, applications
and bound variables only; it requests no new constants, recursors or unsafe
axioms. It is intentionally an inexpensive interface/assurance discriminator,
not a newly discovered theorem or useful-growth demonstration. Root should bind
the exact new target/plan bytes and compare its type with previously used inputs
before adoption; a new output name alone is not novelty. The source text above
specifies the candidate only; no source elaboration or fixture generation ran.

Proposed prospective sequence, **not launch authority**:

- Generate and independently check the exact explicit graph/target using the
  public native-fast `apply` path, zero contexts. Save its actual fragment.
- Adopt that exact fragment manifest/interface. A selected compact or existing
  full `prepare-seal` performs one guest snapshot, no separate duplicated guest
  execute pass. Bind actual n,a, snapshot and charged costs.
- Select a threshold before preparation (for example n<=3,a=0 if the owner funds
  Q(3,0,m) plus disjoint costs and a credible wall envelope). Above threshold,
  stop cleanly after preparation and report the obstacle; do not start an
  expensive campaign merely because preparation passed.
- Only an independently selected, funded continuation may execute all required
  stages. Verify the resulting receipt through an independent installed receiver
  on the same exact capsule/journal. A future consumer may use that certificate
  as frontier without the unsealed proof history; demanded transparent bodies
  still remain necessary when computation requires them.

The suggested n threshold is an acceptance policy, **not a prediction**. Even
this tiny proof passes through the existing foundation/relation machinery.
Native speed, packet size and backend's null `segments` cannot establish n.
If the fixed guest baseline already exceeds the affordable threshold, the useful
result is a measured compact-sealer bottleneck, not a failed mathematical idea.
Changing the guest/checker relation to address that baseline is a separate
security/engineering decision, not an allowed shortcut in this discriminator.

For a prepare-first workflow meant to continue, provision the original allowance
for the prospective full threshold at initial creation; do not start with a tiny
prepare allowance and assume it can later be enlarged. If a prepare-only research
operation is deliberately selected instead, declare it terminal as an experiment
even though its product status is READY, and do not reuse it implicitly.

## Linking growth policy safely

The recurrent-cut theorem in `rollover-policy-01/THEORY.md` remains conditional:
affordable successful cuts before the replay cap yield bounded epoch cost. A
cap alone also admits refusal/stagnation. Native-fast lowers the rent/check cost;
it does not lower the unchanged zk guest's proof-production cost automatically.

A minimal successor advisor should distinguish three evidence states:

- Native-local fragment: exact inert object + local check, guest n unknown.
- Prepared exact guest snapshot: n,a known; original operation funding fixed.
- Completed verified certificate: genuine reusable cut with measured charged
  production and separate adoption/custody costs.

The unknown state may request a bounded shape discriminator, not promise an
economic seal winner. The prepared state may emit a finite continuation only
when original resources suffice under its declared bound/estimate. The completed
state supplies an observed instance, not a uniform future-cost law. Do not graft
native metadata onto the old guest-execution schema or treat a receipt-bearing
definition object as the fragment wire format. Direct definition transport and
proposition `prepare-seal` are distinct public interfaces.

For complete-route bounds L<=actual<=U, the existing minimum-upper-bound selection
and strict advantage test remain valid over the same finite comparable route
set. A sealer contributes a defensible upper envelope only if all relevant
costs, successful output contract and service premises are included. If only a
historical estimate is available, recommendations are useful heuristics, not
proved amortization. The preceding `GROWTH-UNIFORMITY.md` constraints still apply:
new plan/answer construction and discovery are charged causal actions; a tiny
scripted proof cannot be presented as autonomous capability growth.

## Evidence versus near-term decision

Actual old source-free preparation: n=41,a=1; two workers; 1.96875 inner worker
CPU; 17.625 inclusive public Job CPU plus 0.484375 disjoint wrapper CPU; 601.96875
conservative charge; no proof stages and no certificate. Earlier genuine public
child preparation+production cost 42781.21875 known nonoverlapping CPU seconds;
the earlier AB campaign cost 69638.921875, including retained failures/recovery.
These values refute an assumption that certificate production is free, but do
not calibrate a different tiny input or prove any universal cost lower bound.

Recommended order: finish exact compact sealer closure/source review; repair
the advisory evidence-state distinction and no-progress guard in a separately
selected successor; consider one bounded new shape discriminator only if its
outcome can change the final package/release decision. Do not spend the remaining
milestone interval re-running old proofs or chasing a large campaign solely for
a passing headline. A deployable guarded sealer can be a substantial new core
capability while full low-cost recurring cuts remain explicitly unqualified.
