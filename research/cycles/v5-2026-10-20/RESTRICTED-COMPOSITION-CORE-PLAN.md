# RC0 core implementation contract

Source-only plan; no implementation or runtime authorized by this file. Root
owns selection/build/launch. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Exact next component

Implement the normal application-spine profile from
`RESTRICTED-COMPOSITION-REFINEMENT.md`, with the stronger native binder-origin
condition below. Its purpose is to establish ordinary theorem deltas without
constructing the 413-row foundation/native export or invoking the general
kernel in the guest. It is not a new proof language or a replacement for general
Lean mathematics. Initial genuine parent is the retained base-I `binary_congr`.

Proposed frame schema: `DMKN_RESTRICTED_COMPOSITION_V1`.
Exact fields: `schema,image,rank,local_spec,parents,proofs`.

- `image` is the fixed existing I semantic member image, not the new A-RC image.
- `local_spec` uses existing module/group/theorem descriptors unchanged.
- `parents` uses existing `{journal,openings}` records unchanged.
- `proofs` is an ordered array of canonical expressions, exactly one for each
  local singleton theorem group. Its universe arity is that descriptor's arity.
- There are no rows, body openings, user typing annotations or truth flags.

All new/imported groups are ordinary singleton theorems. Imports are authenticated
selected types, never proof bodies. Every external reference resolves within the
opened type-reference closure. New local references resolve only to earlier
checked groups. Reject imported definition/opaque/inductive/constructor/recursor
groups, including any hidden in the required type closure.

Wire forms: `bvar`, `sort`, `const`, `app`, `lam`, `forall`; binder styles are the
existing four values. Public universe expressions are only `zero` and scoped
positional `param`. No let/proj, beta/zeta/delta/iota, universe inference,
literal extension, proof-irrelevance conversion or tactic execution.
Functions must expose a Pi without reduction and sorts a Sort without reduction.
An unsupported case is a refusal, not a fallback accepted under RC0.

## Public caps and conservative original-witness bounds

Use these deliberately modest caps for the initial version:

| Quantity | Cap |
|---|---:|
| Complete canonical RC frame | 256 KiB |
| Frame JSON value nodes / container depth | 32,768 / 64 |
| Parents / selected imported groups / new groups | 8 / 16 / 8 |
| Universes per declaration | 8 |
| Expanded expression occurrences across selected types and all new proofs | 8,192 |
| Expression depth / simultaneously opened binders | 48 / 64 |
| Distinct qualified constant/declaration addresses, including F references | 64 |
| Relative name components / UTF-8 bytes per string component | 8 / 64 |
| Internal expression/substitution work visits | 200,000 |
| Internal interned expression/type nodes | 32,768 |

The counters are aggregate across a whole frame. A repeated occurrence is charged
again even if interned. Constant universe arguments are charged and require exact
arity. Name strings use existing escaping/validation; numeric components are u32.
Internal node/work caps may refuse a mathematically valid input but never make
fuel exhaustion an acceptance. No counter resets per theorem or conversion.

These caps imply the old virtual witness bounds without traversing F per delta:

1. The exact generated `foundation_data.rs` records **413 rows, 23,313 canonical
   UTF-8 bytes**, SHA256
   `736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`.
   These are fixed audited prefix constants, not sender claims.
2. There are at most `64*11 + 8*3 = 728` appended name nodes: at most eleven
   components per qualified address (three fixed prefix components plus eight
   relative), and three per generated universe name. Round the allowance to768.
3. There are at most8 appended universe-level nodes (one per positional parameter)
   and8,192 appended expression nodes. Internal inferred successor/imax levels
   are not serialized into the original proof/type witness.
4. There are at most24 new/import declaration rows. Therefore virtual rows are
   bounded by `413+768+8+8192+24 = 9405`, below250,000. Total declarations are
   at most22+24=46, below16,384; combined groups at most24, below4,096.
5. Original correspondence visits each expression occurrence plus at most eight
   universe leaves. Thus its cumulative work is at most `9*8192 = 73728`, below
   250,000. Its expression/level depth is at most49, below192. No recursor/body
   traversal is hidden in this count.
6. A suffix native name row, including its separating comma, is bounded by512
   bytes: JSON escaping costs at most six bytes per input UTF-8 byte, plus a
   small fixed record and index overhead. An expression/declaration row is bounded
   by256 bytes; a level row by128. References use indices below9405 and at most
   eight universe indices. Retained local-spec/parent material occupies no more
   than the complete256KiB frame, plus4096 bytes for changed wrapper overhead.
   Hence virtual canonical bytes are bounded by:

   `23313 + 768*512 + 8192*256 + 8*128 + 24*256 + 262144 + 4096 < 3 MiB`.

7. The virtual JSON-node count is bounded by prefix23,313 (even the loose bound
   of one node per prefix byte), plus32 nodes per suffix expression/declaration,
   eight per name/level row, the frame's32,768 nodes and a1,024 wrapper allowance.
   This is below350,000, hence below the old1,000,000 limit.
8. Appended native rows have shallow fixed nesting. Copied local-spec/parent
   material already has container depth at most64, well inside serde_json's
   default recursion limit128 and the old independent depth256 census. Actual
   output wrapper nesting must preserve the copied fields' depths, not add an
   extra recursive envelope.

The checker enforces the component caps and uses checked integer arithmetic in
these inequalities. No expensive old-row emission, original parser or whole
foundation allocation is needed merely to test these bounds. The byte constants
and parser nesting argument are implementation review obligations, not informal
operator defaults. The native differential harness can separately construct the
small concrete W once to check the bridge; it is not the guest production path.

## Small source boundary and ownership

Suggested fresh core files under `software/v5/restricted_composition/`:

- `syntax.rs`: exact RC frame/Expr validation, address inventory, immutable parsed
  expression arena and monotone source/work/virtual-bound counters.
- `foundation.rs`: only the compiled Eq/Eq.trans signature projection and its
  original binder metadata, plus fixed audited F prefix constants. No full
  foundation row array or native parser.
- `typing.rs`: bounded syntax-directed inference, opening/closing, simultaneous
  universe substitution and restricted exact/native-binder comparison.
- `relation.rs`: existing F/P/module/group commitments, exact parent/group checks,
  ordered theorem checking and construction of the unchanged J plus parent list.

Core author owns these four files. Reuse existing canonical hashing,
`commitments::{summarize,verify_opening}`, policy and journal implementations;
do not fork their mathematics or hash framing. Wire/aggregate owner separately
owns the distinct outer protocol/census/dispatcher, existing graph integration
and producer routing. Root owns actual guest/host source selection and trust
adoption. Independent reviewer owns new controls and source challenge.

Proposed seam:

```text
parse_bounded_rc_frame(bytes) -> private RcFrame
check_rc_frame(RcFrame) -> private RcConclusion { journal, parent_journals }
```

The frame token is constructible only by the bounded decoder. No externally
supplied counts or alleged native pass enter it. Conclusion construction remains
private and conditional. The existing aggregate graph must establish every exact
parent J before admitting its delta; guest receipt verification then discharges
external I or same-image A-RC assumptions. Host and guest use this same core,
not two nearly matching validators. Exact names may be aligned with the wire
owner before implementation without changing these obligations.

## Minimal checking representation and substitution

Use a small hash-consed expression arena, not Nanoda's complete environment or
general reduction engine. Required internal forms are public forms plus scoped
`Local(id,type)` introduced only while opening a binder. Interning uses complete
structural equality after hashing; collisions cannot identify different terms.
Types and terms use the same representation and exact qualified constant keys.

Retain **native binder-name origin metadata** internally:

- Every canonical imported/local binder has anonymous native name0, exactly as
  the constructive witness emitter specifies.
- Compiled foundation types retain their original native binder-name identities
  and styles, rather than prematurely erasing their names.

This prevents a false proof of native pointer equality when a binder-name
difference occurs underneath an application. The restricted conversion checker
allows either exact full internal structure, or a direct root Pi/Pi (or
Lambda/Lambda) comparison following original `def_eq_binder_aux`: check domains,
open both bodies with the **same** fresh local and recurse. There is no generic
application-congruence alpha conversion and no normalization fallback. Binder
styles/names are ignored only in that explicit native quick-check path. If an
equality cannot be discharged there, return unsupported/refused before delta.

`infer` mirrors the narrow original cases:

- Sort returns Sort(succ level); const substitutes its exact universe parameters.
- An application consumes a syntactic Pi, checks its argument against that
  domain using the restricted comparator, and substitutes it in the result.
- Pi checks each domain/body is a type and computes the internal imax sort.
- Lambda checks its binder type, opens its body and abstracts the inferred type.
- A local returns its stored type; exposed loose bvars always refuse.

Open canonical binder bodies using fresh local IDs; then substitutions act on
terms with no loose bvars, matching native `inst`'s reversal of the ordered
substitution vector. Increment binder offsets under Pi/Lambda, and close only
the locals introduced in that scope. Avoid a separate arbitrary beta reducer.
Universe substitution is simultaneous and does not recursively substitute a
replacement. Cache keys include the expression, substitution and context; caches
are bounded and invocation-local. Generated expression/level visits are charged.

Internal universe constructors are zero, parameter, successor and imax. RC0 need
not decide general universe equality. Exact comparisons are structural; only
Prop recognition needs to establish generated imax chains ending in zero are
zero. This is the original `imax(_,0)=0` path. All other difficult comparisons
refuse. The original input-level grammar remains zero/parameter only.

At each local theorem, require its exact declared type to infer to Prop and its
proof type to pass the restricted comparison against that declared type. Mark
the local available only then. Journal identity still excludes the proof witness;
the proof is checked, not accepted as a new axiom or stored provenance hash.

## Deriving the tiny foundation signature exactly

Whitelist only foundation **Eq** and **Eq.trans** in the first core. Eq is a type
former used in types; Eq.trans is the optional explicit equality-composition
proof constant. The base `binary_congr` is not built in: its exact type and
receipt-backed authority must arrive through an authenticated group opening.
Eq.refl is unnecessary for the selected target; add it only through a separately
reviewed signature expansion if a concrete use requires it.

Derive the two signatures offline from the exact adopted prefix already embedded
in original `foundation_data.rs` / its pinned receipt input. Follow the name,
level and expression DAG to their declaration types and retain original binder
name indices/styles as origin tags. Preserve exact universe arities and ordered
parameters. Check the derived closed type trees against the retained prefix in
the one new native harness; hash/pin the projected table and record its source
F digest in the build selection. This is a finite source-generation step before
adoption, not per-delta reconstruction or trusting an unverified label at runtime.

The tiny table imports authority from the **whole adopted F**, which already
contains Eq's complete inductive block and Eq.trans's checked theorem. It does
not claim Eq can be independently declared without its constructor/recursor
support. The virtual witness still includes the unchanged complete F prefix.
Other foundation constants refuse even though the general library supports them.

## One native changed-boundary harness

After source review, one small native harness can test all changed seams together:

1. Derive/check the two compiled foundation signatures against the exact prefix.
2. Read the retained genuine base J/opening; do not regenerate or re-prove it.
3. Build the exact four-universe/16-binder target and its three explicit bc
   applications from the refinement note. Check it with RC0; separately emit W
   with the existing constructive row format and run the **original** conditional
   module relation on that identical spec/proof/parent set. Compare complete J
   and ordered parent conclusions, not a Boolean or just theorem name.
4. Check a second conditional delta using the first exact J through the graph
   semantics. This tests recursive shape only; native execution cannot manufacture
   a genuine first A-RC receipt, so do not report portable authority.
5. Apply bounded mutations: wrong universe/arity, wrong proof argument,
   binder capture/free variable, changed target type, forward/self reference,
   wrong parent opening, altered group/kind, missing type-reference dependency,
   nested foundation binder-name mismatch, and source/internal/virtual cap edges.

The differential property is **one-way**: every RC0 acceptance must make original
W pass identically. Unsupported-but-valid forms may be accepted by the general
checker while RC0 refuses; such outcomes are correct, not a failed equality-of-
languages test. Malformed commitment/type mutations should refuse in both where
they are in both languages. Preserve original Need versus refusal diagnostics.

This one harness replaces separate syntax/typing/bridge smoke campaigns; it does
not rerun old receipt/custody suites. Select a finite native-only envelope later.
Only after it and the independent outcome review pass should root consider a
guest build and an identical-target cost screen. No cryptographic proof campaign
is selected here. FIRST's148 segments cannot price this different workload, and
fixed po18 workspace/per-segment cryptographic cost is unchanged.

## Conditions for starting implementation

Root must adopt the refinement plus its native-binder correction, agree on the
minimal wire seam, and assign these disjoint files. No new mathematical policy,
old-A bridge, general reduction engine, extra profiling subsystem or broad
foundation import is part of this implementation. The target is a reusable
strict fast path with explicit refusal and ordinary v5 receiver compatibility.
