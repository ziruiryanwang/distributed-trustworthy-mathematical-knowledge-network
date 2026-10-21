# Exact pending-body custody: implementation contract

2026-10-20, core_release. Implements the source decision selected in
`EXACT-CUSTODY-SELECTION.md`; this document selects no execution. Baseline is
the 113-entry `distribution-projection-01-input.json` map. Used bytes stay frozen;
implementation, if selected, uses source successors and the same logical imports.

## 1. One supported operation

While a `SemanticReader` has a validated, pending `NeedBody`, locate an unknown
custodian Q and fetch that exact body without retiring its current query.
Q need not be an index contact. The original candidate, search, acquisition,
structural owner, grant, deadline, policy and mathematical checker do not change.
No module-evidence variant selection, new proof, replication or remote write.

Public ABI:

```python
client.reserve_located_queries(channel, envelope, policy)  # existing
client.reserve_body_location(limits)                      # new, before first query
await client.next_located_query(...)                      # existing
# Existing selection/resolution/staging/preview creates reader and NeedBody d.
located = await reader.locate_body(
    d, event_cap=..., peer_cap=..., descriptor_requests=..., max_age_ms=10000)
for capability in located["capabilities"]:                # caller chooses attempts
    result = await reader.try_fetch_body_from(
        d, capability, max_bytes=..., attempt_timeout_ms=5000)
    # Caller decides whether to stop; there is no implicit fallback/retry.
```

`reserve_body_location` is optional and may be called exactly once. It is a
normal serialized facade action. `locate_body` and `try_fetch_body_from` use
the reader's existing `_call` step counter and one serialized facade action
each. Existing `fetch_body`/`try_fetch_body(..., supplier=...)` remain unchanged.
No string supplier label can invoke the new capability path.

## 2. Semantic address, namespace and wire

Use existing canonical JSON and `F.digest(domain,value)` framing (ASCII domain,
NUL byte, canonical JSON, SHA-256), identically in Python and JavaScript.

The owner-selected domain is exactly:

```json
{"foundation":"<hex64>","policy":"<hex64>"}
```

Derive semantic namespace S, rather than accepting a peer-supplied namespace:

```text
S = digest("DMKN-V5-BODY-CUSTODY-NAMESPACE-V1", {
  "module_schema":"DMKN_MODULE_SPEC_V1",
  "body_schema":"DMKN_MODULE_BODY_V1",
  "foundation":foundation, "policy":policy
})
```

Foundation/policy must equal the client's adapter, actual module store and
selected wire profile. Discovery schema, pair/pattern/fingerprint profile,
provider identity, index cut and receipt image are deliberately absent.

The compact `body_ref` has exactly four fields:

```json
{"module_id":"<hex64>","export_id":"<hex64>",
 "universes":0,"body_hash":"<hex64>"}
```

`universes` is the declaration's universe-parameter **arity**, integer 0..256,
not a universe instantiation. Python derives `export_id` with the unchanged
`C.export_id(module_id, relative_name)` after checking the exact current demand
and acquired declaration. The hash commits the structured name. JavaScript
validates the four compact fields; it does not reinterpret Lean names. This
avoids exceeding existing 2048-byte descriptor-request/16KiB IPC limits for
long supported names or creating a second name codec.

The exact route spec and key are:

```text
spec = {"namespace":S, "role":"committed-body-v1", "body":body_ref}
key  = digest("DMKN-V5-BODY-RENDEZVOUS-V1", spec)
```

There is no stripe or formal-feature predicate in this role. Different module,
name/ExportID, arity, hash, foundation or policy yields a different route under
the hash assumption. Neither role nor namespace may be coerced into the old
`formal-index-v1` schemas.

Descriptor request is exactly `{schema, namespace, role, body, route_key, nonce,
max_bytes}`, with schema `DMKN_V5_BODY_DESCRIPTOR_REQUEST_V1`, `max_bytes=4096`,
fresh hex64 nonce and the exact spec/key above. Canonical length must be <=2048.
Descriptor reply is exactly `{schema, namespace, role, route_key, nonce, peer_id,
endpoints, assurance, global_complete, mathematical_acceptance}`, with schema
`DMKN_V5_BODY_DESCRIPTOR_V1`, one endpoint, `assurance=ADVISORY_SERVICE_HINT_ONLY`
and both booleans false. Namespace, role, key, nonce and authenticated dial PeerID
must bind the request. Validate the endpoint through the same owner egress policy.
No CA file, verifier policy, callback, filesystem path or executable handler is
accepted from the descriptor. Reply length is <=4096.

Add pure explicit functions to logical `location.protocol` in both languages:
`body_namespace`, `body_ref` validation, `body_route_spec`, `body_route_key`,
`body_descriptor_request`, request validation and descriptor verification/creation.
Existing index helpers retain their exact accepted schemas and bytes.

## 3. Same child, explicitly selected from startup

Add `DMKN_V5_MAINTAINED_LOCATION_ROLES_V2`: all V1 config fields plus mandatory
`body_domain` as above. V1 remains accepted unchanged and refuses body commands.
`namespace` still means the original **index** namespace. `role` remains either
`reader` or `index-provider`; enabling an additional fixed body capability does
not give a reader publication authority. The semantic domain is immutable at
startup and is pinned by the existing configuration/source bindings.

Use the same `ServiceLocationProcess`, Node, DHT, peer cache, database, private
IPC sequence, lock, timer, transport budget, metadata quota and shutdown. No
second child and no service restart. Register the new descriptor stream protocol
`/dmkn/v5/body-descriptor/1.0.0` only for a V2 index-provider; the existing index
protocol remains available. Both handlers share `serving <= 2`, descriptor
request/reply reservations and all transport/service counters, not two separate
allowances. A V2 reader may dial either descriptor protocol but serves neither.

Add these four explicit IPC commands to BOTH `ipc_wire.mjs` and
`node_entry_services.mjs`:

- `locate-body`: same route-ticket shape/census as `locate`, but
  `operation="body-route"` and the exact body spec/key above.
- `descriptor-body`: same descriptor-ticket shape as `descriptor`, but
  `operation="body-descriptor"` and the new request schema. No foreign absolute
  `until` is sent; the Node adapter uses only remaining duration as before.
- `publish-body`: payload exactly `{body: body_ref}`; provider-only, V2 only.
- `withdraw-body`: same payload and role restrictions.

Refactor private Node routines where useful so both roles share DHT iteration,
bounded transport and descriptor framing. Role-specific validation must precede
the common engine. The shared known-peer cache conveys only dial hints; Python
must still bind each descriptor peer to that body's returned route result.

`intent.mjs:enableIntent` also needs the closed role-dispatched exact spec/key
validation. Preserve its atomic intent+published transaction and revocation
mechanism. Both roles share `/application/published/` and one `advertised_keys`
cap. No new unconstrained intent prefix or persisted authority is created.

The only settled descriptor unavailability remains the existing narrow local
TCP-connect-unavailable class, now available for either descriptor command.
Keep body response role/key/nonce/peer validation mandatory; malformed data,
unexpected child exit, cancellation and uncertain cleanup remain fatal. No
timeouts are reclassified merely to keep the operation alive.

The 64-frame, 1MiB-per-direction IPC limits and existing runtime-source pin map
shape remain unchanged. Use successor bytes at the same named source paths.
No dependency installation or rebuilt crypto runtime is necessary.

## 4. Prepayment and exact counters

`reserve_body_location(limits)` requires:

- Exact live validated client, installed/pinned new helper and a reserved
  `_LocatedEnvelope` from the existing `reserve_located_queries`.
- No query generation yet, pristine unstarted V2 reader child, no pending
  request, `client._budget.sequence == 0`, and no prior body pool.
- Same grant/deadline/policy/channel as that envelope; `body_domain` matches
  actual semantic stores. No configuration mutation after reservation.

Exact limits object:

```text
schema              = "DMKN_V5_BODY_LOCATION_ALLOWANCE_V1"
route_operations    : 1..16
routing_events      : 1..4096       # sum of issued route caps
routing_peer_slots  : 1..128        # sum of issued peer caps
descriptor_requests: 1..32
capabilities        : 1..32, <= descriptor_requests
```

Before dispatch, call the existing, unchanged
`AcquisitionBudget.charge_external("body-location", route_operations +
descriptor_requests, 4096 * descriptor_requests)`. This is a debit inside the
original outer grant; it neither changes `sequence` nor creates a new budget.
No unused portion is refunded. Failure of prepayment prevents pool adoption.
The original query/location prepaid pool and this pool must jointly fit the
same outer acquisition budget.

Also require prospective query route/descriptor commands plus body
route/descriptor commands plus two lifecycle slots to fit
`min(channel.config.limits.commands, 60)`. Every call still obeys the same
private-pipe frame/byte caps. Per-route `event_cap` and `peer_cap` must not exceed
the existing child's per-call event/provider limits. Child raw transport and
service limits are shared, not multiplied by the two application roles.
This check is performed before adopting the pool: two independently valid
maximum allowances are not presumed simultaneously achievable. The reader
profile issues no periodic health commands; the two reserved lifecycle slots
cover explicit status/stop, with startup READY occupying the existing separate
frame. If a caller spends additional IPC commands outside these reserved paths,
the unchanged channel may refuse before dispatch; it never replenishes capacity.

The new pool keeps bounded monotone counters:

```text
route_operations_issued, routing_events_reserved, routing_peer_slots_reserved,
descriptor_requests_issued, descriptor_reply_bytes_reserved,
descriptor_reply_bytes_observed, capabilities_issued, capabilities_consumed,
body_attempts, body_successes, settled_unavailable
```

Each route consumes its entire selected event/peer allowance at issuance even
if no peers return. Each descriptor consumes one request and a full4096-byte
reservation at issuance; observed bytes are reported separately, never refunded.
Capabilities count cumulative issuance, not only currently live tokens. A lost
reply or expired capability does not restore any counter. DHT event counts and
these logical byte debits do not claim measurement of every DHT wire byte.

Body fetches are **not prepaid twice**. Each actual attempt uses the original
`AcquisitionBudget.begin/settle` and original `_SharedAcquisition` request, byte,
inflight, failure and header/request-bound counters. Both owners and both
endpoint dictionaries are unchanged. Known response bytes use the existing
settlement rules; absent/uncertain pre-validation response extent consumes the
full selected body reservation. The body pool records the attempt but supplies
no replacement capacity.

## 5. Locate and mint a demand-local capability

`reader.locate_body(d, event_cap, peer_cap, descriptor_requests, max_age_ms)`:

1. Run existing reader liveness/step and facade checks. Validate d through
   `_demand`; require kind `NeedBody`, a resolved name, selected module, matching
   acquired descriptor arity and permitted body hash. Reject a body already in
   this reader's staged body set. Freeze exact canonical demand/descriptor bytes
   and compute the route from those bytes, not caller-supplied route fields.
2. Require no pending search/acquisition request, original Node lock free and
   the same current query/acquisition. Validate positive caps and
   `1 <= descriptor_requests <= peer_cap`, `1 <= max_age_ms <= 60000`.
   If the reserved pool cannot cover these caps, return
   `BODY_LOCATION_BUDGET_EXHAUSTED` with an empty capability list; do not dispatch,
   renew or mutate the reader's staged mathematical data.
3. Debit route allowances and send `locate-body`. Use existing census/termination
   checks. Only peers actually returned for this request may receive a body
   descriptor request. Try at most the requested number in returned order,
   sequentially on the existing lock. Do not crawl referrals.
4. A descriptor's local expiration is fixed at its issuance time plus
   `max_age_ms`, clamped to the original grant, outer acquisition budget,
   structural acquisition, body-pool and still-selected original query/session
   deadlines. Response latency never extends it.
5. After verifying a descriptor, mint one opaque `BodySupplier` identity per
   endpoint, stored only in the private pool. Initial profile allows exactly
   one endpoint per descriptor. Stop before the cumulative capability cap;
   additional unrequested descriptors are not fetched.

Pool deadline is fixed at reservation as the minimum of the original grant
and original located-envelope deadline. A particular capability also clamps
to that query's deadline. Location requires a live child within its existing
service lifetime; obtaining a descriptor does not extend that service. A
previously issued hint does not require the locator to remain alive: clean
locator-only service expiry need not revoke its separately live HTTP endpoint.
It still expires at the fixed minima above, and client closure, query retirement
or uncertain child cleanup revokes it. This is not a promise that the remote
provider's HTTP service remains available through that local expiry. A
cleanly settled route with no usable descriptor returns
`NO_BODY_CUSTODIAN_WITHIN_ALLOWANCE`. It preserves the reader. Malformed
descriptor/IPC/owner binding or uncertain cleanup fails closed as above.

Success returns `{status:"BODY_CUSTODIANS_LOCATED", capabilities:[opaque...],
route_key, attempts, global_complete:false, mathematical_acceptance:false}`.
The other two statuses have the same fields and an empty list. `attempts` is a
bounded scalar/census report, not a serialized capability or trusted authority.

Each capability's private record binds:

- Issuing pool/client, exact reader object, grant, budget and current search /
  acquisition / structural-owner identities.
- Original candidate identity and canonical declaration/locator bytes; exact
  current demand and semantic ref/key/domain.
- Exact verified endpoint, peer, original policy object and frozen policy data;
  fixed expiry, issuance counter and unused/consumed state.
- Original limits, deadlines and source-origin bindings.

It is not inserted into `client._search`, `_adopted_endpoints`, `_expiries`,
`acquisition.endpoints`, `structural.endpoints`, the candidate map or a search
coverage object. `_selected_supplier` and existing index-contact `_Binding`
checks are unchanged. The existing supplier API must still reject Q.

## 6. One-body consumption and unchanged validation

`reader.try_fetch_body_from(d, capability, max_bytes, attempt_timeout_ms)` checks
the same exact current demand and descriptor, plus issuance/membership in the
private pool. Token classes alone are insufficient; an invented object, copied
report, other reader, retired query, changed policy or altered demand refuses.
No unrelated revision counter is needed: adding another body need not invalidate
this token if its exact demand/descriptor is still current and unresolved.

Refactor `transport.acquisition_resilience.try_body` into one private attempt
engine with two **closed** binders:

- Existing original-supplier binder: retain exact class/map checks, including
  root's separately selected exact `located_queries._Contact` class correction
  in `LOCATED-CONTACT-REPAIR.md`. No arbitrary subclass acceptance. That narrow
  correction also reaches the unchanged declaration helper's shared binder.
- Demand-capability binder: verifies the issuer record and exact live owner
  identities, captures the unchanged original endpoint maps and supplies only
  an endpoint-compatible demand guard for this fixed body request.

No public caller-provided binder/callback and no third mutable endpoint map.
Both paths share existing `_exchange`, canonical decode, `permitted_hashes`,
`validate_body`, accounting and cleanup. The guard validates token/expiry/owner
egress immediately before dialing and after network return. The request is
the existing `/v5/modules/body` request with the **raw structured name** taken
from the held descriptor; only the locator wire used its ExportID hash.
The unchanged HTTP `REQUEST_MAX=16384` still applies. Compact location does not
make every maximum-size codec name fetchable: oversized body HTTP requests
refuse under the existing limit, without changing their mathematical identity.

After validating token issuance and its exact semantic/owner binding, mark it
`ATTEMPTING` and debit `capabilities_consumed` before calling outer `begin`.
Only that private current-attempt binding may use it while ATTEMPTING; it becomes
`SPENT` in every exit path, even if outer capacity refuses. An expired local hint
is checked again by the predial guard after `begin`, so its attempted dial stays
charged; an already expired original grant refuses earlier and revokes the pool.
Increment `body_attempts` only if `begin` succeeds. Never settle an unissued
ticket or decrement structural counters not entered. Local cap refusal performs
no I/O and grants no replacement allowance; the selected token remains spent.
The common engine must finish existing structural and outer settlements even on
exception. A settled404/503 consumes the token exactly like a successful fetch.

After `BODY_VALIDATED`, perform ordinary `ModuleStore.put_body`, exact read-back
and facade data charging outside every recoverable transport catch, then append
the expression to the same reader's body set and increment its existing revision.
Return its ordinary `FETCHED` shape. A known pre-validation availability failure
returns the ordinary unavailable reason with the exact route/demand scope; token
remains consumed and staged mathematical state unchanged. A wrong body, corrupt
200 response, uncertain socket shutdown, custody failure or source/owner change
retains fatal behavior. No new result is mathematical acceptance.

Invalidate capabilities on consumption, expiration, body fulfillment, removal
of that pending demand, reader failure/finish, current-query retirement or client
close. Keep cumulative counters after discarding dead records. There is no token
serialization, reusable grant extension, implicit re-location or automatic retry.

## 7. Finite provider advertisement with read-back

Add service schema `DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V3`. It retains V1/V2
compatibility and makes `index_view` explicit (null selects ordinary index;
otherwise the existing exact projection selector). Add owner `body_routes`,
a list of 1..8 exact rows `{module_id, relative_name, universes, body_hash}`.
Existing index routes may be empty in V3; at least one body route is required.
Thus a custodian does not have to advertise a fictitious index predicate.

Before starting HTTP/Node or publishing any hint, with the existing exclusive
workspace lock held, validate and deduplicate rows by semantic key, and call
the unchanged `workspace.modules.get_body(...)` for each. It rechecks declaration
permission, canonical bytes and the exact body hash. Derive ExportID and domain
only from these held objects/stores. Release each decoded body before reading
the next; retain only fixed-size refs and bounded observation rows.

This is at most eight selected body reads, not corpus enumeration. Charge the
existing per-object codec limits conservatively: each may read one bounded
group opening and one bounded expression. With current16MiB per object the
selected read-back bound is at most256MiB of such encoded inputs across eight
rows, processed sequentially, not a claimed RAM bound or measurement. Existing
outer CPU/wall/memory containment remains required. Missing/corrupt body or
permission mismatch refuses before advertisement. No new metadata store is
required.

After HTTP starts and its exact endpoint is known, launch the same V2 Node with
domain from `workspace.modules` and publish the finite body refs. Both protocols
serve the same one endpoint. Existing provider health/cleanup still couples
descriptor availability to live HTTP and Node. Reports explicitly state
`READ_BACK_BEFORE_SERVICE_NOT_CONTINUOUS_AVAILABILITY_PROOF` and
`remote_placement_confirmed=False`.

Count `len(index_routes)+len(body_routes)` against the ONE advertised-key quota;
include both sets in the existing prospective publication+health+stop command
reservation. Withdrawal uses the same atomic intent revocation; stale remote
hints may survive until expiry. Private workspace ownership, no remote writes
and immutable bodies mean there is no normal concurrent deletion race in this
profile; disk/process failure remains possible. Do not add periodic full-body
rehashing or promise a retention horizon that was not funded.

## 8. Minimal logical-source delta and ownership

| Logical source | Required successor change |
|---|---|
| `portable/location/protocol.py`, `protocol.mjs` | Explicit pure semantic-domain/body-role schemas and keys; old index functions unchanged |
| `portable/location/intent.mjs` | Closed two-role spec/key validation; same atomic records/quota/revocation |
| `portable/location/maintained_roles.mjs` | V2 immutable domain, body protocol/commands using shared engines/counters |
| `portable/location/ipc_wire.mjs`, `node_entry_services.mjs` | Four command allow-list entries, typed body-descriptor TCP-miss branch |
| `portable/location/controller_services.py` | Explicit V2 config acceptance/domain checks; same class/child/pins/lifecycle |
| `client/body_custody.py` (new) | Prepaid finite pool, route/descriptor issuance and capability registry/guard; no proof authority |
| `client/workspace_evidence.py` | Optional pool initialized/pinned; reserve/fetch facade seams, scoped report and close invalidation |
| `client/semantic_reader.py` | Two new methods, current-demand/capability binding and body staging; existing supplier methods unchanged |
| `transport/acquisition_resilience.py` | One private attempt engine, unchanged original binder plus private demand binder |
| `client/serve_advertised.py` | V3 finite read-back/body advertisement and aggregate command accounting |
| Root-owned distribution builder/source map | Map exact successors, add one helper and recognize V3 injection; no automatic build |

No checker, receipt relation, codec, module-store format, index layout,
`located_queries` generation semantics or original search budgets change.
No new Node/crypto dependency or process is selected. Root assigns disjoint
source ownership after independent contract review; root owns transport/facade/
reader integration as stated in its assignment.
Fresh physical sources belong under `software/v5/body_location/`; logical paths
above are installed names, not permission to edit frozen predecessor files.

## 9. Acceptance boundary for the future small check

First use changed-boundary source controls: cross-language key equality and
role separation; raw-name binding; V1 refusal; startup-domain pinning; original
contacts/maps unchanged; prepayment only before sequence>0; aggregate caps;
same reader identity; one-use/expiry/retirement/mismatch refusal; exact body
validation; clean settled unavailability; fatal corrupt/uncertain outcomes;
provider read-back before hints; shared Node counters/intent caps.

The later minimal integration uses retained valid mathematics: stage P's exact
declaration, with Q absent from all original index contacts; locate Q solely
from a pending body ref, fetch once, and finish the same reader. No expensive
proof production or broad campaign is needed to discriminate this capability.
Root separately selects any execution. Success would not establish global
availability, independent operators, full search recall, net growth or final v5.
