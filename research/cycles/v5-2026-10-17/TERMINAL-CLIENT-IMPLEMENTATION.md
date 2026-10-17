# Two-form ordinary client implementation

Author checkpoint, 2026-10-17. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Selection: `TERMINAL-IMPLEMENTATION-SELECTION.md`.

Status: **source implemented and statically inspected; NOT RUN by this author**.
No imports, syntax compilation, tests, native calls, builds, proofs, network
services or Git changes were performed. Root owns exact selection/execution;
independent reviewer has read the full product source and reported no blocking
source issue. This is not actual A acceptance or a final v5 release.

## Exact sources

| Canonical-root-relative path | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/client/workspace_evidence.py` | 30,313 | `1bdc7dfb6058c0057eb8fe56daf0f370941d275538b6cb7ab964a455a9646f8e` |
| `software/v5/client/API-EVIDENCE.md` | 10,020 | `5eb88a6da8f38db5756742294b0d2ed5b2bdf88e597a0265d7163b8fe6bfaaac` |

The design in `TERMINAL-CLIENT.md` now reflects the agreed concrete signatures:
`inspect_evidence`, `parse_terminal`, `pack_terminal`, unchanged mixed `Envelope`
plus `terminal_receipt_bytes`. No new EvidenceEnvelope class exists. Final
network source hashes/semantics are recorded by its own author in
`TERMINAL-NETWORK-IMPLEMENTATION.md`.

Frozen parent `workspace_mixed.py` (31,054 B,
`eb4e9374707b3e3f03b7e60ad91fd0fd30a3872d3e9fb59fe3f93c039338acbd`)
and all old test/control/source/evidence remain unchanged.

## Implemented behavior

- New concrete workspace/config and exact two-form PacketStore. Same existing
  module and index stores, ledger schema mechanics and finite grants. No old
  workspace migration, second query mode or proxy/fake store.
- Actual A-required/I-optional mixed owner pairing, pristine counters, deadlines,
  suballocations, foundation and origin checks are retained from the predecessor.
  New store/type/profile and five extra source pins are explicit.
- One structural-only EvidenceAcquisition, one original prospective handoff and
  budget. Actual mathematical admission remains exclusively in the client.
- Local/remote typed admission checks optional expected exact J before actual
  verification and after live promotion. Same ModuleID with another J refuses.
- Terminal uses the actual direct A core unwrapped inside one outer action;
  mixed uses the retained private mixed admission core. No nested decorated
  public action, double verification reservation or zero-delta mixed fallback.
- The existing packet cache also acts as a same-live evidence acquisition
  locator. It can avoid exact duplicate packet download. Terminal still runs
  direct A selection on every submission, reusing only the exact existing live
  receipt binding and charging/revalidating membership. No new cache exists.
- Actual group opening uses A member versus mixed issuer according to returned
  warrant kind. Custody and live exact J are revalidated before return.
- Same-provider exact-name declaration/body wrappers use existing routes and
  the original budget. Result provenance distinguishes exact-name demand from
  an index result. Both remain structural, never mathematical authority.
- `export_evidence` returns exact mixed bytes or reconstructs canonical terminal
  bytes from an actual live A-member fact plus bound receipt. No separate
  envelope mapping or recovered persistent authority.
- `retain_semantics` stores and reads back complete group/body records under
  existing permissions and caps. Publication requires selected terminal groups
  already retained before intent. Mixed publication remains inherited.
- Terminal publication preserves exact target module/export identities, records
  the existing bounded intent/outcome and reads selected semantics. A bounded
  store-accounted primary-key presence query distinguishes absent body from
  corrupt present body: absent is counted, corrupt refuses. No broad scan.
- Existing reconciliation reloads exact raw evidence and derives selected
  terminal groups from immutable custody. It never pretends detached caller
  semantic arrays survived a partial publication.

## Inheritance and changed lexical boundaries

Workspace overrides `open`, `operation`, `status`. Existing grant reservation,
active/config checks, record/history, read-record and release/close are inherited.
The explicit open method copies only the predecessor's concrete storage creation
boundary, selecting the new schema/profile/store and receipt cap.

Client overrides constructor and `_active` for exact concrete bindings, plus:

```text
admit_local
resolve
resolve_declaration
acquire_body
acquire
export_evidence
retain_semantics
_publish
report
```

New private helpers are `_inspect`, `_expected`, `_admit_evidence`, `_body_present`.
Original-owner `_fail`/close, all direct I/A admission, live fact/warrant binding,
candidate descriptions, prospective routing/search, packet offers, atomic
context import/extension, source authoring, mixed semantic material and
publication wrapper/reconciliation are inherited. `_publish` delegates mixed
bytes directly to the predecessor implementation and handles terminal bytes
explicitly. `_admit_evidence` delegates mixed admission to the unchanged private
mixed core and terminal admission to `admit_aggregate_member.__wrapped__`.

No neutral method is reimplemented simply to produce a second complete facade.
The lexical type-bound constructor/open logic cannot call the predecessor with
the new store because its exact old-store gates deliberately refuse subclasses.
Those checks are specialized explicitly rather than monkeypatched or bypassed.

## Exact runtime origin and lifetime obligations

The client requires the predecessor's six origin files plus its five new files:

```text
client/__init__.py
client/workspace_atomic.py
client/workspace_mixed.py
client/workspace_evidence.py
mixed_network/__init__.py
mixed_network/custody.py
mixed_network/transport.py
evidence_network/__init__.py
evidence_network/packet.py
evidence_network/custody.py
evidence_network/transport.py
```

Owner constructors still require their larger independent pin closure. Client
origin checks do not replace it. New active checks bind store identities/profile,
the imported parser/store/acquisition symbols, original budget and structural
acquisition's lack of verifier. Construction initializes all these fields before
the final `_active` call; there is no accepted partially initialized mode.

The client adds no new live issuer/resource owner. Parent cleanup still closes
the original transferred I/A/delta/preparation/session owners and acquisition,
clears all caches/tokens and preserves cleanup uncertainty. A new acquisition
closes only structural resources and cannot close an injected verifier object.
Saved evidence and publication records are untrusted data on reopening.

## Control/API alignment reviewed statically

Root's current ten controls use the existing fixture helper only, not its old
test suite. Their new configuration, five extra pins, direct/local/remote API
calls, `retain_semantics` full-body shape, partial publication and re-open calls
match this implementation by source inspection. Actual provider dispatch plus
inert HTTP/search and fabricated issuers remain explicitly synthetic. No result
is inferred before their separate exact selection and execution.

The eventual actual A workflow must still qualify receipt verification,
semantic import, substantive authoring and onward mixed reuse using this final
target-preserving route. Its fixed-target full-cost comparison must include
producer/certification and service costs; zero native target-delta count alone
does not prove positive growth benefit or complete worldwide deployment.
