# Restricted composition: constructive refinement to the original conditional I predicate

Source/theory checkpoint. No checker implementation, execution, build or proof.
This narrows the previous RC decision where its operational refinement was open.

## Answer

There is a constructive refinement route for a **normal application-spine
profile, RC0**, containing the actual base-I `binary_congr` composition target.
It needs no new mathematical policy or new semantic member-journal shape.
A genuinely new adopted aggregate image is still necessary. It is not an I
receipt and cannot reuse old homogeneous-A authority.

The larger proposed beta/zeta-plus-interface-only RC language does **not yet**
have this argument. In particular, Nanoda's conversion evaluation order can demand
a transparent body even where a different sound beta-conversion algorithm would
not. Therefore do not infer old-predicate acceptance from Lean validity, or claim
the broad fragment already refines I. Start with RC0 or discharge those additional
operational obligations; changing the journal label alone would not prove safety.

RC0 is not proposed as evidence that FIRST becomes cheaper. FIRST remains
uncertified and outside this fragment. Whether RC0 saves enough compared with the
existing general checker on **this identical composition target** is still a
prospective cost decision. The following resolves a logical compatibility issue,
not that economic comparison.

## Which predicate is authoritative

The retained base receipt uses image
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
Its assembly04 selection identifies `guest-build-05/RESULT.json`, whose source
selection is `experiments/v5-local-checks/guest-build-05/selection.json`.

For this investigation, file-only SHA checks confirmed the current files below
are byte-identical to that original guest selection: native `tc.rs`, `env.rs`,
`expr.rs`, `level.rs`, `parser.rs`, `module.rs`, `module_correspondence.rs`,
`util.rs`; receipt `relation.rs`, `canonical.rs`, `input.rs`, `journal.rs`,
`policy.rs`. Thus the reasoning is not about an imagined reference kernel or a
later changed implementation. Representative original pins:

| Original source | SHA-256 |
|---|---|
| `modules/native/checker/src/tc.rs` | `f1b5f2e15f231aea52ae3452435c2b91a69a6baf8c010f68214b3e0cf57fa52b` |
| `modules/native/checker/src/module_correspondence.rs` | `f37c855666480553ee9b95f59dc3ba7ad19316e8e707aacd47fecfa29f1d12e2` |
| `modules/native/checker/src/module.rs` | `6c9b6acbf0cae9698b9fa035bad38df8c1e307dd1e78d6971b27f58511c58455` |
| `modules/receipt/src/relation.rs` | `3625bc9c7708e5a03580e1e61bc7019f5b7cf6ad48ee37f6d749919d245e2eb8` |

Define `R_I(W)=(J, Parents)` to mean successful return of the original
`modules/receipt/src/relation.rs::check_bytes` on canonical witness W, before
guest `env::verify` discharges the returned parents. This includes parsing,
bounds, commitments, correspondence and `check_module_extension_conditional`;
it is not merely the kernel typing judgment. Parent discharge is a separate
aggregate graph/cryptographic obligation.

The precise desired implication is:

```text
RC0_accept(C) = (J, Parents)
    implies
R_I(encode_original_witness(C)) = (J, Parents).
```

This is an algorithm-to-algorithm inclusion on a specified subset. The witness
constructor is described below. Its correctness must be implemented and reviewed;
no runtime success or machine-checked refinement theorem is claimed here.

### Current typed-row successor is not a new logical premise

`typed_rows/checker_lib.rs` points to the exact same `tc`, `env`, `expr`, `level`,
`module` and `util`. Its different parser/correspondence represent rows directly.
`typed_rows/module_relation.rs::check_typed` retains the same schema, parent image,
F/P, group/body commitment, rank and local-checking requirements. Its legacy path
is separately compiled from `bounded_parse/module_relation.rs`; fallback happens
before semantic checking, never after a kernel or commitment failure.

Typed correspondence memoization charges repeated *logical visits*, not merely
distinct DAG nodes. It does not authorize a larger original proof-tree witness
or waive the old syntax/depth predicate. This investigation constructs W for
the original relation directly, so a claim of typed-row equivalence is not used
as a substitute for original-predicate refinement. The new typed guest image is
not a fresh I authority merely because its mathematical rules are unchanged.

## RC0: the additional operational restrictions

Keep the previous exact typing/scoping/universe rules, but initially require:

1. Only new ordinary singleton theorems. Imports outside F are ordinary sealed
   theorem interfaces whose finite selected type-reference closure is explicit.
   For the initial endpoint that closure is just the base `binary_congr` theorem
   and foundation equality. No imported transparent definition, opaque value,
   nonfoundation inductive block, recursor, projection or rule body is used.
2. New proofs/types use `sort`, `bvar`, `const`, `app`, `lam`, `forall`. No `let`,
   computational redex, recursor application or requested beta/zeta conversion
   is needed in RC0. A producer can construct normal terms directly. This does
   not authorize silently normalizing an already chosen exported descriptor.
3. After ordinary simultaneous universe substitution and telescope instantiation,
   every application function type is already a syntactic Pi; every inferred
   sort is already a syntactic Sort. No `ensure_pi`/`ensure_sort` needs delta.
4. Every argument-type comparison and the final inferred-versus-declared theorem
   type comparison is **exact structural equality**, retaining binder styles.
   Harmless binder-name differences in the native foundation are handled only
   by the original binder-comparison path described below. Do not use general
   normalization equality as an excuse to enter a new native evaluation path.
5. Universe instantiations match exact arity and are scoped. The first target
   uses only zero/positional parameters in the input; successor/imax arise in
   sort inference. Prop recognition uses the existing zero/imax rule. No
   arbitrary universe-equivalence decision is required by its type comparisons.
6. The **virtual original witness**, not only RC input, fits every original
   parser, traversal, scope, index and byte bound. Witness-resource checking is
   part of RC0 acceptance even if no old native rows are materialized in-guest.

These conditions are stronger than mathematical necessity but inspectable by a
small syntax-directed checker. They prevent accidentally relying on the general
kernel's transparent reduction or proof-irrelevance heuristics. They include a
nonempty, recursively composable family, not only one hard-coded theorem name.
The same strict application rule can use an earlier RC0-certified member as an
ordinary sealed theorem after genuine aggregate authentication.

## Constructing the exact original witness

Let C contain its fixed image I, F/P, local spec, ordered proof terms, exact
parent J values and authenticated openings. Let M be the ordinary module-spec
hash. The following is a constructive algorithm for W; the already-existing
`modules/native_rows.py` and `modules/receipt/witness.py` exhibit this encoding,
but their success is untrusted and not the refinement proof.

### Start with the exact foundation and interned tables

Copy the adopted 413-row foundation prefix, including its existing metadata,
declarations and DAG indices. Seed all name/level/expression tables from that
prefix; append only after it. Deduplicate by complete structural value, not by
an unchecked hash equality. Name indices start at one with anonymous name zero;
level index zero denotes level zero; expression indices start at zero.

For each declaration with k universes, use distinct native parameter names
`DMKN.Universe.0` through `DMKN.Universe.(k-1)` and emit their parameter-level
rows before the declaration. The original parser's `get_uparams_ptr` requires
those levels already to exist. The correspondence checker maps their ordered
positions back to `param 0` through `param (k-1)`. Original foundation parameter
names remain unchanged; `subst_expr_levels` performs the required alpha change
when a foundation constant is instantiated.

### Recursively emit canonical expressions

Emit child rows before their parent and reuse an identical earlier row. This
gives each native expression/level reference a strictly smaller index. Map:

| Canonical form | Exact native form |
|---|---|
| `bvar i` | `bvar: i` (within u16 and scope bounds) |
| `sort u` | `sort: level(u)` |
| `const r us` | `const: {name: name(r), us: map(level,us)}` |
| `app f a` | `app: {fn: expr(f), arg: expr(a)}` |
| `lam bi A b` | `lam: {name:0, type:expr(A), body:expr(b), binderInfo:bi}` |
| `forall bi A B` | `forallE` with the same four fields |

`local r` resolves to `DMKN.Mod.M.r` for the local descriptor/proof. For an
imported descriptor, resolve its local references to **that imported owner**, not
M. An external reference resolves to its stated owner. A foundation reference
resolves to its exact existing foundation name. The initial target uses no
nonfoundation constants in its statement other than its imported theorem in the
proof; no unsupported signature has to be guessed.

For universes, map zero to index zero, param i to its declaration's ordered
parameter name, and successor/max/imax to the corresponding child-first level
rows without silently simplifying the descriptor's universe syntax.

### Emit imports before local declarations

Follow the old relation's sorted `(owner-module, group-index)` order for imports,
then local-spec group order. Each imported theorem becomes exactly:

```text
moduleImportTheorem {
  name: qualified-name-index,
  levelParams: ordered-native-universe-name-indices,
  type: exact-type-expression-index
}
```

It has no proof value, body hash, fake axiom or additional field. The parser
creates `Declar::Theorem { val: SealedProof, ... }`. Each new theorem becomes:

```text
thm {
  name, levelParams, type,
  value: supplied-checked-proof-expression-index,
  all: [name]
}
```

`all` is required by exact correspondence even though the ordinary parser record
does not use it. Descriptor `kind` remains `theorem`, `value_hash` null and `meta`
empty. No supplied proof is placed in `bodies`: theorem proof witnesses are
deliberately not committed as transparent bodies in this policy.

Set original W fields to exactly `schema,image,rank,local_spec,rows,parents,bodies`.
Use the original `DMKN_CERTIFIED_MODULES_V2` schema, fixed image I, original
parent/opening bytes, and `bodies=[]` for RC0. Rank is zero without parents or
`1+max(parent.rank)` with parents. In the actual base endpoint it is one.

Parent journals remain in the exact order C records; the returned `Parents`
vector therefore agrees, while imported rows use the original sorted order.
Enforce no self-module parent and no duplicate parent or group. The local spec
is unchanged by this construction, so its M/group root and resulting J bytes
are exactly unchanged.

## Why the original correspondence and module wrapper accept W

The proof is by the construction above, not an appeal to Lean soundness:

- Foundation equality holds by copying its exact prefix. All prefix names retain
  their indices and complete atomic foundation inductive blocks remain intact.
- Every appended DAG reference is a backreference by child-first emission.
  Relative names and universe positions reconstruct to their original canonical
  values under `Inventory::reference`, `level` and `expression`.
- `match_declaration` therefore reconstructs the exact type in each descriptor.
  It accepts imported theorem headers only as `moduleImportTheorem` and new
  proofs only as ordinary `thm` with a present proof and singleton `all`.
  It traverses every new proof even though the proof is not part of M.
- The declaration census is exactly one row per ordered singleton group, with
  qualified distinct names. There are no body obligations and no unused bodies.
- The original parser inserts imported theorems as SealedProof and locals as
  Present, with complete typed DAG structures and no skipped axiom. The exact
  foundation already satisfies its metadata and inductive constructor census.
- The original relation derives Foundation and Module premises from these exact
  matches. `module.rs` finds all imports before locals, skips only those matched
  imports and rejects no partial nonfoundation inductive block because none is
  present. Every local is in namespace M and has a Present value.
- Each local invokes the exact original `check_declar`; acceptance of this last
  step is established next, rather than assumed from the correspondence report.

## Why the exact native checking execution accepts RC0

The decisive code paths are `tc.rs::{check_declar_info,infer_const,infer_app,
infer_lambda,infer_pi,def_eq_quick_check}`, `expr.rs::{inst,abstr_levels,
subst_expr_levels}`, and `util.rs::alloc_expr`.

Use this invariant while opening a telescope: the native locals have the same
ordered types as the RC0 context; all de Bruijn variables currently exposed to
native `infer` have already been replaced by those locals; the residual
unopened binder bodies remain well scoped. Native `infer` intentionally panics
on a loose bvar, so merely validating the outer descriptor would not suffice.

`infer_lambda` and `infer_pi` open each binder using `ctx.inst`, with parameters
in outer-to-inner order. `inst_aux` selects substitutions in reverse order for
de Bruijn index lookup and increments the offset under binders. Arguments in
these calls have no loose bvars (they may contain the opened native locals), so
its non-lifting substitution is appropriate. Closing uses `abstr_levels`, the
inverse replacement of those fresh local levels. An RC0 implementation can use
the same open/close representation to make this simulation direct; it must not
confuse native substitution with arbitrary textual substitution under binders.

Induct on RC0 expression inference:

1. A local infers its recorded type. Sort infers `Sort(succ u)` and explicitly
   checks every universe parameter against the declaration's ordered parameters.
2. A constant resolves within `EnvLimit::ByName(current-local)`, so all imports
   and only earlier locals are visible. Exact universe arity makes
   `subst_expr_levels`' length assertion pass; substitution is simultaneous and
   traverses the same constructors as the RC0 substitution.
3. For an application, native `infer_app` unfolds the application spine and
   consumes its syntactic Pi telescope. RC0's restriction ensures no computational
   `ensure_pi` step is needed. Native checks every argument's inferred type
   against the instantiated binder type. By the RC0 strict-equality premise and
   the induction hypothesis, both are the same structurally interned expression.
4. `alloc_expr` first probes the immutable export DAG, then the temporary DAG,
   and expression equality includes full constructor fields. Consequently the
   same structure under the same opened locals has the same pointer.
   `def_eq_quick_check` returns true immediately on pointer equality. This occurs
   before proof irrelevance, delta, recursor reduction or a missing-body demand.
   Where a foundation's binder *name* differs, `def_eq_binder_multi` opens both
   Pi telescopes using the same locals, compares their domains recursively and
   reaches identical bodies; binder names do not become semantic constants.
5. Lambda inference closes the inferred body type into the same Pi telescope.
   Pi inference computes `imax(domain-level,codomain-level)` from right to left.
   In the initial endpoint the innermost equality has sort zero; original
   `level.rs::is_zero`/`simplify` recognize each `imax(_,0)` as zero.

Thus `check_declar_info` sees unique universe binders, a closed actual type and
Prop. `check_declar` infers the supplied proof in Check mode and its final type
equals the declared one by the same quick path. Earlier local theorem values
are not unfolded: no equality comparison enters delta in this profile.

This is a source-level operational simulation argument for the specified subset.
It does not assert completeness of Nanoda for all Lean-valid terms or a theorem
about its arbitrary conversion strategy. Independent review must check the
implementation preserves the strict-equality/normal-spine premises rather than
quietly accepting the larger language described in the previous decision.

## Fully explicit initial target and proof

Let `bc` be the exact base-I qualified `CommonsV5.binary_congr`. Its three
universe parameters range over Sort, not just Type. The local telescope is:

```text
{A : Sort u} {B : Sort v} {C : Sort w} {D : Sort z}
(f : B -> C -> D) (g : A -> A -> B) (h : A -> A -> C)
{a a' b b' c c' : A}
(ha : a = a') (hb : b = b') (hc : c = c')
```

The exact body proposition is:

```text
Eq.{z} D (f (g a b) (h b c)) (f (g a' b') (h b' c'))
```

Define these ordinary explicit proof expressions (notation here abbreviates
canonical repeated application; all arguments must actually be supplied):

```text
pg = bc.{u,u,v} A A B g a a' b b' ha hb
ph = bc.{u,u,w} A A C h b b' c c' hb hc
p  = bc.{v,w,z} B C D f
       (g a b) (g a' b') (h b c) (h b' c') pg ph
```

Close p with the same 16 lambda binders as the declared Pi telescope. Each
function type is already Pi; each proof argument type is literally the equality
expected after telescope instantiation; the final inferred equality is the exact
body above. No transparent definition or induction is hidden in this expression.
There are four universe binders in the local theorem, despite the three in bc.

Counting expression constructors before interning gives 51 for bc's type, 93
for this target type and 139 for its proof (including binder-domain expressions).
Universe/name traversals and fixed foundation rows are additional; these counts
are derived syntax counts, not an executed profiler or proof-cost estimate.
They show the construction is far from the original expression-visit ceiling.
The initial proof uses three applications of the same genuinely sealed theorem,
but no ancestor theorem proof is present in W.

A subsequent module can apply this new 16-argument theorem and combine its
result with another exact equality using foundation `Eq.trans`, under the same
strict comparison rule. Its parent is an authenticated A-RC member, not an
invented I receipt. The local refinement is conditional; strict aggregate graph
induction discharges that premise. Thus preserving old-shaped J does not require
an independently produced I receipt for every intermediate member.

## Virtual bounds are part of the refinement

The original relation checks more than semantic derivability. Enforce, for W:

- 16 MiB canonical input, at most one million JSON value nodes and the canonical
  depth limit. `check_bytes` also retains serde_json's default parser recursion
  limit; satisfying a separate nominal 192/256-depth limit alone is insufficient.
- 413..250,000 native rows; at most 4,096 parents/imported groups/combined groups;
  at most 16,384 declarations; at most 256 universe binders per declaration.
- Correspondence's cumulative 250,000 expanded logical expression/level visits
  and depth192, including repeat occurrences in the new proof and imported types.
- Exact name/string bounds, parser indices, u16 de Bruijn indices and local-level
  counters, and original integer/record schemas.

The emitter can calculate conservative virtual bounds or exact streaming counts
without constructing the old general kernel environment. Reject when the bounds
cannot be established. Do not make the fast checker accept a proof DAG whose
expanded witness exceeds I's admitted language, then call it an I refinement.

For the concrete small target above, suffix rows are bounded by the expanded
constructor count plus names/levels and two declaration rows, well below 1,000
total rows including F. With the displayed short names its new syntax nesting
is also small (16 telescope binders plus the shallow conclusion), not near the
parser limit. The exact foundation prefix is already part of the retained
91,385-byte base frame. A final implementation should compute/check these virtual
bounds, not accept these hand counts as a reusable untrusted allocation token.

## Transparent types: the actual obstruction beyond RC0

Type-reference closure and value-body closure are different obligations. An
imported `d : T` can be represented as `moduleImportDef` with its exact body hash
and no body; correspondence permits that. But this only promises that a demand
will be explicit, not that the old checker will never demand the body.

An operational counterexample pattern is an imported abbreviation:

```text
D.{u} (X : Sort u) : Sort u := X
```

Consider comparing `D A` with `D ((fun X : Sort u => X) A)`. A body-free RC
beta-conversion algorithm can establish equality by reducing only the argument.
The old `tc.rs` takes a different path:

1. Its cheap WHNF leaves these distinct applications with the same head D.
2. The terms are types, so the proof-irrelevance shortcut does not discharge it.
3. `lazy_delta_step` sees two applied definitions.
4. `try_eq_const_app` attempts congruence only for matching **Regular** hints,
   not an abbreviation hint.
5. It calls `delta`, which reaches `env.get_declar_val` and
   `ValueSlot::Missing(...).require`, producing a body demand.

This demonstrates why an input-only, no-body witness construction for the broad
RC language is not established by the previous note. It does not by itself
prove that *no* larger witness exists: supplying the genuine D body can repair
this example. But the constructive witness then needs that body, its exact
commitment and dependency closure, and it must still fit the old aggregate and
module bounds. A theorem's authenticated existence is not a computable body
opening or an automatic bound on the combined conversion closure.

For a future broader profile, one must either supply and authenticate every body
actually demanded by a proved simulation of the old conversion schedule, or
prove a stricter no-demand condition for the allowed calls. Merely declaring all
definitions opaque changes their prescribed semantics and is forbidden. Initial
RC0 avoids this issue because its selected signature contains only the sealed
bc theorem and the fixed foundation, and its comparisons take the exact quick
path. No Tree definition/body closure is required.

## Consequence for journals, policy and next work

For RC0 with the witness/simulation/bounds above, preserving the existing semantic
I-shaped member J is justified in principle: it denotes the same conditional
module predicate conclusion. The new aggregate image must enforce RC0 and the
same graph premises; current receivers still require an explicit adoption of that
actual image and a coherent new wire/census profile. Old-A parents remain refused
unless a separately specified bridge genuinely verifies their exact old image.

The broader beta/zeta language is not granted this result. If it is later desired
without original operational inclusion, the honest alternatives are a separately
proved Lean-sound relation with explicitly distinguished journal/header authority,
or a stronger refinement argument. That does not necessarily change mathematical
F/P, but it cannot masquerade as original-predicate evidence merely by copying J.

The useful next decision is whether the strict profile's saved general-checker
work is sufficient on the identical selected target to justify implementing it.
Use existing assembly and the strongest current general route as comparator.
Do not fund a proof or widen the fragment before the refinement receives its
independent challenge and that economic decision has a prospective criterion.

No old I/A source, retained result or proof attempt was changed. No product
runtime was imported or executed and no experiment was repeated.
