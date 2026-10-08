# Retired workspace path: do not work here

This directory is NOT the project. It remains only because an existing Codex
task holds its old working directory open. No code, experiments, output,
checkpoints or other project files may be created here.

The sole canonical project root is:
`E:\Distributed Trustworthy Mathematical Knowledge Network`

Read that root's `AGENTS.md`, `GOAL.md` and `research/NOW.md`. Every shell call
must explicitly set its workdir to the canonical root, and all edits must use
absolute canonical paths. Subagents must receive the canonical root and a
checkpoint location under it; inherited cwd is not authoritative.

Run the canonical `tools/Enter-Project.ps1` guard at the beginning of work.
Do not create a second project here, delete the live directory, change it to
a junction in place, or modify private application databases. Reopen the task
at the canonical directory before removing this retired placeholder.

All five original misplaced files were preserved with verified SHA-256 hashes
under the canonical project's
`research/audits/workspace-repair-2026-09-23/recovered/experiments/`.
