# One focused frontend differential, source-only selection

Root selected acceptance-preserving receipt frontend A/B/C after independent
plan/source review. No build or runtime is selected by this document. The
implementation is one mutable tree; prior guest/native source snapshots stay
unchanged. Root owns eventual exact build/run selections and launches.

## Minimal implementation source map

All paths below are relative to `software/v5/modules/receipt/src/`.

| File | Bytes | SHA256 | Change |
|---|---:|---|---|
|input.rs|2735|`4b5da4aefeef4ca7dc2ce3d2bd10cd0f270a3d5682f2ea16d8ea2e37c63bfa46`|New shallow map/positional-array extraction; move Value fields, serde typed leaves|
|canonical.rs|8249|`989c2695a03c17111d1960c2b4360cb6383b20302c8fac1f52c8034b8f04099b`|Private syntax/framing helpers, unchanged public parse, internal parse+hash and canonical-hash pair|
|relation.rs|7596|`879b3a7bbeeb7f6844597763a737aee9ae5ddea0824cbe83115631aac0c07df3`|Preserved public types/check; check_bytes to private check_bound; once-encoded foundation|
|main.rs|1429|`00e2f0a27837ff846c1a4c209839a7f636b4d23bc2da26e0c3e89ef55b976df0`|Guest uses check_bytes; frame and recursive parent verification unchanged|
|lib.rs|180|`06ab1b9682982e88c85e22c4bef76550b31193784baea59ea04b1385236f6c4f`|Private input module|
|bin/receipt_native.rs|4372|`7122ad27a0143d2b2623cd8a21776edba8aeda25642499a9c7d099ce5174cad3`|Private input module for standalone diagnostic crate|

No native kernel, commitments, journal format, policy, witness schema, limits,
host command, recursive verification or receiver authority changed. The separately
qualified move-based correspondence source remains in the same mutable tree.

## Exact harness and scope

`frontend_differential.rs` is14,918B, SHA256
`06515ba4dd360f1713fc7bd9117bbe1a691458d4a981e42a84bc768b48df421a`.
It directly includes the new actual canonical/input/relation and unchanged
commitments/journal/policy files, preserving relative source topology. Old
canonical.rs is included from exact frozen guest02 path, SHA256
`f5b63e491af8c2d009adb5dbb75a599dece19adc1418be4dd8732deb9489bcb8`.
Input's preserved derive/field ordering is the reference for move extraction;
it invokes serde's independent old conversion, not the new extractor twice.

Link once with the retained actual serde, serde_json, Nanoda and RISC0 libraries
used by `receipt-native-build-01-selection.json`. No Cargo/backend or kernel
library rebuild and no mocked SHA implementation. Nanoda is the retained native
library; constructor move equivalence has its separate actual11-case gate.
Thus this harness qualifies the frontend seam against real native checking,
not a new compiled guest or all components of its future image.

Tests in the one bounded run:

- Five held receipt witnesses: exact old/new parse and extracted fields; old
  witness hash versus held expected hash; each new public check/check_bytes
  result yields the identical216-byte held journal and exact pending parent
  journal bytes. Ten native relation calls total, no parent proof calls.
- For each, old/new foundation raw SHA and domain hash agree.
-58 synthetic extraction controls: eight map/sequence combinations;12 required
  missing fields;three extra fields;six short/long positional records;24 focused
  scalar/container/numeric refusals;four wrong root types;one target-usize
  boundary. Every refusal requires both old and new refusal. Successful outputs
  compare all fields. Error-string equality is deliberately not required.
- Nine retained cross-language hash cases: exact canonical bytes, old/new framed
  hash, retained expected hash and new once-encoded raw-SHA/domain-hash pair.
- Additional raw/encoding boundaries: whitespace/key order accepted identically;
  nested duplicate, trailing bytes, negative/float/exponent/u64-overflow number,
  invalid UTF8 and empty raw input refused; parser depth, raw byte maximum,
  canonical global node maximum, direct canonical depth/byte bounds, and two
  invalid domains refuse identically. Total canonical controls25.

Synthetic shape-valid inputs are not mathematical witnesses. usize conversion
is compared on the native target and remains the same typed serde conversion
on the guest; no claim that a64-bit native run alone tests a32-bit target limit.
Full native comparisons use preserved actual witnesses and expected journals,
not generated successful expectations. Duplicate/limits cases never call kernel.

The wrapper must pin/recheck13 held files: predecessor canonical;two vector
files;five receipt-input/result pairs. Copy the old source separately and keep
its absolute include origin pinned. Runtime file hashes below are exact source
inputs, not executed evidence yet.

| Input relative to experiments/v5-local-checks | Bytes | SHA256 |
|---|---:|---|
|receipt-vectors-01/evidence/canonical-hashes.input.json|1533|`fc6014e7c5546e166daf107d3d7ffd3425b230d6b2d4171b079fe45f1a7b94b1`|
|receipt-vectors-01/evidence/canonical-hashes.stdout|674|`8079b96b39277e4861dbcc3ce1a33d360167f8abefca676d5c93d9e3ea84598d`|
|receipt-prepare-01/prepared/base/receipt-input.json|91311|`025d2ce3c42cf7eeab00d1e6626d22d59afe495c64232ad2687893eea278d4a8`|
|receipt-prepare-01/prepared/base/receipt-result.json|1345|`51e2b590da76786a69f00dc70842f0ecf2e068199ef4a9a4211f294594a297b1`|
|receipt-prepare-01/prepared/fusion/receipt-input.json|100791|`c24c7cc535a047ec548c58b6983149ec988c4550f64972492a127a05a25f0904`|
|receipt-prepare-01/prepared/fusion/receipt-result.json|1349|`4b1d671c76dcdc374b1dcf15766b0f45f3d5c4e64d3b96ddc4aa4d3e3a86933f`|
|receipt-prepare-01/prepared/fold_map/receipt-input.json|99460|`766034d47509df7ecda7f4293234a06da148377d137d751e4fa1fc224efdf8c8`|
|receipt-prepare-01/prepared/fold_map/receipt-result.json|1336|`a5f44515eb73d6874c9a48fe6fac871f6d5cf33c88ad0d8d006357cf8bd5c868`|
|receipt-prepare-01/prepared/fusion_map/receipt-input.json|109160|`a7e5e42ab9be25c464dcf426c9b538e9f7cce9d619b59d6d401f04b031716082`|
|receipt-prepare-01/prepared/fusion_map/receipt-result.json|1340|`4237af1e925bcae2bb5240412e14e1a1a16ede01c51663f5ba69aa5960544bb6`|
|receipt-prepare-01/prepared/project_summary/receipt-input.json|104348|`905a20c3095830dae32aaf36b27e9392caae3bc8c80ecb3152757b7ecdb2ff11`|
|receipt-prepare-01/prepared/project_summary/receipt-result.json|1338|`925ac0553d528c2cc1461ba2e3b94678edd742ee4499ff06b5214845d8d6d65f`|

Suggested run allowance:90CPU/120wall seconds,768MiB,three active processes,
1MiB stdout/stderr. It uses a16MiB worker stack. Near-limit canonical controls
allocate up to16MiB byte/string inputs and1million Value nodes serially; record
their cost rather than treating them as production speed evidence. Outputs are
new case reports only. Old fixture/evidence bytes must never change.

Passing status is exactly
`PASS_FRONTEND_EQUIVALENCE_NOT_GUEST_PROOF_OR_SPEEDUP`.
Native differential success cannot discharge genuine parent certificates or
establish VM/prover savings; those require separately reviewed new-image gates.

## Exact compile adapter

`build_frontend_test.py` SHA256
`5426b5b75f3d184b0d3a5b7a4882a5547b6880639d13bfb9cbf335b3cd9776ed`
adapts the already reviewed standalone compilation lifecycle. It pins the full
172-file explicit receipt-native runtime map (905,860,373B) and exact old link
recipe from `receipt-native-build-01-selection.json`, SHA256
`b9e1b2d77bc8af80a31fe543b251dfc5790b5296613173ed115a43df4e634bf5`.
Only crate name, harness entry and output change in that recipe. This is not a
complete census/pin of every transitive backend search directory or Windows OS;
the result explicitly retains that scope. No backend library is rebuilt.

Twelve selected source/plan files are copied with their source topology; frozen
old canonical is additionally copied under previous-source and its absolute
include origin rebound before/after. The fresh build output is
`experiments/v5-local-checks/frontend-differential-build-01`; an independent
attempt record preserves preallocation failure. Limits180workerCPU/phase-wall,
300totalwall seconds,4096MiB,eight processes,6GiBaccounted storage are unchanged
from the adopted standalone compiler helper. Exact Job-owned/hash-pinned VCTIP
cleanup is selected; unknown lingering descendants refuse. There is no test
invocation in this adapter. Actual executable hash must be read from a successful
reviewed result before deriving the separate runtime selection.
