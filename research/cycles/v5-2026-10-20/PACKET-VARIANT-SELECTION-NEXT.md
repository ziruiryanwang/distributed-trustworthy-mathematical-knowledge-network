# Unknown packet variants: expose the bounded local choices first

2026-10-22, storage_integration_adapter. Source-only decision proposal; no
implementation, test, build, installation change or new runtime is selected.

## Recommended next action

**Permit an explicit `packet_offers(candidate, max_offers=64,
max_bytes=16384)` through the existing packet-offer API and route.** Preserve
the default4, all old1..8 request behavior, exact response grammar, quotas and
mathematical admission. Do not add pagination or relax verifier revocation.

This is the smallest consequential remedy for a real access obstruction:
the current store permits64 packet variants for one module/profile, but its
public offer request can reveal only the SHA-ordered first8. All64 fixed-size
locators fit the already available16KiB reply ceiling. An independent challenge
identified this simpler alternative before any cursor design or code was
selected. The next root decision should select only this bounded metadata
extension after its exact source/pin scope is reviewed.

This resolves **reachability of locally retained packet identities**, not
automatic economical selection, successful certificate verification or recovery
after a failed mathematical attempt. Those are distinct obligations.

## Exact source basis

Read current129 map
`experiments/v5-local-checks/distribution-managed-storage-01-input.json`, SHA256
`a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`, together with
the six frozen replacements selected by `EXACT-PACKET-IMPLEMENTATION-SELECTION`.
This is an explicit source composition, not an assumption that the newest
directory is installed. Root owns actual build/adoption and any later map.
Relevant files were read and rehashed:

| Logical source / SHA prefix | Actual source under `software/v5/` and behavior |
|---|---|
| delta/custody4304e529 | `delta/custody.py`: LIMITS20 permits64 offers/module; `offer_request`46..49 permits only1..8; `put`153..165 enforces per-module/profile cap and inserts immutable records. |
| delta/transport18c1abda | `delta/transport.py`: old `/v5/modules/delta-offer`,16KiB route ceiling; request validated in exchange/dispatch/server, explicit max_bytes reserved. |
| evidence_network/custody4264841e | `managed_storage/evidence_network/custody.py`: `offer`129..141 performs SHA-ordered LIMIT query; `verify_offer`51..73 binds module/profile/form, sorted unique exact digest+size rows and byte/count caps. |
| evidence_network/transport b3403208 | `exact_packet/evidence_network/transport.py`: `offers`69..78 records actual returned locators in `_offers`; `packet_exact` bypasses only the offer prerequisite for already-known exact SHA+size. |
| client/workspace_atomic32e3b95e | `continuing_context/client/workspace_atomic.py`: `packet_offers`587..590 forwards explicit caps; decorators94..120 fail-stop escaped action exceptions. |
| client/workspace_evidence3f39d9b5 | `exact_packet/client/workspace_evidence.py`: direct/local/staged admission reaches actual selected owners; exact-J binding remains mandatory433..468. |
| client/workspace_staged5d96c8cb | `exact_packet/client/workspace_staged.py`: one selected packet/module170..171; consumed stage before admission261..286; failure clears staged tokens288..290. |
| client/semantic_reader253b0ffb | `exact_packet/client/semantic_reader.py`: `_call`71..89 makes helper FAILED on escaped error; `_stage`206..263 rejects changed variant; `finish`516..572 calls actual staged admission/import. |
| client/workspace_mixed eb4e9374 | `client/workspace_mixed.py`: `_fail`245..259 clears warrants/caches/candidates, closes budget and transferred owners. |
| admission/verifier32289cac | `origin_phase/admission/verifier.py`: I receive165..233 retains reservations; ordinary receive failure itself only clears busy, while public-client failure still closes this owner. |
| aggregate_claims/aggregate_admission2ef830f8 | `trust_withdrawal/aggregate_claims/aggregate_admission.py`: failed entered receive revokes owner248..249. |
| mixed_claims/receiver54365699 | `incremental_native/mixed_claims/receiver.py`: failed entered receive revokes owner364..370. |

## What currently fails, and what already works

Let one honest provider retain nine structurally admissible variants for module
M/profile P, with distinct ordered packet digests d1<...<d9. Suppose only d9
meets a recipient's proof-form, resource or validity needs. The store's type
inspection is not certificate verification, and neither validity nor economical
reuse is ordered by packet SHA. This is a permitted obstruction, not an observed
nine-certificate experiment or a claim to have constructed that workload.

Every supported offer request from that provider returns a prefix of d1..d8.
Repeating it, raising4 to8, or retiring/reopening a query does not reveal d9 in
this unchanged store. `packet_exact` cannot discover an unknown SHA+size. An
external exact reference or another provider may help, but neither is guaranteed
by this local provider's willingness and possession. Thus this is stronger than
the unavoidable global-coverage limitation: an honest reachable holder itself
lacks a public request for its later locally stored choices.

Existing ordinary APIs already allow the caller to inspect the returned sizes,
choose any returned entry, or query another authorized candidate/provider before
staging. There is no need for an automatic first-entry selector. Offers reveal
digest+size, not per-entry proof form, exact journal, validity or checking cost.
Their common profile names the allowed family, not a validity assertion for an
individual packet. Size is useful but does not determine all downstream costs.

After staging, the reader exposes untrusted exact journal and member inventory,
but there is no public replace/drop transition for that module. Changing its
packet in the same reader fails; closing/recreating the reader does not clear
the client's retained stage. `select_member` selects within a staged packet,
not a different packet. Preview is structural, not speculative verification.

After an escaped acquire/stage/admit error the public action fails closed.
No current ordinary API can continue the same client/grant with another packet
after a rejected mathematical attempt. In particular, new query generations
cannot revive a failed client or revoked A/mixed owner. The separate search,
body and declaration resilience paths settle specific precommit read failures;
they do not apply to packet custody, certificate rejection or admission.

Do not conflate these two facts: **later-identity access is missing, and
certificate-failure recovery is also missing.** Fixing the first does not justify
catching arbitrary verifier errors or treating uncertain cleanup as recoverable.

## Bounded honest-case argument; why no cursor is needed

Assume the existing trusted-owner store invariant: one live store generation has
at most M=64 immutable offer rows for each `(module, profile)`. The provider is
honest, the selected contact remains usable and the original budget can pay the
request. With `max_offers=64`, the existing single ordered SELECT returns every
row in that key's view at the statement's read point. No offset, exclusion list,
new snapshot state or whole-corpus enumeration is required.

SQLite's statement read view gives the relevant concurrency boundary: an
insertion visible to that read is included; one committed after the view is
established need not be. Since output is one statement, there is no inter-page
cursor race, skipped initial row or insertion-driven traversal. A later read may
discover later changes, still under the same original finite resource envelope.
Neither the module/profile pair nor the response authenticates a store
generation or promises a stable distributed snapshot. Existing formal-index
snapshots and their coverage semantics stay unchanged.

This is a conditional local progress statement, not a protocol proof that a
malicious provider returned everything. Keep `global_complete=False`,
`mathematical_acceptance=False` and unverified-locator assurance. Do not introduce
a trusted `complete` flag. A malicious/omitting/offline provider, a replaced store,
expired permission or insufficient budget can still prevent useful discovery.

Each compact locator has only one64-hex digest and one positive size bounded by
33554432. Its JSON representation is at most108 bytes; allowing a separator per
entry bounds64 entries by6976 bytes. The validated fixed response envelope is
less than1024 bytes. Therefore the complete existing response is below8192 bytes,
well within the explicit16384-byte ceiling. The old default4096-byte ceiling
must NOT silently be assumed sufficient for64 entries.

Under ordinary B-tree assumptions, the `(module,profile,digest)` primary key
permits a range seek plus at most64 packet-size lookups and fixed-size records;
a conservative bound is O(log total_offers + M log total_packets + reply_bytes).
This does not promise fixed latency, eliminate provider CPU/accounting, or claim
logarithmic mathematical relevance search. No packet blobs or proof ancestry
are transferred by this metadata read. Client `_offers` retains at most64 new
tuples per such request; cumulative memory/calls/HTTP bytes are still bounded by
the original finite grant, not by pretending this higher constant is free.

The exact locator is `(provider, module, wire_profile, SHA, byte_count)` in its
request/context. Returned digest/size remain untrusted until ordinary fetch
checks exact length/SHA, typed module/profile custody and actual mathematical
admission. A hash is not a validity certificate. No altered expected journal,
weaker verifier, fresh grant, contact renewal or cost refund follows this change.

## Compatibility and prospective source scope

The proposed API/route shape and response bytes for the same old request stay
unchanged; only the explicitly permitted count increases. Existing default4 and
1..8 callers remain bounded exactly as before. A new request above8 may be
unsupported by an old provider and fail the current operation. This is not
automatic backwards-compatible negotiation or a reason to probe old peers and
silently retry. Document the opt-in as requiring the upgraded provider capability;
do not infer a capability from profile equality alone.

The current choke point is shared `delta.custody.offer_request`, imported by
evidence custody and used by shared delta HTTP validation. Widening it affects
the bounded offer grammar for all users of that shared helper, not just the
evidence facade. Root must review that intended common-scope change against the
then-exact installed map and all source pins before selecting implementation.
No store schema migration or quota increase is justified: the maximum already
is64, old snapshots are not rewritten, and the old proof profile remains exact.
Only fresh successor source/pins/documentation may change; used cuts stay frozen.

A focused future control can use a populated structural store with more than8
exact identities: old-prefix behavior unchanged; explicit64 returns every entry
in that local read view; chosen late identity uses the already-qualified exact
or offered acquisition path. Check65, insufficient max_bytes, malformed digest,
wrong profile, reply/count budget and old-request compatibility. No proof
generation, repeated actual-I import or broad networking campaign is needed
to decide this metadata boundary. No execution is authorized by this note.

## Deduplication and deferred boundary

- `EXACT-PACKET-ACQUISITION-DECISION.md` and its six frozen successors already
  solve known SHA+size acquisition and exact placement. Do not redo them.
- `SEMANTIC-READER-SELECTION.md`, `SEMANTIC-READER-REVIEW.md` and the current
  staged/reader source intentionally make variants explicit and admission
  one-shot. Widened offers do not change that contract.
- `ACQUISITION-FAILURE-DECISION.md`, body/declaration resilience and current
  validated search already address narrowly settled metadata/data refusals.
  They are not a missing implementation of certificate retry.
- The complete-custody export/cutover contract concerns a different inventory:
  this proposal reads one chosen module/profile's bounded locator set only.

A later source decision may need reversible pre-admission variant inspection or
transactional verifier rejection. That decision must distinguish clean invalid
evidence from trust withdrawal, expired grants, corruption, partial durable
effects and uncertain process closure, preserving all charges and prior valid
authority only where justified. It is not selected here. Final v5 remains open.
