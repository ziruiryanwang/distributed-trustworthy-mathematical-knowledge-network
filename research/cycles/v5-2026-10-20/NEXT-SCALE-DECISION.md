# Next scale seam: preserve semantic work across a settled supplier failure

2026-10-20, `core_search`. Canonical guard passed. Source/theory decision only:
no implementation, runtime, product import, RAM investigation or Git mutation.

## Decision

Select **one demanded-body attempt that can return a settled unavailability
result without revoking the current mathematical operation**, after which the
caller may explicitly choose another already-authorized supplier. Keep the
same client, demand, descriptor, grants and deadline. Start with bodies only;
do not expand this increment into packet failover, discovery rerouting,
automatic retries, contact renewal or another service framework.

This fixes a present product obstruction, not a hypothetical larger test:
choosing Q in advance now works, but trying unavailable P first destroys the
operation before the caller can choose Q. Independent custody therefore does
not yet yield ordinary post-failure semantic continuation.

## Concrete source finding

1. `client/supplier_selected/workspace_evidence.py:346` sends a demanded body
   through the original acquisition object, with Q selectable explicitly.
2. `transport/clients.py:98` raises on non-200/EOF/connection failure. Its
   `_SharedAcquisition` caller settles the original budget in `finally`, but
   settlement alone does not classify an error as safe to continue.
3. `client/workspace_atomic.py:106` catches the escaping exception and calls
   `_fail`; line 436 clears warrants/caches/context and closes issuers.
4. `supplier_selected/semantic_reader.py:60` also changes to `FAILED` on any
   escaping exception. The caller cannot fulfill the same demand from Q.

**Do not implement 404-only handling.** The current ordinary HTTP provider
(`transport/http_provider.py:300`) closes the stream when dispatching a missing
body raises; it usually supplies no 404 body. A clean observed peer EOF is a
necessary outcome for this exact server. A peer disappearing before connect
may instead produce a refused connect. Existing search resilience already
demonstrates the relevant bounded transport/settlement pattern, but its route
whitelist and ticket owner are search-specific, not reusable unchanged for
module bodies.

## Principle and formal boundary

Let the live state be `(W,D,C,B,t)`: warranted mathematics W, exact demand D,
custodied semantic values C, consumed/reserved budgets B and original deadline t.
A recoverable attempt may make only this transition:

`(W,D,C,B,t) -> (W,D,C,charge(B,attempt),t)`.

It returns `UNAVAILABLE_AT_SELECTED_SUPPLIER`, not a theorem rejection, global
absence, successful custody, coverage, body token or mathematical admission.
Its refusal includes the supplier and exact requested identity. No pending
ticket/stream/reservation may remain. New request cost is at least one attempt;
unknown reply outcomes charge the full selected response reservation.

Recovery is permitted only **before successful-payload decoding/commit** and
after clean observed stream closure (or the adopted refused-connect cleanup
contract). An explicit finite per-attempt timeout is capped by the original
deadline. An acquired-stream timeout can be classified only after successful
cleanup; an unreturned connect/handshake timeout remains fatal under the
existing conservative model. Contact-policy mismatch, changed source/owner,
malformed or hash-invalid 200 payload, store/commit/readback failure, local
budget/deadline exhaustion, cancellation and uncertain cleanup remain fail-stop.
Never catch arbitrary `ValueError` or match error strings around the public
client to turn those failures into continuation.

For a successful response, retain exact descriptor-permitted hash checking,
canonical body decoding, `validate_body`, before-commit active checks and
durable readback. The mathematical gate is unchanged. A clean 404/503, EOF or
refused connection is merely a failed attempt even if a malicious server lies.
Warrant preservation follows from making no mathematical state transition;
safe continuation does not require trusting the provider's reason.

Given at most r owner-selected authorized contacts, enough residual budget and
time, and a later reachable holder Q of the exact committed body, the client
can reach the unchanged success path despite earlier settled refusals. This
is a deterministic conditional availability improvement, with at most r
attempts and total charged reply capacity bounded by the existing grant; it
does not depend on total network size. It does not guarantee the caller knows
Q, independence of holders, indefinite retention or worldwide completeness.

## Minimal source boundary

Use fresh successor paths because current supplier-selected bytes were used:

- One narrow transport helper, `transport/acquisition_resilience.py`, for a
  single `/v5/modules/body` attempt on the actual existing acquisition/contacts.
  Borrow the search clean-closure classification pattern, not its session or
  route whitelist. Bind original endpoint, policy, deadlines and both shared/
  structural counter owners; settle every reserved byte/request exactly once.
  The existing `search_resilience._response` is route-neutral and can be reused
  with its source identity pinned; its search-specific exchange/ticket flow
  cannot simply be called with a different route.
- `client/supplier_resilient/workspace_evidence.py`, a fresh overlay successor
  of supplier-selected `workspace_evidence.py`: explicit `try_acquire_body`, selected and pinned
  under the same canonical module name. It returns a narrow tagged refusal
  *inside* the unchanged `_async_action` boundary; no exception escape/recovery
  wrapper, issuer substitution or relaxed exact type.
- `client/supplier_resilient/semantic_reader.py`, with explicit `try_fetch_body`:
  on that typed refusal preserve the
  pending demand, selected packet/member, committed body map and ability to
  call again explicitly with Q; charge the helper step and any existing input
  accounting. Do not manufacture progress or alter a cached P candidate's
  recorded supplier.
- One focused test file and short API note; root owns the exact source-map
  integration. No changes to mathematical checkers, packet formats, custody
  schema, location/search protocols or saved passing evidence are required.

Do not introduce a second budget or hide work from the structural counters.
If the helper cannot maintain the existing accounting ownership without
monkeypatching or proxying exact classes, stop and present that specific source
decision before widening the transport abstraction.

The facade can call the helper using the actual existing `EvidenceAcquisition`
and its exact structural owner, then apply the unchanged `put_body`/`get_body`
readback path only on success. No EvidenceAcquisition subclass, replacement
store or modified `_async_action` is needed. Existing fail-stop methods can
remain unchanged; the new names expose the explicit continuation contract.
Move the semantic helper's `_group(data)` effect after successful body retrieval
if the refusal promises exact semantic-state preservation. Exact declarations
have a related transport boundary but add group custody/candidate creation;
they are not necessary to establish this first body-failure capability.

## Why this seam first

Unknown-contact DHT lookup already exists (`CommonsClient.find`, maintained
roles, route/descriptor tickets). Authenticated partitions and rarest-anchor
conjunction lookup already exist. Neither merits another implementation or
repeated search campaign now. The fixed 256-way partitioning is not unlimited
shard scaling, but fixing that is a new index/layout/routing profile, not a
small locally decisive seam.

The ordinary `serve_workspace` entry lacks maintained-location composition;
adding it would make fresh contributions reachable without manually distributing
HTTP endpoints. That is a valid next product task, but it does not prevent loss
of all work when a contacted custodian fails. It also brings the separate Node/
overlay installation role and lifecycle integration (the portable location
runtime checks 5,896 runtime files), which the minimal HTTP deployment omits.
Do not make this optional role a prerequisite for the body-failure fix.

Concurrent publish-while-serving would need explicit store ownership/snapshot
design rather than removing the workspace lock. A native semantic-only branch
would remain half-integrated and supplies no large-ancestry advantage. The
body-attempt seam has a direct fault-tolerance benefit in the already passing
split-custody path and does not require new cryptographic production.

## Smallest later acceptance, not execution permission

Review the precommit refusal boundary, exact counter conservation, cancellation
and cleanup first. Then focused inert controls need only establish failure-P
does not mutate live math/demand state, caller-selected Q uses the same grants,
success bytes remain content-bound, and malformed success/commit/cleanup errors
are still fatal. The one decisive integration can reuse the same retained
body/packet: let P genuinely lack that public body, attempt P, explicitly choose
Q, and reach the unchanged READY path. Do not repeat prior search validation,
already-chosen-Q controls, proof generation or a broad network benchmark.

This recommendation improves locally implementable provider-loss tolerance.
Genuine aggregate certification, deeper shard/routing scalability, full-cost
growth and final global release remain open; none is relabeled complete.
