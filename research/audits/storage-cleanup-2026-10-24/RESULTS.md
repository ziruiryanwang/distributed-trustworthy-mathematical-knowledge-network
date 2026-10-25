# Cleanup complete; v5 work resumed

2026-10-24 Chicago. The user's requested temporary maintenance is complete.
The full deployable-v5 goal remains active and unfinished.

## Removed, with exact recovery copies retained

| Extraction removed | Files | Logical bytes |
|---|---:|---:|
| `product-local/certified-v3-package-01/app` | 13,004 | 2,444,576,373 |
| `product-local/certified-v4-package-01/app` | 13,004 | 2,444,835,804 |
| **Total** | **26,008** | **4,889,412,177 (4.55 GiB)** |

Only these two exact historical software extraction trees were removed. Both
were fully compared to their ZIP payloads before removal. The later guard
revalidated four original archive hashes, four original file-manifest hashes,
complete local file sets/lengths, unchanged pre-verification timestamps,
nonredirected paths and no observed running executable under either target.
Research writers stayed held throughout. See the precise nonadversarial
filesystem assumptions and interrupted final-report boundary in
[INTERRUPTED-VERIFICATION.md](INTERRUPTED-VERIFICATION.md) and [REVIEW.md](REVIEW.md).

`Prune-VerifiedPackages.ps1` exited zero. Its flushed intent/result records and
`PRUNE-RESULT.json` record both removals. Root then confirmed both exact app
paths absent and their recovery files retained. Observed E: free bytes increased
from 49,161,949,184 immediately before the operation to 54,079,934,464 afterward;
that whole-volume delta includes cluster accounting and unrelated activity, so
the exact claim above is removed logical payload, not exact physical recovery.

## Preserved

All ZIPs, package manifests, source, Git history, mathematical state, proof
artifacts, failed/successful experiment evidence, required build inputs and
current runtimes remain. The old Lean extraction also remains: its comparison
did not produce a complete observed outcome, so it was not removed or retried.
Do not infer that a `target` or ignored directory is expendable; some are pinned
later inputs, as CACHE-REVIEW documents.

Current ordinary package PROFILE remains `9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4`;
new cut support remains `8c82b587fe81c6da4021d30b67206d967a0ff0f8a953d1f6e6d7441ea51b0028`;
the current finite runner remains `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
These actual post-cleanup hash checks cover the next selected work's principal
bindings, not every file in the entire project. The canonical Lean runtime and
v4-library supervisor are still present and were outside every removal target.

## Recovery and next work

Both removed extractions can be restored byte-for-byte from their two adjacent
ZIPs, without compilation or network access. Follow [RECOVERY.md](RECOVERY.md).
Historical guide links into those `app` paths are unavailable until restoration;
their original sealed guides/reports were intentionally not rewritten.

At-hand build/control work was committed as `9bf5b00`: minimal support build and
all 42 corrected native-free controls passed scoped independent audits; original
failure remains preserved. No mathematical speedup or v5 completion follows.

Resume the saved nine-worker comparison **source review and full-cost attribution**,
not a new research mechanism. Runtime still requires its own complete reviewed
selection. Ordinary Lean/native batching remain default. Future cleanup should
prefer proven archived duplicates; retain one recovery archive and only required
live extractions instead of accumulating unused convenience copies indefinitely.
