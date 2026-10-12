# Validate new theorem proofs without constructing discarded canonical trees

2026-10-12. Root-requested source/theory plan only. **No checker edit, compiler,
test, guest, proof or network operation is selected or executed here.** The
parse-once build is separately held for root's warrant-variant architecture
review. This plan does not supersede that hold or authorize another build.

## Smallest defensible change

Keep the original `Inventory::expression`, `level`, `reference`, `visit`,
`Inventory::new`, and all type/body comparisons **unchanged**. Add two private
unit-returning methods, `validate_expression` and `validate_level`, to a fresh
copy of the correspondence module. Replace only the call which currently
constructs and discards a **new theorem proof's** canonical expression tree.

Retain calls to the exact existing `reference(owner,index)`, then drop their
results. This deliberately preserves its owner/foundation/name interpretation
and assertions without reimplementing that subtle function. Reference output
allocation remains; the first intervention removes only expression/level tree
materialization and the constant's collected level-Value array.

Current selected file:

`software/v5/modules/native/checker/src/module_correspondence.rs`

SHA-256 `f37c855666480553ee9b95f59dc3ba7ad19316e8e707aacd47fecfa29f1d12e2`.
The sole production call site is currently line367 in `match_declaration`:

```rust
inventory.expression(owner, uint(&record["value"]), &parameters, 0);
```

The replacement would invoke `validate_expression` on exactly those arguments.
It does not change the preceding theorem/type/name/universe/role checks. The
imported-theorem branch has already returned above this point and remains
unchanged. Definition/opaque bodies, types, recursor rules and other committed
expressions continue through the unchanged tree-producing comparison path.

The actual native kernel proof checking remains exactly as before. A proof's
absence from ModuleSpecID does **not** justify dropping correspondence syntax
validation or native checking. No new declaration is accepted on popularity,
receipt-shaped metadata or a conditional success flag.

## Checks and evaluation order to preserve

Every validator entry calls the unchanged `self.visit(depth)` **before** row
lookup, exactly as the old method does. `visit` increments work first, then
asserts `depth<=192` and `work<=250000`. Preserve both increment and failure
order, including failed-prefix state. It is not enough to count only successful
unique nodes or compare final successful totals.

For levels, retain row lookup/tag extraction and this sequence:

| Tag | Exact meaningful sequence after `visit` |
|---|---|
| index0 | Return, with that visit already charged |
| `param` | `uint(value)`; `self.name(name)`; ordered parameter `.position(...).expect(...)`; discard the normalized output index |
| `succ` | Convert child with `uint`; require child<index; validate child at depth+1 |
| `max`, `imax` | Array conversion; length2; convert a then b; require both<index; validate a then b |
| Other | Same `CORRESPONDENCE_LEVEL_TAG` panic |

Do not create new level-row schema constraints. `Inventory::new` and the old
level method already determine which fields are checked and when. Adding a
new harmless-looking early assertion can change the refusal order/domain.

For expressions, retain the row lookup and tag extraction after `visit`.
Every expression-child traversal performs `uint(child)`, requires child<index,
then recurses at depth+1, in the same order as the original closure.

| Tag | Exact meaningful sequence after `visit` and row/tag lookup |
|---|---|
| `bvar` | `uint(value)`; discard the number |
| `sort` | `uint(level index)`; validate that level at depth+1 |
| `const` | Exact fields name/us; array(us); arity<=256; for each level in order convert and validate; **then** convert name and call/drop unchanged `reference(owner,name)` |
| `app` | Exact fields fn/arg; traverse fn then arg |
| `lam`, `forallE` | Exact fields name/type/body/binderInfo; binder name integer and `< names.len()`; allowed binder-style text check; traverse type then body |
| `letE` | Exact fields name/type/value/body/nondep; binder name bound; exact `nondep=false`; traverse type, value, body |
| `proj` | Exact fields typeName/idx/struct; convert typeName and call/drop unchanged reference; **then** convert idx; **then** traverse struct |
| Other | Same `CORRESPONDENCE_NONCANONICAL_EXPRESSION` panic |

The constant's old level `collect::<Vec<Value>>()` occurs before its reference
call. The projection reference occurs before its numeric index and child.
Sequential statements in the new validators must preserve those orders, not
merely visit the same set. Binder index0 remains permitted where it was already
permitted; do not replace `< names.len()` with `self.name`, which rejects0.

`reference` stays unchanged, including all of the following:

- Nonzero name index and names-array bounds.
- Literal `DMKN.Mod` structured prefix interpretation and module component tag.
- Lowercase64hex owner digest syntax and relative-name validation.
- Distinction of current-owner local, other-owner external and foundation names.
- Foundation membership and the existing bounded cloned name/reference output.

Likewise `Inventory::new` continues to validate the **entire** submitted row
inventory: metadata, row kinds/fields/order, name backreferences and parts,
reserved foundation namespaces and duplicate foundation declarations. Do not
change it into a reachable-only constructor. Its global checks precede theorem
proof validation and are part of the accepted-input contract.

## Simulation argument, including refusals

Model observable semantic execution as the sequence of scalar/shape/reference
checks and `visit` state changes. Exclude allocations, deallocation, timing,
allocator failure and stack exhaustion from the equality claim; these resource
behaviors are why the implementation is being optimized and remain bounded by
the external operation envelope. The original `Value` constructors/destructors
do not introduce mathematical premises or user-defined callbacks.

The only mutable inventory field during these methods is `work`. The names,
levels, expressions, foundation names, owner and ordered parameter list are
fixed. Induct on the well-founded rank `(domain,index)`, ordering level calls
below expression calls, expression children by their strictly smaller indices,
and nonzero level children by their strictly smaller indices. Invalid indices
or missing rows stop with the same check/panic before any recursive induction
hypothesis is needed. Level0 is the charged base case.

At each constructor, the inventory table above gives the same sequence of local
checks and recursive calls. Apply the induction hypothesis successively, carrying
the exact work state from one child to the next. The original method then
constructs a Value; the new method returns unit. That construction has no further
semantic check. Therefore:

1. Both succeed or encounter the same first semantic failure.
2. Their work counts and completed/failed visit prefixes are equal.
3. The surrounding declaration routine sees the same inventory state and no
   consumed return value in either version.

The unchanged reference calls are included as identical subroutines, so their
failure order and assertions transfer directly. The same original methods
still compare type/body trees, so their returned committed Values do not change.
Sequential declaration processing then preserves matched groups, foundation
name indices and body obligations, including total cross-declaration work caps.
Combined with the unchanged relation and native checker, this gives identical
conditional module conclusions and exact parent journals on successful inputs.

This is a source-level refinement argument, not a completed machine-checked
proof of the checker or a new cryptographic certificate. The checker-to-Lean
and recursive receipt assumptions remain explicit. A new guest image must be
adopted even if all mathematical identities/internal I journals are preserved.

## Operation-cost consequence, not an unmeasured speed claim

Let U be the number of unfolded expression-plus-level visits in the theorem
proof. Let R be the number of constant/projection reference calls and L_R their
total normalized name/reference output size. The conservative validator keeps
exactly U visits and those R calls. It does not memoize the DAG or weaken the
unfolded work cap. Its reference allocation cost O(L_R) remains.

Each old visited expression/level constructs a tagged Value array and tag
string. Most additionally create child/scalar Values, and each `const` gathers
its level Values into a vector. All those nonreference output Values cease to
be materialized for the theorem proof. The precise logical Value-construction
census can be computed from the retained DAG without running the checker:

    E(bvar) = 3                 L(zero) = 2
    E(sort u) = 2 + L(u)       L(param) = 3
    E(const us) = 3 + sum L(u) L(succ u) = 2 + L(u)
    E(app f x) = 2+E(f)+E(x)  L(max/imax u v) = 2+L(u)+L(v)
    E(lam/forall t b) = 3+E(t)+E(b)
    E(let t v b) = 2+E(t)+E(v)+E(b)
    E(proj s) = 3+E(s).

E intentionally excludes reference subtrees because those are retained and
dropped under both routes. Repeated DAG references count with multiplicity.
These counts are Values, not allocator calls, bytes, RV32 rows or CPU time.
The compiler may optimize some constructors already; this plan claims no
measured speedup or guaranteed cycle-ceiling success.

The old unused proof tree can occupy space proportional to its unfolded output;
the new traversal needs recursive stack plus one temporary reference result,
excluding the already existing input/inventory and native checker state. Native
kernel work, type/body comparison allocation, hashing, parsing and proof-system
costs remain. This addresses demonstrably unused representation work, not all
of the cost of aggregation or meaningful network growth.

## Fresh layout and smallest useful validation

Proposed fresh directory, only after root selects implementation:

`software/v5/modules/native/proof_validation/`

- `module_correspondence.rs`: exact original copy plus the two private validator
  methods, the single theorem-proof call replacement and a test-only child-module
  declaration. Original tree-producing functions stay byte-identical.
- `correspondence_controls.rs`: private test child module, able to construct two
  equal inventories and call both the original `expression` and new validator.
- `control_root.rs`: a standalone test crate importing only that correspondence
  module. It needs retained serde/serde_json, not a full native checker build.
- Later, only if selected, `lib.rs`: thin checker crate root path-reusing every
  frozen existing checker module except this fresh correspondence module. Keep
  the public nanoda API and constant stack size unchanged.

Because the old tree-producing methods remain in the **same** source module,
the focused test does not need to copy or reimplement its reference algorithm.
Independent review must compare those method bytes against the pinned old file.
Run two equal inventories through old/new calls, catch panics separately, compare
first diagnostic and work counter even on failure, and confirm the successful
validator's unit result follows a successful old expansion. No untrusted caller
gets access to these private controls or can fabricate production conclusions.

Minimum cases cover every constructor, zero/nonzero levels, implicit/default
binders, local/external/foundation references, repeated shared children, ordered
universes and the following ordering discriminators:

- Constant with an earlier invalid universe and later invalid name: universe
  refusal must still occur first.
- Projection with invalid reference plus invalid index/child: reference first;
  with valid reference and bad index plus child: index first.
- Binary node with both children invalid: first child refusal and work prefix.
- Depth/work edge cases seeded below/at the limit; global already-used work
  across two consecutive proofs; usize overflow only under the same checked
  arithmetic profile if a test constructs that otherwise unreachable seed.
- Malformed earlier inventory rows and foundation/name policy failures, through
  the unchanged constructor, before either proof method is reached.

A serde-only standalone compile/control is a cheap changed-boundary discriminator
and can precede any heavy checker build. It is not native mathematical acceptance.
After it and independent review pass, build the full checker successor **once**,
then relink the unchanged module relation and chosen aggregate successor against
that same artifact. Compare the already retained actual two-delta positive and
invalid-proof refusal, without reauthoring or generating certificates. Combine
this source change and the separately reviewed parse-once change into a single
later guest candidate if root adopts both; avoid one heavy guest experiment per
small representation edit.

## Decision boundary

This optimization is orthogonal to the live exact-warrant-variant merge question.
Settling aggregation semantics takes precedence over a build likely to be
invalidated by that design decision. No claimed savings here establish that the
new graph is operable or that the aggregate seal is economically justified.
After semantics and source checks settle, one prospective informative guest
screen should measure actual completion/segments and inform whether a finite
proof investment can meet the full-cost workload inequality.

## Source-only implementation selected and written

Root subsequently selected only the three fresh source/control files below.
The earlier no-edit statement describes the original planning boundary; this
selection does **not** authorize compilation, test execution, checker rebuild,
guest execution or proving. The complete v5 objective remains active.

| Fresh path under `software/v5/modules/native/proof_validation/` | SHA-256 |
|---|---|
| `module_correspondence.rs` | `ee4f33a9d4896bd59b2456cb1712d13010d0838b8ba0be34c89c10ebba18bdf8` |
| `correspondence_controls.rs` | `2162b252894f6653dcaa31f36454c1bb07763d1155d830a7a5a46cff4e9b6d35` |
| `control_root.rs` | `74f29dd1ed1a034ad57ec833391dd36a38199429700151a9a1afa3fb6a3d475a` |

The successor adds exactly the two private validators and a test-only child
module, and changes exactly the discarded new-theorem-proof call. A read-only
text comparison removes those additions and reverses that one replacement,
then reconstructs the original pinned correspondence file **byte for byte**.
Original tree-producing `expression`/`level`, `reference`, `visit`, the whole
inventory constructor, all committed type/body comparisons and all other
declaration code therefore remain unchanged. No resource-counter cap changes:
250,000 unfolded visits and depth192, with increment-before-assertion preserved.

The standalone serde-only root contains twelve differential/structural groups:

1. Every expression constructor, all three reference kinds, ordered universes
   and a repeated shared-child expression with59unfolded visits.
2. Zero, parameter, successor, maximum and imax level constructors.
3. Constant levels before references, malformed levels and universe arity.
4. Projection reference before numeric index before expression child.
5. Left-to-right expression/level siblings, comparing failed-prefix work.
6. All binder styles, allowed zero binder names and the nondep=false check.
7. Malformed tags, shapes, missing indices and nondecreasing backreferences.
8. Unknown foundation names, zero reference names, module digest/component
   refusals through the **unchanged** reference subroutine.
9. Work/depth edges, entry charging before missing indices and failed-child
   charging including level0.
10. Sequential proofs sharing one inventory work counter, including continuation
    after caught refusal for diagnostic comparison only.
11. Complete-inventory errors, including unreachable expression rows, malformed
    names, duplicate foundation declarations and reserved namespaces.
12. The changed theorem call and unchanged imported-theorem early return through
    the public structural correspondence entry; its result remains explicitly
    `mathematical_admission=false` and `hash_verification_performed=false`.

Controls1-10 compare success/first panic diagnostic and exact work counter
against the original producing methods in the same module. Control11 exercises
the unchanged shared constructor; control12 exercises the surrounding public
structural API. These are synthetic syntax controls, not native proof checking
or mathematical certification. No native checker build or production guest
image is included in this source assignment. Independent source review is
requested before root selects any bounded execution.

### Separate source-only serde controller

Root then selected one additional source-only `control.py`, SHA-256
`91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1`.
It borrows the already retained compiler command, provision environment and
Windows Job/phase monitor instead of adding a build framework. Its exact
four-source configuration has schema `DMKN_V5_PROOF_VALIDATION_CONTROLS_V1`,
name `proof-validation-controls-NN`, the Boolean
`authorizes_serde_compile_and_syntax_tests=true`, and the four canonical-relative
source `{bytes,sha256}` entries. No such runtime selection is made by this note.

The prospective operation snapshots the four sources and makes exactly two
worker calls: compile `control_root.rs` with `--test`, then run that executable
once with `--test-threads=1`. It retains the existing overflow-checks, unwind,
optimization, compiler/linker and fat-LTO settings but supplies only `serde` and
`serde_json` as extern crates. No checker/module/proof-system extern is linked,
and no Cargo or dependency build is invoked. Existing broad runtime pins are
conservatively rechecked, including artifacts not needed by this smaller target.

Both calls share120workerCPU/120phasewall seconds,1536MiB and6processes. The
outer controller has60CPU/300totalwall seconds,256MiB output and1024entries;
logs are limited to1MiB per command. Owned compiler-telemetry cleanup is allowed
only on the compile call. Exact12test names and12passed/0failed/0ignored/0filtered
are required, with immutable binary, source, runtime and snapshot checks at
completion and an overriding finalization-failure marker on envelope failure.
This controller is unexecuted and requires root's separate exact reviewed
selection before it may run.
