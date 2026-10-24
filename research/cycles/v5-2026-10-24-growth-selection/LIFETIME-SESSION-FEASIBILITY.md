# Finite checked sessions: feasible event rule, limited payoff

2026-10-24. Source/theory analysis by `growth_release_thesis`, under
GROWTH-LIFETIME-DECISION. No code, runtime, protected-state or Git changes.

## Decision

A **bounded live checking session is sound in principle**, but is not a small
cache patch. It needs an explicit live completion event replacing the current
process-exit warrant, a protected incremental context, and one original session
reservation. It is worth considering only for an operation sequence that needs
intermediate durable admissions and therefore cannot use the existing batch.

Do **not** implement an atomic-final-commit session merely to amortize restoration.
When all new units fit one existing batch and no intermediate admitted root is
needed, `admit` already restores once, checks dependent units and commits once.
Ordinary approved Lean authoring can develop the finite result before that call.
An adaptive local investigation does not itself prove a need for durable network
admission between every local proof step.

Even a live session does not remove the long-run quadratic restoration pattern
if it merely groups a fixed number of growing-root operations per session. It
can substantially reduce its coefficient in a real operating region. It cannot
make an oversized parent fit RAM or replace demand-scoped context design.

## Actual current boundary

- `OrdinaryWorkflowWorker.extend` restores its complete selected parent once,
  rebuilds allowed names, decodes up to 1,024 ordered units, and calls the existing
  atomic checker/writer. It does not run arbitrary source or extensions.
- `CheckedExtension.checkBatch` genuinely calls `addDeclCore ... doCheck := true`,
  checks grounding/generated inventories, and returns the actual new environment.
- `LocalSnapshot.WrittenExtension` already carries that environment as internal
  continuation state. `checkAndWriteChunk` writes only the returned added records.
  The writer is private; an arbitrary claimed ConstantInfo array is not authority.
- `ordinary_admission._execute` currently waits for a clean actual process-tree
  exit, checks the exact report/artifact/request, then calls `_commit_checked`.
- `PortableCatalog` has one live grant, fixed ordered input identities, parent,
  root and deadlines. Its owner lock excludes another ordinary catalog writer.
  Activation/withdrawal are checked again immediately before its transaction.

Accordingly, reusing a saved report or returning `checked=true` over an ordinary
socket cannot be substituted for the present authority. Keeping the child alive
without changing the controller rule is not an implementation of the proposal.

## Precise candidate live-event rule

This is a possible finite local protocol, not an implemented new authority.
Its trust premise is the same approved checker/controller code and protected
storage as ordinary admission, plus correct implementation of the following
state machine. No remote identity or cryptographic certificate supplies it.

1. **Open.** The controller holds the owner lock, fixes installation/support and
   activation identities, authenticates parent K0 once, and starts one owned,
   supervised worker with a private inherited channel. Fix a fresh session nonce,
   maximum rounds, cumulative input/output/name/unit bounds and absolute deadline.
   The nonce separates executions; it is not a proof or secret needed for truth.
2. **Prepare i.** Only one request is outstanding. The controller stages immutable
   inert evidence, checks exact import-symbol bindings against its current map,
   reserves output/operation capacity, and issues the ordered unit identities,
   actual byte hashes, grant/root/parent bindings and sequence i. No peer command,
   source text, path referral or generic code-execution verb is accepted.
3. **Check i.** The fixed worker requires its actual current environment to be
   the session's immediately preceding checked state. It runs the existing checker
   on the new units, writes a fresh delta, closes all artifact handles, and emits
   one bounded completion frame bound to every request field and the exact output
   inventory/bytes. On any parse/check failure the first design aborts the session;
   it does not keep a possibly ambiguous successful prefix in service.
4. **Promote i.** The controller obtains the frame from that live owned process,
   not a report file, and checks its sequence, exact request/result binding,
   resource state and retained eligibility. It copies/finalizes the chunk into
   protected immutable storage and verifies the exact bytes. The worker must not
   retain authority to rewrite any promoted artifact through its protocol. The
   existing catalog transaction remains the mathematical-state linearization point.
5. **Acknowledge i.** Only after durable commit does the controller expose the new
   admitted root or acknowledge advancement. Then update the protected incremental
   binding map and permit request i+1. The worker may hold the checked environment
   before acknowledgement, but it cannot accept another request or announce a
   durable root before the controller's commit acknowledgement.
6. **Close.** End by the original deadline/round/resource bound. Reap the worker
   and close its Job. Clean final shutdown is still required for normal session
   completion, but it is no longer the sole evidence for each earlier commit.

The required artifact immutability is a source/ownership invariant, not supplied
by the nonce. Copying to a controller-owned undisclosed path can prevent accidental
rewrite through the issued path; it is not isolation from hostile same-user code.
An actual OS isolation policy would strengthen that boundary separately. Do not
claim that final kernel checking can undo corruption of approved checker/storage.

**Soundness argument.** Assume K0 genuinely warranted and each completion event
really comes from the pinned worker's specified successful branch. Induct on
committed rounds. Exact input binding and the unchanged checker extend warranted
Ki-1 to checked Ki. Exact immutable snapshot binding plus the guarded transaction
records that same extension; the new map adds only those checked names. The live
event is the controller's observation of this branch, not a claim portable to
other owners. Each independent recipient still performs its own acceptance.

This is an elementary implementation-refinement obligation, not its formal proof.
It must be reviewed before coding. An arbitrary message saying success fails the
premise. A child that can skip checking, mutate earlier artifacts, substitute a
different request, or reuse an old completion frame invalidates the argument.

## Cancellation, crash, withdrawal and reservations

- One session-level Job limits aggregate child CPU, elapsed time, memory, process
  count and communication. Idle dialogue consumes the same wall allowance. Each
  round deducts from cumulative input, log, staging and output budgets; no grants
  or heartbeat values renew the parent allocation.
- Reserve a finite total output/operation allowance before starting. Existing
  per-call limits remain ceilings as well; total new stage-two names must fit the
  unchanged checker limit. Failed inputs, unfinished chunks and retained evidence
  are charged, not made free by cancellation. Controller CPU needs its existing
  cooperative checks or an enclosing hard Job as explicitly selected.
- Cancellation/expiry stops further requests, terminates and reaps the owned
  worker, abandons only the current uncommitted grant, and preserves evidence.
  Previously committed roots stay mathematical results under still-supported
  assumptions; a later timeout does not make their proofs false.
- Check activation/support eligibility before every request and immediately before
  each commit. Withdrawal stops the session and refuses any pending promotion.
  Existing retained results remain subject to the established withdrawal policy;
  the session must not make them usable through a stale in-memory cache.
- If the worker dies before a round's commit, that round is not accepted. If the
  controller dies after commit but before acknowledgement, the transaction is
  authoritative and the whole live session is discarded. A new session restores
  committed state normally; it never revives old messages, grants or deadlines.
- Uncertain process cleanup quarantines further owner operations, as today.
  Recovery examines actual committed records and immutable artifacts, not a saved
  `ready` frame. A new session consumes a separately deliberate allocation.

The state machine serializes local owner changes. Concurrent writers, multiplexed
clients, reconnecting resumable sessions and networking are not part of this small
candidate. They would materially enlarge its assurance and implementation scope.

## Cost envelope and the stage-two obstacle

Let k be admitted rounds, Ki their growing contexts, L(K) the charged context
authentication/load/name-initialization cost, and di each round's added names.
Retain actual proof/conversion, evidence, copying, commit and communication costs
separately. They are not constants merely because the checker interface is small.

Repeated calls pay `sum_i L(Ki-1)`. The proposed session pays L(K0) once plus
incremental binding work and live-protocol/reservation costs. However the current
`checkBatch` calls `stageTwoNames` before and after each round: it scans all names
already added during this session. If D is total session-added names, that term
is bounded by a constant times `k*D`, not by D alone. Equal small additions give
a quadratic term in k. The 131,072 stage-two cap still applies.

The comment in CheckedExtension explicitly anticipates restoring accepted prior
chunks into stage one before a subsequent large batch. A naive resident loop
does not do that. Do not claim linear lifetime work from retaining the environment.
One minimal finite-session design can keep this checker unchanged and charge
the bounded `k*D` term. Eliminating it needs a separately justified incremental
generated-name invariant and final census; that is a checker change, not a cache.

There is a defensible benefit region: intermediate durable results are actually
needed, K0 is large relative to the bounded new D, and avoided repeated restoration
exceeds session protocol, retained-memory/idle-time and extra stage-two costs.
This condition can be analyzed from source and selected histories; it does not
require an artificial theorem or claim a Lean-import timing constant.

Against **one existing aggregate batch**, both routes pay L(K0) once. The batch
performs one final stage-two census, has no live event protocol, and keeps the
existing clean-exit authority. There is no established work advantage for a session
if the same final units fit that batch and intermediate durable roots are unused.
Delayed or failed final publication may change a real workflow, but must not be
invented solely to handicap batching. Aggregate batch limits are not silently raised.

For long histories cut into fixed-size sessions, each restart still pays the
then-current L(K). Sessions offer amortization within a window, not independence
from ever-growing local history. They are a complement to bounded/demand-scoped
contexts, not a complete solution to the project's scale requirement.

A stronger existing comparator is **earlier-parent re-admission**. The public
native owner passes `--parent-root` to `baseline_intake.intake`; that implementation
accepts any eligible protected root and checks each complete bundle batch above
the selected branch. Thus a retained complete dependency bundle can be re-admitted
above a smaller known parent, paying real initial rechecking to avoid later
unrelated history. No global checked flag substitutes for missing local premises.
Root/profile/name compatibility and all batch limits remain. Minimal extraction
of an arbitrary retained closure is a separate convenience not supplied by this
fact. Compare sessions against this existing route plus ordinary batching, not
only against repeatedly extending the largest available branch.

## Minimal source delta, and what to select now

If intermediate durable admission is selected as a real supported workflow,
the minimal implementation crosses **three existing responsibilities**:

- A fixed finite successor worker retains the actual checked environment and
  allowed-name set, uses the unchanged checker/writer, and implements the strict
  request/completion/acknowledgement state machine. No arbitrary local Lean source
  execution occurs inside this acceptance worker.
- A successor admission controller owns one supervised interactive process and
  budget, immutable evidence, exact live frames and artifact finalization. Current
  blocking `supervise` plus parsing saved output cannot supply this event rule.
- A successor catalog session handle maintains current bindings incrementally,
  binds them to the locked root/activation/support, and consumes one finite
  reservation. Calling current `context`/`reserve_extension` unchanged every round
  would rebuild the history/map and retain the very overhead being targeted.

No Lean calculus, wire evidence identity, peer protocol or public global daemon
is required. Nevertheless all three are acceptance-critical code, so a prototype
must not be commissioned as a harmless performance tweak.

**Selection recommendation:** retain batching and earlier-parent re-admission;
reject a new atomic session as duplicative. A live session has no selected
implementation gap until an actual supported history needs intermediate durable
roots and still pays excessive restoration after those existing routes are
allowed. For a known complete retained bundle, the smaller-context route has no
missing admission API. Arbitrary-closure collection may later justify a bounded
convenience tool, not a daemon. The full growth goal remains open.

Sources read: GROWTH-LIFETIME-DECISION; the retained ORDINARY-PRACTICAL-COST result;
OrdinaryWorkflowWorker.extend; CheckedExtension.checkBatch/stageTwoNames;
LocalSnapshot writer/restoration/continuation; ordinary_admission budget/admit/
execute; PortableCatalog context, reservation, eligibility and commit; native owner
intake dispatch and baseline_intake.intake. No new
measurement or experiment is needed to support the stated decision boundary.
