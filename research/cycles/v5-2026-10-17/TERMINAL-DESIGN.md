# Same-target certified evidence: concrete dissemination contract

2026-10-17, `memo_tests_review`. Sole canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Guard passed; AGENTS, TERMINAL-SELECTION and prior PUBLIC-A-CLIENT-RESULTS read.
The initial assignment wrote only this design checkpoint. Root subsequently
selected the four new source files in TERMINAL-IMPLEMENTATION-SELECTION.md;
see TERMINAL-NETWORK-IMPLEMENTATION.md for their source-ready pins. No import,
test, native call, build, proof, service, Git or prior evidence was changed.

Status: **selected source implementation, pending independent review/runtime
selection; not runtime-qualified**. The full v5 goal remains open.
This contract supplies wire/custody/acquisition details; TERMINAL-CLIENT owns
ordinary-client integration and TERMINAL-REVIEW the independent challenge.

## 1. Decision: a closed two-form evidence profile

Root's final decision is one new concrete profile and one packet store accepting
exactly two already understood forms:

1. The unchanged `DMKN_MIXED_DELTA_PACKET_V1` raw bytes. Their existing parser,
   native checker and target-last-delta semantics stay unchanged.
2. A new `DMKN_CERTIFIED_TERMINAL_MEMBER_V1` envelope containing one A receipt,
   its exact header H and one exact member opening J/index/ordered path.

There is no generic proof-plugin registry or untyped fallback. Incoming schema
selects one of those two bounded structural parsers; only actual locally adopted
issuers later grant authority. Unknown schema, unsupported profile or malformed
evidence refuses. Neither form can weaken the other's parser.

The alternative separate terminal store/provider is workable but not selected.
`DeltaAcquisition.from_search` consumes one handoff once. Requiring a separate
evidence-mode endpoint or acquisition could require another query/operation just
to choose another representation of the same unknown-ID result. The closed union
requires a narrow fresh store/profile and client constructor specialization,
but retains one discovery session, original contacts and shared finite budget.
It does not introduce a second routing/service architecture.

Old I-only and mixed workspaces, packet databases and used sources remain frozen.
The new workspace/store is fresh; no silent migration or relabeling is proposed.

## 2. Preserve semantic identity and the exact selected warrant

Let a target have module summary S, ModuleID M and exact184-byte journal J:

`M = C.summary_id(S)` and `B.member_journal(J).summary = S`.

The mixed representation computes its requested terminal J from the existing
last witness's summary/rank under fixed I, using `expected_journal(S,rank,I)`.
That computation is structural, not a proof. Actual mixed admission must return
the same J. The certified representation carries J verbatim and binds it as a
member of H; actual A verification must warrant H under the locally adopted A.

**The growth comparison requires both M and exact J equality before/after
certification.** Equal ModuleID alone is insufficient: different rank-bearing
J can describe the same mathematical interface. The seal is not allowed to
replace the target with a wrapper theorem, choose a fresh rank or change exports.

The formal index is unchanged: `ExportID = C.export_id(M, relative_name)` and
the same authenticated group opening creates the same export object, descriptor,
features and index record. Evidence digest is a separate identity. Multiple
different I/A/mixed evidence objects may support one semantic target; neither
evidence count nor receipt count measures knowledge growth.

Unknown-ID discovery initially selects M/interface, not J. Admission must expose
the actual warranted J. Add optional `expected_exact_journal` to the ordinary
acquire/local-admission boundary: if present it is exactly184bytes, matches the
structurally parsed target before verifier work, and matches the live issuer fact
before return. Without it, the caller deliberately learns the selected J and
must use that actual J for later imports. A request for one known J never silently
accepts another J with the same M. The fixed-target evaluation always supplies it.

## 3. Exact terminal envelope

Canonical UTF-8 JSON has exactly these fields:

```text
{
  "schema": "DMKN_CERTIFIED_TERMINAL_MEMBER_V1",
  "header": [192 byte integers],
  "journal": [184 byte integers],
  "member_index": unsigned integer,
  "siblings": [[32 byte integers], ...],
  "receipt_hex": "nonempty lowercase even-length hexadecimal"
}
```

Do not repeat a caller-provided ModuleID, summary, image, proof-success flag or
semantic body list in this envelope. Derive M/S from J; derive A/I/F/P constraints
from the locally selected profile and actual header binding. This removes
redundant fields which otherwise need consistency rules.

For the initial concrete profile:

- Common raw packet cap is the configured mixed envelope's `packet_bytes`,
  at most the existing32MiB transport/CAS ceiling.
- Terminal decoded receipt cap is separately explicit, at most8MiB; default8MiB.
  Hex overhead counts against the raw packet cap. This is a supported-envelope
  bound, not a claim that all possible succinct receipts fit it.
- H is192bytes, J184bytes; each integer is an exact built-in integer0..255,
  never Boolean. Index is an exact nonnegative integer below actual member count.
- Ordered sibling count must be exactly the depth required by H, no more than
  existing `B.MAX_SIBLINGS=6`. H permits at most48 members under current A relation.
- `B.bind_member(H,J,index,siblings,adopted_image=A)` checks existing header magic,
  version, I/F/P, exact path, odd-padding rule, rank bound and member commitment.
  The relation identifiers and header layout are unchanged.
- The selected member rank must also fit the configured shared envelope's
  `rank` ceiling; choosing terminal evidence cannot bypass a lowered local cap.
- Reject extra/missing fields, duplicate JSON keys, floats, noncanonical JSON,
  uppercase/odd/invalid receipt hex, oversize raw/decoded receipt, wrong A/I/F/P,
  malformed J and invalid paths before expensive proof verification.

Use the existing `C.parse_json`/`C.canonical` with an explicit common byte limit;
require `C.canonical(value, limits) == raw`. Important: `C.parse_json` does not
automatically perform a recursive node/depth census from `C.Limits`. Do not
claim it does. The raw byte cap and actual process memory/controller limits
bound decoding; the fixed exact terminal field shapes bound subsequent traversal.
Reject malformed containers before iterating beyond fixed header/path limits.
The unchanged mixed parser retains its own full census.

A minimal private API in new `evidence_network/packet.py` is:

```python
parse_terminal(raw, envelope, *, aggregate_image, terminal_receipt_bytes=8*MIB)
# -> (receipt: bytes, header: bytes, journal: bytes, index: int,
#     siblings: tuple[bytes, ...], member: copied structural journal fields)

inspect_evidence(raw, envelope, *, aggregate_image, terminal_receipt_bytes=8*MIB)
# -> (kind: "mixed" | "terminal", summary: dict, exact_journal: bytes,
#     census: JSON-safe structural accounting)

pack_terminal(header, journal, index, siblings, receipt, *, aggregate_image,
              envelope, terminal_receipt_bytes=8*MIB)
# -> canonical bytes, checked again by parse_terminal, never proof authority
```

Here `envelope` is exactly the existing `mixed_claims.packet.Envelope`, not a
new envelope class. New workspace config/store explicitly records
`terminal_receipt_bytes`. Exact store signature is
`PacketStore(root, profile, limits, *, envelope=None,
terminal_receipt_bytes=8*MIB, create=False)`. `pack_terminal` accepts exact bytes
and a list/tuple of byte-string siblings; it serializes then revalidates the
same terminal grammar. The public profile constructor remains `public_profile(A)`.

`inspect_evidence` bounds raw bytes before decoding for exact schema dispatch.
For mixed, call the unmodified `mixed_claims.packet.parse_packet`; derive exact J
from its last summary/rank using `delta_claims.claims.expected_journal` and fixed I.
For terminal, call the parser above. No branch invokes a verifier, reconstructs
an opaque handle, supplies an artificial witness or turns a receipt into an I.
Repeated bounded structural decoding is real controller work, not counted free.

Census explicitly includes `evidence_kind`, `packet_bytes`, `receipt_bytes`,
`claims`, `deltas` and selected-member/path counts. Terminal has one claim,
zero deltas and one selected member. Those fields describe structure only;
**zero deltas must never be passed to the old mixed parser or receiver**.
The exact J return is separate bytes, not a JSON-incompatible census field.

## 4. Profile and exact-byte custody

New `evidence_network/custody.py` defines a concrete profile with at least:

```text
schema: DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V1
proof_form: mixed-or-certified-terminal-v1
mixed_packet_schema: DMKN_MIXED_DELTA_PACKET_V1
terminal_packet_schema: DMKN_CERTIFIED_TERMINAL_MEMBER_V1
relation_schema: DMKN_CERTIFIED_MODULES_V2
journal_profile: 2
relation_image: fixed I
aggregate_image: explicitly locally adopted A
foundation/policy: fixed F/P
aggregate_header_magic/version/bytes: unchanged v2/192-byte profile
receipt_kind/receipt_encoding: unchanged succinct Poseidon2 values
```

`public_profile(A)` constructs exactly this record. `profile_id(profile)` checks
all fields against that constructor and hashes a new domain, for example
`module-evidence-wire-profile`. It must not reuse the mixed profile ID domain
while changing accepted schemas. A is nonzero and distinct from I through the
existing adoption helper. No algorithm/image negotiation follows peer input.

The new exact `PacketStore` subclasses `delta.custody.PacketStore` only for its
byte/quota/transaction mechanics. Override:

- `__init__`: exact new profile, configured old mixed envelope plus finite
  terminal receipt cap, new database/config schema and file name; same SQLite
  durability/quotas. Preserve the common32MiB packet limit and existing `LIMITS`.
- `inspect(M,raw)`: call `inspect_evidence`, require target summary ID equals M;
  return the target summary and typed structural census.
- `offer`: same bounded digest/length entries and sorting, new offer schema,
  profile and explicit `UNVERIFIED_EVIDENCE_LOCATORS_ONLY` assurance.

Reuse inherited `put/get/status/close`. Its `put` dynamically calls the new
inspector and atomically commits exact blob plus per-M/profile locator. `get`
checks actual size/hash. No signature/acceptance status is stored as authority.
Both proof forms share the same packet/offer/logical-byte/database quotas.
One immutable raw blob has one target M. Quota limits can refuse more variants;
there is no promise to store every proof of the same theorem.

Keep the existing offer-entry ABI exactly:
`{"packet_sha256": digest, "packet_bytes": count}`. A form label is not needed
to acquire or verify an object. Actual schema is learned from the bounded blob;
the top-level offer's proof form identifies the closed two-form profile. Avoid
extra advisory fields that force changes to the shared HTTP request validators.
If future ranking needs cheaply identifying forms, it is a separate measurable
extension, not an authority-bearing field in this first seam.

No receipt-only content-addressed side store or erasure coding is selected.
Different member envelopes can repeat the same aggregate receipt. That bounded
storage/bandwidth cost must be charged; representation deduplication may be a
later improvement if it changes the full-cost decision.

## 5. Reuse transport and one consumed search handoff

New `evidence_network/transport.py` reuses the exact existing routes:

```text
/v5/modules/delta-offer
/v5/modules/delta-packet
```

Their historical spelling does not grant native-delta authority. Requests remain
profile-addressed offers and exact digest/size blob reads. The new wire profile
prevents silently accepting a new proof form at an old mixed endpoint. Both
forms can be offered by the same new provider endpoint/index/custody service.

`CompositeProvider` subclasses `delta.transport.CompositeProvider`, overriding
only construction to require exact new `PacketStore` plus exact `ModuleStore`,
compatible index namespace and profile. Initialize the existing H.Provider as
the mixed provider already does. Inherited dispatch calls `self.packets` and
shared lexical offer/blob request validators; those schemas/maxima remain valid.
Inherited framing/routes, request/reply quotas, TLS/endpoint policy and shutdown
are unchanged. No new remote write or arbitrary referral endpoint is added.

### Structural-only acquisition

Define `EvidenceAcquisition(delta.transport.DeltaAcquisition)` with explicit
new constructor/profile/offer behavior but **no mathematical verifier owner**.
Require `verifier is None`, set both `verifier` and `_origin_verifier` to None,
and override `admit` to refuse with a stable
`PUBLIC_CLIENT_ADMISSION_REQUIRED` diagnostic. Do not inherit the old native
or mixed admission implementation. Only the ordinary client's actual owners
grant I/A/mixed authority, so there is no double verification reservation or
separate aggregate cache to synchronize.

Inherit `from_search`: it calls `cls(...)`, preserves exact actual handoff,
one-time `_issued`, authenticated adopted contact expiries and same budget.
One acquisition can retrieve either schema without another handoff or allowance.
No callback/plugin/factory is accepted for verification.

Inherit `_active`, `_get`, `body` and `custody_ready` where their neutral
contracts apply. Override `close` with the same pending/inflight/budget rules
but never call an issuer, including an object substituted into `verifier` after
construction; this structural object never owned one.
Override `export`/`packet`/`report` assurance text so it says
structural evidence requiring public admission, not an old native-delta result.
Override `offers` to validate the new schema/profile and record only actual
provider/M/digest/size offers. Base `packet` remains exact offered bytes, charges
the shared network budget, invokes new store inspection, commits/readbacks and
creates no mathematical handle.

`custody_ready`'s inherited inspector is dynamic: terminal summary and mixed
summary both must equal the selected export opening's summary. Its demanded
bodies remain exact descriptor-committed hashes. Returned census is explicitly
structural; the client inspects kind and chooses the corresponding issuer path.

### Semantic demands beyond the originally indexed declaration

A certified member authenticates an interface, not all definition bodies that
future computations may need. Do not promise that receipt acquisition alone
is import-ready. The existing atomic materializer remains the arbiter of which
groups/bodies are missing; clients may stop with explicit demands and budget
exhaustion rather than download global proof/semantic ancestry.

The existing `transport.clients.AcquisitionClient.declaration(provider,M,name,
max_bytes)` already fetches a real group opening without an index hint through
`/v5/modules/group`. `_SharedAcquisition` inherits it and charges the same budget.
Add one small `EvidenceAcquisition.declaration` wrapper: active check, real
structural declaration fetch, ModuleStore group put and exact readback, active
check, and structural-only result. This is not a synthetic export record.

The ordinary-client design can expose:

```python
resolve_declaration(existing_candidate, module, relative_name, *, max_bytes)
# -> a new inert Candidate, using only that candidate's existing provider
acquire_body(candidate, digest, *, max_bytes)
# -> exact descriptor-committed body after durable readback
```

These address another declaration in the same complete group or a demanded
known module/name without a global search or new contact. The resulting candidate
is honestly marked demand-resolved, not claimed to have been returned by an index
search. `packet_offers/acquire` still require genuine proof evidence for its
mathematical use. Fetching an external module's semantic opening does not accept
that module's mathematics. Provider does not hold material -> explicit failure;
all future bodies covered remains false. No unbounded closure crawl is selected.

## 6. Ordinary-client admission contract

TERMINAL-CLIENT owns exact new client signatures; these are required wire seams:

1. Preserve one actual A owner, optional I owner, mixed owner, preparation owner
   and existing exact-profile/original-owner lifetime checks. New exact store
   constructor is an explicit successor, not a fake subclass accepted by old
   exact-type checks.
2. `resolve` creates one structural EvidenceAcquisition from the unchanged
   actual handoff/budget. Offers/candidate identity remain advisory.
3. `acquire` verifies the offered blob/hash/M/summary and selected semantic
   custody before admission; `expected_exact_journal`, if given, matches now.
4. Mixed branch uses the actual existing client mixed-admission core and its
   cache/reservation. Terminal branch calls the existing real
   `admit_aggregate_member` core with exact R/H/J/index/path, under one serialized
   action wrapper, not nested decorated actions. Only that core reserves
   verification CPU; acquisition does not also charge it.
5. For terminal, actual `aggregate.open_group(member_handle, opening)` must
   authenticate the selected group against the real live member before return.
   Mixed uses its real delta group-opening method. Recheck exact J and selected
   custody, then genuine live authority immediately before promotion to client
   result. A re-read that lasts past issuer expiry cannot produce a usable token.
6. Cache hits still revalidate issuer/selected semantics and charge submitted
   controller/input work. Receipt caching may avoid a proof verification only
   for the exact same live A/header/receipt binding. Never inject terminal
   facts into the mixed receiver's private cache.
7. Persist only untrusted envelope/group/body/index bytes. New processes must
   acquire or load actual evidence and call their own verifier; no cache/state
   file restores authority. Every fail/close path revokes/clears all new token
   mappings and preserves the tested original-owner/cleanup-uncertainty rules.

The A-member warrant's existing raw bytes are the receipt, not the envelope.
The selected client design avoids an extra envelope cache: `export_evidence`
revalidates the genuine live A-member and passes its actual H/J/index/siblings
and retained exact receipt bytes to `pack_terminal`. This deterministically
reconstructs the canonical terminal form. Never reinterpret envelope bytes as
issuer receipt bytes or store an envelope hash as `receipt_sha256`.

Terminal publication cannot use the mixed-only `_semantic_plan` unchanged.
The selected client design first offers bounded `retain_semantics(openings,bodies)`
which validates, stores and durably reads back material. Terminal publication
then reads selected exported-name groups/bodies from that existing custody,
stores the same M/J envelope, reads it back and indexes the same ExportIDs with
explicit partial-publication/recovery records. Reconciliation therefore does
not depend on detached arrays lost after the original call. Retention can be
partial and is not publication. No dummy native delta is introduced.
Mathematical authority and structural publication remain separate decisions.

## 7. Concrete source map and lexical traps

Suggested new package consists of `evidence_network/__init__.py`, `packet.py`,
`custody.py`, `transport.py`; ordinary-client successor and its docs are separately
owned. This is a closed specialization of retained code, not four new protocols.
Root must choose exact edit paths and source closures before implementation.

| Existing source/site | Reuse or required successor boundary |
|---|---|
| `mixed_claims/packet.py:70` | Preserve unchanged. Mixed branch alone calls it. Terminal zero-delta evidence must not enter it. |
| `aggregate_claims/bindings.py:41,49,117` | Reuse journal/header/member structural binding, exact existing A/I/F/P and member count/path/rank rules. No proof authority. |
| `aggregate_claims/aggregate_admission.py` | Reuse real receive/select_member/open_group and live exact handles through the ordinary client. No new verifier owner. |
| `delta_claims/claims.py:9` | Reuse structural expected-J construction for mixed last target; confirm against actual issuer after admission. |
| `delta/custody.py:79,128,184` | Constructors/inspect/offer have lexical old profile/parser/schema: override. |
| `delta/custody.py:145,175,118,121` | put/get/close/status dynamically use inspector or byte/quota logic: inherit with same blob/offer ABI/maxima. |
| `mixed_network/custody.py:70,109,120` | Existing concrete pattern; do not invoke its initializer or inspector against new profile. |
| `delta/transport.py:87` | Provider constructor exact old PacketStore: override. |
| `delta/transport.py:96,108` | dispatch/_serve use fixed shared request ABI and `self.packets`; inherit unchanged because routes/entries/maxima remain. |
| `delta/transport.py:169,268` | Same exact DeltaLocatedHandoff and from_search: preserve one-shot contact/budget authority; cls constructor must accept verifier=None. |
| `delta/transport.py:242,343,387,415` | Old acquisition constructor, offers, admit and report contain lexical profile/checker/text: override; admit must refuse. |
| `delta/transport.py:293,301,334,367` | _active/_get/body/custody_ready are neutral with verifier=None; preserve original budget and actual storage readback. |
| `delta/transport.py:422` | close otherwise calls current self.verifier; explicitly override to close only structural budget, never an unowned substituted object. |
| `delta/transport.py:319,353` | export/packet algorithms are reusable; override inherited assurance/next-gate text explicitly. |
| `transport/clients.py:135,147` | Existing real declaration/body routes; expose a bounded commit/readback declaration wrapper, no made-up index record or new protocol. |
| `transport/receipt_client.py:32,68,107` | Same AcquisitionBudget and _SharedAcquisition. Verification reservation occurs in public owner core only. |
| `client/workspace_mixed.py:54,112,131,361` | open/operation/init/resolve contain exact mixed schema/PacketStore/CommonsClient/acquisition globals: explicit fresh overrides; changing imports alone is insufficient. |
| `client/workspace_atomic.py` acquire/semantic_material/_publish | acquire assumes mixed handle and acquisition.admit; terminal must dispatch and open real A member. Semantic plan/publication assume witness groups and need separately supplied terminal material. |
| `client/workspace_mixed.py` _active/_fail/report/close | Preserve exact original-owner checks, source pin/origin binding, sticky cleanup uncertainty; extend only new evidence-cache/report needs. |

Fresh runtime selections must include all retained bases plus new package/client
files and actual imports. Exact hash identity is not semantic/certificate
acceptance. Do not loosen existing import-origin guards or mutate frozen package
globals to make subclass construction succeed.

## 8. Conditional assurance and scale argument

For a terminal return, the obligations are:

```text
offered exact bytes -> bounded canonical terminal envelope -> bound (H,J,path)
real local Verify_A(R,H) -> real live Member_A(H,J,path)
live Member_A + exact selected group/body custody -> client-local warranted J
```

The first line alone is never mathematical authority. Cryptographic acceptance
still depends on the adopted A checker/relation and proof-system assumptions.
Semantic bodies are independently content-bound, not guaranteed available merely
because H/J verify. Storage/search are not validity or completeness authorities.

The mandatory terminal acquisition/checking cost depends on the selected receipt,
fixed header/journal, membership path, selected semantic material, bounded search
and service costs. It does not require the old target's native witness or every
ancestral proof step. The per-object aggregate member cap48 is a current relation
limit, not a claim that the whole global library fits one header. No assumption
of universal search completeness, permanent availability or inevitable useful
growth is introduced.

For a fixed target J, certified receiving may save the native target-delta work
against the same optimized local alternative. That saving is not automatic:
the terminal envelope's receipt, encoding, controller, search, body/custody and
verification costs remain. Warm baseline receipt/handle caches must be matched;
count independently warranted cold/new-owner admissions where appropriate, not
every repeated theorem use. A positive `N*d > S+M` region needs actual or justified
bounds for the new public route and full creation/certification/maintenance costs.
This design makes that same-target route implementable; it does not set d>0.

## 9. Distinguishing gates and stop condition

Reuse the16 passed public-A controls and unchanged I/mixed/atomic evidence.
New tests should address only changed dispatch, target, custody and public seams:

- Structurally valid terminal envelope retained without accepting mathematics;
  all malformed/noncanonical/wrong-profile/path/size cases refuse boundedly.
- One new store/provider offers both exact forms for the same M without changing
  index identity. Existing mixed bytes are byte-identical, not re-encoded.
- Known exact J request refuses another J with the same M; same M/J survives
  mixed-to-terminal replacement. No witness/wrapper/native call in terminal branch.
- Shared budget and original contact handoff survive choosing either form;
  acquisition.admit cannot issue authority or double-charge verifier work.
- Wrong semantic group/body, unavailable demanded body and post-custody issuer
  expiry refuse; direct declaration demands remain structural until verified.
- Genuine actual A verification/member selection, followed by semantic import,
  ordinary extension, publication and fresh independent-owner acquisition.
  Combine this with the already pending genuine-A integration, not a duplicate
  intermediate fixture campaign. Synthetic controls are labelled synthetic.
- Original-owner closure, cross-client token rejection, no reopened-state
  authority and sticky cleanup uncertainty remain intact under the new mapping.

Stop this design lane when source scope, exact wire/profile/identity, real issuer
path, demanded semantics and shared-budget integration are independently clear.
Root then selects disjoint source work and narrowly changed controls. No design
statement itself authorizes an execution or declares full v5 delivered.
