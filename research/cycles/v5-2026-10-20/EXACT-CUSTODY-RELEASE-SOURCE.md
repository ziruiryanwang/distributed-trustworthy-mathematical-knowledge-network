# Exact-custody location and provider source checkpoint

2026-10-20, core_release. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Implements the selected contract21f4a095 under
`EXACT-CUSTODY-IMPLEMENTATION.md`. This is source construction and manual
source inspection only: no imports, parsers, tests, child processes, network,
native verification, proof production, builds, installation or Git operations
were executed. No runtime result or release adoption follows.

## Concrete change

The selected113 logical source map has eight fresh successors below
`software/v5/body_location/`; predecessors remain untouched.

- Python/JavaScript agree by source construction on the semantic namespace,
  four-field body reference, rendezvous key and distinct body request/reply.
  ExportID is computed by the existing Python module codec; the Node wire does
  not reinterpret Lean names. The old index role/schema remains distinct.
- V2 maintained roles enable a pinned semantic domain in the same child. Both
  stream handlers share serving/request/reply counters and the transport;
  both advertisements share the original intent transaction and key quota.
  Four explicit IPC commands reuse existing frame/sequence/byte limits.
- Old index operations and the new body operations validate their own exact
  role bindings before `_publishRoute`, `_withdrawRoute`, `_locateTicket`,
  `_descriptorTicket` and `_serveDescriptor`. V1 cannot use the new role.
- Service V3 permits zero index routes but requires1..8 exact owner-selected
  body addresses and explicit nullable `index_view`. It counts both route
  sets against one key limit and one publication/health/stop reservation.
  Selected projected index serving and cleanup remain available.
- `_body_readback` runs while the opened workspace lock is held and before
  HTTP/Node startup. It checks actual store/adapter/configured wire/packet
  foundation and policy, then calls unchanged `ModuleStore.get_body` once
  per selected row. Each decoded body is discarded before the next read.
  Only compact references are advertised; publication is not placement proof.

## ABI for integration and controls

Python `location.protocol` exports:

```python
body_namespace(domain)
body_ref(value)
body_route_spec(namespace, body)
body_route_key(namespace, body)
body_descriptor_request(namespace, body, nonce, max_bytes=4096)
validate_body_request(value)
verify_body_descriptor(raw, request, authenticated_peer, policy)
```

The JavaScript equivalents use camelCase; reply creation is
`makeBodyDescriptor(request, authenticatedLocalPeer, endpoints, policy)`.
`validateIntentSpec(spec,key)` accepts only the exact index or body spec/key.

Provider private test seams:

```python
_body_routes(rows)  # validates/deduplicates exact1..8 addresses, returns copy
_body_readback(workspace, routes, deadline)
# -> {domain, namespace, refs, observations}
```

`observations` contains `bodies_read`, `encoded_input_ceiling_bytes`,
`input_bound_scope`, `assurance`, `remote_placement_confirmed=False` and
`mathematical_acceptance=False`. The bound is32MiB per selected row across
group+expression encoded inputs, not measured bytes or a RAM claim. Assurance
is `READ_BACK_BEFORE_SERVICE_NOT_CONTINUOUS_AVAILABILITY_PROOF`.

V3 result/ready schemas expose `body_readback`, `body_route_dispatch` and
`remote_placement_confirmed=False`; other service health and cleanup retain
their predecessor meanings. V2 Node configuration receives `body_domain`;
its status still reports the original index namespace. Body location helpers
derive their semantic namespace from the pinned configuration, not status.

## Source identities

Paths below are relative to `software/v5/body_location/`.

| Source | SHA-256 |
|---|---|
| `portable/location/protocol.py` | `06f381fb9e4b7b597a0bcb5e72084dbb2689a5cce4c0d8f751868a6bb0ec8cbd` |
| `portable/location/protocol.mjs` | `88c2bc34e5ebefc412b564bef06e0d4210e0c44e3102be1d6adacfc6334af986` |
| `portable/location/intent.mjs` | `220bff266e58f9a460cb182bdc16fb86654fa26f88eee27e8994fb7cd028ad08` |
| `portable/location/maintained_roles.mjs` | `128a5bd4a9f32721e7fa4e149f3c51719fd26dd6f8f6ca22ef389a609899ae77` |
| `portable/location/ipc_wire.mjs` | `34a6245abb7270ec9785e57c392dbbcc6399931ccba9d9d421e737f7c0aab519` |
| `portable/location/node_entry_services.mjs` | `7efae4a2be0de16d20f9d8f334e514a8a042798aee61f3c0e70b093904944205` |
| `portable/location/controller_services.py` | `eeb82d5dd6fe34915d07b2927e7ddd44ee2b5b80278dbf4d2889b87222ad1501` |
| `client/serve_advertised.py` | `28a5b10b8531f277dc9c1a30f1afe2ff0957a5e7936ebcf399acacae265f3f70` |

## Retained boundaries

Manual inspection found no duplicate method braces or accidental second child,
role quota or contact authority. Exact Python/JS equality, refusal cases and
service failure ordering still require the selected independent controls.
Shared transport/capability integration remains separately owned and reviewed.
Compact location does not increase HTTP's unchanged16KiB raw-name request cap.
No continuous availability, complete discovery or mathematical acceptance is
claimed by any advertisement. Full v5 remains unfinished.
