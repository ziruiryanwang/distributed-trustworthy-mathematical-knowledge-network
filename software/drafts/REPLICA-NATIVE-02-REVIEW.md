# Replica native 02: independent source-delta and exact-launch review

2026-09-21. **PASS for the narrowly corrected fresh allocation's pre-execution
source/launch gate; not a runtime or mathematical-acceptance result.** This
review used source reads, inert JSON inspection and file hashes only. Root owns
the single execution. Allocation 01 and its historical reviews are preserved.

## Correction and preserved gates

Independent complete file diffs show exactly three worker hunks: fresh data
root `replica-native-02`, the receipt-status comparison below, and the pinned
coordinator filename. The coordinator changes only its fresh evidence/data
roots and worker filename. No product file or other behavior is changed.

`Scenario.binding()` now chooses `TRANSPORT_COMPLETE` for expected exit 0 and
`TRANSPORT_NONZERO_EXIT` for expected nonzero exit, then still requires the exact
expected return code. This matches the pinned supervisor's receipt contract.
The sole nonzero caller is `finish_service(..., refused=True)`, which supplies
exit 1 for the tampered B service. It does not accept `TRANSPORT_FAILED` or an
arbitrary refusal. Direct-child reap, active-zero, checked Job close, creation
before launch, attach/resume, zero limit terminations, no cleanup/output/
persistence/failure error, exact limits/pins/files/command/request/output/event
bindings and resource bounds remain unchanged.

The downstream negative branch still requires wrapper exit 1 and exact
wrapper/worker correspondence, `SERVICE_REFUSED / BUNDLE_DIGEST_MISMATCH`, false
mathematical acceptance, zero native stages, checker-free event and absent
readiness. Positive-service assertions and all later C/G/H gates are unchanged.
Allocation 01's actual retained negative receipt/output satisfies the intended
status/refusal interpretation but was rejected by the old unconditional status
comparison. My earlier allocation-01 source review missed that interpretation;
its original PASS note is historical, not a reason to relabel the failed run.

## Exact reviewed launch

Every current launch pin and product row was independently size/SHA-256 checked:
14 ordered input pins, 648,121 bytes; 101 product rows, 3,491,243 bytes; zero
missing files or mismatches. The product row list is byte-for-byte equivalent
after inert JSON serialization to allocation 01's list, and its path set matches
the independently enumerated current product selection. All unchanged input
pins, limits and retained bounds match allocation 01. Only the two new source
pins differ. The roots below were absent at review and remain subject to the
coordinator's exclusive fresh-root check:

- `product-local/replica-native-02`
- `software/qualification/replica-native-02`

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/replica_native_worker_v2.py` | 62,622 | `2c8046cf6962dafac9832084e5d31a43b7931d4fb0464800874caf8d0e2fd96e` |
| `tests/run_replica_native_v2.py` | 16,265 | `5b99ad8da8a2c041989d811b0a31d71a409a8ff406235101e1bc0202a651e3b8` |
| `qualification/replica-native-launch-02.json` | 43,423 | `bc4d2feac4d1f9ecc0b395fd0efb2775469174c11cafe147921ea4de3a9268b8` |

The coordinator adds the exact launch as pin 15: 691,544 total bound input
bytes. The fixed limits remain 450 seconds wall/aggregate CPU, 6,144 MiB,
16 processes, 65,536-byte stdout/stderr/event bounds and a 1 GiB retained
endpoint allowance. No timing comparison or borrowed native acceptance is
authorized by this gate. Original allocation-01 worker/coordinator hashes and
source-review hash were checked unchanged. No execution, import, compilation,
SQL, evidence repair or allocation-01 mutation was performed by this reviewer.
