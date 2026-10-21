# One forty-case native refinement/control allocation

2026-10-21, root. Fully read/adopt actual build02 audit
`a54c0138d140969c8c4b249177457936b0c1f78607d2f828df9b406cfb7e98da`.
All three compiles passed; exact source/runtime/linkage/output binding and clean
closure were checked independently. This does not mean the native tests pass.
Build01's syntax failure and its costs remain preserved separately.

Select `restricted-composition-controls-01` exactly once using:

- build02 RESULT: `24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd`;
- binary: `9711910d7c0a32a08df3233bad2416fe0a88a89dae392e4fe71986e95b83e559`;
- adapter: `48e86f99dd1a2ca754de37ff75dca659edf11b4b736c91c9096ee3ed4590779b`;
- selector: `3a8f0870e29c63f5043fc634df032e42c79cc6b9fd17b4f36462a320e1f52cda`.

Use the reviewed selector with expected count40, then the resulting exact
selection and its pinned Python through Run-V5-Check. Nine selected sources,
twenty-six runtime/data pins. Shared Job:45CPU/90wall seconds,512MiB,three
processes; one native child, inner timeout60seconds. No restart or budget renewal.
The exact ordered forty controls and twenty-six refusals must all match; no
errors, skips, panics or empty-suite success. Unexpected failure stays failed.

Adaptive independently audits actual fixture, J/parent correspondence, signature
projection, per-case outcomes, ordered names, source/binary pins and closure.
Conditional native results are not genuine receipts. No guest, crypto proof,
network, image/trust adoption or public producer implementation is selected.
The independent guest preparation remains source-only until this outcome is
actually adopted. All used runner/selector/source/evidence bytes then freeze.
