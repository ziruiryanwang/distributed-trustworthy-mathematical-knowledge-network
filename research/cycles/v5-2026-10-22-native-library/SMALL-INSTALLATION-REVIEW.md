# Small ordinary installation: source review

2026-10-23. Reviewer: `admission_event_audit`. Canonical workspace guard passed.
Scope: the two new file-only installation sources, not another admission-core or
native-checker review. No runtime, tests, installation, catalog or Git operation
was performed. Root has separately reported the four admission controls passing;
they were not repeated here.

## Disposition

**No blocking safety or operability defect found for the proposed explicit
15,704,496-byte assembly with external runtime attachments.** Root may select
that bounded assembly. This is source review, not an installed-file outcome or
mathematical/public-release acceptance. The selected plan's exact map and actual
copied/runtime file counts must still be checked from the resulting evidence.

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/ordinary_installation.py` | `637142362b667e639d5895300dae9d9d575323ea30687dda1dafeebc00812467` |
| `software/v5/ordinary_lean/run_ordinary_installation.py` | `fdea96807049283fd5d677c02547926e7dbf78276f10ead50cb652d8aba96776` |

## Relevant safeguards

- The assembler accepts one externally pinned canonical owner plan, not discovered
  peer instructions. File selection is explicit: no recursive directory copying,
  compiler invocation, native checker execution, catalog opening or migration.
- Destination must be fresh; source/runtime roots and destination must not
  overlap. Existing ordinary-path checks refuse symlinks/reparse points and
  require absolute paths. Logical paths are validated, role targets must be
  enumerated, file pins are bounded and support groups cover every selected file.
- Runtime logical paths must resolve to the exact supplied runtime attachment
  path. Those selected files are read/hash checked in place, never copied or
  modified. The proposed 15.7 MB copy thus need not duplicate the full toolchains.
- Before destination creation, all selected source bytes are checked. Copied
  files use exclusive creation and streaming hash/size checks, then flush/fsync,
  destination verification and source revalidation. No overwrite or deletion
  recovery path exists. A failed attempt preserves its partial fresh destination.
- Named support is capped at 512 files/2 GiB; copied support is separately capped
  at 256 MiB. File sizes, manifest sizes and compiled-file selection are bounded.
  These limits bound selected bytes, not an adversarial filesystem or all runtime
  dependencies. Immutable owner storage remains an explicit premise.
- The complete public manifest is written last through a flushed pending file and
  a same-directory non-overwriting Windows rename. A failure before that commit
  leaves no completed manifest. The result explicitly says `ASSEMBLED_NOT_ADOPTED`.
  Exact executable/core/module policy is still enforced when the installed owner
  opens the manifest; assembly alone does not authorize an old-I store.
- The thin adapter bounds its input read, rejects duplicate JSON keys and floating
  or nonfinite numbers, canonicalizes the selected plan and preserves canonical
  plan/result evidence. Its input is externally pinned by the enclosing selection;
  its computed canonical hash is not a substitute for that external selection.

## Resource and outcome interpretation

The assembler's single absolute deadline is not renewed within file verification,
copying or manifest publication. Checks are cooperative; blocking filesystem I/O
is not a hard real-time bound. The adapter's 90-second assembly window starts
after plan parsing and does not encompass its final receipt writes. The enclosing
root-selected supervisor is therefore the whole-operation resource boundary.

The manifest may be complete while a subsequent adapter receipt write fails.
That must be reported as an ambiguous/incomplete adapter outcome with preserved
installation bytes, not as permission to retry into the same destination or to
assume adoption. Windows rename durability across sudden power loss is not proved
by this source review; installed verification on opening remains necessary.

No full-source audit, runtime copy campaign or repeat of previously passing
native/admission tests is warranted by this file-only step. A compact actual map,
manifest and clean-supervision inspection is sufficient for its stated outcome.
