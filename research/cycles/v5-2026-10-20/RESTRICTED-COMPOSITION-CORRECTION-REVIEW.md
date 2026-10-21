# RC0 parser correction and exact wrapper review

2026-10-21. Independent adaptive review, source-only. **PASS for the exact fresh
correction/wrappers after the pre-use attribute-order correction below.** No
build/test/proof has been run by this reviewer; root owns runtime selection.

## Preserved actual failure

The actual `restricted-composition-build-01` result is FAIL at the first `rc-core`
compile. Its stderr reports an unclosed delimiter beginning at `trans_type` in
foundation.rs:29. The original expression opens six nested `pi` calls (native
binder names4,5,28,29,30,31). After `eq(5,4,2)` its final six closing parentheses
account for that Eq call and only five Pi calls. Exactly one closing parenthesis
is missing before the semicolon. My earlier source review missed this syntax
defect; its source-level semantic discussion did not establish compilability.

The build attempted no aggregate/control compile or test. The retained result
records zero native/test/guest/proof/network calls, worker Job0.046875CPU seconds,
controller1.734375CPU seconds, and3.6389387999661267elapsed seconds. The Job is
closed, active0, terminated0 and no cleanup errors. These are preserved failed
work costs, not a successful gate or a renewed allocation.

The original foundation.rs remains SHA
`12ce087696b026892cf8a52f8dc93b860fac8b0312ad1024b39a7fbda552b2f3`.
Original lib.rs and controls_root.rs likewise retain their reviewed hashes. No
failed source, saved output, original build selection or old evidence was edited.

## Exact fresh correction

The `foundation02.rs` diff adds only the missing `)`; it changes no binding,
universe, de Bruijn index, comparison, commitment or resource rule. Its2604bytes
hash to `e8d0e32b3c480eb05b6813b6afd8eae8413930e26a436955783b2bf3e2452dce`.
The final seven closes account for the innermost Eq call and all six Pi calls.

`controls_root02.rs` changes only its source path from foundation.rs to
foundation02.rs. Its3553bytes hash to
`962d57d9e709c74fd6e9cec9d60f8741b31993f9c630d487dd9cc3dd5e0c1519`.
The exact same corrected foundation is therefore selected for production core
and private unit/signature controls; no independent handwritten replacement
table or weaker testing implementation is introduced.

The first unused `lib02.rs` draft incorrectly placed `#[path]` after `pub(crate)`.
The required syntax is:

```rust
#[path = "foundation02.rs"]
pub(crate) mod foundation;
```

Root corrected that unused draft before selection. The read-back358-byte lib02
has exactly the attribute-first syntax above and SHA
`8399f2c78e6cac10ae3a262cc4c9c8d33b94c8f770fb6a0108dcfeb49b266059`.
No visibility or module identity is changed. The invalid intermediate draft was
not compiled and is not the selected correction.

The reviewed build02 diff selects lib02/foundation02/controls_root02, fresh
build-02 output/selection and crate metadata `dmkn_rc02_`. The retained original
module/checker libraries, remaining core/aggregate/control sources, build caps,
same three thin compile commands and no-test/no-proof scope remain unchanged.
Its reviewed SHA is
`0a7c986b1e012c8d5a0259373c77f9c902737f6122f743ddcd5c250eb86b510b`.
The complete build-chain review remains owned by the release reviewer.

## Upcoming control gate

The40 names/26 refusal names in `RESTRICTED-COMPOSITION-CONTROLS.md` remain
unchanged, as does controls.rs SHA3038aa56. No native controls have run. This
review found that the still-unused Python runner initially checked only count,
uniqueness and all-PASS rather than exact names/refusal set. Root strengthened
that pre-use check and updated its binary path to build02. The8776-byte runner
now has SHA
`48e86f99dd1a2ca754de37ff75dca659edf11b4b736c91c9096ee3ed4590779b`.

Read-only text extraction confirms its40 expected names equal the source's40
actual case names in order. Its expected-refusal indices `[3,22)`, `[24,30)` and35
are exactly the19 direct/import negatives,6 aggregate/wire negatives and1 redex
negative, totaling26 in source emission order. The success predicate compares
both complete ordered lists, besides exit0,40 unique/all-PASS results, no errors,
conditional authority and false crypto/global-growth flags. The command-line
expected count is also required to equal the fixed40, not an arbitrary caller
number. This resolves the runner completeness concern before any test execution.

The corrected source gate is clear. A subsequent runtime outcome must be audited
separately; no new suite, old rerun or broad regression campaign is requested.
