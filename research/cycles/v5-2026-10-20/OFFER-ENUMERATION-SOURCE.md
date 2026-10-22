# Bounded offer enumeration: exact one-file successor

2026-10-22, storage_integration_adapter. Implemented source-only under root's
`OFFER-ENUMERATION-SELECTION.md`; no module import, test, build, installation,
experiment, external action or Git mutation was performed by this author.

## Source identity and exact delta

Base actual129 SDK map:
`experiments/v5-local-checks/distribution-exact-packet-01-input.json`, SHA256
`328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561`.

Logical key: `v5/delta/custody.py`.

| Role | Source | Bytes | SHA256 |
|---|---|---:|---|
| Preserved predecessor | `software/v5/delta/custody.py` | 11388 | `4304e529a15e9249d8ba43f5390e94082d0baad1c55db6fb5b74b4160a1fa27c` |
| Fresh successor | `software/v5/offer_enumeration/delta/custody.py` | 11389 | `e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634` |

The complete UTF-8 successor equals the complete predecessor with exactly one
literal substitution at `offer_request` line49:

```diff
-    F.uint(value["max_offers"], 1, 8); F.uint(value["max_bytes"], 1024, 16384)
+    F.uint(value["max_offers"], 1, 64); F.uint(value["max_bytes"], 1024, 16384)
```

The author checked that equality directly against the selected predecessor and
rehashed both paths. Existing LF encoding/final newline and all other bytes are
unchanged. No broader code rewrite or comment change was necessary. This is a
source-identity check, not an executed functional test.

## Selected importers and pin consequences

Resolved source paths from the actual129 map, not from directory age. A search
over all selected source paths found no hardcoded predecessor digest that
requires another Python/JavaScript successor. Direct and indirect users were
read at their actual selected paths:

- `delta/transport.py` imports this grammar and checks the same request in HTTP
  exchange, dispatch and server parsing. Its16384-byte route maximum and
  explicit max_bytes reservations are unchanged.
- `mixed_network/custody.py`, `frontier_network/custody.py` and selected
  `managed_storage/evidence_network/custody.py` import this validator and the
  unchanged blob/limit definitions. Their exact profile, ordered unique rows,
  requested count and actual compact reply-byte checks remain.
- These selected packet transports use the same delta HTTP machinery. Public
  `continuing_context/client/workspace_atomic.py:packet_offers` and
  `exact_packet/evidence_network/transport.py:offers` already forward explicit
  counts/byte caps. Their default4/4096 does not change.
- The selected `custody/receipt_store.py` has its own offer validator with cap8;
  it is unaffected. Do not claim all receipt-related APIs now accept64.
- Selected `exact_packet/client/managed_owner.py:PINS` does not hardcode the
  delta-custody digest. Its pinned evidence-custody source is unchanged. The
  owner's complete SDK writer commitment includes this logical row, however,
  so the resulting writer identity necessarily changes.
- `client/boot.py` snapshots the selected source table and passes its exact
  digests to the runtime. Selected `trust_withdrawal/client/runtime.py` builds
  source pins from that table; actual receipt/A/mixed owners accept and check
  those selected pin maps. No verifier source exception or weakened pin rule is
  needed for this parameter change.

**No additional source successor is required by the inspected selected pins.**
Root must still substitute this one logical row in any fresh launch/distribution
selection, preserve the other128 SDK rows, derive the exact new source/writer
commitments and authorize any use. A changed writer map must not be used to
silently reopen old managed-state generations. No installation rebuild or
migration is performed or implicitly authorized by this source note.

## Behavioral contract preserved

The change only permits explicit counts9..64. For the same old1..8 request,
all prior validation, SQL, serialization and response checks are byte-identical.
The store cap already is at most64 per module/profile; it is not increased.
Strict integer typing still rejects bool/count65. Reply-byte maximum remains
16384, with default4096 unchanged; callers requesting the full local set should
explicitly use `max_bytes=16384` within their original finite allowance.

The reviewed format bound is64 entries of at most108 bytes plus separators and
less than1024 bytes of fixed envelope: under8192 bytes, inside16KiB. One SELECT
returns one response-local view; later concurrent inserts need not be present.
No new snapshot/cursor state, provider inventory claim or global enumeration is
introduced. Formal-index snapshots and all packet wire profiles are unchanged.

The optional larger count requires a known upgraded provider. An old cap8 peer
can reject it; current public-action failure may terminate the client. Profile
equality does not advertise support. No automatic probe/fallback/retry or fresh
allowance is added. Enumeration creates no mathematical authority and does not
replace proof-form selection, one-shot staged admission or actual checking.
Revocation, storage/profile/hash checks, selected journal equality, custody
readback and body semantics remain unmodified.

## Handoff and validation boundary

API notes: `software/v5/offer_enumeration/README.md`.
Source/theory rationale: `PACKET-VARIANT-SELECTION-NEXT.md` / `e159c49a`;
independent challenge: `PACKET-VARIANT-SELECTION-CHALLENGE.md` / `93dc7413`.
Both explicitly separate later-locator access from certificate-failure recovery.

The separate controls owner is preparing focused real-store/HTTP metadata
controls against this exact successor. Root owns source-map selection, finite
execution and adoption; independent reviewer owns source and actual results.
No cryptographic acceptance, proof production, repeated genuine-I operation or
full-v5 completion follows from the present source-only implementation.
