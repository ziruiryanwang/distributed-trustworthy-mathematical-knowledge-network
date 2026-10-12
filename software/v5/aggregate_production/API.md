# Aggregate staged-production host

Source-only candidate. No compilation, execution or proof is selected. The old
module host/producer and the aggregate snapshot host remain unchanged. Root must
adopt exact host/source/runtime bindings and a finite operation before use.
There is no Python aggregate producer yet.

## Supported commands

    stage ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2
          KIND INDEX FRESH_OUTPUT RECEIPT_COUNT [RECEIPTS...]
          CAPSULE [REQUIRED_CHECKPOINTS...]

    verify ADOPTED_A RECEIPT EXPECTED_HEADER

All file paths must be absolute ordinary paths, without `.`/`..`, symlinks or
Windows reparse ancestry. Output is fresh/create-new/fsynced. No command acquires
a new whole guest session, builds a backend, starts a remote prover or chooses
a proof allowance. Segment proving still performs the pinned SDK's segment
preflight/witness reconstruction; that computation is charged as proving work.

`ADOPTED_A` is the independently selected lowercase image ID, never inferred
from an offered receipt. The ELF must match it. The selected native aggregate
relation must derive the exact192-byte H and pending typed I/A claims from WIRE.
Every receipt argument is genuinely verified in that pending-claim order. Only
the selected fixed-I/same-A profile is supported; no new multi-image policy.

`CAPSULE` is the **complete** existing fixed-integer bincode `DMKNAS01`, version1,
with the snapshot host's exact field order, session and capsule binding domains.
Partial segment files, saved success reports and old module schema3 refuse.
Actual capsule counts are s=1..128 segments and m=0..8 exact assumptions.

| KIND | INDEX | Required checkpoints |
|---|---|---|
| segment | 0..s-1 | None |
| lift | 0..s-1 | Corresponding segment |
| join | 1..s-1 | Previous prefix and corresponding lift |
| resolve | 0..m-1 | Full prefix, or previous resolve |
| finish | 0 | All s segments plus last resolve; full prefix if m=0 |

Prefix0 is lift0; subsequent prefixes are join1,join2,... . The complete fresh
graph has3s+m calls. Each call checks exact inputs and dependencies again; no
implicit next stage, fallback or retry. Finish performs verification, not another
prover operation. The enclosing owner charges all preflight, proving/verification,
file handling, diagnostics and finalization work.

## Checkpoints and outputs

The dedicated checkpoint encoding is bounded fixed-integer bincode:

    ("DMKNAP01" as [u8;8], version:u32=1, capsule_binding:Digest,
     kind:String, index:u32, proof_payload:Vec<u8>)

Field offsets: magic0..8, version8..12, binding12..44, kind-length44..52,
kind52..52+n, index52+n..56+n, payload-length56+n..64+n, payload64+n..EOF.
Kind length is1..7; exact allowed strings exclude finish. Payload is nonempty
and its declared length must equal the actual remainder before allocation/copy.
Unmodified old schema5 envelopes refuse. Anyone can rewrite this unkeyed framing;
doing so supplies no cryptographic authority and cannot bypass final exact A/H
application verification.

Framing binds the selected capsule, **not** a controller/host source-profile ID.
The host cryptographically verifies actual SDK payloads under its adopted verifier
context. Source/profile provenance and explicitly permitted checkpoint reuse
across compatible host versions are owner/producer selection obligations, not
an invented guarantee of this byte envelope. Forged payloads never gain authority
merely because their envelope hash was recomputed.

Successful `stage` stdout is one JSON object with exact fields:

    schema, status, kind, index, aggregate_image, header_sha256,
    capsule_binding, session_binding, segments, assumptions,
    output_bytes, output_sha256, application_receipt_created,
    guest_execute_calls, proof_stage_calls, mathematical_admission

Schema is `DMKN_AGGREGATE_PROOF_STAGE_V1`. Status is
`REAL_AGGREGATE_CHECKPOINT_NOT_APPLICATION_RECEIPT`, or
`REAL_AGGREGATE_RECEIPT_FINISHED` only for finish. `guest_execute_calls` counts
whole-session ExecutorImpl acquisition and is always0, not a claim of zero
segment witness computation;
proof-stage calls are1 for segment/lift/join/resolve and0 for finish.
`application_receipt_created` is true only for finish. `mathematical_admission`
stays false: the producer returns an artifact, not a recipient's private handle.
Stderr contains bounded-by-owner progress lines. A nonzero exit never adopts an
output, even if bytes were already written; retain them for explicit diagnosis.

Finish independently verifies the complete segment composite and all assumptions,
compares both composite and final succinct claims to `ReceiptClaim::ok(A,H)`,
then performs full non-dev succinct-Poseidon2 aggregate application verification
on the exact serialized receipt before writing. A joined conditional proof alone
is insufficient. Session target claims do not eliminate actual resolve work.

`verify` preserves the existing `DMKN_AGGREGATE_VERIFY_RESULT_V1` six-field
contract: schema, status, aggregate_image, header, receipt_sha256, receipt_bytes.
Status is `VERIFIED_RESOLVED_AGGREGATE_RECEIPT`. This remains usable by a freshly
adopted `AggregateReceiptVerifier` owner; no saved stdout is an admission credential.

## Bounds and residuals

ELF, capsule, checkpoint, receipt and output are individually at most64MiB;
WIRE at most16MiB; H exactly192bytes; all stage input reads at most512MiB.
Selected cycles1..2^28 and po2=12..20 are format ceilings, not runtime allocations.
Actual consecutive capsule segments must fit selected po2. No dev-mode or ambient
`RISC0_PPROF_OUT` environment is permitted.

Outer capsule vectors check declared counts before allocating/decode: assumptions
<=8, segments<=128, with nonempty segments required before use. This preserves
the serialized Vec ABI. Checkpoint envelope extents are checked before copying
payload. Bincode byte limits **do not bound total decoded heap**; nested SDK
claims/segments/receipts still use the pinned library's decoders. No total heap/
recursion bound is proved here. Finite enclosing memory/CPU/wall and output/
process limits are mandatory; allocation failure, panic or unclean process exit
cannot yield adoption. Resource Jobs are not hostile-code security sandboxes.

The owner also pins exact inputs, supervises clean closure, reserves reporting
tails, retains failed costs and ensures final input/output identity. Do not repeat
the base I proof or reuse its capsule-specific checkpoints. Existing genuine I
receipt bytes are legitimate premises after full verification. This source adds
no guest, mathematical rule, deployment, security-update policy or economic claim.
