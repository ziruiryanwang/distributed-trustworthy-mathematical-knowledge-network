# One evaluator execution-capsule discriminator

Source-only root selection. Adapter:
`software/v5/evaluator_method/snapshot.py`, 170 lines / 10,394 bytes, SHA-256
`1e68b9c5ee652d2d8fb82c640ee0174ebd5b8209c9b9c635d9058c634e517fa5`.
No runtime, test, import, compiler, guest execution, proof, RAM inquiry or Git
action was performed by this author. Root owns selection/launch; independent
semantic and resource/CLI reviews are separate.

## Why this narrow adapter

Existing `OwnerPreparation.snapshot` requires a producer-specific child record
including source and selection metadata. The accepted mixed result is not that
record. Rather than manufacture such a record or add a product lane, this
bounded operator adapter directly invokes the **existing** adopted module host's
`prepare` and `stage ... snapshot` commands. The existing finite outer runner
provides the Job; direct children have fixed timeouts. No production allowance
or proving request is made.

The snapshotted imports are only `modules/{__init__,codec,model,native_rows}.py`
and `modules/receipt/{__init__,witness}.py`. The latter imports the former;
the full SDK is not copied or substituted. This adapter establishes input/output
bindings and operational evidence, not mathematical acceptance.

## Exact retained inputs

| Role | SHA-256 |
|---|---|
| Installed old-I module host | `74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9` |
| Installed original module image | `d76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f` |
| Accepted evaluator witness (50,017 bytes / 697 rows) | `8b84084486b0aadceb9ee353a28654b2777e297a726693135c575d5c50e85f5a` |
| Genuine BASE I receipt | `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47` |
| Actual evaluator result | `adc7fe79bf6870c01c00df4fdd68567129b3d20217c938a4b125d8b7616ac9e3` |
| Actual accepted child journal | `e1b67f57ac9612a20b33231c2b71b2bd9260e6f4eb50fa9d0d761cd80408fbed` |

Image ID remains
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
The child journal is taken from the pinned completed actual result and separately
hash-bound, not invented from source metadata. The result is inert expected-byte
evidence; the new host call independently verifies its genuine parent and guest
conclusion. The witness must already be canonical with the exact old image,
rank1, selected groups0/10 and two rules. Preparation internally assigns the
computed image field by convention, so **frame payload byte equality with the
original witness** is required, along with byte equality to the actual child J.

## One attempt and useful result

CLI: `snapshot.py CONFIG_PATH CONFIG_SHA`. Configuration schema is
`DMKN_EVALUATOR_SNAPSHOT_SCREEN_V1`; exact fields are `schema`, `host`, `image`,
`witness`, `receipt`, `accepted_result`, `output`. Artifact fields are full
path/byte-length/SHA-256 pins. Root's outer selection pins the runtime closure.

Only two subprocess commands are permitted: prepare (30-second timeout), then
one snapshot (150-second timeout), within the original 200-second owner wall
boundary. Snapshot uses **2^25 cycles, po18, one genuine parent**. No retry,
segment proof, lift, join, resolve or finish command is emitted. RISC0 environment
overrides are removed for these subprocesses; the adopted host separately fixes
non-dev verification options.

A successful schema3 capsule is retained and bound to exact image/frame/J/parent
pins and the host binding. Capsule hashing/schema/census and final pin equality
are checked. Output census/log limits are postchecks; the outer Job provides
hard process/CPU/memory containment, not a security sandbox or filesystem quota.
The returned untrusted session has the existing producer-compatible fields.
For s measured segments, the recorded later production graph is
s segment + s lift + (s-1) join + 1 resolve + 1 finish = **3s+1 calls**.
This reports actual execution geometry, not production affordability, full-cost
growth, a controlled old/new speedup or a new certificate. Any later proving
decision needs fresh selection; failure preserves evidence and stops.
