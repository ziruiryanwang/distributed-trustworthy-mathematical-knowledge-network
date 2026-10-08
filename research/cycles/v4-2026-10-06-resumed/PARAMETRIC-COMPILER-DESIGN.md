# Parametric extraction: defer implementation, preserve the precise contract

2026-10-06. Mechanism source/theory investigation. Canonical root only; no coding,
imports, checker or experiment. Independent metatheory is in PARAMETRIC-MODULES.md.

## Decision

Do not select another compiler merely to claim semantic growth. Existing
definition plans already admit explicit Pi/lambda/let/application terms; the
compiler preserves hash-consed DAGs, and explicit application can use parametric
modules. Automatic lambda lifting would remove a tedious and error-prone authoring
step, but it adds no logical expressivity and is not the present central blocker.
Direct circulation of newly constructed definitions is a more consequential
missing boundary. Root prioritizes that investigation plus GROWTH-UNIFORMITY.md.

There is a real restricted byte-saving region, described below; it does not make
all concrete definitions or computation disappear. No new inductive, named
dependent-definition DAG, universe-polymorphic term value or opaque data axiom
is introduced by lambda lifting.

## Minimal useful extraction contract if later selected

Input: one current definition-composition plan and at most four exact canonical
F-closed definition capsules D_i with closed types T_i. Enumerate each distinct
actually occurring specialization `(D_i, universe_arguments)` in the plan's type
and value. A term parameter stands for one specialized instance, not for a Lean
constant polymorphic over arbitrarily many universe instantiations. Impose a
separate explicit specialization/parameter cap; four input capsules do not imply
four specialized occurrences. Canonical order and fresh binder names are fixed.

For k selected specialized occurrences, introduce outer parameters
`p_0:T_0[sigma_0], ..., p_(k-1):T_(k-1)[sigma_(k-1)]`. In this restricted source
profile each T_i is F-closed and term-closed, so these parameter types do not
depend on earlier added term parameters. Their internal dependent Pi binders
remain ordinary syntax. Universe substitution must be simultaneous and capture
avoiding, with every actual level expressed in the output's declared universe
parameters.

At original binder depth d replace selected constant occurrence i by
`bvar(d + k - 1 - i)`. Preserve original locally bound indices less than d.
Recurse under lambda/Pi bodies at d+1; binder types remain at d; for let, its type
and value remain at d and its body uses d+1. Memoization must include d whenever
the output depends on depth, even when the original graph node is shared. Names
in projection declaration slots cannot be replaced by expression variables.
Reject unsupported projection substitution, free variables, wrong universes,
unselected names and every exceeded node/state/depth/byte bound.

Output type is the added Pi telescope around the transformed original type;
output value is the matching lambda telescope around the transformed value.
Use the unchanged canonical definition codec and a new identity. Include the
input pins, precise specialization-to-parameter correspondence, output pin and
structural cost record, with UNVERIFIED assurance. No source value is embedded
merely to stand for a parameter. The final adopted relation must genuinely check
the new closed output.

**Typing caveat:** checking the original transparent definition is insufficient
to justify its abstraction. `D : Type := Nat` and `0 : D` are valid, but replacing
D by arbitrary `A : Type` does not give `0 : A`. The preservation theorem needs
typing using opaque parameters of the specified types, or direct successful
checking of the generated abstraction. Concrete delta-reduction cannot be used
as a generalized law. The compiler is untrusted and may therefore produce a
candidate that is refused; it must not claim all valid inputs generalize.

## A supported mathematical use beyond the previous iteration example

Take types A,B,C, operations mu_A,mu_B,mu_C, and functions f:A->B and g:B->C.
Assume explicit homomorphism laws hf and hg. Composition satisfies

`g(f(mu_A(x,y))) = mu_C(g(f(x)), g(f(y)))`.

Its proof is `Eq.trans (congrArg g (hf x y)) (hg (f x) (f y))`. Pi/lambda,
application, Eq.trans and congrArg occur in the adopted foundation witness.
Types, operations, functions and laws can all be parameters; no new record or
inductive type is needed. This permits a reusable generic algebraic transport
module/law independent of the sizes of concrete implementations. It is not an
actual newly executed case or an automatic discovery claim. Existing explicit
plans can already express it, which is why a new extractor is not a capability
milestone by itself.

## Byte-cost region and non-claims

Let S_flat(j) be the exact existing codec length of the expanded jth capsule;
let S_param(j) be the exact length after abstraction. Count distinct reachable
serialized DAG rows, not textual expansion trees: existing compilation already
interns equal nodes. If a dependency value has U private reachable rows not
needed by its type or the parameterized construction, the generic capsule omits
those rows. It adds parameter types, binder/name/variable rows and correspondence
metadata. Canonical renumbering changes index digit widths, so actual byte savings
are the exact serialized difference, not automatically U times a guessed row size.

Over a declared set of uses, a sufficient byte-event advantage is

`sum_j S_flat(j) > sum_j S_param(j) + all differential type acquisition,
metadata, installation, instantiation, transport and custody byte-events`.

This region can be nonempty when value bodies are large and interfaces small,
and generic modules are reused without immediately specializing/flattening them.
At a concrete computation, the old checker still needs and checks the demanded
body; passing that body as an argument is not permission to omit it. Universal
statements avoid implementation bodies precisely because they quantify over
the implementations instead. No universal runtime or storage advantage follows.

Current limits remain four local-definition file arguments, four local fragments,
eight combined selected contexts, four definitions required by an output type,
and all existing graph/packet/checker bounds. Packaging many operations in a
lambda/Church tuple does not waive byte/type-checking costs or create new kernel
declaration support. A source-DAG wrapper around the existing compiler would
not establish an advance over its existing hash-consing.
