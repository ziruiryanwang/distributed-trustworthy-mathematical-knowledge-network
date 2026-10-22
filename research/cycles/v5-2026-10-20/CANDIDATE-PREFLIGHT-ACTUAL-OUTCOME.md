# Installed candidate preflight: independent actual outcome

2026-10-22, storage_launch_review. **PASS for the selected installed boundary.**
This is a read-only audit of the completed session24572, not a rerun. No product
module was imported, verifier invoked, database opened or persistent state changed
by this audit. The full final-v5 goal remains open.

## Selection and exact evidence

Selection: CANDIDATE-PREFLIGHT-ACTUAL-DECISION.md; independently reviewed owner
3230440a, selector f5ed6e94 and actual-source9f7ef86d, reviewcacf4391. Installed
release bd9f161c43551a578605d5e0c7da34c332cb838c1c70ddb859d2ebd0062b8f03 has
the already adopted build audit91639355. This audit does not repeat the full
842 MB payload audit.

Let B be `product-local/v5-distribution-candidate-preflight-01`, and O be
`B/candidate-preflight01-operations/installed-candidate-preflight-01`.

| Evidence relative to O | Bytes | SHA-256 |
|---|---:|---|
| RESULT.json | 2502 | 6c5a842f8be578867d104061e040c14627075a1806d15f5e9df5aaa4703df898 |
| BOOT-RESULT.json | 5914 | d89a5bdba1bc858e786d674f8235636e219d0b60d92545a372be5509540357ee |
| plan.json | 23300 | 30ae3a26dfcc1b9cc9a24995dd24d6b5875195ab5677e3ee4136ac6fb2e9fc4b |
| command/command.json | 964 | 07e197707d61bb52916a44890c0973b8f0975e087ae45da94224d0fc10d1cacf |
| work/candidate-preflight-actual-result.json | 347467 | 8573c47d9a84f035d87d81f200e4802a0461d8cf522de976510d54e8743aad3c |
| work/good-terminal-i.json | 447887 | a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3 |
| work/malformed-peer-packet.bin | 1 | 021fb596db81e6d02bf3d2586ee3981fe519f275c0ac9ca76bbcf2ebb4097d96 |

All132 selected source entries (1780031 bytes) independently match plan bytes
and SHA-256 at both their original owner/installed paths and copied operation
paths. The ten inner source hashes match those plan rows. The BOOT origins stay
under the selected copied v5/portable trees. All four input pins independently
match their files. The original owner and fixture are selected test adapters;
the installed consumer implementation is not replaced by a test double.

## Genuine verification and exact data

The retained good packet is DMKN_CERTIFIED_TERMINAL_I_V1. Decoding its receipt
hex as data gives223594 bytes with SHA-256
850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47, exactly the
selected original I receipt and saved receiver receipt.bin. Its184 journal bytes
equal the pinned expected journal and the actual verifier's returned journal.

Consumer operation56fb66240344ba038a4bd655cb72e6cafbc54513e2faa9613fefdc85c0f8b86c
contains exactly one receipt operation, receipt-1. Its saved command invokes the
installed module_host.exe `receive` with image9dfd5892, the exact receipt copy
and module2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e.
The native result is REAL_MODULE_RECEIPT_VERIFIED, fully_resolved=true,
mathematical_admission=true, rank0 and the exact selected summary/policy.
Process exit0, direct child reaped, Job closed, active0, terminated0 and no
cleanup errors. The binding record says SAME_CALL_BINDINGS_VALIDATED_BEFORE_HANDLE.
Receipt process.json SHA-256 ae306c91f0697ef1b6ee4e75ea070872c19bcc8af316cf2cf10972e77ba0ba37;
1535-byte stdout SHA-256 1b6236bda564c7b0a7ce8bc124d2a2be4cc8b9712f5e98a7061bdf8f18636515;
stderr is empty. This is existing-I acceptance, not new proof production.

## Malformed candidate, preserved authority and offline continuation

The separately saved bad byte is literally123 (`{`), with its own correct
advertised digest/length. The test-only adversarial provider dispatches that
byte once through the real socket; it is not seeded into PacketStore. The
unmodified installed client returns CANDIDATE_REJECTED_UNDER_SELECTED_POLICY /
PACKET_STRUCTURE_OR_SELECTED_POLICY, mathematical_acceptance=false, under
LOCAL_CANDIDATE_PREFLIGHT_NOT_MATHEMATICAL_ACCEPTANCE. This is a policy-relative
rejection of these bytes, not a global assertion about the mathematical module.

| Observation | Before bad candidate | After bad candidate | After offline continuation |
|---|---:|---:|---:|
| Charged acquisition requests | 5 | 6 | 6 |
| Charged acquisition reply bytes | 711626 | 711627 | 711627 |
| I verification attempts / submitted bytes | 1 / 223594 | 1 / 223594 | 1 / 223594 |
| Reserved I worker CPU seconds | 10 | 10 | 10 |
| Aggregate / mixed / native attempts | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Same-live reuse hits | 0 | 0 | 2 |

The request/reply increase is retained although the candidate is rejected.
No second mathematical-verifier attempt or reservation is created. HTTP delta
counters advance from1 successful transfer/447887 bytes to2/447888; no transport
failure is substituted for the intended structural rejection. Pending requests,
reserved reply bytes and unknown request/header upper bounds are zero.

Provider accounting ends at5 actual requests,1039 request-body bytes,453838
reply bytes and1142 header bytes, with no active/refused/failed requests. These
are not equal to the conservative client ledger: direct-contact search prepaid
3 requests/262144 reply bytes, giving6 charged client slots overall. Do not
add actual and conservative reservation figures as independent traffic.

The provider is stopped before continuation; its five tracked handlers all
close, with zero active handlers or handler errors. Exact consumer/provider
packet snapshots are unchanged before/after: one good packet/offer in each,
448215 logical bytes, no malformed candidate in custody. The staged report
is exactly unchanged except admission_consumed=false becomes true only after
offline `admit_staged`. The caller's explicit identity checks confirm the same
owners, grant, old READY context and originally unconsumed stage are retained;
no reset or private-state repair fabricates continuation.

Both old and advanced imports return UNTRUSTED_AUTHORING_CONTEXT_READY with
no demands. Each selects one group/declaration,24908 input bytes and26086
frontend packet bytes, with1005 counted expression visits. Both are interface-
only and report zero frontend theorem-ancestor proof bytes. The advanced session
retains one receipt/source/warrant and223594 receipt bytes; calls advance4->10,
submitted bytes225948->228302. This is not zero semantic/checking work and the
authoring context itself is not mathematical acceptance. No authoring, packet
offer publication or proof production occurs in this operation.

## Closure and cost

Inner status COMPLETED, stage done, error=null and cleanup_errors=[]. Client
ends CLOSED with all issuers closed and no live handles/members/aggregates;
consumer and provider workspaces are closed. Temporary trust is withdrawn.
`B/candidate-preflight01-trust/WITHDRAWN` is371 bytes, SHA-256
da91cfb5ee58ddc6fa04087da47ab9cfff599b5baa214a7b65afed1974338930. Its adoption
triple exactly equals the inner report and trust record. ADOPTION.json hashes
to21e7426e7d4ef9b9567fdcffe7582c6b5a89100081c18df6916a872b24c90708 as expected.

Outer status COMMAND_EXITED_ZERO_AND_CLOSED; BOOT OWNER_EXITED_ZERO. Final
error null, no cleanup errors, no termination requested, child reaped and Job
closed with4 total processes,0 active and0 terminated. Outer stdout/stderr0.
Inclusive Job CPU20.390625 seconds (user10.25 + kernel10.140625), wrapper
CPU5.609375: **26.0 known measured CPU seconds**. Bootstrap5.375 and supervisor
0.109375 are already nested in wrapper accounting; receiver work is already
nested in Job accounting. Neither is added again. Wall30.7498198 seconds,
through child cleanup30.6047295. Pre-clock interpreter startup is unmeasured,
not zero. Peak Job private commit117506048 bytes. Observed outputs before final
outer result2605564 bytes/165 entries; no claim of a hard filesystem quota.

This closes the selected actual preflight/continuation boundary. It establishes
neither new A certification nor recursive renewal, growth benefit, arbitrary
hostile-peer isolation, independently hosted availability, global search
completeness or full-v5 release readiness. Preserve this completed operation;
the next central work is genuine same-image certified-frontier production,
not another run of this already demonstrated boundary.
