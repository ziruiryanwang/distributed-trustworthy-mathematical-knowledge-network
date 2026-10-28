# Root execution selections

2026-10-28. Root reads/adopts source REVIEW17f401ee and full CONTROL-REVIEW:
builder d14f2910,map65fde356,seven focused native-free control groups95861889.
The initial5bd6d337 selection was never executed: it placed two foundation
assets outside the runner's permitted snapshot scope. It remains preserved.

Root selected and reviewed the minimal input-only correction:
`current-distribution-controls01-usable-selection.json`, SHA
`40014e2a0a9093f481c9efb1e0984dad3eb4085399abd32a8eede4581644fff1`.
Snapshot only test/runner; externally pin89 canonical read-only build inputs
plus3Python runtime files, and pass canonical --source-root. No test/runner/
builder change. The existing runner verifies all external pins before/after.

Select this one run now, enclosing90wall/60CPU/768MiB/fourprocesses. The suite
allows no child/database/native operation; compiler artifacts are explicitly
labeled inert fixtures. Its actual result cannot qualify a native build.
No other runtime is live. Preserve any failure without automatic retry.

Controls01 closed cleanly,all seven groups passed. Root reads/adopts independent
CONTROL-OUTCOME59c64fbf:15.98457wall/3.875knownCPU,actual fixture154/117/8 census,
three synthetic positive stages and genuine fail-before-output/core/unknownCPU
outcomes. Synthetic markers and CPU samples are not native build evidence.
Used builder/map/test bytes stay frozen; no rerun is selected.

Next selected source work is the95-file ordinary_current_source_bundle successor.
One later real build should consume its verified extraction. The existing
builder permits byte-identical invocation from the runner snapshot while its
explicit --source-root identifies all89 extracted build inputs; it verifies the
invoked builder's bytes equal the extracted builder. This avoids changing the
frozen runner's source scope or adding a wrapper solely for two foundation files.
The input manifest and all extracted source/runtime bytes will be externally
pinned. No native build is launched by this plan.
