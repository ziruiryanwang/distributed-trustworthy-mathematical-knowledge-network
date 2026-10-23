# Owner commands build02: independent saved-evidence audit

Reviewer: `admission_event_audit`, 2026-10-23. No compilation, consumer, native
checking or preparation was rerun. This is compilation evidence only, not
ordinary owner use, successor acceptance or final-v5 qualification.

Operation: `experiments/v5-local-checks/ordinary-owner-commands-build-02`.

| Bound file | SHA-256 |
|---|---|
| selection.json | `86334f964377c5ca1744d0a1dd4f8f2b34445d80d629c9a4c7739b8ead962aa1` |
| RESULT.json | `d901884304a41ff8f7ce284e6051ccf9fb75f2aac9c3bd2a35acf9105541e133` |
| COMPILE-RESULT.json | `746b45cc04475097a90e9775a3f2e8388ea3aa824f5c753f67d298cc075b3d5b` |

Every selected source snapshot and runtime/helper pin was independently hashed
and matched. Both command sources are exact header-only staging successors of
the preserved failed build01 inputs, as recorded in the focused supplement to
OWNER-CONSUMER-SOURCE-REVIEW. All retained lower helpers were reused.

The saved inner commands compile only OwnerUseCommand and SuccessorExportCommand
with `-DElab.async=false`. Both exit zero; all four native stdout/stderr files
are empty. Inner wall times are 4.4109342 s and 0.9754407 s respectively. The
outer report shows a reaped direct child, zero active processes, clean Job closure,
no termination request and no cleanup errors. Recorded Job CPU is 2.46875 s,
wrapper CPU 0.484375 s (2.953125 s known total), outer wall 5.940078 s, and peak
Job private commit 879493120 bytes. The reported 0.03125 s supervision CPU is
within the wrapper process, not an additional independently summed process.

Build01's failed staging attempt remains preserved and charged: 1.75 s Job plus
0.5625 s wrapper CPU, no command artifact; its diagnostic is precisely the
non-meta local run helper. Build02 does not relabel or erase that failure.

## Complete fresh artifact set

The build02 directory has exactly ten files, five per successful module:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| OwnerUseCommand.ir | 227344 | `b2b709204c8a4f199653bc5b03968db3df7a69b5b4e3d9c7201ca4a36a44cbae` |
| OwnerUseCommand.ir.sig | 176 | `eda53933a84e7448bddf8f08b861cce2265de7ecaa658f9d1a96cbcdc208f66c` |
| OwnerUseCommand.olean | 278432 | `a889099f1b53ec785e98b4c071875d3e625dd679a9186e80798072cde804dab1` |
| OwnerUseCommand.olean.private | 579232 | `342d353b08522ac257d1c5a20a1f1d01c09c88bedf9c50f6b1edbb1a76ad54ab` |
| OwnerUseCommand.olean.server | 6928 | `786cce1381aaef4490ece8138e58f2c588ee2d4716002cc340589402bb67ecb3` |
| SuccessorExportCommand.ir | 65824 | `4c5e659488b3d7bf690097c2e7a3e1d702692e194aa3026a8907732eb3ec7bb5` |
| SuccessorExportCommand.ir.sig | 176 | `1b0e12b7564e879e8865d8cb195145d25463916a2419a91e3366741d8c59c8cf` |
| SuccessorExportCommand.olean | 81992 | `a6023a518c3923d3d31960ee2f671668e15a9ffddcc93dcb7631ea30c56bc9eb` |
| SuccessorExportCommand.olean.private | 210120 | `581f915c39dae3c9c077d4ed477f51add0d277d311cd189ec112091c33937a0c` |
| SuccessorExportCommand.olean.server | 2624 | `bbec212ec1bd1cd993ef641f6ae58cb903c73c4f9a00acb318f13276dadd1296` |

Disposition: PASS for the selected two-command compile and reuse of these
complete artifact sets in root-selected actual consumer integration. No adopted
mathematical state or receiver profile was changed. Actual authored successor
export and independent checking remain the substantive next gates.
