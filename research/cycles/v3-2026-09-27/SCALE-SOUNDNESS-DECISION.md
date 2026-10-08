# Scale soundness decision: the exact theorem and the next honest profile

2026-09-28 UTC. Independent decision support by `v3_growth`, commissioned by
root after the actual EQ-DAG1 campaign and repaired native handoff passed.
Read-only source/evidence assessment; no build, proof, repeated check or new
experimental allocation. Canonical workspace guard passed. Existing used
sources and outcomes remain frozen.

## Decision in one paragraph

The certified-interface architecture is realizable **conditional on an actual
faithful local-step checker and an appropriate recursive proof construction**.
The present evidence establishes neither a general Lean checker inside that
construction nor its required large-network cryptographic theorem. Strict
ranks plus ordinary one-shot SNARK soundness are not a substitute. Select a
general Lean-expression checking discriminator next, not another EQ fixture or
network wrapper. Keep existing native admission unchanged, label EQ-DAG1 as an
experimental finite-profile capability, and do not call either a completed
large-scale v3. A new scale-enabled release needs one bound, callable
receive–use–certify–export path whose receiver **and next contributor** do not
open ancestral proof histories.

## 1. State a derivability claim, not an unqualified truth claim

Fix an independently adopted profile

    P = (Lean semantics/version, foundation F, admitted declaration policy,
         canonical encoding, local checker, interface realization rules,
         certificate construction/parameters, resource/security horizon).

Let `Sem_P(I)` mean that the exact interface `I` has an admissible realization
in a well-formed conservative extension of `F`, with the advertised type,
ordered universes, external bindings and computation-relevant identities.
For a sealed theorem this means `F` derives its realized proposition, not that
its textual name occurs in a trusted file. Definitions require their exact
bodies/rules, not merely a witness of the same type. The fixed foundation can
contain its explicitly allowed axioms; semantic truth additionally depends on
the foundation's soundness. Neither cryptography nor a kernel removes that
premise. An inconsistent adopted foundation does not become consistent because
its declarations have certificates.

Separate two deterministic obligations from the probabilistic certificate claim:

1. **Local semantic preservation.** For a mathematical compliance relation
   `C_P(I; I_1,...,I_k,w)` describing the *actual new* checked extension,

       all Sem_P(I_j) and one compatible simultaneous realization
       and C_P(I; I_1,...,I_k,w)
       imply Sem_P(I).

   The base rule uses only `F`; the step checks the new proof, all exposed
   typing/conversion support and exact output binding. A list of individually
   meaningful but mutually incompatible constants is not a common environment.
2. **Implementation fidelity.** The concrete proved computation accepts only
   the stated `C_P`, including canonical decoding, policy, exact identities and
   all checked declaration/typing rules. The runtime/compiler/ISA and importer
   are included in the named trusted implementation unless separately verified.
   A host's Boolean “Lean accepted” is not an implementation of this obligation.

Write `Cl(C_P,F)` for interfaces admitting a finite grounded derivation DAG
from these base/step rules. Mathematical induction gives

    I in Cl(C_P,F) => Sem_P(I).

This is the right separation: the cryptographic theorem must authenticate
membership in the grounded closure, rather than merely authenticate that one
step's circuit found some byte strings accepted as parent proofs.

## 2. Why ordinary soundness plus rank descent is insufficient

The actual recursive circuit relation has witnesses containing parent proof
bytes. Ordinary argument soundness says that an efficient adversary cannot
convince the verifier of a false *circuit relation instance*. It does not say
that every accepting parent proof byte string which exists is semantically
valid, nor automatically expose those bytes to a reduction.

A bad child may still be a true circuit instance if its hidden witness
contains an accepting bad parent proof. Thus a proof of the one-step relation
does not by itself establish the inductive mathematical claim. Computational
soundness limits efficient construction of a false proof, not its bare
existence. Knowledge extraction, or another construction-specific PCD theorem,
is what can connect those hidden accepted parents back to an efficient attack.

Strict finite ranks exclude a genuinely cyclic compliant derivation and permit
induction **once a grounded compliant derivation is justified**. They do not
supply the missing extraction theorem. Naively extracting a binary tree to
depth `D` can cost `2^D`; even polynomially bounded depth is not enough to keep
that reduction polynomial. Shared-parent DAG structure helps honest execution,
but an efficient compressed-DAG extraction/reduction cannot be assumed merely
because the honest prover happens to maintain such a DAG.

Consequently, do not make either inference:

    one-shot security estimate + uint32 ranks => production PCD security;
    finitely many positive/negative tests => adaptive cryptographic soundness.

The uint32 ranks in EQ-DAG1 are well constrained and avoid field wraparound.
That is a useful local semantic fact, not a concrete recursion-security budget.

## 3. The sufficient construction-dependent theorem/assumption

The required security interface is **adaptive multi-claim PCD soundness for
this exact compliance predicate, parameter/key reuse and final verifier**.
For security parameter `lambda` and an explicitly bounded adaptive experiment,
let `Bad_PCD` be the event that an honest receiver accepts `(I,pi)` although
`I` is outside `Cl(C_P,F)`. The experiment permits arbitrary untrusted provers,
malicious parent bytes, observations of honest certificates, adaptive claims,
shared subderivations and concurrent participating nodes. Every honest receiver
pins the permitted construction/profile/key; the adversary cannot select a new
relation merely by sending a different verifier key.

The needed theorem has the shape

    Pr[Bad_PCD] <= epsilon_PCD(lambda; T,Q,D,S,...),

where `T` bounds aggregate adversarial computation (including any allowed
preprocessing/advice), `Q` bounds the relevant oracle/proving/claim queries,
`D` is the supported derivation/recursion depth and `S` bounds encoded step,
interface and network transcript sizes. The theorem must specify the model
(for example its random-oracle/algebraic/knowledge assumptions), allowed setup
and honest-proof access, concurrency/adaptivity and the reduction loss. These
arguments cannot be replaced by an unqualified vendor “security bits” number.
Allowed advice/preprocessing must obey the theorem's setup/oracle independence
conditions; arbitrary setup-dependent advice containing a forged proof cannot
be smuggled into a theorem that assumes advice fixed before fresh setup.

There are two defensible ways to obtain that interface:

- Instantiate an existing PCD/recursive-argument theorem and show the selected
  construction, relation, key arrangement and final verification satisfy its
  hypotheses. This is preferable to inventing a new cryptographic theorem.
- Explicitly assume that very PCD security property for the exact construction,
  **labeling it an additional unestablished assumption**, and publish no claim
  that it was reduced to the underlying one-shot primitive. This can support
  a research prototype's conditional description; it is not enough evidence
  by itself to qualify a production profile.

This is not a demand to mechanically prove every line of the v3 implementation
before useful software can ship. A published construction theorem, a careful
mapping of the actual profile to its hypotheses, explicit remaining trusted
code and appropriate independent tests/review can justify a declared conditional
assurance profile. What is prohibited is silently replacing the missing recursive
theorem with an unrelated one-shot estimate or interpreting tests as that theorem.

A recursive knowledge-soundness route is sufficient only if its extractor and
composition theorem apply to these correlated/adaptively chosen parent proofs,
auxiliary inputs and reused/self-referential parameters. It needs a polynomial
resource reduction without exponential unrolling. Alternatively, a direct PCD
soundness theorem can avoid exposing a complete witness DAG to the receiver;
the receiver is never required to run the extractor. A theorem for sequential
IVC does not automatically cover joins of independent parent certificates.

The concrete construction review must account for the exact recursive verifier,
Fiat–Shamir/domain separation if used, self/cyclic verifier-key binding, base
case and dummy/fallback branches, and the *complete* final acceptance predicate.
For the existing EQ-DAG1 experiment that last predicate includes ordinary
verification **and** exact cyclic-verifier-tail checking under the adopted
assets. The helper proof is not an application theorem. For a zkVM candidate,
it includes expected program/journal and fully resolved assumptions, excludes
fake/dev receipts, and selects a genuinely succinct final receipt rather than
an attached tree of ordinary receipts. A fold without its required final
decider is not a completed proof.

The inspected/planned general architecture does not yet identify a theorem
instantiation giving the above bound for the actually used Plonky2 parameters.
Do not write a made-up numerical `epsilon_PCD`. Deprecated status and the
upstream approximately95/100-bit estimates reinforce the research-only label;
those estimates are not per-verification error probabilities supplied by this
audit. Existing primary-source/theorem references in SCALE-CERTIFICATES are
starting points, not automatically applicable proofs about this executable.

## 4. Finite network horizon and aggregate failure accounting

Asymptotic security quantifies over polynomial-size adversaries and polynomial
query/transcript/network horizons in `lambda`. A polynomial number of nodes
each performing polynomial work still fits an aggregate polynomial budget;
“arbitrarily many nodes for unlimited time at fixed parameters” does not.
For deployment, pin a concrete cumulative work/query/claim horizon and target
failure budget. State limitations/renewal policy when that horizon is exceeded.
Increasing rank capacity does not extend the cryptographic budget by itself.

Under exact checker/implementation fidelity, a valid reduction has the form

    Pr[any bad mathematical acceptance by the horizon]
      <= epsilon_PCD + epsilon_binding + epsilon_setup_or_other_named_crypto.

Terms must cover the *whole* adaptive experiment, with their actual reduction
resource losses, and must not double-count assumptions already inside the PCD
bound. Binding covers every commitment whose collision could change meaning,
including authenticated environment/type/definition lookup. If setup has no
trusted ceremony, do not invent a ceremony probability; use that construction's
actual assumption. If one profile verifier/image is substituted by an allowed
upgrade, the theorem must cover that transition rather than treating an old
receipt as a certificate for a different checker.

If, and only if, a theorem supplies a bound `delta_j` for the next bad acceptance
conditioned on every allowed prior adaptive history, the union bound gives
`Pr[any bad] <= sum_j delta_j <= N*delta`. Independence is unnecessary. If the
theorem already gives an adaptive multi-claim bound, do not multiply it by `N`
again. Rechecking identical deterministic bytes is not a fresh random trial;
the actual attack/query model controls the useful count. An illustrative bound
`delta=2^-128` and `N=2^40` would give `2^-88` **if those hypotheses held**;
this is not a bound established for Plonky2 or any current project artifact.

An exploitable checker, importer or encoding bug is not a negligible-error term
we can estimate from the number of tests. It is a possible violation of the
deterministic fidelity premise. Source review, independent checkers, differential
tests and formal verification address that risk separately. They cannot be
converted into invented cryptographic confidence percentages.

No global ledger, identity vote or worldwide counter is required to articulate
these bounds. A node's local request quota alone also cannot upper-bound an
attacker's prior worldwide computation. Use a defensible threat horizon and
conservative parameter policy, not a claim to observe all activity.

## 5. Minimum honest supported profile

**What can be claimed now.** The delivered native product retains its existing
native acceptance/replay assurance. The actual EQ-DAG1 work is a separate finite
experimental certificate implementation with source-reviewed local semantics
and audited executions. The repaired Lean handoff checks an exact conditional
theorem and retains both parent premises. It neither certifies arbitrary Lean
proofs nor turns those certificate premises into stock Lean proof terms. The
unimplemented typed adapter and an unqualified source16 package are not current
release features. No production scalable profile or useful-growth result exists.

**Smallest consequential general successor to select.** A theorem-extension
profile, provisionally `L4S-THEOREM1`, over one pinned foundation and one fixed
authenticated definition/inductive environment is a coherent initial target:

- Inputs are actual supported Lean expressions, universes and new theorem
  proofs, not five equational recipe tags or a hard-coded list of true results.
- Old derived `Prop` theorems enter only through exact certified sealed
  interfaces. New base axioms, arbitrary module imports, unsafe execution and
  unbacked interface entries are refused. The final step discharges every
  certified imported premise through parent certificates.
- The checker binds full type/support/lookup data and one shared realization.
  Type support may be large and is charged. A fixed base is a disclosed local
  asset, not a hidden ancestry service or a changing globally trusted catalog.
- No new definitions/inductives need be admitted in the first profile; those
  require later explicit conservative-extension checks. Ordinary theorem
  reasoning over genuine base definitions remains required. Local proof-term
  `let`s do not by themselves add global definitions or authorize new axioms.
- Unsupported proof-sensitive conversion returns a controlled refusal. There
  is no fabricated definitional equality and no automatic ancestor download.
  This is an intentionally incomplete source-compatibility profile, not a
  claim that every stock Lean proof can be replayed unchanged.

This is a **prospective implementation contract**, not an already demonstrated
profile. A fresh general-expression typing/conversion checker discriminator can
test whether it is operable without adding crypto or production authority first.
The release label must state the implemented support envelope. A tentative v3
may deliver native improvements plus reproducible scale research; that still
leaves the user's full scale-enabled usable-software requirement incomplete.

## 6. One falsifiable receiver-and-contributor ancestry gate

Before any new launch, select one actual supported theorem and a substantive
new Lean proof using two independently certified parents. Keep the exact parent
interfaces, common foundation/definition support, new proof task and direct
fan-in fixed. Vary ancestral proof-body volume/history and unrelated corpus
volume independently. Do not manufacture extra EQ joins as a substitute for
the missing general checker or call these workload choices network obligations.

Require all of the following in the same selected architecture:

1. A fresh receiver has only the adopted static assets, requested capsule,
   finalized certificate and explicitly selected authenticated interface/data
   support. Ancestor bodies/receipts and global catalog are absent/unavailable.
   It verifies the exact theorem without producer-supplied success authority.
2. A fresh contributor has those same selected interfaces/data and the immediate
   parent certificates, plus its own new proof/witness. It checks and certifies
   the new theorem without replaying parents' proofs, fetching grandparents,
   flattening a dependency census or requesting whole-history prover preparation.
3. A third fresh receiver accepts the actual exported child packet under the
   same profile without access to that contributor's private state or history.
   Conditional native checking alone, a cached receipt or unresolved proof
   assumption fails this step.
4. Bind and record every application read, callback, remote request and stage
   input. Physical absence or access-denial of excluded archives is stronger
   evidence than voluntary logs alone. Distinguish application-read auditing
   from an OS sandbox; never claim the latter from the former.
5. Account cold initialization/static reads, selected support, trace generation,
   recursive parent verification, proving, final verification/import/export,
   failures and output size. Record CPU, wall, peak memory and bytes separately.
   A trace or hidden witness scaling with ancestor history fails contributor
   independence even if the final proof is short.
6. Refuse wrong statement/profile/key/universe/context/body binding, unbacked
   parents, unrecognized assumptions, missing selected support and exhausted
   limits. Missing *irrelevant ancestral* bodies must not cause refusal or
   fallback; missing genuinely selected computation data may cause need-data.

The expected cost shape is

    receiver = selected exposed bytes + final verification + bounded lookups;
    contributor = own checking/trace work + selected data + k parent checks
                  + certificate overhead for that new work.

No mandatory term may be linear in unrelated corpus size or ancestral proof
history. Genuine statement/definition/trace work remains charged. A finite
gate falsifies hidden dependencies and measures constants; the general locality
claim still needs source/architecture analysis. Timing alone cannot prove it.

There is currently **no pass** for this combined general-Lean gate. EQ-DAG1
supplies reusable evidence for the narrow recursive dataflow; the native seam
supplies reusable evidence for sealed conditional reasoning. Running either
again does not fill the missing certificate-of-new-Lean-checking edge.

## 7. Challenges to the two concrete implementation candidates

**Full kernel in a proved VM.** Require an actual closed deterministic guest
dependency manifest/build and the checked `lean_add_decl` path. The inspected
Lean4.34 runtime initializes facilities outside a simple pure checker; C++ guest
support is not a build result. Bind successful termination, exact program and
output, selected foundation/support and resolved parent receipts. A host Lean
call, a guest checking a host status bit, or a composite receipt containing all
old receipts fails. RISC Zero remains a candidate, not a closed port; see the
source-backed feasibility decision rather than reopening the same broad survey.

**General-expression typing/conversion trace.** This can shift search and
normalization work to an untrusted producer, but the trace checker must enforce
every rule needed for actual Lean expressions. DAG judgments must bind the exact
local binder context and let-values, universe instantiation, typing/reduction
mode and authenticated environment lookup. A valid trace node cannot be reused
under a different context just because expression bytes match. Substitution,
definitional equality, projection/recursor/quotient behavior and accepted level
rules need precise coverage or controlled rejection, not assumed completeness.

Its environment invariant must come from the fixed base and compatible certified
extensions, not Merkle membership alone. It must stop at sealed theorem proof
boundaries; flattening ancestor well-formedness/typechecking traces reintroduces
the contributor bottleneck. Trace creation, DAG growth and large normalization
can dominate cost; charge them. A valid small trace for one constructor is not
a Lean4.34 soundness correspondence. A checker targeting another Lean version
must not silently borrow this profile's foundation identity.

The proposed nonadmitting general-Expr discriminator is a reasonable next
engineering selection **only after root fixes its exact rule subset, differential
endpoint and failure/stop budget**. It can reject a bad checker direction quickly;
it is neither cryptographic certification nor acceptance-mode adoption. The
central open edge is precise enough to investigate without promising a complete
new kernel overnight.

**Independent candidate cross-check.** The completed
[trace decision](LEAN-TRACE-CHECKER.md) incorporates the exact-context,
no-ancestor-WF and trace-cost challenges above. It correctly distinguishes an
unfinished proof of a checker rule from evidence of an executable exploit.
Its preference for qualifying one existing general checker, rather than
simultaneously creating another partial checker, is efficient and supported.
Root's pinned nanoda candidate in [GENERAL-CHECKER-DECISION](GENERAL-CHECKER-DECISION.md)
therefore merits one bounded nonadmitting differential/SEALED_PROP discriminator
before a new trace implementation, if its structural/parser gaps are closed.
This is not automatic trust in a recently updated alternative kernel.

Efficiency's source-closure investigation reports that the full native guest
still needs generated Lean exports, audited initialization, C++/exception/TLS
support and target runtime closure; `MULTI_THREAD=OFF` does not remove every TLS
dependency. Those are actual unresolved build obligations, not proof of
impossibility. A Rust target merely appearing in a toolchain's target list does
not establish installed target libraries, guest compilation or runtime behavior.
The pure-Rust route avoids one class of dependency; it does not establish semantic
fidelity or certification of imports.

For either route, malformed structural annotations such as a projection's
declared structure/index must be checked by the *proved* program/import adapter.
Correctness of the honest exporter and agreement on valid examples cannot
compensate for a checker which accepts hostile alternate encodings differently
from the adopted semantics. This challenge does not commission an additional
experiment or duplicate root's exact-source candidate investigation.

## Evidence reused; no duplicate execution

- [General selected design](SCALE-DESIGN.md), [requirements](SCALE-REQUIREMENTS.md),
  [actual executed boundary](SCALE-EXECUTED.md).
- [Certificate/security obligations](SCALE-CERTIFICATES.md),
  [pinned guest feasibility](SCALE-BACKEND-FEASIBILITY.md).
- [Actual EQ-DAG1 source review](../../../experiments/scale-equation-01/SOURCE-REVIEW.md)
  and [campaign outcome](../../../experiments/scale-equation-01/CAMPAIGN-OUTCOME.md).
- [Repaired conditional native outcome](../../../experiments/certified-equation-interface-02/OUTCOME.md)
  and [remaining integration gap](../../../experiments/certified-equation-interface-01/INTEGRATION-GAP.md).

These sources ground the current status. The formal distinctions and proposed
security/gate contract above are this audit's decision support, not a newly
proved metatheorem, a backend security reduction or a selected experimental run.
