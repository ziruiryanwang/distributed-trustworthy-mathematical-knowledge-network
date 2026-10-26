# Checked-context union: principle and implementation boundary

2026-10-26. Theory-only challenge; no implementation, import, state open or test.
This complements the separate current-public-path/cost trace, not a second trace.

## Result worth pursuing

Two independently developed ideas already warranted by this local checker can,
under the premises below, be combined without checking their old theorem proofs
again. Only the new mathematical development needs new proof checking. This is
a compositionality argument, not remote certificate authority or a growth-rate claim.

## Sufficient premises

Fix a foundation F, kernel/checking interpretation K and allowed-axiom policy P.
A context is a finite set of immutable declaration **groups**, with a dependency
order. A mutually inductive group includes its complete types, constructors,
recursors and required generated declarations; internal group dependencies are
not mistaken for forbidden inter-group cycles. Write WF(K,F,P,G) for validity
obtained by the selected kernel's permitted extension rules starting from F.

Assume:

1. Both WF(K,F,P,A) and WF(K,F,P,B) were actually established locally, including
   required complete groups, positivity/termination conditions and mathematical
   support. A marker asserted by a peer, parsing success or a signature is not this.
2. F, K, P and their interpretation/implementation identities are the same and
   currently admissible. Every non-foundational declaration has an established
   justification; neither branch introduces an unchecked axiom, sorry or unsafe
   acceptance path. Fixed permitted foundational axioms remain explicit premises.
3. Overlap is exact at the kernel-declaration/group level: identities, declaration
   kinds, types, values where applicable, ordered universe parameters, universe
   levels, transparency and inductive/recursor metadata agree. No name rebinding,
   hash-only semantic substitution or silent alpha-renaming is performed. Exact
   equality is a conservative sufficient condition, not the weakest possible one.
4. Every reference resolves to F or an included group; the union's group dependency
   graph is acyclic and admits a topological order. Generated/private auxiliaries
   and dependencies of types and transparent bodies are included, not only proofs'
   visible exported theorem names. Each group is included once, not partly merged.
5. Kernel judgments restrict to their closed dependency context and admit weakening:
   compatible additions do not change existing meanings or conversion rules.
   This is a required property of the actual checking interpretation, not
   something deduced from a compiler exit code. Elaborator search may change;
   its newly produced proof must still pass K.
6. The exact locally warranted snapshots, declaration maps, import closure and
   artifacts remain authenticated, immutable and protected from unauthorized local
   modification. Their cached warrants bind the exact bytes and active policy,
   not merely paths or successful historical operations on another context.

Let U = A union B, coalescing only the exact overlaps of premise 3. Then
**WF(K,F,P,U)** follows under those premises. For any newly checked U |- t : T,
the result is warranted under the same F/K/P; no new foundational authority arises.

Argument: topologically enumerate union groups. Each group's needed checked
predecessors are already present with unchanged interpretation. Premise 5 preserves
its original extension judgment in the larger preceding context. Induction yields
the union's validity. Reuse the previously established judgment, not a fabricated
proof. This is a conditional metatheoretic argument, not a completed Lean
formalization/refinement proof for the current loader. Proof irrelevance may permit
weaker overlap tests, but that relaxation is neither needed nor justified here.

## Why the premises matter

| Weakened premise | Failure |
|---|---|
| Match names only | A proves `c = 0` with `c := 0`; B has `c := 1`. Overwriting one interpretation can turn the cached theorem into a false statement. |
| Admit arbitrary fresh axioms | Separately well-formed contexts can assert a proposition and its negation. Their union passes syntactic axiom admission but loses the intended warranted-theorem guarantee. |
| Ignore universe order or inductive metadata | A copied type can refer to different levels or acquire invalid elimination/computation rules; matching displayed type text is insufficient. |
| Check exported signatures only | A missing auxiliary, changed transparent definition or incomplete recursive group can invalidate conversion and downstream uses. |
| Trust cached path/foreign `.olean` | Substitution or unchecked declarations bypass the original local checking event. Same filename or signer does not establish derivability. |
| Ignore policy revocation | A checker later found defective remains silently authoritative even though its cached warrant is no longer admissible. |

## Can protected `.olean` import realize this?

In principle, yes **as reuse of a locally warranted cache**, not admission of an
untrusted foreign binary. A trustworthy local producer must establish correspondence
between each protected artifact and its exact checked declarations/imports; a trusted
loader must preserve that correspondence. Imported native initialization, plugins or
environment extensions cannot silently expand this trusted boundary. Preserve the
current snapshot restoration's exclusion of plugins/extensions and validate the
complete artifact/module-name resolution, not just selected export names.

Ordinary module imports can share a common module already present in the import DAG.
That does not automatically coalesce equal declarations copied into differently named
chunk modules. The separate source trace reports both disjoint siblings and a sibling
pair with repeated nonbasis declarations. It also reports a current single-chain
restriction. These are representation/loader obligations, not a refutation of union.
Simply passing two `.olean` paths is therefore not a justified implementation.
Foreign inert mathematics still needs existing local acceptance before cache reuse;
copying a remote artifact or local READY seal does not meet premise 1.

An eventual implementation also needs an exact committed derived-context identity,
bounded overlap/closure validation and crash-safe authority. Failure must not create
an accepted partial union; stale/revoked authority must refuse. These are obligations,
not a newly selected manifest, registry, storage format or migration mechanism.

## Cost and selection boundary

Let N/E describe selected union declarations/dependency edges, and S the newly
accessed artifact/semantic bytes. With linear canonical-map/graph processing, merge
cost is O(N+E+S) plus new-proof checking, not old-proof checking. General conflict
or missing-edge detection needs inspecting the relevant uncached descriptions;
content addressing does not make that worst-case work constant. Authenticated
previously checked subgraphs can reduce repeated work only with a justified cache.
Ordinary `.olean` loading may still read/hash large modules, retain proof-bearing
data and load transitive semantics. Avoiding proof replay alone does **not** prove
small cold download, memory use or ancestry-independent total receiver time.

Compare the complete public routes: union validation/artifact construction/loading
and maintenance versus the existing selected re-admission and module-realization
cost, with identical final mathematics and trust. Select a union optimization only
if actual independent-idea composition is blocked or this total saving is material.
Disjoint siblings over one shared protected basis are the simplest candidate;
overlapping chunk coalescence is a separate cost, not an automatic prerequisite.
Use current selected re-admission when cheaper or infrequent. No old proof campaign
or new union implementation is authorized by this argument; root selects next work.
