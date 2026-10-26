# One direct public loader/query check

2026-10-26. Root adopts the complete independent PACKAGE-OUTCOME
`c8508caac0369dd42b111d3d578145b68acb31267fe368541c6ea73b971ef48c`.
Select one direct public invocation after source/allocation review. Exact command:
`experiments/v5-local-checks/binding-package-query01.command.json`, SHA256
`09fd84bca537d4ca2073666aec219f65065af66c036dac22b2ab97dae6c3a51f`.
Its 166 pins cover the actual 154-file package, assembly receipt, selected
Python/Lean runtime files and the two existing inert query inputs.

The unchanged new-package `run.py` invokes manual-binding `query`, not owner
state, Lean, search service or mathematics. PROFILE is
`dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0`.
Input bytes are the original retained native type and exact bindings; no fixture
copies, new test adapter, altered preparer or native build are necessary.
The full public loader checks and imports the selected auxiliary binder, even
though query preparation itself does not bind a writer.

The existing public launcher supervises the child with 35 wall / 10 inclusive
CPU seconds, 512 MiB, one active process and 1 MiB per output stream. Its trusted
wrapper is cooperatively bounded and reports its CPU separately; no claim of
hard containment of the wrapper is made. Do not add a second measurement harness
merely to duplicate that boundary. Root verifies pins/fresh outputs before the
call; the independent saved audit rechecks them afterward.

Fresh diagnostics: `experiments/v5-local-checks/binding-package-query01-launch`.
Fresh result: `experiments/v5-local-checks/binding-package-query01-result`.
Expected: clean recorded process closure, exact new profile identity, unchanged
query/spec/feature bytes relative to the retained public query, zero worker CPU,
and `mathematical_acceptance:false`. A loader pass is not successful Std
production, grounding, state compatibility or final v5. Preserve any failure;
no automatic retry, archive/default update or public release follows.
