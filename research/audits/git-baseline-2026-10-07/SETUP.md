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

Completed local baseline on branch `main`:
`7e2c038f2096300e69137b6c86d78e8a2779cd9a`.

- 1,010 regular files, 19,148,512 raw bytes. Exact staged path set equals the
  pre-stage inventory; no links, reparse targets, conflicts, or submodule modes.
- Every pre-stage disk SHA-256 equals its post-stage disk SHA-256 and the SHA-256
  of raw bytes independently read from Git's blob store. No file conversion.
- `tools/Audit-GitBaseline.py` records the reproducible read-only audit procedure.
  Its local inventory is `.git/baseline-prestage.json`, SHA-256
  `48b5a70e33137056e5cb5c491d30588a85de680a9c11bf1ff1dcd24b1466b106`.
  This inventory is local metadata, not a portable backup; committed tree objects
  preserve the complete baseline content directly.
- Scoped private-key/provider-token marker scan passed on every selected file;
  source `Cargo.lock` is tracked. No privacy clearance for external publication.
- Initial commit succeeded; `git status --porcelain=v1` was empty and
  `git fsck --full` returned success. No remote, release tag, or global config edits.
- Neutral author identity was supplied per command only. Repository-local hooks,
  fsmonitor, signing, external attributes and excludes are disabled/isolated.
  `--template=` prevented inherited initialization hooks. Root `.gitattributes`
  disables filters and preserves bytes, including the public source CBOR assets.
- One read-only status attempt refused Windows `NUL` as an excludes file. Before
  any staging it was replaced by actual empty repository-local excludes and
  attributes files. Subsequent inventory, staging, audit, commit and status passed.
  No source mutation resulted from the refused status operation.

Independent assurance challenged the plan before staging: neutralize executable
hooks/filters, check the exact path set/modes, and compare raw staged SHA-256 rather
than relying on Git object IDs. All three safeguards were applied. Original
source/evidence was neither moved, deleted nor rewritten. The subsequent workflow
and live-desk updates are a separate commit, not an amendment of this baseline.
