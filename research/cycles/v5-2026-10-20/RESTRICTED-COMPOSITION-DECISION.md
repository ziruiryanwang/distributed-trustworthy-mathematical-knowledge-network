# Decision: a checked composition fast path in the existing module architecture

Status: source/theory decision, not an implemented checker, new trust adoption,
measured speedup, or permission to build/prove. Root owns those selections.
Canonical project root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision and immediate purpose

The exact FIRST/I typed-execution screen consumed 148 po18 segments, above the
prospectively fixed 128. Do not fund that proof, prepare its prefix, enlarge the
screen after observing it, or call a different theorem an improved FIRST result.

The next architectural candidate is **a sound, intentionally incomplete checker
for typed composition in the existing Lean/module expression language**, called
RC below. Its outputs are ordinary existing v5 theorem descriptors. It is not a
second mathematical language, a named-recipe system, an untrusted simplifier, or
an alternative definition of mathematical validity.

RC checks explicit term application, abstraction and bounded beta/zeta
conversion against authenticated declarations. Equality composition is ordinary
application of already authenticated `Eq.trans` and `CommonsV5.binary_congr`,
not a new equality axiom. Unsupported conversion is a refusal. Arbitrary
induction, transparent-definition unfolding and new inductive declarations are
outside the initial fast path. The existing general relation remains the route
for mathematics outside it; no submission is silently weakened to fit RC.

This removes general kernel/export work from a common *class of new
contributions*. It does not solve the cost of first certifying every difficult
mathematical method. That expensive establishment and cheap repeated certified
composition are separate investments. Whether the latter pays for the former
remains a full-cost question, not a theorem-count claim.

## What already exists, and why it is not this change

| Existing source | Actual capability | What remains checked elsewhere |
|---|---|---|
| v4 `library/library_lower.py` and named-library API | Typed-macro DAG, memoized closure and universe substitution; a named term lowers to an ordinary term | Full final native/guest checking; selected definitions are expanded |
| v4 `source/companion/cert_application.py` | Explicit source-free proof-term graph and exact expected capsule | Dependent application typing and all final mathematics |
| v4 `source/companion/proof_compose.py` | Capture-safe substitution of closed proof fragments, exact frontier/capsule conservation and bounded interning | Its header and `compose_packet` explicitly say UNVERIFIED; full relation still runs |
| v5 `modules/receipt/src/relation.rs` | Authenticated parent/group/body binding, native-row correspondence, native parsing and conditional extension checking | Every new local declaration uses the general native checker |
| v5 `aggregate_claims/relation.rs` | Authenticated I or same-image A frontiers, internally established exact parent journals, DAG/rank/closure checking | Every new delta invokes the existing module relation |
| Current interface-only receiver and incremental native receiver | Selected interfaces, explicit missing semantics, exact warm observation reuse | They do not produce a new portable certificate for the new theorem |

Reuse their codec, commitments, group identities, graph/rank rules and receiver
authority distinction. Do not rewrite their assemblers and claim a proof-cost
breakthrough. RC must replace actual checking work, not move it into an omitted
cost column.

## Trust and mathematical statement

Let F be the exact adopted foundation, P the existing module semantic policy,
and E an immutable qualified environment extending F. Existing module names are
`DMKN.Mod.<ModuleSpecID>.<relative-name>`; binder universes are ordered positional
parameters. Different module owners do not share an unqualified namespace.

The intended mathematical assertion of RC is:

> Given authenticated valid imported declarations under F/P, each exported
> ordinary theorem has its exact declared Prop type in the extended environment.

This assertion is conditional until actual receipt verification establishes all
external premises. A host report, checked syntax, membership opening, native
success transcript or `verified=true` field is not a premise discharge.

There are two distinct refinement obligations:

1. **Lean soundness:** accepted RC typing/conversion derivations embed into Lean's
   calculus for the same exact foundation, universes, names and declared types.
2. **Existing-module correspondence:** the accepted input determines an ordinary
   native-row witness satisfying the existing module correspondence and
   *conditional* module-extension relation, with exactly the claimed descriptors
   and parents. This is needed before retaining the existing I-shaped semantic
   member journal in a new aggregate image. Soundness of an unrelated calculus
   would not establish this claim.

The second is not a claim that an independent I receipt for that new member
already exists. Current A members already distinguish semantic member warrants
from genuine independently verified I receipts. Nor does it require an
already-produced I receipt for each intermediate A member: graph induction
establishes conditional premises inside the aggregate.

Neither obligation is proved merely by this design note. The rules below state
the proof obligation precisely enough for implementation and independent review.
They must be discharged for the supported subset before adoption. Existing
general checker-to-Lean assumptions also remain visible; a proof of checker
execution does not repair a checker bug.

## Exact input and selected signature

Use the existing canonical expression tags from `modules/codec.py`:
`bvar`, `sort`, `const`, `app`, `lam`, `forall`, and `let`. Initially reject `proj`
in new terms/types that RC must inspect. References retain exactly the existing
`foundation`, `external`, and `local` interpretations. There are no metavariables,
free term variables, unification requests, caller-selected axioms or proof flags.

One RC delta contains:

- F/P, the existing exact local module spec, exact mathematical rank, and ordered
  new singleton ordinary-theorem groups. `value_hash` is null and `meta` empty,
  as required by the current theorem schema.
- Exact established parent journals and existing group openings for each imported
  declaration used by checking. Parent relation/image/foundation/policy, module
  uniqueness and strict rank checks are retained.
- One explicit canonical proof expression per new theorem, with the same ordered
  universe binder count as its descriptor. Every proof is checked; no unused
  proof or unbound export is allowed.
- Bounded whole-input bytes, expression visits, substitution expansion, depth,
  imported groups, new groups, proof bytes and output/cache bytes. Work and
  expansion are charged across the whole delta, not reset per lemma or retry.

No full foundation native-row prefix, native export, or earlier proof body is an
RC input. A compiled exact foundation signature is derived from the already
adopted F and pinned with the checker. Its correspondence is reviewed once as
part of the new image; an arbitrary caller-supplied signature cannot replace it.

Initial imported ordinary declarations are handled as follows:

1. Verify their exact existing group openings against established parent J.
2. Interpret `local` in an imported descriptor relative to that descriptor's
   owner, never relative to the new module.
3. Fix universe arity and exact type; instantiate universes simultaneously.
4. Resolve any additional signature declarations actually required for typing.
   A missing type declaration is an explicit unresolved/refused input, not a
   fresh abstract constant.
5. A transparent definition may be *mentioned* using its certified type without
   its body. RC does not unfold it. When the claimed typing equality requires
   its body or a computation rule, initial RC refuses `UNSUPPORTED_CONVERSION`.

For the first implementation, require the finite selected **type-reference
closure** to be authenticated, with ordinary declarations only outside F.
This is conservative and keeps the signature wellformedness argument small.
It includes dependencies hidden inside transparent *types*, not only symbols
visible in the final equality. It excludes all imported proof bodies and all
unrequested transparent value bodies. It may itself be large for some inputs;
there is no constant-cost or global-interface-independence claim.

Complete atomic inductive groups remain the existing import unit. Initial RC
does not open a nonfoundation inductive group; extending this restriction later
must reuse the exact existing census/ownership/rule commitments, not admit a
constructor or recursor as an unexplained ordinary axiom. The initial available
`binary_congr` workload needs no `Tree` import: its signature uses parameters and
foundation equality only. Thus this restriction is actually satisfiable by an
existing genuine certificate, rather than assuming a new easy-to-obtain premise.

## Typing rules and explicit Lean embedding

Write `E; U; Gamma |- t : T`. U is the exact ordered universe parameter list;
Gamma is an ordered, wellformed telescope. All term indices are de Bruijn indices.
The implementation must implement lifting and capture-avoiding substitution,
including beneath binders; context-dependent cache keys include their context
and universe substitution, not only the uninstantiated term digest.

The following is a specification of a restriction of ordinary Lean rules.
It is not permission to trust an annotation of a type or a derivation node.

| Form | Mandatory premises | Inferred or checked conclusion |
|---|---|---|
| `sort u` | u is a scoped valid Lean universe expression | `Sort u : Sort (succ u)` |
| `bvar i` | i is in the current wellformed telescope | The binder's recorded type, lifted by the exact de Bruijn lookup rule |
| `const c us` | c resolves to F, an authenticated import, or a strictly earlier checked local theorem; exact universe arity; every universe in scope | The authenticated type of c after simultaneous universe substitution |
| `forall A B` | `A : Sort u`; under `Gamma,x:A`, `B : Sort v` | `Pi x:A, B : Sort (imax u v)` |
| `lam A b` | `A : Sort u`; under `Gamma,x:A`, `b : B`; inferred B is a wellformed type | `fun x:A => b : Pi x:A, B` |
| `app f a` | inferred type of f beta/zeta-normalizes to `Pi x:A,B`; `a : A'`; supported conversion establishes `A' =def A` | `f a : B[a/x]` |
| `let A v b` | `A : Sort u`; `v : A'`; supported conversion establishes `A' =def A`; under `Gamma,x:A`, `b : B` | `let x:A:=v; b : B[v/x]` |

Implementation may use sound bidirectional checking to avoid redundant inference,
but every premise above remains justified. In particular, matching an untyped
application's output shape is not an application rule. Treating binder types as
trusted because the final statement is called a theorem is unsound.

At each export, check its closed declared type T is a Prop (`T : Sort 0`) and
its supplied closed proof has a type supported-convertible to **that exact T**.
Universes remain universally quantified parameters, not one tested valuation.
Earlier local theorems are available in order only after this check. Reject local
self-reference, forward references, duplicate names and ordinary declaration
cycles. No new definition, opaque value or inductive group is initially exported.

All these syntax forms embed directly into the existing canonical-to-Lean
interpretation. Application embeds to Lean application, binders to Lean binders,
and local theorem addition to ordinary conservative theorem introduction. The
soundness induction is on the checked derivation, then on ordered local exports,
then on the aggregate's strict parent graph. Capture-safe term substitution and
simultaneous universe substitution are separate lemmas, not one informal replace
operation. Universe parameters inside replacements are not recursively replaced.

### Conversion is deliberately incomplete

Supported definitional conversion consists only of:

- alpha-insensitivity already supplied by positional term/universe binders;
- structural equality of qualified constants and their universe arguments;
- beta reduction `(fun x:A => b) a --> b[a/x]`;
- zeta reduction `let x:A:=v; b --> b[v/x]`;
- congruence of these reductions under expressions and binders;
- disregard of binder-info annotations *for conversion only*, as Lean does.
  Exact exported descriptors still preserve their declared annotations/bytes.

Universe conversion uses a small, separately justified simplifier: at least
`imax(u,0)=0`, `imax(0,u)=u`, `imax(u,succ v)=max(u,succ v)`,
`max(0,u)=max(u,0)=u`, and `max(u,u)=u`. The first identity is necessary to
recognize universally quantified propositions as Prop. Otherwise compare
normalized universe syntax exactly. Do not assume arbitrary syntactic level
inequality or universe inequality is an admissible coercion.

There is no initial delta unfolding, iota/recursor reduction, projection
reduction, eta rule, general proof-irrelevance conversion, quotient reduction,
type-class search, tactic execution or theorem-as-rewrite conversion. A theorem
proving `a=b` is not itself a definitional-equality rule. Use its proof explicitly.

Normalization is bounded and failure is terminal for this delta. Exhaustion,
unsupported forms or unresolved required signatures cannot produce an equality
judgment from partial output. All substitution expansion is charged, including
memoization misses under different contexts; an acyclic syntax DAG alone does
not imply a linear substitution bound. Exact structural equality can be a safe
short path once both sides' typing obligations are established.

Beta/zeta reduction of a transparent definition's *name* does not reveal its
body. If a caller needs delta/iota, it must use the general lane or a separately
designed future checked conversion witness. Missing bodies never become opacity
assumptions that falsely make an intended conversion succeed.

## Equality composition and a genuinely available endpoint

The retained genuine I receipt is:

`experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin`

223,594 bytes, SHA-256
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.
Its module is
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
It certifies `CommonsV5.binary_congr`, whose exact type is:

```text
{A : Sort u} {B : Sort v} {C : Sort w}
(f : A -> B -> C) {a a' : A} {b b' : B}
(ha : a = a') (hb : b = b') : f a b = f a' b'
```

It does **not** certify `fusion`, `fold_map`, or FIRST merely because their source
appears later in `FoldFusion.lean`. FIRST has no new genuine portable certificate.
SECOND calls FIRST twice and is therefore only a conditional demonstration of RC
expressivity until a genuine FIRST premise exists. Do not use SECOND to conceal
the same unresolved expensive premise.

An actually premise-available initial workload is application-context transport.
For arbitrary suitably typed binary functions f,g,h and pointwise equality
witnesses `a=a'`, `b=b'`, `c=c'`, derive:

```text
f (g a b) (h b c) = f (g a' b') (h b' c')
```

Its proof is three typed applications of the genuine `binary_congr`, with shared
middle equality premise; all universes, intermediate types and implicit
arguments are explicit in the canonical proof. Chain such a result through an
additional equality step using the exact foundation `Eq.trans`. The output is
parametric, not checking one numerical input, and requires neither Tree induction
nor transparent reduction. The method generalizes to finite application-context
DAGs by structural construction of these ordinary proof terms.

This is an honest first integration endpoint, **not** a claim of a new difficult
mathematical discovery, full-cost growth or FIRST acceleration. Its value is that
it exercises actual parent certification, typed parametric composition and a
renewable certificate route using available premises. A second independent
client must import the resulting theorem as an authenticated member and compose
a further theorem without reopening its proof. That is the reciprocal endpoint,
not simply running RC on an isolated toy term.

## Exact journals, aggregate compatibility and receiver use

The module spec and group commitments remain those of
`modules/receipt/src/commitments.rs`. A journal binds F/P, exact module identity,
group root/count and strict rank. Existing theorem identity intentionally binds
the exact Prop type, **not its proof witness**. RC must check every supplied proof
form against that type, but cannot claim the J bytes authenticate a particular
proof provenance. The adopted relation image binds which checking rules were
executed. If proof provenance were ever desired it would need a separate field;
it is not needed for this mathematical acceptance claim.

Use a freshly reviewed/adopted aggregate image A-RC. Do not invent an I receipt,
overwrite the old I image, or feed an RC success Boolean to the old receiver.
The new image may retain existing semantic I-shaped member J values only after
the conditional-module refinement above is established. It continues to assert
the same module semantics; it does not assert that the old I guest ran on each
member. This is the same distinction between A members and I receipts that the
current receiver already makes.

The smallest initial aggregate input authority permits:

1. Genuine fixed-I receipts as frontiers, verified by exact image and J.
2. Same A-RC-image receipts as aggregate parents, with exact existing membership
   openings and rank/closure checks.
3. RC-checked new deltas, with every imported J already established in the DAG.

Retain the old general delta checker as an explicit separate supported path if
root selects it; dispatch uses an unambiguous versioned input schema and charges
that path's complete work. It must never fall back to trusting the failed RC
result. A versioned dispatcher can share the aggregate graph, member commitment,
closure, pending-assumption and receipt pipeline instead of adding an unrelated
certificate format. The existing wire/census/host must explicitly recognize the
new delta schema; a changed guest alone is not an integrated feature.

**Old homogeneous-A parents are not automatically compatible.** Their image is
not A-RC. Initial A-RC refuses them. A future explicit bridge may verify an exact
adopted old-image receipt and open its members, but requires a distinct supported
assumption tag, image allowlist, assurance argument and controls. Rewriting its
header image, reusing an old trust token or passing the same bytes as an A-RC
parent is never permitted. Genuine I frontiers suffice for the initial endpoint.

Receiver integration should reuse `VerifiedAggregate` and
`VerifiedAggregateMember`, not manufacture `VerifiedModule`. Current
`trust_withdrawal/aggregate_claims/aggregate_admission.py` already binds the
actual caller-adopted aggregate image, native verifier executable, source/runtime
pins, foundation/policy and current live trust binding. A-RC needs a real new
adoption and coherent installed profile. Existing native authoring/import can
consume its exact semantic members only after the refinement and owner checks;
the continuing-context interface must preserve its original grant/counters and
invalidate stale views. This connects the fast path to ordinary agents, rather
than requiring a disconnected RC-only toy client.

Combining independent modules retains existing namespace, exact type and
foundation/policy checks. Equal theorem names under different module IDs remain
different constants; different data must not collide under the same qualified
identity. No merge makes disagreeing definitions equal. Proof witness variation
for an identical theorem descriptor remains permitted by the current policy.

## Work removed, work retained, and the cost argument

For an RC delta let S be selected signature/opening bytes, Pnew new proof/type
syntax, W the charged substitution/normalization work, and H hashing/group work.
Its checking work can be bounded by a constant times `S + Pnew + W + H` for the
specified finite representation and implementation. W is a charged variable,
not assumed linear in Pnew. There is no necessary term for ancestral theorem
proof bodies, full native export construction, general reduction search, or
rechecking earlier valid theorem derivations.

General v5 already omits ancestral theorem proofchecking. The incremental gain
claimed here is narrower: no native-row reconstruction/parser, no general local
kernel execution for RC deltas, no mandatory foundation-row traversal, and no
transparent bodies used only by more general checking machinery. It is not
honest to credit RC with the no-ancestral-proof property as if v5 lacked it.

The following costs remain: authenticating selected interfaces, expression and
universe wellformedness, substitutions, conversion, exact target binding, parent
receipt assumptions, cryptographic proving, receipt resolution/verification,
service and failed searches. Fixed po18 prover workspace and per-segment crypto
are not improved by this checker design. We predict fewer *guest instructions*
for an appropriate identical composition target, not a measured percentage or
constant-time certification of arbitrary mathematics.

A proper comparison uses the same exact output descriptor, initial certified
parents, representation optimizations and receiver policy in RC and the existing
general path. Baseline may use all existing v4/v5 assembly and cache improvements.
Count creating/adopting the specialized checker as engineering investment and
all per-method certificate/service costs as operational investment. The previously
stated full-cost sharing inequality remains the release criterion. RC does not
establish it merely by having a smaller inference-rule list.

## Smallest useful implementation and stopping rules

Recommend source implementation only after independent challenge of this note:

1. One bounded typed-expression/checking core over the existing canonical forms;
   reuse exact codec/group/policy definitions. Start with the genuine base-I
   theorem, ordinary imports and beta/zeta only. Specify the exporter/refinement
   witness, not a new ad hoc theorem envelope.
2. One fresh aggregate successor/dispatcher that reuses the existing graph and
   receipt machinery, with I plus own-image parent authority. No old-A bridge,
   new blockchain, global task list, alternative catalog or broader parser tuning.
3. An explicit public preparation path that produces the exact existing module
   spec/proof input and uses existing import/discovery/custody interfaces. New
   submission schema support must be coherent across host, receiver profile,
   limits and authoring; source-only success cannot mint authority.
4. Focused negative controls at genuinely new seams: wrong parent type/universe,
   untyped binder, capture, substitution under binders, free/forward reference,
   forged descriptor, changed expected type, missing transparent-type dependency,
   unsupported delta/iota, fuel exhaustion, rank cycle, proof-as-I confusion and
   old-A-image relabeling. Existing passing receipt/custody suites are not rerun.

Before any expensive proof, root should have a source-backed refinement argument,
a genuine selected premise, the same target in both lanes, and one reviewed
prospective execution/proof envelope. A single cheap changed-boundary screen may
then test instruction-cost assumptions. Stop if the fragment requires general
conversion to express the selected target, if the semantic-member refinement
fails, or if integration costs dominate the expected savings. Do not repeat
profiles or buy a smaller unrelated target after observing a failed screen.

This decision selects a route with different dominant work, not another RAM
survey or an attempt to fund the rejected 148-segment FIRST run. It leaves the
full v5 objective open while directly addressing economical, recursively reusable
portable contributions within the current architecture.

## Source references and evidence boundary

Read-only sources used for this decision:

- `product-local/v4-library-commons-02/commons-v4/docs/named-library-API.md`
- `product-local/v4-library-commons-02/commons-v4/receiver/APPLICATION-API.md`
- `product-local/v4-library-commons-02/commons-v4/library/library_lower.py`
- `product-local/v4-library-commons-02/commons-v4/source/companion/cert_application.py`
- `product-local/v4-library-commons-02/commons-v4/source/companion/proof_compose.py`
- `software/v5/modules/codec.py`
- `software/v5/modules/receipt/src/{relation,commitments,policy,journal}.rs`
- `software/v5/modules/native/checker/src/{module,module_correspondence}.rs`
- `software/v5/aggregate_claims/{relation,header}.rs`
- `software/v5/trust_withdrawal/aggregate_claims/aggregate_admission.py`
- `software/v5/workloads/{FoldFusion,ReceivedFoldMap,DeltaFoldMapTwice}.lean`
- Current source map and decisions in `research/NOW.md` and `registry/WORK.md`.

No runtime import, parser sweep, build, test, proof, Git mutation, deletion or
resource reconnaissance was performed for this note. Earlier used files and
failed screens remain unchanged. Root and independent reviewer decide adoption.
