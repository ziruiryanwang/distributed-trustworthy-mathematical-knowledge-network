# Typed guest: assembly audit and next-selector review

2026-10-21, adaptive_audit. **PASS for the actual image assembly; PASS for the
exact source-only frontier selector below.** Root reported the selected assembly
terminal exit0 before this audit. No assembly, selector, guest or proof was run
by the reviewer. Root retains adoption and fresh execution selection.

## Actual assembly

Evidence: `experiments/v5-local-checks/typed-guest-image-assembly-01`.

| Item | Exact binding |
|---|---|
| Outer selection | `d911dbfd934b5e43c2743403076afd47794185a593f225582f1bfb73ab025362` |
| Outer `RESULT.json` | `174878e768ed578e0a4f239de8423591ebf4ea34f09213e52c84aff46362b33b` |
| Inner `assembly/RESULT.json` | `4c26d075d850ff38a0922dbbdfad00303d16b49dee41f71a859f3777166e530c` |
| Actual image ID A′ | `9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865` |
| Image bytes / file SHA-256 |1868700 / `0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46` |

Independently rehashed all three outer sources and their snapshots,89 runtime
pins,70 inner selected inputs, built-artifact records, image and logs. The four
saved actual compiler-command records also equal the already adopted build
result. The assembly consumes that exact build result `b1b4f7a8`, its ELF
`eb66a3aa`, the retained assembler executable and selected v1compat kernel.
The build's absent finalization marker remains absent.

The outer actual argv equals the selected argv after both documented snapshot
and output substitutions. The one inner command is the pinned executable's
`assemble` operation on that ELF/kernel and the fresh image path, with60s timeout.
Its103-byte stdout reports the image ID and exact byte length above; stderr is
empty. The emitted ID is not the image file hash. The outer stdout decodes to
the inner report exactly. No RISC0 environment override is forwarded by the
reviewed adapter. One assembly, zero guest executions/proofs/admissions.

The enclosing Job exits0, reaps its child, closes, and reports zero active or
terminated processes, no cleanup errors and no termination request. Worker Job
CPU0.71875s plus wrapper CPU0.40625s gives known disjoint1.125s. The reported outer
wall is1.3019975000061095s; command wall through cleanup is1.1822093003429472s.
The0.015625s supervision CPU is already inside wrapper CPU, not an additional
charge. Peak Job private commit29298688B. These fit original120CPU/120wall/
1024MiB/two-active-process limits. Four cumulative processes do not imply four
concurrently active processes. Final outer report/exit tail is not included in
its pre-report timing; normal terminal completion is separately reported.

This supports adoption of the exact assembled A′, not its mathematical use,
execution cost or a certificate. Earlier build accounting limitations remain.

## Source-only frontier selector

Reviewed completely:
`research/cycles/v5-2026-10-20/Select-TypedFrontier01.ps1`,6620B,
SHA `5db4e2a24af422ad7e66ffb8a0e4684dd1232c0e97af24744c7eef37df987202`.
Also read the unchanged `frontier_snapshot.py`, its prior exact configuration,
selection and relevant image/host binding. All ten retained source pins and36
retained runtime pins still match; no product module was imported.

The selector requires fresh configuration/selection/output, exact canonical cwd,
the adopted assembly result/outer hashes, successful clean outer closure and
exact new image bytes. It requires A′ to differ from the old aggregate image.
It preserves all10 adapter/source entries and the original180CPU/240wall/
3072MiB/three-process wrapper limits. It removes exactly four obsolete runtime
bindings, retains32, adds the three new image records, two historical selection/
configuration records, two exact comparison files and new configuration:40 pins.
Only the fresh image result/hash, image ID, output, run name and configuration
argv binding change. It writes create-new and launches nothing.

The unchanged adapter derives BASE+FIRST from exact retained journals and
FIRST witness, leaving SECOND downstream. It retains the genuine I receipt,
derives a new A′-bound header/wire and makes one fresh snapshot call. Old header/
wire pins are comparison data, not transferred proof authority. No old image
is relabeled as the new one, and no old execution capsule is resumed.

**Two separate thresholds remain explicit:** the unchanged execution adapter
allows1..256 segments at po2=18 under its2^26-cycle envelope; the adopted economic
screen remains **at most128 segments**. The selector's reported128 is not an
adapter enforcement mechanism. Root must apply the128 threshold to the actual
result before considering proof funding; a raw execution PASS at129..256 would
fail that economic screen. Neither threshold authorizes proof production or
ensures the proof tail fits its prospective allowance.

No blocking defect found for this finite exact-target execution preparation.
After root adoption, a distinct launch record must select one invocation.
Its actual target equality, new A′ binding, segment count, costs and closure need
independent audit before any proof decision. No rerun, budget expansion,
distribution copy or claim of v5 completion follows from this review.
