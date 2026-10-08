# Working-directory incident and repair

Status: all misplaced data recovered and work routed to canonical root;
old-path placeholder removal awaits reopening the task at the correct cwd.
Date: 2026-09-23 UTC. Owner: root. User explicitly requests repair and confirms
the canonical root as `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Finding and responsibility

The canonical project is the long-lived Trustworthy tree. The unexpected
Verifiable tree was a separate ordinary directory, created 2026-09-23
02:51:10 UTC. It contained five syntax-probe files (3,259 bytes), a containing
`experiments` directory and an empty `experiments/useful-reuse-u1` directory.
It was not a second installation or node database. Four Lean sources match
canonical peers byte-for-byte. The two Markdown reports differ in their
path-specific invocation records. Preserve both; the files alone do not
establish whether a second invocation ran in the canonical location.

The app's saved project points to Trustworthy, but this live task
`01a04490-1668-7620-aa5a-3ad55a10c02c` reports a Verifiable cwd. This explains
the mechanism by which relative writes can diverge; it does not establish
who originally set that task field. Root failed to enforce the canonical
workspace consistently or close the previously noticed mismatch.

## Preservation and repair record

- [BEFORE.json](BEFORE.json) records exact file hashes, lengths, directory
  inventory and observed project/task path mismatch.
- [Independent pre-repair audit](INDEPENDENT-PRE-REPAIR-AUDIT.md) agrees that
  the four sources are duplicates and the original report must be retained.
- [repair.ps1](repair.ps1) checked both exact roots, rejected reparse points,
  checked inventory and both copies' hashes, and moved only the verified
  `experiments` child tree to [recovered/experiments](recovered/experiments).
  It rechecked every recovered hash. No original file was deleted or overwritten.
- The guard's pre-repair negative test correctly rejected the split.
- Direct script invocation was initially blocked by local PowerShell execution
  policy. Subsequent invocation used process-local `-ExecutionPolicy Bypass`;
  no persistent policy setting was changed.
- The first repair stopped at nonrecursive removal of the now-empty legacy
  directory: Windows reported it held open by another process. A subsequent
  PowerShell `New-Item -ItemType Junction -Force` also refused at deletion.
  No process was killed and no recursive deletion was attempted. Do not rerun
  the one-shot script against its already consumed recovery allocation.

The initial compatibility-junction plan was rejected after a disposable
held-cwd test: the native reparse operation succeeded, but a child whose cwd
predated it failed a subsequent relative write with `EINVAL`. The helper was
**not** applied to the real legacy directory. This failure is preserved, not
converted into a safety pass. No real project directory is a junction.

There is now one working project tree. The locked legacy directory contains
only a retirement `AGENTS.md` marker, identical to the canonical
`tools/retired-workspace-AGENTS.md` template. All original data are in canonical
storage. The guard accepts only that exact sole marker, absence, or a verified
canonical junction; an additional file/subdirectory fails closed. The guard
passes in `retired-placeholder-awaiting-app-cwd-correction` mode. This is an
explicit interim state, not a claim that the app's saved cwd has changed.
The user has been asked to reopen this task at the canonical path; only then
can the obsolete placeholder safely be removed. No project work should use it.
The [independent post-repair audit](INDEPENDENT-POST-REPAIR-AUDIT.md) verifies
every recovered hash, unchanged canonical peers, the sole marker and the passing
guard. The marker/guard is not an OS-enforced write prohibition; the remaining
app cwd correction is explicitly outstanding.

## Prevention

Canonical `AGENTS.md` and `GOAL.md` now pin the exact root. Every shell call
must specify it and every patch must use an absolute canonical path. Every
delegation states the root and a bounded checkpoint location. The small
[workspace guard](../../../tools/Enter-Project.ps1) refuses any legacy project
data beyond the exact retirement marker or a link to any other target. It changes only its shell's
location; calling it is not a change to persisted app metadata.

The OpenAI Docs skill prompted inspection of official environment guidance
and supported app tools. The available project listing and task listing were
read, but no supported tool for changing the calling task's cwd was exposed.
Private app-state editing is deliberately excluded. The Computer Use skill
also explicitly prohibits automating Codex/ChatGPT itself, so UI automation
was not used to force a workspace change. Official environment
reference: <https://learn.chatgpt.com/docs/environments/modes>.

## Central work resumes after verified repair

The project goal is not complete. D1 has independently contributed an exact
checked nontrivial theorem using a prior checked result. Next: verify ordinary
publication operationally; run the prepared source-provider-stop / surviving-
replica / fresh-receiver-admission experiment; then implement a remote-capable
peer profile (current code enforces loopback), and qualify the integrated
usable release and full-workflow cost. Workspace repair is an operational
correction, not a mathematics result or release qualification.
