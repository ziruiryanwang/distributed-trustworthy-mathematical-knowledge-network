# Duplicate Lean extraction: targeted reference/recovery review

2026-10-24. Cleanup-only, read-only investigation. Canonical guard passed and
AGENTS.md was read. No deletion, extraction, native execution, experiment,
database access, full-tree hashing or Git mutation was performed by this agent.
Root owns the independent exact-tree comparison and any deletion decision.

## Disposition

**Conditional cleanup candidate, not an unreferenced directory.** Preserve the
current `software/runtime/lean-4.34.0-windows` completely. The older
`experiments/lean-feasibility/runtime/lean-4.34.0-windows` can be considered for
removal only after root's exact file-map/hash comparison establishes that it
contains no unique files or changed records and root confirms no active use.

The 850488083-byte ZIP in its parent is present, freshly hash-verified against
the recorded official release digest, and must remain. Historical rerun/source
paths will be unavailable until the old extraction is restored. Do not remove
the parent `experiments/lean-feasibility/runtime` or alter frozen history to hide
that operational consequence. This review does not authorize deleting either
runtime, archive, experiment state or evidence.

## Exact targets and archive evidence

- Candidate extraction:
  `E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\lean-feasibility\runtime\lean-4.34.0-windows`.
- Preserve current runtime:
  `E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows`.
- Preserve recovery archive:
  `E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\lean-feasibility\runtime\lean-4.34.0-windows.zip`.
- Observed archive length: **850488083 bytes**.
- Fresh observed SHA-256:
  `d382797e1abb1becd1b22593c059c223bf0698f6593bb9cdeddbf7fe23f54ca0`.

The digest and length exactly match the acquisition record in
`experiments/lean-feasibility/toolchain-provenance.md`, which records the official
Lean v4.34.0 archive, original successful digest verification/extraction, and
source commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.

A current read-only ZIP-directory inspection found:

| Observation | Value |
|---|---:|
| Entries | 18377 |
| Declared uncompressed bytes | 3245697026 |
| Sum of compressed entry bytes | 845817143 |
| Paths outside expected prefix / with parent traversal / rooted or backslash paths | 0 |
| Expected `lean-4.34.0-windows/bin/lean.exe` entry | Present |

These counts match the retained acquisition record. The ZIP was not extracted
or decompressed during this review; its exact historical digest is the recovery
identity evidence. The archive's declared uncompressed size is not an independent
measurement of bytes currently occupied by the candidate extraction. Root's
tree comparison supplies current extraction identity and size evidence.

## References: current use versus retained historical use

Read-only `git grep` over tracked Markdown/Python/PowerShell/JSON/TOML/YAML found
one direct slash-form old runtime reference:

- `research/cycles/2026-09-20-agent-definition-frontend-boundary.md:23` makes
  source citations relative to the old extraction's `src/lean` tree.

The exact old backslash-form path had no tracked matches. A broader tracked
`lean-feasibility` search found historical evidence/provenance links and one
legacy codec artifact-directory message, not an active runtime selection.
The current acceptance-boundary note still cites the **provenance document**;
that document is preserved and does not require retaining two extracted copies.

Targeted untracked historical source inspection established a genuine path
dependency that the tracked search alone would miss:

- `experiments/lean-feasibility/run_probe.py:21` builds
  `ROOT / "runtime" / "lean-4.34.0-windows" / "bin" / "lean.exe"`.
- That runner checks the runtime exists before launching. Removing the old
  extraction therefore disables historical native reruns until restoration.
- Targeted text inspection of `verify_joined_path.py` and `check_artifacts.py`
  found no `runtime`, `lean.exe` or `lean-feasibility` path use. They were not run.
  Their preserved evidence/artifact inputs must still remain untouched.

Current selected work points elsewhere:

- `software/v5/grounded_cut_basis_compare/compare_workflow.py:26` selects
  `ROOT / "software/runtime/lean-4.34.0-windows"`.
- `software/v5/grounded_cut_basis/build_support.py:23` selects the same current
  runtime. The current comparison/build support remains preserved.
- The inspected retained recursive selection similarly pins binaries beneath
  `software/runtime/lean-4.34.0-windows`, not the old extraction.

A current `Win32_Process` snapshot found no process whose exposed executable
path was under the old extraction. This is a point-in-time executable-path
observation, not proof that no process can hold a file or directory handle.
Root must enforce no concurrent runtime/cleanup use before any removal.

Coverage is deliberately targeted: tracked references plus the named historical
and currently selected sources. No disk-wide scan was performed. Absence of an
observed active reference is not inferred from the directory's age and is not a
claim that no arbitrary external script contains its path.

## Recovery and deletion gates for root

1. Finish the exact old-extraction-versus-retained-ZIP relative file-map/size/hash comparison,
   checking for unique files, reparse points or other unexpected entries. Any
   mismatch is a blocker to treating the entire old extraction as redundant.
   Root clarification: complete decompressed ZIP-payload equality establishes
   recoverability directly; separately hashing the current runtime is unnecessary.
2. Keep the verified ZIP and the current software runtime. Keep acquisition
   provenance, scripts, attempts, source cuts, logs, artifacts and Git history.
3. If root selects removal, delete only the resolved old extraction, record its
   exact pre-removal identity/size and document that historical source/rerun paths
   now require restoration. Do not silently replace it with a junction or change
   frozen path-bound scripts/records.
4. To restore later, verify the retained archive digest again, validate every
   entry target remains beneath the original runtime parent, and extract to the
   original exact path. Compare restored identities against the retained file
   manifest before invoking any historical path-bound experiment. Restoring bytes
   does not renew authorization to rerun an old experiment.

No separate `scale-crypto-01` staging investigation was undertaken: the confirmed
Lean duplicate is the high-payoff exact target, and the optional Rust-source
staging question would require its own references and recovery evidence.
