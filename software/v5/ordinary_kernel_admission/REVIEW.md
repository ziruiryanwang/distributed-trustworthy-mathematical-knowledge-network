# Independent actual-source review

Disposition: **PASS_SOURCE_REVIEW; NO BUILD, TEST OR ADOPTION CLAIM**.

The reviewer read the complete three successors and their actual installed
predecessors, CONTRACT and DESIGN, and the relevant checked-addition/import
definitions in Lean 4.34.0. Reads and file hashing only: no product import,
compiler, native command, owner/status/recovery call, database or Git operation.
The canonical workspace guard passed. This review belongs to the checkpoint
`research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.

| Reviewed successor | Bytes | SHA-256 |
|---|---:|---|
| CheckedExtension.lean | 8,768 | `2d6804ea7fe90daacf8889c0e05a9f5a9d7657d2323a36c6e2df48e18cc9a92e` |
| LocalSnapshot.lean | 11,581 | `ae8bc1c9d2e8e01c293d9757d3ab2db744a6a65c2281c965406bdaba993e0f95` |
| OrdinaryWorkflowWorker.lean | 12,293 | `eaed9462acec910e89591e8d9969a34531e792594ff4f3315503d33d887a8be9` |
| DESIGN.md | 4,830 | `201f98009aae66e9d99c914a8fcf58288982a8305a4a9016d57e09a2081f190c` |

The three predecessor hashes match CONTRACT exactly in
`experiments/v5-local-checks/intake-progress-package01/distribution/package/installation/lean-src`.
No finding requires a source change.

## Acceptance-loop preservation

`checkBatchCore` retains the prior loop and ordering: unit/finite-kernel limits,
initialized-parent premise, bounded stage-two census, declaration policy, exact
name and overwrite checks, declared inventory inclusion, closed grounded
references with aggregate scan accounting, checked addition, complete actual
generated-row comparison/safety, and final census/no-unadvertised-name checks.
The limit constants and failure conditions are unchanged. Successful prefixes
remain local until the complete batch returns.

The only abstractions are the kernel projection and addition operation, passed
by two fixed wrappers. The existing `checkBatch` passes `env.toKernelEnv` and
`Environment.addDeclCore ... (doCheck := true)`; its argument/result types and
actual frontend environment remain intact. The native wrapper passes identity
and `Kernel.Environment.addDeclCore`, whose installed declaration explicitly
type-checks and has no unchecked flag. No peer value chooses a callback or mode.
The generic state and loop are private implementation details, not a security
sandbox or substitutes for the existing trusted-parent/controller premises.

Lean's frontend addition also registers normalized names in its async maps;
the kernel API avoids that frontend bookkeeping while retaining exact kernel
checking. This is the intended difference, not mathematical acceptance based
on normalization. No `Environment.ofKernelEnv`, renaming, new axiom, unchecked
addition or stderr suppression was introduced.

## Persistence and routing

The private `writeCheckedRecords` is the original writer factored over the
actual checked environment, records and unit count. Both callers obtain those
arguments immediately from their fixed checked entrypoint. Module/path/freshness,
initialized-profile, bounds, safety and duplicate checks remain. Serialized
`ModuleData` still uses precisely the ordered actual records/full names, one
parent import, `isModule=false`, and empty extra names/extension entries.
The existing `WrittenExtension` API is preserved; the native result is separately
kernel-typed. The restoration suffix from `importArtifacts` through `restoreLocal`
is exactly equal to the predecessor, including metadata checks and private import
with no plugins or loaded extensions.

The entire worker difference is its `extend` call to `checkAndWriteKernelChunk`
with `parent.toKernelEnv`. Its protected restore, decoding, reference allowance,
caps, output/report flow, basis initialization and export behavior are unchanged.
Only chunk metadata is consumed afterward. General authoring/reference APIs
retain their frontend route and real environment metadata.

## Remaining evidence and boundaries

Review focused controls before root selects execution: distinct full private
names with the same normalized suffix, a public/private pair, references to
each exact name, exact duplicate refusal, bad expected/generated inventory,
an actually ill-typed proof, native save/restore/further checked extension, and
the unchanged frontend path. Compilation and control success cannot be inferred
from this source argument. Build and control adapters have separate reviews.

Changed support bytes require a new implementation identity and later explicit
package/state selections. This review neither recovers std-intake02 nor clears a
large intake retry. Native admission compatibility does not establish broad warm
frontend authoring compatibility for multi-origin private names, a growth speedup,
or completion of v5.
