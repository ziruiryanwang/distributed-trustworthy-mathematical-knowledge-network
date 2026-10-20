# Missing-body negative: reuse existing evidence; do not rerun

2026-10-20, core_release. Root requested the smallest remaining native
missing-body control. Source/evidence inspection found that exact boundary
already exercised. **Do not author or run a duplicate negative campaign.**
No runtime, implementation, compilation, receipt fabrication or Git action
occurred in this investigation.

## Existing actual discriminator

`experiments/v5-local-checks/native-controls-01/evidence/` already contains:

- `missing-fold-body`: original imported `CommonsV5.fold` descriptor retained;
  only its native definition row becomes `moduleImportDef` with the same name,
  universes, type, reduction hint and committed body hash. The unchanged local
  fusion proof then yields exact `NeedBody`, native name index 92, body digest
  `0b5f265dfb01a1ed1232443bfdc79c5217be78664b15ee9d12e01fa77d2e6e55`.
- `exact-body-recovery`: restoring precisely the original definition row makes
  the input byte-identical to the known positive fixture. Native checking
  succeeds conditionally and checks local theorem index 101.

Both explicitly retain false certificate-verification and mathematical-admission
flags. These are real kernel behaviors under conditional imported premises,
not genuine receipt issuance or a fake claim of unconditional mathematics.
The missing-body response exits zero because this diagnostic encodes NEED as a
normal result; NEED is never an accepted extension.

Rehashed saved inputs:

| Artifact | SHA-256 |
|---|---|
| missing-fold-body/input.json | 83141727bef1813bf788c6e0bb99274135aa5f8473f0d1d71bc4a88544d9af1b |
| exact-body-recovery/input.json | 81475a04de77c7a65077d2b0722d297c533a8c21441ca8dfc2881a3c9833b5e5 |
| native-binary-02/module_preflight.exe | 90ca34afa0da078a4fe843dbfa1eba809665037b183ce8d5979d18fb19d62236 |

The already adopted independent actual audit is in
`research/cycles/v5-2026-10-07/ASSURANCE.md`, section
“Native-controls01 and provider-contract01 actual audits.” Current saved outputs
still report the exact expected demand and conditional recovery, both passing.

## Applicability to the current installed native boundary

Do not claim the old and current executables are byte-identical. They are not:
the diagnostic links `native-library-01`, while the installed `native_delta`
links `native-library-02`. The selected distribution map identifies
`delta-native-build-02/native_delta.exe` at
`37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40`.
Its linked library02 is
`ba6d0db2e614c2bb032ca5d92d97d31a7ebfe87f85fa6cce6fe5549483b7c651`.
Both files were rehashed and match their preserved build/selection evidence.

The decisive semantic sources are byte-identical across the two library
selection pins, both executed build snapshots, and current canonical source:

| Checker source | SHA-256 in all five comparisons |
|---|---|
| env.rs | 297dfad97a923fea15f4dd5f6d65d76893c109528292264ab7bb2b7cb9403192 |
| tc.rs | f1b5f2e15f231aea52ae3452435c2b91a69a6baf8c010f68214b3e0cf57fa52b |
| module.rs | 6c9b6acbf0cae9698b9fa035bad38df8c1e307dd1e78d6971b27f58511c58455 |
| demand.rs | 6ec3a6b4acc0a38bfbda0bd09393435954f3fe7a1f99ba026c92d5e2e00b0d1d |

Comparing the complete library01/library02 source pin sets finds only two changed
Rust files, plus added Cargo metadata. Reading the actual snapshot diffs shows:

1. `parser.rs` adds `Debug/PartialEq/Eq` and `decode_corresponded_owned_row`, an
   outer-row decoding fast path. It retains the same inner enum deserialization,
   `moduleImportDef` variant, `Definition` construction, body hash and hint.
2. `module_correspondence.rs` replaces repeated JSON tree-copy construction with
   direct tagged-array construction. Missing-import kind/hash/hint validation,
   declaration roles and checking order are unchanged.

The installed `relation.rs` checks exact correspondence and body commitments,
then calls the same `check_module_extension_conditional`. It does not synthesize
the value of a missing definition. When type conversion calls
`ValueSlot::Missing.require`, unchanged `demand::body` unwinds instead of
returning a value. The installed `delta/native.rs` catches that unresolved
demand and returns `REFUSED / CHECKER_PANIC_OR_UNRESOLVED_DEMAND` with false
admission, exit 2. It does not serialize a checked conditional conclusion.
The receiver requires that checked conclusion before issuing a warrant.

Thus the retained negative supplies actual evidence for the unchanged kernel
boundary, while exact source comparison and the current driver's fail-closed
control flow supply the cross-version applicability argument. This is not a
claim that the old diagnostic reran on the current executable or that the new
full client path has already passed an identical runtime negative.

## Consequence for current work

The new interface-view controls already establish that final source emission
keeps the original missing definition descriptor/hash/hint, rather than the
frontend's opaque surrogate. Combining that changed-boundary evidence with the
unchanged native demand behavior is the higher-payoff assurance route.

Prioritize the separately selected positive integration: a real frontend uses an
absent definition abstractly and the existing final checker accepts its exact
body-independent contribution. Do not repeat old fold recovery, invent a second
negative harness, or build another checker. Reopen a negative-runtime decision
only if a future change touches the missing-value semantics, final descriptor
emission, correspondence/role enforcement, or fail-closed receiver branch.
