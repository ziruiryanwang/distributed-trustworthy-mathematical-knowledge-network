# Independent file-only installation source review

2026-10-26. Reviewer: current_acceptance_challenge. Source inspection only; no
selector, assembly, installation opening, native operation or Git action run.
This does not repeat the adopted current-release build audit.

## Disposition and exact inputs

**PASS_FILE_ONLY_ASSEMBLY_SOURCE_CONDITIONAL_ON_ADOPTED_CONTROLS**.
No actual package selection exists at this review. Root must first adopt the
focused control outcome and then inspect the exact resulting package selection.

| File | Bytes | SHA-256 |
|---|---:|---|
| INSTALLATION-PLAN.md | 3408 | d37148b5721a6692b2ff20ffe13ae3921f7bdd421098c74d9112f7570b19de2f |
| assemble.py | 10392 | a7ec0d5393fadb62b17f8cecd9a38c44a1f669828c6d0591a3eec71a956cf064 |
| select_package.py | 8089 | 101b82e8d71661c97f39192a1cebc3719bc9fc556f58ad09fa842eec0e6d52ed |

All three files were read completely and independently hashed. Core successor
and focused-control pins/disposition are in REVIEW.md. The existing installer,
its exact support binding and the file helper's relevant ordinary-path,
pin/census/JSON/exclusive-write functions were also source-traced.

## Authority and exact delta

The base is the actual adopted
`experiments/v5-local-checks/current-release-build01/distribution/package`, not
an arbitrary software directory. Fixed release/profile/installation pins and
the full 154-file census bind it. The release's prebuilt map is adjusted only
with the two actual rebuilt exporter pins from the pinned profile and that
profile's own hash, reproducing the previously adopted actual-build delta.

The operation does not compile or execute Lean. It snapshots the unchanged
existing installer plus its six old support modules, checks their actual old
manifest pins and import origins, and gives that installer a real assembly plan
whose only changed installed payload is `py/ordinary_admission.py`. The tested
new baseline intake is copied into the auxiliary package role separately.
External runtime attachments remain pinned and external.

The pinned installer's implementation descriptor and support-group algorithm
compute the new controller-support digest. The assembler checks the generated
manifest's exact file map, roles, compiled directories and support groups,
requires controller_support to be the only changed implementation field, and
requires a genuinely different implementation identity. It does not manufacture
an old ID or migrate old protected roots.

The expected output has exactly 154 files with exactly these four differences:

- installation/py/ordinary_admission.py;
- reference/baseline_intake.py;
- installation/INSTALLATION.json;
- PROFILE.json.

All other 150 files must remain byte-identical. This includes native semantics,
source, executable/object support and public entrypoints. PROFILE is written
last after copy/readback/census and input rechecks. The final receipt explicitly
says ASSEMBLED_NOT_ADOPTED and makes no acceptance/migration claim. Output is
restricted to the one fresh parse-reuse-package01/distribution allocation;
partial failures are retained rather than overwriting the delivered package.

## Selector and bounded execution design

The selector requires the root-supplied adopted controls RESULT hash, reads its
bound selection, checks closed/zero/clean outer outcome and empty stderr, and
requires the inner result to agree with stdout, report the focused PASS, record
zero forbidden calls and deny mathematical acceptance. It binds both successor
hashes to the actual tested selection. Root's independent outcome adoption is
still required; the selector's syntactic PASS checks are not a replacement for
reviewing all eleven groups.

The exact prospective selection contains fourteen source snapshots and 183
external pins: the 154-file base package, release descriptor, 23 runtime files,
and five saved control files (outer result, selection, stderr, inner result,
stdout). It pins the existing runner, checks ordinary/fresh paths and complete
base census, and rechecks selected inputs before an exclusive write. It only
writes a selection; it does not launch assembly or touch protected owner state.

Proposed outer envelope: 180 wall / 90 inclusive Job CPU seconds, 768 MiB, one
process, 1 MiB per log. Inner assembly: 150 wall / 70 CPU. These are one finite
file-copy/hash/manifest operation, not native allowance or permission to retry.
The existing installer itself retains its deadline and readback checks.

## Required actual review and remaining hold

After a root-selected execution, inspect all exact output pins/census, the
four-file delta, generated descriptor/implementation, PROFILE coherence,
unchanged source/runtime inputs and actual clean closure. Only then may an
unused public-intake selector be bound to the real new implementation. A fresh
owner must initialize under it; existing protected state is not relabeled.

This package is an internal candidate until separately useful qualification and
coherent fresh distribution integration. No native initialization/intake,
external publication, automatic update, failed-operation renewal or final-v5
claim follows from the assembly-source clearance.
