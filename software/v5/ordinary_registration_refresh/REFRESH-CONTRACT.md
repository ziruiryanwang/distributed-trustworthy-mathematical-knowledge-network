# Refresh API: existing contact feeds into one finite directory

2026-10-28. Source implementation contract. No runtime/import/test, network,
owner/native operation or Git was performed. `peer_api.py` is a fresh successor
of deployed `ordinary_multi_source/peer_api.py`; root owns package/launcher
integration. The existing contact wire schemas and mathematical acceptance stay
unchanged. Provider cutoff implementation belongs to query_scaling.

## Public function and exact configuration

```python
async def directory_refresh_serve(loaded, config, allowance, *,
                                  ready=None, network_budget=None)
```

The operation name is `directory-refresh-serve`. It opens no catalog/custody and
never dials an advertised endpoint. It fetches only locally approved feed origins
using their existing `/v5/ordinary/contacts` endpoint. A feed can already run the
public metadata-only `directory-serve`; ordinary mathematical index endpoints
are not assumed to expose that role.

Configuration has exactly six top-level fields:

```text
contacts = {feed_label: existing_direct_contact, ...}
slots = [{feed, specs, max_contacts, max_bytes}, ...]
endpoint_scopes = {feed_label: {tls_names: [...], endpoints: [...]}, ...}
egress = existing_DMKN_V5_OWNER_EGRESS_V1_policy
refresh = {requests, reply_bytes, attempt_timeout_ms, max_age_ms, min_service_ms}
service = {host, port, tls, lease_seconds, cleanup_seconds, limits}
```

`existing_direct_contact` is exactly `{host, port, tls, server_name, ca_file,
ca_sha256}`. Feed CA paths/pins are explicit local choices; replies cannot supply
them. `service` is the current static directory configuration without `entries`.
Its `limits` and TLS object are unchanged. Feed labels are local policy slots,
not proven independent operators. All configured feeds must appear in a slot.

| Field | Exact bounds/meaning |
| --- | --- |
| contacts | 1..8 known feed labels; current direct-contact parser/pins |
| slots | 1..32; each `(feed, compiled exact route)` unique; `specs` uses the existing ordinary compiler, at most eight features |
| slot max_contacts | 1..16; sum for each compiled route across all slots <=16 before I/O |
| slot max_bytes | 1,024..32,768 response bytes |
| endpoint_scopes | Exactly the feed-label set; each scope has 1..16 total TLS names plus exact endpoints |
| tls_names | Sorted unique canonical lower-case TLS server names; no nulls |
| scope endpoints | Unique exact existing four-field contact rows; prevalidated by the local egress policy |
| refresh.requests | 1..32, and at least the total slot count |
| refresh.reply_bytes | 1..1 MiB, and at least the sum of slot max_bytes |
| attempt_timeout_ms | 1..5,000; actual attempt is narrowed by remaining original slice |
| max_age_ms | 1..3,600,000; local request-start issuance age, not provider liveness |
| min_service_ms | 1..60,000, no larger than max_age_ms or requested service lease |
| service | Current 1..3,600-second lease, 10..60-second cleanup and provider bounds |

An advertised row passes its feed scope when either it exactly matches an
approved endpoint row or it uses TLS with an approved `server_name`. It must
also pass the separate current egress policy. Thus approved TLS identities may
move between permitted public numeric IPs/ports without broadening topic/identity
scope. Readers independently apply their own egress and certificate validation.
Explicit loopback test policy remains separate. No learned endpoint is contacted
by this operation to test liveness.

`_refresh_plan` validates all scopes, compiled route sums, complete reservation
capacity and service configuration before network work. Server certificate/key
pins and TLS load are checked before spending requests, then checked again by
the reused server path. No policy data comes from feed replies.

## One grant, fresh replies and partial results

Use the existing `OrdinaryBudget` external prepayment for the complete selected
refresh request/byte allocation. If an existing shared ledger is supplied, its
ordinary exact-type, preallocation and remaining-capacity checks apply; no grant
is renewed. A new owned ledger is closed on exit. No `begin` tickets or owner
admission are involved.

Reserve cleanup and minimum service time before selecting the refresh deadline.
Each slot gets at most one `fair_exchange.exchange` to its selected feed, with
fresh nonce, exact namespace/features and its preallocated contact/byte maxima.
Pin checks occur before/after I/O. The attempt interval is narrowed after local
setup and passed as an absolute deadline. Existing settled transport refusals
are recoverable slot outcomes; unconfirmed cleanup, cancellation, local pin or
outer-budget failures remain terminal. There are no automatic retries.

Parser/binding failure omits the entire reply. In a valid reply, endpoints that
fail egress or feed scope are filtered individually, with rejected counts. Such
a source is incomplete, not a successful empty withdrawal. A valid empty
untruncated response is `EMPTY_SOURCE`; an empty truncated response is
`EMPTY_TRUNCATED_SOURCE`. Nonempty valid replies use `ADVISORY_CONTACTS` even if
all their endpoints are rejected, preserving the distinction from withdrawal.

The successful usable subsets are unioned by exact route and canonical endpoint
bytes. The prevalidated quota sums prevent overflow without choosing winners
after arrival. A source's truncation remains disclosed; the registrar neither
expands its quota nor assumes it saw the whole source. Identical endpoint rows
are deduplicated, while the conservative common horizon still includes every
contributing nonempty slot. One slot's empty answer cannot erase another slot.

No eligible advertisement survives a previous invocation. A failed/omitted slot
has no cached fallback. Empty union returns without constructing a listener:
`REFRESHED_EMPTY` when every selected slot returned usable untruncated unrejected
metadata, otherwise `INCOMPLETE_REFRESH_EMPTY`. Both use termination
`NO_CONTACTS_NO_LISTENER`. Empty does not mean global absence.

## Time and READY boundary

For slot request start `t`, compute

`h = min(original_deadline - cleanup_seconds - 0.001, t + max_age_ms / 1000)`.

Responses that no longer leave `min_service_ms` are omitted. Recheck all accepted
slots during final map assembly. The internal server receives the earliest
included nonempty-slot horizon as `contact_deadline`. Cached maps, response
timestamps and new service launches cannot refresh that horizon. Fresh replies
can still repeat a provider's stale configuration; no revision/rollback detector
or liveness/coverage assertion is introduced.

The reused internal signature is:

```python
async def directory_serve(loaded, config, allowance, *, ready=None,
                          contact_deadline=None, minimum_service_ms=0)
```

These private keywords are computed by trusted local composition, not read from
the static public config. `minimum_service_ms` must be an exact integer in
0..60,000, and nonzero requires a contact deadline. Clip the requested service
lease to that finite monotonic deadline. Pass the **clipped lease end** to
`Provider(contact_deadline=...)`, so a longer row horizon cannot extend a shorter
selected service lease. Default `None/0` preserves the existing static path.

After provider.start and before READY, require the selected minimum remaining
interval. Slow setup refuses with `REFRESH_START_TOO_LATE` and performs normal
bounded provider cleanup; it does not announce a short service or silently
refilter the already constructed map. The provider's independent dispatch and
write-chunk callbacks check the cutoff immediately before new enqueue operations.
This is not hard real-time scheduling or a final-delivery deadline. Already
queued bytes can arrive later, and prior readers retain their own existing
contact-use horizons. No immediate revocation promise is made.

## Reports and failure preservation

The top-level report contains `operation`, `status`, `namespace`, `egress`,
`selected_slots`, `refresh_complete`, `global_complete:false`,
`mathematical_acceptance:false`, `lookups`, `refresh`, `network`,
`route_count/contact_count` when assembled, nested `service`, `ready`,
`quiescent`, `termination`, `cleanup_errors`, and HTTP overhead upper bounds.
`refresh` separates attempted request/reply reservations from actual observed
request/reply/header bytes. Failed settled exchanges retain conservative charges.

Each lookup records slot index/feed/features/status, truncated/returned/adopted/
rejected counts and `included`. Additional reason/error/http_status fields appear
for the corresponding outcome. `included` means its fresh response survived
assembly; it does not imply contacts existed or that source coverage was complete.
An adopted count can remain nonzero on an expired omitted slot; `included:false`
and its explicit status prevent treating it as published. No endpoint absent
from the accepted union becomes connection authority.

`refresh_complete` means every selected slot supplied usable, untruncated,
unrejected metadata for this cycle. It says nothing about global coverage or
source truth. The READY callback includes this flag, selected_slots and
global_complete:false. The successful terminal service status is
`REFRESH_SERVICE_FINISHED` or `INCOMPLETE_REFRESH_SERVICE_FINISHED`, with
`FINITE_SERVICE_CLOSED`. A nested server failure is preserved in `service` and
raised as a top-level PeerFailure with the accumulated refresh evidence.

No executable imports or controls have run for this source checkpoint. Root and
the independent reviewer select only changed-boundary verification next.
