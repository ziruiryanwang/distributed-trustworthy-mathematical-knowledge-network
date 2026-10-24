# Default architecture: ordinary packages, receiver-local assurance, optional interchange

2026-10-24. `demand_producer`, independent whole-architecture audit under
GROWTH-IMPLEMENTATION-SELECTION. Source/evidence/theory only. No runtime, build,
upgrade, download-to-disk, product edit, owner operation or Git mutation. The
canonical guard passed. This file is the reviewer's only edited checkpoint.

## Decision that should change the next implementation

**Make ordinary versioned Lean packages the primary contribution and working
format. Make assurance a receiver-selected operation over exact results and
locally adopted bases. Keep the custom inert interchange path as an optional
supported adapter, not the mandatory route through which ordinary mathematics
must pass.** Rich package reuse and dependable mathematical checking are separate
jobs; requiring every producer and consumer to migrate into our generated-module
ecosystem unnecessarily couples them.

The strongest new implementation alternative is concrete upstream software, not
a hypothetical stronger baseline. Lean v4.35.0 contains `leanexport`, inert export
parsing, kernel replay, and `lake check` with an axiom policy and Linux sandboxing.
These deserve preference over another independent exporter/checker implementation
where their actual contracts suffice. However, their current exit-success
predicate is **not** our exact foundation/target/witness acceptance predicate.
Use the infrastructure behind a small explicit policy boundary; do not equate the
two or silently migrate existing accepted state.

**Highest-payoff next technical decision:** specify the bounded acceptance adapter
around a pinned upstream inert export: exact selected results, canonical allowed
axioms and kernel primitives, explicit version/byte binding, and local outcome
recording. Determine whether upstream parse/replay can supply this contract with
a narrow wrapper. Do this before another custom package build or closure/export
optimization. Source analysis below already identifies policy differences that
need a remedy; a new large experiment cannot erase them.

The currently commissioned three-file clean facade may close as a finite cleanup
of the existing optional lane. It removes unusable commands/dependencies and
preserves working evidence. It must not automatically trigger another whole
distribution or demonstrate that this lane is the final default architecture.
Existing code is reusable evidence and a fallback, not a reason to fund its next
component. No new implementation or upgrade is selected by this audit.

## Real default workflows

| Situation | Default action | What is *not* automatically required |
|---|---|---|
| A researcher already uses an approved Lean project | Continue normal imports, local application/search and normal package publication | A commons owner, re-exporting installed mathematics, a certificate, new notation/instance infrastructure |
| A useful package is already approved and compatible | Reuse the actual package and its local cache; check the new work under the chosen base/policy | Reconstructing that library in a 581-name custom seed or replaying its old proofs on each use |
| A new external package is useful and execution is explicitly approved | Obtain a pinned package revision/dependency/toolchain selection; use the project's normal interface; choose the required mathematical validation separately | A claim that permission to execute implies the package's mathematics is independently warranted |
| A receiver does not approve the publisher's executable code | Obtain inert proof data; independently check under a locally accepted basis; use a supported local realization if needed | Loading the peer's `.olean`, tactics, initializers or Lake configuration as a mathematical warrant |
| A small device cannot afford a missing base or closure | Use an available supported succinct witness/certificate, explicitly chosen trusted-base service, or decline/defer | Silent full replay, silent trust downgrade, or an obligation on every original author to pay for certification |

Ordinary source/package publication can precede any demand for exact proof data.
Existing bundles should be reused. Materialize selected evidence only when it
serves a real receiving policy, or batch it when expected demand justifies the
cost. Network discovery remains untrusted advice; packages and proof objects can
be offered by replaceable repositories/custodians. No global common environment,
mandatory task queue or single package host is needed for this workflow.

## Four different decisions, not one checked flag

1. **Execution approval:** the local user/operator allows a selected toolchain,
   package, plugin or build step to execute. This is an OS/capability decision.
   It grants no mathematical premise. Sandboxing reduces selected machine risks;
   it does not prove the theorem.
2. **Mathematical warrant:** actual accepted evidence establishes the selected
   declarations relative to a specified foundation and already warranted base.
   A certificate can establish this through its stated cryptographic relation;
   ordinary kernel checking can establish it directly. A filename or saved
   compiler-success message cannot establish it by itself.
3. **Explicit trust assumption:** a participant adopts an exact base or service's
   checking practice without independently establishing all of it. This can be
   useful, but is a different assurance policy. Its dependencies must remain
   labeled; signing identifies an attestation and does not turn it into a proof.
4. **Availability/service promise:** someone retains and serves the selected
   bytes before the consumer's deadline. Neither checking nor signatures create
   missing copies or reserve bandwidth, memory, or prover capacity.

The default should reuse each participant's existing *chosen* base, but never
invent that participant's trust choice. A base may be locally independently
validated, derived from an already validated base, or explicitly trusted. A
consumer requesting the first kind must not receive the third under a generic
`verified` label. Different participants can choose different policies and still
exchange the same ordinary work.

This is not weakening a strict checker to make a benchmark pass. It is refusing
to impose the most expensive cold, untrusted receiving policy on every ordinary
local action. It also means not claiming that ordinary imports are freshly
rechecked: the retained ACCEPTANCE-BOUNDARY analysis and inspected
`Environment.finalizeImport` construct constant maps from imported records.
`trustLevel := 0` and `loadExts := false` alone do not establish their proofs.

## Whole-cost comparison and the useful compromise

For an immutable supported base epoch, the ordinary package route can pay one
base adoption/validation cost and then incremental build/check costs for actual
new work. It preserves the package's frontend API. The exact interchange route
adds selected export, evidence transfer/decoding/checking, context/materialization
and possibly missing frontend adaptation. A certificate route adds production
and certification service to potentially reduce some *cold* receiver work.

All routes still pay search, failed candidates, maintenance and actual acquisition.
Common costs cancel only where common. Existing local cache hits are not fresh
cold imports, and one user's validation is not another user's independent warrant.
The relevant horizon is the supported version/policy/retention epoch, not infinity.
Memory and latency remain feasibility constraints even if a scalar total is lower.

The recommended compromise is **one explicit, bounded base adoption plus durable
local reuse**, or an explicitly trusted base where the participant chooses that
assurance. This is already supported in principle by the adopted reaudit. The
important correction now is that the base should normally be the user's useful
ordinary library, not a forced migration through a miniature custom foundation.
No one needs the entire world corpus. A large relevant specialty library can
still exceed the device's budget; changing who pays does not remove that cost.

The current custom implementation is not a free incremental package checker.
ORDINARY-PRACTICAL-COST identifies repeated selected-context binding/name walks,
artifact hashing and native imports; the module materializer has 32-new-unit /
4-MiB bounds and refuses installed non-theorem/group collisions. These are real
scope/operating limits, not mathematical counterexamples. The normal package route
avoids imposing those adapter limits on local work that already succeeds.

The existing U certificate cost approximately 36,414 known CPU seconds; its
observations do not establish a native/certificate same-endpoint ratio. They are
enough to reject compulsory per-contribution certification as today's default.
Keep a certificate when it supplies a funded otherwise-unavailable capability or
its whole cost is repaid by eligible otherwise-uncached demand. Do not restart
that campaign or replace it with a speculative universal prover rewrite.

## New primary source: what upstream v4.35 actually supplies

Read-only raw-source inspection uses Lean commit
`eb6cafb7290e8bd5f2937522d8d804f58f02bafc` (identified by root as v4.35.0).
This reviewer read `src/lake/Lake/CLI/Check.lean`, `Lake/Check/Axioms.lean` and
`Lake/Check/Compare.lean`. Root separately read LeanExport Basic/Json/Parse and
LeanChecker/Replay; their findings below are identified as coordinated source
evidence. Installed local support remains v4.34.0; no upgrade has occurred.

`lake check` is directly relevant without a human-intention/challenge interface:
its `checkProject` builds/exports selected project targets, runs kernels over the
export, parses it, and checks used axioms. `--from-export` skips source/dependency
building and accepts an existing inert export for checking. `lake comparator` is
a separate statement/definition comparison facility; we need not make intended
questions or challenge definitions part of the network to reuse `lake check`.

Concrete supplied boundaries:

- Source building and export run through Linux `bwrap`; only NDJSON crosses into
  the result-processing path. Downloaded compiled artifacts are not mapped into
  that parent to obtain its verdict. The export-only path avoids source execution.
- The bundled exporter/checker are selected from the toolchain. Builtin checking
  invokes `leanchecker --silent --from-export`; optional `--paranoid` adds named
  independent checkers. These are implementations, not a formal proof of the TCB.
- `checkUsedAxioms` permits the names `propext`, `Classical.choice`, `Quot.sound`
  and rejects other axioms *used by another exported declaration*. The current
  `lake check` policy is not an arbitrary participant-supplied whitelist.
- Root's exporter inspection finds target-selected **full closure** and a source
  environment/recursor census, not a persistent frontier cache. It exports kernel
  declarations, not original frontend-extension metadata.
- Root's replay inspection finds actual replay into an empty kernel environment
  and exact generated quotient checks. Replay still accepts axiom declarations,
  skips unsafe/partial entries and uses `addDeclCore 0 0`; its duplicate-theorem
  relation is weaker than exact full proof-inventory equality.

This removes the rationale for assuming all independent validation plumbing
must be bespoke. It does **not** establish that replacing our controller with a
bare `lake check` invocation gives the same policy, cache, resource or availability
contract. Nor does a fresh replay on every use solve scale.

## Small policy gaps that matter before substitution

### Canonical allowed axioms and primitives, not just their names

The inspected `checkProject` path calls kernels and then the name-based used-axiom
check. Unlike comparator's `verifyMatch`, it does not compare against a canonical
reference export in this file. Root confirmed that the inspected replay path
admits an `.axiomInfo` by creating an axiom declaration rather than checking its
statement against the intended standard axiom's statement.

The logical insufficiency is simple. Let `F` be a proposition not derivable from
the intended base. A declaration named `propext` with type `F`, followed by
`t : F := propext`, is well-typed relative to *that supplied axiom*. A predicate
that merely permits the name `propext` has not established `F` under the genuine
propositional-extensionality axiom. This is a structural counterexample to the
policy implication, **not an executed exploit or a claim that every input path
accepts a constructed malicious file**. Exact canonical signature/dependency
binding is what is missing from that implication.

Also, `usedAxioms` deliberately excludes self references. A standalone unused
axiom can appear in an export without violating that used-axiom test. Such a
declaration must not become an accepted theorem merely because the file receives
exit zero. Unsafe/partial skips likewise require an explicit selected-result
coverage check, not promoting every exported name into independently checked work.

A conceptually sufficient remedy is a finite adopted foundation comparison:
match actual permitted axioms' name, universes and type, with their type dependencies
and kernel special-reduction primitives bound to the exact supported foundation;
reject forbidden selected kinds and require a complete checked selected closure.
Do not merely test the printed proposition string or install ambient records.
The current project's exact basis checking and upstream comparator's primitive
comparison supply reusable precedents. No new axiom theory or human-intention
interface is necessary. This remedy is not implemented/qualified by this note.

### Bind the verdict to the result actually reused

Root's parser inspection reports that the first metadata line is discarded rather
than enforcing an exact export-version contract. A successful process exit is
not, by itself, a durable local warrant for arbitrary later files. The wrapper
needs exact input hash, supported exporter/parser/checker/policy identity, target
and declaration coverage, clean completion, and protected state/invalidations.
It must inspect the actual resulting declarations/types, not substitute claimed
preview text. Different valid proof witnesses need not share our current witness
ID, so do not silently reinterpret an existing exact-ID object through upstream's
weaker comparison rules. A prospective new lane can use an explicitly declared
relation; migration is separate work.

This is a thin adoption boundary only if it reuses the upstream checked result
and data model. Reimplementing the whole exporter to attach these fields would
defeat the reason for investigating the upstream route.

### Resource and execution boundaries remain real

The inspected CLI has no aggregate wall/CPU/memory/output reservations equivalent
to our bounded operation contract. Export stdout streams into a temporary file;
some diagnostics are read to the end. Root's parser inspection found unbounded
line/in-memory-map accumulation. The parent also parses the export outside the
child sandbox. A separate aggregate controller/quota boundary is therefore still
needed for hostile/unbounded inputs, including parser and output storage, not
only the source compiler process. Bounding supported work can legitimately refuse;
no claim of a small successful bound for arbitrary mathematics follows.

`mkContext` requires Linux namespaces/bubblewrap unless
`inadvisablyNoSandbox` is chosen, which explicitly warns that the run is not
trustworthy. Our current Windows v4.34 package is not that platform/toolchain.
Disabling the sandbox would not establish public hostile-source readiness.
An owner-approved local experiment is a different permission scope, not a portable
release argument. No WSL/container installation, Linux host, paid compute or
toolchain download is selected here.

Dependency resolution is the one network-enabled phase. It can read the selected
project/toolchain and write `.lake`; a sandbox does not make sensitive material
inside a readable project confidential from that network-enabled code. The source
binds `/` read-only and masks named home/runtime/temp areas: read-only is not a
universal secrecy guarantee. Production packaging must define a minimal approved
workspace and network policy, not just advertise that `bwrap` was used.

## Warm validation and common bases: necessary distinction from cold replay

Upstream's currently inspected fresh replay has no local validated frontier API.
Do not market it as one. The straightforward first use is selected **cold**
independent validation, whose cost may be justified at package adoption. Reuse
an exact protected local validation afterward rather than calling it on every
application. Reusing ordinary compiled artifacts also requires execution approval
and an exact relationship to the validated mathematical records; hashing a source
revision alone does not prove a nondeterministic build's output.

If a genuine incremental validator is required, its contract is conceptually:

    Valid_P(B) and CheckExtension_P(B, delta) -> Valid_P(B + delta).

`B` is an exact locally warranted environment, not a remote checked flag or a
matching library name/version string. All external references in `delta` must
resolve there or to earlier checked new declarations, with exact universes,
definitions, recursion groups and required computation. Mutable build directories
and unnoticed support changes cannot preserve the old warrant. The existing local
snapshot/anchor work already supplies relevant invariants; do not recreate its
reasoning or promise arbitrary original-package registration without resolving
the actual compatibility boundary.

Therefore separate two later decisions: first whether upstream plus a narrow
policy wrapper supplies safer/easier cold adoption; then, only where needed,
how to retain/reuse that event and check new deltas. They need not be one large
rewrite. Explicitly trusted ordinary bases are an optional operational alternative
for users who accept that policy, not a fabricated independent cache hit.

## Immediate implementation consequences and stopping rules

1. Finish the finite clean facade source work already selected; classify it as
   optional exact interchange and preserve all old evidence/failed branches.
2. Before selecting a build, root decides whether the next deliverable should be
   an upstream-based package validation adapter. The source-level acceptance
   differences above are decisive design inputs, not reasons to benchmark another
   tiny theorem. Prefer composing existing code over extending custom plumbing.
3. Keep producer publication ordinary and cheap. Never make independent receiver
   validation, certification, or creation of every exact index entry an author
   enrollment fee. Existing files/repos and optional exact bundles suffice.
4. Keep rich package APIs on the explicitly approved package route. Do not promise
   that reconstructed kernel declarations preserve arbitrary tactics, attributes,
   syntax or executable semantics; fidelity review owns that separate question.
5. Do not use upstream exit status as a mathematical admission authority until
   foundation, selected-output, binding and bounds are addressed. If the remedy
   becomes another large checker ecosystem, reconsider the scope rather than
   automatically implement it. Do not restart certification as an escape hatch.

The useful product may be the small, reproducible adoption/discovery/availability
layer joining ordinary independent libraries and validated evidence, not a new
universal theorem store implementation. This is a consequential simplification,
not abandonment of decentralized reciprocal growth: contributors keep usable
interfaces, consumers retain control of assurance and cost, and useful work can
circulate without a mandatory conversion or certification tax.

## Evidence and scope

- Current local sources: producer controller, OrdinaryModule04, module closure/
  anchor sources, installed Lean Environment/LeanChecker and the native local
  application code read in the prior assigned audit.
- Current retained evidence: PRODUCER-PUBLIC-SELECTION-AUDIT (7.39 s public
  facade; identical six-unit evidence, not growth), NATIVE-FIRST-WORKFLOW-SELECTION,
  ORDINARY-PRACTICAL-COST and ACCEPTANCE-BOUNDARY. No passed campaign was repeated.
- Earlier architecture/cost evidence: v5-2026-10-22-architecture-reaudit/
  ARCHITECTURE-REAUDIT and CERTIFICATE-ECONOMICS, including the preserved U costs.
- Primary upstream source at the exact commit above:
  [CLI Check](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/lake/Lake/CLI/Check.lean),
  [Axioms](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/lake/Lake/Check/Axioms.lean),
  [Compare](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/lake/Lake/Check/Compare.lean).
  Root separately inspected LeanExport and LeanChecker/Replay at the same revision.

No general security audit, migration, supported-platform upgrade, runtime
performance result, complete v5, or worldwide growth claim is established here.

## Independent cross-challenge of the reuse-fidelity decision

Read the complete `GROWTH-REUSE-FIDELITY.md`, including its final local-simp
qualification. Independently inspected the retained Lean 4.34.0 source at
`Elab/Tactic/Simp.lean:433-462,552-579`, `Class.lean:70-78` and the
`Environment.importModules` documentation. **No new blocking contradiction found
in the proposed route distinction.** This is a source/theory cross-review, not
another runtime qualification or an audit of the facade's exact file hashes.

The three important challenges are resolved at the stated boundary:

- `simp only` starts with builtin simp facts, not an absolutely empty mathematical
  context. It also retains approved local congruence/configuration/tactic machinery,
  and its argument processing can add simprocs. The revised note states all three.
  Consequently, exact theorem-reference selection is a trusted local use pattern,
  not a sanitizer for arbitrary peer syntax or evidence of data-only execution.
- Kernel declaration shape does not restore class recognition: `isClass` consults
  `classExtension`. Therefore the proposed `letI` option must remain restricted to
  an already registered class; it cannot recover an unfamiliar hierarchy by naming
  a well-typed constant. The note makes that restriction explicitly.
- `loadExts := true` can involve interpreter/initializer execution. It cannot be
  introduced as harmless metadata restoration in the inert admission lane. Approved
  ordinary packages remain the appropriate route for their rich frontend API,
  while their execution permission and mathematical warrant stay separate.

The growth implication is enabling, not universal: a checked fact or implementation
of a known interface can become usable without approving its publisher's complete
tooling. This expands the feasible reuse set for a constrained receiving policy.
It does not establish positive net growth until useful downstream demand outweighs
validation, transfer, local adaptation, failed searches and service. Ordinary
repositories can transport the same artifacts, and an equally capable baseline
must receive the same local rewrite/instance techniques. The software's potential
margin is reliable, low-friction admission and reuse under the selected policy,
not ownership of an exclusive mathematical automation primitive.

**Disposition:** adopt the fidelity boundary and native-package default in the
next architecture decision; do not commission generic metadata restoration or
another demonstration merely to restate it. This cross-review selects no build,
upgrade, experiment, protocol change or publication.

## Bounded challenge of the seven-step upstream cold contract

Read the complete appended contract in `UPSTREAM-VALIDATION-REUSE.md` and
independently read upstream `Lean/Replay.lean` at the same pinned v4.35 revision.
**The conditional soundness argument is sufficient in principle; no blocking
counterexample was found under its explicit premises.** In particular, the
contract does not rely on matching a human-intended theorem, bare axiom names,
a source build's exit status, a remote `.olean`, or migration of old evidence IDs.

Replay actually returns the resulting kernel environment, so comparing selected
records against that result is a real available seam rather than an invented
interface. Constructor/recursor comparisons and fresh kernel reconstruction do
not by themselves justify all claimed input-record identities; Step 6 correctly
requires the extra actual-result comparison, including generated support and any
claimed proof witness. Rejection of honest but differently normalized data would
be an interoperability limitation, not a counterexample to the stated soundness
implication. The declaration-kind distinction also matters: a selected definition
is a well-formed extension, not itself a proof of an arbitrary proposition.

One implementation-critical precision remains: the canonical primitive comparison
must cover **implicit kernel uses**, not only explicit names found by walking
expression constants. Literal typing/reduction and generated quotient machinery
illustrate why that inventory must be derived from the exact supported kernel and
owned by policy. Step 4 already requires kernel-special anchoring in principle;
an implementation cannot discharge it merely by reusing `getUsedConstantsAsSet`.
Likewise, a protected event must retain the selected-name/support coverage stated
by Steps 3 and 6: it cannot label unchecked or nonselected extra input records as
independently warranted merely because their bytes share E's digest.

**Payoff decision:** the new contract is a plausible replacement for a bounded
cold validation implementation, not yet an end-to-end package-adoption feature.
It intentionally says nothing about safely using separately supplied compiled
artifacts, carrying a warm frontier, or preserving a rich authoring interface.
Therefore source-level compatibility work is worth at most the narrow decision
whether actual honest supported records can pass Steps 4 and 6 using upstream
types/functions plus a small policy layer. It is not a reason to implement another
codec, bridge to the old evidence format, or rebuild a complete package manager.
The migration owner already investigates practical version/support costs; do not
duplicate that work. If the remaining work principally recreates our old checker
ecosystem, or cannot yet replace a needed receiving operation, stop adoption at
this documented candidate and return to the higher-payoff growth workflow.

This review grants no runtime, upgrade, new implementation or public-release
qualification. It supports the theoretical contract, with the explicit coverage
precision above, without turning a conditional cold checker into final v5.
