# Network endpoint V2: readiness and observable incomplete results

This is the source contract for `network_actual02.py`, not a runtime result or
public-release claim. It keeps the mathematical endpoint, seven role/port names,
complete retained packet and finite limits in [the predecessor proposal](network_actual_api.md).
The predecessor's actual failed run and used source remain unchanged.

## Configuration changes

The schema is `DMKN_V5_ACTUAL_DELTA_NETWORK_V2`. All existing keys remain, and
`location` now has exactly:

```text
source_directory, source_pins, role_pins, entry_source, ready_source
```

`ready_source` is an exact `{path, bytes, sha256}` pin for the canonical
`software/v5/location/maintained_roles_ready.mjs`. Its digest must equal the
`role_pins["maintained_roles.mjs"]` digest of the separately pinned 14-file Node
snapshot. The other deliberate alias remains the existing available-descriptor
entry to `node_entry_services.mjs`. Root selects that snapshot and executable
configuration. These fields cannot supply arbitrary code, contacts or topology.

No resource limit increases. No authoring, snapshot execution or new mathematical
proof is introduced. Both recipients and all availability transitions still use
the same original workflow deadline and preallocated request/verification grants.

## What READY means

`READY` means the service is listening and its configured bootstrap dial attempts
have completed. It does **not** mean routing is ready or a provider is discoverable.

The result explicitly includes:

```text
startup_assurance = LISTENING_AND_DIAL_ATTEMPTED_NOT_ROUTING_READY
query_readiness = EVENT_BASED_UNDER_ORIGINAL_OPERATION_SIGNAL
routing_peers = actual current DHT routing-table size
```

`known_peers` remains the application descriptor-cache size, a different quantity.
A neutral bootstrap with no initial peers can start. The subsequent DHT query
waits for the retained library's peer-admission/initial-self-query events under
the original query signal. No fixed startup delay, private provider preload,
polling loop or silently renewed timeout is used. No reachable peer means a
bounded incomplete result, not a statement that no relevant mathematics exists.

## Publication outcome

Each publication returns its route key, a status, termination, optional thrown
error, fixed-size event census and routing-table sizes before/after the query.

| Status | Exact meaning |
|---|---|
| `HINT_DISPATCHED_UNACKNOWLEDGED` | At least one retained-library local `ADD_PROVIDER` write completed; its iterator ended without a yielded query error or abort. |
| `INCOMPLETE` | No completed write, a yielded query error, or an aborted/failed query. Some partial writes may have occurred; the census preserves them. |

Both statuses set `remote_placement_confirmed:false`, `global_complete:false`
and `mathematical_acceptance:false`. The adopted DHT's provider RPC has no reply;
its `PEER_RESPONSE` event for that RPC is a local write observation, not a remote
storage acknowledgment. A local positive status cannot substitute for actual
subsequent discovery. The harness saves every returned publication before judging
whether it satisfies the operation's dispatch precondition.

## Route outcome

`observed_route.route` uses the existing actual workflow, one unchanged ticket
and the same child channel. It does not create another locator or allowance.
Its result retains the existing advisory peer list and adds:

- `termination`: `ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE`, `PROVIDER_BUDGET`,
  `INCOMPLETE_QUERY_ERRORS`, or `INCOMPLETE_ABORTED_OR_FAILED`;
- `error`: bounded thrown-error text or null;
- `census`: `events`, `send_query`, `peer_response`, `final_peer`, `query_error`,
  `provider`, `add_provider_write`, and bounded `last_query_error`;
- `routing_peers_before` and `routing_peers_after`.

These counts describe yielded query events, not packets, wire bytes or remote
work. They do not refund the original precharged allowances. A route may return
usable advisory hints while incomplete; successful descriptor authentication,
formal-index checking and mathematical admission remain separate obligations.
Malformed IPC/diagnostics, channel failure and expired workflow deadlines remain
fail-closed. Only the existing narrowly typed TCP-connect descriptor miss can
support same-channel continuation under the already reserved second route.

## What the eventual integrated result must show

The genuine unknown-ID route must actually lead to a formal index and complete
packet. Reader1 must cold-admit that packet and retain its own semantic custody.
After origin closure, fresh reader2 must consume its genuinely stale route,
observe typed unavailability, discover the independent retained replica, cold-admit
the packet and reconstruct the ordinary import context from its own readback.
No source ID, expected provider identity, private HTTP address or accepting
report is an input to reader candidate choice.

The startup repair makes the query/readiness contract correct; it does not itself
establish this full endpoint, worldwide coverage, independent-host availability,
cheaper useful growth or v5 release completion.
