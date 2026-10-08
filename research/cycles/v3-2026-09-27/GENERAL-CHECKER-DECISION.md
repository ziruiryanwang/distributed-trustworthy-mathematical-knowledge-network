# Next central decision: certify actual Lean checking

2026-09-28 UTC. Root working checkpoint; no new runtime allocation selected.
The full goal and 03:00 Chicago tentative-v3 deadline remain unchanged.

## Why the preceding milestone is not the next implementation target

EQ-DAG1 and its conditional native handoff establish a useful infrastructure
discriminator. They do not check an agent's Lean proof. Another finite equation
adapter or synthetic join would not discharge that central gap. The next step
must reduce the distance to a certifiable dependent type/declaration checker,
with exact interfaces and authenticated computation support.

The source13 native release remains usable and unchanged. Source16's measured
reader saving remains separate. Neither is relabeled ancestry-independent.

## Concrete source finding: zkPi is not a drop-in general checker

Root inspected these primary sources at the already recorded zkPi revision
`ff136f79ca5843cafed61bc1222a5dd85d7a8646`, using read-only HTTPS requests:

- `src/lean.rs`, especially export_theorem 562–610 and export_definition
  1072–1126;
- `src/zk/mod.rs` typing, evaluation, context and lifting trace constructors;
- `zok/eval.zok`, particularly its public input signature 1230–1245;
- `src/main.rs`, `Cargo.toml` and `scripts/oneshot.sh`.

This is substantially more informative than the older toolchain-version check:
the project contains actual dependent-typing and conversion trace machinery,
not just an ordinary proof verifier wrapped in a name. It is a useful design
reference. Nevertheless the selected source has these concrete mismatches:

1. `export_theorem` maps **every universe parameter to zero**. A proof of that
   instance is not a certificate of the original universe-polymorphic theorem.
   A new bridge must preserve ordered universe parameters or explicitly export
   only the exact instantiated proposition; it cannot silently generalize it.
2. `export_definition` recursively exports the value and type of a referenced
   definition. It does not implement our certified sealed-premise boundary.
   Caching repeated work is not cold-contributor ancestry independence.
3. Axioms and inductive metadata are public relation inputs. That can specify
   a relative theorem, but our importer must additionally establish their exact
   foundation/certified origin and simultaneous compatibility. Publicness alone
   is not validity or an allowed-axiom policy.
4. The included oneshot path invokes CirC/ZoKrates R1CS with Mirage. The inspected
   files do not implement our recursively certified immediate-parent interface.
5. The exporter treats some large numeral values as fresh typed axioms and has
   unsupported expression/quotient paths. No general Lean4.34 correspondence or
   original-numeral identity is established by this code inspection.

No exploit, complete security audit, local compilation or timing claim is made.
The result is **NO_DROP_IN_ADOPTION**. Reusing a trace design would require
explicit correspondence, level, policy and composition work, not a version bump.

Primary source base:
<https://github.com/emlaufer/zkpi/tree/ff136f79ca5843cafed61bc1222a5dd85d7a8646>.

## Additional concrete candidate under inspection

`ammkrn/nanoda_lib` resolves to
`3a2407216ee84a75f9e1aead6803d0578be06ae7` (commit 2026-09-22), package 0.4.19.
Its manifest uses Rust libraries including num-bigint, indexmap and serde,
rather than Lean's mixed C++/generated-C/runtime closure. Its README documents
an external Lean4 type checker and operator-selected axiom policy.

This makes it a specific potentially smaller guest implementation candidate,
not a selected trusted backend. Exact supported semantics, native4.34
correspondence, parser validation, sealed-import origin, host/guest compilation,
resource bounds and recursive certification all remain to be established.
In particular the README's illustrative `Lean.trustCompiler` permission is
not adopted by this project. No source download/build/dependency execution has
occurred; root is inspecting the exact parser/checker call path first.

Primary source:
<https://github.com/ammkrn/nanoda_lib/tree/3a2407216ee84a75f9e1aead6803d0578be06ae7>.

## Disjoint decision inputs in progress

- [Native guest closure](LEAN-GUEST-CLOSURE.md): exact code and toolchain path.
- [Inference trace](LEAN-TRACE-CHECKER.md): what a faithful trace must check.
- [Recursive assurance](SCALE-SOUNDNESS-DECISION.md): the required security
  statement and a falsifiable receiver-and-contributor scaling gate.

A plan is not a passing certificate implementation. The next allocation will
be selected only after these inputs identify a bounded, consequential test.

## Selected preparation and actual first build

Root selected [GENERAL-CHECKER-01](../../../experiments/general-checker-01/CONTRACT.md)
for nonadmitting qualification of the pinned existing Rust checker, rather than
writing another partial typechecker. It uses the retained dependent Fin successor,
an actual sealed-parent delta and prospectively fixed semantic/origin controls.
Both independent decision tracks support this direction; no general correspondence
or acceptance-mode adoption is assumed.

The independently reviewed native build completed at20:40 Chicago. Exact upstream
source and committed lock are unchanged; binary SHA256
`f8378c83d6e5b2cd1d9641f9714fdf44466314941b9c18b4f094bd0ed8d98416`,
1,156,096bytes.39.78125workerCPU+10.421875controllerCPU,54.7386wallseconds,
550,969,344peakJobbytes. Selected same-Job VCTIP cleanup actually occurred.
This is a build result, not a theorem/prover result; independent outcome audit
is next. No old native or cryptographic campaign was rerun.

The guest feasibility decision has changed materially: the retained stock
nightly recognizes the RISC Zero target and its matching std source implements
the guest IO/allocation/panic ABI. An exact manual build-std route is plausible.
The current host SDK, however, unconditionally compiles Unix stream/file-descriptor
orchestration in its default-prover module. Selecting a local prover at runtime
does not fix compilation. A focused source search is testing whether a small
explicit in-process-only profile and app-local build dependencies can close the
actual local prover path. No guest/prover build or platform change has occurred.
