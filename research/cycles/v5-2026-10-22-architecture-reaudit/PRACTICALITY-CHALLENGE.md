# Practicality challenge: build a useful commons, not a universal proof service

2026-10-22. Independent reviewer: `commons_practicality_challenge`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source/evidence/theory only. No runtime, experiment, build, Git mutation,
product edit, certificate production or policy adoption occurred.

## Decision

The synthesis is directionally right but initially too constrained by a universal
cold-import ideal. Under the user's newly explicit permission to compromise for
real usefulness, the primary product should be a **decentralized independently
checked library with durable local knowledge and incremental exchange**.
Succinct cold imports should be a valuable supported service class, not the
condition that determines which mathematics the entire commons may contain.

This recommendation changes a performance/service requirement, not mathematical
truth. It explicitly relaxes “every arbitrary cold first use avoids its proof
closure” to “ordinary first onboarding has an explicit finite cost; subsequent
use is incremental; strict thin-client imports still require suitable evidence.”
The earlier strict requirement must remain documented as a distinct profile,
not be silently called satisfied by the new ordinary workflow. Root/user adoption
of this scope change remains a separate decision; this note only recommends it.

The highest-payoff next question is **whether an ordinary useful Lean development
can survive and grow across sessions through our public native path without a
new cryptographic proof**. The answer is not yet established. A universal new
proving backend should not be the prerequisite for answering it.

## Why the objective should change the architecture's center of gravity

Human benefit comes from reliable access to reusable mathematics with tolerable
total costs. It does not require every contributor to service a hypothetical
fresh phone that knows no previous mathematics, nor every reader to know the
whole world. Established agents will normally have relevant local libraries.
Whether this expectation holds for the intended workloads needs evidence;
it is not a theorem about all agents or all mathematical dependency graphs.

A protocol that refuses almost every affordable ordinary contribution can be
sound yet useless. A protocol that verifies tiny examples succinctly but cannot
consume substantial existing Lean work can be technically sophisticated yet
contribute little. A protocol whose bookkeeping overwhelms elementary reuse can
discourage exactly the reciprocal contributions it is intended to enable.
These are central architectural failures, not merely usability polish.

The root synthesis properly rejects universal cheap completeness, voting about
truth and certificate production by every author. It should equally reject
universal cold succinctness as the primary adoption bottleneck when a cheaper
independently checked ordinary lane can meet useful workloads.

## Compare three concrete product choices

| Choice | What the recipient relies on | Main benefit | Explicit compromise |
|---|---|---|---|
| Persistent independently checked library | Local checking of the selected closure, then protected local accepted state and checked updates | Broad ordinary exchange with no per-result cryptographic bill | First onboarding, new specialties and missing cached dependencies may be expensive |
| Hybrid ordinary library plus selected succinct cuts | The same local route, or verified portable evidence under an adopted checker/profile | Cheap cold entry at valuable boundaries; ordinary contributions remain cheap | Certificate service needs justified funding, capacity, availability and supported semantics |
| Opt-in socially trusted snapshot | A chosen distributor/operator's correctness claim about a finite committed library | Very fast bootstrap under familiar software-distribution assumptions | A compromised or mistaken distributor can inject false mathematics into downstream reasoning |

Recommend the second, with the first as its dependable default workflow. Retain
the existing cryptographic capability without commissioning more tiny seals.
Do **not** implement the third merely because it is easy to describe. It adds
policy complexity and changes the independent-verification promise. If a future
operator chooses it, label the assumed root, retain that dependency in every
derived judgment, and prevent silent promotion into the independently checked
profile. A signature authenticates the operator, not mathematical correctness.

Decentralized operation does not require every node to offer every assurance
class. It requires that no unique provider be indispensable and that recipients
can identify what evidence they actually obtained. A public index may describe
an ordinary result even when no supported succinct warrant is available.
Existing publication starts from local admission; no new unrestricted arbitrary-
claim publication mechanism is needed to obtain this architectural benefit.

## Honest amortization and specialty onboarding

Let a recipient independently check a relevant finite base once at cost B.
For n later uses with stable accepted semantics and no forced rechecking,

    total cost = B + sum(new checked work + acquisition + operational overhead).

Thus the base contribution to average cost is B/n. This elementary argument
requires protected persistence, compatibility and actual reuse; it says nothing
about how small B or the new work is. It ceases to apply without adjustment after
eviction, policy withdrawal, incompatible upgrades or an unrelated specialty.

Specialties should be finite versioned dependency sets, not authorities over
truth, mandatory taxonomies or isolated competing foundations. A consumer can
select multiple compatible sets and their exact common dependencies. A shard
label never establishes that its cross-shard requirements are satisfied.
The protocol must preserve all required definitions and computation semantics.

The useful scaling assertion is that a node's ordinary work follows its selected
uncached closure and new contributions, not that it synchronizes with the entire
network. Some selected closures can nevertheless be enormous. Cross-specialty
fan-out is a real workload cost; neither sharding nor local caching proves it
small. If it exceeds the selected budget, offer another evidence route or defer.

This is a more credible practical contract than making a universal cryptographic
service absorb arbitrary growth before users may benefit from ordinary sharing.
It does not erase the separate strict cold-access obligation where that profile
was actually requested. Already available certificates can seed local caches.

## Two blockers may dominate the next prover optimization

### Ordinary Lean interoperability

The native path is not a hidden full-Lean escape hatch: `delta/native.rs` directly
includes `modules/receipt/src/relation.rs`. The latter requires exact foundation
rows and sets `nat_extension=false` and `string_extension=false`. Ordinary Lean
frontend success is not independent admission: imported interfaces are authoring
assumptions, discharged only by the adopted checker/evidence route. The guide
also records that authoring may need a larger semantic closure than lazy checking.
These costs and the unresolved full correspondence do not disappear with a receipt.

We should not make the entire network's mathematical vocabulary the intersection
of “useful Lean” and “currently convenient to prove inside this zkVM.” Broad native
checking and restricted succinct checking may be separate supported profiles.
Any cross-profile transfer needs exact semantic correspondence or a new checked
translation, not shared theorem names or reused success flags. This is a design
option, not evidence that full native Lean support already exists.

Before tying persistent acceptance exclusively to receipt-image journals, define
the kernel-checked exchange/assurance boundary: exact semantic judgment, policy
and evidence route are distinct fields, while old journals retain their exact
meaning. Determine whether the current profile supports one useful existing Lean
family unchanged. If not, compare a pinned ordinary Lean-kernel profile with
expanding the custom relation. Do not reinvent all Lean solely for a proof backend.
Kernel-level validation is the target; executing peer source or blindly loading
peer `.olean` files is not hostile-input validation. Design this boundary before
the cache schema, so persistence does not accidentally enshrine a restricted VM.

### Recurring operational overhead

The saved U-to-V operation cost 84.5625 known CPU seconds. Its nested author,
native-check and two receipt-check observations sum to 1.53125 CPU seconds.
The remaining 83.03125 seconds are not thereby proved unnecessary: their work,
measurement boundaries and security functions need a causal source account.
But this is enough to reject “faster core verification alone makes routine use
fast.” Repeating large installation validation for each tiny task may be a much
larger practical barrier than the tiny native delta check.

The retained native complete-closure component checked a three-module fixture in
1.3125 enclosing known CPU seconds. That is not a matched full-workflow result
and it exposes neither semantic authoring nor durable acceptance. It demonstrates
a real non-cryptographic building block, not the finished practical lane.

A trusted local accepted store or bounded service can amortize safe startup and
accepted mathematics. Choose one minimal mechanism first. Fresh resource grants,
crash-atomic promotion, revocation and local integrity remain necessary; spent
handles are never serialized as authority. Do not multiply daemons, cache layers,
economic schedulers and new protocol types before this seam works publicly.

## One next falsifiable slice, not another general experiment campaign

Select **one existing ordinary Lean library family** with an inductive structure,
its transparent operations and a genuinely reusable lemma, rather than another
handcrafted equality-composition-only example. The local baseline and sharing
route must have the same initial math, caches and tools. A peer-only lemma is
not donated to the isolated baseline. Freeze the intended mathematical endpoint
before determining whether the current adapter happens to accept it.

First perform a source-only compatibility and acceptance trace. Answer precisely:
which existing profile checks each declaration; what data authoring needs;
which public operation can expose native accepted members to it; what survives
closure; and what new trusted persistent state would be introduced. Stop the
design if it requires unchecked axioms or silently trusted peer compilation.

If that trace is feasible, the single consequential implementation milestone is:
independently onboard the finite base once, close/restart, discover an unfamiliar
peer lemma, acquire/check only the additional needed evidence, author a substantive
extension and return it through existing publication. No new succinct proof is
required. The persisted base must not grant renewed CPU or survive withdrawal
unchecked. One deliberately altered dependency must be rejected, not implicitly
treated as an old accepted module. Existing completed tests are not replayed.

The slice succeeds only with an ordinary documented public entry point, preserved
mathematical endpoint, no ancestry replay of the already accepted local base,
and a causal full-cost account. Prospective budgets must come from the source
trace and ordinary baseline, not be enlarged until the candidate passes. Failure
identifies whether compatibility, native integration, persistence or controller
cost is the actual next obstacle. It does not justify another large proof run.

This would distinguish a useful incremental mathematical library from a collection
of impressive but expensive component demonstrations. Afterward, select a cold
certified cut only where its extra capability or amortized savings justify cost.
The whole v5 release, broad-host deployment and sustainable growth remain open.

## Evidence consulted and disposition

- Root `ARCHITECTURE-REAUDIT.md`; adjacent `DEMAND-PROTOCOL.md` and
  `CERTIFICATE-ECONOMICS.md` (including updated practical-compromise discussion).
- `notes/V5-ARCHITECTURE-GUIDE.md`, current source navigation and
  `software/v5/native_closure/README.md`.
- `../v5-2026-10-20/TYPED-RENEWAL-ACTUAL02-OUTCOME.md` for full and nested costs.

These support the observed gaps and costs. The practical-default recommendation,
broader native profile and prospective slice are proposals, not shipped features.
