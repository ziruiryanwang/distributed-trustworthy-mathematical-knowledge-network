# Private GitHub upload scope audit

2026-11-18. Read-only inspection of the canonical project, starting from local
HEAD `9eebc1c`. The workspace guard passed. AGENTS, VERSION-CONTROL, GOAL and the
current NOW entry were consulted. Research/software work remains paused; this
audit ran no project code, tests, builds, experiments or services and changed no
source, Git index, configuration or history. This file is the sole audit output.

## Recommendation

The existing tracked scope plus the 161 reviewed nonignored additions can be
preserved in a **private current-work checkpoint**. Keep the project license
undecided. Preserve current bytes, including incomplete work and pre-existing
line endings. This checkpoint is not a release, source adoption or a complete
build/evidence backup. The export-location integration remains unadopted and its
draft source map/reviews remain incomplete, as its PAUSE.md records.

No additional exclusion was identified inside the inspected candidate set.
Retain the existing ignore boundaries and stage reviewed paths explicitly.
Do not force-add ignored trees or treat this recommendation as a public-release
or third-party redistribution clearance. Git history requires its own review;
this audit inspected current file contents and the present index/worktree.

## Census before this audit file

| Scope | Files | Bytes |
|---|---:|---:|
| Tracked current files | 5,027 | 63,965,401 |
| Nonignored untracked files | 161 | 1,940,892 |
| Combined | 5,188 | 65,906,293 |

There were nine modified tracked files, all Markdown control/checkpoint records.
The untracked additions are project research notes, source, tests, scripts and
small manifests. Their principal groups include the paper feasibility notes,
ordinary-reference sources, installed-production02 sources, source-bundle tooling,
and 39 paused ordinary-export-location draft files. No unexpected external data
collection, operational database, key file, dependency installation or archive
was found among these candidates.

The largest candidate is the already tracked
`deliverables/2026-10-06-v4-local-release/RELEASE-MANIFEST.json` at 2,041,394 bytes.
No candidate approaches GitHub's 100 MiB per-file limit. Existing small CBOR
fixtures under software assets account for the binary-containing files; there
are no candidate executables, compiled libraries or large generated packages.

All 5,027 index entries have ordinary-file mode 100644. No tracked file currently
matches the ignore rules. No symlink or submodule entry was present.

## Credential/state checks

A bounded scan read only `git ls-files --cached --others --exclude-standard`
candidates. It checked private-key blocks, common GitHub/OpenAI/AWS/Google/Slack
token formats, literal credential assignments, bearer literals, credentialed
URLs, suspicious secret/state filenames, and sensitive JSON key names. It did
not traverse ignored experiments, installations, runtimes or product trees.

No credible credential was identified. The only credentialed-URL indicator is
an intentional refusal fixture at
`software/v5/ordinary_authoring_offers/test_offers.py:145`, confirmed by its test
context. The only sensitive JSON-key-name indicator is a release-manifest path
to the Python standard-library `secrets.py`. No matched values were reported.
Pattern screening is a bounded audit, not a guarantee against every possible
secret representation.

## Boundaries to retain

The root allowlist admits Markdown plus software, tools, research, notes, spec,
security and delivery documents. Verified exclusions cover `experiments/`,
`product-local/`, `software/runtime/`, `software/build/`, `software/release/`,
`software/qualification/`, dependency/build caches, compiled outputs and archives,
common credential filenames, private-key extensions, and SQLite/database files.
Ignored material remains preserved locally and must not be deleted or swept in.

The current ignore patterns are not a generic secret detector: for example,
`software/example.env` is not covered by the `.env` / `.env.*` rules. No such
candidate exists in the present scope. Future files still need explicit review.

Pre-existing worktree LF-to-CRLF changes make the ordinary diff large for
`GOAL.md`, `research/NOW.md` and `research/registry/WORK.md`. Ignoring EOL shows
two added pause lines in each. Do not normalize them during upload; this audit
preserves the bytes already present. The nine-file semantic diff is 1,131
insertions and seven deletions when EOL differences are ignored.

The existing VERSION-CONTROL limitations still apply: a clone does not contain
all historical sources, approved runtimes, installed products or raw evidence.
Private GitHub storage is useful source preservation, not full recovery coverage.
