# Derived-support native builder and retained-host reuse

2026-10-21, core_release. Root-selected source only under
`RESTRICTED-SUPPORT-SELECTION.md`. No syntax parse, Python import, native
compile/control, guest, assembler, host, proof or network execution was performed.
No Git mutation. Used predecessor files are unchanged.

## Final builder contract

`software/v5/restricted_support/build.py` SHA-256:
`5f0c4beaa8070aeae5890514f173a87ba9bf7d72904ebb3f235374b6ae2ba377`.

Invoke only after root's separate selection with the retained pinned Python,
`-I -S -B`, exact selector path and selector SHA as its two arguments. Canonical
workdir is `E:\Distributed Trustworthy Mathematical Knowledge Network`.

- Run: `experiments/v5-local-checks/restricted-support-build-01`.
- Selector: sibling `restricted-support-build-01-selection.json`.
- Schema: `DMKN_V5_RC_SUPPORT_BUILD_V1`.
- Exact keys: schema, name, authorizes_compile_only, sources.
- Result schema: `DMKN_V5_RC_SUPPORT_BUILD_RESULT_V1`.
- Success: `PASS_RC_SUPPORT_TWO_COMPILES_ONLY`.
- Commands: `support-core`, then `support-controls`.
- Outputs: `libdmkn_rc_relation.rlib`, `restricted_support_controls.exe`.

Eight selected files are snapshotted, not a broad project copy:

```text
software/v5/restricted_support/lib.rs
software/v5/restricted_support/syntax.rs
software/v5/restricted_support/typing.rs
software/v5/restricted_support/controls.rs
software/v5/restricted_support/controls_root.rs
software/v5/restricted_support/build.py
software/v5/restricted_composition/relation.rs
software/v5/restricted_composition/foundation02.rs
```

The two frozen semantic files must match the adopted native02 source map.
The new lib uses their explicit relative paths. Adaptive confirms its private
control modules need only this same closure; no aggregate/header/wire crate.

The builder reuses the frozen build02 helper and retained original-module
compiler recipe. It changes source/output/crate metadata and adds the two
explicit control externs. Original metadata remains inside the baseline rlib;
fresh metadata `dmkn_rc_support01_*` separates its crate identity. Both crates
use the identical retained original `dmkn_module_relation`, compiler and runtime
libraries, not a newly compiled or bounded-parser module relation. The baseline
alias is `dmkn_rc_baseline`; the new crate is `dmkn_rc_relation`.

Actual retained baseline library was checked read-only:1719004bytes, SHA
`1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b`.
Its exact successful result24e8ebf8, selection659c780e, source-map32e95e4b,
attempt and absence of a finalization override are required before/after build.
The original module build's successful result/attempt and retained runtime pins
are likewise required. No old core, checker, module, SDK or aggregate recompiles.

Resource ceiling:180inclusive worker CPU seconds,240worker wall,1024MiB and six
processes;30controller CPU and360total wall. Fresh output census is128MiB/1024
entries, command log bound1MiB. These reuse the existing owned phase/Job cleanup,
with no new supervisor. Output limits are sampled, not disk quotas. The saved
selection preserves exact input bytes, avoiding the prior reserialization bug.
Final checks bind all source/runtime inputs and the exact source snapshot.
Failure records, partial outputs and charges stay; no retry or controls execution.

## Independent root-selector review

`research/cycles/v5-2026-10-20/Select-RestrictedSupportBuild01.ps1` SHA:
`acac270896001e9619e24fb0957a2e0720daeb4700d2355d9c64e8fdc9acefe6`.

**PASS_SOURCE_CONTRACT_MATCH**: exact eight-source set, schema, keys, name and
fresh output/attempt/selection checks agree with the builder. The selector
requires root's reviewed builder digest, computes actual source length/hash pins,
uses create-new selection writing and starts no process. Root must compare the
fresh Rust/control pins with their independently reviewed versions before the
eventual compile invocation; pinning arbitrary current bytes is not source
review. Missing controls or changed source bytes do not become accepted through
this selector review. This reviewer did not run the selector.

## Reuse the old snapshot host for a future same-fixture guest screen

The adopted `restricted_snapshot_host.exe` can be retained for this narrow
execute-only purpose; a new host link is not required merely because A changes.
Source `aggregate_small/aggregate_host.rs::snapshot` shows:

1. The selected ELF is read and its computed image ID must equal the explicit A.
2. The old linked RC relation preflights the submitted wire and must reproduce
   the exact expected header and pending boundary count.
3. Genuine boundary receipts are verified independently, against exact pending
   claims and the selected image policy.
4. That same wire is passed to the actual selected new ELF. Successful execution
   must reproduce the expected journal/claim; capsule is only execution evidence.

For the retained first fixture, old RC already accepts the exact frame and the
base-I receipt. New-core differential controls must independently reproduce the
same full conditional J and exact parent claims on those same bytes. Only the
wire/header A bytes change to the newly assembled guest image. The derived
support metadata never appears in the wire and must not change its semantics.
The host is not trusted to infer a new result from the old guest image.

This is deliberately not unrestricted producer adoption: a new-core input
accepted only due to lower work usage could still be refused by the old native
preflight. Recursive same-A inputs need their own exact compatible receipts.
The selected first fixture has a genuine fixed-I parent, not a relabeled old-A
receipt. The source-only host reuse conclusion authorizes neither execution nor
reuse of the failed screen as a passing economic result.

Root still owns native review/adoption, prospective guest selection, actual image
assembly and a fresh exact pair configuration. The unchanged row/segment/CPU
screen remains binding, and no proof is invested before its separate success.
