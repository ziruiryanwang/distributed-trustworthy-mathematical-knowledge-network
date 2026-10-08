# CP-001D: interface inventory and cross-layer binding

Date: 2026-09-19  
Status: Concept integration inventory; not a second competing wire specification

The [mathematical](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md), [network](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), and [organization](../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md) companions own their respective record definitions. This inventory identifies where the records meet. A mismatch is a design defect; it is not resolved by an implementer silently choosing a favorable interpretation.

## Identifiers that must never be substituted

| Identifier | Binds | Does not establish |
|---|---|---|
| ContentID | Algorithm, object type, schema, exact canonical payload | Mathematical validity, available bytes |
| LogicProfileID | Pinned native logic/bootstrap/allowed representation | Correctness of every binary claiming that label |
| JudgmentID | Exact profile/context/telescope/conclusion | A proof or a selected witness |
| ProofID | Judgment plus exact native proof term | Selected proofs of all referenced theorem constants |
| ReplayID | Typed root plus exact selected native declaration/witness closure | Current local acceptance or storage |
| ModuleID | A finite set of exact exports and replay selections | Execution authority or a new foundation |
| ByteManifestID | Chunk layout for one object's payload | Logical dependency completeness |
| Snapshot ID/cursor | One provider's bounded indexed view and scan position | Global completeness, future service entitlement |
| Service action key | One issuer-local idempotent funded action | Foreign resource rights or theorem truth |
| NodeID | One operational public key | Unique human, honesty, independent failure domain |

Same ProofID with different ReplayID is a different evidence candidate. The root's selected witnesses determine footprint, availability, replay cost, and retention. A native declaration kind without a proposition must not be assigned a fictional JudgmentID to fit an index/status schema.

## Common encoding and allocation ranges

The common canonical value language uses definite arrays, uint64, and byte strings; fixed arities, shortest CBOR encodings, no maps/tags/text/floats/indefinite lengths/trailing bytes. Optional values are explicitly tagged.

ContentID has the fixed shape [algorithm, type16, schema16, digest32], with SHA-256's algorithm selector 1. The digest preimage includes the exact DTMKN-CAS domain, type, schema, payload length, and canonical payload. It is not a hash of pretty-printed mathematics.

Mathematical types occupy the selected low range: profiles 0x0001–0x0002; term, definition, context, judgment, proof, replay, module, scoped-negative relation, inductive group, and opaque declaration 0x0010–0x0019. NET1 owns 0x8000–0x80FF, with its assigned records 0x8000–0x800B. ORG1 owns 0x8100–0x81FF, including local descriptors 0x8101, query 0x8102, snapshot 0x8103, proof-family selection 0x8104, counters 0x8105, preservation assessment 0x8106, and public descriptor 0x8111.

Record existence does not imply public byte-read permission. Local validation, retention, counters, and control records can have exact local identifiers without being members of any remotely readable native closure.

## Replay roots and local status

| Root tag | Artifact | Evidence/closure path | Status projection |
|---:|---|---|---|
| 0 | ProofID | Exact judgment, native term, selected theorem witnesses and declarations | ProofID and JudgmentID present |
| 1 | DefinitionID | Exact checked type/body and selected dependencies | Proof/Judgment options absent |
| 2 | GroupID | Exact checked inductive group, generated members, external dependencies | Proof/Judgment options absent |
| 3 | OpaqueID | Exact checked type/body with opaque native behavior | Proof/Judgment options absent |

Tags 2 and 3 require the practical profile. The core and practical replay record shapes are determined by the selected mathematical profile; they cannot be interpreted by silently ignoring unsupported fields. A module offers multiple replay roots; it is not a way to hide an unadmitted root behind a collection identifier. In NET1 it is a local/offline batch wrapper decomposed into individually Replay-bound peer operations. ModuleID is not itself a replay root and is not implicitly GET_MANIFEST-readable through one member's closure. A future public module-catalogue operation would require an explicit bounded read scope.

The scoped-negative relation envelope is local derived metadata. NET1 advertises and transfers the ordinary negative proof's ReplayID. A receiver derives and checks the exact endpoint relation; it does not require an arbitrary operational incident object to become publicly readable.

## Operations and their authority

| Operation | Selected scope | Authority-bearing effect |
|---|---|---|
| FIND | One fixed public local index snapshot and exact bounded predicate | None beyond funded query/snapshot work |
| GET_MANIFEST | One object in a permitted public replay closure or audience export | Funded exact-byte serving only |
| GET_CHUNKS | Requested indexes/IDs in that permitted object's checked byte layout | Funded exact-byte serving only |
| GET_STATUS | One exact ReplayID and supported public policy view | A remote snapshot observation, not receiver acceptance |
| EXPORT_HEAD | One permitted replay root and finite audience-bound export | Finite authorized export pin; not eternal retention |
| GET_PROVIDER | One exact ReplayID | Bounded public route observations |
| GET_ROUTES | Profile and bounded formal collection keys | Bounded shareable contact hints, no recursive query |
| Local SUBMIT | Inert candidate package and requested local/public mode | Only local admitted checking and separately approved retention/publication |

Every remote paid operation uses OFFER_REQUEST, OFFER, CALL, and a committed computed RESULT followed by separately funded delivery. Receiving and serving are independently funded. Operational correctness is not inferred from remote self-reported meters.

## Queries and pagination

The five query modes are exact judgment, mentions-all extracted keys, head/shape, direct dependents, and typed formal relations. They query existing stored mathematics. None is a human-language problem statement or an unsolved-task record.

Query, holder, native/extractor profile, source posting list, planner, snapshot, service epoch, and deadline bind a cursor. ORG1 uses the initial marker, next-unprocessed exact descriptor ID, or end marker. A record is processed only after a completed nonmatch or committed matching output. An expired snapshot cannot be resumed by reusing its numeric position in a new collection.

An explicit END_OF_LOCAL_MATCH_SCAN is scoped to the declared extraction/predicate and provider snapshot. Partial scans, truncated structural keys, unsupported queries, and stale cursors remain different outcomes.

## Four different time/state boundaries

| Boundary | Purpose | Must not be confused with |
|---|---|---|
| Reliance epoch | Coherent current local evidence/policy/incident observation | Global theorem order |
| Service capability epoch | Offer/cursor/replay authority and bounded replay history | Automatic replenishment of budgets |
| Local retention time origin | Warm-cache deadlines through an uninterrupted authorized local clock generation | Remote provider timestamps |
| Immutable content/profile identity | Permanent interpretation of exact bytes | Mutable current availability |

Clean control-epoch rollover and actual reboot need not have identical retention effects. The network specification owns the selected distinction; mathematical content identities do not change merely because an operational epoch rotates.

## Cross-layer failures

Wrong bytes fail exact binding before checking. Missing closure ends in nondecision or another admitted fetch. Unsupported profile does not mean the mathematics is false. Native evidence rejection does not imply no alternate proof exists. Policy refusal is distinct from derivability. Storage refusal is distinct from both.

A committed acceptance without complete currently protected bytes is historical, not currently usable. A complete remote index response is still an observation; a local positive status is still bounded by its epoch and actual use pin.

## Remaining release qualification

The concept fixes the mathematical content grammar and key operational structures, but does not claim a released interoperable implementation. Exact enum/record fixtures, every nested public projection, generated bootstrap bytes, full encoder/decoder tests, OS metering/isolation, crash durability, and realistic Lean/export workload qualification are required before release.

Those obligations must preserve the boundaries above. They may calibrate policy defaults; they may not redefine a signature as mathematical evidence, an index as universal knowledge, or an incomplete closure as reusable proof.
