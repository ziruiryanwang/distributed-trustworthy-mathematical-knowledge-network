# Exact retained-byte restoration: independent saved-outcome audit

2026-10-26. `current_acceptance_challenge`.

**PASS_SELECTED_EXACT_INERT_RECONSTRUCTION.** All 2,651 manifest-selected
preimages now exist with their exact committed lengths, raw hashes and V2
UnitIDs. This is complete inert input restoration, not mathematical acceptance.
The native initialization/intake HOLD remains independently in force.

## Selected operation and terminal evidence

Run: `experiments/v5-local-checks/std-reconstruct01`.
Selection SHA-256:
`a8569b15b1805b434fde7e1906fba821ad8363042bee3e66b001b22e5dc114a1`.
The actual selected command executes the reviewed snapshotted reconstructor
`244f1e17...`, with no binder or native worker call. All eleven external pins
and five actual source snapshots independently rehash unchanged.

The outer report has exit zero and `COMMAND_EXITED_ZERO_AND_CLOSED`, direct
child reaped, Job closed, zero final active/terminated processes, no cleanup
errors or termination request, and empty stderr. Successful terminal stdout is
`RESTORED_EXACT_INERT_BASELINE_NOT_ACCEPTED`, not the prepared-metadata status.

| Observation | Actual value |
|---|---:|
| Whole operation wall seconds | 89.49237350001931 |
| Inclusive Job CPU seconds | 42.609375 |
| Separate outer wrapper CPU seconds | 0.84375 |
| Total known CPU seconds | 43.453125 |
| Peak Job private commit bytes | 599,363,584 |
| Inner complete operation wall / CPU seconds | 88.41152090020478 / 42.09375 |

The inner measurement is included in the Job charge, not added again. Original
inner 90-wall / 70-CPU and outer 120-wall / 90-CPU / 1,792-MiB / one-active-process
limits were unchanged. Completion was close to the inner wall limit; this is
one successful operation, not a robust runtime bound or capacity prediction.

## Complete independent byte census

The restored bundle is
`experiments/v5-local-checks/std-reconstruct01/materialized`.
This audit read **every restored unit**, independently recomputed both its raw
SHA-256 and `SHA256(V2-domain || NUL || raw)`, and compared its actual length
against the adopted manifest. All match. The exact directory census contains
2,651 unique ordinary unit files and no unexpected unit/root entry.

| Batch | Units | Exact portable bytes |
|---|---:|---:|
| 1 | 1,024 | 9,997,243 |
| 2 | 1,024 | 17,147,916 |
| 3 | 603 | 17,767,684 |
| Total | 2,651 | 44,912,843 |

The only additional files are the unchanged **468,097-byte** manifest and
**1,862-byte** `RECONSTRUCTION.json`: **2,653 files / 45,382,802 bytes** total,
matching the successful stdout census. Both metadata lengths and hashes match
the terminal report. The report is intentionally
`PREPARED_FOR_MANIFEST_NOT_COMPLETION`; the subsequent successful final census
and outer terminal result, not that label alone, close this operation.

Independently compared all **708 retained old partials byte-for-byte** against
their corresponding reconstructed files. All are identical. The old aggregate
identity remains the one independently checked in MATERIALIZE-OUTCOME; no old
file or failure was overwritten. The original `Std.HashMap.isEmpty_insert`
target is present at UnitID
`ab6f1b22d8760ba5615e9ec7e5a1fda99313c71a8cab34183c2fe88aad31381c`.
The exact target row in the saved report retains ExportID
`bf281176862c75a7c8be1d00359f85bdcfe4904f4aefd5977c954e822e79070c`.
This is object correspondence, not fresh checking of its theorem.

## Saved identities

| File | SHA-256 |
|---|---|
| `RESULT.json` | `0794e33b94b5c6b56e5d3669939996c5c8d9d347caa60b83f322cacfb723b48c` |
| `command/stdout.txt` | `78bb6ae4f9e8ca70e8b0d475447e10fb6fb08ea78338fe5f17528d9ce24019de` |
| `materialized/manifest.json` | `1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c` |
| `materialized/RECONSTRUCTION.json` | `b0c1c18930e02097a85531be048442443a193de9b7847280d886272bdc50889b` |

The unchanged manifest is the exact previously adopted one, not a newly generated
claim. Cryptographic object binding has the assumptions set out in
RECONSTRUCT-REVIEW. The receiver must still perform its independent strict
admission/native checking; these hashes are not mathematical authority.

## Cost and decision boundary

The failed preceding materialization's 71.328125 known CPU seconds remain charged.
These two input-preparation attempts total **114.78125 known CPU seconds**; this
does not include the earlier diagnostic/public-export or later review work.
Do not compare the successful restoration's whole time to the earlier binder's
isolated timing as a measured speedup. The successful route does materially
complete the missing exact bundle without a new native extraction or cap increase.

Root may adopt that exact inert boundary. It does not lift the separate intake
cost HOLD, authorize initializing a mathematical owner, or establish rich-library
acceptance, growth acceleration, public deployment or full v5 completion. Any
public-selector successor must bind these actual reports and new run rather
than relabel failed `std-materialize01`.

This reviewer performed only saved-file reads, byte comparisons and hashes.
A first in-memory hashing check encountered a local .NET hash-provider error;
the completed check used the managed SHA-256 implementation. Neither check
changed any file or reran the reconstruction. No product command, native worker,
owner-state operation or network request was invoked.
