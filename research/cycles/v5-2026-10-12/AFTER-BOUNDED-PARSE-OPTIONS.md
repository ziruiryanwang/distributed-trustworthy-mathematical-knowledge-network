# After bounded-parse: choose the next investment

2026-10-12. Source/retained-data decision memo only. No new implementation,
runtime, proof allocation or Git operation. This supplements, rather than
repeats, `COMPACT-WITNESS-FEASIBILITY.md` and `BOUNDED-PARSE-DECISION.md`.

## What the latest failure establishes

The adopted image `173255698c2bc9030e7528297b627c59d6d35a605ec3a16542b2ba73e5107ac2`
still failed its selected 2^25-cycle screen. Diagnostic SHA-256
`dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72`
reports session-limit refusal and no complete accepted capsule. No proof stage
is justified from those partial segments. The failure gives neither full-run
cost nor remaining work; it is not evidence that doubling the cap will finish.

The current source has already removed duplicate canonical-size scans and
reused immutable structural counts. It already moves large input fields, and
the selected checker wrapper is `modules/native/proof_validation/lib.rs`, not
the older checker lib: local theorem syntax validation without materializing a
discarded proof tree is already implemented. Do not count these as new options.

The base lane is performing **one exact-current-image offline attribution**.
Reuse it; do not map the new PCs through the old ELF or run a second profiler.
The saved samples are saturated and cover only a failed prefix. The diagnostic
contains 131,614 stored and 22,960 omitted sample events; cumulative maximum
trace-cycle labels are not a denominator for the selected session-cycle cap.
Category counts can direct inspection, not establish causal or whole-run shares.

## Three choices, with their actual boundaries

| Choice | Work it can remove | Work it cannot remove | Main implementation cost |
|---|---|---|---|
| Lossless compact encoding into the existing Value algebra | JSON punctuation, escape and decimal-input parsing; some witness transport bytes | Value allocation/maps, most schema traversal, canonical semantic hashing, row correspondence/DAG construction, new mathematical checking, receipt verification | New decoder/bounds and wire version; native and guest integration; new guest image and compatible snapshot/stage hosts |
| One localized redundant-representation/commitment seam | Proven unnecessary copying, rebuilding or re-encoding of the **same authenticated immutable value** | Required checking of new proofs, required transparent semantics, reading new material, exact commitments not already established | Focused equality/invariant argument and source change; new image if guest source changes, with native correspondence preserved |
| Deliberately larger execution envelope | Nothing: buys completion information and potentially a reusable complete capsule | All existing guest/prover work; no efficiency or growth advantage by itself | Explicit joint cycle/segment/memory/storage/proof-cost decision, new fresh execution; no automatic renewal |

All three preserve certificate-based receiver independence from ancestral proof
replay **if** the accepted relation and recursive assumptions remain sound. They
change the producer's acquisition/certification cost, not the semantic search
guarantee. Lower producer cost improves the full-cost benefit region and service
capacity; a successful longer run alone does not establish either improvement.

## Compact transport is not just a decoder patch

Use the existing feasibility note's narrow round-trip target:
`decode(encode(V)) = V`, then unchanged mathematical acceptance of V and exact
canonical commitment bytes. Keep module semantic IDs and member Js unchanged;
aggregate H can retain the current **v2** layout/meaning, but its adopted image
slot changes to A'. No proof/header patching is allowed.

Two concrete prices must enter the decision:

1. The current `BoundedValue` raw-JSON length lemma does not apply to compact
   bytes. The decoder must establish the old canonical-JSON expansion envelope,
   global node/child-slot and depth limits, strict integer/string/map rules and
   exact EOF. Cheap-looking binary input can expand. Computing canonical lengths
   may reintroduce string classification and decimal-length work removed by
   bounded-parse; its net saving is not the entire old JSON parser cost.
2. The retained snapshot and proposed stage host call native aggregate
   `check_bytes` bound to the current v2 JSON-bearing wire. A new guest decoder
   alone is unusable through that path. The source must provide unambiguous
   version dispatch/new wire, matching native module/aggregate libraries, an
   encoder, compatible snapshot/stage host links and image/session bindings.
   A dual-representation shortcut would instead need a new rigorous binding
   argument; it is not free. The unchanged checker/backend can still be reused,
   but these native-library/host boundaries cannot simply be omitted.

Select this option only if exact-current evidence points to substantial lexical
input work that survives bounded-parse, and a source-based operation comparison
supports a net reduction after bounds. It will not solve a dominant checker or
canonical commitment bottleneck. Keep the initial representation lossless; a
typed arena, dictionary/backreference scheme or altered semantic hash is a
different, substantially larger change.

## What a smaller source seam would have to demonstrate

The current source still shows potentially avoidable work, but its magnitude is
unestablished. Examples for **inspection, not an implementation queue**:

- `module_relation::check_bound` clones selected group descriptors into bindings;
  correspondence clones used body openings into `body_hash_obligations`, while
  this relation consumes only that returned vector's length after checking each
  original body hash. Borrowing or a validated-count result could remove copies
  only if the same used-body set, exact comparisons and resource refusals remain.
- Commitment routines construct temporary `json!` Values, serialize canonical
  bytes, then copy those bytes into a second domain-framed buffer. Removing one
  copy can preserve the hash exactly. Replacing this with incremental hashing
  must retain the byte-length prefix, identical canonical bytes and bounds; a
  new counting pass or many tiny accelerated calls can erase the benefit.
- Foundation rows, imports and native DAGs are reconstructed per delta. A
  within-operation cache might save repeated work, but it must bind full immutable
  content, foundation/policy, owner/universe context and validated role. Caching
  by a short name or sender-claimed hash, or skipping a new local proof, is not
  an acceptable optimization. This is a larger seam than a removed copy.

Inspect the **selected** proof-validation wrapper/source map, not an older
source with similar function names. The retained group/body and row/native
representations serve different authenticity/correspondence obligations; two
passes are not redundant merely because both traverse expressions. A useful
candidate supplies an explicit equality/invariant and an exact removed-operation
count on the retained mathematical input. It must not rely on a borrowed theorem
being true without its certified premise or on opaque proofs being unfolded.

Prefer one such localized seam over compact transport if it addresses the
current hot path with substantially fewer changed trust/interop boundaries.
Do not collect many speculative micro-optimizations or redo the three seams
already adopted above. Unmapped allocator/memcpy samples alone do not identify
which Value construction is responsible; caller overlap and inlining matter.

## A higher cap needs more than a larger number

The failed current diagnostic already retains **128 segments**. Both the
snapshot custodian and staged host cap their segment vectors at 128; the
snapshot also caps the sum of retained serialized segments at 64 MiB. Raising
cycles alone with po2=18 cannot authorize a 129th segment. A larger-envelope
choice must jointly review at least:

- execution cap, po2 (supported 12..20), actual segment-count bound and final
  capsule size, not only elapsed runtime;
- larger proving-unit memory/CPU when po2 rises; fewer larger segments are not
  free, and no cost follows by linearly scaling this failed prefix;
- all segment proofs required by finish, complete capsule/parent/checkpoint
  reads within 512 MiB, and the full 3s+m stage graph/retention budget;
- one explicit terminal decision on another refusal, without an automatic
  cap ladder, unchanged retry or disposal of failed costs.

Changing cycle/po2 parameters need not change A if the same guest is used, but
it changes the host session binding and capsule. These partial segment files
are not an execution-resume API. A fresh successful run would be an information/
integration investment and could enable the existing genuine-A producer path;
it would not retrospectively pass the original efficiency gate.

## Recommended decision rule

Finish the exact-current offline attribution first, while pricing these three
bounded options from source. Then make **one** root decision:

1. If a clearly localized removable representation cost is supported, select
   that equality-preserving seam and its changed-boundary checks.
2. If lexical JSON work is the consequential remaining target and the expanded
   bounds/native-host migration still justify it, select the compact Value
   transport work as one coherent native/guest change, not guest-only work.
3. If neither small change has a defensible benefit argument, choose explicitly
   between a joint higher-envelope completion investment and holding proof
   funding pending a deeper representation decision. Do not silently convert
   absence of a cheap optimization into permission for another execution.

Do not force another image change merely to preserve the same failed cap, and
do not claim all options have been exhausted from symbol samples. The next
selection should minimize uncertainty about completing a genuinely reusable
certificate at justified total cost. None selects new experiments by this memo.

## Exact explicit-clone census and decision

The narrow copying seam is now quantified from the current retained input,
not estimated from `memcpy` samples. Read-only PowerShell decoded the exact
`DMKNAI02` frames from
`experiments/v5-local-checks/bounded-parse-aggregate-snapshot-01/evidence/wire.bin`
(215,540 B; SHA-256
`aeddcc517ac61bc14d93e66abe099b73d4167a2ef26f1ef0363d44ddb39aed1e`).
The wire has one assumption, one frontier, two deltas and one target; frame
lengths are 113,220 and 101,687 B, with exact EOF. The independently retained
native report concerns the same mathematics with the earlier aggregate-image
slot; this read neither executes the relation nor establishes a certificate.

Count one abstract Value node per JSON value, including arrays/objects; count
UTF-8 payload bytes in string values and object keys, without punctuation,
capacity, allocation headers or implementation-dependent Value layout. The
walk totals 15,576 + 14,282 = 29,858 nodes, matching the retained native census.
It uses decoded contents, not PowerShell reserialization as canonical bytes.

| Subtrees copied once | Delta 0 | Delta 1 | Both: Value nodes | Both: UTF-8 payload bytes |
|---|---:|---:|---:|---:|
| Imported group descriptors | 11 groups / 2,150 nodes | 12 groups / 2,424 nodes | 4,574 | 13,618 |
| Local group descriptors | 1 group / 274 nodes | 1 group / 337 nodes | 611 | 1,951 |
| Used body expressions | 11 bodies / 4,755 nodes | 11 bodies / 4,755 nodes | 9,510 | 18,200 |

Imported totals comprise 1,790 arrays, 89 objects, 2,159 string values,
316 object keys, 11,471 string bytes and 2,147 key bytes. Body expressions
comprise 4,030 arrays, no objects and 4,366 string values. Cloning the 22
`BodyOpening` structures additionally copies 22 digest strings = 1,408 B;
their integer fields and wrapper storage are not included in Value-node counts.

The exact source seams are different investments:

- `commitments::verify_opening` currently clones each authenticated imported
  descriptor, and `module_relation::check_bound` clones it again into bindings.
  Consuming `imports` in its existing BTreeMap order can remove **only the
  second** copy: 4,574 node clones / 13,618 payload B for a completed input.
  The map is not used afterward; `parents` remains separate. All duplicate,
  count, commitment, order and derived-role checks must remain unchanged.
- The selected `modules/native/proof_validation/module_correspondence.rs`
  clones each used body into returned `body_hash_obligations`; this relation
  subsequently reads only the vector length after authenticating original
  bodies. A distinct checked-used-count or borrowed-result path can remove
  9,510 expression-node clones / 19,608 payload B including digests. It must
  preserve the exact used-key set, missing/duplicate-body checks and unused-body
  refusal. Existing public consumers may still need owned obligations. This
  is a correspondence API/checker-crate change, not just a one-line relation
  move; the existing retained checker artifact cannot be reused unchanged.
- Removing the first imported copy or local-descriptor copies needs additional
  borrowing/ownership changes. These are not counted in the narrow recommendation.

Together the two stated removals eliminate 14,084 abstract node clones and
33,226 UTF-8 payload B, plus their container storage, in a **completed**
two-delta relation evaluation. This is an exact source-operation count, not
a RISC-V heap, instruction, cycle or wall-time estimate. The old explicit
sites collectively copy 19,269 Value nodes (two imported copies, one local
copy, one body copy); other constructions are deliberately outside this census.

Root's exact-current-image attribution
`bounded-parse-pc-attribution-01/attribution/RESULT.json` (SHA-256
`9f100a3f56f7645938fae6eb46803d6d742ddbb7cccfdc1070a58c0ae37f893f`)
contains 14,620 stored `memcpy` labels, but provides no caller attribution to
these clones. Body-obligation clones occur only **after** correspondence;
they need not have been reached in the capped prefix. Neither the operation
counts nor sampled labels establish that their removal permits completion.

**Decision:** do not select another image/build solely for these clones. They
are genuine avoidable work, but the larger repeated proof-DAG syntax traversal
is the better next discrimination target. This is a rejection of the cloning
seam as the immediate investment, not a claim that copying is costless. No clone
implementation, benchmark, host rebuild or renewed execution is selected here.

## Focused independent controls for the proposed proof-syntax memo

Source-only control design, following root's next candidate: memoize successful
syntax validation within **one** theorem-proof invocation. This does not
memoize mathematical truth, committed expressions, body correspondence or
native checking. The unchanged validator is the differential oracle. No test
file, compiler, guest execution or test campaign is selected by this section.

For immutable context `K = (Inventory, owner, ordered universe parameters)`,
a successful entry for an expression or universe-level index records exact
unfolded visit cost `c >= 1` and maximum relative visit depth `h >= 0`.
Expression and level keys are separate; level 0 is a visited zero-level node,
not a missing entry. A hit can skip traversal only if checked arithmetic proves
`work + c <= MAX_NODES` and `depth + h <= MAX_DEPTH`; then it charges exactly
`c`. If either bound does not fit, follow the original visit/check order until
the original first failure. Insert an entry only after successful validation.
The memo must die before owner, universe parameters or Inventory can change.

The observation to preserve is either success with identical final `work`,
or the same first failure diagnostic and same logical visit count at failure.
Physical parser/string/reference work may decrease; logical resource work may
not. Tests must not compare native instruction count or allocation timing as
though they were part of that equivalence.

| Changed boundary | Small targeted control and expected observation |
|---|---|
| Shared DAG compression | Let `E0 = bvar(0)` and `E(j+1) = app(Ej, Ej)`. Baseline visits are `2^(j+1)-1` although only `j+1` expression nodes exist. For an accepted bounded instance, memo success must have the identical logical work while successful syntax evaluation is reused. Include sharing of levels through repeated `sort`/constant arguments, with expression index 0 and level index 0 both reachable, to detect mixed-domain keys. |
| Work-bound fallback | Warm a valid shared sub-DAG within the same proof. Arrange entry states where its exact cost reaches `MAX_NODES` and where it exceeds the remainder by one. The first must succeed exactly at the limit; the second must take fallback and fail at the original visit with `CORRESPONDENCE_EXPANSION_LIMIT` and `work = MAX_NODES + 1`, not charge the entire subtree before failing. |
| Depth at another occurrence | Reach the same valid subtree shallowly, then through a deeper path. Choose a depth where `depth + h = MAX_DEPTH` and a separate case exceeding it by one. A cache hit must not conceal the latter failure; shallow validity does not certify all calling depths. Include a level descendant so height is not computed over expression edges alone. |
| Context reset | First validate a proof containing a bound universe parameter, then validate the same numeric expression/level indices under different ordered parameters where that name is absent. The second must still refuse with `CORRESPONDENCE_UNBOUND_UNIVERSE`. A separate fresh Inventory reusing numeric indices with an invalid reference must not inherit success. Owner/context changes require a fresh memo even where both owner-relative references happen to be syntactically valid. |
| Unreachable malformed syntax | Add a structurally enumerable expression row with invalid expression payload that is unreachable from this proof, and compare old/new syntax-helper outcomes. Do not eagerly prevalidate all expression/level payloads to populate the memo. Separately making that row reachable must recover its original failure. This does not waive later parser/kernel rejection of unused rows or Inventory's existing eager row/name checks. |
| First diagnostic and prefix | Use an `app`/`letE` whose earlier child exhausts the logical visit budget and whose later child is malformed: limit failure must remain first. Reverse their order to make malformed syntax first. Also exercise `const`, where universes are checked before the reference, and `proj`, where reference checks precede its child. A cached completed sibling must charge its full old work before the unchanged remaining prefix. |

These six boundary groups are not six new full proof campaigns. Minimal
in-module differential fixtures can cover them together, followed by only the
actual changed native relation input if separately selected. Do not repeat all
12 historical groups solely to inflate counts. Under first-failure fallback,
an invalid input may still require substantial old traversal; the optimization
must not claim linear worst-case rejection cost. Any retained-input reuse count
from the base lane must distinguish logical visits from newly avoided physical
revalidation and from untouched committed-expression/native checking work.

## 2026-10-16 resumed independent memo-control source checkpoint

The interrupted source assignment left
`software/v5/modules/native/proof_memo/correspondence_controls.rs` written,
but no compiler/control execution or outcome. Its exact 18,660 B SHA-256 is
`94907f917ae2d59542f492de8fc08fbc291023dac1de4a34bda67e03fe6c7917`.
Read-only review on resumption retains this source unchanged. The source
author must supply the separate correspondence implementation and wrapper;
this checkpoint is not a compilation or test PASS.

Tests call unchanged-signature private wrappers
`Inventory::validate_expression(owner, index, parameters, depth)` and
`validate_level(index, parameters, depth)`, each with a fresh per-proof memo.
They compare against unchanged `expression()`/`level()` for semantic panic
payload and final logical `Inventory.work`. Required test-only cumulative
`usize` Inventory counters are `syntax_expression_expansions`,
`syntax_level_expansions`, `syntax_cache_hits`, `syntax_skipped_visits`;
initialize them to zero and omit them from production builds. Expansions count
uncached/fallback bodies in the respective domain; skipped visits charge the
entire successfully skipped logical subtree, not just saved child visits.
The memo lifetime resets between proofs, while work and test counters do not.

Exactly nine `#[test]` names, all under
`module_correspondence::correspondence_controls::`:

1. `all_constructors_and_separate_index_domains_match`
2. `shared_dags_reduce_revalidation_without_discounting_work`
3. `cache_hit_work_bound_falls_back_at_original_visit`
4. `deeper_cache_occurrence_preserves_failed_descendant_and_mixed_height`
5. `malformed_shared_children_do_not_become_successful_memo_entries`
6. `fresh_proof_context_and_inventory_preserve_cumulative_work`
7. `cached_sibling_preserves_first_error_and_logical_prefix`
8. `unreachable_payload_scope_and_eager_inventory_checks_are_unchanged`
9. `retained_two_delta_proofs_match_and_reduce_syntax_work`

The retained-data control requires environment `DMKN_PROOF_MEMO_WIRE` set to
the immutable current wire named above; root's outer selection must pin its
full SHA-256. The test bounds reading to 215,541 B and requires exact 215,540 B,
the selected fixed framing/counts, both expected frame lengths and exact EOF.
It uses serde-only test-local extraction, not project/native/receipt imports.
It finds each new theorem after the 413-row foundation prefix, derives its
owner from the native structured name and parameters from `levelParams`.
Expected root/name pairs are `(1200, 101)` and `(852, 105)`. The source assertion
targets are 18,796/184 unchanged logical visits and 459+14/85+8 actual expression
plus level expansions, respectively. The two structured stdout records will
explicitly deny mathematical admission, kernel execution and a cycle-cost claim.

Synthetic controls first populate successful entries **within the same proof**,
then make an occurrence fail its work/depth guard. Mixed `sort -> succ -> zero`
paths check expression-to-level height as well as same-domain depth. Shared
subtrees at the exact resource boundary must succeed; exceeding it by one must
fall back to the original first failed visit, not reject at the cached root.
Malformed shared nodes, reordered failures, changed universe/owner contexts,
new Inventories with reused numeric indices and cumulative work after caught
failures are covered without rerunning the old twelve unrelated control groups.

No new runtime, compile, guest, proof, larger envelope or Git action was taken
by this lane. Root still owns source adoption, finite selection and execution.

### Independent pre-selection control review, 2026-10-16

The nine-test source above was read against the frozen `proof_validation`
`expression`/`level` oracle and current `bounded_parse/aggregate_relation.rs`
plus `aggregate_claims/wire.rs`. No concrete test defect was found, so its
18,660 B hash `94907f91...` remains unchanged. The fixed wire extraction follows
the real v2 field order: 625 fixed-prefix bytes plus two 4-byte frame lengths
and 113,220/101,687-byte frames equals exactly 215,540 B. It does not interpret
the skipped journal/image fields as authenticated authority.

Source reasoning confirms the synthetic exact-boundary and first-failure visit
counts, including mixed expression/level depth, malformed constant levels
before name lookup, and projection name lookup before its index/child. The
counter contract is unchanged: successful skipped subtrees charge their entire
logical cost, fresh top-level calls discard memo entries, and Inventory work
and test-only counters remain cumulative. Review is ready for root's exact
source selection, not a claim that compilation or the nine controls passed.
No test, inventory recount, compiler, guest, proof or Git operation was run.
