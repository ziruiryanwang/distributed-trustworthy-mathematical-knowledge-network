# Next executable: two-parent recursive equational certificates

2026-09-27, `v3_efficiency`. Root selected **Plonky2 only for a bounded research
discriminator**, not as production trust or a default release mode. This note
is the prospective code/toolchain contract, not execution authority or a passed
test. No toolchain/archive was downloaded to disk, installed or run here; only
read-only local inventory and pinned public text/metadata requests occurred.

## Concrete recommendation

Proceed in two finite gates:

1. Provision an isolated Windows Rust toolchain and build/run exactly one real
   upstream cyclic-recursion proof test at the pins below. This tests the actual
   local host/prover/verifier capability, without porting Lean or using a service.
2. If that passes, implement one general bounded **equational inference circuit
   with two independently certified parents**, its Lean-checked soundness bridge,
   and a three-generation split/join/reuse test. Both imported proofs are verified
   in the new proof; there is no global historical state or full-parent replay.

Stop at the first failed gate. Preserve its source, dependencies, accounting and
diagnostics. Do not spend the deadline porting all Lean/runtime/C++ into a VM,
silently switching to a mock, or relabeling a one-parent sequence as arbitrary
independent-lemma composition.

This is a plausible local research route, **not a guarantee of completion by
03:00 Chicago**. A successful limited lane would not complete the commons goal,
qualify arbitrary Lean proofs or establish useful/exponential knowledge growth.

## Actual local capability

At approximately 18:14 Chicago on 2026-09-27, scoped checks found:

| Item | Actual result |
|---|---|
| `wsl.exe --list --verbose` | Reports Windows Subsystem for Linux is not installed; no usable distribution established. |
| Standard user Rust/zkVM dirs | `.cargo/bin`, `.rustup/toolchains`, `.risc0`, `.rzup` absent under `C:\Users\Uisjs`. |
| MSVC Build Tools | `vswhere` reports complete VS Build Tools 2022 installation at `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`, version `17.14.37411.7`, no reboot requirement. |
| Actual compiler/linker files | `VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe` and `link.exe` exist. No compiler was invoked. |
| Windows SDK | Windows Kits 10 and 8.1 directories exist; exact selected include/lib subversion remains a provisioning preflight. |
| Project runtime | Existing pinned Lean bin includes `lean.exe`, `lake.exe`, `clang.exe`, `ld.lld.exe`, `llvm-ar.exe`, and Lean/LLVM DLLs. Not a Rust or zkVM guest toolchain. |
| Common other locations | No `C:\msys64`, ordinary Program Files LLVM/CMake or Docker installation at the scoped checked paths. Git's `usr/bin` exists. |

This is not an exhaustive machine search. It is enough to reject assuming a
ready Linux zkVM host and enough to identify a realistic isolated native Rust
host route with an existing linker. No host installation, service, WSL feature
change or credential inspection occurred.

## Why this route, not the alternatives

**Full Lean guest:** the previous [backend assessment](SCALE-BACKEND-FEASIBILITY.md)
identified the actual kernel's mixed C++/generated-Lean/runtime closure and active
OS/runtime initialization. A realistic first port gate would require a manifest
of every referenced generated export/runtime object, a single-thread/no-GMP
build policy, explicit allocation/exception/stack/heartbeat initialization and
an actual RV32 checked-declaration build. An upstream C guest is not that gate.
Additionally, the inspected RISC Zero installer documents prebuilt Linux/macOS
hosts, while this machine lacks WSL. That is substantial port/provisioning work
before any Lean certificate; it is not the efficient deadline choice.

**Nova:** inspected Microsoft Nova revision
`01b1e2d662a847ed7029770ecbaf6687398899dd`, manifest version `0.76.0`, provides
real sequential IVC and compressed proofs. It also stores relaxed witnesses
inside its continuation object; a compressed proof alone is not the object
the next prover can simply extend. More importantly, its ordinary sequential
`prove_step` API is not an implemented arbitrary two-parent certificate join.
No such join was supplied by this bounded inspection. Therefore Nova is not
selected for this discriminator. Branching one old sequence twice would not
answer whether independently acquired lemmas can be joined without histories.

**Plonky2:** its checked-in API can place two parent-proof verification gadgets
inside one new circuit. Cyclic verifier-data binding supports a repeated common
inference circuit without embedding the hash of its own final construction.
Its Rust-only application route avoids a Lean runtime port, and the package
manifest explicitly excludes jemalloc dev dependencies on MSVC. Windows build
is still unqualified: upstream CI inspected here runs Linux/WASM, not Windows.
That uncertainty is exactly Gate T, not a hidden assumption.

## Exact pins, security limits and provisioning

Selected source:

```text
repository: https://github.com/0xPolygonZero/plonky2
revision:   5d9da5a65bbcba2c66eb29c035090eb2e9ccb05f
crate:      plonky2 1.1.0 (at that revision)
Rust:       nightly-2025-06-30-x86_64-pc-windows-msvc
host:       native Windows x86_64, existing MSVC linker
```

The repository's `rust-toolchain` says only `nightly`; this contract fixes an
exact date. The official Rust distribution manifest for 2025-06-30 was read
and lists all three needed Windows components as available. Its Cargo version
is `0.91.0-nightly (930b4f62c 2025-06-28)`. Build compatibility with Plonky2 and
resolved crates still needs Gate T. Do not claim the date was tested already.

Official component archive pins from that manifest:

| Component | Exact archive URL | SHA-256 |
|---|---|---|
| rustc | `https://static.rust-lang.org/dist/2025-06-30/rustc-nightly-x86_64-pc-windows-msvc.tar.xz` | `019bc03118ed8458e2c07e3c92064464c658025229fa99ad08c94b847d763abc` |
| cargo | `https://static.rust-lang.org/dist/2025-06-30/cargo-nightly-x86_64-pc-windows-msvc.tar.xz` | `0873084226a9cdacf970c5c4eef5aac741c0e9cdca13764175a39d61f0cab5c3` |
| rust-std | `https://static.rust-lang.org/dist/2025-06-30/rust-std-nightly-x86_64-pc-windows-msvc.tar.xz` | `0a631db9bb2e18d3ee771d230ca0e0836655af9938aa398f75d3c570f13b254a` |

These are archive identities, not proof that the compiler is correct. Preserve
the fetched distribution manifest, archive hashes and extracted maps before use.

Recommended isolated location after root authorization:

```text
E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\scale-crypto-01\
  toolchain\       # portable rustc/cargo/std payload; no user-profile PATH edits
  downloads\       # exact archives + metadata/hashes
  vendor\plonky2\  # exact pinned upstream source, unchanged after first build
  cargo-home\      # this experiment's registry/cache only
  target\          # bounded build outputs
  runs\toolchain-01\
```

Provision by unpacking the three verified component archives into an isolated
prefix according to their inspected component manifests; keep `bin`, `lib` and
`lib/rustlib/x86_64-pc-windows-msvc` relationships intact. Inspect archive paths
before extraction. This avoids installing WSL, Visual Studio, a service or a
system Rust default. Do not run an unreviewed network pipe-to-shell installer.
If component layout cannot be assembled reliably, stop and request a separately
reviewed isolated provisioning method; do not start a machine-wide installer.

Fetch the source archive for the exact revision; record its archive hash and
complete extracted source map before use. The pinned repo has no root Cargo.lock
(the direct contents lookup returned 404), so first resolve dependency versions
into an isolated lockfile and record every dependency checksum before executing
package builds. Cargo dependencies/build scripts are new executed third-party
code; root's provision/build authorization must include this boundary. No paid
API, external prover, Docker or Linux image is needed by the selected route.

Use process-local `CARGO_HOME`, `CARGO_TARGET_DIR`, explicit `RUSTC` and a PATH
limited to the isolated toolchain plus required existing host tools. Initialize
the existing MSVC environment with its `VsDevCmd.bat -no_logo -arch=amd64` in
the reviewed bounded process, or set the inspected include/lib paths explicitly.
Do not print the complete inherited environment. Do not modify user/system PATH,
registry defaults, original project runtimes or prior product installations.

**Security restriction:** this Plonky2 revision is explicitly deprecated and
unsupported. Its README describes a default target of roughly 100-bit conjectured
FRI security and cites a roughly 95-bit estimate for its default Poseidon
configuration. These are the source's caveats, not this project's independently
derived bound. This experiment may demonstrate actual recursive checking; it
does not select a huge-network production security profile. Do not turn up a
FRI parameter and assert that it repairs all hash/security/maintenance issues.

## Gate T — finite toolchain and actual proof capability

Root should authorize one allocation, before writing application circuits:

- One isolated dependency/source resolution and build at the fixed pins. No
  circuit-library source patch or security-parameter alteration after execution.
- Build only the relevant package/test, with `CARGO_BUILD_JOBS=2` and no GPU.
  Freeze Cargo.lock and the complete file map before the proof test.
- Run exactly the selected upstream cyclic-recursion test, which generates
  genuine proofs and checks the cyclic verifier-data binding:

```text
cargo test --locked --release -p plonky2 --lib
  --manifest-path "E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\scale-crypto-01\vendor\plonky2\plonky2\Cargo.toml"
  recursion::cyclic_recursion::tests::test_cyclic_recursion
  -- --exact --nocapture
```

The displayed lines are one command, not separate shell invocations. Do not
run the whole upstream test/benchmark suite. The actual runner must use the
absolute pinned cargo path and canonical workdir, not a rustup shim choosing
an unspecified nightly.

Proposed hard ceilings for root review: dependency downloads at most 1 GiB,
isolated disk at most 6 GiB; provisioning/build at most 45 minutes; proof test
at most 15 minutes and 900 inclusive Job CPU seconds; at most 4 GiB private
commit, eight processes, two build jobs. Stop on unknown/nonquiescent process
state. These are proposed upper bounds, not measured requirements or permission
to expand existing allocations. Record toolchain, dependency, compiler and
proving costs separately from later application costs.

A compiler error, unsupported nightly dependency, memory breach or failed proof
verification is a real failed gate. Preserve it; no automatic latest-nightly
retry, broad source patch or backend switch. Root may choose one diagnosed
fresh continuation separately. A passing test proves only this local backend
capability—not our mathematical relation, two-parent application, product
integration or production security.

The library's cyclic-base/dummy helper is not a mock cryptographic acceptance:
it supplies the internally selected base branch of a real outer proof. For our
application, that inactive-parent branch must be guarded by an actual mathematical
base rule. Never reuse the helper to bypass a required parent or to declare any
chosen theorem true.

## Proposed application contract: EQ-DAG-1

This is a restricted mathematical certificate language, **not an implementation
of the full Lean kernel**. It proves equational entailments about arbitrary
interpretations of a small first-order signature. Its general inference rules,
rather than the names or hashes of test theorems, determine acceptance.

Initial hard limits for a prospective first allocation:

- One-sorted first-order terms; at most four variable symbols and two binary
  function symbols, matching the selected logical-bridge contract. No unary
  or substitution rule is included.
- Terms have depth at most three and use a fixed 15-slot complete binary-tree
  encoding, with root slot zero and child slots `2*i+1`, `2*i+2`. Each slot has
  tag and label limbs: tag zero is a variable (label0..3), tag one a binary
  application (symbol label0..1). All descendants below a variable are
  canonical zero padding; applications at depth three are forbidden. The
  root is always active. There are no attacker-selected node pointers or
  unbounded traversal.
- At most four explicit premise equations in a public context. These premises
  are **hypotheses in the exported Lean theorem**, not newly trusted axioms.
- Exactly zero, one or two live parent proofs per inference, fixed by the
  selected rule. Parent contexts/signatures/profile bindings must match exactly.
- Natural rank encoded with 32 checked bits; child ranks strictly decrease;
  base rank is zero. No field wraparound or unchecked comparison.
- One fixed circuit/profile, at most two recursive verifier gadgets, bounded
  input/witness encodings. Initial circuit degree ceiling `2^16`; exceeding it
  is a failed feasibility gate, not automatic enlargement.

The node-bound term profile is deliberately small to make real source review,
negative tests and finite memory plausible. More terms require a separately
versioned profile; no universal size claim follows.

### Accepted inference rules

`REFL(t)` proves `t = t`, with no parent.

`HYP(i)` proves exactly public premise `i`, with no parent; exported semantics
still quantifies over and assumes all listed premises.

`SYM(p)` proves `r = l` from certified `l = r`.

`TRANS(p,q)` proves `l = r` from independently certified `l = m` and `m = r`,
requiring exact intermediate-term equality and the same context.

`CONGR2(g,p,q)` proves `g(l1,l2) = g(r1,r2)` from two independently certified
equalities. All created terms obey the same finite grammar and context.

This does not search for proofs, claim novelty or silently certify equations
under arbitrary hidden assumptions. It is more than an allowlisted fixture:
arbitrary valid terms, interpretations, hypotheses and rule combinations within
the frozen grammar are allowed; false rule applications must be rejected even
if they contain familiar test names. Universal substitution can be added later
only with a separately checked rule, not presumed in EQ-DAG-1.

### Exact public statement and term/context binding

Each proof binds:

```text
semantic profile / base-soundness theorem identity
signature and exact explicit premise-context commitment
exact left/right term commitments and their canonical size bounds
derivation rank
cyclic verifier-data public inputs required by Plonky2
```

For the first profile, **expose the complete bounded context and result terms
as public limbs rather than implementing an additional application hash**.
Each term has exactly30 scalar limbs (tag,label for15 slots), each equation60;
four premise slots240, result60, context-count1 and rank1, plus fixed profile
identity limbs and required cyclic verifier-data inputs. Unused context slots
are the canonical `var0 = var0` placeholder, and `HYP(i)` requires
`i < context_count`. This is under350 application public limbs with an eight-limb
profile ID, before the backend's own verifier-data fields. Exact order and count
are part of the final code contract.

The receiver reads these actual descriptors before importing the Lean proposition.
The circuit range-checks and decodes them; parent contexts and matching middle
terms use exact corresponding-limb equality. This directly binds the selected
mathematical statement without interpreting a host-supplied hash or success bit.
The backend's proof commitment machinery remains cryptographic; eliminating a
separate application hash does not eliminate its assumptions. Public-input bytes
are fully charged. A future hashed interface is a separately reviewed optimization.

All bytes/indices/tags/selectors must be range-constrained. Mapping an arbitrary
SHA-256 integer into one ~64-bit field element is **not** an exact 256-bit binding.
Use checked limbs or a consciously selected domain-separated algebraic hash
with the prototype's declared assumptions. Native artifact IDs, semantic
profile IDs and the actual cyclic circuit verification key remain separate
roles; the public verifier pins their precise correspondence.

### Lean soundness bridge

Define in Lean the term/context syntax, total interpretation, well-formedness
predicate and the five inference rules. The root-selected Lean relation is
unbounded; the bounded circuit decoder must map into that relation and reject
out-of-profile syntax. For every carrier `A`, assignments to variables
and interpretations of the function symbols, prove:

```text
if all equations in context Gamma hold,
and the parents' exact equations hold,
and Step Gamma parents output rule,
then the output equation holds.
```

Equivalently, prove inductively `Derivable Gamma e -> Entails Gamma e`.
The resulting exported theorem has the full form
`forall A interpretations assignments, Holds Gamma -> eval(lhs) = eval(rhs)`.
It may later be specialized to real Lean structures by ordinary proof work.

The formal soundness proof must be kernel-checked under the existing foundation,
with no `sorry`, extra axioms or trusted external equality evaluator. The
cryptographic receipt is still not a native proof term: the certificate-aware
importer relies on the exact soundness theorem plus the authenticated relation
when installing this particular result as a certified derived premise.

There is a second crucial bridge: **every satisfying circuit assignment must
implement exactly one valid Lean-specified step**. All selectors, range checks,
parent enable bits, commitments, intermediate equalities and rank constraints
need independent code review and adversarial tests. Merely proving Lean's
abstract rules sound does not certify a buggy circuit encoding of those rules.
Before crypto acceptance is enabled, provide an explicit constraint-to-Step
argument for every branch; ideally mechanize the small arithmetic/Boolean
encoding lemmas. Declare what is proved and what remains audited engineering.

### Two-parent recursion and guarded bases

Use two `ProofWithPublicInputsTarget` parent slots and the pinned cyclic verifier
gadgets. A rule's constrained opcode determines whether each slot is live.
`TRANS` and `CONGR2` require both; they cannot disable a failing parent. Base
rules require their own real term/context relation and rank zero. One-parent
rules still enforce their exact rule, parent binding and strict rank increase.

Every live parent uses the same permitted verifier data and semantic profile;
its exact public term/context fields feed the step constraints. Cyclic proof
verification additionally requires the **outer verifier** to call
`check_cyclic_proof_verifier_data` against the real pinned verifier data, as
the upstream API explicitly warns. Parent verifier-data public fields are
connected to the current ones. No attacker-selected verification key, omitted
outer equality check or unconditional dummy branch is allowed.

Common-circuit data and padding must form a genuine fixed point for the two
recursive verifier slots. The upstream one-parent example is a starting source,
not proof that our two-parent circuit has that fixed point within the gate cap.
Construct and freeze it before mathematical runs; if it exceeds the fixed cap
or cannot be matched, fail the application feasibility gate.

Ranks and parent edges are per-result mathematical support, not a global ledger.
Two independent branches may share only their semantic profile and context;
the join prover receives their proof packets and tiny statement descriptors,
not their old inference lists or private process state.

## Application gate and stop conditions

After independent source/bridge review, one allocation should do the following:

1. Two separate producers generate different nontrivial equations from the
   same disclosed context. Each contains multiple rule steps and has its own
   real final certificate; neither is just a shared process's unchecked label.
2. A fresh join process receives only both final parent packets and the selected
   context/terms. It proves an exact `TRANS` or `CONGR2` successor, verifies
   the real resulting certificate and emits the bound Lean proposition.
3. Another fresh process uses that successor and a separately generated second
   branch to produce the next generation. Old traces/source files are absent
   from its packet. Native Lean checks the matched fully reconstructed result
   in separate evaluator evidence, not as mandatory receiver work.
4. The refusal set includes altered lhs/rhs/context, mismatched middle term,
   missing second proof, disabled required parent, wrong cyclic key, rank wrap/
   cycle attempt, malformed term indices/tags/padding and an invalid alleged
   base equation. A valid cryptographic proof of a weakened relation fails
   the exact-statement/profile gate.
5. Hold interface/context/endpoints fixed while comparing short versus longer
   derivations produced by valid detours. Measure parent/join packet bytes,
   actual ancestry file reads, proving/verification CPU/wall/RAM and proof sizes.
   The test targets absence of a mandatory history term; padding proofs with
   redundant steps is not evidence of mathematical usefulness or faster growth.

Proposed application ceilings for root review: one fixed circuit build, two
history-length fixtures, at most 12 actual proof generations, 90 minutes total
wall and 3600 inclusive Job CPU seconds, 4 GiB private commit, serial proof
generation, eight processes, 256 MiB aggregate serialized experiment inputs/
outputs. Count all failed generations. Stop on an unmet soundness obligation,
unreviewed constraint change, native statement mismatch, cap breach or unknown
process state. No automatic parameter expansion, trusted-signer fallback or
labeling success from a debug executor.

These limits may be too small for two recursive verifier gadgets; that is an
honest falsifiable result. Obtain the actual Gate T costs before commissioning
the whole application allocation. Product integration, live peer serving,
arbitrary Lean proof capture, general library joins, independent-host evidence
and high-assurance deployment remain distinct later work.

## Primary-source trace

Plonky2 paths read at the selected exact revision:

- [README: deprecation, nightly, security caveats](https://github.com/0xPolygonZero/plonky2/blob/5d9da5a65bbcba2c66eb29c035090eb2e9ccb05f/README.md).
- [Manifest: version/features/MSVC jemalloc exclusion](https://github.com/0xPolygonZero/plonky2/blob/5d9da5a65bbcba2c66eb29c035090eb2e9ccb05f/plonky2/Cargo.toml).
- [Cyclic verification and mandatory verifier-data check](https://github.com/0xPolygonZero/plonky2/blob/5d9da5a65bbcba2c66eb29c035090eb2e9ccb05f/plonky2/src/recursion/cyclic_recursion.rs).
- [Upstream Linux/WASM CI](https://github.com/0xPolygonZero/plonky2/blob/5d9da5a65bbcba2c66eb29c035090eb2e9ccb05f/.github/workflows/continuous-integration-workflow.yml).
- [Official exact nightly manifest](https://static.rust-lang.org/dist/2025-06-30/channel-rust-nightly.toml).

Nova paths inspected only to reject substituting ordinary sequential IVC for
the required two-parent join: README, Cargo.toml, CI, `src/traits/circuit.rs`,
`src/nova/mod.rs`, provider definitions and `examples/and.rs` at revision
`01b1e2d662a847ed7029770ecbaf6687398899dd`. No Nova runtime was selected.

The next action is now concrete: root reviews/authorizes isolated Gate T, while
the native interface experiment continues. No additional generic backend survey
is needed before that finite executable decision.
