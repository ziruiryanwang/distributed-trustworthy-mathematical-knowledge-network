# Central adversarial triage after rejected v4 handoff

2026-10-06 UTC. Author: `/root/v4_central_reaudit`. Canonical workspace guard
passed using the documented process-local PowerShell policy invocation. This is
a source/theory audit, not a product execution, new checker adoption or test pass.
The latest user explicitly rejected the earlier local release as meeting v4 and
resumed work until **10:00 Chicago / 15:00 UTC on October 6**. Its frozen evidence
remains useful; its version-completion judgment is not an acceptance criterion.

## Central judgment

The previously shipped artifacts establish a bounded reciprocal mathematical
loop, not yet a generally operable huge-network commons. The meaningful next work
is to change an actual binding limitation, rather than repackage the same loop or
increase audit counts. The most important simultaneous requirements remain:

| Requirement | Current evidence supports | Central missing property |
| --- | --- | --- |
| Trustworthy proof reuse | Actual bounded proof substitution above genuine certified cut points; fresh final guest check | General applicability, affordable whole-operation cost and maintainable policy migration |
| Scalable discovery | Bounded local type index and selected contacts | Maintained decentralized paths to relevant holders under explicit capacity/churn conditions |
| Reciprocal useful growth | Received law used in a new checked law and returned through actual TLS | A concrete available capability with justified net savings after search, admission, premises, storage and serving costs |
| Reusable vocabulary | Genuine safe transparent F-closed definitions | Layered semantic vocabulary without requiring every new definition to depend directly on F only |
| Broad release | Relocated same-host package and public commands | Supported operating envelope, maintenance lifecycle, independent-host scope and unresolved licensing |

No universal cheap complete search, universal novelty oracle, unconditional growth
rate, or mathematically optimal proof search is needed. Conversely, noting these
impossibilities does not excuse absent implementable conditional guarantees.
Independent agents should benefit on a stated nonempty class of demands without
subscribing to a mandatory goal list or human-intention acceptance mechanism.

## Actual semantic restriction, traced through current source

Source baseline is `experiments/certified-seal-01/project`. The selected package
contains these source bytes, and this audit does not edit them.

1. `guest/src/relation.rs`, `Dags::foundation_closed` and the contributed `def`
   branch: both type and body may reference only the reserved fixed foundation.
   A contributed definition must be safe, transparent, singleton, canonically
   named from its exact descriptor and genuinely checked as a Definition. Its
   declaration cannot depend on another contributed definition or a selected
   proposition, even if that other declaration has already been checked.
2. `companion/cert_capsule.py`, `inspect_capsule`: a Definition has empty nested
   `definitions`, and type/body constant names must be in fixed support. A Prop
   capsule includes exactly its direct non-F type definitions, sorted by ID,
   with a maximum of four. F-closure makes direct and transitive requirements
   equivalent today; they cease to be equivalent after the proposed extension.
3. `native/ImportTail.lean`, `validateDefinition`, `addExactDefinition`: native
   checking enforces the same F-only reference condition independently. All
   definitions are installed before selected proposition axioms. Existing
   `definition-capture` and `definition-finalize` prohibit parent context and
   recheck under clean support alone.
4. `guest/src/journal.rs`, `Member::validate`: Definition outputs require an
   empty `required_definitions`; Prop outputs contain up to four. These are
   current wire semantics, not an incidental UI limit.
5. `companion/proof_compose.py`, `Packet` and `Composer.finish`: every supplied
   definition is projected as F-closed and re-inspected. The composer already
   orders declaration dependencies, but its current capsule construction and
   F-closed inspection preclude layered definitions before that order helps.
6. `guest/src/main.rs`, `guest/src/journal.rs` and `host.rs`: selected receipts
   use the currently adopted image. Parent journals are validated under that
   same image and foundation; guest recursive verification likewise uses that
   image. A new checker image is not a transparent upgrade of old certificates.

The fixed table is **43 support declaration records containing 66 reserved
constant names**, not 43 arbitrary Lean features. Expression constructors include
sorts, variables, constants with universe instances, application, lambda/forall,
let and projection. The packet schema contains inductive records for existing
foundation support; the guest rejects **nonfoundation** inductive declarations.
Safe source recursion may elaborate through an existing F recursor, but a new
recursive constant or auxiliary group outside F is not thereby supported.
String/natural-literal extensions are disabled in the selected Nanoda config.
This is not arbitrary Lean/mathlib support.

### Smallest missing case

Conceptually, take universe-polymorphic transparent definitions

```lean
def Twice {α : Sort u} (f : α → α) (x : α) : α := f (f x)
def FourTimes {α : Sort u} (f : α → α) (x : α) : α :=
  Twice f (Twice f x)
```

The first definition has no contributed constant in its type/body. The second
does, so direct canonical publication of the two-node dependency graph is
rejected independently at native, capsule and guest boundaries. This claim is
deduced from inspected source, not presented as an executed Lean test. A more
useful instance is a reusable repeated-squaring operation defined using received
`Iter`; the same dependency restriction applies. Manual inlining can express a
result, but does not preserve a reusable named dependency graph.

## Two distinct fixes: do not confuse them

### Route A: bounded semantic compilation into the unchanged relation

An authoring adapter can eliminate selected safe transparent acyclic helper
definitions before producing a current F-closed definition. Replace a helper
constant `D.{us}` by its exact body with formal universes instantiated by `us`,
then recursively eliminate only the selected helper references. Operate on an
interned expression DAG and memoize by exact definition/instantiation (and by
other relevant substitution state). Do not execute arbitrary source to download
a definition, and do not interpret a remote success flag as typing evidence.

Conditional correctness argument: assuming each helper is a genuine well-typed
safe transparent definition in an acyclic environment, delta expansion and
well-scoped universe substitution preserve typing by ordinary conversion and
substitution lemmas. The final expression is independently checked under clean
F by the unchanged native/guest path. Therefore the compiler is not a new
mathematical authority. Claiming that it preserves the *requested* source
definition additionally requires an exact transformation/convertibility check;
final typing alone would not establish that correspondence.

Important implementation constraints:

- Inline only explicitly eligible helper Definition bodies, never body-free
  selected Prop assumptions, unsafe/partial/opaque definitions, inductive groups
  or arbitrary mutable frontend declarations.
- Instantiate universes exactly, detect missing/excess instances, retain free
  variable/metavariable rejection, and refuse cycles before expansion.
- Keep term application explicit instead of eager beta normalization. Closed
  declaration bodies do not require capturing local binders merely because
  they are substituted beneath a binder; universe specialization still matters.
- Bound unique specialization states, visited nodes, emitted bytes and depth.
  Give no polynomial-in-source-size guarantee without restricting instance
  proliferation. Even acyclic graph syntax can describe very expensive demanded
  evaluation; syntactic sharing does not prove an evaluator shares computation.
- Preserve the authored source, helper selections, exact original and expanded
  types/bodies, final canonical ID and refusal evidence in a new allocation.

This is a useful authoring improvement with **no new guest/image** if the output
obeys every current restriction. It can preserve all existing proof cutpoints.
It does **not** solve stored semantic-DAG reuse, independent dependency fetching,
per-definition cache reuse, new inductives, cap exhaustion or general semantics.
It must not be sold as the full semantic scalability solution. Large expansion
still requires bytes and checking proportional to the demanded expanded graph.

### Route B: actual compositional definition DAGs

Let F be the adopted fixed foundation. A finite node D_i contains ordered
universe parameters U_i, type T_i, body v_i, allowed reduction hints and safety,
with an exact content-derived name. Let E_i be the non-F constants appearing in
both T_i and v_i, including projection type names. Require:

1. Every member of E_i resolves to an exact earlier definition node, never an
   imported proposition axiom; the dependency graph is acyclic.
2. Every non-F name is canonical and commits to its exact descriptor and
   dependency identities under a declared foundation/profile.
3. In topological order, the genuine checker establishes
   `F + D_<i |- v_i : T_i` with all existing universe, scope, freshness and
   safe-transparent requirements. No definition is accepted on hash validity
   alone. A reused local result is valid only under a precisely bound cache
   invariant; a transferred result requires independent warranted evidence.
4. A Prop interface's semantic context is the exact transitive closure of its
   direct non-F type references. A proof packet also contains the closure of
   proof references and of actually used selected Prop types. No unreachable
   data can manufacture a use, and repeated identities do not multiply demand.
5. Distinguish **direct root IDs committed by an interface** from **the materialized
   transitive closure** needed to type/check it. Committing root IDs can bind
   closure through recursive exact descriptors; it does not supply absent bodies.

Conservative extension theorem (metatheoretic, conditional on checker soundness):
if each D_i satisfies the genuine typing judgment above, topological induction
adds only conservative definitional extensions. Expanding finitely many new
constants maps derivations in F+D back to F. No new theorem axiom or author
identity is needed. Selected Prop assumptions are separate and retain actual
receipt or complete bounded-proof discharge obligations.

The theorem does not bound the computational expense of normalization. It also
does not admit definitions depending on proof axioms through dependent casts:
such dependencies require a separate explicit semantics/assurance design even
if the source proof happens to be in Prop. The proposed minimal extension keeps
them rejected.

### Content addressing and cost

A node's descriptor already includes exact constant names in type/body. If those
names are content-derived child IDs and the graph is acyclic, root identity binds
the entire semantic dependency graph under collision resistance. Canonical
identity need not depend on transport order or cache residency. Exact binder
and universe names remain part of current identity; semantic equivalence is
not decided. Structurally different but equivalent definitions can coexist.

For demanded distinct closure C, a simple uncached materialization requires
`O(|V(C)| + |E(C)| + bytes(C))` bookkeeping, plus actual checking/normalization
cost `K(C)`. Acquisition additionally incurs overlay routing and returned-byte
cost. With a valid immutable cache, only a missing subgraph M needs fetching;
checking reuse requires an independent cache-assurance argument, not merely a
filesystem path hit. These are demanded-semantic costs, not all-network costs
and not ancestral-lemma-proof costs. A result whose mathematical meaning itself
demands a huge explicit object cannot universally be made constant-sized by
hashing its root.

Use one flat node table with exact ID references and topological validation,
not recursively copied nested capsules that repeat shared subgraphs. Preserve
aggregate bytes/work/node bounds and return explicit incomplete/refusal states.
Local finite bounds need negotiated profiles or paging plans; silently increasing
a global constant neither proves scaling nor handles over-bound requests.

## Necessary implementation seams for Route B

| Source seam | Required change | Existing assurance reusable |
| --- | --- | --- |
| `guest/src/relation.rs` | Earlier-definition closure checks; direct/transitive dependency tracking; transitive actual-use computation; genuine topological type/body checks | Exact structural encoding, reserved F checks, safe Definition role, Prop check and proof receipt logic in unchanged cases |
| `guest/src/journal.rs` | Versioned interpretation of direct semantic roots for Prop/Def; unambiguous old/new schema handling | Framing discipline, count/rank/selection uniqueness principles |
| `companion/cert_capsule.py` | Flat closure projection, node-ID validation, cycle/conflict/missing/extra detection; exact output and parent binding | Graph encoder, bounded reads, F descriptor restoration where unchanged |
| `native/ImportTail.lean` | Decode flat closure; topological exact native insertion under semantic env; keep selected Props later; source capture/finalize context | Clean support reconstruction and genuine exact kernel addition |
| `companion/proof_compose.py` | Closure-aware projection and semantic union; preserve output capsule after substitution | Bounded proof substitution and declaration ordering machinery |
| `cert_bundle.py`, `cert_fragments.py`, workflow/stages | Versioned manifests, closure snapshots/pins, read bindings and receiver paths | Fail-closed resource/operation state machine, if precise unchanged contracts still hold |
| `guest/src/main.rs`, `host.rs`, policy adoption | New image plus deliberate receipt compatibility/migration decision | Old receipts under their exact old image; not silently under a new image |

Two migration choices are honest: keep old and new lanes distinct, reusing old
results only through a specified checked bridge; or adopt an explicit dual-image
verification relation that verifies old journals under their actual old image
and translates exact semantics into the new relation. Neither is a profile-file
rename. Both require source review and a focused changed-boundary qualification.
Avoid a new expensive cryptographic campaign solely to reproduce an already
available old receipt if an independently justified bridge is sufficient.

## Adversarial discriminators for whichever route is selected

Only run these after root selects exact source and bounded execution. They are
requirements for changed-boundary evidence, not authority to launch experiments.

- Positive two-node dependency and one genuinely reused downstream theorem.
- Diamond dependency retained once, exact same node reached by two paths.
- Direct and indirect cycle; absent child; conflicting same-ID data; altered
  body under old ID; duplicate or unused context; wrong topological order.
- Universe-polymorphic reuse at two distinct valid instances plus malformed
  arity/unbound-universe refusal. No trusted default instance filling.
- Definition type dependency, definition value dependency and projection name
  dependency, not just an easy monomorphic body-reference case.
- Definition trying to rely on an imported unproved Prop, opaque/unsafe/partial
  helper or a new inductive group must refuse in the proposed restricted lane.
- Budget/closure overflow must refuse without partial mathematical acceptance.
- Any image migration must reject wrong-image claims and verify genuine old
  receipts under the old image, not accept a syntactically matching journal.

## Priority recommendation to root

1. Require a concrete net-useful-capability application to guide the next source
   change and full-cost accounting. It is not enough to display a known theorem
   and infer network value from its asymptotic algorithm comparison.
2. Lower genuinely repeated per-operation work using exact immutable binding;
   this directly changes the break-even demand region for the capability.
3. Implement maintained decentralized discovery/custody under explicit honest
   contact and capacity assumptions. Known-contact bounded search is not yet
   the required large-network mechanism; cryptography cannot fix absent routes.
4. Choose Route A only if a real capability needs its authoring seam now; do not
   claim it removes the stored-DAG barrier. Choose Route B as a substantial
   semantic extension only with a deliberate profile migration and enough time
   for its broad changed boundary. Do not relax one checker guard and call the
   others incidental compatibility bugs.

These are joint feasibility constraints, not a recommendation to postpone all
mathematics until networking is perfect. Unchanged trustworthy checking evidence
should be reused. Political attribution, global ledgers, compulsory task lists,
and another exhaustive archive rehash are not on the central path.

## Evidence and limitations of this audit

Read current AGENTS/GOAL/NOW and the prior RELEASE-CENTRALITY, relevant frozen
growth decision and intrinsic-definition justification. Inspected the current
guest relation/journal/main, capsule code, native import/capture/finalize,
composer, bundle contract and host receipt/image seams. No product module was
imported, no source copied, no process campaign launched and no frozen source
edited. This is an independently reasoned source audit; proposed algorithms
and metatheorems are not machine-proved or implemented merely by this note.
