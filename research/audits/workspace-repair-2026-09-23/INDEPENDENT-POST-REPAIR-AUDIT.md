# Independent bounded workspace-repair audit

Checked 2026-09-23, read-only except for this note and the separately scoped
disposable in-place-junction test. The canonical project is
`E:\Distributed Trustworthy Mathematical Knowledge Network`; every command
in this audit specified it as the tool working directory. The task's former
cwd, `E:\Distributed Verifiable Mathematical Knowledge Network`, is **not**
yet a junction or an active project. The product/release goal is unaffected
by this infrastructure checkpoint.

## Recovered bytes and current topology

The pre-move [`BEFORE.json`](BEFORE.json) pins five files totaling 3,259 bytes.
The recovered tree under [`recovered/`](recovered/) now has exactly those five
files and three directories (`experiments/`,
`experiments/lean-agent-authoring-syntax/`, and the empty
`experiments/useful-reuse-u1/`), with no reparse points. Independent
`Get-FileHash -Algorithm SHA256` and length checks matched every manifest
entry; the corresponding five canonical peer hashes also still match the
manifest. The recovered `RESULTS.md` retains the original unexpected-path
invocation record, rather than overwriting the separate canonical report.

The unexpected root is still an **ordinary directory** (`Attributes=Directory`,
no `LinkType` or `Target`) with exactly one child, `AGENTS.md`. Its SHA-256
equals the canonical
[`tools/retired-workspace-AGENTS.md`](../../../tools/retired-workspace-AGENTS.md)
template. It explicitly forbids work in that path and directs agents to the
canonical root. No actual in-place reparse operation was applied to the
unexpected root. The old placeholder remains because the active task still
has that directory as its app-managed cwd; app cwd correction/reopening is
pending. The marker and guard mitigate accidental divergence but are not an
OS-enforced write prohibition.

The canonical [`tools/Enter-Project.ps1`](../../../tools/Enter-Project.ps1)
guard returned `Status: PASS`, `WorkingDirectory` equal to the canonical root,
and `LegacyState: retired-placeholder-awaiting-app-cwd-correction`. The
host's normal PowerShell execution policy refused direct `&` invocation;
the audited invocation
`powershell -NoProfile -ExecutionPolicy Bypass -File <canonical absolute path>`
returned exit code 0. This Bypass is process-scoped. A prior negative guard
check refused the split state. I did not create wrong-root files to repeat it.

## Why live in-place junctioning was rejected

The disposable helper [`inplace_junction.py`](inplace_junction.py) tested only
`inplace-junction-test-01/held-open-link` pointing to its sibling `target`.
Using documented `FSCTL_SET_REPARSE_POINT`, it successfully attached an NTFS
mount-point reparse tag `0xA0000003` to an existing empty directory while a
child held that directory as cwd. `fsutil reparsepoint query` and `Get-Item`
confirmed `LinkType=Junction` and the exact sibling target; a new absolute
lookup through the junction read the target's `sentinel.txt`.

However, the already-running child then attempted a relative write and
failed with `OSError: [Errno 22] Invalid argument:
'relative-created.txt'` (test command exit 1). Neither the link path nor
target showed that file. This directly refutes treating in-place conversion
as transparent for a process holding the old cwd handle. The test junction
was retained **only** in the disposable audit child directory for inspection;
it is not the project-root alias. The helper's actual-root mode is disabled.
No process was killed, no directory was recursively removed, and no private
app database was changed.

The relevant API reference is Microsoft Learn's
[FSCTL_SET_REPARSE_POINT](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_reparse_point),
which documents setting a reparse point on a file or directory. That API
fact does not imply transparent behavior for preexisting cwd handles; the
local held-handle observation is the governing safety evidence here.

**Boundary:** exact recovered bytes and the current guarded placeholder are
verified. The task has not yet been reopened at the canonical cwd, the old
placeholder has not been retired, and no reciprocal-return/release claim is
made by this audit.
