# Support guest: actual image assembly outcome

2026-10-21, support_guest. **PASS for the one selected actual image assembly.**
This agent authored the builder, not the assembler. The separate actual build
audit by core_release is reused; this audit inspected assembly inputs, actual
command/output bindings and clean closure without rerunning any operation or
rehashing the old compiler/dependency tree.

Run: `experiments/v5-local-checks/restricted-support-guest-image-assembly-01`.

| Record | Bytes | SHA-256 |
|---|---:|---|
| Original and saved selection | 17916 | `b6b39fe375356c0b47051aafcfb3e85a227e8799482cdd339f3720764eede51a` |
| Outer RESULT | 2322 | `d1da6dfbfdc5ca31f2aeb70b58edb1013a62a678b17979c328cdaf192bce3e88` |
| Inner assembly/RESULT | 1818 | `6ae8d697fbe94dae9926d2ba77386031e7dffa3b18e2f167d53684df784d9b66` |
| assembly/COMMAND | 12793 | `5fb1c720c8915049aecea9c6fb2364b75d7857e56cc46fb0f5966239b3676ed3` |
| Outer command record | 976 | `3a5bc2250c7d45d369f1fd0b65bacf958291536ecd341b9a5308088c677c7c5d` |
| Outer command stdout | 1874 | `efce996c4eeb498743fe2edb875c607aa8640f9acfe0af622bc073c97b6240ac` |

All 45 assembly COMMAND input pins and 64 outer selection runtime pins match
the actual files. The three selected sources match both canonical and snapshot
bytes; the snapshot contains exactly those three files. They include the reviewed
new assembler `e9084fd4...` and frozen helper `220f54cf...`. Original and saved
selection bytes are identical. The adopted build RESULT is exactly
`d90dcb854b01f407c067c6eec6cc29c6f98cc54291896c2afe79cadbb3534e10`, with
ARTIFACT `f32af5d89e30133d131573991156591ba6130796cba6ca2f2ca5e1087ad41a04`.
The assembly command binds that actual selected ELF and kernel:

| Actual artifact | Bytes | SHA-256 |
|---|---:|---|
| User guest ELF | 627224 | `0e6a4c356817dc640a157b592d5ead8868b6ef5d3cb8c388d08d3f4580c5909a` |
| Retained kernel ELF | 58736 | `9dd8af014a24db3752b9beda71c837f553ff361fc1bca83cc79584bd38ac9de5` |
| New aggregate image | 685992 | `cb32fe6a93c6127b5bc7bd7c86187ec085db8040cbf0e6ecd615bbee1daed66c` |
| Assembler stdout | 102 | `b777d5820af95854de98a3518346a9d20c1a2d3aad23b6a82c9c48ec4f11754c` |

The retained pinned assembler executable (`e1d87ff0...`, 66679296 bytes) was
called with `assemble`, the exact new ELF, the retained kernel and the fresh
image output. Its 60-second command timeout remains inside the selected outer
120-second/120-CPU/1024-MiB/two-active-process envelope. The actual stdout says:

```text
COMBINED_IMAGE image_id=ae765f5bb55fdf2b2d95aa28aa70c741b77142d3b1af4f90c89cc648f5a260bf bytes=685992
```

This is the actual assembler-derived image ID, not the image-file SHA-256.
The saved inner report and printed outer stdout agree on the result and image.
Both assembler and outer stderr are empty. All reported image/log byte counts
and hashes match disk. No overriding build or outer finalization marker exists.

The inner schema is `DMKN_V5_RC_SUPPORT_GUEST_IMAGE_ASSEMBLY_RESULT_V1`, with
`PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY`, one assembler call, exit 0, zero guest
executions/proof calls and mathematical_admission false. The outer report is
`COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0, direct child reaped, Job closed,
termination not requested and no cleanup errors; final active/terminated counts
are 0/0. Cumulative process count four is not concurrency. Peak Job private
commit is 25452544 bytes.

Known CPU is **0.96875 seconds**: inclusive worker Job 0.609375 plus disjoint
wrapper 0.359375. Wrapper-supervision CPU is 0; it is not added again. Outer
wall is **1.1338457996025681 seconds** (worker through cleanup 1.0534647996537387).
This is assembly evidence only. It establishes no guest execution, certificate,
row/CPU screen success, installed adoption, growth advantage or v5 release.
No compiler, assembler, guest or project adapter was executed by this audit.
