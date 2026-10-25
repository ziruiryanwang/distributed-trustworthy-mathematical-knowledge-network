# Advisory authoring-offer transport boundary

2026-10-24. Source-only implementation under CONTRACT.md. No tests, service,
owner/store opening, source-repository access, native execution or Git mutation.

## Selected source delta

Fresh exact copies came from
`experiments/v5-local-checks/symbol-inspection-assembly-01/package/support/transport`.
The copy hashes were verified before editing; predecessor files remain unchanged.

| File | Predecessor SHA-256 | Candidate SHA-256 |
|---|---|---|
| http_provider.py | 431aae7f10f1a2c0c0323c4aea720f4139e57bb4bf7b61bf98e9e5b69d6cdd59 | 22858b0b9e21abdde2e076efa123552f7ff30c3fc0166ec377621ba905acee97 |
| ordinary_acquisition.py | e69bd0f33829e4709fdc1a7c3afe4150704dfeabfe30243195b379945081e826 | d4599471b1285650876d53763c4a618a4dd5d7a953197954249052771a9df64f |

Only the optional authoring-offer role/route/client method and essential comments
change. Existing custody data, mathematical formats, native checking, discovery
routes, endpoint selection/TLS and connection cleanup are not altered.

## Provider contract

`AUTHORING_OFFERS_ROUTE = "/v5/ordinary/authoring-offers"`, reply ceiling32KiB.
`Provider(authoring_offers=map)` optionally receives an exact
`transport.authoring_offers.OfferMap` already parsed from the owner's selected
finite sidecar. It can serve alongside existing roles or as its only role.
The transport does not load a file or construct an index per request.

The route is intentionally separate from `ORDINARY_ROUTES`. Dispatch requires
the optional role, then calls `authoring_offers.reply(map, request,
check_budget=...)`, which validates the exact key and returns bounded canonical
bytes. No role means the unchanged `ROLE_NOT_SERVED` failure/connection-close
behavior, not a claim that no source exists. Existing roles remain usable without
the map and do not import its codec unless that role/route is used.

The HTTP service validates `request_limit(request)` before reserving the selected
reply cap, uses the existing aggregate service quota/deadline, emits the returned
bytes, and releases its reservation in the unchanged finally block. Interrupted
and malformed requests retain the existing request-count/cleanup behavior.

## Acquisition contract

```text
await client.authoring_offers(provider, semantic_id, export_id,
                             max_bytes=32768, max_offers=8)
```

`max_offers` is keyword-only. The selected semantic ID must equal the current
adapter's semantic ID. Request fields are `schema`, `semantic_id`, `export_id`,
`max_offers`, `max_bytes`; schema is codec `REQUEST_SCHEMA`. The generated request
contains no repository URL, local path, executable instruction or arbitrary
provider-selected referral.

The method calls the existing `_fetch` once with codec `read_reply(raw, request)`
and `retain=None`. Result fields are `raw`, `reply`, `assurance` and
`mathematical_acceptance:false`. Assurance is explicitly unverified authoring
associations, not execution or mathematical authority. The codec checks exact
query/reply binding, fields and caps. No returned URL is followed or executed,
and nothing is cached in ordinary custody.

The original caller budget, request ticket, conservative full-reservation failure
charge, actual successful-byte charge and HTTP cost counters are unchanged.
The caller still owns ledger close and any outer hard process containment.

Because `ordinary_acquisition.request_limit` now recognizes an additional route,
its custody-only `serve` explicitly rejects that route with
`AUTHORING_OFFERS_NOT_CUSTODY`. It cannot accidentally fall through to the old
evidence lookup. Provider routes advisory metadata directly to its separate map.

## Review/qualification boundary

Independent review should check the new role type, absent-role behavior, exact
request/reply binding, variable response reservation, failed-read charges,
separation from ordinary custody, and absence of repository/network-following
effects. Root owns facade/profile integration and any future bounded execution.
No source association here establishes availability, compatible dependencies,
project correspondence, safe executable code, acceptance or research benefit.

## File-only integration preparation

Root additionally assigned assemble.py, derived from the completed inspector's
assembler. Source SHA-256:
`a72f5b0a4d2676421c03fbb2a088de03786d4ac953600d044a6fa1c0ad6705a0`.
No assembly was executed. Independent reviewer has the exact source/diff.

Its only baseline is the completed symbol-inspection package, PROFILE
`a8d10b6ba7048f90ae4bf2411b7662090199934380fd24b042b62ff5ceb40960`,
with the existing ASSEMBLY receipt also pinned and admitted into the source census.
That historical receipt is not copied as a runtime payload. Native artifacts,
installation/implementation identities and the141-payload baseline remain fixed.

Replace peer.py,peer_api.py,profile.py and the two transport helpers; add only
support/transport/authoring_offers.py. The exact output has142 payloads, five
changed and136 unchanged, plus the newly generated PROFILE/ASSEMBLY records.
The profile has112 auxiliary roles rather than111. All six source files are flat
under ordinary_authoring_offers; their fixed logical destinations are in SOURCES.

Required arguments are --source-root (runner snapshot), --base-package,
--base-profile-sha256, --payload-map-sha256, --python-runtime, --lean-runtime,
--output, --wall-seconds and --cpu-seconds. The aggregate reviewed digest is
SHA256 of existing canonical_json(source_pins), where source_pins maps each of the
six runtime logical paths to its exact {bytes,sha256}; not source-relative paths.
The snapshot also includes the existing pinned ordinary_package/build.py helper.

The assembler preserves full input/copy/final hashes, exact bounded censuses,
fresh output, path/case checks, one finite allowance, profile-last commit and
retained failure output. It does not load the new facade, start native checking,
open owner state, migrate a profile or make an acceptance claim. Root alone selects
runtime and performs later integration/outcome adoption. Existing historical
PREVIEW_ASSEMBLY diagnostic names retain their prior meanings.

## Independent control-source check

At the reviewer's request, the transport author source-read the completed
test_offers.py at SHA-256
`cbbc8235f69cb47d52827daf16a47f205c28a0cdd79649997e09a3476cd41bf8`.
No execution was performed. No source blocker was found at that exact revision.

The reviewer corrected a missing Host header in the in-memory HTTP fixture before
execution. The corrected fixture satisfies the real request-line/header contract;
its MemoryWriter supplies the real write/drain/close/wait_closed surface. The
successful handler compares exact canonical reply bytes and checks reservation
release/closure; the smaller service quota refuses before dispatch. These are
in-memory handler controls, not real HTTP or installed-package evidence.

The module overlay installs AO before H/O/API, updates both sys.modules and parent
package attributes, and checks shared identities. The loaded baseline is a mutable
SimpleNamespace, so its selected O/API rebinding is consistent. Source tracing
confirms the cancellation/malformed-reply controls reach the unchanged conservative
fetch settlement. Root still selects any bounded run and adopts actual evidence.
