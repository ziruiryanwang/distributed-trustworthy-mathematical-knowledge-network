# Directory-validation cache: changed-boundary controls

2026-10-20, core_growth. Canonical guard passed. Source only; root alone selects
the existing bounded runner and exact inputs. No runtime, SDK import, native
worker, prover, compiler, Git mutation or installation copy was performed.

## Why these six controls

Install01's reported obstacle is repeated filesystem metadata work, not memory
or mathematical checking. The proposed successor caches **validated directory
paths only** within one explicit `path_scope()`. Tiny controls therefore count
`Path.resolve` calls and challenge leaf checks; they do not benchmark a large
tree, run the seven already-passed distribution controls again, or adjust RAM.

`software/v5/distribution_efficient/test_paths.py --output EXISTING_DIRECTORY`
loads only the adjacent distribution source. Each test creates a unique tiny
fixture directory beneath that supplied output; final fixtures are retained.
The one leaf deletion/replacement is deliberately part of the fresh/type
control, never removal of project or prior evidence files.

The controls are:

- Stable-directory file checks: initial resolves are bounded by the ancestor
  count; additional leaves and repeats add zero. Exactly one new sibling
  directory adds exactly one resolve. No file leaf is resolved in a scope.
- Fresh/existing status and leaf type: present files refuse fresh, removed
  leaves fail existing checks, and a replacement directory fails file checks.
- Leaf `lstat`: each repeated file check observes current metadata. Controlled
  metadata injection rejects reparse and non-file kinds without needing symlink
  privileges or claiming an actual adversarial filesystem-race experiment.
- Pins: same-length byte changes fail hashes; changed lengths fail sizes.
- Mid-check size changes: appending one byte after the actual digest still
  fails the post-digest size check.
- Lifetimes: nested scopes use new caches and restore the outer cache both
  normally and exceptionally; leaving a failing outer scope resets it; ordinary
  unscoped calls retain their original uncached file-resolution behavior.

`controls.json` reports all six outcomes, exact adjacent source SHA-256 values
and deterministic operation-count metrics. A pass concerns these changed
directory-cache boundaries only. It cannot establish elapsed-time improvement
for the full install, prove race resistance against a hostile local mutator,
or establish any mathematical acceptance or v5 release claim.

## Current state

Source authored, not executed. The product author confirms public
`path_scope()` and unchanged `ordinary`/`pinned` signatures. Root must adopt
the final reviewed source hashes and choose one bounded execution before any
actual control result exists.
