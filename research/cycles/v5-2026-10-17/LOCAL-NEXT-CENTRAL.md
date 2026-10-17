# Next local core seam: a stale index provider must not destroy the investigation

2026-10-17. Owner: `v5_growth_decision`. Source/theory review only; root selects
implementation and any finite runtime. Canonical guard passed. Hardware/cloud
are deferred. This checkpoint changes no product, retained evidence or Git state.

## Decision

Implement **explicit, bounded search-attempt outcomes for safely settled remote
transport refusals**, exposed by a small successor of the ordinary evidence
client. The caller can then try another already authorized index provider using
the **same original grant, query, session, deadline and remaining allowance**.
No automatic retry, provider crawl, allowance renewal or mathematical relaxation.

This is the highest-payoff unimplemented core seam found that does not require
a new A receipt: the present public client cannot survive a common stale-peer
failure even when its existing discovery session already has another usable
contact and enough prepaid resources. It affects actual decentralized discovery,
not an optional reputation or attribution mechanism.

The genuine A/terminal reciprocal milestone remains central and unfinished.
This work is a useful parallel path while its local build/proof feasibility is
resolved, not a replacement v5 acceptance gate.

## Existing capability and the exact missing behavior

The ordinary client already supports owner-chosen formal feature queries,
bounded DHT/contact discovery, authenticated index offers, candidate/interval
pages, exact group/body acquisition, actual admission, atomic source-ready
imports, ordinary Lean authoring, publication and durable custody. The evidence
successor additionally supports native-delta and terminal-A target evidence.
Do not rebuild that facade, implement another ranker, or replay its passing
I-only reciprocal/atomic-import results.

The source trace is decisive:

1. `client/workspace.py:507` creates one location/search handoff from an explicit
   route plan; `search_offer` at554 and `search_page` at560 expose individual
   attempts. They use `_async_action` at106.
2. `_async_action` invokes `_fail` for **every** raised `BaseException`.
   `_fail` at435 changes the client to FAILED, clears warrants/caches/context
   and closes its owners. The mixed/evidence successors preserve fail-stop
   behavior and original-owner cleanup.
3. `transport/clients.py:SearchClient._send` abandons/charges the exact ticket
   on transport failure or non-200 response, then rethrows. The lower session
   remains capable of another call after many such failures; the outer public
   client nevertheless closes it and its mathematical owners.
4. `discovery/search_session.py:abandon` removes one pending ticket and charges
   its full reserved reply/row/hit allowances. It does not reset a session or
   claim a result. `location/workflow.py:_LocatedSearchClient._send` also settles
   an expired-contact attempt before raising.

Therefore `offer(dead_contact); offer(live_contact)` cannot complete through the
ordinary client in one grant: the first call makes the second inaccessible.
This is a source-derived reachable behavior, not a newly run failure test.

The existing candidate-session controls already passed with nine tests, including
unknown transport/non-200 conservative charging, real SQLite and memory streams.
Actual public candidate socket01 already passed unknown-SID offer plus candidate
retrieval. These results are recorded in
`research/cycles/v5-2026-10-07/ASSURANCE.md` under those named headings. They
establish reusable lower-layer behavior, **not** ordinary-client continuation.
Their underlying source remains unchanged at this review.

## Why the simple alternatives are insufficient

| Alternative | Assessment |
|---|---|
| Catch the raised exception in the local agent | Too late: `_async_action` has already revoked all client authority and closed issuers. |
| Start a new client/grant after every unreachable peer | Explicitly possible, but discards reusable live state, repeats setup/reverification and changes the finite-work accounting boundary. It is not within-grant fault tolerance. |
| Call raw SearchClient outside the ordinary client | Existing expert workaround; forfeits the unified owned lifetime/accounting boundary and is not the promised ordinary API. |
| Catch all ValueError/OSError in `_async_action` | Unsafe: these also represent corrupted pins, local storage/owner failures, exceeded budgets, broken invariants and validation failures. |
| Authenticate/rank peers first | Neither proves availability; adds peripheral machinery without repairing the concrete exception boundary. |
| Implement all acquisition/proof-error recovery at once | Unnecessary scope. Custody writes, issuer revocation, partial native work and semantic commits have different atomicity. Keep them fatal for this successor. |

## First implementation scope: only before metadata acceptance

The first successor should handle **pre-admission search transport outcomes**.
`SearchSession.accept` and all mathematical/semantic/custody methods stay
unchanged. Invalid JSON, a bad Merkle proof or a summary conflict arising inside
`accept` remains fatal in this first change. This residual single-peer denial
surface is explicit; safely continuing after arbitrary acceptance rejection
needs a separate commit-boundary argument and is not smuggled into this patch.

Recoverable cases, only after exact ticket settlement and clean closure:

- A configured, unchanged contact has expired before dial; no remote call.
- Explicit connection-refused/reset/broken-pipe conditions, or a separately
  bounded per-attempt timeout, while the original session/owner is still live.
- Peer EOF/truncation or invalid bounded HTTP framing detected in the receive
  phase, before `SearchSession.accept` is called.
- A well-framed 400,404 or503 response under the original byte ceiling.
- Existing valid `NO_OFFER`/`REFUSED` offers already return normally; preserve
  them without a second exception wrapper or fabricated empty result.

Always fatal: changed endpoint/policy/source/issuer binding, invalid local
request, owner or session deadline, global caps, unexpected local OS errors
(e.g. allocation/file-descriptor exhaustion), TLS configuration failure,
MemoryError, cancellation/KeyboardInterrupt/SystemExit, accounting/ticket error,
metadata acceptance error, dirty cleanup or unknown socket/task closure.
Do not broadly classify `OSError`, `ValueError` or exception-message prefixes.
Use narrow typed exceptions emitted at the known receive/connect boundary;
explicit HTTP parser refusals may be mapped there using a fixed local allowlist.
TLS verification failure need not be recoverable in the first scope; TLS must
never downgrade or acquire provider-supplied CA authority.

### Closure is a real source change, not a status label

The frozen `http_provider.exchange` calls `writer.close()` but suppresses
`wait_closed` exceptions. Its return/raise does not distinguish clean settlement
from cleanup uncertainty. Consequently a wrapper around that function alone
cannot establish the proposed continuation condition.

Create a small successor bounded search exchange using the existing exact
endpoint, HTTP encoder/parser/body helpers and size limits, but requiring a
bounded successful close before returning a recoverable transport outcome.
Keep connection/TLS setup validation outside the recoverable-error region.
On cancellation attempt bounded cleanup, then propagate cancellation; never
turn it into an unavailable-peer report. If close itself times out/fails,
propagate a fatal cleanup error even if the original peer error was ordinary.
The outer Job remains the ultimate process-containment boundary, not a sandbox.

## Minimal proposed source change

Root should select only these new boundaries, preserving used predecessors:

1. `transport/search_resilience.py`: new finite outcome/settled-exchange helper
   operating on the actual existing located search object's session/endpoints.
   Recheck exact original egress binding/expiry before dial, reserve one normal
   existing ticket, close the socket, abandon once on a classified refusal, and
   otherwise delegate the successful200 body to unchanged `session.accept`.
   Any acceptance exception escapes. Do not monkeypatch classes or globals.
2. `client/workspace_resilient.py`: a thin successor of `workspace_evidence`
   overriding only `search_offer` and `search_page` with explicit outcomes.
   The frozen predecessor keeps its old behavior. Inherit workspace storage
   schema and all admission/import/publication rules; copy only the narrow
   operation constructor to instantiate the new client. Bind both new source
   origins in the actual owner pins. Avoid a new `_active` override if possible:
   after the complete inherited constructor, append checked new origins/pins
   and rerun inherited `_active` before ownership transfer. If an override is
   essential, set required fields before base virtual dispatch; no temporary
   skip flag may bypass checks on a live client.
3. One focused contract source and short API addition documenting the finite
   refusal outcome, accounting and no-global-absence assurance. No new store,
   registry, routing protocol, checker, certificate, index schema or benchmark.

Caller-facing sketch, not current callable API:

```text
await client.search_offer(provider, existing caps,
                          attempt_timeout_ms=bounded_value)
await client.search_page(provider, snapshot, partition, start, limits,
                         candidates_only=True,
                         attempt_timeout_ms=bounded_value)
```

A refused outcome identifies the actual provider, one consumed ticket and a
closed finite reason category, with `mathematical_acceptance=false`,
`global_complete=false`, no candidate/coverage and no implicit retry. The caller
chooses whether to spend another already authorized attempt. The timeout is at
most the ticket and original deadline; it cannot extend either. Existing
success payloads remain ordinary authenticated metadata, never mathematical
authority. Keep reports bounded by the existing call/request/report caps.

## Safety and cost argument

Let S be the live session state, A its mathematical authority state, and t one
reserved search ticket. A recoverable refusal is permitted only if:

1. The source/owner/endpoint bindings remain exact and every owner remains live.
2. No metadata `accept`, custody write, issuer call or import occurs on this path.
3. The socket is closed (or no socket was acquired), t is removed exactly once,
   no other ticket is affected, and t's original reservations are fully charged.
4. Original session query, grant and deadlines are unchanged and global caps
   still hold. A post-settlement liveness/accounting failure is fatal.

Then A_after=A_before, no invalid metadata is promoted, and used resources are
monotone. Repeating explicitly chosen attempts within the original finite caps
does not increase the total authorized work. This is isolation of a failed
remote read, not trust in the peer or an excuse to ignore failures.

If the caller chooses a sequence containing an honest reachable provider, the
preceding attempts are only these recoverable failures, and enough original
resources/time remain, this seam permits reaching that provider. The old facade
cannot do so after the first thrown refusal. This is a deterministic conditional
capability improvement; no independent-peer probability assumption is needed.

For growth accounting, a failed attempt still costs its reservation plus actual
transport/controller work. The avoided cost is discarded local setup/live
authority and forced cold re-admission, not zero-cost search. Whether the new
capability improves total useful work depends on the workload; do not claim
positive full-cost growth or worldwide reliable recall from this local seam.

## Smallest decision-changing qualification

First source review proves the error-stage/settlement boundaries. Then one
small finite run can target only these new controls, with no Lean/prover:

- Refused configured provider followed by an honest provider succeeds in one
  actual session/client/grant. Assert no regrant, deadline change, issuer close,
  lost pre-existing live-token mapping or metadata commit on the failed step.
- Exact full reservation charging once; provider/page/snapshot/byte/row/hit
  caps remain shared. Insufficient remainder refuses rather than replenishes.
- Expired contact does not dial; changed contact/policy still fatally refuses.
- Malformed HTTP/non200 and a per-attempt timeout preserve state only after
  clean closure; failed closure/cancellation/local unexpected error is fatal.
- A valid HTTP200 with invalid authenticated metadata remains fatal, with no
  snapshot/coverage/candidate promotion; do not accidentally catch accept errors.
- One held live proof-context/token mapping survives the safe refusal, using
  existing inert owner fixtures only; this is not genuine mathematical evidence.

Reuse the already passing lower candidate/session controls. A single tiny
loopback unavailable-then-honest read would test the new actual close/continuation
boundary; no new peer-count, timing, throughput or theorem-growth campaign is
justified. Root decides whether to combine it with the focused controls under
one small allocation. No experiment or implementation was launched here.

## Source identities inspected

| Canonical-root-relative file | SHA-256 |
|---|---|
| software/v5/client/workspace.py | dbf6004d6b465eb53c6a8a4ebeff234f1e74aef1b8accebe3cac25f301ecf5fc |
| software/v5/client/workspace_evidence.py | 1bdc7dfb6058c0057eb8fe56daf0f370941d275538b6cb7ab964a455a9646f8e |
| software/v5/transport/clients.py | 640d1344824829865060712370444b5051720ce7b0a741e8efc0da8a066c6464 |
| software/v5/transport/http_provider.py | e1666a57bfc4d94e1a316c93eedee8b730edaeaf6441a5b22bc4345c32e7b3e4 |
| software/v5/discovery/search_session.py | e82c628eb75a584b33e637d4758cc9e789c3953ef4fb86b7d6e5111e3fd425cf |
| software/v5/location/workflow.py | 0e0eafd11ff601ac069aa95e5b9de3608f3d77c7f9864cf5709d900d4c25c57e |

Full v5 still requires scalable trustworthy discovery/proof reuse, genuine
recurring certificates, useful full-cost growth, availability/repair, ordinary
portable operation, security/update assurance and deployment/release decisions.
This one choice advances reliability without declaring any of those solved.

## Selected implementation checkpoint

Root selected the fresh helper and companion facade in LOCAL-RESUMPTION. The
helper `software/v5/transport/search_resilience.py` is now source-complete:
13,454 bytes; SHA-256
`e3cf6a06ab59ac28e04411de62ae225a719c6d7d21a7ec17ae3004e735a707b1`.
Public `offer` and `page` keep successful `SearchSession.accept` results intact
and return `DMKN_SEARCH_SETTLED_REFUSAL_V1` only after exact conservative ticket
settlement. Every call uses the original located client, query, endpoint policy,
session, clock, deadline and finite allowance. The owner serializes operations;
concurrent/pending raw-helper calls are refused. No metadata acceptance error is
softened, mathematical authority changed, or custody written by this helper.

The implemented recovery scope is deliberately narrower than generic network
timeouts: connect/handshake timeout or reset **before a writer is returned**
remains fatal, since this helper has no acquired stream whose closure it can
observe. Explicit connection refusal uses asyncio's failed-connect cleanup
contract. Recoverable errors after acquiring a writer require successful
`close`/bounded `wait_closed`; uncertain closure and cancellation remain fatal.
Cleanup has a separate one-second bound and does not renew the original session
deadline; post-I/O liveness failure still closes the owner. Partial physical
traffic is not retrospectively measured; reservation charges remain conservative.

This is an unexecuted source checkpoint, not a passing control, deployment or
growth result. No import, compile, test, build, proof or Git mutation was performed
by this author. Root owns the companion facade and launch selection; separate
agents own focused controls and independent review. Used predecessors remain
unchanged.
