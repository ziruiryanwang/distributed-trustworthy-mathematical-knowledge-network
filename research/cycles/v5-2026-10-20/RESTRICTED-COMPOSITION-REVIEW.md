# Independent review: restricted composition and the existing commons

2026-10-21. Reviewer: core_release. Source/data review only; no product imports,
build, native execution, proof attempt or Git mutation.

Reviewed decision: `RESTRICTED-COMPOSITION-DECISION.md`, SHA-256 prefix
`324f42c1`, as assigned by root. Current SDK source identities were resolved
through `distribution-terminal-i-01-input.json`; its old atomic/import sources
are superseded only by the explicitly selected continuing-context successors.
In particular, current runtime is `trust_withdrawal/client/runtime.py`, aggregate
admission is `trust_withdrawal/aggregate_claims/aggregate_admission.py`, and terminal
evidence is `terminal_i/{client,evidence_network}`. Older similarly named files
are not the integrated selection.

## Disposition

**The architecture can remove actual checking work while retaining ordinary
module reuse. The broad proposed beta/zeta fragment is not yet an established
refinement of the fixed-I conditional relation.** Select only a small
structural-conversion/application-spine successor after the constructive
refinement fixes its exact accepted grammar and witness bounds. Do not select
the broad fragment, a proof campaign, or an I/A profile reinterpretation merely
from this architectural pass.

This is not another representation optimization: the candidate replaces the
production call to `module_relation::check` for a precisely tagged class of
new deltas. Conversely, accepting a generic RC Boolean and then retaining all
old native work would provide no such saving. The replacement needs its own
sound implementation and new adopted aggregate image.

## Actual semantic compatibility

The fixed module journal is 184 bytes (`DMKNM002`, profile 2). It binds the
fixed relation image, foundation, policy, module ID, group root/count and rank.
The module ID hashes the exact summary; group commitments bind the theorem's
name, universe count and exact type. They do not bind its proof witness.
Ordinary theorem descriptors require singleton groups, null `value_hash` and
empty metadata. RC must enforce these fields itself: group commitment code
deliberately leaves some expression/metadata validation to correspondence.

The appropriate refinement statement is not "Lean accepts the same theorem"
alone. For every accepted RC input x, construct an ordinary witness W(x) such
that the fixed-I **conditional** relation returns the same J and the same exact
parent journals. RC then inherits the existing module interpretation. An
independent fixed-I receipt for W(x) need not be produced, and must not be
fabricated. This is already the distinction made by A's semantic members.

In current `aggregate_claims/relation.rs`, each new delta is checked by the
module relation; `Graph::delta` then requires each exact parent journal to
already exist, strict/exact mathematical rank, bounded edges and no duplicate
exact journal. The target-closure check rejects unused frontiers/deltas. The
aggregate receiver verifies the actual adopted image and header, then selects
exact members by a committed membership path. A replacement checker can preserve
all these graph obligations. None of them independently checks a new proof.

The aggregate soundness induction is therefore:

1. Genuine fixed-I receipts establish initial selected J values.
2. A genuine same-A-RC receipt and its membership path establish selected earlier
   J values under the same recursively defined assertion.
3. An accepted RC delta refines a valid old conditional extension under those
   exact J premises; its new J is consequently warranted.
4. The guest verifies every unique pending receipt claim before committing the
   aggregate header. No host transcript or structural opening supplies step 1
   or 2.

Keep old homogeneous-A parents refused until a separately specified image bridge
exists. Their semantic compatibility does not make their receipt image A-RC.

## One concrete refinement obstruction

The decision correctly separates Lean typing soundness from operational
refinement, but its broad proposed input fragment does not yet discharge the
second. The original native checker can seek an imported transparent value
before recognizing a conversion that a small beta/zeta checker can establish
without that value.

In `tc.rs`, `def_eq`/`lazy_delta` and `get_applied_def` may attempt delta unfolding
for an imported abbreviation. `env.rs` deliberately distinguishes a sealed
imported theorem from a missing transparent definition: only the former can be
used without its proof, while demanding the latter's absent value fails. Thus
two applications of the same abbreviation to beta-equal but syntactically
different arguments are not automatically an old-checker-accepted witness with
no body openings. Lean's congruence theorem alone does not prove that this
particular native algorithm succeeds on that witness.

This is not evidence that the restricted inference rules are mathematically
unsound. It is a precise gap in the claimed existing-I operational refinement.
The same issue can arise in ensuring that an inferred type is a sort/function,
not just in the final proof-type comparison. A restriction only on the final
equality is insufficient.

Core_growth independently identified this issue while deriving W(x). Its
proposed repair is a normal application-spine profile whose required conversion
comparisons are structural (with a separately justified binder-alpha treatment),
using the genuine base-I `binary_congr` signature. For the first selection,
require the fragment predicate to cover **every** inference/conversion demand,
not an informal claim that the target "uses no unfolding". The initial target
does not need a nonfoundation inductive group or definition body.

Also preserve old witness bounds, even when W(x) is only a mathematical
construction rather than materialized inside the guest:

- At most 250,000 native rows and 16,384 declarations.
- At most 4,096 combined imported/local groups, with the exact old ordering and
  namespace interpretation.
- At most 250,000 correspondence expansion visits and depth 192. These count
  repeated expansions of shared syntax, not merely distinct DAG nodes.
- Canonical 16 MiB input, node/depth bounds and the actual original parser's
  recursion restrictions. A compact RC input need not imply its old witness
  fits the old input bound.
- Exactly the 413-row adopted foundation prefix in W(x), and correct ordinary
  missing-value tags for imported declarations. New theorems have actual proof
  rows; imported theorems have `moduleImportTheorem`, never arbitrary axioms.

The RC checker need not execute the old row parser to enforce conservative
bounds on a deterministic W(x). It does need a source-supported bound formula
or a bounded counting pass; otherwise the existential refinement is too broad.

## Ordinary-agent integration is available, but producer dispatch is new

| Boundary | Existing implementation | Necessary RC change |
|---|---|---|
| Module/group identity | Existing codec and exact group commitments | No new theorem envelope; enforce the restricted schema and typing fully |
| Aggregate graph/header | Exact J members, ranks, closure, fixed-I or same-image frontiers | New image and explicit RC delta branch; preserve all graph checks |
| Aggregate input census | Parse-once census requires `schema,image,rank,local_spec,rows,parents,bodies` | Distinct versioned RC frame and whole-stream census; do not send RC data to the old parser |
| Receipt production | Existing aggregate receipt/assumption machinery | Coherent new guest/host input preparation and real new-image adoption |
| Receipt/member admission | `AggregateReceiptVerifier` accepts an explicitly adopted aggregate image, never an arbitrary proof flag | Fresh support/trust and installed profile, not a restored old trust token |
| Discovery/acquisition/import | Terminal-A packets, exact member opening, ordinary `LiveWarrant` and `MixedImportSession` already support A members | Configure the new wire image; publish/acquire actual terminal evidence and selected semantics |

The current terminal-A path verifies receipt plus header, selects the exact J,
and returns an `A-member` warrant. `_context_data` routes that warrant through
`use_aggregate_member`; it does not mint `VerifiedModule`. Its selected interfaces
can reach the normal authoring context. The continuing-context successor keeps
the same owners and budgets when a later certified contribution is added.

No theorem proof body is needed for this receiver path. The theorem's declared
type and required selected signature still are. Normal `author` may continue
to use Lean for a new contribution; RC's public preparation path can additionally
accept/produce bounded canonical proof terms. The network need not prescribe a
local agent's proof-search strategy.

The current wire profile binds one aggregate image, and fresh adoption binds
its verifier/support files. Consequently, this is not transparent interoperability
with every existing A workspace. The existing discovery namespace's F/P binding
does not itself authorize a foreign-image receipt. Use fresh compatible state
and explicit profile selection; do not overwrite old workspaces or assume a
cross-image packet offer will pass.

## Payoff: genuine opportunity, not yet a speedup result

The old `modules/receipt/src/relation.rs` always checks the foundation-row
prefix, binds native rows to every selected descriptor, parses native rows,
reconstructs the native environment, and invokes the general local checker.
The RC branch can replace these steps with selected-signature authentication,
restricted typing, exact output commitments and a conservative virtual-witness
bound. A compiled fixed foundation signature avoids mandatory per-delta traversal
of the 413-row native prefix. Its exact correspondence is a new-image assurance
obligation, not caller-supplied data.

Costs that remain include reading selected signatures, hash/Merkle operations,
capture-safe substitution, universe checking, receipt assumptions/resolution,
cryptographic proof production and network services. Charge declaration lookup,
key comparisons, allocation and substitution work too; a high-level expression
visit count alone does not establish a linear implementation-time bound.

Most importantly, the rejected 148-segment FIRST target is an induction workload.
The available binary-congruence target is not that target. Its existing general
path may already be cheap. FIRST's failed screen is **not** comparative evidence
that RC is necessary or profitable for composition. The defensible prediction
is removal of concrete general-checker overhead on one identical composition
target. Fixed po18 prover workspace and cryptographic per-segment work remain.

Prioritize one small checker/dispatcher source slice, not a general-purpose new
kernel. Before expensive proof production, compare the same exact output
descriptor/parents in both lanes under a predeclared envelope. Reuse source
bounds and existing evidence first; if actual instruction cost remains the
decision-changing uncertainty, one inexpensive execution comparison is enough.
Do not replay FIRST or survey RAM. Do not infer full-cost growth from fewer guest
segments or from this review.

## Narrow next selection

Subject to adoption of the constructive refinement, the high-payoff source
selection is:

1. One explicitly restricted typed composition core and deterministic virtual
   old-I witness/counting specification. Initially use the genuine base-I
   `binary_congr` premise and structural conversion obligations, not unrestricted
   beta/zeta underneath missing transparent definitions.
2. One aggregate successor with only fixed-I and own-A-image frontiers, an RC
   frame/census and unchanged exact-J/rank/closure rules. Avoid an old-A bridge
   or a second catalog/protocol.
3. One exact parametric composition plus a successor using its new certified
   member. Verify the second client's normal terminal-A acquisition and import
   path; an isolated RC execution does not establish recursive usable renewal.
4. New-seam negative controls for scope/substitution/universe mistakes, forged
   parent/descriptor, untyped binder, unsupported conversion, budget overflow,
   graph/rank conflict and receipt-kind/image confusion. Existing unchanged
   receipt/network suites need not be rerun.

No proof launch is recommended by this note. A source implementation is a
bounded engineering investment; broad-fragment refinement and economical
certificate production remain separate gates. A successful RC route would be
a reusable capability of the commons, not completion of final v5 by itself.
