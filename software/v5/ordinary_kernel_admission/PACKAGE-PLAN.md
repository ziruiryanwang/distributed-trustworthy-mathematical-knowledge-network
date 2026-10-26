# Integrate the reviewed receiver without rebuilding authoring

Source preparation only. Root must independently adopt focused controls and make
a finite exact selection before running `assemble.py`. The actual build is already
independently audited in BUILD-OUTCOME; this script does not infer mathematical
acceptance from a build receipt. No native call, DB open or state migration occurs.

The fixed source of receiver bytes is
`experiments/v5-local-checks/kernel-admission-build01/native`, with BUILD SHA-256
`275764e8b0da12ffb2254d0c257452e5ea2082082072de9e965618723866ded9`.
The base is `intake-progress-package01/distribution/package`, bound by PROFILE
`b850b12a96667b9a31984fe86fc0330517db9b5172bd6e63982782c10ee3ae47`,
INSTALLATION `a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb`
and ASSEMBLY `d3aec3e91b9b4b82bbc1a0aed8300530fb0c4870ec090c670f8a58f4a1749a8a`.

Validate the exact eight source/object rows and their directories before assembling.
Select the three source successors and all five recompiled receiver objects.
BasisSnapshot's recompiled object is byte-identical to its predecessor, so the
actual package delta is nine files, not ten:

- CheckedExtension, LocalSnapshot and OrdinaryWorkflowWorker receiver sources.
- CheckedExtension, LocalSnapshot, OrdinaryExport and OrdinaryWorkflowWorker objects.
- INSTALLATION and PROFILE, each regenerated with their new bindings.

All 117 auxiliary PROFILE file rows remain identical, including every authoring
helper, extractor, search, custody and transport file. The full package remains
154 files, of which 145 are unchanged. The exact existing module names, compiled
directory map, roles and support groups stay unchanged.

The pinned ASSEMBLY receipt, not PROFILE alone, supplies the full 154-file map.
PROFILE plus nonruntime INSTALLATION rows and both descriptors covers 146 files.
The other eight are BOUNDED-TRANSPORT.md, CONTACTS.md, EXECUTION-TRUST.md,
LAUNCHER.md, PRODUCER.md, README.md, RECEIVE-POLICY.md and SPARSE-SEARCH.md.
Require that exact difference, verify every projected row against the receipt,
and copy all 125 non-installation/non-PROFILE payloads (117 auxiliary rows plus
eight documents). Independent source review found and corrected the initial
omission before any package execution; the original plan would have refused
its own 154-file guard. No failed package run or used input was rewritten.

## Reuse the existing installer with the actual current controller

Use `ordinary_installation.assemble`, exact source SHA-256
`637142362b667e639d5895300dae9d9d575323ea30687dda1dafeebc00812467`.
Its sibling-source import behavior must not select the old ordinary_admission
instead of the adopted parse-reuse successor already in the current package.

After verifying their current INSTALLATION pins, preload these six current
`installation/py` modules in dependency order:

1. ordinary_evidence
2. ordinary_semantics
3. portable_evidence
4. local_catalog
5. portable_catalog
6. ordinary_admission

Then import the unchanged installer from the owner source snapshot. Refuse any
preexisting module-name collision; assert every loaded module's exact origin and
the installer's module-object bindings. This imports definitions and pure identity
constructors; it creates no catalog or admission object and opens no database.
The older installer therefore computes support digests through the exact current
controller's implementation rather than silently loading another source lane.

The new implementation must differ only in `adapter_support` and `snapshot_support`.
The actual unchanged BasisSnapshot source/object preserves `basis_receiver_support`.
Semantic identity, kernel support and controller support remain identical.
Derive the complete new implementation identity; never rewrite the old owner's
marker, reuse its checked state under a new identity, or relabel failed intake.

## Finite execution shape, still unselected

Use existing `tools/Run-V5-Check.py` with four source snapshots: that runner,
this assembler, the exact existing ordinary installer, and the existing
ordinary_fair_search file helper (`9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`).
No new selector or manifest schema is added. Required external pins are the
154 current package files, its ASSEMBLY receipt, the native BUILD receipt and
sixteen source/object files, plus nine named runtime files: 181 distinct files.
Root may additionally pin the actual control evidence/audit as launch prerequisites.

Invoke the selected Python with `-I -S -B`, the assembler under
`{snapshot}/software/v5/ordinary_kernel_admission/assemble.py`, and
`--output {output}/distribution`. Fixed fresh run name is
`kernel-admission-package01`. The assembler requires this exact snapshot/output
relationship. Proposed outer bounds: 120 wall seconds, 60 Job CPU seconds,
512 MiB, one process, 1 MiB per stream. The assembler checks 90 wall seconds and
45 controller CPU seconds; the existing installer receives that same absolute
deadline. These are proposed limits, not a renewed run allowance.

Write INSTALLATION-PLAN before invoking the existing installer. Copy the unchanged
auxiliary files, verify the full result and recheck every selected input. Write
PROFILE last within the package, then ASSEMBLY with actual changed-file identities
and costs. Preserve partial outputs on any failure. An actual independent file-map
and identity audit is required before adoption. Assembly creates support bytes;
fresh checked state and any later intake remain separate root decisions.
