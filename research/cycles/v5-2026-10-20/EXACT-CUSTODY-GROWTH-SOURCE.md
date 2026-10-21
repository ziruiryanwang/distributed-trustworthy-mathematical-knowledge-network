# Exact-demand custody helper source checkpoint

2026-10-20, core_growth. Canonical root only. Source-only implementation under
`EXACT-CUSTODY-IMPLEMENTATION.md`; no import, test, build, proof, service, network
operation or Git mutation was run. Predecessor bytes remain unchanged.

Implemented `software/v5/body_location/client/body_custody.py`;
initial review SHA-256
`a780be385fe32841bbe5b7da3c24db6487e8fc99f3df47f8dcc9ca8f5c0c1ead`.
Root owns integration and adoption; this fingerprint is not qualification.

Independent release review subsequently identified known unexpected Node exits
not represented by `channel_failed` alone. The unused source was corrected:
`check` and pruning reject forced termination, cleanup uncertainty and a known
nonzero process return code, while allowing clean locator-only return0/closure.
Expired rows are explicitly inert tombstones, and the report separately counts
unexpired issued hints. That intermediate source SHA-256 was
`ce5916d173df3b9f3e5abe7a63b3774594a4a5e7d5caf0f34a77ea1b8809af08`.
The same review then identified parent-close-task failure after a zero child
exit (for example a post-close source-pin refusal). The final guard also
rejects an already-owned close task that is pending, cancelled or completed
with an exception; it only reads task state and never starts/waits/retries
cleanup. Final source SHA-256:
`d4ad056417996b37b50463037a72217a4dbca8aedab18d18c8c5b0a24d23e89c`.
Adaptive auditor was asked to include these distinctions in the existing
lifecycle control group; no new campaign or execution was requested.

## Exact integration ABI

- Facade initializes `_body_pool = _origin_body_pool = None`, adopts the exact
  object returned by `reserve(client, limits)` once, and pins the helper plus
  reader/located-query/transport sources through the original mathematical
  owners. The helper imports exact client/reader classes locally to avoid
  construction cycles.
- `pool.locate(reader, demand, *, event_cap, peer_cap, descriptor_requests,
  max_age_ms=10000)` runs inside both existing reader and facade serialized
  actions. It uses the current held candidate and exact pending demand.
- `pool.begin_attempt(reader, demand, capability)` returns `_BodyAttempt`,
  already marked ATTEMPTING. The existing common transport engine calls
  `attempt.validate(check_expiry=False)` before reservation,
  `attempt.reserved(ticket)` immediately after original budget issuance,
  default `validate()` predial/postreturn, and `attempt.settled(status)` after
  complete settlement. Allowed statuses are `BODY_VALIDATED` and
  `UNAVAILABLE_AT_SELECTED_SUPPLIER`. The facade always calls `finish()`.
- The attempt exposes `acquisition`, `structural`, `budget`, `resolved`,
  `digest`, `request`, `supplier`, `route_key` and exact `_BodyContact`.
  The latter binds `_endpoint`, `_expires`, `_policy`, `_budget`, `_binding`
  and forwards ordinary endpoint properties; `validate()` delegates to the
  exact issued current attempt, not to caller code.
- `pool.prune()`, `invalidate_reader(reader)`, `close()` and `report()` do not
  enter a facade action or recurse through client liveness. Pruning removes
  fulfilled/removed/terminal/retired records; expired hints are unusable at
  the predial guard but remain bounded private records until attempted or
  invalidated, so expiration cannot bypass the selected attempt charge.

## Implemented boundaries

The optional pool is prepaid before the first query/acquisition ticket through
the unchanged outer `charge_external`; combined query/body commands fit the
same child. Every location/descriptor allowance is monotonically consumed.
Body fetches use the original acquisition and structural counters, never a
shadow owner or allowance. A spent token is removed while cumulative counters
remain. Local capacity refusal spends the token but issues no replacement.

The semantic domain binds actual codec/module-store/adapter foundation and
policy, independent of the optional discovery profile. Compact exact ExportID
addresses use the new explicit protocol helpers. Same-child raw route and
descriptor replies are checked against exact tickets, peer/key/role bindings,
bounded census, owner egress and fixed expiration. Only the existing typed
TCP-connect descriptor miss is recoverable. Other location exceptions revoke
the pool, close the original child and retain uncertain-cleanup poisoning.

Neither original endpoint dictionary changes. A shared per-location selection
references already-held immutable description bytes and original resolved data;
it does not duplicate a complete opening per returned endpoint. Pending demand,
member selection, declaration commitment, original candidate/provider and
search/acquisition/structural identities are checked throughout. Known body
hashes do not grant mathematical authority.

Iterator census counts and reserved DHT `onProgress` event caps are distinct
measures in the retained implementation. The helper mirrors `observed_route`
validation; it deliberately does not invent `census.events <= event_cap` or a
wire-byte measurement. Body success counters mean exact transport validation,
not custody, admission or mathematical acceptance; the facade owns the latter
gates. Clean locator-only service expiry does not automatically revoke a still
live HTTP hint; failed channel/uncertain cleanup does.

## Cross-source review and remaining work

Read root's new reader/facade/shared-transport seams; names and lifecycle agree.
Added `attempt.route_key` requested by the facade's scoped unavailable result.
The shared engine retains exact located-contact admission and ordinary
body/declaration behavior. Protocol author confirmed the exact Python helper
signatures used here. Adaptive auditor received the file/ABI for controls.

Independent source review and focused controls are still pending. No runtime
is authorized by this checkpoint; root selects a bounded check only after
integration review. Full v5, broad availability and useful-growth benefit remain
open and are not inferred from this helper.
