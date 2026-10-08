# Next useful-reuse gate: hierarchical chunk summaries

2026-09-22. **Prospective protocol, NOT RUN.** This note proposes one bounded
same-machine, real-Lean discrimination on a fresh installation of the now
locally qualified one-pass peer candidate. It authorizes no
launch, source change, result promotion, or inference of useful growth. The
prior [matched pair](../../software/qualification/usefulness-consumers-01/COMPARISON.md)
and its [peer consumer audit](../../software/qualification/usefulness-consumer-B-01/OUTCOME.md)
are evidence of one checked dependency, not a second trial or a speedup baseline.
The [goal](../../GOAL.md) distinguishes mathematical acceptance, availability,
usefulness and sustained accumulation. The one-pass
[delivery statement](../../deliverables/2026-09-22-onepass-peer-candidate/RESULTS.md)
records its subsequent qualification, which does not prequalify this gate.

## Question and mathematical endpoint

Can a fresh agent, given a formal target and ordinary product/API documentation
but **no answer name or ID**, discover a previously checked peer theorem, admit
it locally, and use it to publish a distinct, portable result within a fixed
practical budget? What changes when that peer theorem is absent but the same
agent has the ordinary Lean library, local proof construction, and the same
background corpus? This is a *demand-driven task-level* question. It does not
ask the network to judge human intention or impose a system-wide task list.

Use exactly the previously checked right-fold definition `R` from
[UsefulnessVocabulary.lean](../../software/drafts/UsefulnessVocabulary.lean).
For `A : Type u`, `op : A → A → A`, `e : A`, assume associativity and left and
right unit laws, with no commutativity and no specialized carrier. For
`blocks : List (List (List A))`, define only for the evaluator's statement
display

```text
flatRows(blocks) = List.flatten (List.map List.flatten blocks)
blockSummary(block) = R A op e (List.map (R A op e) block)
```

The exact new theorem to submit and publish is

```text
R A op e (flatRows blocks)
  = R A op e (List.map blockSummary blocks).
```

The packet must spell both sides in supported Lean 4 source using the checked
receiving name of `R`, with the quantifiers, universe and three laws exactly
as above. No locally added axiom, extra hypothesis, specialized `A`, weakened
conclusion, or redefinition of `R` qualifies. The evaluator preflights the
*statement alone* through the installed source/description path, checks that
it elaborates in the declared fragment, and freezes its canonical proposition
DAG and derived expected theorem type before either consumer starts (as in
the prior target-conformance comparison of definition value with theorem type).
This preflight is not a proof. If elaboration/export
fails, record a target-fragment failure and redesign in a separate proposal;
do not repair the statement mid-arm. A reviewer should also check that the
generic goal is not solved by definitional reflexivity under abstract `blocks`.

This equation certifies two-level aggregation: first summarize elements within
each row, then summarize rows within each block, then reduce the block
summaries, obtaining the same answer as flattening all rows and reducing all
elements. It is a distinct statement, not a renamed proof
of the old `R(flatten chunks) = R(map R chunks)` theorem. It is plausibly
derivable from that theorem by (i) applying it to `map flatten blocks`, and
(ii) inducting on `blocks` to replace each `R(flatten block)` with
`R(map R block)` using the old theorem on that block. That is a feasibility
argument, **not** a supplied proof script, proof hint in either packet, or an
assertion that the existing source exporter will accept a particular agent
proof. The local-only agent may derive it directly or use ordinary library
facts. A noncommutative instance such as list concatenation illustrates why
the specification must not quietly add commutativity; it is not the theorem's
restricted carrier.

## Fixed information boundary and matched arms

Retain the seven historical genuine package entries from
[the qualified previous corpus](../../software/qualification/usefulness-corpus-01/OUTCOME.md),
including the append/fold law, plus the prior consumer B's independently
accepted and published chunk theorem as an **eighth** entry. Do not prepare
65 new Lean packages or an inert page-full of decoys to make the search look
large. Eight complete bundles should first be revalidated, byte-pinned and
checked against the unchanged 64-MiB view and per-operation limits; this fit
is a prelaunch check, not assumed from file-count arithmetic. The corpus
preparation author freezes actual ordered descriptors, canonical packages,
catalog/page/bundle bytes and service grant before agent dispatch. The
historical result is not relabeled a new producer contribution. Any static
fixture service is disclosed as a fixture, not falsely described as a new
product-node publication; the receiver still performs ordinary `peer_acquire`
and independent native `admit`. Prefer the candidate's owner-authorized
exposure only if it can offer the exact historical result through documented
ordinary or replica custody operations without database surgery or rewriting
the old proof. Pick **one** delivery path before launch; do not switch after
seeing an outcome.

Run two fresh, no-history, sequential consumer agents with the same model,
effort, tool allowance, checked `R` onboarding, Lean runtime/foundation,
package/context ceilings, public API documents, target, and deadlines. Use a
single frozen random byte to choose order. The control sees the same seven
background entries but **not** the eighth theorem; it retains unrestricted
ordinary source/library lookup and may author an equivalent theorem locally.
The treatment sees all eight through an unranked paged peer catalog and may
also solve directly. The treatment's extra genuine entry means catalog work
is not byte-matched: this gate can test bounded task advantage or usable
reuse, not isolate remote-discovery overhead against already having the same
theorem locally. A direct-local comparator is a separate later arm. Do not
reveal the eighth entry's title, identity, page,
position, proof, prior transcript, or evaluator's rationale. No filter query
containing a hidden result ID is placed into a consumer packet. Consumers
derive all query choices and selections from the formal target and returned
public metadata. The operator forwards exact agent-authored requests and
returns exact replies, without mathematical repair, suggested names or
unrequested admission. Public `find`'s local exact-symbol option does not
secretly become remote search: remote selection uses the existing paged
`peer_find`/continuation and optional `peer_acquire`; locally indexed `find`
may be used only on entries the agent has ordinarily acquired.

Use separate fresh node state/scratch trees and separate service allocations,
not copied accepted databases. Both receive the same actual canonical `R`
package and fresh `admit` during identical common onboarding; compare their
checked `R` identities, type/body and context contents before dispatch. No
agent may read prior consumer sources/results, evaluator corpus-order maps,
other arm files, research notes, or conversation history. Permit only its
packet, its own responses, the installed API and selected Lean library source.
These are cooperative restrictions, **not OS-enforced secrecy** on the shared
Windows host; record complete exposure transcripts and classify discovered
cross-arm/evaluator leakage as invalidation, not as agent discovery.

## Exact acceptance and useful-output equivalence

For either arm, completion means ordinary owner-authorized `submit` with the
frozen target as the selected theorem root, successful canonical candidate
capture, fresh native replay, inverse export and replay, followed by ordinary
`publish` at the returned current snapshot. Bare compilation, a proposition
definition, an acquired package or a local `admit` is not completion. The two
accepted theorem **types** must equal the preflight target canonical type
including foundation, universe levels, all binders, the exact `R` reference,
and both conclusion sides; proof terms/CIDs may differ. An independent audit
compares the complete type DAG and source-capture-to-canonical mapping, not
`typeText`, declaration spelling, or a displayed equation alone. It verifies
every referenced package and old context under the receiving checker, all
reachable proof nodes, native candidate/inverse records, actual publication
binding, request replay records, source bytes, and terminal process receipts.
Any `sorryAx`, extra axiom, unsafe/partial escape, unsupported source kind,
false package metadata, or missing required closure fails acceptance.

There are three deliberately separate positive labels:

1. **Exact mathematical endpoint:** an arm publishes the theorem above within
   its budget. This may be achieved without a peer.
2. **Substantive peer reuse:** in addition, treatment selected the eighth
   entry through its returned remote handle, acquired it, freshly admitted
   it, and its published proof has a reachable proof-producing application of
   that exact prior theorem to an appropriate block or outer chunking. Mere
   presence in context, source text, a type, an unused let, or a catalog row
   does not count. This does not assert logical indispensability: the control
   may prove the same result independently.
3. **Returned reusable contribution:** treatment's new theorem is ordinarily
   published and, in a separately budgeted finite service check, offered by
   its actual product node and freshly admitted by another empty consumer
   from exact bytes. This checks that the output re-enters the commons, not
   that a later autonomous agent has found a use for it. A subsequent third
   agent producing a distinct nontrivial result with this theorem would be a
   separate stronger growth gate, not silently credited here.

Count both arms' completion equally. An arm that proves the result directly
does not fail just because it did not cite the peer. If both complete, compare
the identical portable outputs and full costs; do not declare the treatment
better because its source is shorter or its CID is new. If the treatment
alone completes within equal limits, report one bounded task advantage with
model/order confounding, not a population or causal speedup. If the control
also completes comparably, the peer may still have demonstrated optional
usable reuse, but no comparative advantage. If neither completes, distinguish
proof difficulty, source-fragment failure, interface failure and time/resource
exhaustion from unsafe mathematical acceptance.

## Frozen execution envelope and accounting

Reuse the prior matched trial's small policy as a **proposal requiring an exact
prelaunch freeze**: 45 minutes dispatch-to-publication per arm; at most 24
post-onboarding ordinary `manage.py request` calls (including `info` and
`preview`), two theorem submissions, three admissions, eight acquisitions and
two separately bounded read-only `manage.py inspect` calls; no renewal, repair by root,
replacement arm or after-the-fact extension. Select context-package limit 16
so the five common packages, checked `R`, background candidates actually
admitted and eighth candidate cannot exceed it silently. Use one prospective
standalone static-fixture service slot per arm, at most 600 wall seconds (the
product's session maximum), 120 service CPU seconds, 128 connections and
256 MiB sent. Start that slot only after the agent has authored its first
peer request; retain the exact authored request, wait for ready, then forward
its unchanged bytes once. Both agents are told this finite access policy in
advance, without identifying the hidden result. Readiness time, startup and
operator delay remain inside the unchanged 45-minute dispatch deadline and
full cost account. Do not restart or renew the slot, add a second grant, or
delay its clock after readiness. If acquisition or later lookup is blocked by
expiry, classify availability-window exhaustion; that negative result does not
diagnose relevance, discovery strategy, proof ability or comparative advantage.
A theorem acquired and admitted while the slot was live may be used and
published after expiry, within the arm's ordinary deadline. This gate does
not claim 45-minute continuous availability or sustained operation; a later
separately frozen test may investigate multi-session availability if this
bound is decisive. Preserve ordinary per-call supervision and the existing
view/connection/byte bounds. These numerical
ceilings may be changed **only before** either arm, based on a documented
preflight fit, with both arms' bound then identical.

Before dispatch freeze a distinct loopback contact/alias and exact seven- or
eight-entry view for each arm. The operator queues the first agent-authored
peer request, launches its one supervised standalone service, verifies fresh
readiness and the pinned catalog, then forwards that request exactly once.
The 600-second service clock begins before full view authentication; record
the remaining seconds at readiness and predeclare a minimum usable remainder
after measuring the frozen fixture's startup. Failure to meet that minimum
stops the arm as setup/availability evidence, not a reason to restart it.
If no peer request is made, launch no service and still account for the
preparation. Retain the terminal service receipt even when proof/publication
ends before the slot. Report occupied service wall time, idle time, disjoint
service CPU and egress separately from dispatch-to-publication time.

Observe at most 600 disjoint enclosing-Job CPU seconds per arm after common
onboarding, including its own service Job, checked after each completed call.
This is an observed qualification ceiling, **not** a hard aggregate quota;
an in-flight overshoot is retained and makes an endpoint out-of-envelope.
Do not add nested Lean-stage CPU to its containing public Job CPU or the
service worker's internal CPU to its containing service Job. Account separately
for owner/operator/agent CPU where measurable; model tokens and any unmetered
agent compute are unknown, never zero. Keep common onboarding in cold totals
for both arms. Charge corpus construction, previously spent producer work,
preflight, packaging, service startup, failed setup and static fixture work
separately, with an explicit amortization horizon if reporting marginal use.

Before launch freeze a retained-tree ceiling (provisionally 1 GiB per arm,
including scratch/evidence), source and corpus pins, each package's actual
framed transfer bytes, service egress/grant, and peak-commit cap. Check the
tree ceiling after each operation and classify overshoot, without pretending
it is mid-operation enforcement. Report, for each arm, cold and marginal
dispatch-to-endpoint wall time, disjoint public/hosting CPU, native stages,
requests/failures, downloaded catalog/page/bundle bytes, package checking and
admission, source attempts, conservative reserved MiB versus observed disk
bytes, final retained bytes, peak memory, and quiescent processes. The finite
service period, readiness wait and every operator pause remain in elapsed time.
Sequential execution avoids competing Lean jobs but does not remove model
stochasticity, cache warming or unrelated host-load confounding. One pair is
not a statistical performance study.

## Decision and stop rules

Prelaunch stop: the selected one-pass package or its audits no longer match
their exact pins; statement-only preflight or exact onboarding fails; the
eighth theorem cannot be offered
under the selected legal product/fixture path; an eight-entry authenticated
view does not fit unchanged bounds; or frozen prompts/service/CPU/retention
limits and independent audit roles are missing. Do not repair these during an
arm. Preserve each consumed preparation and its exact reason.

In-run stop: uncertain ordinary outcome, incompatible context/foundation,
malformed or altered bytes, failed fresh native admission, wrong canonical
target, contamination, elapsed deadline, observed CPU or retained-tree
overshoot, exhausted grant, or a failed/quiescence-uncertain service ends the
affected arm. Record late bounded calls, partial outputs and all charges; do
not restart with another request ID or a new arm to rescue the comparison.
If the peer result is unavailable or omitted, that is a real availability or
selection result, not evidence that the theorem has no mathematical value.

The strongest possible positive report is one **engineered finite** instance
of independent formal selection, trusted local checking, substantive theorem
reuse, a distinct checked output and return availability at an observed cost,
alongside a fair local-library/withheld-result comparison. The endpoint is
mathematically nontrivial and structurally two-level; its test is not another
reflexivity-wrapper or a manually supplied proof name. But the evaluator chose
this related target, the eight-entry corpus is small and curated, the agents
are cooperatively isolated, and the host is shared. Therefore even a pass does
not prove novelty, broad retrieval quality, comparative speedup, sustained or
exponential useful growth, independent-host operation, or global availability.
Repeated held-out tasks and a later agent's actual use of this returned result
are necessary before stronger reciprocal-growth claims.
