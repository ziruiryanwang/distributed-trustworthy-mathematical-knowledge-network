# RC0 focused native controls: final source contract

2026-10-21. **Source complete; NOT RUN.** Exactly40 controls,26 expected-refusal
entries. No test/build/proof/product import was performed by the control author.
Root owns finite execution selection and outcome adoption. The independent core
source disposition is `RESTRICTED-COMPOSITION-CORE-REVIEW.md`.

## Exact sources and interface

Both files are under `software/v5/restricted_composition`:

| Source | Bytes | SHA-256 |
|---|---:|---|
| controls.rs | 28602 | 3038aa56d19c4b4b08d9044a802268f118e6f52dc95d34f229604981d1983946 |
| controls_root.rs | 3551 | cee1d76d71e135784cb9e91413f30b72d5264d45ada2f367c030e457035b12a2 |

The executable accepts exactly one bounded fixture-file path. The fixture has
exactly `first`, `second`, `first_witness`, `second_witness`; input is capped at
4MiB. The complete suite runs on one explicitly joined16MiB-stack thread. The
wrapper prints exactly one JSON report and exits nonzero unless status is PASS.
No command line switches enable a weaker checker, source replacement, skipped
case, saved acceptance or production trust adoption.

The schema is `DMKN_RC0_CONTROLS_V1`, with:

```text
status: PASS | FAIL
executed_count: 40
executed: [{name, status, detail?}, ...]
expected_refusals: [the 26 names marked refusal below]
errors: [] for PASS
authority: NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY
crypto_produced: false
global_growth_claim: false
```

Root's success gate must require the exact unique case names, all PASS, no skips
and no errors. Fixture/thread/outer panic failure reports do not assert a full
40-case execution. Unexpected panic is a failure, never an expected refusal.
For prepared negative cases, setup runs outside the expected-refusal inversion:
failure to construct the mutation or positive precursor cannot count as success.
Target-specific diagnostics are required where the preparation could otherwise
conceal a missed mutation. Simple direct mutations still require checker refusal.

## Exact ordered control names

| Name | Kind |
|---|---|
| first_exact_original_refinement | positive |
| second_exact_original_refinement | positive |
| second_uses_exact_first_conclusion | positive |
| wrong_semantic_image | refusal |
| wrong_exact_rank | refusal |
| extra_legacy_rows_field | refusal |
| proof_count_mismatch | refusal |
| loose_proof_bvar | refusal |
| free_binder_domain | refusal |
| unknown_binder_style | refusal |
| out_of_scope_universe | refusal |
| unsupported_public_successor_level | refusal |
| unsupported_let | refusal |
| wrong_composition_argument | refusal |
| nonproposition_theorem_type | refusal |
| extra_theorem_metadata | refusal |
| self_reference_not_earlier_local | refusal |
| changed_parent_group_path | refusal |
| wrong_constant_universe_arity | refusal |
| unavailable_foundation_constant | refusal |
| imported_definition_is_not_a_sealed_theorem | refusal |
| missing_import_type_reference_closure | refusal |
| conditional_two_delta_target_closure | positive |
| conditional_same_image_member_continuation | positive |
| aggregate_wrong_parent_image | refusal |
| aggregate_unestablished_exact_premise | refusal |
| aggregate_exact_eof | refusal |
| aggregate_old_magic | refusal |
| frame_length_before_allocation | refusal |
| duplicate_JSON_field | refusal |
| exact_foundation_signature_projection | positive |
| binder_origin_comparison_is_root_only | unit boundary |
| simultaneous_universe_substitution | unit boundary |
| capture_safe_open_under_binder | unit boundary |
| raw_imax_zero_comparison_is_root_only | unit boundary |
| syntactic_beta_redex_refused | refusal |
| source_counter_exact_boundary | unit boundary |
| work_counter_exact_boundary | unit boundary |
| aggregate_source_counter_is_shared | unit boundary |
| aggregate_work_counter_is_shared | unit boundary |

## Why these are discriminating and what they do not establish

The two mathematical positives invoke the separately compiled RC relation and
retained original I relation on a full constructive W. They compare all184 J
bytes and the entire ordered parent list. The successor's input premise must be
the exact first J. Foundation projection is derived independently from native
rows after checking the complete canonical F prefix, rather than testing one
handwritten expected table against a duplicate handwritten table.

Positive graph controls invoke the real compiled aggregate relation. The first
requires a three-member/two-edge exact target closure from one I premise; the
second requires one same-image aggregate membership premise and a new successor,
with seal height2. The arbitrary nonzero outer image is only a conditional test
label. No I/A receipt is invented or verified. The negative-only modified-import
helper rehashes inert one-group premise bytes solely to reach the import guards.

Private comparator/substitution/census units include the exact selected product
source files using their natural crate-private interfaces. No public testing
helper is added to the production core. Their deliberately synthetic internal
terms are not submitted as mathematical evidence. Root-binder equivalence and
root-zero equivalence must succeed, but embedding the same mismatch under App
must fail; raw inferred Pi levels must remain IMax. Simultaneous substitution
must not resubstitute its replacement, and opening must avoid capturing an inner
binder and refuse a dangling outer variable.

Counter controls place a counter immediately before its bound rather than
building thousands of irrelevant terms. They verify exact boundary, next-step
refusal, overflow handling and sharing across charges. Source8,192 is explicitly
an aggregate acceptance bound charged after core work, not a claim of an8,192
pre-work refusal ceiling. The aggregate work bound is16*200,000. This is a tiny
changed-boundary suite, not an attempt to exhaust every cap/nesting combination.

A PASS supports this finite native implementation boundary only. It does not
establish machine-checked universal refinement, a guest-image identity, receipt
soundness, cost savings, useful-growth rates, public deployment or full v5.
The completed sharing audit is not rerun or relabeled by these controls.
