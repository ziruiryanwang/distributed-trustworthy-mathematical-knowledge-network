# Independent audit: retained v5 base-module production

Date: 2026-10-12, America/Chicago. Reviewer: `v5_base_actual_audit`.

## Disposition

**PASS for the recorded base-receipt production and exact retained artifacts.**
The previously backgrounded operation reached its 325th selected stage, wrote a
223,594-byte receipt and saved `PASS_FINISHED_RECEIPT_ARTIFACT`. This is materially
stronger than the October 8 guide's earlier, unexamined background-run status.

**Not fresh receiving-node admission or v5 release completion.** This audit used
read-only filesystem inspection, SHA-256 hashing, JSON comparison, checkpoint
header decoding and source review. It did not invoke a prover, verifier, Lean,
guest execution, service or admission controller. Saved success documents are not
mathematical authority. A fresh receiver must independently verify the receipt
and bind its exact module before creating a private live admission handle.

There is no artifact-integrity or per-stage-closure blocker to retaining this
receipt and selecting that separate future receiving operation. No such operation
is selected by this note. The writing task returns to the requested pause.

## Evidence identity

All paths below are relative to the sole canonical project root,
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

The terminal directory is `experiments/v5-local-checks/module-base-production-01`.
Its final result is 169,817 bytes, SHA-256
`1ccfa4835ce7cf8ef62386bd2fc82a548d7e9b82db948a879ab9809f36027749`.
The final file's observed last-write time is October 8, 06:37:24 UTC
(01:37:24 Chicago); this filesystem timestamp is not a substitute for a process
exit observation.

| Item | SHA-256 |
|---|---|
| Original CLI profile | `406fb0453b114315339d2e5e54af785cacd0b032a5856004fe0ebd407421c6fb` |
| Original CLI request | `33c4947f60ccc3abec2a309d0c68882136211a2f016eebe33ae19af6af59c76a` |
| Saved canonical profile | `71af83f7c4822d8d2a322e93dda5f08a59311614d434ab887cc5c33c318d84d0` |
| Saved canonical request | `ca3095c72e0d6fb65f22511e9bc6924a59f670d866fb7b8513b5949d414ce5df` |
| Finish-stage result | `92d512263798888b11c883a92494c61cdc9bb93740cfd230da1bef4349656b9f` |
| Receipt, `finish-0/receipt.bin` | `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47` |

Original CLI documents are the sibling files
`module-base-production-01-profile.json` and
`module-base-production-01-request.json`. Their raw hashes differ from the saved
copies because the producer serializes canonical JSON. A recursive comparison
verified identical objects, including array order, with JSON object member order
ignored. Both raw input pins and both saved-control pins match their respective
expected bytes; this is not evidence of a changed request.

Allowance: `6e23ea7e9fa04070afc2fb33f9a5f5953918bcaad6a74b7eb4243bb6229f6a89`.
Session: `9a5ce7de0eef351a7eb886c930e0910e08f2b2d0cf5f07f9a250f24e5957e3ed`.
Capsule binding: `4608ca4e3c12d338a86813afa96dbf418a1076eca79b2a8ab2838bb78135d925`.

## Complete stage and binding audit

The independent reconstruction starts with the five selected retained keys:
`segment:0`, `lift:0`, `segment:1`, `lift:1`, `join:1`.
For each index 2 through 109, it requires `segment:i`, `lift:i`, `join:i`, in that
order; then `finish:0`. This gives exactly 108 + 108 + 108 + 1 = 325 new calls.
There is no repeated old stage, `snapshot`, `execute` or `resolve` call.
The original capsule contains 110 segments and zero assumptions/parents.

Checks performed across the entire selection, not a sample:

- All 325 result length/hash pins, statuses, stage identities and ordering match.
- Every reservation has the selected session and allowance identities. Its
  deterministic host argv matches both the embedded process report and saved
  `command.json` request; cwd and limits also match. `command.json` is an initial
  command request, not a second terminal report.
- Every lift consumes its corresponding segment; every new join consumes the
  preceding join plus corresponding lift. Finish consumes all 110 segment
  checkpoints and `join:109`. Dependency paths, sizes and hashes agree with the
  evolving inventory. No missing, extra or reordered dependency is accepted.
- All 329 final retained checkpoint files match their pins and independent
  schema-5 envelope decoding: capsule binding, exact kind/index and total payload
  length. The inventory is exactly the original five plus 324 new checkpoints.
- The receipt size/hash matches both final and finish-stage reports. All 325
  stdout lines match their exact stage-specific markers. Both logs for each stage
  have the lengths reported by that stage and remain below the selected caps.
- All 22 profile pins match current files: host, Python executable/DLL, release
  manifest, 16 further runtime DLL/PYD files and two producer sources. The three
  supervisor/helper source pins selected through that exact manifest also match.
- All four session inputs match: image, frame, expected journal and capsule.
  Both saved control documents and the final receipt are checked independently.
- All selected host-source snapshot files that are present match the retained
  build selection. The actual host executable matches
  `74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9`;
  the finish/verification source matches `1e30b0f2...`. This reuses the retained
  build/source assurance; it is not a new reproducible-build qualification.

The earlier segment0 and prefix result hashes remain respectively
`6212efa399c55e6032e78889e1180e578f015060bb128b58c9830be499fed066`
and `fb61eb62eb75a1c40694a4b5ab12c650c39cdb4738153b356591eb895672afee`.
Their already-reviewed costs agree with the carried subtotal. This audit does
not redo their former runtime campaigns.

## What finish actually records

The selected host's finish branch checks the complete segment composite,
checks both composite and succinct claim digests against the exact capsule
claim, constructs the receipt with the selected expected journal, then calls
`checked_receipt` before writing the file. That function permits only real
succinct Poseidon2 receipts, uses a non-dev verifier context and invokes full
application verification for the selected image, not integrity-only checking.
It then validates the adopted image/foundation/policy. Finish again requires
exact journal equality before writing and emitting its marker.

The actual finish report records clean zero exit and the matching marker:
rank 0, 11 groups, 223,594 receipt bytes, zero parents, 110 segments and the exact
capsule binding. Stderr records the crypto and written phases, with no failure.
The pinned 184-byte journal identifies:

- Image: `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
- Foundation: `d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481`.
- Policy: `5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377`.
- Module: `2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.

Exact journal bytes occur within the retained receipt; that byte observation is
only an additional binding consistency check, not receipt deserialization or
cryptographic verification. The source-and-runtime evidence supports *recorded
full host verification during production*. Fresh independent verification of the
retained artifact remains unperformed by this audit.

## Costs, limits and closure

| New operation stage | Calls | Worker CPU seconds | Summed stage wall seconds |
|---|---:|---:|---:|
| Segment | 108 | 90,118.328125 | 8,966.991920 |
| Lift | 108 | 17,937.296875 | 1,540.212126 |
| Join | 108 | 18,046.015625 | 1,579.272186 |
| Finish | 1 | 3.984375 | 4.690200 |
| Total | 325 | 126,105.625 | 12,091.166431 |

The sum independently equals the final worker charge. Final controller CPU is
688.375 seconds and whole-operation active wall is 12,767.42750380002 seconds,
about 3 h 32 min 47 s. Limits are respectively 150,000 worker CPU, 900 controller
CPU and 14,400 active wall seconds. Nested stage-supervision CPU is 50.125 seconds
and is already inside the controller measurement; do not add it twice.

All stages report zero child exit, direct reaping, a closed Job, zero active and
terminated processes, no termination request and no cleanup errors. Every
stage's worker CPU and measured wall are below its selected limits. Maximum
worker CPU / wall observations are 973.03125 / 129.914068 for a segment,
187.359375 / 22.134364 for a lift and 199.59375 / 23.679400 for a join. Finish is
3.984375 / 4.690200. These satisfy 1500/300, 250/120 and 30/120 stage caps.
Peak Job private commit is 3,534,692,352 bytes, below 4096 MiB; maximum reported
total processes is two. Every reservation, process and result agrees on these
configured limits.

Current complete output census is 76,005,362 bytes across 2,603 entries, below
1 GiB / 4,096 entries; no reparse point or failure-override file is present.
The census is a current observation, not a reconstruction of every peak. Output
and some process limits are sampled, not hard filesystem quotas.

Adding only the explicitly carried segment0/prefix subtotal gives
127,958.078125 worker CPU seconds, 691.15625 controller CPU seconds and
12,943.591426400235 summed active wall seconds. These are **not total project or
full mathematical-workflow costs**: source preparation, builds, failed snapshots,
tests and other historical work remain excluded rather than assigned zero.
Startup, exit and post-observation/report tails are also excluded from these
measurements. No useful-growth advantage follows from these production totals.

## Original parent handle limitation and safe handoff

The root reported the old unified session71174 unavailable and PID18132 absent;
this reviewer independently observed PID18132 absent. No current worker is
claimed. A missing handle does not recover the original parent's exit status:
this audit has no freshly observed original-controller exit/reap event. All 325
child-stage closure reports are available and consistent, and no
`FINALIZATION-FAILED.json` overrides the terminal report. Those facts must not be
expanded into a claim that the original parent's final exit was observed, or that
every unmeasured tail was charged. The producer writes its result before its final
census/history/return steps, so an absent failure marker alone cannot prove those
last parent steps completed.

This does not erase the independently bound, already written finish artifact.
On a future authorized resumption, verify it through the actual receiving API
under a fresh finite allowance; do not replay production merely because the old
session handle is gone. Then ordinary-source reuse and child certification,
network distribution, full-cost growth and release readiness remain separate
central obligations. This audit changed no software, evidence, allocations or
Git state. Only this checkpoint was written; reviewer work is complete.
