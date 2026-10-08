# Maintained discovery: dependency and design decision

2026-10-06. Root-owned design under the renewed full-v4 reaudit. Source/theory
and dependency acquisition only at this point; no peer service or public-network
joining is selected. The prior private TLS peer stays frozen and is not relabeled
as a maintained overlay. This work must become integrated software, not only a
library recommendation.

## Choice being developed

Use a mature libp2p Kademlia implementation rather than expanding the old fixed
contact list or one-split directory into an unreviewed bespoke DHT. Node v24.16.0
is available locally. Registry metadata on this date reports libp2p3.3.11 and
@libp2p/kad-dht16.4.5. Pin exact acquired versions and the generated dependency
lock. npm acquisition may run only with dependency scripts disabled; do not
start imported code or a service merely by fetching it.

Select a custom application/DHT protocol namespace, explicitly configured initial
contacts, persistent peer identity/state, and no default public bootstrap,
multicast discovery, telemetry, public swarm joining or external deployment.
Qualification peers will listen/dial only loopback. This is an isolated local
test of the same maintained algorithms, not proof of physical-world uptime.

The Kademlia layer supplies bounded-degree peer routing and provider hints for
domain-separated mathematical object/query keys. The mathematical layer retains
exact manifest/framing/namespace checks and final independent proof checking.
Neither provider status nor authenticated transport asserts a valid theorem.
No natural-language or human-intention layer is added.

## Exact integration obligations

1. No full network roster or global corpus scan at startup or per query. Bound
   routing-table storage, query concurrency/deadline and returned candidates.
2. Use authenticated peer streams for bounded metadata queries and exact fragment
   acquisition. Reuse the actual inert codec and final checking path; do not
   invent a second mathematical acceptance rule in JavaScript.
3. Provider expiry, renewal and routing-table refresh must actually operate.
   Persistent local record selection, custody limits and reprovide capacity
   remain application obligations, not magically supplied by a DHT.
4. Exact identity lookup, exact-type/structural candidate discovery and full
   enumeration have different guarantees. Hot keys need bounded candidate
   views/refinement; a cheap query cannot enumerate arbitrarily many matches.
5. Apply owner endpoint policy before dialing learned addresses, including
   prohibition on unintended local/private destinations in public mode. Admit
   only bounded untrusted frames/metadata. Peer identity is transport integrity,
   not attribution or Byzantine routing completeness.
6. Initial peer absence, partitions, budget exhaustion, overload, stale adverts
   and unavailable holders return explicit incomplete/failure states. They may
   not become global absence or mathematical rejection.
7. Integrate the public operation envelope and document startup, join, publish,
   lookup, acquire, renew, leave/restart and storage capacity. Avoid a one-shot
   demo with no maintenance lifecycle.

## Conditional scale argument to complete against source

Routing can be logarithmic in network size under a stated healthy/routable
membership and routing-table coverage model. This is not a worst-case theorem
under arbitrary malicious identities, partitions or adversarial churn. Local
fixed resource caps imply incomplete operations outside their envelope.
Provider metadata and actual retained theorem bytes require separately funded
storage. Reprovide/repair work must fit capacity with renewal delay margins;
publication rates cannot exceed service/storage growth indefinitely. Rare useful
results cannot be guaranteed discoverable by simply ranking popular providers.

The release claim must name exactly what the selected library implements and
what our adapter adds, then qualify actual unknown-holder retrieval, join/refresh,
expiry/renewal, interrupted-holder alternatives, malformed inputs, limits and
fresh mathematical checking. Never infer these from merely importing libp2p.

## Primary sources and observations

- [libp2p Kademlia specification](https://github.com/libp2p/specs/blob/master/kad-dht/README.md), inspected2026-10-06: client/server roles, XOR routing, provider advertisement/discovery, bootstrap and maintenance parameters guide this design; they do not prove this integration conforms.
- [libp2p DHT overview](https://docs.libp2p.io/concepts/fundamentals/dht/): maintained routing/provider concepts; bootstrap reachability is a join prerequisite, not an indispensable central server.
- [JS kad-dht documentation](https://libp2p.github.io/js-libp2p-kad-dht/) currently renders v9.3.8 while registry reports16.4.5. Do not code against that stale API: inspect the exact acquired package source/types.
- [Kubo RPC API](https://docs.ipfs.tech/reference/kubo/rpc/) and [experimental features](https://github.com/ipfs/kubo/blob/master/docs/experimental-features.md) were inspected as alternatives. Kubo stream tunneling adds another experimental subsystem; direct libp2p is the selected candidate instead.

Dependency fetching is selected into `experiments/maintained-overlay-01/project`.
No existing package or global Node installation may be changed. This document
is not product/runtime authorization; exact application source and test selection
follow source/API inspection and the independent design review.
