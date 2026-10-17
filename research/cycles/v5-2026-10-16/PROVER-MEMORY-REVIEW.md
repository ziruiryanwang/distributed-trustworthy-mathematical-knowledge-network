# Independent retained CPU prover memory review

**Decision: do not fund an unchanged `po2=19` segment proof under a 4 GiB
Job limit.** Its persistent C++ constructor allocations alone exceed that
limit. This remains true if Rust's oversized preflight vector is corrected or
entirely released. No experiment is necessary to settle this profile.

2026-10-16, `memo_independent_review`, independent challenge coordinated with
`v5_growth_decision`. Source/data review only: no SDK edits, imports, build,
execution, proof or Git mutation. Canonical root used throughout. This is a
lower bound for the retained CPU implementation, not a lower bound for every
possible prover algorithm, an observed peak or a newly authorized allocation.

## Actual path and units

Let `SDK` denote the retained source directory
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8`.
Source references below are relative to it; `CXX` abbreviates
`risc0/circuit/rv32im-sys/cxx`.

The selected stage host calls `prove_segment` on the actual capsule segment.
The retained server's `prove/prover_impl.rs:218,238` creates Rust preflight and
then calls `segment_prover(po2)` **while owning that preflight**, before calling
`prover.prove(&preflight_results.inner)`. `risc0/circuit/rv32im/src/prove.rs`
exports the Rust preflight, not `preflight_cxx`, and selects CPU on this Windows
build without `cuda`. Retained fingerprints for circuit `5583c41cc4b1f748` and
sys `f53cb91133411b30` show `execute/prove/std` and `prove`, respectively, with no
CUDA feature. The selected zkVM fingerprint `e4b4822463e0ff62` has the retained
`commons-inprocess-only` and `disable-dev-mode` features.

`CXX/hal/hal.h:157` multiplies typed element counts by `sizeof(T)`.
`Fp` contains one `uint32_t`; `Digest` contains eight, so their sizes on the
selected ABI are 4 and 32 bytes. `CXX/hal/cpu/hal.cpp:55` uses a fresh
`new char[size]` and `memset` for each buffer; these are distinct owned CPU
allocations, not views of one reused arena. The owning `shared_ptr` buffers
remain members of `Rv32imProver`, `Prover` and its `PolyGroup`/`MerkleProver`
objects. The construction sequence allocates all of them before witness
computation starts.

## A stronger, Rust-independent lower bound

Put `N = 2^po2`, and let `D` and `A` be the data and accumulation column counts.

**Data:** `CXX/rv32im/emu/blocks.cpp:86` takes the maximum of
`base + count + count * sizeof(Block)/sizeof(Fp)`. The selected circuit has
43 block kinds plus Empty, so its major/minor selector sizes are 6 and 8.
`P2IntRoundsBlock` contains `1+24+21+21+24=91` scalar registers and has count 2.
Its `ArgCountContext::RegImpl` contains one `Fp`. Therefore
`D >= 6+8+2+2*91 = 198`.

**Accumulation:** the same file's `computeMaxAccumPerRow` computes
`4 + 4*ceil(max_argument_count/2)`, then `computeTotalAccum` adds the top
accumulator. `InstLuiBlock::addArguments` in `CXX/rv32im/circuit/inst.ipp:672`
unconditionally performs two pulls and one push. `ArgCountContext` increments
on each, and nested fields can only add more. There are nine InstLui slots per
row, hence the maximum argument count is at least 27. The top accumulator is
`7+1+4*4=24` scalar registers (`top.h:34`, `regext.h:20`). Consequently
`A >= 4 + 4*ceil(27/2) + 24 = 84`.

`Rv32CircuitInfo` adds a distinct tap for every column. `Prover` allocates a
table and a separate coefficient matrix for each group; `PolyGroup` allocates
its separate fourfold expansion. Thus both groups require at least
`4*(1+1+4)*(D+A)*N >= 6768*N` bytes. `gs.expTable` aliases the expansion and is
**not counted again**.

Additional distinct persistent allocations give:

| Allocation | Lower-bound bytes per row |
|---|---:|
| Both groups' table, coefficients and fourfold expansion | 6,768 |
| C++ aux: P2Block witness 204 bytes times three slots | 612 |
| `checkRaw`: four columns on a fourfold domain | 64 |
| Check `PolyGroup.expanded`: 16 columns on a fourfold domain | 256 |
| Three Merkle trees: data, accum and check, each `2*(4N)*32` bytes | 768 |
| **Total, excluding Rust preflight** | **8,468** |

The check coefficient matrix is a reshape/view of `checkRaw`, so it is counted
once, not twice. The three trees are separate arrays. All these members coexist
at the end of the constructor; local handle destruction does not free buffers
still owned by `polys`/`groups`. The bound excludes row metadata, lookup tables,
FRI, combo arrays, temporary evaluation data, transcript, capsule, runtime and
allocator overhead.

At `po2=19`:

`8468 * 524288 = 4,439,670,784 bytes = 4.134765625 GiB > 4 GiB`.

The excess is 138 MiB **before** the excluded allocations. The selected CPU
constructor cannot complete within that memory cap. Returning from constructor
failure, encountering an earlier limit or terminating cleanly cannot make it a
successful proof. A higher CPU/time budget does not address this obstacle.

## Rust preflight: confirmed unit mismatch and lifetime

`preflight.rs:39` computes the maximum witness size in **bytes**, but line159
uses it as the number of **u32 elements** per row. Independently pairing all
43 generated witness size assertions with the block-count header gives maximum
612 bytes (P2Block: 204 times 3); next-largest is 528. Current allocation is
therefore `2448*N` bytes. `Vec::truncate` at line178 changes length, not capacity.
That vector remains owned across the C++ constructor and its FFI proof call.

The stronger retained-implementation lower bound is consequently
`(8468+2448)*N = 5,723,127,808 bytes = 5.330078125 GiB` at po19. This is still
only a lower bound, **not** evidence that 6 GiB or 8 GiB is sufficient.

In principle, dividing the maximum byte size by four is semantics-preserving
for this trace representation: `Trace::add_block` reserves
`count_per_row * sizeof(Witness)/sizeof(u32)` words for each new row, every
witness size is divisible by four, and no successful trace allocates more than
`N` rows. A zero-initialized `153*N`-word vector therefore supplies the same
accessible witness prefix and padding for every successful original trace.
Neither the circuit, guest mathematics nor statement need change. This is a
capacity argument, not implementation/test clearance for an SDK patch.

Even that correction leaves the lower bound `(8468+612)*N = 4.43359375 GiB`.
Releasing Rust's vector completely cannot lower the C++-only 4.134765625 GiB
bound. Moreover, current FFI still needs the vector for its input copy, so simply
dropping it before constructing the prover would be invalid.

## Design consequence, without an unselected rewrite

- A unit fix is worthwhile as a future narrow SDK maintenance candidate, but
  is **not the solution** to fitting this po19 implementation within 4 GiB.
- Releasing witness/aux data after its last use can preserve semantics, provided
  every buffer owner and captured callback is handled. Releasing it only after
  witness generation does not avoid the current earlier constructor peak.
- A 4 GiB po19 backend would need a different allocation schedule, buffer reuse,
  streamed/out-of-core operation or another backend, with a new memory proof and
  implementation qualification. Cryptographic soundness does not authorize
  arbitrarily aliasing live buffers. This review selects none of those changes.
- Smaller actual segments scale this particular lower bound down, but do not
  establish an upper bound or affordability. Existing po19 capsule segments
  cannot be relabeled as smaller proofs. Geometry/session identity and execution
  replay remain explicit costs, under the separate small-segment investigation.
- A separately provisioned higher-memory proving role may be simpler than an
  SDK rewrite. Its admissible memory envelope must be justified; the present
  lower bound neither selects a new cap nor establishes one as sufficient.

The efficient next decision is therefore between honest producer provisioning
and a smaller-segment production path, not a doomed 4 GiB proof attempt or an
unjustified memory-cap ladder. Receiver-side succinct verification and the
mathematical acceptance policy are unchanged by this producer feasibility issue.

## Reproducibility pins

The argument reads the retained selected build tree, under the existing
source-to-binary/toolchain trust assumptions; it is not binary decompilation or
a new formal compiler-correctness proof. Key source identities are:

| SDK-relative source | SHA-256 |
|---|---|
| `risc0/circuit/rv32im/src/prove/preflight.rs` | `bf427f0e3964756d66024bb66e7952bd6544d52d0c6f68b008e85aa1ad228bde` |
| `risc0/circuit/rv32im/src/prove/preflight/trace.rs` | `3d7b6c4271f8526ffd83d8107b267731855b89fdcf521b3cbf8ce96b004fbbb7` |
| `risc0/zkvm/src/host/server/prove/prover_impl.rs` | `f0d76ebe18a69798158ac475e3ce0357f8d96448fe9dcf9bb5fe9649f64613e2` |
| `CXX/rv32im/emu/blocks.cpp` | `8422904a9d0a14495fdaf169ab37bc4d4cb2f4bf253250c1ffcfabe48d22f7c3` |
| `CXX/rv32im/circuit/inst.ipp` | `36ff14da178f0f5d358fefeae112e0653926bced3a3f1709b27db6b7caa69b95` |
| `CXX/prove/rv32im.cpp` | `3b901b6906efea997651fa4b55caa8dc43fc2cca5869c37c952e203281fe38ad` |
| `CXX/prove/prove.cpp` | `cca2f379c4f4de11ed588e6f458c65089eb4c2de5802369909a15614363383b1` |
| `CXX/prove/poly_group.cpp` | `9c513875a6e648177f47a8a5314705f6f2684deffe89098225c80be3270028e7` |
| `CXX/prove/merkle.cpp` | `56b94abda6283983af8a5c4fd892dbb31b96c681b0989bc2a7670847532c933b` |
| `CXX/hal/cpu/hal.cpp` | `9f550352ad5cdcfa3e9038a4bdda1a5d9bae447b2e7fc11db2853dc37c6cf1d3` |

Actual generated binding assertions are in the retained target's
`release/build/risc0-circuit-rv32im-sys-93d06bb7698b10ee/out/bindings.rs`, SHA-256
`8a87f54abff64918f0d4a4bda5c87879b4b2b6e1a2846162e1757eb77727a054`.
No source or retained proof artifact was changed to obtain this result.
