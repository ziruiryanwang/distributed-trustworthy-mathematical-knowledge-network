# Local Git introduction

User authority: introduce Git carefully and continue v5. This does not authorize
publication, a license choice, moving files, deleting evidence, or changing the
canonical project location.

## Read-only findings and selection

- The canonical workspace guard passes. The retired path stays a placeholder.
- Git 2.54.0.windows.1 is available. The canonical root has no existing repository
  or ancestor repository; no existing history is being replaced.
- System configuration has `core.autocrlf=true` and LFS filters. No configured
  personal author identity, attributes/excludes override, custom hooks path, or
  init template directory was found. Do not change global configuration.
- All three active v5 contributors checkpointed and held edits/runtimes before
  baseline staging. No root runtime is live.
- Initial candidate roots contain about 18 MB of small source/documents before
  final exclusions and public CBOR assets. Large mixed experiment/installation
  trees are excluded in full rather than blindly staged.
- Initial path and content-marker scans in candidate roots found no private-key
  blocks or common provider credential tokens. This is a scoped hygiene check,
  not a proof that future publication is safe.

## Planned reversible operation

Initialize a local `main` repository only at the canonical root. Disable automatic
line-ending conversion locally and disable normalization/filters/ident in tracked
attributes. Review the candidate file set; compare pre/post SHA-256 and raw Git
blob identities; stage only reviewed paths. Create a neutral automation-authored
baseline without hooks, remotes, external writes, or any original file changes.
No release tag is assigned. Inspect repository consistency and final status.

The scope and ongoing multi-agent commit/recovery rules are in
`VERSION-CONTROL.md`. Original artifacts stay where they are. A clone is not yet
self-contained; excluded evidence requires separate preservation and eventual
curation. This bounded setup is not a v5 mathematical/runtime test.

## Actual outcome

Pending baseline staging, byte audit, and initial commit. No commit success is
claimed by this preparatory checkpoint.
