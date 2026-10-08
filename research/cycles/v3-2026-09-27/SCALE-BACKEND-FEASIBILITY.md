# First backend discriminator: RISC Zero and pinned Lean 4.34

2026-09-27. `v3_efficiency`, bounded primary-source inspection commissioned
by root. Status: **source-level candidate assessment; no SDK install, source
checkout, build, guest execution, cryptographic proof or benchmark**.
Canonical guard passed; all project changes are confined to this Markdown
checkpoint and the separately assigned integrated-design review.

## Decision

**RISC Zero has a concrete source-backed route for recursive execution
certificates and documented C/C++ guest support. Keep it as the first bounded
backend candidate. It is NOT presently a GO for an immediate full Lean 4.34
kernel-in-VM implementation or a tentative-v3 scale claim.**

The source-level discriminator is negative for the proposed shortcut “compile
the existing Lean checker into a supported C++ guest.” The checker is a mixed
C++/generated-Lean/runtime dependency closure, and the normal runtime actively
initializes OS/thread/process/I/O/event-loop facilities. No guest-compatible
closed build/initialization path was established in this inspection. C++
language support alone does not discharge that blocker.

This is a **NO-GO for selecting an immediate full-kernel port on the available
evidence**, not a theorem that Lean cannot run on this VM. The sources include
useful single-threaded and built-in-bignum options; a future deliberately
bounded port is plausible but remains engineering and semantic-validation work.
Do not promise it overnight or silently replace real kernel checks by a host
success bit.

The immediate coding choice remains the native-only certified-interface seam
already specified by the Lean-interface investigation. For cryptographic work,
root should choose either a separately bounded runtime-port contract or a
restricted proof-oriented checker with an explicit Lean soundness connection.
Do not start an open-ended whole-Lean port by calling it routine integration.

## Exact source pins and evidence scope

Read-only GitHub commit/tree/raw-file requests were made without downloading
a repository or executing source.

| Project | Inspected revision | Observation |
|---|---|---|
| `risc0/risc0` | `3bbcd44d6459b9ef6ac0df3846dc9215514934e8` | `main` resolved to this revision; commit dated 2026-07-20, subject “Update guest building docker image to 1.97.0”. Its `risc0/zkvm/Cargo.toml` declares `risc0-zkvm` version `5.0.0`. This is a pinned source inspection, not a claim of a qualified release installation. |
| `leanprover/lean4` | `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` | The requested v4.34 lineage commit exists; dated 2026-09-14, subject “[Backport releases/v4.34.0] chore: update to mimalloc 3.4.4”. Actual kernel/runtime sources inspected at this revision. |

The repository's prior zkPi check remains separate: its example pin is
Lean `4.8.0-rc1`, not this Lean revision. No new compatibility inference is
drawn from zkPi in this assessment.

Local command lookup found no `cargo`, `rustc`, `clang`, `clang++`, `cmake`,
`ninja`, `lean` or `lake` on PATH. `wsl.exe` was present, but no distribution,
compiler or SDK was invoked or established. The project's local
`software/runtime/lean-4.34.0-windows/bin/lean.exe` does exist. These scoped
observations do not prove that no alternative installation exists elsewhere.
In particular, a Windows Lean executable is not an RV32IM guest image.

## What the SDK actually offers

At the pinned RISC Zero revision:

- `website/api/zkvm/rust-crates-with-cpp.md` documents a GCC-based guest C++
  toolchain targeting `riscv32im`, usable from a Rust crate's build script.
  It explicitly warns that not all C code works out of the box and that the
  VM is single-threaded; its BLST example uses a `no_threads` option.
- `examples/c-guest/README.md` provides a pure-C example but labels it
  experimental and not extensively tested. It requires the Rust/toolchain
  setup; its existence is not a ready build of our checker.
- The VM specification documents RV32IM and a single-thread execution model
  without normal scheduler/atomic-instruction support. The current document
  also contains old/new machine-mode descriptions, so this note does not use
  its prose as a complete audited ISA specification. Actual guest ABI and
  memory/instruction semantics need version-pinned qualification.
- `risc0/zkvm/src/guest/env/verify.rs` implements `env::verify(image_id,
  journal)`: hash the specified journal, construct the corresponding normal
  receipt claim, and record its claim/control-root assumption through the
  verification syscall and guest assumption accumulator.
- `examples/composition/src/main.rs` supplies a prior receipt with
  `ExecutorEnv::builder().add_assumption(...)`; its guest calls
  `env::verify(expected_image_id, expected_journal)`. Host proving produces
  a final receipt, then host verification checks the expected image.

The last two facts establish a concrete composition seam: the new prover
can consume existing parent receipts rather than execute each parent guest
again from its original witness. They do **not** establish our exact Lean
relation, an adaptive cryptographic security bound, successful local builds,
proving costs, or the absence of historical-data access in our future program.

## The receipt traps that must be designed out

### Conditional evidence is not finished composition

The composition documentation explicitly says that guest verification first
adds assumptions. Those assumptions must then be resolved. It describes
automatic resolution for succinct/Groth16 proving options. The current
`prover_impl.rs` imports and uses recursion operations including `resolve`;
the exact full prover flow was not independently security-audited here.

The receiver must accept only a complete receipt for the selected claim,
with no unresolved assumptions. `Receipt::verify_with_context` checks the
inner proof and the digest of `ReceiptClaim::ok(expected_image,
expected_journal_digest)`. The constructor fixes normal successful exit,
empty input commitment and empty assumptions. This is much stronger than
testing an arbitrary claim's cryptographic integrity without checking which
program, output and success state it describes.

`env::verify_integrity` and especially lower-level `verify_assumption` are
not interchangeable application APIs. The latter explicitly says it does
not check the claim's semantic fields. Use the narrow expected-image/journal
binding or reproduce its full claim checks; do not import an attacker-chosen
claim/control root merely because a seal verifies.

### A verified receipt is not necessarily succinct

`InnerReceipt` includes:

- `Composite`: explicitly non-succinct, one receipt per execution segment;
- `Succinct`: a single STARK receipt for the computation;
- `Groth16`: a single Groth16 receipt, with that construction's additional
  assumptions and parameters;
- `Fake`: development evidence with no cryptographic integrity.

`receipt/composite.rs` stores segment receipts and assumption receipts, loops
over every segment, then verifies every attached assumption receipt. Thus a
successful generic `Receipt::verify` is **not by itself evidence that the
receiver cost is independent of a large collection of subproofs**.

For the first scale candidate, select an actual finalized `Succinct` receipt
with bounded encoding/journal and pinned verifier parameters. A Groth16 wrapper
can be a separate measured/security choice; it is not needed just to claim
the existence of composition. Do not admit `Composite` under a “succinct”
profile, and do not accidentally attach full ancestor receipt trees outside
the succinct claim. The producer also requires already finalized parent
receipts so its operation does not grow a hidden ancestry-verification tree.

### Fake/dev mode must never qualify acceptance

`FakeReceipt::verify_integrity_with_context` returns success when the verifier
context enables dev mode. Default contexts can read the development-mode
environment. Therefore “the SDK verification call returned Ok” is insufficient
experimental evidence unless the receipt kind and verifier configuration
exclude that path.

The future profile must reject `Fake`, explicitly disable development mode,
and pin the build/features/context. The SDK exposes `disable-dev-mode` and
`with_dev_mode(false)` mechanisms; their exact build and environment behavior
must be checked in the selected adapter. A mocked success, executor-only run,
or fake receipt cannot pass the crypto gate even for an otherwise valid theorem.

### Self-recursive image binding must not be attacker-selected

The guest must constrain every child receipt to an allowed relation/image and
the exact child journal, not just accept a host-supplied image ID. For a
self-compositional checker, its expected image/profile may be carried in the
committed public configuration and compared across parent/child claims; the
top-level verifier independently pins that configuration to the actual guest
image it verifies. This avoids demanding a binary literally embed the hash
of its own final binary, while avoiding arbitrary-image certificate laundering.

No proof of successful VM execution fixes an incorrect guest program. The
guest must recompute the canonical interface commitments, enforce base/policy
and rank rules, run the real checker for the new proof, and emit exact outputs.
It cannot outsource the new check to an untrusted host `true` response.

## Actual Lean dependency boundary

The pinned local `Lean/Environment.lean` declares checked `addDeclCore` through
`@[extern "lean_add_decl"]`. The upstream source shows what that entails:

| Source fact at the pinned Lean revision | Consequence for a guest port |
|---|---|
| `kernel/CMakeLists.txt` includes level/expr handling, substitution, local contexts, declaration/environment/type checker, quotient and inductive logic, caches and initialization. | Not one self-contained theorem-checking C function. The accepted fragment must specify which paths are included, not simply omit inconvenient checks. |
| `kernel/environment.cpp::lean_add_decl` installs heartbeat/recursion/cancellation scopes and calls real `environment.add`; the no-check variant is a distinct entry point. | The guest must call the checked path and preserve its limits/refusal semantics. Replacing it with `lean_add_decl_without_checking` would prove the wrong relation. |
| `add_theorem` checks declaration name/universes/type, Prop membership, no free/metavariables, actual proof typing and definitional equality. | A faithful theorem guest must include these checks, not just type-header validation. |
| `environment.cpp` calls external `lean_environment_add/find`, quotient-state and diagnostic functions supplied from Lean-generated code; `expr.cpp` also calls external Lean representation helpers. | The native C++ objects depend on generated Lean code and its object/runtime ABI. Copying only `kernel/*.cpp` is not a complete port. |
| `runtime/CMakeLists.txt` includes memory/object/application/bignum handling plus I/O, process, threads, stack handling, libuv networking/event-loop files and OpenSSL support. | The ordinary runtime build is substantially broader than the desired pure checker. Not all linked features are necessarily logically required, but exclusion must be an actual closed supported build, not a promise. |
| `runtime/init_module.cpp::lean_initialize_runtime_module` actually calls allocation, object, I/O, thread, mutex, process, stack-overflow and libuv initialization. | This is not merely a dead-file-list concern. A minimal guest needs an audited initialization/dependency plan or compatible implementations. |
| `runtime/thread.h` has a `LEAN_MULTI_THREAD` branch and a no-multithreading fallback; CMake can disable `MULTI_THREAD`. | Single-thread support is a positive porting ingredient, not proof that every runtime/atomic/TLS assumption disappears. |
| CMake can disable GMP; `runtime/mpz.h` then uses the built-in `mpn` representation. The pinned CMake also warns that old GMP versions can be unsound. | GMP is not an unavoidable external dependency. Do not invent a GMP blocker, but do audit whichever integer implementation and word-size behavior are actually used. |
| `include/lean/lean.h` explicitly discusses 32-bit as well as 64-bit object layouts. | RV32 is not rejected here merely because current product execution is Windows64. Correct canonical decoding/object layout, generated-code ABI, size limits and arithmetic still require validation. |
| `kernel/type_checker.cpp` consults kernel resource settings, including the numeral-size bound initialized using `LEAN_NAT_MAX_SIZE`. | The deterministic proved relation must pin/validate semantically relevant guest configuration and limit behavior rather than inherit arbitrary host environment values. |

C++ exceptions/standard-library behavior, allocation/object ownership, TLS,
generated Lean initialization, stack/heartbeat behavior, supported libc calls,
and the selected bignum implementation remain part of the unresolved guest
closure. This assessment does not claim each is inherently incompatible. It
establishes that no supported closed port was demonstrated by the docs/examples
inspected and that the normal build is not already such a port.

## Concrete GO/NO-GO result

| Discriminator | Result |
|---|---|
| Documented C/C++ guest toolchain exists | YES, source-backed, uninstalled and untested here |
| Concrete recursive receipt API and assumption-resolution path exists | YES, source-backed, not independently proven or run here |
| Receiver can select finalized succinct rather than composite/fake receipts | YES in the inspected API; exact adapter still absent |
| Actual pinned Lean checked-declaration program and full guest dependency closure identified/buildable without unreviewed stubs | NOT ESTABLISHED; normal runtime initialization has unresolved guest dependencies |
| Exact canonical bridge, sealed import/axiom discharge and guest image/profile binding implemented | NO |
| Local Rust/SDK/C++ guest build environment demonstrated | NO |
| Real Lean certificate generation, independent verification and next-generation composition measured | NO |

Overall: **NO_GO_IMMEDIATE_FULL_LEAN_GUEST; RETAIN_RISC_ZERO_AS_BOUNDED_CANDIDATE**.
This prevents an unsupported implementation promise while preserving the
positive composition/toolchain evidence.

## Next action that can change the decision

Complete the bounded native sealed-interface test already selected. Its output
should pin an exact new-declaration input, certified-premise interface plan and
checked-output commitment without requiring historical bodies. This isolates
the semantic seam before any expensive proof backend work.

After that, root must select one of two concrete code contracts:

- **Port contract:** extract a minimal deterministic checked-declaration guest
  closure from this exact Lean revision, explicitly resolve generated Lean
  exports/runtime initialization and prove that no unchecked host-return path
  supplies mathematical authority. The first gate is a reproducible guest build
  and exact positive/ill-typed differential result, not full-library execution.
  Failure to close the dependency manifest within the fixed allocation stops
  the port; it does not trigger unbounded platform surgery.
- **Restricted-checker contract:** implement a standalone, explicitly limited
  certificate/checker relation whose accepted propositions have a checked Lean
  soundness/translation connection. Run that exact deterministic checker in a
  real succinct backend and compose it with certified premises. This can be
  a genuine scalable supported fragment, but must not be called arbitrary
  Lean4.34 checking. A hard-coded allowlist of true test theorems or a syntax-only
  checker is not the substitute.

Only after the selected first actual proof exists should the next gate add
one real parent receipt, produce a finalized child receipt, reject wrong-image/
wrong-journal/unresolved/fake evidence, and measure receipt-only cold checking
plus a substantive downstream Lean use. A receiver-only benchmark that leaves
new proof production dependent on old histories still fails our project goal.

No backend runtime was installed or run in this assignment. No paid/cloud
prover is selected. In particular, the example's `default_prover()` invocation
is not authority to use an externally configured service in a future test;
the test must explicitly bind its execution and accounting environment.

## Primary-source navigation

All RISC Zero links below are pinned to `3bbcd44d6459b9ef6ac0df3846dc9215514934e8`:

- [C++ guest support](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/website/api/zkvm/rust-crates-with-cpp.md).
- [Experimental C guest](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/examples/c-guest/README.md).
- [Composition explanation](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/website/api/zkvm/composition.md).
- [Guest verify and assumption APIs](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkvm/src/guest/env/verify.rs).
- [Host composition example](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/examples/composition/src/main.rs).
- [Receipt verification, kinds and dev mode](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkvm/src/receipt.rs).
- [Composite receipt verification loops](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkvm/src/receipt/composite.rs).
- [Normal successful receipt claim](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkvm/src/claim/receipt.rs).
- [Prover implementation](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkvm/src/host/server/prove/prover_impl.rs).
- [VM specification](https://github.com/risc0/risc0/blob/3bbcd44d6459b9ef6ac0df3846dc9215514934e8/website/api/zkvm/zkvm-specification.md).

All Lean links below are pinned to `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`:

- [Checked environment/declaration implementation](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp).
- [Kernel build list](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/CMakeLists.txt).
- [Kernel type checker](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp).
- [Runtime build list](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/runtime/CMakeLists.txt).
- [Runtime initialization](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/runtime/init_module.cpp).
- [Build options, including threading/GMP](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/CMakeLists.txt).
- [Threading alternatives](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/runtime/thread.h).
- [Integer representations](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/runtime/mpz.h).
- [Object/runtime header](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/include/lean/lean.h).

Sources establish the specific capabilities and unresolved dependencies above;
they do not supply our missing deployment security proof or performance data.
