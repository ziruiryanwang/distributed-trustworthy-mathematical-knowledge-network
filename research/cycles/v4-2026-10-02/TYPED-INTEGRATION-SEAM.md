# Smallest coherent typed discovery and exchange seam

2026-10-02 UTC. `/root/typed_review`; source-only proposal at the canonical root.
Root prioritizes intrinsic-definition soundness/implementation first. No product
source, installation, profile, database, package or runtime was changed here.

**Decision:** adapt one fresh selected peer/index successor to the actual typed
codec, do not overlay definition codecs into maintained-directory source05.
Root selected DefinitionID-aware diverse representatives, separate exact-type
query keys, a new typed index schema/namespace and no silent state migration.

## Actual incompatibilities inspected

Source05 `cert_index.py` is29040B/SHA
`52ca8e9674c920e1b0420422b81c2ce18067b06cfbc89bee25e116cdaaaa5093`;
`cert_peer.py` is33520B/SHA
`c8f6dd6c987e7ea650eb34b781e07bcbdda920d36a7f895ded59ca4c42ab013b`.
Its PINS select old11723B Prop-only capsule and15032B BundleV2 codecs. Definitions
need the new kind/header/value/semantic-context codec and typed journal/BundleV3.
Current `discovery_features` calls `Graph.header(header)` with its default Prop
kind; a definition header necessarily fails that exact field shape. Its offer
schema omits mathematical member kind and required-definition IDs. Its namespace/
store/discovery contracts predate those typed inputs. Changing pins alone is
therefore not an integration.

The peer's four-file framing uses B's derived payload limits but declares
`DMKN-CERTIFIED-BUNDLE-V2`, bundle-v2 media and old offer contracts. Its acquired
bundle is rebound and redescribed before custody/index commitment; that exact
comparison must include new typed metadata. Routing/store code consumes
`I.validate_offer`, generic key/namespace and opaque bounded offer bytes, rather
than a mathematical verifier. The maintained-directory logic can remain unchanged
if these public bounds/contracts are preserved and a fresh namespace/state is used.

The existing standalone receiver is also incompatible: `cert_verify.verifier_marker`
requires `journal_bytes == 120+32*members`, whereas the typed layout is
`120+sum(40+32*k)`. Its installed profile/codecs/driver image are old. Editing a
policy value cannot turn it into a typed receiver. The new contributor already
has a typed receipt intake/reuse path; that can be the first integrated full-node
path if root does not select a separate small receiver yet.

## Typed index semantics: exact type and diverse identity differ

For registration, bind the actual bundle through the new active B codec, call
`Graph.header(header, capsule.kind)`, and derive all metadata from that bound
snapshot. An offer should add unambiguous `member_kind` and exact sorted
`required_definition_ids` from manifest/binding. Do not confuse mathematical
member kind with Store.offer's existing publication/custody role. Kind metadata
is an advisory discovery facet; it never certifies mathematics.

Derive a new name-erased exact type query fingerprint from namespace/F, explicit
member kind, ordered universe names, actual structural type and committed required
definition IDs. For definition type search exclude the definition's body/own name:
agents should be able to request all definitions of a known type without already
knowing their bodies. The new typed namespace separates these features from old
states/cursors and image-specific proposition certificates.

But diverse representatives must not collapse definitions by that type. Identity,
zero and successor may all have type Nat->Nat while denoting different functions.
Root's selected rule is:

| Mathematical kind | Exact-type query key | Diverse representative identity |
| --- | --- | --- |
| Proposition | New typed committed name-erased type fingerprint | Kind-tagged exact type fingerprint; a syntactic redundancy heuristic only |
| Definition | New typed type fingerprint, excluding body | Kind-tagged exact DefinitionID; never Nat->Nat alone |

Keep `type_key` and `representative_id` separate in the fresh representatives
table. Proposed fields are namespace/key/representative_id/type_key/sequence,
with primary(namespace,key,representative_id) and the existing selected-range
index on namespace/key/sequence. Diverse replies continue returning the actual
type_key; acquisition recomputes and matches it. This preserves unknown-definition
type search while retaining different bodies in broad-key diverse search. Same
exact DefinitionID across receipt/bundle variants may share a first-sequence
representative; no semantic equivalence or novelty oracle is claimed.

Preserve bounded conclusion-spine features and local SQL range pagination. For
definitions, actual type/body constant features can help retrieval, but do not
invent a universal complete mathematical search guarantee. New kind/context
metadata must stay within current offer4096B and per-query budgets. An over-bound
request refuses instead of resetting budget. No human intention is admitted into
mathematical acceptance.

## Proposed leaf boundary after separate root selection

| Fresh successor leaf/artifact | Required change or preserved role |
| --- | --- |
| cert_capsule.py / cert_bundle.py | Copy exact selected typed/intrinsic-compatible codec leaves; no independent parallel codec implementation. |
| cert_index.py | Update exact pins; typed offers/features; separate representative_id/type_key; new store/discovery/enumeration namespace/schema; old state refusal before writable PRAGMA. |
| cert_peer.py | Explicit BundleV3 framing/media declaration, consistent byte limits and actual typed describe/acquire comparison; retain TLS/pinned helper/resource/quarantine/custody behavior. |
| cert_route.py / cert_route_store.py | Prefer byte-identical maintenance/routing logic. They already delegate offer/key/namespace validation; only edit on a demonstrated incompatibility. Fresh routing/directory state binds the new namespace. |
| CERTIFIED-NETWORK-API.md | Explain typed discovery, DefID-aware diversity, advisory ads, intrinsic local data versus receipts, version/refusal/budget limits and exact known-contact/current-view behavior. |
| Contributor native/workflow/stages/docs | Use the separately selected intrinsic-definition successor, not a second authoring branch. Receiptparents and local semanticcaps remain distinct. |
| Fresh installed contributor profile/map | New exact image/driver/codecs/native/workflow pins and matching typed profileID/F; reuse unchanged Lean/Python/support/runtime maps exactly. No old installation in-place overlay. |
| Fresh peer configuration | Explicit identical profileID/imagewords/F/registry and resulting namespace; operator paths/contacts/TLS identities remain private data outside package. |
| Optional cert_verify.py + receiver profile/install | Only if separately selected: actual typed journal parser/marker/schema/image and truthful receipt-only assurance. It cannot claim native Definition installation because its small runtime has no Lean. |
| New pack/install adapters/maps/guide | Fresh exact allowlisted inputs, matching new profiles/policies and relocation gate. Existing v3 pack.py hardcodes old profiles/image/deadline and cannot package v4 unchanged. |

Generic checker/schema/foundation/serializer/support helpers and peer_wire/
peer_service should remain unchanged. Do not add identity/governance/global-task
mechanisms or a new network service merely to perform this binding adaptation.
Existing separate producer/peer commands remain an operable explicit workflow;
automatic publication inside theorem acceptance is unnecessary.

## Intrinsic data and network scope

The current peer transfers four-file certified bundles. A bare intrinsic definition
capsule is not such a bundle; do not forge an empty receipt or silently offer it
under a certificate schema. The smallest v4 path can carry required definitions
inside certified proposition capsules and reuse local canonical data via the
selected --local-definition API. Existing standalone certified Definition bundles
may remain optionally searchable/transferable, but their certification is not
required for local semantic use.

A future one-file unverified semantic-data offer is possible, but would be a new
storage/wire/offer lane needing separate exact bounds/assurance tests. It is not
necessary to close the first typed theorem discovery/acquire/check/reuse/return
loop, and is not selected here. State this limitation honestly: intrinsic raw
capsule-only network publication is not yet implemented by BundleV3 transfer.

## Minimal integrated gates, not repeated old campaigns

Before package adoption, register actual bound typed proposition/definition
bundles under the fresh namespace, verify exact metadata/keys and different-body
same-type DefinitionID diversity. Refuse swapped kind/context, stale namespaces/
stores/cursors, old frames and changed payloads at intended gates. Show that a
selected bounded directory search returns an unknown typed proposition, transfers
only its four files/embedded semantic bodies, then actual installed native+
certificate workflow reuses it and publishes a successor for opposite-node
discovery/acquisition. Suppliers may go offline after custody; no ancestor body/
receipt fetch or root-injected acceptance is permitted.

Unchanged TLS/routing/storage helper evidence need not be wholly rerun, but new
typed boundary behavior and genuine integrated policy coherence need actual
qualification. The existing directory10 PASS is inert maintenance evidence,
not evidence that these new typed bundles interoperate. Account producer/native/
snapshot/proof/search/transfer/check/maintenance/return resources; isolate the
still-failed typed-parser performance claim and preserve v3 fallback. A packaged
file map alone is not global operation, useful growth or a new proof-cost pass.
