# Standalone old/new constructor differential

Source-only plan. Root selects compilation and then a separate bounded actual
run after independent review. No compiler/checker/prover is launched by this
plan. It compares the constructor seam, not whole mathematical acceptance.

`correspondence_move_differential.rs` is 9,272 bytes, SHA256
`a96000ac637bdcc81b269482dd1332b7e81cf8aa1c5566485c5f68d0032ace7a`.
It imports only std, serde (through the included modules) and serde_json.
No Nanoda arena/typechecker, guest/backend, Lean exporter or network code is
linked. Both exact correspondence sources compile in the same executable:

| Input | SHA256 |
|---|---|
| Frozen guest02 `project/modules/native/checker/src/module_correspondence.rs` |`8f77984f670a8da23b889059fc4650d7c8bcf43fa21675b0994ffde7cd431597`|
| Mutable successor, snapshotted before compile |`f37c855666480553ee9b95f59dc3ba7ad19316e8e707aacd47fecfa29f1d12e2`|

The predecessor is an exact absolute `#[path]` to the frozen guest02 snapshot.
The successor is a relative `#[path]` resolving inside the root-selected new
source snapshot. Compile selection must pin the old source as a read-only
runtime input and preserve the successor's source topology. Recheck both source
and executable bindings before/after the actual run; never reinterpret a
generic success file as test output from another binary.

## Small direct build

Use the held rustc and native serde/serde_json dependencies, without Cargo or a
checker rebuild. The already used direct native externs are:

```text
experiments/general-checker-01/build-01/target/release/deps/libserde-d2875ea8be5e26d6.rlib
experiments/general-checker-01/build-01/target/release/deps/libserde_json-d8d8d972d853b6e4.rlib
```

Select their exact retained dependency closure and compiler/linker origins.
Use Rust2021, overflow checks, panic unwind and retained LTO-compatible link
flags. Do not repeat the known failed unassisted VCTIP lifecycle: root's build
wrapper must preserve bounded Job ownership and the reviewed exact-image
telemetry cleanup policy. No successful build or executable hash exists yet.
Native serde_json may be a different selected retained build from guest
serde_json1.0.151; both sides must use the same native dependency. Actual guest
equivalence still rests on the independently reviewed same-Value construction
argument, followed by any separately selected guest comparison.

`build_correspondence_test.py` now supplies the fresh compile-only adapter.
It uses the retained `phase_class(p,a)` monitor with
`allow_build_telemetry=True`, whose only exceptional successful-build cleanup
is an exact remaining Job-owned, image/hash-pinned VCTIP process. Unknown
descendants refuse. The underlying Job has4096MiB/eight-process limits;
workerCPU/phase-wall180seconds and total allocation-wall300seconds are selected,
with6GiB accounted storage. Its retained no-credential environment is unchanged.
Invocation requires `D:\Python314\python.exe -B -I -S`, then the absolute
adapter, exact selection path and SHA256. No test executable is run by it.

The bounded retained runtime reference is `native-binary-02-selection.json`,
SHA256 `bbd704986fc50956376017ea8f2e578d875849dccca41528af9f9762b6dbcbba`.
The adapter selects its explicit runtime pins except the three Nanoda rlib/rmeta
records; it does not infer success from that historical build's failed lifecycle.
All selected files are size/hash-rebound before and after compilation; both
direct externs must occur in that exact map. This is not a census of the giant
cryptographic backend or a claim that every file in a compiler search directory
or the Windows OS is hermetically pinned. That scope is stated in the result.

Four current source/plan files are copied to a fresh exact source topology;
the exact predecessor is additionally copied under `previous-source/` while
its absolute include origin is independently rebound. No old source is edited.
The new allocation is `experiments/v5-local-checks/correspondence-differential-build-01`;
its separate attempt record retains even preallocation failures and identifies
overlapping controller costs so they are not double-counted. Runtime still
requires independent source/exact-selection review and root's launch.

## Exactly eleven cases

Five positive inputs are the retained new-policy `native.json` files under
`experiments/v5-local-checks/receipt-prepare-01/prepared/`:

| Module | Bytes | SHA256 |
|---|---:|---|
| base |99747|`16963893ecd12a3a44181fd40c328ecb7c6f34551cfd957d30c972c3735b8358`|
| fusion |105959|`217156a2168bab58a712f75ee2e4252b1ccca3ccb525907f19734c090c9d4dd4`|
| fold_map |103693|`636caebafe8265ec30596214a79a66ee400591d044a06ae1303f464da2e30f1b`|
| fusion_map |109204|`0318029911b271407551d76ce96ad4a12a0cd44068150a35d299c8229631fd10`|
| project_summary |105365|`fb8eb0efbffa41cc9a98a2f12d42a5d308be3b8f6e59eff278348ebbc0fae8d8`|

Six fresh mutations of base target exactly type equality, body equality,
universe count, proof forward/self DAG reference, proof binder style and
unbound level parameter. These test the changed construction paths' retained
guards. They do not claim to retest kernel false-proof rejection, signatures,
receipt resolution or every grammar branch. The held base has no let expression;
the let-constructor equivalence is source-reviewed, not runtime-covered here.

Both public correspondence functions receive equivalent deserialized groups,
bodies and the same immutable rows. Compare every returned field, including
every expanded body obligation, using normalized Value equality. Compare exact
panic payloads and require each expected boundary marker; matching two wrong
successes is not a negative pass. Unexpected harness failures retain ordinary
panic diagnostics. Sequential calls restore the panic hook before assertions.
Each case writes one common exact input and one complete compared result, not
two duplicative copies. A 16MiB worker stack matches the held diagnostic profile.

Run command, after root binds the actual executable:

```text
HARNESS_EXE FRESH_OUTPUT BASE_NATIVE FUSION_NATIVE FOLD_MAP_NATIVE
            FUSION_MAP_NATIVE PROJECT_SUMMARY_NATIVE
```

Paths must be exact absolute canonical fixture paths, in that order. Suggested
small-check run allowance:30 CPU/60 wall seconds,512MiB,two processes and1MiB
stdout/stderr each. Input files have a separate2MiB cap. The harness has no
child processes, network, Lean/kernel execution or proof calls. Root's operation
supervisor, not this source harness, supplies time/memory containment.

Success is only `PASS_OLD_NEW_STRUCTURAL_EQUIVALENCE_ONLY`, five positives and
six negatives. No speedup is inferred from a tiny native run; actual guest
cost and cryptographic admission remain separate gates.
