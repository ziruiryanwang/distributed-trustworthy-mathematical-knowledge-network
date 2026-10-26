# Contact directory helper and HTTP provider: source handoff

Owner: `ordinary_routing_gap`. Implemented under root's CONTRACT.md. No imports,
tests, network, builds, mathematical admission, state changes or Git operations
were executed. Independent source review and root's finite selection remain
required before this source is used. Other authors own the peer compositions,
launcher, fair transport route allowlist and exact package/profile closure.

## Exact selected predecessor

The provider successor starts from the actual adopted ordinary package:

`experiments/v5-local-checks/fair-investigator-assembly01/assembled/package/support/transport/http_provider.py`

Baseline SHA-256:
`22858b0b9e21abdde2e076efa123552f7ff30c3fc0166ec377621ba905acee97`.
No predecessor bytes were edited. `http_provider.py` is a fresh source successor;
the new pure helper is `contact_directory.py`, logically `transport.contact_directory`.

## Helper interface

Constants:

- `ROUTE = "/v5/ordinary/contacts"`
- `MAP_SCHEMA = "DMKN_ORDINARY_CONTACT_MAP_V1"`
- `REQUEST_SCHEMA = "DMKN_ORDINARY_CONTACT_REQUEST_V1"`
- `REPLY_SCHEMA = "DMKN_ORDINARY_CONTACT_REPLY_V1"`
- `STATUS = "ADVISORY_INDEX_CONTACTS"`
- `ASSURANCE = "UNVERIFIED_SPECIALIST_REGISTRATION"`
- `MAP_MAX = 2097152`, `REPLY_MAX = 32768`, `MAX_KEYS = 2048`,
  `MAX_ENDPOINTS = 16`, `MAX_CONTACTS = 64`.

`ContactMap.from_bytes(raw, check_budget=None)` accepts only canonical JSON bytes:

```text
{schema: MAP_SCHEMA, namespace: HEX64,
 entries: [{features: sorted nonempty unique HEX64[1..8],
            endpoints: [endpoint[1..16]]}][0..2048]}
endpoint = {host: canonical IPv4, port: 1..65535,
            tls: genuine Boolean, server_name: strict lowercase DNS name or null}
```

Exact duplicate route keys and duplicate endpoints within one route are refused.
The map retains immutable encoded rows, not mutable caller dictionaries, and is
a frozen dataclass. Public fields: `namespace`, `raw_sha256`, `key_count`,
`contact_count`; lookup method `.reply(request, check_budget=None)` returns bytes.
The function `reply(contact_map, request, check_budget=None)` enforces exact map
type. Returned parsed objects do not expose retained row storage.

Requests have exactly `schema`, `namespace`, `features`, `nonce`, `max_contacts`,
`max_bytes`; the namespace/nonce are HEX64, features are canonical 1..8 hashes,
contact limit is 1..64, byte limit is 1..32768. `request_limit(request)` validates
and returns the byte limit. Too-small limits are refused if even an empty reply
envelope does not fit.

Replies have exactly `schema`, `namespace`, `features`, `nonce`, `status`,
`assurance`, `contacts`, `truncated`, `global_complete`, `mathematical_acceptance`.
They echo the exact request domain/key/nonce, carry the constants above, and
require both assurance Booleans to be false. `read_reply(raw, request)` returns
a detached validated dictionary. It validates endpoint **syntax only**; it does
not authorize dialing or prove freshness, endpoint possession or mathematical
truth. The caller must separately use the owner egress policy and fixed lease.

A missing key or different requested namespace returns a request-bound empty
advisory reply. This says nothing about absence outside the local partial map.
A stored row returns a deterministic insertion-order prefix constrained by both
caps; `truncated` reports omitted stored rows, not global completeness. No scan,
subset search, remote write, second-hop referral, code or filesystem action is
performed by the helper.

## Owner egress

`OwnerEgressPolicy(config)` preserves the pure endpoint semantics from
`software/v5/portable_runtime/location/protocol.py` without importing that
runtime. Its accepted config schema remains `DMKN_V5_OWNER_EGRESS_V1` with exact
`mode`, `public_ports`, `test_endpoints` fields. Public mode requires listed
ports, public canonical numeric IPv4 and HTTPS; test mode lists exact
`127.0.0.1` ports. No remote CA path, DNS dialing, private/public-mode address,
IPv6 or mapped-address fallback is accepted.

The policy is frozen and snapshots canonical config bytes. `.report()` returns
a fresh config copy and the explicit system-CA/trusted-owner-environment premise.
`.endpoint(row)` returns the exact selected `http_provider.Endpoint` with
`ca_file=None` only after policy validation. `endpoint_spec(row)` returns copied
syntax-validated fields but is deliberately **not an egress authorization**.

Private numeric addresses can be represented as inert syntax; they cannot pass
the public owner policy. The reader must reject them before any connection.
Directory seed contacts remain separate explicit owner choices with their own
existing CA pins. None of this helper's data establishes a transferable dial
grant, lifetime extension or mathematical acceptance.

## Minimal provider difference

Only these provider sites changed:

1. Module/dispatch documentation describes the additional advisory role.
2. `CONTACT_DIRECTORY_ROUTE` and its fixed 32768-byte hard ceiling are added.
3. Constructor accepts optional `contact_directory`, permits it as the sole
   provider role, checks exact `ContactMap` type and retains it.
4. Closed dispatch calls `contact_directory.reply` for that route only.
5. The existing per-request reservation path calls its `request_limit` before
   the aggregate provider reply-budget test.
6. The existing byte-reply branch includes this route (no double JSON encoding).

Endpoint/TLS transport, header/body parser, old routes, provider request/byte/
connection quotas, operation deadline, sockets, task ownership, stop and status
logic are preserved. No global lookup, outbound referral, index, custody or
catalogue is needed by a directory-only `Provider(contact_directory=map)`.
The old provider's cleanup semantics are not newly qualified by this source edit;
the public composition still owns the original finite lease and cleanup reserve.

## Integration obligations

- The API author supplies the ordinary compiled namespace/features and applies
  the owner policy before retaining learned contacts.
- The reader anchors contact expiry at request **start**, narrows only, prepays
  the directory slice while `OrdinaryBudget.sequence == 0`, preserves the exact
  search remainder and invokes existing find at most once on the same ledger.
- Root's fair-exchange successor explicitly admits `H.CONTACT_DIRECTORY_ROUTE`
  while preserving uncertain-closure refusal; the older two-route allowlist
  intentionally refuses this new route.
- The public directory service compiles formal registration specs locally,
  constructs canonical map bytes and serves them in memory for one finite lease.
- Public dispatch, profile role pins, source recipe and tests are other owners'
  assignments. These two payloads alone are not an adopted runnable package.
