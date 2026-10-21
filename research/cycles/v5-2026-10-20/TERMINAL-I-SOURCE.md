# Direct-I evidence in the ordinary facade: implementation checkpoint

2026-10-21, core_growth. Source-only implementation of root's
[selection](TERMINAL-I-IMPLEMENTATION.md), reviewed contract SHA-256
`38a5f73ccabe70e1bdcffba55623d6f9ce008b46188f46d4348a86668a8c80a8`
and independent review
`c82d15c63ea2718c981b80c5d86c35006330fcb068410d017f983361c4fe6519`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No product import, parsing/compilation, test, build, installation, native call,
network operation or proof production was performed by this assignment.

## Exact five-file successor

Baselines are the five selected files from current114 map d11abac9, not old
logical-path implementations. All baseline hashes were rechecked unchanged
after writing. Only assigned fresh paths below `software/v5/terminal_i/` were
edited. Frozen origin-validation sources and Git were not modified.

| Logical module | Baseline path beneath `software/v5/` | Baseline SHA-256 |
|---|---|---|
| `evidence_network/packet.py` | `evidence_network/packet.py` | `b4080ed8d8c0438079a1291a7493dea9df863d269b7eea35e32b4be961d9188d` |
| `evidence_network/custody.py` | `evidence_network/custody.py` | `38246a2892e8a14f74c6e78e7c25d1d70ffbe26269c59c71e5436623bd5ef73c` |
| `evidence_network/transport.py` | `iterative_queries/evidence_network/transport.py` | `5808c0e253b203cdf38bd2069c593888ea4814d47f756871237c38eb3e0caab7` |
| `client/workspace_evidence.py` | `body_location/client/workspace_evidence.py` | `fa636e2c75c9cd599732d7cb1e5a8fd8b2c5d42afc05e64ab6e67edbee92ff99` |
| `client/workspace_staged.py` | `interface_views/workspace_staged.py` | `23829a95bc047010487f16db39f6259cff35cb9bd75f722643f5e2a046851d76` |

| Fresh path beneath `software/v5/terminal_i/` | Bytes | SHA-256 |
|---|---:|---|
| `evidence_network/packet.py` | 7795 | `cf8aaa6190d46c4b41792cb54da7da5983d19450cafb65920af2a188afbbcefd` |
| `evidence_network/custody.py` | 8166 | `c039af086cf73d57191187e9d5b02292c5c9b8a3fb455d67dc719ad8f7d183a0` |
| `evidence_network/transport.py` | 6474 | `7ac7204b6e97b48eb1764c92b98437ad87e45f0fc62aa78973f5985816d63827` |
| `client/workspace_evidence.py` | 51539 | `8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68` |
| `client/workspace_staged.py` | 16522 | `ae3dc1a743a0cf4bd2da7f388ed46d6f75f73330802b9263a03a54a230fafd2b` |

The root's subsequently staged origin114 source map is
`2ea8322879b2e45afb2a2f5e8d99500bfcfdbe0982cdf14687b1e8bdd0950556`;
its two origin changes do not alter these five baselines. Root owns the exact
future integrated selector; this note does not select or perform a build.

## API and diff summary

Packet representation adds only the explicit schema
`DMKN_CERTIFIED_TERMINAL_I_V1` (`I_SCHEMA`) with exact fields `schema`,
`journal`, `receipt_hex`. Journal is an exact 184-byte array; receipt is bounded,
nonempty, lowercase even-length hex. Canonical bytes, the existing packet and
receipt limits, `B.member_journal` and envelope rank limits are enforced. The
returned evidence kind is `terminal-i`; existing `terminal` remains A-only.

- `inspect_evidence(..., terminal_i=False)` preserves V1's refusal by default.
- `parse_terminal_i(raw, envelope, *, aggregate_image,
  terminal_receipt_bytes=MAX_RECEIPT, terminal_i=False)` returns
  `(receipt_bytes, exact_journal, structural_member_facts)` and requires explicit
  `terminal_i=True`.
- `pack_terminal_i(journal, receipt, *, aggregate_image, envelope,
  terminal_receipt_bytes=MAX_RECEIPT, terminal_i=False)` has the same explicit
  capability requirement. No parser/packer creates authority.
- `public_profile(aggregate_image, terminal_i=False)` returns exactly the old
  V1 profile by default. True selects schema
  `DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V2`, form
  `mixed-or-certified-terminal-v2`, and the additional exact
  `terminal_i_packet_schema` commitment. `profile_id` validates either complete
  closed profile, not arbitrary schema/field combinations.
- `verify_offer(value, request, *, profile)` now requires the exact selected
  profile. Root explicitly approved this intentional helper-signature
  tightening: an opaque request profile ID alone cannot establish its proof
  form. Both selected provider/acquirer callers pass the profile. V1 wire bytes
  and default profile meaning remain unchanged; there is no two-argument
  fallback that could accept a V1 label paired with a V2 request ID.

Custody inspection and offers revalidate the selected profile ID, then use that
profile's capability/form. Existing store transactions, quotas, routes, config
binding and readback remain. A new V2 workspace is fresh and explicitly
configured; no V1 store is migrated. Unchanged mixed/A evidence can be retained
under the explicit new profile without changing its mathematical meaning.

Client construction snapshots `_wire_profile_id`; `_active` binds store,
configuration and original ID. `resolve` passes the selected profile instead
of accidentally reconstructing default V1. New parser/packer symbols enter
the existing exact symbol guard and are covered by the same required source
pins. Direct acquisition and staged admission open I groups through the real
I owner. Staging retains one inert member J, preserving one-use transition,
packet/group/member readback and existing budgets. The generic semantic reader,
sealed/interface-only import and `use_legacy_handle` paths need no changes.

`export_evidence` uses the original live I warrant, packs its receipt/J, checks
the exported target, then rechecks the live warrant before return. Publication
reuses the terminal durable semantics/readback path and keeps
`mathematical_acceptance=False`. Missing committed bodies remain explicit.

## Exact mathematical authority and failure behavior

For terminal-I, `_admit_evidence` calls the existing inherited
`M.CommonsClient.admit_receipt.__wrapped__`; its original reservation, receipt
cache, genuine verifier, resource and trust behavior remain. It then checks
live kind I, exact receipt bytes/digest, selected I profile, exact journal and
summary. The existing common live-J comparison is unconditional, including
receipt-cache hits and callers that did not provide `expected_exact_journal`.

This closes the concrete same-summary/different-rank gap: if a packet pairs
receipt for `J_r` with `J_(r+1)`, summary-only receipt checking may succeed, but
the mandatory live-J equality fails before an outer public call can return.
The unmodified outer action failure closes/clears client authority. There is
no catch that releases the internally minted token after a mismatch.

Conditionally, unchanged real I verification establishes `Valid(J_actual)`;
the new exact binding establishes `J_actual = J_packet`; unchanged semantic
opening and import rules bind the selected reusable mathematics to that J.
No A receipt/membership or native-delta verification is called for terminal-I
admission. The modern facade still has a genuine configured A owner for its
broader operation; this is not an I-only runtime or optional-A claim.

The receipt proves module validity under the adopted relation, not provenance
of separately supplied source or theorem-proof bytes. Publication/discovery
remain structural. Unchanged withdrawal, source origins, resource enforcement,
failure cleanup and exact semantic materialization remain necessary.

## What this advances, and what is not established

This connects existing ancestry-independent I certificates to the ordinary
discover/stage/admit/import/contribute facade without another checker, transport,
reader or proof-production route. Receiver cost includes selected receipt,
interface and demanded semantic material, not mandatory ancestor proof replay.
It does not establish cheaper new I production, new certified frontier growth,
positive full-cost benefit or a completed v5 release.

Independent focused controls are assigned to adaptive_audit; root owns their
finite launch and integration. Required boundaries include V1/V2 isolation,
profile/form crossing, actual I dispatch, fresh/cache rank substitution,
staged authority absence and final semantic readback. No old passing campaign
needs repetition. These sources are ready for exact independent review, not
represented as executed or adopted software.
