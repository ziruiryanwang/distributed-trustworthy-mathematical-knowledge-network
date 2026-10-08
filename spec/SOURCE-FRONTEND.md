# Source elaboration and mathematical acceptance

Development contract, 2026-09-23. The source frontend repair is under test.
This contract explains the boundary used by `software/native/AgentClient.lean`
and the five-step submission pipeline in `software/py/checking.py`.

## Two environments

Let K be the environment reconstructed from the node's selected foundation and
checked context packages. Every added kernel declaration is checked locally.
K contains mathematical declarations but need not contain Lean's imported
parser, notation, macro, tactic, or elaborator extension state.

Let F be the authoring environment obtained from the selected runtime's `Init`
module with its frontend extensions enabled, as for an ordinary Lean file. The
loaded Lean runtime supplies built-in elaborators and tactics. For every name already in K, the
declaration in F must agree with K under the existing canonical inventory
representation, including its name, universe arity, type, body where present,
declaration kind, and structural metadata. Both declarations are screened for
safety. Universe parameters are compared by ordinal position; binder names and
expression metadata are omitted. Ordinary definition/theorem/opaque `all`
metadata is lowered to the singleton declaration as in the existing foundation
codec, and definition height hints are omitted because the receiver recomputes
them. These are the canonical profile's existing normalizations; type-only or
name-only equality is insufficient. Missing K declarations are installed into F in
dependency order and the agreement check is repeated. A mismatch refuses the
source operation. The frontend and kernel checker use the same pinned Lean
runtime; executable runtime/library files are trusted operator dependencies.

Agent source is elaborated in F. It may use ordinary installed syntax and
tactics, and the exact receiving names of checked contributions. Peer packages
do not install executable code, macros, tactic implementations, or attributes.
The source remains executable input authorized by the local operator.

## Acceptance obligation

For a source-selected root r, form its complete reachable declaration closure
C relative to K, including dependencies in types, proof/definition bodies,
inductive declarations and generated recursor rules. An ordinary imported
library theorem outside K must be included in C with its proof. Its presence
in F grants no mathematical authority. The capture rejects new axioms and
quotient primitives outside K, unsafe/partial declarations, unsupported forms,
cycles, unbound references and over-budget closures.

The product accepts only after all of the following succeed:

1. Source processing preserves every pre-existing declaration in F and produces
   a supported root and a bounded complete capture C.
2. Canonical compilation binds every reference to the selected foundation,
   inherited checked objects, or a declaration in C.
3. A fresh data-only environment reconstructs and kernel-checks the canonical
   candidate using the selected foundation, without importing F.
4. Inverse export and a second fresh data-only replay agree with the candidate
   and the requested root under the existing canonical equality checks.

Consequently a faulty tactic cannot make a false proof acceptable solely by
reporting success in F. Acceptance requires an actual kernel-checked proof
under the selected foundation and assumptions. This argument depends on the
correctness of the kernel, codecs, binding checks and trusted local execution;
it does not assert consistency of arbitrary user-selected axioms.

Human intention, attribution, popularity and producer identity do not enter
this mathematical acceptance rule. A statement may be accepted as a definition
without being a theorem proving that statement. Relevance and usefulness remain
separate empirical questions.

## Supported scope and evidence needed

Normal source syntax is broader than the finite canonical capture profile.
For example, an imported lemma may require too many dependencies or an
unsupported nested inductive group. Such source can elaborate and still be
refused by the contribution path. Checked peer declarations also arrive without
their original source-level attributes; agents can apply their exact names.

The regression must show multiline `by`/`let`/`exact` passing ordinary submit,
publication, and fresh admission; a further proof must use the received theorem
and survive the same path. Negative controls must refuse `sorry` and proofs
depending on a newly introduced axiom. Capturing a legitimate ambient theorem
must include its dependencies and survive data-only replay. Record elapsed and
CPU costs because importing the frontend adds a fixed authoring cost.

The [causal investigation](../research/cycles/2026-09-23-reconstructed-frontend-hypothesis.md)
and [current desk](../research/NOW.md) track the actual evidence separately
from these implementation obligations.
