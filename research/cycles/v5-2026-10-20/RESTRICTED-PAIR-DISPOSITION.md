# RC cost screen failed: reject proof investment; investigate only identity shortcuts

2026-10-21, core_growth. Source/evidence diagnosis only. No source mutation,
import, test, guest execution, proof, retry or threshold change was performed.
The complete actual-outcome audit belongs to adaptive; this note reads the
retained pair result/diagnostics to inform the next central decision.

## Decision

Do not adopt the current RC checker as an efficiency improvement and do not
fund its proof production. Its compact representation did not buy cheaper guest
checking on the same actual target. The largest defensible next RC step is a
small **source-only identity-shortcut successor**, not another representation,
parser redesign, broader language or runtime campaign. Derived node summaries
can avoid provably useless substitution/abstraction work without changing
mathematical rules. This has a concrete implementation advantage over generic
profiling, but no evidence yet that it can meet the unchanged investment screen.

Root should select that successor only as a bounded implementation/refinement
task. Before any later build/guest selection, require its precise equivalence
argument and focused source/control review. If that does not produce a credible
changed cost boundary, shelve RC as a performance route and retain the stronger
general checker while prioritizing actual reusable-context/import amortization.
Do not spend successive full cycles guessing at guest speed.

## What the actual result says

Source: `experiments/v5-local-checks/restricted-matched-execution-01/pair/RESULT.json`.
Both exact endpoints completed, but overall status is
`FAIL_RC_INVESTMENT_SCREEN`, with no proof or mathematical admission.

| Quantity | General | Restricted |
|---|---:|---:|
| Wire bytes | 35720 | 7037 |
| Retained segments | 36 | 40 |
| Padded rows | 9240576 | 10354688 |
| Nonpadding rows | 8367627 | 9329690 |
| Instructions | 10202450 | 13661107 |
| Host Job CPU seconds | 0.859375 | 0.796875 |
| Arm controller CPU seconds | 0.65625 | 1.046875 |
| Standalone known CPU including common setup | 2.171875 | 2.5 |

Common measured setup/final-binding CPU was0.65625 seconds, charged equally to
both standalone arms and once in pair total4.015625. The0.328125-second standalone
regression is not erased by the host's0.0625-second lower observed CPU. A single
fixed-order pair at this granularity is not statistical timing evidence.

The larger rows/instruction counts are a stronger reason not to fund a proof:
RC has12.0567% more padded rows,11.4974% more nonpadding rows and33.9003% more
instructions despite80.2996% fewer input bytes. The75%-of-general row threshold
is6930432. Reaching it from current RC requires33.0696% fewer padded rows,
not merely removing the12% regression. The64-segment cap passes, but both the
row-ratio and CPU-nonregression conditions fail. None is relaxed here.

These are complete-session observations, not a per-function guest profile.
The retained host phase durations are wall observations: general/RC native
preflight140/60ms, guest execution+custody415/464ms, materialization286/50ms.
They do not isolate guest functions, explain controller overhead or establish
repeatable savings. Controller work includes file/path checking, segment
readback/hashing and bookkeeping; no retained per-operation CPU breakdown can
assign its0.390625-second difference to one cause.

## Deterministic source facts, not inferred timings

### RC repeatedly traverses unchanged term regions

In `restricted_composition/typing.rs`:

- `open` at line68 starts a fresh BTreeMap per call. Its visitor walks every
  reachable App/Pi/Lam subtree, including regions containing no relevant loose
  variable; unchanged nodes are cloned and sent through arena interning.
- `close` at line89 similarly walks and re-interns regions containing no
  occurrence of the selected Local node. Const values carry owned names and
  vectors; cloning/re-interning them is not a pointer-only identity operation.
- `subst_levels` has independent traversal caches, and all map/cache lookups are
  BTree-based. Replacing every map is not selected: no evidence isolates it.
- `Arena::node` at `syntax.rs:105` charges work and probes the interning map
  even when the traversal has reconstructed a node unchanged. The arena has no
  loose-variable/local-occurrence summary to prove an early return.

The retained general checker already has corresponding optimizations:
`modules/native/checker/src/expr.rs:175` returns immediately when
`num_loose_bvars(e) <= offset`; abstraction at lines231/287 immediately returns
when `has_fvars(e)` is false. `util.rs` derives those summaries when allocating
nodes. Thus a simpler language does not imply a cheaper implementation: RC
removed broad kernel machinery but also omitted optimizations relevant to this
very workload.

### RC also lacks the baseline's telescope/application batching

RC infers each Pi/Lam by opening its entire remaining body, then recurses. Its
App inference processes nested applications and opens each residual Pi body.
General `tc.rs:550`, `:615` and `:645` unfold application/telescope spines and
instantiate domains plus the final body against accumulated arguments/locals.

The fixed target has sixteen Pi binders, sixteen lambda binders and three
ten-argument applications of `binary_congr`. The RC strategy repeatedly walks
the decreasing binder tails. For a fresh k-binder chain, tail traversal alone
visits k(k-1)/2 residual binder constructors, before counting their domains or
the final body. The general batching avoids those particular repeated tail
walks. Caching within one open call cannot remove work repeated across calls
with changed replacements. This is an algorithmic source fact, not proof that
batching would save a specified fraction of the measured total.

Batching is a possible second step, but not the initial recommendation: it
changes local creation/order, inference-cache behavior and close/level handling.
Identity shortcuts have a smaller semantic/refinement surface.

### Repeated validation exists, but is not the selected first repair

The RC aggregate uses `census.charge`: strict `parse_validated` performs a
canonical-size traversal, then aggregate census walks the Value. Core
`check_with_census` calls `frame_bounds`, which walks the Value and calls
`canonical_size` again. Two structural walks plus two canonical-size traversals
occur after parsing. Eliminating them requires an unforgeable parser-produced
validated-frame boundary or an equivalent combined traversal argument; removing
checks ad hoc is not sound. The frame has only1184 JSON nodes in this workload,
and the result does not attribute costs to these passes. A parser redesign is
therefore lower priority than the clear substitution identity seam.

## Smallest justified successor and proof obligations

If root selects it, create **fresh** `restricted_composition/syntax03.rs`,
`typing03.rs`, and `lib03.rs` (new lib path attributes select the two successors).
Keep used lib02/foundation02/typing/syntax/relation/aggregate sources and all
used adapters/evidence frozen. Relation semantics, fixed foundation, frame/wire,
virtual-witness bounds, exact target and screen remain unchanged. Any build or
control adapter is a separate later root selection, not part of this note.

The fresh arena derives immutable summaries for each newly interned node:

1. Loose-variable extent L. `L(Bvar i)=i+1`; Sort/Const/Local have0;
   `L(App f a)=max(L(f),L(a))`; for Pi/Lam,
   `L=max(L(domain), max(L(body)-1,0))`.
2. Optional min/max range of syntactically occurring Local **node IDs**.
   A Local node's range is its own arena ID; App/Pi/Lam combine child ranges;
   all other nodes have no range. A Local's stored type is deliberately not
   traversed: the existing open/close treats Local as an atomic expression.
   Using node IDs matches close's exact equality directly without assuming
   that serial numbers identify nodes with arbitrary stored types.
3. Traversal height H with atomic leaves height0 and App/Pi/Lam height
   `1+max(child heights)`. Local's stored type remains atomic here too. Before
   taking an identity shortcut at recursive depth d, require checked
   `d+H(e)<=MAX_INTERNAL_DEPTH`. This conservatively preserves the explicit
   depth cap instead of silently omitting the skipped recursive checks.

These summaries are computed solely from immutable constructors and earlier
child summaries. They are not caller-supplied capabilities, wire fields,
mathematical authority or approximated equalities. Reusing an interned node
reuses its already derived summary. No declaration body is inspected or hidden.

The only initial operational changes should be:

- Before cloning/traversing a node in open at offset o, return its original ID
  when `L(e)<=o`. This cannot hide the old `i>offset` refusal: any such variable
  would force L(e)>o. Induction over constructors proves the old traversal
  leaves every node unchanged on the shortcut branch.
- Before cloning/traversing a node in close for local ID q, return its original
  ID when the local range is empty or excludes q. Induction proves q is absent
  from every traversed syntactic position; the old close therefore has exactly
  the same result. A range containing q may be a false positive and simply
  falls back to the unchanged algorithm; it cannot grant false equality.

Depth checking at the current visit and the shortcut's derived-height guard
remain. The height guard can conservatively refuse a case whose old per-call
cache would prune a deeper traversal; no broader acceptance claim is made.
Original parsing/source-depth, arena-size and overflow limits remain. Charge
metadata construction and lookup as actual bounded work; summaries are not
free. Root must explicitly review how skipped
visits affect the engineering `inference_work` census: it should count the new
actual work, not falsely report the old work. Reduced work can move some inputs
below a resource refusal; that is not a mathematical language extension, but
must not be described as identical resource-refusal behavior. Virtual-witness
existence bounds remain source-derived and unchanged. The refinement obligation
is equal conclusions on completed old/new checks, plus soundness of newly
resource-admissible checks under the unchanged rules—not identical counter values.

For a traversal over n reachable node/offset states, old work visits n states
and performs associated map/interner operations. New work visits only the
affected paths and their shortcut boundary (at most the old visited states),
plus fixed-size summary work once per new node. Repeated substitution of large
irrelevant regions can therefore change repeated traversal cost into constant
identity checks. This establishes a nonempty improvement region, not a global
speedup: summary derivation/storage and branch overhead can cost more on fully
affected small terms. It does not prove33.0696% savings on this target.

Do not simultaneously add batch binders, a new hash table, direct binary syntax,
weaker equality, new parameters or general beta/delta reduction. Those would
make attribution and refinement substantially harder than the selected seam.

## Integration priority and fallback

Current RC proof production remains rejected. A single narrowly reviewed source
successor is justifiable because it removes demonstrably unnecessary work using
the same invariant already exploited by the baseline. Only a later separately
selected changed-boundary screen can determine whether the implementation clears
the original investment rule; this note authorizes none.

In parallel, release owns product-level reusable-context/import-payload costs
and the actual local contribution loop. Those costs are distinct from this
guest-core diagnosis; neither should duplicate the other. If the narrow seam
cannot justify another central step, use the retained general checker and move
the main effort to continued context reuse/owner-authorized amortization of
checking and validation. This can improve deployable local operation without
pretending it solves economical new certificates.

The earlier31.515625-second sharing observation concerns a different workload
and is not transferred as a benefit coefficient. Any certificate investment
needs its own same-workload reuse/benefit region, all creation/build/proof/service
costs and honest uncertainty. The failed pair remains failed regardless of any
future component success.
