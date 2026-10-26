# Selected coherent-source distribution check

2026-10-26. Root read/adopts the complete source, guide, tests and exact-selection
review (REVIEW.md SHA-256
`82873333c6714277ecf2d5296c2857744f0c1ebaea71c96cf57e415591528868`).
Select exactly one file-only controls01 run, not a native or mathematical test.

Selection: `experiments/workflow-source-controls01-selection.json`, SHA-256
`b113376f8e209b5585df5e369dde42c949b73f9acba9641449bb42e4492eb6c4`.
Fresh output: `experiments/v5-local-checks/workflow-source-controls01`.

The runner snapshots 156 exact files: 143 base payloads, ten new mapped pack
inputs, test/plan/runner. Four external pins bind the original approved ZIP and
three Python runtime files. Product input comes only from that finite mirrored
snapshot. The test obtains the exact original manifest from the selected ZIP;
no installed package, Lean runtime, owner state or historical generated artifact
is attached. The approved old helper is present at its required snapshot path.

Outer bounds: 120 wall / 60 inclusive Job CPU seconds, 384 MiB, four processes,
2 MiB stdout and 1 MiB stderr. The stdout cap is deliberately stricter than the
test plan's proposed 4 MiB. A cap/failure does not authorize a retry or renewal.

Execute the unchanged `tools/Run-V5-Check.py` using selected Python `-I -S -B`,
absolute selection path and exact hash, from the canonical root. The gate packs
once, independently compares the full original/new projection, relocates and
verifies once, checks current operational file links, and exercises the bounded
new manifest/bootstrap/extra-file refusals. Preserve all partial output and used
bytes. No source or guide repair after execution, native build, service, network,
external distribution or new proof campaign is selected.

Root must follow terminal closure and obtain independent saved-output review
before adoption. Count the inclusive descendant Job CPU once plus the separate
runner. Existing archive installation and companion tests retain their original
scope; this file-only check cannot supply mathematical growth or full-v5 evidence.
