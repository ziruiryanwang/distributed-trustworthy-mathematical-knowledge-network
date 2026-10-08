# Minimal receipt custody and acquisition seam

Root selected source implementation at D18; source and controls remain unrun
and await independent review and a separate exact finite runtime selection.
All used transport, custody, admission, location, source and evidence stay
unchanged. The immediate target is discovery -> authenticated group -> exact
receipt bytes -> actual local admission -> retained independent custody. It
does not replace the existing proof relation, index, DHT or group/body protocol.

## Existing guarantees and the actual gap

`AcquisitionClient.export` already authenticates a returned group opening,
resolves the exact export locator and recomputes its formal feature record.
`ModuleStore` retains structurally authenticated groups and demanded committed
definition/rule bodies. Neither grants mathematical validity. `ReceiptVerifier`
already launches an independently adopted verifier, checks same-call exact
receipt/journal/module bindings and issues private revocable live handles.
Neither the current HTTP transport nor ModuleStore stores/transfers receipt
bytes or locates a receipt when only ModuleID is known.

The current transport fixes `ROUTES`, JSON Content-Type and JSON acquisition
parsing. A receipt is the host's exact bounded bincode Receipt encoding, not
canonical JSON. Do not base64 it into the object schema, parse it as JSON,
register routes by mutating frozen globals, or import a remote verifier path.

## Three identities, with no global canonical proof

1. **ModuleID** remains `codec.summary_id(summary)`. It identifies the committed
   mathematical interface, independent of which compatible proof certifies it.
2. **ReceiptSHA256** is lowercase hexadecimal SHA-256 of the exact raw receipt
   bytes, matching the existing verifier's `receipt_sha256`. It authenticates
   bytes only; arbitrary junk also has a digest. Same digest requires same
   bytes under the collision-resistance assumption.
3. **WireProfileID** describes public compatibility. Define it by
   `codec.hash_value("receipt-wire-profile", public_profile)` with exact fields:

   ```json
   {
     "schema": "DMKN_V5_RECEIPT_WIRE_PROFILE_V1",
     "encoding": {
       "codec": "bincode",
       "integer_encoding": "fixed-width",
       "endianness": "little",
       "trailing_bytes": "reject",
       "max_bytes": 67108864,
       "receipt_type": "risc0_zkvm::Receipt",
       "retained_risc0_zkvm_rlib_sha256": "5c5bff2476163fe1fcb6453f9b7d5aa84e1887b349a939ae5fffddd90ee5c434",
       "retained_serde_rlib_sha256": "c2bdec00d6bc0942b77e31495ca7d3aec7df7370e42cf65335b232ff35e32044",
       "retained_bincode_rlib_sha256": "c9dc6a56e36315e813f1f02aeb8a67edd1c5fdc287347fb7810f94c9e310ddfa",
       "retained_dependency_manifest_sha256": "ced49032a348d1784cee327d5a3368e8f942335210854e403053d289b06b5e0a",
       "verifier_context": "RETAINED_SDK_DEFAULT_WITH_DEV_MODE_FALSE_FULL_APPLICATION_NO_ASSUMPTIONS"
     },
     "receipt_kind": "succinct-poseidon2",
     "journal_profile": 2,
     "image": "<locally adopted 64-lowercase-hex image>",
     "foundation": "<locally adopted foundation>",
     "policy": "<locally adopted semantic policy>"
   }
   ```

`encoding` is exactly the object above. Its mandatory parameters are bincode,
fixed-width integers, little endian, rejection of trailing
bytes, 67,108,864 maximum bytes and the exact `risc0_zkvm::Receipt` serde type of
the selected implementation. The current host uses `DefaultOptions::new()` plus
`with_fixint_encoding`, `with_limit(64*1024*1024)` and `reject_trailing_bytes`.
Its default endian is little. The verification context is retained SDK default,
dev mode false, full application verification with no unresolved assumptions.

The profile also pins the three retained risc0-zkvm, serde and bincode **compiled
rlib artifacts** and retained dependency-manifest provenance, as explicitly
named in `ENCODING`. Their exact bytes and names come from
`experiments/certified-collection-01/host-build-01/LINK-INPUTS.json`, reused by
the selected module host. These hashes are not a proof of a portable serialization
ABI and independently rebuilt compatible artifacts need not have equal hashes.
They deliberately limit initial support to this adopted implementation selection;
no machine path appears on the wire. A later independently built implementation
requires explicit schema/verification-parameter conformance and owner adoption,
not an arbitrary cross-SDK decoder fallback. This first selection adds no alternate
receipt decoder. A successor with incompatible encoding needs a new profile.

The public profile is constructed from owner adoption before reading offers.
It MUST NOT be `ReceiptVerifier._profile_id`: that intentionally includes local
runtime paths, executable pins and the supervisor manifest. Two correctly
configured machines may have different local admission IDs but the same wire
profile. Matching a wire profile grants no authority to an endpoint or receipt.
Multiple receipts/proofs/ranks for one ModuleID are permitted; no network-wide
winner, receipt ledger or consensus operation is needed.

## Exact read-only wire additions

Keep the current one-request/connection framing, bounded headers, Content-Length,
EOF/trailing-data refusal, TLS/owner egress and no redirects/compression. Requests
remain canonical JSON. The response media type is selected by the **local route
definition**, never negotiated from untrusted headers.

### Offer route: `/v5/modules/receipt-offer`

Request fields are exactly
`{module_id, wire_profile_id, max_offers, max_bytes}`.
Module/profile digests are strict; `1 <= max_offers <= 8`,
`1024 <= max_bytes <= 16384`. Reserve the whole offer-byte allowance before I/O.

The canonical JSON response has exactly:

```text
{schema:"DMKN_V5_MODULE_RECEIPT_OFFER_V1",
 module_id, wire_profile_id,
 receipts:[{receipt_sha256, receipt_bytes}],
 assurance:"UNVERIFIED_RECEIPT_BYTE_LOCATORS_ONLY",
 global_complete:false, mathematical_acceptance:false}
```

Receipt entries are sorted by digest, distinct, at most max_offers, and have
`1 <= receipt_bytes <= 64 MiB`. Empty means no offered local compatible bytes,
not absence of a valid proof anywhere. The client checks exact expected ModuleID
and its independently selected WireProfileID, but even a matching entry remains
an unverified hint. No profile, URL, file path, credential, executable or script
arrives in this response. The initial query is an indexed bounded lookup, not a
scan of all locally retained receipts. First-k offers are explicitly incomplete;
there is no promise to enumerate all proofs or survive malicious offer ordering.

### Blob route: `/v5/modules/receipt`

Request fields are exactly `{receipt_sha256, receipt_bytes}`. The size is the
owner-selected accepted offer's exact expected length, bounded by the same
64 MiB hard profile ceiling and the remaining owner allowance. Requesting a
smaller cap than a real receipt is a refusal, never a reason to increase it.

The response is exactly the raw receipt, `application/octet-stream`, with exact
Content-Length equal to requested receipt_bytes and no trailing byte. The client
hashes the returned bytes and compares ReceiptSHA256 before receipt custody or
verification. Wrong bytes, size, media type, truncation, duplication of headers,
trailing bytes and unsupported compression refuse. This check is still only
byte authentication. No constructor/decode of untrusted bincode belongs in the
HTTP service or custody path; the supervised adopted verifier owns decoding.

The host's current maximum is 64 MiB; this is a ceiling, not a typical size or a
permission to spend 64 MiB per retry. The first supported implementation may
buffer one bounded receipt under its external memory Job, as the existing
verifier already takes bytes. Streaming/chunk-tree proofs are not necessary to
close this seam. Preserve literal measured byte count plus digest in evidence.

## Minimal durable store

Add a separate owner-created bounded `receipt_store.py` SQLite store; do not
migrate or edit the used ModuleStore database. Its logical schema is:

```text
meta(singleton configuration, receipt_count, offer_count, logical_bytes)
receipts(receipt_sha256 PRIMARY KEY, byte_count, opaque_blob)
offers(module_id, wire_profile_id, receipt_sha256,
       PRIMARY KEY(module_id,wire_profile_id,receipt_sha256),
       FOREIGN KEY(receipt_sha256) REFERENCES receipts)
```

An owner-only put validates exact wire profile/namespace identifiers, receipt
length and digest; it atomically admits bytes, offer row and quota counters.
The initial constructor durably binds one exact owner-selected public profile;
put/offer requests for another profile refuse. A new image/profile uses a fresh
explicitly adopted store or later reviewed migration, not a downloaded switch.
It does not accept remote writes or run a prover/verifier. Limits must include
total receipt count, total offer count, offers per (module,profile), individual
receipt bytes, total logical bytes and SQLite pages. Logical bytes and physical
page caps are separate. Same digest/bytes coalesces; conflicting bytes refuse.
Owner commit deadline is checked before COMMIT. Read-only get checks stored
length and hash again; changing an untrusted DB flag cannot mint a handle.

Rows are **unverified associations**, including if the owner originally inserted
them after a successful local verification. Optionally recording audit evidence
must not turn restart into trusted-cache loading. The first store needs no GC:
quota exhaustion refuses new custody rather than deleting promised bytes. This
is bounded retained custody, not an infinite or independently replicated lease.
Receipt existence and referenced group/body existence are separate facts.

The two databases commit separately; no cross-database atomicity is claimed.
A partial commit leaves retained partial custody, not a successful whole request.
The controller declares selected-component custody only after each selected
group, opaque receipt and explicitly demanded body has committed and passed a
fresh content-authenticating readback. It repeats those checks after real local
verification before returning the live handle. A failure after handle minting
closes that verifier instance, revoking its handles. Cold process reconstruction
from either database yields no handle: the actual receipt verifier must run again.

At successful acquisition, retain the exact receipt and selected group openings
and any demanded computational bodies before claiming supplier-independent
reuse. On cold restart reverify the retained succinct receipt and authenticate
the openings/bodies; no ancestor receipt or theorem-proof history is required.
If unrequested definitions are demanded later, further bounded retrieval or
explicit unavailable status may be necessary. Do not claim every future use is
offline merely because one theorem export was retained.

## Composition and accounting

A new thin owner controller owns one original monotonic deadline D and a finite
resource vector for search, group/body acquisition, receipt offers/blobs and
verification. Assign disjoint fixed suballocations up front, so their sum does
not exceed the owner grant; alternatively share one reservation ledger. Reusing
the existing classes must not instantiate a fresh allowance per hint/failure.
All outputs must arrive and be checked before their phase and original D; no
live handle may escape after D. Original outer process containment bounds total
wall/CPU/memory, including parsing, hashing, SQLite and verification wrappers.

The existing classes do not yet offer one common absolute-deadline public
constructor. The implementation selection must supply that seam explicitly in
the new owner controller/successor, not claim that independent relative phase
timers are already one workflow. Runtime adoption hashing and evidence/custody
I/O count. A late verifier result is refused and its handles revoked; no new
operation can start during teardown. Same owner process is trusted, as in the
current admission API; this is not isolation against malicious local Python.

The implemented `AcquisitionBudget` shares attempts/reply reservations across
group/body and receipt HTTP operations. `DeadlineReceiptVerifier` checks D even
during inherited adoption hashing, then clamps the inherited worker deadline.
Its constructor takes owner configuration only. `charge_external` prepays a
finite earlier search/location suballocation before any local acquisition
dispatch. This is a trusted-owner composition contract: it does not by itself
prove that an external phase observed its grant, so integrated callers must pass
the same D and retain the external phase's actual bounded accounting. Request
and header exposure bounds remain additional counters, not reply-body bytes.
Outer Job accounting still includes all wrapper, SQLite and hash CPU/memory.

Each attempted network request reserves its full allowed reply bytes and one
attempt before dialing. Unknown outcomes keep the full reservation charged;
completed bounded responses may charge measured body bytes. Invalid complete
responses still consume their observed bytes and attempt. Header/request bytes
are separately measured for completed requests and bounded/conservatively
accounted for uncertain ones; TLS/kernel overhead is not renamed payload bytes.
Provider serving counts receipt replies against the **same service-wide** reply
and request caps as other routes. It reserves before reading/loading the blob.

Receipt verification separately charges the current verifier's complete attempt,
receipt length and worker CPU reservation before launch. Failure, wrong image,
wrong module, unresolved assumptions and fake receipts never issue handles or
refund a new attempt. Duplicate offers may be deduplicated for selection, not
erased from accounting. Success JSON, a saved receipt-offer row and an index
record are never inputs that substitute for real verification.

The admission order is:

```text
candidate record
 -> existing export acquisition + exact feature/locator recomputation
 -> opening.summary whose ModuleID equals the candidate's module
 -> owner-profile receipt offer -> exact raw receipt acquisition/custody
 -> ReceiptVerifier.receive(raw, expected_summary, ...)
 -> ReceiptVerifier.open_group(live_handle, exact_opening)
 -> demanded committed bodies / root-owned checked reuse
```

No receipt parsing result alone supplies an expected theorem or profile. The
candidate's claimed ModuleID is untrusted but must be the same ID authenticated
by the opening and finally certified by the locally adopted verifier. The local
agent can then judge usefulness; human intention does not enter acceptance.

## Endpoint and source selection

An index endpoint does not promise custody. The first integrated provider may
explicitly serve index + module + receipt roles at the same owner-approved
endpoint; requesting a missing role simply spends/refuses that attempt. Existing
configured independent custodians remain usable. No automatic remote referral
dial, arbitrary URL, or change to the location descriptor is needed for this
minimal seam. General unknown-custodian routing is a separate remaining service
condition, not a claim supplied by cohosting a small loopback test.

Proposed fresh files, only after root selection:

- `custody/receipt_store.py`: the bounded opaque byte/offer store above.
- `transport/http_provider_receipts.py`: reviewed successor of current provider
  with two static routes and route-selected response media; existing JSON paths
  unchanged. Old SearchClient/AcquisitionClient can talk to those JSON routes.
- `transport/receipt_client.py`: bounded offer/blob acquisition and outer owner
  composition with existing structural acquisition and ReceiptVerifier.
- Focused changed-boundary controls for binary framing/digest/size/quota,
  wrong module/profile, aggregate failure charges and restart/reverification.

Do not rewrite the already passing search/location stack or run old campaigns.
The first actual positive certificate integration awaits a genuine current-image
profile2 receipt plus freshly derived current-policy module exports/index.
Retained old-policy discovery bytes are not relabeled. A later one-time actual
test should acquire, admit and retain the selected current receipt/group, close
the supplier, reopen local custody and freshly verify/reuse. Synthetic receipts
can test byte transport/refusals only; they cannot qualify that positive path.
