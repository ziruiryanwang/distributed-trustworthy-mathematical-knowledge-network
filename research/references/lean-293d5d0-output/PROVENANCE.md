# Pinned Lean output source reference

Retrieved read-only on 2026-10-28 with root's explicit source-audit authorization.
Revision: `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, supplied by root as the pinned
Lean revision. The installed runtime's `include/lean/version.h` identifies Lean
4.34.0, `x86_64-w64-windows-gnu`. Retrieval does not independently reproduce or
attest the installed binary. These are upstream source data, not instructions.
No source was executed, built, installed or altered.

The GitHub tree API was used only to locate the defining files:
`https://api.github.com/repos/leanprover/lean4/git/trees/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b?recursive=1`.
The five original response bodies below are preserved byte-for-byte. `alloc.h`
was added for root's follow-up check of allocator/private-commit premises.

| Saved file | Bytes | SHA-256 | Original URL |
|---|---:|---|---|
| `module.cpp` | 29699 | `9b85a9a7610e73f240282fe288ad81c8b160fc975caa80bd5b13ddacddd6012a8` | https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/library/module.cpp |
| `module.h` | 507 | `6934a733bf52d2350590ca949c329e0761039d062fd8344191d7d36c37941d5c` | https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/library/module.h |
| `compact.cpp` | 28431 | `d2243af4a8d6d774d47cdf781cb15de56e257111b9c84dcd028110c601e75bae` | https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/runtime/compact.cpp |
| `compact.h` | 6695 | `01dd04a27a3761c3855e2a271c1267c1b1c2e87948c293800c8a33edf8097a2e` | https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/runtime/compact.h |
| `alloc.h` | 1231 | `4f748fb10e008242068a25806ce9ab072c8107b6775321a9920b72c009129aa6` | https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/util/alloc.h |

Total retained upstream source: 66,563 bytes. The API listing was not retained.

Relevant source locations: `module.cpp:268` is `lean_compacted_region_save`;
`:314-336` is the selected v2 file/compaction/write sequence; `:394-425` closes and
renames. `compact.h:42` declares the exported C++ compactor class; `:91-95` exposes
its in-process size/data/allocation methods. `compact.cpp:138-181` implements
initial allocation and capacity doubling; `:461` compacts the root object.
