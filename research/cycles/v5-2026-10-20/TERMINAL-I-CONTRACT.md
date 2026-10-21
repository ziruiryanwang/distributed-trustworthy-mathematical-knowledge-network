# Direct-I certificates in the ordinary evidence facade

2026-10-21, core_growth. **Source contract only; no implementation, build, test,
proof production or installation is selected.** This bounded lane stops here;
mirror02's actual controller refusal now has priority. Root owns any resumption.

## Decision and exact current gap

The gap is real in current114 map
`experiments/v5-local-checks/distribution-validation-01-input.json`, SHA-256
`d11abac9a9c5a5ac7d7b22efbf26bb04fcad1e886f19a2195d42060dd44ab565`.
Do not introduce another checker, compiler, receipt transport or import session.
Use one explicitly tagged terminal-I packet in the existing ordinary facade.

Selected files that would need successors:

| Logical module | Current selected source beneath `software/v5/` | Current SHA-256 |
|---|---|---|
| `evidence_network/packet.py` | `evidence_network/packet.py` | `b4080ed8d8c0438079a1291a7493dea9df863d269b7eea35e32b4be961d9188d` |
| `evidence_network/custody.py` | `evidence_network/custody.py` | `38246a2892e8a14f74c6e78e7c25d1d70ffbe26269c59c71e5436623bd5ef73c` |
| `evidence_network/transport.py` | `iterative_queries/evidence_network/transport.py` | `5808c0e253b203cdf38bd2069c593888ea4814d47f756871237c38eb3e0caab7` |
| `client/workspace_evidence.py` | `body_location/client/workspace_evidence.py` | `fa636e2c75c9cd599732d7cb1e5a8fd8b2c5d42afc05e64ab6e67edbee92ff99` |
| `client/workspace_staged.py` | `interface_views/workspace_staged.py` | `23829a95bc047010487f16db39f6259cff35cb9bd75f722643f5e2a046851d76` |

Current packet terminal schema `DMKN_CERTIFIED_TERMINAL_MEMBER_V1` is exclusively
an A receipt plus member opening. Mixed packets require at least one delta.
`workspace_evidence._admit_evidence` sends every nonmixed packet to A admission;
`acquire` has no I opening branch; `export_evidence` explicitly rejects I;
`_publish` recognizes only mixed/A-terminal. `workspace_staged` also rejects the
new kind in inventory, stage/readback and final admission. Fixing only export or
packet parsing would leave the ordinary semantic reader unusable.

Already sufficient and unchanged: actual `ReceiptVerifier`; inherited
`M.CommonsClient.admit_receipt`; same-client I warrants; `use_legacy_handle`;
sealed/interface-only materialization; generic semantic-reader member handling;
module/group/body custody; index and HTTP routes. The lower-level direct-receipt
transport exists but should not become a second modern client workflow.

## Small exact representation

Add `DMKN_CERTIFIED_TERMINAL_I_V1`, with exactly these fields:

```text
{"schema":"DMKN_CERTIFIED_TERMINAL_I_V1", "journal":[184 bytes],
 "receipt_hex":"nonempty lowercase even-length hex"}
```

Use kind `terminal-i`; keep existing kind `terminal` unambiguously A. Require
canonical JSON, exact fields, current packet/terminal-receipt bounds, exact-byte
journal decoding and `B.member_journal(J)`'s existing I/foundation/policy/nonempty
group profile. Require `rank(J) <= envelope.rank`. Do not duplicate a summary,
infer I from the absence of A fields, create a zero-delta mixed exception, or
accept any header/index/siblings/extra field in this new schema.

Summary and ModuleID are derived from J. A structural parser returns receipt
bytes, exact J and those inert facts. Its census is one claim, one selected
terminal, zero deltas and no A membership siblings. Parsing never verifies a
receipt or establishes mathematical authority/source provenance.

## Explicit compatibility; no silent widening

Retain the exact V1 profile and default behavior. Add a closed V2 wire profile,
e.g. `DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V2`, that names both the unchanged A
terminal schema and the new I schema and uses a distinct proof-form string.
`public_profile(image, terminal_i=False)` may select the old/new exact profile;
`profile_id` must validate by exact version, never accept arbitrary added keys.

Thread the selected capability through custody `inspect`, client `_inspect` and
I export. V1 must still reject terminal-I even when its parser is installed.
Client constructor and `_active` must bind the immutable selected profile, not
always compare it with default V1. New parse/pack symbols remain covered by the
existing exact imported-symbol and required-source-pin checks.

Keep existing offer/packet routes and bounded database structure. Offer validation
must bind its proof-form string to the **selected request profile**, not accept
either string globally. Provider offers and acquisition reports use that same
selected form. This is the only transport-level change. Different profile IDs
refuse explicitly; do not automatically downgrade or mix old/new custody state.

A fresh V2 workspace uses its exact config-bound database; no old workspace is
migrated or rewritten. Existing mixed/A packet bytes can be explicitly retained
under V2 because their meanings are unchanged. This is custody, not new admission.
The discovery namespace for unchanged formal export features need not change;
the evidence-wire profile and its offer checks are separate commitments.

## Same public operations, exact authority

1. `export_evidence(I_warrant)` rechecks the original live I handle, packs its
   exact receipt and journal, then rechecks the live warrant before return.
2. `retain_semantics` and `publish` reuse the terminal publication path: selected
   group openings must already be durably held and match J's summary; available
   bodies remain commitment-checked, missing bodies remain explicit. Index,
   custody and publication success stay `mathematical_acceptance=False`.
3. Direct `acquire` or `admit_local` inspect the new form, bind the candidate's
   summary and any caller-selected J, then invoke the existing inherited
   `admit_receipt.__wrapped__` with its normal reservation/accounting. No A receipt,
   membership, conditional-native or new prover call occurs for this terminal.
4. After that call, require kind I, matching live profile, exact receipt binding,
   **live J == packet J**, and live summary == selected summary. This check is
   mandatory even without caller `expected_exact_journal`, and on same-live
   receipt-cache hits. Only then can the outer public call return the warrant.
5. Direct acquisition opens the selected group with the real I owner. Staging
   exposes a singleton inert member inventory [J]; it does not call any issuer.
   `admit_staged` consumes the existing one-use stage, follows the same I gate,
   calls I `open_group`, and performs unchanged final packet/group/member readback.
6. `SemanticReader.finish` already checks actual member inventory and imports
   selected exact journals. Its unchanged `import_context` dispatches I through
   `use_legacy_handle`, then the existing semantic-demand/sealed-interface path.
   Authoring yields ordinary mixed native evidence as today, not a new I receipt.

The mandatory post-admission J comparison is essential: ModuleID/summary do not
include rank. A genuine receipt for J at rank r paired with a packet claiming
the same module at rank r+1 may pass structural parsing and summary-only receipt
admission. It must fail before the outer call returns. An internal token minted
by the inherited routine cannot escape; the existing `_action` failure path
clears/ closes the client and owners on mismatch. Do not add a bypassing catch.

For this bounded extension, the modern aggregate-capable facade may retain its
existing **real configured A owner**. It must not reinterpret an I receipt as A,
create a dummy A handle, or require an A receipt. Making A configuration entirely
optional is a separate runtime simplification, not silently claimed here.

## Assurance and cost

Conditional on unchanged real I verifier/recursive-proof soundness and checking
interpretation, successful admission establishes validity of the actual verified
journal. Exact-J equality transfers that conclusion to the selected packet J.
Authenticated group/body checking and existing live import preserve its selected
semantics. Structural publication, provider identity, cached reports and source
bytes play no role as mathematical authority.

This certifies a valid module witness exists; it does not certify that separately
supplied Lean source or theorem-proof bytes were those used by the producer.
I and A remain distinct proof representations of exact mathematical journals.

Receiver work is receipt transfer/verification plus selected interface and
actually required semantic material, local validation and new contribution
checking. No mandatory theorem-proof-ancestry replay is introduced. A terminal-I
packet is `2*receipt_bytes + O(184)` JSON bytes; rank/payload/receipt and existing
operation budgets still apply. Transparent definitions and recursors can require
additional authenticated bodies/modules. No constant-time semantic-use claim,
cheap I-production claim, new certified frontier or positive full-cost growth
claim follows from this interface change.

## Concrete future discriminator, not an authorized run

Use the retained genuine receipt
`experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin`:
223,594 bytes, rechecked SHA-256
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.
Its base module is
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`,
rank zero; existing audited J hash is
`22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682`.

An existing custodian publishes that receipt as terminal-I plus group 10's
`binary_congr` opening, without any native wrapper or ancestral proofs. A fresh
agent discovers the theorem by a prospectively fixed formal query (not supplied
ModuleID), stages it, then admits/imports after provider shutdown. It can reuse
binary congruence twice to prove ternary congruence for arbitrary f and three
argument equalities, and publish the ordinary resulting mixed extension. This
is a small integrated workload, not an assertion of new mathematical novelty.
The actual query/type/source bytes and finite costs need separate review before
execution; no new I production is needed.

Required focused boundaries: exact schema/limits; V1 rejection/V2 acceptance;
profile/proof-form mismatch; forged I/A crossing; wrong receipt and same-module
different-rank J (including receipt-cache hit); absent I owner; withdrawn/foreign
handle; no staged authority; unchanged semantic NEED outcomes; durable selected
group readback; exact onward receipt/J preservation; zero A/native calls for
terminal-I admission. Existing completed campaigns should not be repeated.

The independent challenge is `TERMINAL-I-REVIEW.md`. This contract closes only
the source decision. Stop this lane now; address the current mirror02 controller
bottleneck before assigning implementation or an additional workload.
