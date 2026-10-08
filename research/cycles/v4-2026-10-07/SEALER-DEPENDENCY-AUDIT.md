# Compact sealer: retained build/source dependency audit

Independent reviewer `v4_oct7_assurance`, October 7, 2026. Read-only source,
retained build metadata and PE import inspection; **no product, guest, proof,
compiler build, network request or old operation ran**. `dumpbin` inspected
the existing executable without loading it. Old evidence is unchanged.

## Judgment

The specific October 6 concern about omitted segment/lift-only SDK runtime
assets is substantially discharged for the shipped **Windows CPU-only succinct
stage route**: recursion programs are compiled-in bytes, the segment/recursion
provers are statically linked, and the actual executable's direct PE imports
are Windows/API-set and bundled MSVC runtime libraries. The source-free worker
does not inherit external SDK/profiler/authoring configuration.

Thus the source-compositional completion argument need not retain an unexplained
"perhaps external recursion circuits" premise. It still depends on the ordinary
adopted compiler/linker/SDK correctness and Windows platform assumptions. This
is source/build-supported dependency assurance, not a machine-checked proof of
all possible binary behavior or an observed fresh compact certificate. It does
not prove time/memory affordability and does not renew any old proof allocation.

## Exact implementation chain

1. The shipped `receiver/bin/commons-certified-checker.exe` and retained
   `experiments/certified-definitions-04/host-build-01/commons-certified-checker.exe`
   were independently rehashed: both 66,458,624 bytes, SHA-256
   `32356c4f1aa94d0cf1404e23eb092f2bdeb75ab3f88396e90ea88747a54db0a7`.
   The retained host build result identifies the exact host source, `rustc`
   invocation and reused host05 rlibs/native-link directories. It reports a
   successful driver compile, not a mathematical qualification.
2. The exact reused `risc0_zkvm-e4b4822463e0ff62` fingerprint enables `client`,
   `commons-inprocess-only`, `disable-dev-mode`, `prove`, `std`; not `cuda`,
   `metal`, `bonsai`, `docker` or `dual`. The recursion and rv32im fingerprints
   likewise have proving but no CUDA/metal/dual acceleration features.
3. Driver `stage` calls `get_prover_server` with `ProverOpts::succinct()` and
   explicit dev-mode false. The SDK selects in-process `ProverImpl`, not a
   remote service or external prover executable. Direct segment/lift/join/resolve
   methods are used; Groth16/Docker compression is not invoked by this route.
4. `rv32im/src/prove.rs` selects `ProverContext::new_cpu` for this target/features;
   the retained build output records `rustc-link-lib=static=risc0_rv32im`.
   Recursion's dispatch similarly selects its CPU implementation; its build
   output records `rustc-link-lib=static=risc0_recursion_cpu`.
5. Lift/join/resolve names are mapped in
   `zkvm/src/host/recursion/prove/zkr.rs`. The called
   `circuit/recursion/src/prove/zkr.rs` obtains `&'static [u8]` from the
   `risc0_circuit_recursion_zkrs::ZKRS` PHF table and decompresses it in memory
   with `XzDecoder`. Its build script generated `include_bytes!(OUT_DIR/...xz)`
   table entries. **OUT_DIR is a compile-time embedding path, not a receiver
   runtime directory or missing installation asset.** No runtime ZKR download
   or file lookup occurs along this program-selection path.
6. Actual PE `/DEPENDENTS /IMPORTS` reports only `kernel32.dll`, `ntdll.dll`,
   `bcryptprimitives.dll`, `api-ms-win-core-synch-l1-2-0.dll`, `VCRUNTIME140.dll`,
   `VCRUNTIME140_1.dll`, and eight `api-ms-win-crt-*` API sets. No Lean, CUDA,
   RISC0, LZMA or recursion-circuit DLL is imported. The two MSVC runtime DLLs
   are physically present beside the executable (pins below); Windows/API sets
   remain the declared host platform rather than falsely counted payloads.
7. The import table also contains `LoadLibraryA/W`; this does **not** prove a
   missing prover dependency. The retained NVTX source explains one dynamic
   profiling-injection route: on Windows it loads a library only when
   `NVTX_INJECTION32_PATH` / `NVTX_INJECTION64_PATH` is supplied; otherwise the
   extension becomes no-op. `cert_stages.py:555-559,619-624` constructs a fresh
   small worker environment, omitting these variables and external SDK controls,
   and removes Lean paths for nonnative workers. Host DLL injection/compromised
   OS is outside the existing trusted-platform model, not solved by asset maps.

The driver still reads the explicitly bound guest/input/journal/receipts,
snapshot/checkpoints and operation temporary files. Those are required inputs
or owned operation state, not omitted authoring assets. The real snapshot test
already exercised execution; this audit addresses the additional proving paths.

## Independently checked source bindings

SDK root below is
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8`.
All seven listed files were rehashed and match the retained `SOURCE-MAP.json`
candidate rows (zero mismatches).

| Relative SDK source | SHA-256 |
|---|---|
| `risc0/zkvm/src/host/server/prove/mod.rs` | `ab591498199da027edff1a714b681a852229bf95d2a846d6d6f8f4ab7e8cecd1` |
| `risc0/zkvm/src/host/server/prove/prover_impl.rs` | `f0d76ebe18a69798158ac475e3ce0357f8d96448fe9dcf9bb5fe9649f64613e2` |
| `risc0/zkvm/src/host/recursion/prove/zkr.rs` | `8e68c42ce8d620e33e690a21a29b0b85c6e73688c5f5ee0e7e755152e4e25334` |
| `risc0/circuit/recursion/src/prove/zkr.rs` | `b9e842ed49c6b0655ca6a5477e93af1ed491cf9e10a588b293c4df4d396da345` |
| `risc0/circuit/recursion-zkrs/build.rs` | `df4e90dd239b149e10d0b8f64ab896e2880e99a68d7d07fbf0186073c5b6898a` |
| `risc0/circuit/rv32im/src/prove.rs` | `9fa9e9658a9d0242b7db771598a5ce48ac24a6c4894781bd97d80368680fe02e` |
| `risc0/circuit/recursion/src/prove/hal/mod.rs` | `073f7010da02490373bcbfd524e8f743db5bcfa7b0b084a494016750ca9abac7` |

Retained metadata separately rehashed:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| host05 `build-01/SOURCE-MAP.json` | 717646 | `de7671a890c20d4c676c8e2fbd5b0ef054995acdd846f6a8c90dd307f0a728ad` |
| definition04 `host-build-01/RESULT.json` | 9296 | `36c4aeb95e9726f22288d82a1903008e774c4294a426676fd4595d0b85a557b0` |
| zkvm fingerprint JSON | 3422 | `74e3f8070851f0d7941fbcbf530443ffa5e7d8516aa11364d7156c57700866a4` |
| recursion fingerprint JSON | 1947 | `b6f2cfd3fb8d169b1aaaab6a63361bc9bc0fee5434c8f5965a328c93169cbde5` |
| rv32im fingerprint JSON | 2464 | `1be9951c2068edb57834aefff635efed203eadab5acba10ed4f2aa31bbe05b06` |
| shipped `bin/vcruntime140.dll` | 120400 | `052ad6a20d375957e82aa6a3c441ea548d89be0981516ca7eb306e063d5027f4` |
| shipped `bin/vcruntime140_1.dll` | 49776 | `6a99bc0128e0c7d6cbbf615fcc26909565e17d4ca3451b97f8987f9c6acbc6c8` |

Fingerprints are under host05
`build-01/target/x86_64-pc-windows-msvc/release/.fingerprint/`, respectively
`risc0-zkvm-e4b4822463e0ff62/lib-risc0_zkvm.json`,
`risc0-circuit-recursion-4bf141966895b5f7/lib-risc0_circuit_recursion.json`, and
`risc0-circuit-rv32im-5583c41cc4b1f748/lib-risc0_circuit_rv32im.json`.

## Scope and remaining checks

This review reuses the already adopted full build/asset map; it does not pretend
to independently rebuild the compiler or exhaustively verify every standard
library dependency. Hash equality binds the inspected binary to retained build
evidence; it does not prove compiler correctness. The no-external-authoring
claim is specific to the selected stage route, clean worker environment,
CPU-only features and Windows installation. Optional SDK commands/features are
not newly qualified.

The material compact completion claim is consequently an implemented path with
a source/build-preservation justification and prior exact-driver completed-stage
evidence. No fresh compact certificate was produced, and no empirical proving
speedup was measured. The next useful work remains named-library integration,
not repeating a proof solely to cover these unchanged embedded circuit bytes.
