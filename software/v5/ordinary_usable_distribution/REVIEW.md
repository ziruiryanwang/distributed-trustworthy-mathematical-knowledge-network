# Independent kit utility and source-selection review

2026-10-28. **PASS for the pinned source and explicit local selection below.**
This is not an executed packing, relocation, native-trust or release-authentication
result. I did not author `kit.py`; I read the selected utility/helper, source map
and builder seams, current package metadata and exact selection. Read-only file
hash/length comparisons were performed with PowerShell. No product imports,
kit execution, native process, owner/database access, network or Git occurred.
Guide/catalog usability has a separate reviewer.

| Reviewed artifact | SHA-256 |
|---|---|
| `kit.py` | `e844924cf9f66a0c963142f7dc8a9a0f0128623bf15b6a90514a858dfb908ebf` |
| `file_helpers.py` | `b5d211a83644b61c6a6fe673785ccd1e1960816a2d58f20787b9d4dfdb3c9da9` |
| `SELECTED-FILES.json` | `27acdcefd95b6d5b397f20b3c98bebe15986b17f74513e8d66118060eecd83d1` |
| Current source map | `05d96f671ecb755b20bcb55d0a93a33a8e70abdaa559017c750635deaba1eef5` |
| Current direct builder | `80c9615f8742d14a7fa2e0b94914268bc1f0735da637f8d666bfb60c5e5f0f2e` |

The helper is byte-for-byte the retained `ordinary_current_source_bundle/bundle.py`.
Its unrelated historical source-selection functions are not used by this utility.
The adjacent helper is bounded, checked against its fixed hash, then executed;
it imports only standard-library modules. The utility never imports the package,
builder, operator or preview to pack/verify them.

## Exact selection and closure

All **260 selected actual files** match their descriptor's byte length and SHA-256;
there were zero mismatches. Payload total is **42,800,455 bytes**. The extraction
requires 56 directories and 317 census entries including the new manifest.

- All 158 `package/` selections have origin `package` and identical source/destination
  suffixes. Every pin matches the adopted reply-capacity `ASSEMBLY.json`. The
  package payload is 39,572,640 bytes; its largest file is 5,588,544 bytes.
- The 93 `source/` files are exactly the pinned map's 91 direct source inputs plus
  the current recipe and map. Every source pin/origin/suffix matches. The map
  includes its file-helper/compiler-worker and installation assembler; current
  builder bootstrap and lane inputs come from this closure, not an experiment
  package or another extraction. External Python/Lean toolchains remain inputs.
- The other nine files are the root guide/request catalog/utility/helper, the
  matching three-file operator companion, and the two-file offline preview
  companion. The preparer's adjacent helper/map and the preview's adjacent
  renderer are present. Preview codec dependencies are already within `package/`.

The selection is an explicit approved byte set, not a filesystem discovery or
wildcard. The utility additionally checks fixed current PROFILE/map/builder/helper
identities, 158 package members, actual PROFILE payload pins, the actual installation
manifest hash and all local installed payload pins. The two runtime prefixes in
that fixed installation manifest are explicitly external; their bytes are neither
bundled nor verified. The map's 91 sources are all checked against selected data.
Source-byte closure does not assert a newly successful build or reproducible PE bytes.

## Archive, extraction and path relation

The archive contains the selected payloads and canonical manifest in deterministic
sorted order, stored without compression. Readback checks exact member names/order,
bytes, sizes and fixed metadata. It does not extract an arbitrary peer archive.
Extraction uses selected relative paths and fresh writes, then the ordinary kit
verifier independently rechecks the actual extracted tree, manifest and all payload
pins. Extra files/directories, missing members and changed bytes cannot produce
successful exact-census verification.

The source and selection are re-read before success; the original package census
is checked again. The captured archive pin is now required to agree at the terminal
read, so the receipt binds the same archive checked before extraction. Receipt
creation occurs only after these checks. Failed output is preserved, with no
cleanup, overwrite, retry, migration or renewed allowance.

Relative-path checks reject rooted/traversing/reserved names, alternate stream
syntax, redirects and invalid Windows components. Absolute-path checks require
ordinary local drive paths and reject symlink/reparse ancestors and hard-linked
files. Output cannot contain a selected source or overlap the package. Required
directories are derived only from selected names. This is a locally approved,
immutable-source and exclusive-output workflow; path checks are not an atomic
security boundary against a hostile concurrent filesystem actor. The actual
selection uses ordinary ASCII path components and has no case-fold collisions.

The verifier is itself an approved executable input: selecting a manifest digest
does not authenticate an arbitrary downloaded `kit.py`. Neither matching hashes
nor this review selects a publisher, license, external release or mathematical
acceptance policy.

## Finite resource envelope

The code limits selection/manifest payloads to 250..384 files, 8 MiB per file,
64 MiB aggregate payload, 2 MiB manifest and 1,024 actual tree entries; archive
readback is bounded at 72 MiB. The actual selection fits each limit. ZIP members
are stored, and their bounded sizes are checked before reading each one; no
compression-expansion path is accepted.

The implementation keeps payload bytes in memory and temporarily retains a second
copy during extracted verification. Chunk joining can momentarily retain both
archive chunks and their joined bytes. Thus the payload total is not a process
memory bound. The source design is finite and a 512 MiB outer Job is a reasonable
selected envelope for this approximately 43 MB input; actual peak memory remains
an execution measurement, not a source-proved value. The existing helper's
60-wall/30-CPU cooperative guard is retained, and nested verification calls the
original guard too. Blocking filesystem calls still require the outer envelope.

## Resolved before execution

Two initial consistency gaps were reported to root and repaired in the reviewed
hash: terminal archive bytes had not been compared to a pre-readback pin, and
the installation hash had only been checked as a PROFILE field. The first version
of the new installed-payload loop also attempted to require external runtime bytes
inside the kit; readback identified that refusal and root corrected the exact
runtime-prefix distinction. These were source findings, not failed experiments.

## Minimum changed-boundary evidence

Select one bounded pack of this exact descriptor. Its inherent archive readback,
fresh relocated extraction, exact verification and terminal receipt already
exercise the principal new boundary; do not repeat packing to produce redundant
successes. Retain and independently inspect the resulting manifest/receipt/tree.

One wrong-manifest-digest verification should refuse against that unchanged
extraction. Then one relocated inert operator preparation and one offline preview
display over retained authentic input should establish that the matching companions
resolve their dependencies from the extraction. These operations execute no
generated mathematical command and need no native worker, service or new theory.
Use the established input/codec/control evidence for unchanged behavior.

No separate synthetic package campaign, second native build or reciprocal theorem
loop is justified. Successful local relocation would establish usable packaging
on this computer, not independent-machine deployment, external authenticity,
worldwide availability or causal research acceleration.
