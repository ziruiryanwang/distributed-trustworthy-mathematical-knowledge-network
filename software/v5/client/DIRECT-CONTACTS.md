# Search an explicitly configured service

`direct_contacts.bind` connects the ordinary **validated** client to one or more
owner-selected HTTP services, including `serve_workspace`. It avoids requiring
a Node/DHT process when the owner already knows a service address. It introduces
no central server: each operation can choose different, independently operated
providers. Routing-based `client.find` remains available and unchanged.

```python
from client.direct_contacts import bind
from location.protocol import OwnerEgressPolicy

# client is constructed by RuntimeProfile.open_operation(..., mode="validated").
# Include client/direct_contacts.py in the launcher's selected source map.
policy = OwnerEgressPolicy(owner_egress_config)
ready = bind(client, owner_contacts, formal_query_specs, policy, search_limits)
offer = await client.search_offer(
    "provider-a", max_bytes=65536, max_expanded_bytes=262144)
# Select partitions/pages using the actual offer; use the existing search_page,
# resolve, packet_offers, stage/acquire, admit, import and author APIs unchanged.
```

`owner_contacts` maps unique local labels to records with exactly `host`,
`port`, `tls`, `server_name`. The existing egress policy requires numeric public
IPv4, permitted ports and TLS for public use. Local tests require explicitly
allowed loopback ports. Remote replies cannot add endpoints, choose certificate
authorities, extend deadlines or enable plaintext public connections.

This is one query per original client operation, sharing the slot with `find`.
Binding performs no I/O and prepays the complete search request/reply capacity
against the original acquisition allowance. Search usage is nested inside that
prepayment, not an additional independent charge. Subsequent acquisition consumes
the remainder. The owner must leave enough capacity for selected module/evidence
retrieval. Search/controller, HTTP framing/request, storage and provider costs
retain their existing distinct accounting scopes.

The search deadline cannot exceed the original grant. Contacts expire after
`contact_lifetime_ms` (default 60,000), also bounded by that grant. Acquisition
rechecks expiry and egress policy before dialing. There is no automatic refresh,
retry, refund or fallback. A failed call retains the client's normal fail-stop
behavior, except for already-supported settled discovery refusals. Close the
client/workspace using their existing lifecycle.

The result explicitly states `location_performed=False`; `report()["location"]`
remains `None`. Despite its historical class name, the reused guarded search
transport is not evidence that DHT location occurred. The custody acquisition
is structural only; resolved candidates must originate in this search.
Mathematical use still requires an actual live warrant from the unchanged
receipt/aggregate/native owners. Neither configured trust in a service, a
correct authenticated index answer nor successful data retrieval grants one.

This entry is trusted local owner code, not a hostile-code sandbox. Direct
contacts do not solve global discovery coverage, availability or the outstanding
v5 aggregate certification/release obligations.
Owner code must not mutate the constructed client, session, contacts or budget
internals; the guards are consistency checks, not hostile in-process isolation.
