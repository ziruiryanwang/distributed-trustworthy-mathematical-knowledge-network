# Combined managed-observed distribution: actual audit

2026-10-21, support_guest. **PASS_SELECTED_COMBINED_127_DIRECTORY_BUILD.**
Root reported session50011 terminal0 before this audit inspected the output.
The selected directory contains exactly the two reviewed replacements and passes
the saved full-verification/closure boundary. Root owns adoption after the
separate control audits; this is not public contribution02 or actual closure.

## Exact evidence

Installation: `product-local/v5-distribution-managed-observed-01/Mathematical Commons v5`.
Evidence: `experiments/v5-local-checks/distribution-managed-observed-build-01`.
Input: `experiments/v5-local-checks/distribution-managed-observed-01-input.json`,
SHA-256 `e0f0dc5d63dee0d088b8edd9e61d9a1d1bebbe31d3dde76b53887d1c901f7201`.

| File | Bytes | SHA-256 |
|---|---:|---|
| Installed `V5-RELEASE.json` | 2370190 | `7381fa03ba8d02017b3f96ff589eca468cdba8c2aa9c4b0a4c1ca4ad968dc344` |
| `RESULT.json` | 2258 | `980e29165332186faa0940aa5cfc12efd1f4e26db68e643d8639b2473a78b260` |
| Retained/original selection | 8542 | `c3257f270ca3b45bfa5a5c7f88798112dac49d9aaea378913ec1df9f98e3b3f6` |
| `command/command.json` | 910 | `f17afde9670e7b6955a37920c8b67c546a1d8d2dd6c6d9ab0315a81e01ec1671` |
| `command/stdout.txt` | 357 | `aff94d5ff1fef0bc5a8833ea54c025dfd98d0e30a6aa9fcf58424ed5a241631c` |
| `command/stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

These hashes, the input and adopted predecessor input/release were independently
checked. Complete command/stdout/stderr/outer result were read. The read-only
audit script `Audit-ManagedObservedDistribution01.ps1`,10688 bytes/SHA-256
`da2ebf9c4319fb6c23700b23fdd0d59ec3476dc0437075e1aac036ec28b2acfb`,
ran once and returned `PASS_READ_ONLY_SAVED_BUILD_EVIDENCE`/exit0. No product
import, verifier/build rerun, credential access or live-process inspection.

## Exact changed boundary and verification reuse

Comparison with adopted input33bd99d7 confirms127 SDK rows,125 complete original
path/length/digest rows unchanged, no addition/removal and exactly two replacements:

| Logical source | Previous | Selected bytes | Selected SHA-256 |
|---|---|---:|---|
| `v5/client/managed_owner.py` | 26492 bytes,75c0e8a9 | 31626 | `1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503` |
| `v5/client/serve_placement.py` | 22670 bytes,7e735337 | 24566 | `c815331f035618b36f504d604a1fb75d8682439f0488453c72e9801a63d78bd8` |

All non-SDK input fields and top-level field names are unchanged. All127 SDK
manifest mappings are exactly `sdk/<logical>` with selected lengths/digests.
All106 preparation rows exactly equal the selected v5 Python subset, including
names/lengths/digests and no duplicate/missing/additional row. Both changed source
originals and their installed copies were independently hashed, as was the small
installed builder. The new manifest binds the selected input and unchanged base
manifesta93714ec.

Manifest-only comparison against adopted release2cb30fae finds9870 payload rows
unchanged and exactly the two SDK rows above changed. File count stays9872;
payload bytes are842694113, an increase of7030 =5134 owner +1896 service bytes.
These independently calculated totals match the sole terminal builder object,
`DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`, with exact installation/release identity
and mathematical_acceptance=false.

Runner44a7bf1b and buildereb1348f6 originals/snapshots match their selected pins;
all29 runtime/input pins were independently rehashed. The unchanged builder
path was rechecked: manifest save precedes `verify_release(..., full=True)` and
success output follows it. That path revalidates manifest, exact on-disk census,
all payload lengths/hashes and base-role projection. Reuse this completed full
verification and prior MANAGED-CONTRIBUTION-DISTRIBUTION-OUTCOME boundary audit.
No second842MB payload sweep, directory comparison or product verifier was run.
Explicit runtime pins remain a finite binding, not a hermetic-toolchain claim.

## Closure and cost

Selection, command and result agree on canonical cwd, isolated `-I -S -B`,
snapshot builder, new input/hash/output and all six limits:120CPU seconds,
600wall seconds,128MiB,two active processes and1MiB per log. Actual status is
`COMMAND_EXITED_ZERO_AND_CLOSED`, exit0, direct child reaped, active0, Job closed,
termination_requested=false, terminated_processes0 and no cleanup errors.
Saved cumulative total_processes is2. Build stderr is empty; this does not erase
the separately preserved close-control warnings.

Job CPU61.4375 seconds =33.34375 user +28.09375 kernel; wrapper CPU1.578125:
**63.015625 known CPU seconds**. Nested supervision1.234375 is inside the wrapper
and is not added again. Outer wall327.9588742996566 seconds; command-through-
cleanup327.8242807998322; peak Job private commit57360384 bytes. Log lengths
357 stdout/0 stderr match saved observations. All are within the selected
envelope; sampled wall/total-CPU/log enforcement is not a hard disk bound.

Accept only the file-only combined127/106 candidate. No real service, token,
contribution02, downstream reuse, native/proof/verifier qualification, storage
guarantee, independent host, migration or final-v5 claim follows. Prior failures,
private credentials, installations and all used source/input/evidence remain
preserved. Root owns any separately selected public operation.
