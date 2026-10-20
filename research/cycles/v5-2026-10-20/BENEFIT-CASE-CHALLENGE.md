# Independent challenge: no speculative SAT benchmark implementation

2026-10-20, core_search. Source/theory only; no execution, proof, install or Git.
Reviews BENEFIT-WORKLOAD-DECISION `53f82a45` and BENEFIT-CASE `6cb956b1`.
**NO-GO to implement or run the unspecified CaDiCaL/Church reuse workload.**
This rejects this construction now, not proof sharing or the unchanged v5 goal.
The tiny constructive resolution rule is valid; it does not settle the gates below.

## Exact semantic boundary, before search cost

The bundled Lean `LRAT/Internal/Formula/Class.lean` explicitly distinguishes
`rupAdd_sound : ... Liff ...` from `ratAdd_sound : ... Equisat ...`.
RAT can preserve satisfiability without making each added clause a consequence.
Thus arbitrary LRAT additions cannot be exported as implication step lemmas.
The bundled `Lean/Meta/Tactic/BVDecide/External.lean` requests `--lrat` and
`--shrink=0`; this is not evidence that its trace is plain constructive resolution.
An untrusted solver is fine, but every accepted step must reconstruct to the
exact ordinary Lean theorem. Reject unsupported traces; do not silently assume
a new LRAT-checker support closure, classical axiom or trusted UNSAT oracle.
Boolean semantic entailment alone is not a proof for arbitrary propositions:
`P or not P` is valid on Boolean assignments but not constructively derivable.
An explicit resolution/weakening DAG can avoid that gap; replay must establish it.

Current `modules/codec.py` caps depth at 192, nodes at 250000, declarations at
16384 and bytes at 16 MiB. A naive exported type with n proposition binders
followed by m clause-premise arrows has depth at least n+m. Typical CNF sizes
can violate this before proof checking. Balanced premise bundling is possible,
but its introduction/elimination and repeated type costs must be counted.
`source_rows.py` expands expression-DAG subtrees and counts that expansion.
Named step constants share proofs, not automatically every repeated type/context.
No exact family with a supported, bounded type and reconstructed proof is supplied.

## Unknown-ID discovery must not be supplied by the test

The actual `conjunction_index/discovery/module_export_adapter.py` hashes the
relocated declared type. A new local `OrC` or `FalseC` name incorporates its
unknown producing ModuleID; a fresh consumer cannot derive that exact query.
Either inline these encodings in the exported type, or put them in an initially
shared encoding module given equally to both routes and charge its establishment.
Derive the generic query from the consumer's existing formal problem; do not
feed it the answer's ID, post hoc profile or an undisclosed generic core.
Then charge target construction/hashing, candidate inspection, acquired types,
needed semantics, substitutions and genuine premise proofs. Generic arrow-shape
features, even paired, offer no selectivity theorem over a huge mathematical corpus.
Exact-type discovery is useful but is not general matching modulo equivalence.

## Strong comparator and full-cost consequence

Use the existing optimized solver/tool portfolio, not a newly written weak solver.
Pigeonhole/parity/structured CNFs need their direct counting, algebraic or structural
proof alternatives considered; solver preprocessing may also erase apparent work.
These are challenges, not claims that every such instance is easy. No lower bound
against all possible algorithms is required, only an explicit honest comparator.
Each isolated library may generalize and cache once. Count independent first uses,
not repeated substitutions in one warm library. Both routes have the same initial
mathematics, optimizer, index, representation and proof reconstruction facilities.
With identical proof endpoints common checking can cancel; if a shorter alternative
wins, compare its actual check/reconstruction costs instead. Charge producer work,
failed searches, query/type traffic, publication, finite retention, repair and service.
No observed or bounded search margin currently survives these obligations.
An inequality with an unspecified positive margin is not a witnessed benefit region.
Native sharing benefit and optional succinct-certification premium remain separate;
this candidate justifies neither a new receipt nor renewed evaluator-M certification.

## Smallest useful next decision

Do not build a solver port, universal applicability engine or benchmark generator.
Existing author/admit/publish and exact-type discovery already provide the basic path;
the present gap is a justified workload, not evidence that those APIs need replacing.
A future GO needs one independently specified target, its supported proof/type bounds,
an independently derivable query, and a credible margin over its best supported local
route. Prefer an existing real Lean contribution and its direct alternatives; stop
source construction if they erase the margin. A small fixed check is warranted only
after that screen. Root should redirect current implementation effort to an actual
remaining reuse/interoperability or release obstacle instead of manufacturing a gap.
The proposed numeral feasibility is suitably narrow, but frontend `2` can elaborate
through `OfNat.ofNat`; inspect its exact Nat/add/instance closure, not only `natVal`.
Built-in numeral/constructor definitional equality does not by itself justify an
arbitrarily relocated Nat. Resolve that correspondence before selecting a lowering.
