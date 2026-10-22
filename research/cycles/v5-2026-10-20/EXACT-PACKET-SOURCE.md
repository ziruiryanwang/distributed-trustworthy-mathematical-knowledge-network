# Exact packet: six-file source checkpoint

2026-10-22. Author: storage_integration_adapter. Source-only implementation under
[root selection](EXACT-PACKET-IMPLEMENTATION-SELECTION.md), following the
[decision](EXACT-PACKET-ACQUISITION-DECISION.md) and independent
[challenge](EXACT-PACKET-ACQUISITION-CHALLENGE.md). No execution, installation,
credential access or Git mutation was performed by this assignment.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Immutable base map: `experiments/v5-local-checks/distribution-managed-storage-01-input.json`,
SHA256 `a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.

All new source paths start `software/v5/exact_packet/`. Paths in the predecessor
column start `software/v5/`. Sources were copied mechanically through
`apply_patch`, then narrowly changed; no predecessor was edited.

| Logical suffix | Predecessor source | Predecessor SHA256 | Successor bytes | Successor SHA256 |
|---|---|---|---:|---|
| `evidence_network/transport.py` | `terminal_i/evidence_network/transport.py` | `7ac7204b6e97b48eb1764c92b98437ad87e45f0fc62aa78973f5985816d63827` | 8581 | `b34032085bca3ddbd248afe57e655777a140d2c34b6f33ea61b80721a07b926c` |
| `placement/controller.py` | `selective_placement/placement/controller.py` | `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49` | 18008 | `77820241984b9dc7ba5d2117a4b11bc89bf217b81697ed8d8ce90fff15e115f2` |
| `client/workspace_evidence.py` | `managed_storage/client/workspace_evidence.py` | `d94e38257444da3bda04e4d9b298d422280a573becc27eaa063fdbc01f9c02a2` | 53636 | `3f39d9b594490f04e2737c0f0595c881785a9a6a168cf8fc679d25a5cdef700e` |
| `client/workspace_staged.py` | `terminal_i/client/workspace_staged.py` | `ae3dc1a743a0cf4bd2da7f388ed46d6f75f73330802b9263a03a54a230fafd2b` | 17110 | `5d96c8cb891eabeb083b0bc501df1a7b268c21b73f4c17da7eb536d2428ad995` |
| `client/semantic_reader.py` | `body_location/client/semantic_reader.py` | `17a3da541ac6f55914e4f4aee1da140dbc2b4cf1b96139bd34bb16503b950383` | 35110 | `253b0ffb5825de15c239be785edcda7e15647038716679402cdf990b81f4128d` |
| `client/managed_owner.py` | `managed_storage/client/managed_owner.py` | `6991ac58310b0c3a6456f033bff7bccbb02dd1299c67716d805762e0dea69a0f` | 33789 | `9a459df2cf2c81b953044b4b5172aaefb9a3001cede6f3a1a23b29f8beb6dcb1` |

## Changed boundary

- Transport `packet`/`packet_exact` share `_packet(..., offered=...)`. Only the
  offered branch requires a recorded offer. Both freeze strict scalar identity
  before awaiting and retain actual typed custody, current profile/object-cap
  preflight, original `_get` accounting, precommit activity and exact readback.
- Client `acquire`/`acquire_exact` share `_acquire_packet(..., offered=...)`.
  Entry and every body selection are copied before the first transfer. The
  existing admission/cache/live-journal tail is unchanged. Public decorators
  remain the only action wrappers; the private helper is undecorated.
- `stage_packet`/`stage_packet_exact` share `_stage_packet(..., offered=...)`.
  Staged tokens still name only structurally checked held bytes. Source caps,
  same-module selection refusal, member inventory and metadata charges remain.
- `SemanticReader.stage`/`stage_exact` share `_stage(..., offered=...)` with one
  original `_call()` scope. Exact pending-demand/variant and staged-binding
  checks remain; admission/import is unchanged.
- Placement replaces only the missing-packet offer request/prerequisite with
  the existing manifest's exact request. Its conservative quote is unchanged.
- Managed owner changes only the explicit evidence-client pin. Complete SDK
  writer identity changes; no silent old-state reopen/migration is selected.

No false offer is inserted, no new wire protocol/schema/source logical name is
introduced, and no structural response grants mathematical authority. Exact
size remains mandatory. Point retrieval is independent of the length of the
offer prefix; it is not useful unknown-ID discovery or global completeness.

## Handoff

Independent review owns the source judgment. Distinct controls cover actual
HTTP/typed stores/placement and explicitly labeled synthetic facade ownership
and dispatch checks. Root owns all execution/adoption and the next129-source map.
These source hashes are not evidence of executed qualification or full v5 release.
The short [API README](../../../software/v5/exact_packet/README.md) records use
and limits without adding a second operator guide.
