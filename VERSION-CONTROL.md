# Version control

Git is local to the sole canonical project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
The retired similarly named directory is not a second checkout. On 2026-11-18,
at the user's request, the project is being uploaded to the private GitHub
repository `ziruiryanwang/distributed-trustworthy-mathematical-knowledge-network`.
The remote uses HTTPS with Git Credential Manager. The license remains undecided;
private source backup does not constitute a public release or v5 acceptance.
See `research/audits/github-upload-2026-11-18/UPLOAD.md` for scope and checks.

## What this repository preserves

The initial baseline records root documentation; source, tests, and checked-in
assets under `software/` (including v5); tools; research ledgers and notes;
specifications; security documents; and small delivery documents/manifests.
This is a snapshot of the existing work, not a claim that it passes v5 gates.

`experiments/`, `product-local/`, installed runtimes, generated builds, packages,
raw qualification outputs, operational databases, keys, and caches remain
untouched on disk and deliberately outside the initial repository. Some essential
retained dependencies and historical source snapshots are there. Consequently a
Git clone alone is **not yet a self-contained build or evidence archive**. The
existing manifests/checkpoints still identify those dependencies. Promote any
additional source or compact reproducibility evidence through a reviewed scope
change; never force-add a whole excluded directory. Ignored does not mean disposable.

The 2026-10-25 ordinary network handoff narrows this remaining gap: its exact
136-payload source closure is selected for local Git recording, including the
unchanged bounded builder, fair/contact/sparse overlays and matching offline kit.
The source archive and relocated interface check are documented in
`software/v5/ordinary_network_bundle/ADOPTION.md`. This is a source-completeness
boundary, not a claim of a newly executed native build from a Git clone, external
publication or complete v5. Supported runtimes and raw evidence remain separately
retained and ignored; unrelated dirty research files are not swept into commits.

The 2026-10-28 [current local kit](software/v5/ordinary_usable_distribution/ADOPTION.md)
now includes a direct current source handoff: 91 mapped build inputs plus its
recipe/map, accompanied by current operator/viewer/guide utilities. All 102 unique
source-origin paths selected by that kit are tracked and match HEAD after commits
fa424c6 and 1769a7b; no selected path is missing or locally modified. This closes
the selected ordinary-commons source closure at Git's byte-preservation boundary.
External approved runtimes and raw evidence remain separately retained. It does
not claim a new build from a fresh clone, hermetic toolchains or public release.

The ordinary-owner lane now has a narrower reproducible source boundary:
`software/v5/ordinary_package/build.py` builds its receiver and authoring support
from versioned source and explicitly supplied supported runtimes, without reading
old experiment helpers. A relocated payload passed the recorded owner lifecycle
after a caller-only visibility correction. This does not make every historical
lane reproducible or place ignored runtime/evidence archives in Git. See the
[package documentation](software/v5/ordinary_package/README.md) for exact scope.

## Byte preservation

This repository uses `core.autocrlf=false` locally and `.gitattributes` disables
text normalization, content filters, and ident expansion. Existing mixed line
endings and encodings are intentional inputs to byte pins; do not bulk-format,
renormalize, or convert them. Git content IDs supplement, not replace, the
existing SHA-256 experiment and mathematical commitments.

## Working with multiple agents

1. Run `tools/Enter-Project.ps1` with the canonical workdir. Read the live desk
   and ownership ledger before editing. Every shell call uses that workdir.
2. Agents edit only their assigned paths. The central agent owns Git's shared
   index, commits, branch operations, and repository configuration. Agents must
   not stage, commit, switch branches, or run cleanup without explicit coordination.
3. Inspect `git status --short` and scoped diffs. Stage explicit reviewed paths,
   never an uninspected `git add .` or `git add -A`. Review the staged diff before
   committing. Commit coherent checkpoints, with test status and limitations.
4. Git does not waive frozen-source rules. Executed sources, failed runs, and
   sealed evidence retain their original bytes and identities. A tested source
   successor still needs its recorded selection. Never rewrite old evidence to
   match new code.
5. Do not use `git clean` (especially `-x`), hard resets, blanket checkout/restore,
   force pushes, or history rewriting. These can destroy ignored evidence or
   another agent's work. For recovery, first inspect history and recover a named
   file into a separate reviewed destination; coordinate before replacing anything.

Useful read-only commands, from the canonical root:

```powershell
git status --short
git diff -- software/v5
git diff --cached --stat
git log --oneline -8
git show HEAD:software/v5/README.md
```

No personal author identity was found during setup. Automated commits use the
explicit non-person identity `Project automation <automation@invalid>` through
per-command Git configuration, not global or persistent personal configuration.
Choose a personal commit identity later if desired. No author identity implies
license rights, mathematical trust, or public release approval.

## Recovery boundaries

Committed files can be recovered from local Git history. Uncommitted changes and
ignored evidence cannot. Local Git on the same disk is not a disaster-recovery
backup. No automatic remote backup, artifact registry, or independent-host copy
is claimed. The initialization audit is in
`research/audits/git-baseline-2026-10-07/SETUP.md`.
