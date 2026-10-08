# Compositional certificates for proof-history-independent Lean reuse

2026-09-27. Author: `v3_efficiency`. Status: **proposed architecture and
proof obligations, not implemented, benchmarked, or enabled acceptance**.
Canonical root guard passed. No product, used test, installation, state,
failed evidence, or held growth/installed adapter was changed or executed.

## Decision being supported

The central new requirement is not merely a faster success badge. A receiver
must be able to accept a useful theorem, build a genuinely new result from it,
and certify that successor **without downloading or replaying all prior
theorem proof bodies**. A succinct receipt bolted onto today's `admit`, while
leaving today's full-context `submit` unchanged, does not satisfy this.

The candidate is a **certificate-aware, compositional Lean interface layer**:

- Certificates discharge the validity of imported theorem premises back to
  a receiver-selected foundation and policy.
- Authenticated interface and reduction data supply the mathematical objects
  actually needed by the local proof task.
- The next certificate verifies its imported certificates and checks only
  its new declarations, rather than replaying their ancestors' proof bodies.
- A proof-carrying dependency DAG, not a global ledger or common research
  goal, connects independent participants.

This is a significant new assurance boundary, not an optimization permitted
inside frozen source16. The old native-only deferral is superseded as a
research priority by the explicit large-scale requirement. It remains wrong
to label a design document an implemented cryptographic mode.

## Three different objects

Keep these objects separate even if they share a storage representation.

| Object | Purpose | Does the ordinary receiver need it? |
|---|---|---|
| Original proof artifact | Public mathematical evidence, independent replay, audit, alternative proving | Not every old theorem body for certificate-backed opaque reuse |
| Certified interface and reduction data | Names/identities, types, universe parameters, definitions and structural rules actually needed for new reasoning | Yes, to the extent the new task accesses them |
| Succinct certificate | Locally verifiable computational evidence that the exact compositional checking relation accepts | Yes, or a locally cached verified equivalent for the exact claim/profile |

A compact hash is not the interface itself. A succinct certificate is not
the original Lean proof term. A commitment or proof of knowledge is not a
storage service or future availability guarantee. Omitting ancestor proof
traffic must not silently omit definitions whose bodies affect conversion.

The use interface can be much smaller than the old proof history without
being constant size. Large statements, type dependencies, accessible
definitions, and long reductions remain genuine costs. There is no claim
that all mathematics can be used from a fixed-size packet.

## Pinned profile and public statement

The following are design roles, not already shipped wire fields.

Define an immutable `ProfileID` committing to:

- the foundation, its exact accepted declaration environment and base axioms;
- Lean version/kernel semantics, actual checker/guest program, build choices
  and options that can affect checking;
- canonical encodings, domain-separated commitment scheme, symbol/universe
  representation and interface/import semantics;
- accepted declaration kinds and group reconstruction/inventory rules;
- axiom, unsafe/foreign-computation and supported-fragment policy;
- the recursive certificate relation, verifier parameters, proof-system and
  security profile, and allowed predecessor-profile transitions, if any.

Receiver policy pins the profile or an explicitly permitted set of profiles.
A prover cannot nominate its own executable, verification key or foundation
and thereby make it trusted. The hash of a program specifies which program
was certified; it does not demonstrate that the program implements the
intended relation correctly. Native and certificate validation bases must
remain separately recorded.

For one atomic declaration block, a schematic public claim is:

```text
x = (ProfileID, FoundationID, PolicyID,
     BlockArtifactID, InterfaceRoot, ReductionRoot,
     DependencyBindingRoot, OutputEnvironmentRoot?, Rank)
```

`FoundationID` and `PolicyID` can be included transitively in `ProfileID`;
they are shown explicitly to prevent accidental omission. The optional
environment root is useful for certified environment-transition variants,
not permission to import an arbitrary environment with the same label.

The committed interface covers every exported declaration's exact:

- content-based binding and kernel name/name-mapping rule;
- declaration kind, full ordered universe parameters and complete type;
- opaque/sealed versus reduction-relevant status;
- body commitment where applicable, and exact referenced declaration IDs;
- inductive/mutual-group membership and generated declarations/recursors,
  including all kernel-relevant reduction metadata required by the profile.

This is not a hash of a pretty-printed theorem, a parser's guessed symbol
list, an LLM summary, or a type alone for a transparent definition. A source
alias may aid humans/agents but cannot alter the committed kernel meaning.

The binding to `BlockArtifactID` is important: our existing canonical objects
commit to proof and other bytes, not just informal theorem statements. The
certificate must bind its witness to the claimed artifact and its certified
export projection. An alternative proof of the same proposition does not
silently inherit an old artifact ID. A future semantic-equivalence index is
a distinct feature, not assumed here.

## Exact compositional relation

Let `F` be the pinned base environment, `B` the new declaration block,
`I_i` the imported certified interfaces, and `pi_i` their certificates.
`Seal(I_i)` exposes previously established theorem constants without their
old proof bodies; it does not expose unsupported hidden computation as if
it were available. Let `D` contain the exact definition/group/reduction data
required by this operation. Define the deterministic step relation
`R_step(x; w)` with witness

```text
w = (new canonical block/proof bytes,
     imported interface bytes and relevant reduction bytes,
     child public claims/certificates,
     authenticated membership/opening data,
     any checking trace required by the selected proof backend).
```

Acceptance requires all of the following, in the actual proved program:

1. **Exact decoding and binding.** Decode the canonical bytes with bounded,
   unambiguous types; recompute the relevant commitments; bind the selected
   roots, new proof, imports and emitted interface to `x`. No uncommitted
   host filesystem, network reply, or parser success bit can affect meaning.
2. **Grounded imported evidence.** Each non-foundation imported declaration
   has an accepted child claim/certificate in a permitted profile. Its exact
   interface and reduction binding match the data supplied to this step.
   Every reference reachable through the checked new proof, its type, and
   the actually exposed environment is covered. An authenticated membership
   path into an arbitrary root is not evidence that the member is valid.
3. **Well-founded certificate composition.** The base case is exactly the
   permitted foundation. Every child has a strictly smaller natural `Rank`;
   arithmetic and encodings cannot wrap or alias. Legitimate mutual
   inductive declarations are checked as one atomic group, not justified by
   circular theorem certificates. A finite implementation may impose an
   explicit maximum rank and refuse on exhaustion. No global rank allocator
   or total order on unrelated mathematics is necessary.
4. **Compatible mathematical environment.** Construct the selected union
   from authenticated interfaces and data. One kernel binding cannot have
   two different meanings. Names, universe order, bodies, declaration kinds,
   generated group members and reduction behavior agree wherever contexts
   overlap. A conflict fails or uses a separately justified renaming/transport
   rule; it is not settled by whichever packet arrived first.
5. **Authorized import.** Old theorem premises are imported only because
   their child evidence discharges them; old definitions/groups only through
   the certified import rule. There is no branch accepting an arbitrary
   `axiom`, `sorryAx`, unsafe shortcut, unchecked external computation result,
   or arbitrary serialized environment as a new mathematical premise.
   The exact allowed base axioms remain explicit. The phrase "all proofs
   checked" must not conceal a broader axiom policy.
6. **New native checking.** Check the new block's well-formed types and proof
   terms with the pinned kernel operation over this exact certified context.
   New definitions and inductive groups satisfy the selected ordinary kernel
   checks and policy. Existing canonical/native correspondence, generated
   inventory and export bindings must be preserved or replaced by explicit
   proved obligations, not dropped when moving to a VM.
7. **Output agreement.** The declarations and environment projection actually
   produced by checking have the committed artifact/interface/reduction roots.
   Any discovery metadata accepted as exact must derive from this projection.
   Heuristic rankings and usefulness labels are not certificate conclusions.

Direct child certificates and imported interfaces may be private witness
data for a recursive aggregate. The receiver need not fetch or verify their
whole ancestry itself. The public statement nevertheless binds their exact
dependency root; a party auditing/using the object can request relevant
openings. Zero knowledge is unnecessary for public mathematics; “witness”
does not imply a confidentiality objective.

An implementation can certify small batches rather than single declarations,
but must support authenticated per-export claims. A batch root without a
statement membership opening cannot authorize an arbitrary claimed member.

## Why this can discharge imported premises

The assurance argument needs two separate theorems; cryptography does not
replace the mathematical one.

**Semantic step obligation.** Under a well-formed compatible foundation and
environment, suppose every imported sealed theorem constant has a genuine
derivation of its exact type under that same foundation and the imported
definitions/groups are valid with the committed reduction behavior. If the
pinned checker accepts new proof `p : T` using only these imports, the full
mathematical environment supports a derivation of `T` without adding any new
unproved axiom. In outline this is admissibility of substituting valid proofs
for certified premise constants, together with conservative, compatible
environment extension.

This outline is not yet a mechanized Lean metatheorem or proof that an
arbitrary loader is correct. Dependent references, name translation,
universe instantiation, reduction and generated group semantics are exactly
where the import/step rule must be checked. Merely checking `p` after adding
arbitrary statements as axioms proves only a conditional theorem and does
not discharge those statements.

For combining independently certified environments `E1` and `E2`, require
**one simultaneous realization** `rho` of `E1 union E2` into a well-formed
extension of `F`, preserving every imported type and exposed conversion.
Two unrelated existential realizations of name-based contexts do not suffice.
The proposed conservative preconditions are the same base/profile, exact
agreement on overlapping kinds/ordered universes/types/reduction modes/
semantic references and computational body/group commitments, injective
canonical naming and a well-founded combined dependency structure. Even
equal theorem judgments do not automatically identify their different proof
instances: preserve distinct sealed names/instance bindings until a justified
transport establishes that the intended use is interchangeable. These are
premises for the realization/substitution lemma, not a claim that an arbitrary
JSON map union proves that lemma. The parallel `v3_index` investigation
identified this as a necessary explicit merge obligation.

**Recursive cryptographic obligation.** The chosen construction must provide
an adaptive, multi-claim, recursively compositional soundness theorem for the
actual step relation, parameter/key reuse and resource bounds. Except with
its quantified soundness error, an accepted top-level certificate has a
grounded valid derivation DAG satisfying the semantic step rules. Together
with the semantic obligation, this yields derivability under the pinned
foundation and policy, conditional on the stated implementation and
cryptographic assumptions.

A one-shot SNARK theorem is not automatically this recursive theorem. Strict
ranks exclude circular logical support; they do not prove that a recursive
verifier circuit, fold, accumulator or hidden child witness is sound. If a
proof of the reduction needs extraction of child arguments, use the scheme's
appropriate knowledge/PCD theorem and assumptions rather than pretending
ordinary one-shot soundness supplies extraction. A folding accumulator is
not itself a finalized succinct certificate unless its construction supplies
and checks the required final argument.

The soundness accounting is for the declared adaptive/concurrent workload,
including base and recursive invocations, setup and hash assumptions. A
simple `q * epsilon` bound is justified only by a theorem that supports the
relevant use. `q` is an analysis/local deployment bound, not a requirement
for a worldwide verification counter, validator committee, blockchain, or
global clock. Parameter selection must not assume an indefinitely growing
network performs only one verification.

## The Lean reuse boundary is part of the design

Stock Lean does not interpret a cryptographic receipt as a native proof term
of the original arbitrary theorem. A certificate-aware importer is therefore
a new explicit trusted boundary. It may use Lean's existing kernel for new
proofs while changing the authority for importing already certified premises.
“Unmodified kernel” is not the same as “unchanged whole-system trust model.”

The permitted initial target is a **sealed theorem interface profile** with
explicit supported reduction data. A local agent receives an authenticated
type/name/universe interface for lemma `L`, reasons using `L` as an established
premise, and supplies new proof `p`. Its successor certificate verifies `L`'s
certificate, checks `p` under the sealed interface and binds the resulting
new type. Neither the local author nor the successor prover must reconstruct
`L`'s ancestor proof bodies for this supported path.

Sealing is not universally semantics-preserving for every existing Lean
program. The parallel pinned-Lean investigation reports that theorem proof
unfolding can matter, including computations through `Acc.rec`. Such work
may need the relevant certified body/reduction material, a proof rewritten
against a sealed interface, or explicit unsupported status. This is a
completeness/compatibility limitation to qualify, not a license to accept a
false proof. Do not claim universal theorem-body erasure.

Likewise, `f : Nat -> Nat` with two different bodies does not have one
interchangeable computational interface merely because its type agrees.
Transparent definitions and inductive recursors must carry the exact data
and behavior used by the new proof. A succinct proof cannot make a missing
body available or execute an arbitrary long reduction in no time. A narrower
opaque interface plus certified behavioral theorems can avoid some unfolding,
when the mathematical task can actually use that interface.

Use two checks at the software boundary:

- A minimal certificate/import validator decides exactly which authenticated
  declarations may enter the working environment and records their basis.
- A new-contribution checker rejects unknown/unbacked premises and rebinds
  all actually used mathematical inputs in its certificate relation.

An agent's personal Lean process may execute strategies, elaboration and
tactics. That is not a remotely trusted success oracle. A producer can use
an untrusted elaborator to find a proof, but the certified deterministic
checker must check the resulting kernel terms and policy. A certificate of
“the source process printed success” is insufficient. A correctly certified
checker execution also does not prove that the submitted mathematics is
useful, novel or correctly described in natural language.

## Backend choices and their actual tradeoffs

No backend is selected or measured by this checkpoint.

| Route | Attraction | Central cost/risk to establish |
|---|---|---|
| Portable pinned Lean checker in a general zkVM | Reuse ordinary checker code and a general execution proof; composition can use a supported receipt-verification mechanism | Getting the real accepted checker/encoding/import relation into the guest, reproducible image binding, ISA/compiler/runtime/syscall trust, large trace/prover memory/time, and recursive receipt semantics |
| Dedicated arithmetized Lean-compatible checker | Potentially lower proving overhead than a general VM for a fixed structured relation | Significant specialized engineering; exact fidelity to pinned Lean/kernel/group/reduction semantics, policy and canonical encoding; upgrade/audit burden |
| Recursive SNARK/PCD over bounded step proofs | Small verifier/proof for many independent receivers; dependency-aware aggregation | Setup/algebraic assumptions depend on scheme; exact recursive composition theorem, public-input binding and per-step bounds; proving may be expensive |
| Transparent STARK-style execution/recursion | Avoid some trusted setup assumptions; useful execution-proof path | Often larger certificates and hashing work; recursion/aggregation details matter; “transparent” is not assumption-free or automatically post-quantum for every surrounding component |
| Folding/IVC with final compression | Amortize long incremental checking transitions | Not automatically arbitrary DAG composition; merging independently certified environments and final decider soundness must be designed; one linear history must not become a mandatory global history |
| Domain-specific Lean proof certificate/reflection | Keep native logical assurance for suitable domains and avoid expensive search/repeated expanded derivations | Not universal proof-history compression; certificate and kernel reduction costs are workload-dependent; checker soundness theorem and instance proof must really be available |

These categories overlap: a zkVM can use STARKs and wrap/aggregate with a
SNARK; a recursive construction can use folding internally. Comparing names
alone is not a backend evaluation.

The first execution proof should cover the deterministic checker relation,
not the Windows process wrapper, TLS server, LLM, package manager or entire
historical workflow. If an external native checker result is just passed into
a VM as a trusted bit, the VM proves the bit was read, not that Lean accepted
the intended object. All meaningful computation must be in the proved
relation or an explicitly justified authenticated subrelation.

The prior literature records zkPi, recursive SNARK/PCD and Nova as feasibility
precedents. Root's current primary-source check reports zkPi's example pin is
Lean `v4.8.0-rc1`, not our `4.34.0`; it is not a drop-in compatibility claim.
No literature number is used here as a benchmark of our new exact relation.

## Why no global ledger is required

Let every immutable claim identify its foundation/profile, exact mathematical
bindings and strict dependency support. Nodes verify and combine whichever
compatible claims their own work requires. Two disjoint valid claims need no
agreement on which one happened first. Equivocal bindings are rejected by
the authenticated join rule; alternative foundations/profiles coexist as
distinct assurance universes, not forcibly merged truths.

A node may certify a local environment snapshot or useful batch to amortize
repeated access. The snapshot root is a local authenticated map of established
declarations, not the unique state of all mathematics. Inclusion plus snapshot
validity can supply a declaration certificate; inclusion alone cannot.

One global recursive aggregate creates unnecessary update, availability and
subset-access coupling. Prefer object/block certificates with optional local
batch aggregates. Indexing/discovery and source custody remain decentralized
services; they can lie, omit or be offline without making a false theorem
pass certificate validation. They can still harm availability and efficiency.

## Cost model and expected scaling boundary

For a selected old lemma let:

- `H` be the total old transitive proof-history bytes and replay computation;
- `U` be the useful authenticated interface/reduction bytes actually fetched;
- `k` be the number of selected direct certificate/import dependencies;
- `C_delta` be the new proof/type/group checking work;
- `V` be certificate verification work for the pinned scheme/profile;
- `P_delta` be succinct proving work for this compositional step.

The intended supported receiver path costs approximately

```text
certificate verification + reading/hashing U + authenticated openings
+ local import/materialization + the local task's actual reduction work.
```

It must contain **no mandatory `read(H)` or `replay(H)` term**. This is a
dependency-boundary requirement, not a guarantee that `U`, import time or
new proof computation is small. For an authenticated map, a naive opening
may have logarithmic map-size overhead; useful multi-openings can reduce
shared work. The public input itself must be a bounded commitment plus the
selected statement/openings, not an unbounded ancestor list disguised as a
“constant-time verifier.”

The intended successor prover checks roughly the new `C_delta`, direct
certificate composition and required authenticated context operations. Its
one-time cryptographic `P_delta` is generally greater than ordinary checking,
potentially much greater. A nonrecursive implementation that puts the whole
old history into every prover witness can reduce receiver work but leaves a
central cumulative production bottleneck; it is only an intermediate
experiment, not the final solution to recursive accumulation.

Across `N` independent receiver trust domains, after canceling equal costs:

```text
native route:       N * C_native
certificate route: P_delta + N * (V + C_data_import_reuse)
```

This wins total chosen-resource cost when the second expression is smaller.
No current measurement supplies `P_delta`, `V` or the new complete reuse
cost. Count distinct trust domains after local caching, not all agents sharing
one trusted node. Receiver bandwidth/latency can improve before total-system
compute breaks even. CPU, GPU, RAM, bytes, delay and money are not one unit;
report them separately or justify the conversion.

Open prover participation is necessary but not sufficient for decentralization:
very high proving cost can create practical concentration. Permit many
independent provers for the same immutable claim, asynchronous certificates,
and native witness archival/reproving. Never require a selected commercial
prover, secret service or single credential holder to keep the commons usable.
Proof availability and native artifact availability are separately reported.

## Failure and attack checklist

| Failure | Required boundary |
|---|---|
| Valid receipt for another theorem/program | Exact requested statement/artifact/profile/key checks outside and inside the proved relation |
| Arbitrary premise laundering | Every used non-base premise backed by compatible child evidence; transitive base-axiom policy preserved |
| Cyclic mutually supporting certificates | Grounded base plus well-founded ranks and an actual recursive soundness theorem |
| Same name/type with a different definition | Body/reduction/group identities and coherent environment join, not type hash alone |
| Universe/order or encoding ambiguity | Canonical typed encodings and exact ordered universe instantiation |
| Valid proof but malicious generated inventory | Bind the actual checked group output and every imported generated member/metadata |
| Child checked under weaker policy | Exact policy/profile match or explicitly proved allowed transition; no implicit policy weakening |
| Fake VM native-check syscall | Execute the checker relation in the proved machine or verify an appropriate subcertificate |
| Fold/aggregate presented as final proof | Require the construction's complete verifier/decider and verified recursion parameters |
| Poisoned local certificate cache/import image | Key by full immutable semantic profile and claim; authenticate bytes; crash-safe local acceptance records |
| Proof/certificate loss or malicious withholding | Treat as availability failure; independently replicated retrievable data, not false mathematical acceptance |
| Huge malformed statements/certificates/ranks | Admission byte/shape/resource limits before heavy work; bounded parse/verification; honest refusal |
| Unsupported theorem unfolding | Explicit supported sealed profile; required body fetch or safe refusal, never invented conversion |
| Checker/profile vulnerability | Explicit local distrust/update policy and invalidation of reliance; old signed/hash-bound records do not repair an unsound relation |
| Cheap production of useless correct results | Local usefulness/ranking/resource policies outside validity; cryptography is not a usefulness oracle |

Cryptographic failure probabilities and ordinary implementation bugs differ.
Use a stated security target for the former; audits, differential tests and
small trusted boundaries address the latter. The mathematical assurance is
relative to the foundation's consistency/soundness and kernel semantics,
not an unconditional proof that the whole chosen foundation is true.

## Central qualification sequence

Do not start by proving an entire library or declaring a new release mode.
The smallest consequential sequence is:

1. Specify and independently audit the exact sealed-import and compatible
   union rules against the pinned Lean implementation. Show that independently
   certified premises really discharge the conditional new proof. Include
   proof-sensitive reduction, transparent-definition and inductive-group
   counterexamples. This is the main semantic uncertainty.
2. Implement a small reference step checker for this selected profile in a
   fresh successor, with no certificate bypass in the old product. Compare
   it against full native replay on exact genuine declarations. At this stage
   local verification of all child witnesses can validate the semantics,
   but it is not yet the scale acceptance mode.
3. Select one backend only after confirming support for the actual deterministic
   program/relation, reproducible bindings and compositional theorem. Generate
   a real proof, verify it independently and require forged input/policy/body/
   namespace/rank refusals. A stub/mock/signature is not this gate.
4. Run a true three-generation reuse case: receiver B obtains certified `L`
   without ancestor proof bodies; B authors and certifies a substantive `M`
   from `L`; fresh C obtains `M`'s certificate/interface and authors a successor
   without fetching/replaying `L`'s or `M`'s proof histories. Audit actual file/
   byte accesses, installed environment, exported premises and native fallback.
5. Hold the selected interface/task fixed while increasing irrelevant or hidden
   ancestor proof history. Measure receiver bytes/time/RAM and successor prover
   work. Check that the claimed mandatory-history term is absent. Separately
   vary real interface/reduction size and direct fan-in; disclose these costs.
6. Report producer proof-generation costs, recursive certificate size, verifier
   costs, import/materialization and the full downstream contribution, using
   the same accounting boundaries as the native baseline. Preserve negative
   results. This is scale-mechanism evidence, not useful-growth evidence by
   itself.

Step 2 can use full witness checks as a development oracle, but it must not
be sold as satisfying the final no-history requirement. Step 4 must test the
next author/prover, not only a light observer. A hard-coded theorem fixture,
preinstalled full library or unnoticed shared proof cache invalidates that
particular independence claim.

The existing reader saving and paused Count/growth experiments remain useful
evidence for their own scopes, but they cannot substitute for these new
semantic and compositional qualification gates. The tentative v3 handoff
must clearly distinguish whatever software is actually qualified from this
still-unimplemented scale architecture.

## Sources and coordination

Reused local investigations, read in full for this assignment:

- [Current-v2 trust design](../../audits/succinct-checking-2026-09-24/TRUST-DESIGN.md).
- [Current-v2 succinct assessment](../../audits/succinct-checking-2026-09-24/ASSESSMENT.md).
- [Independent prior assessment review](../../audits/succinct-checking-2026-09-24/INDEPENDENT-REVIEW.md).
- [Earlier SNARK assessment](../../SNARK-ASSESSMENT.md). Its historical P0
  priority, validator-cell terminology and epoch-counter prescription are
  not new requirements or shipped mechanisms. Its guarantee/cost warnings
  remain relevant.

The pinned Lean interface/body investigation is assigned to `v3_index`;
selective dataflow/availability to `v3_growth`; root owns the synthesis and
backend/implementation selection. This note does not independently assert
new primary-source backend benchmarks or compatibility. Root supplied the
zkPi example-toolchain check and will preserve its primary-source trace.

Existing literature pointers, not newly replicated results:

- Laufer, Ozdemir and Boneh, *zkPi: Proving Lean Theorems in Zero-Knowledge*,
  CCS 2024, DOI [10.1145/3658644.3670322](https://doi.org/10.1145/3658644.3670322).
- Recursive SNARK/proof-carrying-data composition, STOC 2013,
  DOI [10.1145/2488608.2488623](https://doi.org/10.1145/2488608.2488623).
- Nova folding/IVC, CRYPTO 2022,
  DOI [10.1007/978-3-031-15985-5_13](https://doi.org/10.1007/978-3-031-15985-5_13).

The central unresolved obligations are now concrete: sound compatible sealed
imports; faithful deterministic relation/guest; recursively sound compositional
certificates; and measured active reuse without history downloads. They are
not peripheral identity, attribution, blockchain consensus or agent-prompting
questions.
