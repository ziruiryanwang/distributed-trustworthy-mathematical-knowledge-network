# Private GitHub source backup

2026-11-18. The user requested uploading this project to GitHub. This authorizes
private repository storage; it does not resume the paused research or declare v5
complete. The canonical workspace remains unchanged.

Repository: https://github.com/ziruiryanwang/distributed-trustworthy-mathematical-knowledge-network
Branch: `main`. Intended local remote: `origin`, using the matching HTTPS Git URL.
GitHub visibly confirmed the repository is private, under the signed-in account
matching the user-supplied identity. No collaborator, public exposure or license
was added. Authentication uses the existing Git Credential Manager/browser flow;
credentials are not included in this repository.

## Content

Preserve the existing 298-commit history at `9eebc1c` and add a current-work
checkpoint containing reviewed nonignored project source, scripts, tests,
research notes, manifests and pause records. This includes unfinished
ordinary-export-location work exactly as paused. Its draft SOURCES manifest is
still stale, and its remaining reviews/tests are unfinished. Committing those
files preserves work; it does not adopt or validate them.

The history audit and current-scope audit are saved beside this note. The former
scanned 5,735 reachable blobs; the latter inspected 5,188 candidate files before
the audit outputs. Neither found a credible credential or GitHub size blocker.
These are bounded pattern checks, not a proof of absence of every possible secret.

Existing ignore rules continue to exclude raw experiments, operational state,
installed runtimes, build/dependency caches, generated packages, and unselected
root directories. Those files remain intact locally. GitHub is a source/history
backup, not a complete disk backup or a self-contained archive of every historical
experiment. VERSION-CONTROL.md describes reproducibility boundaries.

## Upload procedure

Root stages explicit inspected paths from the current Git candidate list and
checks staged names, sizes, bytes and whitespace diagnostics before committing.
Preserve existing line endings and all predecessor history. Do not rewrite or
force-push history, delete state, or run the paused software.

Add the private repository as `origin`, push `main` with upstream tracking, and
compare `git ls-remote origin refs/heads/main` with local HEAD. Verify the GitHub
page shows the uploaded files and private visibility. Completion is claimed only
after those checks. The final local upload receipt records the exact pushed commit
and observed remote head; it is not mathematical or release qualification.
