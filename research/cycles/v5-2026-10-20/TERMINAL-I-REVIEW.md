# Terminal-I ordinary circulation: independent source challenge

2026-10-21. Reviewer: adaptive_audit. **Source-design supported, subject to the
explicit obligations below; no implementation or runtime selected by this note.**

Reviewed against root's
[TERMINAL-I-CONCEPT-SELECTION.md](TERMINAL-I-CONCEPT-SELECTION.md), the exact
114-source input `distribution-validation-01-input.json` SHA-256
`d11abac9a9c5a5ac7d7b22efbf26bb04fcad1e886f19a2195d42060dd44ab565`,
and core_growth's directly communicated minimal contract. This is an independent
source/contract challenge, not a claim that a new implementation exists. No
imports, tests, build, proof or installation mutation were performed.

## Decision

The missing boundary is real but narrow. Add one explicitly tagged, closed
terminal-I packet to the existing evidence path. Do not create another checker,
receipt transport, semantic reader, import-session type or proof-production
controller. Existing direct-I verification and exact live-I imports already
provide the authority needed.

The proposed packet has precisely `schema`, `journal` and `receipt_hex`, with
schema `DMKN_CERTIFIED_TERMINAL_I_V1`. The exact 184-byte journal is structurally
checked under the current I/foundation/policy profile; the receipt is bounded
canonical lowercase hex. There is no duplicate summary, A header, member index,
membership path or claimed source provenance. Keep evidence kind `terminal-i`
distinct from the existing A kind `terminal`.

This is worth implementing only to remove the demonstrated ordinary-facade
incompatibility. It does not establish cheaper proof production, a newly
advancing frontier, positive full-cost growth or complete v5 deployability.
Root's now-observed mirror02 operational failure can take priority without
invalidating this source decision.

## Independently traced current behavior

Paths below are the selected physical sources, not similarly named historical
predecessors.

| Boundary | Current behavior / necessary consequence |
|---|---|
| `software/v5/evidence_network/packet.py` | Its terminal grammar calls `bind_member` and denotes A membership only. Add an independent exact I tag; never relax mixed packets to zero deltas. |
| `software/v5/body_location/client/workspace_evidence.py` | `_admit_evidence` sends every nonmixed form to A admission; `acquire` permits only A/mixed; `export_evidence` refuses I; `_publish` permits only A terminal. These are the direct missing branches. |
| `software/v5/client/workspace_mixed.py` | `admit_receipt` already delegates to actual I issuance; `_warrant` authenticates same-client owner handles and exact stored live facts. Reuse it. |
| `software/v5/conjunction_index/client/workspace_atomic.py` | Existing I admission owns reservation, live-cache validation, actual receipt verification and issuance. Do not duplicate it. |
| `software/v5/interface_views/workspace_staged.py` | Singleton inventory, stage/read kind checks and `admit_staged` currently omit I. They must accept the explicit new kind and call the actual I owner's `open_group`. |
| `software/v5/body_location/client/semantic_reader.py` | Already consumes staged inventories, then real `admit_staged`, then `import_context`. It needs no new proof-form workflow. |
| `software/v5/interface_views/imports_atomic.py` | `use_legacy_handle` creates an exact I frontier; actual handle type/profile, receipt digest, journal and committed groups/bodies are revalidated. Reuse this unchanged. |
| `software/v5/evidence_network/custody.py` and `software/v5/iterative_queries/evidence_network/transport.py` | Existing storage/routes are sufficient, but the exact profile and fixed proof-form label need an explicit V2 capability distinction. |

## Obligations that decide safety

### 1. Exact journal, not merely the same mathematical module

`ReceiptVerifier.receive` binds actual cryptographic output to the expected
summary. Module identity is derived from that summary; rank is not part of the
summary. Consequently the following is a concrete adversarial input:

- A genuine receipt verifies journal `J_r`.
- A terminal-I packet supplies a structurally valid `J_(r+1)` with the identical
  summary and ModuleID, within the allowed rank cap.
- The caller does not separately supply `expected_exact_journal`.

Summary equality and genuine receipt verification alone would accept the wrong
packet binding. Therefore the new outer path must unconditionally compare the
actual live I journal to the packet's entire journal, both on first admission
and same-live receipt-cache hits. An optional caller expectation is an
additional check, not a replacement for this comparison.

Require live kind `I`, unchanged I issuer/profile, exact receipt digest, exact
journal and summary before returning a public warrant. Reuse the existing
owner's `describe` and same-client `_warrant` checks. Inherited admission may
internally issue a token before the outer exact-J comparison; no such token may
escape on mismatch. Preserve the existing outer action failure's closing and
clearing of authority. Do not treat a structural parse or saved report as an
alternative issuer.

### 2. No I/A authority coercion

A terminal-I packet must use the existing real `ReceiptVerifier`, never
`AggregateReceiptVerifier.select_member`, a fabricated zero-member header or a
native/dummy theorem wrapper. A client lacking its explicit I owner refuses
mathematical I admission. Structural custody can remain possible without one.

The same ordinary facade presently requires a real configured A owner for its
broader mixed operation. Retaining that configuration is acceptable for this
minimal extension, provided a pure-I path makes zero A verification/membership
calls and zero native-delta checks. It is not evidence of an independently
deployable I-only runtime. Removing that unrelated construction requirement is
a separate design decision, not an excuse to fabricate an A owner.

### 3. Closed capability profiles and compatibility

Do not silently widen V1. The new profile must explicitly advertise terminal-I
support and have a distinct exact profile identity. Retain the old public
profile's defaults/meaning and refuse crossed or malformed forms.

In particular, adding a parser branch must not let an old V1 `PacketStore`
silently accept I packets. Thread the exact owner-selected profile capability
through packet inspection, store inspection, local/staged/network admission,
packing/export and publication. Current constructor/activity checks compare
against `public_profile(image)`; successors must validate the selected exact
version, not accidentally reconstruct V1 for every client.

Offers must bind their proof-form label to the exact selected/requested profile,
not merely accept either V1 or V2 label globally. The current transport imports
a fixed `PROOF_FORM`; its validation and reporting require the same explicit
version binding. Existing routes, budgets and store transactions can remain.
The immutable stored configuration already includes the full wire profile:
use fresh configured stores, not in-place migration of retained workspaces.

### 4. Semantics and source bindings remain independent

Use current `B.member_journal` restrictions plus the envelope rank cap, exact
byte/field/canonical checks and existing receipt/packet limits. Those are
structural checks only. Real same-call I verification must retain fully resolved,
non-development certificate checks, current trust adoption, source/runtime pins,
resource limits and clean process closure.

Pin new parser/packer imports as actual selected symbols and loaded source
origins, as the current facade does for A terminal helpers. Do not let a provider
choose an executable, image, policy, authority owner or source file. A valid
module receipt certifies module validity under the adopted relation; it does
not attest that separately supplied Lean source or proof bytes produced it.

After admission, call the I owner's `open_group` in both immediate and staged
paths. Keep the existing explicit exact-J selection, sealed interface/context
and demanded-body validation. Definitions, universes, recursors and conversion
dependencies do not disappear behind a receipt. Missing semantic data remains
an explicit demand/incompleteness outcome. No theorem proof witness or parent
receipt becomes mandatory just because this wire representation is new.

### 5. Publication and retained custody do not transfer live authority

Reuse the terminal publication branch's durable packet/group readback,
quota-bounded retention, false mathematical-acceptance labels and explicit
partial-publication outcomes. A raw structural publication is not receipt
verification. An export from a live I warrant can bind exact receipt bytes to
that warrant, but the resulting packet is again untrusted data for another
owner. Closing/withdrawing the sender must revoke live tokens without deleting
otherwise retained public bytes or making their recipient trust automatic.

## Conditional correctness and cost argument

Let `E=(tag_I,J,r)` be a well-formed packet and `S=summary(J)`. Existing real I
verification supplies `Verify_I(r) => Valid(J_actual)` under its stated
cryptographic and checking assumptions. The new mandatory comparison supplies
`J_actual=J`; existing group/body opening checks then bind selected semantics to
`S`. Thus successful use obtains the same I frontier already accepted by the
current import relation. No A authority premise has been introduced.

The receiving work consists of packet transfer/parsing, one genuine I
verification or same-live cached-handle revalidation, selected semantic opening
checks and any actually demanded semantic acquisition. It has no mandatory
term for transitive theorem-proof witnesses or ancestor certificates. This is
an ancestry-independence statement, not constant-time mathematics, global search
completeness, a practical speedup or a successful production-cost bound.

## Minimum later evidence, if root selects implementation

One focused changed-boundary suite should cover strict schema/caps, V1 refusal,
profile/offer mismatches, unsupported I ownership, actual I-versus-A dispatch,
the same-ModuleID/different-rank counterexample including cache hits, staged
singleton inventory, final source/trust invalidation and committed semantic
binding. Reuse unchanged lower-level transport/import controls.

One later same-facade workload may use a retained genuine I receipt: publish
and discover its formal export, structurally acquire it, close the original
provider, freshly admit through the actual I owner, import its selected
interface and expose/reuse it through the existing contribution path. Record
receipt/native/A call counts and exact J/source/policy bindings. A second proof
campaign or repeated lower-level transport demonstration is unnecessary.

This note selects none of those operations. It establishes a bounded actionable
design, preserves the pending successful-frontier and full-cost-growth gaps,
and leaves the root free to address the higher-priority current operational
failure first.
