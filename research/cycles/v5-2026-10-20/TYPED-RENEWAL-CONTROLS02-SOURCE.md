# Renewal controls02: test-support closure correction

2026-10-22, storage_launch_review. Source-only root assignment, canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Root reports controls01 failed before any test at import of
`aggregate_claims.prepare_mixed`; no suite/result was produced. The completed
failed run, original controls, used owner/helper and source selection remain
frozen. Root/outcome reviewer own actual failure evidence; this note does not
reinterpret the failed run as passing or waive its charges.

## Minimal correction

New `software/v5/typed_renewal/controls02.py` is the original six-test harness
with only four mechanical differences:

- Its own selected filename is `controls02.py`.
- Its **test-support** staging map additionally includes unchanged
  `aggregate_claims/prepare_mixed.py` and `aggregate_claims/input.py`.
- Source-path census is137 (130 SDK + init/helper/owner/control + two pure
  helpers + existing wrapper); staged logical-code census is136.
- The result has `harness_revision=2`; schema and result filename are unchanged.

Read the complete pure encoder and preparation imports. Their remaining direct
dependencies (`aggregate_claims` package/bindings, `delta.packet`,
`delta_claims.claims`, `mixed_claims.packet`, `modules.codec`) are already exact
logical entries in current130. The encoder's only function-local import is
`delta.packet`, also present. No additional transitive helper is needed beyond
those already loaded by the product map. No producer owner or runtime is added.

The failure was in this test support's dependency selection, not a missing
ordinary consumer API. The actual renewal owner never imports either added
helper. Product130, the132-source actual consumer and all six test bodies are
unchanged. This correction does not authorize another product/source cut.

## Exact pins

| Source | Bytes | SHA-256 |
|---|---:|---|
| new `typed_renewal/controls02.py` | 25822 | `0b3a775d7e5ba6fe0b5232e83d88b0d5446fd4f9cffac80e92d2579fed6f017b` |
| unchanged `aggregate_claims/prepare_mixed.py` | 7502 | `2d03b635553eaffa406fba57011bf3bd346ec23fd59e0092b29d9442a95802ff` |
| unchanged `aggregate_claims/input.py` | 5679 | `d40b611e288fd73a060df021809e403f80b1e6c16ca8b81ff2fd528d1f2fe61f` |
| frozen `typed_renewal/controls.py` | 25533 | `94659d28dd92f2a525d29aaca3a8548771c74c34069151542c2da6475d8e3f1c` |

`git diff --no-index` confirms only the listed staging/self/census/report
changes; it is a read-only comparison, not a Git mutation. The original control
hash still matches. Entry remains `--output <root-selected existing output>`;
output remains `typed-renewal-controls-result.json`, schema
`DMKN_TYPED_RENEWAL_CONTROLS_V1`. Root prepares a fresh selector/output and owns
execution after independent changed-boundary review. No imports, compilation,
syntax checks, tests, DB opening, native or proof calls were performed here.
