# CP-001G: exact profile negotiation and proof-root consumers

Date: 2026-09-20. Status: selected root-owned integration contract, independently reviewed in the [profile audit](../audits/CP-001G-profile-integration-audit.md). No implementation or protocol execution. Frozen F records retain their original schemas and semantics.

## Why an evidence format change reaches other layers

A ProofInstanceID is not a ProofID. Replacing the proof graph while continuing to put the new ID in a field whose grammar requires the old kind produces a noninteroperable specification, even when the eventual native checking rule is sound. This note fixes the boundary between [PI1](CP-001G-proof-instance-composition.md), [STRUCT2](CP-001G-structural-retrieval.md), and existing NET2/organization/custody contracts.

The first selected PI1 profile uses NativeRules code 4 and its exact FoundationID. It accepts InstanceReplay `0x0015/3`, not a rule-3 replay relabeled as new evidence. Native semantic schema-2 descriptors in that closure must themselves name the exact code-4 foundation. The original code-3 objects remain separately readable under their frozen profile or as inert migration inputs.

## Capability and outer envelope

NET2 keeps outer version 2 and ServiceCall `0x8004/2`. Append **8=PI1** to the sorted capability-code namespace. Capability 8 means support for the exact mathematical reader and the explicit code-4 consumer bindings in this note; it does not mean that any advertised remote theorem is trusted, that the peer offers every service, or that a foundation is locally adopted.

Each communicating side must receive the other's matching HELLO_REPLY capability advertisement on the authenticated connection, using reciprocal existing HELLO exchanges. The existing 16-code and message-byte ceilings still apply. PI1 native content service requires the exact advertised FoundationID and capability 8; independent native acceptance additionally requires the receiver's actual local adoption/qualification of that foundation. A FoundationID alone is not evidence of a supported replay codec. A routing-only holder needs the negotiated record/key codecs and local storage authority, but need not adopt the advertised mathematical foundation, import its bootstrap or check an anchor. Routing records remain untrusted metadata.

Capability 7 continues to identify STRUCT2/1. For the first selected code-4 structural service, require 3, 7 and 8 for FIND_WINDOW; routing K4 additionally needs 5; FULL_FEATURE group operations additionally need 6. A peer can understand PI1 without offering structural search or routing storage. No presence of a root hint infers a missing capability.

The mathematical PI1 schema allocation, NativeModule3 and opposing-evidence3 are exactly those in the composition note. The new evidence scope includes WitnessTermDAG `0x0022/1`, ProofInstance `0x0023/1`, RepresentativeMapNode `0x0024/1`, and the actual reached native semantic/foundation/direct-set objects. Old Proof2/witness-map2 objects are not substitute members of that scope.

## Public root descriptor

Select `PublicIndexDescriptor` **`0x8111/3`**, with exact payload:

`[FoundationID,typedRoot,judgmentOption,InstanceReplayID,structuralDescriptorOption]`.

The typed root is `[4,ProofInstanceID]`, `[1,DefinitionID]`, `[2,GroupID]`, or `[3,OpaqueID]`, matching that exact InstanceReplay. An option is `[0]` or `[1,value]`. judgmentOption is present exactly for tag 4 and must equal the instance's exact target; it is absent for nonproof roots. structuralDescriptorOption, when present, contains one StructuralDescriptorID `0x8124/1` bound to that same foundation and anchor replay. A group-root descriptor may thereby point to one selected constructor view; it does not pretend that the constructor is an independent declaration root.

This record has at most 4096 canonical bytes, contains no private checking-assessment/ledger identifiers, and is a public candidate hint, not an acceptance certificate. Several different structural descriptors may share one replay, but a root descriptor commits to just its one optional hint; other views appear as their own bounded STRUCT2 rows. A missing structural hint does not prevent exact judgment lookup.

The structural hint supplies no generic CAS read permission. A STRUCT2 page carries its actual bounded `0x8124/1` descriptor payload inline. A client can compare its derived CID with the hint when both are supplied. Otherwise it obtains descriptors by separately funded public search, or ignores the absent/unavailable hint. Native type/evidence bytes remain in the exact native read scope.

For code-4 exact-judgment FIND/FIND_WINDOW results, return these schema-3 root descriptors. For STRUCT2 mode 6, return StructuralDescriptor records under the explicitly negotiated predicate, ordering by their own exact public descriptor IDs. Snapshot/cursor state binds the result-record schema and mode as well as the existing predicate/extractor/planner/holder fields. A cursor cannot be resumed against a different descriptor universe. Other inherited query modes retain their specified predicates with the explicitly supported code-4 native-ID domain; old schema-bound requests are not silently recast as new ones.

The local private IndexDescriptor and ProofFamilySelection use schema 3 where serialized, retaining their receiver-owned role and replacing proof-evidence pairs by `(ProofInstanceID,InstanceReplayID)`. Counters distinguish new statements, instances and replay contexts rather than combining them into a novelty total. A local reverse edge can name an exact proof instance or semantic alias obligation as a derived relation; it is not a remote theorem-verification verdict.

## Provider advertisements and group maps

Select ProviderAd **`0x8022/2`** for code-4 PI1 advertisements, with payload

`[2,providerNodeID,K,revision,publicContact,anchorPublicDescriptorCID,anchorReplayID]`.

Keep the exact prior signature wrapper, provider identity, positive lease handling, revision comparison, contact shape and 4096-byte total bound. The changed leading value agrees with schema 2. anchorPublicDescriptorCID is `0x8111/3`, anchorReplayID is `0x0015/3`, and both describe the exact same code-4 root/foundation. The signature binds these typed bytes, not mathematical validity.

Inherited K0/K1/K2/K3 route keys keep their frozen shapes and meanings under this explicit new code-4 record. K4 is exactly `[4,FoundationID,ExtractorID,featureToken32]` and additionally requires STRUCT2 capability 7. For K4 the producer's anchor root descriptor must have a structural hint whose actual currently public structural descriptor contains that exact token and binds the same replay/extractor/foundation. The holder validates record/key/schema/signature/authority bounds without fetching any anchor or independently checking a theorem.

New code-4 ads use schema 2 for exact as well as structural keys. Frozen `0x8022/1` remains the code-3 service record; it is never used to carry a new proof-root descriptor, replay or K4 tuple by changing its prose interpretation. A schema-2 provider contact may contain K4 index hints only under the same negotiated capability; it does not add a remotely executable role.

ROUTE1 cells and group membership remain operational data. For code-4 groups, `0x8023/1` retains its exact canonical cell-bearing map grammar, but its admissible key/ad domain is selected by the negotiated record profile and immutable group mode: operation 16 creates FULL_EXACT accepting only K1; operation 20 creates FULL_FEATURE accepting only K4 at its bound ExtractorID. The new leaf carries a schema-2 ad CID and still fits the inherited 2048-byte bound. An old code-3 map is neither reinterpreted nor mutated into a code-4 group. A remote contact cannot force a receiver to use a broader cell/key grammar without the declared capability/profile.

Calls 11–19 retain their envelopes and arguments with these expressly negotiated record domains. Calls 17–19 check the immutable mode/foundation/extractor/owner state before mutation, renewal or closing. The signed ad does not grant group authority. GROUP_BATCH cannot move an exact group to feature mode; delayed old-group garbage collection remains fenced against replacement ownership/generation.

## Status and announcements

Status observation uses **`0x800A/3`** for code-4 roots. Its 18 fields retain the NET2 order and snapshot/current-guard semantics; replace the old `proofIDOption` position by `proofInstanceIDOption`, and require rootReplayID to be InstanceReplayID. `typedRoot` uses the PI1 union above. Both proof-instance and judgment options use `[0]` absent or `[1,value]` present, and are present exactly for tag 4. The option values must bind the same instance and its target as the replay. The nativeProfileID position names the exact code-4 FoundationID; serviceEpoch continues to mean NET2 admissionEpoch, not a proof of present reuse.

A code-4 GET_STATUS request is serviced only under capability 8. Its reply is a historical observation at the named local cut, not receiver acceptance or a synchronized global state. Relevant exact policy, incident and protection guards remain the amended v2/v3 guards, not the superseded global-epoch retry rule from v1.

HINT keeps its outer NET2 message kind and four-field shape, but the negotiated PI1 profile admits rootReplayID `0x0015/3` and objectKind 4 for a proof instance. An optional root descriptor is `0x8111/3`. Tags 1/2/3 remain nonproof roots. The code-4 profile forbids tag 0; it cannot use a legacy discriminator merely because a proof instance is informally called a proof. Hints remain bounded nonauthorizing messages and create no import, checking, publication or custody work automatically.

## Native reads, archives and evidence consumers

Public-root and holder-bound export scopes can name an exact InstanceReplay only under capability 8 and the selected code-4 profile. BUNDLE1, EXPORT_HEAD2, byte layouts and inventory nodes keep their explicit generic typed-CID payloads and unchanged invocation accounting. Their validator's allowed closure is the exact PI1 traversal, including representation-map/term objects. A root CID does not authorize all map nodes of the same type or every proof of the same judgment.

EXPORT_HEAD2's required-profile list includes the exact code-4 FoundationID; the authenticated connection must also have advertised capability 8. An offline archive's exact root schema provides the replay-reader requirement. Offline content carries no right to install the checker named by the archive. Inventory equality, same-foundation checks and independent native replay remain required before acceptance.

Custody, current-incident support, transfer frontiers, public eligibility, evidence-family deduplication and reuse records bind exact InstanceReplayID and its actual full closure. Bare PI equality does not merge two representative contexts. A replacement proof of the same judgment does not discharge an existing promise to retain another exact replay. The mathematical profile change supplies no new deletion authority.

## Inert advisory pages

For code-4 client views select AdvisoryManifest `0x8120/2`, LibraryViewPage `0x8121/2`, and CollectionGuidePage `0x8122/2`. Their fixed existing shapes, member/entry/byte limits, kinds 0/1, and inert no-execution behavior remain unchanged. Manifest member kinds must agree with these schema-2 page types. Their replay-hint slots admit only InstanceReplayID under their exact code-4 FoundationID; theorem target references remain canonical JudgmentIDs, never proof-instance selectors in semantic syntax.

Serving these pages requires capabilities 4 and 8; a STRUCT2 hint does not enlarge the advisory manifest's allowed member kinds. Its exact explicit member list is still the entire advisory read authority. The optional presentation recipe of CLIENT1 is owner-local, not a new advisory record or permission to import arbitrary extension payloads. Old advisory schema 1 remains its frozen profile, not a place to smuggle new replay interpretations.

## Conformance cases and status

- A peer advertises code-4 F without capability 8: return unsupported-profile/codec; do not guess that generic content addressing implies native support.
- A legacy ProofID slot contains a PI ID: reject that schema binding, even if the instance later checks independently in a different correctly typed record.
- An ad claims K4 but its actual structural anchor lacks that token: it is a false lead/invalid producer binding, not a theorem verdict; holders never fetch it during admission.
- A mode-6 continuation is replayed against the schema-3 root-descriptor ordering: predicate/schema mismatch, not a new scan.
- A root's PI body remains identical while its representative map changes: evidence-pair deduplication, footprint and custody retain the distinct replay context.
- A current code-4 group receives an old-profile ad or an exact-key group receives K4: the whole bounded mutation fails before row ownership/root/version changes.
- An advisory root names a new semantic target but an incompatible replay hint: it remains an invalid advisory binding, never a new theorem acceptance path.

These bindings are selected specification decisions with the independent paper review recorded above; successful native, network or archive execution is not claimed.
