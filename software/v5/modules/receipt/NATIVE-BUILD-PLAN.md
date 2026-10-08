# Native wrapper: exact retained build plan

Source-only plan under root selection D08. Root owns the actual bounded command,
immutable source snapshot, output directory, resource selection and adoption.
No compilation, metadata pass, guest image or proof is claimed here.

## One adapter, no intermediate wrapper library

Compile `src/bin/receipt_native.rs` directly. Its `#[path]` declarations include
`src/canonical.rs`, `commitments.rs`, `journal.rs`, `policy.rs`, and `relation.rs`.
Snapshot all six with their existing relative layout. `src/main.rs` is the guest
entry point and is NOT part of this native build. Retain Cargo/source files as
review context, but this build need not run Cargo or access the network.

Use the same retained compiler as `native-binary-02`:

`experiments/scale-crypto-01/runs/run-01/rust/bin/rustc.exe`

SHA-256 `9d4ba43cfc3d62c1aa8c3047fbde3b1121ce4603b589e7f710fcc0b3f8e983c2`.

Direct externs, paths relative to the canonical project root:

| Crate | Exact retained file | SHA-256 |
|---|---|---|
| `nanoda_lib` | `experiments/v5-local-checks/native-library-01/libnanoda_lib.rlib` | `b52ee8efe8883b2b6025c08dbcc55a7032a6ec94e87a6adc9d202b0f8587a2c5` |
| `serde` | `experiments/general-checker-01/build-01/target/release/deps/libserde-d2875ea8be5e26d6.rlib` | `47b36c1e7f876deee17c16fe6c580ee4fa4b42794eb8652459c587e1d67143b5` |
| `serde_json` | `experiments/general-checker-01/build-01/target/release/deps/libserde_json-d8d8d972d853b6e4.rlib` | `798e955d92dd8b3141ed5b4b60e054ce65b5c4f58678a933381d3250f01da2cf` |
| `risc0_zkvm` | `experiments/general-checker-host-05/build-01/target/x86_64-pc-windows-msvc/release/deps/librisc0_zkvm-e4b4822463e0ff62.rlib` | `5c5bff2476163fe1fcb6453f9b7d5aa84e1887b349a939ae5fffddd90ee5c434` |

Read selected keys, not the huge whole manifest, from the preserved
`experiments/native-relation-01/build-selection03.json`:

- `dependency_dirs`: use each as `-L dependency=<directory>`.
- `native_link_dirs` and `library_dirs`: use each as `-L native=<directory>`.
- `linker`: use its exact selected Visual Studio linker.
- Existing retained dependency maps identify further runtime pin candidates.
  The local-check runner allows at most 256 explicit runtime pins. Do not claim
  hermetic toolchain closure when only selected files are pinned.

Required compiler parameters:

```text
--edition=2021 --target x86_64-pc-windows-msvc
--crate-type bin --crate-name receipt_native
-C overflow-checks=yes -C panic=unwind -C opt-level=2
-C lto=fat -C embed-bitcode=yes
-C linker=<selected linker>
<six-file snapshot entry path> -o <fresh output>/receipt_native.exe
--extern nanoda_lib=<new checker above>
--extern serde=<above> --extern serde_json=<above>
--extern risc0_zkvm=<above>
<selected -L arguments>
```

Retained SDK dependencies contain LTO-only LLVM bitcode. Omitting final LTO
already caused a preserved earlier linker failure. `--emit=metadata` can cheaply
test source/type compatibility before a separately selected link, but neither
success counts as executing the wrapper relation.

## Build-lifecycle evidence must stay distinct

`native-binary-02/RESULT.json` records compiler exit 0, zero diagnostics, and
23.453125 Job CPU seconds, but **DESCENDANTS_REQUIRED_TERMINATION**. That build
lifecycle remains failed even though root separately adopted its produced
executable for diagnostics. The output includes a PDB; a lingering PDB service
is a plausible hypothesis, not an established cause: that result does not name
the child processes. Do not rewrite it or rerun unchanged native math controls.
The next actual build can record descendant identity or deliberately select
no-debug/no-PDB link behavior if root reviews the exact command change first.

## Next execution boundary

After independent source/build-selection review, root may run one fresh native
wrapper build, then `native_controls.py` and newly repinned binding inputs.
Assurance owns full-relation rejection controls. This still leaves the new guest
build, actual resolved receipts, strict receiving gate, containment and public
reciprocal use as separate central release obligations.
