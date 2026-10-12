# Actual retained two-delta network endpoint: configuration proposal

This document proposes one fresh root-selected operation, not an executable
configuration, runtime permission, actual pass or public deployment qualification.
All file references and seven ports must be resolved and pinned by root. The
harness never authors mathematics or manufactures receipts/verified handles.

## Inputs and exact key schema

Run the selected snapshot's `delta/network_actual.py` with `--config` and
`--config-sha256` under the existing isolated finite owner Job. Configuration has
exactly these keys:

| Key | Meaning |
|---|---|
| `schema` | `DMKN_V5_ACTUAL_DELTA_NETWORK_V1` |
| `packet` | Exact `{path, bytes, sha256}` retained complete two-delta packet. |
| `lineage` | 1–16 exact file pins recording source-derived lineage/repair/admission. Evidence is not authority. |
| `preparation_profile` | Exact retained profile pin; its `producer` supplies independently adopted frontier-verifier runtime. |
| `foundation` | Exact local adopted foundation-row pin, used only to reconstruct ordinary authoring context. |
| `native_executable` | Exact genuine native relation-checker file pin, also present in `runtime_pins`. |
| `runtime_pins` | Exact loaded snapshot Python/controller/helper closure plus selected native runtime and executable. No canonical-source borrowing from another snapshot. |
| `location` | `{source_directory, source_pins, role_pins, entry_source}` as below. |
| `ports` | Seven distinct owner-selected loopback TCP ports, keys below. |
| `output_directory` | Fresh absent canonical path under `experiments/v5-local-checks`, not overlapping any selected input/source/runtime. |
| `limits` | Exactly the finite maps below. |

The intended retained packet is the independently audited, corrected
`delta-reprepare-01/evidence/delta-packet.json`, 662480 bytes, SHA-256
`54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1`.
The earlier failed author01 packet remains failed and is not selected. No
successful authoring/export is repeated to supply this network endpoint.

`location.source_directory` is a fresh exact adopted Node source snapshot whose
last three components are `software/v5/location`, under `experiments/v5-local-checks`.
`source_pins` has the existing exact nine `SOURCE_NAMES`; `role_pins` has the
existing exact five `ROLE_NAMES`. The sole intentional snapshot alias is the
fresh reviewed canonical `location/node_entry_services_available.mjs` copied as
`node_entry_services.mjs`. `entry_source` pins the canonical fresh entry, and its
hash must equal the selected alias's role hash. The other thirteen files are
unchanged adopted source. This preserves the exact existing controller class,
framing, role schema, libp2p/Noise/DHT implementation and runtime manifest.

`ports` has exactly `bootstrap`, `origin_location`, `replica_location`, `reader1`,
`reader2`, `origin_http`, `replica_http`. Root checks availability immediately
before selecting the launch. That observation cannot eliminate a port-binding
race; a later bind failure is a charged failure, not permission to choose new
ports or repeat the campaign. The broad local egress allowlist is permission to
dial returned contacts, not a preloaded holder list. Readers receive only the
neutral bootstrap address; no result-provider peer ID or HTTP endpoint is given.

## Proposed finite values

Root selected a **480-second original workflow deadline**, inside the unchanged
600-second enclosing owner wall ceiling, leaving time for teardown/final records.
It starts before input validation. Both readers inherit this absolute deadline;
neither creating a reader nor changing provider availability renews it.

The following JSON is a limits proposal, not a runnable selected configuration:

```json
{
  "wall_seconds": 480,
  "call": {
    "native_cpu_seconds": 30,
    "receipt_cpu_seconds": 30,
    "wall_seconds": 60,
    "memory_mib": 1024
  },
  "node": {
    "service_ms": 480000,
    "operation_ms": 15000,
    "query_events": 512,
    "provider_limit": 4,
    "advertised_keys": 2,
    "provider_ttl_ms": 120000,
    "reprovide_interval_ms": 30000,
    "maintenance_ms": 60000,
    "commands": 32,
    "descriptor_requests": 16,
    "descriptor_reply_bytes": 65536,
    "metadata": {},
    "transport": {
      "outbound_attempts": 128,
      "inbound_upgrades": 128,
      "receive_bytes": 8388608,
      "send_bytes": 8388608
    }
  },
  "location": {
    "wall_ms": 180000,
    "route_operations": 2,
    "routing_events": 512,
    "routing_peer_slots": 8,
    "descriptor_requests": 8,
    "contacts": 4,
    "reply_bytes": 1081344
  },
  "search": {
    "providers": 4,
    "snapshots": 4,
    "requests": 8,
    "pages": 4,
    "examined": 128,
    "candidates": 16,
    "bytes": 1048576,
    "wall_ms": 90000,
    "inflight": 1
  },
  "candidate": {
    "scanned": 32,
    "matches": 8,
    "bytes": 131072,
    "timeout_ms": 1000,
    "record_probes": 256,
    "node_reads": 32768,
    "hash_calls": 200000,
    "sql_vm_steps": 1000000
  },
  "acquisition": {
    "requests": 32,
    "reply_bytes": 33554432,
    "verify_attempts": 1,
    "verification_input_bytes": 16777216,
    "worker_cpu_seconds": 90
  },
  "module_store": {
    "modules": 32,
    "groups": 128,
    "declarations": 512,
    "bodies": 256,
    "logical_bytes": 33554432,
    "db_pages": 16384
  },
  "packet_store": {
    "packets": 4,
    "offers": 8,
    "offers_per_module": 2,
    "packet_bytes": 16777216,
    "logical_bytes": 67108864,
    "db_pages": 32768
  },
  "index_store": {
    "max_objects": 128,
    "max_postings": 8192,
    "max_features": 1024,
    "max_snapshots": 256,
    "max_logical_bytes": 33554432,
    "max_db_pages": 16384
  },
  "provider": {
    "max_connections": 2,
    "max_requests": 32,
    "max_reply_bytes": 67108864,
    "operation_ms": 10000
  },
  "offer_bytes": 8192
}
```

Each prospective handoff prepays 2 route + 8 descriptor + 8 search request
ceilings, and 1081344 reply bytes, before its reader starts. Reader1 uses only
one route and receives no refund. Reader2 reserves two routes from the outset.
The full packet admission reserves 30 receipt + 2 × 30 native = 90 CPU seconds,
inside both its acquisition budget and its separately owned receiver allowance.
There are exactly two independent recipients: at most two cryptographic receipt
verifications and four native relation checks for the complete endpoint. These
are ceilings; actual CPU is measured separately. Repeated nested reservations
must never be added as if they were additional consumed CPU.

Per-node service/transport limits do not replace the outer Job. All five Node
lifetimes, runtime pre/post hashing, provider SQL/HTTP work, Python semantic
reconstruction and failed operations consume real resources. DHT routing events
are not wire-byte measurements. Maximum concurrent location children is three;
native supervision adds its own selected bounded descendants. Root must size the
unchanged owner process/memory/CPU grant for the full closure and finalization,
not just the two verification calls.

## Endpoint and absence semantics

1. Origin stores the exact selected packet and its structurally committed groups
   and available definition/recursor bodies. It indexes target formal exports and
   advertises the existing formal-feature rendezvous key.
2. Reader1 starts with only the neutral reader/router bootstrap plus formal query
   features: theorem kind, equality result head, and known base `fold` symbol. It
   locates an index, obtains an authenticated descriptor, searches, acquires the
   first returned candidate and complete packet, and genuinely cold-admits it.
3. Reader1 derives selected semantic custody from those acquired packet bytes.
   Its mathematical owners and location reader close. Replica is prepared from
   this independent custody, with no borrowed live handle or private origin store.
4. Fresh reader2 starts and performs a real first route while origin is reachable
   and replica has not advertised. It has acquired/accepted no mathematics.
5. Origin HTTP, origin Node and all origin stores close. Replica starts from
   reader1's retained packet/groups/bodies and actually serves its own formal index.
6. Reader2 attempts its genuinely returned stale peer. Only a narrow typed local
   TCP-connect unavailability is recoverable; its full descriptor allowance is
   charged, with no authenticated-peer or global-absence assertion. It spends its
   already reserved second route on the same channel/deadline. Already failed
   *publicly returned* peer IDs may be skipped; no private replica ID is used.
7. Reader2 discovers, acquires and cold-admits the same complete packet through
   the surviving replica. From its own durable semantic readback and its live
   accepted closure, it opens a `DeltaImportSession` and reconstructs ordinary
   authoring context, without ancestor theorem proofs in the frontend. No Lean
   compilation or new theorem is produced during this network endpoint.
8. All owners, HTTP tasks, stores and Node processes close independently even if
   another closer fails. Runtime pins, reader-role purity, actual call counts,
   original deadline and final report write are checked. A sibling
   `FINALIZATION-FAILED.json` overrides any earlier PASS-bearing result.

Invalid mathematical packets, authentication errors, malformed descriptors,
unclassified transport errors, resource exhaustion and expired grants stay
fail-closed. A typed unavailable peer is not proof that no result exists. This
same-host endpoint establishes neither independently hosted availability nor
worldwide semantic-search completeness or sustained net useful growth.
