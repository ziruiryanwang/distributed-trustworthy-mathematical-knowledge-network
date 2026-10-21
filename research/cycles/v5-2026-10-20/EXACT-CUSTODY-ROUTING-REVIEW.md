# Independent custody routing/provider source review

2026-10-20, core_growth. Source inspection and read-only diffs only. No imports,
tests, build, Node child, network, proof, installation or Git mutation occurred.
Reference contract: `EXACT-CUSTODY-CONTRACT.md` SHA-256 `21f4a095` (full hash in
`EXACT-CUSTODY-REVIEW.md`). Root retains runtime/integration authority.

**GO for the reviewed source boundary; no blocking implementation issue found.**
This does not qualify execution or establish continued global availability.

## Exact source identities

Paths below are relative to `software/v5/body_location/`.

| File | SHA-256 |
|---|---|
| `portable/location/protocol.py` | `06f381fb9e4b7b597a0bcb5e72084dbb2689a5cce4c0d8f751868a6bb0ec8cbd` |
| `portable/location/protocol.mjs` | `88c2bc34e5ebefc412b564bef06e0d4210e0c44e3102be1d6adacfc6334af986` |
| `portable/location/intent.mjs` | `220bff266e58f9a460cb182bdc16fb86654fa26f88eee27e8994fb7cd028ad08` |
| `portable/location/maintained_roles.mjs` | `128a5bd4a9f32721e7fa4e149f3c51719fd26dd6f8f6ca22ef389a609899ae77` |
| `portable/location/ipc_wire.mjs` | `34a6245abb7270ec9785e57c392dbbcc6399931ccba9d9d421e737f7c0aab519` |
| `portable/location/node_entry_services.mjs` | `7efae4a2be0de16d20f9d8f334e514a8a042798aee61f3c0e70b093904944205` |
| `portable/location/controller_services.py` | `eeb82d5dd6fe34915d07b2927e7ddd44ee2b5b80278dbf4d2889b87222ad1501` |
| `client/serve_advertised.py` | `28a5b10b8531f277dc9c1a30f1afe2ff0957a5e7936ebcf399acacae265f3f70` |

Compared each successor with the source selected by the installed113 map;
read the retained engines and provider cleanup as well as the changed blocks.

## Protocol and role separation

Python/JavaScript namespace descriptors, hash domains, canonical field shapes,
arity bounds, role tags, request/reply schemas and fixed4096-byte descriptor cap
match by source. Body refs contain only exact hex identities and bounded arity;
name hashing remains in the existing Python module codec. No raw Lean name is
parsed by Node. The helper ABI matches `body_custody.py`.

Existing index helper bodies are unchanged. Body and index schemas cannot be
substituted: canonical reconstruction checks exact role/spec, and separate
request/reply schemas and descriptor stream protocols bind the selected role.
Python validates canonical raw reply, nonce, key, semantic namespace, actual
authenticated peer, fixed endpoint count and unchanged owner egress policy.
These remain advisory contacts, not mathematical or availability proofs.

V2 configuration explicitly adds one exact foundation/policy domain. V1 retains
its previous shape and body commands fail its domain gate. A V2 reader gains
no publication or descriptor-serving authority. Body namespace is derived from
startup configuration and rechecked before body operations; it never replaces
the index namespace or depends on the selected discovery profile.

## One child and aggregate limits

The four new IPC commands are admitted by both the pipe allow-list and actual
entry dispatcher. Body descriptor dispatch rejects foreign absolute `until`,
uses the same remaining-duration truncation and narrow typed TCP-connect miss,
and keeps all other errors terminal. Existing pipe count/byte/source-map shapes
are unchanged; no extra runtime dependency or process was introduced.

The maintained locator's role-specific wrappers validate before entering the
shared publication, withdrawal, route, descriptor and serving engines. Both
roles use the same DHT, peer cache, transport counters, lifetime, metadata,
`advertised_keys`, command counter and descriptor-serving reservations. Adding
a second descriptor protocol does not add a second `serving` or reply pool.
The common application count stays at two active handlers; rejected extra
streams still consume the existing finite transport/mux capacities.

`intent.mjs` now delegates to a closed two-role exact spec/key validator.
Atomic insertion of both local intent and publication remains unchanged, as
does the synchronous provider-write intent guard and revoke transaction.
An unknown role falls through to exact body reconstruction and is rejected;
it is not accepted as an arbitrary role. Both roles occupy the same key quota.

The private known-peer cache still supplies only dial hints. Body descriptor
key/peer association is enforced by the Python request owner, not inferred
from a cache entry. Reserved progress-hook events and observed iterator census
are distinct measures; neither proves a complete DHT wire-byte count.

## Provider selection, read-back and cleanup

V3 accepts one to eight explicit body rows and may advertise no index predicate.
It keeps existing ordinary/projected index selection and the actual composite
HTTP provider, not a second provider framework. Both body and index publication
counts enter the same advertised-key and publication/health/stop command bounds.

Before HTTP/Node construction, the opened workspace lock is required and each
selected body is fetched through ordinary `ModuleStore.get_body`. That path
checks the committed declaration, name/arity/hash permissions and canonical
expression. Domain equality covers actual codec, module store, adapter,
configured wire profile and packet-store profile. The result keeps compact refs
and bounded observations, discarding each decoded expression before the next.
The encoded-input ceiling is explicitly not RAM or measured execution cost.

A missing/corrupt selected body exits before either service starts. The existing
finally path then closes the optional projection/workspace and persists failure;
no partially successful body advertisement is fabricated. Later exceptions or
partial publication use the same Node-stop, process-reap, HTTP-drain and lock
cleanup as the predecessor. A cleanup uncertainty keeps the result FAILED.

The report states read-back-before-service only and no remote placement.
No renewal proof, independent replica claim, global inventory or future
availability guarantee has been introduced. The existing private workspace
ownership excludes normal concurrent local mutation, not disk/process failure.

## Remaining verification boundary

Cross-language vectors and focused new-role/old-role controls still need the
root-selected execution. Root's fresh distribution source map must include
these exact successors and propagate V3 service injection. The inherited16KiB
body-HTTP request limit remains; compact location alone does not remove it.
No repeated theorem proof or broad network campaign is needed for this review.
