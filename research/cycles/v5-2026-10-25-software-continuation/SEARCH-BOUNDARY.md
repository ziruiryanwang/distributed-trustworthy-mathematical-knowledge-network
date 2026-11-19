# Default search boundary: stop one provider monopolizing a finite search

2026-10-25. Source-only audit by current_security_obstruction. No code change,
import, test, database open, network request or benchmark. Only this checkpoint
is written. Canonical guard passed. Root owns any successor and execution selection.

## Decision

The highest-payoff bounded correction is **fair serial request scheduling with
per-attempt time limits and confirmed cleanup**, inside the existing ordinary
`find` operation. Current aggregate caps prevent unlimited client spending, but
do not prevent the first provider consuming the whole useful search opportunity.
This is a practical availability/discovery defect, not a mathematical soundness
failure or a violation of the current documented slow-peer disclaimer.

Do not replace the search protocol, introduce a new distributed index, parallelize
connections, or restart the certificate lane for this correction. Manual separate
CLI searches are an available workaround, but require user scheduling/new explicit
grants and do not repair one aggregate-budget public search.

## Actual selected path

The bounded ordinary profile imports `transport.clients.SearchClient`,
`discovery.search_session`, the formal feature/query adapters and the existing
provider. `ordinary_bounded_operations/source-map.json:467` maps those discovery
roles; `:477` selects `ordinary_authoring_offers/http_provider.py`, **not** the
different located-search resilience lane.

The source and adopted package `peer_api.py` currently have the same SHA-256:
`7a2567a96095263e5be53749217eac81b74404d8b1d01d4d24e3a98cd8ecdffd`.
Package inspected: `experiments/v5-local-checks/bounded-investigator-src01/distribution/package`.

The public path is:

```text
peer.py find -> peer_api.find -> SearchClient.offer/candidates
  -> selected provider /v5/discovery/offer and /candidates
  -> authenticated summary + positive membership verification
  -> exact returned candidate selections; no mathematical acceptance
```

`ordinary_formal_query/discovery/ordinary_export_adapter.py:88` compiles supported
formal features, including exact type keys, type symbols and declaration/type
heads. No result ID is required in the query. Provider `dispatch` at
`ordinary_authoring_offers/http_provider.py:205` uses the existing bounded
candidate query; it narrows the requested operation time to its own ceiling.
`discovery/candidate_query.py` drives an indexed anchor posting list, probes other
features, and returns membership-proved hits with an advisory cursor. Provider
SQLite/proof-work limits and client aggregate reservations already exist.

These features do not imply semantic completeness, globally complete indexes,
cheap full posting-list enumeration, or permission to dial unknown referrals.

## Concrete counterexample

`ordinary_bounded_operations/peer_api.py:212-249` visits providers serially and
drains every offered partition/page of A before attempting B. Its docstring at
`:169` explicitly admits that a slow peer can consume the original remaining
deadline. `transport/clients.py:31-35` assigns each request up to the remaining
session time, capped at60seconds. Candidate requests have no smaller attempt cap.

Let A and B be approved reachable contacts; B has a useful matching record.
Give the operation enough request/byte/row allowances for both providers, but a
30second remaining deadline. If A accepts a connection and stalls its offer or
candidate response, A can consume essentially the whole deadline. B is never
queried. A need not be malicious; overload suffices. Likewise, a fast A with a
large posting list can consume the page/examined/candidate budget before B's
first request. A finite global cap alone is not fair access to diverse sources.

## Transport facts that constrain the repair

- The selected `exchange` at `ordinary_authoring_offers/http_provider.py:115`
  already takes `timeout_ms`. Its asynchronous timeout encloses TCP connection,
  TLS handshake, write/drain, headers, exact body and trailing EOF. TLS handshake
  receives the same timeout explicitly (`:130-145`).
- `Endpoint.validate` requires an IP literal (`:54`), so this path has no DNS
  resolution deadline to add. `server_name` is TLS identity/SNI, not a dialled
  hostname. Do not silently broaden contact addressing.
- SSL context/CA loading is synchronous and occurs before the async timer
  (`:125`). Local validation/JSON/proof work is also not preempted by an async
  timer. Their work still needs the existing original allowance and outer Job;
  a new per-attempt number is not a hard all-work wall guarantee.
- Closure has a separate1second wait, but current `:150-151` suppresses its
  errors. Consequently a timeout cannot be advertised as a *settled* recoverable
  provider failure merely because `SearchClient._send` abandons its ticket.
  Budget settlement and observed transport cleanup are different conditions.
- The existing `transport/search_resilience.py:143-247` already distinguishes a
  settled read timeout from external cancellation, unreturned-connect uncertainty
  and dirty closure, and forwards `attempt_timeout_ms`. Its cleanup/settlement
  rules and tests are reusable source evidence. Its owner binding explicitly
  requires `_LocatedSearchClient` (`:48`); that whole module/owner path is not
  shipped by the bounded profile and must not be blindly imported here.

## Smallest consequential successor

1. Keep the same one `SearchSession`, precharged network suballocation, original
   deadline, provider allowlist, query identity and conservative failure charges.
   Keep requests serial. Never renew a budget, clear deduplication, or retry a
   failed provider automatically.
2. Replace provider-draining loops with a finite queue: one offer per provider
   in the first round; thereafter at most one candidate-page request per active
   provider per round. Maintain its existing partition/cursor state. Remove a
   provider when finished, refused or failed under the existing precise policy.
   Do not follow a nonprogressing advisory cursor or turn it into coverage.
3. Pass a narrowed attempt limit to the existing client/transport call, including
   page calls. Bound it by the configured finite attempt ceiling and the original
   remaining time with a cleanup reserve. Subdivide residual time across currently
   eligible providers; do not allocate every request the whole remainder. If a
   legal slice or reservation cannot fit, return explicit incomplete-budget
   termination without dialing. Exact constants/config compatibility belong to
   root's prospective source contract, not an unselected new default here.
4. Reuse the existing strict transport cleanup logic in a minimal Python-only
   successor: only an observed closed stream may yield a recoverable read-timeout
   outcome. Dirty cleanup, external cancellation and unknown local failures stay
   fatal after settling the original ticket exactly once. Do not implement this
   by an outer timeout around the old error-suppressing `exchange`.

This yields an auditable scheduling property: no provider receives a second
request in a round while another eligible provider awaits its first. If enough
aggregate resources remain and local processing/cleanup stay within the stated
envelope, a stalled early provider cannot consume later peers' allotted I/O
opportunities. It does **not** guarantee contacting all64configured peers under
arbitrarily small grants, wall-time fairness under blocked local filesystem/CPU
work, eventual success, or discovery completeness. If per-page reservations are
too large for later peers, termination remains explicit; no hidden refund is
derived from provider-reported scan work.

No Lean rebuild or change of mathematics/index commitments is inherently needed.
A fresh reviewed package overlay/source map could reuse the approved installation
and replace only Python roles plus documentation. Frozen shipped bytes stay frozen.

## Existing tests and exact changed-boundary controls

Read-only test inspection establishes coverage intent, not a rerun:

- `discovery/test_search_session.py:138` checks workflow-wide provider/page caps.
- `transport/test_candidate_session.py:97,109` checks no scan refund and malformed
  replies retaining charges; it does not test this public scheduling loop.
- `transport/test_search_resilience.py:200,254,299` covers settled failures,
  fatal dirty closure/cancellation and actual loopback unavailable-then-honest
  behavior, but through the different located owner. These passes cannot be
  transferred automatically to the bounded public `find`.

Select only these changed-boundary tests if root implements the successor:

1. A's offer/read stalls; its cleanly closed attempt consumes one conservative
   ticket; B's offer and positive page succeed within the same original grant.
   Assert unchanged deadline/limits/session, no pending reservation, no retry.
2. Both providers are fast; A returns a continuing cursor on a large anchor.
   Assert request order `offerA, offerB, pageA, pageB` before any second A page.
   Use an actual authenticated finite fixture; B's hit remains discoverable.
3. A stalls on a candidate page after offering: full scan/match/byte reservation
   survives once, no coverage is added, and B can still be attempted if affordable.
4. Dirty `wait_closed`, external cancellation, unreturned-connect uncertainty,
   and an unknown local error stop the operation; no subsequent contact is dialled.
   Invalid membership never contributes a match or gains mathematical authority.
5. Exhausted/tiny grants, expired original deadline and insufficient cleanup slice
   dial nobody further and report incomplete/exhausted status without renewal.
6. Verify the attempt cap reaches TCP/TLS/read/EOF paths; pin endpoint/CA policy;
   retain explicit `global_complete=False` and `verified_scan_coverage=False`.

Use small native-free deterministic controls and, only if necessary to verify
the selected transport path, one bounded loopback continuation. No large corpus,
native proof, expensive benchmark or new search architecture is needed to decide
and fix this boundary.

## Proposed exact two-file implementation split

Fresh candidate only; not yet authored or selected:

- `software/v5/ordinary_fair_search/fair_exchange.py`: exports
  `async exchange(endpoint, route, request, maximum, timeout_ms)` and explicit
  `SettledRefusal` / `UnsettledTransportError` result/error types. Reuse the
  existing selected HTTP codec/Endpoint and the inspected resilience stream
  closure rules, without importing `location` or changing frozen transport.
  It returns a raw successful response or a settled transport refusal; it does
  not parse peer JSON, authenticate mathematics, mint tickets or retry.
- `software/v5/ordinary_fair_search/fair_search.py`: exports a small
  `FairSearch(session, endpoints)` coordinator, `await run(providers, offer,
  page, *, attempt_timeout_ms, check_owner, recover_metadata_failure)`, and
  read-only `result()` / `report()` accessors. Root supplies the already-created
  original `SearchSession` and immutable approved contacts. The object owns one
  serial queue, existing HTTP counters and partial offers/matches/refusals.
  `report()` retains the existing `{session,http}` shape; `result()` supplies
  partial public search fields even after a fatal failure. Ticket creation,
  reservation, accept/dedup and abandon use the unchanged SearchSession API.

The recovery callback preserves root's existing precise metadata-refusal policy;
it cannot convert `UnsettledTransportError`, cancellation or local/unknown errors
into another dial. Known transport refusals settle once before returning; malformed
successful-response handling remains a separate validation path. `check_owner`
preserves the allowance/CA repins before and after requests and during scheduling.
No callback can renew the original session limits/deadline. The implementation
must check that original bindings remain unchanged at each boundary.

Root owns a separately selected `peer_api.py` bridge and source-map/profile
integration: preserve config/contacts/prepayment and outer error handling, invoke
the two-file helper instead of draining loops, and merge its partial result in
`finally`. Existing frozen `clients.py`, HTTP provider, SearchSession, wire
schemas, Lean support and installation remain untouched. A fixed finite attempt
ceiling may be an internal initial policy to avoid a new required config field;
root should record that value prospectively. No automatic product rebuild follows.

Payoff is direct: one existing query can reach an independent useful provider
despite a settled slow peer or a large first posting list, without more aggregate
resources or proof work. The finite round-robin queue and narrowed transport
attempts address that failure together; a timeout knob alone leaves fast-provider
page monopolization, and round-robin alone leaves the first stalled request.
This is conditional opportunity fairness, not relevance, availability, population
coverage or mathematical acceptance.
