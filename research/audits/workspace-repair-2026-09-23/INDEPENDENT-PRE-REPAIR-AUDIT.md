# Independent pre-repair audit of split workspace paths

Read-only checkpoint, 2026-09-23. The user-confirmed active project is
`E:\Distributed Trustworthy Mathematical Knowledge Network` (canonical). The
current task's unexpected cwd is
`E:\Distributed Verifiable Mathematical Knowledge Network`. Every command
in this audit explicitly used the canonical working directory. I read the
canonical `AGENTS.md` before comparing.

## Inventory and identity

Both roots were ordinary directories when inspected: `Attributes=Directory`,
no `LinkType` or `Target`; neither root was a junction/reparse point. The
canonical root contained `deliverables/`, `experiments/`, `notes/`,
`product-local/`, `research/`, `security/`, `software/`, `spec/`, and the
top-level project Markdown files. The unexpected root contained only
`experiments/lean-agent-authoring-syntax/`. A `-Force -Recurse` census found
three directories including the unexpected root's descendants, five files,
and no reparse points. An `fsutil hardlink list` check of the first Lean file
showed only its unexpected-root path, not a shared hard link.

All four Lean files exist under the same relative path in canonical and are
**byte-identical** by SHA-256:

| Relative path below `experiments/lean-agent-authoring-syntax/` | SHA-256 |
| --- | --- |
| `01-term.lean` | `e355f852e5aa7ab06fa1a8b972c9d34ce7ad7b2e1fc3ee7198a2da1a2c690201` |
| `02-same-line-by-exact.lean` | `f91059779a23a6e471187a240bc5380f057646ecbce34fa1b0af87d90bea19ba` |
| `03-multiline-by-exact.lean` | `a327c12ead61a85c490a4d58e6231f1488e356301cbb5d32d8068ccf22b48ff5` |
| `04-multiline-by-let.lean` | `bc6f8fd741f96e5677d35f019bf2e99e7834b753d382bf8651943dc3428fc859` |

The fifth file, `RESULTS.md`, is **not** byte-identical. Unexpected-root
version: 2,905 bytes, SHA-256
`1fec3055efe00a43f40ef2dbc317859f799c9ff145a6ee40f7fb7afed3b3e323`,
created/modified 05:48:51 UTC. Canonical version: 3,092 bytes, SHA-256
`91e92912dbfacc57709149cc9a226be7615725d5ab06feba4ed1d7f08d049c33`,
created/modified 05:49:53 UTC. A read-only `git diff --no-index` shows only
the introductory path-correction sentence and working-directory/argument
paths differ; the listed Lean results and scientific conclusion are the same.
The unexpected record says the four source arguments and cwd used the
unexpected path. The canonical record says they used the canonical path and
acknowledges the preliminary unexpected copy. The one-minute-later file may
describe an actual rerun, but neither directory contains separate raw process
logs, so this audit cannot independently certify those exact invocation
claims. The unexpected version is unique **path-specific historical
evidence**, not unique Lean source or a distinct mathematical result.

## Safe consolidation recommendation

Preserve the entire unexpected subtree under a uniquely named canonical
`research/audits/workspace-repair-2026-09-23/recovered/` path with a pinned
pre-move manifest. Keep both `RESULTS.md` versions intact and label the
recovered one as the original unexpected-path record; do not silently merge
or replace the canonical report. Route every agent/command to the canonical
working directory and recheck the unexpected-root census immediately before
the move to catch races. Remove only verified-empty unexpected directories
nonrecursively, stopping if an open cwd handle prevents removal. If creating
an alias junction at the old path, verify the exact target and reparse/link
attributes, and read a canonical sentinel through both spellings to verify
identity. A junction prevents future stale-cwd writes from forking the data,
but consumers must avoid recursively traversing **both** path spellings and
double-counting the same tree. Do not assume a path string returned by
`Resolve-Path` proves junction target identity.

This audit made no changes to either root other than writing this checkpoint
under canonical research/audits. It did not certify running process handles
or execute a new Lean probe.
