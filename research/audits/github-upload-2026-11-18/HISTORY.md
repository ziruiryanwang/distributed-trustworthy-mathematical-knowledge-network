# Existing Git history upload audit

Date: 2026-11-18. Read-only Git inspection; no index, configuration, branch,
history, source, runtime, or evidence changes. The canonical workspace guard
passed. This report is the only file written by this audit.

## Disposition

**No size or credential-pattern blocker found in existing reachable history.**
The inspected history is suitable for the proposed private GitHub upload within
the bounded checks below. No license decision or public release is implied.

Inspected reference: `refs/heads/main` at
`9eebc1c42d84047c01bd2e3e065e484ee58d084d` (the only reference at inspection).

| Check | Result |
|---|---:|
| Reachable commits | 298 |
| Reachable Git objects | 8,501 |
| Unique reachable blobs read and scanned | 5,735 |
| Uncompressed bytes scanned | 284,849,218 |
| Current tracked paths / distinct historical changed paths | 5,027 / 5,027 |
| Blobs at least 50 MiB / at least 100 MiB | 0 / 0 |
| Credential-pattern findings | 0 |
| Secret-file, database, archive, or executable/runtime path candidates | 0 |

The largest blob is 2,041,394 bytes:
`1724e2a58b1b39fd4de00f7b602344f3bac82cf9`,
`deliverables/2026-10-06-v4-local-release/RELEASE-MANIFEST.json`.
No Git LFS migration or history rewrite is indicated by file size.

## Coverage

`git rev-list --objects --all` enumerated reachable objects;
`git cat-file --batch-check` supplied object types/sizes, and
`git cat-file --batch` supplied every reachable blob's exact bytes.
The byte scan checked PEM/OpenSSH/PGP private-key headers; recognizable GitHub,
OpenAI, Anthropic, AWS, Google, Slack, Stripe, SendGrid, npm, DigitalOcean,
GitLab and Azure credential formats; credential-bearing connection URLs; JWTs;
and quoted literal assignments to common credential names. UTF-16 BOM content
was additionally decoded where present. No pattern matches or suppressed generic
assignment candidates occurred. SHA pins were not treated as credentials.

`git log --all --name-only --no-renames` additionally checked all historical
changed paths, including deleted names. Secret-file names/extensions, mutable
SQLite/database files, dependency/build directories, executables, archives and
common generated-output extensions produced no candidates. Historical raw modes
were only regular files and absence markers: no symlink or submodule entries.

The tracked asset inventory includes 68 `.cbor` paths. Twenty unique historical
blobs contained NUL bytes; every such blob had a `.cbor` path. All were included
in the byte scan. No tracked compressed archive was present.

## Limits and preservation

This is a local pattern audit, not proof that arbitrary, custom, obfuscated or
otherwise unrecognized credentials are absent. No external security service was
used and no matched content or secret values were printed. Uncommitted working
files, untracked files, ignored runtime/experiment trees, unreachable objects and
reflogs were outside this history audit. Root must separately review anything
newly staged for upload.

Existing ignored installations, operational state, raw evidence and packages
remain preserved locally and are not backed up by uploading this Git history.
`VERSION-CONTROL.md` records that boundary. Research remains paused; no runtime
or code test was launched.
