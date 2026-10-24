# Retained package successor: independent source audit

2026-10-24. Reviewer `retained_registration`, independent of the package author.
Root owns runtime selection and Git. This review reads sources and retained
metadata, parses ASTs and hashes three small overlay files. It does not import
the adapter, execute the selector, build a package, open an owner, compile Lean,
run native mathematics or mutate catalog state.

## Disposition

**SOURCE-CLEAR for the bounded file-only successor**, not an executed package or
mathematical/release qualification. No blocking issue was identified in the two
complete sources or the exact retained builder functions they call.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `ordinary_reference_package/assemble02.py` | 13105 | `ad4a10722697308d3749d09465213b3d5ce17735a48980287f5216830c94e2ba` |
| `ordinary_reference_package/select_assembly02.py` | 4380 | `950b038733233158849f99a2d85fa2f706c8e571fab22f98b6d53e54ed6cabb4` |

Both parse with `ast.parse`; they were not imported. Full root is
`E:\Distributed Trustworthy Mathematical Knowledge Network\software\v5`.

## Exact three-overlay map

The independently calculated canonical sorted compact-JSON map digest is:

`da760ed80f258b5922aad2dfddeea8f05810165c3daea603d408be5d65632899`

| Logical package path | Source | Bytes | SHA-256 |
|---|---|---:|---|
| `owner.py` | `ordinary_reference_package/owner02.py` | 38588 | `295fbb25f8f41ebd2b647ce02bb833d60cd039d4056737fbcf9c07ef918bc2f1` |
| `reference/reference_registration.py` | `ordinary_reference/reference_registration02.py` | 16529 | `9225d68660555e93266a7f0d35a067f76dceaad772520e90305b6f4d03782b19` |
| `reference/reference_store.py` | `ordinary_reference/reference_store03.py` | 76686 | `5ad587b779eb0b81958706c3df17f108c330bd618379b4bcd2c289f6a3e6dc9f` |

This reviewer authored store03 and therefore does not claim independent review
of that implementation here. Root and the separately assigned trust reviewer
handle that boundary. This reviewer independently checked root's controller/CLI
diffs in RETAINED-REGISTRATION-CONTINUATION.md and the package author's mapping,
input/copy/commit behavior here.

## Checked package behavior

The base is exact `ordinary-reference-assembly-01/package`, not a fresh native
build or a guess about the newest source tree. Its retained profile, assembly
receipt and installation manifest are independently pinned by constants. The
expected implementation remains fixed. The adapter enumerates the full bounded
base tree and requires exactly its 165 selected payloads plus the two metadata
files. All 137 auxiliary profile entries and all installation entries must match
their retained length/hash pins. Selected external runtime files are pinned but
are not copied into a different installation or falsely described as hermetic.

Only the three logical paths above may differ. The replacement sources must be
existing profile entries, and the exact changed set must equal all three paths.
There are 162 unchanged payloads and no new logical payload. The installation
manifest, accepted implementation identity, compiled helpers, profile loader and
other peer/authoring sources remain byte-identical. New support identity follows
from the new Python payloads; no accepted old reference is relabeled.

The assembler loads only the exact pinned legacy builder as a helper module.
I read its import/entry-point layout and the actual `ordinary`, `pin`,
`fresh_bytes` and `save_json` functions. Loading that module does not invoke its
compiler/build functions. Its path checks reject redirected/reparse ancestry,
nonordinary files and multiple hard links; its bounded pin function checks sizes
and SHA-256. No product profile, owner or native module is loaded by assembly.

The fresh destination is fixed to `ordinary-reference-assembly-02/package`.
Canonical input paths are checked for overlap. Copying uses fresh exclusive files,
bounded chunks, fsync, exact byte count/hash and readback. Every selected input
and destination payload is rehashed, then the final output tree must exactly
match the selected map before metadata publication. The new auxiliary profile
has the same 137 logical entries and changes only the three pins. The assembly
receipt explicitly says file-only/nonadopted; PROFILE is committed last through
a fresh pending file. Partial state remains on failure; there is no deletion,
overwrite, migration, automatic retry or successful-prefix rerun.

The diagnostic receipt parser permits finite JSON floats only where explicitly
selected for retained operational metadata; the policy/profile parser continues
to reject them. Duplicate keys and nonfinite constants are rejected. This
preserves the corrected distinction that blocked the preceding unused assembler.

## Selection and cost boundary

The selector pins the exact assembler plus source-map identity, seven snapshotted
source files, all inspected base/runtime files and the unchanged helper. It checks
that selected source hashes agree with the overlay map, rehashes inputs and
sources before writing, and publishes a fresh selection with readback. It does
not launch the check. Neither old operation state nor a prior runtime allowance
is imported.

Proposed outer bounds are 90 wall seconds, 50 aggregate CPU seconds, 512 MiB and
two active processes; the assembler's cooperative limits are 75 wall/45 process
CPU seconds. Output payload bytes are capped at 80 MiB, tree depth/entries and
input counts are bounded. These are not a during-execution hard filesystem quota
or a hostile-local-administrator guarantee. Outer Job behavior is the retained
root runner's separate premise. Copying this approximately 58-MB package does
not recopy the 389,559,024-byte protected library snapshot or repeat init/intake.

Actual package hashes, closure and census still require the later selected run's
saved-output review. The source review alone does not establish registration,
authoring, growth benefit, worldwide deployment or final v5.

## Actual saved-output audit: assembly02

Root subsequently selected and executed the file-only assembly once. This
reviewer read its completed result and independently hashed the saved/current
inputs and entire package; no selected operation or product code was rerun.

**PASS for this file-only successor.** Exact output census is 167 files: 165
payloads plus PROFILE and ASSEMBLY, with no pending profile/failure/extra files.
Ordinary-file, single-link and no-reparse checks pass for that output tree.
All 137 auxiliary profile entries and all copied installation entries match their
length/hash pins. Every one of the 165 payloads was compared with its predecessor:
exactly the three reviewed Python files changed, 162 did not, and zero were added.
Total payload size is 57,984,185 bytes. The complete installation manifest is
byte-identical to assembly01; no helper/native payload changed.

All 180 selected runtime/input pins and all seven used source snapshots match
their selected SHA-256 identities and current source bytes. Copied and outer
selection files match exactly. Each overlay matches the installed file, its used
source snapshot, current source and recorded map. The independent canonical
three-overlay map digest remains `da760ed80f258b5922aad2dfddeea8f05810165c3daea603d408be5d65632899`.
Saved stdout parses to exactly the ASSEMBLY document; stderr is empty.

| Artifact below `experiments/v5-local-checks/ordinary-reference-assembly-02/` | SHA-256 |
|---|---|
| `selection.json` | `e460a5c85ef65084759f88c27dbe205d9bcf5a99fd9cce7ee8baf8055705492c` |
| `RESULT.json` | `4193f892d44cc2bd8fe9155932aeba57f53bce69f984cb7ff64a3ef2953068b5` |
| `package/PROFILE.json` | `1054b9a339503f919ac8f0bd78078c5287a16481cfe6f627b49919b45469aa10` |
| `package/ASSEMBLY.json` | `537b88521344f659c0a439847e8c39f9790b88d9ee0df14e43ae98976821d85f` |
| `package/installation/INSTALLATION.json` | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |

The actual root result records child exit zero, direct child reaped, closed Job,
no cleanup errors, no termination request and zero active/terminated processes.
Wall time is 6.125578499864787 seconds; 2.359375 Job CPU plus 0.703125 enclosing
wrapper CPU gives 3.0625 known CPU seconds. Peak Job private commit is 18,808,832
bytes. Nested supervisor CPU is not added a second time.

The package remains `ASSEMBLED_NOT_ADOPTED`. This evidence qualifies its finite
copy/map boundary, not the still-unexecuted public retained registration or
mathematical reuse. The prior failed workflow and its snapshot remain untouched
by this assembly. A separate reviewed finite public continuation is still needed.
